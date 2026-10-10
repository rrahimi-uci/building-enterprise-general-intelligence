# Chapter 09 — Turn Skills into a Coherent Domain Platform: Continuity and Flow Review

Reviewed: `source/parts/03-part-iii.md:356–502`, with the close of Ch 08 (`:352–354`), the opening of Ch 10 and the Part IV orientation (`04-part-iv.md:1–30`), and `examples/platform/skills_registry.py` (the source of the inline excerpt).

## Overall Assessment

Ch 09 rests on two things:
- **One strong idea:** § Installing a pack grants nothing (`:390–413`). It confronts the package-manager intuition directly, gives a "does / does not" table, and closes with the business-unit example. It is the best-argued passage in Part III.
- **One good motivating scenario:** the evidence-schema gap between document validation and income verification (`:377`).

The rest is thin. At ~1,130 words it is the shortest chapter in the book; the next shortest is Ch 10 at ~1,380, and the catalog chapters Ch 16 and Ch 17 are ~1,430 and ~5,950. [verified: corrected — it is the shortest outright, not "apart from the catalog chapters"]

1. **The chapter's thesis, compatibility, is asserted but never explained.** CompatibilityReport is a core contract (`:382`) that the body never describes. The fullest account of what compatibility covers is the design-review answer (`:495`), not the prose.
2. **§ Pack governance and sharing is two sentences** (`:415–417`). It does not cover:
   - how pack and Skill lifecycles interact (the example code enforces "an active pack references only active Skills", but the prose never says so);
   - how to deprecate one Skill inside a pack, even though exercise 2 (`:488`) asks the reader to design exactly that;
   - who owns a pack when its Skills have different owners. Ch 08's closing promise "without dissolving ownership" (`:354`) is never kept;
   - how the pack version relates to the ReleaseManifest's `skill_pack_versions` (`08-part-viii.md:366`) and to each run's RunManifest.
3. **Vocabulary drifts on promotion.** The prose gives the aliases as "development, staging, and production" (`:417`). Q4 gives "dev, staging, shadow, canary, production, and rollback aliases" (`:497`). Ch 08 has lifecycle states and Ch 27 has promotion stages. Nothing separates a *lifecycle state* (trust status of a version) from an *alias* (which version an environment resolves).
4. **The mortgage Skill list appears three times** (`:360`, `:386`, `:421`). The case box names five Skills (evidence retrieval, document validation, income and property checks, policy explanation, underwriter-package preparation); `:386` and `:421` repeat them and add a sixth, document request. The three off-thread domain examples (`:422–424`) add little. [verified: corrected — the case box lists five, not six]
5. **The inline code excerpt is broken and violates policy.** It calls `_semver_key`, which is not defined in the excerpt, and imports names it never uses. It also repeats the four-state `status` problem (`:437–465`). `AGENTS.md` forbids code in `source/parts/`.
6. **The closing gives no bridge into Part IV.** Ch 10 never mentions the platform (`04-part-iv.md:9–30`).

**Merge into Ch 08?** I considered and rejected it. Packs answer a distinct question: co-release and tenant distribution. Merging would also change the 28-chapter topology, a versioned invariant in `AGENTS.md`. The better move is to rebalance: cut about 150 words of repetition and add about 300 words of compatibility and governance mechanism.

## Intended Reader Mental Model

**What the reader brings (Ch 08):**
- the Skill manifest, digest, and lifecycle;
- discovery versus resolution;
- runs pinning a digest.

**What the reader should leave with:**
- **What:** a Skill Pack is a release unit, not a permission unit. It pins Skill versions known to work together, plus shared policy, knowledge strategy, workflow templates, and pack-level evaluations.
- **Why:** independent Skill releases can leave a run caught between incompatible schemas.
- **How:**
  - A CompatibilityReport is produced at pack build and blocks certification on any mismatch.
  - The pack is promoted and rolled back by moving aliases, backed by evidence.
  - The ReleaseManifest pins the pack version, and each run resolves Skills only from that pack.
  - Installing makes Skills resolvable, never permitted.
- **When:** use a pack once several Skills must agree on schemas and policy for one domain workflow.
- **Trade-offs:** coordinated releases are slower than independent ones, but they are safe.
- **Relationships:**
  - Ch 08 lifecycle and resolution;
  - Ch 27 ReleaseManifest and rollback;
  - Ch 21 tenant grants;
  - Ch 23 and Ch 27 supply chain;
  - Ch 12 compile-time failure when a pack Skill won't resolve.
- **Ownership:** each Skill keeps its owner. The pack owner owns compatibility, shared policy, pack evaluation, and the support window.

Today the reader gets What, Why, and the install invariant. How, Ownership, and Relationships are mostly missing.

## Section-by-Section Flow Review

**Opening boxes (`:358–364`).**
- The case box and the design choice are good.
- The case box is a MORTGAGE CASE box, while Ch 08 used a NORTHSTAR box (concept map T1). Follow the synthesizer's decision.
- The case box's Skill list (five Skills; `:386` and `:421` add document request) is the first of three.

**`## Why domain capabilities need to ship together` (`:366`).**
- *Role:* the "why".
- *Adds:* Skills must agree about schemas, policy, terminology, evaluation, and operations.
- *Verdict:* fine, but its final payoff sentence ("roll out a compatible capability bundle…") is restated in substance, not verbatim, at `:377` ("one unit to promote or roll back"). [verified: softened — same point, different wording]
- *Issue:* this is a double-why opening with the next section.

**`## Compatibility, not convenience` (`:375`).**
- *Role:* a second "why" with the concrete schema-gap scenario, then the state-owner table (`:380–382`).
- *Adds:* the best concrete paragraph.
- *Verdict:* keep the scenario and merge the heading with `:366` (C09-R08).
- *Issue:* the scenario shows *that* compatibility can break, never *how* the pack checks it. CompatibilityReport is introduced here in the table and never mentioned again.

**`## From one capability to a coherent domain experience` (`:384`).**
- *Role:* defines what a pack pins and what the pack manifest declares.
- *Adds:* the manifest field list (`:388`).
- *Issues:*
  - The list of six Skills repeats the case box's five and adds document request.
  - "A pack can expose a smaller capability surface to each agent" (`:388`) is an important least-agency claim with no mechanism (C09-R06).
  - "risk ceiling" agrees with C08-R06. Keep it.

**`### Installing a pack grants nothing` (`:390`).**
- *Role:* the core invariant.
- *Verdict:* strong. It is reinforcement (R) of Ch 08's discovery invariant, applied to distribution.
- *Issue:* the business-unit example (`:409–413`) stops at "will not resolve". The reader is not told *when* that failure surfaces. It should surface before the run starts, at plan compile or admission, not mid-run (C09-R07).

**`### Pack governance and sharing` (`:415`).**
- *Role:* lifecycle and rollout.
- *Verdict:* badly under-developed for its importance. See items 2 and 3 of the Overall Assessment (C09-R02).
- *Issue:* "sharing" in the title is actually covered by `:409–413`. This section never mentions sharing.

**`### Domain pack examples` (`:419`).**
- *Role:* breadth.
- *Verdict:* low value.
- *Issues:*
  - Bullet 1 is the third mortgage list.
  - Bullets 2–4 introduce three new domains with no follow-through.
  - The comparative supplier-onboarding thread the book promises (concept map S13) is absent here, though this is the natural place for it (C09-R04).

**`## What the evidence lets us conclude` (`:426`).**
- *Role:* the supply-chain claim.
- *Verdict:* the content is right, but it carries reasoning that should be in prose. *Why* a pack is executable supply chain is never argued (Skill instructions direct behavior at trust tier 2, Ch 06).
- *Issue:* no pointer to Ch 27 § Release attestation verification (`08-part-viii.md:385`) or Ch 23 containment layer 7 (`06-part-vi.md:1067`).

**`## A sensible place to start` / `### Skill Pack contract` (`:434–465`).**
- *Role:* code.
- *Verdict:* replace it (C09-R05).
- *Issues:*
  - The H2 is an empty wrapper.
  - The excerpt is a partial copy of `examples/platform/skills_registry.py`: it uses `_semver_key` without defining it, and its imports (`hashlib`, `json`, `re`, `Field`, `model_validator`, `SkillRequirement`) are unused in the excerpt.
  - It shows only the manifest class. The parts of the example that enforce pack-to-Skill lifecycle consistency, `register_pack` (unknown Skills refused; an active pack may reference only active Skills) and `resolve_pack` (deprecated content only in replay mode), are left out. Note that neither checks schema compatibility; the example has no CompatibilityReport. [verified: softened — the omitted code teaches lifecycle consistency, not compatibility]

**Template sections: `## If this fails in production` (`:467`), `## What to verify before production` (`:473`), `## Put the idea to work` (`:485`), `## Questions to bring to design review` (`:490`).**
- *If this fails:* all three steps are good and pack-specific. Step 2 ("Compare pack alias history with active run manifests") assumes the RunManifest records the pack version, which Ch 04's RunManifest does not (C09-R02, plus the Ch 04 owner change in the Ch 08 review).
- *Checklist:* sound.
- *Exercises:* exercise 2 relies on content the chapter does not teach until C09-R02 lands.
- *Questions:*
  - Q2 (`:495`) is richer than the body. Move its substance into the body (C09-R01).
  - Q4 (`:497`) conflicts with `:417` on aliases.
  - Q1, Q3, and Q5 are fine.

**`## Where this leads next` (`:500–502`).**
- *Verdict:* an abrupt Part transition.
- *Issue:* "The platform and capability model are complete" gives the reader no idea how Part IV's loops relate to AgentSpec, Skills, and the Tool Gateway (C09-R09).

## Sparse or Underdeveloped Content

- **Compatibility checking:** what the CompatibilityReport checks, when it runs, and what a failure blocks (C09-R01). About 150 words plus a small table.
- **Pack governance:** lifecycle state versus alias; pack-versus-Skill lifecycle; deprecating one Skill; ownership split; pack → ReleaseManifest → RunManifest; supply-chain reasoning (C09-R02). About 250 words.
- **Per-agent capability surface (`:388`):** one sentence of mechanism (C09-R06).
- **Resolution failure timing (`:409–413`):** one sentence (C09-R07).

The additions above are all mechanism. The cuts are C09-R03, C09-R04, and C09-R08 (about −150 words).

## Missing Conceptual Connections

- **Pack version → ReleaseManifest → RunManifest, missing "the ReleaseManifest pins pack versions; each run resolves Skills only from the pinned pack and records the digests".** Location: § Pack governance and sharing. Links Ch 27 `08-part-viii.md:366` and Ch 04 § RunManifest (C09-R02).
- **Pack compatibility (Skill-to-Skill) ↔ Ch 27 compatibility matrix (run-to-worker), missing the distinction.** These are two different "compatibility" checks. The reader will conflate them unless one sentence separates them (C09-R01).
- **Skill instructions at tier 2 (Ch 06) → "a pack is executable supply chain" (`:430`), missing the reasoning** (C09-R02 (e); also C08-R02).
- **Installing a pack grants nothing → Ch 21 authorization by intersection, missing the pointer.** "The installing tenant's own grants" (`:400`) is Ch 21's model (C09-R07).
- **Pack aliases (`:417`) → Ch 08 lifecycle and Ch 27 § Promotion and continuous-improvement loop (`08-part-viii.md:251`), missing the alias-versus-state distinction and the stage vocabulary** (C09-R02).
- **Pack Skill that won't resolve → Ch 12 § Compile-time checks (`04-part-iv.md:514`), missing "fail before the run starts"** (C09-R07).
- **Ch 09 → Part IV, missing "patterns run inside one bounded step on this platform"** (C09-R09).

## Transition Problems

- **Ch 08 → Ch 09 (`:354` → `:360`).** Ch 08 promises composition "without dissolving ownership or compatibility boundaries". Ch 09 covers compatibility only by assertion and ownership not at all (C09-R01, C09-R02).
- **Within the chapter:**
  - § Why domain capabilities… → § Compatibility, not convenience gives the same payoff twice (C09-R08).
  - § Installing a pack grants nothing → § Pack governance and sharing jumps from runtime authority to release aliases with no bridge. C09-R02's opening sentence (lifecycle state versus alias) provides one.
- **Ch 09 → Ch 10 (`:502` → `04-part-iv.md:3–7`, `:9–30`).** Neither the Part IV orientation nor Ch 10 refers back. Readers lose the thread of how patterns run *on* the paved road. The concept map's Ch 09 entry makes the same point, and it holds: no chapter after Ch 09 cites Ch 07, 08, or 09 by number. The only inbound pointers to Part III from outside it are all earlier: Ch 03's "Chapters 4–7" (`01-part-i.md:904`), Ch 05 → Chapter 8 (`02-part-ii.md:430`), and Ch 06's closing → Chapter 7 (`02-part-ii.md:947`). [verified: corrected — Ch 05 is not the only inbound pointer; none comes from Parts IV–VIII or the appendices]

## Redundant and Repetitive Concepts

| Concept | Occurrences | Verdict |
| --- | --- | --- |
| Mortgage pack's Skills (five in the case box, six at `:386` and `:421`) | `:360` (case box), `:386`, `:421` | D. Keep the case box only (C09-R03). |
| "Promote or roll back as one unit" | `:370–373`, `:377` | D. Merge the openings (C09-R08). |
| Installation does not grant authority | `:392–394`, table `:402–407`, checklist `:479`, Q3 `:496` | R (the invariant). Keep. |
| Promotion stages and aliases | `:417`, `:481`, Q4 `:497` | Conflicting. Unify (C09-R02). |

## Cross-Chapter Duplication

| Ch 09 location | Other chapter | Verdict |
| --- | --- | --- |
| § Installing a pack grants nothing (`:390`) | Ch 08 § Discovery is not permission; Ch 19 "A registry entry does not grant trust" / `agents:resolve` "discovery never returns a grant" (`05-part-v.md:507`); Ch 02 principle 5 | R. This is the distribution-time instance and Ch 09 is canonical for it (concept map §3). |
| Supply-chain evidence row (`:430`) | Ch 27 § Release attestation verification (`08-part-viii.md:385`) and the supply-chain evidence row (`:346`); Ch 23 containment layer 7 (`06-part-vi.md:1067`); T-16 | R once Ch 09 points to Ch 27 as canonical (concept map §3: supply chain → Ch 27). |
| Pack promotion and aliases (`:417`, Q4 `:497`) | Ch 27 § Promotion and continuous-improvement loop (`08-part-viii.md:251`: Build, Evaluate, Shadow, Canary, Promote, Learn); Ch 07 golden path | D with drift. Use Ch 27's stage names (C09-R02). |
| `SkillPackManifest` inline code (`:441–465`) | `examples/platform/skills_registry.py` (Ch 08's example); Ch 27 `ReleaseManifest.skill_pack_versions` (`08-part-viii.md:366`) | D. Replace it with an example region (C09-R05). |
| Pack-level "risk ceiling" (`:388`) | Ch 08 C08-R06 `risk_ceiling` | R, consistent if C08-R06 lands. |
| Ch 27 § Versioned objects has no Skill Pack row (`08-part-viii.md:235–247`) | — | **Owner: Ch 27.** Add a "Skill Pack" row: version rule "SemVer + signed digest; pins exact Skill digests"; promotion gate "CompatibilityReport + pack-level evaluation (Chapter 9)". This complements the Ch 08 review's split of "Prompt/skill bundle". |
| Appendix H Skill Pack entry (`09-appendices.md:217`) "Certified domain distribution…" | — | R, consistent. No change. |

## Structural Recommendations

Keep the chapter. The resulting order:

1. Opening boxes.
2. One merged H2: § Why domain capabilities need to ship together, absorbing § Compatibility, not convenience and its scenario.
3. A new short H2, § What compatibility means, holding the CompatibilityReport table (C09-R01).
4. § From one capability to a coherent domain experience, minus the repeated list, plus the per-agent surface mechanism.
5. § Installing a pack grants nothing, plus the failure-timing sentence.
6. § Pack governance and sharing, expanded (C09-R02).
7. § Domain pack examples, reduced or replaced (C09-R04).
8. Evidence.
9. A sensible place to start, now an example marker with two sentences.
10. Template sections.
11. A rewritten closing.

The net change is about +300 / −150 words.

## Concrete Recommended Changes

1. **C09-R01**
   - **Priority:** High. **Action:** Add / Move.
   - **Location:** a new `## What compatibility means`, placed after the merged opening (current `:375–382`). The source is Q2's strong answer (`:495`).
   - **Issue:** Compatibility is the chapter's thesis, but CompatibilityReport is never described, and the best account sits in a design-review answer.
   - **Why it matters to the reader's mental model:** The reader learns *that* packs prevent schema gaps, not *how*.
   - **Change:**
     - Add one lead sentence: "A pack build produces a CompatibilityReport; any failed check blocks the pack from certification."
     - Add a table, "Check | Fails when":
       - Skill-to-Skill schemas: a producer's output schema does not satisfy the consumer's input schema, as in the evidence-schema scenario above.
       - Tool schemas: two Skills require incompatible versions of one tool.
       - Policy obligations: Skills declare conflicting data-class or region constraints.
       - Workflow contracts: a workflow template expects a Skill output the pack does not provide.
       - Knowledge versions: Skills pin different snapshots of the same source.
       - Runtime and model requirements: Skills need different adapter or model capabilities.
       - Deprecation windows: a pinned Skill's compatibility window ends before the pack's support window.
     - Add one sentence: "This is Skill-to-Skill compatibility inside a release; Chapter 27's compatibility matrix is a different check, between a run's pinned release and the workers that may execute it."
     - Keep Q2 as reinforcement.
   - **Related sections:** Ch 27 § Release compatibility check (`08-part-viii.md:353`).

2. **C09-R02**
   - **Priority:** High. **Action:** Add / Rewrite.
   - **Location:** `### Pack governance and sharing` (`:415–417`); Q4 (`:497`).
   - **Issue:** The section is two sentences. It has no lifecycle interaction, no single-Skill deprecation, no ownership split, no release linkage, and no supply-chain reasoning, and its alias vocabulary conflicts with Q4.
   - **Why it matters to the reader's mental model:** It delivers Ch 08's "without dissolving ownership" promise and connects packs to Ch 27, where packs reappear as `skill_pack_versions`.
   - **Change:** Replace the section with about 250 words in five short paragraphs:
     - (a) "A lifecycle state (Chapter 8) is a version's trust status; an alias is a pointer that says which pack version an environment or tenant cohort resolves. Moving an alias is a promotion and needs the same evidence; rollback moves it back." Use Ch 27's stages (shadow, canary, tenant cohort, production) for alias progression.
     - (b) "An active pack may reference only active Skills, which the example enforces. To deprecate one Skill, release a new pack version that drops or replaces it; runs pinned to the old pack finish on it (Chapter 27 § Rollback and active runs)."
     - (c) "Each Skill keeps its owner. The pack owner owns the CompatibilityReport, shared policy, pack-level evaluation, and the support window."
     - (d) "The ReleaseManifest pins pack versions (Chapter 27). Each run resolves Skills only from the pinned pack and records pack version and Skill digests in its RunManifest."
     - (e) Move the substance of the evidence row into prose: "A pack is executable supply chain because Skill instructions direct behavior (trust tier 2, Chapter 6): sign it, attach SBOM and provenance, and verify them at promotion (Chapter 27 § Release attestation verification; Chapter 23 containment layer 7)."

     Then:
     - Rename the H3 to `### Pack lifecycle, ownership, and release`. Sharing is covered in the previous H3.
     - Change Q4's answer to "As signed immutable releases promoted through shadow, canary, tenant-cohort, and production aliases backed by evaluation evidence; rollback reassigns the alias to the prior version." Delete "rollback aliases".
     - Keep the evidence table row as is.
   - **Related sections:** Ch 08 C08-R03, C08-R05, C08-R08. Ch 27 (owner: add the Skill Pack row to § Versioned objects). Ch 04 (owner: add `skill_pack` and `skills` to the RunManifest JSON).

3. **C09-R03**
   - **Priority:** Medium. **Action:** Remove.
   - **Location:** `:386`, § From one capability to a coherent domain experience; `:421`, § Domain pack examples, bullet 1.
   - **Issue:** The six-Skill list is repeated three times.
   - **Why it matters to the reader's mental model:** Repetition dilutes the one new thing `:386–388` says, namely what else a pack pins.
   - **Change:**
     - Add "document request" to the case box's list at `:360` so it names all six Skills, then change `:386` to: "Harborlight's mortgage-evidence pack pins the six Skills named above, together with shared policy, taxonomy, knowledge strategy, workflow templates, evaluation datasets, dashboards, and runbooks." [verified: amended — the case box currently names only five Skills, so "the six named above" would be false without this edit]
     - Delete bullet 1 at `:421`.
   - **Related sections:** case box `:360`.

4. **C09-R04**
   - **Priority:** Medium. **Action:** Condense / Rewrite (conditional).
   - **Location:** `### Domain pack examples` (`:419–424`).
   - **Issue:** Three off-thread domains add breadth without teaching anything.
   - **Why it matters to the reader's mental model:** They also compete with the book's promised comparative thread.
   - **Change:** **Reconciled (see overall-book-review.md §D-21):** The supplier-onboarding thread is retired book-wide. Apply the "If the thread is retired" branch only: delete the H3 and append the one sentence to `:388`.
     - **If the synthesizer keeps the supplier-onboarding thread (concept map S13):** replace the bullets with one supplier-onboarding pack (validate supplier, screen sanctions, propose approval, create supplier record, notify) and one sentence on what transfers unchanged (the manifest shape, install ≠ grant, the compatibility checks) and what does not (domain Skills and policy).
     - **If the thread is retired:** delete the H3 and add to the end of `:388`: "The same structure fits any domain where several Skills must agree on schemas and policy."
   - **Related sections:** concept map S13, T17.

5. **C09-R05**
   - **Priority:** High. **Action:** Remove / Add (example region).
   - **Location:** `### Skill Pack contract` (`:437–465`); `examples/platform/skills_registry.py`.
   - **Issue:** The inline code violates `AGENTS.md`. It is a broken excerpt (it uses `_semver_key` undefined and has unused imports), it carries the four-state status, and it omits the logic that enforces the prose's lifecycle rule (`register_pack`, `resolve_pack`). [verified: softened — the example contains no compatibility check to show]
   - **Why it matters to the reader's mental model:** The code should show the invariants the prose states.
   - **Change:**
     - Delete the inline block.
     - In `skills_registry.py`, add a region `packs` covering `SkillPackManifest`, `register_pack`, and `resolve_pack`. Reorder so the region is contiguous, or split into regions as the extractor allows.
     - Insert `[[EXAMPLE:skills-registry#packs]]` and add `packs` to the `regions` map in `config/examples.json`.
     - Before the marker, add two sentences: "`register_pack` refuses unknown Skills and an active pack that references any non-active Skill. `resolve_pack` returns deprecated content only in explicit replay mode, which is Chapter 8's compatibility window in code."
     - The six-state status fix is C08-R05; do it once, in the shared example.
   - **Related sections:** C08-R05, C08-R12.

6. **C09-R06**
   - **Priority:** Medium. **Action:** Add.
   - **Location:** `:388`, the sentence "A pack can expose a smaller capability surface to each agent…".
   - **Issue:** This is a least-agency claim with no mechanism.
   - **Why it matters to the reader's mental model:** Without a mechanism, the reader may assume every agent gets the whole pack.
   - **Change:** Append: "Each AgentSpec names the pack Skills it requires; resolution refuses any other Skill for that agent's steps, so least agency (Chapter 2, principle 2) holds inside a pack."
   - **Related sections:** Ch 08 C08-R03 (binding at build).

7. **C09-R07**
   - **Priority:** Medium. **Action:** Add.
   - **Location:** the end of `### Installing a pack grants nothing` (after `:413`).
   - **Issue:** The text does not say when a non-resolvable pack Skill fails, and it does not point to the grant model.
   - **Why it matters to the reader's mental model:** It keeps "fail closed" from becoming "fail mid-run".
   - **Change:** Add: "The refusal should surface before work starts: at plan compilation (Chapter 12 § Compile-time checks) or admission, naming the rule that denied it, never mid-run. The installing tenant's grants are combined by intersection with the subject's and actor's (Chapter 21)."
   - **Related sections:** Ch 12 (owner: add "(Chapter 8)" at `04-part-iv.md:410`); Ch 21.

8. **C09-R08**
   - **Priority:** Medium. **Action:** Merge.
   - **Location:** `## Why domain capabilities need to ship together` (`:366–373`) and `## Compatibility, not convenience` (`:375–382`).
   - **Issue:** A double-why opening with a repeated payoff.
   - **Why it matters to the reader's mental model:** The concrete scenario is the hook. Right now it comes second.
   - **Change:**
     - Keep the `:366` heading. Its body becomes `:368–371` (the first two sentences, ending "…promoted as one release."), followed by the `:377` paragraph.
     - Delete the third sentence at `:371–373` (from "The payoff is visible…") and the `:375` heading. [verified: corrected — "The payoff" begins on `:371`, not `:370`]
     - Keep the state-owner table after the merged text.
   - **Related sections:** Ch 08 C08-R09 (same pattern).

9. **C09-R09**
   - **Priority:** High. **Action:** Rewrite (Ch 09) / Cross-reference (Part IV owner).
   - **Location:** `## Where this leads next` (`:502`); Part IV orientation (`04-part-iv.md:3–7`).
   - **Issue:** This is an abrupt Part transition, and nothing in Parts IV–VIII refers back to Part III by chapter number.
   - **Why it matters to the reader's mental model:** Readers should carry into Part IV the picture of one bounded step: an AgentSpec running through AgentRuntime, with resolved Skills and governed tools.
   - **Change:** **Reconciled (see overall-book-review.md §D-28):** The Ch 09 closing rewrite stands. The Part IV orientation sentence is subsumed by the merged paragraph in overall-book-review.md §D-28 (C10-R01's first inserted sentence carries it); do not add it separately. Original text:
     - Replace `:502` with: "The platform now supplies the units every later pattern binds to: an agent runs one bounded step through AgentRuntime, with Skills resolved from a pinned pack and tools called through the Tool Gateway. Part IV asks what shape the reasoning inside that step, and the workflow around it, should take, starting with the smallest bounded loop in Chapter 10."
     - **Owner: Part IV/Ch 10 review.** Add one sentence to the Part IV orientation: "Every pattern here runs on the platform of Part III; routing chooses among eligible agents and Skills (Chapter 11), and plan compilation binds steps to Skill releases (Chapter 12)."
   - **Related sections:** Ch 11 `04-part-iv.md:220`; Ch 12 `:410`.

10. **C09-R10**
    - **Priority:** Low. **Action:** Rewrite.
    - **Location:** `## If this fails in production`, step 2 (`:470`).
    - **Issue:** The step assumes the RunManifest records the pack version.
    - **Why it matters to the reader's mental model:** Triage steps must rest on records that actually exist.
    - **Change:** Change it to "Compare pack alias history with the pack version and Skill digests recorded in each affected run's RunManifest." This depends on the Ch 04 RunManifest change listed in the Ch 08 review.
    - **Related sections:** C09-R02 (d).

## Verification log

- **Line refs checked:** 54 in-chapter and cross-chapter references; 2 fixed (C09-R08: `:368–370` → `:368–371` and `:370–373` → `:371–373`). All other cited lines exist as described, including `04-part-iv.md:3–7`, `:9–30` (no "platform" in Ch 10's opening), `:410`, `:514`; `06-part-vi.md:1067`; `08-part-viii.md:162`, `:170` (compatibility matrix), `:235–248`, `:251–262`, `:346`, `:353`, `:366`, `:385`; `09-appendices.md:217`; `01-part-i.md:744` (principle 2, least agency); `06-part-vi.md:407` (intersection of grants, Ch 21).
- **Claims removed:** none.
- **Claims corrected (3):**
  - "the shortest chapter in the book apart from the catalog chapters" → the shortest outright (1,134 words; Ch 10 is next at 1,378; Ch 16 is 1,432, Ch 17 is 5,946).
  - "The six-Skill mortgage list appears three times": the case box (`:360`) lists five Skills; `:386` and `:421` list six (adding document request). C09-R03 amended so the case box names all six before `:386` refers to "the six Skills named above".
  - "The only inbound pointer to Part III anywhere is Ch 05 → Ch 8": grep of all `source/parts/*.md` finds three inbound pointers, all earlier than Part III (`01-part-i.md:904` "Chapters 4–7", `02-part-ii.md:430` "Chapter 8", `02-part-ii.md:947` "Chapter 7") and none from Parts IV–VIII or the appendices. The core claim (no later chapter cites Ch 07/08/09 by number) is confirmed.
- **Claims softened (3):**
  - The `:366` payoff sentence is "restated in substance" at `:377`, not repeated.
  - `register_pack`/`resolve_pack` enforce lifecycle consistency; they do not check compatibility, and the example has no CompatibilityReport (section review and C09-R05 Issue).
- **Confirmed, consequential:**
  - The inline excerpt (`:441–465`) calls `_semver_key`, which is defined at `skills_registry.py:30` but absent from the excerpt; `hashlib`, `json`, `re`, `Field`, `model_validator`, and `SkillRequirement` are imported and unused in the excerpt. Its `status` Literal has four states (`:458`).
  - `CompatibilityReport` occurs once in the book (`:382`). `support window` occurs at `:327` (Ch 08) and `:388` (Ch 09). `skill_pack_versions` occurs once (`08-part-viii.md:366`).
  - § Pack governance and sharing is two sentences (`:417`) with aliases "development, staging, and production"; Q4 (`:497`) lists "dev, staging, shadow, canary, production, and rollback aliases"; Ch 27's stages are Build, Evaluate, Shadow, Canary, Promote, Learn (`08-part-viii.md:255–262`) and its CD stages are shadow, canary, tenant cohort, regional (`:158`).
  - Ch 27 § Versioned objects (`08-part-viii.md:238–248`) has eleven rows and no Skill Pack row; the nearest is "Prompt/skill bundle" (`:240`).
  - `register_pack` enforces "active pack must reference only active skills" (`skills_registry.py:123–127`), which the prose never states; exercise 2 (`:488`) asks for a single-Skill deprecation plan that `:415–417` does not teach.
  - Ch 04's RunManifest records no pack version (`02-part-ii.md:177–195`), so step 2 of § If this fails (`:470`) rests on a field that does not exist (C09-R10).
- **Recommendations amended:** C09-R03 (add document request to the case box), C09-R08 (line ranges), C09-R05 (Issue wording). C09-R04's reconciled branch (D-21, retire the thread) and C09-R09's reconciled handling (D-28) are consistent with §12; C09-R02(b)'s "Chapter 27 § Rollback and active runs" is already flagged in §12 for renaming when applied. No recommendation touches the 8/28/12 topology; C09-R05 moves code to `examples/` as required.
- **Could not verify:** the "+300 / −150 words" estimates; whether `resolve_pack`'s replay mode is "Chapter 8's compatibility window in code" (C09-R05's proposed sentence) is an interpretation, since the code's docstring does not say so.
