from __future__ import annotations

import pytest
from pydantic import ValidationError

from mortgage_case.domain.case import SYNTHETIC_NOTICE, load_anchor_case
from mortgage_case.domain.evidence import CaseSummaryCandidate
from mortgage_case.stages.c01_baseline import run


def test_anchor_case_is_synthetic_and_stable():
    case = load_anchor_case()
    assert case.case_id == "MORT-2026-000184"
    assert case.synthetic_notice == SYNTHETIC_NOTICE
    assert case.available_document_ids == ("APP-000184", "PAY-000184-01", "PUR-000184")


def test_missing_document_is_reported_without_inventing_a_fact():
    report = run("missing_income_document")
    assert report.status == "needs_input"
    assert report.details["candidate"]["missing_document_kinds"] == ["pay_statement"]
    assert report.details["candidate"]["lending_decision"] == "not_provided"


def test_baseline_has_no_write_or_lending_decision_field():
    with pytest.raises(ValidationError):
        CaseSummaryCandidate(
            status="CANDIDATE_READY",
            summary="unsafe",
            available_document_ids=(),
            proposed_next_control="none",
            lending_decision="approve",  # type: ignore[arg-type]
        )


def test_happy_path_is_only_a_candidate_summary():
    report = run("happy_path")
    assert report.status == "completed"
    assert any("not a lending decision" in item.lower() for item in report.limitations)
