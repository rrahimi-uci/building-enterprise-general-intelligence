"""The shared contracts must actually enforce what the prose claims they do."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from examples.contracts import (
    AgentDecision, AgentStepRequest, CandidatePlan, EvidenceRef, PlanNode,
    SkillRequirement, ToolCall,
)


def test_evidence_reference_requires_a_verifiable_digest():
    ref = EvidenceRef(uri="s3://records/1", sha256="a" * 64,
                      source_revision="r-9", authorization_decision_id="d-1")
    assert ref.sha256.startswith("a")
    with pytest.raises(ValidationError):
        EvidenceRef(uri="s3://records/1")  # a citation without provenance is not evidence


def test_decision_disposition_is_closed():
    ok = AgentDecision(disposition="answer", answer="done")
    assert ok.disposition == "answer"
    with pytest.raises(ValidationError):
        AgentDecision(disposition="do_whatever")


def test_tool_call_carries_an_optional_logical_effect_key():
    call = ToolCall(
        tool_id="mortgage.document.request",
        arguments={"case_id": "MORT-2026-000184", "document_kind": "employment_verification"},
        logical_effect_key="mortgage:document-request:MORT-2026-000184:employment_verification",
    )
    assert call.logical_effect_key == "mortgage:document-request:MORT-2026-000184:employment_verification"
    assert ToolCall(tool_id="lookup", arguments={}).logical_effect_key is None


def test_step_request_pins_everything_a_replay_needs():
    request = AgentStepRequest(
        run_id="r1", node_id="n1", state_version=3, agent_version="1.4.0",
        context_manifest_id="ctx:1", eligible_tool_versions=frozenset({"mortgage.document.request@1"}),
        max_turns=6, deadline=datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc),
    )
    # A replayable step pins run, state, agent, context, the eligible tool versions,
    # and its own bounds. Dropping any one of them makes the replay a new decision.
    assert (request.state_version, request.agent_version) == (3, "1.4.0")
    assert "mortgage.document.request@1" in request.eligible_tool_versions
    with pytest.raises(ValidationError):
        AgentStepRequest(run_id="r1", node_id="n1", state_version=3,
                         agent_version="1.4.0", context_manifest_id="ctx:1")


def test_plan_nodes_must_declare_their_own_bounds():
    SkillRequirement(capability="mortgage.evidence.review",
                     purpose="mortgage_pre_underwriting_review", region="us",
                     maximum_risk=2)
    node = PlanNode(id="n1", capability="lookup", maximum_cost_usd=Decimal("0.25"),
                    maximum_attempts=2, risk_class=1)
    # Every node carries its own cost, attempt, and risk bounds, so a plan cannot
    # be approved without the reviewer seeing what each step may spend.
    assert (node.maximum_cost_usd, node.maximum_attempts) == (Decimal("0.25"), 2)
    with pytest.raises(ValidationError, match="Decimal"):
        PlanNode(id="n-float", capability="lookup", maximum_cost_usd=0.25,
                 maximum_attempts=2, risk_class=1)
    with pytest.raises(ValidationError):
        PlanNode(id="n2", capability="lookup")
