# Chapter 27 — Release New Behavior Without Breaking Work in Flight: Continuity and Flow Review

Reviewed: `source/parts/08-part-viii.md:126–461`. Context read: Ch 26 close (`:107–124`), Ch 28 opening (`:463–533`), Ch 04 § RunManifest and cells (`02-part-ii.md:87`, `:116–140`, `:172–193`, `:319–336`), Ch 15 durable execution (`04-part-iv.md:1204–1259`, `:1333`, `:1350`), Ch 25 learning loop and records (`07-part-vii.md:356–404`, `:474`, `:490–491`), Ch 01 Friday failure (`01-part-i.md:127–136`), Ch 22 § Risk classes, Ch 23 kill switch, Appendix C/D/L, Figure 27-1 source (`assets/diagrams/src/release-recovery.gv`).

## Overall Assessment

The core of Chapter 27 is excellent and unique. It covers "treat the full behavior as the release", rollback that changes *assignment* rather than history, and the tool-schema walkthrough (`:154–180`). This is the book's canonical home for release semantics, and the walkthrough table is the clearest worked example in Part VIII.

The chapter is overloaded with material that belongs elsewhere or is already taught:

- a deployment topology that re-teaches Ch 04's control-plane/cell split under a conflicting name;
- generic deployment guidance (isolation, secrets, worker classes) owned by Ch 21/23/28;
- a technology stack that duplicates Appendix D;
- a promotion "Learn" stage that re-teaches Ch 25's loop;
- the whole governance implementation, which belongs to Ch 26;
- compatibility bullets that repeat Ch 15.

The result is a chapter in which the release mental model is diluted, and the reader cannot tell which parts are new.

Two terminology defects contradict earlier chapters:

1. **RunManifest vs ReleaseManifest conflation.** `:158` says Northstar "pins the [ReleaseManifest] to each run". `:230` says "Resolve every run to an immutable RunManifest". `:310` defines a separate ReleaseBundle entity, and the code types a *worker* as a ReleaseManifest (`:376`). Ch 04's RunManifest (`02-part-ii.md:174–193`) carries no reference to any release.
2. **"Execution plane".** Ch 27 uses it for a regional environment (`:186`, `:191`, `:200`, `:455`). Ch 04 uses "Execution plane" for the sandbox layer (`02-part-ii.md:140`) and "regional execution cells" for what Ch 27 means (`:87`).

Regional recovery, a distinct topic from rollback, is filed under § Rollback and active runs and stated three times with drift. Its "resume by risk tier" step uses an undefined scale.

## Intended Reader Mental Model

- **What:** a release is an immutable, signed graph of everything that can change behavior. It is not a container image.
- **Why:** model aliases drift, prompts and tools interact, runs outlive deployments, and Ch 01's Friday failure is a release failure.
- **How:**
  - A ChangeBundle (Ch 25) is promoted into a ReleaseManifest.
  - An EnvironmentBinding assigns a ReleaseManifest to new starts.
  - Each run's RunManifest (Ch 04) records the ReleaseManifest it was admitted under.
  - Compatible workers serve old manifests.
  - Rollback moves the binding.
  - Promotion is a chain of evidence carried by the same signed artifact.
- **When:** rollback for a bad candidate; emergency deny and revocation for immediate risk (separate from release); explicit tested migration only when an active run must change.
- **Trade-offs:** pinning costs storage and discipline, and buys reproducibility, rollback, and investigation.
- **Relationships:** Ch 15 keeps histories replayable on compatible builds. Ch 25 produces the evidence the gates consume. Ch 26 sets gate depth. Ch 04 cells bound where a release runs. Ch 22 reconciles effects before resuming after failover. Ch 23 owns the kill switch.
- **Practical:** design CI/CD gates and a regional recovery sequence.

## Section-by-Section Flow Review

**Opening (`:128–136`): evidence context, NORTHSTAR box, THE DESIGN CHOICE.**
- The evidence context cites NIST SP 800-61 [R42] for an "incident lifecycle" the chapter does not teach. Ch 20 teaches it (`06-part-vi.md:272`). The chapter's actual evidence claims are SBOM/SLSA [R17][R18] (`:346`) (C27-R06).
- The boxes are good and state the thesis. NORTHSTAR naming follows the global T1 decision.

**§ Why a release is more than a deployment (`:138–144`).** Role: intro. Clear. It is missing a callback to Ch 01's Friday failure (`01-part-i.md:127–136`), which is the same problem in its smallest form, and an inbound bridge from Ch 26 ("who may approve" → "how approved change is applied") (C27-R11).

**§ Keep releases immutable and workers compatible (`:146–152`).** It contains only Figure 27-1 and the state-owner table, with no prose. The table's Core contracts ("CompatibilityMatrix · RolloutPlan") do not match the chapter's records (CompatibilityRule, PromotionDecision, EnvironmentBinding) (C27-R10). Verdict: merge into the next H2 (C27-R09).

**§ Treat the full behavior as the release (`:154–160`).** Role: core concept. `:156` is the chapter's best paragraph. `:158` gives the first of five release-content lists and introduces the RunManifest/ReleaseManifest conflation. `:160` (CI and CD) is good. Verdict: keep. Add the four-object chain (C27-R01) and point the content list at § Versioned objects (C27-R09).

**### Rollback and active runs (`:162–166`).** `:164` is canonical and excellent. `:166` (regional recovery) is a different topic: failover, not rollback. It depends on the topology that comes 20 lines later, and it says "resumes by risk tier" without naming the scale. Verdict: keep `:164`; move `:166` (C27-R07).

**### A release walkthrough (`:168–180`).** This is the best worked example in Part VIII and uses the running case's tool. `:170` says "compatibility matrix" where the records say CompatibilityRule. `:180` gives the "roll back the model is incomplete" argument, which the PRODUCTION CONSIDERATION box (`:338–340`) and Q1 (`:453`) repeat. Verdict: keep. The last row ("Region fails during a write") is a good bridge to recovery.

**§ A deployment shape that supports safe change (`:182`).** An empty wrapper H2 (map §5.3). Verdict: add a one-sentence lead that recalls Ch 04 (C27-R02).

**### A production topology that is easy to reason about (`:184–195`).** Role: control plane vs regional environment. It adds the "What it must not assume" column and the fail-closed/last-known-good rule (`:195`); both are new and valuable. Issues:
- "Regional execution plane" collides with Ch 04's "Execution plane" (sandbox layer).
- The split itself was taught in Ch 04 (`02-part-ii.md:87`, Q `:333`), and the last-known-good rule appears in Ch 04 Q `:336`.
- None of this is acknowledged.

Verdict: keep, renamed, with a recall (C27-R02).

**### Deployment guidance (`:197–206`).**
- Bullets "Control plane", "Regional execution planes", "Release", and "Disaster recovery" are release/recovery-relevant.
- "High availability" is partly relevant ("multi-region without replay tests is not a resilience claim").
- "Isolation" (`:202`) re-teaches Ch 21 (`06-part-vi.md:432`, `:506`). "Worker classes" (`:203`) re-teaches Ch 23 sandbox profiles and Ch 28 pools (`:549`). "Secrets" (`:204`) re-teaches Ch 21/23 credential leases.

Verdict: condense to the four release-relevant bullets (C27-R03).

**### Suggested baseline stack—not a mandate (`:208–221`).** A technology-selection table that duplicates Appendix D's framework tables (`09-appendices.md:81`, `:98`) and is unrelated to release flow. Verdict: move to Appendix D (map S10) (C27-R03).

**§ Version every artifact that can change behavior (`:223–233`).** A Required-analysis table. The "Recommended architecture" row contains the RunManifest sentence that contradicts `:158`. "Failure scenarios" duplicates the walkthrough. "Enterprise example: regulated underwriting" is effectively Harborlight, unnamed. "Design alternatives" and "Trade-offs" carry the only new content. Verdict: delete the table and keep two sentences (C27-R09).

**### Versioned objects (`:235–249`).** An 11-row table of version rule and promotion gate. This is the most complete release-content list in the book and should be the canonical one. It sits after the topology, far from § Treat the full behavior, where it is needed. Verdict: move up (C27-R09).

**### Promotion and continuous-improvement loop (`:251–264`).** "Promotion is a chain of evidence" (`:253`) is strong. The Build → Evaluate → Shadow → Canary → Promote rows expand Ch 25's Validate → Approve → Deploy → Monitor stages (`07-part-vii.md:400–403`) but never say so. The "Learn" row (`:262`) and paragraph `:264` re-teach Ch 25 § Close the loop / § Automate only when regressions are contained. Verdict: keep Build–Promote, map them to Ch 25, and drop Learn (C27-R04).

**### Governance controls (`:266–274`).** These are Ch 26's concepts (inventory, control mapping, pre-release documentation, evidence package, explanations). Bullet 5 (telemetry access separation) is already in Ch 24 (`07-part-vii.md:62`) and Ch 25 (Content Vault, `:349`). Bullet 7 duplicates Ch 25 (`:389`, `:436`) and Ch 27's own `:264`. Verdict: move or delete (C27-R05).

**§ A workable implementation (`:276`).**
- **### Who should own each decision (`:278–289`).** The release components are right. Governance Inventory belongs in Ch 26. Emergency Control should point to Ch 23 § Scoped operational kill switch. Drift Monitor overlaps Ch 25's Detect stage (DetectionEvent). Verdict: trim and add pointers (C27-R05, R10).
- **### The contracts between components (`:291–303`).** The release APIs are good. `:evaluate` (`:297`) collides with Ch 25 `POST /v1/release-gates:evaluate` and `/v1/eval-runs` (`07-part-vii.md:363–365`). The governance APIs (`:302–303`) belong in Ch 26. `manifests:resolve` (`:299`) is where the RunManifest → ReleaseManifest relation should be explicit. Verdict: trim and align (C27-R01, R05, R10).
- **### Records worth preserving (`:305–318`).** ReleaseBundle and ReleaseManifest are two names for one thing. EvaluationEvidence overlaps Ch 25 ReleaseGateDecision. GovernanceRecord and ExceptionWaiver belong in Ch 26. Verdict: align (C27-R01, R05, R10).
- **### Compatibility and long-running execution (`:320–326`).** Bullets 1–2 repeat Ch 15 (`04-part-iv.md:1248`, Q `:1350`) and `:164`. Bullets 3–5 (fallback as a versioned route, emergency-deny precedence, knowledge-snapshot reproducibility levels) are new, release-level, and valuable. Verdict: condense (C27-R08).
- **### Scalability and control-plane resilience (`:328–336`).** Useful (digest-keyed regional caches, resolve once at admission, dependency-edge index for "what uses this version?", tombstones). `:331` restates `:195`. Verdict: keep and trim `:331` (C27-R08).
- **PRODUCTION CONSIDERATION box (`:338–340`).** Restates `:156`, `:180`, and Q1. Verdict: delete (C27-R09).

**§ What the evidence lets us conclude (`:342–348`).** One supply-chain row [R17][R18]. Fine. `:348` lists R42, which no claim in the chapter uses (C27-R06).

**§ A sensible place to start (`:350–424`).** An empty H2 lead, then two inline code blocks with no `[[EXAMPLE:…]]` marker, contrary to `AGENTS.md`.
- `compatible(run: ReleaseManifest, worker: ReleaseManifest)` types a worker's capability as a release.
- `verify_release_artifact` checks signer and builder identity strings against allowlists. It performs no cryptographic signature verification, although `:346` says "verify signatures".

Verdict: move to `examples/` and fix the typing and caption (C27-R13).

**Template sections (`:426–457`).**
- If-fails: 3 steps, fine.
- Checklist: `:434` repeats the conflation (C27-R01). The rest are fine.
- Put the idea to work: good, and exercise 2 rehearses the recovery sequence.
- Questions: Q1 and Q2 are reinforcement (acceptable), but Ch 25 Q `07-part-vii.md:490–491` duplicates them. Ch 27 is the owner. Q3 needs the rename. Q4 re-teaches Ch 25 (C27-R04). Q5's recovery sequence includes "Stop admission", which `:166` lacks (C27-R07).

**§ Where this leads next (`:459–461`).** Accurate and concise. Verdict: keep.

## Sparse or Underdeveloped Content

- **The release object chain.** The chapter never defines how ChangeBundle, ReleaseManifest, EnvironmentBinding, and RunManifest relate. One paragraph fixes this (C27-R01). It is the main conceptual gap.
- **Regional recovery** is a canonical sequence the book needs (Ch 04, 15, and 22 all defer to it), but here it is a single dense sentence (`:166`). A numbered seven-step list in its own H3 is warranted (C27-R07).
- **Deprecation impact analysis** (`:301`, `:333`) is mentioned only in an API row and a scalability bullet. It is the release-side counterpart of Ch 08's deprecation window (`03-part-iii.md:292`). It deserves the replacement design-review question (C27-R04), not a new section.

Nothing else needs expansion. The chapter's problem is excess, not sparseness.

## Missing Conceptual Connections

- **Ch 25 ChangeBundle (`07-part-vii.md:399`) → Ch 27 ReleaseManifest**, missing "a ChangeBundle becomes a ReleaseManifest only when promoted". Ch 27 never uses "ChangeBundle". Location: `:158` (C27-R01).
- **Ch 04 RunManifest (`02-part-ii.md:174`) → Ch 27 ReleaseManifest**, missing the reference field and the sentence "a RunManifest records the ReleaseManifest digest plus run-specific subject, purpose, budget, and knowledge-snapshot choice". Location: `:158`, `:230`, `:299`, `:434` (C27-R01). Ch 04 needs the field (Ch 04 reviewer).
- **Ch 04 global control plane / regional execution cells → Ch 27 topology**, missing the recall. Location: `:184–186` (C27-R02).
- **Ch 15 Version Router and compatible task queues (`04-part-iv.md:1204`, `:1248`) → Ch 27 compatibility matrix**, missing "the Version Router is what enforces this chapter's compatibility rules at dispatch". Location: `:170` or § Compatibility (C27-R08).
- **Ch 25 Validate/Approve/Deploy/Monitor → Ch 27 Build/Evaluate/Shadow/Canary/Promote**, missing a mapping sentence. Location: `:253` (C27-R04).
- **Ch 26 tier → "risk-tiered eval gates" (`:230`, `:258`)**, missing a pointer to C26-R02's review-depth rule. Location: `:258` row Evaluate (C27-R04).
- **Ch 22 effect reconciliation and R-classes → recovery "resume by risk tier"**, missing the scale. Location: `:166`, `:457`, Figure 27-1 edge label (C27-R07).
- **Ch 20 incident lifecycle (Recover stage) → regional recovery**, missing the link that the evidence context implies. Location: `:128` (C27-R06).
- **Ch 01 Friday failure → this chapter**, missing the callback. Location: `:138–144` (C27-R11).
- **Ch 23 kill switch → Emergency Control (`:289`)**, missing a pointer (C27-R10).

## Transition Problems

- **Inbound (Ch 26 → Ch 27).** Ch 26's close is accurate, but Ch 27's opening does not acknowledge it, and Ch 27 then re-implements governance (§ Governance controls). C27-R05 and C27-R11.
- **Within the chapter.**
  - The order runs concept → topology → stack → versioning table → promotion → governance → implementation. The versioned-objects table, which defines what "the full behavior" contains, arrives after the topology and the stack.
  - Regional recovery appears before the topology it depends on.
  - § Keep releases immutable… is a heading with no prose. § A deployment shape… is an empty wrapper.
  - See C27-R09 for the order.
- **Outbound (Ch 27 → Ch 28).** The sentence is accurate. Ch 28 could pick up "release cohorts" and "canary volume" as a capacity consumer, but this is not required.

## Redundant and Repetitive Concepts

- **Release contents ×6:** `:158`, `:170`, `:230`, `:235–249`, `:363–373` (code), `:340` (box). Canonical: § Versioned objects. The others shrink to pointers or are deleted (C27-R09).
- **Rollback changes assignment, not history ×8:** design choice `:136`, NORTHSTAR `:132`, `:164`, `:176`, `:300`, `:322`, `:436`, `:454`, plus Figure 27-1. The boxes, `:164`, the walkthrough row, the checklist, and Q2 are acceptable reinforcement. Delete `:322` (C27-R08).
- **"Roll back the model is incomplete" ×3:** `:180`, `:340`, `:453`. Delete the box (C27-R09).
- **Regional recovery sequence ×3 with drift:** `:166`, `:457` (adds "Stop admission"), and partially `:178` and `:206`. One canonical list (C27-R07).
- **Last-known-good / fail closed ×3:** `:195`, `:331`, `:455`. Keep `:195`, trim `:331`, keep Q3 short (C27-R08).
- **Never self-rewrite production ×2:** `:264`, `:274`. Both are deleted in favor of Ch 25 (C27-R04, R05).

## Cross-Chapter Duplication

| Other location | Content | Verdict | Owner / action |
| --- | --- | --- | --- |
| Ch 04 `02-part-ii.md:87`, `:319`, Q `:333`, Q `:336` | Global control plane vs regional execution cells; last-known-good during control-plane outage | D in Ch 27 under a conflicting name | Ch 04 owns design. Ch 27 keeps the operational "must not assume" view with a recall and the rename (C27-R02) |
| Ch 04 § RunManifest (`02-part-ii.md:172–193`) | Per-run pins without a release reference | Gap/drift | Ch 04 reviewer adds `"release_manifest": "sha256:..."`. Ch 27 states the relation (C27-R01) |
| Ch 03 § Framework upgrades are behavioral changes, RunManifest table | Version-pin list | D (map) | Ch 04/Ch 03 reviewers |
| Ch 15 `04-part-iv.md:1204` (Version Router), `:1217` (`:migrate`), `:1248`, `:1259` (RTO/RPO), `:1333`, Q `:1350` | Compatible workers for in-flight histories; migration; DR objective | Ch 27 `:320–323` D; `:164` R | Ch 15 owns workflow-level compatibility. Ch 27 keeps release-level additions (C27-R08). Ch 27 owns regional DR (C27-R07); Ch 15's `:1259` row stays as a one-line pointer |
| Ch 25 § Close the loop… (`07-part-vii.md:387–404`), § Automate only… (`:436`) | Learning loop, no self-rewrite | Ch 27 `:262–264`, `:274` D | Ch 25 owns (C27-R04, R05) |
| Ch 25 Q `07-part-vii.md:490–491` | Release bundle contents; rollback without breaking active runs | D of Ch 27 Q1/Q2 and `:158`/`:164` | Ch 27 owns. Ch 25 reviewer deletes both Qs, or replaces them with evaluation questions |
| Ch 25 records ReleaseGateDecision, `release-gates:evaluate` (`07-part-vii.md:365`, `:380`) | Gate evaluation | Ch 27 `:297`, `:312` collide | Ch 25 owns the gate. Ch 27 references it (C27-R10) |
| Ch 07 golden path Package/Improve (`03-part-iii.md:64`, `:105`, `:108`) | ReleaseManifest, ChangeBundle | R (preview) | Keep. Ch 27 canonical |
| AP-15 / AP-16 (`04-part-iv.md:1847–1863`) | Model swap as config; in-place change | R (anti-pattern view) | Keep |
| Ch 08 deprecation window (`03-part-iii.md:292`) | Compatibility window for active runs | R | Keep. Ch 27 `:301` is the platform-wide form |
| Ch 23 kill switch (`06-part-vi.md:1127`) | Scoped kill switch | R | Ch 27 Emergency Control points to Ch 23 (C27-R10) |
| Ch 21 isolation and credentials (`06-part-vi.md:432`, `:506`) | Tenant isolation, secrets | Ch 27 `:202`, `:204` D | Delete from Ch 27 (C27-R03) |
| Ch 26 (whole chapter) | Governance | Ch 27 `:266–274`, `:288`, `:302–303`, `:316–317` misplaced | Move to Ch 26 (C26-R03, C27-R05) |
| Ch 20 incident lifecycle (`06-part-vi.md:272`) | Detect → … → Recover → Learn | Ch 27 evidence context promises it | C27-R06 |
| Appendix D (`09-appendices.md:81`, `:98`) | Framework landscape | Ch 27 `:208–221` D | Move to Appendix D (Appendices reviewer merges) |
| Appendix C ReleaseManifest/RunManifest (`09-appendices.md:65`, `:75`) | Contract summary | R, with drift | Appendices reviewer aligns to C27-R01 |
| Appendix L Supply chain/Durability rows (`09-appendices.md:552`, `:556`) | Acceptance evidence | R | Keep |

## Structural Recommendations

Proposed order (no content added except C27-R01's chain paragraph and C27-R07's list):

1. Opening boxes (evidence context fixed per C27-R06).
2. § Why a release is more than a deployment (with the Ch 01/Ch 26 bridge).
3. § Treat the full behavior as the release: Figure 27-1, the state-owner table, `:156`, the four-object chain, § Versioned objects (moved up), the CI/CD paragraph `:160`, and a two-sentence alternatives/trade-offs summary replacing the Required-analysis table.
4. § Roll back assignment, not history: `:164`, compatibility bullets 3–5 from § Compatibility, and § A release walkthrough.
5. § Promotion as a chain of evidence: the stages table without Learn, mapped to Ch 25.
6. § A deployment shape that supports safe change: a lead recalling Ch 04, the renamed topology table, condensed deployment guidance, and the new § Regional recovery.
7. § A workable implementation: release-only owners, APIs, and records, with § Scalability and control-plane resilience.
8. Evidence, start (examples), and the template sections.

This agrees with map S10 (governance → Ch 26, stack → Appendix D, topology → reference Ch 04). The NIST 800-61 evidence context is fixed rather than moved.

**Disagreement with the concept map:** none. One refinement: the map's §3 row says Ch 27 regional cells are "D, renamed". The "What it must not assume" column and the fail-closed vs last-known-good distinction are new operational content, so the topology section should be renamed and trimmed, not removed.

## Concrete Recommended Changes

1. **C27-R01 — High — Rewrite.** Location: `08-part-viii.md:158` (§ Treat the full behavior as the release); `:230` (§ Version every artifact…, Recommended architecture row); `:299` (`manifests:resolve`); `:310` (ReleaseBundle record); `:376` (code); `:434` (checklist); `:152` (state-owner table).
   - **Issue:** RunManifest and ReleaseManifest are used interchangeably. ReleaseBundle is a third name. A worker is typed as a release.
   - **Why it matters:** the reader learned in Ch 04 that a RunManifest is per-run. This chapter is where the release object is defined, so ambiguity here propagates to Appendix C and every "pinned" claim.
   - **Change:**
     - Add after `:158`, in substance: "Four records keep this precise. A ChangeBundle is a proposed change (Chapter 25's Recommend stage). A ReleaseManifest — the 'release bundle' in this chapter's prose — is the immutable, signed, promoted graph listed in § Versioned objects. An EnvironmentBinding says which ReleaseManifest new starts receive for a tenant, use case, environment, and region. A RunManifest (Chapter 4) is resolved once at admission: it records the ReleaseManifest digest plus the run's subject, purpose, budget, risk tier, and knowledge-snapshot choice. Rollback changes an EnvironmentBinding; it never edits a ReleaseManifest or a RunManifest."
     - Rewrite the end of `:158` as "Northstar records these in an immutable ReleaseManifest; each run's RunManifest references it."
     - Row `:230`: "Resolve every run to an immutable RunManifest that references exactly one signed ReleaseManifest."
     - Rename the ReleaseBundle record (`:310`) to ReleaseManifest. The Release Bundle Builder and the `/v1/release-bundles` API names may stay, with "produces a ReleaseManifest".
     - `:299`: "Return immutable RunManifest referencing the bound ReleaseManifest…".
     - `:434`: "Every run's RunManifest references one immutable ReleaseManifest; no mutable 'latest' reference reaches an active run."
     - In the code, rename the second parameter to a `WorkerProfile` (build, SDK, supported tool/schema versions) when moving it per C27-R13.
   - **Related sections:**
     - Ch 04 reviewer adds a `release_manifest` digest field to the RunManifest JSON (`02-part-ii.md:174–193`).
     - Appendices reviewer aligns Appendix C rows `:65` and `:75`.
     - Map T7 canonical, agreed.

2. **C27-R02 — High — Rewrite.** Location: `08-part-viii.md:182–195` (§ A deployment shape… / § A production topology…), `:199–200`, Q `:455`.
   - **Issue:** "regional execution plane" collides with Ch 04's "Execution plane" (sandbox layer, `02-part-ii.md:140`). The control-plane/cell split is re-taught without acknowledgment.
   - **Why it matters:** "plane" is the book's ownership-domain term (map T2). A second meaning of "execution plane" breaks Ch 04's model at the point the reader most needs it.
   - **Change:** **Reconciled (see overall-book-review.md §D-09):** As stated, but use "global control tier" (Ch 04's term, C04-R12) instead of "Global control plane" at `:182`, `:186`, and `:190`. In Related, Ch 04's Q5 (`:336`) moves here (C27-R14); it does not stay in Ch 04.
     - Add a lead sentence under `:182`: "Chapter 4 separated a global control plane from regional execution cells; this section adds what each side must not assume while releases change and regions fail."
     - Replace "regional execution plane(s)" with "regional execution cell(s)" at `:186`, `:191`, `:200`, and `:455`, and "Control plane" with "Global control plane" at `:186` and `:190`.
     - Keep the "What it must not assume" column and `:195` unchanged.
   - **Related sections:** C28-R09 (Ch 28 `:542` "stateless control plane"); Ch 04 Q `:336` stays.

3. **C27-R03 — High — Condense/Move.** Location: `08-part-viii.md:197–221` (§ Deployment guidance; § Suggested baseline stack—not a mandate).
   - **Issue:** generic platform deployment guidance and a technology stack, both owned elsewhere.
   - **Why it matters:** they bury the release model and duplicate Ch 21/23/28 and Appendix D.
   - **Change:**
     - Keep the bullets Control plane (`:199`), Regional execution cells (`:200`), Release (`:205`), and Disaster recovery (`:206`). Fold into DR the HA clause "'multi-region' without replay tests is not a resilience claim", and drop DR's last sentence (it moves into C27-R07's sequence).
     - Delete Isolation (`:202`; see Ch 21 `06-part-vi.md:432`, `:506`), Worker classes (`:203`; see Ch 23 sandbox and Ch 28 § Scale by workload and failure boundary), and Secrets (`:204`; see Ch 21 credential lease). Replace them with one sentence: "Isolation, worker classes, and secrets follow Chapters 21, 23, and 28."
     - Move § Suggested baseline stack (`:208–221`) to Appendix D as a sub-table. Leave the pointer "Appendix D lists typical technology choices and selection criteria."
   - **Related sections:** Appendices reviewer merges the stack table with Appendix D's two tables (map §7.2).

4. **C27-R04 — High — Rewrite/Remove.** Location: `08-part-viii.md:251–264` (§ Promotion and continuous-improvement loop); Q4 `:456`.
   - **Issue:** the Learn row and `:264` re-teach Ch 25. The Build–Promote stages are not mapped to Ch 25's loop. "Risk-tiered" has no pointer.
   - **Why it matters:** the reader sees a third promotion stage list (after Ch 07 and Ch 25) with no relation stated.
   - **Change:**
     - Retitle the section "### Promotion as a chain of evidence".
     - After `:253`, add: "These stages expand Chapter 25's Validate, Approve, Deploy, and Monitor stages for a single candidate; the gate depth at each stage follows the use-case tier and change class (Chapter 26)."
     - Delete the Learn row (`:262`) and paragraph `:264`. Replace them with: "What production evidence does next belongs to Chapter 25's learning loop; it re-enters here only as a new candidate."
     - Replace Q4 (`:456`) with: "Before deprecating a tool or model version, how do you know what still depends on it? — Query the dependency-edge index from a consistent snapshot for active runs, pinned releases, replays, audits, and legal holds; set warning and end-of-use dates; never archive a digest still referenced, and keep its tombstone." This draws on `:301` and `:333`–`:336`.
   - **Related sections:** Ch 25 `07-part-vii.md:387–404`, `:436`; C26-R02.

5. **C27-R05 — High — Move/Remove.** Location: `08-part-viii.md:266–274` (§ Governance controls); `:288` (Governance Inventory row); `:302–303` (governance APIs); `:316–317` (GovernanceRecord, ExceptionWaiver).
   - **Issue:** Ch 26's implementation is in Ch 27.
   - **Why it matters:** this is the mirror of C26-R03. It removes governance from the release chapter so each chapter has one job.
   - **Change:**
     - Move bullets 1, 2, 3, 4, and 6 and the four listed table rows to Ch 26 exactly as C26-R03 specifies.
     - Delete bullet 5 (`:272`; covered by Ch 24 `07-part-vii.md:62` and Ch 25 Content Vault `:349`) and bullet 7 (`:274`; Ch 25 `:389`, `:436`).
     - Leave in Ch 27 one sentence at the end of § Promotion as a chain of evidence: "A release cannot promote without the governance evidence Chapter 26 requires for its tier."
   - **Related sections:** C26-R03.

6. **C27-R06 — Medium — Rewrite.** Location: `08-part-viii.md:128` (evidence context); `:348` (sources sentence).
   - **Issue:** the chapter cites NIST SP 800-61 [R42] for an incident lifecycle it does not teach. R42's recorded scope ("incident-response integration with organizational risk management", `09-appendices.md:507`) does not support regional recovery mechanics.
   - **Why it matters:** this violates the citation-safety rule (`AGENTS.md`: "A source may support only its recorded scope") and promises content the reader will not find.
   - **Change:**
     - Replace `:128` with: "Evidence context: SBOMs describe components and SLSA provenance describes how an artifact was built; the release controls here use both [R17][R18]. Regional recovery mechanics are book-authored recommendations."
     - Change `:348` to "draws on R17; R18".
     - In the new § Regional recovery (C27-R07), add without citation: "Regional recovery is the Recover stage of Chapter 20's incident lifecycle."
     - R42 remains cited in Ch 20/23 (`06-part-vi.md:1189`), so the registry stays consistent. Run the citation validator after the change.
   - **Related sections:** Ch 20 `06-part-vi.md:272`.

7. **C27-R07 — Medium — Move/Rewrite.** Location: `08-part-viii.md:166` (in ### Rollback and active runs); Q5 `:457`; `:206`; Figure 27-1 (`release-recovery.gv` edge `recovery -> worker` label "resume by risk tier").
   - **Issue:** regional recovery is filed under rollback, precedes the topology it needs, appears three times with drift (Q5 adds "Stop admission"), and "resume by risk tier" names no scale.
   - **Why it matters:** this is the book's only regional failover sequence. Ch 04, 15, and 22 defer to it.
   - **Change:**
     - Delete `:166`.
     - Add `### Regional recovery` as the last H3 of § A deployment shape that supports safe change, with a numbered list:
       1. stop new admission in the affected cell;
       2. fence the old writer;
       3. restore durable state with a compatible build (Chapter 15);
       4. reconcile executing and unknown effects against source systems (Chapter 22);
       5. verify pending signals, timers, and task ownership (Chapters 15 and 18);
       6. advance placement atomically;
       7. resume read-only work first, then mutating work in ascending effect risk class (R0–R4, Chapter 22), with R3/R4 effects only after reconciliation evidence is recorded.
     - End with: "Recovery is rehearsed with evidence, not inferred from replica health."
     - Mark step 7's ordering as a book-authored recommendation.
     - Q5 answer: "Follow the seven-step sequence in § Regional recovery — admission stops first, and mutations resume last."
     - Figure label: "resume by effect risk class".
   - **Related sections:** C26-R01 (scale names); Ch 15 `04-part-iv.md:1259` (Ch 15 reviewer may point here).

8. **C27-R08 — Medium — Condense.** Location: `08-part-viii.md:320–326` (### Compatibility and long-running execution); `:331` (### Scalability and control-plane resilience).
   - **Issue:** bullets 1–2 repeat Ch 15 and `:164`. `:331` repeats `:195`.
   - **Why it matters:** the reader cannot see what the release level adds beyond workflow-level compatibility.
   - **Change:**
     - Replace bullets 1–2 with one sentence: "Chapter 15 keeps compatible workers and explicit migrations for in-flight histories, and its Version Router enforces this chapter's compatibility rules at dispatch; at the release level three further rules apply:". Keep bullets 3–5 verbatim.
     - Move this H3 to sit under § Roll back assignment, not history (see Structural Recommendations).
     - `:331`: keep only the first sentence ("Workers verify bundle signatures/digests locally and keep a last-known-good cache"), since § A production topology states the fail-closed rule.
   - **Related sections:** Ch 15 `04-part-iv.md:1204`, `:1248`.

9. **C27-R09 — Medium — Restructure/Remove.** Locations:
   - `:146–152` (§ Keep releases immutable and workers compatible);
   - `:223–233` (§ Version every artifact that can change behavior, Required-analysis table);
   - `:235–249` (### Versioned objects);
   - `:338–340` (PRODUCTION CONSIDERATION box);
   - `:158` (content list).

   - **Issue:** the release-content list is stated six times. The canonical table arrives late. Two headings have no prose. The Required-analysis table is boilerplate whose one unique row contradicts `:158`.
   - **Why it matters:** the "what is a release" model should be taught once, where it is introduced.
   - **Change:**
     - Merge the figure and state-owner table from `:146–152` under § Treat the full behavior as the release, and delete that heading.
     - Move § Versioned objects to directly after the C27-R01 chain paragraph.
     - Shorten `:158`'s first sentence to: "A production release pins every object in the table below, plus dashboards, runbooks, rollout, and rollback plans."
     - Delete the Required-analysis table (`:225–233`). Keep two sentences after § Versioned objects: "The alternatives — mutable 'latest' configuration, environment snapshots, semantic versions alone — fail when an alias drifts or a long-running workflow spans deployments. Content-addressed, signed bundles cost storage and release discipline, and buy rollback, replay, and investigation."
     - Delete the PRODUCTION CONSIDERATION box.
     - Delete the now-empty § Version every artifact… heading.
   - **Related sections:** map S16.

10. **C27-R10 — Medium — Rewrite.** Locations: `:152` (state-owner table), `:170`, `:289`, `:297`, `:312`, `:318`.
    - **Issue:** contract and record names drift from the chapter body and from Ch 25.
    - **Why it matters:** this is the T23 collision. The reader sees EvaluationEvidence, ReleaseGateDecision, and ValidationReport for one gate output.
    - **Change:** **Reconciled (see overall-book-review.md §D-05):** As stated, except `:318`: DriftFinding → "feeds Chapter 25's Detect stage (alert or containment action)". Ch 25 drops DetectionEvent (C25-R08).
      - State-owner Core contracts → "ReleaseManifest · CompatibilityRule · EnvironmentBinding · PromotionDecision".
      - `:170` "compatibility matrix" → "compatibility rules".
      - `:289` Emergency Control → append "(scoped kill switch, Chapter 23)".
      - `:297` `:evaluate` → "Invoke Chapter 25's release-gate evaluation (`POST /v1/release-gates:evaluate`) for the bundle's required suites and the target tier".
      - `:312` EvaluationEvidence → delete, and add in the PromotionDecision row "gate digest = Chapter 25 ReleaseGateDecision".
      - `:318` DriftFinding → append "emitted as a Chapter 25 DetectionEvent".
    - **Related sections:** C26-R10; Ch 25 reviewer settles the gate-record name.

11. **C27-R11 — Low — Add.** Location: `08-part-viii.md:140–144` (§ Why a release is more than a deployment).
    - **Issue:** there is no callback to Ch 01's Friday failure and no bridge from Ch 26.
    - **Why it matters:** the book promised in Ch 01 that release control is one of five non-intelligence failures. This is where that promise is paid.
    - **Change:** add one sentence at the end: "Chapter 1's Friday failure — a cheaper model swapped in with no code change — is this problem in its smallest form; Chapter 26 decided who may approve such a change, and this chapter makes the approved change safe to apply."
    - **Related sections:** C28-R11 (Closing Perspective replay).

12. **C27-R12 — Low — Rewrite.** Location: `08-part-viii.md:233`, Enterprise example row.
    - **Issue:** an unnamed "regulated underwriting run" is effectively Harborlight.
    - **Change:** moot if C27-R09 deletes the table. If the table is kept, rename it to "Harborlight's mortgage-evidence run".
    - **Related sections:** map S16.

13. **C27-R13 — Low — Move/Rewrite.** Location: `08-part-viii.md:350–424` (§ A sensible place to start; ### Release compatibility check; ### Release attestation verification).
    - **Issue:**
      - Inline code violates `AGENTS.md` ("never write code directly into `source/parts/`").
      - `compatible()` types the worker as a ReleaseManifest.
      - The attestation excerpt checks identity strings, but `:346` says "verify signatures".
    - **Why it matters:** the listings should model the chapter's contracts exactly.
    - **Change:**
      - Move both listings to `examples/` with behavioural tests, register them in `config/examples.json`, and replace them with `[[EXAMPLE:release-compatibility]]` and `[[EXAMPLE:release-attestation]]`.
      - Retype the second `compatible()` argument as `WorkerProfile`.
      - Add a one-line caption to the attestation example: "Signature verification itself is delegated to the signing toolchain; this check binds the verified identities to the allowlists."
      - Add a lead sentence under the empty H2 (`:350`).
    - **Related sections:** C28-R12 (same treatment).

14. **C27-R14 — Low — Rewrite.** Location: `08-part-viii.md:455` (Q3).
    - **Issue:** it uses "regional execution planes".
    - **Change:** **Reconciled (see overall-book-review.md §D-24):** Replace Q3, which duplicates Ch 04's Q2, with Ch 04's Q5 as moved by C04-R12: "How should execution behave during a global-control-tier outage? — Continue compatible in-flight work on pinned last-known-good bundles, apply local denies and kill switches (Chapter 23), and restrict high-risk admission when freshness cannot be established." Original text, superseded: apply C27-R02's rename. The answer otherwise stays.
    - **Related sections:** C27-R02.

15. **C27-R15 — Medium — Rewrite / Add.** *Added in reconciliation (see overall-book-review.md §D-27).*
   - **Location:** § Versioned objects (`08-part-viii.md:240`, "Prompt/skill bundle" row) and the C27-R01 chain paragraph.
   - **Issue:** The Ch 08 and Ch 09 reviews ask Ch 27 to split the row and add a Skill Pack row; no Ch 27 item did.
   - **Change:** Replace the row with three: "Prompt bundle | immutable digest; declared compatible schemas and models | regression and adversarial evals"; "Skill | SkillManifest digest (Chapter 8) | Chapter 8 certification"; "Skill Pack | SemVer plus signed digest; pins exact Skill digests | CompatibilityReport and pack-level evaluation (Chapter 9)". Add to the chain paragraph: "The ReleaseManifest fixes the eligible Skill and pack versions; each RunManifest records the digests resolved from that set (Chapter 8)."
   - **Related:** C08-R03, C09-R02, C04-R20, C27-R01.

16. **C27-R16 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** End of § If this fails in production.
   - **Issue:** Same request as C05-R16.
   - **Change:** Add one line: "If a model or prompt swap shipped as configuration, or a release was changed in place, see AP-15 and AP-16 in Chapter 17."
   - **Related:** C17-R03.
