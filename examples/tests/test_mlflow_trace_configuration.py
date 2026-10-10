from __future__ import annotations

import mlflow

from examples.observability.mlflow_trace_configuration import traced_step


@mlflow.trace(span_type="AGENT")
def _governed_run(run_id: str, case_id: str) -> dict[str, str]:
    return traced_step(run_id, case_id)


def test_step_emits_a_retriever_span_and_run_tags():
    out = _governed_run("run-77", "MORT-2026-000184")
    assert out["status"] == "needs_input"
    assert out["context_manifest_id"] == "ctx:run-77:1"

    trace = mlflow.get_trace(mlflow.get_last_active_trace_id(), flush=True)
    spans = {s.name: s for s in trace.data.spans}
    assert "load_authorized_context" in spans, "the authorized-context load must be a span"
    assert trace.info.tags["run_id"] == "run-77"
    assert trace.info.tags["case_id"] == "MORT-2026-000184"
    assert trace.info.tags["risk_class"] == "R2"
    # The manifest id is recorded; the context body is deliberately not.
    assert "ctx:run-77:1" in str(spans["load_authorized_context"].outputs)


def test_pinned_autolog_disables_the_agents_sdk_tracer_by_default():
    # Chapter 24 states this default; the example opts in explicitly because of it.
    import inspect

    import mlflow.openai

    default = inspect.signature(mlflow.openai.autolog).parameters[
        "disable_openai_agent_tracer"
    ].default
    assert default is True
