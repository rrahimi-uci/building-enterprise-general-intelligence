# PART VI — MULTI-AGENT & PLATFORM INTEGRATION

This Part expands beyond one runtime. It shows when specialized agents are justified and how MCP, A2A, APIs, events, and shared services can cross platform boundaries without transferring hidden authority or trust.

# 18 — Supervisor/Worker and Multi-Agent Collaboration

> **Evidence note.** Public multi-agent implementation reports describe supervisor/specialist designs and substantial token/context trade-offs; these observations justify explicit topology and cost tests rather than universal multi-agent adoption. [R28][R33]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Screening, tax, security, and procurement specialists can run concurrently, but a plausible multi-agent conversation is not a coordination protocol. Northstar defines durable tasks, one owner per task, narrowed authority, explicit joins, and artifact contracts. |

|  |
| --- |
| **DESIGN DECISION**  Give one component ownership of each task, derive narrower child authority, and define explicit join and cancellation semantics. |

## What this chapter delivers

Give each task one owner, narrow authority on delegation, and make fan-out, fan-in, cancellation, and conflicts explicit.

## Solution blueprint


Figure 12. Supervisor/Worker and Multi-Agent Collaboration.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Task Service and supervisor workflow | parent/child authority and artifact adoption | task tree · specialist queue | one child task | TaskEnvelope · ChildGrant · JoinPolicy |

## Collaboration is a state machine

A supervisor/worker topology is justified when specialists have different tools, data boundaries, owners, SLOs, or deployment needs. Northstar’s supervisor owns the onboarding outcome and creates durable child tasks for screening, tax, and security. Each child receives only the capability, evidence, budget, deadline, and cancellation scope it needs.

Fan-in is explicit: wait for all, quorum, first valid, or fallback. Artifact conflicts use deterministic precedence, source freshness, confidence thresholds, or human resolution. Free-form conversation may help agents explain results, but it cannot replace task status, ownership, artifact, or effect records.

Nested delegation multiplies cost and risk. Northstar caps depth, children, concurrency, total turns, total tokens, external calls, and wall-clock time across the entire task tree. Parent cancellation propagates as durable intent; a child with an executing mutation must reconcile before acknowledging final cancellation.

## Agent topology, orchestration, delegation, and termination

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Divide work without creating ambiguous ownership, recursive loops, duplicated side effects, or unnecessary agent chatter. |
| Why it is difficult | Task boundaries are semantic; model routing is fallible; every new agent adds context transfer, policy, latency, cost, and failure surfaces. |
| Design alternatives | Single augmented agent; deterministic chain/DAG; router with specialists; manager using agents as tools; conversational handoff; peer swarm/blackboard. |
| Recommended architecture | Default to one agent inside a typed workflow. Add a specialist only when its instructions, tools, policy, context window, owner, deployment, or SLO differ. Use manager-as-tools for bounded work; use handoff only when user-facing ownership truly transfers. Avoid peer swarms for transactional work. |
| Trade-offs | Central coordination is easier to govern but can bottleneck; decentralized collaboration may increase coverage but weakens determinism, auditability, and cost control. |
| Failure scenarios | Ping-pong handoffs; orphaned tasks; two agents mutate the same record; context or permission loss; circular delegation; premature “done”; aggregator accepts incompatible artifacts. |
| Enterprise example | A mortgage-underwriting coordinator delegates document extraction, policy retrieval, and anomaly review, but a deterministic workflow owns the case and only the authorized decision service commits status. |

### Topology decision table

| **Pattern** | **Use when** | **Avoid when** | **Control model** |
| --- | --- | --- | --- |
| One model call + retrieval | Answer is bounded and no external side effect is needed | Task requires iterative environmental feedback | Request/response |
| Single agent loop | Open-ended steps share the same permissions, context, and owner | Multiple teams or security zones must be isolated | One agent, bounded tool loop |
| Deterministic workflow | Steps and invariants are known | Discovery or decomposition cannot be anticipated | Code/state machine owns routing |
| Router + specialists | Inputs fall into stable classes with distinct prompts/tools | Classification is unstable or branches share nearly all context | Deterministic or model router with confidence threshold |
| Manager + agents as tools | One coordinator must synthesize a final answer | Specialist should own the user relationship | Parent retains task ownership |
| Handoff | A specialist must take over the next user-facing branch | The work is a hidden bounded subtask | Ownership token transfers explicitly |
| Hierarchical fan-out/fan-in | Subtasks are independent and benefit from parallelism | Shared mutable context or tight ordering dominates | Coordinator sets fan-out and aggregation contract |
| Peer swarm / group chat | Research exploration where diversity is worth the cost | Regulated decisions, side effects, or strict SLOs | Experimental; hard budgets and sandbox only |

### Recommended orchestration rules

* **Creation:** instantiate agents from an immutable AgentManifest; never construct production instructions and permissions ad hoc in a prompt.
* **Delegation:** create a child task with explicit goal, input artifact references, output schema, authority ceiling, budget, deadline, trace context, and parent run ID.
* **Handoff:** atomically transfer the conversation owner and issue a new capability envelope; preserve the prior agent as history, not as a competing owner.
* **Coordination:** use a workflow node, not a group chat, to decide readiness, joins, retries, cancellation, and aggregation.
* **Shared state:** store it in a concurrency-controlled state service. Agents receive snapshots and return proposed patches with expected versions.
* **Termination:** terminal states are deterministic—acceptance criteria satisfied, user canceled, policy denied, budget/time/step limit reached, or unrecoverable error. The model may recommend completion but cannot invent the terminal transition.
* **Plan changes:** append a versioned plan revision with rationale and diff; validate new nodes against the original authority envelope. Materially broader scope requires new consent or approval.

### Detailed design — APIs, data model, and scalability

### Component boundaries

| **Component** | **Owns** | **Does not own** |
| --- | --- | --- |
| Agent Registry | Immutable agent versions, capability declarations, compatibility, ownership | Per-run mutable state |
| Run Coordinator | Goal lifecycle, plan revision, child-task policy, terminal decision | Provider-specific model calls or connector credentials |
| Task Service | Task records, dependencies, assignment, deadlines, idempotent creation | Business effects performed by the task |
| Ownership Service | Atomic handoff, leases, cancellation tree, current accountable owner | Natural-language routing judgment |
| Router | Ranked eligible agents/tools using manifest, health, policy, cost, and locality | Authorization or unrestricted discovery |
| Join/Aggregation Service | Readiness, quorum, schema validation, conflict policy, accepted result | Free-form “consensus” without evidence |

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| GET /v1/agents/{agent\_id}/versions/{version} | Resolve a pinned manifest; ETag is the manifest digest |
| POST /v1/runs/{run\_id}/tasks | Idempotently create a child task from goal, contract, inputs, authority ceiling, deadline, budget, and dependency IDs |
| POST /v1/tasks/{task\_id}:accept | Receiver accepts ownership using expected\_version; starts or binds a child workflow |
| POST /v1/tasks/{task\_id}:handoff | Atomically transfer owner; requires target agent/version, rationale, remaining budget, and narrowed capability grant |
| POST /v1/tasks/{task\_id}:complete | Submit typed result/artifacts; server runs acceptance and provenance checks before terminal transition |
| POST /v1/tasks/{task\_id}:fail | Record typed failure, retryability, partial artifacts, and recommended parent disposition |
| POST /v1/tasks/{task\_id}:cancel | Request hierarchical cancellation; response distinguishes requested, acknowledged, and completed |
| POST /v1/runs/{run\_id}/plans:revise | Append a plan revision with diff, trigger, rationale, and optimistic run version |
| GET /v1/runs/{run\_id}/graph | Read materialized task/dependency/owner/status graph for UI and operations |

Example child-task request:

JSON · implementation excerpt

```json
{
  "idempotency_key": "run_42:screen-supplier:1",
  "receiver": {"agent_id": "sanctions-screening", "version": "2.3.0"},
  "goal": "Screen the named supplier under policy EU-2026-09",
  "input_artifacts": [{"uri": "artifact://supplier/77", "sha256": "..."}],
  "output_schema": "schema://screening-result@2",
  "authority_ceiling": "grant://run_42/screen-readonly",
  "depends_on": ["task_extract_identity"],
  "deadline": "2026-09-11T03:00:00Z",
  "budget": {"usd": 2, "steps": 8, "delegation_depth": 0},
  "acceptance": ["schema-valid", "sources-present", "policy-version-matches"]
}
```

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| AgentVersion | (tenant\_id, agent\_id, version), digest, instructions digest, tool allowlist, schemas, owner, risk tier, lifecycle state; immutable after release |
| Task | task ID, tenant/run/parent IDs, logical key, owner agent/version, state, goal, input/output schema refs, deadline, priority, current revision; unique (tenant\_id, run\_id, logical\_key) |
| TaskDependency | from/to task, dependency type, satisfaction condition; graph compiler prevents unauthorized cycles |
| TaskAttempt | task ID, attempt number, worker/child-workflow ID, start/end, outcome, retry class, trace ID; append-only |
| OwnershipTransfer | task ID, from/to owner, previous/new authority grant, proposal hash, reason, timestamp, actor; transactionally updates Task.owner |
| TaskArtifact | task ID, role (input/partial/output/evidence), immutable artifact URI/hash, schema, producer, classification |
| JoinPolicy | join node, required predecessors, all/quorum/first-valid strategy, timeout, conflict resolver, partial-result policy |

### State, consistency, and scale

* Partition operational rows, workflow queues, and read models by tenant\_id + run\_id; all tasks in one run should have a stable home shard so parent/child transitions are local.
* Let the durable workflow instance serialize control decisions for one run. Scale across runs horizontally; do not use a global coordinator or distributed lock for ordinary task ownership.
* Dispatch by capability + region + risk\_class + priority. A receiver queue contains task references, not full sensitive context; workers fetch authorized artifacts after assignment.
* Use a strongly consistent transaction for task creation, owner transfer, terminal transition, and budget reservation. Graph/UI projections, search indexes, and analytics may be eventually consistent.
* Enforce manifest-level defaults such as max\_delegation\_depth, max\_children\_per\_task, max\_parallel\_children, and max\_plan\_revisions; risk policy may lower them per run.
* Store the authoritative graph as normalized tasks/edges; publish an incrementally updated materialized projection for fast operator queries. Large evidence and messages remain in object storage.
* Mitigate “hot runs” by batching status events, limiting concurrent ready nodes, and applying per-run semaphores. A single run should not require more coordinator throughput than its bounded fan-out permits.
* Idempotent task creation and completion make queue redelivery safe. Task terminal state plus accepted artifact hash is immutable; corrections create a new revision/task rather than reopening history.

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Collaboration claim | Multi-agent structure does not inherently improve quality. Add specialists only when capability, ownership, trust, isolation, or parallelism justifies coordination cost, and evaluate against the strongest single-agent baseline. | MULTIAGENT; A2A-101 |

Evidence anchors: MULTIAGENT; A2A-101. Full URLs, authority, version, and scope appear in Appendix M.

## Pattern reference — Supervisor/Worker

|  |
| --- |
| **PROBLEM**  One outcome requires specialist work that benefits from parallelism or separate capability boundaries while a single component retains overall ownership. |

### Architecture and flow

The supervisor creates typed child tasks with narrower grants and acceptance criteria. Workers return artifacts; the supervisor or deterministic join validates and aggregates them.

1. Decompose only along meaningful specialist boundaries.
2. Create durable TaskEnvelopes and child capability envelopes.
3. Schedule independently with deadlines and cancellation lineage.
4. Collect artifacts under explicit join semantics.
5. Resolve conflicts and accept the parent outcome.

| **Use when** | **Do not use when** |
| --- | --- |
| Use when specialists differ in tools, data, trust, cost, SLO, ownership, or deployment and parallel work helps. | Avoid when one agent with tools is simpler, context is inseparable, or coordination cost exceeds specialization gain. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Specialization and parallelism | More coordination, cost, cancellation, and artifact validation. |
| One parent owner | Clear accountability; can become a bottleneck. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Runaway fan-out | Depth, child, concurrency, cost, and time budgets. |
| Conflicting artifacts | Schema, provenance, version, quorum, precedence, or human resolution. |
| Child leakage | Narrow grant, data, context, and egress boundaries. |

### Minimum observability

* task tree
* current owners
* grant lineage
* child state and budget
* join condition
* conflicts and resolution

## Pattern reference — Multi-Agent Collaboration

|  |
| --- |
| **PROBLEM**  Several autonomous or semi-autonomous components must exchange tasks and artifacts while preserving ownership, authority, evidence, and recovery. |

### Architecture and flow

Collaboration uses durable TaskEnvelope, message, status, artifact, cancellation, and join contracts; conversation is advisory, while workflow state determines truth.

1. Create a task with owner, goal, acceptance, grant, budget, and deadline.
2. Exchange authenticated versioned messages and artifacts.
3. Persist statuses and correlation independently of chat context.
4. Adopt artifacts only after schema, provenance, quality, and policy validation.
5. Join, cancel, escalate, or compensate under explicit rules.

| **Use when** | **Do not use when** |
| --- | --- |
| Use across teams, regions, vendors, trust domains, or independently recoverable specialist work. | Avoid free-form agent conversations as the sole coordination mechanism. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Organizational scale | More protocol, trust, compatibility, and operations work. |
| Independent ownership | Improves isolation; complicates global optimization and debugging. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Split ownership | Single current owner and versioned transfer. |
| Message duplication or reordering | Inbox dedupe, sequence, expected version, and idempotent reducers. |
| Remote task never completes | Deadline, heartbeat, cancellation, fallback, and intervention. |

### Minimum observability

* task and message IDs
* peer identity
* owner version
* status history
* artifact lineage
* deadline, cancellation, and join outcome

## Implementation reference


### Durable child-task contract

PYTHON · implementation excerpt

```python
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
class TaskEnvelope(BaseModel):
    task_id: str
    parent_task_id: str | None
    owner_agent: str
    capability: str
    goal: str
    acceptance_contract: str
    capability_grant_id: str
    input_artifact_ids: tuple[str, ...]
    deadline: datetime
    maximum_cost_usd: float = Field(ge=0)
    cancellation_parent_id: str
    state_version: int = 0
```

### Monotonic child authority

PYTHON · implementation excerpt

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def _resource_within(child: str, parent: str) -> bool:
    if parent.endswith("://"):
        return child.startswith(parent)
    normalized = parent.rstrip("/")
    return child == normalized or child.startswith(normalized + "/")


@dataclass(frozen=True)
class CapabilityEnvelope:
    grant_id: str
    subject_id: str
    actor_id: str
    actions: frozenset[str]
    resource_prefixes: frozenset[str]
    purposes: frozenset[str]
    data_classes: frozenset[str]
    regions: frozenset[str]
    maximum_risk: int
    maximum_cost_usd: float
    delegation_depth: int
    expires_at: datetime

    def assert_current(self, now: datetime | None = None) -> None:
        current = now or datetime.now(timezone.utc)
        if self.expires_at <= current:
            raise PermissionError("capability envelope expired")


def derive_child(
    parent: CapabilityEnvelope,
    child: CapabilityEnvelope,
    *,
    now: datetime | None = None,
) -> CapabilityEnvelope:
    """Prove monotonic narrowing; actor identity may change, subject may not."""

    parent.assert_current(now)
    if child.subject_id != parent.subject_id:
        raise PermissionError("subject cannot change")
    if not child.actions <= parent.actions:
        raise PermissionError("actions broadened")
    if not child.purposes <= parent.purposes:
        raise PermissionError("purposes broadened")
    if not child.data_classes <= parent.data_classes:
        raise PermissionError("data classes broadened")
    if not child.regions <= parent.regions:
        raise PermissionError("regions broadened")
    if child.maximum_risk > parent.maximum_risk:
        raise PermissionError("risk ceiling raised")
    if child.maximum_cost_usd > parent.maximum_cost_usd:
        raise PermissionError("cost ceiling raised")
    if child.delegation_depth >= parent.delegation_depth:
        raise PermissionError("delegation depth was not reduced")
    if child.expires_at > parent.expires_at:
        raise PermissionError("lifetime extended")
    for resource in child.resource_prefixes:
        if not any(_resource_within(resource, allowed) for allowed in parent.resource_prefixes):
            raise PermissionError("resource scope broadened")
    return child
```

## Debugging playbook

1. Build the durable task tree and identify the current owner of every node.
2. Verify each child grant is a subset of the parent grant.
3. Inspect join semantics, missing artifacts, duplicates, and conflicts.

## Production checklist

**✓** Another agent exists only when expertise, tools, data, trust, ownership, SLO, or scaling truly differs.

**✓** Delegation creates a typed durable task with one current owner.

**✓** Child authority is provably narrower than parent authority.

**✓** Joins define all, quorum, first-valid, or fallback semantics and conflict policy.

**✓** MCP and A2A pass through gateways that verify peers, schemas, artifacts, quotas, and cancellation.

## Exercises

1. Design supervisor/worker fan-out with quorum and a deterministic conflict rule.
2. Model cascading cancellation across two local agents and one remote task.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| When is a multi-agent system justified? | When meaningful boundaries differ—domain, tools, data access, owner, deployment, SLO, or cost—not merely because multiple personas sound sophisticated. |
| Compare an agent-as-tool, a handoff, and a durable child task. | An in-run specialist with parent control; conversational control transfer; or independently owned durable work with retries, waits, deadlines, and cancellation. |
| How do you prevent delegation from escalating privilege? | Derive child authority by intersection; narrow action, resource, data, time, budget, and depth; reauthorize each invocation; issue scoped last-hop credentials. |
| How should fan-in be implemented? | Persist child states and artifacts, wait for an explicit join condition, then validate schemas, provenance, conflicts, quality, and policy deterministically. |
| What does an A2A or MCP protocol not solve? | Business authorization, peer trust, quality, tenant isolation, effect semantics, artifact safety, cancellation guarantees, and audit remain local platform responsibilities. |


## Transition to Chapter 19

Multi-agent collaboration inside one platform is only part of the problem; Chapter 19 governs cross-platform tools, agents, APIs, and events.

# 19 — MCP, A2A, and External Integration

> **Evidence note.** MCP 2026-07-28 defines a stateless, self-contained protocol core for resources, prompts, and tools, while A2A v1.0.1 defines agent cards and task/message/artifact exchange. Neither protocol transfers application authorization or business acceptance automatically. [R05][R06][R07]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Northstar consumes a third-party screening MCP server and delegates regional verification to a partner agent through A2A. Protocol conformance makes messages interoperable; it does not make the endpoint trusted or the artifact safe to adopt. |

|  |
| --- |
| **DESIGN DECISION**  Terminate MCP and A2A at governed local gateways; verify endpoints, artifacts, authority, quotas, and effect semantics locally. |

## What this chapter delivers

Federate tools and agents through locally governed gateways, registries, task protocols, and artifact adoption controls.

## Solution blueprint


Figure 13. MCP, A2A, and External Integration.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| MCP and A2A Gateways | local trust domain to external endpoint or peer | endpoint · peer · tenant quota | one remote call or task | ServerManifest · A2ATask · ArtifactEnvelope |

## Two protocols, two responsibilities

MCP standardizes how a host discovers and invokes tools, resources, and prompts exposed by a server. A2A standardizes collaboration around tasks, messages, status, streaming, artifacts, and cancellation. They can coexist: a local agent may use MCP for a capability and A2A to delegate independently owned work.

Northstar terminates both protocols at gateways. The MCP Gateway resolves a pinned server manifest, authenticates the endpoint, filters tools, validates schemas, applies tenant and user policy, constrains egress, and wraps mutating calls in effect semantics. The A2A Gateway verifies peer identity and trust profile, translates local TaskEnvelope to the negotiated protocol, persists status, enforces deadlines and quotas, and scans returned artifacts before local adoption.

### Registry model

A server or peer registry entry contains owner, endpoint, protocol version and profile, authentication method, trust material, schemas, supported capabilities, data classifications, regions, risk, rate limits, health, release aliases, evaluation evidence, and revocation state. Discovery never substitutes for authorization.

### MLflow MCP Registry note

MLflow 3.15.0 introduced experimental MCP Registry capabilities for registering servers, managing versions and aliases, creating access endpoints, and discovering tools. Northstar can use this as an operational registry surface while retaining business authorization, tenant policy, credential exchange, and effect control in its platform gateways. Because the feature is experimental, pin exact MLflow and registry schema versions and test migration and rollback.

## Agent-to-agent communication and task ownership

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Independent agents need to discover capabilities, delegate work, exchange artifacts, propagate failure, and agree on ownership without exposing internal prompts or state. |
| Why it is difficult | Natural-language messages are ambiguous; remote agents have separate identities and SLOs; asynchronous tasks outlive connections; protocol interoperability does not guarantee shared authorization or semantics. |
| Design alternatives | In-process calls; queue topics; shared blackboard; RPC; workflow child runs; MCP tool exposure; A2A tasks and messages. |
| Recommended architecture | For agents under one platform, use workflow-native child tasks. Across deployment or vendor boundaries, use an A2A gateway with typed task/artifact envelopes and authenticated async operations. Use MCP for tools/resources. Never use conversation alone as the durable task record. |
| Trade-offs | Standard protocols reduce integration cost but cover transport more than governance. A gateway may reduce protocol features, yet it supplies policy, tenant binding, quotas, schema validation, and audit. |
| Failure scenarios | Agent advertises a misleading capability; task status is lost; result schema differs; duplicate delegation starts duplicate work; parent cancels but child continues; remote agent requests broader rights. |
| Enterprise example | A procurement platform delegates sanctions screening to a separately operated agent. The remote agent receives document references and read-only scope, returns a signed screening artifact, and cannot place or approve the order. |

### Protocol roles

| **Mechanism** | **Best use** | **Not sufficient for** |
| --- | --- | --- |
| Direct function call | Low-latency, same-process specialist | Independent lifecycle, failure isolation, cross-team deployment |
| Durable child workflow | Same trust domain, long-running task with strong parent/child semantics | Cross-vendor discovery and open interoperability |
| Event bus | Facts, triggers, status distribution, loose coupling | Request ownership, interactive clarification, synchronous results |
| MCP | Tools, prompts, and resources exposed to an agent | Full multi-agent task lifecycle and enterprise authorization policy |
| A2A | Agent discovery, messages, stateful tasks, streaming/push updates, artifacts | Internal durable execution, shared business transactions, policy authority |
| Shared blackboard | Experimental collaboration and broad exploration | Transactional ownership, tenant isolation, deterministic conflict resolution |

A2A’s task/message/artifact model and async operations are useful at remote-agent boundaries. Its agent card is discovery metadata—not proof of trust. Pin the card version or digest, verify issuer and endpoint, and filter advertised skills through enterprise policy.

### Required TaskEnvelope

| **Field group** | **Minimum contents** |
| --- | --- |
| Identity | task\_id, parent\_run\_id, context\_id, tenant, requester subject, caller workload, receiving agent/version |
| Goal | Bounded objective, non-goals, acceptance criteria, priority, deadline |
| Data | Immutable input artifact references, content hashes, provenance, classification, permitted purpose |
| Contract | Input/output schemas, artifact media types, status model, protocol version |
| Authority | Allowed capabilities/resources, denied operations, maximum delegation depth, expiry |
| Budgets | Tokens, currency, wall time, steps, tool calls, parallelism, data-egress limit |
| Reliability | Idempotency key, retry ownership, heartbeat, cancel semantics, compensation owner |
| Observability | Trace/span context, causation/correlation IDs, sampling class, audit references |

### Ownership and failure rules

* A task has exactly one current owner and one parent coordinator; leases may move execution, but ownership changes are transactional and audited.
* The receiver may reject, accept, request input, produce partial artifacts, complete, fail, or acknowledge cancellation. Terminal tasks cannot accept new work; create a new task for follow-up.
* Cancellation propagates downward by default; compensation does not automatically propagate and must follow domain policy.
* Child failure is data. The parent chooses fail-fast, quorum, fallback, partial result, targeted retry, or human escalation based on the join contract.
* Aggregators validate schema, provenance, duplicate claims, evidence quality, and conflict policy. They do not concatenate prose and call it consensus.
* Shared mutable state is prohibited across trust domains. Exchange immutable artifacts or versioned patches; use optimistic concurrency for authorized updates.

### Detailed design — APIs, data model, and scalability

### Component boundaries

The Agent Directory stores validated cards and endpoint metadata; the Peer Trust Registry stores organizational trust and allowed purposes; the A2A Gateway terminates authentication and protocol bindings; the Task Bridge maps remote tasks to internal child workflows; the Artifact Broker exchanges immutable references; the Subscription Dispatcher handles push/status delivery; and the Trace Bridge links remote and local causal graphs.

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/peers | Register remote agent issuer/domain, trust material, approved endpoints, allowed skills/purposes, risk ceiling, and data boundary |
| POST /v1/peers/{peer\_id}:refreshCard | Fetch and verify agent card; new digest remains pending until compatibility/policy checks pass |
| GET /v1/agents:resolve?skill=...; region=... | Resolve policy-eligible local or remote agents; discovery never returns a grant |
| POST /v1/federated-tasks | Create an internal durable child task and dispatch an A2A task/message idempotently |
| GET /v1/federated-tasks/{task\_id} | Return canonical local state, mapped remote state, artifacts, heartbeat, deadlines, and trace links |
| POST /v1/federated-tasks/{task\_id}/messages | Send typed clarification or additional artifact reference under the existing authority ceiling |
| POST /v1/federated-tasks/{task\_id}:cancel | Persist parent cancellation first, relay to peer, and track acknowledgment/terminal state separately |
| POST /v1/a2a/callbacks | Authenticated ingress for peer status/artifact events with source+event ID deduplication |
| POST /v1/federated-tasks/{task\_id}:adoptResult | Validate remote terminal artifact and explicitly commit it into the parent workflow |

At an open boundary, expose the standard A2A agent-card and task/message operations. Internally, normalize every binding to the platform’s task state, identity, artifact, error, and audit contracts.

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| RemoteAgent | peer/agent ID, issuer, card URI/digest/version, endpoints/bindings, skills, auth schemes, owner, region, trust/risk status, last verification |
| PeerTrustPolicy | peer, allowed tenants/purposes/data classes/skills, max risk, required assurance, artifact rules, rate limits, expiry |
| FederatedTask | local task ID, remote task/context IDs, parent run, peer/agent/version, authority grant, state mapping, idempotency key, deadline, budget, last heartbeat |
| FederatedMessage | task, direction, message/event IDs, role/type, parts/artifact refs, payload hash, sequence/logical time, verification status |
| RemoteArtifact | remote and local artifact IDs, URI/reference, media/schema, content hash, producer signature/attestation, classification, scan/validation state |
| CallbackSubscription | peer/task, endpoint handle, event types, auth key/version, expiry, delivery cursor, failure policy |
| PeerObservation | latency, availability, schema violations, security findings, cancellation compliance, quality score; evidence for routing, not silent trust escalation |

### State mapping and ownership

| **Canonical local state** | **Remote interpretation** | **Parent behavior** |
| --- | --- | --- |
| Created/Dispatched | Submitted/message sent | Retry dispatch only with same idempotency key |
| Accepted/Running | Task working/streaming | Monitor heartbeat and deadline |
| NeedsInput | Input-required state/message | Route a typed question to parent/user; budget clock follows policy |
| CompletedPendingValidation | Remote task completed | Quarantine artifacts until schema, provenance, malware, policy, and acceptance checks pass |
| Succeeded | Local adoption committed | Parent may satisfy dependency |
| CancelRequested | Cancel sent | Stop issuing new authority; continue monitoring possible effects |
| Failed/Expired/InterventionRequired | Terminal or ambiguous remote outcome | Apply parent join/reconciliation policy |

### Scalability, federation, and failure isolation

* Partition task-relay state by tenant + peer domain + task ID. Serialize updates for one federated task while scaling across tasks and peers.
* Prefer asynchronous callbacks or streaming for progress; poll only as a bounded fallback with exponential backoff. Persist callbacks before acknowledgment.
* Enforce per-peer and per-skill rate, concurrency, byte-egress, and cost budgets. Circuit-break a misbehaving peer without disabling unrelated local agents.
* Exchange large or sensitive data by short-lived, audience-bound artifact references. Validate recipient, region, classification, and purpose before issuing each reference.
* Carry W3C trace context when supported and create span links when the remote system returns a different trace. Never rely on a remote trace as the enterprise audit record.
* Keep peer card/configuration reads cached by signed digest, but re-evaluate authorization and trust policy per task/message. Card changes cannot alter an in-flight task’s pinned contract.
* Bound remote fan-out at the parent. A peer may not recursively delegate unless the task grant explicitly permits a depth and the resulting chain remains visible.
* Treat missed heartbeat, callback failure, cancellation ambiguity, and artifact validation failure as distinct states; do not automatically resubmit a potentially active remote task.

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| MCP correction | Use MCP 2026-07-28 for new designs: the core is stateless, initialize and Mcp-Session-Id are removed, requests carry protocol/capability metadata, and server/discover supports version selection. Application state uses explicit handles. Tasks and Skills over MCP are optional extensions, not core guarantees. | MCP-2026; MCP-CHANGELOG |
| MCP authorization | Use protected-resource and authorization-server discovery, PKCE, audience/resource binding, short-lived tokens, step-up scopes, issuer validation, and SSRF-safe metadata retrieval. Token passthrough to an upstream API is forbidden. | MCP-AUTH; RFC8707; RFC9728 |
| A2A correction | Pin A2A 1.0.1. Normative operations include SendMessage, GetTask, ListTasks, CancelTask, and SubscribeToTask; local /v1 bridges are Northstar APIs, not A2A endpoints. Cancellation is best effort and authorization must prevent task-existence leakage. | A2A-101 |

Evidence anchors: MCP-2026; MCP-AUTH; A2A-101. Full URLs, authority, version, and scope appear in Appendix M.

## Implementation reference


### A2A task envelope

PYTHON · implementation excerpt

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class A2ATaskEnvelope(BaseModel):
    task_id: str
    parent_task_id: str | None = None
    owner: str
    goal: str
    acceptance_contract: str
    capability_grant_id: str
    input_artifact_ids: tuple[str, ...]
    deadline: datetime
    maximum_cost_usd: float = Field(ge=0)
    status: Literal[
        "submitted", "working", "waiting", "completed",
        "failed", "cancel_requested", "canceled",
    ] = "submitted"
    expected_version: int = 0
```

### MLflow MCP Registry adapter

PYTHON · implementation excerpt

```python
from __future__ import annotations
import os
from typing import Literal
import mlflow
from mlflow.entities import Feedback, SpanType, Trace
from mlflow.genai import scorer
from mlflow.genai.judges import make_judge
from mlflow.genai.scorers import Correctness, Guidelines, ToolCallCorrectness, ToolCallEfficiency

def register_supplier_mcp_server():
    """MLflow 3.15 MCP Registry is experimental; pin exact versions in releases."""
    return mlflow.genai.register_mcp_server(
        server_json={
            "name": "com.northstar/supplier-tools",
            "version": "1.2.0",
            "description": "Governed supplier onboarding tools",
            "remotes": [
                {"url": "https://mcp.northstar.example/supplier", "type": "streamable-http"}
            ],
        },
        status="active",
        create_access_endpoints_from_remotes=True,
    )

def resolve_production_mcp_server():
    return mlflow.genai.get_mcp_server_version_by_alias(
        name="com.northstar/supplier-tools", alias="production"
    )
```

## Debugging playbook

1. Verify the registry version, endpoint identity, protocol profile, and trust material.
2. Inspect local authorization and quota decisions for one remote call.
3. Validate the returned artifact hash, schema, classification, provenance, and scan result.

## Production checklist

**✓** MCP and A2A endpoints terminate at authenticated governed gateways.

**✓** Registry entries pin endpoints, owners, trust, schemas, and versions.

**✓** Per-call or per-task authority, quotas, classification, and egress are checked locally.

**✓** Remote artifacts are scanned and adopted under local policy.

**✓** Cancellation, retries, idempotency, effects, and audit have local semantics.

## Exercises

1. Wrap an MCP tool with a local Tool Gateway policy.
2. Define an A2A TaskEnvelope with status, cancellation, and artifact adoption semantics.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| What does MCP standardize? | How hosts discover and invoke server tools and resources; it does not establish business authorization or endpoint trust. |
| What does A2A add? | Durable task, message, status, artifact, streaming, and cancellation semantics across agent boundaries. |
| Why put protocol gateways at the boundary? | To verify peers, schemas, authority, quotas, classifications, artifacts, egress, effects, and audit using local policy. |
| How should a remote artifact be adopted? | Authenticate the source, validate schema and hash, scan content, enforce classification and provenance, then copy or reference under local policy. |
| How do you version external capabilities? | Pin registry entry, endpoint, protocol profile, schemas, trust material, tool or agent version, and tested compatibility in the release manifest. |

|  |
| --- |
| **PART IV**  **ENTERPRISE CONTROL**  Control context, state, identity, authorization, effects, security, and governance outside the model. |

14 Context Engineering, Memory, and State

15 Identity, RBAC/ABAC, and Delegated Authorization

16 Tool Security, Effects, Idempotency, and Approval

17 Sandboxing, Egress, Data Security, and Governance


## Transition to Chapter 20

External integrations are bounded; Chapter 20 isolates model-provider access and policy in the LLM Gateway control plane.
