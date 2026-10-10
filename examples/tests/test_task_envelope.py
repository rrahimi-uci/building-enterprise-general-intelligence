"""The Task Service must enforce what Chapter 18 says delegation guarantees."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from examples.contracts import TaskConflict, TaskEnvelope, TaskService

DEADLINE = datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc)
GRANTS = {("grant://run/supervisor", "grant://run/income-read")}


def narrower(parent: str, child: str) -> bool:
    return (parent, child) in GRANTS


def envelope(**overrides) -> TaskEnvelope:
    fields = dict(
        task_id="task-income", run_id="RUN-98217", parent_task_id="task-root",
        tenant_id="harborlight", subject_id="applicant-184",
        owner_agent="income-verification@0.1.0",
        goal="Verify income for MORT-2026-000184",
        acceptance_contract="schema://income-verification-result@1",
        deadline=DEADLINE, output_schema="schema://income-verification-result@1",
        capability_grant_id="grant://run/income-read", delegation_depth=0,
        maximum_cost_usd=Decimal("2.00"), idempotency_key="RUN-98217:income:1",
        trace_context="00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
    )
    fields.update(overrides)
    return TaskEnvelope(**fields)


PARENT = envelope(
    task_id="task-root", parent_task_id=None, owner_agent="mortgage-evidence-agent@0.1.0",
    capability_grant_id="grant://run/supervisor", delegation_depth=2,
    maximum_cost_usd=Decimal("5.00"), idempotency_key="RUN-98217:root",
)


def test_redelivered_creation_returns_the_same_task_without_a_second_withdrawal():
    service = TaskService(narrower)
    first = service.create_child(PARENT, envelope())
    assert service.create_child(PARENT, envelope()) == first
    # Only one $2 withdrawal happened, so $3 is still available.
    service.create_child(PARENT, envelope(task_id="t2", idempotency_key="k2",
                                          maximum_cost_usd=Decimal("3.00")))


def test_reusing_a_key_for_different_work_is_a_conflict():
    service = TaskService(narrower)
    service.create_child(PARENT, envelope())
    with pytest.raises(TaskConflict):
        service.create_child(PARENT, envelope(goal="Something else"))


def test_delegation_depth_must_shrink_and_a_leaf_cannot_delegate():
    service = TaskService(narrower)
    with pytest.raises(PermissionError, match="depth"):
        service.create_child(PARENT, envelope(delegation_depth=2))
    leaf = envelope()
    grandchild = envelope(task_id="t3", parent_task_id=leaf.task_id, idempotency_key="k3")
    with pytest.raises(PermissionError, match="depth"):
        service.create_child(leaf, grandchild)


def test_children_withdraw_from_the_parent_budget_rather_than_get_fresh_limits():
    service = TaskService(narrower)
    service.create_child(PARENT, envelope(maximum_cost_usd=Decimal("4.00")))
    with pytest.raises(PermissionError, match="budget"):
        service.create_child(PARENT, envelope(task_id="t2", idempotency_key="k2",
                                              maximum_cost_usd=Decimal("2.00")))


def test_the_subset_check_runs_before_any_child_exists():
    calls: list[tuple[str, str]] = []

    def refuse(parent: str, child: str) -> bool:
        calls.append((parent, child))
        return False

    service = TaskService(refuse)
    with pytest.raises(PermissionError, match="subset"):
        service.create_child(PARENT, envelope())
    assert calls == [("grant://run/supervisor", "grant://run/income-read")]
    # Nothing was recorded, so a corrected retry with the same key is not a conflict.
    assert TaskService(narrower).create_child(PARENT, envelope()).task_id == "task-income"


def test_subject_tenant_and_deadline_cannot_widen():
    service = TaskService(narrower)
    with pytest.raises(PermissionError):
        service.create_child(PARENT, envelope(subject_id="someone-else"))
    with pytest.raises(PermissionError, match="deadline"):
        service.create_child(PARENT, envelope(deadline=DEADLINE.replace(day=20)))
