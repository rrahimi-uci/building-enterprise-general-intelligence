from datetime import timedelta

import pytest
from pydantic import ValidationError

from mortgage_case.domain.errors import ProposalRejected
from mortgage_case.platform.enterprise import (
    NOW,
    ApprovalDecision,
    ApprovalRequest,
    digest,
    proposal_hash,
    verify_approval,
)


CASE_ID = "CASE-APPROVAL-BINDING"
CASE_VERSION = 7
POLICY_VERSION = "mortgage-policy@2026.09"
REQUIRED_ROLE = "underwriter"
EXPIRES_AT = NOW + timedelta(minutes=15)
EVIDENCE = {
    "documents": [
        {"document_id": "DOC-1", "content_hash": "sha256:original"},
    ]
}


def _approved_pair() -> tuple[ApprovalRequest, ApprovalDecision, str]:
    evidence_snapshot_digest = digest(EVIDENCE)
    action = "underwriting.mark_ready"
    resource = f"mortgage://case/{CASE_ID}"
    proposal_arguments = {
        "case_id": CASE_ID,
        "policy_version": POLICY_VERSION,
        "evidence_snapshot_digest": evidence_snapshot_digest,
        "required_role": REQUIRED_ROLE,
        "expires_at": EXPIRES_AT,
    }
    request = ApprovalRequest(
        approval_id="APR-BINDING-1",
        case_id=CASE_ID,
        action=action,
        resource=resource,
        proposal_hash=proposal_hash(action, resource, proposal_arguments, CASE_VERSION),
        case_version=CASE_VERSION,
        policy_version=POLICY_VERSION,
        evidence_snapshot_digest=evidence_snapshot_digest,
        expires_at=EXPIRES_AT,
        required_role=REQUIRED_ROLE,
        status="approved",
    )
    decision = ApprovalDecision(
        approval_id=request.approval_id,
        proposal_hash=request.proposal_hash,
        approver_id="human-9",
        approver_role="underwriter",
        decision="approve",
        decided_at=NOW,
        reason="synthetic test decision",
    )
    return request, decision, evidence_snapshot_digest


def _verify(request: ApprovalRequest, decision: ApprovalDecision, *, policy_version: str, evidence_digest: str) -> None:
    verify_approval(
        request,
        decision,
        current_case_version=CASE_VERSION,
        current_policy_version=policy_version,
        current_evidence_snapshot_digest=evidence_digest,
    )


def test_approval_accepts_the_current_policy_and_evidence_snapshot():
    request, decision, evidence_snapshot_digest = _approved_pair()

    _verify(
        request,
        decision,
        policy_version=POLICY_VERSION,
        evidence_digest=evidence_snapshot_digest,
    )


def test_approval_rejects_a_changed_evidence_snapshot():
    request, decision, _ = _approved_pair()

    with pytest.raises(ProposalRejected, match="STALE_EVIDENCE_SNAPSHOT"):
        _verify(
            request,
            decision,
            policy_version=POLICY_VERSION,
            evidence_digest=digest({"documents": [{"document_id": "DOC-1", "content_hash": "sha256:changed"}]}),
        )


def test_approval_rejects_a_changed_policy_version():
    request, decision, evidence_snapshot_digest = _approved_pair()

    with pytest.raises(ProposalRejected, match="STALE_POLICY_VERSION"):
        _verify(
            request,
            decision,
            policy_version="mortgage-policy@2026.10",
            evidence_digest=evidence_snapshot_digest,
        )


@pytest.mark.parametrize(
    ("field", "tampered_value"),
    (
        ("action", "underwriting.cancel"),
        ("resource", "mortgage://case/OTHER-CASE"),
        ("case_id", "CASE-OTHER"),
        ("case_version", CASE_VERSION + 1),
        ("policy_version", "mortgage-policy@2026.10"),
        ("evidence_snapshot_digest", digest({"documents": [{"document_id": "DOC-1", "content_hash": "sha256:changed"}]})),
        ("required_role", "senior-underwriter"),
        ("expires_at", EXPIRES_AT + timedelta(minutes=1)),
    ),
)
def test_approval_rejects_request_fields_changed_after_approval(field: str, tampered_value: object):
    request, decision, evidence_snapshot_digest = _approved_pair()
    tampered_request = request.model_copy(update={field: tampered_value})

    with pytest.raises(ProposalRejected, match="APPROVAL_BINDING_MISMATCH"):
        _verify(
            tampered_request,
            decision,
            policy_version=POLICY_VERSION,
            evidence_digest=evidence_snapshot_digest,
        )


def test_approval_proposal_hash_binds_policy_and_evidence_context():
    request, _, evidence_snapshot_digest = _approved_pair()
    changed_evidence_hash = proposal_hash(
        request.action,
        request.resource,
        {
            "case_id": request.case_id,
            "policy_version": POLICY_VERSION,
            "evidence_snapshot_digest": digest({"documents": []}),
            "required_role": request.required_role,
            "expires_at": request.expires_at,
        },
        CASE_VERSION,
    )
    changed_policy_hash = proposal_hash(
        request.action,
        request.resource,
        {
            "case_id": request.case_id,
            "policy_version": "mortgage-policy@2026.10",
            "evidence_snapshot_digest": evidence_snapshot_digest,
            "required_role": request.required_role,
            "expires_at": request.expires_at,
        },
        CASE_VERSION,
    )

    assert request.proposal_hash != changed_evidence_hash
    assert request.proposal_hash != changed_policy_hash


def test_approval_request_context_cannot_be_mutated_after_creation():
    request, _, _ = _approved_pair()

    with pytest.raises(ValidationError):
        request.evidence_snapshot_digest = digest({"documents": []})
    with pytest.raises(ValidationError):
        request.policy_version = "mortgage-policy@2026.10"
