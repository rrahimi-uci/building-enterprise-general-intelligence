"""Routing by handoff: a triage agent that transfers ownership, not just context.

A handoff is an authority transfer. The receiving agent runs with its own
instructions, its own tools, and -- in a real deployment -- its own grant. That
is what makes routing an architecture decision rather than a prompt trick.
"""
from __future__ import annotations

from agents import Agent, Runner
from agents.run import RunConfig

# --8<-- example:start

evidence_specialist = Agent(
    name="Mortgage evidence specialist",
    handoff_description="Handles missing and contradictory mortgage evidence.",
    instructions=(
        "Review mortgage evidence gaps. Do not make or imply a lending decision."
    ),
)

policy_specialist = Agent(
    name="Mortgage policy specialist",
    handoff_description="Explains the policy that governs mortgage evidence review.",
    instructions=(
        "Explain the applicable mortgage policy and cite the policy revision. "
        "Do not make or imply a lending decision."
    ),
)

# The triage agent owns routing only. It deliberately has no domain tools, so it
# cannot quietly answer a question it should have handed off.
triage = Agent(
    name="Triage",
    instructions=(
        "Route the request to the specialist that owns it. "
        "Do not answer domain questions yourself."
    ),
    handoffs=[evidence_specialist, policy_specialist],
)


async def run(request: str, *, model=None):
    result = await Runner.run(
        triage, request, max_turns=5,
        run_config=RunConfig(model=model, tracing_disabled=True),
    )
    # last_agent is the audit answer to "who actually decided this?"
    return result.final_output, result.last_agent.name


# --8<-- example:end
