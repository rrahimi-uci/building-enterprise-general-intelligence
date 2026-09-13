from __future__ import annotations

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
from examples.patterns.bounded_react_loop import RunBudget, run


async def test_budget_stops_the_loop_without_raising():
    budget = RunBudget(max_tool_calls=2)
    model = ScriptedModel([
        ToolCall("search_records", {"query": "sanctions"}),
        ToolCall("search_records", {"query": "tax"}),
        ToolCall("search_records", {"query": "credit"}),   # over budget
        Say("Budget exhausted after two lookups; sanctions clear, tax verified."),
    ])
    answer = await run("Research supplier S-1001", budget=budget, model=model)

    assert budget.tool_calls == 2, "the third call must not consume budget"
    assert budget.exhausted_at == "search_records"
    assert "exhausted" in answer.lower()


async def test_within_budget_runs_normally():
    budget = RunBudget(max_tool_calls=3)
    model = ScriptedModel([
        ToolCall("search_records", {"query": "sanctions"}),
        Say("No sanctions match."),
    ])
    answer = await run("Check sanctions for S-1001", budget=budget, model=model)
    assert budget.exhausted_at is None
    assert budget.tool_calls == 1
    assert "sanctions" in answer.lower()
