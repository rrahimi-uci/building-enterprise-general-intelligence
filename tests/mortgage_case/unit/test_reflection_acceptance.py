"""Deterministic reflection and acceptance contract tests."""

from __future__ import annotations

import pytest

from mortgage_case.domain.errors import ProposalRejected
from mortgage_case.platform.reflection_acceptance import (
    Candidate,
    Critique,
    evaluate_acceptance,
)


def _candidate(*, evidence_refs: tuple[str, ...] = ("income-verified", "policy-current")) -> Candidate:
    return Candidate(
        candidate_id="candidate-1",
        producer_id="agent-producer",
        evidence_refs=evidence_refs,
    )


def _critique(
    *, candidate_id: str = "candidate-1", critic_id: str = "independent-critic", findings: tuple[str, ...] = ()
) -> Critique:
    return Critique(candidate_id=candidate_id, critic_id=critic_id, findings=findings)


def _evaluate(
    candidate: Candidate,
    critique: Critique,
    *,
    known: tuple[str, ...] = ("income-verified", "policy-current"),
    required: tuple[str, ...] = ("income-verified", "policy-current"),
    actor: str = "human-approver",
):
    return evaluate_acceptance(
        candidate=candidate,
        critique=critique,
        known_evidence_refs=known,
        required_evidence_refs=required,
        acceptance_actor_id=actor,
    )


def test_accepts_candidate_with_supported_required_evidence_and_clear_independent_critique():
    result = _evaluate(_candidate(), _critique())

    assert result.accepted is True
    assert result.candidate_id == "candidate-1"
    assert result.reasons == ()
    assert len(result.checks) == 5
    assert all(check.passed for check in result.checks)


@pytest.mark.parametrize(
    ("evidence_refs", "known", "expected_reason", "expected_details"),
    [
        ((), (), "candidate_evidence_missing", ()),
        (("income-verified", "unregistered"), ("income-verified",), "unsupported_evidence_refs", ("unregistered",)),
    ],
)
def test_rejects_empty_or_unsupported_candidate_evidence(
    evidence_refs: tuple[str, ...],
    known: tuple[str, ...],
    expected_reason: str,
    expected_details: tuple[str, ...],
):
    result = _evaluate(
        _candidate(evidence_refs=evidence_refs),
        _critique(),
        known=known,
        required=(),
    )

    assert result.accepted is False
    check = result.checks[0]
    assert check.passed is False
    assert check.reason == expected_reason
    assert check.details == expected_details
    assert result.reasons == (expected_reason,)


def test_rejects_when_a_required_evidence_reference_is_missing():
    result = _evaluate(
        _candidate(evidence_refs=("income-verified",)),
        _critique(),
        known=("income-verified", "policy-current"),
        required=("income-verified", "policy-current"),
    )

    assert result.accepted is False
    check = result.checks[1]
    assert check.passed is False
    assert check.reason == "required_evidence_refs_missing"
    assert check.details == ("policy-current",)


def test_rejects_candidate_with_unresolved_critique_findings():
    result = _evaluate(_candidate(), _critique(findings=("income figure conflicts with source",)))

    assert result.accepted is False
    check = result.checks[3]
    assert check.passed is False
    assert check.reason == "critique_findings_unresolved"
    assert check.details == ("income figure conflicts with source",)


def test_raises_stable_rejection_for_critique_bound_to_another_candidate():
    with pytest.raises(ProposalRejected) as exc_info:
        _evaluate(_candidate(), _critique(candidate_id="candidate-2"))

    assert exc_info.value.code == "CRITIQUE_CANDIDATE_MISMATCH"


def test_raises_stable_rejection_when_critic_is_candidate_producer():
    with pytest.raises(ProposalRejected) as exc_info:
        _evaluate(_candidate(), _critique(critic_id="agent-producer"))

    assert exc_info.value.code == "CRITIC_NOT_INDEPENDENT"


def test_raises_stable_rejection_when_candidate_producer_attempts_acceptance():
    with pytest.raises(ProposalRejected) as exc_info:
        _evaluate(_candidate(), _critique(), actor="agent-producer")

    assert exc_info.value.code == "SELF_APPROVAL"
