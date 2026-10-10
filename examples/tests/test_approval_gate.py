from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from examples.patterns.approval_gate import (
    ApprovalDecision, ApprovalExpired,
    ApprovalMismatch, ApprovalNotAuthentic,
    ApprovalService, PendingApprovals, proposal_hash,
)

NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)


def service() -> ApprovalService:
    return ApprovalService(secret=b"approval-service-key")


def store() -> PendingApprovals:
    return PendingApprovals(service=service())


def decision(svc: ApprovalService, digest: str, *, approver="u-7", expires=None) -> ApprovalDecision:
    return svc.issue(digest, approver, expires or NOW + timedelta(hours=1))


def test_approved_proposal_commits_once():
    s = store()
    digest = s.pause("r1", "request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "pay_statement"
    }, timedelta(days=2))
    result = s.commit("r1", decision(s.service, digest), now=NOW)
    assert result.startswith("committed request_mortgage_document")
    assert "r1" not in s.pending, "a committed pause must not remain pending"


def test_document_kind_changed_after_approval_is_refused():
    s = store()
    s.pause("r1", "request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "pay_statement"
    }, timedelta(days=2))
    # An approver who agreed to one document kind has not approved another.
    tampered = proposal_hash("request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "tax_return"
    })
    with pytest.raises(ApprovalMismatch):
        s.commit("r1", decision(s.service, tampered), now=NOW)


def test_expired_approval_is_a_refusal_not_a_warning():
    s = store()
    digest = s.pause("r1", "request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "pay_statement"
    }, timedelta(days=2))
    with pytest.raises(ApprovalExpired):
        s.commit("r1", decision(s.service, digest), now=NOW + timedelta(hours=2))
    assert "r1" in s.pending, "a lapsed approval leaves the run paused, not committed"


def test_a_fabricated_decision_cannot_approve_anything():
    s = store()
    digest = s.pause("r1", "request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "pay_statement"
    }, timedelta(days=2))
    # The code that wants the effect mints its own permission for it.
    forged = ApprovalDecision(proposal_hash=digest, approver_id="cfo",
                           expires_at=NOW + timedelta(hours=1), signature="0" * 64)
    with pytest.raises(ApprovalNotAuthentic):
        s.commit("r1", forged, now=NOW)
    assert "r1" in s.pending


def test_a_decision_from_a_different_service_is_refused():
    s = store()
    digest = s.pause("r1", "request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "pay_statement"
    }, timedelta(days=2))
    other = ApprovalService(secret=b"some-other-key")
    with pytest.raises(ApprovalNotAuthentic):
        s.commit("r1", decision(other, digest), now=NOW)


def test_mutating_the_caller_dict_after_pausing_cannot_change_the_record():
    s = store()
    arguments = {"case_id": "MORT-2026-000184", "document_kind": "pay_statement",
                 "meta": {"note": "ok"}}
    digest = s.pause("r1", "request_mortgage_document", arguments, timedelta(days=2))
    arguments["document_kind"] = "tax_return"  # the caller mutates its own dict afterwards
    arguments["meta"]["note"] = "urgent"   # including a nested value
    assert s.pending["r1"]["arguments"]["document_kind"] == "pay_statement"
    assert s.pending["r1"]["arguments"]["meta"]["note"] == "ok"
    assert s.commit("r1", decision(s.service, digest), now=NOW).startswith("committed")


def test_tampering_with_the_pending_record_is_caught_at_commit():
    s = store()
    digest = s.pause("r1", "request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "pay_statement"
    }, timedelta(days=2))
    approval = decision(s.service, digest)
    # Commit recomputes from the stored proposal, so editing the record -- and
    # even its cached digest -- does not make the effect approved.
    s.pending["r1"]["arguments"]["document_kind"] = "tax_return"
    s.pending["r1"]["digest"] = proposal_hash("request_mortgage_document", {
        "case_id": "MORT-2026-000184", "document_kind": "tax_return"
    })
    with pytest.raises(ApprovalMismatch):
        s.commit("r1", approval, now=NOW)
