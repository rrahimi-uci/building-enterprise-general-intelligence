"""Tracing a manual agent/tool boundary with MLflow.

A trace is the difference between "the agent gave a wrong answer" and "the agent
called the right tool, got stale data, and the staleness was never surfaced".
This example instruments the deterministic shell, not the model: every span is
something the enterprise owns and can assert on.
"""
from __future__ import annotations

import mlflow

# --8<-- example:start


@mlflow.trace(span_type="TOOL")
def lookup_supplier(supplier_id: str) -> dict[str, str]:
    """Tool spans record the arguments and the result, not just the latency."""
    records = {"S-1001": "active", "S-2002": "suspended"}
    return {"supplier_id": supplier_id, "status": records.get(supplier_id, "unknown")}


@mlflow.trace(span_type="AGENT")
def handle_request(supplier_id: str) -> str:
    """The parent span ties every child call into one causally-ordered run."""
    record = lookup_supplier(supplier_id)
    # Attributes carry the decision inputs. Recording *why* a branch was taken
    # is what makes a trace answer questions later, instead of only timing them.
    span = mlflow.get_current_active_span()
    if span is not None:
        span.set_attributes({"supplier.status": record["status"]})
    if record["status"] == "unknown":
        return f"No authorized record for {supplier_id}; escalating to a human."
    return f"Supplier {supplier_id} is {record['status']}."


# --8<-- example:end


def main() -> str:
    mlflow.set_experiment("book-examples")
    return handle_request("S-1001")


if __name__ == "__main__":
    print(main())
