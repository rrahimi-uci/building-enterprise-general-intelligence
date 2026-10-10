# PART II — ARCHITECTURE, KNOWLEDGE, AND CONTEXT

The first Part established that the model is not the system of record. This Part
draws the system around it: who owns each fact, where policy is enforced, how
knowledge stays current, and how one run receives only the context it is
allowed to see. By the end, “the agent knows” has become a set of inspectable
contracts rather than a vague claim about a prompt.

# 04 — Design the Architecture Around the Model

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Harborlight's evidence review now spans an edge API, a durable run, a bounded agent step, model routing, document tools, policy knowledge, approvals, and operations. Before any of it ships, the platform must give each record—the run, its context, the document request, the approval—one owner, one store, and one failure domain. |

|  |
| --- |
| **THE DESIGN CHOICE** Give every authoritative record one owning plane and one writer; deploy global definitions and governance into regional execution cells connected by provider-neutral contracts. |

## Why the model cannot own the architecture

Chapter 3 drew one seam: AgentRuntime runs a bounded step from an
AgentStepRequest and returns an AgentStepResult. This chapter places that seam,
and every service around it, so that each record has one writer. The agent is a
decision component—not the workflow, authorization service, database, policy
engine, or proof of completion. Principles become useful when they tell a team
where a fact lives, who may change it, and what happens when a dependency fails;
this chapter turns the book's boundary rules into planes, services, contracts,
stores, and regional cells. Return to it when a design review has too many boxes
with overlapping authority—or when nobody can say which service owns the truth.

## Seven planes, one owner per record

The planes and layers are two views of the same system. Planes tell you who owns a class of decisions—runtime and workflow, knowledge and context, security and governance. Layers show what is deployed and the path a request follows. The LLM Gateway may sit on every model call, but it should not own business workflow simply because every call passes through it. Without a clear line, central components accumulate authority they were never designed to hold.

[[DIAGRAM:reference-architecture|Figure 4-1 — The reference architecture: seven ownership planes, the components in each, and the two planes that cross them all]]

Read the figure downward: each band is one ownership plane and lists its main components, and the solid path traces one request from intent to committed effect, narrowing in authority at every step. *Security and governance* and *Evaluation and operations* are drawn as vertical spines rather than bands because neither sits between two planes — the policy decision point is consulted at admission, at run control, and again at the gateways, and the collector gathers from every plane. Dashed edges are control, dotted edges are evidence, and the bottom band sits outside the trust boundary: nothing there is assumed, and everything returned from it is revalidated.

Figure 1-3 drew the same system as orientation bands. Figure 4-1 refines them into ownership planes:

| Figure 1-3 band | Chapter 4 plane |
| --- | --- |
| Channels | Experience and channels |
| Agent runtime | Agent applications; Runtime and workflow |
| Collaboration | Runtime and workflow (child tasks); Gateways and integration (A2A) |
| Knowledge | Knowledge, context, and memory |
| Control points | Gateways and integration; admission sits in Experience and channels, approval in Security and governance |
| Security | Security and governance |
| Systems of record | Outside the planes |
| Evidence | Evaluation and operations |
| Platform and operations | Part III; not drawn here |

| **Plane** | **Responsibilities** | **Authoritative records** | **Boundary** |
| --- | --- | --- | --- |
| Experience and channels | Intent, interaction, review, accessibility, recourse | Request and interaction record | UI state is not approval or workflow truth |
| Agent applications | Domain instructions, topology, response assembly | AgentSpec, Skill manifest, application release | Cannot mint authority or directly commit protected effects |
| Runtime and workflow | Run graph, deadlines, budgets, retries, cancellation, checkpoints, joins | RunManifest, run state, TaskEnvelope | Transcript is evidence, not execution state |
| Knowledge, context, and memory | Governed knowledge, authorized evidence, provenance, snapshots, governed persistence | ContextManifest, MemoryRecord | Retrieved text remains untrusted data |
| Gateways and integration | LLM routing, tool façades, effects, MCP/A2A, APIs, events | RoutingDecision, ToolManifest, EffectRecord, protocol envelope | Revalidate identity, policy, schema, and tenancy |
| Security and governance | Identity, least privilege, RBAC/ABAC, guardrails, approval, DLP, audit | PolicyDecision, CapabilityEnvelope, ApprovalRequest/Decision | Protected actions fail closed; ambiguous effects become unknown |
| Evaluation and operations | Tracing, evaluation, SLOs, incidents, release, capacity, learning | Trace graph, EvaluationResult, ChangeBundle, ReleaseManifest | Monitoring cannot self-promote behavior change |

The Runtime and workflow plane builds the AgentStepRequest; the Agent applications plane executes it through AgentRuntime and its framework adapter; the typed AgentStepResult returns to the workflow, which alone decides the next transition.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Each platform service owns one authoritative record | global control tier to regional execution cell | tenant · queue · partition · cell | one service/cell | Run · Task · Tool · Artifact · Release APIs |

## Where truth lives

| **Concern** | **Owner** | **Model may** | **Model may not** |
| --- | --- | --- | --- |
| Workflow | Run Service | Propose a semantic result | Invent state, retry history, or terminal outcome |
| Authorization | Identity and policy services | Explain requested scope | Grant or expand authority |
| Business truth | Domain system | Read an authorized projection | Replace truth with a summary |
| Effects | Effect Service (Chapter 22) and downstream receipt | Propose arguments | Assert a mutation completed |
| Approval | Approval Service (Chapter 14) | Generate rationale and preview | Reuse Boolean or stale conversational consent |
| Knowledge | Governed source/snapshot catalog | Synthesize evidence | Treat similarity as truth or freshness |
| Learning | Evaluation, dataset, release services | Recommend a candidate | Self-certify or self-deploy |

## The decisions that shape the system

Centralize identity, policy, gateways, tool/effect contracts, telemetry schemas, evaluation infrastructure, release evidence, and incident controls. Federate domain prompts, accepted outcomes, tools, Skills, knowledge, datasets, and SLOs to accountable owners. Standardize interfaces and evidence—not every framework implementation.

## From planes to deployable layers

This chapter presents two decompositions, and they are easy to mistake for a
contradiction. They are not: they answer different questions.

The **plane** table is the conceptual model. It answers *who owns which
decision*, and it is what you reason with when deciding where a responsibility
belongs. Seven planes is the smallest set that keeps every authoritative record
in exactly one place.

The **layer** table below is the deployable decomposition. It answers *what you
build, run, and page someone about*. Planes split into layers wherever two parts
of one responsibility have different scaling, failure, or trust properties.

| Plane | Splits into layers | Why it splits |
| --- | --- | --- |
| Experience and channels | Experience · Edge and admission | Admission is a security surface with its own scaling and failure profile |
| Agent applications | Agent registry and release | Defining and releasing capability is separate from running it |
| Runtime and workflow | Run control · Durable execution | Deciding a transition and durably surviving it are different problems |
| Gateways and integration | Model access · Tool and protocol access · Sandboxed execution | Inference, effects, and sandboxed code have unrelated blast radii |
| Knowledge, context, and memory | Knowledge and context services | — |
| Security and governance | Trust and governance | — |
| Evaluation and operations | Operations and improvement | — |

Use planes when you are arguing about ownership and boundaries. Use layers when
you are drawing a deployment diagram or assigning an on-call rota. If the two
ever disagree about who owns a record, the plane model wins — the layer exists
to serve it.

### Architecture layers

| **Layer** | **Major components** | **Primary responsibility** |
| --- | --- | --- |
| Experience | Chat/UI, API clients, event subscriptions, operator console | Intent capture, progress, approvals, cancel/override |
| Edge and admission | API Gateway, WAF, tenant router, request validator | Authentication, quotas, schema validation, risk classification |
| Agent registry and release | Agent registry, policy bundles, prompt bundle registry and Skill Registry (Chapter 8), release manager | Define, version, approve, discover, and deploy capabilities |
| Run control | Run API, planner, coordinator, budget manager | Own the run lifecycle and deterministic transition decisions |
| Durable execution | Workflow engine, timers, signal handlers, checkpoint/event store | Crash recovery, pause/resume, retries, compensation, replay |
| Model access | LLM Gateway, router, prompt assembler, structured-output validator | Provider abstraction, routing, caching, quotas, redaction |
| Tool and protocol access | Tool Gateway, Effect Service, MCP Gateway, A2A Gateway, connectors | Discovery, authorization, invocation, effects, isolation, versioning |
| Knowledge and context services | Context Service, Enterprise Knowledge Hub (Chapter 5), search/vector index, catalog/lineage, memory service | Authorized retrieval, provenance, ACLs, governed memory; shared stores: see § Where each kind of state belongs |
| Sandboxed execution | Sandboxed workers, code/browser runners, egress proxy | Resource isolation and constrained side effects |
| Trust and governance | IdP, STS, workload identity, PDP/PEP, Approval Service, secrets, audit/WORM | Least privilege, tenant isolation, policy, approval, evidence and retention |
| Operations and improvement | OTel collector, trace store, metrics, eval service, incident tooling | Debug, replay, evaluate, optimize, alert, and promote |

### What the LLM Gateway enforces

The LLM Gateway is the Model access layer of the Gateways and integration plane: the controlled boundary between enterprise workloads and model providers or self-hosted inference. It normalizes model access and enforces model-specific routing, policy, privacy, economics, observability, and release governance. It does not own business workflow, tool effects, agent delegation, or the external API perimeter.

| **Capability** | **Behavior** | **Control** |
| --- | --- | --- |
| Provider abstraction | Normalize requests, streaming, errors, usage, capabilities | Preserve provider/model/version and raw evidence references |
| Model routing | Select by task, risk, region, quality, latency, cost, health | Deterministic eligibility before optimization; record reason |
| Authentication and authorization | Authenticate workload and subject context | Audience, tenant, purpose, approved models |
| Policy enforcement | Enforce use, data, region, model, output, risk rules | External policy decision; never prompt-only policy |
| PII/secrets protection | Classify, minimize, redact/tokenize, block | Authorized reversible boundary; never log secrets |
| Rate limits and budgets | Tenant/workload/user quotas, tokens, spend, concurrency, deadline | Hierarchical budgets before provider charge |
| Caching | Reuse only policy-safe, semantically equivalent results | Key every security and semantic dependency (Chapter 21) |
| Retries and fallbacks | Classify transient failures; use approved alternatives | One retry owner and shared deadline/budget |
| Content filtering | Input/output safety, injection, DLP, schema, evidence checks | Filters are evidence; policy still authorizes actions |
| Model/version governance | Allowlist, aliases, deprecation, eval, canary, rollback | Alias change is a versioned routing release |
| Logging, tracing, evaluation hooks | Normalized spans, route, usage, policy, cache, scorers | Redaction, evaluator version, scope, uncertainty, override lineage |

It applies deterministic eligibility before any optimization; Chapter 28 treats routing as a cost decision. Centralization adds latency and blast-radius risk: deploy it regionally, isolate tenants and high-risk workloads, use bulkheads, and retain platform-owned contracts even when buying a gateway.

## Trust boundaries

| **Boundary** | **Treat as untrusted** | **Mandatory controls** | **Developed in** |
| --- | --- | --- | --- |
| User/tenant → platform | Prompts, attachments, callback URLs | AuthN, tenant binding, malware/content scan, request schema, quotas | Chapter 21 |
| Knowledge → model | Documents, email, web text, OCR, metadata | Provenance, ACL filters before retrieval, instruction/data labeling, DLP | Chapter 6 |
| Model → orchestrator | Plans, arguments, classifications, generated code | Strict schema, allowlists, invariant checks, confidence/risk routing | Chapter 2 |
| Orchestrator → tool | Requested action and delegated context | PDP decision, downscoped token, idempotency, dry-run/approval, audit | Chapters 21–22 |
| Agent → agent | Claims, artifacts, status, requested authority | Authenticated channel, signed task envelope, scope intersection, limits | Chapters 18–19 |
| Sandbox → network | Code, browser activity, generated payloads | Default-deny egress, DNS/HTTP proxy, quotas, filesystem isolation | Chapter 23 |
| Platform → model vendor | Prompts, retrieved content, telemetry | Redaction, residency policy, retention controls, vendor allowlist | § What the LLM Gateway enforces |
| Result → destination | Reports, emails, records, deployments | Output classification, provenance, approval, destination authorization | Chapters 14 and 22 |

## Global control and regional cells

The platform separates a global control tier from regional execution cells. The global tier publishes signed, immutable definitions—AgentSpecs, policy bundles, ReleaseManifests—and holds no run state. Each run has a home cell holding its run control, durable workflow, bounded agent workers (AgentRuntime and its adapters, Chapter 3), LLM Gateway, Tool Gateway, context services, effect ledger, artifact store, and regional telemetry and audit pipelines. Cells bound residency and blast radius: definitions fan out, while active tenant runs stay regional. A cell that cannot reach the global tier continues pinned in-flight work but fails closed on high-risk admission when it cannot verify freshness; Chapter 27 covers the operations.

Scale stateless APIs horizontally, partition state by tenant and run, shard workflow history and trace indexes, and isolate workload classes through queues and concurrency pools.

## End-to-end responsibility flow

With planes, layers, and boundaries in place, one request can be followed through them. Each step has one owning plane and leaves one record.

[[DIAGRAM:request-sequence|Figure 4-2 — Request-to-verified-outcome sequence]]

| **Step** | **Owning plane** | **Record produced** | **Developed in** |
| --- | --- | --- | --- |
| 1. Authenticate the initiating subject and workload; establish tenant, purpose, risk, deadline, and trace | Experience and channels | Request record | Chapter 21 |
| 2. Admit a run and resolve the versions it may use | Runtime and workflow | RunManifest | Chapter 4 |
| 3. Resolve eligible tools and models and build an authorized ContextManifest into the AgentStepRequest | Knowledge, context, and memory | ContextManifest, AgentStepRequest | Chapters 3 and 6 |
| 4. The model proposes a typed decision inside that bound | Agent applications | AgentStepResult | Chapter 3 |
| 5. Policy authorizes the exact proposed action; protected changes bind to an expiring human approval | Security and governance | PolicyDecision, ApprovalDecision | Chapters 14 and 21 |
| 6. Commit through the Tool Gateway façade with short-lived credentials, idempotency, and reconciliation | Gateways and integration | EffectRecord | Chapter 22 |
| 7. Evaluate the result against executable acceptance criteria and record the run's terminal state | Runtime and workflow | AcceptanceDecision, run state | Chapters 13 and 15 |
| 8. Join traces, evaluations, human feedback, cost, latency, incidents, and outcomes for controlled improvement | Evaluation and operations | Trace graph, EvaluationResult | Chapters 24–25 |

## The contracts that hold the platform together

A reference architecture becomes implementable when every arrow has an API or event contract and every record has one authoritative writer. Each record below has one owner, version, retention policy, and consistency boundary.

| **Record** | **Owning plane** | **Defined in** |
| --- | --- | --- |
| RunManifest | Runtime and workflow | Chapter 4 |
| WorkflowExecution | Runtime and workflow | Chapter 15 |
| TaskEnvelope | Runtime and workflow | Chapter 18 |
| AgentStepRequest/AgentStepResult | Runtime and workflow → Agent applications | Chapter 3 |
| ContextManifest, MemoryRecord | Knowledge, context, and memory | Chapter 6 |
| Skill manifest | Agent applications | Chapter 8 |
| CapabilityEnvelope, CredentialLease | Security and governance | Chapter 21 |
| PolicyDecision | Security and governance | Chapter 21 |
| ToolManifest, EffectRecord | Gateways and integration (Effect Service) | Chapter 22 |
| ApprovalRequest/ApprovalDecision | Security and governance | Chapter 14 |
| Artifact | Runtime and workflow (the producing run owns the version; the artifact store holds the bytes) | Chapter 4 |
| EvaluationResult | Evaluation and operations | Chapter 25 |
| ReleaseManifest, ChangeBundle | Evaluation and operations | Chapter 27 |

### Run API

The public Run API is asynchronous and idempotent. Commands carry expected state version and deadline; accepted work returns 202 plus a run resource. Status and events are durable and paginated. Large inputs and outputs use immutable artifact references rather than oversized JSON. Public contracts do not expose SDK messages or provider-specific run objects.

| **Operation** | **Semantics** |
| --- | --- |
| POST /v1/runs | Create idempotently from agent/workflow reference, goal, inputs, subject delegation, autonomy request, budgets, and callback preferences; returns 202, run ID, home region, pinned RunManifest, and status URL |
| GET /v1/runs/{id} | Return authorized status, current stage, owner, progress, budgets, waits, and result/artifact references |
| GET /v1/runs/{id}/events | Cursor-based event history or server-sent stream; redaction and history limits by role |
| POST /v1/runs/{id}:signal | Send typed, authenticated input such as clarification, approval, callback, or document-ready event |
| POST /v1/runs/{id}:cancel | Request hierarchical cancellation with reason and compensation policy |
| POST /v1/runs/{id}:update | Optimistic, authorized patch to budget, priority, assignee, or plan; may require approval |
| POST /v1/runs/{id}:fork | Create a sandbox replay/fork from checkpoint with pinned or explicitly changed versions; never reapply live effects |

Chapter 15 adds the durable-execution operations (events:ingest, :pause, :resume, :migrate) and the durable semantics of :signal and :cancel; Chapter 24 explains diagnostic replay and fork.

### RunManifest

The RunManifest is written once, at admission (step 2). It references the promoted ReleaseManifest it was resolved from (Chapter 27), which already pins the agent build, prompt bundle, policy bundle, and tool contracts, and records only what is resolved for this run: the Skill and pack digests, the knowledge snapshots, the model route chosen within the release's eligible set, the runtime adapter, the capability envelope, the budget, and the use-case tier (Chapter 26). Every AgentStepRequest (Chapter 3) and every ContextManifest (Chapter 6) references it. It never changes; a run that needs different versions is a new run or an explicit migration (Chapter 15). Its model is in § A sensible place to start.

### Artifact contract

Every artifact has artifact\_id, immutable version, schema/media type, content hash, creator run/node/agent, source references and hashes, tenant, owner, classification, residency, ACL/purpose policy, confidence/quality metadata, retention/deletion linkage, and optional signature. Large artifacts move by reference; callers receive short-lived authorized URLs rather than embedded payloads.

### Effect receipt

A mutating tool returns a receipt from the system of record (proof of what happened); the platform's EffectRecord, not the receipt or the model, holds the effect's state. A timeout without a receipt is Unknown, not failed; Chapter 22 defines the receipt fields and the effect state machine.

### Event contract

> **Evidence context:** CloudEvents defines the portable event envelope used here, while the transactional-outbox source supports atomic state/event publication and warns that consumers still require duplicate handling. **[R03][R04]**

Events record facts that already happened (`run.status.changed`); commands go through the Run API and carry an expected state version. Every event uses one CloudEvents 1.0 envelope with `tenant_id`, `correlation_id`, `causation_id`, and `traceparent` alongside the standard attributes. Large or sensitive payloads travel by `dataref` and `datahash`, never embedded. Producers publish through a transactional outbox and consumers deduplicate on (source, id); Chapter 22 defines both records.

## Where each kind of state belongs

| **Store** | **Recommended contents** | **Consistency and controls** |
| --- | --- | --- |
| Workflow history store | Events, timers, activity results, signal cursor | Engine-managed durability; replay semantics; encrypted per environment/tenant |
| Relational operational DB | Run projections, manifests, budgets, ownership, approvals, effect ledger, dedup keys | Strong transactions, optimistic versions, row-level security |
| Object store | Prompts by digest, large tool outputs, artifacts, evidence bundles, replay fixtures | Immutable/versioned objects, hashes, retention lock, tenant keys |
| Search/vector index | ACL-aware chunks and embeddings derived from source systems | Source revision/provenance, pre-retrieval authorization, rebuild/delete pipeline |
| Conversation and memory stores | Conversation turns (append-only); approved cross-run MemoryRecords | Tenant+subject partitioning, write policy, TTL, deletion tombstones (Chapter 6) |
| Event log/broker | CloudEvents, status changes, business triggers | At-least-once, partitions, schema registry, outbox/inbox, DLQ/quarantine |
| Trace/metric store | OTel spans, metrics, logs with content references | Tiered retention, sampling, redaction, restricted content access |
| Audit/WORM archive | Policy decisions, approvals, effects, release evidence | Append-only, signed/hashed, legal hold and regulatory retention |
| Secret broker / KMS | Connector secrets, token-exchange keys, encryption keys | No secrets in prompts/state; short-lived delivery; rotation and hardware-backed keys |
| Cache | Model, retrieval, tool-read, schema and policy-safe results | Scope-aware keys, TTL/freshness, encryption, no cross-tenant leakage |

A vector database is an index, not the source of truth; an agent transcript is not workflow state; a trace store is not the audit ledger; and a queue is not a business transaction. Keeping these responsibilities separate prevents attractive shortcuts from becoming systemic risks.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Event contract | Use a CloudEvents 1.0-compatible envelope for interoperability, but keep domain semantics and delivery guarantees in versioned event contracts. Source plus ID supports deduplication; large or sensitive artifacts should be referenced rather than embedded. | R04 |

The discussion above draws on R03; R04. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

Start with the three contracts every run touches: the manifest it is admitted under, the artifacts it produces, and the events it emits.

### Run, artifact, and event contracts

[[EXAMPLE:contracts#platform]]

## If this fails in production

1. Trace one API command through stores, queues, services, and contracts.
2. Find any record with two authoritative writers.
3. Map a cell failure to its intended containment boundary.

## What to verify before production

**✓** Every record and transition has one authoritative owner.

**✓** Public contracts remain independent of model providers and SDK types.

**✓** Every trust boundary states authentication, authorization, validation, and data handling.

**✓** Regional execution can continue safely on pinned releases while the global control tier is unreachable (Chapter 27).

**✓** Cells, queues, and local dependencies bound failure domains.

## Put the idea to work

1. For one workflow you own, assign each record in the authoritative-records table to one plane and one writer; mark any record with two writers.
2. Select a store and consistency model for each authoritative record.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Which plane owns the run's terminal outcome, and why can the LLM Gateway not own it even though every call passes through it? | Runtime and workflow. Position on the request path is not authority; the gateway sees model calls, not the run's state, acceptance criteria, or effects. |
| Why separate the global control tier from regional execution cells? | They have different scaling, availability, data-residency, and failure characteristics; immutable definitions can fan out while active tenant runs stay regional. Cells add scale additively and give tenant placement, residency, bounded blast radius, independent canaries, and predictable stateful-service limits. |
| Which trust boundary does indirect prompt injection cross, and which control there does not depend on detection? | Knowledge → model. ACL filtering before retrieval and instruction/data labeling (Chapter 6) hold even when no detector recognizes the attack. |

## Where this leads next

The reference architecture names a knowledge, context, and memory plane but not what fills it; Chapter 5 fills its knowledge half—the governed artifacts agents retrieve, reason over, are constrained by, and act through—and Chapter 6 its per-run context and memory.

# 05 — Give Knowledge an Owner

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Harborlight's evidence agent can retrieve the underwriting policy and quote it accurately. It still recommends proceeding with an application whose property or income profile the policy excludes, because retrieving a sentence is not the same as being bound by it. The platform team stops adding documents to the index and starts treating policy as governed knowledge. |

|  |
| --- |
| **THE DESIGN CHOICE** Treat institutional knowledge as governed artifacts with owners, versions, scope, and provenance — not as a corpus. Retrieval becomes one consumer of those artifacts rather than the knowledge itself. |

## Why retrieval alone is not a knowledge strategy

Chapter 4 gave knowledge, context, and memory one plane; this chapter fills its
knowledge half. Teams often say “put the knowledge in a vector store” when they
really mean four different jobs: supply context, support reasoning, enforce
constraints, and enable action. Those jobs have different owners and different
failure modes. This chapter separates them and uses the Harborlight case to
show why a single semantic index cannot be the evidence source, the inference
model, the policy engine, and the tool catalog at once.

## Why similarity cannot tell you what to trust

[[DIAGRAM:knowledge-fabric|Figure 5-1 — The enterprise knowledge fabric and its four consumption modes]]

| State owner | Trust boundary | Scale unit | Failure containment | Core contracts |
| --- | --- | --- | --- | --- |
| Knowledge Hub and its registries | authored source to governed artifact | artifact · domain · tenant | one artifact version | KnowledgeArtifact · Rule · Capability · ResolutionQuery |

Retrieval-augmented generation answers one question well: *what text is relevant to this?* Enterprises then ask it three questions it was never designed for; Figure 5-1 shows all four behind one governed resolution surface.

| Mode | The question | Representation | How it fails when wrong |
| --- | --- | --- | --- |
| Context | What is the situation? | Documents, embeddings, semantic search | Plausible grounding that is stale, superseded, or outside the reader's authority |
| Reasoning | What should happen? | Ontology, knowledge graph, decision models | Correct facts, invalid inference |
| Constraints | What may I do? | Policies and permissions as enforceable rules | The agent explains the rule, then violates it |
| Action | How do I do it? | Capability and API contracts | Right decision, wrong or unauthorized effect |

The fourth column is the argument. Each mode fails differently, so each needs different evidence and different tests. A system that cannot say which mode failed cannot be debugged, and a similarity score is not evidence of authority, currency, or permission.

The clearest case is the one Harborlight hit. An underwriting policy excludes a property or income condition. Retrieval returns the policy, the model quotes it, and the agent proceeds anyway, because nothing in the pipeline was responsible for *enforcing* the exclusion. The document was context. Nobody made it a constraint.

## How enterprise knowledge becomes usable

Each representation in the knowledge fabric is derived from—and traceable back to—the source above it. That lineage lets an engineer explain why a rule exists, detect when the source changed, and rebuild every derived artifact. A constraint that cannot point to the sentence or decision behind it is not an enforceable policy; it is an opinion encoded in software.

### Semantic knowledge

Documents, policies, procedures, standards, and prior decisions, reached through embeddings and hybrid search. Chapter 6 owns how retrieved evidence enters a model call—authorization order, ranking, token allocation, and the ContextManifest. What belongs here is what makes retrieval *governed*: source authority, effective dates, jurisdiction, supersession, and the difference between text that appears in a document and text that is authoritative.

A retrieved passage should never reach a model without the metadata that decides whether it still applies.

### Ontology and knowledge graph

Entities, relationships, dependencies, and the organization's own semantics. Traversal answers questions similarity cannot: *what depends on this system three hops away?* No wording links a payments API to a regulatory filing obligation, so no embedding will connect them. The graph does.

[[EXAMPLE:knowledge-graph]]

Traversal must be bounded. An unbounded walk over an enterprise graph is a denial of service against your own agent, and a cycle makes it non-terminating.

The honest caveat: ontologies are where enterprise knowledge programs go to die. The useful heuristic is to model only what an agent must traverse to make a decision it cannot make otherwise, and to let a modeling exercise justify itself one query at a time.

### Business rules as enforceable constraints

The core of the layer. A rule an agent reads is documentation; a rule the platform evaluates at the effect boundary is a control. The move from prose to knowledge is not parsing — it is committing to a shape.

[[EXAMPLE:policy-to-rule]]

Scope is required, not optional. A rule whose applicability is implicit will be applied where it does not belong, which is the most common way a correctly extracted rule still produces a wrong decision. Identity by content rather than by assigned identifier is what lets two independent extractions of one sentence recognize each other later.

Enforcement then happens where intent becomes action:

[[EXAMPLE:rule-as-guardrail]]

Note the refusal on missing input. A rule check that reads *unknown* as *permitted* is not a control. Three-valued evaluation — true, false, unknown — is what stops an absent field from silently authorizing an effect.

### Business data catalog

Entities, fields, definitions, ownership, lineage, sensitivity, and access constraints, described so an agent can discover and query data safely. A column name is not a definition, and a schema without a sensitivity class cannot tell an agent which fields it must not put in a prompt—the class Chapter 6's context pipeline uses to redact before a prompt is built.

### Capability and API catalog

What the agent may do, with the consequences attached. A tool list says what exists; a capability catalog says whether an action mutates, what must be true first, who may invoke it, and whether a retry is safe.

[[EXAMPLE:capability-catalog]]

Filtering during discovery matters more than it looks. A capability the caller may not invoke should never appear (Chapter 8 § Discovery is not permission; AP-12), because a listed-but-forbidden tool is an invitation to try. The catalog does not own these entries; it indexes the Skill manifests of Chapter 8 and the ToolManifests of Chapter 22 for discovery, and every invocation still resolves against those registries.

### Process and decision models

Four OMG standards already describe what most enterprises are otherwise inventing badly. The question to ask of each is not whether it is rigorous but what an agent can do with it that it could not do with prose.

| Standard | Represents | What an agent does with it |
| --- | --- | --- |
| BPMN [R44] | Processes and their control flow | Plans against the real sequence, including the steps it may not skip |
| DMN [R45] | Decisions as tables with a hit policy | Evaluates a decision deterministically instead of reasoning about it |
| CMMN [R46] | Case management, unordered work | Handles work with no fixed sequence without inventing one |
| SBVR [R47] | Business vocabulary and rules | Resolves what a term means in this domain before acting on it |

DMN earns its place fastest. A decision table with a declared hit policy is the one artifact that turns a class of judgment calls into a lookup, and a lookup can be tested. BPMN pays off where the sequence is genuinely fixed and the cost of skipping a step is high. CMMN and SBVR are narrower; adopt them when case work or vocabulary ambiguity is the actual problem, not because the set is incomplete without them.

## Turn policy prose into logic the system can enforce

Extraction is probabilistic. Verification must not be. The pipeline that works separates the two and refuses to let the first vouch for itself.

Consider a policy sentence that says a pay statement is acceptable only within a particular age window. The source document is authoritative, but the runtime cannot safely enforce prose. The platform extracts a candidate rule with its exact source span, proves that the span says what the rule says, has an eligible owner approve the interpretation, compiles the approved rule, and records the version used for each case. Skip a link in that chain and the system may enforce a rule nobody can explain or prove is current.

[[DIAGRAM:policy-to-guardrail|Figure 5-2 — Extract, prove, approve, and project: from policy text to an enforced constraint]]

**Extract** is the part a language model does well: find the rules, type their conditions and outcomes, record where each came from.

**Prove** is the part that decides whether to believe it. The critical move is that verification does not trust the citation a rule carries; it rebuilds the evidence from the raw corpus and compares.

[[EXAMPLE:grounding-verifier]]

A model that invents a rule will invent a plausible citation for it, so checking that a citation is well-formed proves nothing. Checking that the cited passage *says what the rule says* is a different operation, and it is the one that matters. In one run of a compliance extraction pipeline built on this design, independent verification rejected 44% of the dependency and conflict claims that the pipeline's own deterministic guard had already accepted [R48]. That figure is one measurement of one pipeline on one corpus; it is not a general rate. It is, however, the empirical case for making verification independent of extraction.

**Approve.** An eligible owner accepts the interpretation; the approval, the source digest, and the rule version are recorded together. Verification shows the rule matches the text; approval makes it the organization's rule.

**Project** turns what survived into the standards-compliant models above, and into the constraints the runtime enforces at the effect boundary.

|  |
| --- |
| **COMMON PITFALL**  Treating extraction confidence as grounding. A high-confidence rule with a fabricated citation is more dangerous than a low-confidence one, because it will pass review. Verify against the corpus, not against the model's own certainty. |

## Combine knowledge without flattening its differences

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

## Why provenance determines what you can trust

Every representation above is only as good as the metadata that says whether to believe it.

| Field | Why an agent needs it |
| --- | --- |
| Owner | Who answers when the artifact is wrong |
| Version and supersedes | Which of two conflicting statements is current |
| Effective from / until | Whether it applied on the date in question |
| Jurisdiction and scope | Whether it applies to this subject at all |
| Provenance | The passage, offsets, and document digest it derives from: content provenance, distinct from the build provenance of released artifacts in Chapter 27 |
| Confidence and status | Authoritative, inferred, or draft |
| Permissions and data class | Who may see it, and whether it may enter a prompt |
| Lifecycle | Review cadence and expiry |

The document digest deserves emphasis. Without it, a rule extracted from last year's policy still verifies against this year's text, and nothing in the system notices that the ground moved.

Freshness follows from the same rule: the source revision is authoritative, and every index entry is a disposable projection that carries its source revision, ACL pointer, ingestion time, and deletion state. Ingestion runs as separate extract, classify, ACL, chunk, embed, and index stages with independent cursors, so a failed embedding never blocks an ACL deletion.

|  |
| --- |
| **SECURITY AND GOVERNANCE**  Permissions belong to the knowledge artifact, enforced at the resolution boundary. Filtering retrieved passages after the model has seen them is not access control; it is redaction after disclosure. |

## Reference architecture: the Enterprise Knowledge Hub

Agents must not hold connection strings to six stores. They ask one service, which resolves, authorizes, and attributes.

| Hub view | Holds | Answers | Serves mode / built from |
| --- | --- | --- | --- |
| Governance | Ownership, versions, effective dates, permissions, lifecycle | May this agent see this, and is it current? | All modes / § Why provenance determines what you can trust |
| Semantic | Documents and embeddings | What text is relevant? | Context / § Semantic knowledge |
| Structural | Ontology, graph, data catalog | What is related to what, and what does this field mean? | Reasoning / § Ontology and knowledge graph, § Business data catalog |
| Normative | Rules, decision tables, vocabulary | What is required, permitted, or forbidden? | Constraints / § Business rules as enforceable constraints, DMN, SBVR |
| Procedural | Process and case models | In what order, and what may not be skipped? | Reasoning / BPMN, CMMN |
| Capability | Tools, APIs, effects, prerequisites | What can be done, and at what cost? | Action / § Capability and API catalog |

One query surface sits above all six. Permissions are enforced there, attribution is attached there, and an agent that asks for knowledge it may not have receives a refusal rather than a filtered answer.

The Hub is the knowledge half of the knowledge, context, and memory plane (Chapter 4). It has two kinds of caller: the Context Service, which resolves pre-step context (Chapter 6), and read-only tools invoked through the Tool Gateway during a step (Chapter 3). Both reach the same permissions and attribution; neither holds store connections.

|  |
| --- |
| **PRODUCTION CONSIDERATION**  Version the knowledge layer alongside the agent. An agent release pinned to a policy version (the RunManifest's `knowledge_snapshots`, Chapter 4) is reproducible; one that resolves against "current" changes behavior when a document changes, with no deployment and no trace. |

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Standards scope | BPMN, DMN, CMMN, and SBVR are OMG specifications; each citation supports the existence and semantics of its own standard and nothing about its suitability for agentic systems. That assessment is book-authored. | R44; R45; R46; R47 |
| Verification measurement | The 44% rejection figure is one run of one compliance pipeline on one corpus, reported in the book author's own implementation repository. It is evidence that independent verification finds real errors, not a general error rate for extraction. | R48 |

The discussion above draws on R44; R45; R46; R47; R48. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The examples above are the reference implementation, and each is executed in continuous integration. Composed, they show the shape of the Hub: a rule extracted with provenance, verified against its corpus, placed in a graph, reconciled against a second source, and finally enforced at the effect boundary.

## If this fails in production

| Symptom | Likely cause | First check |
| --- | --- | --- |
| Agent quotes the right policy and violates it | The rule is context, never a constraint | Is any rule evaluated at the effect boundary? |
| Correct answer in staging, wrong in production | Scope or effective date not enforced | Does the rule declare jurisdiction and effective_from, and are they checked? |
| Two runs disagree on identical input | Resolution against "current" rather than a pinned version | Is the knowledge version recorded in the RunManifest (Chapter 4)? |
| A conflict surfaces only after an incident | Contradictions resolved silently at merge | Does the union preserve per-source attribution? |
| An agent selects a mutating tool for a read | Capability discovery filters on names, not effects | Does the catalog carry each capability's effect semantics and risk class (Chapter 22), and is discovery filtered on them? |
| Provenance points at text that does not support the rule | Citation trusted rather than verified | Is verification rebuilding evidence from the corpus? |

If the vector index is being treated as the source of truth, the repair is structural; see AP-09 in Chapter 17.

## What to verify before production

**✓** Every knowledge artifact has an owner, a version, an effective range, and a provenance reference that resolves.

**✓** Retrieval results carry authority and currency metadata, not just a similarity score.

**✓** At least one rule is enforced at the effect boundary, with a test proving the effect does not run when it refuses.

**✓** Missing inputs refuse rather than default to permitted.

**✓** Union preserves per-source attribution; contradictions are escalated, never auto-resolved.

**✓** Capability discovery filters on granted actions, prerequisites, and data class before returning results.

**✓** The knowledge version used by a run is recorded in its RunManifest (Chapter 4).

**✓** Permissions are enforced at the resolution boundary, not after the model has seen the passage.

## Put the idea to work

1. Take one policy sentence from your own organization and express it as a typed rule with scope and provenance. Note every field you cannot fill from the sentence alone.
2. Find a question your retrieval system answers plausibly and wrongly. Identify which of the four consumption modes it actually needed.
3. Compute the intersection of two overlapping policy sets in your domain. Inspect the differences before the union.
4. Take a rule your agents are expected to follow and make it refuse an effect in a test.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Which consumption mode failed in your last incident? | The four modes are separable in your architecture |
| How does an agent know a retrieved passage is still authoritative? | Governance metadata reaches the point of use |
| What happens when two authoritative sources disagree? | Contradiction is a first-class result |
| Where is a policy enforced, as opposed to described? | Constraints exist outside the prompt |
| What does the system do when a required input is missing? | Unknown is not silently treated as permitted |
| Can you reproduce a decision made six months ago? | Knowledge is versioned and pinned per run |

## Where this leads next

The knowledge layer defines what the organization knows and what agents may do with it. Chapter 6 turns to the run itself: how context is assembled, how memory and workflow state differ, and how a single request gets exactly the knowledge it needs and nothing more.

# 06 — Build Context Without Losing the Plot

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** As Harborlight's evidence runs grow, prompts mix conversation, workflow state, retrieved policy, summaries, and remembered preferences. The platform keeps these sources separate and records exactly which authorized projection reached each model call. |

|  |
| --- |
| **THE DESIGN CHOICE** Treat prompts as disposable authorized projections; keep canonical state, knowledge, artifacts, and memory in distinct stores. |

## Why context needs an architecture of its own

The prompt is the model's working view, not the system's memory. It may contain
conversation, workflow state, retrieved evidence, summaries, and preferences,
all with different authority and retention rules. This chapter shows how to
assemble that view deliberately, how to keep memory from becoming an
unreviewed shadow database, and why these distinctions matter when context is
large, sensitive, stale, or later challenged in an audit. Chapter 3's
AgentStepRequest carries an authorized ContextManifest; this chapter defines how
it is built and recorded. Knowledge arrives through the Enterprise Knowledge Hub
of Chapter 5.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Context Service; workflow remains canonical | authorized sources to model prompt | tenant · source · context budget | one context projection | ContextManifest · MemoryRecord · EvidenceRef |

## Five sources, one disposable projection

These sources often appear together in a prompt, which makes it tempting to store them together. They have different jobs. Workflow state says what must happen next and must survive a restart; it is canonical in the durable run (Chapter 15). Conversation is the interaction history. Enterprise knowledge supplies governed facts and rules (Chapter 5). Working memory holds run-scoped hypotheses, and long-term memory holds approved reusable facts under their own retention policy. Context is only the temporary projection of these five for one step. Mixing them makes deletion, authorization, freshness, and recovery ambiguous—and turns prompt history into an accidental source of truth.

| **Source** | **Scope and examples** | **System of record** | **Rules** |
| --- | --- | --- | --- |
| Workflow state | Current node, variables, child tasks, budgets, approvals | Durable run history (Chapter 15); context reads the RunStateProjection | Strong transition rules; versioned; queryable; replay-safe |
| Conversation | Recent messages, channel state, current clarification | Conversation service / document DB | Append-only turns; compact with source links; not authoritative business state |
| Enterprise knowledge | Policies, contracts, code, tickets, records, catalogs | Source systems + governed search/vector/graph indexes, through the Hub (Chapter 5) | Source remains authoritative; ACL filter before retrieval; freshness and lineage |
| Working memory | Scratch notes, candidate plan, intermediate hypotheses | Run-scoped state or object artifacts | TTL; no automatic cross-run reuse; label confidence and provenance |
| Long-term memory | Approved preferences, reusable facts, learned procedures | Governed memory service / relational + search index | Explicit write policy, consent, provenance, TTL, ACL, correction/deletion |

Artifacts, telemetry, audit, secrets, and caches live in the stores of Chapter 4 § Where each kind of state belongs. Artifacts produced by other agents or trust boundaries enter context only after adoption (Chapter 18; Chapter 19 shows the cross-boundary adoption check).

## How context is assembled

Everything the model sees on a given step is produced by a pipeline, and the
order of its stages is a security property rather than an implementation
detail. The pipeline admits five kinds of source—pinned instructions and policy
constraints, the run's state projection, a minimal conversation window,
enterprise knowledge, and memory—and each passes every stage.

[[DIAGRAM:context-pipeline|Figure 6-1 — The context build pipeline: authorization precedes retrieval, and bytes materialize last]]

| Stage | What it does | What it prevents |
| --- | --- | --- |
| 1 · Parse request | Extract intent, entities, and the declared purpose | Retrieval driven by raw user text |
| 2 · Candidate sources | Choose candidate sources, including memory, which passes its own policy gate | Searching corpora the purpose does not justify |
| 3 · Authorize | Filter by tenant, subject, and resource ACL | The classic RAG leak: retrieving what the caller may not read |
| 4 · Fetch pinned versions | Read immutable snapshots named in the RunManifest (Chapter 4) | A run that cannot be replayed because sources moved |
| 5 · Classify and sanitize | Label each segment's kind and trust tier (see the hierarchy below), strip active content | Instructions embedded in retrieved documents |
| 6 · Deduplicate | Collapse near-identical chunks | One loud document crowding out the rest of the evidence |
| 7 · Rank | Order by relevance, freshness, source authority and effective dates (Chapter 5) | Similarity alone deciding what the model believes |
| 8 · Allocate tokens | Allocate tokens within per-section caps fixed before retrieval | Silent truncation dropping the constraint that mattered |
| 9 · Ordered references | Emit references, not content | Oversized payloads and unattributable claims |
| 10 · ContextManifest | Record exactly what was assembled and why, and record its hash on the model span | An answer nobody can audit |

Two ordering decisions carry most of the safety. **Authorization is stage three,
before any content is fetched** — filtering results after retrieval means the
unauthorized bytes already existed in a process that could log or cache them.
And **only the final boundary materializes bytes** into the model request;
everything upstream moves references, which is what keeps the manifest an
accurate record of what the model actually saw.

### The trust hierarchy of instructions

The model receives text from several origins in one window, and it has no
inherent way to rank them. The platform must, because the ranking is what stops
a document from behaving like an instruction.

| Tier | Origin | Trust | Can it direct behavior? |
| --- | --- | --- | --- |
| 1 | System and application instructions | Release artifact, code-reviewed | Yes — this is the definition of the agent |
| 2 | Skill instructions (Chapter 8) | Pinned, versioned capability artifact | Yes, within the capability's declared scope |
| 3 | User request | Authenticated intent, bounded by the caller's authority | It states a goal; it cannot grant itself authority |
| 4 | Retrieved documents and tool output | Untrusted evidence, whatever its source | **No.** It is data to reason over, never direction |

Workflow-state projections, conversation history, and memories are tier-four
data with different authority as facts: run state is canonical, conversation is
a record of what was said, and memory is advisory. None of them can direct
behavior. Each segment therefore carries one `kind`: `system_instruction`
(tier 1), `skill_instruction` (tier 2), `user_request` (tier 3), or one of
`run_state`, `conversation`, `enterprise_data`, `tool_result`, and `memory`
(tier 4).

Content cannot promote itself between tiers. A retrieved document that contains
"ignore previous instructions" is a tier-four artifact containing a string; it
does not become tier one by asserting that it should. This is why tool
eligibility is decided by policy before the step runs and never by what the
model has just read — the one rule that makes indirect prompt injection a
containable problem rather than an open one.

Retrieval can also happen inside a step, through a read-only tool behind the
Tool Gateway (Chapter 3); it calls the same Hub, and its results enter the next
model call as tier-four segments in a new manifest revision.

## Memory is not a bag of embeddings

One source feeding this pipeline behaves differently from the rest. Retrieval reads; memory *writes*, and a write that outlives the run is a protected data effect rather than a caching convenience. Creating long-term memory therefore carries the same obligations as any other durable write: an owner, a scope, provenance, a confidence, the policy basis that permitted it, a TTL, and a correction and deletion path. The write validates contradiction and sensitivity before it lands, and derived guesses default to run-scoped working memory, not long-term memory. And when a remembered summary disagrees with canonical business state, canonical state wins — always, and without the model being asked to adjudicate. Chapter 17 catalogs ungoverned memory writes as AP-13 and summary-as-state as AP-02.

### How the pattern works

Working memory is run-scoped; long-term memory carries the obligations above.

1. Identify a candidate reusable fact.
2. Validate evidence, subject, purpose, consent or policy basis, and sensitivity.
3. Write a versioned memory record with TTL and provenance.
4. Retrieve only after authorization and trust labeling.
5. Correct, supersede, expire, or delete through propagation workflows.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for stable preferences, repeated domain facts, or learned operational hints with clear value and governance. | Do not persist transient chain-of-thought, secrets, unverified hypotheses, protected data without basis, or facts already authoritative elsewhere. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Continuity | Creates privacy, staleness, correction, and deletion obligations. |
| Reduced context cost | May lose nuance or introduce summary drift. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Stale memory overrides state | Canonical precedence: the run state (Chapter 15) and the domain system of record win; freshness checks. |
| Cross-tenant leakage | Tenant-partitioned keys and authorization before retrieval. |
| Deletion gaps | Lineage graph, tombstones, cache invalidation, and rebuild. |

### What you need to see in production

* memory ID and version
* source provenance
* scope and tenant
* policy basis
* confidence and TTL
* retrieval and deletion events

## A workable implementation

### Who should own each decision

The Conversation Service owns turns; the Workflow Projection Service owns canonical run state; the Context Service's assembler creates an ephemeral model-input projection; its Retrieval Broker, the client of the Chapter 5 Hub, queries governed knowledge; the Memory Service owns approved cross-run memory; the Provenance Service tracks lineage; and the Compaction Service produces source-linked summaries. No component can silently promote a conversation statement into workflow truth or long-term memory.

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/context:assemble | Build a token-bounded context from pinned instructions, run state, conversation, knowledge, and memory under a policy and data budget |
| GET /v1/runs/{run\_id} (Chapters 4 and 15) | The canonical state projection and state\_version that context reads; never the transcript |
| POST /v1/conversations/{id}/turns | Append an immutable user/agent/tool turn with provenance, classification, and client idempotency key |
| POST /v1/knowledge:search | The Hub's query surface (Chapter 5): hybrid search with subject+actor context, source allowlist, freshness, filters, top-k, and required citations |
| POST /v1/memories | Propose/write a governed memory with scope, provenance, confidence, consent, TTL, and deduplication key; policy may require review |
| GET /v1/memories:search | Search only memories visible to the subject/purpose/run; returns confidence and source lineage |
| PATCH /v1/memories/{memory\_id} | Correct via optimistic version; preserves previous version and reason |
| DELETE /v1/memories/{memory\_id} | Create deletion tombstone and enqueue removal from indexes, caches, summaries, and derived artifacts |
| POST /v1/context:compact | Produce a source-linked summary/checkpoint under a target token budget; never overwrites source turns |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ConversationTurn | conversation/turn IDs, role/type, content reference/hash, producer, created time, classification, source/trace refs; append-only |
| RunStateProjection | run ID, schema/version, state version, variables, obligations, unresolved questions, budgets, artifact refs; derived from workflow history |
| ContextManifest | context ID, run ID, RunManifest digest, node ID, step request ID, revision, policy version, per-section caps and allocation, ordered segments, omitted candidate IDs, redactions, manifest hash, created time |
| ContextSegment | segment ID, kind and trust tier, source URI/revision, content hash, authorization decision ID, freshness, token count |
| MemoryRecord | memory ID, tenant, subject/team scope, type, canonical value, provenance, confidence, consent, purpose allowlist, TTL, status, supersedes |
| KnowledgeObject | source URI/revision, object/chunk IDs, text/blob reference, embedding version, metadata, ACL pointer, ingestion cursor, deletion state |
| SummarySnapshot | input segment hashes, summary hash/reference, model/prompt version, coverage map, unresolved facts, expiry; immutable |

There is one RunManifest per run and one ContextManifest per AgentStepRequest; the ContextManifest references the RunManifest digest. Tool results observed inside the step's loop are appended as tier-four segments in a new manifest revision recorded on each model span.

### Retrieval and memory consistency

* Search performs tenant/source pruning, exact ACL filtering, hybrid lexical/vector scoring, reranking, freshness filtering, and diversity/deduplication before context selection.
* Correcting or deleting a source creates lineage events that invalidate affected memories, summaries, embeddings, model caches, and evidence packages according to retention/legal-hold policy.

### Scalability and token economics

* Partition conversations and memories by tenant + subject/team; partition knowledge by tenant + source + region. Use routing metadata so a query touches only eligible partitions.
* Store content in object storage and metadata in relational/search stores. Context APIs exchange references; only the assembler materializes bytes for the authorized model call.
* Cache retrieval candidates by tenant, source revision, normalized query, policy scope, and embedding/reranker version; re-run exact authorization on cache hit (Chapter 21 owns authorization-scoped caching).
* Compact long conversations asynchronously and incrementally. Keep recent turns plus source-linked summaries; rebuild summaries when covered inputs change.
* Enforce deletion SLOs across primary metadata, vector/search indexes, caches, and derived summaries. Tombstones must outlive the longest replica/cache lag to prevent resurrection.

|  |
| --- |
| **PERFORMANCE AND COST**  Measure answer quality against context size — most systems are past the point where more retrieval helps. |

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Privacy lifecycle | Context and memory need purpose limitation, consent or other legal basis where applicable, data-subject request handling, deletion propagation, legal-hold precedence, residency, provider retention controls, and proof that derived summaries/indexes were handled too. | R13; R39 |

The discussion above draws on R13; R39. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

Start with the record every model call should leave behind: one ContextManifest whose segments carry their kind, trust tier, source revision, authorization decision, and hash, sealed so a later change is detectable.

[[EXAMPLE:context-manifest#core]]

## If this fails in production

1. Reconstruct one ContextManifest without relying on logged plaintext.
2. Compare canonical state with summaries and working memory.
3. Trace a corrected or deleted fact through indexes, cache, memory, and artifacts.

If the transcript is the state or memory is written by default, the repair is structural; see AP-02 and AP-13 in Chapter 17.

## What to verify before production

**✓** Workflow state, conversation, enterprise knowledge, working memory, and long-term memory are separate sources, and artifacts, telemetry, and audit live in the Chapter 4 stores.

**✓** Authorization occurs before content materialization.

**✓** Context records ordered references, hashes, trust labels, decisions, versions, redactions, and token allocation.

**✓** Memory creation is a governed write with scope, provenance, confidence, lawful basis, TTL, correction, and deletion.

**✓** Correction and deletion propagate through indexes, caches, summaries, memories, contexts, and artifacts.

## Put the idea to work

1. Design a token budget across instructions, state, evidence, memory, and reserve.
2. Define the lifecycle of a reusable mortgage evidence-review preference memory.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why call the prompt a projection rather than state? | It is a temporary, token-bounded view assembled from authoritative stores for one step; it can be rebuilt, audited by reference, and discarded. |
| How do the five sources of context differ? | Workflow state is canonical in the durable run; conversation is interaction history; enterprise knowledge is source-backed governed fact; working memory holds run-scoped hypotheses; long-term memory holds approved reusable facts—each with different ownership, retention, authority, and deletion. |
| What problem does a ContextManifest solve? | Reproducibility and diagnosis through ordered source, version, and hash references, authorization decisions, trust labels, redactions, and budget without logging all plaintext. |
| How should retrieved instructions be handled? | As untrusted data with provenance and untrusted-content labels; they cannot alter system instructions, tool eligibility, policy, credentials, or destination grants. |
| How do you delete a fact from an agentic system? | Tombstone and revoke the source, remove derived indexes, invalidate caches, rebuild summaries and contexts, clean governed memory and affected artifacts, and preserve permitted audit evidence. |

## Where this leads next

Context assembly completes Part II: every model call now has an owned plane, a pinned RunManifest, governed knowledge, and a recorded ContextManifest. Chapter 7 packages these contracts as a paved road so teams build on them rather than rebuilding them.
