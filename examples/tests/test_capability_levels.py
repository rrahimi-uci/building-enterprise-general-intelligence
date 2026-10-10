"""Chapter 1's prototype works on the first try -- and fails the demo week."""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from agents import set_tracing_disabled
from agents.exceptions import MaxTurnsExceeded

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
from examples.foundations import capability_levels as levels

CASE_ID = levels.CASE_ID
MISSING = "A second pay statement is missing."


@pytest.fixture(autouse=True)
def _offline_run():
    # Keep the SDK's trace exporter off for these runs only; the MLflow tests
    # in the same session rely on the global tracing switch staying on.
    set_tracing_disabled(True)
    levels.DOCUMENT_REQUESTS.clear()
    yield
    levels.DOCUMENT_REQUESTS.clear()
    set_tracing_disabled(False)


def _review_script() -> ScriptedModel:
    return ScriptedModel([
        ToolCall("read_mortgage_case", {"case_id": CASE_ID}),
        ToolCall("request_mortgage_document",
                 {"case_id": CASE_ID, "document_kind": "pay_statement"}),
        Say(MISSING),
    ])


async def test_the_demo_works_on_the_first_try():
    answer = await levels.review(CASE_ID, model=_review_script())
    assert answer == MISSING
    assert levels.DOCUMENT_REQUESTS == [(CASE_ID, "pay_statement")]


async def test_a_retried_run_duplicates_the_document_request():
    # Wednesday: the confirmation is lost and the caller runs the review again.
    # Nothing in the prototype recognizes the second request as the same one.
    await levels.review(CASE_ID, model=_review_script())
    await levels.review(CASE_ID, model=_review_script())
    assert levels.DOCUMENT_REQUESTS == [(CASE_ID, "pay_statement")] * 2


def test_level_one_sends_only_the_prompt():
    calls: list[dict] = []

    def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(output_text="Application, one pay statement, purchase agreement.")

    client = SimpleNamespace(responses=SimpleNamespace(create=create))
    answer = levels.summarize(client, "case_id=MORT-2026-000184")
    assert answer.startswith("Application")
    # A bare model call has no tools: it knows only what the prompt carries.
    assert set(calls[0]) == {"model", "input"}
    assert "MORT-2026-000184" in calls[0]["input"]


async def test_level_two_tool_is_ordinary_code_that_decides_the_answer():
    model = ScriptedModel([
        ToolCall("read_mortgage_case", {"case_id": "MORT-2026-000999"}),
        Say("No mortgage case record."),
    ])
    await levels.review("MORT-2026-000999", model=model)
    assert levels.case_gateway.status("MORT-2026-000999").startswith("no mortgage case record")
    assert levels.case_gateway.status(CASE_ID) == "second pay statement missing"


async def test_level_three_stops_only_at_the_turn_limit():
    # The loop decides for itself when it is done; max_turns is its only stop.
    model = ScriptedModel([ToolCall("read_mortgage_case", {"case_id": CASE_ID})] * 9)
    with pytest.raises(MaxTurnsExceeded):
        await levels.review_in_a_loop(CASE_ID, model=model)
    assert len(model.calls) == 8
