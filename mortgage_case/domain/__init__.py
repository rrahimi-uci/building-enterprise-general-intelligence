"""Domain contracts for the synthetic mortgage case."""

from .case import MortgageCase, SyntheticDocument
from .decisions import AgentProposal, ExtractedFactCandidate, WorkflowCommand
from .evidence import CaseSummaryCandidate
from .money import CalculationResult

__all__ = [
    "AgentProposal",
    "CalculationResult",
    "CaseSummaryCandidate",
    "ExtractedFactCandidate",
    "MortgageCase",
    "SyntheticDocument",
    "WorkflowCommand",
]
