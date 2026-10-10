# PART III — THE DEVELOPER PLATFORM

Parts I and II defined the contracts; this Part decides who builds them once.
Chapter 7 describes the paved road (platform-owned contracts, adapters,
services, and a golden path) and doubles as a map: most of its services are
developed in Parts IV–VIII. Chapters 8 and 9 define what teams reuse on that
road: the versioned Skill and the Skill Pack. Three owners share it: the
platform team, domain-capability owners, and application teams.

# 07 — Build a Paved Road for Agent Teams

> **Evidence context:** The portability layer is informed by current public agent abstractions from OpenAI, Microsoft, and Google; capability parity is not assumed and must be proven by adapter conformance tests. **[R29][R31][R32]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** A second Harborlight team begins an agent for the compliance review and starts copying the mortgage team's SDK wrapper. |

|  |
| --- |
| **THE DESIGN CHOICE** Give teams platform-owned contracts, conformance-tested adapters, and a golden path that emits evidence at every stage; leave domain behavior, topology, and acceptance to the team. |

## Why teams should not each rebuild the safety layer

The need for a paved road becomes obvious after the second or third team ships. One team retries inside its SDK wrapper, another records only transcripts, and a third gives tools a broad service credential. Each local choice looks reasonable, but the organization now has three incompatible meanings of failure, audit, and authorization. A platform earns its place by making those cross-cutting decisions once and leaving product teams free to build differentiated domain behavior.

The goal is not to force every application into one monolith; it is to make
the safe path easier to reuse than the clever shortcut.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Platform services own contracts and evidence; applications and domain-capability owners own domain behavior | application code to platform-owned services | template · adapter · release artifact | one application release | AgentSpec · AgentStepRequest/Result · ToolManifest · ReleaseManifest |

## What teams should be able to rely on

The developer platform lets teams build differentiated agents without repeatedly rebuilding identity, policy, tool safety, tracing, evaluation, durable execution, and delivery infrastructure. Applications use platform-owned contracts and replaceable adapters. Most of these services are developed later in the book; the last column says where.

[[DIAGRAM:developer-platform|Figure 7-1 — Agentic developer platform and SDK capability stack]]

| **Capability** | **Reusable platform responsibility** | **Application-specific responsibility** | **Taught in** |
| --- | --- | --- | --- |
| Agent Runtime | Step contract, budgets, typed outputs, interruption, cancellation, adapter | Domain instructions, acceptance, specialist roles | Ch 3 |
| Workflow and durable execution | Durable state, timers, joins, checkpoints, leases, deduplication, retries, replay, recovery, reconciliation | Domain process graph, deadlines, state machine, and compensation choices | Ch 15 |
| Tool SDK | Schema, identity context, idempotency, effect protocol, mocks, telemetry | Domain operation and compensation semantics | Ch 2 (introduction), Ch 22 (contract) |
| MCP Integration | Server registry, trust, gateway, discovery cache, compatibility tests | Approved servers/tools and domain interpretation | Ch 19 |
| Agent-to-Agent Communication | Task/artifact envelopes, delegation, identity, deadline, cancellation | Collaboration topology and child acceptance | Ch 18–19 |
| Context/RAG | Connectors, ACL filtering, snapshot/provenance, ranking hooks, budgets | Sources, retrieval policy, evidence requirements | Ch 5–6 |
| Memory | Eligibility, scope, TTL, provenance, correction/deletion, encryption | Purpose, schema, confidence, business ownership | Ch 6 |
| Skills | Manifest, versioning, dependencies, signing, registry, tests | Domain-capability owner: capability logic, knowledge, examples, acceptance suite | Ch 8–9 |
| Identity & Permissions | Subject/workload identity, action policy, short-lived credentials | Declared permissions and resource scopes | Ch 21 |
| Guardrails | Injection and content detectors, input/output safety, DLP | Domain risk rules, safe responses, escalation | Ch 20 |
| LLM Gateway | Provider adapters, routing, budgets, filtering, cache, fallback, telemetry | Quality/cost/latency policy and needed capabilities | Ch 4 (contract), Ch 28 (routing and cost) |
| Evaluation | Dataset/evaluator registry, experiments, regression gates | Domain truth, rubrics, thresholds, reviewers | Ch 25 |
| Observability/Tracing | Unified run graph, schemas, sampling, redaction, correlation | Domain events and outcome linkage | Ch 24 |
| Human-in-the-Loop | Proposal, preview, grants, queues, SLAs, recourse | Reviewer policy, domain evidence, decision rights | Ch 14 |
| Deployment & Versioning | Packaging, manifests, environments, gates, canary, rollback | Application release and risk sign-off | Ch 27 |

Two kinds of team sit on the application side. Application teams own an agent: its AgentSpec, topology, and acceptance. Domain-capability owners own the Skills and Skill Packs that several applications reuse (Chapters 8–9). Chapter 4 § The decisions that shape the system already federates both to accountable owners.

The Tool SDK is the authoring side of the Tool Gateway. A developer writes a typed operation; the SDK emits the ToolManifest (Chapter 22 § What a ToolManifest must declare) that the gateway enforces on every call (Chapter 2).

## Keep contracts stable while frameworks change

[[DIAGRAM:portability|Figure 7-2 — Platform contracts with replaceable framework and provider adapters]]

Chapter 3 put the framework behind `AgentRuntime.execute(AgentStepRequest) → AgentStepResult`; the platform's job is to own that seam for every team. The stable contracts are AgentSpec (Chapter 4), AgentStepRequest/AgentStepResult (Chapter 3), ToolManifest (Chapter 22), ContextManifest and MemoryRecord (Chapter 6), TaskEnvelope (Chapter 18), EvaluationResult (Chapter 25), and ReleaseManifest (Chapter 27). Compatibility suites verify cancellation, tools, streaming, approvals, errors, telemetry, usage, and version behavior.

## Make the safe path the easy path

Developer experience should compress setup and diagnosis time while making authority, versions, risk, evidence, and cost visible. A convenient SDK that hides those concerns transfers complexity to production incidents.

[[DIAGRAM:dx-golden-path|Figure 7-3 — Developer golden path from scaffold to operated release]]

| **Stage** | **Developer action** | **Platform assistance** | **Evidence** |
| --- | --- | --- | --- |
| Scaffold | Select template and use-case tier (Chapter 26) | AgentSpec, ownership, tests, eval, deployment skeleton | Purpose, owner, acceptance, data/effect class |
| Develop | Add instructions, tools, Skills, context, workflow | Local runtime, mocks, seeded simulation, hot reload | Unit/contract tests and permissions |
| Debug | Inspect and compare run graphs | Trace viewer, state/time travel, prompt/context diff, replay | Reproducible failure and first divergence |
| Evaluate | Run golden, adversarial, failure, load suites | Dataset/evaluator registry and slice reports | Thresholds, reviewers, baseline, uncertainty |
| Package | Build immutable bundle | Lock, SBOM, signing, provenance, compatibility | ReleaseManifest and rollback target |
| Promote | Bind environment and canary | Policy gate, approval, progressive delivery | ValidationReport and ReleaseGateDecision (Chapter 25); risk approval (promotion detail: Chapter 27) |
| Operate | Observe SLO, quality, safety, cost | Alerts, runbooks, reconciliation, incident tools | On-call and operational ownership |
| Improve | Build ChangeBundle from evidence | Trace mining, dataset curation, experiment workflow | Causal hypothesis, tests, approval, reviewed regression case (learning loop: Chapter 25) |

A paved road has costs. Its abstractions lag new framework features, and the platform team can become a queue. Allow negotiated extensions behind the same contracts (P-12, Appendix A), and route any deviation through a scoped, expiring exception (Chapter 26 § Make review predictable and proportional) rather than an unrecorded bypass.

## What the road looks like to a developer

A developer meets the road as a few declarations. The mortgage team's agent declares its AgentSpec `mortgage-evidence-agent@0.1.0`; a Skill requirement `mortgage.evidence.read@^0.1`, which is a compatible range rather than a digest (Chapter 8 pins the digest per run); the tool `mortgage.case.read@1` at effect risk class R1 (Chapter 22); the knowledge snapshot `mortgage-policy@approved-2026.09`; budgets; and the permissions it needs. Those permissions are a ceiling, intersected with the caller's grants at run time (Chapter 21); declaring them grants nothing. The platform compiles these declarations to the Chapter 3 contracts, and those contracts, not the SDK's method names, are the stable interface.

The command line walks the golden path, from `agentctl init mortgage-evidence-agent` through `agentctl promote --from staging --to production --canary 5%` to `agentctl rollback mortgage-evidence-agent@0.1.0 --to 0.0.9`. Build one immutable artifact, pin everything listed in Chapter 27 § Versioned objects, and bind endpoints, identities, secrets, sources, quotas, regions, and review queues only at deployment.

## Test the contracts before you test the model

Most defects are cheaper to catch without a model. The platform makes those tests cheap to write by supplying the harnesses: tool mocks, seeded simulation, a controllable clock, fault injection, and recorded-trace replay. The full set of evaluation levels, and which gate each feeds, is defined in Chapter 25 § Layer tests from contracts to outcomes.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Framework portability | Public agent SDKs differ in cancellation, streaming, tool, approval, and error semantics. A shared contract does not make them interchangeable; only adapter conformance tests demonstrate parity, and any gap must be recorded as a known limitation rather than assumed away. | R29; R31; R32 |

The discussion above draws on R29; R31; R32. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The suite below makes that evidence row executable. It drives any adapter with scripted test models and checks four promises of the Chapter 3 seam: a typed disposition, reported usage, cancellation that reaches the model call, and SDK errors mapped to the platform's result shape. A failed check is reported as a named gap to publish as a known limitation of that adapter.

[[EXAMPLE:adapter-conformance]]

## If this fails in production

1. Check that the run's RunManifest references a ReleaseManifest whose every pin resolves. A run without one bypassed the road.
2. Compare the artifact digest across environments. A difference means the one-artifact rule broke at build or binding.
3. Run the adapter conformance suite against the deployed adapter version. A gap such as dropped cancellation is a platform defect, not an application defect.
4. For behavior inside a run, follow Chapter 24 § Debugging method. Do not edit the prompt until the evidence locates the failing responsibility.

## What to verify before production

**✓** One immutable artifact crosses every environment; endpoints, identities, secrets, sources, quotas, regions, and review queues bind at deployment.

**✓** SDKs, adapters, model aliases, tool schemas, Skills, MCP servers, policy bundles, evaluators, and knowledge snapshots are pinned in the ReleaseManifest.

**✓** A model or provider swap ships as a behavior change with evaluation, canary, and rollback — never as configuration.

**✓** Adapter conformance suites cover cancellation, tools, streaming, approvals, errors, telemetry, usage, and version behavior.

**✓** Every golden-path stage emits its evidence artifact; a stage that produces no evidence is not complete.

## Put the idea to work

1. Take one existing agent and list which of the fifteen platform capabilities it reimplements locally. Estimate the cost of replacing each with the platform service.
2. Add a streaming check to the conformance suite, run it against a second framework's adapter, and record each gap as a known limitation.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Who owns a Skill: the platform, the domain, or the application? | The platform owns the registry, manifest schema, signing, and resolution; the domain-capability owner owns content, evaluation suite, and support window; the application declares requirements and acceptance. |
| What makes a paved road adopted rather than mandated? | It removes work the team would otherwise do — identity, policy, tracing, durable execution, release — while leaving domain behavior, topology, and acceptance to the team. A road that constrains domain decisions gets bypassed. |
| How do you detect a team bypassing the paved road? | Runs without a ReleaseManifest, tools unknown to the gateway registry, SDK calls outside AgentRuntime in dependency scans, and traces without platform correlation. |
| What does the golden path make visible that a convenient SDK hides? | Authority, versions, risk, evidence, and cost. An SDK that hides them does not remove the complexity; it relocates it to production incidents. |
| When is framework portability proven? | Only when adapter conformance tests pass across cancellation, tools, streaming, approvals, errors, telemetry, usage, and version behavior. Parity is never inferred from documentation. |

## Where this leads next

The paved road standardizes how an agent is built, tested, and released. It does not yet say how reusable behavior travels between agents without copy-and-paste; Chapter 8 packages it as versioned Skills with explicit contracts and lifecycle controls.

# 08 — Package Capabilities as Versioned Skills

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Teams begin copying prompts and tool wrappers between agents. Results diverge, fixes do not propagate, and no owner can prove which behavior reached production. Harborlight introduces a Skill as the unit of reusable capability. |

|  |
| --- |
| **THE DESIGN CHOICE** Make the Skill manifest the versioned capability contract and resolve exact releases through policy and evaluation evidence. |

## Why a prompt is not a reusable capability

Prompts and tool wrappers become hard to govern as soon as several teams copy
them. A Skill gives a meaningful capability an owner, an interface, a release,
and evidence that it was tested. This chapter explains what belongs in that
package and when versioning the whole capability is more useful than versioning
an instruction string by itself. A small prompt edit can alter tool selection,
data exposure, or output shape even though no application code changed.

Skills separate reuse from copy-and-paste. An application requests a capability such as `mortgage.evidence.read`; it does not embed a specific prompt and connector.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Skill Registry and resolver | semantic discovery to policy-bound resolution | Skill family · registry partition | one Skill version | SkillManifest · SkillRequirement · SkillRelease |

## The Skill manifest

A Skill is the smallest independently owned and versioned package that lets an agent perform a meaningful capability. Its manifest names interface schemas, instructions, eligible tools, knowledge sources, optional workflow template, policy constraints, risk ceiling, observability fields, evaluation suite, owner, and immutable digest.

That list is abstract until you see one. A manifest is a declaration, not code:

YAML · a Skill manifest, abridged

```yaml
skill: mortgage.evidence.read
version: 0.1.0
digest: sha256:9f3c...            # immutable; the version alias may move, this cannot
owner: mortgage-platform-team

interface:
  input:  MortgageEvidenceRequest@1
  output: MortgageEvidenceBundle@1

requires:
  tools:     [mortgage.case.read@1, mortgage.document.read@1]
  knowledge: [mortgage-policy@approved-2026.09]
  runtime:   {max_turns: 6, deadline_s: 45}

policy:
  data_classes: [mortgage_financial]
  regions:      [us]             # resolution fails outside these, it does not warn
  # highest effect risk class (R0–R4, Chapter 22) this Skill is certified for;
  # resolution refuses any requirement above it
  risk_ceiling: R1

evaluation:
  suite: mortgage-evidence-regression@1
  gates: {accuracy: 0.94, cross_tenant_leak: 0}
```

Three things in that file are doing more work than they appear to. The
`digest` is what a run actually pins, so an alias moving under you cannot
change behavior mid-flight. The `requires` block is exhaustive: a tool not
listed there is outside the step's eligible set, so the Tool Gateway refuses
the call, which is what makes the manifest a contract rather than
documentation. And `evaluation.gates` means promotion is decided by evidence,
not by a reviewer's judgment on the day.

Lifecycle is not in the manifest. The manifest is immutable and digested, so its state lives in the registry's release record (SkillRelease), which changes as evidence arrives.

Every change, even one instruction sentence, produces a new digest and must re-pass certification. The version number communicates interface compatibility only: MAJOR for a breaking input or output schema change, a widened `requires` set, or a raised risk ceiling, each of which makes consumers re-run their policy review; MINOR for compatible additions; PATCH for instruction or example changes that keep the interface. Behavioral compatibility is never inferred from the number; the evaluation gates establish it and the release records it.

### Skill, tool, agent, pack — which is which

| **Unit** | **What it is** | **Contract** | **Owner** | **Enforced by** |
| --- | --- | --- | --- | --- |
| Tool | One typed operation with effect semantics | ToolManifest (Chapter 22) | Tool owner | Tool Gateway on every call (Chapters 2, 22) |
| Skill | Instructions, interface, eligible tools, knowledge, policy, and evaluation for one reusable capability, executed inside an agent step | SkillManifest | Domain-capability owner | Resolver (this chapter), then Tool Gateway |
| Agent | A configured worker that runs bounded steps and requires Skills | AgentSpec, executed as AgentStepRequest (Chapter 3) | Application team | AgentRuntime |
| Skill Pack | Compatible, co-released Skills plus shared policy and evaluations | SkillPackManifest (Chapter 9) | Pack owner | Registry and release (Chapter 27) |

One deterministic operation with an effect is a tool; model judgment over several tools or sources, reused across agents, is a Skill; anything that owns a run, its acceptance, and its topology is an agent. Chapter 5's capability catalog is the discovery view across the tool and Skill registries; the registries stay separate because their contracts and enforcement points differ.

### Discovery is not permission

This is the distinction the chapter turns on: conflating discovery with resolution is how
governed capability quietly becomes ungoverned.

[[DIAGRAM:skill-resolution|Figure 8-1 — Discovery proposes candidates; resolution pins exactly one version, or fails]]

**Discovery** is semantic and broad. It searches a catalog for Skills that
might satisfy a stated need, and it may legitimately return several. It answers
*what exists*. Its candidates are input to resolution, not a menu for the
model. When a model must choose among Skills, it sees only a shortlist that
resolution has already made eligible (Chapter 5 § Capability and API catalog;
AP-12 in Chapter 17).

**Resolution** is deterministic and restrictive. Given one requirement and the
run's envelope, it filters by tenant, purpose, subject and actor grants, data
class, region, risk, compatibility, release stage, health, and cost — then pins
exactly one version by digest. It answers *what this run may use, right now*.

| | Discovery | Resolution |
| --- | --- | --- |
| Input | A capability need in natural terms | A requirement plus the run envelope |
| Method | Semantic search over the catalog | Deterministic policy evaluation |
| Output | Zero or more candidates | Exactly one pinned digest, or a failure |
| May a model influence it? | Yes — it can describe the need. It never sees unfiltered candidates. | **No** |
| Failure mode | Returns nothing useful | Fails closed, with the rule that refused |

The asymmetry matters. Discovery may be fuzzy because nothing it returns is yet
permitted. Resolution may not, because its output is what will actually run.
A system that lets a model pick from discovery results has skipped the gate and
is back to ungoverned capability with a registry in front of it.

The pinned release is compiled into the step. Its instructions enter the ContextManifest at trust tier 2 (Chapter 6 § The trust hierarchy of instructions); its `requires.tools` becomes the step's eligible tool versions and its `runtime` block the step's bounds in the AgentStepRequest (Chapter 3 § The request is bounded before the model sees it); its digest is recorded in the RunManifest (Chapter 4 § RunManifest).

Resolution decides which Skill may run. It authorizes none of the calls that Skill proposes: each still passes the six gates at the Tool Gateway (Chapter 2) against the subject, purpose, and exact resource (Chapter 22). Because Skill instructions direct behavior, Skill content is executable supply chain, which is why Chapter 9 signs and attests packs.

A Skill is bound four times, and each binding fixes something different:

| **When a Skill is bound** | **What is fixed** |
| --- | --- |
| Build (Chapter 7) | A requirement: capability plus compatible version range, not a digest |
| Release (Chapters 9, 27) | The exact Skill and pack versions eligible for this release |
| Plan compile (Chapter 12) | Each plan node's requirement, bound to one release from that set |
| Run (this chapter) | Resolution against the run envelope pins one digest, recorded in the RunManifest and never re-resolved for the life of the run |

Each later binding may only narrow the earlier one.

### Skill lifecycle

Draft → Certified → Staged → Active → Deprecated → Revoked is evidence-driven. Each transition requires an artifact rather than an approval conversation. When a Skill serves a use case at tier T3 or T4 (Chapter 26 § Match the control to the risk), the required artifact includes a recorded risk approval.

| State | Means | What moves it forward |
| --- | --- | --- |
| **Draft** | Authored, not trusted | Passing the certification suite |
| **Certified** | Evidence exists; not yet deployed | A staging release decision |
| **Staged** | Running in staging, shadow, or a limited canary | Canary evidence within gates |
| **Active** | Resolvable by production runs | A successor release, or an owner decision to retire |
| **Deprecated** | Not resolvable for new runs; runs that pinned it keep executing that digest | The compatibility window expiring |
| **Revoked** | Not resolvable; in-flight runs pinned to it pause or migrate by risk class | — |

Certification includes contract, unit, simulation, trajectory, threat, failure-injection, load, and operator-readiness checks (levels defined in Chapter 25 § Layer tests from contracts to outcomes). Deprecation retains a compatibility window for active runs — a long-running mortgage evidence review started three weeks ago must finish on the version it pinned. Revocation removes the Skill from all resolution and may trigger workflow pause or migration by risk class. It normally follows the compatibility window; revoking earlier is the one transition that can affect a run already in flight, which is why it is reserved for a defect serious enough to justify that. Revocation is the Skill-scoped case of Chapter 23 § Stop new risky work without abandoning effects; the rule that rollback changes only new work is Chapter 27 § Roll back assignment, not history.

### Skill contract surface

- `describe(requirement) -> candidates`
- `resolve(requirement, run_envelope) -> SkillRelease`
- `bind(release, step_request) -> AgentStepRequest`. Skills are not called directly; the bound request is executed by AgentRuntime (Chapter 3).
- `evaluate(release, dataset_version) -> EvaluationResult` (Chapter 25)
- `promote(release, stage, evidence) -> PromotionDecision` (Chapter 27), where the evidence includes Chapter 25's ReleaseGateDecision

The registry scales as a read-heavy service in the global control tier with immutable manifests, version indexes, cached eligibility metadata, and regional last-known-good replicas. Runtime execution remains in regional execution cells.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Terminology | Skill is a platform-owned package in this book. It is not an OpenAI Agents SDK primitive and is not identical to A2A AgentSkill metadata or Skills over MCP. Interchange requires an explicit adapter and loss analysis. | R05; R07 |

The discussion above draws on R05; R07. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The resolver filters by capability, purpose, region, risk ceiling, and data class, then picks the highest eligible SemVer. Production resolution also takes the run envelope (subject and actor grants, tenant), evaluation, health, cost, and rollout policy, which the example omits. Lifecycle state sits in the registry's release record, so promotion never moves a digest.

[[EXAMPLE:skills-registry#resolution]]

## If this fails in production

1. Read the pinned digest and the recorded requirement and envelope from the RunManifest. Re-run resolution as of the run's start and compare: a different answer means the registry changed underneath; the same answer locates the defect in that Skill version.
2. Diff Skill manifests across a regression.
3. Verify no hidden tool, knowledge, or policy dependency exists outside the manifest.

## What to verify before production

**✓** Every Skill has an owner, immutable version, digest, lifecycle state, and compatibility window.

**✓** Inputs, outputs, risk ceiling, data, region, and observability are explicit.

**✓** Discovery is semantic; resolution is deterministic and policy-bound.

**✓** Tool and knowledge dependencies are pinned and compatible.

**✓** Contract, trajectory, threat, failure, and load evidence gate promotion.

## Put the idea to work

1. Author a Skill manifest for mortgage evidence retrieval.
2. Define a certification suite that catches a cross-tenant retrieval defect.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| What is a Skill? | A versioned capability package combining contract, instructions, tools, knowledge, policy, workflow, tests, release evidence, and ownership. |
| How is Skill discovery different from resolution? | Discovery finds semantic candidates; resolution applies deterministic eligibility, compatibility, health, policy, and release rules to pin one version. |
| Does resolving a Skill authorize its tool calls? | No. Resolution selects which Skill version may run; every tool call it proposes still passes the Tool Gateway's validation, authorization, and effect controls. |
| How should a Skill be tested? | Contract, unit, simulation, trajectory, threat, failure-injection, load, and operator-readiness checks (levels in Chapter 25). |
| When should behavior remain application-specific? | When it encodes one product transaction, unstable workflow, private data boundary, or ownership model that should not be generalized. |

## Where this leads next

Individual Skills are governable; Chapter 9 composes them into domain packs without dissolving ownership or compatibility boundaries.

# 09 — Turn Skills into a Coherent Domain Platform

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Harborlight needs a complete domain experience, not isolated Skills. Evidence retrieval, document validation, income and property checks, policy explanation, underwriter-package preparation, and document requests must ship as a compatible, evaluated pack. |

|  |
| --- |
| **THE DESIGN CHOICE** Ship domain behavior as immutable Skill Packs with compatibility, policy, evaluation, and promotion metadata. |

## Why domain capabilities need to ship together

One Skill can be useful; a domain workflow needs several Skills to agree about
schemas, policy, terminology, evaluation, and operations. This chapter shows
how to compose those pieces into a Skill Pack that can be promoted as one
release.

Shipping related Skills together is less about convenience than compatibility. Suppose document validation begins returning a new evidence schema while income verification still expects the old one. Independent releases can leave a run in the gap between them. A pack pins versions known to work together, tests shared workflow and policy as one behavior, and gives operators one unit to promote or roll back.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Skill Pack Registry and release pipeline | pack authoring to tenant/runtime use | domain pack · tenant rollout cohort | one pack release | SkillPackManifest · CompatibilityReport · EvaluationSuite |

## What compatibility means

A pack build produces a CompatibilityReport; any failed check blocks the pack from certification.

| **Check** | **Fails when** |
| --- | --- |
| Skill-to-Skill schemas | A producer's output schema does not satisfy the consumer's input schema, as in the evidence-schema gap above |
| Tool schemas | Two Skills require incompatible versions of one tool |
| Policy obligations | Skills declare conflicting data-class or region constraints |
| Workflow contracts | A workflow template expects a Skill output the pack does not provide |
| Knowledge versions | Skills pin different snapshots of the same source |
| Runtime and model requirements | Skills need different adapter or model capabilities |
| Deprecation windows | A pinned Skill's compatibility window ends before the pack's support window |

This is Skill-to-Skill compatibility inside a release. Chapter 27's release compatibility check is a different test, between a run's pinned release and the workers that may execute it.

## From one capability to a coherent domain experience

A Skill Pack composes a coherent domain experience. Harborlight’s mortgage-evidence pack pins the Skills named above, together with shared policy, taxonomy, knowledge strategy, workflow templates, evaluation datasets, dashboards, and runbooks.

A pack is not a directory of prompts. The pack manifest declares dependency constraints, schema compatibility, required runtime capabilities, data and region policy, risk ceiling, evaluation gates, release aliases, owner, and support window. A pack can expose a smaller capability surface to each agent even though the complete domain distribution contains more Skills: each AgentSpec names the pack Skills it requires, and resolution refuses any other Skill for that agent's steps, so least agency (Chapter 2, principle 2) holds inside a pack. The same structure fits any domain where several Skills must agree on schemas and policy.

### Installing a pack grants nothing

The most important property of a pack is the one it does *not* have. Installing
a Skill Pack makes its capabilities **resolvable**; it does not make them
**permitted**, and it grants no access to the data or tools those Skills use.

This is worth stating plainly because the intuition from package managers points
the other way. Installing a library gives you its code and, transitively, its
capabilities. Installing a pack gives you a catalog entry. Every Skill in it
still resolves through the same policy evaluation as any other, against the
installing tenant's own grants.

| Installing a pack does | Installing a pack does not |
| --- | --- |
| Add its Skills to the discovery catalog | Grant access to any data source |
| Publish its manifests, schemas and digests | Grant any tool permission |
| Make its evaluation suites available | Bypass region or data-class policy |
| Declare its dependency and risk ceiling | Change the installing tenant's grants |

A business unit that installs the mortgage-evidence pack and has no entitlement
to the income-verification source gets a pack whose income-verification Skill will not resolve for
its runs. That is the correct outcome, and it is why sharing a pack across
business units is a policy and data-boundary review rather than a package
install.

The refusal should surface before work starts, at plan compilation (Chapter 12 § Compile-time checks) or admission, naming the rule that denied it, never mid-run. The installing tenant's grants are combined by intersection with the subject's and actor's (Chapter 21).

### Pack lifecycle, ownership, and release

A lifecycle state (Chapter 8) is a version's trust status; an alias is a pointer that says which pack version an environment or tenant cohort resolves. Moving an alias is a promotion and needs the same evidence, through Chapter 27's stages: shadow, canary, tenant cohort, and production. Rollback moves the alias back.

An active pack may reference only active Skills, which the example enforces. To deprecate one Skill, release a new pack version that drops or replaces it; runs pinned to the old pack finish on it (Chapter 27 § Roll back assignment, not history).

Each Skill keeps its owner. The pack owner owns the CompatibilityReport, shared policy, pack-level evaluation, and the support window.

The ReleaseManifest pins pack versions (Chapter 27). Each run resolves Skills only from the pinned pack and records the pack version and Skill digests in its RunManifest.

A pack is executable supply chain because Skill instructions direct behavior (trust tier 2, Chapter 6): sign it, attach SBOM and provenance, and verify them at promotion (Chapter 27 § Release attestation verification).

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Distribution security | A Skill Pack is executable supply chain: pin dependencies and tool schemas, produce SBOM and signed provenance, scan transitive content and binaries, enforce publisher trust, and support revocation without rewriting historical runs. | R16; R17 |

The discussion above draws on R16; R17. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

`register_pack` refuses unknown Skills, and `set_pack_state` refuses to activate a pack that references any non-active Skill. `resolve_pack` returns deprecated content only in explicit replay mode, which is Chapter 8's compatibility window in code.

[[EXAMPLE:skills-registry#packs]]

## If this fails in production

1. Expand the pack dependency graph and locate the incompatible version.
2. Compare pack alias history with the pack version and Skill digests recorded in each affected run's RunManifest.
3. Run the pack-level evaluation suite on the failing tenant slice.

## What to verify before production

**✓** The pack manifest pins exact compatible Skill and dependency versions.

**✓** Shared policy, knowledge, workflows, and evaluations are explicit artifacts.

**✓** Installation does not grant runtime authority.

**✓** Promotion, deprecation, rollback, and tenant rollout use aliases and evidence.

**✓** Pack-level failures can be isolated without disabling unrelated capabilities.

## Put the idea to work

1. Compose a mortgage-evidence Skill Pack and define compatibility rules.
2. Design a deprecation plan for one Skill without breaking the pack.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why create a Skill Pack? | To distribute a compatible domain capability set with shared policy, knowledge, workflows, evaluation, and lifecycle controls. |
| What must pack compatibility cover? | Skill and tool schemas, policy obligations, workflow contracts, knowledge versions, runtime and model requirements, and deprecation windows. |
| Can installing a pack grant authority? | No. Installation exposes definitions; tenant policy and each run envelope still determine eligibility and exact authorization. |
| How should packs be promoted? | As signed immutable releases promoted through shadow, canary, tenant-cohort, and production aliases backed by evaluation evidence; rollback reassigns the alias to the prior version. |
| What is the main pack anti-pattern? | A monolithic prompt-and-tools bundle with hidden dependencies, no owner, no tests, and no independent versioning. |

## Where this leads next

The platform now supplies the units every later pattern binds to: an agent runs one bounded step through AgentRuntime, with Skills resolved from a pinned pack and tools called through the Tool Gateway. Part IV asks what shape the reasoning inside that step, and the workflow around it, should take, starting with the smallest bounded loop in Chapter 10.
