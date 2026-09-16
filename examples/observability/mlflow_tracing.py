"""Tracing a manual agent/tool boundary with MLflow.

A trace is the difference between "the agent gave a wrong answer" and "the agent
called the right tool, got stale data, and the staleness was never surfaced".
This example instruments the deterministic shell, not the model: every span is
something the enterprise owns and can assert on.
"""
from __future__ import annotations

import mlflow
from mortgage_case.domain.case import load_anchor_case

# --8<-- example:start


ANCHOR_CASE_ID = load_anchor_case().case_id


@mlflow.trace(span_type="TOOL")
def read_mortgage_case(case_id: str) -> dict[str, str]:
    """Tool spans record the arguments and the result, not just the latency."""
    records = {ANCHOR_CASE_ID: "needs_input"}
    return {"case_id": case_id, "status": records.get(case_id, "unknown")}


@mlflow.trace(span_type="AGENT")
def handle_request(case_id: str) -> str:
    """The parent span ties every child call into one causally-ordered run."""
    record = read_mortgage_case(case_id)
    # Attributes carry the decision inputs. Recording *why* a branch was taken
    # is what makes a trace answer questions later, instead of only timing them.
    span = mlflow.get_current_active_span()
    if span is not None:
        span.set_attributes({"mortgage.case.status": record["status"]})
    if record["status"] == "unknown":
        return f"No authorized mortgage case for {case_id}; escalating to a human."
    return f"Mortgage case {case_id} is {record['status']}."


# --8<-- example:end


def main() -> str:
    mlflow.set_experiment("book-mortgage-evidence-review")
    return handle_request("MORT-2026-000184")


if __name__ == "__main__":
    print(main())
