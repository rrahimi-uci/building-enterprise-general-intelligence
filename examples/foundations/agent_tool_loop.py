"""A bounded agent loop with a typed tool, using the OpenAI Agents SDK.

Shows the smallest complete shape of the pattern the book calls a deterministic
shell: the model *proposes* a tool call, the SDK dispatches it, and the tool
itself -- ordinary Python the enterprise owns and tests -- decides what actually
happens. The model never touches the system of record directly.
"""
from __future__ import annotations

import asyncio

from agents import Agent, Runner, function_tool
from agents.run import RunConfig
from pydantic import BaseModel

# --8<-- example:start


class SupplierStatus(BaseModel):
    """The structured answer the agent must produce."""

    supplier_id: str
    active: bool
    summary: str


# A tool is a normal, testable function. Its type hints become the schema the
# model is allowed to call, so an out-of-contract proposal fails before dispatch.
@function_tool
def lookup_supplier(supplier_id: str) -> str:
    """Return the onboarding status of one supplier record."""
    records = {"S-1001": "active", "S-2002": "suspended"}
    status = records.get(supplier_id)
    if status is None:
        # Returning an error *as data* keeps the loop bounded: the model can
        # react to it, but it cannot escalate its own privileges by retrying.
        return f"no supplier record for {supplier_id}"
    return f"supplier {supplier_id} is {status}"


def build_agent() -> Agent:
    return Agent(
        name="Supplier onboarding",
        instructions=(
            "Answer questions about supplier onboarding. "
            "Always call lookup_supplier before making a claim about a record."
        ),
        tools=[lookup_supplier],
        # max_turns on the run, plus a declared output type, are what make this
        # a bounded loop rather than an open-ended conversation.
        output_type=SupplierStatus,
    )


async def run(question: str, *, model=None) -> SupplierStatus:
    result = await Runner.run(
        build_agent(),
        question,
        max_turns=4,
        run_config=RunConfig(model=model, tracing_disabled=True),
    )
    return result.final_output


# --8<-- example:end


if __name__ == "__main__":  # pragma: no cover - requires a real model
    print(asyncio.run(run("Is supplier S-1001 active?")))
