"""An input guardrail that stops a run before any tool can act.

The book's position is that injected instructions arrive as ordinary content, so
a guardrail placed only around the user's prompt misses them. This one runs on
input, but the important property is where it sits in the pipeline: it trips
*before* the agent reaches a tool, so a refusal costs nothing downstream.
"""
from __future__ import annotations

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    function_tool,
    input_guardrail,
)
from agents.exceptions import InputGuardrailTripwireTriggered
from agents.run import RunConfig

# --8<-- example:start

# Phrases that attempt to re-authorize the agent from inside the content. A real
# deployment classifies rather than matches strings; the architecture is the
# point, not the detector.
OVERRIDE_MARKERS = ("ignore previous instructions", "you are now", "disregard the policy")


@input_guardrail
async def no_instruction_override(
    context: RunContextWrapper[None], agent: Agent, user_input
) -> GuardrailFunctionOutput:
    text = user_input if isinstance(user_input, str) else str(user_input)
    hit = next((m for m in OVERRIDE_MARKERS if m in text.lower()), None)
    return GuardrailFunctionOutput(
        output_info={"marker": hit},
        # Tripping raises before the model is asked to act, so nothing downstream
        # sees the request at all.
        tripwire_triggered=hit is not None,
    )


@function_tool
def request_mortgage_document(case_id: str, document_kind: str) -> str:
    """Propose a document request; a workflow still owns the external effect."""
    if not case_id.startswith("MORT-") or not document_kind:
        return "invalid mortgage document request"
    return f"document request proposed for {case_id}: {document_kind}"


agent = Agent(
    name="Mortgage evidence intake",
    instructions="Identify missing mortgage evidence and propose a document request.",
    tools=[request_mortgage_document],
    input_guardrails=[no_instruction_override],
)


async def run(request: str, *, model=None) -> tuple[bool, str]:
    """Return (allowed, result). A blocked run never reaches a tool."""
    try:
        result = await Runner.run(
            agent, request, max_turns=4,
            run_config=RunConfig(model=model, tracing_disabled=True),
        )
        return True, result.final_output
    except InputGuardrailTripwireTriggered:
        return False, "blocked: the request tried to override the agent's instructions"


# --8<-- example:end
