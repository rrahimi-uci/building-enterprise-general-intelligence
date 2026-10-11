# Knowledge CI/CD model — control plane, runtime plane, lifecycle, gates

Supporting file for `chapter-update-plan.md` §§ 4–6. Everything here is a **book-authored proposal** unless a reference ID is given. The mental model is the author-supplied "Policy Workbench — GitHub Process Mapping" (unpublished; not citable) adapted from policies and playbooks to knowledge objects, ontologies, and graphs, and the lifecycle discipline of Policy Logic Forge [R48] adapted from one pipeline to an enterprise control plane. Neither is described in the chapter; only the adapted design is.

## 1. Two planes and the interface between them

### 1.1 Control plane (develop knowledge)

Owns: creation, extraction (Chapter 5 § Turn policy prose…, and the ingestion plan's § Ingest documents…), modelling (ontology and vocabulary), validation, versioning, testing, independent approval, publication, promotion, rollback, deprecation, retirement. Lives in the global control tier (Chapter 4 § Global control and regional cells), next to the Skill Registry and the Release Registry. Writers: knowledge owners and SMEs (through a workbench or a repository), the AI assistant that proposes staged edits, and exactly one service identity that may publish: the **publishing controller**. Holds no run state.

### 1.2 Runtime plane (consume releases)

Owns: resolve a release at admission, retrieve, traverse, query, evaluate, enforce — over approved knowledge only, read-only, inside the regional execution cell. Consumers (the book's control points): Context Service / Retrieval Broker (Chapter 6), plan compiler (Chapter 12), policy decision point (Chapter 21), Tool Gateway and Effect Service (Chapter 22), acceptance engine (Chapter 13), and read-only knowledge tools behind the Tool Gateway (Chapter 3). Never writes knowledge. Memory writes (Chapter 6) are a different store with a different gate and never enter a release.

### 1.3 Interface

| Crosses | Direction | Object | Carried by | Notes |
| --- | --- | --- | --- | --- |
| Release | down | **KnowledgeRelease** manifest + content-addressed bundle | Knowledge registry → regional last-known-good replica | Immutable; signed by the controller; digest is the identity |
| Live pointer | down | **EnvironmentBinding** for a knowledge stream (tenant · environment · region → release digest) | Publishing controller moves it; registry serves it | Same record type as Chapter 27's binding, scoped to a knowledge stream; "main" is approved desired state, the pointer is actual runtime state |
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

## 2. Vocabulary mapping (from the workbench model to knowledge)

| Workbench term | Knowledge-management term used in the chapter | Book record or component |
| --- | --- | --- |
| Playbook (stable-ID Markdown with metadata) | Knowledge object: a typed rule, a vocabulary term, an ontology class or relation, a graph node/edge set, a decision table | KnowledgeArtifact (ingestion plan) |
| Base release (agency) + lender overlay | Upstream base release (regulator, group policy, shared ontology) + tenant overlay | Knowledge stream with `base_pin` and `overlay_revision` |
| Resolve base + overlay into effective playbooks | Deterministic resolution into an effective release; unresolved semantic conflict blocks | Resolver (control plane), `resolver_version` in the manifest |
| Change = branch + PR | Knowledge change: one reviewable unit touching declared objects | Change record (`change_id`, scope, rationale, sources, version bump) |
| Juno (AI assistant proposes; no write credentials; never approves) | Extraction and curation assistant: proposes rules, terms, edges, impact lists; SME accepts; cannot approve or publish | Same constraint as Chapter 25's loop: never self-authored behaviour |
| Submit → candidate identity | Candidate identity = head revision + effective-release digest + source digests + target live digest + resolver version; frozen; any edit invalidates approval | Field group in the change record |
| Independent approval (different eligible human) | Independent SME approval of the exact candidate | KnowledgeApproval inside the release manifest (not Chapter 14's ApprovalDecision, which binds an *effect*) |
| Publishing controller | Publishing controller: sole merge/release/activation actor; rechecks scope, identity, freshness, pointer, eligibility, gates; stores and verifies the bundle before moving the pointer | Service identity in the global control tier |
| Release manifest (source of truth) + tag | KnowledgeRelease manifest | Appendix C row |
| Live pointer per environment | EnvironmentBinding for the stream | Chapter 27 record, knowledge-scoped |
| Promote identical bundle | Promote by digest equality; refuse if target diverged | Chapter 27 § Knowledge releases (new short subsection) |
| Rollback = reactivate prior approved release | Same; never rewrites history; in-flight runs keep their pin; open changes re-checked for staleness | Chapter 27 § Roll back assignment, not history |
| Runtime pins one bundle per loan | One run pins one release digest per stream for its whole life | RunManifest `knowledge_snapshots` |
| Decision record carries version + hash | Decision span carries release digest + rule ids | Chapter 24 |
| Audit trail = PR + manifest + activation ledger | Change record + release manifest + activation ledger in the audit/WORM archive (Chapter 4); repository history is not the compliance archive | Chapter 4 § Where each kind of state belongs |

## 3. Software CI/CD → knowledge management → book component

| Software CI/CD stage | Knowledge-management equivalent | Book component or record | Established or proposed |
| --- | --- | --- | --- |
| Source code | Knowledge objects in a repository or workbench: typed rules, vocabulary (SKOS/SBVR-style terms), ontology, graph data, decision tables, overlays | KnowledgeArtifact; ontology version | Representation: established [R47][R55]–[R58]; the unit set: proposed |
| Dependency lockfile | Pinned upstream base release (regulatory text release, group ontology) | `base_pin` in the stream | proposed (adapted) |
| Dependency-update bot | Upstream update proposal: a generated change that bumps the base pin and lists impacted objects; no automatic go-live | Change record opened by the control plane | proposed |
| Feature branch + PR | Knowledge change | Change record, candidate identity | proposed |
| Build | Resolve base + overlay + ontology into an effective release; content-address it | Resolver; release digest | proposed |
| Lint / static analysis | Named quality gates (§ 5) | Gate record in the manifest | shapes: established [R57]; the gate set: proposed |
| Unit / regression tests | Knowledge test suite: golden decision cases, refusal cases, traversal fixtures, shape fixtures; impact diff vs previous release | EvalCase / EvaluationResult (Chapter 25) | proposed |
| Integration test | Shadow evaluation of the candidate release on representative runs (observational, never pass/fail alone) | Chapter 27 Shadow stage | proposed |
| Code review | Independent SME approval of the whole candidate | KnowledgeApproval | proposed |
| Artifact registry | Knowledge registry: immutable bundles by digest | Knowledge registry (Chapter 4 store row) | proposed |
| Release tag | Release version per stream and environment (semantic version + digest) | KnowledgeRelease | versioning scheme: established practice (Semantic Versioning 2.0.0, optional R61); application: proposed |
| Deploy | Activate the live pointer | EnvironmentBinding; publishing controller | proposed |
| Environment promotion | Promote the identical digest staging → UAT → production per tenant | Chapter 27 § Promotion as a chain of evidence | proposed |
| Rollback | Reactivate a prior Active release by pointer | Chapter 27 § Roll back assignment, not history | proposed |
| Deprecation | Deprecated → Revoked with a compatibility window; retained while referenced | Chapter 8 lifecycle vocabulary | proposed |
| Monitoring | Decision records, refusals, contradictions, superseded citations, SME corrections | Chapter 24 spans; Chapter 25 Observe/Measure | proposed |
| Feedback → next change | Learning loop produces a ChangeBundle draft naming knowledge objects | Chapter 25 Recommend; Chapter 27 ChangeBundle | proposed |

## 4. The lifecycle, end to end

Enterprise sources → extraction → semantic representation → knowledge graph (candidate release) → validation (gates) → versioning (candidate identity, version allocation) → review/approval → publication (pointer activation) → runtime consumption (pinned per run) → monitoring → feedback → evolution (next change).

### 4.1 What a knowledge change is

A **knowledge change** is one reviewable unit that (a) names the objects it touches by stable id, (b) states its rationale and sources (digests), (c) declares a version bump, and (d) is resolved into one candidate effective release. A change may add or modify rules, vocabulary terms, ontology classes/relations, graph edges, decision tables, or an overlay. A change never deletes a released object; it deprecates it (deletion is retirement after the retention window, § 4.6). Scope check: the objects actually touched must equal the objects declared.

Ontology changes are **schema changes**: a renamed or removed class or relation invalidates instances. They carry a MAJOR bump, a migration (what happens to instances that conform to the old shape), and a coexistence window during which runs pinned to the old major version still resolve. A MINOR bump adds classes, relations, or terms without invalidating existing instances; a PATCH bump changes definitions, labels, or source spans without changing what conforms.

### 4.2 Branching and controlled development

| Situation | Branch? | Why |
| --- | --- | --- |
| One change to rules, terms, or graph data | Yes: one change, one branch, one candidate | A reviewable unit with a frozen identity |
| Long-lived "next quarter" branch of the whole knowledge base | No | Staleness: by the time it merges the base and the live release have moved; semantic conflicts hide in a clean textual merge |
| Tenant-specific deviations from a shared ontology or base policy | No branch; an **overlay** resolved against a pinned base | A branch forks the shared ontology; an overlay keeps it shared and makes the deviation explicit, versioned, and checkable (stricter than base: flagged and allowed; looser than a base floor: conflict, blocks) |
| Experimental ontology redesign | A separate stream (new major version) with its own releases | Coexistence window instead of a branch merge |
| Hotfix | Same path, priority review; documented break-glass with after-the-fact review, never bypass | Same as the workbench model and Chapter 26 exceptions |

### 4.3 Quality gates (named checks)

All gates run on the **effective candidate release**, not on the textual diff, because two edits that do not touch the same object can still produce a contradictory effective state. Each gate writes a record (name, version, inputs digest, result, findings) into the candidate's gate record; the publishing controller refuses a candidate whose gate record is incomplete or stale.

| Gate | Checks | Kind | Fails closed on | Limits (state in the chapter) |
| --- | --- | --- | --- | --- |
| `knowledge-schema` | Every object conforms to the ontology/schema it declares: required properties (owner, scope, effective_from, source span, data class), allowed node and edge kinds, value types and units; for RDF data, SHACL-style shape validation [R57]; for property graphs, schema constraints; for typed rules, the rule contract (`policy-to-rule`) | deterministic | any violation | Proves well-formedness, not meaning |
| `grounding` | Every source-derived claim re-verified against the pinned source digest and span (`grounding-verifier`); derived values verified structurally; one verdict per claim, verifier output must be complete | deterministic comparison (a model may locate evidence; the verdict needs a literal match) | any contradicted claim; incomplete verifier output | Proves the source says it, not that the source is right (Chapter 20 T-04) |
| `change-contract` | Scope declared = objects touched; rationale and sources present; version bump consistent with the kind of change (MAJOR for ontology-breaking) | deterministic | missing or mismatched | — |
| `consistency` | Contradictions: typed rules on the same subject with incompatible outcomes or modalities (`set-operations.contradictions`), across base + overlay and across the whole effective release; ambiguity: terms used in rules that are not defined in the vocabulary, concepts with no declared kind, scope dimensions not in the ontology → held for review, never filed under a guess | contradiction: deterministic for typed rules; ambiguity: deterministic for undefined terms, advisory for everything else | contradiction; undefined term in a decision-material field | Only sees contradictions the typing can express; prose contradictions, scope-conditional conflicts, and cross-vocabulary synonyms are invisible; a conflict between jurisdictions is scope, not contradiction |
| `duplicate-overlap` | Exact duplicates by content digest (`Rule.digest()`); overlap by shared subject with compatible outcomes; semantic near-duplicates proposed by a model are advisory and marked for review; never change deterministic alignment | exact: deterministic; semantic: advisory | exact duplicate inside one release | Paraphrase duplicates escape the digest; embedding similarity is a hint |
| `staleness` | Touched object revisions still match the target live release; pinned base release is the current base (or the change is an explicit base bump); candidate identity unchanged since submit; approval, if any, was given on this identity | deterministic | any mismatch → Stale; refresh, re-resolve, re-review | — |
| `regression` | Knowledge test suite replay: golden decision cases (facts → expected `true`/`false`/`unknown`), refusal cases (missing input → `unknown`), traversal fixtures (expected reachability and bounds), shape fixtures; impact diff vs the previous release in which every object is exactly one of `changed` / `unchanged` / `review-held` / `refused`, nothing dropped, and `review-held` never auto-resolves | deterministic | any golden case regressed; any object with no status | A suite is only as good as the cases SMEs authored; an empty suite passes and must be reported as empty, not green |
| `independent-approval` | An eligible SME (role recorded in the knowledge stream's owner record, Chapter 26) who is not the author and not the AI assistant approved this exact candidate identity; the approval note has the required fields | deterministic check of a human decision | author = approver; identity drift; missing note | The approval is the only gate that judges meaning |
| `publication-readiness` | Bundle stored and verified (digest) before the pointer moves; controller is the actor; version allocated once per publication-attempt identity; target pointer equals expected previous digest (compare-and-swap) | deterministic | any failure → Publish failed, old release stays live, idempotent retry | — |

### 4.4 Lifecycle states

Reuse Chapter 8's Skill states, adding one mandatory human state:

| State | Means | Moves forward on |
| --- | --- | --- |
| Draft | Authored or proposed (by SME, extraction pipeline, or assistant); not resolvable | Candidate submitted; gates pass |
| Certified | All automated gates passed on a frozen candidate identity | Independent SME approval |
| Approved | Approved on that identity; any edit returns to Draft | Publishing controller activates |
| Active | The stream's live pointer for an environment names this release; resolvable by new runs | Successor release, or owner decision to deprecate |
| Deprecated | Not resolvable for new runs; runs that pinned it keep reading it for the compatibility window | Window expiry |
| Revoked | Not resolvable; in-flight runs pinned to it pause or migrate by use-case tier (Chapter 26) and effect risk class (Chapter 22) | — |

"Approved" is the state Skills do not need as a separate step because certification suites can establish behavioural compatibility for code; for knowledge, semantic correctness has no automated oracle, so the human gate is explicit and mandatory. Retired releases are retained, read-only, for as long as any RunManifest within retention references them (Chapter 4 audit/WORM); deletion is a retention event, not a lifecycle state.

### 4.5 Publication semantics

- One approval authorizes the controller to finish the whole operation: recheck → merge approved content → allocate version → store and verify bundle → move pointer → record activation. **Activation is the publication boundary.** Before it, nothing in the runtime can see the candidate; after it, new runs resolve it. A run never sees a mixture of two releases.
- Publish failed leaves the previous release live; retry is idempotent on the same attempt identity and never allocates a second version.
- Promotion carries the identical digest; the target environment records the source release; a diverged target blocks and is reconciled explicitly.
- Rollback moves the pointer to a prior Active release, mints no number, records reason and versions, and marks open changes Stale for re-evaluation. A repository revert alone does not complete a rollback (the pointer is runtime truth).
- Emergency deny (Chapter 27) may overlay a pinned release for in-flight runs; the run records both the pinned release and the higher-precedence denial.

### 4.6 Deprecation and retirement

Deprecation is a release decision (a successor release or an owner decision), never an edit to a released object. Supersession is a relation in the new release (`supersedes`), not a change to the old one. Compatibility window: the longest run the use case admits plus the replay horizon; Harborlight's evidence review started three weeks ago finishes on the release it pinned (same rule as Chapter 8). Revocation is reserved for a defect serious enough to affect in-flight work (a rule that permits what the regulator forbids); it follows Chapter 23 § Stop new risky work without abandoning effects.

### 4.7 Monitoring and feedback

| Signal | Source | Denominator | Feeds |
| --- | --- | --- | --- |
| `unknown` verdicts per rule and per fact name | `:evaluate` decision records | all evaluations of that rule under that release | A rule whose required fact is never supplied is either mis-scoped or the fact pipeline is missing (ingestion plan) |
| Refusals at the effect boundary per rule | Tool Gateway / Effect Service records | effects attempted under the release | Rules that refuse too often or never |
| Runtime contradictions surfaced | `:evaluate` over base + overlay; acceptance engine | evaluations | A consistency-gate escape; becomes a regression case |
| Citations of superseded releases | retrieval spans (Chapter 24) | retrievals | Index not rebuilt after release; AP-09 metric |
| SME corrections and disputed interpretations | InterventionTask outcomes, review comments | review items | Proposed changes |
| Evaluation slice regressions after a knowledge release | Chapter 25 release gate on the agent, run against the new knowledge release | cases per slice | Shadow evidence for the next knowledge release |

Every signal is evidence into the control plane; none is a write. The learning loop (Chapter 25) drafts a ChangeBundle naming knowledge objects; it enters the lifecycle at Draft.

## 5. Where the software analogy breaks for knowledge

1. **Correctness is semantic.** Gates prove structure, grounding, resolution, and staleness; only an SME judges meaning. Shadow runs are evidence, not pass/fail.
2. **Authors are not engineers.** The workbench, the assistant's staged edits, and the review interface hide repository mechanics; the controller, not the author, performs the repository operations. Segregation of duties is enforced by the controller's record plus the independent-approval check, not by repository permissions alone.
3. **A clean merge is not valid knowledge.** Two conflict-free edits can produce contradictory thresholds in the effective release; `consistency` and `staleness` therefore run on the resolved release and are stricter than code review.
4. **Audit carries compliance weight.** Every live version must be reconstructable: who changed what, why, who approved, what evidence existed. The release manifest records human identities, never only a bot's; the activation ledger lives in the audit archive, not in repository history.
5. **Knowledge has an upstream supply chain.** Regulatory and agency sources change on their own schedule; an update is a dependency bump that requires re-review of every overlay against the new floor. The source itself arrives as text, so the extraction pipeline sits inside the lifecycle, not before it.
6. **Pinning is per run, not per request.** One run uses one release per stream start to finish; a three-week evidence review does not change rules mid-flight.
7. **Ontology changes are migrations.** A class rename is a breaking change to every instance and every rule that names the class; versioning the schema separately from the instances, with a coexistence window, is the only way to keep old runs replayable.
8. **A graph diff is not a meaning diff.** Triple-level or record-level diffs show what changed, not what it affects; the impact diff over dependencies (rule → rule, rule → term, overlay → base) is the test-suite input, and `review-held` objects never auto-resolve.
9. **Contradiction can be legitimate.** Two jurisdictions may require different things; scope separates them. The gate flags, a human decides, and the release records the decision.
10. **The test suite is thin by default.** Golden cases must be authored by SMEs; the gate must report suite size and coverage so an empty suite cannot pass as green.

## 6. Harborlight thread for the lifecycle (synthetic)

- Stream `mortgage-policy`, base pin `agency-base@2026.08` (fictional regulator release), tenant overlay for `harborlight-us-west`, ontology `mortgage-ontology@3.2`. Active release in production: `mortgage-policy@2026.09` (the version Chapters 3 and 8 already name).
- The regulator shortens the acceptable pay-statement age window. The control plane opens change `change/pay-statement-age-window`: a base bump plus the overlay re-check. Extraction (Chapter 5 § Turn policy prose…) proposes rule v2 with its span; `grounding` passes; `knowledge-schema` passes; `consistency` finds the old and new rule on the same subject with different thresholds and the change declares `supersedes`, so it is supersession, not contradiction; the overlay's stricter window is flagged and allowed; `regression` replays the golden cases (15-day statement acceptable; 75-day statement not; missing `pay_statement_age_days` → `unknown`) and reports the impact diff (one rule `changed`, two eligibility rules `unchanged`, one income rule `review-held` because its term "qualifying income" is undefined in the vocabulary — the ambiguity finding).
- The underwriting policy owner, not the author, approves the candidate identity; the controller publishes `mortgage-policy@2026.10` to staging, then promotes the same digest to production. Run `RUN-98217`, admitted last week, keeps `2026.09`; new runs pin `2026.10`.
- At the effect boundary the enforced age-window rule evaluates `pay_statement_age_days` from the verified KnowledgeArtifact (ingestion plan); if the fact is absent, `UnknownUnderPolicy`; the income rule, `review-held`, is not in the release's evaluable set, so a plan node that needs it is refused at compile time (Chapter 12), naming the rule, and the case escalates (Chapter 14).
- A reviewer finds the new window was transcribed with the wrong unit; rollback moves production's pointer back to `2026.09`; runs that pinned `2026.10` continue (an age-window rule is not a safety defect) and are listed for re-evaluation; the open change returns to Draft as Stale; the regression suite gains the unit case.
