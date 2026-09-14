from __future__ import annotations

import mlflow

from examples.observability.mlflow_tracing import handle_request


def test_run_produces_a_trace_with_a_tool_span():
    result = handle_request("S-1001")
    assert "active" in result
    trace = mlflow.get_last_active_trace_id()
    assert trace is not None, "the agent call must be traced"
    spans = mlflow.get_trace(trace, flush=True).data.spans
    names = {s.name for s in spans}
    assert "handle_request" in names
    assert "lookup_supplier" in names, "tool calls must appear as child spans"


def test_unknown_supplier_escalates():
    assert "escalating" in handle_request("S-4040")
