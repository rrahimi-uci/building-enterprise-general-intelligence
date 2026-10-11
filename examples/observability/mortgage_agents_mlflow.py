"""Trace the cumulative mortgage agent with the real Agents SDK and MLflow.

The model is scripted so this example is offline, but the agent, function tool,
structured output, runner, and MLflow Agents SDK trace processor are real. The
gateway deliberately returns only synthetic document metadata: a diagnostic
trace is not an excuse to copy an applicant's name, address, or document text.
"""
from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timedelta, timezone

import mlflow

from examples._harness.scripted_model import Say, ScriptedModel, ToolCall
from mortgage_case.adapters.openai_agents import execute_with_agents_sdk
from mortgage_case.domain.case import SYNTHETIC_NOTICE, load_anchor_case
from mortgage_case.platform.runtime import AgentStepRequest

# --8<-- example:start


class SyntheticMortgageGateway:
    """Return a safe projection, never raw mortgage documents or PII."""

    async def invoke(self, **kwargs: object) -> dict[str, object]:
        if kwargs.get("tool_version") != "mortgage.case.read@1":
            return {"error_code": "UNSUPPORTED_TOOL", "synthetic_notice": SYNTHETIC_NOTICE}
        return {
            "case_id": kwargs["case_id"],
            "available_document_ids": ["APP-000184", "PAY-000184-01", "PUR-000184"],
            "missing_document_kinds": ["pay_statement"],
            "synthetic_notice": SYNTHETIC_NOTICE,
        }


def configure_observability(experiment: str = "book-mortgage-agents") -> None:
    """Enable MLflow's OpenAI and Agents SDK integrations for this run."""

    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))
    mlflow.set_experiment(experiment)
    # MLflow 3.15.2 registers its Agents SDK trace processor whatever the flag,
    # so AgentRunner, agent, and tool spans appear either way. False also keeps
    # the SDK's own exporter, which sends nothing without an API key.
    mlflow.openai.autolog(
        log_traces=True,
        disable_openai_agent_tracer=False,
    )


def run_mortgage_review() -> dict[str, object]:
    """Run one read-only mortgage evidence review and return safe trace facts."""

    case = load_anchor_case()
    request = AgentStepRequest(
        run_id="RUN-MORT-000184-OBS",
        case_id=case.case_id,
        tenant_id=case.tenant_id,
        input_items=(
            f"Review authorized evidence metadata for {case.case_id}. "
            "Report missing evidence. Do not decide credit or write to a system."
        ),
        agent_version="mortgage-evidence-agent@0.1.0",
        eligible_tool_versions=("mortgage.case.read@1",),
        deadline=datetime.now(timezone.utc) + timedelta(seconds=10),
        max_turns=3,
    )
    model = ScriptedModel([
        ToolCall("read_mortgage_case", {"case_id": case.case_id}),
        Say(
            '{"status":"needs_input","summary":"A second pay statement is '
            'missing.","evidence_artifact_ids":[]}'
        ),
    ])
    result = asyncio.run(
        execute_with_agents_sdk(
            request,
            model=model,
            gateway=SyntheticMortgageGateway(),
        )
    )
    trace_id = mlflow.get_last_active_trace_id()
    if trace_id is None:
        raise RuntimeError("MLflow did not return a trace for the Agents SDK run")
    trace = mlflow.get_trace(trace_id, flush=True)
    return {
        "status": result.status,
        "summary": result.summary,
        "trace_id": trace_id,
        "span_names": sorted({span.name for span in trace.data.spans}),
        "synthetic_notice": SYNTHETIC_NOTICE,
    }


# --8<-- example:end


if __name__ == "__main__":  # pragma: no cover - exercised by the example test
    configure_observability()
    print(json.dumps(run_mortgage_review(), indent=2, sort_keys=True))
