"""The agent example must dispatch the tool and return typed output, offline."""
from __future__ import annotations

import pytest

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
from examples.foundations.agent_tool_loop import SupplierStatus, run


@pytest.mark.asyncio
async def test_agent_calls_the_tool_before_answering():
    model = ScriptedModel([
        ToolCall("lookup_supplier", {"supplier_id": "S-1001"}),
        Say('{"supplier_id": "S-1001", "active": true, "summary": "Supplier S-1001 is active."}'),
    ])
    result = await run("Is supplier S-1001 active?", model=model)
    assert isinstance(result, SupplierStatus)
    assert result.active is True
    assert result.supplier_id == "S-1001"
    # The tool was genuinely dispatched by the SDK, not simulated by the test.
    assert isinstance(model.calls[0], ToolCall)
    assert model.calls[0].name == "lookup_supplier"


@pytest.mark.asyncio
async def test_unknown_supplier_is_reported_as_data_not_an_exception():
    model = ScriptedModel([
        ToolCall("lookup_supplier", {"supplier_id": "S-9999"}),
        Say('{"supplier_id": "S-9999", "active": false, "summary": "No record."}'),
    ])
    result = await run("Is supplier S-9999 active?", model=model)
    assert result.active is False
