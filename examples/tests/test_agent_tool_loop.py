"""The agent example must dispatch the tool and return typed output, offline."""
from __future__ import annotations

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
from examples.foundations.agent_tool_loop import MortgageCaseStatus, run

CASE_ID = "MORT-2026-000184"


async def test_agent_calls_the_tool_before_answering():
    model = ScriptedModel([
        ToolCall("read_mortgage_case", {"case_id": CASE_ID}),
        Say('{"case_id": "MORT-2026-000184", "needs_input": true, '
            '"summary": "Employment verification is missing."}'),
    ])
    result = await run("Does MORT-2026-000184 have all required evidence?", model=model)
    assert isinstance(result, MortgageCaseStatus)
    assert result.needs_input is True
    assert result.case_id == CASE_ID
    # The tool was genuinely dispatched by the SDK, not simulated by the test.
    assert isinstance(model.calls[0], ToolCall)
    assert model.calls[0].name == "read_mortgage_case"


async def test_unknown_mortgage_case_is_reported_as_data_not_an_exception():
    model = ScriptedModel([
        ToolCall("read_mortgage_case", {"case_id": "MORT-2026-000999"}),
        Say('{"case_id": "MORT-2026-000999", "needs_input": true, '
            '"summary": "No mortgage case record."}'),
    ])
    result = await run("Review mortgage case MORT-2026-000999", model=model)
    assert result.needs_input is True
