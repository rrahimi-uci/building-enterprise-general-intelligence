# Closing Perspective: What Production-Grade Intelligence Requires

|  |
| --- |
| **THE PRODUCTION STANDARD**  An enterprise-grade system produces a verified outcome within explicit authority, time, cost, data, and risk boundaries; survives partial failure and change; and preserves evidence sufficient for users, operators, reviewers, and auditors. |

Chapter 1's prototype failed in one week for five reasons, none of them intelligence.

| **Day** | **Failure** | **What now contains it** |
| --- | --- | --- |
| Monday | A redeploy erased a running case with no record of what it had done | Durable run history, suspended waits, compatible workers (Chapters 15 and 27) |
| Tuesday | An uploaded document carried an injected instruction | Content–instruction separation, boundary enforcement, containment (Chapters 6, 20, and 23) |
| Wednesday | A document request committed, but its confirmation was lost | Effect ledger, intent hash, reconciliation of unknown outcomes (Chapter 22) |
| Thursday | An auditor asked why the case advanced, and only the model's statement remained | Causal run trace plus a separate audit ledger (Chapter 24) |
| Friday | A cheaper model shipped with no code change and missed incomplete evidence | Evaluated, immutable release with rollback of assignment (Chapters 25 and 27) |

The model provides bounded reasoning; the surrounding system owns state, authority, effects, evidence, and recovery.

## The unified enterprise architecture

Figure S-1 is the book's canonical **logical** architecture. Chapter 4's seven
ownership planes determine who writes each record; the figure groups their
components by design time, regional runtime, external boundary, and
offline improvement. The deterministic workflow owns the run. A bounded agent
step proposes; independent controls decide whether its proposal may change
anything outside the run. No model, framework, vector index, or trace store
becomes the system of record by being on the request path.

[[DIAGRAM:unified-enterprise-architecture|Figure S-1 — The unified enterprise architecture: governed releases and knowledge enter a regional run; bounded reasoning proposes, deterministic gates control effects, and evidence returns through an offline improvement loop]]

### Read the boundaries and line styles

The pale frames separate the **global control tier**, a **regional execution
cell**, **external systems**, and **offline evidence and improvement**. Boxes
name services, service groups, or immutable release records. Each box's icon only helps the eye find it; the label
carries the meaning. Solid blue arrows
carry requests, authorized actions, and results; solid cyan arrows carry knowledge or returned
evidence; dashed arrows carry released definitions and enforcement; dotted
arrows carry recorded evidence, including joined task results and effect
receipts. Each arrow points in the direction of the named transfer. Paired
arrows to models and enterprise systems mean a governed
request crosses the boundary and a response or receipt returns. A release
arrow is a reviewed promotion, not a runtime write.

| **Architectural area** | **Responsibility in the figure** | **Ownership planes and chapters** |
| --- | --- | --- |
| Experience and admission | Users, APIs, and events enter through authenticated, risk- and capacity-aware admission; verified results return through the same channel. | Experience and channels; 1, 4, 14, 21, 28 |
| Durable runtime and agent applications | The Run Service pins a manifest, schedules bounded agent steps and child tasks, owns workflow history and acceptance, and survives waits and failures. AgentRuntime owns only one step's reasoning and typed result. | Runtime and workflow; Agent applications; 2–4, 10–18 |
| Knowledge, context, and memory | The registry releases governed knowledge. The Context Service assembles an authorized, token-bounded ContextManifest from pinned knowledge, current workflow state, conversation, evidence, and eligible memory. | Knowledge, context, and memory; 5–6 |
| Model and tool access | The LLM Gateway selects an eligible model and enforces privacy and budgets. Separate Tool, MCP, and A2A gateways terminate their respective boundaries; the Effect Service records mutating intent, outcome, and reconciliation. | Gateways and integration; 2, 4, 19, 22, 28 |
| Trust and governance | Subject and actor identity, policy, narrow grants, proposal-bound approval, secret leases, sandbox and egress control, and a separate audit path apply at admission, retrieval, inference, delegation, and effects. | Security and governance; 14, 20–23, 26 |
| Evidence and operations | Linked traces, metrics, SLOs, cost, incidents, and human feedback diagnose runs; the audit ledger preserves protected decisions separately from sampled telemetry. | Evaluation and operations; 24, 28 |
| Engineering and release | Domain and platform owners build and test agents, Skills and packs, workflows, policies, tools, and evaluation cases. Risk-tiered validation and approval promote immutable release bundles; canaries and rollback control new assignments. | Agent applications; Evaluation and operations; 7–9, 25–27 |

### Follow one request to a verified outcome

1. A channel authenticates a subject and acting workload; admission checks
   tenant, purpose, risk, deadline, and capacity. The Run Service writes one
   RunManifest from a promoted ReleaseManifest, including Skill and knowledge
   release digests, model eligibility, capability envelope, and budgets
   (Chapters 4, 21, 27, and 28).
2. The workflow asks the Context Service for a step-specific ContextManifest.
   Authorization and source ACL checks happen *before* retrieval. The manifest
   records source revisions, trust tiers, redactions, and token allocation;
   retrieved text stays data, never an instruction or a grant (Chapters 5–6).
3. AgentRuntime executes one bounded step. Its framework may reason, choose an
   eligible tool façade, plan, critique, or request a specialist, but returns a
   typed AgentStepResult to the workflow. The Task Service owns durable child
   tasks and joins; MCP and A2A terminate at local gateways when work crosses
   those boundaries (Chapters 3, 10–13, and 18–19).
4. The workflow validates the proposal, asks policy for the exact subject,
   actor, purpose, action, and resource, and pauses for a proposal-bound human
   approval when required. After reauthorization, the Tool Gateway commits a
   permitted effect under one logical key. A receipt confirms it; an ambiguous
   timeout becomes **Unknown** and is reconciled before dependent work proceeds
   (Chapters 2, 14, and 20–22).
5. The workflow checks executable acceptance criteria against authoritative
   state and effects, records the terminal outcome, and returns the authorized
   result. A model's completion claim cannot close the run. Traces and audit
   records link the request, versions, decisions, effects, and outcome
   (Chapters 13, 15, and 24).

### Follow knowledge from source to use

Enterprise policy, documents, and structured source records enter an intake
process as bytes with source digests and permissions. Extraction proposes
fields, requirements, terms, relationships, and rules; source-span grounding,
schema, consistency, regression, staleness, and independent SME review gate
the candidate. The registry publisher activates an immutable KnowledgeRelease.
At admission, each required stream resolves once to a digest in the
RunManifest. The Context Service consumes authorized views of that pin, while
control points evaluate its enforceable rules against verified facts. Runtime
contradictions, refusals, and corrections become evidence for a *new* reviewed
knowledge change; they never edit the pinned release in place (Chapters 5–6
and 27).

### Close the evidence and improvement loop

Runtime emits causal traces, operational metrics, protected audit records,
effect receipts, and feedback. Evaluation joins these with reviewed cases and
ground truth, checks outcome and trajectory per risk slice, calibrates judges
against human labels, and gives deterministic security and effect invariants
precedence. Owners diagnose failures and propose the smallest ChangeBundle;
CI, review, approval, canary, and release promotion move a new immutable
bundle to eligible *new* runs. Active runs remain pinned to compatible workers;
rollback changes new assignment, not their history (Chapters 24–27).

The figure deliberately groups plan compilation, intervention, budgeting,
sandboxing, cache policy, and incident response with their owning services;
their separate contracts remain in Chapters 12, 14, 23, and 28 and Appendix C.
Likewise, the source-intake card represents governed copies and digests of
enterprise material, not authority over the external system of record. This
logical view does not prescribe one vendor or one deployment product.

The companion code implements the first three checkpoints (C01–C03); later checkpoints are roadmap targets, specified in this book and tracked in Appendix H.

# PART REFERENCE — APPENDICES: FIELD GUIDE AND REFERENCE

The appendices are meant to be used at the desk, not admired at the end of the
book. They collect decision aids, runbooks, contracts, framework notes, the
Harborlight implementation guide, the evidence registry that keeps the main
argument honest, and a glossary. An index of key terms follows them.

# Appendix A — Choosing the Right Pattern: A Decision Guide

## Start with the outcome the system must protect

1. Known path: deterministic workflow; add a bounded semantic node only where ambiguity remains.
2. Next step depends on observation: bounded ReAct with budgets and executable acceptance.
3. Work survives waits/restarts/humans: durable execution.
4. Specialists collaborate: typed tasks, one owner, artifacts, deterministic join.
5. Trust/deployment boundary: identity, authorization, protocol gateway, tenancy, audit.
6. Side effect: the six gates (Chapter 2), idempotency, and reconciliation.
7. Post-deployment improvement: governed learning; never self-certification.

Chapter 16 and its Figure 16-1 cover the Part IV subset of these choices.

## Pattern cards

Each card names the obligation it protects, the shortcut that fails, the better design, and the chapter that builds it. Where the pattern already has a card in its chapter, the entry stays short and points there.

### P-01 — Bounded ReAct

**Use when.** The next step depends on an observation, and adaptive evidence gathering is needed.

**Shortcut that fails.** An unbounded think–act loop, in which the model owns stopping, budget, and success.

**Better design.** A controller bounds steps, time, tokens, tools, and evidence, and deterministic acceptance decides when the work is done.

**Built in.** Chapter 10; card: Chapter 10 § ReAct at a glance.

### P-02 — Deterministic spine with semantic nodes

**Use when.** Known obligations include a few judgment points.

**Shortcut that fails.** A conversational agent owns the process, so retries, waits, joins, approval, and compensation become ambiguous.

**Better design.** A durable workflow with bounded semantic nodes: workflow state → semantic task → typed result → deterministic transition. The Harborlight evidence review always loads the case, checks the policy snapshot, requests missing documents through the six gates, and runs acceptance; only the evidence assessment between those steps is semantic.

**Watch and cost.** Track transcript-only state, orphan tasks, duplicate effects, and recovery time. Workflow modeling adds upfront cost.

**Built in.** Chapters 12 and 15.

### P-03 — Typed ContextManifest

**Use when.** The model needs authorized, fresh evidence within a token budget.

**Shortcut that fails.** Top-k hits and chat history are dumped into the prompt, so selection, access control, freshness, poisoning, and truncation cannot be reproduced.

**Better design.** Authorization precedes retrieval, and a manifest records each segment's source, snapshot, provenance, rank, freshness, and token allocation: planner → authorization → retrieval → ranking/dedup → manifest → model.

**Built in.** Chapter 6 § How context is assembled.

### P-04 — Provenance-bound memory

**Use when.** Useful facts must persist beyond one run.

**Shortcut that fails.** Every interaction is written to one vector store, so errors, secrets, stale facts, and injected instructions persist.

**Better design.** Working memory stays run-scoped; long-term memory is written only through a gate that requires purpose, scope, TTL, provenance, verification, and a deletion path.

**Built in.** Chapter 6 § Memory is not a bag of embeddings.

### P-05 — Tool façade behind the six gates

**Use when.** An agent must cause a business effect.

**Shortcut that fails.** A broad CRUD call with ambient credentials, so language becomes authorization and retries duplicate work.

**Better design.** A typed, least-privilege tool whose effects pass the six gates: propose → validate → authorize → commit → verify → accept.

**Built in.** Chapters 2 and 22; card: Chapter 2 § Tool Use at a glance.

### P-06 — Typed task ownership and join

**Use when.** Specialists collaborate on one outcome.

**Shortcut that fails.** Free-form agent chat owns the work, producing duplicate owners, cycles, lost artifacts, and premature completion.

**Better design.** A TaskEnvelope gives each task one owner, narrowed authority, a deadline, artifacts by reference, cancellation, and a deterministic join.

**Built in.** Chapters 11 and 18; card: Chapter 18 § Supervisor/Worker at a glance.

### P-07 — Least-privilege capability envelope

**Use when.** Agents need sensitive access.

**Shortcut that fails.** One reusable token follows the chain, so injection or compromise gains broad authority.

**Better design.** Subject and workload identity yield a capability envelope (scope) by intersection, and a short-lived credential lease (proof) is minted at the moment of use: identity → policy → capability envelope → credential lease → gateway and tool enforcement. A loan officer may read an authorized mortgage case and propose a document request, but cannot approve the operation or make the lending decision.

**Watch and cost.** Track scope and age, expansion attempts, cross-tenant attempts, and denials. Fine-grained policy needs templates and simulation.

**Built in.** Chapter 21.

### P-08 — Effect ledger and reconciliation

**Use when.** A timeout may follow a committed external effect.

**Shortcut that fails.** Timeout means failure and retry, so the same logical effect executes twice.

**Better design.** An EffectRecord reserved before dispatch, a stable logical effect key, an Unknown state that blocks retry, and reconciliation against the authoritative system: reserve → dispatch → receipt or Unknown → reconcile → accept. A timed-out mortgage document request is looked up by its idempotency key before anything retries it.

**Watch and cost.** Track Unknown rate and age, duplicate effects, and reconciliation latency. It requires downstream receipts or a query interface.

**Built in.** Chapter 22.

### P-09 — Causal run trace

**Use when.** Diagnosis spans model, context, policy, tools, humans, and effects.

**Shortcut that fails.** Independent logs and transcripts, so the first divergence and the attribution of outcome and cost are lost.

**Better design.** One trace links request, release, context, decisions, effects, acceptance, and outcome through trace IDs and domain IDs. The trace reveals stale retrieval before a correct but misinformed tool call.

**Watch and cost.** Track unlinked spans, missing versions, outcome joins, and diagnosis time. Capture is costly and sensitive; sample and reference payloads.

**Built in.** Chapter 24.

### P-10 — Evidence gates scaled to the change

**Use when.** Behavior changes often but review capacity is finite.

**Shortcut that fails.** Manually review everything, or auto-deploy from one score; fatigue or self-certification hides risk.

**Better design.** Review depth follows change class × use-case tier (Chapter 26), with proportional tests, reviewers, canary, and rollback: ChangeBundle → change class and tier → validation → approval → staged release. A typo fix in a low-tier assistant auto-promotes; a model change for the mortgage evidence agent requires domain, privacy, and risk approval.

**Watch and cost.** Track bypasses, reviewer fatigue, exception age, and regression escapes. Classification needs calibration.

**Built in.** Chapters 25–27.

### P-11 — Durable runtime with backpressure

**Use when.** Runs face bursts, waits, humans, and unreliable dependencies.

**Shortcut that fails.** Synchronous workers retry locally, so state is lost and outages amplify queues and retries.

**Better design.** Durable state, timers, and bounded retries (Chapter 15), plus admission permits, quotas, circuit breakers, and degraded mode (Chapter 28).

**Built in.** Chapters 15 and 28; card: Chapter 15 § Durable execution at a glance.

### P-12 — Portable contracts and adapters

**Use when.** Several frameworks or providers must coexist.

**Shortcut that fails.** Application code depends on provider-native objects, so migration rewrites applications and controls diverge.

**Better design.** Platform-owned contracts and normalized events with conformance-tested adapters: application contracts → adapters → shared services → providers and protocols. A framework migration keeps tools, policy, traces, evaluation, and release intact.

**Watch and cost.** Track native-object leakage, conformance failures, and migration effort. The abstraction may lag new features; allow negotiated extensions.

**Built in.** Chapters 3 and 7.

### P-13 — Pinned knowledge release

**Use when.** Agents reason over, or are bound by, institutional knowledge such as policies, obligations, and controls.

**Shortcut that fails.** "Current" documents are indexed and similarity decides, so a rule changes under a run with no deployment, no approval, and no trace.

**Better design.** Knowledge is developed in a control plane and consumed as a release: change → gates → independent approval → release → live pointer → one pin per run → control points consult the pin.

**Watch and cost.** Track held objects per release, unknown-under-policy refusals, and citations of superseded releases. Gates prove structure, not meaning, so SME review time is the real cost.

**Built in.** Chapter 5 § Change compliance knowledge the way you change software.

## Match the obligation to a pattern

The chapters column lists where each pattern is built, plus Chapter 17 for its anti-patterns. The last four rows are Part IV patterns without a P-card; their cards are in Chapters 11–14.

| **Category** | **Recommended pattern** | **Anti-pattern** | **Chapters** |
| --- | --- | --- | --- |
| Reasoning | P-01 Bounded ReAct | AP-11 unbounded loops | 10, 17 |
| Orchestration | P-02 deterministic spine | AP-01 monolith; AP-07 model says done | 12, 15, 17 |
| Context | P-03 ContextManifest | AP-02 prompt database | 6, 17 |
| Knowledge | P-13 pinned knowledge release | AP-09 vector truth | 5, 17 |
| Memory | P-04 provenance-bound memory | AP-13 memory write by default | 6, 17 |
| Tools | P-05 tool façade behind the six gates | AP-06 Boolean approval; AP-12 ungated discovery | 2, 17, 21, 22 |
| Multi-agent | P-06 typed tasks/join | AP-08 chat as workflow | 11, 17, 18 |
| Security | P-07 capability envelope | AP-03 ambient authority; AP-10 judge gate | 17, 21 |
| Reliability | P-08 effect reconciliation | AP-04 retry everywhere; AP-05 timeout=failure | 17, 22 |
| Observability | P-09 causal run trace | AP-14 unlinked telemetry | 17, 24 |
| Governance | P-10 evidence gates scaled to the change | AP-15 provider swap as config; AP-16 in-place change | 17, 25–27 |
| Operations | P-11 durable runtime/backpressure | AP-04 retry amplification under load | 15, 17, 28 |
| Architecture | P-12 portable contracts/adapters | — | 3, 7, 17 |
| Routing and handoff | Chapter 11 routing and handoff | AP-08 chat as workflow; AP-12 ungated discovery | 11, 17 |
| Planning | Chapter 12 plan compilation | AP-11 unbounded loops | 12, 17 |
| Quality | Chapter 13 reflection, evaluator–optimizer, and acceptance | AP-07 model says done; AP-10 judge gate | 13, 17 |
| Human authority | Chapter 14 approval and intervention | AP-06 Boolean approval | 14, 17 |

# Appendix B — When Things Go Wrong: Triage and Runbooks

Each row names the Chapter 17 card that describes the failure's usual cause.

| **Symptom** | **Inspect first** | **Safe response** | **Anti-pattern** |
| --- | --- | --- | --- |
| Plausible answer, wrong evidence | ContextManifest, revisions, authorization, trust labels | Rebuild context; reject unsupported claims; add regression case | AP-02, AP-09 |
| Two runs decide differently on identical input | RunManifest knowledge snapshots and the release manifests they name | Compare the releases; never re-resolve against "current" | AP-09 |
| Repeated tool loop | Action-observation signatures and information gain | Stop on no-progress; reduce tools; route or escalate | AP-11 |
| Duplicate business write | Effect key, intent hash, idempotency, receipt | Freeze dependents; reconcile; repair retry ownership | AP-04 |
| Write timed out | Effect state and downstream request ID | Mark Unknown; never blind-retry; reconcile | AP-05 |
| Run stuck after approval | Proposal hash, expiry, version, signal | Reauthorize; reapprove if drifted; repair wait | AP-06 |
| Cross-tenant retrieval | Tenant key, policy, cache key, artifact lineage | Emergency deny; quarantine; incident response | AP-03 |
| Old run fails after deploy | RunManifest and compatibility | Compatible worker or tested migration | AP-16 |
| High p95 latency | Queue, model, retrieval, tool, human, retry path | Fix dominant segment; enforce permits | AP-04 |
| Judge passes security failure | Scorer precedence | Hard deterministic failure blocks release | AP-10 |
| Run closed with obligations outstanding | AcceptanceDecision and acceptance criteria | Reopen through intervention; require executable acceptance | AP-07 |
| Unsafe remote artifact | Peer, grant, schema/hash/classification/scan | Reject adoption; quarantine; review trust profile | — (Chapter 19) |

## When an effect may have happened but no receipt returned

1. Stop dependent work and preserve cancellation intent.
2. Load EffectRecord, intent hash, expected version, downstream request ID, and trace.
3. Query the authoritative downstream system by idempotency key, resource ID, or business predicate.
4. Classify the result in Chapter 22's effect states: Committed; Declined (proven absent: no match after the visibility window the tool manifest declares); Partial; still Executing (check again within that window); or InterventionRequired (unprovable, including a provider that declares no window).
5. Record evidence; then accept a Committed receipt, retry a Declined effect under the same logical key, compensate a Partial one, or open an intervention task (Chapter 14).
6. Add the failure to simulation and release regression tests.

# Appendix C — Core Platform Contracts at a Glance

Each contract has one owner and one defining chapter, as indexed in Chapter 4 § The contracts that hold the platform together. Key fields are abridged; the defining chapter holds the full record.

| **Contract** | **Owner** | **Key fields** | **Defined in** |
| --- | --- | --- | --- |
| RunManifest | Run Service | ReleaseManifest digest; resolved Skill and pack digests, knowledge snapshots (release digests per stream), model route, runtime adapter, capability envelope, budget, use-case tier; written once at admission | Chapter 4 |
| Artifact | Producing run (bytes in the artifact store) | artifact ID, immutable version, schema, content hash, creator run/node/agent, source refs, classification, residency, retention | Chapter 4 |
| Event (CloudEvent envelope) | Producing service, through its outbox | standard attributes plus tenant, correlation, and causation extensions (wire names `tenantid`, `correlationid`, `causationid`; CloudEvents allows only lowercase letters and digits) and `traceparent`; payload by `dataref` and `datahash` | Chapter 4 |
| AgentStepRequest / AgentStepResult | Run Service builds the request; AgentRuntime returns the result | request: identity, behavior pins, ContextManifest, capabilities, bounds, output schema, trace; result: status (`completed`, `needs_input`, `proposed_action`, `failed`), payload, artifact refs, proposed action, usage, error | Chapter 3 |
| KnowledgeArtifact | Knowledge Hub | kind, source digest and region, extractor and verifier versions, per-field verdicts, corroboration, status and review route, owner, version/supersedes, effective range, scope, ACL and data class | Chapter 5 |
| KnowledgeRelease | Knowledge registry; the registry publisher writes | stream, version, digest, ontology version, object digests, source revisions, pinned base and tenant-extension revision, gate records, author, approving human, candidate digest, previous release, effective period, activation record | Chapter 5 |
| KnowledgeBinding | Knowledge registry; moved only by the registry publisher | stream, tenant, environment, region → active release digest; previous digest; compare-and-swap on move; activation record | Chapters 5 and 27 |
| ContextManifest | Context Service | RunManifest digest, node, step request ID, revision, policy version, section caps and allocation, ordered segments (kind, trust tier, source revision, hash, authorization decision), omitted candidates, redactions, manifest hash | Chapter 6 |
| MemoryRecord | Memory Service | tenant, subject/team scope, type, value, provenance, confidence, consent, purpose allowlist, TTL, status, supersedes | Chapter 6 |
| Skill manifest | Skill owner; Skill Registry | interface schemas, instructions, required tools and knowledge, data-class and region policy, `risk_ceiling`, evaluation suite and gates, owner, digest; lifecycle lives in SkillRelease | Chapter 8 |
| SkillPackManifest | Pack owner | pinned Skill digests, dependency constraints, runtime capabilities, data and region policy, risk ceiling, evaluation gates, release aliases, support window; certified by a CompatibilityReport | Chapter 9 |
| RoutingDecision | Route service (agents); LLM Gateway (models) | candidate routes, exclusions and reasons, selected route, confidence and reason, fallback | Chapters 11 and 28 |
| OwnershipTransfer | Ownership Service | task, from/to owner, previous/new capability envelope, obligations, deadline, acknowledgment state (proposed, accepted, rejected, expired), proposal hash | Chapter 11 (record in Chapter 18) |
| Plan IR (CandidatePlan, PlanNode) | Planner proposes; Plan Compiler validates | plan ID, revision, goal, `capability_envelope_id`, budget; nodes with kind, capability ref, dependencies, inputs, output schema, `risk_class`, retry policy, acceptance checks, failure strategy | Chapter 12 |
| AcceptanceDecision | Acceptance engine | candidate, criteria version, outcome (accepted, rejected with typed defects, escalated), per-criterion evaluator type and evidence refs | Chapter 13 |
| ApprovalRequest / ApprovalDecision | Approval Service | request: proposal hash, resource and logical effect key, before/after diff, subject and actor, evidence, policy digest, risk class, expected resource version, expiry, allowed responses; decision: proposal hash, approver identity and assurance, decision, reason, signature, time | Chapter 14 |
| InterventionTask | Assignment/Queue Service | run/node, trigger and reason code, evidence refs, alternatives, allowed responses, assignee, SLA, state/version, response | Chapter 14 |
| WorkflowExecution | Workflow engine | run ID, workflow type/build, home region/shard, state, state version, history generation | Chapter 15 |
| TaskEnvelope | Task Service | identity, goal, data, contract, authority (`capability_grant_id`), budgets, reliability (idempotency key, cancellation), observability | Chapter 18 |
| FederatedTask | A2A Gateway (Task Bridge) | local and remote task IDs, parent run, peer/agent/version, capability envelope ref, state mapping, idempotency key, deadline, budget | Chapter 19 |
| CapabilityEnvelope | Authorization Service | grant ID, run/task, permitted actions/resources/data classes, explicit denies, purpose, regions, maximum risk class, cost ceiling, delegation depth, expiry, parent grant | Chapter 21 |
| PolicyDecision | Authorization Service | decision ID, input hash, result, obligations, reason codes, policy digest, evaluated time | Chapter 21 |
| CredentialLease | Access Broker/STS | opaque handle, kind, grant and decision IDs, audience, scope, expiry, use count, sender binding; secret never in run state | Chapter 21 |
| ToolManifest | Tool Registry | identity, interface schemas, security, risk class, runtime limits, effect semantics (idempotency key, precondition, receipt, compensation), operations | Chapter 22 |
| EffectRecord / EffectReceipt | Effect Service | logical key, idempotency key, intent hash, expected version, state (Chapter 22's lifecycle), downstream IDs, receipt, compensation refs | Chapter 22 |
| OutboxRecord / InboxReceipt | Producing service / consumer | event ID, aggregate version, envelope, publish state; consumer, source/event ID, payload hash, status | Chapter 22 |
| EvaluationResult / ValidationReport / ReleaseGateDecision | Evaluation Orchestrator; Evaluation/Gate Service | metric, score, evaluator type and version; candidate digest, comparisons, slice regressions; tier, thresholds, decision, waiver, approvers | Chapter 25 |
| GovernanceRecord / ExceptionWaiver | Governance Inventory; Exception Service | use case, owners, risk tier, autonomy, data classes, effects, controls, evaluations, current release, exceptions, review date; waiver scope, compensating controls, expiry | Chapter 26 |
| ChangeBundle / ReleaseManifest | Release Bundle Builder | proposed changes, evidence, risk, rollback plan; immutable signed dependency graph including Skill and pack digests, migrations, rollout and rollback | Chapter 27 |
| EnvironmentBinding / PromotionDecision | Promotion Service | tenant/use case/environment/region, active manifest, traffic weights; gate digest (ReleaseGateDecision), approvers, canary cohort, rollback trigger | Chapter 27 |
| BudgetReservation | Usage/Cost Ledger | reservation ID, owner run/node, resource, amount, consumed/released, expiry, ledger version | Chapter 28 |

# Appendix D — Choosing an Agent Framework

> **Evidence context:** Each row's strengths come from that product's or standard's own current documentation, cited in the row. Those sources describe what the tool says it does; they do not certify it for production. The enterprise cautions are this book's assessment of what an organization still has to supply around each tool. Every source is living documentation, so re-check the version and maturity status before relying on a row.

|  |
| --- |
| **FRAMEWORKS SOLVE DIFFERENT LAYERS**  An agent SDK is not automatically a durable workflow engine; a protocol is not an authorization system; a trace product is not an audit ledger; and a managed agent runtime does not remove the enterprise’s responsibility for data, policy, and outcome risk. |

## Compare frameworks by the layer they serve

Read the caution column through five questions, because they are where
framework choices fail in enterprises. **State:** does the tool's memory of a
run become the record of the business case, or only a copy? **Authority:** whose
identity does a tool call carry, and who decides it is allowed? **Lifecycle:** is
the feature generally available, in preview, or in maintenance, and how fast
does the API change? **Exit:** what would it cost to move runs, traces, and
prompts to another tool? **Evidence:** can the organization prove afterwards
what happened, or only see a debug trace?

| **Framework or standard** | **Strength** | **Enterprise caution** | **Recommended placement** |
| --- | --- | --- | --- |
| OpenAI Agents SDK | Compact Python runtime for agents, tools, handoffs, guardrails, structured outputs, sessions, tracing, MCP, human-in-the-loop with resumable RunState, and sandbox agents [R29][R30] | **State:** sessions and RunState hold conversation and paused runs, never the mortgage case. **Authority:** the SDK carries no enterprise identity; tools must call governed façades with delegated credentials. **Lifecycle:** a 0.x release line, so pin the version and re-run conformance tests on every upgrade. **Evidence:** tracing is on by default, exports to OpenAI, and includes sensitive model and tool data unless turned off; configure it before any regulated data flows [R29] | Bounded AgentRuntime adapter (Chapter 3); an SDK handoff moves control inside one step, never accountability (Chapter 11). Book baseline: `openai-agents==0.22.2` with `openai==3.13.0` in the offline profile |
| Claude Agent SDK and Managed Agents | The Agent SDK exposes Claude Code's agent loop, built-in tools, hooks, permissions, subagents, MCP, and sessions as a library [R55]; Managed Agents is a hosted agent harness for long-running work with persisted sessions, a server-sent event stream, and Anthropic-managed or self-hosted sandboxes [R56] | **Lifecycle:** Managed Agents is documented as beta, so plan for interface change and confirm support terms [R56]. **State and exit:** hosted sessions live with the vendor; keep the run, effect, and audit records in the platform so a run can move. **Authority:** SDK permissions govern the agent's own tools, not enterprise data access; effects still pass the Tool Gateway | Research and coding workloads behind the same AgentRuntime boundary; keep run, effect, and audit state portable |
| Google ADK and A2A | Composable model-driven agents, tools, and multi-agent workflows [R32]; A2A 1.0.1 defines agent cards, tasks, messages, artifacts, bindings, and lifecycle operations [R07] | **Authority:** an agent card describes a peer; it does not make the peer trustworthy or authorize what it may receive. **State:** a remote task's status is the peer's claim until the platform adopts the artifact (Chapter 19). **Exit:** cloud-managed conveniences can tie deployment to one provider; keep A2A at the boundary so peers stay replaceable | ADK as one harness option behind the platform boundary; the A2A Gateway at cross-team and vendor boundaries (Chapter 19) |
| Microsoft Agent Framework | Agent and graph-workflow abstractions that succeed and combine AutoGen and Semantic Kernel: sessions, middleware, telemetry, broad provider integrations [R31] | **Lifecycle:** some languages and features remain in preview (the Go SDK, for example), so check each feature's status before depending on it [R31]. **Exit:** Azure-centric managed integrations increase coupling. **State:** framework sessions and workflow state are not the system of record; do not bind public contracts to framework messages | Behind adapters where the Microsoft ecosystem and typed middleware matter; pair with the durable and effect architecture |
| LangGraph and LangSmith | Explicit graph state, checkpointers, interrupts, stores, time travel, human-in-the-loop [R34]; trace-based offline and online evaluation [R25] | **State:** checkpoints let a graph resume, but they are not enterprise durability: retries of external writes, timers over weeks, and versioned workflow upgrades still need a durable engine or careful design. **Evidence:** LangSmith traces are diagnostic; audit still needs a separate, append-only record. **Authority:** identity, policy, and effects must be integrated by the application | Application-level graph orchestration, optionally inside a separate durable workflow; keep external writes governed |
| Pydantic AI | Typed agents with durable-execution integrations, including Temporal, DBOS, Prefect, and Restate [R36] | **Correctness:** a typed output proves shape, not authorization, truth, or that an effect happened. **State:** durability is only as strong as the chosen backend and where activity boundaries are drawn; a side effect inside a replayed step can repeat | Strongly typed application adapters and testable agent code |
| LlamaIndex Workflows | Lightweight event-driven, asynchronous workflows integrated with retrieval and data pipelines [R35] | **State:** assess whether workflow state survives process loss and deployment for the target runtime. **Authority:** retrieval pipelines must filter by the caller's permissions before results reach the model (Chapter 6) | Retrieval-heavy flows and controlled event-driven pipelines behind platform gateways |
| CrewAI | Crews of role-playing agents with goals and tools, and event-driven Flows that manage state and control execution [R57] | **Design:** role-play encourages more agents than a task needs; compare against a single agent first (Chapter 16). **State, authority, evidence:** the documentation does not establish durability, permission, trace, or effect semantics, so verify each before production [R57] | Prototyping and bounded automations whose flow layer passes platform controls |
| Dapr Agents | Connects agents to Dapr workflows, actors, state, pub/sub messaging, resiliency policies, and distributed tracing [R37] | **Operations:** adds a sidecar and actor model the team must run, patch, and observe. **State:** guarantees depend on the configured Dapr components (state store, broker), so test failure behavior with the production components | Teams already standardized on Dapr that want durable, stateful, event-driven agents |
| Amazon Bedrock Agents Classic / AgentCore | Bedrock Agents Classic documents a supervisor/collaborator model; its documentation states the service is closed to new customers and points to AgentCore for similar capabilities [R33] | **Lifecycle:** do not start new work on a service closed to new customers; budget a migration for existing estates [R33]. **Exit:** managed supervisor topology and AWS-specific services raise switching cost. **Authority and evidence:** wrap source-system authorization and keep the audit record outside the managed service | Existing Classic estates or AWS-native evaluations that account for its status; wrap source-system authorization and evidence externally |
| Temporal | Durable execution: crash-proof workflows that resume in a new process after failure, reliable long waits, and long-running processes [R02] | **Engineering discipline:** workflow code must stay deterministic and versioned, so model calls and tool calls belong in activities. **Effects:** durable retries make a non-idempotent write happen twice unless effects carry keys and reconciliation (Chapter 22). **Operations:** self-hosting means running the cluster and its persistence; a managed service shifts that to a vendor | Strong default for long-running workflows and recoverable coordination (Chapter 15) |
| DBOS, Restate, and cloud durable runtimes | Crash-resilient workflows, timers, retries, external-event waits, and long-running processes [R38][R58] | **Scope:** they supply durability only, not agent reasoning, knowledge governance, tool semantics, or business authorization. **Scale and recovery:** their documentation does not establish scale or regional-recovery behavior, so load-test and rehearse recovery before relying on them [R58] | Execution substrate beneath the agent harness when a code-centric, simpler operational footprint fits |
| MLflow 3.15.x | GenAI tracing and evaluation: datasets, judges and scorers, feedback, and production monitoring [R20][R21] | **Evidence:** traces support debugging, not audit, and must be redacted before they hold customer data. **Measurement:** model judges need calibration against human labels before they gate a release (Chapter 25) | Diagnostics and evaluation baseline pinned to 3.15.2 in this edition (Chapters 24 and 25) |
| MCP | Tool and resource interoperability with standard transports [R05] and OAuth-based HTTP authorization with audience-bound tokens [R06] | **Authority:** the specification makes authorization optional, so an MCP server may have none; token passthrough and confused-deputy risks follow. **Trust:** tool descriptions are third-party text; tool trust, risk class, tenancy, and business policy are out of the protocol's scope (Chapter 19) | Behind the MCP Gateway and Tool Gateway (Chapters 19 and 22), never direct unrestricted production access |
| OpenTelemetry GenAI conventions | Emerging common vocabulary for model, agent, MCP, span, metric, and event telemetry [R19] | **Lifecycle:** the conventions are still in Development and may change, so map them behind an internal layer [R19]. **Privacy:** capturing full prompts and tool content puts personal data in telemetry. **Evidence:** a shared vocabulary does not guarantee every causal step was recorded | Instrumentation base plus organization-specific run, effect, and policy attributes (Chapter 24) |

## Where the industry is heading

1. **From chains to explicit state:** graph and workflow abstractions are replacing invisible prompt loops.
2. **From synchronous chat to sessions and tasks:** managed runtimes and A2A now model asynchronous, interruptible, long-running work.
3. **From bespoke plugins to protocols:** MCP standardizes tools and resources; A2A standardizes remote-agent interaction.
4. **From logs to trajectories:** framework traces and OpenTelemetry conventions increasingly capture handoffs, tools, tokens, and evaluation signals.
5. **From single-vendor demos to gateways:** enterprises need model, tool, policy, identity, and telemetry gateways to retain control across frameworks.
6. **From prompt safeguards to capability security:** OWASP’s agentic list ranks agent goal hijack, tool misuse, and identity and privilege abuse as its top three risks [R15].
7. **From “autonomy” to bounded agency:** public guidance recommends simple composable patterns and earning orchestration complexity only where measurable value justifies it [R27].

## A practical way to choose

Choose the smallest harness that expresses the agent behavior, the strongest durable engine that matches the run’s consequences, and enterprise-owned gateways for identity, policy, tools, models, telemetry, and artifacts. Do not force one framework to own all three layers.

## A baseline stack by concern—not a mandate

Each row names typical choices for one concern and the criteria that should decide among them.

| **Concern** | **Typical choices** | **Selection criteria** |
| --- | --- | --- |
| Durable workflow | Temporal, DBOS, Restate, cloud durable functions/state machines | Replay/versioning, signals/timers, child workflows, visibility, language/runtime fit, operations |
| Agent graph/harness | LangGraph, OpenAI Agents SDK, Claude Agent SDK/Managed Agents, Microsoft Agent Framework, Google ADK, Pydantic AI, LlamaIndex | Typed state, interrupts, tool ergonomics, model portability, trace quality, escape hatches |
| Events/queues | Kafka/Pulsar, cloud pub-sub/queues, NATS | Ordering, retention, throughput, replay, tenancy, ecosystem, residency |
| Identity | Enterprise identity provider for users, workloads, and agents, for example Microsoft Entra ID with Workload ID and Agent ID [R64] | One identity per human, workload, and agent; short-lived tokens; conditional access; lifecycle and access reviews |
| Authorization (policy decision point) | Cedar or Amazon Verified Permissions for analyzable role and attribute rules [R59][R60]; a Zanzibar-style relationship service such as OpenFGA for per-object sharing [R61][R62]; OPA/Rego for platform and infrastructure policy [R63] | Rule types to express, formal analysis and testing, decision logs for replay, latency at the gateways, tenant model (Chapter 21) |
| Workload identity | SPIFFE/SPIRE, cloud workload federation, service mesh identity | Short-lived credentials, federation, attestation, sender/audience binding |
| Operational state | PostgreSQL-compatible relational store | Transactions, RLS, JSON support, operational maturity, backup/restore |
| Artifacts | Versioned object storage | Immutability, retention lock, encryption, signed access, regionality |
| Retrieval | Search engine + vector index + optional graph | ACL correctness, freshness, hybrid search, lineage, deletion, scale |
| Sandboxing | Ephemeral containers or microVMs with egress proxy | Isolation strength, startup latency, observability, policy integration |
| Telemetry/evals | OpenTelemetry + trace/metric backend + evaluation service | Portability, privacy controls, async trace linking, dataset/experiment workflow |

# Appendix E — What This Architecture Means for Research

## Why this appendix exists

The chapters argue from production failures; this appendix connects that
argument to published research. It has two readers. **Practitioners** use it to
read an agent paper or benchmark result correctly: to see what the result
actually established, and what it does *not* license an enterprise to assume.
A benchmark score, for example, says how a model performed in that test
environment, not whether an agent built on it can safely change a mortgage
record. **Researchers and benchmark designers** use it the other way round: to
see which properties an enterprise deployment depends on that current
evaluations rarely measure, such as policy compliance across repeated runs,
recovery after a failed step, or cost per verified outcome.

Each row below names one well-known result, states what it showed in the
authors' own terms, and draws the architectural implication this book takes
from it. The implications are the book's interpretation, not claims made by
the cited authors.

## What researchers and benchmark designers should test

| **Research or benchmark** | **What it established** | **Architectural implication** |
| --- | --- | --- |
| ReAct [R01] | Interleaving reasoning and environment actions improves many interactive tasks compared with reasoning or acting alone | Agent loops need real tool feedback and explicit stop limits; reasoning text does not supply transaction safety |
| AutoGen [R49] | Multi-agent conversation is a flexible composition mechanism for tools, models, and humans | Conversation is useful as an application abstraction, but enterprise ownership and durable task semantics must be added |
| AgentBench [R50] | Across eight interactive environments, agent performance differs widely between models; weak long-term reasoning, decision-making, and instruction following are the main failure causes | Evaluate in environment-specific tasks with real tool and state constraints |
| GAIA [R51] | Questions that are simple for humans but require reasoning, multimodality, web browsing, and tool use expose a large gap between humans and tool-equipped models | “Easy for a human” is not an adequate release assumption; test cross-capability, long-tail tasks |
| SWE-bench [R52] | Real repository issues with executable tests give grounded evaluation for coding agents | Prefer domains with objective environmental feedback; still require human review for broader requirements and security |
| τ-bench [R53] | Tool agents must interact with users while following domain rules, and they behave inconsistently across repeated trials | Test multi-turn policy compliance and repeated-run consistency, not only final-answer quality |
| AgentDojo [R54] | Tool-integrated agents can be evaluated jointly for task utility and prompt-injection security | Security evaluations must measure both attack resistance and retained task utility |

The common lesson is not that “more agents” is state of the art. It is that useful agent behavior comes from environment grounding, specialized interfaces, explicit state, executable verification, and bounded iteration. This book's working hypothesis, not a cited result, is that long trajectories compound even modest per-step error; architecture should therefore create shorter verified segments and durable recovery points, and measure reliability by task horizon.

## Open questions this architecture raises

These are research questions the book's design depends on but cannot settle
from current evidence. Each is stated as a measurable question, with the
chapter that relies on the answer.

| **Question** | **Why it matters to the architecture** | **Chapters** |
| --- | --- | --- |
| How does task success decay with the number of steps, and how much do verified checkpoints slow that decay? | Decides how long a bounded agent step may be before the workflow must verify and checkpoint | 10, 12, 15 |
| How consistent is an agent's policy compliance across repeated runs of the same task? | A control that holds on one run in five is not a control; release gates need a repeated-run measure | 13, 25 |
| How much task utility does each injection defense cost? | Security that destroys usefulness gets switched off; defenses must be measured on both axes | 20, 23 |
| How well do model-based judges agree with expert reviewers, by task and risk tier? | Decides where a judge may gate a release and where a human must decide | 13, 25 |
| When does a multi-agent design beat the strongest single agent on the same budget? | Multi-agent topology adds cost and coordination failure; it needs a measured advantage | 16, 18 |
| What is the cost per verified successful outcome, not per token, across model routes? | Routing and capacity decisions optimize the wrong quantity without it | 28 |

A result that answers one of these questions on realistic, regulated
workloads would change a default in this book; the chapters name which one.

# Appendix F — Known Limits and the Controls That Contain Them

## Known limits—and how to contain them

1. Prompt injection is not assumed solved. Mitigation: treat retrieved content as untrusted, remove ambient credentials, minimize capabilities, and enforce identity, policy, schema, sandbox, egress, and effect controls outside the model.
2. Delegated authorization is not universally interoperable end to end. Mitigation: preserve a platform-owned subject+actor+purpose model, narrow authority at every hop, bind token audience and resource, and reject peers that cannot provide required proof.
3. Semantic idempotency is domain specific. Mitigation: define domain-owned logical effect keys, reject argument-hash conflicts, record receipts, and reconcile ambiguous outcomes against the authoritative downstream system.
4. Exact model replay cannot be guaranteed. Mitigation: pin release graphs, retain inputs and outputs by reference and hash, replay deterministic workflow history, and evaluate replacements against immutable cases.
5. Long-horizon reliability requires empirical control. Mitigation: segment trajectories into bounded verified steps, detect no progress and plan drift, simulate correlated failures, and gate releases on repeated-run and tail-risk evidence.
6. Multi-agent quality is not inferred from component scores. Mitigation: benchmark against the strongest single-agent baseline and test ownership, delegation, aggregation, cancellation, compromised peers, and policy interaction end to end.
7. Memory governance requires platform-owned lifecycle controls. Mitigation: enforce scope, lawful basis or policy, provenance, confidence, TTL, correction, deletion propagation, legal hold, residency, and derived-index lineage.
8. Protocol connectivity does not establish trust. Mitigation: terminate MCP and A2A at governed gateways, verify publishers and signed artifacts, apply local authorization and quotas, scan adopted artifacts, and require conformance evidence.
9. Model explanations are not evidence. Mitigation: separate rationale from authoritative evidence and require source revisions, policy decisions, typed plans, deterministic calculations, and effect receipts for material claims.
10. Online evaluation requires controlled statistical and ethical safeguards. Mitigation: use immutable datasets, leakage checks, deterministic gate precedence, calibrated scorer ensembles, confidence intervals, risk-weighted slices, and human review.
11. Cross-vendor portability is intentionally bounded. Mitigation: keep provider-neutral run, task, tool, effect, approval, and artifact contracts; isolate vendor adapters; and prove fallback compatibility through exact-release evaluation.
12. Human accountability is implemented as an operating model, not a button. Mitigation: define roles and separation of duties, accessible evidence-first previews, training, review-time budgets, fatigue metrics, recourse, and explicit exception ownership.

# Appendix G — A Practical Roadmap for Enterprise Adoption

## A staged path to enterprise adoption

| **Phase** | **Build** | **Exit criteria** |
| --- | --- | --- |
| 0 — Foundations | Use-case/risk inventory, identity model, data classification, agent/tool registry, model and tool gateways, baseline OTel traces | Every pilot has owner, purpose, boundaries, data map, rollback, and measurable acceptance criteria |
| 1 — Read-only copilots | Governed retrieval, typed outputs, no autonomous writes, offline evals, red-team tests, cost/latency SLOs | ACL correctness, trace completeness, quality threshold, zero cross-tenant leakage in tests |
| 2 — Draft and reversible actions | Durable workflows, idempotency, effect ledger, previews, human approval, sandboxed tools | Crash/replay/fault tests pass; duplicate-effect rate target met; operator console usable |
| 3 — Bounded autonomous workflows | Risk-based approvals, event-driven resume, compensation, model routing, canaries, continuous eval | Stable success/safety/cost SLOs over representative volume; audited exception process |
| 4 — Cross-agent ecosystem | A2A gateway, signed manifests, cross-team contracts, delegated token exchange, federated traces | Interoperability, cancellation, identity, schema, failure, and audit contract tests pass |
| 5 — Continuous optimization | Failure mining, incremental execution, model/tool substitution, automated rollback, governance reporting | Improvements are evidence-driven; no self-modifying production behavior outside release controls |

### The minimum bar before an agent can write

Before an agent can mutate an enterprise system, require all of the following:

* Named business, engineering, security, and operational owners.
* Version-pinned manifest, prompt/Skill bundle, workflow, model route, policy, tool schemas, and runtime image.
* Subject+actor authorization and a least-privilege capability envelope.
* Durable execution with tested crash recovery, cancellation, and code-version compatibility.
* Tool idempotency/effect receipt or an explicit compensation/reconciliation design.
* Data classification, tenant isolation, DLP, secret brokering, and sandbox/egress controls.
* Risk-based approvals and an operator console for pause, inspect, override, and compensate.
* End-to-end trace, cost accounting, immutable audit evidence, and retention policy.
* Unit, contract, workflow fault, simulation, adversarial, regression, and staging E2E tests.
* Canary, kill switch, rollback, incident runbook, and SLOs for quality, reliability, safety, latency, and cost.

# Appendix H — Companion Implementation Guide: Harborlight Mortgage

This appendix explains how to run and verify the book's companion code.

## Versions used in this guide

* Python 3.13
* OpenAI Agents SDK 0.22.2
* OpenAI Python SDK 3.13.0 (the exact offline-profile pin; the pinned Agents SDK declares the compatible `openai` 3.x range)
* MLflow 3.15.2 (the pinned example baseline [R21]; re-verify current releases before implementation)
* Pydantic 2

The examples deliberately pin versions so a reader can reproduce behavior.

## Run the examples, tests, and demo

From the repository root:

1. `make examples-run` executes every registered example's tests.
2. `.venv-examples/bin/python -m pytest tests/mortgage_case -q` runs the mortgage-case tests.
3. `.venv-examples/bin/python -m mortgage_case --chapter 3 --scenario happy_path --offline --json` runs the deterministic demo through checkpoint C03.

The direct OpenAI Python SDK adapter and OpenAI Agents SDK adapter are optional
provider integrations behind provider-neutral contracts. The default offline path
uses the scripted Agents SDK model and a synthetic gateway, while the MLflow
example uses a local SQLite tracking URI. No command in the offline profile
requires credentials or a network connection.

## What is included

* `mortgage_case/domain/` — synthetic case, evidence, proposal, and money contracts
* `mortgage_case/platform/` — provider-neutral runtime and gateway boundaries
* `mortgage_case/stages/` — cumulative C01–C03 checkpoint façades
* `mortgage_case/adapters/openai_responses.py` — direct OpenAI Python SDK Responses adapter
* `mortgage_case/adapters/openai_agents.py` — OpenAI Agents SDK 0.22.2 adapter
* `examples/_harness/scripted_model.py` — offline implementation of the Agents SDK model interface
* `examples/observability/mortgage_agents_mlflow.py` — real Agents SDK run with MLflow tracing
* `examples/observability/mlflow_evaluation.py` — `mlflow.genai.evaluate` dataset/scorer orchestration
* `code-gap.md` — chapter-by-chapter C04–C28 implementation roadmap

The live provider path still requires credentials and should be treated as an
explicit integration test, not as evidence supplied by the offline suite. As
Chapter 8 notes, the book's Skill and Skill Pack are platform-owned packaging
patterns, not aliases for A2A AgentSkill metadata or Skills over MCP.

## Rebuild and verify

Run `.venv-examples/bin/python -m compileall -q mortgage_case examples tests`, then repeat the three commands above. The repository README records the companion code's correction history.

# Appendix I — References

<!-- Generated at assembly from config/references.json by tools/assemble_manuscript.py. Edit the registry, not this section. -->

# Appendix J — Glossary

Chapter 1 § The vocabulary this book assumes introduces the core terms; this glossary defines them and the rest of the book's working vocabulary. Records are listed with their fields in Appendix C.

| **Term** | **Definition** | **Chapter** |
| --- | --- | --- |
| A2A Gateway | Control point that decides whether an external agent may receive or return a task, and terminates the A2A protocol; internal delegation belongs to the Task Service | 19 |
| Acceptance criteria | Executable checks over authoritative state that decide whether a run succeeded; evaluated by code, never asserted by the model | 2 |
| Acceptance engine | The only component that may mark a candidate, plan node, or answer as accepted; runs deterministic checks first and calibrated judges only where a criterion cannot be computed | 13 |
| AcceptanceDecision | The acceptance engine's record: accepted, rejected with typed defects, or escalated, with evaluator type and evidence per criterion | 13 |
| Activity | A unit of I/O, such as a model or tool call, that a durable workflow schedules, retries, and records | 15 |
| Actor | The workload identity performing an action on behalf of a subject | 21 |
| AgentRuntime | Provider-neutral interface that executes one bounded agent step: `AgentRuntime.execute(AgentStepRequest) → AgentStepResult` | 3 |
| AgentSpec | The versioned definition of an agent: instructions, required Skills, topology, and owner | 4 |
| AgentStepRequest / AgentStepResult | The platform contract into and out of one agent step; the result's status is `completed`, `needs_input`, `proposed_action`, or `failed` | 3 |
| API Gateway | Control point that decides whether a caller is admitted to the platform at all | 1 |
| Approval | A human decision bound to one exact proposal and its expiry (ApprovalRequest, ApprovalDecision, Approval Service); it never replaces reauthorization at commit | 14 |
| Artifact | Immutable output or evidence object with schema, hash, classification, and provenance | 4 |
| Audience binding | Restricting a credential to one intended recipient so it cannot be replayed against another service | 21 |
| Authorization | The policy decision over subject, actor, purpose, resource, and action; distinct from a human approval | 21 |
| Canary | Exposing a change to a bounded cohort of real traffic with explicit stop conditions before full release | 27 |
| Candidate digest | The hash over a proposed knowledge release's content, its pinned base, the live release it expects to replace, and the resolver version; an approval binds to it as an ApprovalDecision binds to a proposal hash (14), and any edit invalidates it | 5 |
| Capability envelope | The platform-computed maximum scope a run or child task may use (actions, resources, purpose, data, region, risk, time, spend, delegation), identified by its `grant_id`; a child's envelope is a provable subset of its parent's | 21 |
| Causal run trace | One run's linked spans across workflow, model, tools, approvals, and effects; links to the authoritative records and replaces none | 24 |
| Change class | The classification of a proposed change; with the use-case tier it sets review depth | 25 |
| ChangeBundle | A proposed change to versioned objects; it becomes a ReleaseManifest only when promoted | 27 |
| Child task | Durable delegated work with one owner, carried by a TaskEnvelope and executed as a child workflow | 18 |
| Compensation | A new, authorized business action that reverses a committed effect; it never erases the original receipt | 22 |
| Compliance knowledge | The requirements an organization takes from regulations, standards, contracts, and internal policies, the obligations and controls derived from them, the constraints the runtime enforces, and the definitions they depend on, each with provenance to its authoritative source; managed as a versioned, released asset | 5 |
| ContextManifest | Record of exactly what one agent step's context contained and why: ordered segments with source, trust tier, authorization decision, and token allocation | 6 |
| Control | The mechanism by which an obligation is discharged or its breach prevented: an enforced rule, a check, an approval, or a review. Controls execute at control points (1); a guardrail is a detector, not a control | 5 |
| Credential lease | A short-lived, audience-bound credential minted after authorization for one downstream call; the proof that accompanies a capability envelope's scope | 21 |
| Deterministic shell | The six gates around a model proposal: propose, validate, authorize (including any human approval), commit, verify, accept | 2 |
| Downscoping | Deriving a narrower credential from a broader one so delegated work never exceeds its delegator's authority | 21 |
| Effect | An externally observable mutation with durable intent, state, receipt, and reconciliation | 22 |
| Effect ledger | The Effect Service's durable record of every external change attempted, its idempotency key, and its confirmed outcome | 22 |
| Effect risk class (R0–R4) | Classification of one tool effect, from R0 pure transform to R4 irreversible, privileged, or financial action that an agent may only propose | 22 |
| Enforced rule | A typed rule from a pinned knowledge release that a control point evaluates before an effect, with true, false, or unknown results; unknown refuses. Distinct from a guardrail, which only detects | 5 |
| EnvironmentBinding | Says which ReleaseManifest new runs receive for a tenant, use case, environment, and region; rollback changes it. A knowledge stream's pointer is a KnowledgeBinding | 27 |
| EvaluationResult | One evaluator's score for one case and attempt, with evaluator type and version | 25 |
| EvidenceRef | Source revision or artifact reference with hash, provenance, and authorization lineage | 6 |
| Federated task | A child task that crosses a trust boundary to an external agent through the A2A Gateway | 19 |
| Global control tier | The deployment tier that publishes signed, immutable definitions and holds no run state | 4 |
| Guardrail | A probabilistic detector, such as an input or output check; its finding feeds a policy point and never decides authorization | 20 |
| Handoff | An accountable transfer of task or interaction ownership that takes effect only when the recipient acknowledges; a framework handoff moves control, not accountability | 11 |
| Idempotency key | A stable identifier the platform derives from tenant, run, and logical effect and binds to an intent hash; passed to a downstream system that supports one so it recognizes a repeated request as the same request. The model never chooses it | 22 |
| InterventionRequired | Run, task, or effect state used when correctness cannot be established automatically; it opens an intervention task | 15, 22 |
| Intervention task | A typed request for human help with an uncertain run; its response is an input to the run and never approves an effect | 14 |
| Knowledge graph | The governed, versioned instance of an ontology: typed nodes and edges with provenance, scope, and permissions, frozen into a release and traversed within bounds | 5 |
| Knowledge registry | Control-plane store of ontology versions, knowledge objects, release manifests, and the live pointer (KnowledgeBinding) per stream, tenant, environment, and region; the Knowledge Hub is its read-only runtime surface | 5 |
| Knowledge release | The immutable, content-addressed set of knowledge objects, ontology version, and source revisions that the registry publisher activated after a complete gate record and an independent approval; what a run pins | 5 |
| KnowledgeArtifact | The Knowledge Hub's record of a governed artifact (document, chunk, extracted field, or rule) with its source digest and region, versions, verdicts, owner, and scope | 5 |
| Layer | A deployable unit of the architecture (for example, Model access or Durable execution); layers serve the planes | 4 |
| LLM Gateway | Control point that decides which model may answer under which data policy, and enforces model routing, privacy, budgets, and evidence | 4 |
| MCP Gateway | Control point that terminates MCP and decides whether an external server and tool are trusted and eligible | 19 |
| Obligation | A duty derived from a requirement, with a subject, a scope, a modality, and an effective period. A PolicyDecision's obligations (21) and a run's obligations (13) are obligations bound to one action or one run | 5 |
| Ontology | The schema of a knowledge graph: the entity kinds, relationships, properties, constraints, and vocabulary its objects must conform to; versioned separately from the instances it governs | 5 |
| Plan IR | Typed representation of proposed work that is compiled and checked before any node is scheduled | 12 |
| Plane | An ownership domain; the seven planes give every authoritative record one owner | 4 |
| Provenance | Where content came from, under what authority it was retrieved, and how far it may be trusted | 5, 6 |
| Purpose | Why an action is requested; carried with subject and actor so a valid identity cannot be reused for an unrelated operation | 21 |
| Regional execution cell | The regional unit that holds a run's control, workflow, workers, gateways, context, and effect ledger | 4 |
| Registry publisher | The knowledge registry's single service identity that merges approved content, stores and verifies a release, and moves the live pointer; no human or assistant holds it | 5 |
| Release gate | The decision whether a candidate may be promoted, recorded as a ReleaseGateDecision | 25 |
| ReleaseManifest | The immutable, signed graph of every behavior-relevant version in a release; fixes the eligible Skill and pack set | 27 |
| Requirement | A statement in an authoritative source that the organization must satisfy; the source, span, and digest are its provenance | 5 |
| Run | One admitted unit of work with a RunManifest; it contains a workflow execution whose nodes run activities, agent steps, or child tasks | 4, 15 |
| RunManifest | Per-run record written once at admission: the ReleaseManifest digest plus what was resolved for this run | 4 |
| Skill | Versioned capability package: interface, instructions, eligible tools, knowledge, policy, risk ceiling, evaluation, owner, digest | 8 |
| Skill Pack | Certified, co-released set of compatible Skills with shared policy and evaluations; installing one grants nothing | 9 |
| Subject | The principal whose delegated authority initiates a protected action | 21 |
| TaskEnvelope | The contract every child task carries, in eight field groups | 18 |
| Tenant extension | A tenant's additions to a shared base knowledge release (stricter rules, extra kinds, relationships, or terms), versioned and resolved against a pinned base; never a fork, and never a removal or redefinition of a base element | 5 |
| Tool Gateway | Control point that decides whether an effect may happen for this subject and dispatches it as one logical effect under the effect ledger, so a retry cannot repeat it; it does not promise cross-system exactly-once delivery; protocol-agnostic | 2, 22 |
| Trajectory | A run's ordered decisions viewed for evaluation | 25 |
| Trust tier | The rank of a context segment's origin, from tier 1 system instructions to tier 4 retrieved data that can never direct behavior | 6 |
| Unknown | Effect state when a mutation may have reached the downstream system and the platform holds neither a receipt nor proof of absence; it blocks retry and dependent work | 22 |
| Use-case tier (T0–T4) | Classification of a whole use case that sets governance and release depth; never lower than its most dangerous eligible effect requires | 26 |
| ValidationReport | The release evidence for one candidate: evaluation comparisons, other test results, and slice regressions | 25 |
| Verification status | A claim's or field's verdict against its pinned source: supported, contradicted, or insufficient evidence. It shows the source says it, not that it is true; corroboration by an independent source is recorded separately | 5 |
| Workflow execution | The durable, replayable history that owns a run's state; one active execution per run generation | 15 |

# Index

[[INDEX]]
