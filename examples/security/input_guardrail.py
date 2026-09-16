"""An input guardrail that stops a run before any tool can act.

The book's position is that injected instructions arrive as ordinary content, so
a guardrail placed only around the user's prompt misses them. This one runs on
input, but the important property is where it sits in the pipeline: it trips
*before* the agent reaches a tool, so a refusal costs nothing downstream.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

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
def issue_refund(order_id: str, amount_usd: str) -> str:
    """Issue a refund. Guarded: this is a real, irreversible effect."""
    try:
        amount = Decimal(amount_usd)
    except (InvalidOperation, ValueError):
        return "invalid refund amount"
    if amount < 0:
        return "invalid refund amount"
    return f"refunded {amount:.2f} for {order_id}"


agent = Agent(
    name="Refunds",
    instructions="Process refunds that policy allows.",
    tools=[issue_refund],
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
