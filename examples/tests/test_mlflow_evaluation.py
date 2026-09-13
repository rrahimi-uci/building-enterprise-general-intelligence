from __future__ import annotations

from examples.observability.mlflow_evaluation import DATASET, evaluate, predict


def test_every_case_passes_both_scorers():
    scores = evaluate()
    assert scores["status_is_correct"] == 1.0
    assert scores["escalates_when_unknown"] == 1.0


def test_unknown_supplier_escalates_rather_than_guessing():
    out = predict("S-4040")
    assert out["status"] == "unknown"
    assert out["escalated"] is True


def test_a_regression_is_actually_detected():
    # Guard the guard: if predict stopped escalating, the suite must fail.
    import examples.observability.mlflow_evaluation as m
    original = m.predict
    m.predict = lambda supplier_id: {"status": "active", "escalated": False}
    try:
        scores = m.evaluate()
        assert scores["status_is_correct"] < 1.0
        assert scores["escalates_when_unknown"] < 1.0
    finally:
        m.predict = original
