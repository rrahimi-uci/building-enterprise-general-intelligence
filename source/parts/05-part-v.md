# PART V — WORKING TOGETHER ACROSS BOUNDARIES

Once a system has more than one worker—or reaches beyond its own process—the
conversation becomes a distributed protocol. This Part makes the ownership,
authority, cancellation, and artifact rules explicit for internal specialists
and external peers alike. It also keeps a useful distinction in view: a
protocol can move a message without granting permission to act.

# 18 — Coordinate Specialists Without Losing Control

> **Evidence context:** Public multi-agent implementation reports describe supervisor/specialist designs and substantial token/context trade-offs; these observations justify explicit topology and cost tests rather than universal multi-agent adoption. **[R28][R33]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Document extraction, income verification, property review, and policy specialists can run concurrently, but a plausible multi-agent conversation is not a coordination protocol. Harborlight defines durable tasks, one owner per task, narrowed authority, explicit joins, and artifact contracts. |

|  |
| --- |
| **THE DESIGN CHOICE** Give one component ownership of each task, derive narrower child authority, and define explicit join and cancellation semantics. |

## Why more agents do not automatically make a better system

Multiple agents can shorten a workflow, but conversation alone does not tell
you who owns a task, who may cancel it, or which result wins when specialists
disagree. Chapter 17 showed the two ways this goes wrong: chat used as the
workflow (AP-08) and budgets that reset at every hop (AP-11). This chapter
builds the replacement: a task tree with one owner per task, narrowing
authority, explicit joins, and durable cancellation.

## What every collaboration must make explicit

Every additional agent introduces another scheduler, context boundary, identity, budget, and failure mode. That cost is justified when a specialist has meaningfully different expertise, data access, tools, ownership, latency, or scaling needs. It is not justified merely because a multi-agent conversation looks modular. The collaboration contract makes the cost visible by requiring each task to have one owner, one capability envelope, explicit artifacts, and a rule for joining or canceling work.


| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Task Service and supervisor workflow | parent/child authority and artifact adoption | task tree · specialist queue | one child task | TaskEnvelope · CapabilityEnvelope · JoinPolicy |

## Treat collaboration as durable work, not conversation

[[DIAGRAM:supervisor-worker|Figure 18-1 — Supervisor/worker: narrowed child grants, an explicit fan-in contract, and durable cancellation]]

Harborlight’s supervisor owns the evidence-package outcome and creates durable child tasks for document extraction, income verification, property review, and policy explanation. The extraction child runs Chapter 5's document ingestion as a capability and returns a KnowledgeArtifact, not free text. Each child receives only the capability, evidence, budget, deadline, and cancellation scope it needs.

Each child's authority is a *capability envelope*: the maximum actions, resources, purposes, data classes, regions, risk, cost, delegation depth, and lifetime it may use. The Task Service derives it from the parent's envelope by intersection and refuses any child envelope that is not a provable subset. Chapter 21 defines the envelope and gives the subset proof.

Fan-in is explicit: wait for all, quorum, first valid, or fallback. Artifact conflicts use deterministic precedence, source freshness, verification status (Chapter 5), confidence thresholds, or human resolution. Free-form conversation may help agents explain results, but it cannot replace task status, ownership, artifact, or effect records.

Nested delegation multiplies cost and risk. The Task Service caps depth, children, concurrency, total turns, total tokens, external calls, and wall-clock time across the entire task tree (the AP-11 correction). Parent cancellation propagates as durable intent; a child with an executing mutation must reconcile before acknowledging final cancellation (Chapter 22 § A reliable protocol for changing the outside world).

## Choose a topology—and define how the work ends

Central coordination is easier to govern but can bottleneck; decentralized collaboration may widen coverage at the cost of determinism, auditability, and cost control. Routing and handoff keep the meanings from Chapter 11: routing chooses a worker; handoff transfers accountability and completes only when the recipient acknowledges.

### Topology decision table

| **Pattern** | **Use when** | **Avoid when** | **Control model** |
| --- | --- | --- | --- |
| One model call + retrieval | Answer is bounded and no external side effect is needed | Task requires iterative environmental feedback | Request/response |
| Single agent loop | Open-ended steps share the same permissions, context, and owner | Multiple teams or security zones must be isolated | One agent, bounded tool loop |
| Deterministic workflow | Steps and invariants are known | Discovery or decomposition cannot be anticipated | Code/state machine owns routing |
| Router + specialists | Inputs fall into stable classes with distinct prompts/tools | Classification is unstable or branches share nearly all context | Deterministic or model router with confidence threshold |
| Manager + agents as tools | One coordinator must synthesize a final answer | Specialist should own the user relationship | Parent retains task ownership |
| Handoff | A specialist must take over the next user-facing branch | The work is a hidden bounded subtask | Ownership transfers only when the recipient accepts |
| Hierarchical fan-out/fan-in | Subtasks are independent and benefit from parallelism | Shared mutable context or tight ordering dominates | Coordinator sets fan-out and aggregation contract |
| Peer swarm / group chat | Research exploration where diversity is worth the cost | Regulated decisions, side effects, or strict SLOs | Experimental; hard budgets and sandbox only |

### Recommended orchestration rules

* **Creation:** instantiate agents from an immutable AgentSpec; never construct production instructions and permissions ad hoc in a prompt.
* **Delegation:** create a child task carrying a TaskEnvelope (§ Durable child-task contract).
* **Handoff:** follow Chapter 11's acknowledged transfer. The Ownership Service records it as an OwnershipTransfer with a narrowed capability envelope; the prior owner remains accountable until the recipient accepts and is kept as history afterward, not as a competing owner.
* **Coordination:** use a workflow node, not a group chat, to decide readiness, joins, retries, cancellation, and aggregation.
* **Shared state:** store it in a concurrency-controlled state service. Agents receive snapshots and return proposed patches with expected versions.
* **Termination:** terminal transitions follow the task lifecycle below; the model may recommend completion but cannot make the transition.
* **Plan changes:** use Chapter 12's revision protocol; new nodes are validated against the original capability envelope, and materially broader scope needs new approval.

### Task lifecycle

| **State** | **Entered when** | **Who may move it on** |
| --- | --- | --- |
| Created/Dispatched | The Task Service persists the TaskEnvelope under its idempotency key and queues it for the receiver | The receiver accepts or rejects; the parent may cancel |
| Accepted/Running | The receiver calls `:accept` with the expected version; a child workflow starts (Chapter 15) | The owner, by completing, failing, or requesting input |
| NeedsInput | The owner needs a clarification, document, or approval it cannot obtain itself | The parent or user supplies it; the deadline moves it to Expired |
| CompletedPendingValidation | The owner submits artifacts through `:complete`; they stay quarantined | The Task Service, after schema, provenance, and acceptance checks |
| Succeeded | Validation passes and the parent's join adopts the artifacts (Chapter 15 § Terminal correctness) | No one; terminal |
| CancelRequested → Canceled | The parent persists cancellation intent; Canceled only after any executing mutation reconciles | The Task Service, once children acknowledge and effects settle |
| Failed / Expired | A typed failure (including the receiver's rejection) or a passed deadline | No one; terminal, and the parent applies its join policy |
| InterventionRequired | An outcome no rule can settle; an intervention task opens (Chapter 14) | The intervention task's response; non-terminal until it resolves the task (Chapter 15 § Terminal correctness) |

The receiver may reject, accept, request input, produce partial artifacts, complete, fail, or acknowledge cancellation. Terminal states reuse Chapter 15's run terminal names, and a terminal task accepts no new work; follow-up is a new task. Cancellation propagates downward by default; compensation does not propagate automatically and follows domain policy (Chapter 22).

## A workable implementation

### Who should own each decision

| **Component** | **Owns** | **Does not own** |
| --- | --- | --- |
| Agent Registry | Immutable agent versions, capability declarations, compatibility, ownership | Per-run mutable state |
| Run Coordinator | Goal lifecycle, child-task policy, terminal decision; requests plan revisions from the Plan Service (Chapter 12) | Provider-specific model calls or connector credentials |
| Task Service | Task records, dependencies, assignment, deadlines, idempotent creation | Business effects performed by the task |
| Ownership Service | Ownership transfers (pending until accepted), leases, cancellation tree, current accountable owner | Natural-language routing judgment |
| Router | Ranked eligible agents/tools using manifest, health, policy, cost, and locality (Chapter 11's route service) | Authorization or unrestricted discovery |
| Join/Aggregation Service | Readiness, quorum, schema validation, conflict policy, accepted result | Free-form “consensus” without evidence |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| GET /v1/agents/{agent\_id}/versions/{version} | Resolve a pinned manifest; ETag is the manifest digest |
| POST /v1/runs/{run\_id}/tasks | Idempotently create a child task from a TaskEnvelope; refuse a capability envelope that is not a subset of the parent's |
| POST /v1/tasks/{task\_id}:accept | Receiver accepts a new child task or a pending ownership transfer using expected\_version; starts or binds a child workflow (Chapter 15) |
| POST /v1/tasks/{task\_id}:handoff | Propose an ownership transfer to a target agent/version with rationale, obligations, deadline, remaining budget, and narrowed capability envelope; the transfer stays pending until the recipient calls `:accept` with expected\_version; rejection or expiry leaves the current owner accountable |
| POST /v1/tasks/{task\_id}:complete | Submit typed result/artifacts; server runs acceptance and provenance checks before terminal transition |
| POST /v1/tasks/{task\_id}:fail | Record typed failure, retryability, partial artifacts, and recommended parent disposition |
| POST /v1/tasks/{task\_id}:cancel | Request hierarchical cancellation; response distinguishes requested, acknowledged, and completed |
| GET /v1/runs/{run\_id}/graph | Read materialized task/dependency/owner/status graph for UI and operations |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| AgentVersion | (tenant\_id, agent\_id, version), digest, instructions digest, tool allowlist, schemas, owner, risk tier, lifecycle state; immutable after release |
| Task | task ID, tenant/run/parent IDs, logical key, owner agent/version, state (§ Task lifecycle), goal, input/output schema refs, deadline, priority, current revision; unique (tenant\_id, run\_id, logical\_key) |
| TaskDependency | from/to task, dependency type, satisfaction condition; graph compiler prevents unauthorized cycles |
| TaskAttempt | task ID, attempt number, worker/child-workflow ID, start/end, outcome, retry class, trace ID; append-only |
| OwnershipTransfer | the handoff record of Chapter 11: task ID, from/to owner, previous/new capability envelope, obligations, deadline, acknowledgment state (proposed, accepted, rejected, expired), proposal hash, reason, timestamp, actor; updates Task.owner only on acceptance |
| TaskArtifact | task ID, role (input/partial/output/evidence), immutable artifact URI/hash, schema, producer, classification |
| JoinPolicy | join node, required predecessors, all/quorum/first-valid strategy, timeout, conflict resolver, partial-result policy |

### State, consistency, and scale

* Partition by tenant + run so a run's tasks are shard-local; let the run's durable workflow serialize its control decisions; use strongly consistent transactions for task creation, owner transfer, terminal transition, and budget reservation, and eventually consistent projections for the graph and analytics.
* Dispatch by capability + region + risk class (Chapter 22) + priority. A receiver queue contains task references, not full sensitive context; workers fetch authorized artifacts after assignment.
* Enforce manifest-level defaults such as max\_delegation\_depth, max\_children\_per\_task, max\_parallel\_children, and max\_plan\_revisions; risk policy may lower them per run.
* Mitigate “hot runs” by batching status events, limiting concurrent ready nodes, and applying per-run semaphores. A single run should not require more coordinator throughput than its bounded fan-out permits.
* Idempotent task creation and completion make queue redelivery safe. Task terminal state plus accepted artifact hash is immutable; corrections create a new revision/task rather than reopening history.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Collaboration claim | R28 reports a supervisor/specialist research architecture and its token and context costs; R33 documents a managed supervisor/collaborator pattern. The book's recommendation, not a sourced finding, is to add specialists only when capability, ownership, trust, isolation, or parallelism justifies the cost, and to evaluate against the strongest single-agent baseline. | R28; R33 |

The discussion above draws on R28; R33. Appendix K lists the complete sources and records their authority, version, and scope.

## Supervisor/Worker at a glance

### How the pattern works

1. Decompose only along meaningful specialist boundaries.
2. Create durable TaskEnvelopes and child capability envelopes.
3. Schedule independently with deadlines and cancellation lineage.
4. Collect artifacts under explicit join semantics and adopt them only after schema, provenance, quality, and policy validation.
5. Resolve conflicts and accept the parent outcome.

| **Use when** | **Do not use when** |
| --- | --- |
| Use when specialists differ in tools, data, trust, cost, SLO, ownership, or deployment and parallel work helps. | Avoid when one agent with tools is simpler, context is inseparable, or coordination cost exceeds specialization gain, or when free-form conversation would be the only coordination record. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Specialization and parallelism | More coordination, cost, cancellation, and artifact validation. |
| One parent owner | Clear accountability; can become a bottleneck. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Runaway fan-out | Depth, child, concurrency, cost, and time budgets. |
| Conflicting artifacts | Schema, provenance, version, quorum, precedence, or human resolution. |
| Child leakage | Narrow grant, data, context, and egress boundaries. |
| Split ownership | Single current owner and versioned OwnershipTransfer. |
| Duplicate or reordered status | Idempotent task creation/completion and expected versions. |
| Ping-pong or circular delegation | Acyclic ownership graph and depth limits. |

### What you need to see in production

* task tree
* current owner and owner version
* grant lineage
* child state and budget
* join condition and outcome
* artifact lineage
* conflicts and resolution

## A sensible place to start

Start with the one contract every child task carries.

### Durable child-task contract

A TaskEnvelope carries eight field groups:

| **Field group** | **Minimum contents** |
| --- | --- |
| Identity | task\_id, parent\_run\_id, tenant, requester subject, caller workload, receiving agent/version |
| Goal | Bounded objective, non-goals, acceptance criteria, priority, deadline |
| Data | Immutable input artifact references, content hashes, provenance, classification, permitted purpose |
| Contract | Input/output schemas, artifact media types, status model (§ Task lifecycle) |
| Authority | Capability envelope reference (`capability_grant_id`), denied operations, maximum delegation depth, expiry |
| Budgets | Tokens, currency, wall time, steps, tool calls, parallelism, data-egress limit |
| Reliability | Idempotency key, dependencies, retry ownership, heartbeat, cancel semantics, compensation owner |
| Observability | Trace/span context, causation/correlation IDs, sampling class, audit references |

The model below carries one field or more from each group, and the Task Service enforces the three rules that make delegation safe: a reused idempotency key returns the original task, a child's delegation depth and budget come out of its parent's, and the capability-envelope subset check (Chapter 21) runs before any child exists.

[[EXAMPLE:contracts#task]]

## If this fails in production

1. Build the durable task tree and identify the current owner of every node.
2. Verify each child grant is a subset of the parent grant (the subset proof in Chapter 21 § A sensible place to start).
3. Inspect join semantics, missing artifacts, duplicates, and conflicts.

If chat is the coordination record or each child gets fresh limits, see AP-08 and AP-11 in Chapter 17.

## What to verify before production

**✓** Another agent exists only when expertise, tools, data, trust, ownership, SLO, or scaling truly differs.

**✓** Delegation creates a typed durable task with one current owner.

**✓** Child authority is provably narrower than parent authority.

**✓** Joins define all, quorum, first-valid, or fallback semantics and conflict policy.

## Put the idea to work

1. Design supervisor/worker fan-out with quorum and a deterministic conflict rule.
2. Model cascading cancellation across two local agents and one remote task.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| When is a multi-agent system justified? | When meaningful boundaries differ—domain, tools, data access, owner, deployment, SLO, or cost—not merely because multiple personas sound sophisticated. |
| What must happen before a parent cancellation is reported complete? | Cancellation is persisted as durable intent and propagated to every child; children with executing mutations reconcile before acknowledging; the API distinguishes requested, acknowledged, and completed. |
| How do you prevent delegation from escalating privilege? | Derive child authority by intersection; narrow action, resource, data, time, budget, and depth; reauthorize each invocation; issue scoped last-hop credentials. |
| How should fan-in be implemented? | Persist child states and artifacts, wait for an explicit join condition, then validate schemas, provenance, conflicts, quality, and policy deterministically. |
| How do you keep a task tree inside its budget? | Children withdraw from the parent's remaining budget rather than receive fresh limits; depth, children, concurrency, and plan revisions are capped by manifest defaults that risk policy may lower; per-run semaphores bound ready nodes. |

## Where this leads next

Inside one platform, the Task Service enforces these rules directly. Chapter 19 carries the same ownership and narrowing rules to tools and agents outside the platform, where a protocol moves the message but not the trust.

# 19 — Crossing System Boundaries: MCP, A2A, and Local Control

> **Evidence context:** MCP 2026-07-28 defines a stateless, self-contained protocol core for resources, prompts, and tools, while A2A v1.0.1 defines agent cards and task/message/artifact exchange. Neither protocol transfers application authorization or business acceptance automatically. **[R05][R06][R07]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Harborlight consumes a third-party income-verification MCP server, and the property-review specialist from Chapter 18 is now a partner-operated agent reached through A2A. Protocol conformance makes messages interoperable; it does not make the endpoint trusted or the artifact safe to adopt. |

|  |
| --- |
| **THE DESIGN CHOICE** Terminate MCP and A2A at governed local gateways; verify endpoints, artifacts, authority, quotas, and effect semantics locally. |

## Why interoperability does not transfer trust

External protocols make it easier to discover and exchange work with tools and
agents outside your boundary. They do not make those endpoints trustworthy, or
their artifacts safe to adopt. An MCP server can describe a tool accurately and
still be unauthorized for this tenant; an A2A peer can accept a task and still
lack the evidence or identity needed to act. Model providers are a third
external boundary; the LLM Gateway that terminates it sits in the Gateways and
integration plane (Chapter 4), and model routing, which filters by policy
before it optimizes, is treated as a cost decision in Chapter 28 (Figure 28-2).

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| MCP and A2A Gateways | local trust domain to external endpoint or peer | endpoint · peer · tenant quota | one remote call or task | ServerManifest · FederatedTask · RemoteArtifact |

## Two protocols, two responsibilities

MCP and A2A are routinely discussed as alternatives. They are not, and choosing
between them is usually the wrong question — they standardize different things,
and a mature system runs both.

| | **MCP** | **A2A** |
| --- | --- | --- |
| Standardizes | How a host discovers and invokes **tools, resources, and prompts** on a server | How peers collaborate around a **task**: messages, status, streaming, artifacts, cancellation |
| Unit of exchange | A tool call and its result | A task with a lifecycle |
| Who owns the work | The caller, throughout | Transfers to the peer, which reports status back |
| Typical use | "Read this record for me" | "Own this sub-goal and tell me when it is done" |
| What it does **not** decide | Whether the caller may invoke the tool | Whether the peer may be trusted with the task |

That last row is the one that matters: neither protocol carries business authorization, so each terminates at a gateway that supplies the decision the protocol omits.

The MCP Gateway resolves a pinned ServerManifest, authenticates the endpoint, filters tools to the caller's eligible set, validates schemas, and constrains egress. It validates audience-bound tokens and never passes an inbound token upstream. A mutating MCP call then continues to the Tool Gateway (Chapter 1), which reauthorizes the exact resource, enforces idempotency, and records the effect receipt; the MCP Gateway decides whether the server and tool may be used, not whether the effect may happen.

The A2A Gateway is the agent-to-agent control point in Chapter 1's gateway table: it decides whether this external peer may receive or return this task, and it terminates the protocol; inside the platform the same decision is made by the Task Service (Chapter 18). It verifies peer identity and trust profile, translates Chapter 18's TaskEnvelope into an A2A task (adding the remote task and context IDs, peer and card digest, and protocol version, recorded in FederatedTask), persists status, enforces deadlines and quotas, and quarantines returned artifacts until local adoption.

### Registry model

A ServerManifest (MCP) or RemoteAgent entry (A2A) contains owner, endpoint, protocol version and profile, authentication method, trust material, schemas, supported capabilities, data classifications, regions, risk, rate limits, health, release aliases, evaluation evidence, and revocation state. It is pinned by digest; a changed manifest is a new version that must pass policy before use. The gateway pins one MCP protocol revision per server and negotiates explicitly; Tasks and Skills over MCP are optional extensions, so durable ownership never depends on them. Discovery never substitutes for authorization (Chapter 8 § Discovery is not permission; AP-12). An operational registry product can host these entries (Appendix D notes the options and their maturity), but it holds metadata, not authorization.

## Delegate work across a trust boundary

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Independent agents need to discover capabilities, delegate work, exchange artifacts, propagate failure, and agree on ownership without exposing internal prompts or state. |
| Why it is difficult | Natural-language messages are ambiguous; remote agents have separate identities and SLOs; asynchronous tasks outlive connections; protocol interoperability does not guarantee shared authorization or semantics. |
| Recommended architecture | For agents under one platform, use workflow-native child tasks. Across deployment or vendor boundaries, use the A2A Gateway with typed task/artifact envelopes and authenticated async operations. Use MCP for tools/resources. Never use conversation alone as the durable task record. |
| Trade-offs | Standard protocols reduce integration cost but cover transport more than governance. A gateway may reduce protocol features, yet it supplies policy, tenant binding, quotas, schema validation, and audit. |
| Failure scenarios | Agent advertises a misleading capability; task status is lost; result schema differs; duplicate delegation starts duplicate work; parent cancels but child continues; remote agent requests broader rights. |

### Protocol roles

| **Mechanism** | **Best use** | **Not sufficient for** |
| --- | --- | --- |
| Direct function call | Low-latency, same-process specialist | Independent lifecycle, failure isolation, cross-team deployment |
| Durable child workflow | Same trust domain, long-running task with strong parent/child semantics | Cross-vendor discovery and open interoperability |
| Event bus | Facts, triggers, status distribution, loose coupling | Request ownership, interactive clarification, synchronous results |
| MCP | Tools, prompts, and resources exposed to an agent | Full multi-agent task lifecycle and enterprise authorization policy |
| A2A | Agent discovery, messages, stateful tasks, streaming/push updates, artifacts | Internal durable execution, shared business transactions, policy authority |
| Shared blackboard | Experimental collaboration and broad exploration | Transactional ownership, tenant isolation, deterministic conflict resolution |

A2A’s task/message/artifact model and async operations are useful at remote-agent boundaries. Its agent card is discovery metadata—not proof of trust. Pin the card version or digest, verify issuer and endpoint, and filter advertised skills through enterprise policy—an advertised A2A skill is discovery metadata, not a certified Skill in the sense of Chapter 8. Across trust domains, never share mutable state: exchange immutable artifacts or versioned patches under optimistic concurrency.

## A workable implementation

### Who should own each decision

The Agent Directory stores validated cards and endpoint metadata for remote agents alongside the Agent Registry's local versions (Chapter 18), and `agents:resolve` queries both; the Peer Trust Registry stores organizational trust and allowed purposes; the A2A Gateway terminates authentication and protocol bindings; the Task Bridge maps remote tasks to internal child workflows; the Artifact Broker exchanges immutable references; the Subscription Dispatcher handles push/status delivery; and the Trace Bridge links remote and local causal graphs.

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/peers | Register remote agent issuer/domain, trust material, approved endpoints, allowed skills/purposes, risk ceiling, and data boundary |
| POST /v1/peers/{peer\_id}:refreshCard | Fetch and verify agent card; new digest remains pending until compatibility/policy checks pass |
| GET /v1/agents:resolve?skill=...&region=... | Resolve policy-eligible local or remote agents; discovery never returns a grant |
| POST /v1/federated-tasks | Create a child task through the Task Service (Chapter 18) and dispatch an A2A task/message idempotently |
| GET /v1/federated-tasks/{task\_id} | Return canonical local state, mapped remote state, artifacts, heartbeat, deadlines, and trace links. Unauthorized callers receive the same response whether or not the task exists |
| POST /v1/federated-tasks/{task\_id}/messages | Send typed clarification or additional artifact reference under the existing capability envelope |
| POST /v1/federated-tasks/{task\_id}:cancel | Persist parent cancellation first, relay to peer, and track acknowledgment/terminal state separately |
| POST /v1/a2a/callbacks | Authenticated ingress for peer status/artifact events with source+event ID deduplication |
| POST /v1/federated-tasks/{task\_id}:adoptResult | Validate remote terminal artifact and explicitly commit it into the parent workflow |

At an open boundary, expose the standard A2A agent-card and task/message operations. Internally, normalize every binding to the platform’s task state, identity, artifact, error, and audit contracts.

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| RemoteAgent | peer/agent ID, issuer, card URI/digest/version, endpoints/bindings, skills, auth schemes, owner, region, trust/risk status, last verification |
| PeerTrustPolicy | peer, allowed tenants/purposes/data classes/skills, max risk, required assurance, artifact rules, rate limits, expiry |
| FederatedTask | local task ID, remote task/context IDs, parent run, peer/agent/version, capability envelope reference, state mapping, idempotency key, deadline, budget, last heartbeat |
| FederatedMessage | task, direction, message/event IDs, role/type, parts/artifact refs, payload hash, sequence/logical time, verification status |
| RemoteArtifact | remote and local artifact IDs, URI/reference, media/schema, content hash, producer signature/attestation, classification, scan/validation state |
| CallbackSubscription | peer/task, endpoint handle, event types, auth key/version, expiry, delivery cursor, failure policy |
| PeerObservation | latency, availability, schema violations, security findings, cancellation compliance, quality score; evidence for routing, not silent trust escalation |

### State mapping and ownership

Local states are the task lifecycle of Chapter 18; the gateway maps each remote state of the pinned A2A 1.0.1 specification onto one of them.

| **Local state** | **A2A task state** | **Parent behavior** |
| --- | --- | --- |
| Created/Dispatched | TASK\_STATE\_SUBMITTED | Retry dispatch only with same idempotency key |
| Accepted/Running | TASK\_STATE\_WORKING | Monitor heartbeat and deadline |
| NeedsInput | TASK\_STATE\_INPUT\_REQUIRED | Route a typed question to parent/user; budget clock follows policy |
| NeedsInput | TASK\_STATE\_AUTH\_REQUIRED | Route to the credential or approval path, not the user prompt |
| CompletedPendingValidation | TASK\_STATE\_COMPLETED | Quarantine artifacts until schema, provenance, malware, policy, and acceptance checks pass |
| Succeeded | No remote state; local adoption committed through `:adoptResult` | Parent may satisfy dependency |
| CancelRequested | CancelTask sent; no terminal state yet | Stop issuing new authority; continue monitoring possible effects |
| Canceled | TASK\_STATE\_CANCELED | Close only after any possible effect reconciles |
| Failed | TASK\_STATE\_FAILED or TASK\_STATE\_REJECTED | Apply parent join policy |
| Expired | Deadline passed | Apply parent join policy; never resubmit automatically |
| InterventionRequired | Remote outcome ambiguous | Open an intervention task and hold dependent work until its response; never resubmit automatically |

### Scalability, federation, and failure isolation

* Partition task-relay state by tenant + peer domain + task ID. Serialize updates for one federated task while scaling across tasks and peers.
* Prefer asynchronous callbacks or streaming for progress; poll only as a bounded fallback with exponential backoff. Persist callbacks before acknowledgment.
* Enforce per-peer and per-skill rate, concurrency, byte-egress, and cost budgets. Circuit-break a misbehaving peer without disabling unrelated local agents.
* Exchange large or sensitive data by short-lived, audience-bound artifact references. Validate recipient, region, classification, and purpose before issuing each reference.
* Carry W3C trace context when supported and create span links when the remote system returns a different trace. Never rely on a remote trace as the enterprise audit record.
* Keep peer card/configuration reads cached by signed digest, but re-evaluate authorization and trust policy per task/message. Card changes cannot alter an in-flight task’s pinned contract.
* Bound remote fan-out at the parent. A peer may not recursively delegate unless the task grant explicitly permits a depth and the resulting chain remains visible.
* Treat missed heartbeat, callback failure, cancellation ambiguity, and artifact validation failure as distinct states; do not automatically resubmit a potentially active remote task.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| MCP correction | Use MCP 2026-07-28 for new designs: the core is stateless, initialize and Mcp-Session-Id are removed, requests carry protocol/capability metadata, and server/discover supports version selection. Application state uses explicit handles. Tasks and Skills over MCP are optional extensions, not core guarantees. | R05 |
| MCP authorization | Use protected-resource and authorization-server discovery, PKCE, audience/resource binding, short-lived tokens, step-up scopes, issuer validation, and SSRF-safe metadata retrieval. Token passthrough to an upstream API is forbidden. | R06; R09; R10 |
| A2A correction | Pin A2A 1.0.1. Normative operations include SendMessage, GetTask, ListTasks, CancelTask, and SubscribeToTask; local /v1 bridges are platform APIs, not A2A endpoints. Cancellation is best effort and authorization must prevent task-existence leakage. | R07 |

The discussion above draws on R05; R06; R07; R09; R10. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

Start where remote work re-enters the platform.

### Remote artifact adoption check

`:adoptResult` runs this check after schema and scan validation and before the parent workflow may depend on the artifact.

[[EXAMPLE:artifact-adoption]]

## If this fails in production

1. Verify the registry version, endpoint identity, protocol profile, and trust material.
2. Inspect local authorization and quota decisions for one remote call.
3. Validate the returned artifact hash, schema, classification, provenance, and scan result.

## What to verify before production

**✓** MCP and A2A endpoints terminate at authenticated governed gateways.

**✓** Registry entries pin endpoints, owners, trust, schemas, and versions.

**✓** Per-call or per-task authority, quotas, classification, and egress are checked locally.

**✓** Remote artifacts are scanned and adopted under local policy.

**✓** Cancellation, retries, idempotency, effects, and audit have local semantics.

## Put the idea to work

1. Wrap an MCP tool with local MCP Gateway policy.
2. Map a local TaskEnvelope to a FederatedTask, including state mapping, cancellation, and artifact adoption.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| What does MCP standardize? | How hosts discover and invoke server tools, resources, and prompts; it does not establish business authorization or endpoint trust. |
| What does A2A add? | Stateful task, message, status, artifact, streaming, and best-effort cancellation semantics across agent boundaries. |
| Why put protocol gateways at the boundary? | To verify peers, schemas, authority, quotas, classifications, artifacts, egress, effects, and audit using local policy. |
| How should a remote artifact be adopted? | Authenticate the source, validate schema and hash, scan content, enforce classification and provenance, then copy or reference under local policy. |
| How do you version external capabilities? | Pin registry entry, endpoint, protocol profile, schemas, trust material, tool or agent version, and tested compatibility in the release manifest. |

## Where this leads next

Gateways control what crosses a protocol boundary, but not the entire attack surface; Chapter 20 introduces defense in depth across all agentic trust boundaries.
