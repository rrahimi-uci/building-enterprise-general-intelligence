"""One bounded agent step behind a platform-owned adapter.

Everything the enterprise is accountable for -- the tool gateway, the context
manifest, the disposition contract -- belongs to the platform. The framework
sits inside this boundary and can be replaced without touching the callers.
"""
import os
from dataclasses import dataclass
from typing import Literal, Protocol

from agents import Agent, RunConfig, RunContextWrapper, Runner, ToolExecutionConfig
from agents.decorators import tool
from pydantic import BaseModel


class ToolGateway(Protocol):
    async def invoke(self, *, tenant_id: str, subject_id: str,
                     actor_id: str, run_id: str, tool: str,
                     arguments: dict[str, object]) -> dict[str, object]: ...


@dataclass(frozen=True)
class PlatformContext:
    tenant_id: str
    subject_id: str
    actor_id: str
    run_id: str
    gateway: ToolGateway


class StepDisposition(BaseModel):
    status: Literal["completed", "needs_input", "proposed_action"]
    summary: str
    evidence_artifact_ids: list[str]


@tool
async def retrieve_supplier_policy(
    ctx: RunContextWrapper[PlatformContext], country: str
) -> dict[str, object]:
    """Retrieve authorized policy through the enterprise Tool Gateway."""
    return await ctx.context.gateway.invoke(
        tenant_id=ctx.context.tenant_id,
        subject_id=ctx.context.subject_id,
        actor_id=ctx.context.actor_id,
        run_id=ctx.context.run_id,
        tool="supplier.policy.read.v2",
        arguments={"country": country},
    )


agent = Agent[PlatformContext](
    name="Supplier analyst",
    # Read with a default, not os.environ[...]: reading a required variable at
    # import time makes the module unimportable wherever it is unset, including
    # in tests and in any tool that merely inspects the package.
    model=os.environ.get("OPENAI_AGENT_MODEL", "gpt-4.1-mini"),
    instructions=(
        "Analyze only supplied authorized evidence. Return a structured "
        "disposition. Never claim that an external write occurred."
    ),
    tools=[retrieve_supplier_policy],
    output_type=StepDisposition,
)


# --8<-- region:core
async def execute_step(request, context: PlatformContext, *, model=None) -> dict[str, object]:
    result = await Runner.run(
        starting_agent=agent,
        input=request.input_items,
        context=context,
        max_turns=request.max_turns,
        run_config=RunConfig(
            # An injectable model is what lets the platform test this step without
            # a provider. Production passes nothing and the configured model wins.
            model=model,
            workflow_name="supplier-onboarding",
            group_id=request.run_id,
            trace_include_sensitive_data=False,
            trace_metadata={
                "run_id": request.run_id,
                "agent_version": request.agent_version,
            },
            tool_execution=ToolExecutionConfig(
                max_function_tool_concurrency=2,
            ),
        ),
    )
    output = StepDisposition.model_validate(result.final_output)
    return {
        "status": output.status,
        "decision_summary": output.summary,
        "output_artifacts": output.evidence_artifact_ids,
        "usage": str(result.context_wrapper.usage),
    }

# --8<-- endregion:core
