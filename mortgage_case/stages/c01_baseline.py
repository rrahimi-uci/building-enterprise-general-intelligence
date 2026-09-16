"""Chapter 1: honest, read-only mortgage evidence summary."""

from __future__ import annotations

from ..adapters.scripted_model import ScriptedSummaryModel
from ..domain.case import load_anchor_case
from ..stage_report import StageReport


SCENARIOS = {"happy_path", "missing_income_document"}


def run(scenario: str = "happy_path") -> StageReport:
    """Run the first checkpoint without network access or protected tools."""

    if scenario not in SCENARIOS:
        raise ValueError(f"C01 does not define scenario {scenario!r}")
    case = load_anchor_case()
    candidate = ScriptedSummaryModel().summarize(case, scenario=scenario)
    status = "needs_input" if candidate.status == "NEEDS_INPUT" else "completed"
    return StageReport(
        chapter="C01",
        scenario=scenario,
        case_id=case.case_id,
        status=status,
        before="There is no executable mortgage case; a prototype could be mistaken for an autonomous underwriter.",
        added="A deterministic, read-only summary of the synthetic anchor case and its available evidence.",
        after="The system can identify available and missing evidence, but it cannot verify facts, calculate authoritative metrics, write to an LOS, or make a lending decision.",
        evidence=case.available_document_ids,
        limitations=(
            "The summary is a model candidate, not verified evidence.",
            "The candidate summary is not a lending decision.",
            "No approval, denial, rate, adverse-action reason, or external effect is produced.",
            "The fixture is synthetic and not suitable for real credit decisions.",
        ),
        details={"candidate": candidate.model_dump(mode="json")},
    )
