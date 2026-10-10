"""Eligibility-first routing: the model picks only from what it may use.

The eligible set is computed deterministically before any model sees it. The
model proposes a route and a confidence; the router validates the proposal and
falls back instead of guessing. A route grants no authority: exact authorization
still happens at the Tool Gateway when the chosen specialist acts.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

from examples.contracts import RiskClass


@dataclass(frozen=True)
class Route:
    name: str
    capability: str
    risk_ceiling: RiskClass
    healthy: bool = True

    def __post_init__(self) -> None:
        # Same representation as the shared contracts: R0-R4, never a bare number.
        if not isinstance(self.risk_ceiling, RiskClass):
            raise TypeError("risk_ceiling must be a RiskClass (R0-R4)")


@dataclass(frozen=True)
class RouteProposal:
    """What the classifier model returns. It is a proposal, not a decision."""

    route: str
    confidence: float
    reason: str


@dataclass(frozen=True)
class RoutingDecision:
    route: str
    fallback: bool
    reason: str
    eligible: tuple[str, ...]


# The classifier sees the request and the eligible route names, nothing else.
Classifier = Callable[[str, tuple[str, ...]], Awaitable[RouteProposal]]

# --8<-- region:router
class DeterministicRouter:
    """Eligibility first, model proposal second, deterministic validation last."""

    def __init__(
        self, routes: tuple[Route, ...], fallback: str, threshold: float = 0.8
    ) -> None:
        self.routes = routes
        self.fallback = fallback  # e.g. a human triage queue; always available
        self.threshold = threshold

    def eligible(
        self, allowed_capabilities: frozenset[str], risk: RiskClass
    ) -> tuple[Route, ...]:
        return tuple(
            route for route in self.routes
            if route.capability in allowed_capabilities
            and risk <= route.risk_ceiling
            and route.healthy
        )

    async def route(
        self,
        request: str,
        classify: Classifier,
        allowed_capabilities: frozenset[str],
        risk: RiskClass,
    ) -> RoutingDecision:
        names = tuple(r.name for r in self.eligible(allowed_capabilities, risk))
        if not names:
            return RoutingDecision(self.fallback, True, "no_eligible_route", names)
        proposal = await classify(request, names)
        if proposal.route not in names:
            # Selecting a route is never authorization: outside the set, fall back.
            return RoutingDecision(self.fallback, True, "not_eligible", names)
        if proposal.confidence < self.threshold:
            return RoutingDecision(self.fallback, True, "low_confidence", names)
        return RoutingDecision(proposal.route, False, proposal.reason, names)

# --8<-- endregion:router
