"""Gate findings routed by kind, and a quality budget that cannot pass by rounding.

Adapted from Policy Logic Forge [R48], commit c22dc450 (MIT):
utils/semantic_routing.py::classify_review_route (routes) and
utils/quality_budget.py::summarize_quality_budget (budget), reduced to the two
properties the book relies on and renamed into its vocabulary. One deliberate
change: a finding of a kind the gate does not recognise goes to a person here,
not to case management. Synthetic data only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

# --8<-- example:start
# --8<-- region:routes
Route = Literal["human_review", "targeted_repair", "case_management"]

REPAIRABLE = {"contract", "structure", "naming", "test_case"}   # deterministic defects
EVIDENCE_GAPS = {"evidence_gap", "unhandled_kind"}


@dataclass(frozen=True)
class Finding:
    """A gate's finding holds an object; it never removes it."""

    object_id: str
    kind: str
    reason: str
    human_required: bool = False   # an explicit judgment finding


def route(findings: Iterable[Finding]) -> Route | None:
    """Only a contradiction or an explicit judgment call needs a person's time.

    A structure defect is repaired narrowly and re-enters the same gate; a gap in
    the evidence is worked as a case; a kind nobody planned for fails closed.
    """
    found = list(findings)
    if not found:
        return None
    if any(f.kind == "contradiction" or f.human_required for f in found):
        return "human_review"
    kinds = {f.kind for f in found}
    if kinds <= REPAIRABLE:
        return "targeted_repair"
    if kinds <= REPAIRABLE | EVIDENCE_GAPS:
        return "case_management"
    return "human_review"
# --8<-- endregion:routes


# --8<-- region:budget
class BudgetError(ValueError):
    """The record's own counts disagree, so no verdict can be read from it."""


@dataclass(frozen=True)
class GateRecord:
    gate: str
    in_release: int    # every object in the effective release: the denominator
    examined: int
    evaluable: int
    held: int          # review-held: still in the release, not evaluable
    refused: int       # refused with a typed reason: still counted


@dataclass(frozen=True)
class Budget:
    denominator: int
    held: int
    maximum_held: int
    passes: bool


def budget(record: GateRecord, rate_percent: int) -> Budget:
    """Held objects against an integer ceiling: floor, never a rounded percentage."""
    counts = (record.in_release, record.examined, record.evaluable, record.held, record.refused)
    if any(c < 0 for c in counts):
        raise BudgetError("counts are non-negative")
    if record.evaluable + record.held + record.refused != record.in_release:
        raise BudgetError("evaluable + held + refused must equal the objects in the release")
    if record.examined != record.in_release:
        raise BudgetError(f"{record.gate} examined {record.examined} of {record.in_release}")
    maximum = record.in_release * rate_percent // 100
    passes = record.examined > 0 and record.held <= maximum   # examined nothing: not a pass
    return Budget(record.in_release, record.held, maximum, passes)
# --8<-- endregion:budget
# --8<-- example:end
