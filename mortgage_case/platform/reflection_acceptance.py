"""Deterministic critique and acceptance contracts for synthetic candidates."""

from __future__ import annotations

from collections.abc import Collection
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from mortgage_case.domain.errors import ProposalRejected


AcceptanceCheckName = Literal[
    "candidate_evidence_refs_supported",
    "required_evidence_refs_present",
    "critique_matches_candidate",
    "critique_findings_empty",
    "acceptance_actor_independent",
]


class Candidate(BaseModel):
    """A proposed result with a stable producer and explicit evidence lineage."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    candidate_id: str = Field(min_length=1)
    producer_id: str = Field(min_length=1)
    evidence_refs: tuple[str, ...]


class Critique(BaseModel):
    """An independent review tied to one candidate identifier."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    candidate_id: str = Field(min_length=1)
    critic_id: str = Field(min_length=1)
    findings: tuple[str, ...] = ()


class AcceptanceCheck(BaseModel):
    """One deterministic hard check and its machine-readable failure reason."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    name: AcceptanceCheckName
    passed: bool
    reason: str | None = None
    details: tuple[str, ...] = ()

    @model_validator(mode="after")
    def reason_matches_result(self) -> AcceptanceCheck:
        if self.passed and self.reason is not None:
            raise ValueError("a passing check cannot have a failure reason")
        if not self.passed and self.reason is None:
            raise ValueError("a failing check must have a failure reason")
        return self


class AcceptanceResult(BaseModel):
    """Computed acceptance outcome, checks, and stable rejection reasons."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str
    accepted: bool
    checks: tuple[AcceptanceCheck, ...]
    reasons: tuple[str, ...]

    @model_validator(mode="after")
    def outcome_matches_checks(self) -> AcceptanceResult:
        check_reasons = tuple(check.reason for check in self.checks if check.reason is not None)
        if self.accepted != all(check.passed for check in self.checks):
            raise ValueError("accepted must equal the result of all hard checks")
        if self.reasons != check_reasons:
            raise ValueError("reasons must match failed hard checks in check order")
        return self


def evaluate_acceptance(
    *,
    candidate: Candidate,
    critique: Critique,
    known_evidence_refs: Collection[str],
    required_evidence_refs: Collection[str],
    acceptance_actor_id: str,
) -> AcceptanceResult:
    """Evaluate the candidate against evidence and independent-review contracts.

    Candidate/critique binding, critic independence, and separation from the
    candidate producer are authorization boundaries and raise stable proposal
    rejection codes. Evidence completeness and unresolved findings instead
    produce an explicit rejected result with failed checks.
    """

    if critique.candidate_id != candidate.candidate_id:
        raise ProposalRejected(
            "CRITIQUE_CANDIDATE_MISMATCH",
            "critique is not bound to the submitted candidate",
        )
    if critique.critic_id == candidate.producer_id:
        raise ProposalRejected(
            "CRITIC_NOT_INDEPENDENT",
            "candidate producer cannot critique their own candidate",
        )
    if acceptance_actor_id.strip() == candidate.producer_id:
        raise ProposalRejected(
            "SELF_APPROVAL",
            "candidate producer cannot accept their own candidate",
        )

    candidate_refs = frozenset(candidate.evidence_refs)
    known_refs = frozenset(known_evidence_refs)
    required_refs = frozenset(required_evidence_refs)
    unsupported_refs = tuple(sorted(candidate_refs - known_refs))
    missing_refs = tuple(sorted(required_refs - candidate_refs))

    evidence_supported = bool(candidate.evidence_refs) and not unsupported_refs
    evidence_reason = None
    evidence_details: tuple[str, ...] = ()
    if not candidate.evidence_refs:
        evidence_reason = "candidate_evidence_missing"
    elif unsupported_refs:
        evidence_reason = "unsupported_evidence_refs"
        evidence_details = unsupported_refs

    checks = (
        AcceptanceCheck(
            name="candidate_evidence_refs_supported",
            passed=evidence_supported,
            reason=evidence_reason,
            details=evidence_details,
        ),
        AcceptanceCheck(
            name="required_evidence_refs_present",
            passed=not missing_refs,
            reason=None if not missing_refs else "required_evidence_refs_missing",
            details=missing_refs,
        ),
        AcceptanceCheck(name="critique_matches_candidate", passed=True),
        AcceptanceCheck(
            name="critique_findings_empty",
            passed=not critique.findings,
            reason=None if not critique.findings else "critique_findings_unresolved",
            details=critique.findings,
        ),
        AcceptanceCheck(name="acceptance_actor_independent", passed=True),
    )
    reasons = tuple(check.reason for check in checks if check.reason is not None)
    return AcceptanceResult(
        candidate_id=candidate.candidate_id,
        accepted=all(check.passed for check in checks),
        checks=checks,
        reasons=reasons,
    )
