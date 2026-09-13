from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from examples.patterns.approval_gate import (
    ApprovalExpired, ApprovalGrant, PendingApprovals, ProposalMismatch, proposal_hash,
)

NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)


def _grant(digest, **kw):
    return ApprovalGrant(proposal_hash=digest, approver_id="u-7",
                         expires_at=kw.get("expires_at", NOW + timedelta(hours=1)))


def test_approved_proposal_commits_once():
    store = PendingApprovals()
    digest = store.pause("r1", "issue_refund", {"order": "A-1", "usd": 20}, timedelta(days=2))
    assert store.commit("r1", _grant(digest), now=NOW).startswith("committed issue_refund")
    assert "r1" not in store.pending, "a committed pause must not remain pending"


def test_amount_changed_after_approval_is_refused():
    store = PendingApprovals()
    store.pause("r1", "issue_refund", {"order": "A-1", "usd": 20}, timedelta(days=2))
    # An approver who agreed to $20 has not agreed to $5000.
    tampered = proposal_hash("issue_refund", {"order": "A-1", "usd": 5000})
    with pytest.raises(ProposalMismatch):
        store.commit("r1", _grant(tampered), now=NOW)


def test_expired_grant_is_a_refusal_not_a_warning():
    store = PendingApprovals()
    digest = store.pause("r1", "issue_refund", {"order": "A-1", "usd": 20}, timedelta(days=2))
    late = NOW + timedelta(hours=2)
    with pytest.raises(ApprovalExpired):
        store.commit("r1", _grant(digest), now=late)
    assert "r1" in store.pending, "a lapsed approval leaves the run paused, not committed"


def test_mutating_the_caller_dict_after_pausing_cannot_change_the_record():
    store = PendingApprovals()
    arguments = {"order": "A-1", "usd": 20}
    digest = store.pause("r1", "issue_refund", arguments, timedelta(days=2))
    arguments["usd"] = 5000          # the caller mutates its own dict afterwards
    assert store.pending["r1"]["arguments"]["usd"] == 20
    # And the approved digest still commits, because nothing actually changed.
    assert store.commit("r1", _grant(digest), now=NOW).startswith("committed")
