"""The shared contracts must actually enforce what the prose claims they do."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from examples.contracts import (
    AgentDecision, AgentStepRequest, ArtifactRef, CandidatePlan, CloudEvent,
    EvidenceRef, PlanNode, RiskClass, RunManifest, SkillRequirement, ToolCall,
    deduplication_key,
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


def test_a_mutation_is_a_proposed_action_not_a_tool_invocation():
    proposal = AgentDecision(
        disposition="proposed_action",
        tool_call=ToolCall(tool_id="mortgage.document.request@1",
                           arguments={"case_id": "MORT-2026-000184", "document_kind": "pay_statement"}),
    )
    assert proposal.disposition == "proposed_action"


def test_tool_call_carries_an_optional_logical_effect_key():
    call = ToolCall(
        tool_id="mortgage.document.request",
        arguments={"case_id": "MORT-2026-000184", "document_kind": "pay_statement"},
        logical_effect_key="mortgage:document-request:MORT-2026-000184:pay_statement",
    )
    assert call.logical_effect_key == "mortgage:document-request:MORT-2026-000184:pay_statement"
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


def test_risk_is_an_effect_risk_class_never_a_bare_number():
    requirement = SkillRequirement(capability="mortgage.evidence.review",
                                   purpose="mortgage_pre_underwriting_review", region="us",
                                   risk_ceiling="R2")
    assert requirement.risk_ceiling is RiskClass.R2
    assert RiskClass.R1 < requirement.risk_ceiling < RiskClass.R4
    # The JSON form matches the prose: "R2", not 2.
    assert requirement.model_dump(mode="json")["risk_ceiling"] == "R2"
    with pytest.raises(ValidationError, match="bare number"):
        SkillRequirement(capability="c", purpose="p", region="us", risk_ceiling=2)
    with pytest.raises(ValidationError):
        SkillRequirement(capability="c", purpose="p", region="us", risk_ceiling="R5")


def test_plan_nodes_must_declare_their_own_bounds():
    node = PlanNode(id="n1", capability="lookup", maximum_cost_usd=Decimal("0.25"),
                    maximum_attempts=2, risk_class=RiskClass.R1)
    # Every node carries its own cost, attempt, and risk bounds, so a plan cannot
    # be validated without the compiler seeing what each step may spend.
    assert (node.maximum_cost_usd, node.maximum_attempts) == (Decimal("0.25"), 2)
    with pytest.raises(ValidationError, match="Decimal"):
        PlanNode(id="n-float", capability="lookup", maximum_cost_usd=0.25,
                 maximum_attempts=2, risk_class=RiskClass.R1)
    with pytest.raises(ValidationError):
        PlanNode(id="n2", capability="lookup")


DIGEST = "sha256:" + "b" * 64


def run_manifest(**overrides) -> RunManifest:
    fields = dict(
        run_id="RUN-98217", tenant_id="harborlight", subject="user:loan-officer-17",
        actor="spiffe://harborlight/agent-runtime/prod",
        purpose="mortgage_pre_underwriting_review", risk_tier="T3",
        release_manifest=DIGEST, agent="mortgage-evidence-agent@0.1.0",
        runtime={"adapter": "openai-agents-adapter@1.0.0", "sdk": "openai-agents@0.22.2"},
        skills=("mortgage.evidence.read@0.1.0#" + DIGEST,),
        skill_pack="mortgage-evidence@0.1.0#" + DIGEST,
        model_route="reasoning-standard@4",
        knowledge_snapshots=("mortgage-policy@approved-2026.09",),
        capability_envelope="cap_77",
        budget={"usd": "25", "tokens": 300000, "steps": 80, "delegation_depth": 2},
        retention_class="regulated-7y", trace_id="trace-1",
    )
    fields.update(overrides)
    return RunManifest(**fields)


def test_run_manifest_is_written_once_and_never_edited():
    manifest = run_manifest()
    assert manifest.release_manifest == DIGEST
    # A run that needs different versions is a new run, not an edited manifest.
    with pytest.raises(ValidationError):
        manifest.model_route = "reasoning-premium@1"


def test_run_manifest_risk_is_a_use_case_tier_not_a_label_or_effect_class():
    assert run_manifest(risk_tier="T3").risk_tier == "T3"
    for wrong in ("high", "R3", 3):
        with pytest.raises(ValidationError):
            run_manifest(risk_tier=wrong)


def test_skills_and_release_are_pinned_by_digest():
    with pytest.raises(ValidationError):
        run_manifest(skills=("mortgage.evidence.read@latest",))
    with pytest.raises(ValidationError):
        run_manifest(release_manifest="release-2026.09")


def test_artifact_reference_carries_version_and_hash():
    ref = ArtifactRef(artifact_id="art_1", version=1, media_type="application/pdf",
                      sha256=DIGEST, created_by_run="RUN-98217", tenant_id="harborlight",
                      classification="confidential", residency="us")
    with pytest.raises(ValidationError):
        ref.version = 2  # an artifact version is immutable; a change is a new version
    with pytest.raises(ValidationError):
        ArtifactRef(artifact_id="art_1", version=0, media_type="application/pdf",
                    sha256=DIGEST, created_by_run="RUN-98217", tenant_id="harborlight",
                    classification="confidential", residency="us")


def event(**overrides) -> CloudEvent:
    fields = dict(
        id="evt_1", source="urn:harborlight:agent-platform",
        type="com.harborlight.agent.run.status.changed.v1", subject="run/RUN-98217",
        time=datetime(2026, 9, 10, 21, 0, tzinfo=timezone.utc), tenant_id="harborlight",
        correlation_id="RUN-98217", dataref="artifact://event-payload/1", datahash=DIGEST,
    )
    fields.update(overrides)
    return CloudEvent(**fields)


def test_event_payload_travels_by_reference_with_its_hash():
    assert event().data is None
    with pytest.raises(ValidationError, match="travel together"):
        event(datahash=None)
    with pytest.raises(ValidationError, match="travel together"):
        event(dataref=None)


def test_event_source_must_be_a_uri_reference():
    with pytest.raises(ValidationError, match="URI-reference"):
        event(source="agent platform")


def test_consumers_deduplicate_on_source_and_id():
    first, redelivered = event(), event()
    other = event(id="evt_2")
    seen = {deduplication_key(e) for e in (first, redelivered, other)}
    assert seen == {("urn:harborlight:agent-platform", "evt_1"),
                    ("urn:harborlight:agent-platform", "evt_2")}
