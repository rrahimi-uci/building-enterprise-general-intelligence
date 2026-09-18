# PART VIII — RUNNING THE SYSTEM IN THE REAL WORLD

Shipping the first version is the easy milestone. The hard work is operating
the system when usage grows, people change roles, vendors drift, and a run is
still active during a deployment. This Part connects governance, release and
recovery, capacity, reliability, and cost so the platform remains usable after
the demo has become a dependency.

# 26 — Make Governance Part of How the Platform Runs

> **Evidence context:** NIST AI RMF and its Generative AI Profile are voluntary risk guidance; ISO/IEC 42001 specifies an AI management system; the EU AI Act source provides official implementation context. Applicability and legal obligations require qualified jurisdiction-specific review. **[R12][R13][R14][R40]**

## Why governance belongs in the operating model

Governance works when it changes what teams do, not when it produces another
committee packet. This chapter turns risk appetite into named decisions,
proportional controls, evidence, exceptions, and review cadence. It becomes
especially important when several teams share a platform and no single team
can see the full consequence of a release.

## Governance starts with clear decisions and owners

Good governance should make routine, low-risk change faster because teams know the path in advance. It becomes bureaucracy when every change enters the same queue or exceptions have no owner or expiry. Start by naming the decision, the accountable role, the evidence needed, and the time boundary. Then scale review to the risk. The operating model is working when people can predict how a change will be evaluated and see who must act next.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| A named accountable owner per decision class; a named risk authority owns exceptions | delegated domain autonomy to enterprise risk appetite | risk tier · domain · release | one decision, one exception, one release | risk classification · PolicyDecision · ValidationReport · exception record |

Governance is easiest to understand as a control loop, not as a meeting. A team first states the outcome it is accountable for, then identifies what could make that outcome harmful, chooses controls proportional to the consequence, collects evidence while the system runs, and revises the controls when evidence or circumstances change. The loop is useful only when each step has an owner and a record that another person can inspect.

Consider Harborlight's mortgage-evidence assistant. The domain owner may accept a draft evidence classification, but the assistant must not make or record a lending decision. The data owner decides which application and policy records may enter context; the risk owner classifies the workflow; the resource owner defines whether a document-request tool is available; and the release owner verifies that the assembled controls were tested. No single committee needs to understand every underwriting rule, but every decision has a clear owner and an evidence boundary.

| **If the team asks…** | **Governance must answer…** | **Evidence that closes the question** |
| --- | --- | --- |
| “Can this use case run?” | What outcome, data, autonomy, and consequence define its risk tier? | Use-case record, risk assessment, prohibited-use boundary |
| “Can this tool be called?” | Who owns the resource, and what authorization and reconciliation does the effect require? | Tool contract, capability decision, effect policy |
| “Can this release go live?” | Did the candidate satisfy the required technical, safety, and business gates? | ValidationReport, approvals, canary plan, rollback owner |
| “Why was an exception allowed?” | What exact gap was accepted, by whom, with which compensating controls, and until when? | Time-bounded exception record and monitoring result |

This framing also explains why a central board alone scales poorly. A board can set the risk vocabulary and approve high-consequence boundaries, but it cannot supply the local knowledge needed for every data source, business effect, or acceptance criterion. Central services make decisions consistent; domain owners make them meaningful.

## Share responsibility without losing accountability

Governance makes decisions explicit, proportional, evidence-based, and reversible. It accelerates safe delivery with reusable risk tiers, policy, review paths, and evidence rather than sending every prompt edit to one committee.

[[DIAGRAM:governance-model|Figure 26-1 — Federated governance with centralized control services]]

| **Decision** | **Accountable owner** | **Evidence** |
| --- | --- | --- |
| Business outcome/acceptance | Domain/product owner | Outcome contract, tests, business SLO |
| Risk tier/autonomy | Risk owner | Threat/data/effect assessment and controls |
| Platform contracts | Platform product owner | RFC, compatibility/migration, SLO |
| Data/context/memory purpose | Data owner | Source, ACL, purpose, retention, deletion, quality |
| Tool/effect authorization | Resource owner | Tool contract, permission, idempotency/reconcile, approval policy |
| Model/provider/route | Model governance owner | Capability, evaluation, data terms, region, cost, resilience |
| Evaluator/dataset truth | Domain evaluation owner | Lineage, rubric, calibration, uncertainty |
| Production promotion | Release owner | ValidationReport, required approvals, canary, rollback |
| Exception | Named risk authority | Scope, rationale, compensating controls, expiry, monitoring |

## Match the control to the risk

| **Tier** | **Typical use** | **Minimum governance** |
| --- | --- | --- |
| 0 Deterministic/assistive | No model or harmless ideation | Standard engineering/data policy |
| 1 Bounded advisory | Low-impact content with verification | Owner, basic evaluation, data controls, monitoring |
| 2 Operational recommendation | Business decision support/internal tools | Domain acceptance, security/privacy, regression, recourse |
| 3 Protected action | Financial, identity, customer, employee, infrastructure effect | Least privilege, exact approval, effect ledger, strong eval, canary, incident plan |
| 4 High consequence/systemic | Regulated, safety-critical, large-scale autonomous/cross-boundary | Executive/risk approval, independent assurance, strict envelope, recovery exercise |

Assess incorrect-outcome impact, sensitive data, protected effects, legal relevance, autonomy, exposure, scale, reversibility, multi-agent/tool complexity, and human detectability. Risk is not the model name.

## Make review predictable and proportional

Principles define non-negotiable outcomes; standards define reusable contracts; policy-as-code decides eligible models, data, tools, actions, budgets, and approvals; application configuration selects within the envelope; exceptions are scoped, monitored, owned, and expiring. Review outcome/acceptance, deterministic boundary, state/effect ownership, identity/delegation, context/memory, tool/MCP/A2A trust, threats, evaluation truth, observability/privacy, recovery, release, capacity/cost, human oversight, and portability.

Operate per run (admission/policy/effects/acceptance), daily/weekly (SLO, quality, safety, cost, incidents, evaluator health), per release (classification, regression, security/privacy, compatibility, canary/rollback), quarterly (portfolio value/risk and platform roadmap), and annually/material change (policy, law, threat, recovery, independent assurance).

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Regulatory applicability | NIST AI RMF and its Generative AI Profile are voluntary guidance; ISO/IEC 42001 specifies a management system; the EU AI Act creates binding obligations that vary by risk category and by whether the enterprise acts as provider or deployer. Mapping a control in this book to a clause is engineering evidence, not legal advice, and qualified jurisdiction-specific review remains required. | R12; R13; R14; R40 |

The discussion above draws on R12; R13; R14; R40. Appendix K lists the complete sources and records their authority, version, and scope.

## If this fails in production

Governance fails as queues and exceptions rather than as stack traces. Diagnose it the same way.

1. When a release is blocked, find which single decision lacks a named owner instead of escalating the whole release.
2. When the same exception recurs, treat it as a missing standard rather than a repeated approval.
3. When risk tier and control effort disagree, re-score impact, reversibility, and human detectability before changing the tier.
4. When review takes longer than delivery, check whether evidence is produced by the pipeline or assembled by hand. Hand-assembled evidence is the usual cause.

## What to verify before production

**✓** Every decision class in the accountability table has one named owner and one required evidence artifact.

**✓** Risk tier is derived from impact, protected effects, autonomy, exposure, scale, reversibility, and human detectability — not from the model name.

**✓** Exceptions are scoped, compensated, monitored, owned, and expiring. An exception without an expiry is a silent policy change.

**✓** Policy-as-code decides eligible models, data, tools, actions, budgets, and approvals; application configuration only selects within that envelope.

**✓** Each cadence — per run, daily or weekly, per release, quarterly, annually — has a named owner and a defined input.

## Put the idea to work

1. Classify three current use cases into risk tiers and list the minimum governance each one triggers. Where two people disagree, the tier definition is the defect.
2. Take one standing exception and write either its expiry date or the standard that would retire it permanently.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why federate governance rather than centralize it? | Central review of every prompt edit becomes the bottleneck and is abandoned. Centralize reusable control services, risk tiers, policy, and evidence; federate domain acceptance, tools, knowledge, and SLOs to accountable owners. |
| What makes a risk tier defensible? | It is derived from consequence and reversibility — incorrect-outcome impact, sensitive data, protected effects, autonomy, exposure, scale, and human detectability — rather than from the model or framework in use. |
| Why must every exception expire? | An exception that never expires is an undocumented policy change with no owner and no review. Expiry forces either the standard to change or the compensating control to be retired deliberately. |
| What separates principles, standards, policy-as-code, and configuration? | Principles state non-negotiable outcomes; standards define reusable contracts; policy-as-code decides what is eligible at runtime; configuration selects within that envelope. Only the first two are argued; the last two are executed. |
| How do you know governance is accelerating delivery? | Time from evidence-complete to approved is falling, exceptions are trending down as standards absorb them, and the same evidence serves engineering review, risk review, and audit without rework. |

## Where this leads next

Governance defines who may release change; Chapter 27 makes releases immutable, promotable, observable, reversible, and recoverable.

# 27 — Release New Behavior Without Breaking Work in Flight

> **Evidence context:** The incident lifecycle aligns with NIST SP 800-61 Rev. 3’s integration of incident response into cybersecurity risk management; agent-specific containment and recovery remain workload-defined. **[R42]**

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  A new release changes a tool schema and workflow decision. Active runs still contain the old event history. Northstar deploys compatible workers, pins release manifests, canaries new starts, and rolls back assignment without rewriting history. |

|  |
| --- |
| **THE DESIGN CHOICE** Release immutable bundles with compatibility evidence; roll back new assignment while active runs remain pinned to compatible code. |

## Why a release is more than a deployment

An agentic release changes more than application code: it can change prompts,
tools, policies, model routes, schemas, and the behavior of work already in
flight. This chapter shows how to package those changes, prove compatibility,
canary new work, and recover without rewriting history or abandoning active
runs.

## Keep releases immutable and workers compatible

[[DIAGRAM:release-recovery|Figure 27-1 — Immutable release promotion and recovery without rewriting active history]]

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Release Registry and compatible worker pools | candidate artifact to production assignment | release cohort · workflow build · cell | one release cohort | ReleaseManifest · CompatibilityMatrix · RolloutPlan |

## Treat the full behavior as the release

For an agentic system, behavior is spread across more than application code. A model route, prompt, Skill, tool schema, policy bundle, evaluator, and workflow definition can each change what the user experiences or what the system may do. A release therefore pins the whole graph. That makes a production result reconstructable and gives rollback a precise meaning: restore known behavior, not merely an older container image.

A production release includes more than application code: agent and Skill versions, prompts and instructions, SDK adapter, workflow build, model route and fallbacks, tool and policy versions, schemas, sandbox image, knowledge strategy, evaluation suite, dashboards, runbooks, rollout, and rollback. Northstar records these in an immutable ReleaseManifest and pins the manifest to each run.

CI verifies types and contracts, deterministic replay, policy and grant subsets, tool and effect semantics, prompt and trajectory regressions, threat cases, performance, container signatures, provenance, and migration compatibility. CD promotes the exact same signed artifacts through shadow, canary, tenant cohort, and regional stages.

### Rollback and active runs

Rollback changes the release assigned to **new work**. Active workflows continue on compatible workers or use an explicit tested migration. Rewriting history or silently changing a tool schema underneath an active run is not rollback. High-risk changes may pause affected runs until a compatible worker or reviewed migration is available.

Regional recovery fences the old writer, restores durable state with a compatible build, reconciles executing and unknown effects, verifies signals and task ownership, advances placement atomically, and resumes by risk tier. Recovery is rehearsed with evidence, not inferred from replica health.

### A release walkthrough

The distinction between a release and a deployment becomes concrete during a tool-schema change. Suppose the mortgage workflow changes `request_mortgage_document` so that the tool requires a new `document_kind` field. The release builder creates a new bundle containing the workflow build, tool schema, policy, model route, image, evaluation evidence, and rollback plan. The compatibility matrix records that workers serving old runs understand the old schema, while the new worker pool understands the new one.

| **Moment** | **Control** | **What must remain true** |
| --- | --- | --- |
| Candidate assembled | Resolve every dependency to a digest and test compatibility | The bundle can be reproduced and no mutable “latest” reference is admitted |
| New starts canary | Assign only a bounded tenant or traffic cohort | Existing runs remain on their pinned manifest; canary evidence is separately attributable |
| Canary finds a defect | Stop new assignment and restore the prior binding | Rollback changes placement, not the history or effects of an active run |
| Old run reaches a tool call | Route to a worker compatible with its manifest | A worker may support the run’s old contract, or a tested migration must be explicit |
| Region fails during a write | Fence the old writer, restore, reconcile, then advance placement | No effect is assumed absent merely because the request timed out |

This is why “roll back the model” is usually incomplete. If the prompt, tool schema, policy, workflow build, or retrieved knowledge strategy also changed, restoring one model identifier does not restore the behavior. The smallest safe rollback unit is the release bundle, while emergency deny and credential revocation remain separate controls that can take effect immediately and be recorded alongside the pinned release.

## A deployment shape that supports safe change

### A production topology that is easy to reason about

The topology has two different jobs. The control plane decides what may run and which immutable bundle a run receives; regional execution planes do the work within that decision. Keeping those jobs separate lets a release be globally described while state, queues, credentials, and model endpoints remain inside the required residency and failure boundary.

| **Layer** | **Owns** | **What it must not assume** |
| --- | --- | --- |
| Control plane | Registries, release bundles, evaluation gates, governance inventory, and promotion decisions | That a healthy registry means an execution region can safely resume effects |
| Regional execution plane | Admission, workflow history, queues, workers, retrieval, traces, and local service endpoints | That a replica is a compatible worker for every historical run |
| Source systems and effect boundaries | Business records, external writes, receipts, and reconciliation predicates | That a timeout proves the write was absent |
| Recovery controls | Fencing, deny/kill switch, credential revocation, placement, and resume policy | That normal deployment automation is sufficient during an incident |

The boundary is operational as well as logical. A regional worker should be able to verify a signed bundle from a local cache, but it should not invent a new policy when the control plane is unavailable. A high-risk admission may therefore fail closed, while a low-risk read-only task can use a documented last-known-good policy. That explicit distinction is more useful than a generic claim of “high availability.”

### Deployment guidance

* **Control plane:** globally available registry, release, evaluation, and governance services publish signed immutable bundles. Production workers pull approved versions; they do not edit control-plane definitions.
* **Regional execution planes:** keep prompts, state, artifacts, retrieval indexes, queues, traces, and model endpoints in the required residency boundary. Route each run to a home region and avoid transparent cross-region migration of in-flight state.
* **High availability:** run gateways, policy decision points, workflow front ends, and queue workers across zones. The workflow history and relational stores need tested backup/restore and defined regional failover; “multi-region” without replay tests is not a resilience claim.
* **Isolation:** namespaces are not the only boundary. Combine tenant-aware authorization, row-level security, separate encryption keys, network policies, workload identity, queue quotas, and—where risk requires—dedicated accounts/clusters.
* **Worker classes:** separate lightweight model/tool orchestration from browser/code execution, GPU inference, data processing, and high-risk connectors. Each class has an immutable image, resource limits, egress policy, and workload identity.
* **Secrets:** fetch just in time from a broker or exchange identity for a short-lived credential. Never bake secrets into images, prompts, tool manifests, checkpoints, or environment dumps.
* **Release:** deploy agent and workflow bundles using GitOps-style promotion, canaries, feature flags, and automated rollback. Keep old workflow code available until all compatible in-flight runs complete or migrate.
* **Disaster recovery:** define RPO/RTO separately for run history, business effects, artifacts, indexes, telemetry, and audit. Reconcile effects against source systems after recovery before resuming mutations.

### Suggested baseline stack—not a mandate

| **Concern** | **Typical choices** | **Selection criteria** |
| --- | --- | --- |
| Durable workflow | Temporal, DBOS, Restate, cloud durable functions/state machines | Replay/versioning, signals/timers, child workflows, visibility, language/runtime fit, operations |
| Agent graph/harness | LangGraph, OpenAI Agents SDK, Anthropic Agent SDK/Managed Agents, Microsoft Agent Framework, Google ADK, PydanticAI, LlamaIndex | Typed state, interrupts, tool ergonomics, model portability, trace quality, escape hatches |
| Events/queues | Kafka/Pulsar, cloud pub-sub/queues, NATS | Ordering, retention, throughput, replay, tenancy, ecosystem, residency |
| Policy | OPA/Rego, Cedar/Verified Permissions, cloud IAM plus domain service | RBAC/ABAC expressiveness, decision logs, latency, analysis/testing, tenant model |
| Workload identity | SPIFFE/SPIRE, cloud workload federation, service mesh identity | Short-lived credentials, federation, attestation, sender/audience binding |
| Operational state | PostgreSQL-compatible relational store | Transactions, RLS, JSON support, operational maturity, backup/restore |
| Artifacts | Versioned object storage | Immutability, retention lock, encryption, signed access, regionality |
| Retrieval | Search engine + vector index + optional graph | ACL correctness, freshness, hybrid search, lineage, deletion, scale |
| Sandboxing | Ephemeral containers or microVMs with egress proxy | Isolation strength, startup latency, observability, policy integration |
| Telemetry/evals | OpenTelemetry + trace/metric backend + evaluation service | Portability, privacy controls, async trace linking, dataset/experiment workflow |

## Version every artifact that can change behavior

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Safely change a system whose behavior depends on code, models, prompts, policies, schemas, tools, knowledge, and external services while preserving reproducibility and regulatory evidence. |
| Why it is difficult | Model aliases drift; prompt/tool combinations interact; long-running workflows span deployments; knowledge changes continuously; policies may need immediate revocation. |
| Design alternatives | Mutable latest configuration; environment snapshots; semantic versions; content-addressed bundles; feature flags; canary/shadow releases; full immutable run manifests. |
| Recommended architecture | Resolve every run to an immutable RunManifest of content digests and semantic versions. Promote signed release bundles through dev → QA → staging → canary → production using risk-tiered eval gates. Keep emergency policy/kill-switch controls separate and auditable. |
| Trade-offs | Pinning and compatibility management add storage and release discipline. They enable rollback, replay, investigation, and controlled experimentation. |
| Failure scenarios | Model alias changes behavior; tool schema breaks old prompt; replay uses current knowledge; policy rollback re-enables a forbidden action; active workflow cannot replay under new code. |
| Enterprise example | A regulated underwriting run stores the exact decision-service version, policy bundle, model route, prompts, retrieved document revisions, tool digests, approvals, and output hashes for examination months later. |

### Versioned objects

| **Object** | **Version rule** | **Promotion gate** |
| --- | --- | --- |
| Agent manifest | Semantic version + content digest | Contract, behavior, security, ownership review |
| Prompt/skill bundle | Immutable digest; declared compatible schemas/models | Regression and adversarial evals |
| Workflow code | Build artifact + replay/change version markers | Determinism, migration, fault-injection tests |
| Tool/connector | Semantic API version + implementation/image digest | Contract, auth, idempotency, sandbox, rollback tests |
| Model route | Provider model ID/version + decoding/config + fallback chain | Quality, safety, latency, cost, regional/compliance evals |
| Policy bundle | Signed version + effective period | Policy tests, separation of duties, emergency rollback |
| Data/schema | Versioned contract and migration | Backward/forward compatibility and lineage checks |
| Knowledge snapshot | Source revision/index build ID + ACL snapshot strategy | Freshness, ACL correctness, deletion propagation |
| Eval dataset/rubric | Immutable examples, provenance, reviewer/version | Coverage, leakage review, judge calibration |
| Runtime image | Signed digest + SBOM/provenance | Vulnerability, sandbox, supply-chain checks |
| Artifact | Content hash + schema + creator run/version | Classification, destination policy, retention |

### Promotion and continuous-improvement loop

Promotion is a chain of evidence, not a sequence of environments that an artifact happens to visit. Each stage asks a narrower question, and the answer travels with the same signed bundle to the next stage. A failed gate returns the candidate to revision; it does not create an undocumented production-only patch.

| **Stage** | **Question** | **Evidence** |
| --- | --- | --- |
| Build | Can the dependency graph be reproduced and attested? | Digests, lockfiles, SBOM, provenance, signature |
| Evaluate | Does the candidate satisfy its risk-tiered behavioral and security gates? | Dataset results, replay, threat cases, slice analysis |
| Shadow | What would the candidate do on representative traffic without effects? | Linked traces, drift signals, latency and cost forecast |
| Canary | Does bounded real traffic stay within acceptance and SLO limits? | Cohort-level metrics, effect safeguards, rollback trigger |
| Promote | Is the decision owned and recorded? | Approval, effective binding, release and audit record |
| Learn | Did production evidence justify a change? | Incident/eval case, reviewed proposal, new candidate—not direct mutation |

The last row closes the loop without allowing production to rewrite itself. A trace or conversation can become input to a curated dataset, but it becomes a release only after de-identification, review, evaluation, and promotion. That separation preserves both learning velocity and the ability to explain which version produced an earlier result.

### Governance controls

* Inventory every deployed agent, use case, owner, business purpose, autonomy level, tools, data classes, users, vendors, regions, SLOs, and risk tier.
* Map controls to NIST AI RMF Govern/Map/Measure/Manage, ISO/IEC 42001 management-system processes, security/privacy standards, and applicable sectoral rules. As of August 2026, most EU AI Act rules and enforcement apply; legal classification must be use-case specific.
* Require documented intended use, prohibited use, foreseeable misuse, human-oversight design, evaluation evidence, residual risk acceptance, and rollback owner before release.
* Produce an immutable evidence package per material run: request, identities, purpose, versions, policy decisions, source provenance, plan revisions, tool effects, approvals, output, metrics, incidents, and retention class.
* Separate telemetry access from business-data access; redact by default and support legal hold, deletion, residency, and customer-managed keys.
* Document explanations at the right level: evidence and rules for business decisions; trajectory summaries for operations; model internals are neither necessary nor sufficient.
* Never auto-train or rewrite production policies/prompts directly from live conversations. Curate, de-identify, review, evaluate, and promote changes through the same lifecycle.

### A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Artifact Registry | Immutable versions/digests for agent, prompt, skill, workflow, tool, schema, policy, model route, dataset, and runtime |
| Release Bundle Builder | Resolve dependencies, compatibility, SBOM/provenance, signatures, migration requirements, and rollout policy |
| Evaluation/Gate Service | Run risk-tiered quality, reliability, security, latency, cost, and compliance gates |
| Promotion Service | Move signed bundle through environments with approvals, canary/shadow, and rollback |
| Runtime Resolver | Resolve a run to one immutable manifest and regional endpoints; never serves mutable “latest” to an active run |
| Drift Monitor | Detect model/provider/tool/data/policy behavior or availability changes against baselines |
| Governance Inventory | Track use case, owners, data, autonomy, controls, evidence, exceptions, retention, and regulatory mapping |
| Emergency Control | Kill switch, deny policy, credential revocation, and safe rollback independent of normal release cadence |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/artifacts/{kind} | Register content-addressed artifact/version with owner, dependencies, compatibility, provenance, SBOM, signature, and lifecycle |
| POST /v1/release-bundles | Resolve a candidate manifest; fails on mutable/unavailable dependency, incompatible schema, missing control, or unsigned artifact |
| POST /v1/release-bundles/{bundle\_id}:evaluate | Start required eval, security, replay, migration, and operational tests for target risk/environment |
| POST /v1/release-bundles/{bundle\_id}:promote | Promote to environment/canary cohort using expected bundle state, gate evidence, approvers, and rollout plan |
| POST /v1/manifests:resolve | Return immutable RunManifest from tenant/use case/environment/region while recording resolution evidence |
| POST /v1/deployments/{deployment\_id}:rollback | Stop new assignment, restore prior binding, preserve in-flight compatibility, and create incident/evidence record |
| POST /v1/artifacts/{kind}/{id}/versions/{version}:deprecate | Set warning/end-of-new-use/end-of-support dates and enumerate impacted active runs/releases |
| POST /v1/governance/exceptions | Create time-bounded, scoped waiver with compensating controls, approvers, owner, evidence, and renewal prohibition/default |
| GET /v1/governance/inventory | Query deployed agents/use cases by owner, risk, autonomy, data class, region, vendor, controls, incidents, and review date |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ArtifactVersion | kind/ID/version/digest, URI, owner, source/build provenance, signature, dependencies, compatibility, risk, lifecycle; released content immutable |
| ReleaseBundle | bundle ID/digest, complete dependency graph, target use case/risk, migrations, rollout/rollback, build time, state |
| CompatibilityRule | producer/consumer kinds and ranges, schema/effect/replay constraints, test evidence, effective interval |
| EvaluationEvidence | bundle, required suite/version, environment, results/slices/confidence, pass/fail, artifact refs, expiry |
| PromotionDecision | bundle/environment, prior binding, gate digest, approvers, decision, canary cohort, time, rollback trigger |
| EnvironmentBinding | tenant/use case/environment/region, active bundle, traffic weights, effective interval, version |
| Deployment | binding/bundle, region/pool/build, status, capacity, start/end, health, rollback relation |
| GovernanceRecord | use case, owners, purpose, autonomy, users, data/tools/vendors/regions, risk, controls, reviews, evidence, incidents |
| ExceptionWaiver | exact control gap/scope, rationale, compensating controls, owner/approvers, start/expiry, usage count, status |
| DriftFinding | subject/version, baseline/window, metric/slice, magnitude/confidence, severity, action/owner |

### Compatibility and long-running execution

* Every run records a resolved bundle. A deployment change affects new runs only unless an explicit, tested migration updates an active run.
* Workflow compatibility includes replay behavior, activity names/schemas, state migrations, signals, and effect semantics—not just API request shape.
* Tool/model fallback is itself a versioned route with eval evidence. “Same family” or “newer model” is not proof of compatibility.
* Policies can impose emergency deny outside the pinned bundle; the run records both the original policy and the current higher-precedence denial.
* Knowledge snapshots may be “as-of,” “current under freshness policy,” or a recorded set of source revisions. The manifest states which reproducibility level applies.

### Scalability and control-plane resilience

* Registry/release/governance writes are low volume and strongly consistent. Reads are high volume: distribute signed bundles/manifests through regional caches/object storage keyed by digest.
* Workers verify bundle signatures/digests locally and keep a last-known-good cache. New high-risk runs fail closed if current policy/kill-switch state cannot be verified.
* Avoid a synchronous global registry call on every activity. Resolve once at admission, pass content addresses, and refresh only explicitly dynamic health/authorization data.
* Index dependency edges to answer “what uses this version?” before deprecation, incident containment, or vulnerability response. Run impact analysis asynchronously but from a consistent snapshot.
* Roll out by tenant/use case/risk/region cohorts with bounded canary volume. Automated rollback consumes streaming SLO/eval signals but never rewrites historical manifests.
* Keep release metadata, signatures, policies, and governance evidence replicated with tested backup/restore. Separate normal promotion permissions from emergency deny/rollback authority.
* Archive old artifacts only after all active-run, replay, audit, legal-hold, and rollback dependencies expire. Retain digest tombstones permanently enough to prevent ambiguous reuse.

|  |
| --- |
| **PRODUCTION CONSIDERATION**  Version the prompt, the model pin, the tool manifests, and the policy as one release artifact. Rolling back an agent means restoring all four together; a deployment that can change the model without changing the recorded version has no rollback, only a guess. |

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Supply chain | An SBOM describes components; SLSA provenance describes where and how an artifact was built. Use both, verify signatures and builder identity before promotion, and include model/prompt/Skill/policy/evaluation digests in the release manifest. | SLSA |

The discussion above draws on SLSA; CISA-SBOM. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start


### Release compatibility check

🐍 · implementation excerpt

```python
from __future__ import annotations

from pydantic import BaseModel


class ReleaseManifest(BaseModel):
    release_id: str
    agent_versions: tuple[str, ...]
    skill_pack_versions: tuple[str, ...]
    workflow_build: str
    sdk_version: str
    model_route_version: str
    tool_versions: tuple[str, ...]
    policy_version: str
    schema_versions: tuple[str, ...]
    evaluation_report_id: str


def compatible(run: ReleaseManifest, worker: ReleaseManifest) -> bool:
    return (
        run.workflow_build == worker.workflow_build
        and run.sdk_version == worker.sdk_version
        and set(run.tool_versions) <= set(worker.tool_versions)
        and set(run.schema_versions) <= set(worker.schema_versions)
    )
```

### Release attestation verification

🐍 · implementation excerpt

```python
from __future__ import annotations

import hashlib
from pydantic import BaseModel, Field


class ReleaseAttestation(BaseModel):
    release_id: str
    artifact_sha256: str
    signer_identity: str
    source_revision: str
    builder_identity: str
    sbom_ref: str
    provenance_ref: str
    dependency_lock_digest: str
    evaluation_evidence_refs: tuple[str, ...] = Field(min_length=1)


def verify_release_artifact(
    content: bytes,
    attestation: ReleaseAttestation,
    *,
    trusted_signers: frozenset[str],
    trusted_builders: frozenset[str],
) -> None:
    digest = "sha256:" + hashlib.sha256(content).hexdigest()
    if digest != attestation.artifact_sha256:
        raise ValueError("artifact digest mismatch")
    if attestation.signer_identity not in trusted_signers:
        raise PermissionError("untrusted release signer")
    if attestation.builder_identity not in trusted_builders:
        raise PermissionError("untrusted build platform")
    if not attestation.sbom_ref or not attestation.provenance_ref:
        raise ValueError("SBOM and provenance are required")
```

## If this fails in production

1. Resolve the exact release manifest and worker compatibility for the run.
2. Replay history before migrating workflow code.
3. Verify rollback stopped new assignment without changing active history.

## What to verify before production

**✓** Client and workflow contracts remain stable across SDKs, providers, engines, and connectors.

**✓** Idempotency, concurrency, asynchronous operations, deadlines, pagination, events, errors, and artifacts are consistent.

**✓** Each authoritative record and consistency boundary has one owner and store.

**✓** Partitions, queues, quotas, fairness, backpressure, and cells isolate workloads.

**✓** Compatibility, schema migration, fencing, regional recovery, and effect reconciliation are designed before deployment.

## Put the idea to work

1. Design CI/CD gates for an agent, Skill Pack, policy, and workflow release.
2. Write a regional recovery sequence that fences the old writer and reconciles effects.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| How do stable contracts make an agent platform portable? | Public run, task, and tool contracts and authoritative records remain provider neutral; SDK and model-specific objects stay behind adapters and gateways. |
| What conventions are essential for a long-running Run API? | Idempotent commands, expected versions, 202 operations, durable status and events, typed errors, deadlines, cancellation semantics, and immutable artifact references. |
| How would you choose stores for workflow, business state, artifacts, search, telemetry, and audit? | Match consistency, access, retention, rebuildability, write pattern, and scale; do not use queues as transactions, vectors as truth, traces as audit, or prompts as state. |
| Why use workload queues and regional cells? | Isolate risk and latency classes, control noisy neighbors, scale additively, enforce residency, bound blast radius, and keep critical execution dependencies local. |
| Describe safe regional failover during an external write. | Stop admission, fence the old writer, restore compatible durable state, reconcile executing and unknown effects and signals, atomically advance placement, then resume by risk tier. |

## Where this leads next

The release lifecycle is controlled; Chapter 28 sizes the system and optimizes cost, latency, capacity, and reliability around verified outcomes.

# 28 — Treat Performance as a Business Decision

> **Evidence context:** Little’s Law relates average items in a stable system to arrival rate and average time in system. The capacity equations in this chapter are planning approximations and must be calibrated by load tests. **[R43]**

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Demand triples at quarter end. Northstar must protect deadlines and tenant fairness while controlling tokens, tool calls, queue depth, and human load. Optimization is judged by verified business outcomes, not by token price alone. |

|  |
| --- |
| **THE DESIGN CHOICE** Optimize cost per verified success through shorter trajectories, selective context, deliberate routing, bounded concurrency, and safe degradation. |

## Why cost and latency have to be designed into the workflow

The cheapest token is not a cheap outcome if it creates a rework loop, a human
queue, or an unverified effect. This chapter connects latency, cost, capacity,
fairness, reliability, and verified business success, then uses that model to
choose routing, context, concurrency, and degradation strategies. It is where
the architecture meets the operating budget.

## Optimize the whole journey

[[DIAGRAM:reliability-economics|Figure 28-1 — Admission, bounded execution, and outcome-based operating feedback]]

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Admission controller and budget service | tenant demand to scarce shared capacity | workload class · tenant · queue | one admitted run | BudgetLease · CapacityPermit · DegradationDecision |

## Optimize the trajectory, not the token

A cheaper model call can make the workflow more expensive if it causes extra retrieval, repeated tool calls, evaluator retries, or human escalation. The unit of optimization is the accepted business outcome and the path taken to reach it. Measure cost and latency at each stage, then improve the bottleneck that changes the journey. This keeps local savings from shifting work—and risk—to a more expensive part of the system.

The useful objective is **cost and latency per verified successful outcome**, constrained by quality, safety, reliability, and compliance. A cheaper model can be more expensive if it causes more turns, retrievals, retries, escalations, or human review. First remove unnecessary work: prefer deterministic paths, smaller eligible tool sets, early acceptance, selective retrieval, artifact reuse, and bounded parallelism.

### Give each stage a latency and cost budget

Allocate an end-to-end deadline across admission, queue, context, model, tools, human dwell, and reserve. Each child task inherits a narrower budget. Track expected and worst-case tokens, tool calls, external charges, sandbox minutes, and human minutes. The budget service issues permits; workers cannot exceed the lease by continuing to reason.

### Share capacity without starving important work

Separate queues by workload and risk class. Weighted fair scheduling prevents a large tenant from starving others. Concurrency permits reflect the actual scarce resource: model route, vendor rate limit, browser pool, code sandbox, database writer, or approver queue. Backpressure starts at admission rather than after every subsystem is overloaded.

### Decide what the system may drop or defer

Under pressure, Northstar can defer nonurgent work, produce a draft rather than commit, reduce optional context, use an evaluated lower-cost route, serialize optional fan-out, or request human scheduling. It never disables authorization, tenant isolation, approval, effect verification, or required audit. Every optimization is tested by slice, canaried, reversible, and observable.

### Start with the four measurements

Optimization becomes confused when one number is treated as the whole system. Latency tells us how long a user waits; cost tells us what resources the run consumes; capacity tells us how much work can be admitted; and reliability tells us whether the result is completed correctly. These measures interact, but they are not interchangeable.

| **Question** | **Useful measure** | **A misleading shortcut** |
| --- | --- | --- |
| How long did the customer wait? | End-to-end p50/p95/p99, including queue and human dwell | Model-token latency alone |
| How much work did success require? | Cost per verified successful outcome, including retries and review | Price per million tokens |
| How much can the system accept? | Queue age, service-time distribution, permits, and downstream quota | CPU utilization without provider limits |
| Did the system do the right thing? | Acceptance rate, groundedness, effect correctness, and failure recovery | “The request returned 200” |

For a stable workload, Little’s Law gives a useful first estimate: `average work in system = arrival rate × average time in system`. If Northstar admits 120 runs per minute and an admitted run occupies the workflow system for four minutes on average, about 480 runs are active. That estimate is not a capacity guarantee: fan-out, retries, provider quotas, and burstiness can require more permits. It is a way to locate the question that a load test must answer.

### A quarter-end planning example

Assume the 120-runs-per-minute peak is expected to last long enough for queues to reach steady state. The planning model estimates 480 active runs before headroom. Northstar reserves 25 percent of capacity for close-critical work, so ordinary research cannot consume the last protected permits. When the browser pool reaches its limit, the admission controller defers new browser-heavy runs or offers a draft path; it does not keep accepting work that will wait past its deadline.

| **Observed pressure** | **Safe response** | **Shortcut to avoid** |
| --- | --- | --- |
| Queue age predicts a deadline miss | Defer low-priority work, preserve reserved capacity, and expose a retry-after time | Add workers while the provider quota is already exhausted |
| Token spend rises without better acceptance | Reduce duplicate context, tighten tool schemas, and inspect retry/fan-out causes | Switch every node to the cheapest model |
| A lower-cost route increases escalations | Revert the route for the affected slice and compare cost per verified success | Keep the route because token cost fell |
| A tool call is slow or unknown | Preserve the effect record and reconcile before retrying | Treat timeout as proof that no effect occurred |

The numbers above are illustrative planning inputs, not universal limits. Their purpose is to show the order of reasoning: measure demand, identify the scarce resource, reserve capacity for the outcomes that matter, choose a reversible degradation, and verify that the degraded path still satisfies its safety and acceptance contract.

## Scale the workflow, not just the model call

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Scale bursty, heterogeneous, quota-bound work while controlling latency, spend, fairness, noisy neighbors, and long-lived idle runs. |
| Why it is difficult | Model and tool limits differ; agent fan-out is dynamic; a slow branch holds joins; retries amplify load; GPU and sandbox workloads have very different resource profiles. |
| Design alternatives | Synchronous monolith; generic job queue; serverless functions; Kubernetes worker pools; actor systems; workflow-task queues; provider-managed runtime. |
| Recommended architecture | Separate the stateless control plane from queue-driven execution pools. Partition queues by workload/risk/tenant/region; use fair scheduling and admission budgets; autoscale on backlog age and service time; apply hierarchical quotas and backpressure before model providers. Suspend idle workflows without workers. |
| Trade-offs | More pools improve isolation and tuning but increase operations. Managed runtimes reduce undifferentiated work while increasing vendor dependency and potentially weakening cross-vendor trace and state portability. |
| Failure scenarios | One tenant consumes all quota; fan-out explosion; retry storm; head-of-line blocking; model quota is exhausted while workers scale uselessly; sandbox image cold starts dominate latency. |
| Enterprise example | A month-end finance workload uses priority queues and reserved model quota for close-critical tasks, separate pools for OCR/code execution, and backpressure that defers low-priority research rather than failing all runs. |

### Scale by workload and failure boundary

Begin with a small number of meaningful pools rather than a queue for every tenant. A pool represents a real operational difference: interactive versus batch latency, read-only versus mutating risk, browser versus GPU resource profile, or one residency boundary versus another. Within a pool, tenant-aware quotas and fair scheduling provide isolation without creating an unmanageable number of services.

| **Layer** | **Scaling signal** | **Overload behavior** |
| --- | --- | --- |
| Admission | Predicted deadline miss, budget, risk, and downstream permits | Reject, defer, or offer a bounded draft path |
| Queue and scheduler | Oldest age, arrival rate, priority, and fairness | Preserve reserved capacity; prevent starvation and retry storms |
| Worker pool | Service time, active leases, and workload-specific utilization | Scale compatible workers; do not exceed provider or tool permits |
| External dependency | Provider quota, browser slots, database writers, and approver dwell | Queue before the dependency; expose retry-after and reconcile unknowns |
| Usage ledger | Reserved versus actual cost and successful outcomes | Release unused reservations and flag unexplained spend |

This layered view prevents a common operational mistake: treating worker count as capacity. If the model provider has no remaining token quota, adding workers only increases contention and may amplify retries. The scheduler should keep work queued until the scarce permit is available, while the admission controller decides whether waiting is still compatible with the deadline.

### Control concurrency before queues control you

* Hierarchical token buckets: organization → environment → tenant → agent → user → run → provider/tool.
* Queue partitions and worker pools by latency class, risk, region/residency, sandbox profile, model family, and data classification.
* Concurrency keys for scarce resources or records; use optimistic concurrency for data and semaphores for quotas.
* Backpressure on predicted service time, queue age, provider quota, and spend—not CPU alone. KEDA-style event-driven autoscaling is appropriate for queue workers.
* Bounded fan-out and speculative execution. Cancel losing branches once a validated result wins; account for cancellation lag.
* Fair scheduling with reserved capacity for critical workflows and protection against a single tenant or recursive agent tree.
* Prewarmed sandboxes only for latency-sensitive workloads; immutable images, snapshot pools, and aggressive idle reclamation for the rest.

### Optimize in the order that changes outcomes

1. **Remove unnecessary agency:** replace stable decisions with code, rules, search, or classifiers.
2. **Reduce work:** incremental recomputation, event correlation, cached deterministic results, delta retrieval, and early exit on acceptance criteria.
3. **Reduce context:** structured state projections, source-linked summaries, retrieval top-k tuning, deduplication, and tool-result compression.
4. **Route models:** choose the cheapest evaluated model for the node; escalate by difficulty, uncertainty, or failed validation—not by habit.
5. **Parallelize selectively:** only independent, sufficiently valuable branches; cap fan-out and straggler time.
6. **Cache safely:** key by model/version, prompt hash, normalized input, tenant, authorization scope, policy, and knowledge snapshot. Do not share sensitive cache entries across principals.
7. **Batch:** embeddings, classification, and offline evals where latency permits.
8. **Optimize the ACI:** precise tool schemas and smaller tool sets reduce retries and wrong calls more reliably than ever-longer prompts.
9. **Use spend-aware planning:** each plan estimates cost and reserves budget; report marginal value of optional branches.
10. **Measure cost per accepted outcome:** token price alone ignores retries, human review, failed trajectories, and tool charges.

### A workable implementation

### Who should own each decision

The Admission Controller predicts resource/risk and accepts, defers, or rejects work; the Hierarchical Quota Service owns organization-to-run limits; the Queue/Scheduler owns priority and fairness; the Worker Lease Service owns assignment/heartbeat; Provider Limiters translate external quotas into dispatch permits; the Capacity Controller scales pools; and the Usage/Cost Ledger attributes reserved and actual resources.

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/admission:check | Evaluate tenant/run request against predicted cost, deadline, risk, regional capacity, model/tool quotas, and approval capacity |
| POST /v1/budgets:reserve | Atomically reserve dollars/tokens/tool calls/compute/time for a run or plan node with expiry |
| POST /v1/quotas:acquire | Internal hierarchical token/concurrency permit; returns granted, defer-until, or hard-limit response |
| POST /v1/work-items | Enqueue typed reference with partition, priority, deadline, resource profile, build compatibility, and idempotency key |
| POST /v1/work-items/{id}:lease | Worker claims with lease/heartbeat, expected queue version, and workload attestation |
| POST /v1/work-items/{id}:complete | Idempotently record result and actual usage; workflow—not queue—decides domain transition |
| POST /v1/usage-events | Append metered tokens, requests, compute, storage, network, tool charges, and allocation dimensions |
| GET /v1/capacity | Return region/pool/provider availability, queue age, reserved capacity, health, and planning hints |
| GET /v1/runs/{run\_id}/cost | Return reserved/actual/forecast cost by node, agent, model, tool, retry, tenant, and outcome |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| QuotaDefinition | scope hierarchy, resource, sustained/burst limits, concurrency, priority reservations, effective interval, policy version |
| QuotaState | scope/resource/shard, available tokens, refill/version, outstanding permits; updated atomically without a global lock |
| BudgetReservation | reservation ID, owner run/node, resource/currency, amount, consumed/released, expiry, ledger version |
| QueuePartition | region, workload/risk/data class, model/tool/profile, build compatibility, priority policy, max backlog age |
| WorkItem | item/logical key, tenant/run/node, queue, priority/deadline, resource profile, payload ref/hash, attempt/lease state |
| WorkerLease | work item, workload identity/worker/pool, lease token, acquired/heartbeat/expiry, cancellation status |
| ProviderCapacity | provider/account/model/region, request/token/concurrency limits, observed use, retry-after, health, reservation |
| UsageEvent | immutable event ID, tenant/run/node/agent/model/tool, resource units, unit cost, timestamp, source/request ID |
| CostAllocation | aggregated period/scope, committed/estimated cost, successful-outcome attribution, tags and chargeback owner |

### Scheduling algorithm

1. Admission estimates critical-path latency, maximum concurrency, worst/expected cost, required capabilities, and regional constraints.
2. Reserve hard budget and scarce capacity only for the near execution horizon; use forecasts for later nodes.
3. Place work into the narrowest compatible queue. Weighted fair queuing selects tenant/class, then earliest deadline/priority within it.
4. Acquire provider/tool/sandbox permits before leasing work; if unavailable, keep the item queued rather than occupying a worker.
5. Lease with bounded heartbeat. Expiry makes work eligible for redelivery, while activity/effect idempotency protects correctness.
6. Emit usage immediately, reconcile provider invoices asynchronously, and release unused reservations when nodes terminate.
7. Backpressure admission when oldest age, predicted deadline miss, approval backlog, provider quota, or budget risk exceeds policy.

### Scalability mechanics

* Scale each workload pool independently. A practical concurrency estimate is arrival\_rate × mean\_service\_time / target\_utilization; add burst and failure margin, then verify with queue-age SLOs.
* Partition queues by region/residency, risk, workload profile, model/tool compatibility, and latency class—but avoid per-tenant queues unless isolation or volume justifies the operational cardinality.
* Use hierarchical distributed rate limiting with regional allocations and periodic reconciliation; no request should require a synchronous global lock. Keep a safety margin for clock/network skew and provider quota uncertainty.
* Autoscale on backlog arrival rate, oldest age, service time, active leases, and downstream permits. Do not scale workers when provider quota is the bottleneck.
* Enforce bounded fan-out, ready-node concurrency, delegation depth, speculative branches, context bytes, and retries per run. Admission reserves the aggregate worst permitted burst.
* Protect priority traffic with reserved capacity; cap each class so “urgent” cannot starve routine work indefinitely. Use aging to prevent starvation.
* For large tenants, assign dedicated queue partitions/provider accounts/pools when needed; otherwise use shared pools with tenant-aware quotas and noisy-neighbor telemetry.
* Cost caches, prompt caches, and response caches must include tenant, authorization, model/tool/prompt/schema/policy versions, and knowledge snapshot. Cache hits still emit usage/provenance events.

### Illustrative starting guardrails

| **Limit** | **Interactive/read-heavy** | **Mutating or high-risk** | **Rationale** |
| --- | --- | --- | --- |
| Parallel ready nodes | Small bounded fan-out; raise only from measured value | One or very few effects at a time per business aggregate | Control quota bursts and concurrency conflicts |
| Delegation depth | Usually 1–2; hard platform ceiling | 0–1 unless explicitly approved | Prevent invisible recursive authority/cost |
| Retry ownership | Workflow activity only | Workflow + effect reconciliation; no blind write retry | Avoid multiplicative retries |
| Context budget | Per-node fixed allocation with evidence cap | Minimum necessary; exclude secrets and unrelated history | Cost, privacy, injection surface |
| Spend/time | Reserve expected + bounded contingency | Hard stop before effect if reservation is insufficient | Prevent sunk-cost pressure from bypassing controls |

These are policy shapes, not universal numbers. Determine actual limits from task value, provider quotas, benchmark distributions, risk appetite, and SLO/error budgets.

|  |
| --- |
| **PERFORMANCE AND COST**  Route on policy first, then on price. Model choice is a governance decision before it is an economic one: data residency, retention, and approved use constrain the candidate set, and only then does cost per verified outcome pick from what remains. |

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Sizing method | Size from measured arrival rates and service-time distributions. Include fan-out, retry amplification, model/tool quotas, approval dwell time, tenant fairness, and headroom. Cost per verified success is more useful than token cost alone. | QUEUEING; MLFLOW-TRACE |

The discussion above draws on QUEUEING; MLFLOW-TRACE. Appendix K lists the complete sources and records their authority, version, and scope.

|  |
| --- |
| **BEST PRACTICE**  Measure cost per verified successful outcome, not per token or per request. Tokens are an input; the business pays for completed work. A change that halves token spend while pushing five percent more runs into human review has almost certainly cost money. |

## A sensible place to start


### Admission and capacity permit

🐍 · implementation excerpt

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapacityPermit:
    tenant_id: str
    workload_class: str
    model_tokens: int
    tool_calls: int
    sandbox_seconds: int


def admit(requested: CapacityPermit, available: CapacityPermit) -> CapacityPermit:
    if requested.tenant_id != available.tenant_id:
        raise PermissionError("permit tenant mismatch")
    if requested.workload_class != available.workload_class:
        raise PermissionError("workload class mismatch")
    if requested.model_tokens > available.model_tokens:
        raise RuntimeError("insufficient model-token capacity")
    if requested.tool_calls > available.tool_calls:
        raise RuntimeError("insufficient tool-call capacity")
    if requested.sandbox_seconds > available.sandbox_seconds:
        raise RuntimeError("insufficient sandbox capacity")
    return requested
```

## If this fails in production

1. Decompose end-to-end p95 into queue, workflow, model, retrieval, tool, and human components.
2. Measure turns, calls, tokens, retries, and escalations per verified success.
3. Inspect tenant fairness, queue age, and safe-degradation decisions under load.

## What to verify before production

**✓** The objective is cost and latency per verified success, not token price alone.

**✓** Capacity is budgeted by tenant, risk, workload class, and scarce resource.

**✓** Queues, backpressure, fairness, overload, and safe degradation are explicit.

**✓** Caching keys include authorization, policy, version, and data-boundary dimensions.

**✓** Every optimization is evaluated, canaried, reversible, and constrained by safety gates.

## Put the idea to work

1. Build a capacity model for 10,000 daily runs with burst and tenant quotas.
2. Design an experiment that reduces context cost without regressing groundedness.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| What is the correct optimization objective? | Cost, latency, and resource use per verified successful outcome subject to quality, safety, reliability, and compliance constraints. |
| What should be optimized before changing models? | Remove unnecessary turns, tools, retrieval, context, retries, and serialization; add early acceptance and deterministic shortcuts. |
| How do you avoid cache authorization bugs? | Include tenant, subject scope, policy version, data version, purpose, redaction, locale, and release in keys and invalidate on revocation or correction. |
| How should overload degrade? | Reject or defer early, protect durable state, reduce optional context, switch to approved bounded routes, produce drafts, and preserve audit. |
| Why can the cheapest model be more expensive? | Lower reliability may cause more turns, retries, escalations, human work, and failed outcomes, increasing total cost per success. |

## Where this leads next

The architecture narrative is complete. The appendices provide decision aids, runbooks, contracts, framework evidence, references, maintenance criteria, and production acceptance checks for implementation and future editions.
