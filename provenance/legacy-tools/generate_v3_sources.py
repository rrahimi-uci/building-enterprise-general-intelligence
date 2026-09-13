from pathlib import Path
import json

OUT = Path('/data/v3_sources')
OUT.mkdir(exist_ok=True)

parts = [
    ('I', 'Foundations', 'Establish the deterministic shell, typed tools, and portable agent runtime.'),
    ('II', 'Enterprise Reference Architecture', 'Place agent behavior inside explicit control, data, integration, and governance planes.'),
    ('III', 'Agentic Developer Platform & SDK', 'Give teams a paved road from local development to governed production operation.'),
    ('IV', 'Patterns', 'Select the smallest architecture pattern that resolves the actual uncertainty.'),
    ('V', 'Anti-Patterns', 'Recognize recurring system shapes that hide unsafe authority, fragile state, or weak evidence.'),
    ('VI', 'Multi-Agent & Platform Integration', 'Coordinate specialists and cross-boundary systems with typed, governed protocols.'),
    ('VII', 'LLM Gateway', 'Control model access, routing, policy, economics, and provider portability.'),
    ('VIII', 'Security & Guardrails', 'Apply defense in depth across content, identity, tools, code, data, and supply chain.'),
    ('IX', 'Observability & Evaluation', 'Measure trajectories, outcomes, invariants, reliability, and cost.'),
    ('X', 'Continuous Learning', 'Convert production evidence into validated, approved, reversible improvements.'),
    ('XI', 'Governance', 'Define decision rights, risk tiers, evidence, exceptions, and accountability.'),
    ('XII', 'Deployment & Production Operations', 'Release, scale, recover, and optimize verified outcomes.'),
]

chapters = [
    (1,'From an LLM Call to a Production System','old','01'),
    (2,'Tools, Structured Outputs, and the Deterministic Shell','old','02'),
    (3,'Agent Runtime and Framework Abstraction','old','03'),
    (4,'Enterprise Agentic AI Reference Architecture','new','04-reference-architecture.md'),
    (5,'Platform Boundaries, APIs, and Data Models','old','20'),
    (6,'Agentic Developer Platform and SDK','new','06-developer-platform.md'),
    (7,'Developer Experience, Testing, and Delivery Lifecycle','new','07-developer-experience.md'),
    (8,'Skills as Versioned Capabilities','old','10'),
    (9,'Skill Packs and Domain Platforms','old','11'),
    (10,'ReAct: Bounded Reason–Act–Observe Loops','old','04'),
    (11,'Routing, Triage, and Handoffs','old','05'),
    (12,'Planning and Plan–Execute','old','06'),
    (13,'Reflection and Evaluator–Optimizer','old','07'),
    (14,'Human-in-the-Loop','old','08'),
    (15,'Long-Running and Durable Agents','old','09'),
    (16,'Enterprise Pattern Catalog','new','16-pattern-catalog.md'),
    (17,'Enterprise Anti-Pattern Catalog','new','17-anti-pattern-catalog.md'),
    (18,'Supervisor/Worker and Multi-Agent Collaboration','old','12'),
    (19,'MCP, A2A, and External Integration','old','13'),
    (20,'LLM Gateway and Model Control Plane','new','20-llm-gateway.md'),
    (21,'Agentic AI Security and Guardrails Architecture','new','21-security-guardrails.md'),
    (22,'Context Engineering, RAG, Memory, and State','old','14'),
    (23,'Identity, RBAC/ABAC, and Delegated Authorization','old','15'),
    (24,'Tool Security, Effects, Idempotency, and Approval','old','16'),
    (25,'Sandboxing, Egress, Data Security, and Governance','old','17'),
    (26,'Observability and Tracing with MLflow','old','18'),
    (27,'Evaluation, Testing, and Debugging with MLflow','old','19'),
    (28,'Continuous Learning and Improvement Architecture','new','28-continuous-learning.md'),
    (29,'Governance, Risk, and Operating Model','new','29-governance.md'),
    (30,'Deployment, Versioning, CI/CD, and Recovery','old','21'),
    (31,'Cost, Latency, Capacity, and Reliability Optimization','old','22'),
]

part_chapters = {
    'I':[1,2,3], 'II':[4,5], 'III':[6,7,8,9], 'IV':[10,11,12,13,14,15,16],
    'V':[17], 'VI':[18,19], 'VII':[20], 'VIII':[21,22,23,24,25],
    'IX':[26,27], 'X':[28], 'XI':[29], 'XII':[30,31]
}

front = '''# How to use this guide

This is an architecture reference, developer-platform blueprint, pattern catalog, security model, and production operating guide in one coherent system. Read the executive map first, then follow the lane that matches your decision. Each technical chapter moves from problem and boundaries to architecture, implementation, failure modes, metrics, trade-offs, and review questions.

| **Reader** | **Primary path** | **Decision supported** |
| --- | --- | --- |
| Executive and product leader | Parts II, III, VII, VIII, X, XI | Investment, operating model, risk appetite, platform scope, and outcome governance |
| Enterprise / solution architect | Parts I–VIII, X–XII | Boundaries, contracts, topology, integration, security, and lifecycle |
| Platform engineer | Parts II, III, VI–XII | Reusable control planes, SDKs, gateways, telemetry, release, and operations |
| Application developer | Parts I, III–VI, IX–X | Agent design, tools, Skills, tests, debugging, and improvement |
| Security / risk / privacy | Parts VII, VIII, XI, Appendices F, M–O | Threat controls, evidence, approvals, exceptions, and assurance |
| SRE / operations | Parts IX, X, XII, Appendices B and O | SLOs, incident response, recovery, capacity, and verified-success economics |

## Architecture at a glance

[[DIAGRAM:book-map|Figure 0-1 — Guide map from foundations to production operations]]

| **Flow** | **Question answered** |
| --- | --- |
| Foundations → Reference Architecture | What is an agentic system, and where does probabilistic reasoning stop? |
| Developer Platform & SDK | Which capabilities become reusable paved-road services? |
| Patterns → Anti-Patterns | Which system shape fits, and which recurring failure shape must be removed? |
| Multi-Agent & Integration → LLM Gateway | How do agents, tools, protocols, and models cross boundaries safely? |
| Security → Observability → Learning | How is behavior constrained, measured, diagnosed, and improved? |
| Governance → Production Operations | Who approves change, what evidence is required, and how is the system released and recovered? |

## The reference-guide contract

1. **Probabilistic components propose; deterministic components authorize and commit.**
2. **Every run is pinned to immutable versions and a typed context manifest.**
3. **Every side effect has one owner, an idempotency key, an effect record, and an acceptance rule.**
4. **Every trust-boundary crossing revalidates identity, authority, content, and data policy.**
5. **Every material change is evaluated, approved at the right risk tier, canaried, observable, and reversible.**
6. **Every production failure can become an authorized regression case and improvement candidate.**

## Hierarchical table of contents

[[TOC]]

## Visual language

- **Navy boxes** represent deterministic enterprise control planes.
- **Cyan boxes** represent probabilistic or model-mediated behavior.
- **Teal boxes** represent data, context, memory, and evaluation services.
- **Amber boundaries** represent approval, policy, or external trust crossings.
- Arrows show responsibility or evidence flow—not decorative connectivity.
'''

ref_arch = '''# 04 — Enterprise Agentic AI Reference Architecture

## What this chapter delivers

A cohesive enterprise architecture that places agent behavior inside explicit experience, runtime, control, knowledge, integration, security, and operations planes. The model is framework-neutral: an application may use an agent SDK, a graph framework, direct model APIs, or deterministic workflow code, while the enterprise controls remain stable.

## Architecture principles

- Treat the agent as one decision component inside a larger sociotechnical system—not the system of record.
- Separate **intent**, **plan**, **authority**, **execution**, **effect**, **acceptance**, and **learning**.
- Keep policy, identity, credentials, durable state, approvals, effect reconciliation, and release promotion outside the model.
- Place reusable controls on the platform path so application teams receive secure defaults rather than optional guidance.
- Preserve portability through typed platform contracts and adapters instead of exposing provider-native objects throughout applications.

## Layered reference architecture

[[DIAGRAM:reference-architecture|Figure 4-1 — Enterprise agentic AI layered reference architecture]]

| **Plane** | **Responsibilities** | **Authoritative records** | **Failure boundary** |
| --- | --- | --- | --- |
| Experience and channels | User intent, conversation UX, review, accessibility, recourse | Request and interaction record | Never treats UI state as approval or workflow truth |
| Agent application | Domain instructions, task decomposition, specialist composition, response assembly | Application release manifest | Cannot mint authority or directly commit protected effects |
| Runtime and orchestration | Run graph, deadlines, budgets, cancellation, retries, checkpoints, joins | Run and TaskEnvelope state | Owns execution state; model transcript is supporting evidence |
| Context, RAG, memory, and Skills | Source selection, evidence projection, memory eligibility, versioned capability packaging | ContextManifest, knowledge snapshot, MemoryRecord, Skill manifest | Untrusted content never becomes instruction or authority |
| Gateways and integration | LLM routing, tool façades, MCP/A2A mediation, event/API normalization | Routing decision, ToolCall, EffectRecord, protocol envelope | Revalidates identity, scope, schema, and policy at every boundary |
| Security and governance | Identity, least privilege, policy, guardrails, approvals, DLP, audit, exceptions | PolicyDecision, CapabilityEnvelope, ApprovalGrant, evidence ledger | Fail closed for protected action; preserve explicit unknown effect state |
| Evaluation and operations | Tracing, evaluation, SLOs, incidents, release, capacity, cost, continuous improvement | Trace graph, EvaluationResult, incident, ChangeBundle, ReleaseManifest | Monitoring cannot silently promote behavior-changing change |

## End-to-end responsibility flow

[[DIAGRAM:request-sequence|Figure 4-2 — Request-to-verified-outcome responsibility sequence]]

1. The API or channel authenticates the initiating subject and creates a request with tenant, purpose, risk, and deadline.
2. The runtime creates a run pinned to application, prompt, Skill, workflow, policy, model-route, tool, and knowledge versions.
3. Context services build a typed ContextManifest from authorized sources; retrieved content remains untrusted data.
4. The agent proposes a typed decision or tool call. Policy and tool services validate schema, actor, subject, purpose, scope, budget, and current resource version.
5. Protected changes become an ActionProposal and require an ApprovalGrant bound to the exact logical effect.
6. The tool façade dispatches once, records the effect, reconciles ambiguous outcomes, and returns evidence.
7. A deterministic acceptance function decides whether the business outcome is accepted, blocked, needs input, failed, or has unknown effect.
8. Trace, outcome, cost, safety, human, and business signals feed evaluation and controlled improvement.

## Systems of record

| **Concern** | **System of record** | **What the model may do** | **What the model may not do** |
| --- | --- | --- | --- |
| Workflow | Durable workflow/run service | Propose next semantic step | Invent terminal state or retry history |
| Authorization | Identity and policy decision point | Explain requested scope | Grant itself or another agent more authority |
| Business truth | Domain system | Read authorized projections | Replace authoritative state with a summary |
| Effects | Tool/effect service plus downstream receipt | Propose arguments | Assert that a side effect completed |
| Approval | Proposal and approval service | Generate rationale and preview | Reuse a Boolean or stale conversational approval |
| Knowledge | Governed source and snapshot catalog | Select and synthesize evidence | Treat vector similarity as truth or freshness |
| Learning | Evaluation, dataset, and release services | Recommend a candidate | Self-certify or self-deploy behavioral changes |

## Trust boundaries and tenancy

Every request crosses at least five boundaries: channel to platform, application to model, model to context, model to tool, and platform to external systems. Multi-agent and MCP/A2A deployments add workload-to-workload boundaries. At each crossing validate both the initiating subject and acting workload; enforce tenant, purpose, resource, action, region, and spend constraints; classify and minimize data; and create attributable audit events.

## Executive architecture decisions

- **Centralize** identity, policy, gateways, tool contracts, telemetry schemas, evaluation infrastructure, release evidence, and incident controls.
- **Federate** domain prompts, accepted outcomes, tools, Skills, knowledge, evaluation cases, and business SLOs to accountable domain owners.
- **Standardize** interfaces and evidence; do not standardize every internal framework implementation.
- **Fund** the developer platform as a product with adoption, reliability, security, and developer-experience measures.

## Production checklist

- [ ] Authoritative owners are named for workflow, policy, context, memory, tools, effects, acceptance, telemetry, and release.
- [ ] Every run and artifact is version-pinned and tenant-scoped.
- [ ] Model, tool, MCP, A2A, and external-system boundaries have explicit threat and failure models.
- [ ] Unknown side-effect outcomes reconcile before retry or compensation.
- [ ] Acceptance is executable and independent from the model's claim of completion.
- [ ] Evaluation and rollback evidence exist before production promotion.
'''

platform = '''# 06 — Agentic Developer Platform and SDK

## Platform promise

The developer platform is the reusable architecture that lets teams build differentiated agents without repeatedly rebuilding identity, policy, tool safety, tracing, evaluation, durable execution, and delivery infrastructure. It is a **paved road**, not a mandatory monolith: application teams use stable contracts and may replace internal frameworks through adapters.

## Capability stack

[[DIAGRAM:developer-platform|Figure 6-1 — Agentic developer platform and SDK capability stack]]

| **Capability** | **Platform responsibility** | **Application responsibility** |
| --- | --- | --- |
| Agent Runtime | Run context, budgets, typed outputs, interruption, cancellation, framework adapter | Domain instructions, accepted outcome, specialist roles |
| Workflow / Orchestration | Durable state, timers, retries, joins, compensation, replay | Domain workflow graph and business deadlines |
| Tool SDK | Schemas, auth context, idempotency, effect protocol, test doubles, telemetry | Domain operation, validation, compensation semantics |
| MCP Integration | Server registry, trust policy, discovery cache, gateway, compatibility tests | Approved server/tool selection and domain interpretation |
| Agent-to-Agent Communication | Task/artifact envelopes, identity, delegation, deadlines, cancellation, audit | Collaboration topology and acceptance of child results |
| Context / RAG | Source adapters, ACL filtering, snapshot/provenance, ranking hooks, context budgets | Domain sources, retrieval policy, evidence requirements |
| Memory | Eligibility, scope, TTL, provenance, correction/deletion, encryption | Memory purpose, schema, confidence, business ownership |
| Skills | Manifest, versioning, dependency resolution, signing, distribution, tests | Capability logic, knowledge, examples, acceptance suite |
| Identity & Permissions | Subject/workload identity, policy decision/enforcement, short-lived credentials | Declared permissions and resource scopes |
| Guardrails | Input/output classifiers, prompt-injection controls, DLP, action policy | Domain rules, risk labels, safe response and escalation paths |
| LLM Gateway | Provider adapters, routing, budgets, filtering, cache, fallback, telemetry | Quality/cost/latency policy and approved model capabilities |
| Evaluation | Dataset registry, evaluator API, experiments, regression gates | Domain truth, rubrics, thresholds, human reviewers |
| Observability / Tracing | Unified run graph, schemas, sampling, redaction, correlation | Domain events and business outcome linkage |
| Durable Execution | Checkpoints, leases, deduplication, recovery, effect reconciliation | Domain state machine and compensation choices |
| Human-in-the-Loop | Proposal, preview, approval grant, queues, SLAs, recourse | Reviewer policy, domain evidence, decision rights |
| Deployment & Versioning | Packaging, manifests, environments, policy gates, canary, rollback | Application release, change notes, risk owner sign-off |

## Platform boundaries

A reusable platform should own cross-cutting invariants that must work the same across teams: identity propagation, policy enforcement, trace correlation, version pinning, effect safety, approval binding, evaluation contracts, secrets, tenancy, and release evidence. Application teams should own business intent, domain instructions, workflow meaning, data-source selection, tool semantics, acceptance rules, evaluation truth, and product experience.

Do not hide important semantics behind a convenient SDK. The SDK must make authority, risk, deadlines, evidence, side effects, and versions visible in types.

## Portable core contracts

| **Contract** | **Minimum fields** | **Why stable** |
| --- | --- | --- |
| AgentSpec | ID, version, instructions ref, model policy, tools, Skills, permissions, budgets | Separates application intent from a framework object |
| RunContext | tenant, subject, actor, purpose, risk, deadline, release manifest, trace | Gives every component attributable bounded context |
| TaskEnvelope | owner, goal, acceptance, inputs, authority, budget, deadline, cancellation | Makes delegation and multi-agent work explicit |
| ToolSpec / ToolCall | schema, risk, preconditions, idempotency, logical effect, telemetry | Supports safe tools across local, API, and MCP adapters |
| ContextManifest | source IDs, ACL decision, snapshot, provenance, ranking, token allocation | Makes context composition replayable and auditable |
| MemoryRecord | scope, purpose, source, confidence, TTL, correction/deletion lineage | Prevents ungoverned transcript accumulation |
| EvaluationResult | metric/version, target, score, evidence, evaluator, uncertainty | Avoids vendor-specific scores as release contracts |
| ReleaseManifest | all artifact versions, dependency lock, policy digest, evaluators, rollback target | Enables reproduction, comparison, and rollback |

## Framework and provider portability

[[DIAGRAM:portability|Figure 6-2 — Portable contracts with framework and provider adapters]]

Applications compile AgentSpec and TaskEnvelope into a provider or framework adapter. The platform receives normalized events, tool calls, context manifests, evaluation results, and effects. Provider-native features may be exposed through explicit capability negotiation—not leaked as ambient assumptions. Compatibility tests verify that each adapter preserves cancellation, tool schema behavior, tracing, approvals, streaming, error mapping, and usage accounting.

Use MCP for governed tool/context interoperability, A2A-style task and artifact envelopes for cross-agent responsibility, APIs for synchronous platform services, CloudEvents-compatible events for asynchronous facts, and gateways for policy-controlled boundary crossing. Standards reduce integration cost; they do not replace tenancy, authorization, versioning, or threat modeling.

## Developer lifecycle

[[DIAGRAM:developer-lifecycle|Figure 6-3 — Local-to-production agent lifecycle]]

1. **Create** from an approved template with an AgentSpec, risk tier, owner, and acceptance contract.
2. **Attach** typed tools, Skills, context sources, and memory policies through local adapters or sandboxed mocks.
3. **Configure** model policy, permissions, token/cost/deadline budgets, guardrails, and human-review points.
4. **Test** deterministic units, tool contracts, traces, simulations, golden datasets, adversarial cases, and failure injection.
5. **Evaluate** quality, faithfulness, retrieval, tool selection, trajectory, safety, latency, and verified-success cost.
6. **Package** immutable artifacts with dependency lock, SBOM, signatures, provenance, and ReleaseManifest.
7. **Promote** through development, test, staging, and production using policy gates and environment bindings.
8. **Observe** one correlated run graph from request to accepted outcome and effect.
9. **Improve** through trace mining, reviewed datasets, ChangeBundles, regression gates, canary, and rollback.

## SDK shape

PYTHON · implementation excerpt

```python
agent = platform.agent(
    spec="supplier_onboarding@3.2.0",
    model_policy="quality-balanced@7",
    permissions=["supplier:read", "screening:propose"],
    budgets={"tokens": 18_000, "usd": 0.45, "deadline_s": 90},
)
agent.attach_skill("supplier-screening@2.4.1")
agent.attach_tool(screen_supplier, risk="protected", effect="screening.create")
agent.use_context(source="supplier-policy", snapshot="approved-latest")
agent.use_memory(policy="tenant-user-preferences@3")

report = platform.test(agent).simulate("supplier-onboarding-regression")
platform.release(agent, require=["quality", "security", "cost", "rollback"]) 
```

The fluent API is convenience. The compiled AgentSpec, policy decisions, tool contracts, traces, and release evidence are the stable interfaces.

## Platform product metrics

Measure adoption, time to first evaluated agent, local-to-staging lead time, percentage of tools using the safe effect protocol, evaluation coverage, policy violations prevented, mean time to diagnose, rollback time, SDK/API compatibility, platform SLOs, developer satisfaction, and cost per accepted business outcome.
'''

dx = '''# 07 — Developer Experience, Testing, and Delivery Lifecycle

## Design goal

The best enterprise controls are easiest to use correctly. Developer experience should compress setup and debugging time while making risk, authority, versions, evidence, and cost visible. A “simple” SDK that hides those concerns merely transfers complexity to incidents.

## Golden path

[[DIAGRAM:dx-golden-path|Figure 7-1 — Developer golden path from template to operated release]]

| **Stage** | **Developer action** | **Platform assistance** | **Required evidence** |
| --- | --- | --- | --- |
| Scaffold | Select domain template and risk tier | CLI creates AgentSpec, ownership, test, evaluation, and deployment skeletons | Owner, purpose, acceptance, data and effect classification |
| Develop | Add instructions, tools, Skills, context, and workflow | Local runtime, mocks, seeded simulation, secret isolation, hot reload | Unit and contract tests; permission declaration |
| Debug | Inspect run graph and compare traces | Trace viewer, state/time travel, prompt/context diff, tool replay | Reproducible failing case and first divergence |
| Evaluate | Run datasets and adversarial/failure suites | Evaluator registry, parallel experiments, confidence intervals, slice reports | Thresholds, reviewers, baseline, regression analysis |
| Package | Build immutable bundle | Lockfile, SBOM, signing, provenance, schema compatibility | ReleaseManifest and rollback target |
| Promote | Bind environment and release | Policy gate, canary, change approval, progressive delivery | ValidationReport and approval for risk tier |
| Operate | Observe SLO, quality, safety, cost | Alerts, runbooks, effect reconciliation, incident tooling | Operational ownership and on-call coverage |
| Improve | Convert evidence to ChangeBundle | Trace mining, dataset curation, experiment and canary workflow | Causal hypothesis, tests, approval, learning record |

## CLI and project layout

BASH · implementation excerpt

```bash
agentctl init supplier-onboarding --template regulated-workflow --risk high
agentctl dev --scenario late-sanctions-response --trace
agentctl test --unit --contracts --failure-injection
agentctl eval --dataset supplier-regression@12 --compare production
agentctl package --lock --sbom --sign
agentctl promote --from staging --to production --canary 5%
agentctl traces diff run:failed run:accepted
agentctl rollback supplier-onboarding@3.2.0 --to 3.1.4
```

A project should contain declarative AgentSpec and workflow files, typed tool and event contracts, Skills, evaluation datasets or references, policy and permissions, environment overlays, dependency locks, runbooks, threat model, and release tests. Secrets and production data never live in the project template.

## Testing and simulation pyramid

[[DIAGRAM:test-pyramid|Figure 7-2 — Agentic testing and simulation pyramid]]

1. **Deterministic unit tests** for schemas, policy helpers, acceptance, routing thresholds, reducers, calculators, and state transitions.
2. **Tool and adapter contract tests** for auth, idempotency, error mapping, timeouts, unknown effects, protocol capability, and telemetry.
3. **Component evaluations** for retrieval, tool choice, arguments, structured outputs, safety, and memory writes.
4. **Trajectory simulations** for plans, handoffs, loops, deadlines, cancellation, duplicate delivery, dependency degradation, and human delay.
5. **End-to-end staging tests** against exact model, identity, gateway, data, and integration versions.
6. **Canary and shadow evaluation** with sequential guardrails and explicit rollback conditions.

## Debugging method

Start from the accepted business outcome and walk backward through the causal run graph. Find the first span where failed and successful traces diverge: input classification, context source/freshness, prompt version, route, model output, tool selection, arguments, policy decision, effect, approval, or acceptance. Do not “fix the prompt” until evidence locates the failing responsibility.

The trace inspector should show versions, redacted inputs/outputs, context manifest, evidence positions, policy decisions, tool schemas and receipts, retries, queue and service time, token/cost attribution, human actions, and business outcome. Authorized replay uses captured contracts and references—not uncontrolled copies of sensitive payloads.

## Configuration and environment promotion

Use one immutable application artifact promoted across environments. Bind environment-specific model allowlists, endpoints, identities, secrets, data sources, quotas, regions, and human queues at deployment. Validate every binding against the declared contract. Never rebuild code between staging and production or use prompt text pasted into a console as the release source.

## Dependency and compatibility management

Pin SDK, provider adapters, model aliases, tool schemas, Skills, MCP servers, policy bundles, evaluator versions, and knowledge snapshots. Generate an SBOM and signed provenance. Test N-1/N compatibility for rolling platform upgrades, and publish deprecation windows. A provider or model swap is a behavior change that requires evaluation, not a harmless configuration edit.

## Production troubleshooting

| **Symptom** | **First evidence** | **Likely owner** | **Safe first action** |
| --- | --- | --- | --- |
| Success drops after release | Release-sliced outcome and trace diff | Application / evaluation | Halt promotion; compare first divergence |
| Latency spikes | Queue/model/retrieval/tool span decomposition | Platform / SRE | Shed optional work; activate approved fallback |
| Duplicate effects | Effect ledger and idempotency collisions | Tool platform | Pause mutation; reconcile authoritative state |
| Cost rises with stable traffic | Tokens, fan-out, retries, route mix | Application / gateway | Enforce budgets; inspect loops and route changes |
| Wrong tenant data | ACL decisions, context manifest, cache keys | Security / context platform | Isolate, revoke, preserve evidence, start incident response |
| Agent “completed” but work is missing | Acceptance evidence and effect terminals | Application / workflow | Reopen as failed/blocked; repair acceptance rule |
'''

pattern_data = [
('Reasoning','P-01','Bounded ReAct','A task requires adaptive evidence gathering but the next step depends on observations.','An unconstrained think–act loop continues until the model feels complete.','The model owns stopping, budget, and success; loops amplify prompt injection, latency, and cost.','Use bounded ReAct inside a deterministic Run Service with step, time, token, tool, and evidence budgets.','Run Service → reason step → eligible tool façade → observation → deterministic stop/acceptance.','Supplier screening may query two approved registries, ask once for a missing identifier, then stop with accepted, blocked, or needs-input.','Step-count tail, no-progress loops, repeated queries, budget exhaustion, evidence coverage, false-completion rate.','Bounds can stop useful exploration; tune by risk and provide explicit escalation.'),
('Orchestration','P-02','Deterministic spine with semantic nodes','A workflow has known obligations but a few decisions require judgment.','A conversational agent owns the entire process and stores progress in the transcript.','Retries, waits, cancellation, approvals, and compensation become ambiguous.','Compile the process as a durable workflow; place agents only at bounded semantic decision nodes.','Workflow state machine → semantic task → typed result → deterministic transition.','Onboarding always validates tax data, screens, approves, creates the vendor, and notifies; models classify documents and summarize evidence only.','Runs without current state, transcript-only state, orphan tasks, duplicate effects, recovery time.','Workflow design adds upfront modeling and can feel rigid when the domain is poorly understood.'),
('Context engineering','P-03','Typed ContextManifest','A model needs relevant, authorized, fresh evidence under a token budget.','Dump top-k search results and conversation history into one prompt.','The system cannot reproduce source selection, detect stale/poisoned content, or explain truncation.','Build a ContextManifest with source identity, ACL, snapshot, provenance, ranking, freshness, and token allocation.','Context planner → governed retrieval → policy filter → ranking/dedup → manifest → model.','A contract-review agent receives only clauses from authorized agreements plus policy versions effective on the review date.','ACL rejection, source freshness, evidence recall/precision, lost-position, token allocation, unsupported claims.','Manifests and snapshotting add storage and latency; use risk-based capture.'),
('Memory','P-04','Provenance-bound tiered memory','Useful preferences and learned facts must persist without turning chat history into truth.','Write every interaction or model summary into one vector store.','Secrets, errors, stale preferences, and malicious instructions become durable and hard to delete.','Separate working, episodic, semantic, and profile memory with eligibility, purpose, scope, confidence, TTL, provenance, correction, and deletion.','Candidate write → policy/quality gate → typed MemoryRecord → scoped retrieval → revalidation.','A support agent stores a verified communication preference, not a model inference about health or identity.','Write acceptance, stale retrieval, correction frequency, cross-scope access, deletion propagation, memory-caused failures.','Stricter eligibility reduces personalization; provide transparent user correction and opt-out.'),
('Tools','P-05','Proposal–authorize–commit tool façade','An agent must cause a business side effect safely.','The model calls a broad CRUD API with ambient credentials.','Natural language becomes authorization; retries duplicate work and ambiguous timeouts hide effects.','Use typed tool contracts, least-privilege credentials, policy checks, ActionProposal/ApprovalGrant, idempotency, and EffectRecord reconciliation.','Agent proposal → policy → optional approval → tool façade → downstream effect → receipt → acceptance.','A payment agent proposes one invoice payment bound to amount, account, policy digest, expiry, and resource version.','Denied calls, invalid arguments, approval mismatch, duplicate keys, unknown effects, reconciliation age.','More control adds latency and engineering; reserve approval for material risk and automate low-risk verification.'),
('Multi-agent collaboration','P-06','Typed task ownership and join','Specialists must collaborate while one parent remains accountable for the outcome.','Agents exchange free-form messages and infer who owns work.','Delegation loops, conflicting owners, lost artifacts, and premature completion appear.','Use TaskEnvelope, one owner, explicit authority, deadlines, artifacts, cancellation, terminal states, and deterministic join.','Supervisor workflow → child task service → specialist runtimes → artifact store → acceptance/join.','A due-diligence supervisor fans out finance, security, and legal reviews; it cannot finish until each required artifact passes acceptance.','Orphan tasks, owner conflicts, fan-out/depth, join wait, late effects, artifact rejection.','Typed collaboration is less fluid; keep brainstorming conversational but commit work through tasks.'),
('Security','P-07','Policy-enforced least-privilege capability','An agent must act across sensitive systems without becoming a privileged identity.','One reusable service token follows the agent through every tool and sub-agent.','Compromise or prompt injection gains broad, long-lived authority with weak attribution.','Carry initiating subject plus workload identity; mint short-lived audience-bound capability envelopes that narrow scope, purpose, spend, and time.','Subject + workload → policy decision → capability lease → gateway enforcement → audit.','A procurement agent may read one tenant’s supplier and propose screening, but cannot approve or create payment.','Over-broad scopes, credential age, delegation expansion, denied actions, unused privileges, cross-tenant attempts.','Fine-grained policy can be complex; use templates and policy simulation.'),
('Reliability','P-08','Effect ledger and reconciliation','External calls can time out after the downstream system commits.','Timeout is treated as failure and immediately retried.','The same logical effect may execute twice; local and downstream state diverge.','Record pre-dispatch intent, use stable idempotency keys, mark ambiguous results unknown, and reconcile authoritative state before retry/compensation.','Prepared EffectRecord → dispatch → receipt or unknown → reconcile → terminal → acceptance.','Vendor creation times out; the platform queries by idempotency key before attempting another create.','Unknown-effect rate/age, duplicate logical effects, reconciliation latency, compensation rate.','Reconciliation requires downstream query support or durable receipts.'),
('Observability','P-09','Causal run graph with outcome linkage','Teams need to diagnose behavior across model, retrieval, tools, policy, humans, and effects.','Independent logs and model transcripts are collected without stable identifiers or versions.','Latency, cost, quality, and failures cannot be attributed to the first divergent component.','Emit a correlated graph linking request, run, task, model, context, policy, tool, effect, approval, acceptance, release, and business outcome.','Trace context + domain IDs → spans/events → protected payload references → evaluation/outcome join.','A failed onboarding trace shows stale evidence entered at retrieval before a correct but misinformed tool call.','Unlinked spans, missing versions, trace completeness, outcome join rate, first-divergence time, redaction violations.','Full capture is costly and sensitive; use policy-aware sampling and references.'),
('Governance','P-10','Risk-tiered evidence gates','Behavior changes frequently but review capacity is finite.','Every change is either manually approved the same way or auto-deployed from a score.','Uniform review creates fatigue; self-certification hides evaluator errors and systemic risk.','Classify change and application risk; require proportional datasets, reviewers, security/privacy checks, canary, and rollback evidence.','ChangeBundle → risk classification → validation policy → accountable approval → staged release.','A typo fix can auto-promote after tests; a memory-policy or model-route change for hiring requires domain, privacy, and risk approval.','Gate bypass, reviewer fatigue, exception age, regression escape, rollback readiness, approval lead time.','Risk classification itself needs governance and periodic calibration.'),
('Operations','P-11','Durable runtime with budgets and backpressure','Runs span bursts, waits, human review, and unreliable dependencies.','Synchronous workers hold state and retry locally until completion.','Restarts lose work, queues explode, and downstream outages amplify retries.','Use durable state, leases, timers, bounded retries, concurrency permits, tenant quotas, circuit breakers, and degraded safe modes.','Ingress → admission control → durable queue/workflow → bounded workers → dependency bulkheads.','During registry degradation, screening queues remain bounded and low-risk lookups use a stale-but-declared cache while protected writes pause.','Queue age, permits, retry amplification, saturation, cancellation latency, recovery point/time.','Durability infrastructure adds operational complexity and eventual-consistency considerations.'),
('System architecture','P-12','Platform contracts with replaceable adapters','Teams need several frameworks and providers without fragmentation.','Application code depends on provider message objects, tracing IDs, tool decorators, and model names.','Migration requires rewrites; controls behave differently by stack.','Define platform-owned AgentSpec, ToolSpec, ContextManifest, TaskEnvelope, EvaluationResult, and normalized telemetry; adapt at boundaries.','Application contracts → framework adapters → shared platform services → provider/tool protocols.','A team moves from one orchestration framework to another while retaining tool authorization, evaluations, traces, and release policy.','Provider-native leakage, adapter conformance failures, migration effort, portability test coverage.','The abstraction may lag novel provider features; allow explicit negotiated extensions.'),
]

def pattern_card(x):
    cat,pid,name,problem,anti,why,rec,arch,ex,metrics,trades=x
    return f'''## {cat}\n\n### {pid} — {name}\n\n**Problem.** {problem}\n\n**Anti-Pattern.** {anti}\n\n**Why It Fails.** {why}\n\n**Recommended Pattern.** {rec}\n\n**Architecture.** {arch}\n\n**Enterprise Example.** {ex}\n\n**Detection Metrics.** {metrics}\n\n**Trade-offs.** {trades}\n'''

pattern_catalog = '''# 16 — Enterprise Pattern Catalog

## How to use the cards

Select a card by the uncertainty or control problem—not by fashionable terminology. Each card uses the same sequence so architecture reviews can compare options consistently. A production design usually composes several cards; one component must still own each state, authority, side effect, and acceptance decision.

[[DIAGRAM:pattern-decision-tree|Figure 16-1 — Pattern selection decision tree]]

| **If the dominant problem is…** | **Start with…** |
| --- | --- |
| Adaptive evidence gathering | P-01 Bounded ReAct |
| Known business obligations with a few semantic decisions | P-02 Deterministic spine with semantic nodes |
| Reproducible evidence projection | P-03 Typed ContextManifest |
| Durable personalization or learned facts | P-04 Provenance-bound tiered memory |
| Protected side effects | P-05 Proposal–authorize–commit tool façade |
| Specialist collaboration | P-06 Typed task ownership and join |
| Delegated authority | P-07 Least-privilege capability |
| Ambiguous external outcomes | P-08 Effect ledger and reconciliation |
| Cross-component diagnosis | P-09 Causal run graph |
| Safe frequent change | P-10 Risk-tiered evidence gates |
| Long-running or bursty workloads | P-11 Durable runtime and backpressure |
| Framework/provider portability | P-12 Platform contracts and adapters |

''' + '\n'.join(pattern_card(x) for x in pattern_data) + '''
## Composition review

For every selected pattern, name the input contract, output contract, state owner, authority owner, failure terminal, acceptance rule, observability evidence, and rollback path. If two components claim the same responsibility—or no component claims it—the composition is incomplete.
'''

anti_data = [
('Reasoning','AP-01','Autonomous monolith','A prototype mixes reasoning, state, credentials, tools, retries, approvals, and completion in one process.','One unconstrained agent owns end-to-end control.','Probabilistic behavior becomes the control plane; failures cannot be isolated or replayed.','Bounded AgentRuntime inside durable workflow, policy, tool/effect, and acceptance services.','Monolith → prompt → direct tools → “done” versus workflow → bounded semantic nodes → governed effects → acceptance.','Supplier onboarding loses progress on restart and repeats vendor creation after timeout.','Responsibilities per component, missing state owner, direct protected calls, restart loss, false completion.','Decompose incrementally around highest-risk effects; more services add interfaces and operations.'),
('Context engineering','AP-02','Prompt as database','Current business state exists only in chat history, scratchpad, or model summary.','The prompt/transcript is treated as authoritative state.','It truncates, drifts, is hard to query, and has no concurrency, schema, or durable audit semantics.','Canonical typed state plus a versioned ContextManifest projection.','Transcript state → hidden mutations versus State Service → snapshot/projection → prompt.','A renewal agent forgets that legal approval is pending after summarization.','Recovery mismatch, missing fields after compaction, conflicting summaries, transcript-only decisions.','Typed state requires schema evolution; preserve useful conversation as evidence, not truth.'),
('Security','AP-03','Ambient authority','Agent workers receive reusable broad credentials unrelated to one task.','Possession of runtime identity implies permission to all connected systems.','Injection or compromise turns broad access into enterprise-wide blast radius.','Subject-plus-workload identity and short-lived capability leases narrowed by purpose, resource, action, spend, and time.','Broad token → any tool versus policy → scoped lease → gateway/tool enforcement.','A support agent token can unexpectedly export every customer record.','Credential scope/age, unused privileges, delegation expansion, cross-tenant attempts, denied actions.','Fine-grained authorization adds policy design and latency; cache only safe decisions with correct keys.'),
('Reliability','AP-04','Retry everywhere','SDK, gateway, workflow, connector, and tool each retry the same failure.','Every layer adds a generic retry policy.','Attempts multiply, dependencies collapse under load, cost explodes, and mutations duplicate.','One retry owner per failure class with shared attempt budget, backoff, deadline, idempotency, and circuit breaking.','Nested retries versus classified error → single owner → bounded schedule → terminal/reconcile.','Three-by-three-by-two retries create eighteen screening calls during an outage.','Attempts per logical operation, retry amplification, correlated spikes, duplicate keys, deadline overrun.','Central policy can be conservative; allow operation-specific budgets within platform caps.'),
('Reliability','AP-05','Timeout means failure','A post-dispatch timeout is immediately mapped to failed and retried.','Local absence of response is mistaken for downstream absence of effect.','The first call may have committed; retry creates duplicates or conflicting state.','Unknown-effect terminal plus authoritative reconciliation before retry or compensation.','Timeout → failed → retry versus timeout → unknown → lookup receipt/state → decide.','Vendor create succeeds but response is lost; a second vendor is created.','Unknown-effect count/age, duplicate business keys, post-timeout conflicts, reconciliation success.','Holding unknown can delay completion; design downstream idempotency and query endpoints.'),
('Governance','AP-06','Boolean or conversational approval','A Boolean or chat message authorizes a later action.','Approval is modeled as sentiment instead of a resource-bound grant.','Arguments, policy, price, actor, or resource version may change after approval.','ActionProposal and expiring ApprovalGrant bound to exact logical effect and expected version.','approved=true → execute current args versus immutable proposal hash → grant → revalidate → commit.','A buyer approves $10,000; the agent later executes $100,000 with the same flag.','Proposal/grant hash mismatch, grant reuse, expiry, post-approval incidents, reviewer dwell.','Strong binding may require reapproval after benign changes; show precise diffs.'),
('Observability','AP-07','Model says done','The run succeeds because the model asserts completion.','Natural-language confidence substitutes for an executable outcome contract.','Missing artifacts, stale evidence, pending approvals, or unknown effects are hidden as success.','Independent deterministic acceptance over authoritative state, evidence, effects, and obligations.','Model text → succeeded versus AcceptanceEngine(manifest, artifacts, effects, obligations).','An onboarding assistant says complete while sanctions evidence is stale.','False-completion rate, reopened runs, missing artifacts/effects, acceptance failures by release.','Acceptance rules require domain ownership and maintenance as obligations evolve.'),
('Multi-agent collaboration','AP-08','Multi-agent chat as workflow','Multiple agents coordinate only through free-form messages.','Conversation is used for ownership, state transitions, deadlines, and joins.','Agents duplicate work, delegate cyclically, lose cancellation, and infer completion inconsistently.','Typed TaskEnvelope, one owner, durable child tasks, artifact contracts, and deterministic join.','Agent chat mesh versus supervisor workflow → task service → specialists → accepted artifacts.','Finance and legal agents both think the other owns final supplier approval.','Orphan tasks, owner conflicts, delegation depth, join age, late effects, lost artifacts.','Formal tasks reduce spontaneity; allow chat inside a bounded task, not as the task ledger.'),
('Context engineering','AP-09','Vector store as source of truth','Similarity search results are treated as current authoritative facts.','Retrieval convenience collapses ranking, truth, authorization, and freshness.','Stale, duplicate, unauthorized, or poisoned chunks can drive decisions and effects.','Governed sources and snapshots; vector index as a derived locator with ACL/freshness/evidence verification.','Vector hit → answer/action versus query → ACL/source/snapshot → evidence → claim/decision.','A policy assistant applies an obsolete travel limit from an old chunk.','Freshness failures, source disagreement, ACL rejection, citation mismatch, stale-effect incidents.','Authoritative lookups may be slower; cache validated projections with versioned keys.'),
('Security','AP-10','LLM judge as security or compliance gate','A model score alone permits or denies protected actions.','Semantic flexibility is mistaken for deterministic policy enforcement.','Judges can be injected, nondeterministic, biased, and wrong under distribution shift.','Deterministic policy/invariant gate; model judge may triage or add evidence, never be sole authority.','Judge score > threshold → execute versus policy checks → optional judge → human/escalation → effect.','A model marks a payment request “low risk” despite exceeding delegated spend.','Repeated-run disagreement, policy false negatives, adversarial bypass, override/incident rate.','Deterministic rules cannot express every nuance; use reviewed escalation for ambiguity.'),
('Reasoning','AP-11','Unbounded loops and recursive delegation','Agents continue reasoning or create children without global limits.','Each local step appears reasonable, but no service owns total budget or progress.','Runaway cost, queue saturation, cyclic delegation, and hidden denial of service result.','Global budgets, acyclic task ownership, depth/fan-out caps, progress invariant, and stop/escalation states.','Agent may recurse versus runtime allocates decreasing budget and validates graph.','A research supervisor repeatedly spawns fact-checkers for each disagreement.','Depth, fan-out, repeated state, no-progress iterations, budget exhaustion, queue impact.','Hard caps can truncate rare complex work; permit accountable exception paths.'),
('Tools','AP-12','Ungated tool discovery and catalog dumping','Every discovered tool and schema is exposed to the model.','Discovery is treated as authorization and more choice is assumed to improve capability.','Prompt size, tool confusion, malicious descriptions, and excessive agency increase.','Governed registry → eligibility/policy filter → task-specific shortlist → schema validation → invocation.','Full MCP catalog in prompt versus approved server/tool slice with capability lease.','A reporting agent discovers and invokes an unrelated admin deletion tool.','Tools exposed/eligible/used, selection confusion, token overhead, unauthorized discovery, schema errors.','Narrow catalogs may omit a needed tool; support explicit discovery escalation.'),
('Memory','AP-13','Memory write by default','Every interaction, model summary, or tool output becomes durable memory.','Storage is cheap and personalization pressure rewards capture.','Errors, secrets, prompt injections, bias, and obsolete facts persist and propagate.','Purpose-bound candidate memory with classification, provenance, confidence, TTL, consent/policy, verification, and deletion.','Transcript → vector memory versus candidate → gate → typed scoped record → review/revalidation.','A malicious email instructs the agent to remember a fake bank account.','Write acceptance, sensitive writes, stale retrieval, correction/deletion, memory-caused incidents.','Strict writes reduce recall and convenience; use short-lived working memory separately.'),
('Observability','AP-14','Telemetry without causal and effect lineage','Logs and spans exist but cannot connect behavior to versions, policy, effect, or business result.','Instrumentation is component-centric and success is defined locally.','Teams optimize latency or model scores while accepted outcomes deteriorate.','One causal run graph and evidence model joining release, context, decisions, effects, acceptance, cost, and outcome.','Separate dashboards versus correlated graph and sliceable evaluation/outcome store.','A lower model latency hides more retries and lower completed-onboarding rate.','Outcome-join rate, missing parent/versions, unattributed cost, trace completeness, diagnosis time.','Correlation increases data-governance burden; protect payloads and store references.'),
('System architecture','AP-15','Model or provider swap as configuration','A model alias changes without full behavioral validation.','Providers expose similar APIs, so teams assume equivalent semantics.','Tool calling, refusals, schemas, latency, cost, safety, and context behavior change.','Treat route/model change as versioned ChangeBundle with compatibility, evaluation, security, load, and canary evidence.','Edit config in place versus immutable route policy → replay → approval → canary → rollback.','A cheaper model silently drops required tool arguments in one language.','Schema/tool regression, refusal shift, quality/cost slices, fallback rate, drift by language/task.','Full validation slows experimentation; automate low-risk evaluation but preserve promotion gates.'),
('Operations','AP-16','In-place change and test after release','Prompts, Skills, tools, policies, or routes are edited directly in production.','Console convenience and weak artifact discipline bypass release engineering.','Runs become irreproducible; partial rollout and rollback are unsafe; incidents lack attribution.','Immutable artifacts, ReleaseManifest, pre-deploy regression, signed promotion, canary, monitoring, and compatible rollback.','Mutable production config versus build once → validate → approve → promote → observe → learn.','A prompt edit improves one task but increases data leakage and cannot be rolled back exactly.','Unversioned runs, manifest mismatch, out-of-band edits, rollback failure, regression escape.','Immutability requires tooling and storage; the platform should make the correct path faster.'),
]

def anti_card(x):
    cat,pid,name,problem,anti,why,rec,arch,ex,metrics,trades=x
    return f'''## {cat}\n\n### {pid} — {name}\n\n**Problem.** {problem}\n\n**Anti-Pattern.** {anti}\n\n**Why It Fails.** {why}\n\n**Recommended Pattern.** {rec}\n\n**Architecture.** {arch}\n\n**Enterprise Example.** {ex}\n\n**Detection Metrics.** {metrics}\n\n**Trade-offs.** {trades}\n'''

anti_catalog = '''# 17 — Enterprise Anti-Pattern Catalog

## Field-guide method

Anti-patterns are recurring system shapes, not isolated coding mistakes. Diagnose the responsibility boundary that failed, not only the visible symptom. Each card uses the same review sequence and points to a replacement architecture.

[[DIAGRAM:anti-before-after|Figure 17-1 — From autonomous monolith to governed agentic system]]

| **Review step** | **Question** |
| --- | --- |
| Problem | What legitimate need drove the design? |
| Anti-Pattern | Which recurring system shape appeared? |
| Why It Fails | Which distributed-systems, security, quality, or governance obligation is hidden? |
| Recommended Pattern | Which explicit owner, contract, or control replaces it? |
| Architecture | How does responsibility and evidence flow before and after? |
| Enterprise Example | What does the shape look like in production? |
| Detection Metrics | Which trace, effect, quality, security, or operational signals expose it? |
| Trade-offs | What cost or constraint does the replacement introduce? |

''' + '\n'.join(anti_card(x) for x in anti_data) + '''
## Recurring anti-pattern review

1. Select failed, corrected, escalated, expensive, slow, and randomly sampled successful traces.
2. Reconstruct the responsibility graph for state, authority, context, tools, effects, acceptance, and change.
3. Tag known cards and capture unexplained shapes as candidate anti-patterns.
4. Compare successful and failed traces to locate the first divergence.
5. Replace the failed boundary with the smallest recommended pattern.
6. Add deterministic, trajectory, security, and operational regression cases.
7. Canary and monitor displacement into adjacent anti-patterns.
'''

gateway = '''# 20 — LLM Gateway and Model Control Plane

## Position in the architecture

The LLM Gateway is the controlled boundary between enterprise workloads and model providers or self-hosted inference. It normalizes model access and enforces model-specific policy, routing, economics, privacy, observability, and release governance. It does not own the business workflow, tool effects, agent delegation, or external API perimeter.

[[DIAGRAM:gateway-position|Figure 20-1 — LLM Gateway position and adjacent gateways]]

| **Component** | **Primary boundary** | **Owns** | **Does not own** |
| --- | --- | --- | --- |
| API Gateway | External client → enterprise API | API auth, routing, quotas, WAF, protocol termination | Agent semantics or model selection |
| Agent Gateway | Agent/workload → agent platform | Agent identity, task admission, delegation policy, tenancy, cross-agent audit | Provider-native inference controls |
| LLM Gateway | Workload → model/inference provider | Provider abstraction, model routing, content/data policy, token/cost control, model telemetry | Durable workflow or business acceptance |
| MCP Gateway | Agent/platform → MCP servers | Server trust, discovery, tool eligibility, protocol mediation, credentials, audit | General model inference or workflow ownership |
| Orchestration layer | Run → tasks/activities | State, deadlines, retries, joins, cancellation, compensation | Provider perimeter or policy source of truth |

## Gateway capabilities

| **Capability** | **Required behavior** | **Critical control** |
| --- | --- | --- |
| Provider abstraction | Normalize requests, streaming, errors, usage, and capabilities | Preserve provider/model/version and raw evidence references |
| Model routing | Choose eligible model by task, risk, region, quality, latency, cost, and health | Deterministic eligibility before optimization; record reason |
| Authentication and authorization | Authenticate workload and initiating subject context | Audience-bound identity; tenant/purpose/model policy |
| Policy enforcement | Enforce allowed use, data class, region, model, output, and risk rules | External policy decision/enforcement; no prompt-only policy |
| PII and secrets protection | Classify, minimize, redact/tokenize, and block disallowed data | Reversible tokenization only in authorized boundary; no secret logging |
| Rate limiting and budgets | Enforce tenant/workload/user quotas, tokens, spend, concurrency, and deadline | Hierarchical budgets; fail predictably before provider charge |
| Caching | Reuse only semantically and policy-safe responses or embeddings | Key includes tenant, policy, model/version, prompt/template, context snapshot, safety settings |
| Retries and fallbacks | Classify transient failures and choose approved alternatives | One retry owner; shared deadline/budget; no unsafe behavior drift |
| Content filtering | Apply input/output safety, injection, DLP, and schema checks | Filters add evidence; protected actions still require deterministic policy |
| Model/version governance | Maintain allowlist, aliases, deprecation, evaluation, canary, rollback | Alias change creates versioned routing-policy release |
| Logging and tracing | Emit normalized spans, usage, route, policy, cache, retry, and error | Redaction and protected payload references |
| Evaluation hooks | Sample and attach online/offline evaluators | Evaluator version, scope, uncertainty, and human override lineage |

## Routing policy

[[DIAGRAM:model-routing|Figure 20-2 — Policy-first model-routing decision tree]]

First filter by tenant, purpose, data classification, residency, risk, required capabilities, context length, tool/JSON behavior, and model/version approval. Only then optimize expected accepted-outcome quality subject to latency and cost budgets. Health, quota, and carbon or infrastructure policy may further constrain choices. The fallback route must satisfy the same invariants; “any available model” is not a safe fallback.

A routing decision records candidates, exclusions and reasons, selected model/version/provider/region, policy digest, expected budgets, fallback chain, and experiment cohort. This makes route behavior replayable and comparable.

## Request sequence

1. Workload sends normalized inference request with RunContext, data classification, capability requirements, budgets, and trace context.
2. Gateway authenticates workload, validates tenant/purpose, and obtains policy decision.
3. Data guard classifies and minimizes inputs; disallowed secrets or regulated data are blocked or tokenized.
4. Router filters eligible deployments and selects one under quality, latency, cost, and health policy.
5. Cache lookup uses full security and semantic key; unsafe cross-tenant or cross-policy reuse is impossible.
6. Provider adapter invokes the exact model version; retry and fallback consume shared deadline and budget.
7. Output guard validates content, schema, DLP, citations/evidence expectations, and provider metadata.
8. Gateway returns normalized result plus route, usage, policy, safety, cache, retry, and trace evidence.

## Cache, retry, and fallback pitfalls

Never cache protected decisions whose correctness depends on current authorization, resource version, or mutable evidence unless the cache key and TTL preserve those dependencies. Do not retry non-idempotent provider extensions blindly. Fallbacks can change refusal, language, reasoning, tool schema, and safety behavior; validate the chain as one release artifact.

## Build-versus-buy decision

Evaluate protocol/provider breadth, policy integration, data handling, telemetry, routing flexibility, self-hosted support, availability, latency overhead, lock-in, and incident control. Even when buying a gateway, retain platform-owned request, routing-decision, evaluation, and trace contracts so the enterprise can replace the implementation.

## Production metrics

Route eligibility and selection distribution; quality and task success by route; schema/tool-call correctness; refusal and safety rates; p50/p95/p99 gateway and provider latency; queue and retry amplification; cache hit and unsafe-key rejection; tokens and cost per accepted outcome; policy denials; PII/secrets detections; provider errors; fallback frequency and regression; unversioned aliases; and trace completeness.
'''

threats = [
('Direct prompt injection','A user explicitly instructs the model to ignore policy, reveal hidden instructions, or call a forbidden tool.','Unauthorized action, data exposure, policy bypass, or unsafe output.','Override phrases, policy/tool denial spikes, instruction hierarchy conflicts, anomalous tool requests.','Separate trusted instructions from untrusted input; typed intent; least privilege; adversarial tests.','Input classification, policy gate before tools, output/schema/DLP guard, bounded runtime, approval for protected effects.','Block or degrade capability, revoke run credentials, preserve trace, notify owner, add regression case.'),
('Indirect prompt injection','A document, web page, email, ticket, or tool result contains instructions aimed at the agent.','Compromised decisions or effects through otherwise authorized retrieval.','Instruction-like text in retrieved content, source-risk score, divergence after one source, unusual tool chain.','Treat all retrieved content as data; isolate content; source allowlists; provenance; content sanitization and injection detectors.','Context boundary labels, tool eligibility independent of content, least privilege, evidence/claim checks.','Quarantine source/snapshot, invalidate derived context/memory, revoke effects if possible, retrain filters/tests.'),
('Jailbreaks','An attacker uses obfuscation, role-play, encoding, multilingual or multi-turn techniques to evade safeguards.','Harmful output, policy evasion, or stepwise acquisition of restricted information.','Classifier disagreement, encoded payloads, repeated boundary probing, rapid reformulations, policy near-misses.','Layered policy and classifiers, rate limits, behavior testing, restricted capabilities, safe response patterns.','Session risk score, capability reduction, refusal/redirect, human escalation, output filter.','Suspend session or capability, investigate campaign, rotate defenses, add attack variants to suite.'),
('Malicious context','Authorized-looking context is crafted to mislead, confuse, or override the task.','Incorrect high-confidence decisions and manipulated business outcomes.','Source disagreement, sudden semantic drift, low provenance, unsupported claims, outlier metadata.','ContextManifest, source trust tiers, cross-source corroboration, freshness and signature checks.','Risk-weighted retrieval, claim-evidence verifier, abstention/escalation on conflict.','Quarantine artifact, invalidate cache/snapshot, correct decisions and downstream records.'),
('Retrieval/RAG poisoning','An attacker inserts or promotes poisoned documents/chunks into the retrieval corpus or index.','Systematic misinformation, targeted exfiltration, or unsafe tool use across many runs.','Ingestion anomalies, rank manipulation, source/embedding drift, new-source failure correlation, citation mismatch.','Signed/approved ingestion, separation of source from index, ACLs, provenance, quality gates, poisoning tests.','Filter by source/snapshot/ACL, anomaly-aware ranking, evidence diversity, protected-action corroboration.','Remove poisoned data, rebuild index from trusted source, invalidate caches, replay affected runs.'),
('Memory poisoning','A user, document, tool, or model causes malicious or false durable memory.','Persistent compromise that survives sessions and spreads incorrect behavior.','Unusual write rate, sensitive/instruction-like memory, correction spikes, failures correlated with one record.','Candidate-write gate, purpose/scope/TTL, provenance, verification, user controls, no default writes.','Memory retrieval policy, confidence/freshness checks, no authority from memory, read/write audit.','Quarantine/delete record and derivatives, notify affected users, replay decisions, tighten eligibility.'),
('Tool misuse','The model selects a wrong tool or valid tool with unsafe arguments.','Corruption, financial loss, privacy violation, or operational disruption.','Low tool precision, invalid/precondition failures, unusual argument distribution, denied calls, effect anomalies.','Narrow tool catalog, typed schemas, semantic constraints, risk classification, contract tests.','Policy and precondition check, preview, idempotency, approval, effect ledger, acceptance.','Pause tool, revoke credentials, reconcile/compensate effects, repair schema/policy/evaluation.'),
('Excessive agency','The agent has too many tools, time, budget, autonomy, or delegation depth.','Runaway cost, unintended changes, large blast radius, and hard-to-audit behavior.','Long-tail steps/fan-out, budget exhaustion, scope unused but available, no-progress loops.','Least-agentic design, global budgets, eligible-tool slicing, depth/fan-out limits, risk-tiered approval.','Runtime admission and stop conditions, capability leases, circuit breakers, human escalation.','Terminate/pause run, revoke leases, reconcile effects, redesign topology and budgets.'),
('Privilege escalation','An agent or sub-agent acquires broader resource, action, purpose, spend, or time scope.','Cross-tenant or high-impact unauthorized access.','Delegation envelope expansion, audience mismatch, policy denials, unusual role assumptions.','Subject-plus-workload identity, monotonic delegation, ABAC/RBAC, short-lived credentials, no token forwarding.','Gateway/tool reauthorization at each hop, scope intersection, just-in-time grants.','Revoke grants/tokens, isolate workloads, audit affected resources, fix policy and delegation tests.'),
('Data exfiltration','Sensitive data is sent to an unauthorized model, tool, agent, URL, or covert output channel.','Regulatory breach, IP loss, customer harm, and contractual violation.','Egress anomaly, unusual domain/tool, tokenized secret recovery attempts, high-entropy output, cross-region route.','Data classification, egress allowlists, minimization/tokenization, provider contracts, private endpoints, DLP.','Egress proxy, DNS/network policy, output DLP, destination authorization, rate and volume limits.','Block egress, revoke keys, contain workload, preserve evidence, breach assessment and notification workflow.'),
('Sensitive-data leakage','PII, secrets, regulated data, prompts, or memory appear in responses, logs, traces, caches, or evaluations.','Privacy/security incident and irreversible credential exposure.','DLP detections, canary secrets, redaction failures, sensitive cache/log fields, access anomalies.','Minimize collection, structured redaction/tokenization, secret scanning, field-level encryption, retention policy.','Input/output/logging guards, protected payload references, role-based trace access.','Rotate secrets, delete/repair copies, execute rights/incident process, improve detectors and schemas.'),
('Insecure agent-to-agent communication','Agents accept unauthenticated tasks, artifacts, callbacks, or delegated authority.','Spoofed work, confused deputy, data leakage, or cross-tenant effects.','Unknown issuer, signature/audience failure, task/artifact mismatch, replayed messages, delegation expansion.','Mutual workload identity, signed envelopes, audience/tenant binding, nonce/idempotency, schema/version policy.','Agent gateway validates identity, authority, deadline, artifact provenance, and cancellation.','Reject/quarantine messages, revoke trust, replay audit, rotate credentials, notify peer owner.'),
('Malicious MCP servers','A server advertises deceptive tools, changes behavior, steals data, or returns injected content.','Credential theft, tool misuse, supply-chain compromise, and persistent injection.','Manifest/tool drift, unsigned version, unexpected egress, schema changes, anomalous outputs, trust-score change.','Approved registry, signing/provenance, sandbox, network policy, version pinning, capability negotiation/tests.','MCP gateway filters discovery, injects scoped credentials, validates schema/output, records effects.','Disable/quarantine server/version, revoke credentials, inspect affected traces/effects, restore trusted version.'),
('Unsafe code execution','Generated or retrieved code runs with host, network, secret, or persistent access.','Remote code execution, data theft, lateral movement, resource abuse, or supply-chain insertion.','Unexpected syscalls/egress/files, resource spikes, prohibited imports, sandbox escape indicators.','Avoid execution when possible; isolated ephemeral sandbox, read-only base, no secrets, allowlists, signed dependencies.','Resource/time limits, syscall/network/file policy, malware scanning, output/artifact validation.','Kill sandbox, isolate host pool, revoke credentials, collect forensic image, patch and rotate base images.'),
('Identity spoofing','Requests or tool calls misrepresent the initiating user, workload, tenant, or approval actor.','Unauthorized access and non-repudiation failure.','Token/audience/issuer mismatch, impossible actor chain, unsigned context, session anomalies.','Strong authentication, workload identity, signed context propagation, channel binding, approval authentication.','Revalidate at gateways and tools; never trust model-supplied identity fields.','Revoke sessions/credentials, invalidate approvals, audit and repair effects, strengthen identity proofing.'),
('Supply-chain attacks','Compromised SDK, package, model artifact, Skill, container, prompt bundle, evaluator, or build pipeline enters release.','Widespread code execution, hidden behavior, data leakage, or corrupted assurance.','Hash/signature mismatch, dependency drift, new maintainer/source, provenance gaps, anomalous build/network behavior.','Locks, SBOM, signed provenance, trusted builders/signers, review, scanning, immutable registries, revocation.','Admission verifies signature/provenance/policy; runtime pins digest and restricts egress/privilege.','Revoke artifact/signing key, halt rollout, roll back, scope affected releases, rotate secrets, incident disclosure.'),
]

def threat_section(i,t):
    name,scenario,impact,signals,prevent,runtime,recovery=t
    return f'''### T-{i:02d} — {name}\n\n**Attack scenario.** {scenario}\n\n**Enterprise impact.** {impact}\n\n**Detection signals.** {signals}\n\n**Prevention mechanisms.** {prevent}\n\n**Runtime controls.** {runtime}\n\n**Recovery strategy.** {recovery}\n'''

security = '''# 21 — Agentic AI Security and Guardrails Architecture

## Security model

Agentic systems combine untrusted language, privileged tools, dynamic context, durable memory, third-party protocols, and autonomous timing. Security therefore cannot be a single prompt or classifier. It is a defense-in-depth architecture that constrains **what enters**, **what the model may infer**, **which capabilities become eligible**, **what may leave**, **which effects can commit**, and **how the enterprise detects and recovers**.

[[DIAGRAM:security-depth|Figure 21-1 — Defense-in-depth guardrails and trust boundaries]]

| **Layer** | **Controls** | **Evidence** |
| --- | --- | --- |
| Channel and input | Authentication, abuse controls, input classification, injection/jailbreak detection, normalization | Request identity, session risk, classifier/version, decision |
| Context and memory | Source trust, ACL, provenance, freshness, poisoning detection, scope, TTL, correction/deletion | ContextManifest, MemoryRecord lineage, source/snapshot |
| Model and output | Approved model route, system instruction integrity, structured output, content safety, claim/evidence, DLP | RoutingDecision, output-guard results, citations/evidence |
| Agent and workflow | Least-agentic topology, budgets, deadlines, loop/fan-out caps, durable state, safe terminals | Run/task graph, budget ledger, stop/cancel events |
| Identity and policy | Subject/workload identity, RBAC/ABAC, capability leases, purpose/spend/time constraints | PolicyDecision, CapabilityEnvelope, credential audit |
| Tools and effects | Eligible-tool slice, schema/preconditions, proposal/approval, idempotency, reconciliation | ToolCall, ActionProposal, ApprovalGrant, EffectRecord |
| Execution and egress | Sandbox, network/file/syscall controls, secrets isolation, DLP, destination allowlist | Sandbox policy, egress decision, artifact scan |
| Supply chain and release | Lock, SBOM, signatures, provenance, tests, risk approval, canary, rollback | ReleaseManifest, attestation, ValidationReport |
| Detection and response | Correlated monitoring, anomaly/rule evaluation, audit, incident playbooks, revocation | Alert, incident timeline, containment and recovery record |

## Trust-boundary architecture

[[DIAGRAM:security-boundaries|Figure 21-2 — Agentic security trust-boundary diagram]]

Trust is not inherited across a chain. Channel identity does not automatically authorize an agent; agent identity does not authorize a tool; tool discovery does not authorize invocation; retrieved content does not become instruction; an agent message does not prove peer identity; a successful HTTP status does not prove business acceptance. Each boundary reauthenticates or validates the relevant claim.

## Runtime guardrail sequence

[[DIAGRAM:guardrail-sequence|Figure 21-3 — Runtime guardrail and protected-effect sequence]]

1. Authenticate initiating subject and workload; establish tenant, purpose, risk, deadline, and trace.
2. Classify/minimize input and detect abuse, injection, jailbreak, secrets, and data-policy violations.
3. Build authorized context from governed sources; label untrusted content and preserve provenance.
4. Select an eligible model route under data, region, capability, safety, cost, and version policy.
5. Validate structured output; compute eligible tools from task, identity, policy, and current state.
6. For an action, validate schema, preconditions, scope, spend, effect, and expected resource version.
7. Create a proposal and human approval when policy requires; bind approval to exact effect and expiry.
8. Execute through sandboxed/tool gateway boundaries with scoped credentials, idempotency, egress/DLP, and audit.
9. Reconcile ambiguous effects and run deterministic acceptance.
10. Monitor, alert, contain, revoke, recover, and create reviewed regression cases.

## Threat catalog

''' + '\n'.join(threat_section(i+1,t) for i,t in enumerate(threats)) + '''
## Incident response for agentic systems

Use **Detect → Contain → Revoke → Reconcile → Eradicate → Recover → Learn**. Containment may pause a tool, MCP server, model route, Skill, memory namespace, tenant, or entire agent. Revocation covers credentials, capabilities, approvals, artifact versions, signing keys, and trust relationships. Reconciliation determines which effects actually occurred; do not infer this from the final model message. Recovery restores a known compatible release and authoritative state. Learning produces threat-specific regression cases without copying disallowed sensitive content.

## Security metrics

Injection/jailbreak detection and bypass; protected-action denial; excessive-agency budget termination; privilege-expansion attempts; DLP/secrets events; cross-tenant and cross-region violations; unauthorized egress; malicious-source/MCP quarantine; sandbox violations; signature/provenance failures; approval mismatch; unknown-effect age; mean time to contain/revoke/reconcile/recover; repeated incident rate; and security regression coverage by threat and release.
'''

learning = '''# 28 — Continuous Learning and Improvement Architecture

## Capability, not a background script

Continuous improvement is a governed architectural capability that joins production evidence to versioned change and release. It does **not** permit an agent to rewrite its own instructions, memory policy, permissions, evaluator, or code and then certify the result. Production produces observations and candidates; accountable services and people decide what becomes a release.

## Closed-loop architecture

[[DIAGRAM:learning-loop|Figure 28-1 — Observe → Measure → Detect → Diagnose → Recommend → Validate → Approve → Deploy → Monitor → Learn]]

| **Stage** | **Inputs and work** | **Durable output** | **Automation boundary** |
| --- | --- | --- | --- |
| Observe | Traces, context manifests, tool/effect records, evaluations, user feedback, human corrections, incidents, latency, cost, outcome | ObservationRecord linked to run/release | Automated capture/redaction/sampling; human approval for sensitive collection purpose/access |
| Measure | Deterministic invariants, quality/safety scorers, retrieval/tool/trajectory metrics, SLOs, economics | Versioned EvaluationResult and metric series | Approved scorers can run automatically; humans define truth, thresholds, and review calibration |
| Detect | Statistical process control, anomaly/rule alerts, drift, slice regression, recurring correction | DetectionEvent with affected slice and confidence | Automatic alert and safe containment inside pre-approved envelope |
| Diagnose | Compare failed/successful traces, locate first divergence, cluster structural/semantic fingerprints, test causal alternatives | FailureCluster and causal hypothesis | Tools rank evidence; accountable owner confirms cause and business meaning |
| Recommend | Generate smallest change candidate, predicted benefit, risks, affected contracts, rollback | ImprovementCandidate / ChangeBundle draft | Candidate generation automated; no self-approval or production mutation |
| Validate | Replay, simulation, deterministic tests, security/privacy/adversarial tests, load, cost, compatibility | ValidationReport with baseline and uncertainty | CI runs automatically; owners approve datasets, exceptions, and residual risk |
| Approve | Risk classification, segregation of duties, domain/security/privacy/operations decision | Signed PromotionDecision | Low-risk pre-approved changes may auto-approve; behavior/authority/data/effect changes require accountable review |
| Deploy | Immutable build, environment binding, staged rollout, canary/shadow, rollback readiness | ReleaseManifest and deployment record | Automated progressive delivery within approved policy |
| Monitor | Compare canary and production to baseline across quality, safety, reliability, latency, cost, and business outcomes | MonitoringDecision | Auto-halt/rollback for tested stop conditions; human decides wider promotion or exception |
| Learn | Record causal result, curate regression cases, update taxonomy/runbook, retire ineffective change | LearningRecord, dataset and control updates | Metadata/taxonomy updates may automate; training data, policy, architecture, and risk changes require governance |

## Evidence architecture

Production evidence must join request, run, task, user feedback, human correction, context source/snapshot, memory records, prompt/Skill/tool/workflow/policy/model versions, routing decision, tool/effect/approval, acceptance, incident, latency, tokens, cost, and business outcome. Protect payloads by reference; keep purpose, retention, residency, access, deletion, and legal-hold policy. No training or long-term dataset receives raw telemetry by default.

## Runtime adaptation versus controlled offline improvement

[[DIAGRAM:runtime-offline|Figure 28-2 — Runtime adaptation and offline improvement boundary]]

| **Runtime adaptation** | **Controlled offline improvement** |
| --- | --- |
| Uses only pre-approved options and fixed policy envelope | Creates a new immutable behavior or architecture release |
| May select eligible model/fallback, reduce optional context, shed load, stop a loop, ask for input, or roll back | May edit prompts, Skills, context policy, memory eligibility, tool schemas, route thresholds, topology, workflow, code, policy, or training data |
| Cannot expand permission, purpose, data access, spend cap, tool catalog, or model allowlist | Requires evaluation and approval proportional to risk |
| Every decision is logged and bounded by deadline/budget | Every candidate has hypothesis, evidence, tests, migration, canary, and rollback |

## Improvement surfaces

| **Layer** | **Production evidence** | **Candidate improvement** | **Validation / approval** |
| --- | --- | --- | --- |
| Prompts | Omissions, conflicts, format drift, unsupported claims | Clarify responsibility, examples, evidence and stop rules | Golden/adversarial replay; human review for behavior/policy wording |
| Context / RAG | Low recall/precision, stale sources, lost-position, injection correlation | ACL/freshness filters, ranking, dedup, token allocation, authoritative lookup | Retrieval/faithfulness/security tests; data-owner approval for new source |
| Memory | Stale personalization, correction, leakage, poisoning | Eligibility, purpose/scope, TTL, verification, correction/deletion, schema | Privacy/security and longitudinal replay; owner approval |
| Tools | Wrong selection/args, timeout, retries, ambiguous effect | Narrow schema/catalog, preconditions, batch/read split, idempotency, reconciliation | Contract/failure/load/security tests; approval for effects/permissions |
| Skills | Version-specific failure or inconsistent domain behavior | New immutable Skill, dependencies, examples, knowledge, acceptance suite | Skill certification and accountable domain owner |
| Model selection | Quality/cost/latency/refusal/tool-schema drift | Eligibility, thresholds, route, cascade, fallback, context window | Full route evaluation, privacy/residency, canary and rollback approval |
| Routing | Misroutes, escalations, capacity imbalance | Calibrate threshold, deterministic pre-router, fallback/escalation policy | Shadow/counterfactual tests; approval if authority/ownership changes |
| Deterministic code | Stable low-entropy model decision repeated at cost or variance | Extract classifier, lookup, rule, calculation, parser, schema transformation | Unit/property/exception tests and domain approval |
| Agent topology | Duplicate work, excessive fan-out/handoffs, unclear owner | Merge agents, add supervisor/task service, change specialization boundary | Simulation, ownership/authority and migration review |
| Workflows | Loops, stuck joins, poor recovery, compensation failures | Add state, deadline, join, checkpoint, stop, compensation, degraded mode | Replay/concurrency/recovery/RTO-RPO tests and operations approval |
| System architecture | Recurring failures across applications or controls | Platform service, contract, gateway, trust boundary, policy or data redesign | Architecture/security/privacy review, migration, portfolio-level evidence |

## Evaluation and observability ecosystem

OpenTelemetry/OpenInference-compatible traces provide portable telemetry. DeepEval and Ragas offer trajectory, component, tool, RAG, faithfulness, and goal metrics. MLflow supports datasets, evaluation-driven development, judges, human/programmatic feedback, experiments, and production monitoring. Phoenix supports trace analysis, annotations, datasets, prompt experiments, and replay. LangSmith supports offline/online evaluation and production-trace-to-dataset workflows. Use adapters and normalize results into platform-owned EvaluationResult; framework scores are evidence, not release authority.

Measure task success, deterministic acceptance, correctness, faithfulness, unsupported-claim/hallucination rate, tool-selection precision/recall/F1, argument correctness, retrieval relevance/precision/recall/freshness/evidence coverage, plan quality/adherence, step efficiency, p50/p95/p99 latency by component, tokens, cost per request and accepted outcome, retry amplification, failure and unknown-effect rate, human correction/override/escalation/fatigue, user satisfaction, and business outcome.

## Recurring-failure and new anti-pattern discovery

Create structural fingerprints from route, tool sequence, error/terminal, handoff graph, retries, context-source mix, effect state, and release versions. Add semantic embeddings only after redaction and purpose review. Compare clusters against the catalog. An unexplained recurring shape becomes a candidate anti-pattern only after a named hidden obligation and replacement boundary are demonstrated. Track recurrence and displacement after remediation.

## Regression-suite lifecycle

1. Capture a failed/corrected trace and preserve its release/evidence links.
2. Apply privacy, security, consent/purpose, retention, and quality review.
3. Reduce it to the smallest reproducible case while preserving the failure cause.
4. Define expected outcome, invariants, allowed trajectory envelope, cost/latency budget, and slice.
5. Add deterministic, component, trajectory, adversarial, failure-injection, and human-review checks as appropriate.
6. Version dataset and evaluators; record disagreement, uncertainty, and overrides.
7. Run in CI, staging, shadow, and canary; block statistically and practically material regression.
8. Retire or update cases only with evidence and lineage.

## Safe automation policy

Safe automated actions include telemetry normalization, redaction using approved rules, evaluator execution, anomaly detection, candidate clustering, draft recommendations, test execution, sandbox deployment, canary traffic adjustment, halt, and rollback within a pre-approved envelope. Human/governance review is required for permissions, policy, data sources or retention, memory purpose, protected tool/effect semantics, model allowlists in sensitive workloads, topology/ownership, architecture, evaluator truth, training data, residual-risk exceptions, and wider promotion. Prohibited self-modification includes expanding authority, disabling controls, editing audit evidence, changing its own approval requirement, or promoting its own behavioral change.
'''

governance = '''# 29 — Governance, Risk, and Operating Model

## Governance objective

Governance makes agentic-system decisions explicit, proportional, evidence-based, and reversible. It should accelerate safe delivery by providing reusable risk tiers, policies, review paths, and evidence—not centralize every prompt edit in a committee.

[[DIAGRAM:governance-model|Figure 29-1 — Federated governance with centralized control services]]

## Decision rights

| **Decision** | **Accountable owner** | **Required partners** | **Evidence** |
| --- | --- | --- | --- |
| Business outcome and acceptance | Domain/product owner | Operations, legal/compliance as applicable | Outcome contract, test cases, business SLO |
| Application risk tier and autonomy | Risk owner | Security, privacy, domain, platform | Threat/data/effect assessment and control plan |
| Platform contract and control | Platform product owner | Architecture, security, developer representatives | RFC, compatibility/migration plan, SLO |
| Data/context/memory purpose | Data owner | Privacy, security, domain | Source, ACL, purpose, retention, deletion, quality |
| Tool/effect authorization | Resource owner | Security, operations, domain | Tool contract, permissions, idempotency/reconciliation, approval policy |
| Model/provider/route approval | Model governance owner | Security, privacy, finance, domain | Capability, evaluation, data terms, region, cost, resilience |
| Evaluator/dataset truth | Domain evaluation owner | Risk, data/privacy, human reviewers | Dataset lineage, rubric, calibration, uncertainty |
| Production promotion | Release owner | Owners required by risk tier | ValidationReport, approvals, canary, rollback |
| Exception acceptance | Named executive/risk authority | Control owners | Scope, rationale, compensating controls, expiry, monitoring |

## Risk tiering

Assess impact of incorrect advice, sensitive data, protected effects, legal/regulatory relevance, autonomy, external exposure, scale, reversibility, multi-agent/tool complexity, and human detectability. Map the result to required controls and release evidence. Risk is not the model name; the same model can support a low-risk drafting assistant or a high-risk financial action system.

| **Tier** | **Typical use** | **Minimum governance** |
| --- | --- | --- |
| 0 — Deterministic/assistive | No model or non-sensitive ideation with no action | Standard engineering and data policy |
| 1 — Bounded advisory | Low-impact content with user verification | Owner, basic evaluation, data controls, monitoring |
| 2 — Operational recommendation | Business decision support or internal tools | Domain acceptance, security/privacy review, regression, human recourse |
| 3 — Protected action | Financial, identity, customer, employee, or infrastructure effect | Least privilege, proposal-bound approval, effect ledger, strong evaluation, canary, incident plan |
| 4 — High-consequence/systemic | Regulated, safety-critical, large-scale autonomous or cross-boundary system | Executive/risk approval, independent assurance, strict runtime envelope, recovery exercises, ongoing review |

## Architecture review scorecard

Review outcome and acceptance; deterministic versus probabilistic boundary; state and effect ownership; identity and delegated authority; context/memory provenance; tool/MCP/A2A trust; threat controls; evaluation truth and slices; observability and privacy; availability/recovery; release and rollback; cost/capacity; human oversight and recourse; and vendor/standard portability. A diagram without owners, contracts, or failure terminals is not an architecture decision.

## Policy hierarchy

Enterprise principles define non-negotiable outcomes. Standards define reusable contracts and controls. Policies-as-code decide eligible models, data, tools, actions, budgets, and approvals. Application configuration selects within that envelope. Exceptions are scoped, monitored, owned, and expiring. A prompt may explain policy but is never the policy decision point.

## Operating cadence

- **Per run:** admission, policy, budgets, guardrails, effects, acceptance, evidence.
- **Daily/weekly:** SLO, quality/safety/cost review, incidents, recurring failures, evaluator health.
- **Per release:** change classification, regression, security/privacy, compatibility, canary, approval, rollback.
- **Quarterly:** portfolio value/risk, control effectiveness, provider/framework dependencies, red-team themes, platform roadmap.
- **Annually or on material change:** policy, legal/regulatory applicability, threat model, recovery exercise, independent assurance.

## Governance metrics

Coverage of risk classification and accountable ownership; percentage of runs with complete release/evidence lineage; exception count/age/expiry; policy and gate bypass; approval fatigue and lead time; evaluator calibration and human disagreement; control false-positive/negative rates; incident recurrence; time to revoke/rollback/recover; application adoption of paved-road controls; and business value per governed accepted outcome.
'''

appendix_a = '''# Appendix A — Pattern Selection Decision Tree and Catalog Index

## Selection sequence

1. Is the path known? Use deterministic workflow; add a bounded semantic node only where ambiguity remains.
2. Does the next step depend on an observation? Use bounded ReAct with explicit budgets and stop/acceptance.
3. Must work survive waits, restarts, or humans? Use durable execution.
4. Are responsibilities split among specialists? Use typed tasks, one owner, artifact contracts, and deterministic join.
5. Does the design cross a trust or deployment boundary? Add identity, authorization, protocol gateway, tenancy, and audit.
6. Can the system cause an effect? Use proposal/authorize/commit, idempotency, reconciliation, and acceptance.
7. Must behavior improve after deployment? Use the governed continuous-learning architecture; never self-certify.

## Pattern catalog index

| **Category** | **Pattern** | **Primary chapter** |
| --- | --- | --- |
| Reasoning | Bounded ReAct | 10 and P-01 |
| Orchestration | Deterministic spine, routing, planning, HITL, durable workflow | 11–15 and P-02 |
| Context | Typed ContextManifest | 22 and P-03 |
| Memory | Provenance-bound tiered memory | 22 and P-04 |
| Tools | Proposal–authorize–commit | 24 and P-05 |
| Multi-agent | Typed task ownership and join | 18 and P-06 |
| Security | Least-privilege capability | 21, 23 and P-07 |
| Reliability | Effect ledger and reconciliation | 24 and P-08 |
| Observability | Causal run graph | 26 and P-09 |
| Governance | Risk-tiered evidence gates | 29 and P-10 |
| Operations | Durable runtime and backpressure | 15, 30–31 and P-11 |
| Architecture | Portable platform contracts and adapters | 4–7 and P-12 |

## Anti-pattern index

| **ID** | **Anti-pattern** | **Category** | **Replacement** |
| --- | --- | --- | --- |
''' + '\n'.join(f'| {x[1]} | {x[2]} | {x[0]} | {x[6]} |' for x in anti_data) + '''

See Chapter 17 for the complete cards and detection/trade-off guidance.
'''

sources = {
    '00-front.md': front,
    '04-reference-architecture.md': ref_arch,
    '06-developer-platform.md': platform,
    '07-developer-experience.md': dx,
    '16-pattern-catalog.md': pattern_catalog,
    '17-anti-pattern-catalog.md': anti_catalog,
    '20-llm-gateway.md': gateway,
    '21-security-guardrails.md': security,
    '28-continuous-learning.md': learning,
    '29-governance.md': governance,
    'appendix-a.md': appendix_a,
}
for name, text in sources.items():
    (OUT/name).write_text(text.strip()+'\n',encoding='utf-8')

plan = {'parts':parts,'chapters':chapters,'part_chapters':part_chapters}
(OUT/'plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({'files':len(sources),'chapters':len(chapters),'pattern_cards':len(pattern_data),'anti_pattern_cards':len(anti_data),'threats':len(threats)},indent=2))
