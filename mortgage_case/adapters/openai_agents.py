"""Optional OpenAI Agents SDK implementation behind AgentRuntime."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from ..platform.runtime import AgentRuntime, AgentStepRequest, AgentStepResult

try:  # Keep importing the platform package possible without the optional SDK.
    from agents import RunContextWrapper
except ImportError:  # pragma: no cover - only used in the book build environment
    class RunContextWrapper:  # type: ignore[no-redef]
        """Placeholder used until the optional adapter is executed."""


class AgentsAdapterDisabled(RuntimeError):
    """Raised unless a caller explicitly opts into the provider-backed adapter."""


@dataclass(frozen=True)
class _RuntimeContext:
    tenant_id: str
    case_id: str


class OpenAIAgentsRuntime:
    """Provider adapter implementing the platform-owned runtime protocol."""

    def __init__(self, *, gateway: Any, model: Any = None) -> None:
        self.gateway = gateway
        self.model = model

    async def execute(self, request: AgentStepRequest) -> AgentStepResult:
        return await execute_with_agents_sdk(
            request,
            model=self.model,
            gateway=self.gateway,
        )


async def execute_with_agents_sdk(
    request: AgentStepRequest,
    *,
    model: Any = None,
    gateway: Any,
) -> AgentStepResult:
    """Execute one bounded step, translating SDK types at this boundary only."""

    if model is None and os.environ.get("MORTGAGE_CASE_ALLOW_LIVE_OPENAI") != "1":
        raise AgentsAdapterDisabled(
            "provider-backed execution is opt-in; pass a test model or set "
            "MORTGAGE_CASE_ALLOW_LIVE_OPENAI=1 explicitly"
        )
    allowed_tools = {"mortgage.case.read@1", "mortgage.policy.read@1"}
    if any(tool_version not in allowed_tools for tool_version in request.eligible_tool_versions):
        return AgentStepResult(
            status="failed",
            summary="The provider adapter rejected an out-of-scope tool version.",
            error_code="TOOL_NOT_ELIGIBLE",
        )
    try:
        from agents import Agent, RunConfig, Runner, ToolExecutionConfig
        from agents.decorators import tool
        from pydantic import BaseModel, ConfigDict, Field
    except ImportError as exc:  # pragma: no cover - exercised in a minimal install
        raise AgentsAdapterDisabled("openai-agents is not installed") from exc

    class StepOutput(BaseModel):
        model_config = ConfigDict(extra="forbid")

        status: str = Field(pattern=r"^(completed|needs_input|proposed_action)$")
        summary: str = Field(min_length=1)
        evidence_artifact_ids: list[str] = Field(default_factory=list)

    @tool
    async def read_mortgage_case(
        ctx: RunContextWrapper[_RuntimeContext], case_id: str
    ) -> dict[str, object]:
        """Read scoped case metadata through the platform gateway."""

        if case_id != ctx.context.case_id:
            return {"error_code": "CASE_SCOPE_DENIED"}
        return await gateway.invoke(
            tenant_id=ctx.context.tenant_id,
            case_id=case_id,
            tool_version="mortgage.case.read@1",
        )

    @tool
    async def read_mortgage_policy(
        ctx: RunContextWrapper[_RuntimeContext], policy_version: str
    ) -> dict[str, object]:
        """Read a scoped policy projection through the platform gateway."""

        if not policy_version or len(policy_version) > 64:
            return {"error_code": "INVALID_POLICY_VERSION"}
        return await gateway.invoke(
            tenant_id=ctx.context.tenant_id,
            case_id=ctx.context.case_id,
            policy_version=policy_version,
            tool_version="mortgage.policy.read@1",
        )

    tools = []
    if "mortgage.case.read@1" in request.eligible_tool_versions:
        tools.append(read_mortgage_case)
    if "mortgage.policy.read@1" in request.eligible_tool_versions:
        tools.append(read_mortgage_policy)

    agent = Agent[_RuntimeContext](
        name="Mortgage evidence reviewer",
        instructions=(
            "Review only authorized synthetic evidence. Return a structured "
            "evidence disposition. Never approve or deny credit and never claim "
            "that an external write occurred."
        ),
        tools=tools,
        output_type=StepOutput,
    )
    remaining_seconds = (request.deadline - datetime.now(timezone.utc)).total_seconds()
    if remaining_seconds <= 0:
        return AgentStepResult(
            status="failed",
            summary="The bounded agent step exceeded its workflow deadline.",
            error_code="DEADLINE_EXPIRED",
        )
    try:
        result = await asyncio.wait_for(
            Runner.run(
                starting_agent=agent,
                input=request.input_items,
                context=_RuntimeContext(request.tenant_id, request.case_id),
                max_turns=request.max_turns,
                run_config=RunConfig(
                    model=model,
                    workflow_name="mortgage-evidence-review",
                    group_id=request.run_id,
                    trace_include_sensitive_data=False,
                    tool_execution=ToolExecutionConfig(max_function_tool_concurrency=1),
                ),
            ),
            timeout=remaining_seconds,
        )
    except asyncio.TimeoutError:
        return AgentStepResult(
            status="failed",
            summary="The bounded agent step exceeded its workflow deadline.",
            error_code="DEADLINE_EXPIRED",
        )
    except Exception as exc:  # provider errors are not allowed across the seam
        return AgentStepResult(
            status="failed",
            summary="The provider failed before the workflow received a result.",
            error_code=f"PROVIDER_ERROR:{type(exc).__name__}",
        )
    try:
        output = StepOutput.model_validate(result.final_output)
    except Exception as exc:
        return AgentStepResult(
            status="failed",
            summary="The provider returned output outside the platform contract.",
            error_code=f"MALFORMED_OUTPUT:{type(exc).__name__}",
        )
    return AgentStepResult(
        status=output.status,
        summary=output.summary,
        evidence_artifact_ids=tuple(output.evidence_artifact_ids),
        usage={"turns": len(getattr(result, "raw_responses", ()))},
    )
