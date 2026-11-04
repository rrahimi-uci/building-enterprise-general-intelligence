from __future__ import annotations

import pytest

from mortgage_case.stages import c04_reference_architecture as c04
from mortgage_case.stages import c05_knowledge as c05
from mortgage_case.stages import c06_context as c06
from mortgage_case.stages import c07_paved_road as c07
from mortgage_case.stages import c08_skills as c08
from mortgage_case.stages import c09_skill_pack as c09


CHECKPOINTS = (c04, c05, c06, c07, c08, c09)


def test_happy_path_reports_have_correct_chapter_ids_and_are_redacted():
    for expected_chapter, stage in enumerate(CHECKPOINTS, start=4):
        report = stage.run()

        assert report.chapter == f"C{expected_chapter:02d}"
        assert report.status == "completed"
        assert "Alex Morgan" not in report.as_json()


@pytest.mark.parametrize(
    ("stage", "scenario", "failure"),
    (
        (c04, "unsupported_scenario", None),
        (c05, "contradictory_employer", "POLICY_CONFLICT"),
        (c06, "cross_tenant_case_reference", "CONTEXT_SCOPE_DENIED"),
        (c07, "offline_network_attempt", "OFFLINE_NETWORK_DENIED"),
        (c08, "wrong_region_skill", "SKILL_NOT_ELIGIBLE"),
        (c09, "incompatible_pack", "PACK_INCOMPATIBLE"),
    ),
)
def test_refusal_scenario_per_checkpoint(stage, scenario, failure):
    if failure is None:
        with pytest.raises(ValueError, match="does not define scenario"):
            stage.run(scenario)
        return

    report = stage.run(scenario)
    assert report.status == "refused"
    assert report.failures == (failure,)
    assert "Alex Morgan" not in report.as_json()
