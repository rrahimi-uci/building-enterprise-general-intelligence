"""A bounded evaluator-optimizer that cannot approve its own work.

Executable checks run first and become structured feedback. A judge returns a
score and a rationale -- evidence, never a verdict. Only the acceptance engine
issues an AcceptanceDecision, and when the loop runs out of revisions, spend, or
progress it escalates with both candidate versions instead of raising.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Awaitable, Callable, Literal


@dataclass(frozen=True)
class CheckFailure:
    invariant: str  # e.g. "address_matches_application"
    detail: str


@dataclass(frozen=True)
class EvaluationResult:
    """One judge score. Deliberately has no 'accepted' field."""

    criterion: str
    score: float
    rationale: str
    evaluator: str  # judge identity and version, recorded with the score


@dataclass(frozen=True)
class Candidate:
    text: str
    cost_usd: float


@dataclass(frozen=True)
class AcceptanceDecision:
    outcome: Literal["accepted", "rejected", "escalated"]
    defects: tuple[str, ...]
    candidates: tuple[str, ...]  # the accepted text, or both versions on escalation
    reason: str = ""


Generator = Callable[[str, tuple[str, ...]], Awaitable[Candidate]]
Checks = Callable[[str], tuple[CheckFailure, ...]]
Judge = Callable[[str], Awaitable[tuple[EvaluationResult, ...]]]

# --8<-- region:core
class AcceptanceEngine:
    """The only component that may accept. Checks decide; scores are evidence."""

    def __init__(self, thresholds: dict[str, float]) -> None:
        self.thresholds = thresholds  # every criterion here must be scored to accept

    def decide(
        self, candidate: str, failures: tuple[CheckFailure, ...],
        scores: tuple[EvaluationResult, ...],
    ) -> AcceptanceDecision:
        defects = tuple(f.invariant for f in failures)
        if not defects:  # judge evidence counts only once every executable check passes
            scored = {s.criterion: s.score for s in scores}
            defects = tuple(
                criterion for criterion in dict.fromkeys((*self.thresholds, *scored))
                if not math.isfinite(scored.get(criterion, math.nan))  # missing or NaN
                or scored[criterion] < self.thresholds.get(criterion, 1.0)
            )
        if defects:
            return AcceptanceDecision("rejected", defects, (candidate,))
        return AcceptanceDecision("accepted", (), (candidate,))

    def escalate(
        self, previous: str, current: str, defects: tuple[str, ...], reason: str
    ) -> AcceptanceDecision:
        return AcceptanceDecision("escalated", defects, (previous, current), reason)


@dataclass(frozen=True)
class RevisionLimits:
    """Spend is checked before acceptance and before every further call. A call's
    cost is known only afterwards, so the last call can overrun the cap by its own
    cost; that overrun escalates to a person instead of being accepted."""

    maximum_revisions: int = 2
    maximum_cost_usd: float = 1.0


async def evaluate_and_revise(
    task: str, generate: Generator, checks: Checks, judge: Judge,
    engine: AcceptanceEngine, limits: RevisionLimits = RevisionLimits(),
) -> AcceptanceDecision:
    feedback: tuple[str, ...] = ()
    previous: str | None = None
    previous_defects: tuple[str, ...] | None = None
    spent = 0.0
    for revision in range(limits.maximum_revisions + 1):
        candidate = await generate(task, feedback)
        spent += candidate.cost_usd
        failures = checks(candidate.text)            # executable invariants first
        scores = () if failures else await judge(candidate.text)  # qualitative only
        decision = engine.decide(candidate.text, failures, scores)
        prior = previous if previous is not None else candidate.text
        if spent > limits.maximum_cost_usd:          # over the cap: never accept, surface it
            return engine.escalate(prior, candidate.text, decision.defects, "budget_exhausted")
        if decision.outcome == "accepted":
            return decision
        if decision.defects == previous_defects:     # new wording, same failure
            return engine.escalate(prior, candidate.text, decision.defects, "no_progress")
        if spent >= limits.maximum_cost_usd:         # nothing left for another call
            return engine.escalate(prior, candidate.text, decision.defects, "budget_exhausted")
        if revision == limits.maximum_revisions:
            return engine.escalate(prior, candidate.text, decision.defects, "maximum_revisions")
        feedback = tuple(f"{f.invariant}: {f.detail}" for f in failures) + tuple(
            f"{s.criterion}: {s.rationale}" for s in scores
        )
        previous, previous_defects = candidate.text, decision.defects
    raise AssertionError("unreachable: the last revision always returns")

# --8<-- endregion:core
