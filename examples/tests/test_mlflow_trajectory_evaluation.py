from __future__ import annotations

from examples.observability.mlflow_trajectory_evaluation import (
    no_unknown_effects,
    tool_trajectory_judge,
)


class _TraceWithoutUnknownEffects:
    def search_spans(self):
        return []


def test_deterministic_safety_scorer_is_a_real_mlflow_scorer():
    feedback = no_unknown_effects(trace=_TraceWithoutUnknownEffects())
    assert feedback.value is True
    assert feedback.name == "no_unknown_effects"


def test_model_judge_is_configured_without_running_a_provider_call():
    assert tool_trajectory_judge.name == "tool_trajectory_grounded"
    assert "trace" in tool_trajectory_judge.template_variables
