"""Routing by handoff: a triage agent that transfers ownership, not just context.

A handoff is an authority transfer. The receiving agent runs with its own
instructions, its own tools, and -- in a real deployment -- its own grant. That
is what makes routing an architecture decision rather than a prompt trick.
"""
from __future__ import annotations

from agents import Agent, Runner
from agents.run import RunConfig

# --8<-- example:start

refunds = Agent(
    name="Refunds specialist",
    handoff_description="Handles refund eligibility and processing.",
    instructions="Decide refund eligibility. State the policy rule you applied.",
)

sanctions = Agent(
    name="Sanctions specialist",
    handoff_description="Handles sanctions and restricted-party screening.",
    instructions="Screen the named party. Never assert a clear result without a check.",
)

# The triage agent owns routing only. It deliberately has no domain tools, so it
# cannot quietly answer a question it should have handed off.
triage = Agent(
    name="Triage",
    instructions=(
        "Route the request to the specialist that owns it. "
        "Do not answer domain questions yourself."
    ),
    handoffs=[refunds, sanctions],
)


async def run(request: str, *, model=None):
    result = await Runner.run(
        triage, request, max_turns=5,
        run_config=RunConfig(model=model, tracing_disabled=True),
    )
    # last_agent is the audit answer to "who actually decided this?"
    return result.final_output, result.last_agent.name


# --8<-- example:end
