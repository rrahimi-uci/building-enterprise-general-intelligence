from __future__ import annotations

import mlflow

from examples.observability.mlflow_tracing import handle_request

CASE_ID = "MORT-2026-000184"


def test_run_produces_a_trace_with_a_tool_span():
    result = handle_request(CASE_ID)
    assert "needs_input" in result
    trace = mlflow.get_last_active_trace_id()
    assert trace is not None, "the agent call must be traced"
    spans = mlflow.get_trace(trace, flush=True).data.spans
    names = {s.name for s in spans}
    assert "handle_request" in names
    assert "read_mortgage_case" in names, "tool calls must appear as child spans"


def test_unknown_mortgage_case_escalates():
    assert "escalating" in handle_request("MORT-2026-000999")
