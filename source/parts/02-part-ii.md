# PART II — ENTERPRISE REFERENCE ARCHITECTURE

This Part converts the foundational invariants into an enterprise system of record. It assigns ownership across experience, application, runtime, knowledge, gateway, security, governance, and operations planes, then specifies the APIs and records that let those planes evolve independently.

# 04 — Enterprise Reference Architecture, Boundaries, and Contracts

## What this chapter delivers

Translate principles into planes, services, contracts, stores, consistency boundaries, and regional cells.

## Solution blueprint

Figure 20. Enterprise Platform Architecture, APIs, and Data Models.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Each platform service owns one authoritative record | global control plane to regional execution cell | tenant · queue · partition · cell | one service/cell | Run · Task · Tool · Artifact · Release APIs |

## Purpose and principles

The enterprise architecture places probabilistic reasoning inside explicit experience, runtime, workflow, knowledge, integration, security, evaluation, and operations planes. The agent is a decision component—not the workflow, authorization service, database, policy engine, or proof of completion.

[[DIAGRAM:reference-architecture|Figure 4-1 — Enterprise agentic AI layered reference architecture]]

| **Plane** | **Responsibilities** | **Authoritative records** | **Boundary** |
| --- | --- | --- | --- |
| Experience and channels | Intent, interaction, review, accessibility, recourse | Request and interaction record | UI state is not approval or workflow truth |
| Agent applications | Domain instructions, topology, response assembly | AgentSpec and application release | Cannot mint authority or directly commit protected effects |
| Runtime and workflow | Run graph, deadlines, budgets, retries, cancellation, checkpoints, joins | Run and TaskEnvelope state | Transcript is evidence, not execution state |
| Context, RAG, memory, Skills | Authorized evidence, provenance, snapshots, governed persistence | ContextManifest, MemoryRecord, Skill manifest | Retrieved text remains untrusted data |
| Gateways and integration | LLM routing, tool façades, MCP/A2A, APIs, events | RoutingDecision, ToolCall, protocol envelope | Revalidate identity, policy, schema, and tenancy |
| Security and governance | Identity, least privilege, RBAC/ABAC, guardrails, approval, DLP, audit | PolicyDecision, CapabilityEnvelope, ApprovalGrant | Protected actions fail closed; ambiguous effects become unknown |
| Evaluation and operations | Tracing, evaluation, SLOs, incidents, release, capacity, learning | Trace graph, EvaluationResult, ChangeBundle, ReleaseManifest | Monitoring cannot self-promote behavior change |

## End-to-end responsibility flow

[[DIAGRAM:request-sequence|Figure 4-2 — Request-to-verified-outcome sequence]]

1. Authenticate the initiating subject and workload; establish tenant, purpose, risk, deadline, and trace.
2. Admit a run and pin all behavior, policy, data, evaluator, and dependency versions.
3. Build an authorized ContextManifest; preserve provenance and untrusted-content labels.
4. Let the model propose a typed decision. Policy determines eligible models, tools, data, and actions.
5. Bind protected changes to an ActionProposal and exact, expiring ApprovalGrant.
6. Commit through a tool façade with short-lived credentials, idempotency, EffectRecord, and reconciliation.
7. Determine accepted, blocked, needs-input, failed, or unknown-effect using executable business criteria.
8. Join traces, evaluations, human feedback, cost, latency, incidents, and outcomes for controlled improvement.

## Systems of record

| **Concern** | **Owner** | **Model may** | **Model may not** |
| --- | --- | --- | --- |
| Workflow | Durable Run Service | Propose a semantic result | Invent state, retry history, or terminal |
| Authorization | Identity and policy services | Explain requested scope | Grant or expand authority |
| Business truth | Domain system | Read an authorized projection | Replace truth with a summary |
| Effects | Tool/effect service and downstream receipt | Propose arguments | Assert a mutation completed |
| Approval | Proposal and approval service | Generate rationale and preview | Reuse Boolean or stale conversational consent |
| Knowledge | Governed source/snapshot catalog | Synthesize evidence | Treat similarity as truth or freshness |
| Learning | Evaluation, dataset, release services | Recommend a candidate | Self-certify or self-deploy |

## Architecture decisions

Centralize identity, policy, gateways, tool/effect contracts, telemetry schemas, evaluation infrastructure, release evidence, and incident controls. Federate domain prompts, accepted outcomes, tools, Skills, knowledge, datasets, and SLOs to accountable owners. Standardize interfaces and evidence—not every framework implementation.

> **Evidence note.** CloudEvents defines the portable event envelope used here, while the transactional-outbox source supports atomic state/event publication and warns that consumers still require duplicate handling. [R03][R04]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  The design now spans edge APIs, definitions, workflows, workers, model routing, tools, knowledge, trust, and operations. Northstar turns diagrams into explicit contracts, stores, ownership, partitions, and failure domains. |

|  |
| --- |
| **DESIGN DECISION**  Deploy global definitions and governance into regional execution cells connected through stable provider-neutral contracts. |

## From boxes to contracts

A reference architecture becomes implementable when every arrow has an API or event contract and every record has one authoritative writer. Northstar separates a global definition and governance plane from regional execution cells. Cells contain run control, durable workflow, bounded agent workers, model and Tool Gateways, context services, effect ledger, artifact store, and regional telemetry/audit pipelines.

The public Run API is asynchronous and idempotent. Commands carry expected state version and deadline; accepted work returns 202 plus an operation or run resource. Status and events are durable and paginated. Large inputs and outputs use immutable artifact references rather than oversized JSON. Public contracts do not expose SDK messages or provider-specific run objects.

### Core authoritative records

RunManifest, WorkflowExecution, TaskEnvelope, AgentStep, ContextManifest, CapabilityEnvelope, PolicyDecision, CredentialLease, ToolManifest, ApprovalRequest, EffectRecord, Artifact, EvaluationReport, and ReleaseManifest each have one owner, version, retention policy, and consistency boundary.

Scale stateless APIs horizontally, partition state by tenant and run, shard workflow history and trace indexes, and isolate workload classes through queues and concurrency pools. Cell placement enforces region and residency while bounding blast radius.

## Recommended reference architecture

### Architecture layers

| **Layer** | **Major components** | **Primary responsibility** |
| --- | --- | --- |
| Experience | Chat/UI, API clients, event subscriptions, operator console | Intent capture, progress, approvals, cancel/override |
| Edge and admission | API gateway, WAF, tenant router, request validator | Authentication, quotas, schema validation, risk classification |
| Agent control plane | Registry, policy bundles, prompt/skill catalog, release manager | Define, version, approve, discover, and deploy capabilities |
| Run control plane | Run API, planner, coordinator, budget manager, approval service | Own task lifecycle and deterministic transition decisions |
| Durable execution | Workflow engine, timers, signal handlers, checkpoint/event store | Crash recovery, pause/resume, retries, compensation, replay |
| Model plane | Model gateway, router, prompt assembler, structured-output validator | Provider abstraction, routing, caching, quotas, redaction |
| Capability plane | Tool gateway, MCP clients/servers, A2A gateway, connectors | Discovery, authorization, invocation, isolation, versioning |
| Data and knowledge | RDBMS, object store, search/vector index, catalog, lineage | Authoritative state, artifacts, retrieval, provenance and ACLs |
| Execution plane | Sandboxed workers, code/browser runners, egress proxy | Resource isolation and constrained side effects |
| Trust and governance | IdP, STS, workload identity, PDP/PEP, secrets, audit/WORM | Least privilege, tenant isolation, policy, evidence and retention |
| Operations and improvement | OTel collector, trace store, metrics, eval service, incident tooling | Debug, replay, evaluate, optimize, alert, and promote |

### Trust boundaries

| **Boundary** | **Treat as untrusted** | **Mandatory controls** |
| --- | --- | --- |
| User/tenant → platform | Prompts, attachments, callback URLs | AuthN, tenant binding, malware/content scan, request schema, quotas |
| Knowledge → model | Documents, email, web text, OCR, metadata | Provenance, ACL filters before retrieval, instruction/data labeling, DLP |
| Model → orchestrator | Plans, arguments, classifications, generated code | Strict schema, allowlists, invariant checks, confidence/risk routing |
| Orchestrator → tool | Requested action and delegated context | PDP decision, downscoped token, idempotency, dry-run/approval, audit |
| Agent → agent | Claims, artifacts, status, requested authority | Authenticated channel, signed task envelope, scope intersection, limits |
| Sandbox → network | Code, browser activity, generated payloads | Default-deny egress, DNS/HTTP proxy, quotas, filesystem isolation |
| Platform → model vendor | Prompts, retrieved content, telemetry | Redaction, residency policy, retention controls, vendor allowlist |
| Result → destination | Reports, emails, records, deployments | Output classification, provenance, approval, destination authorization |

## Core platform APIs and contracts

### Run API

| **Operation** | **Semantics** |
| --- | --- |
| POST /v1/runs | Create idempotently from agent/workflow reference, goal, inputs, subject delegation, autonomy request, budgets, and callback preferences |
| GET /v1/runs/{id} | Return authorized status, current stage, owner, progress, budgets, waits, and result/artifact references |
| GET /v1/runs/{id}/events | Cursor-based event history or server-sent stream; redaction and history limits by role |
| POST /v1/runs/{id}:signal | Send typed, authenticated input such as clarification, approval, callback, or document-ready event |
| POST /v1/runs/{id}:cancel | Request hierarchical cancellation with reason and compensation policy |
| POST /v1/runs/{id}:update | Optimistic, authorized patch to budget, priority, assignee, or plan; may require approval |
| POST /v1/runs/{id}:fork | Create a sandbox replay/fork from checkpoint with pinned or explicitly changed versions; never reapply live effects |
| GET /v1/runs/{id}/audit | Return evidence manifest to authorized compliance/incident roles |

### RunManifest

JSON · implementation excerpt

```json
{
  "run_id": "run_...",
  "tenant_id": "t_...",
  "subject": {"id": "user_...", "assurance": "mfa"},
  "actor": {"workload_id": "spiffe://corp/agent-runtime/prod"},
  "purpose": "supplier_onboarding",
  "risk_tier": "high",
  "agent": {"id": "supplier-agent", "version": "3.4.1", "digest": "sha256:..."},
  "workflow": {"id": "supplier-onboarding", "version": "7.2.0", "build": "sha256:..."},
  "prompt_bundle": "sha256:...",
  "policy_bundle": "policy://enterprise-agent@2026.09.3",
  "model_route": "route://reasoning-standard@18",
  "tool_contracts": ["tool://kyc/read@2.0.1", "tool://case/draft@4.2.0"],
  "knowledge_snapshots": ["index://policies@2026-09-10T21:00Z"],
  "authority_envelope": "cap_...",
  "budget": {"usd": 25, "tokens": 300000, "steps": 80, "delegation_depth": 2},
  "retention_class": "regulated-7y",
  "trace_id": "..."
}
```

### Artifact contract

Every artifact has artifact\_id, immutable version, schema/media type, content hash, creator run/node/agent, source references and hashes, tenant, owner, classification, residency, ACL/purpose policy, confidence/quality metadata, retention/deletion linkage, and optional signature. Large artifacts move by reference; callers receive short-lived authorized URLs rather than embedded payloads.

### Effect receipt

A mutating tool returns a structured receipt: logical effect ID, idempotency key, downstream request ID, target resource and before/after version, committed/declined/unknown state, timestamp, actor/subject, compensation reference, verification query, and audit link. A timeout without a receipt is unknown, not failed.

### Event contract

JSON · implementation excerpt

```json
{
  "specversion": "1.0",
  "id": "evt_...",
  "source": "urn:corp:agent-platform",
  "type": "com.corp.agent.run.status.changed.v1",
  "subject": "run/run_...",
  "time": "2026-09-10T21:00:00Z",
  "dataschema": "schema://run-status-changed@1",
  "tenant_id": "t_...",
  "correlation_id": "run_...",
  "causation_id": "evt_...",
  "traceparent": "00-...",
  "dataref": "artifact://event-payload/...",
  "datahash": "sha256:..."
}
```

## Storage architecture

| **Store** | **Recommended contents** | **Consistency and controls** |
| --- | --- | --- |
| Workflow history store | Events, timers, activity results, signal cursor | Engine-managed durability; replay semantics; encrypted per environment/tenant |
| Relational operational DB | Run projections, manifests, budgets, ownership, approvals, effect ledger, dedup keys | Strong transactions, optimistic versions, row-level security |
| Object store | Prompts by digest, large tool outputs, artifacts, evidence bundles, replay fixtures | Immutable/versioned objects, hashes, retention lock, tenant keys |
| Search/vector index | ACL-aware chunks and embeddings derived from source systems | Source revision/provenance, pre-retrieval authorization, rebuild/delete pipeline |
| Event log/broker | CloudEvents, status changes, business triggers | At-least-once, partitions, schema registry, outbox/inbox, DLQ/quarantine |
| Trace/metric store | OTel spans, metrics, logs with content references | Tiered retention, sampling, redaction, restricted content access |
| Audit/WORM archive | Policy decisions, approvals, effects, release evidence | Append-only, signed/hashed, legal hold and regulatory retention |
| Secret broker / KMS | Connector secrets, token-exchange keys, encryption keys | No secrets in prompts/state; short-lived delivery; rotation and hardware-backed keys |
| Cache | Model, retrieval, tool-read, schema and policy-safe results | Scope-aware keys, TTL/freshness, encryption, no cross-tenant leakage |

A vector database is an index, not the source of truth; an agent transcript is not workflow state; a trace store is not the audit ledger; and a queue is not a business transaction. Keeping these responsibilities separate prevents attractive shortcuts from becoming systemic risks.

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Event contract | Use a CloudEvents 1.0-compatible envelope for interoperability, but keep domain semantics and delivery guarantees in versioned event contracts. Source plus ID supports deduplication; large or sensitive artifacts should be referenced rather than embedded. | CLOUDEVENTS |

Evidence anchors: CLOUDEVENTS. Full URLs, authority, version, and scope appear in Appendix K.

## Implementation reference

### Core platform data contracts

PYTHON · implementation excerpt

```python
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

class EvidenceRef(BaseModel):
    uri: str
    sha256: str
    source_revision: str
    authorization_decision_id: str

class ToolCall(BaseModel):
    tool_id: str
    arguments: dict[str, Any]
    logical_effect_key: str | None = None

class AgentDecision(BaseModel):
    disposition: Literal["answer", "needs_input", "invoke_tool", "delegate"]
    answer: str | None = None
    tool_call: ToolCall | None = None
    evidence: list[EvidenceRef] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)

class AgentStepRequest(BaseModel):
    run_id: str
    node_id: str
    state_version: int
    agent_version: str
    context_manifest_id: str
    eligible_tool_versions: tuple[str, ...]
    max_turns: int = Field(ge=1, le=20)
    deadline: datetime

class AgentStepResult(BaseModel):
    status: Literal["completed", "needs_input", "proposed_action", "failed"]
    decision: AgentDecision | None = None
    output_artifact_ids: tuple[str, ...] = ()
    usage: dict[str, int | float] = Field(default_factory=dict)
    error_code: str | None = None

class SkillRequirement(BaseModel):
    capability: str
    purpose: str
    maximum_risk: int = Field(ge=0, le=4)
    required_data_classes: frozenset[str] = frozenset()
    region: str

class PlanNode(BaseModel):
    id: str
    capability: str
    depends_on: tuple[str, ...] = ()
    maximum_cost_usd: float = Field(ge=0)
    maximum_attempts: int = Field(ge=1, le=10)
    risk_class: int = Field(ge=0, le=4)

class CandidatePlan(BaseModel):
    revision: int = Field(ge=1)
    nodes: tuple[PlanNode, ...] = Field(min_length=1, max_length=100)
```

### CloudEvents and outbox contracts

PYTHON · implementation excerpt

```python
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

class CloudEvent(BaseModel):
    """CloudEvents 1.0-compatible application envelope."""

    specversion: Literal["1.0"] = "1.0"
    id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    type: str = Field(min_length=1)
    subject: str | None = None
    time: datetime
    datacontenttype: str = "application/json"
    dataschema: str | None = None
    data: dict[str, Any]
    tenant_id: str
    traceparent: str | None = None

    @field_validator("source")
    @classmethod
    def source_is_uri_reference(cls, value: str) -> str:
        if ":" not in value and not value.startswith("/"):
            raise ValueError("source must be a URI-reference")
        return value

class OutboxRecord(BaseModel):
    event: CloudEvent
    aggregate_id: str
    aggregate_version: int = Field(ge=0)
    state: Literal["pending", "published", "dead_letter"] = "pending"
    publish_attempts: int = Field(default=0, ge=0)

def deduplication_key(event: CloudEvent) -> tuple[str, str]:
    """CloudEvents producers make (source, id) unique for each distinct event."""

    return event.source, event.id
```

## Debugging playbook

1. Trace one API command through stores, queues, services, and contracts.
2. Find any record with two authoritative writers.
3. Map a cell failure to its intended containment boundary.

## Production checklist

**✓** Every record and transition has one authoritative owner.

**✓** Public contracts remain independent of model providers and SDK types.

**✓** Every trust boundary states authentication, authorization, validation, and data handling.

**✓** Regional execution can continue safely on pinned releases during control-plane disruption.

**✓** Cells, queues, and local dependencies bound failure domains.

## Exercises

1. Define Run, Task, Tool, Approval, Effect, Artifact, and Release contracts.
2. Select a store and consistency model for each authoritative record.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Walk through the major planes of an enterprise agent platform. | Experience and edge, global definition, run control, durable execution, agent and model, capability, data and context, trust, and operations—with explicit ownership and interfaces. |
| Why separate the control plane from the execution plane? | They have different scaling, availability, data-residency, and failure characteristics; immutable definitions can fan out while active tenant runs stay regional. |
| Where are the most important trust boundaries? | User-to-edge, knowledge-to-model, model-to-workflow, workflow-to-tool, sandbox-to-network, peer-to-platform, and platform-to-model provider. |
| Why use cell-based deployment? | Additive scale, tenant placement, residency, bounded blast radius, independent canaries, and predictable stateful-service limits. |
| How should execution behave during a control-plane outage? | Continue compatible in-flight work on pinned last-known-good bundles, apply local denies and kill switches, and restrict high-risk admission when freshness cannot be established. |

## Transition to Chapter 5

The reference architecture is now concrete enough to productize; Chapter 5 defines the reusable developer platform and SDK.
