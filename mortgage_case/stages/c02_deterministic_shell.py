"""Chapter 2: typed proposals and deterministic calculation boundaries."""

from __future__ import annotations

from decimal import Decimal

from ..domain.case import load_anchor_case
from ..domain.decisions import AgentProposal, ExtractedFactCandidate, WorkflowCommand
from ..domain.money import calculate_ltv, parse_usd_amount
from ..domain.errors import ProposalRejected
from ..platform.tools import validate_proposal
from ..stage_report import StageReport


SCENARIOS = {"happy_path", "missing_income_document", "stale_case_version", "unsupported_lending_decision"}


def _proposal(scenario: str) -> AgentProposal:
    case = load_anchor_case()
    # Keep the stale value structurally valid so semantic version checking, not
    # schema parsing, owns this failure mode.
    version = 2 if scenario == "stale_case_version" else case.case_version
    proposal = AgentProposal(
        case_id=case.case_id,
        case_version=version,
        summary="The case needs one more income document before income-based review.",
        candidate_facts=(
            ExtractedFactCandidate(
                field_name="purchase_price",
                value=case.purchase_price.removeprefix("USD "),
                evidence_ref="PUR-000184",
                confidence_label="high",
            ),
        ),
        calculations=(
            calculate_ltv(
                parse_usd_amount(case.requested_principal, "requested_principal"),
                parse_usd_amount(case.purchase_price, "purchase_price"),
                evidence_refs=("APP-000184", "PUR-000184"),
            ),
        ),
        next_command=WorkflowCommand(
            command="request_document",
            case_id=case.case_id,
            case_version=version,
            document_kind="pay_statement",
            reason="A second pay statement is required before income can be verified.",
        ),
    )
    if scenario == "unsupported_lending_decision":
        # Extra fields are rejected by the Pydantic contract before dispatch.
        return AgentProposal.model_validate(
            {**proposal.model_dump(), "lending_decision": "approve"}
        )
    return proposal


def run(scenario: str = "happy_path") -> StageReport:
    """Run the deterministic shell and report refusals without side effects."""

    if scenario not in SCENARIOS:
        raise ValueError(f"C02 does not define scenario {scenario!r}")
    case = load_anchor_case()
    try:
        proposal = _proposal(scenario)
        validate_proposal(proposal, case)
    except ProposalRejected as exc:
        return StageReport(
            chapter="C02",
            scenario=scenario,
            case_id=case.case_id,
            status="refused",
            before="The baseline returns a summary but has no typed proposal, calculation, or command boundary.",
            added="Typed candidate facts, a Decimal LTV result, and a read-only workflow command are validated before dispatch.",
            after=f"The proposal was refused safely with {exc.code}; no tool or external effect ran.",
            failures=(exc.code,),
            limitations=("This checkpoint still does not verify income or make a lending decision.",),
        )
    except ValueError as exc:
        return StageReport(
            chapter="C02",
            scenario=scenario,
            case_id=case.case_id,
            status="refused",
            before="The baseline accepts unconstrained model-shaped text.",
            added="The proposal schema rejects fields outside the platform-owned contract.",
            after="The candidate was rejected before dispatch.",
            failures=(type(exc).__name__,),
            limitations=("This is contract validation, not a production policy decision.",),
        )
    return StageReport(
        chapter="C02",
        scenario=scenario,
        case_id=case.case_id,
        status="needs_input",
        before="The baseline returns a summary but has no typed proposal, calculation, or command boundary.",
        added="Typed candidate facts, a Decimal LTV result, and a read-only workflow command are validated before dispatch.",
        after="The system can produce a deterministic request for missing evidence while keeping verification, policy, authority, and effects outside the model.",
        evidence=("APP-000184", "PUR-000184"),
        limitations=(
            "The LTV is an illustrative calculation from synthetic inputs, not an eligibility rule.",
            "DTI remains blocked until income and obligations are verified.",
            "No workflow command sends a document request in this checkpoint.",
        ),
        details={
            "proposal": proposal.model_dump(mode="json"),
            "calculation": proposal.calculations[0].model_dump(mode="json"),
        },
    )
