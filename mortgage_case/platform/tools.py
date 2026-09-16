"""A read-only Tool Gateway façade for the first two checkpoints."""

from __future__ import annotations

from dataclasses import dataclass

from ..domain.case import MortgageCase
from ..domain.decisions import AgentProposal
from ..domain.errors import ProposalRejected


@dataclass(frozen=True)
class ReadOnlyToolGateway:
    """Expose sanitized case metadata without credentials or mutation methods."""

    case: MortgageCase

    def read_case(self, *, case_id: str, tenant_id: str) -> dict[str, object]:
        if tenant_id != self.case.tenant_id or case_id != self.case.case_id:
            raise ProposalRejected("CASE_SCOPE_DENIED", "the requested case is outside the scoped tenant")
        return {
            "case_id": self.case.case_id,
            "case_version": self.case.case_version,
            "document_ids": list(self.case.available_document_ids),
            "document_kinds": [document.kind for document in self.case.available_documents],
        }


def validate_proposal(proposal: AgentProposal, case: MortgageCase) -> AgentProposal:
    """Validate a proposal before any tool or workflow dispatch."""

    if proposal.case_id != case.case_id:
        raise ProposalRejected("CASE_SCOPE_DENIED", "proposal targets a different case")
    if proposal.case_version != case.case_version:
        raise ProposalRejected("STALE_CASE_VERSION", "proposal was created against an old case version")
    known_refs = set(case.available_document_ids)
    unknown_refs = {
        fact.evidence_ref for fact in proposal.candidate_facts if fact.evidence_ref not in known_refs
    }
    if unknown_refs:
        raise ProposalRejected("UNKNOWN_EVIDENCE_REF", "proposal cites unavailable evidence")
    if proposal.next_command and proposal.next_command.case_id != case.case_id:
        raise ProposalRejected("COMMAND_SCOPE_DENIED", "workflow command targets a different case")
    if proposal.requested_effect != "none":
        raise ProposalRejected("PROTECTED_EFFECT_BLOCKED", "this checkpoint cannot request an external effect")
    return proposal
