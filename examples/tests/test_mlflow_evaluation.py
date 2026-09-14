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


def test_the_scorers_are_the_ones_actually_invoked():
    # The predicates used to be re-implemented inside evaluate(), so a broken
    # scorer scored perfectly. Replacing a scorer must move the reported number.
    import examples.observability.mlflow_evaluation as m

    class AlwaysFails:
        name = "status_is_correct"
        def __call__(self, **kwargs): return False

    original = m.SCORERS
    m.SCORERS = (AlwaysFails(), original[1])
    try:
        assert m.evaluate()["status_is_correct"] == 0.0
    finally:
        m.SCORERS = original


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
