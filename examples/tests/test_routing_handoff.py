from __future__ import annotations

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
from examples.patterns.routing_handoff import run


async def test_request_is_handed_to_the_owning_specialist():
    # A handoff is dispatched as a tool call named transfer_to_<agent>.
    model = ScriptedModel([
        ToolCall("transfer_to_mortgage_evidence_specialist", {}),
        Say("MORT-2026-000184 is missing a second pay statement."),
    ])
    answer, decided_by = await run(
        "What evidence is missing from MORT-2026-000184?", model=model
    )
    assert decided_by == "Mortgage evidence specialist", "control must pass to the specialist"
    assert "second pay statement" in answer


async def test_routing_to_the_other_specialist():
    model = ScriptedModel([
        ToolCall("transfer_to_mortgage_policy_specialist", {}),
        Say("Apply mortgage-policy@2026.09 to the evidence review."),
    ])
    answer, decided_by = await run(
        "Which policy revision governs MORT-2026-000184?", model=model
    )
    assert decided_by == "Mortgage policy specialist"
    assert "mortgage-policy" in answer
