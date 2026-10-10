"""Admission returns a typed disposition instead of raising on capacity shortfall."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from examples.platform.admission_permit import CapacityPermit, admit

NOW = datetime(2026, 9, 30, 16, 0, tzinfo=timezone.utc)


def permit(tokens=40_000, calls=12, sandbox=0, tenant="harborlight-retail",
           workload="interactive-read") -> CapacityPermit:
    return CapacityPermit(tenant, workload, tokens, calls, sandbox)


AVAILABLE = permit(tokens=100_000, calls=50, sandbox=60)
HARD_LIMIT = permit(tokens=500_000, calls=200, sandbox=600)


def decide(requested, available=AVAILABLE, *, refill_in=timedelta(minutes=2),
           deadline_in=timedelta(minutes=30)):
    return admit(requested, available, HARD_LIMIT,
                 refill_at=NOW + refill_in, deadline=NOW + deadline_in)


def test_request_within_capacity_is_granted():
    decision = decide(permit())
    assert decision.disposition == "granted"
    assert decision.permit == permit()


def test_shortfall_that_refills_before_deadline_is_deferred():
    decision = decide(permit(tokens=150_000))
    assert decision.disposition == "defer_until"
    assert decision.retry_after == NOW + timedelta(minutes=2)
    assert decision.permit is None


def test_shortfall_that_would_miss_deadline_is_rejected():
    decision = decide(permit(calls=80), refill_in=timedelta(hours=1))
    assert decision.disposition == "rejected"
    assert "deadline" in decision.reason


def test_request_over_hard_limit_is_rejected_even_with_time_to_wait():
    decision = decide(permit(sandbox=900), deadline_in=timedelta(days=1))
    assert decision.disposition == "rejected"
    assert decision.reason == "hard limit: sandbox_seconds"


def test_tenant_mismatch_is_an_authorization_error():
    with pytest.raises(PermissionError):
        decide(permit(tenant="other-tenant"))


def test_workload_class_mismatch_is_an_authorization_error():
    with pytest.raises(PermissionError):
        decide(permit(workload="browser-heavy"))
