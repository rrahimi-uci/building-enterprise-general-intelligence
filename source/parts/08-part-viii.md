# PART VIII — RUNNING THE SYSTEM IN THE REAL WORLD

Shipping the first version is the easy milestone. The hard work is operating
the system when usage grows, people change roles, vendors drift, and a run is
still active during a deployment. Part VII produced evidence and candidate
changes. This Part decides who may approve them (Chapter 26), how approved
change reaches production without disturbing work in flight (Chapter 27), and
how much work the platform admits, and at what cost, when demand peaks
(Chapter 28).

# 26 — Make Governance Part of How the Platform Runs

> **Evidence context:** NIST AI RMF and its Generative AI Profile are voluntary risk guidance; ISO/IEC 42001 specifies an AI management system; the EU AI Act source provides official implementation context. Applicability and legal obligations require qualified jurisdiction-specific review. **[R12][R13][R14][R40]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Harborlight's mortgage-evidence assistant now depends on data, tools, models, and releases that different teams own. Before the document-request tool goes live, the platform must know who classifies the use case, who approves the release, and who may accept a gap in controls—and until when. |

|  |
| --- |
| **THE DESIGN CHOICE** Govern by decision class: one accountable owner, proportional tiers, evidence produced by the pipeline, and exceptions that expire. |

## Why governance belongs in the operating model

Governance works when it changes what teams do, not when it produces another
committee packet. Chapter 25's improvement loop ends at an Approve stage; this
chapter decides who approves, how deeply, and what happens when a required
control cannot be met. It becomes especially important when several teams
share a platform and no single team can see the full consequence of a release.

Good governance should make routine, low-risk change faster because teams know the path in advance. It becomes bureaucracy when every change enters the same queue or exceptions have no owner or expiry. Start by naming the decision, the accountable role, the evidence needed, and the time boundary. Then scale review to the risk.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| A named accountable owner per decision class; a named risk authority owns exceptions | delegated domain autonomy to enterprise risk appetite | risk tier · domain · release | one decision, one exception, one release | risk tier · PolicyDecision · ReleaseGateDecision · GovernanceRecord · ExceptionWaiver |

## Governance starts with clear decisions and owners

Governance is easiest to understand as a control loop, not as a meeting. A team first states the outcome it is accountable for, then identifies what could make that outcome harmful, chooses controls proportional to the consequence, collects evidence while the system runs, and revises the controls when evidence or circumstances change. The loop is useful only when each step has an owner and a record that another person can inspect.

| **If the team asks…** | **Governance must answer…** | **Evidence that closes the question** |
| --- | --- | --- |
| “Can this use case run?” | What outcome, data, autonomy, and consequence define its risk tier? | Use-case record, risk assessment, prohibited-use boundary |
| “Can this tool be called?” | Who owns the resource, and what authorization and reconciliation does the effect require? | Tool contract, capability decision, effect policy |
| “Can this release go live?” | Did the candidate satisfy the required technical, safety, and business gates? | ValidationReport (Chapter 25), approvals, canary plan, rollback owner |
| “Why was an exception allowed?” | What exact gap was accepted, by whom, with which compensating controls, and until when? | Time-bounded exception record and monitoring result |

This framing also explains why a central board alone scales poorly. A board can set the risk vocabulary and approve high-consequence boundaries, but it cannot supply the local knowledge needed for every data source, business effect, or acceptance criterion. Central services make decisions consistent; domain owners make them meaningful.

## Share responsibility without losing accountability

Figure 26-1 shows the split. Central services provide identity and policy, evidence and audit, and risk tiers and exceptions once; domain teams decide in context; and the review board engages in proportion to risk tier, not to team.

[[DIAGRAM:governance-model|Figure 26-1 — Federated governance with centralized control services]]

| **Decision** | **Accountable owner** | **Evidence** |
| --- | --- | --- |
| Business outcome/acceptance | Domain/product owner | Outcome contract, tests, business SLO |
| Risk tier/autonomy | Risk owner | Threat/data/effect assessment and controls |
| Platform contracts | Platform product owner | RFC, compatibility/migration, SLO |
| Data/context/memory purpose | Data owner | Source, ACL, purpose, retention, deletion, quality |
| Tool/effect authorization | Resource owner | Tool contract, permission, idempotency/reconciliation, approval policy |
| Model/provider/route | Model governance owner | Capability, evaluation, data terms, region, cost, resilience |
| Evaluator/dataset truth | Domain evaluation owner | Lineage, rubric, calibration, uncertainty |
| Production promotion | Release owner | ReleaseGateDecision (Chapter 25), required approvals, canary, rollback |
| Exception | Named risk authority | Scope, rationale, compensating controls, expiry, monitoring |

In Harborlight's mortgage-evidence assistant, the table resolves as follows: the domain owner may accept a draft evidence classification, but the assistant must not make or record a lending decision. The data owner decides which application and policy records may enter context; the risk owner classifies the workflow; the resource owner defines whether a document-request tool is available; and the release owner verifies that the assembled controls were tested. No single committee needs to understand every underwriting rule, but every decision has a clear owner and an evidence boundary.

## Match the control to the risk

| **Tier** | **Typical use** | **Minimum governance** |
| --- | --- | --- |
| T0 Deterministic/assistive | No model or harmless ideation | Standard engineering/data policy |
| T1 Bounded advisory | Low-impact content with verification | Owner, basic evaluation, data controls, monitoring |
| T2 Operational recommendation | Business decision support/internal tools | Domain acceptance, security/privacy, regression, recourse (Chapter 14) |
| T3 Protected action | Financial, identity, customer, employee, infrastructure effect | Least privilege (Chapter 21), proposal-bound approval of each protected action (Chapter 14), effect ledger (Chapter 22), strong evaluation, canary, incident plan |
| T4 High consequence/systemic | Regulated, safety-critical, large-scale autonomous/cross-boundary | Executive/risk sign-off of the use case, independent assurance, strict capability envelope, recovery exercise |

Three risk scales recur in the platform, each with its own subject. Effect risk classes R0–R4 (Chapter 22 § Risk classes) classify each tool action and are enforced at dispatch. Use-case tiers T0–T4 classify a use case and set its governance and release depth. Change classes (Chapter 25's Approve stage) classify a proposed change. This book recommends one rule linking the first two: a use case's tier is never lower than its most dangerous eligible effect demands, so any eligible R3 or R4 tool implies at least T3 controls, and any R2 tool at least T2.

The risk owner assigns the tier and re-scores it whenever eligible tools, data classes, autonomy, or exposure change. Assess incorrect-outcome impact, sensitive data, protected effects, legal relevance, autonomy, exposure, scale, reversibility, multi-agent/tool complexity, and human detectability. Risk is not the model name.

## Make review predictable and proportional

The tier sets the minimum controls. Review stays predictable when every rule has a known layer, owner, and enforcement point.

| **Layer** | **What it decides** | **Who changes it** | **How it is enforced** |
| --- | --- | --- | --- |
| Principles | Non-negotiable outcomes | Executive and risk leadership | Periodic review |
| Standards | Reusable contracts | Platform product owner | RFC |
| Policy-as-code | Eligible models, data, tools, actions, budgets, and approvals | Policy owner | Policy decision point (Chapter 21); budgets and quotas as QuotaDefinition (Chapter 28) |
| Application configuration | Selection within the policy envelope | Owning team | Release pipeline |
| Exceptions | A time-bound gap in one control | Named risk authority | ExceptionWaiver (§ Exceptions that expire) |

Principles and standards are argued; policy-as-code and configuration are executed.

The release gate (Chapter 25's ReleaseGateDecision) takes two inputs: the use case's tier and the change class. In T0–T2 use cases, pre-approved low-risk change classes (metadata, documentation, evaluated prompt wording) may promote automatically on passing gates. A change in the "Require human governance" row of Chapter 25 § Close the loop without handing control to the model always requires a named approver, whatever the tier. In T3–T4 use cases every behavior change needs the release owner's recorded approval and a canary; T4 adds independent assurance.

A design review covers each area below; the chapter in parentheses holds its controls: outcome and acceptance (Chapters 2 and 13), deterministic boundary (2), state and effect ownership (15, 22), identity and delegation (21), context and memory (6), tool, MCP, and A2A trust (19), threats (20), evaluation truth (25), observability and privacy (24), recovery and release (27), capacity and cost (28), human oversight (14), and portability (3).

Reviews also run on a fixed cadence. Incidents enter the daily or weekly review because incident response belongs inside organizational risk management [R42].

| **Cadence** | **Input** | **Owner** | **Output** |
| --- | --- | --- | --- |
| Per run | Admission, policy, effects, acceptance | Platform product owner | PolicyDecision, effect records, AcceptanceDecision |
| Daily or weekly | SLO, quality, safety, cost, incidents, evaluator health | Domain and platform owners | Corrective actions and regression cases |
| Per release | Classification, regression, security/privacy, compatibility, canary/rollback | Release owner | ReleaseGateDecision and PromotionDecision (Chapters 25 and 27) |
| Quarterly | Portfolio value and risk, platform roadmap | Risk owner and platform product owner | Re-scored tiers, retired exceptions, roadmap |
| Annually or on material change | Policy, law, threat, recovery, independent assurance | Named risk authority | Revised principles and standards, assurance report |

Governance is accelerating delivery when time from evidence-complete to approved is falling, open exceptions shrink in number and age as standards absorb them, the same evidence serves engineering review, risk review, and audit without rework, and bypass and regression-escape rates stay low.

### Exceptions that expire

An exception starts as a request that names the exact control gap, its scope, and the compensating controls. The named risk authority approves it with an expiry, recorded as an ExceptionWaiver. When Chapter 25's release gate returns waiver-required, only a matching, unexpired waiver satisfies it. The platform monitors how often each waiver is used. At expiry the gap is closed or absorbed into a changed standard; an exception that keeps recurring is a missing standard.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Governance Inventory | Track each use case's owners, data, autonomy, controls, evidence, exceptions, retention, and regulatory mapping as a GovernanceRecord |
| Exception Service | Record exception requests and the named risk authority's decisions; enforce expiry and report usage |
| Policy Bundle Registry | Turn approved standards into signed, tested policy-as-code bundles with effective periods |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/governance/exceptions | Create time-bounded, scoped waiver with compensating controls, approvers, owner, evidence, and renewal prohibition/default |
| GET /v1/governance/inventory | Query deployed agents/use cases by owner, risk tier, autonomy, data class, region, vendor, controls, incidents, and review date |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| GovernanceRecord | use case, business purpose, owners and approvers, risk tier, autonomy, users, data classes, tools and external effects, human controls, model and vendor dependencies, regions, controls, evaluations, current release, exceptions, incidents, review date, retirement plan |
| ExceptionWaiver | exact control gap/scope, rationale, compensating controls, owner/approvers, start/expiry, usage count, status |

### What governance requires before release

* Keep every deployed agent and use case in the inventory as a current GovernanceRecord.
* Map controls to NIST AI RMF Govern/Map/Measure/Manage, ISO/IEC 42001 management-system processes, security/privacy standards, and applicable sectoral rules. EU AI Act obligations phase in by date and risk category; confirm the current timeline against the official source [R40] and classify each use case individually.
* Require documented intended use, prohibited use, foreseeable misuse, human-oversight design, evaluation evidence, residual risk acceptance, and rollback owner before release.
* Produce an immutable evidence package per material run: request, identities, purpose, versions, policy decisions, source provenance, plan revisions, tool effects, approvals, output, metrics, incidents, and retention class. The audit ledger that holds it is Chapter 24's.
* Document explanations at the right level: evidence and rules for business decisions; trajectory summaries for operations; model internals are neither necessary nor sufficient.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Regulatory applicability | NIST AI RMF and its Generative AI Profile are voluntary guidance; ISO/IEC 42001 specifies a management system; the OWASP Top 10 for Agentic Applications is community security guidance; the EU AI Act creates binding obligations that vary by risk category and by whether the enterprise acts as provider or deployer. Mapping a control in this book to a clause is engineering evidence, not legal advice, and qualified jurisdiction-specific review remains required. | R12; R13; R14; R15; R40 |
| Incident response | NIST SP 800-61 Rev. 3 integrates incident response into organizational cybersecurity risk management. Feeding incidents into the governance cadence and the GovernanceRecord is this book's recommendation. | R42 |

The discussion above draws on R12; R13; R14; R15; R40; R42. Appendix K lists the complete sources and records their authority, version, and scope.

## If this fails in production

Governance fails as queues and exceptions rather than as stack traces. Diagnose it with the same rigor as an outage.

1. When a release is blocked, find which single decision lacks a named owner instead of escalating the whole release.
2. When the same exception recurs, treat it as a missing standard rather than a repeated approval (§ Exceptions that expire).
3. When risk tier and control effort disagree, re-score impact, reversibility, and human detectability before changing the tier.
4. When review takes longer than delivery, check whether evidence is produced by the pipeline or assembled by hand. Hand-assembled evidence is the usual cause.

## What to verify before production

**✓** Every decision class in the accountability table has one named owner and its required evidence defined.

**✓** Risk tier is derived from the consequence factors in § Match the control to the risk, and bounded below by the highest eligible effect class—never from the model name.

**✓** Exceptions follow the lifecycle in § Exceptions that expire; none is open-ended.

**✓** Policy-as-code decides eligible models, data, tools, actions, budgets, and approvals; application configuration only selects within that envelope.

**✓** Each cadence—per run, daily or weekly, per release, quarterly, annually—has a named owner and a defined input.

## Put the idea to work

1. Classify three current use cases into tiers T0–T4 and list the minimum governance each one triggers. Where two people disagree, the tier definition is the defect.
2. Take one standing exception and write either its expiry date or the standard that would retire it permanently.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why federate governance rather than centralize it? | Central review of every prompt edit becomes the bottleneck and is abandoned. Centralize reusable control services, risk tiers, policy, and evidence; federate domain acceptance, tools, knowledge, and SLOs to accountable owners. |
| What makes a risk tier defensible? | Consequence and reversibility, scored with the chapter's factors and bounded by the eligible effect classes, rather than the model or framework in use. |
| Why must every exception expire? | An exception that never expires is an undocumented policy change with no owner and no review. Expiry forces a deliberate choice: absorb the exception into a changed standard or close the gap. |
| What separates principles, standards, policy-as-code, and configuration? | Principles state non-negotiable outcomes; standards define reusable contracts; policy-as-code decides what is eligible at runtime; configuration selects within that envelope. Only the first two are argued; the last two are executed. |
| How do you know governance is accelerating delivery? | Time from evidence-complete to approved is falling, exceptions are trending down as standards absorb them, and the same evidence serves engineering review, risk review, and audit without rework. |

## Where this leads next

Governance defines who may release change and at what depth; Chapter 27 makes releases immutable, promotable, observable, reversible, and recoverable.

# 27 — Release New Behavior Without Breaking Work in Flight

> **Evidence context:** SBOMs describe components and SLSA provenance describes how an artifact was built; the release controls here use both **[R17][R18]**. Regional recovery mechanics are book-authored recommendations.

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** A new release changes the document-request tool schema and the workflow definition while MORT-2026-000184 is still waiting for the second pay statement. Its history was recorded under the old release. The platform deploys compatible workers, pins each run's release, canaries new starts, and rolls back assignment without rewriting history. |

|  |
| --- |
| **THE DESIGN CHOICE** Release immutable bundles with compatibility evidence; roll back new assignment while active runs remain pinned to compatible code. |

## Why a release is more than a deployment

An agentic release changes more than application code: it can change prompts,
tools, policies, model routes, schemas, and the behavior of work already in
flight. This chapter shows how to package those changes, prove compatibility,
canary new work, and recover without rewriting history or abandoning active
runs. Chapter 1's Friday failure—a cheaper model swapped in with no code
change—is this problem in its smallest form; Chapter 26 decided who may approve
such a change, and this chapter makes the approved change safe to apply.

## Treat the full behavior as the release

[[DIAGRAM:release-recovery|Figure 27-1 — Immutable release promotion and recovery without rewriting active history]]

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Release Registry and compatible worker pools | candidate artifact to production assignment | release cohort · workflow build · cell | one release cohort | ReleaseManifest · CompatibilityRule · EnvironmentBinding · PromotionDecision |

For an agentic system, behavior is spread across more than application code. A model route, prompt, Skill, tool schema, policy bundle, evaluator, and workflow definition can each change what the user experiences or what the system may do. A release therefore pins the whole graph. That makes a production result reconstructable and gives rollback a precise meaning: restore known behavior, not merely an older container image.

A production release pins every object in the table below, plus dashboards, runbooks, rollout, and rollback plans. The platform records these in an immutable ReleaseManifest; each run's RunManifest references it.

Four records keep this precise. A ChangeBundle is a proposed change (Chapter 25's Recommend stage); it becomes a ReleaseManifest only when promoted. A ReleaseManifest—the "release bundle" in this chapter's prose—is the immutable, signed graph listed in § Versioned objects. An EnvironmentBinding says which ReleaseManifest new starts receive for a tenant, use case, environment, and region. A RunManifest (Chapter 4) is resolved once at admission: it records the ReleaseManifest digest plus the run's subject, purpose, budget, risk tier, and knowledge-snapshot choice. The ReleaseManifest fixes the eligible Skill and pack versions; each RunManifest records the digests resolved from that set (Chapter 8). Rollback changes an EnvironmentBinding; it never edits a ReleaseManifest or a RunManifest.

### Versioned objects

| **Object** | **Version rule** | **Promotion gate** |
| --- | --- | --- |
| Agent manifest | Semantic version + content digest | Contract, behavior, security, ownership review |
| Prompt bundle | Immutable digest; declared compatible schemas and models | Regression and adversarial evals |
| Skill | SkillManifest digest (Chapter 8) | Chapter 8 certification |
| Skill Pack | SemVer plus signed digest; pins exact Skill digests | CompatibilityReport and pack-level evaluation (Chapter 9) |
| Workflow code | Build artifact + replay/change version markers | Determinism, migration, fault-injection tests |
| Tool/connector | Semantic API version + implementation/image digest | Contract, auth, idempotency, sandbox, rollback tests |
| Model route | Provider model ID/version + decoding/config + fallback chain | Quality, safety, latency, cost, regional/compliance evals |
| Policy bundle | Signed version + effective period | Policy tests, separation of duties, emergency rollback |
| Data/schema | Versioned contract and migration | Backward/forward compatibility and lineage checks |
| Knowledge snapshot | Source revision/index build ID + ACL snapshot strategy | Freshness, ACL correctness, deletion propagation |
| Eval dataset/rubric | Immutable examples, provenance, reviewer/version | Coverage, leakage review, judge calibration |
| Runtime image | Signed digest + SBOM/provenance | Vulnerability, sandbox, supply-chain checks |
| Artifact | Content hash + schema + creator run/version | Classification, destination policy, retention |

The alternatives—mutable "latest" configuration, environment snapshots, semantic versions alone—fail when an alias drifts or a long-running workflow spans deployments. Content-addressed, signed bundles cost storage and release discipline, and buy rollback, replay, and investigation.

CI verifies types and contracts, deterministic replay, policy and grant subsets, tool and effect semantics, prompt and trajectory regressions, threat cases, performance, container signatures, provenance, and migration compatibility. CD promotes the exact same signed artifacts through shadow, canary, tenant cohort, and regional stages.

## Roll back assignment, not history

Rollback changes the release assigned to **new work**. Active workflows continue on compatible workers or use an explicit tested migration. Rewriting history or silently changing a tool schema underneath an active run is not rollback. High-risk changes may pause affected runs until a compatible worker or reviewed migration is available.

### Compatibility and long-running execution

Chapter 15 keeps compatible workers and explicit migrations for in-flight histories, and its Version Router enforces this chapter's compatibility rules at dispatch; at the release level three further rules apply:

* Tool/model fallback is itself a versioned route with eval evidence. “Same family” or “newer model” is not proof of compatibility.
* Policies can impose emergency deny outside the pinned bundle; the run records both the original policy and the current higher-precedence denial.
* Knowledge snapshots may be “as-of,” “current under freshness policy,” or a recorded set of source revisions. The manifest states which reproducibility level applies.

### A release walkthrough

The distinction between a release and a deployment becomes concrete during a tool-schema change. Suppose the release replaces `mortgage.document.request@1` with `@2`, which adds a required field. The release builder creates a new bundle containing the workflow build, tool schema, policy, model route, image, evaluation evidence, and rollback plan. The compatibility rules record that workers serving old runs understand the old schema, while the new worker pool understands the new one.

| **Moment** | **Control** | **What must remain true** |
| --- | --- | --- |
| Candidate assembled | Resolve every dependency to a digest and test compatibility | The bundle can be reproduced and no mutable “latest” reference is admitted |
| New starts canary | Assign only a bounded tenant or traffic cohort | Existing runs remain on their pinned manifest; canary evidence is separately attributable |
| Canary finds a defect | Stop new assignment and restore the prior binding | Rollback changes placement, not the history or effects of an active run |
| Old run reaches a tool call | Route to a worker compatible with its manifest | A worker may support the run’s old contract, or a tested migration must be explicit |
| Region fails during a write | Fence the old writer, restore, reconcile, then advance placement (§ Regional recovery) | No effect is assumed absent merely because the request timed out |

This is why “roll back the model” is usually incomplete. If the prompt, tool schema, policy, workflow build, or retrieved knowledge strategy also changed, restoring one model identifier does not restore the behavior. The smallest safe rollback unit is the release bundle, while emergency deny and credential revocation remain separate controls that can take effect immediately and be recorded alongside the pinned release.

## Promotion as a chain of evidence

Promotion is a chain of evidence, not a sequence of environments that an artifact happens to visit. Each stage asks a narrower question, and the answer travels with the same signed bundle to the next stage. A failed gate returns the candidate to revision; it does not create an undocumented production-only patch. These stages expand Chapter 25's Validate, Approve, Deploy, and Monitor stages for a single candidate; the gate depth at each stage follows the use-case tier and change class (Chapter 26).

| **Stage** | **Question** | **Evidence** |
| --- | --- | --- |
| Build | Can the dependency graph be reproduced and attested? | Digests, lockfiles, SBOM, provenance, signature |
| Evaluate | Does the candidate pass the behavioral and security gates its tier requires? | Dataset results, replay, threat cases, slice analysis |
| Shadow | What would the candidate do on representative traffic without effects? | Linked traces, drift signals, latency and cost forecast |
| Canary | Does bounded real traffic stay within acceptance and SLO limits? | Cohort-level metrics, effect safeguards, rollback trigger |
| Promote | Is the decision owned and recorded? | Approval, effective binding, release and audit record |

What production evidence does next belongs to Chapter 25's learning loop; it re-enters here only as a new candidate. A release cannot promote without the governance evidence Chapter 26 requires for its tier.

## A deployment shape that supports safe change

Chapter 4 separated a global control tier from regional execution cells; this section adds what each side must not assume while releases change and regions fail.

### A production topology that is easy to reason about

The topology has two different jobs. The global control tier decides what may run and which immutable bundle a run receives; regional execution cells do the work within that decision. Keeping those jobs separate lets a release be globally described while state, queues, credentials, and model endpoints remain inside the required residency and failure boundary.

| **Layer** | **Owns** | **What it must not assume** |
| --- | --- | --- |
| Global control tier | Registries, release bundles, evaluation gates, governance inventory, and promotion decisions | That a healthy registry means an execution region can safely resume effects |
| Regional execution cell | Admission, workflow history, queues, workers, retrieval, traces, and local service endpoints | That a replica is a compatible worker for every historical run |
| Source systems and effect boundaries | Business records, external writes, receipts, and reconciliation predicates | That a timeout proves the write was absent |
| Recovery controls | Fencing, deny/kill switch, credential revocation, placement, and resume policy | That normal deployment automation is sufficient during an incident |

The boundary is operational as well as logical. A regional worker should be able to verify a signed bundle from a local cache, but it should not invent a new policy when the control tier is unavailable. A high-risk admission may therefore fail closed, while a low-risk read-only task can use a documented last-known-good policy. That explicit distinction is more useful than a generic claim of “high availability.”

### Deployment guidance

* **Global control tier:** globally available registry, release, evaluation, and governance services publish signed immutable bundles. Production workers pull approved versions; they do not edit control-tier definitions.
* **Regional execution cells:** keep prompts, state, artifacts, retrieval indexes, queues, traces, and model endpoints in the required residency boundary. Route each run to a home region and avoid transparent cross-region migration of in-flight state.
* **Release:** deploy agent and workflow bundles using GitOps-style promotion, canaries, feature flags, and automated rollback. Keep old workflow code available until every in-flight run pinned to it completes or migrates.
* **Disaster recovery:** define RPO/RTO separately for run history, business effects, artifacts, indexes, telemetry, and audit; “multi-region” without replay tests is not a resilience claim.

Isolation, worker classes, and secrets follow Chapters 21, 23, and 28. Appendix D lists typical technology choices and selection criteria.

### Regional recovery

Regional recovery is the Recover stage of Chapter 20's incident lifecycle. When a cell fails, recover in this order:

1. Stop new admission in the affected cell.
2. Fence the old writer.
3. Restore durable state with a compatible build (Chapter 15).
4. Reconcile executing and unknown effects against source systems (Chapter 22).
5. Verify pending signals, timers, and task ownership (Chapters 15 and 18).
6. Advance placement atomically.
7. Resume read-only work first, then mutating work in ascending effect risk class (R0–R4, Chapter 22), with R3 and R4 effects only after reconciliation evidence is recorded.

The ordering in step 7 is this book's recommendation. Recovery is rehearsed with evidence, not inferred from replica health.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Artifact Registry | Immutable versions/digests for agent, prompt, skill, workflow, tool, schema, policy, model route, dataset, and runtime |
| Release Bundle Builder | Resolve dependencies, compatibility, SBOM/provenance, signatures, migration requirements, and rollout policy; produces a ReleaseManifest |
| Evaluation/Gate Service | Run the suites Chapter 25's release gate requires for the bundle's tier and change class |
| Promotion Service | Move signed bundle through environments with approvals, canary/shadow, and rollback |
| Runtime Resolver | Resolve each new run to a RunManifest that references one bound ReleaseManifest, plus regional endpoints; never serve mutable “latest” to an active run |
| Drift Monitor | Detect model/provider/tool/data/policy behavior or availability changes against baselines |
| Emergency Control | Kill switch, deny policy, credential revocation, and safe rollback independent of normal release cadence (scoped kill switch, Chapter 23) |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/artifacts/{kind} | Register content-addressed artifact/version with owner, dependencies, compatibility, provenance, SBOM, signature, and lifecycle |
| POST /v1/release-bundles | Resolve a candidate into a ReleaseManifest; fails on mutable/unavailable dependency, incompatible schema, missing control, or unsigned artifact |
| POST /v1/release-bundles/{bundle\_id}:evaluate | Invoke Chapter 25's release-gate evaluation (POST /v1/release-gates:evaluate) for the bundle's required suites and the target tier |
| POST /v1/release-bundles/{bundle\_id}:promote | Promote to environment/canary cohort using expected bundle state, gate evidence, approvers, and rollout plan |
| POST /v1/manifests:resolve | Return immutable RunManifest referencing the bound ReleaseManifest for tenant/use case/environment/region while recording resolution evidence |
| POST /v1/deployments/{deployment\_id}:rollback | Stop new assignment, restore prior binding, preserve in-flight compatibility, and create incident/evidence record |
| POST /v1/artifacts/{kind}/{id}/versions/{version}:deprecate | Set warning/end-of-new-use/end-of-support dates and enumerate impacted active runs/releases |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ArtifactVersion | kind/ID/version/digest, URI, owner, source/build provenance, signature, dependencies, compatibility, risk, lifecycle; released content immutable |
| ChangeBundle | change ID, proposed changes to versioned objects, source evidence/cases, predicted benefit, risk, affected contracts, rollback plan, author, state |
| ReleaseManifest | manifest ID/digest, complete dependency graph including Skill and Skill Pack digests, target use case/risk tier, migrations, rollout/rollback, build time, signature; immutable once signed |
| CompatibilityRule | producer/consumer kinds and ranges, schema/effect/replay constraints, test evidence, effective interval |
| PromotionDecision | manifest/environment, prior binding, gate digest = Chapter 25 ReleaseGateDecision, approvers, decision, canary cohort, time, rollback trigger |
| EnvironmentBinding | tenant/use case/environment/region, active manifest, traffic weights, effective interval, version |
| Deployment | binding/manifest, region/pool/build, status, capacity, start/end, health, rollback relation |
| DriftFinding | subject/version, baseline/window, metric/slice, magnitude/confidence, severity, action/owner; feeds Chapter 25's Detect stage (alert or containment action) |

### Scalability and control-tier resilience

* Registry and release writes are low volume and strongly consistent. Reads are high volume: distribute signed bundles/manifests through regional caches/object storage keyed by digest.
* Workers verify bundle signatures/digests locally and keep a last-known-good cache.
* Avoid a synchronous global registry call on every activity. Resolve once at admission, pass content addresses, and refresh only explicitly dynamic health/authorization data.
* Index dependency edges to answer “what uses this version?” before deprecation, incident containment, or vulnerability response. Run impact analysis asynchronously but from a consistent snapshot.
* Roll out by tenant/use case/risk tier/region cohorts with bounded canary volume. Automated rollback consumes streaming SLO/eval signals but never rewrites historical manifests.
* Keep release metadata, signatures, policies, and governance evidence replicated with tested backup/restore. Separate normal promotion permissions from emergency deny/rollback authority.
* Archive old artifacts only after all active-run, replay, audit, legal-hold, and rollback dependencies expire. Retain digest tombstones permanently to prevent ambiguous reuse.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Supply chain | An SBOM describes components; SLSA provenance describes where and how an artifact was built and by which builder. Using both, verifying signatures and builder identity before promotion, and pinning model, prompt, Skill, policy, and evaluation digests in the release manifest are this book's recommendations. | R17; R18 |

The discussion above draws on R17; R18. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

Two checks carry most of the release model: whether a worker may serve a run's pinned release, and whether a bundle's evidence binds to the exact bytes being promoted.

### Release compatibility check

The worker is described by a WorkerProfile—what it can execute—rather than by a release of its own.

[[EXAMPLE:release-compatibility]]

### Release attestation verification

Signature verification itself is delegated to the signing toolchain; this check binds the verified identities to the allowlists.

[[EXAMPLE:release-attestation]]

## If this fails in production

1. Resolve the run's RunManifest, the ReleaseManifest it references, and worker compatibility.
2. Replay history before migrating workflow code.
3. Verify rollback stopped new assignment without changing active history.

If a model or prompt swap shipped as configuration, or a release was changed in place, see AP-15 and AP-16 in Chapter 17.

## What to verify before production

**✓** Every run's RunManifest references one immutable ReleaseManifest; no mutable “latest” reference reaches an active run.

**✓** Rollback changes the release assigned to new work; active runs stay on compatible workers or follow an explicit, tested migration.

**✓** Promotion moves the same signed bundle through every stage, and each gate's evidence travels with it.

**✓** Emergency deny, kill switch, and credential revocation work independently of the normal release cadence.

**✓** Compatibility, schema migration, fencing, regional recovery, and effect reconciliation are designed before deployment.

## Put the idea to work

1. Design CI/CD gates for an agent, Skill Pack, policy, and workflow release.
2. Write a regional recovery sequence that fences the old writer and reconciles effects.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why is “roll back the model” usually incomplete? | Behavior also depends on the prompt, tool schema, policy, workflow build, and knowledge strategy. The smallest safe rollback unit is the release bundle; emergency deny and credential revocation remain separate, immediate controls. |
| What happens to active runs when a release is rolled back? | Rollback changes the release assigned to new work. Active runs stay pinned to compatible workers or move only through an explicit, tested migration; history is never rewritten. |
| How should execution behave during a global-control-tier outage? | Continue compatible in-flight work on pinned last-known-good bundles, apply local denies and kill switches (Chapter 23), and restrict high-risk admission when freshness cannot be established. |
| Before deprecating a tool or model version, how do you know what still depends on it? | Query the dependency-edge index from a consistent snapshot for active runs, pinned releases, replays, audits, and legal holds; set warning and end-of-use dates; never archive a digest still referenced, and keep its tombstone. |
| Describe safe regional failover during an external write. | Follow the seven-step sequence in § Regional recovery—admission stops first, and mutations resume last. |

## Where this leads next

The release lifecycle is controlled; Chapter 28 sizes the system and optimizes cost, latency, capacity, and reliability around verified outcomes.

# 28 — Treat Performance as a Business Decision

> **Evidence context:** Little’s Law relates average items in a stable system to arrival rate and average time in system. The capacity equations in this chapter are planning approximations and must be calibrated by load tests. **[R43]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Mortgage demand triples at quarter end. The platform must protect closing deadlines and tenant fairness while controlling tokens, tool calls, queue depth, and underwriter load. Optimization is judged by verified business outcomes, not by token price alone. |

|  |
| --- |
| **THE DESIGN CHOICE** Optimize cost per verified success through shorter trajectories, selective context, deliberate routing, bounded concurrency, and safe degradation. |

## Why cost and latency have to be designed into the workflow

The cheapest token is not a cheap outcome if it creates a rework loop, a human
queue, or an unverified effect. This chapter connects latency, cost, capacity,
fairness, reliability, and verified business success, then uses that model to
choose routing, context, concurrency, and degradation strategies. It is where
the architecture meets the operating budget.

The pieces already exist. Chapter 10 bounded one loop's turns and per-run spend;
Chapter 12's compiler estimated a plan's worst-case cost and reserved budget per
node; Chapter 14 counted approvers as capacity; Chapter 15 let waiting runs
release their workers; AP-11 made budgets shrink down the delegation tree. This
chapter composes them into one admission and scheduling system for the whole
platform.

## Measure the whole journey

[[DIAGRAM:reliability-economics|Figure 28-1 — Admission, bounded execution, and outcome-based operating feedback]]

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Admission controller and budget service | tenant demand to scarce shared capacity | workload class · tenant · queue | one admitted run | BudgetReservation · CapacityPermit · DegradationDecision |

Optimization becomes confused when one number is treated as the whole system. Latency tells us how long a user waits; cost tells us what resources the run consumes; capacity tells us how much work can be admitted; and reliability tells us whether the result is completed correctly. These measures interact, but they are not interchangeable.

| **Question** | **Useful measure** | **A misleading shortcut** |
| --- | --- | --- |
| How long did the customer wait? | End-to-end p50/p95/p99, including queue and human dwell | Model-token latency alone |
| How much work did success require? | Cost per verified successful outcome, including retries and review | Price per million tokens |
| How much can the system accept? | Queue age, service-time distribution, permits, and downstream quota | CPU utilization without provider limits |
| Did the system do the right thing? | Acceptance rate, groundedness, effect correctness, and failure recovery | “The request returned 200” |

For a stable workload, Little’s Law gives a useful first estimate: `average work in system = arrival rate × average time in system`. Apply it to each scarce resource separately. Runs *in the system* include durable waits: a mortgage run waiting nine days for the second pay statement holds history and a timer but no worker, because Chapter 15 suspends idle workflows. Work *holding a permit* counts only active service time. If the platform admits 120 runs per minute and each run spends four minutes of active service time holding a workflow-worker permit, about 480 permits are in use; waiting runs add to stored state and approval queues, not to that number. That estimate is not a capacity guarantee: fan-out, retries, provider quotas, and burstiness can require more permits. It locates the question a load test must answer; Appendix L § Quantitative sizing method gives the effective work rate and the permit-pool formula.

## Optimize the trajectory, not the token

A cheaper model call can make the workflow more expensive if it causes extra retrieval, repeated tool calls, evaluator retries, or human escalation. The unit of optimization is the accepted business outcome and the path taken to reach it. Measure cost and latency at each stage, then improve the bottleneck that changes the journey. This keeps local savings from shifting work—and risk—to a more expensive part of the system. A change that halves token spend while pushing five percent more runs into human review may well cost money.

The useful objective is **cost and latency per verified successful outcome**, constrained by quality, safety, reliability, and compliance. Token price alone ignores retries, human review, failed trajectories, and tool charges. First remove unnecessary work: prefer deterministic paths, smaller eligible tool sets, early acceptance, selective retrieval, artifact reuse, and bounded parallelism.

## Admit work against budgets and scarce capacity

A generic job queue or a synchronous monolith cannot express provider quotas, durable waits, or tenant fairness; partitioned queue-driven pools can, at the cost of more pools to operate. Managed runtimes reduce undifferentiated work but increase vendor dependency and can weaken trace and state portability.

### Give each stage a latency and cost budget

Allocate an end-to-end deadline across admission, queue, context, model, tools, human dwell, and reserve. Each child task inherits a narrower budget (AP-11; Chapter 21's narrowing applies to spend as well as authority). Track expected and worst-case tokens, tool calls, external charges, sandbox minutes, and human minutes. The budget service issues permits; workers cannot exceed the lease by continuing to reason.

### Share capacity without starving important work

Separate queues by workload and effect risk class (read-only versus mutating; Chapter 22). Weighted fair scheduling prevents a large tenant from starving others. Concurrency permits reflect the actual scarce resource: model route, vendor rate limit, browser pool, code sandbox, database writer, or approver queue (Chapter 14). Backpressure starts at admission rather than after every subsystem is overloaded.

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

## Decide what the system may drop or defer

Under pressure, the platform can defer nonurgent work, produce a draft rather than commit, reduce optional context, use an evaluated lower-cost route, serialize optional fan-out, or request human scheduling. It never disables authorization, tenant isolation, approval, effect verification, or required audit. Every optimization is tested by slice, canaried, reversible, and observable.

## A quarter-end planning example

Assume the 120-runs-per-minute peak is expected to last long enough for queues to reach steady state. The planning model estimates 480 worker permits in use before headroom. Harborlight reserves 25 percent of capacity for deadline-critical cases, so lower-priority work cannot consume the last protected permits. When the browser pool reaches its limit, the admission controller defers new browser-heavy runs or offers a draft path; it does not keep accepting work that will wait past its deadline.

| **Observed pressure** | **Safe response** | **Shortcut to avoid** |
| --- | --- | --- |
| Queue age predicts a deadline miss | Defer low-priority work, preserve reserved capacity, and expose a retry-after time | Add workers while the provider quota is already exhausted |
| Token spend rises without better acceptance | Reduce duplicate context, tighten tool schemas, and inspect retry/fan-out causes | Switch every node to the cheapest model |
| A lower-cost route increases escalations | Revert the route for the affected slice and compare cost per verified success | Keep the route because token cost fell |
| A tool call is slow or its outcome is unknown | Preserve the effect record and reconcile before retrying | Treat timeout as proof that no effect occurred |

The numbers above are illustrative planning inputs, not universal limits. Their purpose is to show the order of reasoning: measure demand, identify the scarce resource, reserve capacity for the outcomes that matter, choose a reversible degradation, and verify that the degraded path still satisfies its safety and acceptance contract.

## Optimize in the order that changes outcomes

1. **Remove unnecessary agency:** replace stable decisions with code, rules, search, or classifiers (Chapter 12 § What should be agentic?).
2. **Reduce work:** incremental recomputation, event correlation, cached deterministic results, delta retrieval, and early exit on acceptance criteria.
3. **Reduce context:** structured state projections, source-linked summaries, retrieval top-k tuning, deduplication, and tool-result compression.
4. **Route models:** after policy has fixed the eligible set—region, data class, tenant, purpose; the eligibility-first rule of Chapter 11—choose the cheapest evaluated model for the node; escalate by difficulty, uncertainty, or failed validation, not by habit (§ Route models after policy fixes the eligible set).
5. **Parallelize selectively:** only independent, sufficiently valuable branches; cap fan-out and straggler time.
6. **Cache safely:** key every cache by the dimensions in Chapter 21 § Consistency and revocation policy, plus model/version, prompt hash, and knowledge snapshot; a hit still emits usage and provenance events.
7. **Batch:** embeddings, classification, and offline evals where latency permits.
8. **Optimize the agent–computer interface (ACI):** precise tool schemas and smaller tool sets reduce retries and wrong calls more reliably than ever-longer prompts (tool contracts, Chapter 22).
9. **Use spend-aware planning:** each plan estimates cost and reserves budget; report marginal value of optional branches.

### Route models after policy fixes the eligible set

Model routing happens at the LLM Gateway (Chapter 4), and model choice is a governance decision before it is an economic one. Filter by tenant, purpose, data class, residency, risk, required capabilities, context length, tool/JSON behavior, and approved version. Only then optimize expected accepted-outcome quality under latency and cost budgets. Health and quota further constrain selection. Fallbacks obey the same invariants; “any available model” is not a safe fallback. Figure 28-2 shows the decision tree.

[[DIAGRAM:model-routing|Figure 28-2 — Policy-first model-routing decision tree]]

Record each routing decision: candidate routes, exclusions and reasons, selected provider/model/version/region, policy digest, budgets, fallback chain, and experiment cohort.

Measure route distribution and eligibility, task success and quality by route, schema/tool correctness, refusal/safety, p50/p95/p99 latency, queue/retry amplification, cache hits and unsafe-key rejection, tokens and cost per accepted outcome, policy denials, PII/secrets detections, provider error/fallback, alias/version drift, and trace completeness.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Admission Controller | Predict resource use and risk; accept, defer, or reject work |
| Hierarchical Quota Service | Own organization-to-run limits |
| Queue/Scheduler | Own priority and fairness |
| Worker Lease Service | Own assignment and heartbeat |
| Provider Limiters | Translate external quotas into dispatch permits |
| Capacity Controller | Scale pools |
| Usage/Cost Ledger | Attribute reserved and actual resources |

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
| BudgetReservation | reservation ID, owner run/node, resource/currency, amount, consumed/released, expiry, ledger version; requested per plan node by the Chapter 12 compiler |
| QueuePartition | region, workload/effect risk class/data class, model/tool/profile, build compatibility, priority policy, max backlog age |
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

* Size each pool with the permit-pool formula in Appendix L, then verify with queue-age SLOs.
* Hierarchical token buckets: organization → environment → tenant → agent → user → run → provider/tool.
* Use hierarchical distributed rate limiting with regional allocations and periodic reconciliation; no request should require a synchronous global lock. Keep a safety margin for clock/network skew and provider quota uncertainty.
* Partition queues and worker pools by latency class, effect risk class, region/residency, sandbox profile, model/tool compatibility, and data classification—but avoid per-tenant queues unless isolation or volume justifies the operational cardinality.
* Concurrency keys for scarce resources or records; use optimistic concurrency for data and semaphores for quotas.
* Backpressure on predicted service time, queue age, provider quota, and spend—not CPU alone. Autoscale on backlog arrival rate, oldest age, service time, active leases, and downstream permits; event-driven autoscaling (for example, KEDA on Kubernetes) suits queue workers. Do not scale workers when provider quota is the bottleneck.
* Enforce bounded fan-out, ready-node concurrency, delegation depth, speculative branches, context bytes, and retries per run. Cancel losing branches once a validated result wins, and account for cancellation lag. Admission checks the run’s worst permitted burst; hard reservations still cover only the near execution horizon.
* Protect critical workflows with reserved capacity, and guard against a single tenant or recursive agent tree; cap each class so “urgent” cannot starve routine work indefinitely, and use aging to prevent starvation.
* Prewarmed sandboxes only for latency-sensitive workloads; immutable images, snapshot pools, and aggressive idle reclamation for the rest.
* For large tenants, assign dedicated queue partitions/provider accounts/pools when needed; otherwise use shared pools with tenant-aware quotas and noisy-neighbor telemetry.

### Illustrative starting limits

| **Limit** | **Interactive/read-heavy** | **Mutating or high-risk** | **Rationale** |
| --- | --- | --- | --- |
| Parallel ready nodes | Small bounded fan-out; raise only from measured value | One or very few effects at a time per business aggregate | Control quota bursts and concurrency conflicts |
| Delegation depth | Usually 1–2; hard platform ceiling | 0–1 unless explicitly approved | Prevent invisible recursive authority/cost |
| Retry ownership | Workflow activity only | Workflow + effect reconciliation; no blind write retry | Avoid multiplicative retries (one retry owner per failure class, Chapter 22) |
| Context budget | Per-node fixed allocation with evidence cap | Minimum necessary; exclude secrets and unrelated history | Cost, privacy, injection surface (Chapter 6) |
| Spend/time | Reserve expected + bounded contingency | Hard stop before effect if reservation is insufficient | Prevent sunk-cost pressure from bypassing controls |

These are policy shapes, not universal numbers. Determine actual limits from task value, provider quotas, benchmark distributions, risk appetite, and SLO/error budgets.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Little’s Law | In a stable system, mean work in system equals arrival rate × mean time in system (L = λW); the chapter applies it per scarce resource, counting only active service time for permits. | R43 |
| Sizing method (book-authored recommendation) | Size from measured arrival rates and service-time distributions. Include fan-out, retry amplification, model/tool quotas, approval dwell time, tenant fairness, and headroom. Cost per verified success is more useful than token cost alone. | — |

The discussion above draws on R43. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

Admission should mirror the `quotas:acquire` contract: grant what fits, defer what will fit in time, and reject the rest so the caller can choose a draft or degraded path.

### Admission and capacity permit

[[EXAMPLE:admission-permit]]

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
| Why is worker count not capacity? | Capacity is the scarcest downstream permit: provider quota, browser slots, database writers, approvers. Adding workers when a provider quota is exhausted only increases contention and retries; keep work queued until the permit exists, and let admission decide whether waiting still meets the deadline. |
| How should overload degrade? | Reject or defer early, protect durable state, reduce optional context, switch to approved bounded routes, produce drafts, and preserve audit. |
| Why can the cheapest model be more expensive? | Lower reliability may cause more turns, retries, escalations, human work, and failed outcomes, increasing total cost per success. |

## Where this leads next

Part VIII closes the operating loop: governance decides who may change behavior and how deeply it is reviewed, releases decide which behavior each run receives, and admission decides how much work runs and at what cost—each judged by verified outcomes. The Closing Perspective that follows returns to Chapter 1's week of failures and shows where each is now contained. The appendices are desk tools: pattern and triage guides (A, B), contracts and framework choice (C, D), research, limits, roadmap, and glossary (E–H), the Harborlight implementation and coding-agent prompt (I, J), and the evidence registry and acceptance gates (K, L).
