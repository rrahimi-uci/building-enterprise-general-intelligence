"""Integration coverage for the C20-C28 stage wrappers."""

from __future__ import annotations

import pytest

from mortgage_case.domain.case import load_anchor_case
from mortgage_case.platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from mortgage_case.stage_report import StageReport
from mortgage_case.stages import (
    c20_containment,
    c21_identity,
    c22_effects,
    c23_sandbox_privacy,
    c24_tracing,
    c25_evaluation,
    c26_governance,
    c27_release,
    c28_capacity,
)


STAGES = (
    (20, "C20", c20_containment),
    (21, "C21", c21_identity),
    (22, "C22", c22_effects),
    (23, "C23", c23_sandbox_privacy),
    (24, "C24", c24_tracing),
    (25, "C25", c25_evaluation),
    (26, "C26", c26_governance),
    (27, "C27", c27_release),
    (28, "C28", c28_capacity),
)


@pytest.mark.parametrize("chapter, chapter_id, stage", STAGES)
def test_happy_path_wrappers_return_their_checkpoint_report(chapter, chapter_id, stage):
    """Every wrapper delegates to the shared checkpoint composition."""

    assert stage.SCENARIOS == CHECKPOINT_SCENARIOS[chapter]
    report = stage.run()

    assert isinstance(report, StageReport)
    assert report.chapter == chapter_id
    assert report.scenario == "happy_path"
    assert report.status == "completed"
    assert report.case_id == "MORT-2026-000184"


@pytest.mark.parametrize(
    "stage, scenario, expected_status, expected_failure",
    (
        (c20_containment, "malicious_document_instruction", "refused", "PROMPT_INJECTION"),
        (c21_identity, "revoked_loan_officer", "refused", "SUBJECT_REVOKED"),
        (c22_effects, "los_timeout_after_commit", "needs_input", "UNKNOWN_EFFECT"),
        (c23_sandbox_privacy, "sensitive_output", "refused", "DLP_BLOCKED"),
        (c24_tracing, "pii_in_trace", "refused", "TRACE_PRIVACY_VIOLATION"),
        (c25_evaluation, "fairness_slice_regression", "refused", "block"),
        (c26_governance, "expired_exception", "refused", "GOVERNANCE_EXCEPTION_EXPIRED"),
        (c27_release, "incompatible_worker", "refused", "WORKER_INCOMPATIBLE"),
    ),
)
def test_representative_control_failures_are_reported(stage, scenario, expected_status, expected_failure):
    """Security and operations failures stay typed and visible at the stage boundary."""

    report = stage.run(scenario)

    assert report.status == expected_status
    assert expected_failure in report.failures


@pytest.mark.parametrize("_, chapter_id, stage", STAGES)
def test_serialized_reports_do_not_include_sensitive_applicant_display_name(_, chapter_id, stage):
    """All report scenarios serialize identifiers and evidence, never the applicant name."""

    applicant_display_name = load_anchor_case().applicant_display_name

    for scenario in stage.SCENARIOS:
        report = stage.run(scenario)
        assert report.chapter == chapter_id
        assert applicant_display_name not in report.as_json()
