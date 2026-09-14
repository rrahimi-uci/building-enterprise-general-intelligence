from __future__ import annotations

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
from examples.patterns.routing_handoff import run


async def test_request_is_handed_to_the_owning_specialist():
    # A handoff is dispatched as a tool call named transfer_to_<agent>.
    model = ScriptedModel([
        ToolCall("transfer_to_sanctions_specialist", {}),
        Say("Screened: no restricted-party match for Acme Ltd."),
    ])
    answer, decided_by = await run("Is Acme Ltd on a sanctions list?", model=model)
    assert decided_by == "Sanctions specialist", "ownership must transfer, not just context"
    assert "no restricted-party match" in answer


async def test_routing_to_the_other_specialist():
    model = ScriptedModel([
        ToolCall("transfer_to_refunds_specialist", {}),
        Say("Eligible under the 30-day policy."),
    ])
    answer, decided_by = await run("Can I refund order 88?", model=model)
    assert decided_by == "Refunds specialist"
    assert "30-day" in answer
