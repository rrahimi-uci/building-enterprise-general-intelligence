"""Evaluating an agent against a dataset with MLflow, offline.

The book's position is that an evaluation suite should be grown from production
failures, and that a judge you have not calibrated is just another model with
its own drift. This example keeps the scorers deterministic so the mechanics are
visible without a live judge in the loop.
"""
from __future__ import annotations

import mlflow
from mlflow.genai.scorers import scorer

# --8<-- example:start

# These are controlled synthetic cases, not production incidents. A production
# dataset needs its own privacy, purpose, leakage, and retention review.
DATASET = [
    {"inputs": {"supplier_id": "S-1001"}, "expectations": {"status": "active"}},
    {"inputs": {"supplier_id": "S-2002"}, "expectations": {"status": "suspended"}},
    {"inputs": {"supplier_id": "S-9999"}, "expectations": {"status": "unknown"}},
]


@scorer
def status_is_correct(outputs: dict, expectations: dict) -> bool:
    """A deterministic check. Prefer one wherever the answer is checkable."""
    return outputs.get("status") == expectations.get("status")


@scorer
def escalates_when_unknown(outputs: dict, expectations: dict) -> bool:
    """Unknown records must escalate rather than guess -- the failure that matters."""
    if expectations.get("status") != "unknown":
        return True
    return bool(outputs.get("escalated"))


def predict(supplier_id: str) -> dict:
    """The system under evaluation."""
    records = {"S-1001": "active", "S-2002": "suspended"}
    status = records.get(supplier_id, "unknown")
    return {"status": status, "escalated": status == "unknown"}


# The scorers are the thing under test as much as the system is. Invoking them
# here -- rather than re-implementing their predicates inline -- is what makes a
# regression in a scorer visible. A scorer nobody has seen fail is not evidence.
SCORERS = (status_is_correct, escalates_when_unknown)


def evaluate_result():
    """Run MLflow's evaluation orchestration and return its result object."""
    mlflow.set_experiment("book-mortgage-evaluation")
    return mlflow.genai.evaluate(
        data=DATASET,
        predict_fn=predict,
        scorers=list(SCORERS),
    )


def evaluate() -> dict[str, float]:
    """Return the mean metrics produced by ``mlflow.genai.evaluate``."""
    result = evaluate_result()
    return {
        scorer_fn.name: float(result.metrics[f"{scorer_fn.name}/mean"])
        for scorer_fn in SCORERS
    }


# --8<-- example:end
