"""Chapter 1's ten-line prototype and the four agent levels, runnable offline.

The prototype is deliberately incomplete. `request_mortgage_document` writes
straight into an in-memory list: no authorization, no idempotency key, no
receipt. The tests use that gap to reproduce the chapter's Wednesday failure --
a retried request creates a second document request -- which is the point of
showing the prototype at all. Nothing here is a pattern to copy.
"""
from __future__ import annotations

import asyncio
from decimal import Decimal

from agents import Agent, Runner, function_tool
from agents.run import RunConfig
from openai import OpenAI

CASE_ID = "MORT-2026-000184"


class CaseGateway:
    """A stand-in for the case store the level-two tool reads."""

    def __init__(self) -> None:
        self._status = {CASE_ID: "second pay statement missing"}

    def status(self, case_id: str) -> str:
        return self._status.get(case_id, f"no mortgage case record for {case_id}")


case_gateway = CaseGateway()

# The prototype's only "system of record" for document requests. A real one
# would deduplicate on a logical effect key; this one, on purpose, does not.
DOCUMENT_REQUESTS: list[tuple[str, str]] = []


@function_tool
def calculate_ltv(loan_amount: str, property_value: str) -> str:
    """Return the loan-to-value ratio for two decimal amounts."""
    return str((Decimal(loan_amount) / Decimal(property_value)).quantize(Decimal("0.0001")))


@function_tool
def request_mortgage_document(case_id: str, document_kind: str) -> str:
    """Ask the applicant for a document. Unprotected: every call is a new request."""
    DOCUMENT_REQUESTS.append((case_id, document_kind))
    return f"document request {len(DOCUMENT_REQUESTS)} created for {case_id}"


# --8<-- example:start
# --8<-- region:level-two
@function_tool
def read_mortgage_case(case_id: str) -> str:
    """Return the evidence status of one mortgage case."""
    return case_gateway.status(case_id)          # your code, your case store
# --8<-- endregion:level-two


# --8<-- region:demo
agent = Agent(
    name="Mortgage evidence review",
    instructions="Review authorized mortgage evidence and identify missing inputs.",
    tools=[read_mortgage_case, calculate_ltv, request_mortgage_document],
)

async def review(case_id: str, model=None) -> str:
    result = await Runner.run(agent, f"Review mortgage case {case_id}",
                              run_config=RunConfig(model=model))
    return result.final_output   # "A second pay statement is missing."
# --8<-- endregion:demo


# --8<-- region:level-one
def summarize(client: OpenAI, evidence_metadata: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="Summarize this authorized mortgage evidence metadata: " + evidence_metadata,
    )
    return response.output_text
# --8<-- endregion:level-one


# --8<-- region:level-three
async def review_in_a_loop(case_id: str, model=None) -> str:
    result = await Runner.run(agent, f"Review mortgage case {case_id}",
                              max_turns=8, run_config=RunConfig(model=model))
    return result.final_output
# --8<-- endregion:level-three
# --8<-- example:end


if __name__ == "__main__":  # pragma: no cover - requires a real model and key
    print(asyncio.run(review(CASE_ID)))
