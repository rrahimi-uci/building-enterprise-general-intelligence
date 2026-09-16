"""An action authorization must cover this exact proposal, by this reviewer, now."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from examples.patterns.approval_verification import (
    HumanActionAuthorizationDecision, HumanActionAuthorizationRequest,
    verify_action_authorization,
)

NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)
POLICY = "sha256:" + "b" * 64


def proposal(**kw) -> HumanActionAuthorizationRequest:
    base = dict(tenant_id="t1", run_id="r1", actor_id="agent-1",
                tool_version="mortgage.document.request@1",
                logical_effect_key="mortgage:document-request:MORT-2026-000184:employment_verification",
                arguments={"case_id": "MORT-2026-000184", "document_kind": "employment_verification"},
                expected_resource_version=7,
                policy_digest=POLICY, expires_at=NOW + timedelta(hours=4))
    base.update(kw)
    return HumanActionAuthorizationRequest(**base)


def decision(p: HumanActionAuthorizationRequest, **kw) -> HumanActionAuthorizationDecision:
    base = dict(approval_id="ap-1", proposal_hash=p.digest(), tenant_id=p.tenant_id,
                run_id=p.run_id, approver_id="human-9", approved_at=NOW - timedelta(minutes=5),
                expires_at=NOW + timedelta(hours=1), policy_digest=POLICY)
    base.update(kw)
    return HumanActionAuthorizationDecision(**base)


def test_a_matching_authorization_verifies():
    p = proposal()
    verify_action_authorization(p, decision(p), now=NOW, actual_resource_version=7)


def test_changing_the_document_kind_invalidates_the_authorization():
    approved = proposal()
    authorization = decision(approved)
    tampered = proposal(arguments={
        "case_id": "MORT-2026-000184", "document_kind": "tax_return"
    })
    with pytest.raises(PermissionError, match="not bound"):
        verify_action_authorization(tampered, authorization, now=NOW, actual_resource_version=7)


def test_an_agent_cannot_approve_its_own_action():
    p = proposal()
    with pytest.raises(PermissionError, match="self-approve"):
        verify_action_authorization(p, decision(p, approver_id="agent-1"), now=NOW, actual_resource_version=7)


def test_policy_change_after_approval_fails_closed():
    p = proposal()
    with pytest.raises(PermissionError, match="policy changed"):
        verify_action_authorization(p, decision(p, policy_digest="sha256:" + "c" * 64),
                        now=NOW, actual_resource_version=7)


def test_expired_authorization_is_refused():
    p = proposal()
    late = NOW + timedelta(hours=2)
    with pytest.raises(PermissionError, match="expired"):
        verify_action_authorization(p, decision(p), now=late, actual_resource_version=7)


def test_resource_moved_under_the_authorization():
    p = proposal()
    with pytest.raises(PermissionError, match="resource changed"):
        verify_action_authorization(p, decision(p), now=NOW, actual_resource_version=8)


def test_naive_timestamps_are_rejected_rather_than_assumed_utc():
    p = proposal()
    with pytest.raises(ValueError, match="timezone-aware"):
        verify_action_authorization(p, decision(p), now=datetime(2026, 9, 13, 12, 0),
                        actual_resource_version=7)
