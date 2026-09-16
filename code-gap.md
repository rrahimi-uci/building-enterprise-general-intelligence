# Northstar Running Example — Code Gap and Implementation Roadmap

**Book:** v2.1.0 · **Scope:** Chapters 1–28 and the implementation appendices
**Audit date:** 2026-09-16
**Status:** roadmap; no implementation is claimed by this document

## Executive decision

The book already has a coherent business thread: Northstar Components wants to
reduce supplier onboarding from twelve days to two, while collecting evidence,
screening sanctions, obtaining approval, creating a supplier record, and
preserving evidence. The prose evolves that scenario well, especially in
Chapter 3 and the security chapters.

The code does not yet evolve with it. The repository contains 23 registered,
behavior-tested examples, but they are mostly chapter-sized demonstrations with
different fixtures and different levels of integration. The first prototype
also names `lookup_supplier`, `create_supplier`, and `send_email` without
defining them. Consequently, a reader can understand each pattern in
isolation, but cannot clone one small program and watch it become the Northstar
system described by the book.

This roadmap makes that missing implementation explicit. It establishes one
canonical case, one cumulative module family, and one before/added/after
contract for every chapter. The existing examples remain useful as focused
pattern tests; the Northstar stages become the connective tissue.

### Severity

| Severity | Meaning for the running example |
| --- | --- |
| **Blocker** | A reader cannot run the first stage or cannot tell what system is being evolved. |
| **Major** | A chapter teaches a production boundary that the cumulative example does not exercise. |
| **Moderate** | The concept is demonstrated in isolation, but the Northstar integration, failure path, or acceptance evidence is missing. |
| **Editorial** | The implementation exists or is nearly sufficient, but labels, transitions, registration, or before/after explanation can mislead the reader. |

## The canonical case that every chapter extends

Do not introduce a second business application as the primary example. Mortgage,
refund, payment, and customer-support examples may remain as short contrasts,
but Northstar supplier onboarding is the only cumulative implementation.

### Business problem

Northstar Components onboards industrial suppliers. Procurement currently spends
about twelve days collecting documents, checking sanctions and tax information,
requesting corrections, and creating an ERP supplier record. The target is two
days for eligible cases without weakening authorization, evidence, approval,
audit, or recovery requirements.

The first case is **Acme Industrial GmbH**, supplier ID `SUP-8421`, in tenant
`northstar-eu`. The identifier is stable across all stages. A test fixture may
contain a second supplier or a malicious document, but it must not change the
business narrative.

### Actors and authority

| Actor | Responsibility | May not do |
| --- | --- | --- |
| Procurement requester | Starts the run and supplies business purpose | Grant itself supplier-write authority |
| Supplier | Provides application and evidence | Change platform state through document text |
| Northstar workflow | Owns run state, waits, deadlines, joins, acceptance, and recovery | Interpret evidence as a business transaction |
| Evidence-review agent | Assesses authorized evidence and proposes next work | Authorize, commit, or claim completion |
| Policy/authorization service | Decides subject, actor, purpose, resource, data, and effect scope | Use model prose as a policy decision |
| Human approver | Approves the exact protected proposal when required | Approve a different proposal through conversational context |
| Tool Gateway/domain service | Validates and commits authorized reads and writes | Expand the model’s authority |
| Sanctions/tax connectors | Return versioned external evidence | Be treated as trusted merely because a protocol call succeeded |
| Operator/auditor | Investigates, intervenes, reconciles, and reviews evidence | Rewrite immutable run history |

### Inputs, outputs, workflow, and constraints

| Contract area | Canonical definition |
| --- | --- |
| Inputs | Tenant, subject, acting workload, purpose, supplier application, immutable document references, country/jurisdiction, policy revision, risk tier, deadline, and callback/approval preferences |
| Evidence | Legal name, registration, tax, beneficial ownership, address, sanctions result, source revision, digest, classification, authorization decision, and freshness metadata |
| Expected outputs | `EvidenceAssessment`, missing-evidence request, `ScreeningResult`, `ActionProposal`, proposal-bound `ApprovalRequest`, `EffectRecord`/receipt, verified supplier projection, and final acceptance decision |
| Normal states | `RECEIVED → EVIDENCE_PENDING → EVIDENCE_REVIEW → SCREENING_PENDING → APPROVAL_PENDING → EFFECT_PENDING → VERIFYING → ACCEPTED` |
| Non-success states | `NEEDS_INPUT`, `REJECTED`, `FAILED`, `UNKNOWN_EFFECT`, `CANCELED`, and `INTERVENTION_REQUIRED`; each has an owner and operator action |
| Constraints | Exact-resource authorization; least privilege; no reusable credentials in prompts or agent state; bounded turns/tools/tokens/cost/time; tenant and region isolation; evidence provenance; stale-resource checks; one retry owner; effect idempotency; approval hash and expiry; fail-closed unknowns |
| Success criteria | Required evidence is present and fresh; sanctions and policy checks pass; the exact action is authorized and approved when required; the ERP mutation has one durable receipt; the supplier projection is verified; all obligations are discharged; trace, audit, and artifacts are joinable by stable IDs |

The two-day target is a Northstar business objective and an example acceptance
target, not a benchmark established by this repository. Stage tests should assert
correctness and safety; performance tests should label their workload assumptions.

### Cumulative architecture

```text
Requester
   │ authenticated request
   ▼
Run control ── durable history/checkpoints ── waits, retries, joins, acceptance
   │ bounded AgentStepRequest
   ▼
AgentRuntime ── OpenAI Agents SDK adapter ── optional OpenAI API provider
   │ typed proposals only
   ▼
Context/Policy/Capability services ── Tool Gateway ── approval service
   │ exact authority, evidence, idempotency, short-lived credentials
   ▼
Domain connectors ── sanctions / tax / ERP ── EffectRecord and receipt
   │
   └──────────── MLflow/OpenTelemetry trace + separate audit/evidence ledger
```

The model and Agents SDK are used for bounded interpretation and tool-loop
mechanics. Custom Python owns the authoritative workflow, contracts, policy
decisions, state fold, effect ledger, reconciliation, fixtures, and tests.
MLflow owns trace/evaluation mechanics and joins to platform IDs; it is not the
system of record for approvals, effects, or audit.

## Current implementation inventory

| Existing asset | What it proves today | Why it is not yet the running example |
| --- | --- | --- |
| `examples/foundations/agent_tool_loop.py` | Real OpenAI Agents SDK tool loop, structured output, bounded turns, offline scripted model | Uses `S-1001`/`S-2002` status fixtures and only a read tool |
| `examples/foundations/governed_tool_gateway.py` | Tool eligibility, authority, stale version, idempotency, unknown outcome | Generic in-memory gateway; no Northstar supplier connector, approval, receipt, or state transition |
| `examples/contracts.py` | Provider-neutral step/platform Pydantic contracts | Test fixture still contains unrelated `refund@1.2.0`; no canonical case manifest or domain outputs |
| `examples/runtime/step_execution.py` | One AgentRuntime adapter around the SDK and a supplier-policy façade | Executes one step; it does not invoke the cumulative workflow or domain effect path |
| `examples/runtime/durable_state.py` | Replayable event fold and unknown-effect blocking | Generic events are not driven by a Northstar run, artifacts, task IDs, or connector receipts |
| `examples/knowledge/*.py` | Typed rules, provenance, graph traversal, grounding, guardrails, algebra, capability discovery | Fixtures use generic policy/transaction examples; no supplier-policy/evidence projection |
| `examples/patterns/*.py` | ReAct limits, routing, planning, approval, verification | Examples use separate refund/sanctions/generic domains and are not cumulative |
| `examples/security/input_guardrail.py` | An input tripwire can stop an SDK run before tools | Demonstrates a refund tool, not a malicious supplier document across retrieval, tool, egress, and effect boundaries |
| `examples/observability/*.py` | MLflow spans, autolog configuration, and deterministic evaluation | IDs and outputs are not correlated across one Northstar run, effect ledger, approval, or audit package |
| `config/examples.json` and `examples/README.md` | Registry and CI execution contract | Registry has no cumulative stage/scenario metadata; README chapter labels reflect older topology in several places |
| Chapter 1 inline prototype | Communicates the initial gap | References undefined tools and is not the executable baseline cited by CI |

## Technology ownership and boundaries

| Technology | Use in the cumulative example | Do not delegate to it |
| --- | --- | --- |
| OpenAI API | Optional provider-backed smoke test, model route, structured response in a developer-configured environment | Workflow truth, authorization, credentials, effects, or acceptance |
| OpenAI Agents SDK `0.22.2` | Concrete adapter for `Agent`, `Runner`, tools, structured output, local handoffs, guardrails, sessions, and framework tracing | Durable workflow state, business records, approval grants, or provider-neutral contracts |
| MLflow `3.15.2` | Trace spans/tags, run correlation, datasets, scorers, evaluation evidence, and regression comparison | Protected audit ledger, policy source, effect receipt, or release authority |
| Custom Python | Domain fixture, Pydantic contracts, workflow reducer, context builder, policy façade, capability intersection, gateway, effect ledger, reconciliation, sandbox/egress test doubles, and CI tests | None of the authoritative enterprise controls should be hidden behind a framework-only helper |
| Test doubles | Offline model, ERP/sanctions/tax connectors, clock, queue, approval signer, failure injector | Production security claims; doubles must be marked as such |

The offline path is mandatory. No example test may require an API key, network,
MLflow server, or live ERP. A separate opt-in integration test may use
`OPENAI_API_KEY` and a configured MLflow backend, but it must never be the only
evidence that an example works.

## Chapter-by-chapter gap register

Each entry uses the same contract so implementation can proceed in order:
**concept**, **current**, **expected**, **missing**, **educational reason**,
**changes**, **technology**, **dependencies**, **order**, **acceptance**, and
**files**.

### Stage 0 — Chapter 1: From an LLM Call to a Production Agentic System

| Field | Roadmap |
| --- | --- |
| Severity | **Blocker** |
| Concept being taught | Start with a simple working agent, then distinguish model, tools, agent, and enterprise system. Define the business problem before complexity. |
| Current state | The narrative names Northstar and Acme, but the inline prototype calls undefined `lookup_supplier`, `create_supplier`, and `send_email`. The registered `agent-tool-loop` example is a different, read-only status question. |
| Expected implementation | A runnable `northstar_stage_00` accepts one supplier application, reads a fixed fixture, produces a clear status/summary, and prints the actors, inputs, output, and known limitations. It must be intentionally non-production and have a visible “before” contract. |
| What is missing | Canonical case fixture; stable IDs; baseline output schema; executable prototype; explicit unsupported claims and failure boundaries. |
| Why it matters | Readers need one mental model before seeing gateways, state, or multi-agent patterns. An undefined first listing teaches that architecture examples need not run. |
| Required changes | Replace or relabel the inline pseudo-code; add a baseline domain fixture and a small `run_baseline()` function. Keep the baseline incapable of writes and explain that later stages add each missing control. |
| Technology | Custom Python for the fixture and result; OpenAI Agents SDK for an optional bounded read-only loop; scripted model for CI. |
| Dependencies | None; this is the root of the stage graph. |
| Recommended order | **PR-NS-00**, before all other Northstar stages. |
| Acceptance criteria | Fresh checkout runs offline; Acme input produces a deterministic structured result; no undefined symbol remains in the cited listing; test asserts the baseline cannot claim a committed supplier effect. |
| Relevant files | Create `examples/northstar/stage_00_baseline.py`, `examples/northstar/fixtures.py`, `examples/tests/test_northstar_stage_00.py`; modify `config/examples.json`, `examples/README.md`, `source/parts/01-part-i.md`. |

### Stage 1 — Chapter 2: Tools, Structured Outputs, and the Deterministic Shell

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Convert model intent into typed proposals and pass through validate, authorize, commit, verify, and accept gates. |
| Current state | `governed_tool_gateway.py` and `effect_idempotency.py` prove generic controls. The Chapter 2 JSON and gateway are not wired to the Chapter 1 case or a domain connector. |
| Expected implementation | The baseline emits a `ToolIntent`/`ActionProposal` for supplier evidence or supplier creation. A Northstar gateway validates `supplier.create@2`, exact resource/version, grant, approval requirement, and logical effect key; a fake ERP returns a receipt. |
| What is missing | Shared Northstar proposal schema; supplier connector; deterministic gate result; typed `EffectRecord` and receipt; before/after diff. |
| Why it matters | This is the first visible transition from “the agent did it” to “the platform accepted a verified effect.” |
| Required changes | Generalize shared contracts without breaking existing IDs; add gateway composition around the existing generic implementation; add stale, unauthorized, duplicate, and unknown-outcome fixtures. |
| Technology | Custom Python gateway/ledger and Pydantic; Agents SDK only for proposal generation; no live API. |
| Dependencies | Stage 0 fixture and output contract. |
| Recommended order | **PR-NS-01**, immediately after PR-NS-00. |
| Acceptance criteria | A valid proposal yields one receipt; replay returns the same receipt without a second ERP call; stale/unauthorized/changed-intent proposals are rejected before dispatch; unknown outcome blocks success. |
| Relevant files | Create `examples/northstar/stage_01_shell.py`, `examples/northstar/contracts.py`, `examples/northstar/connectors.py`, `examples/tests/test_northstar_stage_01.py`; modify `config/examples.json` and the Chapter 2 regions in `source/parts/01-part-i.md`. |

### Stage 2 — Chapter 3: Agent Runtime and Framework Abstraction

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Put the OpenAI Agents SDK behind a provider-neutral `AgentRuntime`; keep workflow, authority, credentials, effects, and audit outside the framework. |
| Current state | `runtime/step_execution.py` runs one supplier-policy step behind a platform façade. It does not consume the Stage 1 gateway/contracts or return a result that the workflow can advance. |
| Expected implementation | The Northstar runtime receives an `AgentStepRequest`, builds authorized tools from the capability envelope, invokes the SDK with the scripted model, validates `AgentStepResult`, and returns a proposal to the Stage 1 shell. |
| What is missing | A cumulative adapter path; shared request/context IDs; mapping from SDK result to domain disposition; optional real OpenAI provider boundary; framework replacement contract test. |
| Why it matters | Without this bridge, the reader sees a good SDK example but cannot understand how a framework participates in a durable enterprise system. |
| Required changes | Refactor the existing step example around Northstar request/fixture types while preserving `step-execution` as a focused listing; add adapter conformance tests for model injection, tool allowlist, max turns, cancellation, structured output, and trace linkage. |
| Technology | OpenAI Agents SDK `0.22.2`; optional OpenAI API integration; custom Python `AgentRuntime`; scripted model for CI. |
| Dependencies | Stages 0–1; uses their contracts and gateway façade. |
| Recommended order | **PR-NS-02**. |
| Acceptance criteria | Runtime cannot create an authority or commit an effect; a provider-neutral request produces a provider-neutral result; SDK state is absent from durable workflow records; replacing the adapter test double leaves the caller unchanged. |
| Relevant files | Create `examples/northstar/stage_02_runtime.py`, `examples/northstar/runtime.py`, `examples/tests/test_northstar_stage_02.py`; modify `examples/runtime/step_execution.py`, `config/examples.json`, `source/parts/01-part-i.md`. |

### Stage 3 — Chapter 4: Enterprise Reference Architecture, Boundaries, and Contracts

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Turn planes and layers into authoritative records, service boundaries, asynchronous Run API, regional execution cell, and event/outbox contracts. |
| Current state | Chapter 4 has detailed contracts and `examples/contracts.py`, but the runnable code has no RunManifest, task owner, artifact store, event history, or outbox around Northstar. |
| Expected implementation | Compose Stage 2 into a minimal in-memory reference architecture: `RunManifest`, `WorkflowExecution`, `Artifact`, `Task`, event envelope, idempotent command, and outbox publication. The implementation should show where each record is written. |
| What is missing | One authoritative writer map; run creation/status/signal/cancel façade; event correlation; artifact references; outbox duplicate handling. |
| Why it matters | The diagram currently teaches more deployed components than the executable example instantiates. A small composition map makes the boundary actionable without pretending to be a production database. |
| Required changes | Add a `NorthstarPlatform` composition root and an architecture-contract test; distinguish in-memory teaching stores from production adapters in comments and prose. |
| Technology | Custom Python/Pydantic; CloudEvents-shaped envelope and transactional-outbox test double; no framework-specific run objects. |
| Dependencies | Stage 2 runtime; Stage 1 effect record. |
| Recommended order | **PR-NS-03**. |
| Acceptance criteria | `POST`-like start is idempotent; every record has one owner; events carry tenant/run/trace IDs; status reads are projections; outbox redelivery is deduplicated; SDK types do not cross the public contract. |
| Relevant files | Create `examples/northstar/platform.py`, `examples/northstar/events.py`, `examples/tests/test_northstar_stage_03.py`; extend `examples/northstar/contracts.py`, `config/examples.json`, `source/parts/02-part-ii.md`. |

### Stage 4 — Chapter 5: Enterprise Knowledge Management for Agents

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Governed knowledge artifacts, ontology/graph, provenance, rules, grounding, and policy projection into enforceable controls. |
| Current state | Six knowledge examples are individually tested, but their fixtures concern generic regulatory rules and transaction systems. Northstar prose says a jurisdiction exclusion is retrieved but not enforced. |
| Expected implementation | Add Northstar supplier-policy artifacts with owner, revision, jurisdiction, effective date, digest, source span, and rule ID. The evidence-review stage retrieves a governed projection; the effect shell evaluates the rule independently. |
| What is missing | Supplier policy fixture; document-to-rule provenance; authorized retrieval; policy revision pin; contradiction/unknown handling in the cumulative path. |
| Why it matters | It demonstrates the crucial distinction between “the agent quoted policy” and “the platform enforced policy.” |
| Required changes | Parameterize or wrap existing policy/grounding/guardrail modules with Northstar fixtures; add a policy change test that invalidates a stale plan/approval. Do not silently replace generic educational fixtures. |
| Technology | Custom Python typed rules/graph/provenance; optional retrieval adapter; the model may extract a candidate, never certify it. |
| Dependencies | Stage 3 RunManifest and Stage 2 authorization/effect boundary. |
| Recommended order | **PR-NS-04**. |
| Acceptance criteria | A rule includes a verifiable source digest/span and scope; unauthorized or out-of-scope policy is not retrieved; unknown required facts fail closed; the same rule is checked before protected effect. |
| Relevant files | Create `examples/northstar/knowledge.py`, `examples/northstar/fixtures/policy.py`, `examples/tests/test_northstar_stage_04.py`; modify relevant knowledge examples/regions and `source/parts/02-part-ii.md`. |

### Stage 5 — Chapter 6: Context Engineering, RAG, Memory, and State

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Separate canonical workflow state, authorized context, artifacts, retrieval, conversation, memory, and recovery state. Materialize a reproducible `ContextManifest`. |
| Current state | Chapter 6 has a strong conceptual context pipeline, but no registered Northstar context builder or memory lifecycle; `durable_state.py` is a generic event fold. |
| Expected implementation | Build a context manifest for `SUP-8421` that records authorization decisions, source revisions, trust labels, redactions, ordering, and digest. Add an explicit memory record with scope, purpose, provenance, TTL, correction, and deletion linkage. |
| What is missing | Authorized retrieval before model access; separate namespaces; prompt projection digest; memory write policy; restartable state linked to artifacts. |
| Why it matters | Readers must see that a prompt is a disposable projection, not the database, memory store, or approval history. |
| Required changes | Add `ContextBuilder`, `MemoryStore` test double, and `NorthstarRunState`; extend the runtime request to require a manifest ID and state version; test tenant/corpus leakage and stale snapshots. |
| Technology | Custom Python for state/context/memory; OpenAI Agents SDK receives only the authorized projection; optional vector/search adapter is non-authoritative. |
| Dependencies | Stages 3–4; policy and artifacts must exist before context can be built. |
| Recommended order | **PR-NS-05**. |
| Acceptance criteria | Same pinned inputs produce the same manifest digest; unauthorized content never reaches the model; memory cannot become an instruction or broaden authority; replay identifies exactly which manifest was used. |
| Relevant files | Create `examples/northstar/context.py`, `examples/northstar/memory.py`, `examples/northstar/state.py`, `examples/tests/test_northstar_stage_05.py`; modify `examples/runtime/durable_state.py`, `examples/contracts.py`, `source/parts/02-part-ii.md`. |

### Stage 6 — Chapter 7: Agentic Developer Platform, SDK, and Delivery Lifecycle

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Provide a platform golden path, adapter conformance, local simulation, versioned definitions, and promotion evidence. |
| Current state | Chapter 7 shows platform APIs and supplier skill snippets, but there is no Northstar scaffold, release manifest, conformance suite, or local-to-production command path. |
| Expected implementation | Make the cumulative example runnable as a platform package with a pinned agent/workflow/policy/tool/model/adapter manifest and an offline simulation command. Add a conformance suite for the runtime boundary. |
| What is missing | Build/run metadata; reproducible stage selection; contract version compatibility; developer-facing failure messages; provider integration seam. |
| Why it matters | The book promises an agentic developer platform; the example should show how a developer obtains and tests one governed capability. |
| Required changes | Add a small manifest and `run_northstar.py` entry point; validate all digests/versions at startup; add a compatibility matrix test. Keep live-provider integration opt-in. |
| Technology | Custom Python platform CLI/manifest; Agents SDK adapter; optional OpenAI API; MLflow config only when observability is enabled. |
| Dependencies | Stages 0–5. |
| Recommended order | **PR-NS-06**. |
| Acceptance criteria | One command runs the offline Northstar stage; manifest pins all behaviorally relevant versions; incompatible worker/manifest is rejected; CI does not require credentials. |
| Relevant files | Create `examples/northstar/manifest.py`, `examples/northstar/cli.py`, `examples/tests/test_northstar_stage_06.py`; modify `examples/README.md`, `config/examples.json`, `source/parts/03-part-iii.md`. |

### Stage 7 — Chapter 8: Skills as Versioned Capabilities

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Concept being taught | Resolve an exact Skill version from capability, purpose, region, risk, data class, tool versions, policy, and evaluation evidence. |
| Current state | `skills_registry.py` proves policy-aware SemVer resolution and packs, but the Northstar runtime does not resolve or pin a Skill. |
| Expected implementation | Register `supplier.evidence.read`, `supplier.screening.propose`, and `supplier.record.create` Skills; resolve one exact version into the Stage 6 manifest and expose only its eligible tools/knowledge. |
| What is missing | Northstar Skill manifests; resolution evidence; revocation/deprecation behavior for active and replay runs; runtime linkage. |
| Why it matters | It shows that a Skill is a governed release unit, not a copied prompt or an SDK primitive. |
| Required changes | Add domain manifests and resolution output; preserve existing registry tests; add a digest and evaluation-suite reference to the Northstar run manifest. |
| Technology | Custom Python registry; Agents SDK only as the resolved execution adapter. |
| Dependencies | Stage 6 release manifest and Stage 4 knowledge refs. |
| Recommended order | **PR-NS-07**. |
| Acceptance criteria | Resolution is deterministic and explainable; inactive/revoked versions cannot start a new run; a deprecated version remains available only under an explicit replay policy; resolved tools are the only tools exposed. |
| Relevant files | Create `examples/northstar/skills.py`, `examples/tests/test_northstar_stage_07.py`; extend `examples/platform/skills_registry.py`, `config/examples.json`, `source/parts/03-part-iii.md`. |

### Stage 8 — Chapter 9: Skill Packs and Domain Platforms

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Compose compatible Skills, policy, knowledge, workflow templates, evaluation, dashboards, and runbooks into an immutable domain pack. |
| Current state | Chapter 9 describes a supplier-onboarding pack, but it has no registered pack consumed by the running implementation. |
| Expected implementation | Resolve `supplier-onboarding@1.x` as the one Northstar pack, including evidence, document validation, sanctions, policy explanation, approval preparation, and supplier-record creation capabilities. The pack must be compatible with the current workflow and policy bundle. |
| What is missing | Pack-to-run binding; compatibility rules; promotion/revocation behavior; distinction between platform-shared controls and domain-owned behavior. |
| Why it matters | The example should demonstrate domain composition without starting a new application or hiding shared controls in a prompt. |
| Required changes | Add pack fixture and install/resolve test; show a before/after table where Stage 7 resolves one Skill and Stage 8 resolves the coherent experience. |
| Technology | Custom Python manifest and registry; Agents SDK executes selected Skills; MLflow suite reference remains metadata until Chapter 24–25. |
| Dependencies | Stage 7 Skills, Stage 4 policy, Stage 6 manifest. |
| Recommended order | **PR-NS-08**. |
| Acceptance criteria | Active pack references only compatible active Skills and policy/evaluation refs; a mismatch fails resolution; the resulting run records pack ID/version/digest. |
| Relevant files | Create `examples/northstar/skill_pack.py`, `examples/tests/test_northstar_stage_08.py`; modify `examples/platform/skills_registry.py`, `config/examples.json`, `source/parts/03-part-iii.md`. |

### Stage 9 — Chapter 10: ReAct — Bounded Reason–Act–Observe Loops

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Concept being taught | Use ReAct only where the next information need depends on the last observation, with external turn/tool/time/cost/no-progress limits. |
| Current state | `bounded_react_loop.py` and `react_engine.py` prove limits, but they are not invoked by Northstar evidence review and do not call the governed gateway. |
| Expected implementation | At `EVIDENCE_REVIEW`, the agent may retrieve one missing or contradictory evidence item, observe it, and stop at bounded limits. Every tool call passes the Northstar capability/gateway path. |
| What is missing | Stage-specific budget; observation/artifact capture; no-progress outcome mapping; distinction between read-only ReAct and protected effect. |
| Why it matters | It demonstrates adaptive information gathering without implying that ReAct should own workflow or mutation. |
| Required changes | Add a Northstar `ReActEngine` invoker; emit `needs_input` or `intervention_required` when bounds are hit; never let the loop call `supplier.create`. |
| Technology | OpenAI Agents SDK for the concrete loop or custom engine for platform limits; custom Python gateway and budget. |
| Dependencies | Stages 2, 5, and 8. |
| Recommended order | **PR-NS-09**. |
| Acceptance criteria | Repeated/empty observations terminate; max turns/tools/cost are enforced outside the model; all retrieved artifacts are authorized and cited; protected write is unavailable in this stage. |
| Relevant files | Create `examples/northstar/react.py`, `examples/tests/test_northstar_stage_09.py`; adapt `examples/patterns/react_engine.py`, `config/examples.json`, `source/parts/04-part-iv.md`. |

### Stage 10 — Chapter 11: Routing, Triage, and Handoffs

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Route deterministically and record whether a local handoff changes responsibility, authority, cancellation, deadlines, and final ownership. |
| Current state | `routing_handoff.py` routes between refunds and sanctions specialists. Northstar prose names evidence, screening, and protected onboarding but does not use one routed case. |
| Expected implementation | Route Acme requests to evidence, sanctions, tax, or onboarding-approval specialists. Local handoff preserves the parent activity owner; durable delegation creates a Stage 15 task with a new owner and narrowed grant. |
| What is missing | Northstar route taxonomy; ownership record; route eligibility/fallback; handoff audit event; authority difference between local and durable delegation. |
| Why it matters | Readers otherwise infer that changing agents is merely passing context, while the chapter teaches a responsibility transfer. |
| Required changes | Add route decision schema and specialist stubs that accept only authorized task inputs; test unsupported/ambiguous routes and cancellation owner. |
| Technology | Agents SDK local handoffs where useful; custom Python route policy and ownership records. |
| Dependencies | Stage 6 runtime and Stage 7 capabilities; durable task contract is introduced before full fan-out in Stage 17. |
| Recommended order | **PR-NS-10**. |
| Acceptance criteria | Every route has an owner and fallback; a specialist cannot access another specialist’s tools by prompt; local handoff does not silently create durable authority; route decision is traceable. |
| Relevant files | Create `examples/northstar/routing.py`, `examples/tests/test_northstar_stage_10.py`; adapt `examples/patterns/routing_handoff.py`, `source/parts/04-part-iv.md`. |

### Stage 11 — Chapter 12: Planning and Plan–Execute

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Treat a model plan as data; compile typed Plan IR against policy, budgets, capabilities, dependencies, and risk before scheduling nodes. |
| Current state | `plan_compilation.py` validates generic `CandidatePlan` nodes, but no plan represents the supplier onboarding obligations or freezes completed work. |
| Expected implementation | Compile a Northstar plan such as collect evidence → validate identity → screen sanctions/tax → request approval if needed → create supplier → verify. Conditional nodes and prerequisites are explicit. |
| What is missing | Domain Plan IR; obligation/acceptance mapping; plan digest in RunManifest; revision policy; committed-node freeze. |
| Why it matters | It makes the before/after sequence visible: the agent proposes a graph, the compiler decides what may run, and the workflow owns execution. |
| Required changes | Add Northstar node types and compiler adapter; validate capabilities, policy digest, budgets, cycles, deadlines, and risk; test plan revision after one node commits. |
| Technology | Custom Python compiler; SDK may propose candidate nodes but never schedules them. |
| Dependencies | Stages 3–8; knowledge and Skill refs must be pinned. |
| Recommended order | **PR-NS-11**. |
| Acceptance criteria | Invalid/dangerous nodes are refused; compiled plan is deterministic and digest-bound; committed past work is not silently replayed; conditional approval/effect nodes are not runnable before prerequisites. |
| Relevant files | Create `examples/northstar/planning.py`, `examples/tests/test_northstar_stage_11.py`; adapt `examples/patterns/plan_compilation.py`, `source/parts/04-part-iv.md`. |

### Stage 12 — Chapter 13: Reflection and Evaluator–Optimizer

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Use bounded reflection for targeted revision; use an independently defined evaluator for acceptance and promotion. |
| Current state | Chapter 13 explains a contradictory address and overconfidence, but the registry has no reflection/evaluator example connected to Northstar. |
| Expected implementation | Add an evidence-assessment candidate with a contradictory address. A bounded reflector requests a revision or missing document; a deterministic/evaluator component checks required evidence, citations, uncertainty, and policy alignment. |
| What is missing | Independent evaluator contract; candidate versus accepted assessment; reflection budget; no self-promotion rule; regression artifact. |
| Why it matters | It prevents readers from equating a polished self-critique with proof that a protected decision is correct. |
| Required changes | Add candidate/evaluation models, cap revision count, preserve prior candidates, and require workflow acceptance outside the model. |
| Technology | Custom Python deterministic checks; optional Agents SDK evaluator call; MLflow dataset linkage is added in Stage 23. |
| Dependencies | Stages 4–5 knowledge/context and Stage 9 bounded loop. |
| Recommended order | **PR-NS-12**. |
| Acceptance criteria | Reflection cannot change policy/authority; evaluator catches missing/contradictory evidence; exceeding revision budget produces a typed intervention; accepted output records evaluator version and evidence. |
| Relevant files | Create `examples/northstar/reflection.py`, `examples/northstar/evaluation_contracts.py`, `examples/tests/test_northstar_stage_12.py`; modify `source/parts/04-part-iv.md`. |

### Stage 13 — Chapter 14: Human-in-the-Loop

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Persist an exact proposal-bound approval, require approver authority and expiry, show before/after evidence, and reauthorize immediately before commit. |
| Current state | `approval_gate.py` and `approval_verification.py` prove hash binding, authenticity, self-approval refusal, expiry, and policy-change rejection, but use generic refunds/arguments. |
| Expected implementation | Northstar pauses `SUP-8421` with an exact supplier-create proposal, evidence list, policy digest, expected ERP version, risk, destination, and diff. The approval service issues a grant; the workflow verifies it before Stage 1 commit. |
| What is missing | Northstar approval request/UI payload; exact connector proposal; durable wait/resume integration; reviewer role/purpose; rejection and escalation path. |
| Why it matters | “Approve the agent” is not a meaningful enterprise control. The reader must see exactly what a human approves and what invalidates it. |
| Required changes | Wrap existing approval modules with Northstar proposal; add approval event history, accessible preview metadata, reauthorization, and policy/record-change invalidation. |
| Technology | Custom Python approval service/signature and workflow; Agents SDK interruption surface only as a local mechanism. |
| Dependencies | Stages 1, 4, 6, 11, and 12. |
| Recommended order | **PR-NS-13**. |
| Acceptance criteria | Changed supplier, arguments, policy, grant, approver, expiry, or resource version blocks commit; approval cannot be minted by the effect caller; rejection leaves a recoverable terminal/wait state. |
| Relevant files | Create `examples/northstar/approval.py`, `examples/tests/test_northstar_stage_13.py`; adapt `examples/patterns/approval_gate.py`, `approval_verification.py`, `source/parts/04-part-iv.md`. |

### Stage 14 — Chapter 15: Long-Running and Durable Agents

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Model long-running work as replay-safe history, durable waits, bounded activities, deployment survival, and effect reconciliation. |
| Current state | `durable_state.py` folds generic events and blocks success with unknown effects. It is not exercised by a nine-day Northstar document wait or crash between ERP write and acknowledgment. |
| Expected implementation | Run Acme until a certificate wait, serialize history/checkpoint, restart with a new worker, accept the document signal, reconcile any unknown effect, refresh authority, and continue without duplicate work. |
| What is missing | Northstar event vocabulary; timer/signal/deduplication; worker restart test; active-run version pin; crash-after-write scenario; cancellation/compensation behavior. |
| Why it matters | The central promise of a production agent is survival across time and process failure, not just replaying a prompt. |
| Required changes | Drive the existing reducer from Northstar events; add a fake clock/queue and failure injector; separate replay from live-effect reapplication; add operator intervention state. |
| Technology | Custom Python event fold and test workflow; a production deployment may use Temporal/another durable engine, but the book example must retain provider-neutral contracts. |
| Dependencies | Stages 3, 5, 11, and 13; effect ledger from Stage 1. |
| Recommended order | **PR-NS-14**. |
| Acceptance criteria | Replay and resume agree; duplicate signals are harmless; a crash after downstream write does not cause a second write; unknown effect prevents acceptance until reconciliation; active run remains compatible with its pinned manifest. |
| Relevant files | Create `examples/northstar/workflow.py`, `examples/northstar/failures.py`, `examples/tests/test_northstar_stage_14.py`; extend `examples/runtime/durable_state.py`, `source/parts/04-part-iv.md`. |

### Stage 15 — Chapter 16: Enterprise Pattern Catalog

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Concept being taught | Select patterns by context, risk, ownership, dependency, and failure mode rather than fashion. |
| Current state | The chapter is a decision catalog and diagram; it does not point to a single cumulative Northstar decision or test. |
| Expected implementation | Add a Northstar pattern-selection matrix: simple tool loop for read, bounded ReAct for evidence uncertainty, plan-execute for obligations, approval gate for protected activation, durable task for waits, supervisor/worker only when boundaries justify it. |
| What is missing | Decision records tying catalog choices to stages and acceptance tests; anti-complexity baseline. |
| Why it matters | The reader should understand why the running example gains each mechanism and why it does not use every pattern everywhere. |
| Required changes | Add a small decision fixture or documentation table; link each choice to the Northstar stage and test, without adding a new framework abstraction. |
| Technology | Custom Python metadata/tests; no new runtime technology. |
| Dependencies | Stages 0–14. |
| Recommended order | **PR-NS-15**, alongside the anti-pattern checks in PR-NS-16. |
| Acceptance criteria | Every selected pattern names problem, alternative rejected, owner, risk, and test; a simpler baseline remains available for comparison. |
| Relevant files | Create `examples/northstar/pattern_choices.py`, `examples/tests/test_northstar_stage_15.py`; modify `source/parts/04-part-iv.md`. |

### Stage 16 — Chapter 17: Enterprise Anti-Pattern Catalog

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Concept being taught | Make unsafe designs concrete: autonomous monolith, ambient authority, layered retries, boolean approval, and unbounded loops. |
| Current state | Four diagrams explain before/after designs, but no Northstar negative tests prove the bad path is rejected. |
| Expected implementation | Add deliberately failing fixtures/tests for direct ERP access, broad tool discovery, retry-after-unknown, approval reuse after mutation, and model-controlled termination. The tests should assert the platform refuses these paths. |
| What is missing | Executable negative evidence and links from each anti-pattern to its replacement stage. |
| Why it matters | Readers retain a control more reliably when they see the exploit/failure and the guard that stops it. |
| Required changes | Add test-only unsafe doubles; never make unsafe behavior runnable as a normal example or include real credentials. |
| Technology | Custom Python tests and failure injection; Agents SDK only for bounded comparison. |
| Dependencies | Stages 1, 2, 9, 13, and 14. |
| Recommended order | **PR-NS-16**. |
| Acceptance criteria | Each anti-pattern has one regression test and one cross-reference to the safe Northstar implementation; tests fail if a guard is removed. |
| Relevant files | Create `examples/northstar/anti_patterns.py`, `examples/tests/test_northstar_stage_16.py`; modify `source/parts/04-part-iv.md`. |

### Stage 17 — Chapter 18: Supervisor/Worker and Multi-Agent Collaboration

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Use durable child tasks with one owner, narrowed grants, explicit fan-out/fan-in, artifact contracts, deadlines, and cancellation. |
| Current state | The chapter describes Northstar screening, tax, security, and procurement specialists and includes task/grant excerpts, but there is no runnable supervisor/worker composition. |
| Expected implementation | Northstar supervisor creates bounded child tasks for sanctions and tax evidence, runs them concurrently, validates artifacts, and joins according to an explicit all/quorum policy before approval or effect. |
| What is missing | `TaskEnvelope` persistence; child grant intersection; child artifact adoption; join/conflict/cancel semantics; aggregate acceptance. |
| Why it matters | It shows when multi-agent architecture is justified and prevents “several personas chatting” from being mistaken for coordination. |
| Required changes | Add child-task store and scheduler test double; derive grants from parent; inject duplicate/out-of-order child events; use local SDK agents only inside child steps. |
| Technology | Custom Python durable task/join logic; optional Agents SDK child adapters; A2A is reserved for the external boundary in Stage 18. |
| Dependencies | Stages 6, 8, 10, 11, and 14; identity narrowing is formalized in Stage 20 but can use a minimal subset first. |
| Recommended order | **PR-NS-17**. |
| Acceptance criteria | Child authority is a strict intersection; one child owner is recorded; duplicate completion is idempotent; join waits for its declared condition; cancellation propagates; conflicting evidence becomes a typed intervention. |
| Relevant files | Create `examples/northstar/delegation.py`, `examples/northstar/join.py`, `examples/tests/test_northstar_stage_17.py`; modify `source/parts/05-part-v.md`. |

### Stage 18 — Chapter 19: External Integration — MCP, A2A, and the Model Control Plane

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Terminate MCP/A2A at governed local gateways; verify endpoint, peer, schema, artifact, authority, quota, egress, and effect semantics locally. |
| Current state | Chapter 19 has A2A envelope and MLflow MCP registry excerpts, but they are not connected to Northstar’s sanctions child or Tool Gateway. |
| Expected implementation | Add test-double MCP screening server and A2A regional verification peer. The local gateways pin registry/agent-card versions, validate responses, scan/adopt artifacts, downscope authority, and convert remote status into Northstar child events. |
| What is missing | Protocol adapter contract; endpoint/peer trust; remote artifact adoption; cancellation and retry semantics; no token passthrough; local effect boundary. |
| Why it matters | Protocol interoperability is not enterprise trust or authorization; the example must make that boundary visible. |
| Required changes | Add protocol façades with fake network transports and contract tests; keep live MCP/A2A smoke tests opt-in and clearly non-required. |
| Technology | Custom Python protocol gateways; optional MCP/A2A client libraries only behind adapters; MLflow registry metadata is not the trust decision. |
| Dependencies | Stage 17 task/artifact contracts; Stage 1 gateway; Stage 20 identity policy. |
| Recommended order | **PR-NS-18**. |
| Acceptance criteria | Untrusted peer/artifact/schema/audience is refused; remote cancellation is best-effort and recorded; no upstream token is forwarded; adopted artifacts carry digest, source, classification, and local authorization. |
| Relevant files | Create `examples/northstar/protocols.py`, `examples/northstar/remote_doubles.py`, `examples/tests/test_northstar_stage_18.py`; modify `source/parts/05-part-v.md`, `config/examples.json` only if a listing is cited. |

### Stage 19 — Chapter 20: Agentic AI Security and Guardrails Architecture

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Layered defense across input, retrieval, model, tool, identity, sandbox, egress, DLP, output, monitoring, and incident response boundaries. |
| Current state | `input_guardrail.py` proves an SDK input tripwire, but uses a refund and does not test a malicious Northstar PDF through later boundaries. |
| Expected implementation | Add a supplier document containing an override instruction and an exfiltration destination. The system labels it as untrusted data, blocks instruction promotion, restricts tools/data, denies egress, redacts output, and records an incident without relying on the detector alone. |
| What is missing | Retrieval-time content labeling; tool/data/egress containment; DLP output check; incident event; security regression fixture. |
| Why it matters | Prompt injection is a model-compromise scenario. The reader must see that containment still works if detection misses the attack. |
| Required changes | Wrap the existing input guardrail as one detector in a defense-in-depth harness; add malicious artifact and trusted-artifact fixtures; prove no secret or unauthorized supplier data leaves the system. |
| Technology | Agents SDK guardrail for the local detector; custom Python policy/egress/DLP/sandbox façades; no real external exfiltration. |
| Dependencies | Stages 5, 6, 17, and 18. |
| Recommended order | **PR-NS-19**. |
| Acceptance criteria | Attack content cannot broaden instructions, tools, data, network, credentials, or effects; blocked/contained path is observable; legitimate supplier evidence still flows; failure is fail-closed at each relevant boundary. |
| Relevant files | Create `examples/northstar/security.py`, `examples/northstar/fixtures/attacks.py`, `examples/tests/test_northstar_stage_19.py`; adapt `examples/security/input_guardrail.py`, `source/parts/06-part-vi.md`. |

### Stage 20 — Chapter 21: Identity, RBAC/ABAC, and Delegated Authorization

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Preserve initiating subject and acting workload; authorize exact action/resource/purpose/time/data; derive narrower child grants and last-hop credentials. |
| Current state | Chapter 21 has detailed identity prose and child-grant code in Chapter 18, but no reusable Northstar authorization evaluator or credential lease. |
| Expected implementation | Carry requester, workflow workload, specialist actor, tenant, purpose, region, risk, and supplier resource through every call. Exchange for an audience-bound short-lived connector credential only after policy permits the exact call. |
| What is missing | Subject/actor model; ABAC decision; delegation lineage; credential lease; resource/purpose mismatch tests; token audience/expiry checks. |
| Why it matters | It prevents the common but dangerous shortcut of passing the requester’s broad token or an agent service credential to every connector. |
| Required changes | Add a policy façade and capability-envelope intersection; connect its decision to Stage 1 gateway and Stage 17 child tasks; retain a fake STS/credential broker. |
| Technology | Custom Python policy/ABAC and credential-lease doubles; optional OAuth token-exchange adapter in a separate integration module. |
| Dependencies | Stages 3, 6, 8, 17, and 18. |
| Recommended order | **PR-NS-20**. |
| Acceptance criteria | Subject cannot change during delegation; child scope never broadens actions/resources/data/region/risk/cost/lifetime; wrong audience/tenant/purpose/expiry is refused; no bearer token reaches the model. |
| Relevant files | Create `examples/northstar/identity.py`, `examples/northstar/policy.py`, `examples/northstar/credentials.py`, `examples/tests/test_northstar_stage_20.py`; modify `examples/foundations/governed_tool_gateway.py`, `source/parts/06-part-vi.md`. |

### Stage 21 — Chapter 22: Tool Security, Side Effects, Idempotency, and Approval

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Protect mutations with logical effect key, intent hash, expected version, request ID, receipt, unknown-effect state, reconciliation, and approval. |
| Current state | Generic gateway and idempotency examples cover parts of this, while Chapter 14 covers approval. No one example performs the Northstar ERP creation and then survives timeout/replay. |
| Expected implementation | Make `supplier.create@2` the canonical protected mutation. The gateway records proposal, policy decision, approval, effect execution, downstream request ID, receipt, and reconciliation state; the workflow accepts only a verified supplier projection. |
| What is missing | End-to-end protected write; connector timeout-after-write; reconciliation query; effect/audit join; conflict on reused logical key. |
| Why it matters | This is the concrete proof that “success” is a verified business outcome, not model text or an HTTP response. |
| Required changes | Compose Stages 1, 13, 14, and 20 into one mutation path; add a fake ERP with controllable timeout, duplicate, stale-version, and conflict behavior. |
| Technology | Custom Python effect ledger/gateway/domain connector; Agents SDK only proposes; approval signer test double. |
| Dependencies | Stages 1, 4, 13, 14, and 20. |
| Recommended order | **PR-NS-21**. |
| Acceptance criteria | Valid action creates exactly one supplier record and receipt; replay is safe; timeout-after-write becomes `UNKNOWN_EFFECT` and reconciles; approval/hash/version mismatch blocks; audit contains evidence and receipt. |
| Relevant files | Create `examples/northstar/effects.py`, `examples/northstar/erp.py`, `examples/tests/test_northstar_stage_21.py`; extend `examples/foundations/governed_tool_gateway.py`, `effect_idempotency.py`, `source/parts/06-part-vi.md`. |

### Stage 22 — Chapter 23: Sandboxing, Egress, Data Security, and Governance

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Contain untrusted model/content behavior through sandbox, default-deny egress, capability, credential, DLP, classification, residency, retention, and approval controls. |
| Current state | Chapter 23 has the attack path and `sandbox-egress` diagram, but no executable sandbox/egress/DLP policy façade around Northstar. |
| Expected implementation | Run any document/OCR/code helper with a restricted filesystem, allowlisted destinations, no raw secrets, resource budgets, content classification, and redacted output. The malicious PDF cannot upload contracts or call an unapproved host. |
| What is missing | Testable sandbox/egress contract; secret lease boundary; destination allowlist; DLP/redaction; retention/deletion/legal-hold state. |
| Why it matters | It demonstrates that security remains effective even when reasoning is manipulated, and clarifies which controls require custom platform code. |
| Required changes | Add deterministic policy façades and failure-injection tests; explicitly label them as control contracts, not a production container implementation. |
| Technology | Custom Python sandbox/egress/DLP/credential test doubles; production may bind to an isolated runtime/proxy. |
| Dependencies | Stages 5, 19, 20, and 21. |
| Recommended order | **PR-NS-22**. |
| Acceptance criteria | Unauthorized host/data/classification/secret is denied; sandbox limits terminate runaway helper; output is redacted/classified; audit records the policy decision without storing secrets; deletion removes memory/artifact links according to policy. |
| Relevant files | Create `examples/northstar/containment.py`, `examples/northstar/privacy.py`, `examples/tests/test_northstar_stage_22.py`; modify `source/parts/06-part-vi.md`. |

### Stage 23 — Chapter 24: Distributed Tracing

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Link asynchronous workflow, agents, models, retrieval, policy, tools, approvals, effects, and external calls in a causal trace while keeping protected audit evidence separate. |
| Current state | MLflow tracing/configuration examples emit supplier/status and context spans, but not a complete Northstar run with effect, approval, or task correlation. |
| Expected implementation | Instrument one full or representative Northstar run with `run_id`, `task_id`, `node_id`, `context_manifest_id`, `policy_decision_id`, `approval_id`, `effect_id`, and provider/model versions. Record IDs and safe summaries, not secrets. |
| What is missing | Cross-stage trace context; MLflow span taxonomy; audit/trace distinction; asynchronous parent/child links; sensitive-data policy; trace completeness assertion. |
| Why it matters | Operators need to explain latency, failure, and authority path—not only view a final answer. |
| Required changes | Extend MLflow helpers with Northstar context manager; add spans at workflow/gateway/policy/retrieval/approval/effect boundaries; add trace-to-audit join test and missing-span alert. |
| Technology | MLflow `3.15.2` for example traces/evaluation hooks; OpenTelemetry-compatible IDs; custom Python audit ledger. |
| Dependencies | Stages 3, 5, 14, 20, 21, and 22. |
| Recommended order | **PR-NS-23**. |
| Acceptance criteria | Offline SQLite-backed MLflow test produces a trace with required IDs/spans; trace payload excludes secrets by default; audit remains authoritative and complete; unknown effect and approval wait are visible as causal states. |
| Relevant files | Create `examples/northstar/observability.py`, `examples/tests/test_northstar_stage_23.py`; adapt `examples/observability/mlflow_tracing.py`, `mlflow_trace_configuration.py`, `source/parts/07-part-vii.md`. |

### Stage 24 — Chapter 25: Continuous Learning and Governed Improvement

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Turn production failures and feedback into immutable datasets, deterministic/trajectory/safety checks, calibrated judges, slice analysis, approval, release, and monitoring. |
| Current state | `mlflow_evaluation.py` evaluates simple supplier status cases and detects a regression, but not a Northstar trajectory, unauthorized tool path, effect, approval, or protected slice. |
| Expected implementation | Capture a failed/blocked Northstar run as a regression case; evaluate candidate runtime/Skill/prompt bundles on correctness, evidence grounding, safety, tool trajectory, approval binding, repeated-run reliability, cost, latency, and human burden. Gate promotion by risk slice and baseline comparison. |
| What is missing | Northstar evaluation dataset; production-trace-to-case conversion; deterministic trajectory graders; judge calibration; release gate; no runtime self-modification. |
| Why it matters | It closes the learning loop without letting aggregate answer quality hide a low-volume unauthorized trajectory. |
| Required changes | Extend MLflow evaluation with Northstar cases and candidate metadata; add a deterministic release decision object and approval record; link candidate digest to Stage 6 manifest. |
| Technology | MLflow datasets/scorers/traces; custom Python deterministic graders and release gate; optional OpenAI judge only as calibrated evidence. |
| Dependencies | Stages 8, 12, 21, and 23. |
| Recommended order | **PR-NS-24**. |
| Acceptance criteria | A candidate that improves text quality but violates tool/approval policy is rejected; failures become immutable cases; scorers are actually invoked; judge version/calibration/slice is recorded; runtime cannot self-promote. |
| Relevant files | Create `examples/northstar/evaluation.py`, `examples/northstar/regressions.py`, `examples/tests/test_northstar_stage_24.py`; adapt `examples/observability/mlflow_evaluation.py`, `source/parts/07-part-vii.md`. |

### Stage 25 — Chapter 26: Governance, Risk, and Operating Model

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Concept being taught | Assign risk ownership, control-plane responsibilities, exception/incident governance, review cadence, and measurable operating obligations. |
| Current state | Chapter 26 provides federated governance and decision/evidence prose but no Northstar risk register, control owner, exception record, or operating review fixture. |
| Expected implementation | Attach risk tier, owner, control set, data class, region, review date, exception status, and escalation route to the Northstar pack/run. Show who can approve policy, release, runtime intervention, and effect recovery. |
| What is missing | Governance metadata model; exception lifecycle; owner/recourse fields; operational review evidence; link from risk tier to controls and approval. |
| Why it matters | Governance becomes practical when the reader can answer who owns a denied, failed, stale, or harmful run. |
| Required changes | Add governance manifest and checks; do not turn the example into a legal compliance claim or encode jurisdiction-specific law without scoped sources. |
| Technology | Custom Python governance metadata and runbook links; MLflow/trace references only as evidence, not governance authority. |
| Dependencies | Stages 8, 19–24. |
| Recommended order | **PR-NS-25**. |
| Acceptance criteria | Every R-tier decision has owner, policy, evidence, escalation, and expiry; open exceptions cannot silently authorize effects; governance review can locate the exact Northstar run and release. |
| Relevant files | Create `examples/northstar/governance.py`, `examples/tests/test_northstar_stage_25.py`; modify `source/parts/08-part-viii.md`, Appendix B/C/I if references are added. |

### Stage 26 — Chapter 27: Deployment, Versioning, CI/CD, and Recovery

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Concept being taught | Promote immutable release bundles, pin active runs, canary new starts, preserve compatibility, and recover without rewriting history. |
| Current state | Chapter 27 describes release manifests and rollback, but the cumulative example has no serialized bundle, compatibility checker, canary assignment, or migration/recovery test. |
| Expected implementation | Package Northstar agent/Skill/workflow/policy/model/tool schemas/evaluator/adapter versions and digests. Start new runs on a canary; keep active runs pinned; reject incompatible worker; roll back assignment; replay and reconcile. |
| What is missing | Release manifest implementation; schema compatibility rules; active-run pin; rollout/rollback state; CI release gate; recovery rehearsal. |
| Why it matters | Readers see how an evolving system remains trustworthy while work is in flight. |
| Required changes | Add compatibility checker and release test fixture; integrate examples registry and validation into the stage CI command; document that generated book artifacts remain a separate build concern. |
| Technology | Custom Python manifest/compatibility logic; CI scripts; Agents SDK/MLflow versions recorded as dependencies, not deployment authority. |
| Dependencies | Stages 6, 8, 14, 23, 24, and 25. |
| Recommended order | **PR-NS-26**. |
| Acceptance criteria | Manifest is immutable and complete; incompatible schema/worker is rejected; active run does not change behavior unexpectedly; rollback affects new assignment only; clean checkout rebuilds examples and book artifacts. |
| Relevant files | Create `examples/northstar/releases.py`, `examples/tests/test_northstar_stage_26.py`; modify `config/examples.json`, `source/parts/08-part-viii.md`, `CHANGELOG.md` when implementation begins. |

### Stage 27 — Chapter 28: Cost, Latency, Capacity, and Reliability Optimization

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Concept being taught | Optimize cost per verified success using admission, bounded execution, selective context, routing, concurrency, safe degradation, and workload-specific capacity estimates. |
| Current state | Chapter 28 has a Northstar quarter-end scenario, equations, and reliability diagram, but no scenario-driven simulator or metrics bound to the cumulative run. |
| Expected implementation | Replay a workload of Northstar runs with queue, tool, model, human-wait, retry, and effect outcomes. Compute cost/latency/capacity per accepted supplier, tenant fairness, deadline misses, and safe degradation decisions. |
| What is missing | Metric schema; workload fixture; admission/concurrency controller; cost per verified success; retry amplification and human burden; sensitivity analysis. |
| Why it matters | It prevents optimization from becoming token-price tuning that increases unsafe retries or human load. |
| Required changes | Add deterministic simulator/metrics collector; label all values as example workload assumptions; test admission and fairness under a threefold demand spike and provider outage. |
| Technology | Custom Python simulator and metrics; MLflow can store experiment results, but acceptance remains custom and business-outcome based. |
| Dependencies | Stages 14, 21, 23, 24, and 26. |
| Recommended order | **PR-NS-27**, final chapter implementation. |
| Acceptance criteria | Simulator reports verified-success denominator; limits protect tenant/risk fairness; safe degradation never bypasses policy/approval/effect controls; reliability/cost changes are compared against a baseline. |
| Relevant files | Create `examples/northstar/capacity.py`, `examples/northstar/simulation.py`, `examples/tests/test_northstar_stage_27.py`; modify `source/parts/08-part-viii.md`, Appendix L if the acceptance table gains links. |

## Appendix and navigation gaps

The appendices already contain the right contracts and acceptance themes, but
they should become the handoff surface for the implementation stages.

| Appendix | Gap | Required follow-up |
| --- | --- | --- |
| B — Failure triage and operator runbooks | Runbooks are not yet keyed to Northstar IDs/states/effect outcomes | Add commands and expected evidence for `UNKNOWN_EFFECT`, stale policy, approval expiry, poisoned event, child timeout, and replay; link to Stage 14/21/23 tests |
| C — Platform contracts quick reference | Contract list is conceptual rather than linked to cumulative modules | Add the final module/class name and owner for Run, Task, ContextManifest, PolicyDecision, ApprovalGrant, EffectRecord, Trace, Evaluation, and Release |
| I — Northstar Reference | It is the natural implementation guide but must not become a second source of truth | Make it a reader-facing map to `examples/northstar/` and `code-gap.md`; keep prose in `source/parts`, code in `examples` |
| J — Coding-agent prompt and acceptance criteria | It asks for architecture breadth but not stage-by-stage Northstar implementation | Add the stage ledger, severity gates, offline requirement, registry steps, and PR sequence from this roadmap |
| L — Capacity, resilience, and release acceptance | Strong final gates but not linked to test names | Add acceptance-test IDs after implementation; do not mark a gate complete from prose alone |
| Front-matter TOC | Current TOC is authored and structurally correct for the 8/28/12 topology | Do not add roadmap stages as chapters. If `code-gap.md` is included in a release package, keep it project documentation outside the manuscript TOC |
| `examples/README.md` | Several chapter labels reflect earlier numbering/topology and there is no cumulative order | Replace the table with stage IDs and current chapter numbers after each stage lands; add a Northstar progression table |
| `config/examples.json` | Registry validates paths/tests but has no stage or scenario fields | Add optional `stage`, `chapter`, `scenario`, and `northstar_phase` fields only when implementation begins; update validator/schema tests first |

## Recommended implementation order and PR boundaries

Implement the example as small reviewable PRs. Do not land all stages in one
large change, and do not modify `main` directly.

| PR | Stages | Outcome |
| --- | --- | --- |
| `PR-NS-00` | 0 | Runnable case definition and honest baseline |
| `PR-NS-01` | 1 | Typed proposal, gateway, effect ledger, connector |
| `PR-NS-02` | 2 | SDK adapter and provider-neutral runtime |
| `PR-NS-03` | 3 | Run/platform composition and event/outbox boundary |
| `PR-NS-04` | 4 | Governed supplier knowledge and policy enforcement |
| `PR-NS-05` | 5 | Context manifest, memory, and replayable Northstar state |
| `PR-NS-06` | 6 | Developer package, manifest, and conformance path |
| `PR-NS-07`–`PR-NS-08` | 7–8 | Versioned Skills and supplier domain pack |
| `PR-NS-09`–`PR-NS-12` | 9–12 | ReAct, routing, planning, reflection |
| `PR-NS-13`–`PR-NS-16` | 13–16 | Approval, durability, pattern decisions, anti-pattern regression tests |
| `PR-NS-17`–`PR-NS-18` | 17–18 | Supervisor/worker and external protocol gateways |
| `PR-NS-19`–`PR-NS-22` | 19–22 | Defense in depth, identity, protected effects, containment |
| `PR-NS-23`–`PR-NS-24` | 23–24 | Causal traces and governed learning/evaluation |
| `PR-NS-25`–`PR-NS-27` | 25–27 | Governance, release recovery, capacity/reliability |

Each PR must contain only the stage implementation, its behavioral tests,
registry entries, exact book listing markers, and the relevant chapter
before/after transition. It must update the PR description with architectural
decisions, tests, risks, and generated-artifact status. A PR may depend on the
previous PR, but it must not silently reimplement earlier contracts.

## Agent-executable implementation protocol

For every stage:

1. Read the complete affected Part, previous/next chapter transitions,
   `AGENTS.md`, the design system, and the current stage entries in this file.
2. Inspect the existing examples, tests, registry, and source markers before
   creating a new module. Reuse stable contracts where semantics match.
3. Write the **before** test or fixture first. It should demonstrate the
   capability missing at the chapter boundary.
4. Implement the smallest **added** capability in `examples/northstar/` and
   keep business truth/custom controls outside the Agents SDK.
5. Write the **after** test, including at least one refusal, failure, replay, or
   recovery case appropriate to the stage.
6. Register every listing in `config/examples.json`, cite it from the canonical
   `source/parts/*.md`, and update `examples/README.md`. Never paste a second
   copy of executable code into the manuscript.
7. Add or update a transition table with: previous state, new capability, why,
   new records, new failure modes, and next chapter dependency.
8. Run the narrow example tests, then `make examples`, `make examples-run`,
   `make assemble`, `make build`, and `make validate` as appropriate. Use the
   repository’s pinned `.venv-examples`/`.venv` rather than an unpinned global
   interpreter.
9. For changes to source or generated artifacts, rebuild Markdown, DOCX,
   LaTeX, diagrams, manifests, checksums, and release package according to
   `AGENTS.md`; never hand-edit generated outputs.
10. Open a dedicated PR, complete `.github/pull_request_template.md`, assign
    the author and Copilot when available, address review comments with
    additional commits, and leave the PR open for the author to merge.

## Full-book acceptance gates

The roadmap is complete only when a new reader can follow one executable
Northstar run from Stage 0 through Stage 27 and the following are true:

- Every chapter says what the example looked like before, what is added, why it
  is needed, and what it looks like after.
- Every registered Northstar listing has a behavioral test and runs offline.
- An optional OpenAI API path is clearly separated from the deterministic CI
  path and does not own enterprise truth.
- Agents SDK versions, MLflow versions, model routes, Skills, policies, tools,
  schemas, evaluators, and workflow releases are pinned in the run/release
  manifest.
- No model output directly transitions protected state, grants authority,
  commits an effect, certifies evidence, or promotes a release.
- Context retrieval enforces tenant/source ACLs before model exposure; memory
  has explicit type, scope, provenance, TTL, correction, and deletion policy.
- Delegation carries subject and actor identity, narrows authority, and records
  ownership, budget, cancellation, and join semantics.
- Approval is bound to exact proposal/evidence/resource version/policy,
  expires, and is reauthorized immediately before commit.
- Duplicate delivery, stale state, provider outage, timeout-after-write,
  unknown effect, poison event, cancellation, approval expiry, child failure,
  prompt injection, and compatibility mismatch have executable tests and an
  operator action.
- MLflow/trace evidence joins to platform IDs while the audit/effect ledger
  remains separate and authoritative.
- Evaluation covers business outcome, evidence/grounding, trajectory/tool use,
  safety, repeated-run reliability, cost, latency, and human burden, with
  slice-aware release gates.
- The book’s TOC, examples registry, source markers, diagrams, tables, code,
  generated Markdown/DOCX/LaTeX, manifests, checksums, and release package are
  synchronized after implementation.

Until those gates are met, the book may describe the architecture, but it must
not claim that the Northstar implementation is production-ready.
