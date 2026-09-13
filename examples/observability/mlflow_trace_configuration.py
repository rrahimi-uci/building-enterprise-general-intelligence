"""Configuring MLflow tracing around a governed agent step.

The model provider's autolog captures the LLM calls. Everything the enterprise
is actually accountable for -- which context was authorized, which policy
applied, which effect committed -- only appears in the trace if the platform
adds those spans itself. This example does both.
"""
from __future__ import annotations

import os

import mlflow
from mlflow.entities import SpanType

# --8<-- example:start


def configure_observability(experiment: str = "northstar-supplier-onboarding") -> None:
    """Point MLflow at the tracking backend and capture provider calls.

    MLflow 3.15 placed the filesystem store into maintenance mode for traces, so
    a database-backed URI is required; `sqlite:///` is fine for a laptop and a
    server URI for shared environments.
    """
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))
    mlflow.set_experiment(experiment)
    # Captures OpenAI calls; the explicit spans below cover the platform-owned
    # workflow, policy, approval, and effect boundaries that autolog cannot see.
    mlflow.openai.autolog()


def traced_step(run_id: str, supplier_id: str) -> dict[str, str]:
    """One governed step, instrumented so a later investigation can replay it."""
    # Trace-level tags are the join key between a trace and the run, tenant, and
    # risk class recorded in the system of record.
    mlflow.update_current_trace(tags={"run_id": run_id, "risk_class": "R2"})
    with mlflow.start_span(
        name="load_authorized_context", span_type=SpanType.RETRIEVER
    ) as span:
        span.set_inputs({"supplier_id": supplier_id})
        context_manifest_id = f"ctx:{run_id}:1"
        # Recording the manifest id, not the context body, keeps the trace
        # useful without turning it into a second copy of sensitive data.
        span.set_outputs({"context_manifest_id": context_manifest_id})
    return {"status": "ready_for_approval", "context_manifest_id": context_manifest_id}


# --8<-- example:end
