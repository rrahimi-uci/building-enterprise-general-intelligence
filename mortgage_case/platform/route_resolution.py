"""Deterministic resolution of eligible routing candidates."""

from __future__ import annotations

from collections.abc import Sequence

from ..domain.errors import ProposalRejected
from .enterprise import RouteDecision


def resolve_route(candidates: Sequence[RouteDecision]) -> RouteDecision:
    """Return the sole eligible candidate with the highest confidence.

    Candidate order never breaks a tie: equal top confidence is ambiguous and
    must be resolved by the caller before ownership is transferred.
    """

    eligible = tuple(candidate for candidate in candidates if candidate.eligible)
    if not eligible:
        raise ProposalRejected("NO_ELIGIBLE_ROUTE", "no eligible route candidate was available")
    if any(not candidate.confidence.is_finite() or not 0 <= candidate.confidence <= 1 for candidate in eligible):
        raise ProposalRejected("ROUTE_SCORE_INVALID", "route confidence must be finite and within [0, 1]")

    highest_confidence = max(candidate.confidence for candidate in eligible)
    winners = tuple(candidate for candidate in eligible if candidate.confidence == highest_confidence)
    if len(winners) != 1:
        raise ProposalRejected("ROUTE_AMBIGUOUS", "multiple eligible routes share the highest confidence")

    return winners[0]
