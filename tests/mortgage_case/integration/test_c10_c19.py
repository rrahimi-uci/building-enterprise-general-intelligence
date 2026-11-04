"""Integration coverage for the C10-C19 cumulative stage wrappers."""

from __future__ import annotations

from importlib import import_module

import pytest

from mortgage_case.domain.case import load_anchor_case
from mortgage_case.platform.checkpoints import (
    SCENARIOS as CHECKPOINT_SCENARIOS,
    case_evidence_snapshot_digest,
)


STAGES = tuple(
    (f"c{chapter:02d}", chapter, module_name)
    for chapter, module_name in (
        (10, "c10_react"),
        (11, "c11_routing"),
        (12, "c12_planning"),
        (13, "c13_reflection"),
        (14, "c14_human_review"),
        (15, "c15_durable"),
        (16, "c16_patterns"),
        (17, "c17_anti_patterns"),
        (18, "c18_multi_agent"),
        (19, "c19_protocols"),
    )
)


@pytest.mark.parametrize("label, chapter, module_name", STAGES, ids=lambda item: str(item))
def test_happy_path_reports_are_exposed_by_each_wrapper(label: str, chapter: int, module_name: str):
    """Every wrapper delegates to the shared composition and preserves Cxx."""

    stage = import_module(f"mortgage_case.stages.{module_name}")

    report = stage.run()

    assert report.chapter == f"C{chapter:02d}"
    assert report.scenario == "happy_path"
    assert report.status == "completed"
    assert report.evidence
    assert stage.SCENARIOS == CHECKPOINT_SCENARIOS[chapter]


@pytest.mark.parametrize(
    "module_name, scenario, failure",
    (
        ("c10_react", "repeated_observation", "NO_PROGRESS"),
        ("c11_routing", "ambiguous_route", "ROUTE_AMBIGUOUS"),
        ("c12_planning", "plan_cycle", "PLAN_CYCLE"),
        ("c13_reflection", "self_approval", "SELF_APPROVAL"),
        ("c14_human_review", "approval_changed_case", "STALE_CASE_VERSION"),
        ("c14_human_review", "approval_changed_evidence", "STALE_EVIDENCE_SNAPSHOT"),
        ("c14_human_review", "approval_changed_policy", "STALE_POLICY_VERSION"),
        ("c18_multi_agent", "scope_expansion", "SCOPE_EXPANSION"),
        ("c19_protocols", "malicious_remote_artifact", "REMOTE_ARTIFACT_REJECTED"),
    ),
)
def test_representative_refusals_are_reported_without_raising(module_name: str, scenario: str, failure: str):
    """Representative safety boundaries remain visible as typed refusals."""

    stage = import_module(f"mortgage_case.stages.{module_name}")

    report = stage.run(scenario)

    assert report.status == "refused"
    assert report.failures == (failure,)


def test_c10_provider_outage_retains_partial_observation_in_needs_input_report():
    from mortgage_case.stages import c10_react

    report = c10_react.run("provider_outage")

    assert report.status == "needs_input"
    assert report.failures == ("PROVIDER_UNAVAILABLE",)
    assert report.evidence == ("OBS-01",)
    assert report.details["observations"] == ("application",)
    assert report.details["partial_observation_retained"] is True


def test_c13_contradictory_candidate_is_held_even_when_critique_is_empty_or_misses_it():
    from mortgage_case.stages import c13_reflection

    report = c13_reflection.run("contradictory_candidate")

    assert report.status == "needs_input"
    assert report.details["critique"]["findings"] == []
    assert report.details["acceptance"]["accepted"] is False
    assert "candidate_claims_contradict_evidence" in report.failures


def test_c14_evidence_snapshot_changes_when_content_changes_under_the_same_document_id():
    case = load_anchor_case()
    changed_documents = tuple(
        document.model_copy(update={"sha256": "f" * 64})
        if index == 0
        else document
        for index, document in enumerate(case.available_documents)
    )

    assert tuple(document.document_id for document in changed_documents) == case.available_document_ids
    assert case_evidence_snapshot_digest(case) != case_evidence_snapshot_digest(
        case,
        documents=changed_documents,
    )


def test_c15_duplicate_signal_is_deduplicated_in_event_projection_and_outbox():
    """A redelivered durable signal creates one event and one transition."""

    from mortgage_case.stages import c15_durable

    report = c15_durable.run("duplicate_document_event")

    assert report.status == "completed"
    assert report.details["deduplicated"] is True
    assert report.details["event_count"] == 2
    assert report.details["outbox_event_count"] == 2
    assert report.details["replayed_projection"]["signals"] == 1
    assert report.details["duplicate_event_id"] == report.evidence[0]


@pytest.mark.parametrize("label, chapter, module_name", STAGES, ids=lambda item: str(item))
def test_serialized_reports_do_not_expose_applicant_display_name(label: str, chapter: int, module_name: str):
    """No serialized checkpoint scenario leaks the fixture's display name."""

    stage = import_module(f"mortgage_case.stages.{module_name}")

    for scenario in stage.SCENARIOS:
        assert "Alex Morgan" not in stage.run(scenario).as_json()
