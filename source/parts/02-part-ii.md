# PART II — ENTERPRISE REFERENCE ARCHITECTURE & KNOWLEDGE

This Part converts the foundational invariants into an enterprise system of record, then fills the knowledge plane it names. It assigns ownership across experience, application, runtime, knowledge, gateway, security, governance, and operations planes; defines the governed knowledge layer agents retrieve, reason over, are constrained by, and act through; and closes with how a single run assembles the context it is entitled to.

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

[[DIAGRAM:reference-architecture|Figure 4-1 — The layered reference architecture: planes, the components in each, and the two concerns that cross them all]]

Read the figure downward: each layer names the components the plane owns, and the solid path traces one request from intent to committed effect, narrowing in authority at every step. Trust and governance and evidence and improvement are drawn as vertical spines rather than layers because neither sits between two planes — the policy decision point is consulted at admission, at run control, and again at the Tool Gateway, and the collector gathers from every plane. Dashed edges are control, dotted edges are evidence, and the bottom band sits outside the trust boundary: nothing there is assumed, and everything returned from it is revalidated.

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

[[EXAMPLE:contracts]]

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

The reference architecture names a knowledge plane but does not say what fills it; Chapter 5 defines the governed knowledge layer agents retrieve, reason over, are constrained by, and act through.

# 05 — Enterprise Knowledge Management for Agents

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Northstar's onboarding agent can retrieve the supplier policy and quote it accurately. It still approves a supplier in a jurisdiction the policy excludes, because retrieving a sentence is not the same as being bound by it. The platform team stops adding documents to the index and starts building a knowledge layer. |

|  |
| --- |
| **DESIGN DECISION**  Treat institutional knowledge as governed artifacts with owners, versions, scope, and provenance — not as a corpus. Retrieval becomes one consumer of that layer rather than the layer itself. |

## What this chapter delivers

Separate the four things an agent does with what the organization knows, and give each one a representation it can actually use. An agent retrieves to understand a situation, reasons to decide what should happen, checks constraints to learn what it may do, and consults capabilities to act. These are four responsibilities with four failure modes, and an architecture that serves all four from one semantic index has not separated them — it has hidden them.

## Solution blueprint

[[DIAGRAM:knowledge-fabric|Figure 5-1 — The enterprise knowledge fabric and its four consumption modes]]

| State owner | Trust boundary | Scale unit | Failure containment | Core contracts |
| --- | --- | --- | --- | --- |
| Knowledge Hub and its registries | authored source to governed artifact | artifact · domain · tenant | one artifact version | KnowledgeArtifact · Rule · Capability · ResolutionQuery |

## Why retrieval is not a knowledge architecture

Retrieval-augmented generation answers one question well: *what text is relevant to this?* Enterprises then ask it three questions it was never designed for.

| Mode | The question | Representation | How it fails when wrong |
| --- | --- | --- | --- |
| Context | What is the situation? | Documents, embeddings, semantic search | Plausible grounding that is stale, superseded, or outside the reader's authority |
| Reasoning | What should happen? | Ontology, knowledge graph, decision models | Correct facts, invalid inference |
| Constraints | What may I do? | Policies and permissions as enforceable rules | The agent explains the rule, then violates it |
| Action | How do I do it? | Capability and API contracts | Right decision, wrong or unauthorized effect |

The fourth column is the argument. Each mode fails differently, so each needs different evidence and different tests. A system that cannot say which mode failed cannot be debugged, and a similarity score is not evidence of authority, currency, or permission.

The clearest case is the one Northstar hit. A policy excludes a jurisdiction. Retrieval returns the policy, the model quotes it, and the agent proceeds anyway, because nothing in the pipeline was responsible for *enforcing* the exclusion. The document was context. Nobody made it a constraint.

## The knowledge fabric

Seven representations, each derived from the one above it and carrying provenance back to it. A guardrail that cannot name the sentence it came from is an opinion.

### Semantic knowledge

Documents, policies, procedures, standards, and prior decisions, reached through embeddings and hybrid search. Chapter 6 owns the mechanics — chunking, reranking, and the context window itself. What belongs here is what makes retrieval *governed*: source authority, effective dates, jurisdiction, supersession, and the difference between text that appears in a document and text that is authoritative.

A retrieved passage should never reach a model without the metadata that decides whether it still applies.

### Ontology and knowledge graph

Entities, relationships, dependencies, and the organization's own semantics. Traversal answers questions similarity cannot: *what depends on this system three hops away?* No wording links a payments API to a regulatory filing obligation, so no embedding will connect them. The graph does.

[[EXAMPLE:knowledge-graph]]

Traversal must be bounded. An unbounded walk over an enterprise graph is a denial of service against your own agent, and a cycle makes it non-terminating.

The honest caveat: ontologies are where enterprise knowledge programmes go to die. The useful heuristic is to model only what an agent must traverse to make a decision it cannot make otherwise, and to let a modelling exercise justify itself one query at a time.

### Business rules as enforceable constraints

The core of the layer. A rule an agent reads is documentation; a rule the platform evaluates at the effect boundary is a control. The move from prose to knowledge is not parsing — it is committing to a shape.

[[EXAMPLE:policy-to-rule]]

Scope is required, not optional. A rule whose applicability is implicit will be applied where it does not belong, which is the most common way a correctly extracted rule still produces a wrong decision. Identity by content rather than by assigned identifier is what lets two independent extractions of one sentence recognize each other later.

Enforcement then happens where intent becomes action:

[[EXAMPLE:rule-as-guardrail]]

Note the refusal on missing input. A guardrail that reads *unknown* as *permitted* is not a guardrail. Three-valued evaluation — true, false, unknown — is what stops an absent field from silently authorizing an effect.

### Business data catalog

Entities, fields, definitions, ownership, lineage, sensitivity, and access constraints, described so an agent can discover and query data safely. A column name is not a definition, and a schema without a sensitivity class cannot tell an agent which fields it must not put in a prompt.

### Capability and API catalog

What the agent may do, with the consequences attached. A tool list says what exists; a capability catalog says whether an action mutates, what must be true first, who may invoke it, and whether a retry is safe.

[[EXAMPLE:capability-catalog]]

Filtering before discovery matters more than it looks. A capability the caller may not invoke should never appear, because a listed-but-forbidden tool is an invitation to try. This is the knowledge-side view of the Skills of Chapter 8 and the tool manifests of Chapter 22; it is the same artifact seen from discovery rather than from execution.

### Process and decision models

Four OMG standards already describe what most enterprises are otherwise inventing badly. The question to ask of each is not whether it is rigorous but what an agent can do with it that it could not do with prose.

| Standard | Represents | What an agent does with it |
| --- | --- | --- |
| BPMN [R44] | Processes and their control flow | Plans against the real sequence, including the steps it may not skip |
| DMN [R45] | Decisions as tables with a hit policy | Evaluates a decision deterministically instead of reasoning about it |
| CMMN [R46] | Case management, unordered work | Handles work with no fixed sequence without inventing one |
| SBVR [R47] | Business vocabulary and rules | Resolves what a term means in this domain before acting on it |

DMN earns its place fastest. A decision table with a declared hit policy is the one artifact that turns a class of judgement calls into a lookup, and a lookup can be tested. BPMN pays off where the sequence is genuinely fixed and the cost of skipping a step is high. CMMN and SBVR are narrower; adopt them when case work or vocabulary ambiguity is the actual problem, not because the set is incomplete without them.

## From policy text to enforceable logic

Extraction is probabilistic. Verification must not be. The pipeline that works separates the two and refuses to let the first vouch for itself.

[[DIAGRAM:policy-to-guardrail|Figure 5-2 — Extract, prove, and project: from policy text to an enforced guardrail]]

**Extract** is the part a language model does well: find the rules, type their conditions and outcomes, record where each came from.

**Prove** is the part that decides whether to believe it. The critical move is that verification does not trust the citation a rule carries; it rebuilds the evidence from the raw corpus and compares.

[[EXAMPLE:grounding-verifier]]

A model that invents a rule will invent a plausible citation for it, so checking that a citation is well-formed proves nothing. Checking that the cited passage *says what the rule says* is a different operation, and it is the one that matters. In one run of a compliance extraction pipeline built on this design, independent verification rejected 44% of the dependency and conflict claims that the pipeline's own deterministic guard had already accepted [R48]. That figure is one measurement of one pipeline on one corpus; it is not a general rate. It is, however, the empirical case for making verification independent of extraction.

**Project** turns what survived into the standards-compliant models above, and into the guardrails the runtime enforces.

|  |
| --- |
| **COMMON PITFALL**  Treating extraction confidence as grounding. A high-confidence rule with a fabricated citation is more dangerous than a low-confidence one, because it will pass review. Verify against the corpus, not against the model's own certainty. |

## Knowledge algebra

An enterprise never has one knowledge base. It has a regulator's and its own, last quarter's and this quarter's, one business unit's and another's. Agents must operate across them, and that requires defined operations rather than a merge.

[[EXAMPLE:set-operations]]

| Operation | Meaning | What an agent may do with the result |
| --- | --- | --- |
| Intersection | Asserted by both sources | Highest-confidence knowledge; safe to act on |
| Difference | Asserted by one source only | Scope-dependent; requires a jurisdiction check first |
| Union | Every distinct rule, with per-source attribution | Complete coverage; conflicts still possible |
| Contradiction | Rules that cannot both be satisfied | Stop, escalate, and never resolve automatically |

Three properties are worth stating as rules of the architecture.

**Union is not merge.** Combining two knowledge bases must preserve which source asserted each rule and what its original identifier was. A union that flattens attribution destroys the only information that can later resolve a conflict.

**A contradiction is a result, not an error.** Two authoritative sources that disagree is a finding about the organization, frequently a valuable one. The platform's job is to surface it with structured evidence — the shared subject, each side's requirement, and why they cannot both hold — not to pick a winner quietly.

**Semantic equivalence never overrides deterministic alignment.** Where rules align by identifier or citation, that alignment stands. Model-judged equivalence is advisory, marked for review, and never allowed to change a deterministic match.

|  |
| --- |
| **ARCHITECTURE GUIDANCE**  Define these operations over typed rules with declared scope, not over documents. Two documents cannot be intersected; two rule sets can. If your knowledge base cannot support the algebra, it is a corpus with a search box. |

## Governance and provenance

Every representation above is only as good as the metadata that says whether to believe it.

| Field | Why an agent needs it |
| --- | --- |
| Owner | Who answers when the artifact is wrong |
| Version and supersedes | Which of two conflicting statements is current |
| Effective from / until | Whether it applied on the date in question |
| Jurisdiction and scope | Whether it applies to this subject at all |
| Provenance | The passage, offsets, and document digest it derives from |
| Confidence and status | Authoritative, inferred, or draft |
| Permissions and data class | Who may see it, and whether it may enter a prompt |
| Lifecycle | Review cadence and expiry |

The document digest deserves emphasis. Without it, a rule extracted from last year's policy still verifies against this year's text, and nothing in the system notices that the ground moved.

|  |
| --- |
| **SECURITY AND GOVERNANCE**  Permissions belong to the knowledge artifact, enforced at the resolution boundary. Filtering retrieved passages after the model has seen them is not access control; it is redaction after disclosure. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Standards scope | BPMN, DMN, CMMN, and SBVR are OMG specifications; each citation supports the existence and semantics of its own standard and nothing about its suitability for agentic systems. That assessment is book-authored. | R44; R45; R46; R47 |
| Verification measurement | The 44% rejection figure is one run of one compliance pipeline on one corpus, reported by its authors. It is evidence that independent verification finds real errors, not a general error rate for extraction. | R48 |

Evidence anchors: R44; R45; R46; R47; R48. Full URLs, authority, version, and scope appear in Appendix K.

## Implementation reference

The examples above are the reference implementation, and each is executed in continuous integration. Composed, they show the shape of a knowledge hub: a rule extracted with provenance, verified against its corpus, placed in a graph, reconciled against a second source, and finally enforced at the effect boundary.

## Reference architecture: the Enterprise Knowledge Hub

Agents must not hold connection strings to six stores. They ask one service, which resolves, authorizes, and attributes.

| Plane | Holds | Answers |
| --- | --- | --- |
| Governance | Ownership, versions, effective dates, permissions, lifecycle | May this agent see this, and is it current? |
| Semantic | Documents and embeddings | What text is relevant? |
| Structural | Ontology, graph, data catalog | What is related to what, and what does this field mean? |
| Normative | Rules, decision tables, vocabulary | What is required, permitted, or forbidden? |
| Procedural | Process and case models | In what order, and what may not be skipped? |
| Capability | Tools, APIs, effects, prerequisites | What can be done, and at what cost? |

One query surface sits above all six. Permissions are enforced there, attribution is attached there, and an agent that asks for knowledge it may not have receives a refusal rather than a filtered answer.

|  |
| --- |
| **PRODUCTION CONSIDERATION**  Version the knowledge layer alongside the agent. An agent release pinned to a policy version is reproducible; one that resolves against "current" changes behaviour when a document changes, with no deployment and no trace. |

## Debugging playbook

| Symptom | Likely cause | First check |
| --- | --- | --- |
| Agent quotes the right policy and violates it | The rule is context, never a constraint | Is any guardrail evaluating it at the effect boundary? |
| Correct answer in staging, wrong in production | Scope or effective date not enforced | Does the rule declare jurisdiction and effective_from, and are they checked? |
| Two runs disagree on identical input | Resolution against "current" rather than a pinned version | Is the knowledge version recorded in the run manifest? |
| A conflict surfaces only after an incident | Contradictions resolved silently at merge | Does the union preserve per-source attribution? |
| An agent selects a mutating tool for a read | Capability discovery filters on names, not effects | Does the catalog carry an effect class, and is it filtered on? |
| Provenance points at text that does not support the rule | Citation trusted rather than verified | Is verification rebuilding evidence from the corpus? |

## Production checklist

* Every knowledge artifact has an owner, a version, an effective range, and a provenance reference that resolves.
* Retrieval results carry authority and currency metadata, not just a similarity score.
* At least one rule is enforced at the effect boundary, with a test proving the effect does not run when it refuses.
* Missing inputs refuse rather than default to permitted.
* Union preserves per-source attribution; contradictions are escalated, never auto-resolved.
* Capability discovery filters on granted actions, prerequisites, and data class before returning results.
* The knowledge version used by a run is recorded in its manifest.
* Permissions are enforced at the resolution boundary, not after the model has seen the passage.

## Exercises

1. Take one policy sentence from your own organization and express it as a typed rule with scope and provenance. Note every field you cannot fill from the sentence alone.
2. Find a question your retrieval system answers plausibly and wrongly. Identify which of the four consumption modes it actually needed.
3. Compute the intersection of two overlapping policy sets in your domain. Inspect the differences before the union.
4. Take a rule your agents are expected to follow and make it refuse an effect in a test.

## Technical review questions

| Question | What a good answer demonstrates |
| --- | --- |
| Which consumption mode failed in your last incident? | The four modes are separable in your architecture |
| How does an agent know a retrieved passage is still authoritative? | Governance metadata reaches the point of use |
| What happens when two authoritative sources disagree? | Contradiction is a first-class result |
| Where is a policy enforced, as opposed to described? | Constraints exist outside the prompt |
| What does the system do when a required input is missing? | Unknown is not silently treated as permitted |
| Can you reproduce a decision made six months ago? | Knowledge is versioned and pinned per run |

## Transition to Chapter 6

The knowledge layer defines what the organization knows and what agents may do with it. Chapter 6 turns to the run itself: how context is assembled, how memory and workflow state differ, and how a single request gets exactly the knowledge it needs and nothing more.

# 06 — Context Engineering, RAG, Memory, and State

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  As runs grow, prompts become a mixture of chat, workflow state, retrieved documents, summaries, and learned preferences. Northstar separates these domains and records exactly which authorized projection reached each model call. |

|  |
| --- |
| **DESIGN DECISION**  Treat prompts as disposable authorized projections; keep canonical state, knowledge, artifacts, and memory in distinct stores. |

## What this chapter delivers

Assemble authorized context from distinct state and knowledge domains and govern reusable memory as a data product.

## Solution blueprint


Figure 14. Context Engineering, Memory, and State.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Context Service; workflow remains canonical | authorized sources to model prompt | tenant · source · context budget | one context projection | ContextManifest · MemoryRecord · EvidenceRef |

## The context build pipeline

Northstar assembles context in stages: parse the request, calculate source candidates, enforce tenant and resource authorization, fetch immutable versions, classify and sanitize content, deduplicate, rank, allocate tokens, produce ordered references, and record a ContextManifest. Only the final authorized boundary materializes bytes into the model request.

Instructions have a trust hierarchy. System and application instructions are code-like release artifacts. Skill instructions are pinned capability artifacts. User requests express intent within authority. Retrieved documents and tool outputs are untrusted evidence. Content cannot promote itself to a higher trust role by saying “ignore previous instructions.”

Memory is not a bag of embeddings. Long-term memory creation is a protected data write with owner, scope, provenance, confidence, policy basis, TTL, correction, and deletion. Canonical business state always wins over a memory summary.

## Context, workflow state, memory, and enterprise knowledge

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | “Memory” often conflates prompts, conversation history, task state, preferences, learned facts, documents, and recovery data—causing leakage, stale decisions, and unreproducible runs. |
| Why it is difficult | Each type has different scope, consistency, privacy, retention, freshness, and retrieval semantics; models can misclassify or invent memories. |
| Design alternatives | Full transcript replay; summarization; graph checkpoints; key/value memory; vector memory; knowledge graph; source-grounded retrieval; event-sourced state. |
| Recommended architecture | Separate stores and APIs by semantic role. Build the model context as a policy-filtered projection of authoritative workflow state, recent conversation, relevant source-grounded knowledge, and explicitly approved memories. |
| Trade-offs | Separation requires more schemas and retrieval logic, but enables correct ACLs, deletion, freshness, replay, and bounded context. |
| Failure scenarios | Stale summary overwrites a current constraint; private memory leaks across tenants; model treats retrieved text as instruction; vector result lacks source ACL; deletion does not remove derived memory. |
| Enterprise example | In claims handling, the chat transcript supports interaction, the workflow record tracks claim steps, policy documents remain in governed search, and any remembered customer preference has consent, provenance, TTL, and deletion linkage. |

### State taxonomy and storage

| **Information class** | **Scope and examples** | **System of record** | **Rules** |
| --- | --- | --- | --- |
| Conversation context | Recent messages, channel state, current clarification | Conversation service / document DB | Append-only turns; compact with source links; not authoritative business state |
| Workflow state | Current node, variables, child tasks, budgets, approvals | Durable workflow history + relational projection | Strong transition rules; versioned; queryable; replay-safe |
| Durable execution state | Event history, timers, activity results, checkpoint cursor | Workflow engine persistence | Engine-owned; encrypted; retention aligned to run evidence |
| Short-term working memory | Scratch notes, candidate plan, intermediate hypotheses | Run-scoped state or object artifacts | TTL; no automatic cross-run reuse; label confidence and provenance |
| Long-term memory | Approved preferences, reusable facts, learned procedures | Governed memory service / relational + search index | Explicit write policy, consent, provenance, TTL, ACL, correction/deletion |
| Enterprise knowledge | Policies, contracts, code, tickets, records, catalogs | Source systems + governed search/vector/graph indexes | Source remains authoritative; ACL filter before retrieval; freshness and lineage |
| Artifacts | Reports, patches, extracted tables, evidence packages | Versioned object store | Immutable versions, content hash, classification, owner, retention |
| Telemetry and audit | Traces, metrics, policy decisions, effect records | Trace store + SIEM + append-only/WORM archive | Redaction; role-separated access; retention/legal hold |

### Context assembly pipeline

1. Start with agent instructions and policy-owned constraints from pinned versions.
2. Load canonical workflow state and unresolved obligations—not the raw event history.
3. Select the smallest recent conversation window needed for continuity.
4. Retrieve enterprise knowledge only after identity/tenant/ACL filtering; attach source, timestamp, classification, and confidence metadata.
5. Retrieve long-term memory through a separate policy gate; prefer verified facts and user-approved preferences.
6. Remove duplicates, stale items, secrets, and content outside the task purpose; summarize only with links to originals.
7. Label each segment as instruction, user\_input, enterprise\_data, tool\_result, or memory; the model must not promote data into instructions.
8. Record a context-manifest hash on the model span so the call can be reconstructed without logging sensitive plaintext by default.

### Detailed design — APIs, data model, and scalability

### Component boundaries

The Conversation Service owns turns; the Workflow Projection Service owns canonical run state; the Context Assembler creates an ephemeral model-input projection; the Retrieval Broker queries governed knowledge; the Memory Service owns approved cross-run memory; the Provenance Service tracks lineage; and the Compaction Service produces source-linked summaries. No component can silently promote a conversation statement into workflow truth or long-term memory.

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/context:assemble | Build a token-bounded context from pinned instructions, run state, conversation, knowledge, and memory under a policy and data budget |
| GET /v1/runs/{run\_id}/state | Return the canonical typed state projection and state\_version; separate from transcript/history |
| POST /v1/conversations/{id}/turns | Append an immutable user/agent/tool turn with provenance, classification, and client idempotency key |
| POST /v1/knowledge:search | Hybrid search with subject+actor context, source allowlist, freshness, filters, top-k, and required citations |
| POST /v1/memories | Propose/write a governed memory with scope, provenance, confidence, consent, TTL, and deduplication key; policy may require review |
| GET /v1/memories:search | Search only memories visible to the subject/purpose/run; returns confidence and source lineage |
| PATCH /v1/memories/{memory\_id} | Correct via optimistic version; preserves previous version and reason |
| DELETE /v1/memories/{memory\_id} | Create deletion tombstone and enqueue removal from indexes, caches, summaries, and derived artifacts |
| POST /v1/context:compact | Produce a source-linked summary/checkpoint under a target token budget; never overwrites source turns |

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ConversationTurn | conversation/turn IDs, role/type, content reference/hash, producer, created time, classification, source/trace refs; append-only |
| RunStateProjection | run ID, schema/version, state version, variables, obligations, unresolved questions, budgets, artifact refs; derived from workflow history |
| ContextManifest | context ID, run/node/model call, token budget/allocation, policy/version pins, ordered segment refs/hashes, redaction summary, total tokens |
| ContextSegment | segment ID/type, source URI/revision, content hash, trust label, instruction flag, classification, ACL decision, freshness, token count |
| MemoryRecord | memory ID, tenant, subject/team scope, type, canonical value, provenance, confidence, consent, purpose allowlist, TTL, status, supersedes |
| KnowledgeObject | source URI/revision, object/chunk IDs, text/blob reference, embedding version, metadata, ACL pointer, ingestion cursor, deletion state |
| SummarySnapshot | input segment hashes, summary hash/reference, model/prompt version, coverage map, unresolved facts, expiry; immutable |

Example context-manifest shape:

JSON · implementation excerpt

```json
{
  "context_id": "ctx_...",
  "run_id": "run_42",
  "node_id": "n7",
  "budget": {"max_tokens": 24000, "instructions": 3000, "state": 4000, "evidence": 14000, "conversation": 3000},
  "segments": [{
    "kind": "enterprise_data",
    "uri": "doc://policy/91@rev17",
    "sha256": "...",
    "trust": "untrusted-content",
    "acl_decision_id": "dec_...",
    "tokens": 1840
  }],
  "redactions": ["pii:ssn"],
  "manifest_sha256": "..."
}
```

### Retrieval and memory consistency

* The source system revision is authoritative. Index entries are disposable projections and must carry source revision, ACL pointer, ingestion time, and deletion state.
* Search performs tenant/source pruning, exact ACL filtering, hybrid lexical/vector scoring, reranking, freshness filtering, and diversity/deduplication before context selection.
* A memory write is a governed business operation: validate type, scope, consent, provenance, contradiction, retention, and sensitivity. Derived guesses default to run-scoped working memory, not long-term memory.
* Correcting or deleting a source creates lineage events that invalidate affected memories, summaries, embeddings, model caches, and evidence packages according to retention/legal-hold policy.

### Scalability and token economics

* Partition conversations and memories by tenant + subject/team; partition knowledge by tenant + source + region. Use routing metadata so a query touches only eligible partitions.
* Store content in object storage and metadata in relational/search stores. Context APIs exchange references; only the assembler materializes bytes for the authorized model call.
* Run ingestion as an asynchronous CDC/event pipeline with separate extract, classify, ACL, chunk, embed, and index stages. Track independent cursors so failed embedding does not block ACL deletion.
* Cache retrieval candidates by tenant, source revision, normalized query, policy scope, and embedding/reranker version; re-run exact authorization on cache hit.
* Allocate a fixed context budget before retrieval. Use maximum marginal relevance/source diversity, per-source caps, and evidence-quality thresholds rather than filling the entire window.
* Compact long conversations asynchronously and incrementally. Keep recent turns plus source-linked summaries; rebuild summaries when covered inputs change.
* Enforce deletion SLOs across primary metadata, vector/search indexes, caches, and derived summaries. Tombstones must outlive the longest replica/cache lag to prevent resurrection.

|  |
| --- |
| **PERFORMANCE AND COST**  Retrieve less, and cite what you retrieved. Context is the dominant cost in most agentic systems and the dominant cause of distraction. Record a context manifest identifier rather than the context body, and measure answer quality against context size — most systems are past the point where more retrieval helps. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Privacy lifecycle | Context and memory need purpose limitation, consent or other legal basis where applicable, data-subject request handling, deletion propagation, legal-hold precedence, residency, provider retention controls, and proof that derived summaries/indexes were handled too. | NIST-GAI; GDPR |

Evidence anchors: NIST-GAI; GDPR. Full URLs, authority, version, and scope appear in Appendix K.

## Pattern reference — Memory

|  |
| --- |
| **PROBLEM**  The system should reuse useful information across turns or runs without confusing stale summaries with canonical truth or retaining data indefinitely. |

### Architecture and flow

Working memory is run-scoped; long-term memory is a governed write with subject, scope, provenance, confidence, policy basis, TTL, correction, deletion, and retrieval authorization.

1. Identify a candidate reusable fact.
2. Validate evidence, subject, purpose, consent or policy basis, and sensitivity.
3. Write a versioned memory record with TTL and provenance.
4. Retrieve only after authorization and trust labeling.
5. Correct, supersede, expire, or delete through propagation workflows.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for stable preferences, repeated domain facts, or learned operational hints with clear value and governance. | Do not persist transient chain-of-thought, secrets, unverified hypotheses, protected data without basis, or facts already authoritative elsewhere. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Continuity | Creates privacy, staleness, correction, and deletion obligations. |
| Reduced context cost | May lose nuance or introduce summary drift. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Stale memory overrides state | Canonical state precedence and freshness checks. |
| Cross-tenant leakage | Tenant-partitioned keys and authorization before retrieval. |
| Deletion gaps | Lineage graph, tombstones, cache invalidation, and rebuild. |

### Minimum observability

* memory ID and version
* source provenance
* scope and tenant
* policy basis
* confidence and TTL
* retrieval and deletion events

## Implementation reference


### Auditable context projection

PYTHON · implementation excerpt

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class ContextSegmentRef(BaseModel):
    artifact_id: str
    source_revision: str
    sha256: str
    authorization_decision_id: str
    trust_role: Literal["instruction", "user_intent", "evidence"]
    token_count: int


class ContextManifest(BaseModel):
    context_id: str
    run_id: str
    release_id: str
    policy_version: str
    segments: tuple[ContextSegmentRef, ...]
    omitted_candidate_ids: tuple[str, ...]
    created_at: datetime
```

### Cross-boundary artifact adoption policy

PYTHON · implementation excerpt

```python
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class ArtifactDescriptor(BaseModel):
    artifact_id: str
    tenant_id: str
    data_classes: frozenset[str]
    region: str
    allowed_purposes: frozenset[str]
    provenance_digest: str
    expires_at: datetime
    legal_hold: bool = False


class AdoptionPolicy(BaseModel):
    tenant_id: str
    allowed_data_classes: frozenset[str]
    allowed_regions: frozenset[str]
    purpose: str
    trusted_provenance_digests: frozenset[str]


def authorize_artifact_adoption(
    artifact: ArtifactDescriptor, policy: AdoptionPolicy, *, now: datetime
) -> None:
    if artifact.tenant_id != policy.tenant_id:
        raise PermissionError("cross-tenant artifact adoption denied")
    if not artifact.data_classes <= policy.allowed_data_classes:
        raise PermissionError("artifact classification exceeds policy")
    if artifact.region not in policy.allowed_regions:
        raise PermissionError("artifact region is not allowed")
    if policy.purpose not in artifact.allowed_purposes:
        raise PermissionError("artifact purpose is not allowed")
    if artifact.provenance_digest not in policy.trusted_provenance_digests:
        raise PermissionError("artifact provenance is not trusted")
    if now > artifact.expires_at and not artifact.legal_hold:
        raise PermissionError("artifact expired")
```

## Debugging playbook

1. Reconstruct one ContextManifest without relying on logged plaintext.
2. Compare canonical state with summaries and working memory.
3. Trace a corrected or deleted fact through indexes, cache, memory, and artifacts.

## Production checklist

**✓** Conversation, workflow state, working memory, long-term memory, knowledge, artifacts, telemetry, and audit are separate domains.

**✓** Authorization occurs before content materialization.

**✓** Context records ordered references, hashes, trust labels, decisions, versions, redactions, and token allocation.

**✓** Memory creation is a governed write with scope, provenance, confidence, lawful basis, TTL, correction, and deletion.

**✓ Final implementation and deletion propagate through indexes, caches, summaries, memories, contexts, and artifacts.**

## Exercises

1. Design a token budget across instructions, state, evidence, memory, and reserve.
2. Define the lifecycle of a reusable supplier preference memory.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why call the prompt a projection rather than state? | It is a temporary, token-bounded view assembled from authoritative stores for one model call; it can be rebuilt, audited by reference, and discarded. |
| How do conversation, knowledge, working memory, and long-term memory differ? | Interaction history; source-backed enterprise facts; run-scoped hypotheses; and approved reusable facts—each with different ownership, retention, authority, and deletion. |
| What problem does a ContextManifest solve? | Reproducibility and diagnosis through ordered source, version, and hash references, authorization decisions, trust labels, redactions, and budget without logging all plaintext. |
| How should retrieved instructions be handled? | As untrusted data with provenance and taint; they cannot alter system instructions, tool eligibility, policy, credentials, or destination grants. |
| How do you delete a fact from an agentic system? | Tombstone and revoke the source, remove derived indexes, invalidate caches, rebuild summaries and contexts, clean governed memory and affected artifacts, and preserve permitted audit evidence. |

## Transition to Chapter 7

Context assembly completes the knowledge Part. Chapter 7 turns from what agents know to how teams build with it, defining the reusable developer platform and SDK.
