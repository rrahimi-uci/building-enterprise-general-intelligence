"""A bounded mortgage evidence loop with a typed tool, using the OpenAI Agents SDK.

Shows the smallest complete shape of the pattern the book calls a deterministic
shell: the model *proposes* a tool call, the SDK dispatches it, and the tool
itself -- ordinary Python the enterprise owns and tests -- decides what actually
happens. The model never touches the system of record directly.
"""
from __future__ import annotations

import asyncio

from agents import Agent, Runner, function_tool
from agents.run import RunConfig
from mortgage_case.domain.case import load_anchor_case
from pydantic import BaseModel

# --8<-- example:start


class MortgageCaseStatus(BaseModel):
    """The structured answer the agent must produce."""

    case_id: str
    needs_input: bool
    summary: str


# A tool is a normal, testable function. Its type hints become the schema the
# model is allowed to call, so an out-of-contract proposal fails before dispatch.
ANCHOR_CASE_ID = load_anchor_case().case_id


@function_tool
def read_mortgage_case(case_id: str) -> str:
    """Return the evidence status of one synthetic mortgage case."""
    records = {
        ANCHOR_CASE_ID: "missing a second pay_statement",
    }
    status = records.get(case_id)
    if status is None:
        # Returning an error *as data* keeps the loop bounded: the model can
        # react to it, but it cannot escalate its own privileges by retrying.
        return f"no mortgage case record for {case_id}"
    return f"mortgage case {case_id} {status}"


def build_agent() -> Agent:
    # Keep each behavioral instruction explicit and reviewable. These are
    # model-facing hints, not a substitute for gateway authorization.
    instructions = "\n".join(
        [
            "Answer questions about mortgage evidence review.",
            "Always call read_mortgage_case before making a claim about a case.",
        ]
    )
    return Agent(
        name="Mortgage evidence review",
        instructions=instructions,
        tools=[read_mortgage_case],
        # max_turns on the run, plus a declared output type, are what make this
        # a bounded loop rather than an open-ended conversation.
        output_type=MortgageCaseStatus,
    )


async def run(question: str, *, model=None) -> MortgageCaseStatus:
    result = await Runner.run(
        build_agent(),
        question,
        max_turns=4,
        run_config=RunConfig(model=model, tracing_disabled=True),
    )
    return result.final_output


# --8<-- example:end


if __name__ == "__main__":  # pragma: no cover - requires a real model
    print(asyncio.run(run("Does MORT-2026-000184 have all required evidence?")))
