from __future__ import annotations

import mlflow

from examples.observability.mortgage_agents_mlflow import (
    configure_observability,
    run_mortgage_review,
)


def test_real_agents_sdk_run_is_recorded_by_mlflow_without_raw_case_content():
    configure_observability("book-mortgage-agents-test")
    output = run_mortgage_review()

    assert output["status"] == "needs_input"
    assert "AgentRunner.run" in output["span_names"]
    assert "Mortgage evidence reviewer" in output["span_names"]
    assert "read_mortgage_case" in output["span_names"]
    assert output["synthetic_notice"] == "SYNTHETIC TRAINING DATA — NOT FOR CREDIT DECISIONS"

    trace = mlflow.get_trace(output["trace_id"], flush=True)
    rendered = str(trace.data.spans)
    assert "Alex Morgan" not in rendered
    assert "101 Example Avenue" not in rendered
