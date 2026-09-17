"""Deterministic platform doubles used by the cumulative mortgage checkpoints.

The module deliberately keeps provider mechanics out of the contracts.  These
objects are small, offline-safe teaching implementations: they model the
ownership and failure boundaries that a production service would enforce, but
they do not claim to be a credit policy, security certification, or LOS.
"""

from __future__ import annotations

import hashlib
import ipaddress
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..domain.case import MortgageCase
from ..domain.errors import MortgageCaseError, ProposalRejected


UTC = timezone.utc
NOW = datetime(2026, 9, 16, 12, 0, tzinfo=UTC)


def canonical_json(value: Any) -> str:
    """Serialize platform values with stable ordering and decimal strings."""

    def normalize(item: Any) -> Any:
        if isinstance(item, BaseModel):
            return normalize(item.model_dump(mode="python"))
        if isinstance(item, Decimal):
            return str(item)
        if isinstance(item, datetime):
            return item.astimezone(UTC).isoformat().replace("+00:00", "Z")
        if isinstance(item, dict):
            return {str(k): normalize(v) for k, v in sorted(item.items(), key=lambda pair: str(pair[0]))}
        if isinstance(item, (tuple, list)):
            return [normalize(v) for v in item]
        if isinstance(item, (set, frozenset)):
            values = [normalize(v) for v in item]
            return sorted(values, key=lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return item

    return json.dumps(normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    """Return the SHA-256 digest used by immutable teaching records."""

    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


class PrincipalContext(BaseModel):
    """Non-executable subject/actor context carried by a run."""

    model_config = ConfigDict(extra="forbid")

    tenant_id: str
    subject_id: str
    actor_id: str
    purpose: str
    region: str
    risk: Literal["low", "medium", "high"] = "medium"


class CapabilityScope(BaseModel):
    """Requested scope; this is metadata until C21 authorization."""

    model_config = ConfigDict(extra="forbid")

    actions: frozenset[str] = frozenset()
    resources: frozenset[str] = frozenset()
    data_classes: frozenset[str] = frozenset()
    purpose: str
    region: str
    expires_at: datetime
    max_cost: Decimal = Decimal("10.00")
    depth: int = Field(default=0, ge=0, le=8)

    @field_validator("expires_at")
    @classmethod
    def utc_expiry(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")
        return value.astimezone(UTC)


def narrow_scope(parent: CapabilityScope, child: CapabilityScope) -> CapabilityScope:
    """Intersect a child scope and reject every attempted expansion."""

    if child.purpose != parent.purpose or child.region != parent.region:
        raise ProposalRejected("SCOPE_EXPANSION", "child purpose or region is broader than its parent")
    if not child.actions <= parent.actions or not child.resources <= parent.resources:
        raise ProposalRejected("SCOPE_EXPANSION", "child action or resource scope is broader than its parent")
    if not child.data_classes <= parent.data_classes or child.depth > parent.depth + 1:
        raise ProposalRejected("SCOPE_EXPANSION", "child data or delegation depth is broader than its parent")
    if child.max_cost > parent.max_cost or child.expires_at > parent.expires_at:
        raise ProposalRejected("SCOPE_EXPANSION", "child time or cost budget is broader than its parent")
    return child


class Artifact(BaseModel):
    """Immutable evidence/result reference; raw document bytes stay elsewhere."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    kind: str
    source_revision: str
    content_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    classification: Literal["synthetic", "restricted", "public"] = "synthetic"
    adopted: bool = False


class RunManifest(BaseModel):
    """Pinned run identity and intended scope, not an authorization decision."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    case_id: str
    tenant_id: str
    principal: PrincipalContext
    requested_scope: CapabilityScope
    workflow_version: str
    release_digest: str
    synthetic: Literal[True] = True


class WorkflowEvent(BaseModel):
    """Append-only event used by the replayable teaching workflow."""

    model_config = ConfigDict(extra="forbid")

    event_id: str
    run_id: str
    sequence: int = Field(ge=1)
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = None


class EventStore:
    """In-memory event/outbox store with duplicate and conflict detection."""

    def __init__(self) -> None:
        self.events: dict[str, list[WorkflowEvent]] = {}
        self.keys: dict[str, WorkflowEvent] = {}
        self.outbox: list[WorkflowEvent] = []

    def append(self, run_id: str, event_type: str, payload: dict[str, Any], *, idempotency_key: str | None = None) -> WorkflowEvent:
        if idempotency_key and idempotency_key in self.keys:
            previous = self.keys[idempotency_key]
            if (
                previous.run_id != run_id
                or digest(previous.payload) != digest(payload)
                or previous.event_type != event_type
            ):
                raise ProposalRejected("IDEMPOTENCY_CONFLICT", "the idempotency key was reused for different intent")
            return previous
        sequence = len(self.events.setdefault(run_id, [])) + 1
        event = WorkflowEvent(
            event_id=f"EVT-{run_id}-{sequence:04d}",
            run_id=run_id,
            sequence=sequence,
            event_type=event_type,
            payload=payload,
            idempotency_key=idempotency_key,
        )
        self.events[run_id].append(event)
        self.outbox.append(event)
        if idempotency_key:
            self.keys[idempotency_key] = event
        return event

    def read(self, run_id: str) -> tuple[WorkflowEvent, ...]:
        return tuple(self.events.get(run_id, ()))

    def publish_outbox(self) -> tuple[WorkflowEvent, ...]:
        published = tuple(self.outbox)
        self.outbox.clear()
        return published


class ReferenceArchitecture:
    """Start/status/signal/cancel façade backed by the event store."""

    def __init__(self) -> None:
        self.events = EventStore()
        self.manifests: dict[str, RunManifest] = {}

    def start(self, manifest: RunManifest, *, idempotency_key: str) -> RunManifest:
        existing = self.manifests.get(manifest.run_id)
        if existing:
            if digest(existing) != digest(manifest):
                raise ProposalRejected("START_CONFLICT", "run ID already has a different manifest")
            return existing
        self.manifests[manifest.run_id] = manifest
        self.events.append(manifest.run_id, "RunStarted", {"case_id": manifest.case_id}, idempotency_key=idempotency_key)
        return manifest

    def signal(self, run_id: str, name: str, payload: dict[str, Any], *, idempotency_key: str) -> WorkflowEvent:
        if run_id not in self.manifests:
            raise ProposalRejected("RUN_NOT_FOUND", "signal targets an unknown run")
        return self.events.append(run_id, "SignalReceived", {"name": name, **payload}, idempotency_key=idempotency_key)

    def cancel(self, run_id: str, *, reason: str, idempotency_key: str) -> WorkflowEvent:
        if run_id not in self.manifests:
            raise ProposalRejected("RUN_NOT_FOUND", "cancellation targets an unknown run")
        return self.events.append(run_id, "RunCancelled", {"reason": reason}, idempotency_key=idempotency_key)


class KnowledgeObject(BaseModel):
    """Versioned source object with scope, freshness, owner, and digest."""

    model_config = ConfigDict(extra="forbid")

    object_id: str
    source_revision: str
    owner: str
    scope: str
    effective_from: datetime
    effective_to: datetime | None = None
    content: str
    content_digest: str


class Rule(BaseModel):
    """Deterministic projection of a fictional training policy."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str
    object_id: str
    policy_version: str
    required_documents: frozenset[str]
    prohibited_conditions: frozenset[str] = frozenset()
    reason_code: str


class KnowledgeStore:
    def __init__(self) -> None:
        policy = KnowledgeObject(
            object_id="KNOW-MORTGAGE-POLICY-2026.09",
            source_revision="mortgage-policy@2026.09",
            owner="harborlight-policy-team",
            scope="harborlight-us-west:mortgage_pre_underwriting_review",
            effective_from=datetime(2026, 9, 1, tzinfo=UTC),
            content="Synthetic training rule: income evidence must be current and internally consistent.",
            content_digest=digest("income-evidence-rule"),
        )
        self.objects = {policy.object_id: policy}
        self.rules = {
            "mortgage-policy@2026.09": Rule(
                rule_id="RULE-INCOME-FRESHNESS-1",
                object_id=policy.object_id,
                policy_version="mortgage-policy@2026.09",
                required_documents=frozenset({"mortgage_application", "pay_statement", "purchase_agreement"}),
                prohibited_conditions=frozenset({"contradictory_employer", "stale_credit_artifact"}),
                reason_code="EVIDENCE_NOT_READY",
            )
        }

    def get_rule(self, version: str) -> Rule:
        try:
            return self.rules[version]
        except KeyError as exc:
            raise ProposalRejected("POLICY_NOT_FOUND", "the policy revision is not registered") from exc


class MemoryRecord(BaseModel):
    """Run-scoped memory with explicit provenance and retention."""

    model_config = ConfigDict(extra="forbid")

    memory_id: str
    run_id: str
    value: str
    source_refs: tuple[str, ...]
    trust: Literal["derived", "user_supplied"] = "derived"
    expires_at: datetime
    deleted: bool = False


class ContextManifest(BaseModel):
    """Exact authorized projection shown to a model-facing activity."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    tenant_id: str
    case_id: str
    source_revisions: tuple[str, ...]
    artifact_ids: tuple[str, ...]
    redacted_fields: tuple[str, ...]
    trust_labels: tuple[str, ...]
    token_budget: int = Field(ge=1)
    manifest_digest: str


def build_context(case: MortgageCase, manifest: RunManifest, *, artifact_ids: tuple[str, ...], source_revisions: tuple[str, ...], allowed_case_id: str, token_budget: int = 1200) -> ContextManifest:
    """Authorize case identity before materializing a reproducible projection."""

    if (
        allowed_case_id != case.case_id
        or manifest.case_id != case.case_id
        or manifest.tenant_id != case.tenant_id
        or manifest.principal.tenant_id != case.tenant_id
        or manifest.principal.purpose != case.purpose
    ):
        raise ProposalRejected("CONTEXT_SCOPE_DENIED", "case or tenant is outside the run scope")
    payload = {
        "run_id": manifest.run_id,
        "tenant_id": manifest.tenant_id,
        "case_id": case.case_id,
        "source_revisions": source_revisions,
        "artifact_ids": artifact_ids,
        "redacted_fields": ("applicant_display_name", "property_address", "account_numbers"),
        "trust_labels": ("synthetic", "retrieved", "untrusted_text_excluded"),
        "token_budget": token_budget,
    }
    return ContextManifest(**payload, manifest_digest=digest(payload))


class SkillManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_id: str
    version: str
    digest: str
    owner: str
    required_tools: frozenset[str]
    policy_version: str
    regions: frozenset[str]
    status: Literal["active", "revoked", "deprecated"] = "active"


class SkillRegistry:
    def __init__(self) -> None:
        self.skills = [
            SkillManifest(skill_id="mortgage.income.reconcile", version="1.1.0", digest=digest("income-1.1.0"), owner="mortgage-domain", required_tools=frozenset({"mortgage.case.read@1"}), policy_version="mortgage-policy@2026.09", regions=frozenset({"us-west"})),
            SkillManifest(skill_id="mortgage.review.prepare", version="1.0.0", digest=digest("review-1.0.0"), owner="mortgage-domain", required_tools=frozenset({"mortgage.case.read@1", "mortgage.policy.read@1"}), policy_version="mortgage-policy@2026.09", regions=frozenset({"us-west"})),
        ]

    def resolve(self, skill_id: str, *, region: str, policy_version: str, allow_revoked: bool = False) -> SkillManifest:
        candidates = [s for s in self.skills if s.skill_id == skill_id and region in s.regions and s.policy_version == policy_version and (allow_revoked or s.status == "active")]
        if not candidates:
            raise ProposalRejected("SKILL_NOT_ELIGIBLE", "no active skill satisfies the requested region and policy")
        return sorted(candidates, key=lambda s: tuple(int(v) for v in s.version.split(".")), reverse=True)[0]


class SkillPack(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str
    version: str
    digest: str
    skills: tuple[str, ...]
    policy_version: str
    workflow_version: str
    evaluation_version: str
    regions: frozenset[str]
    status: Literal["active", "revoked"] = "active"


class PlanNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node_id: str
    capability: str
    depends_on: tuple[str, ...] = ()
    estimated_cost: Decimal = Decimal("1.00")
    read_only: bool = True


class PlanRevision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: str
    version: int = Field(ge=1)
    case_id: str
    policy_version: str
    nodes: tuple[PlanNode, ...]
    plan_digest: str


def compile_plan(case_id: str, policy_version: str, nodes: tuple[PlanNode, ...], allowed_capabilities: frozenset[str]) -> PlanRevision:
    """Compile a proposed graph before any node is schedulable."""

    names = {node.node_id for node in nodes}
    if len(names) != len(nodes) or any(dep not in names for node in nodes for dep in node.depends_on):
        raise ProposalRejected("INVALID_PLAN_GRAPH", "plan contains duplicate nodes or missing dependencies")
    if any(node.capability not in allowed_capabilities for node in nodes):
        raise ProposalRejected("PLAN_CAPABILITY_DENIED", "plan contains an ineligible capability")
    # Kahn's algorithm keeps cycle detection deterministic and dependency-only.
    remaining = {node.node_id: set(node.depends_on) for node in nodes}
    visited: set[str] = set()
    while remaining:
        ready = sorted(node for node, deps in remaining.items() if not deps)
        if not ready:
            raise ProposalRejected("PLAN_CYCLE", "plan graph contains a cycle")
        for node in ready:
            visited.add(node)
            remaining.pop(node)
            for deps in remaining.values():
                deps.discard(node)
    payload = {"case_id": case_id, "policy_version": policy_version, "nodes": nodes}
    return PlanRevision(
        plan_id=f"PLAN-{case_id}",
        version=1,
        case_id=case_id,
        policy_version=policy_version,
        nodes=nodes,
        plan_digest=digest(payload),
    )


class Budget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_turns: int = Field(ge=1, le=20)
    max_tool_calls: int = Field(ge=0, le=50)
    max_cost: Decimal = Decimal("10.00")
    max_seconds: int = Field(ge=1, le=3600)


def bounded_react(observations: tuple[str, ...], budget: Budget) -> tuple[str, ...]:
    """Stop on repeated observations or an exhausted external budget."""

    if len(observations) > budget.max_turns or len(observations) > budget.max_tool_calls:
        raise ProposalRejected("REACT_BUDGET_EXCEEDED", "the controller budget ended the reasoning loop")
    if len(set(observations)) != len(observations):
        raise ProposalRejected("NO_PROGRESS", "the loop repeated an identical observation")
    return observations


class RouteDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    route: Literal["income", "property", "policy", "underwriter", "human"]
    reason_code: str
    confidence: Decimal = Decimal("1.00")
    eligible: bool = True
    owner: str


class OwnershipTransfer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transfer_id: str
    previous_owner: str
    new_owner: str
    acknowledged: bool = False
    cancellation_lineage: tuple[str, ...] = ()


class HumanActionAuthorizationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    authorization_id: str
    case_id: str
    action: str
    resource: str
    proposal_hash: str
    case_version: int = Field(ge=1)
    policy_version: str
    expires_at: datetime
    required_role: str
    status: Literal["pending", "authorized", "rejected", "expired"] = "pending"

    @field_validator("expires_at")
    @classmethod
    def utc_expiry(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")
        return value.astimezone(UTC)


class HumanActionAuthorizationDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    authorization_id: str
    proposal_hash: str
    approver_id: str
    approver_role: str
    decision: Literal["authorize", "reject"]
    decided_at: datetime
    reason: str

    @field_validator("decided_at")
    @classmethod
    def utc_decision_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("decided_at must be timezone-aware")
        return value.astimezone(UTC)


def proposal_hash(action: str, resource: str, arguments: dict[str, Any], case_version: int) -> str:
    return digest({"action": action, "resource": resource, "arguments": arguments, "case_version": case_version})


def verify_action_authorization(request: HumanActionAuthorizationRequest, decision: HumanActionAuthorizationDecision, *, current_case_version: int, now: datetime = NOW) -> None:
    if request.status != "authorized" or decision.decision != "authorize":
        raise ProposalRejected("AUTHORIZATION_NOT_GRANTED", "authorization is not active")
    if decision.authorization_id != request.authorization_id or decision.proposal_hash != request.proposal_hash:
        raise ProposalRejected("AUTHORIZATION_BINDING_MISMATCH", "decision is not bound to this proposal")
    if decision.approver_role != request.required_role:
        raise ProposalRejected("APPROVER_NOT_ELIGIBLE", "approver does not satisfy the role predicate")
    if now >= request.expires_at:
        raise ProposalRejected("AUTHORIZATION_EXPIRED", "authorization expired before commit")
    if current_case_version != request.case_version:
        raise ProposalRejected("STALE_CASE_VERSION", "case changed after authorization")


class TaskEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    parent_run_id: str
    capability: str
    owner: str
    scope: CapabilityScope
    status: Literal["created", "accepted", "completed", "failed", "cancelled"] = "created"
    result_artifact_id: str | None = None


class TaskStore:
    def __init__(self) -> None:
        self.tasks: dict[str, TaskEnvelope] = {}

    def create(self, task: TaskEnvelope, parent_scope: CapabilityScope) -> TaskEnvelope:
        narrow_scope(parent_scope, task.scope)
        if task.task_id in self.tasks:
            if digest(self.tasks[task.task_id]) != digest(task):
                raise ProposalRejected("TASK_CONFLICT", "task ID was reused for different work")
            return self.tasks[task.task_id]
        self.tasks[task.task_id] = task
        return task

    def complete(self, task_id: str, artifact_id: str) -> TaskEnvelope:
        if task_id not in self.tasks:
            raise ProposalRejected("TASK_NOT_FOUND", "completion targets an unknown task")
        task = self.tasks[task_id].model_copy(update={"status": "completed", "result_artifact_id": artifact_id})
        self.tasks[task_id] = task
        return task


class ProtocolGateway:
    """Pinned fake MCP/A2A boundary with local artifact adoption."""

    def __init__(self) -> None:
        self.mcp_digest = digest("employment-verification-mcp@1.0")
        self.a2a_digest = digest("appraisal-partner-card@1.0")

    def invoke_mcp(self, *, server_digest: str) -> Artifact:
        if server_digest != self.mcp_digest:
            raise ProposalRejected("MCP_METADATA_CHANGED", "server metadata changed after resolution")
        return Artifact(artifact_id="ART-MCP-EMP-000184", kind="employment_verification", source_revision="mcp-employer@1.0", content_digest=digest("verified-employment"))

    def send_a2a(self, *, card_digest: str, malicious: bool = False) -> Artifact:
        if card_digest != self.a2a_digest:
            raise ProposalRejected("A2A_CARD_CHANGED", "remote agent card changed after resolution")
        artifact = Artifact(artifact_id="ART-A2A-APPRAISAL-000184", kind="appraisal", source_revision="appraisal-partner@1.0", content_digest=digest("malicious" if malicious else "appraisal"))
        if malicious:
            raise ProposalRejected("REMOTE_ARTIFACT_REJECTED", "remote artifact failed local adoption policy")
        return artifact.model_copy(update={"adopted": True})


class SecurityResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed: bool
    reason_code: str
    incident_id: str | None = None
    redacted_evidence: tuple[str, ...] = ()


def scan_untrusted_document(text: str, *, detector_enabled: bool = True) -> SecurityResult:
    """Detect instruction-like content without making detection the only guard."""

    suspicious = any(term in text.lower() for term in ("upload applicant", "send bank", "ignore policy", "reveal account"))
    if suspicious and detector_enabled:
        return SecurityResult(allowed=False, reason_code="PROMPT_INJECTION", incident_id="INC-MORT-000184-01")
    return SecurityResult(allowed=True, reason_code="CONTENT_UNTRUSTED", redacted_evidence=("instruction_text_excluded",))


class PrincipalChain(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_id: str
    actors: tuple[str, ...]
    tenant_id: str
    purpose: str
    region: str
    revoked_subjects: frozenset[str] = frozenset()


class CapabilityEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chain: PrincipalChain
    actions: frozenset[str]
    resources: frozenset[str]
    data_classes: frozenset[str]
    expires_at: datetime

    @field_validator("expires_at")
    @classmethod
    def utc_expiry(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")
        return value.astimezone(UTC)


def authorize(chain: PrincipalChain, envelope: CapabilityEnvelope, *, action: str, resource: str, tenant_id: str, purpose: str, now: datetime = NOW) -> None:
    if chain.subject_id in chain.revoked_subjects or envelope.chain.subject_id != chain.subject_id:
        raise ProposalRejected("SUBJECT_REVOKED", "current subject entitlement is revoked")
    if (
        tenant_id != chain.tenant_id
        or purpose != chain.purpose
        or envelope.chain.tenant_id != chain.tenant_id
        or envelope.chain.purpose != chain.purpose
        or envelope.chain.region != chain.region
    ):
        raise ProposalRejected("AUTHORIZATION_DENIED", "tenant or purpose is not authorized")
    if action not in envelope.actions or resource not in envelope.resources:
        raise ProposalRejected("AUTHORIZATION_DENIED", "action or resource is outside the capability envelope")
    if now >= envelope.expires_at:
        raise ProposalRejected("CREDENTIAL_EXPIRED", "capability envelope expired")


class CredentialLease(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lease_id: str
    audience: str
    action: str
    resource: str
    expires_at: datetime

    @field_validator("expires_at")
    @classmethod
    def utc_expiry(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")
        return value.astimezone(UTC)


class EffectRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    effect_id: str
    logical_key: str
    intent_hash: str
    state: Literal["proposed", "executing", "committed", "unknown", "reconciled", "intervention"] = "proposed"
    downstream_request_id: str | None = None
    receipt: str | None = None


class SyntheticLOS:
    """Synthetic connector; its call count makes duplicate prevention visible."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.ready_cases: set[str] = set()

    def mark_ready(self, case_id: str, request_id: str, *, fail_after_commit: bool = False) -> str:
        self.calls.append(request_id)
        self.ready_cases.add(case_id)
        if fail_after_commit:
            raise TimeoutError("receipt lost after synthetic LOS commit")
        return f"LOS-RECEIPT-{case_id}"


class EffectLedger:
    def __init__(self) -> None:
        self.records: dict[str, EffectRecord] = {}

    def commit_mark_ready(self, *, tenant_id: str, case_id: str, case_version: int, intent: dict[str, Any], los: SyntheticLOS, fail_after_commit: bool = False) -> EffectRecord:
        logical_key = f"{tenant_id}:case:{case_id}:mark_ready:v{case_version}"
        intent_hash = digest(intent)
        existing = self.records.get(logical_key)
        if existing:
            if existing.intent_hash != intent_hash:
                raise ProposalRejected("IDEMPOTENCY_CONFLICT", "logical effect key was reused for different intent")
            return existing
        record = EffectRecord(effect_id=f"EFFECT-{case_id}", logical_key=logical_key, intent_hash=intent_hash, state="executing", downstream_request_id=f"REQ-{case_id}")
        self.records[logical_key] = record
        try:
            receipt = los.mark_ready(case_id, record.downstream_request_id, fail_after_commit=fail_after_commit)
        except TimeoutError:
            record = record.model_copy(update={"state": "unknown"})
            self.records[logical_key] = record
            return record
        record = record.model_copy(update={"state": "committed", "receipt": receipt})
        self.records[logical_key] = record
        return record

    def reconcile(self, logical_key: str, *, committed: bool) -> EffectRecord:
        if logical_key not in self.records:
            raise ProposalRejected("EFFECT_NOT_FOUND", "reconciliation targets an unknown effect")
        record = self.records[logical_key]
        state = "reconciled" if committed else "intervention"
        updated = record.model_copy(update={"state": state})
        self.records[logical_key] = updated
        return updated


class SandboxProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: str
    max_seconds: int = Field(ge=1, le=300)
    max_memory_mb: int = Field(ge=16, le=4096)
    max_output_bytes: int = Field(ge=256, le=10_000_000)
    egress_hosts: frozenset[str] = frozenset()
    read_only_inputs: bool = True
    ephemeral_output: bool = True


def check_egress(profile: SandboxProfile, host: str) -> SecurityResult:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    blocked_address = bool(address and (address.is_private or address.is_loopback or address.is_link_local or address.is_unspecified or address.is_multicast))
    if host not in profile.egress_hosts or blocked_address:
        return SecurityResult(allowed=False, reason_code="EGRESS_DENIED", incident_id="INC-EGRESS-000184")
    return SecurityResult(allowed=True, reason_code="EGRESS_ALLOWED")


def dlp_publish(text: str) -> SecurityResult:
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b|\b\d{10,16}\b", text):
        return SecurityResult(allowed=False, reason_code="DLP_BLOCKED", incident_id="INC-DLP-000184")
    return SecurityResult(allowed=True, reason_code="DLP_CLEAR", redacted_evidence=("raw_document_excluded",))


class TraceSpan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    span_id: str
    name: str
    attributes: dict[str, str]


class TraceEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str
    spans: tuple[TraceSpan, ...]
    sensitive_capture: Literal[False] = False
    audit_reference: str


def build_trace(*, include_pii: bool = False, outage: bool = False) -> TraceEnvelope:
    attributes = {"case_ref": "case-ref-000184", "state": "waiting_or_committed", "release": "release-ref-2.1.0"}
    if include_pii:
        attributes["applicant_name"] = "Alex Morgan"
    if outage:
        raise MortgageCaseError("TRACE_STORE_UNAVAILABLE", "diagnostic trace store is unavailable; audit remains separate")
    if any("Alex Morgan" in value for value in attributes.values()):
        raise ProposalRejected("TRACE_PRIVACY_VIOLATION", "PII is not allowed in ordinary telemetry")
    spans = tuple(TraceSpan(span_id=f"SPAN-{index:02d}", name=name, attributes=attributes) for index, name in enumerate(("workflow", "agent", "policy", "human_authorization", "effect"), start=1))
    return TraceEnvelope(trace_id="TRACE-REF-000184", spans=spans, audit_reference="AUDIT-REF-000184")


class EvaluationCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    expected: dict[str, Any]
    cohort: str
    protected_features_excluded: bool = True


class EvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dataset_version: str
    candidate_version: str
    sample_size: int
    outcome_score: Decimal
    safety_score: Decimal
    protected_slice_status: Literal["pass", "fail", "inconclusive"]
    gate: Literal["promote", "block", "inconclusive"]
    reasons: tuple[str, ...]


def evaluate_candidate(*, fairness_regression: bool = False, sample_size: int = 12) -> EvaluationResult:
    if sample_size < 0:
        raise ProposalRejected("INVALID_EVALUATION_SAMPLE", "sample size cannot be negative")
    slice_status: Literal["pass", "fail", "inconclusive"] = "fail" if fairness_regression else ("inconclusive" if sample_size < 5 else "pass")
    if slice_status == "fail":
        gate: Literal["promote", "block", "inconclusive"] = "block"
        reasons = ("protected_slice_regression", "aggregate_score_cannot_dilute_high_consequence_failure")
    elif slice_status == "inconclusive":
        gate = "inconclusive"
        reasons = ("minimum_sample_rule",)
    else:
        gate = "promote"
        reasons = ("deterministic_safety_and_outcome_checks_passed",)
    return EvaluationResult(dataset_version="evaluation_cohort_v1", candidate_version="candidate-mortgage@1.0.0", sample_size=sample_size, outcome_score=Decimal("0.92"), safety_score=Decimal("1.00"), protected_slice_status=slice_status, gate=gate, reasons=reasons)


class GovernanceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str
    purpose: str
    prohibited_uses: tuple[str, ...]
    owners: dict[str, str]
    risk_tier: Literal["high"] = "high"
    evidence_refs: tuple[str, ...]
    exception_expires_at: datetime | None = None
    recourse_contact: str


def validate_governance(record: GovernanceRecord, *, now: datetime = NOW) -> None:
    if not record.owners or any(not owner for owner in record.owners.values()):
        raise ProposalRejected("GOVERNANCE_OWNER_MISSING", "every material control needs an accountable owner")
    if record.exception_expires_at and now >= record.exception_expires_at:
        raise ProposalRejected("GOVERNANCE_EXCEPTION_EXPIRED", "an expired exception cannot provide authority")
    if not record.recourse_contact or not record.evidence_refs:
        raise ProposalRejected("GOVERNANCE_EVIDENCE_MISSING", "recourse and evidence references are mandatory")


class ReleaseBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    release_id: str
    digest: str
    workflow_version: str
    schema_version: str
    compatible_workers: frozenset[str]
    model_route: str
    evaluation_version: str
    signed: bool = False


def route_worker(bundle: ReleaseBundle, worker_version: str) -> str:
    if not bundle.signed:
        raise ProposalRejected("RELEASE_UNSIGNED", "an unsigned bundle cannot receive work")
    if worker_version not in bundle.compatible_workers:
        raise ProposalRejected("WORKER_INCOMPATIBLE", "worker cannot safely replay this release")
    return bundle.release_id


class CapacityResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workload_version: str
    sample_size: int
    completed_packages: int
    p50_seconds: int
    p95_seconds: int
    cost_per_verified_package: Decimal
    unknown_effect_backlog: int
    deadline_misses: int
    safe_degradation: bool


def simulate_capacity(*, spike: bool = False, provider_outage: bool = False) -> CapacityResult:
    if provider_outage:
        return CapacityResult(workload_version="workload_v1", sample_size=12, completed_packages=10, p50_seconds=420, p95_seconds=900, cost_per_verified_package=Decimal("1.90"), unknown_effect_backlog=0, deadline_misses=2, safe_degradation=True)
    if spike:
        return CapacityResult(workload_version="workload_v1", sample_size=36, completed_packages=32, p50_seconds=480, p95_seconds=1200, cost_per_verified_package=Decimal("2.10"), unknown_effect_backlog=1, deadline_misses=4, safe_degradation=True)
    return CapacityResult(workload_version="workload_v1", sample_size=12, completed_packages=12, p50_seconds=360, p95_seconds=720, cost_per_verified_package=Decimal("1.60"), unknown_effect_backlog=0, deadline_misses=0, safe_degradation=True)


def anchor_manifest(case: MortgageCase, chapter: int) -> RunManifest:
    if not 1 <= chapter <= 28:
        raise ProposalRejected("CHAPTER_OUT_OF_RANGE", "the cumulative mortgage checkpoint must be between C01 and C28")
    principal = PrincipalContext(tenant_id=case.tenant_id, subject_id="loan-officer-042", actor_id="mortgage-evidence-agent", purpose=case.purpose, region="us-west")
    scope = CapabilityScope(actions=frozenset({"read_case", "read_policy", "prepare_evidence"}), resources=frozenset({f"mortgage://case/{case.case_id}"}), data_classes=frozenset({"mortgage_evidence"}), purpose=case.purpose, region="us-west", expires_at=NOW + timedelta(hours=1))
    return RunManifest(run_id=f"RUN-{case.case_id}-C{chapter:02d}", case_id=case.case_id, tenant_id=case.tenant_id, principal=principal, requested_scope=scope, workflow_version=f"mortgage-workflow@{chapter}.0.0", release_digest=digest(f"release-c{chapter}"))
