"""A ReAct loop with an explicit budget, so cost cannot run away.

The book's position is that a ReAct trajectory is roughly quadratic in tokens:
every observation re-enters the context. Bounding the loop is therefore a cost
control, not just a safety one. The budget lives outside the model, in a context
object the tools can read and the runner enforces.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from agents import Agent, RunContextWrapper, Runner, function_tool
from agents.run import RunConfig
from mortgage_case.domain.case import load_anchor_case

# --8<-- example:start


@dataclass
class RunBudget:
    """Budget for one run. The model cannot see or change it."""

    case_id: str = load_anchor_case().case_id
    max_tool_calls: int = 3
    tool_calls: int = 0
    exhausted_at: str | None = None

    def consume(self, tool: str) -> bool:
        if self.tool_calls >= self.max_tool_calls:
            self.exhausted_at = tool
            return False
        self.tool_calls += 1
        return True


@function_tool
def search_mortgage_evidence(context: RunContextWrapper[RunBudget], query: str) -> str:
    """Search evidence for the anchor case. Refuses after the run budget."""
    if not context.context.consume("search_mortgage_evidence"):
        # Refusing *as data* keeps the loop bounded without raising: the model can
        # read this, stop, and explain itself rather than retrying blindly.
        return "budget exhausted: no further searches permitted in this run"
    hits = {
        "income": "employment_verification is missing",
        "property": "purchase_agreement is available",
        "title": "title evidence is not in this checkpoint",
    }
    evidence = hits.get(query, f"no mortgage evidence for {query!r}")
    return f"{context.context.case_id}: {evidence}"


def build_agent() -> Agent[RunBudget]:
    return Agent[RunBudget](
        name="Mortgage evidence research",
        instructions=(
            "Research the mortgage case using search_mortgage_evidence. "
            "If the budget is exhausted, summarize what you found and stop."
        ),
        tools=[search_mortgage_evidence],
    )


async def run(question: str, *, budget: RunBudget, model=None) -> str:
    result = await Runner.run(
        build_agent(),
        question,
        context=budget,
        # max_turns is the runner's own stop; the budget is the domain's. Both
        # matter: one bounds the loop, the other bounds what the loop may spend.
        max_turns=8,
        run_config=RunConfig(model=model, tracing_disabled=True),
    )
    return result.final_output


# --8<-- example:end
