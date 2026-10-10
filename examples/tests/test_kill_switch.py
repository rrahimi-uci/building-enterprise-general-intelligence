from __future__ import annotations

import pytest
from pydantic import ValidationError

from examples.security.kill_switch import KillSwitchRule

REQUEST = {
    "tenant_id": "harborlight",
    "agent_version": "mortgage-evidence-agent@0.1.0",
    "tool_version": "mortgage.document.request@1",
    "model_route": "reasoning-standard@4",
}


def test_a_rule_without_a_scope_is_rejected():
    with pytest.raises(ValidationError, match="requires a scope"):
        KillSwitchRule(reason="suspected injection campaign")


def test_a_rule_requires_a_reason():
    with pytest.raises(ValidationError):
        KillSwitchRule(tool_version="mortgage.document.request@1", reason="")


def test_a_tool_version_rule_blocks_that_version_everywhere():
    rule = KillSwitchRule(tool_version="mortgage.document.request@1", reason="LOS incident")
    assert rule.blocks(**REQUEST)
    assert rule.blocks(**{**REQUEST, "tenant_id": "other-tenant"})


def test_a_rule_leaves_work_outside_its_scope_running():
    rule = KillSwitchRule(tool_version="mortgage.document.request@1", reason="LOS incident")
    # A read through a different tool keeps working: containment, not outage.
    assert not rule.blocks(**{**REQUEST, "tool_version": "mortgage.case.read@1"})
    assert not rule.blocks(**{**REQUEST, "tool_version": None})


def test_every_named_scope_must_match():
    rule = KillSwitchRule(
        tenant_id="harborlight", model_route="reasoning-standard@4", reason="route drift"
    )
    assert rule.blocks(**REQUEST)
    assert not rule.blocks(**{**REQUEST, "model_route": "reasoning-standard@5"})
    assert not rule.blocks(**{**REQUEST, "tenant_id": "other-tenant"})
