"""Deterministic reflection and acceptance contract tests."""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from pydantic import ValidationError

from mortgage_case.domain.errors import ProposalRejected
from mortgage_case.platform.reflection_acceptance import (
    Candidate,
    CandidateClaim,
    Critique,
    evaluate_acceptance,
)


_KNOWN_FACTS = {
    ("monthly_income", "income-verified"): "6000",
    ("policy_status", "policy-current"): "active",
}


def _candidate(
    *,
    evidence_refs: tuple[str, ...] = ("income-verified", "policy-current"),
    claims: tuple[CandidateClaim, ...] = (),
) -> Candidate:
    return Candidate(
        candidate_id="candidate-1",
        producer_id="agent-producer",
        evidence_refs=evidence_refs,
        claims=claims,
    )


def _critique(
    *, candidate_id: str = "candidate-1", critic_id: str = "independent-critic", findings: tuple[str, ...] = ()
) -> Critique:
    return Critique(candidate_id=candidate_id, critic_id=critic_id, findings=findings)


def _evaluate(
    candidate: Candidate,
    critique: Critique,
    *,
    known: tuple[str, ...] | None = ("income-verified", "policy-current"),
    required: tuple[str, ...] = ("income-verified", "policy-current"),
    actor: str = "human-approver",
    known_facts: Mapping[tuple[str, str], str] | None = None,
):
    return evaluate_acceptance(
        candidate=candidate,
        critique=critique,
        known_evidence_refs=known,
        required_evidence_refs=required,
        acceptance_actor_id=actor,
        known_facts=_KNOWN_FACTS if known_facts is None else known_facts,
    )


def test_accepts_candidate_with_supported_required_evidence_and_clear_independent_critique():
    claims = (
        CandidateClaim(field_name="monthly_income", value="6000", evidence_ref="income-verified"),
        CandidateClaim(field_name="policy_status", value="active", evidence_ref="policy-current"),
    )
    result = _evaluate(_candidate(claims=claims), _critique(), known=None)

    assert result.accepted is True
    assert result.candidate_id == "candidate-1"
    assert result.reasons == ()
    assert len(result.checks) == 8
    assert all(check.passed for check in result.checks)


def test_rejects_candidate_without_claims_and_claim_values_must_be_nonempty():
    candidate = _candidate()

    result = _evaluate(candidate, _critique())

    assert candidate.claims == ()
    assert result.accepted is False
    claims_check = next(check for check in result.checks if check.name == "candidate_claims_present")
    assert claims_check.passed is False
    assert claims_check.reason == "candidate_claims_missing"

    with pytest.raises(ValidationError):
        CandidateClaim(field_name="monthly_income", value="", evidence_ref="income-verified")


def test_rejects_claim_contradicting_authoritative_fact_with_empty_critique():
    candidate = _candidate(
        claims=(
            CandidateClaim(field_name="monthly_income", value="9000", evidence_ref="income-verified"),
        )
    )

    result = _evaluate(candidate, _critique(findings=()), known=None)

    assert result.accepted is False
    claims_check = next(check for check in result.checks if check.name == "candidate_claims_match_known_facts")
    assert claims_check.passed is False
    assert claims_check.reason == "candidate_claims_contradict_evidence"
    assert claims_check.details == ("monthly_income@income-verified",)
    assert result.reasons == ("candidate_claims_contradict_evidence",)


def test_rejects_claim_without_an_authoritative_source_fact():
    candidate = _candidate(
        claims=(CandidateClaim(field_name="monthly_income", value="6000", evidence_ref="income-verified"),)
    )

    result = _evaluate(candidate, _critique(), known_facts={})

    assert result.accepted is False
    source_check = next(check for check in result.checks if check.name == "candidate_claim_source_facts_present")
    assert source_check.passed is False
    assert source_check.reason == "candidate_claim_source_fact_missing"
    assert source_check.details == ("monthly_income@income-verified",)


@pytest.mark.parametrize(
    ("evidence_refs", "known", "expected_reason", "expected_details", "expected_reasons"),
    [
        ((), (), "candidate_evidence_missing", (), ("candidate_evidence_missing", "candidate_claims_missing")),
        (
            ("income-verified", "unregistered"),
            ("income-verified",),
            "unsupported_evidence_refs",
            ("unregistered",),
            ("unsupported_evidence_refs", "candidate_claims_missing"),
        ),
    ],
)
def test_rejects_empty_or_unsupported_candidate_evidence(
    evidence_refs: tuple[str, ...],
    known: tuple[str, ...],
    expected_reason: str,
    expected_details: tuple[str, ...],
    expected_reasons: tuple[str, ...],
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
    assert result.reasons == expected_reasons


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
    check = next(check for check in result.checks if check.name == "critique_findings_empty")
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
