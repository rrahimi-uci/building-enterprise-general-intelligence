"""Deterministic model double for the offline mortgage baseline."""

from __future__ import annotations

from ..domain.case import MortgageCase
from ..domain.evidence import CaseSummaryCandidate


class ScriptedSummaryModel:
    """Return a fixed evidence summary without network access or side effects."""

    def summarize(self, case: MortgageCase, *, scenario: str) -> CaseSummaryCandidate:
        missing = ("pay_statement",)
        status = "NEEDS_INPUT" if scenario == "missing_income_document" else "CANDIDATE_READY"
        return CaseSummaryCandidate(
            status=status,
            summary=(
                "The synthetic mortgage file contains an application, one pay statement, "
                "and a purchase agreement. A second pay statement is not available."
            ),
            available_document_ids=case.available_document_ids,
            missing_document_kinds=missing,
            evidence_refs=case.available_document_ids,
            proposed_next_control="Collect and verify the missing income document before calculating income-based metrics.",
        )
