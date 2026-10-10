from __future__ import annotations

from dataclasses import dataclass

from mlflow.entities import SpanType

from examples.observability.mlflow_trajectory_evaluation import (
    forbidden_tool_absent,
    no_unknown_effects,
    tool_trajectory_judge,
)


@dataclass
class _Span:
    name: str
    span_type: str
    attributes: dict


class _Trace:
    def __init__(self, *spans: _Span):
        self._spans = list(spans)

    def search_spans(self):
        return list(self._spans)


ELIGIBLE = {"eligible_tools": ["mortgage.case.read@1"]}


def test_deterministic_safety_scorer_is_a_real_mlflow_scorer():
    feedback = no_unknown_effects(trace=_Trace())
    assert feedback.value is True
    assert feedback.name == "no_unknown_effects"


def test_unknown_effect_blocks_the_case():
    trace = _Trace(_Span("mortgage.document.request@1", SpanType.TOOL, {"effect.state": "unknown"}))
    assert no_unknown_effects(trace=trace).value is False


def test_eligible_tool_calls_pass():
    trace = _Trace(
        _Span("mortgage-evidence-agent@0.1.0", SpanType.AGENT, {}),
        _Span("mortgage.case.read@1", SpanType.TOOL, {}),
    )
    feedback = forbidden_tool_absent(trace=trace, expectations=ELIGIBLE)
    assert feedback.value is True
    assert feedback.name == "forbidden_tool_absent"


def test_attempted_tool_outside_the_eligible_set_fails_the_case():
    trace = _Trace(
        _Span("mortgage.case.read@1", SpanType.TOOL, {}),
        _Span("los.lookup", SpanType.TOOL, {}),
    )
    feedback = forbidden_tool_absent(trace=trace, expectations=ELIGIBLE)
    assert feedback.value is False
    assert "los.lookup" in feedback.rationale


def test_missing_eligible_set_fails_closed():
    trace = _Trace(_Span("mortgage.case.read@1", SpanType.TOOL, {}))
    assert forbidden_tool_absent(trace=trace, expectations={}).value is False


def test_model_judge_is_configured_without_running_a_provider_call():
    assert tool_trajectory_judge.name == "tool_calls_necessary"
    assert "trace" in tool_trajectory_judge.template_variables
    # Authorization is a deterministic check, never the judge's question.
    assert "authorized trajectory" not in tool_trajectory_judge.instructions
