# Chapter 08 — Package Capabilities as Versioned Skills: Continuity and Flow Review

Reviewed: `source/parts/03-part-iii.md:179–354`, with the close of Ch 07 (`:175–177`), the opening of Ch 09 (`:356–377`), and the backing example `examples/platform/skills_registry.py` (`[[EXAMPLE:skills-registry#resolution]]`).

## Overall Assessment

Ch 08 is the strongest chapter in Part III. Three pieces carry it:
- an abridged YAML manifest with an explanation of what each part does (`:212–246`);
- a precise discovery-versus-resolution table (`:266–272`);
- an evidence-driven lifecycle table (`:283–290`).

"Discovery is not permission" is a real invariant, and this chapter is its correct canonical home (concept map §3).

The chapter underdelivers on the word in its own title, "versioned", and on the relationships a reader needs in order to place a Skill in the architecture they already hold:

1. **No Skill / tool / agent / pack distinction.** The reader knows ToolManifest (Ch 02), AgentSpec (Ch 04/07), and the capability catalog (Ch 05). Nothing says when something should be a Skill rather than a tool or an agent. Ch 05 (`02-part-ii.md:430`) even claims the catalog, Skills, and tool manifests are "the same artifact".
2. **No path from a resolved Skill to the model.** The contract surface's `invoke(step_request) -> AgentStepResult` (`:298`) is the only hint. The reader is never told that the Skill's instructions enter the ContextManifest at trust tier 2 (Ch 06), that `requires.tools` narrows the step's eligible tools (Ch 03's AgentStepRequest), or that every call still passes the Tool Gateway. A reader could take "resolution answers *what this run may use*" (`:264`) to mean authorization.
3. **Binding time is never reconciled.** A Skill is bound four times in the book:
   - attach at build time (Ch 07 `:77`);
   - pinned in the ReleaseManifest (Ch 27 `08-part-viii.md:366`);
   - bound to plan nodes at compile time (Ch 12 `04-part-iv.md:410`);
   - resolved per run (here).

   No passage says how these four relate.
4. **Versioning semantics are missing.** The chapter does not say what a version number promises, or that any change produces a new digest.
5. **Five internal contradictions:**
   - `lifecycle: active` sits inside a manifest that is "immutable" and digested (`:217`, `:238`), and the example code includes `status` in the digest.
   - "Deprecated: still resolvable for runs already using it" (`:289`) contradicts "the digest is what a run actually pins" (`:242`).
   - YAML `min_risk_tier` (`:233`) means the opposite of the code's `maximum_risk` ceiling.
   - The prose has six lifecycle states, while the code's `status` (in this chapter's own example, not only Ch 09) has four.
   - "Discovery is semantic and permissive" (`:257`) contradicts Ch 05's "filter during discovery" (`02-part-ii.md:430`) and AP-12 (`04-part-iv.md:1697`).

The chapter needs about 400 words of added mechanism (C08-R01–R03, R07) and about 120 words of cuts (R09). The topology should stay as it is.

## Intended Reader Mental Model

**What the reader brings:**
- Ch 02 principle 5, "discovery never implies authorization" (`01-part-i.md:747`).
- Ch 03's AgentStepRequest field groups (`01-part-i.md:1039`).
- Ch 05's capability catalog.
- Ch 06's tier-2 "Skill instructions" (`02-part-ii.md:650`).
- Ch 07's paved road.

**What the reader should leave with:**
- **What:** a Skill is the reusable unit between a tool (one typed operation with effect semantics) and an agent (a configured worker). It packages instructions, interface, eligible tools, knowledge, policy, and an evaluation suite under one owner and one digest.
- **Why:** copied prompts diverge, fixes don't propagate, and nobody can prove what ran.
- **How:**
  - Discovery finds candidates.
  - Resolution pins one digest against the run envelope, or fails closed.
  - The digest is recorded in the RunManifest and compiled into the step.
  - The Tool Gateway still authorizes every call.
- **When:** make something a Skill when it needs model judgment over several tools or sources and is reused. Make it a tool when it is one deterministic operation. Make it an agent when it owns a run, acceptance, and topology.
- **Trade-offs:** registry latency and certification cost, set against reproducibility.
- **Lifecycle:** lifecycle state governs what *new* runs may resolve; pinned runs never re-resolve. The version number communicates interface compatibility, and only evidence certifies behavior.
- **Relationships:** ToolManifest (Ch 22), Tool Gateway (Ch 02/22), capability catalog (Ch 05), ReleaseManifest (Ch 27), kill switch (Ch 23), plan compiler (Ch 12).

## Section-by-Section Flow Review

**Opening boxes (`:181–187`).**
- The NORTHSTAR box states the problem crisply and the design choice is good.
- Box type: this is a NORTHSTAR box, while Ch 09 uses a MORTGAGE CASE box. Defer to the synthesizer's T1/S12 decision.

**`## Why a prompt is not a reusable capability` (`:189`).**
- *Role:* the "why".
- *Adds:* owner, interface, release, and evidence as what a Skill gives a capability.
- *Verdict:* good, but it is the first of three successive descriptions of what a Skill contains.

**`## What belongs inside a Skill` (`:197`).**
- *Role:* a second "why" plus a contents list, then the state-owner table (`:202–204`).
- *Adds:* the key fact that a small prompt edit can change tool selection, data exposure, or output shape (`:199`).
- *Verdict:* redundant with `:191–195` and `:208`. Merge it (C08-R09).
- *Issues:* the table's "SkillRequirement · SkillRelease" names are never explained in the prose. SkillRelease is the natural home for lifecycle state (C08-R05).

**`## The Skill manifest` (`:206`).**
- *Role:* the definition (`:208`), the YAML, and the "three things" explanation.
- *Adds:* the digest pin, the exhaustive `requires` block, and evidence-gated promotion. This is the chapter's best teaching passage.
- *Issues:*
  - (a) `side_effect_class: read_only` and `min_risk_tier: 1` are never explained. They collide with Ch 22 R0–R4 and Ch 26 tiers 0–4 (concept map §6 T11), and `min_` inverts the code's `maximum_risk` ceiling.
  - (b) `lifecycle: active` inside a digested, immutable manifest is a logical error. Changing state would change the digest.
  - (c) "a Skill that reaches for a tool not listed there fails" (`:243–245`) does not say who enforces it.
  - (d) `:248` ("Skills separate reuse from copy-and-paste…") is motivation stranded after the explanation.
  - (e) The section has nothing on what the version number means, although the title is "Versioned Skills".
  - (f) The knowledge pin `mortgage-policy@approved-2026.09` drifts from Ch 03's `mortgage-policy@2026.09` (T16).

**`### Discovery is not permission` (`:250`).**
- *Role:* the chapter's central invariant, with Figure 8-1 and a comparison table.
- *Adds:* the asymmetry between "fuzzy is fine because nothing is permitted yet" and "strict because this is what runs".
- *Verdict:* strong, and canonical.
- *Issues:*
  - (a) "Discovery is semantic and permissive" conflicts in wording with Ch 05 `02-part-ii.md:430` ("A capability the caller may not invoke should never appear") and AP-12's shortlist. The reconciliation (discovery output goes to the resolver, never unfiltered to a model) is only implied by `:276–277`.
  - (b) It never says that resolution is not per-call authorization.
  - (c) It never says where the pinned digest goes. That is the bridge to Ch 03/04/06 (C08-R02).
  - (d) It never relates itself to the Tool Registry and Discovery Service of Ch 22 (`06-part-vi.md:732–733`), which repeat the pattern for tools.

**`### Skill lifecycle` (`:279`).**
- *Role:* the state machine.
- *Adds:* evidence-driven transitions and the compatibility window. The three-weeks-in-flight example is good.
- *Issues:*
  - (a) The Deprecated row's "still resolvable for runs already using it" confuses pinning with resolution.
  - (b) Active has no exit trigger ("—").
  - (c) The Revoked row ("not resolvable by anything new") contradicts the prose at `:292` (it "can affect a run already in flight").
  - (d) "an artifact rather than an approval conversation" (`:281`) sits uneasily with Ch 26's tier 3–4 human approvals.
  - (e) The certification list (`:292`) is an 8-item test list with no pointer to Ch 25's levels.
  - (f) Revocation is the Skill-scoped kill switch, but there is no pointer to Ch 23 § Scoped operational kill switch or Ch 27 § Rollback and active runs.

**`### Skill contract surface` (`:294`).**
- *Role:* the API.
- *Verdict:* weak.
- *Issues:*
  - `invoke(step_request) -> AgentStepResult` implies a Skill is called like a sub-agent. This is the only, and misleading, hint about runtime execution.
  - `EvaluationReport` and `ReleaseDecision` drift from EvaluationResult/PromotionDecision (T23).
  - The escaped underscores (`run\_envelope`) render oddly. These should be code spans.
  - The registry-scale paragraph (`:302`) is fine and unique (regional last-known-good replicas).

**`## What the evidence lets us conclude` (`:304`).**
- *Role:* terminology disclaimer.
- *Verdict:* useful.
- *Issues:* It distinguishes A2A AgentSkill and Skills over MCP but not the "Agent Skills" (SKILL.md) packaging that many 2026 readers will associate with the word. Adding that needs a registered primary source (C08-R11). Ch 19 also uses "skills" in the A2A sense with no disambiguation.

**`## A sensible place to start` / `### Skill manifest and resolver` (`:312–317`).**
- *Role:* the example link.
- *Verdict:* this is an empty-wrapper H2 (concept map §5.3) with no prose saying what the example shows.
- *Issues:* The example resolves by policy and then the highest SemVer. Its `resolve(requirement)` takes no run envelope, unlike the contract `resolve(requirement, run_envelope)` at `:297`. It uses a four-state status, and it puts `status` inside the digest.

**Template sections: `## If this fails in production` (`:319`), `## What to verify before production` (`:325`), `## Put the idea to work` (`:337`), `## Questions to bring to design review` (`:342`).**
- *If this fails:* step 1 ("Resolve a Skill version from the recorded requirement") would re-resolve against today's registry and may produce a different answer (C08-R13). Steps 2 and 3 are good. Step 3 depends on enforcing `requires`.
- *Checklist:* sound. "Support window" appears only here; the lifecycle calls it the "compatibility window", so align the terms.
- *Exercises:* good. Exercise 2 ("cross-tenant retrieval defect") matches the YAML gate `cross_tenant_leak: 0`.
- *Questions:*
  - Q1 repeats the definition (acceptable reinforcement).
  - Q3, "What makes a Skill portable?", is never discussed in the body.
  - Q4 lists ten test kinds, against eight in `:292`.
  - Q5, "When should behavior remain application-specific?", is the chapter's only When content and belongs in the body (C08-R01).

**`## Where this leads next` (`:352`).**
- *Verdict:* good, though Ch 09 must deliver "without dissolving ownership" (see C09-R02).

## Sparse or Underdeveloped Content

- **Skill versus tool versus agent versus pack.** The chapter has no comparison, and the only When guidance is in a design-review answer (`:350`) (C08-R01).
- **Runtime materialization.** How a pinned Skill becomes part of an AgentStepRequest and ContextManifest, and how the Tool Gateway enforces `requires` (C08-R02).
- **Binding time.** The chapter never says which of attach, release, plan compile, and run resolution fixes what (C08-R03).
- **Version semantics.** What MAJOR/MINOR/PATCH mean for a Skill, and the rule that any change creates a new digest needing certification (C08-R07).
- **Portability.** It is asked in Q3 and answered only there. Either one sentence in the body or replace the question (C08-R14).

All of these are mechanism, not padding. Together they come to about 400 words.

## Missing Conceptual Connections

- **Resolution → model call, missing "the digest populates AgentStepRequest: instructions at ContextManifest tier 2, `requires.tools` as the step's eligible tool versions, `runtime` as its bounds".** Location: after `:277`. Links Ch 03 (`01-part-i.md:1039–1047`) and Ch 06 (`02-part-ii.md:650`) (C08-R02).
- **Resolution → tool call, missing "resolution does not authorize any call the Skill proposes; each call passes the six gates at the Tool Gateway".** Links Ch 02 § One proposal, six gates and Ch 22 ToolEligibility, "discovery cache only, not final invocation authorization" (`06-part-vi.md:766`) (C08-R02).
- **Pinned digest → reconstruction, missing "the digest is recorded in the RunManifest".** Ch 04's RunManifest (`02-part-ii.md:177–195`) has `prompt_bundle` but no Skill field (owner: Ch 04; see Cross-Chapter Duplication).
- **Ch 05 capability catalog → Ch 08 Skill Registry → Ch 22 Tool Registry, missing "one discovery view over two registries".** Location: § Discovery is not permission (C08-R01, C08-R04).
- **Skill instructions (tier 2) → supply chain, missing "because Skill content directs behavior, it is executable supply chain".** This is the reasoning behind Ch 09's evidence row (`:430`) and Ch 23 layer 7 (`06-part-vi.md:1067`) (C08-R02, last sentence).
- **Revocation → containment, missing pointers to Ch 23 § Scoped operational kill switch and Ch 20 `06-part-vi.md:286` ("Containment can pause … Skill").** Location: `:292` (C08-R08).
- **Lifecycle "Active" → release promotion, missing "lifecycle is a version's trust status; Ch 27 promotion assigns it to environments and cohorts".** The Ch 09 aliases depend on this (C09-R02).
- **Skill resolution ↔ Ch 11 eligible route set.** Both compute an eligible set deterministically before any model choice. Ch 11 should cite Ch 08 when it introduces the eligible set (owner: Ch 11).

## Transition Problems

- **Ch 07 → Ch 08 (`:177` → `:183`).** Works; see C07-R12 for sharpening the Ch 07 side.
- **Within the chapter:**
  - § Why a prompt… → § What belongs inside a Skill → § The Skill manifest (`:189–208`) is three successive starts on the same topic.
  - `:248` interrupts the move from the manifest explanation to § Discovery is not permission. Move it up (C08-R09).
  - § Skill lifecycle → § Skill contract surface has no bridge, which is acceptable for a reference H3.
- **Ch 08 → Ch 09 (`:354` → `:360`).** The promise ("without dissolving ownership or compatibility boundaries") is only half kept. Ch 09 explains compatibility but never pack-versus-Skill ownership (C09-R02).

## Redundant and Repetitive Concepts

| Concept | Occurrences | Verdict |
| --- | --- | --- |
| What a Skill contains | `:191–195`, `:199`, `:208`, Q1 `:346` | Keep `:208` as the definition and Q1 as reinforcement. Merge `:191–199` (C08-R09). |
| Test kinds for certification | `:292` (8), Q4 `:349` (10), checklist `:335` (5) | Align Q4 to `:292` and point to Ch 25. The checklist is fine. |
| "Discovery semantic, resolution deterministic" | `:257–264`, table `:266`, checklist `:331`, Q2 `:347` | R (an invariant worth repeating in the checklist and review). Keep. |
| Deprecation and revocation | table `:289–290` and prose `:292` | Keep the prose. Fix the table so the two agree (C08-R08). |

## Cross-Chapter Duplication

| Ch 08 location | Other chapter | Verdict |
| --- | --- | --- |
| § Discovery is not permission (`:250`) | Ch 02 principle 5 (`01-part-i.md:747`); Ch 05 § Capability and API catalog (`02-part-ii.md:430`); Ch 11 eligible route set; Ch 19 `agents:resolve` "discovery never returns a grant" (`05-part-v.md:507`); AP-12 (`04-part-iv.md:1691`); Ch 20 Q (`06-part-vi.md:325`); Ch 22 Discovery Service and ToolEligibility (`06-part-vi.md:733`, `:766`) | Ch 08 is canonical. Ch 02, 05, 11, 19, 22, and AP-12 are R (new instances), **but Ch 05 and Ch 08 currently conflict in wording** (C08-R04). Ch 20's Q is D (concept map §5.2); the Ch 20 review should point to Ch 08. |
| Skill Registry and resolver (`:204`, `:296–302`) | Ch 22 Tool Registry and Discovery Service (`06-part-vi.md:732–733`) | R, as a parallel pattern. Ch 08 should name the parallel once (C08-R01). Ch 22 should cite Ch 08 for the principle (owner: Ch 22). |
| YAML `side_effect_class`, `min_risk_tier` (`:219`, `:233`) | Ch 22 ToolManifest Risk group and § Risk classes (`06-part-vi.md:709`, `:714`); Ch 26 tiers (`08-part-viii.md:62`) | A collision, not a duplication. Fix it in Ch 08 (C08-R06). |
| § Skill lifecycle deprecation and compatibility window (`:289–292`) | Ch 27 § Rollback and active runs (`08-part-viii.md:162`); Ch 15 Version Router | R. Ch 08 is the Skill-scoped instance and Ch 27 is canonical for rollback of assignment. Add a pointer. |
| Certification list (`:292`), Q4 (`:349`) | Ch 25 § Evaluation pyramid (`07-part-vii.md:295`) and § Layer tests… (`:305`); Ch 25 Skills row (`:420`) | R if pointed to Ch 25. Ch 25's Skills row is good reinforcement. |
| Tier-2 Skill instructions (Ch 06 `02-part-ii.md:650`) | (no reciprocal in Ch 08) | Missing reciprocal. Add it (C08-R02). |
| "Prompt/skill bundle" | Ch 04 layer "prompt/skill catalog" (`02-part-ii.md:134`); Ch 15 Snapshot (`04-part-iv.md:1159`); Ch 27 § Versioned objects (`08-part-viii.md:240`) | These conflate prompt and Skill, contradicting this chapter's thesis. **Owners: Ch 04, Ch 15, Ch 27** should say "prompt bundle and Skill digests". Ch 27 should split the row into "Skill (SkillManifest digest), gate: Chapter 8 certification" and "Skill Pack, gate: pack compatibility and evaluation (Chapter 9)". |
| RunManifest lacks Skills | Ch 04 § RunManifest (`02-part-ii.md:172`); Ch 03 RunManifest table (`01-part-i.md:1225`) | **Owner: Ch 04.** Add `"skills": ["mortgage.evidence.read@0.1.0#sha256:9f3c…"]` (and `"skill_pack"` per C09-R02). Ch 03's AgentStepRequest Capabilities row (`01-part-i.md:1044`) should read "Resolved Skill digests, eligible tool versions, …" (owner: Ch 03). |
| A2A "skills" | Ch 19 `05-part-v.md:471`, `:505`, `:507`, `:521`, `:522`, `:545` | A terminology collision. **Owner: Ch 19.** Qualify the first use as "A2A agent-card skills (advertised metadata, not the Skills of Chapter 8)". |

## Structural Recommendations

Keep the H2/H3 skeleton, with these changes:

1. Merge § What belongs inside a Skill into § Why a prompt is not a reusable capability, and move `:248` to the end of the merged opening.
2. Within § The Skill manifest, after the "three things" explanation, add a short "What a version promises" paragraph (C08-R07).
3. Add a new H3 under § The Skill manifest, before § Discovery is not permission: `### Skill, tool, agent, pack — which is which` (C08-R01).
4. Inside § Discovery is not permission, after `:277`, add two paragraphs: the runtime path and authorization (C08-R02), and binding time (C08-R03).
5. Fix the lifecycle table. Rewrite the contract surface.
6. Give § A sensible place to start two sentences of prose.

The net change is about +400 / −120 words.

## Concrete Recommended Changes

1. **C08-R01**
   - **Priority:** High. **Action:** Add.
   - **Location:** a new `### Skill, tool, agent, pack — which is which` under `## The Skill manifest`, after `:246` (and after the moved `:248`).
   - **Issue:** The chapter has no distinction between the units the reader now holds, and no When guidance in the body.
   - **Why it matters to the reader's mental model:** The reader cannot place a Skill relative to ToolManifest (Ch 02/22), AgentSpec (Ch 04/07), and the capability catalog (Ch 05).
   - **Change:** Add a four-row table with columns Unit | What it is | Contract | Owner | Enforced by:
     - **Tool:** one typed operation with effect semantics | ToolManifest (Chapter 22) | tool owner | Tool Gateway on every call (Chapters 2, 22).
     - **Skill:** instructions, interface, eligible tools, knowledge, policy, and evaluation for one reusable capability, executed inside an agent step | SkillManifest | domain-capability owner | resolver (this chapter), then Tool Gateway.
     - **Agent:** a configured worker that runs bounded steps and requires Skills | AgentSpec, executed as AgentStepRequest (Chapter 3) | application team | AgentRuntime.
     - **Skill Pack:** compatible, co-released Skills plus shared policy and evaluations | SkillPackManifest (Chapter 9) | pack owner | registry and release (Chapter 27).

     Then add two sentences:
     - "One deterministic operation with an effect is a tool; model judgment over several tools or sources, reused across agents, is a Skill; anything that owns a run, its acceptance, and its topology is an agent."
     - "Chapter 5's capability catalog is the discovery view across the tool and Skill registries; the registries stay separate because their contracts and enforcement points differ."

     Keep Q5 (`:350`) as reinforcement.
   - **Related sections:** Ch 05 `02-part-ii.md:430` (its "same artifact" sentence should become "the same catalog view over the Skill and tool registries"; owner: Ch 05). Ch 07 C07-R02.

2. **C08-R02**
   - **Priority:** High. **Action:** Add.
   - **Location:** the end of `### Discovery is not permission`, after `:277`. Also the gloss sentence at `:243–245`.
   - **Issue:** Nothing says how a resolved Skill reaches the model or who enforces `requires`, and resolution can be misread as authorization.
   - **Why it matters to the reader's mental model:** This bridges Part III back to Ch 03/06 and forward to Ch 22. Without it the Skill floats outside the six-gate model.
   - **Change:** Add about 120 words:
     - "The pinned release is compiled into the step. Its instructions enter the ContextManifest at trust tier 2 (Chapter 6 § The trust hierarchy of instructions); its `requires.tools` becomes the step's eligible tool versions and its `runtime` block the step's bounds in the AgentStepRequest (Chapter 3 § The request is bounded before the model sees it); its digest is recorded in the RunManifest (Chapter 4 § RunManifest)."
     - "Resolution decides which Skill may run. It authorizes none of the calls that Skill proposes: each still passes the six gates at the Tool Gateway (Chapter 2) against the subject, purpose, and exact resource (Chapter 22)."
     - "Because Skill instructions direct behavior, Skill content is executable supply chain, which is why Chapter 9 signs and attests packs."

     At `:243–245`, change "a Skill that reaches for a tool not listed there fails" to "a tool not listed there is outside the step's eligible set, so the Tool Gateway refuses the call".
   - **Related sections:** Ch 03, Ch 06, Ch 22 `06-part-vi.md:766`. Ch 04 RunManifest change (owner: Ch 04).

3. **C08-R03**
   - **Priority:** High. **Action:** Add.
   - **Location:** immediately after the C08-R02 paragraph.
   - **Issue:** There are four unreconciled binding moments: Ch 07 `attach_skill` (`:77`), Ch 27 ReleaseManifest `skill_pack_versions` (`08-part-viii.md:366`), Ch 12 plan compile (`04-part-iv.md:410`), and per-run resolution here.
   - **Why it matters to the reader's mental model:** Readers of Ch 12 and Ch 27 will otherwise ask which one is the real pin.
   - **Change:** Add a four-row table, "When a Skill is bound | What is fixed":
     - **Build (Chapter 7):** a requirement (capability plus compatible version range), not a digest.
     - **Release (Chapters 9, 27):** the exact Skill and pack versions eligible for this release.
     - **Plan compile (Chapter 12):** each plan node's requirement, bound to one release from that set.
     - **Run (this chapter):** resolution against the run envelope pins one digest, recorded in the RunManifest and never re-resolved for the life of the run.

     Then one rule sentence: "Each later binding may only narrow the earlier one."

     Ch 07's SDK call becomes `attach_skill("mortgage.evidence.read@^0.1")` (C07-R05).
   - **Related sections:** Ch 07 C07-R05; Ch 12 `04-part-iv.md:410` (owner: Ch 12, add "(Chapter 8)"); Ch 27 (owner: Ch 27, state that the ReleaseManifest fixes the eligible set and the RunManifest records the resolved digests; this also feeds concept map T7).

4. **C08-R04**
   - **Priority:** High. **Action:** Rewrite.
   - **Location:** `:257–259` (Discovery paragraph); table row "Method" (`:269`); `:274–277`; Figure 8-1 node label "semantic, permissive" (`assets/diagrams/src/skill-resolution.gv`).
   - **Issue:** "Permissive" discovery contradicts Ch 05's "a capability the caller may not invoke should never appear" (`02-part-ii.md:430`) and AP-12's eligibility-filtered shortlist (`04-part-iv.md:1697`).
   - **Why it matters to the reader's mental model:** A reader holding Ch 05 sees a contradiction about the book's central discovery invariant.
   - **Change:**
     - Change "semantic and permissive" to "semantic and broad" at `:257` and in the figure label.
     - Add after `:259`: "Its candidates are input to resolution, not a menu for the model. When a model must choose among Skills, it sees only a shortlist that resolution has already made eligible (Chapter 5 § Capability and API catalog; AP-12)."
     - Table row "May a model influence it?": append "It never sees unfiltered candidates."
   - **Related sections:** Ch 05 (owner: Ch 05 keeps its sentence and adds "(Chapter 8 § Discovery is not permission)"); AP-12.

5. **C08-R05**
   - **Priority:** High. **Action:** Remove / Rewrite (prose and example code).
   - **Location:** YAML `lifecycle: active` (`:238`); the explanation at `:241–246`; `examples/platform/skills_registry.py` (`SkillManifest.status` and `validate_digest`; also `SkillPackManifest.status`, used by Ch 09).
   - **Issue:** Lifecycle state sits inside a manifest described as immutable and digested. In the example, `validate_digest` excludes only `digest`, so promoting draft→active changes the digest. The code's four states (`draft`, `active`, `deprecated`, `revoked`) contradict the prose's six. The concept map attributes this drift to Ch 09 only, but Ch 08's own example has it.
   - **Why it matters to the reader's mental model:** It breaks the chapter's core promise that the digest cannot move.
   - **Change:**
     - Delete `lifecycle: active` from the YAML.
     - Add to the explanation: "Lifecycle is not in the manifest. The manifest is immutable and digested, so its state lives in the registry's release record (SkillRelease), which changes as evidence arrives."
     - In the example, either move `status` to a registry-side record, or exclude `status` from the digest body. Widen the Literal to `draft`, `certified`, `staged`, `active`, `deprecated`, `revoked` for both manifests.
     - Make `register_pack`'s "active pack must reference only active skills" rule use the widened set.
     - Update `examples/tests/test_skills_registry.py` to assert that a status change does not change the digest.
   - **Related sections:** Ch 09 C09-R05; the state-owner table (`:204`, SkillRelease).

6. **C08-R06**
   - **Priority:** High. **Action:** Rewrite.
   - **Location:** YAML `side_effect_class: read_only` (`:219`) and `min_risk_tier: 1` (`:233`); the definition list at `:208` ("side-effect class").
   - **Issue:** Neither field is explained. "Tier" collides with Ch 26 governance tiers. `min_` inverts the code's semantics: `SkillManifest.maximum_risk` is a ceiling, and resolution admits only `requirement.maximum_risk <= skill.maximum_risk`. The effect semantics duplicate the ToolManifest Risk group (`06-part-vi.md:709`).
   - **Why it matters to the reader's mental model:** It plants a third and a fourth risk vocabulary in the reader's first manifest (T11).
   - **Change:** **Reconciled (see overall-book-review.md §D-01):** As stated: `risk_ceiling: R1` is an effect risk class. The conditional last bullet is resolved: R0–R4 stay defined in Ch 22 § Risk classes, with a gloss at first use in Ch 02, so point to Chapter 22. Ch 26's request to render this field as a T-tier (C26-R01 Related) is withdrawn.
     - Replace both lines with one: `risk_ceiling: R1   # highest effect risk class (R0–R4, Chapter 22) this Skill is certified for; resolution refuses anything above it`.
     - Remove `side_effect_class`; per-tool effect semantics live in each ToolManifest.
     - At `:208`, change "side-effect class" to "risk ceiling".
     - Optionally rename the code field `maximum_risk` to `risk_ceiling` in `examples/platform/skills_registry.py` and `examples/contracts.py` (`SkillRequirement`), keeping `PlanNode.risk_class` consistent.
     - If the synthesizer adopts concept map S6 (define R0–R4 earlier), point to that location instead of Ch 22.
   - **Related sections:** Ch 22 § Risk classes; Ch 26 § Match the control to the risk; Ch 09 "risk ceiling" (`:388`) is already consistent.

7. **C08-R07**
   - **Priority:** High. **Action:** Add.
   - **Location:** `## The Skill manifest`, after the explanation (`:246`), before the new H3 from C08-R01.
   - **Issue:** The chapter title promises versioning, but nothing says what a version number means.
   - **Why it matters to the reader's mental model:** The reader needs a model of "the number communicates interface, evidence certifies behavior". This is the Skill-level case of the book's "configuration change ≠ no release" invariant.
   - **Change:** Add about 90 words: "Every change, even one instruction sentence, produces a new digest and must re-pass certification. The version number communicates interface compatibility only: MAJOR for a breaking input/output schema change, a widened `requires` set, or a raised risk ceiling (each forces consumers' policy review to re-run); MINOR for compatible additions; PATCH for instruction or example changes that keep the interface. Behavioral compatibility is never inferred from the number; it is established by the evaluation gates and recorded on the release."
   - **Related sections:** Ch 27 § Treat the full behavior as the release; the example's SemVer parser.

8. **C08-R08**
   - **Priority:** Medium. **Action:** Rewrite / Cross-reference.
   - **Location:** `### Skill lifecycle`: the `:281` sentence, table rows Active, Deprecated, and Revoked (`:288–290`), and the prose at `:292`.
   - **Issue:** The table mixes up pinning and resolution and disagrees with the prose. It has no pointers to containment or rollback, and it may conflict with Ch 26's human approvals.
   - **Why it matters to the reader's mental model:** "Runs never re-resolve" is the property that makes rollback safe in Ch 27.
   - **Change:** **Reconciled (see overall-book-review.md §D-02, §D-32):** As stated, with three fixes. At `:281` write "For use-case tiers T3–T4 (Chapter 26 § Match the control to the risk), the required artifact includes a recorded risk approval." At `:292` the pointers become "(levels defined in Chapter 25 § Layer tests from contracts to outcomes)" and "Revocation is the Skill-scoped case of Chapter 23 § Stop new risky work without abandoning effects; the rule that rollback changes only new work is Chapter 27 § Roll back assignment, not history", because C25-R06, C23-R08/R09, and Ch 27's restructure rename those sections.
     - Active row, "What moves it forward": "A successor release, or an owner decision to retire".
     - Deprecated row, "Means": "Not resolvable for new runs; runs that pinned it keep executing that digest".
     - Revoked row, "Means": "Not resolvable; in-flight runs pinned to it pause or migrate by risk class".
     - At `:281`, append: "For higher governance tiers, the required artifact includes a recorded risk approval (Chapter 26 § Match the control to the risk)."
     - At `:292`, add after "Certification includes …": "(levels defined in Chapter 25 § Evaluation pyramid)". At the end, add: "Revocation is the Skill-scoped case of Chapter 23 § Scoped operational kill switch; the rule that rollback changes only new work is Chapter 27 § Rollback and active runs."
     - Align "support window" (checklist `:327`) with "compatibility window": use "compatibility window" in both.
   - **Related sections:** Ch 23, Ch 27, Ch 26, Ch 25.

9. **C08-R09**
   - **Priority:** Medium. **Action:** Merge / Move.
   - **Location:** `## Why a prompt is not a reusable capability` (`:189–195`), `## What belongs inside a Skill` (`:197–204`), and `:248`.
   - **Issue:** There are three successive descriptions of a Skill's contents, and motivation is stranded after the manifest explanation.
   - **Why it matters to the reader's mental model:** The reader should meet one definition (`:208`) and one motivation.
   - **Change:**
     - Delete the `## What belongs inside a Skill` heading and its first three sentences (`:199`, from "A Skill is useful…" through "…healthy.").
     - Append the remaining sentence ("A small prompt edit can alter tool selection, data exposure, or output shape even though no application code changed.") to the `:191–195` paragraph.
     - Move `:248` to follow it.
     - Keep the state-owner table directly under the merged H2.
   - **Related sections:** Ch 09 C09-R08 (same double-why pattern).

10. **C08-R10**
    - **Priority:** Medium. **Action:** Rewrite.
    - **Location:** `### Skill contract surface` (`:294–300`).
    - **Issue:** `invoke(step_request) -> AgentStepResult` misdescribes runtime execution, and the record names drift.
    - **Why it matters to the reader's mental model:** It contradicts the C08-R02 model, where a Skill is compiled into a step and not called.
    - **Change:** **Reconciled (see overall-book-review.md §D-05):** Rename `EvaluationReport` → `EvaluationResult` (Chapter 25) and `ReleaseDecision` → `PromotionDecision` (Chapter 27); the gate input to `promote` is Chapter 25's ReleaseGateDecision. The other items stand.
      - Replace the `invoke` bullet with `bind(release, step_request) -> AgentStepRequest`, and add the note "Skills are not called directly; the bound request is executed by AgentRuntime (Chapter 3)."
      - Rename `EvaluationReport` and `ReleaseDecision` to the names the Ch 25 review makes canonical (concept map T23; likely EvaluationResult and PromotionDecision).
      - Format the signatures as code spans, without backslash escapes.
    - **Related sections:** Ch 03; Ch 25/27.

11. **C08-R11**
    - **Priority:** Medium. **Action:** Add (conditional on a verified source) / Cross-reference.
    - **Location:** `## What the evidence lets us conclude` (`:308`).
    - **Issue:** The terminology row omits the "Agent Skills" folder format (SKILL.md instructions plus resources), the association many 2026 readers will bring to the word.
    - **Why it matters to the reader's mental model:** Without this, readers may assume the book's Skill *is* that format, and miss that the book adds manifest, policy, resolution, and evidence around such content.
    - **Change:**
      - Only after the author verifies and registers a primary source in `config/references.json` with a narrow scope (what the format packages), extend the row: "…nor the SKILL.md 'Agent Skills' packaging format; such content can serve as a Skill's instructions and resources, with the manifest, policy, and evidence supplied by the platform."
      - If no source is registered, make no claim.
      - Separately, **owner Ch 19**: qualify A2A "skills" at first use (`05-part-v.md:471`).
    - **Related sections:** Appendix D `09-appendices.md:289–290` (it already distinguishes A2A AgentSkill and Skills-over-MCP; keep it in sync).

12. **C08-R12**
    - **Priority:** Medium. **Action:** Add.
    - **Location:** `## A sensible place to start` / `### Skill manifest and resolver` (`:312–317`).
    - **Issue:** This is an empty wrapper with an unexplained example whose simplifications contradict the prose.
    - **Why it matters to the reader's mental model:** The reader should know what the code proves and what it leaves out.
    - **Change:** Add two sentences before the marker: "The resolver filters by capability, purpose, region, risk ceiling, and data class, then picks the highest eligible SemVer. Production resolution also takes the run envelope (subject and actor grants, tenant), evaluation, health, cost, and rollout policy, and pins by digest, which the example omits."
    - **Related sections:** C08-R05 (code fix).

13. **C08-R13**
    - **Priority:** Low. **Action:** Rewrite.
    - **Location:** `## If this fails in production`, step 1 (`:321`).
    - **Issue:** Re-resolving today can give a different answer from the original run.
    - **Why it matters to the reader's mental model:** It reinforces "pinned runs never re-resolve".
    - **Change:** "Read the pinned digest and the recorded requirement and envelope from the RunManifest. Re-run resolution as of the run's start and compare: a different answer means the registry changed underneath; the same answer locates the defect in that Skill version."
    - **Related sections:** C08-R02 (RunManifest field).

14. **C08-R14**
    - **Priority:** Low. **Action:** Rewrite.
    - **Location:** `## Questions to bring to design review`: Q3 (`:348`) and Q4 (`:349`).
    - **Issue:** Portability is never taught in the body, and Q4's test list disagrees with `:292`.
    - **Why it matters to the reader's mental model:** Review answers should test the chapter's model.
    - **Change:**
      - Replace Q3 with "Does resolving a Skill authorize its tool calls?" Strong answer: "No. Resolution selects which Skill version may run; every tool call it proposes still passes the Tool Gateway's validation, authorization, and effect controls."
      - Change Q4's answer to the `:292` list plus "(levels in Chapter 25)".
    - **Related sections:** C08-R02.
