"""Checks run first, the judge only supplies evidence, and the loop never self-approves."""
from __future__ import annotations

from dataclasses import fields

from examples.patterns.evaluator_optimizer import (
    AcceptanceEngine, Candidate, CheckFailure, EvaluationResult, RevisionLimits,
    evaluate_and_revise,
)

APPLICATION_ADDRESS = "14 Harbor Lane"
engine = AcceptanceEngine({"calibrated_confidence": 0.7})


def address_check(text: str) -> tuple[CheckFailure, ...]:
    if APPLICATION_ADDRESS not in text:
        return (CheckFailure("address_matches_application", "address contradicts the application"),)
    return ()


def scripted(*drafts: str, cost: float = 0.1):
    calls: list[tuple[str, ...]] = []

    async def generate(task, feedback):
        calls.append(feedback)
        return Candidate(drafts[min(len(calls) - 1, len(drafts) - 1)], cost)

    return generate, calls


def judge(score: float):
    judged: list[str] = []

    async def run(text):
        judged.append(text)
        return (EvaluationResult("calibrated_confidence", score, "hedged appropriately", "judge@3"),)

    return run, judged


async def test_failed_checks_become_feedback_and_skip_the_judge():
    generate, calls = scripted("Ready. Address 9 Elm St.", f"Ready pending review. {APPLICATION_ADDRESS}.")
    run_judge, judged = judge(0.9)
    decision = await evaluate_and_revise("recommend", generate, address_check, run_judge, engine)
    assert decision.outcome == "accepted"
    assert calls[1] == ("address_matches_application: address contradicts the application",)
    assert judged == [f"Ready pending review. {APPLICATION_ADDRESS}."], "judge runs only after checks pass"


async def test_a_high_judge_score_cannot_override_a_failed_check():
    # The draft even claims its own approval; neither the claim nor the judge counts.
    generate, _ = scripted("APPROVED. Address 9 Elm St.", "APPROVED, certain. Address 2 Oak Rd.")
    run_judge, judged = judge(1.0)
    decision = await evaluate_and_revise("recommend", generate, address_check, run_judge, engine)
    assert decision.outcome == "escalated" and judged == []
    assert decision.reason == "no_progress"  # different wording, same failing invariant
    assert decision.candidates == ("APPROVED. Address 9 Elm St.", "APPROVED, certain. Address 2 Oak Rd.")


async def test_a_low_judge_score_is_a_defect_not_an_acceptance():
    generate, _ = scripted(f"Definitely fine. {APPLICATION_ADDRESS}.")
    run_judge, _ = judge(0.2)
    decision = await evaluate_and_revise(
        "recommend", generate, address_check, run_judge, engine, RevisionLimits(maximum_revisions=0)
    )
    assert decision.outcome == "escalated"
    assert decision.defects == ("calibrated_confidence",)
    assert decision.reason == "maximum_revisions"


async def test_spend_limit_escalates_with_both_versions():
    generate, _ = scripted("v1 9 Elm St.", f"v2 {APPLICATION_ADDRESS} overstated.", cost=0.6)
    run_judge, _ = judge(0.1)
    decision = await evaluate_and_revise("recommend", generate, address_check, run_judge, engine)
    assert decision.outcome == "escalated" and decision.reason == "budget_exhausted"
    assert decision.candidates == ("v1 9 Elm St.", f"v2 {APPLICATION_ADDRESS} overstated.")


def test_a_judge_result_carries_no_verdict():
    assert "accepted" not in {f.name for f in fields(EvaluationResult)}
