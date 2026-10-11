# Knowledge CI/CD model — control plane, runtime plane, lifecycle, gates

Supporting file for `chapter-update-plan.md` §§ 4–6. Everything here is a **book-authored proposal** unless a reference ID is given. [reframed: the sentence that named an author-supplied process-mapping document as the model for this file is removed; the lifecycle below is book-authored Knowledge CI/CD for **compliance knowledge** — requirements, obligations, controls, constraints, and definitions with provenance to their authoritative source — and is attributed to no external document. The author's extraction pipeline is cited only as the already-registered R48, for the extraction and grounding claims the ingestion plan scopes; it is not described here.]

## 1. Two planes and the interface between them

### 1.1 Control plane (develop knowledge)

Owns: creation, extraction (Chapter 5 § Turn policy prose…, and the ingestion plan's § Ingest documents…), modelling (ontology and vocabulary), validation, versioning, testing, independent approval, publication, promotion, rollback, deprecation, retirement. Lives in the global control tier (Chapter 4 § Global control and regional cells), next to the Skill Registry and the Release Registry. Writers: compliance and domain knowledge owners and SMEs (through a review interface or a repository) [reframed], the AI assistant that proposes staged edits, and exactly one service identity that may publish: the **registry publisher**. Holds no run state.

### 1.2 Runtime plane (consume releases)

Owns: resolve a release at admission, retrieve, traverse, query, evaluate, enforce — over approved knowledge only, read-only, inside the regional execution cell. Consumers: the book's control points (Tool Gateway and Effect Service, Chapter 22; the policy decision point they ask, Chapter 21; read-only knowledge tools behind the Tool Gateway, Chapter 3), the Context Service / Retrieval Broker (Chapter 6), and the two components Chapter 1 names as lifecycle controls rather than control points — the plan compiler (Chapter 12) and the acceptance engine (Chapter 13). [reviewed: corrected — the original sentence called all of these "the book's control points"; Chapter 1 reserves the term for the request-time gateways.] Never writes knowledge. Memory writes (Chapter 6) are a different store with a different gate and never enter a release.

### 1.3 Interface

| Crosses | Direction | Object | Carried by | Notes |
| --- | --- | --- | --- | --- |
| Release | down | **KnowledgeRelease** manifest + content-addressed bundle | Knowledge registry → regional last-known-good replica | Immutable; signed by the registry publisher; digest is the identity |
| Live pointer | down | **EnvironmentBinding** for a knowledge stream (tenant · environment · region → release digest) | Registry publisher moves it; registry serves it | Same shape as Chapter 27's binding, scoped to a knowledge stream; "main" is approved desired state, the pointer is actual runtime state. [reviewed: corrected — not the "same record type": Appendix C defines EnvironmentBinding as tenant/use case/environment/region → active ReleaseManifest with traffic weights and a gate digest. The knowledge pointer is a new record (`KnowledgeBinding`: stream · tenant · environment · region → release digest, activation record, previous digest) or an explicit widening of that row; either way Appendix C and H change.] |
| Resolution | down, once per run | `knowledge_snapshots` in the RunManifest: stream → release digest | Run Service at admission (Chapter 4 step 2) | Never re-resolved for the life of the run |
| Read APIs | down | `:resolve`, `:search` (Chapter 6), `:query`, `:evaluate`, `GET releases/{digest}` | Hub query surface | All take a release digest; none accepts "current" |
| Observations | up | decision records (release digest, rule ids, verdict incl. `unknown`), refusals, runtime contradictions, retrieval citations of superseded releases, acceptance defects, evaluation results (Chapter 25) | Trace graph and EvaluationResult → knowledge owner | Evidence, never a write |
| SME feedback | up | corrections, disputed interpretations, missing terms | InterventionTask outcomes (Chapter 14), review comments | Becomes a proposed change |
| Proposed change | up | ChangeBundle draft naming knowledge objects (Chapter 25 Recommend stage) | Learning loop → control plane | Enters the lifecycle at Draft; nothing self-promotes |

Hub operations (book-authored; `:search` already exists in Chapter 6):

| Operation | Semantics |
| --- | --- |
| `POST /v1/knowledge:resolve` | Given a stream and the run envelope (tenant, environment, region, purpose), return the Active release digest the run may pin, or refuse (stream Deprecated past window, Revoked, or not entitled). Called at admission only. |
| `POST /v1/knowledge:search` | Chapter 6's hybrid search, now scoped to one release digest; returns KnowledgeObjects with release digest, source revision, and authority metadata |
| `POST /v1/knowledge:query` | Bounded graph query or traversal (max hops, max nodes, deadline) over one release; returns typed nodes/edges with provenance |
| `POST /v1/knowledge:evaluate` | Evaluate named rules or a decision table over supplied facts against one release; returns per-rule `true` / `false` / `unknown` with the rule id, source span, and release digest |
| `GET /v1/knowledge/releases/{digest}` | The release manifest (for audit, replay, and the trace) |

## 2. Vocabulary

[reframed: removed — the vocabulary-mapping table that translated an external process document's terms into the chapter's is deleted. The chapter uses only the book's own vocabulary (knowledge release, release manifest, RunManifest, Knowledge Hub, control points, enforced rule, provenance, approval, promotion, rollback, deprecation) plus the plain-English terms the plan adds to the glossary in `chapter-update-plan.md` § 10: compliance knowledge, requirement, obligation, control, candidate digest, tenant extension, registry publisher, knowledge registry, knowledge graph, ontology.]

## 3. Software CI/CD → knowledge management → book component

| Software CI/CD stage | Knowledge-management equivalent | Book component or record | Established or proposed |
| --- | --- | --- | --- |
| Source code | Compliance knowledge objects in a repository: requirements, obligations, controls as typed rules, definitions (SKOS/SBVR-style terms), ontology, graph data, decision tables, tenant extensions [reframed] | KnowledgeArtifact; ontology version | Representation: established [R47][R59]–[R62]; the unit set: proposed |
| Dependency lockfile | Pinned upstream base release (regulatory text release, group ontology) | `pinned_base` in the stream | proposed (adapted) |
| Dependency-update bot | Upstream update proposal: a generated change that bumps the pinned base and lists impacted objects; no automatic go-live | Change record opened by the control plane | proposed |
| Feature branch + PR | Knowledge change | Change record, candidate digest | proposed |
| Build | Resolve base + tenant extension + ontology into an effective release; content-address it | Resolver; release digest | proposed |
| Lint / static analysis | Named quality gates (§ 5) | Gate record in the manifest | shapes: established [R61]; the gate set: proposed |
| Unit / regression tests | Knowledge test suite: golden decision cases, refusal cases, traversal fixtures, shape fixtures; impact diff vs previous release | EvalCase / EvaluationResult (Chapter 25) | proposed |
| Integration test | Shadow evaluation of the candidate release on representative runs (observational, never pass/fail alone) | Chapter 27 Shadow stage | proposed |
| Code review | Independent SME approval of the whole candidate | KnowledgeApproval | proposed |
| Artifact registry | Knowledge registry: immutable bundles by digest | Knowledge registry (Chapter 4 store row) | proposed |
| Release tag | Release version per stream and environment (semantic version + digest) | KnowledgeRelease | versioning scheme: established practice (Semantic Versioning 2.0.0, optional R65); application: proposed |
| Deploy | Activate the live pointer | EnvironmentBinding; registry publisher | proposed |
| Environment promotion | Promote the identical digest staging → production per tenant, through Chapter 27's canary and tenant-cohort stages | Chapter 27 § Promotion as a chain of evidence | proposed |
| Rollback | Reactivate a prior Active release by pointer | Chapter 27 § Roll back assignment, not history | proposed |
| Deprecation | Deprecated → Revoked with a compatibility window; retained while referenced | Chapter 8 lifecycle vocabulary | proposed |
| Monitoring | Decision records, refusals, contradictions, superseded citations, SME corrections | Chapter 24 spans; Chapter 25 Observe/Measure | proposed |
| Feedback → next change | Learning loop produces a ChangeBundle draft naming knowledge objects | Chapter 25 Recommend; Chapter 27 ChangeBundle | proposed |

## 4. The lifecycle, end to end

Enterprise sources → extraction → semantic representation → knowledge graph (candidate release) → validation (gates) → versioning (candidate digest, version allocation) → review/approval → publication (pointer activation) → runtime consumption (pinned per run) → monitoring → feedback → evolution (next change).

### 4.1 What a knowledge change is

A **knowledge change** is one reviewable unit that (a) names the objects it touches by stable id, (b) states its rationale and sources (digests), (c) declares a version bump, and (d) is resolved into one candidate effective release. A change may add or modify rules, vocabulary terms, ontology classes/relations, graph edges, decision tables, or an tenant extension. A change never deletes a released object; it deprecates it (deletion is retirement after the retention window, § 4.6). Scope check: the objects actually touched must equal the objects declared.

Ontology changes are **schema changes**: a renamed or removed class or relation invalidates instances. They carry a MAJOR bump, a migration (what happens to instances that conform to the old shape), and a coexistence window during which runs pinned to the old major version still resolve. A MINOR bump adds classes, relations, or terms without invalidating existing instances; a PATCH bump changes definitions, labels, or source spans without changing what conforms.

### 4.2 Branching and controlled development

| Situation | Branch? | Why |
| --- | --- | --- |
| One change to rules, terms, or graph data | Yes: one change, one branch, one candidate | A reviewable unit with a frozen identity |
| Long-lived "next quarter" branch of the whole knowledge base | No | Staleness: by the time it merges the base and the live release have moved; semantic conflicts hide in a clean textual merge |
| Tenant-specific deviations from a shared ontology or base policy | No branch; an **tenant extension** resolved against a pinned base | A branch forks the shared ontology; an tenant extension keeps it shared and makes the deviation explicit, versioned, and checkable. For *rules*: stricter than base is flagged and allowed; looser than a base floor is a conflict and blocks. For the *ontology*: an tenant extension may add classes, relations, properties, and terms; it may never remove, rename, or redefine a base element — that is a new major stream. Tenant extensions are tenant-private; only the base is shared. [reviewed: corrected — the stricter/looser rule was stated for the ontology too, where it has no meaning.] |
| Experimental ontology redesign | A separate stream (new major version) with its own releases | Coexistence window instead of a branch merge |
| Hotfix | Same path, priority review; documented break-glass with after-the-fact review, never bypass | Chapter 26 § Exceptions that expire (ExceptionWaiver) [reframed] |

### 4.3 Quality gates (named checks)

All gates run on the **effective candidate release**, not on the textual diff, because two edits that do not touch the same object can still produce a contradictory effective state. Each gate writes a record (name, version, inputs digest, result, findings) into the candidate's gate record; the registry publisher refuses a candidate whose gate record is incomplete or stale.

| Gate | Checks | Kind | Fails closed on | Limits (state in the chapter) |
| --- | --- | --- | --- | --- |
| `knowledge-schema` | Every object conforms to the ontology/schema it declares: required properties (owner, scope, effective_from, source span, data class), allowed node and edge kinds, value types and units; for RDF data, SHACL-style shape validation [R61]; for property graphs, schema constraints; for typed rules, the rule contract (`policy-to-rule`) | deterministic | any violation | Proves well-formedness, not meaning |
| `grounding` | Every source-derived claim re-verified against the pinned source digest and span (`grounding-verifier`); derived values verified structurally; one verdict per claim, verifier output must be complete | deterministic comparison (a model may locate evidence; the verdict needs a literal match) | any contradicted claim; incomplete verifier output | Proves the source says it, not that the source is right (Chapter 20 T-04) |
| `change-contract` | Scope declared = objects touched; rationale and sources present; version bump consistent with the kind of change (MAJOR for ontology-breaking) | deterministic | missing or mismatched | — |
| `consistency` | Contradictions: typed rules on the same subject with incompatible outcomes or modalities (`set-operations.contradictions`), across base + tenant extension and across the whole effective release; ambiguity: terms used in rules that are not defined in the vocabulary, concepts with no declared kind, scope dimensions not in the ontology → held for review, never filed under a guess | contradiction: deterministic for typed rules; ambiguity: deterministic for undefined terms, advisory for everything else | contradiction; undefined term in a decision-material field | Only sees contradictions the typing can express; prose contradictions, scope-conditional conflicts, and cross-vocabulary synonyms are invisible; a conflict between jurisdictions is scope, not contradiction |
| `duplicate-overlap` | Exact duplicates by content digest (`Rule.digest()`); overlap by shared subject with compatible outcomes; semantic near-duplicates proposed by a model are advisory and marked for review; never change deterministic alignment | exact: deterministic; semantic: advisory | exact duplicate inside one release | Paraphrase duplicates escape the digest; embedding similarity is a hint |
| `staleness` | Touched object revisions still match the target live release; pinned base release is the current base (or the change is an explicit base bump); candidate digest unchanged since submit; approval, if any, was given on this digest | deterministic | any mismatch → Stale; refresh, re-resolve, re-review | — |
| `regression` | Knowledge test suite replay: golden decision cases (facts → expected `true`/`false`/`unknown`), refusal cases (missing input → `unknown`), traversal fixtures (expected reachability and bounds), shape fixtures; impact diff vs the previous release in which every object is exactly one of `changed` / `unchanged` / `review-held` / `refused`, nothing dropped, and `review-held` never auto-resolves | deterministic | any golden case regressed; any object with no status | A suite is only as good as the cases SMEs authored; an empty suite passes and must be reported as empty, not green |
| `independent-approval` | An eligible SME (role recorded in the knowledge stream's owner record, Chapter 26) who is not the author and not the AI assistant approved this exact candidate digest; the approval record has the required fields | deterministic check of a human decision | author = approver; identity drift; missing note | The approval is the only gate that judges meaning |
| `release-integrity` | Bundle stored and verified (digest) before the pointer moves; the registry publisher is the actor; version allocated once per publication-attempt digest; target pointer equals expected previous digest (compare-and-swap) | deterministic | any failure → Publish failed, old release stays live, idempotent retry | — |

### 4.4 Lifecycle states

Reuse Chapter 8's Skill states, adding one mandatory human state (Approved) and omitting one (Staged — a knowledge release is Active *per environment*, so "running in staging" is Active in staging and the Staged state would duplicate the environment axis). "Stale" below is a flag on a Draft candidate, not a state; "Retired" is the retention event after Deprecated or Revoked, not a state. [reviewed: corrected — the original sentence claimed a pure superset of Chapter 8's states.]

| State | Means | Moves forward on |
| --- | --- | --- |
| Draft | Authored or proposed (by SME, extraction pipeline, or assistant); not resolvable | Candidate submitted; gates pass |
| Certified | All automated gates passed on a frozen candidate digest | Independent SME approval |
| Approved | Approved on that identity; any edit returns to Draft | Registry publisher activates |
| Active | The stream's live pointer for an environment names this release; resolvable by new runs | Successor release, or owner decision to deprecate |
| Deprecated | Not resolvable for new runs; runs that pinned it keep reading it for the compatibility window | Window expiry |
| Revoked | Not resolvable; in-flight runs pinned to it "pause or migrate by risk class" (Chapter 8's wording; the risk class is Chapter 22's, the tier Chapter 26's) | — |

"Approved" is the state Skills do not need as a separate step because certification suites can establish behavioural compatibility for code; for knowledge, semantic correctness has no automated oracle, so the human gate is explicit and mandatory. Retired releases are retained, read-only, for as long as any RunManifest within retention references them (Chapter 4 audit/WORM); deletion is a retention event, not a lifecycle state.

### 4.5 Publication semantics

- One approval authorizes the registry publisher to finish the whole operation: recheck → merge approved content → allocate version → store and verify bundle → move pointer → record activation. **Activation is the publication boundary.** Before it, nothing in the runtime can see the candidate; after it, new runs resolve it. A run never sees a mixture of two releases.
- Publish failed leaves the previous release live; retry is idempotent on the same attempt digest and never allocates a second version.
- Promotion carries the identical digest; the target environment records the source release; a diverged target blocks and is reconciled explicitly.
- Rollback moves the pointer to a prior Active release, mints no number, records reason and versions, and marks open changes Stale for re-evaluation. A repository revert alone does not complete a rollback (the pointer is runtime truth).
- Emergency deny (Chapter 27) may tenant extension a pinned release for in-flight runs; the run records both the pinned release and the higher-precedence denial.
- [reviewed: corrected — added] A knowledge activation changes production behaviour without an agent release, so it is a **change class** under Chapter 26 § Make review predictable: review depth follows change class × use-case tier (a vocabulary label fix in a T1 use case and a new eligibility threshold in a T4 use case do not get the same review), the `independent-approval` gate is the floor, and the shadow evaluation in § 3 is the evidence a T3/T4 activation needs. Without this sentence the lifecycle would let a knowledge change bypass the proportional review the book requires of every other behaviour change.

### 4.6 Deprecation and retirement

Deprecation is a release decision (a successor release or an owner decision), never an edit to a released object. Supersession is a relation in the new release (`supersedes`), not a change to the old one. Compatibility window: the longest run the use case admits plus the replay horizon; Harborlight's evidence review started three weeks ago finishes on the release it pinned (same rule as Chapter 8). Revocation is reserved for a defect serious enough to affect in-flight work (a rule that permits what the regulator forbids); it follows Chapter 23 § Stop new risky work without abandoning effects.

### 4.7 Monitoring and feedback

| Signal | Source | Denominator | Feeds |
| --- | --- | --- | --- |
| `unknown` verdicts per rule and per fact name | `:evaluate` decision records | all evaluations of that rule under that release | A rule whose required fact is never supplied is either mis-scoped or the fact pipeline is missing (ingestion plan) |
| Refusals at the effect boundary per rule | Tool Gateway / Effect Service records | effects attempted under the release | Rules that refuse too often or never |
| Runtime contradictions surfaced | `:evaluate` over base + tenant extension; acceptance engine | evaluations | A consistency-gate escape; becomes a regression case |
| Citations of superseded releases | retrieval spans (Chapter 24) | retrievals | Index not rebuilt after release; AP-09 metric |
| SME corrections and disputed interpretations | InterventionTask outcomes, review comments | review items | Proposed changes |
| Evaluation slice regressions after a knowledge release | Chapter 25 release gate on the agent, run against the new knowledge release | cases per slice | Shadow evidence for the next knowledge release |

Every signal is evidence into the control plane; none is a write. The learning loop (Chapter 25) drafts a ChangeBundle naming knowledge objects; it enters the lifecycle at Draft.

## 5. Where the software analogy breaks for knowledge

1. **Correctness is semantic.** Gates prove structure, grounding, resolution, and staleness; only an SME judges meaning. Shadow runs are evidence, not pass/fail.
2. **Authors are not engineers.** A review interface and the assistant's staged edits hide repository mechanics [reframed]; the registry publisher, not the author, performs the repository operations. Segregation of duties is enforced by the publisher's record plus the independent-approval check, not by repository permissions alone.
3. **A clean merge is not valid knowledge.** Two conflict-free edits can produce contradictory thresholds in the effective release; `consistency` and `staleness` therefore run on the resolved release and are stricter than code review.
4. **Audit carries compliance weight.** Every live version must be reconstructable: who changed what, why, who approved, what evidence existed. The release manifest records human identities, never only a bot's; the activation ledger lives in the audit archive, not in repository history.
5. **Knowledge has an upstream supply chain.** Regulatory and standards sources change on their own schedule; an update is a dependency bump that requires re-review of every tenant extension against the new floor. The source itself arrives as text, so the extraction pipeline sits inside the lifecycle, not before it.
6. **Pinning is per run, not per request.** One run uses one release per stream start to finish; a three-week evidence review does not change rules mid-flight.
7. **Ontology changes are migrations.** A class rename is a breaking change to every instance and every rule that names the class; versioning the schema separately from the instances, with a coexistence window, is the only way to keep old runs replayable.
8. **A graph diff is not a meaning diff.** Triple-level or record-level diffs show what changed, not what it affects; the impact diff over dependencies (rule → rule, rule → term, tenant extension → base) is the test-suite input, and `review-held` objects never auto-resolve.
9. **Contradiction can be legitimate.** Two jurisdictions may require different things; scope separates them. The gate flags, a human decides, and the release records the decision.
10. **The test suite is thin by default.** Golden cases must be authored by SMEs; the gate must report suite size and coverage so an empty suite cannot pass as green.

## 6. Harborlight thread for the lifecycle (synthetic)

- Stream `mortgage-policy`, pinned base `upstream-base@2026.08` (a synthetic release of an authoritative upstream source; no real regulator, law, or regulation is named) [reframed], tenant tenant extension for `harborlight-us-west`, ontology `mortgage-ontology@3.2`. Active release in production: `mortgage-policy@2026.09` (the version Chapters 3 and 8 already name). Objects in the thread, in the chapter's compliance vocabulary: requirement "income evidence must be current at decision time" (from the upstream source) → obligation "verify income with a pay statement no older than the window" (subject: underwriting; scope: US; effective from the release) → control: the age-window rule → constraint: the Tool Gateway's three-valued reading of it.
- The upstream requirement changes: the acceptable pay-statement age window shortens. The control plane opens change `change/pay-statement-age-window`: a base bump plus the tenant extension re-check. Extraction (Chapter 5 § Turn policy prose…) proposes rule v2 with its span; `grounding` passes; `knowledge-schema` passes; `consistency` finds the old and new rule on the same subject with different thresholds and the change declares `supersedes`, so it is supersession, not contradiction; the tenant extension's stricter window is flagged and allowed; `regression` replays the golden cases (15-day statement acceptable; 75-day statement not; missing `pay_statement_age_days` → `unknown`) and reports the impact diff (one rule `changed`, two eligibility rules `unchanged`, one income rule `review-held` because its term "qualifying income" is undefined in the vocabulary — the ambiguity finding).
- The underwriting policy owner, not the author, approves the candidate digest; the registry publisher publishes `mortgage-policy@2026.10` to staging, then promotes the same digest to production. Run `RUN-98217`, admitted last week, keeps `2026.09`; new runs pin `2026.10`.
- At the effect boundary the enforced age-window rule evaluates `pay_statement_age_days` from the verified KnowledgeArtifact (ingestion plan); if the fact is absent, `UnknownUnderPolicy`; the income rule, `review-held`, is not in the release's evaluable set, so a plan node that needs it is refused at compile time (Chapter 12), naming the rule, and the case escalates (Chapter 14).
- A reviewer finds the new window was transcribed with the wrong unit; rollback moves production's pointer back to `2026.09`; runs that pinned `2026.10` continue (an age-window rule is not a safety defect) and are listed for re-evaluation; the open change returns to Draft as Stale; the regression suite gains the unit case.
