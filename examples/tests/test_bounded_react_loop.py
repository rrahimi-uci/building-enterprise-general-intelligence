from __future__ import annotations

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
from examples.patterns.bounded_react_loop import RunBudget, run


async def test_budget_stops_the_loop_without_raising():
    budget = RunBudget(max_tool_calls=2)
    model = ScriptedModel([
        ToolCall("search_mortgage_evidence", {"query": "income"}),
        ToolCall("search_mortgage_evidence", {"query": "property"}),
        ToolCall("search_mortgage_evidence", {"query": "title"}),   # over budget
        Say("Budget exhausted after two lookups; income is missing, property is present."),
    ])
    answer = await run("Review mortgage case MORT-2026-000184", budget=budget, model=model)

    assert budget.tool_calls == 2, "the third call must not consume budget"
    assert budget.exhausted_at == "search_mortgage_evidence"
    assert "exhausted" in answer.lower()


async def test_within_budget_runs_normally():
    budget = RunBudget(max_tool_calls=3)
    model = ScriptedModel([
        ToolCall("search_mortgage_evidence", {"query": "income"}),
        Say("A second pay statement is missing."),
    ])
    answer = await run("Check income evidence for MORT-2026-000184", budget=budget, model=model)
    assert budget.exhausted_at is None
    assert budget.tool_calls == 1
    assert "missing" in answer.lower()
