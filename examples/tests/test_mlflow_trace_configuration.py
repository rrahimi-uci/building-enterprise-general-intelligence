from __future__ import annotations

import mlflow

from examples.observability.mlflow_trace_configuration import traced_step


@mlflow.trace(span_type="AGENT")
def _governed_run(run_id: str, supplier_id: str) -> dict[str, str]:
    return traced_step(run_id, supplier_id)


def test_step_emits_a_retriever_span_and_run_tags():
    out = _governed_run("run-77", "S-1001")
    assert out["status"] == "ready_for_approval"
    assert out["context_manifest_id"] == "ctx:run-77:1"

    trace = mlflow.get_trace(mlflow.get_last_active_trace_id(), flush=True)
    spans = {s.name: s for s in trace.data.spans}
    assert "load_authorized_context" in spans, "the authorized-context load must be a span"
    assert trace.info.tags["run_id"] == "run-77"
    assert trace.info.tags["risk_class"] == "R2"
    # The manifest id is recorded; the context body is deliberately not.
    assert "ctx:run-77:1" in str(spans["load_authorized_context"].outputs)
