"""Behaviour of gate routing and the fixed-denominator budget.

Two cases are adapted from Policy Logic Forge [R48] (tests/test_semantic_routing.py
and tests/test_quality_budget.py, commit c22dc450, MIT); the fixtures are the
Harborlight age-window change with invented finding kinds and counts.
"""
from __future__ import annotations

import pytest

from examples.knowledge.gate_record import BudgetError, Finding, GateRecord, budget, route


def test_only_a_positive_contradiction_or_judgment_finding_enters_human_review():
    assert route([Finding("CTL-age-window", "contradiction", "two thresholds, one subject")]) == "human_review"
    assert route([Finding("OBL-income", "evidence_gap", "owner must decide scope",
                          human_required=True)]) == "human_review"
    assert route([Finding("CTL-age-window", "contract", "missing effective_from")]) != "human_review"


def test_a_contract_defect_routes_to_targeted_repair_not_case_management():
    assert route([Finding("CTL-age-window", "contract", "missing effective_from"),
                  Finding("CTL-age-window", "naming", "id not canonical")]) == "targeted_repair"


def test_an_evidence_gap_routes_to_case_management():
    assert route([Finding("REQ-income", "evidence_gap", "span not located"),
                  Finding("CTL-age-window", "contract", "missing owner")]) == "case_management"


def test_a_finding_of_unknown_kind_fails_closed_to_human_review():
    assert route([Finding("X-1", "something_new", "no route was planned")]) == "human_review"


def test_no_findings_means_no_route():
    assert route([]) is None


def record(**overrides) -> GateRecord:
    values = dict(gate="grounding", in_release=437, examined=437, evaluable=360, held=43, refused=34)
    return GateRecord(**(values | overrides))


def test_the_budget_is_an_integer_floor_so_rounding_cannot_pass():
    # 10% of 437 is 43.7: 43 held passes, 44 does not, although both "round" to 10%.
    assert budget(record(), 10).maximum_held == 43
    assert budget(record(), 10).passes
    assert not budget(record(evaluable=359, held=44), 10).passes


def test_a_record_whose_cohorts_do_not_reconcile_is_refused():
    with pytest.raises(BudgetError):
        budget(record(held=10), 10)          # 33 objects vanished from the counts


def test_held_and_refused_objects_stay_in_the_denominator():
    result = budget(record(), 10)
    assert result.denominator == 437         # not 360, the evaluable subset
    with pytest.raises(BudgetError):
        budget(record(in_release=360, examined=360), 10)   # dropping held and refused


def test_a_gate_that_examined_nothing_reports_zero_not_pass():
    empty = budget(GateRecord("regression", 0, 0, 0, 0, 0), 10)
    assert (empty.denominator, empty.passes) == (0, False)
    with pytest.raises(BudgetError):
        budget(record(examined=400), 10)     # skipped work is not a pass either
