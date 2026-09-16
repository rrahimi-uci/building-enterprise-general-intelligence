from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from mortgage_case.adapters.openai_agents import AgentsAdapterDisabled
from mortgage_case.adapters.openai_agents import OpenAIAgentsRuntime
from mortgage_case.adapters.openai_agents import execute_with_agents_sdk
from mortgage_case.platform.runtime import AgentStepRequest, ScriptedRuntime
from mortgage_case.stages.c03_agent_runtime import run


def request() -> AgentStepRequest:
    return AgentStepRequest(
        run_id="RUN-MORT-000184-C03",
        case_id="MORT-2026-000184",
        tenant_id="harborlight-us-west",
        input_items="Review synthetic mortgage evidence.",
        agent_version="mortgage-evidence-agent@0.1.0",
        eligible_tool_versions=("mortgage.case.read@1", "mortgage.policy.read@1"),
        deadline=datetime(2099, 12, 31, 23, 59, tzinfo=timezone.utc),
    )


def test_runtime_returns_platform_owned_result():
    result = asyncio.run(ScriptedRuntime(requested_tool="mortgage.case.read@1").execute(request()))
    assert result.status == "completed"
    assert result.tool_calls == ("mortgage.case.read@1",)


def test_runtime_rejects_tool_allowlist_escape():
    result = asyncio.run(ScriptedRuntime(requested_tool="mortgage.los.write@1").execute(request()))
    assert result.status == "failed"
    assert result.error_code == "TOOL_NOT_ELIGIBLE"


def test_runtime_rejects_naive_deadline():
    with pytest.raises(ValidationError):
        request_data = request().model_dump()
        request_data["deadline"] = datetime(2026, 9, 16, 12, 0)
        AgentStepRequest.model_validate(request_data)


def test_provider_adapter_is_opt_in_without_a_model():
    with pytest.raises(AgentsAdapterDisabled):
        asyncio.run(
            execute_with_agents_sdk(request(), model=None, gateway=object())
        )


def test_provider_adapter_rejects_out_of_scope_tool_before_provider_execution():
    request_data = request().model_dump()
    request_data["eligible_tool_versions"] = ("mortgage.los.write@1",)
    result = asyncio.run(
        execute_with_agents_sdk(
            AgentStepRequest.model_validate(request_data), model=object(), gateway=object()
        )
    )
    assert result.status == "failed"
    assert result.error_code == "TOOL_NOT_ELIGIBLE"


def test_agents_sdk_adapter_maps_to_platform_result_with_scripted_model():
    from examples._harness.scripted_model import Say, ScriptedModel, ToolCall

    class Gateway:
        async def invoke(self, **kwargs):
            return {"case_id": kwargs["case_id"], "document_ids": ["APP-000184"]}

    model = ScriptedModel([
        ToolCall("read_mortgage_case", {"case_id": "MORT-2026-000184"}),
        Say(
            '{"status":"needs_input","summary":"A second pay statement is missing.",'
            '"evidence_artifact_ids":["PAY-000184-01"]}'
        ),
    ])
    result = asyncio.run(
        OpenAIAgentsRuntime(gateway=Gateway(), model=model).execute(request())
    )
    assert result.status == "needs_input"
    assert result.evidence_artifact_ids == ("PAY-000184-01",)


def test_c03_stage_reports_boundary_failure():
    report = run("tool_allowlist_escape")
    assert report.status == "failed"
    assert report.failures == ("TOOL_NOT_ELIGIBLE",)
