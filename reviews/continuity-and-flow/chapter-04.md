# Chapter 04 — Design the Architecture Around the Model: Continuity and Flow Review

Reviewed: `source/parts/02-part-ii.md:1–340` (Part II orientation and Chapter 04). For transitions I also read `01-part-i.md:480–513` (Figure 1-3 and the "same picture" claim), `01-part-i.md:1012–1312` (Ch 03 AgentRuntime through its closing), and `02-part-ii.md:342–360` (Ch 05 opening). Figures were checked in `assets/diagrams/src/reference-architecture.gv`, `system-overview.gv`, and `request-sequence.mmd`. Later homes were checked in Ch 15 (`04-part-iv.md:1142–1240`), Ch 22 (`06-part-vi.md:665–900`), Ch 27 (`08-part-viii.md:186–200`, `:230`, `:299`, `:455`), and `examples/contracts.py`.

## Overall Assessment

Ch 04 is meant to be the book's map: the chapter where every later contract gets an owner and a place. The parts it needs are all present: the plane table, the ownership table, the layer table, the trust boundaries, the contracts, and the store table. As written, though, it reads as a set of reference tables in a confusing order rather than as a map. There are four main problems.

1. **Three decompositions with three vocabularies.** The plane table (`:36–44`), Figure 4-1, and the layer table (`:130–142`) name the same things differently. Five layers are called "…plane", and a third sense of "plane" (the deployment tier: "global definition and governance plane" at `:87`, "global control plane" at `:26` and `:333`) arrives mid-chapter. [verified: corrected — "sixth meaning" overcounted; the chapter uses "plane" in three senses (ownership plane, layer called plane, deployment tier), matching C04-R12] Ch 01 tells the reader Figure 4-1 is "this same picture at higher resolution" (`01-part-i.md:510`). It is not: no band name in Figure 1-3 survives unchanged in Figure 4-1 (the closest is "Systems of record" → "Systems of record and providers").
2. **The Ch 03 seam disappears.** Ch 03 closes by promising to place the AgentRuntime boundary in the architecture (`01-part-i.md:1312`). The Ch 04 prose never names AgentRuntime, AgentStepRequest, or AgentStepResult. The "Agent Runtime" participant appears only in Figure 4-2, and "bounded agent workers" appears only in Figure 4-1 and at `:87`.
3. **Contracts without owners or pointers.** About 20 records are listed (`:38–44`, `:93`) with no defining chapter. Several of them (RunManifest, the effect receipt, the event envelope, the Run API) are later re-specified with drift in Ch 03, 15, 22, and 27. The effect receipt paragraph blurs the downstream receipt and the platform's effect state (`:204`). [verified: softened — see § Effect receipt] The chapter's own example, `[[EXAMPLE:contracts]]` (`:256`), contains none of the contracts the chapter defines.
4. **Order.** The opening callouts sit mid-chapter (`:75–83`). Two H2s are empty wrappers (`:97`, `:157`). The layer explanation points back to "the plane table above" across five sections (`:104`). The Run API paragraph (`:89`) is 70 lines away from the Run API table (`:159`).

None of these problems needs new material. They need renaming, reordering, pointers, and handing detail to its later homes.

## Intended Reader Mental Model

On arrival the reader knows four things: the model proposes and the platform commits (Ch 02); the six gates; AgentRuntime runs one bounded step behind `AgentStepRequest → AgentStepResult`; and framework state ≠ business state (Ch 03).

The reader should leave with:

- **What:** seven ownership planes. Each authoritative record has exactly one writing plane.
- **Why:** central components such as gateways sit on every path and will accumulate authority unless ownership is explicit.
- **How:** planes split into deployable layers; one request crosses eight trust boundaries; a few cross-cutting contracts hold it together (Run API, RunManifest, artifact, receipt, event); named stores carry the records; a global control tier is separated from regional execution cells.
- **When:** use planes to argue about ownership and layers to deploy and page.
- **Relationships:** where AgentRuntime sits, and which later chapter owns each record.
- **Practical application:** for any record, a team can name its single writer, its store, and its consistency model.

The reader should leave holding one picture, with one name per box, and an index from each box to the chapter that develops it.

## Section-by-Section Flow Review

**Part II orientation (`:1–7`).** *Role:* frames Part II as "draw the system around" the model. *Adds:* four promises (who owns each fact, where policy is enforced, how knowledge stays current, per-run authorized context). *Verdict:* adequate and brief. *Issues:* the promise of "how knowledge stays current" is only weakly kept. Ch 05 covers versions and supersession, but index freshness and ingestion sit in Ch 06's scale bullets (`:760`, `:769`); see C05-R08. Nothing else needs to change.

**§ Why the model cannot own the architecture (`:11–18`).** *Role:* chapter intro. *Adds:* the purpose (turn rules into planes, services, contracts, stores, cells). *Verdict:* weak opening. *Issues:*

- The heading promises an argument the paragraph never makes.
- There is no bridge from Ch 03's AgentRuntime seam.
- No case box. The NORTHSTAR and DESIGN CHOICE boxes appear 60 lines later (`:77–83`).

**§ The planes and the ownership map (`:20–26`).** *Role:* defines planes versus layers. *Adds:* the key distinction, plus the warning that a model gateway "should not own business workflow simply because every call passes through it" (`:22`). *Verdict:* the right idea in the wrong container. *Issues:*

- The heading promises the map, but the map (the plane table) is in the next section.
- The parenthetical "identity, policy, execution, knowledge, or operations" names five examples, none of which is a plane name as written; only "operations" echoes one ("Evaluation and operations"). [verified: softened — "match none" overstated the mismatch]
- The state-owner table (`:24–26`) is the section's only other content. It is never explained (map §5.1), and it previews "global control plane to regional execution cell" before cells are introduced.

**§ What the architecture is trying to protect (`:28–44`).** *Role:* Figure 4-1 plus the plane table. *Adds:* the seven planes and their records and boundaries. This is the chapter's core. *Verdict:* essential content with a mismatched heading and figure. *Issues:*

- Figure 4-1's bands (`reference-architecture.gv:32–145`) are not the planes. It has "Edge and admission" (a layer), "Run control and durable execution" (two layers fused), "Knowledge, context and memory" (the plane table says "Context, RAG, memory, Skills"), "Trust and governance" (the layer name; the plane is "Security and governance"), "Evidence and improvement" (the plane is "Evaluation and operations"), and "Systems of record and providers" (not a plane).
- `:34` says "each layer names the components the plane owns", which conflates the two decompositions the chapter later says not to confuse (`:101–102`).
- "Skills" is placed in the context plane (`:41`), yet the layer table puts the "prompt/skill catalog" in the Agent control plane (`:134`), and Ch 08 makes the Skill a registry-released capability. Skills therefore have two owning planes.
- None of the ~18 records in the table has a chapter pointer (map §4 row 19). [verified: corrected — the Authoritative records column names 18 records, not ~12]

**§ End-to-end responsibility flow (`:46–57`).** *Role:* walks one request through the architecture. *Adds:* Figure 4-2 and eight steps. *Verdict:* useful, but it does not yet do the Ch 04-specific job. *Issues:*

- The steps never name the plane or record that owns each step, which is what would distinguish them from Ch 03 § The complete execution path (9 steps) and Ch 15 § Canonical control flow (10).
- Step 4 says "Let the model propose… Policy determines eligible models, tools…", which places eligibility after the proposal. Ch 06 (`:656–658`) and Ch 03 (`01-part-i.md:1044`) fix eligibility before the step.
- Step 7's terminal vocabulary (accepted / blocked / needs-input / failed / unknown-effect) is a fourth vocabulary (map T12).
- Figure 4-2 (`request-sequence.mmd`) has the *Agent Runtime* resolve context from *Policy & Identity* after receiving the bounded step. That contradicts Ch 03 (the AgentStepRequest already carries an authorized ContextManifest) and Ch 06 (a Context Service assembles it). The figure also shows no human-approval hop (its only authorization hop is Run → Policy & Identity, `request-sequence.mmd:20–21`), although step 5 binds protected changes to a human authorization. [verified: corrected — the figure does have a policy-authorization hop; what is missing is the human approval]

**§ Where truth lives (`:59–69`).** *Role:* the model-may / model-may-not table per concern. *Adds:* the canonical "truth ownership" table (map §3). *Verdict:* keep it as the canonical home. *Issues:* component names drift from their later homes: "Durable Run Service", "Tool/effect service" (Ch 22: Effect Service), and "Proposal and human action authorization service" (Ch 14: Human Action Authorization Service). Map T24 and T25 apply.

**§ The decisions that shape the system (`:71–83`).** *Role:* centralize versus federate. *Adds:* a unique, useful rule (`:73`). *Verdict:* the paragraph is good; what follows it is misplaced. *Issues:*

- The CloudEvents/outbox evidence-context box (`:75`) belongs to § Event contract.
- The NORTHSTAR and DESIGN CHOICE boxes (`:77–83`) are opening callouts stranded mid-chapter.
- The design choice ("Deploy global definitions … into regional execution cells") states one deployment decision, not the chapter's thesis (single-writer ownership across planes).

**§ Turn the diagram into enforceable contracts (`:85–95`).** *Role:* introduces the global control versus regional cell split and the Run API semantics. *Verdict:* two topics fused, and the chapter's headline design choice is under-explained. *Issues:*

- "Global definition and governance plane" adds a third sense of "plane" (deployment tier). [verified: corrected — was "sixth"; consistent with C04-R12]
- What a *cell* is, and why runs have a home cell, is explained only in the Q&A answers (`:333`, `:335`).
- The Run API paragraph (`:89`) is separated from its table (`:159`).

**§ Core authoritative records (`:91–95`).** *Role:* lists the 14 records that need single owners. *Verdict:* the most valuable list in the chapter, but it is unusable as written. *Issues:*

- No owners, no planes, no chapter pointers.
- Names drift: "AgentStep" (T9); "EvaluationReport" is never defined and appears only here and in Ch 08's `evaluate()` signature (`03-part-iii.md:299`), while Ch 25 uses EvaluationResult (T23, D-05) [verified: corrected — not a strict orphan; one other occurrence]; WorkflowExecution belongs to Ch 15 (`04-part-iv.md:1224`).
- The scale paragraph (`:95`) has nothing to do with "records" and belongs with cells.

**§ A practical reference architecture (`:97`).** An empty wrapper H2. Remove it.

**§ Seven planes, eleven layers — which is which (`:99–126`).** *Role:* reconciles planes and layers. *Adds:* a clear rule ("If the two ever disagree about who owns a record, the plane model wins"). *Verdict:* good content in the wrong position, and it undermines itself. *Issues:*

- "The plane table above" is 68 lines back.
- The split table renames five layers "…plane", so the section meant to separate the two terms re-entangles them.
- "Context, RAG, memory, Skills → Data and knowledge" maps a plane onto a layer that holds *every* plane's RDBMS and object storage (`:139`), which contradicts "every authoritative record in exactly one place" (`:107`).

**§ Architecture layers (`:128–142`).** *Role:* the deployable components per layer. *Verdict:* needed reference content. *Issues:*

- "Model gateway" (`:137`; also `:22`, `:87`) versus "LLM Gateway" in Figure 4-1 and Ch 01/19 (T4).
- "Human action authorization service" sits in the Run control layer, while the plane table puts HumanActionAuthorization records in Security and governance (`:43`). Two owners again.

**§ Trust boundaries (`:144–155`).** *Role:* eight boundaries with untrusted inputs and mandatory controls. *Verdict:* strong and canonical (map §3). *Issues:*

- Controls name later mechanisms without pointers: "PDP decision, downscoped token" (Ch 21), "signed task envelope" (Ch 18/19), "dry-run/approval" (Ch 14), "default-deny egress" (Ch 23).
- Ch 20 § Follow the request across each trust boundary never cites this table.

**§ The contracts that hold the platform together (`:157`).** An empty wrapper H2. It should lead with the authoritative-records table instead (C04-R04).

**§ Run API (`:159–170`).** *Role:* the public run resource. *Verdict:* duplicated, and it has drifted from Ch 15 § The contracts between components (`04-part-iv.md:1208–1218`). Both tables define POST runs, GET, signal, and cancel. Ch 04 alone has `:update`, `:fork`, and `/audit`; Ch 15 alone has `:pause`, `:resume`, `:migrate`, `events:ingest`, and `/history`. *Issues:* the `:fork` name collides with Ch 25's `:forkReplay` (map §5.2).

**§ RunManifest (`:172–196`).** *Role:* per-run version pinning. *Verdict:* the canonical home (map §3), but there is no prose at all, only JSON. *Issues:*

- It never says what a RunManifest is, when it is written (step 2), or how it relates to ReleaseManifest (Ch 27, T7), ContextManifest (Ch 06), or AgentStepRequest (Ch 03).
- Ch 03's RunManifest table (`01-part-i.md:1225–1232`) pins `sdk` and `context_manifest`. This JSON has no SDK/adapter field, so it cannot support Ch 03's "SDK upgrades are behavioral changes". It also has, rightly, no per-call context manifest.
- Identifiers drift from Ch 03 (`route://reasoning-standard@18` vs `reasoning-standard@4`; `policy://enterprise-agent@2026.09.3` vs `mortgage-policy@2026.09`; map T16).
- `authority_envelope` should be CapabilityEnvelope (T6), and `"risk_tier": "high"` is a third risk scale (T11).
- It is inline code, against `AGENTS.md`.

**§ Artifact contract (`:198–200`).** *Role:* the artifact field list. *Verdict:* fine. It is the only full statement in the book. Dense, but it earns its place.

**§ Effect receipt (`:202–204`).** *Role:* previews the effect receipt. *Verdict:* redundant with Ch 22, and it blurs the receipt and the effect state. *Issues:* the receipt carries a "committed/declined/unknown state", and the next sentence says "a timeout without a receipt is unknown". The two sentences are not strictly contradictory (unknown can arise from a receipt or from its absence), but together they make the downstream receipt the carrier of effect state. [verified: softened — the text never says "unknown" means "no receipt", so the self-contradiction claim was overstated; the receipt-versus-EffectRecord conflation stands] Ch 22 separates the downstream receipt (proof) from the EffectRecord state (`06-part-vi.md:671`, `:769`, `:870`); Ch 04 merges them. Its state set (3) also differs from Ch 22's nine (T13).

**§ Event contract (`:206–226`).** *Role:* the CloudEvents envelope. *Verdict:* this is the envelope's canonical home (map §3), but there are two shapes in one chapter. *Issues:*

- The JSON has `correlation_id`, `causation_id`, `dataref`, and `datahash`. The Python model at `:270–290` has none of these and makes `data: dict` required. That diverges from the JSON's own `dataref`/`datahash` design and sits uneasily with the by-reference rule at `:89` and `:200`, which is stated for large payloads. [verified: softened — the `:89`/`:200` rule covers large inputs and artifacts, so a required `data` dict is a divergence, not a contradiction]
- There is no prose. "Commands versus facts" is never said, although Ch 22's checklist assumes it (map §4 row 59).
- Ch 15 § Event architecture (`04-part-iv.md:1198`) re-lists the same fields.

**§ Where each kind of state belongs (`:228–242`).** *Role:* nine physical stores and their consistency controls. *Adds:* the closing invariant paragraph (`:242`), one of the book's best sentences. *Verdict:* keep it here (see Cross-Chapter Duplication for my disagreement with the map). *Issues:*

- There is no row for the conversation store or the governed memory service, which Ch 06 introduces (`:683`, `:687`). Memory therefore has no physical home in the platform's store table.

**§ What the evidence lets us conclude (`:244–250`).** One claim, R04. R03 (outbox) is cited in the stray evidence box (`:75`) and in the `:250` sources sentence, but has no claim row. [verified: corrected — `:250` also cites R03] *Verdict:* adequate.

**§ A sensible place to start (`:252`) / § Core platform data contracts (`:254–256`) / § CloudEvents and outbox contracts (`:258–303`).** *Verdict:* mismatched. *Issues:*

- `[[EXAMPLE:contracts]]` renders all of `examples/contracts.py`: EvidenceRef, ToolCall, AgentDecision, AgentStepRequest/Result, SkillRequirement, PlanNode, and CandidatePlan. None of these is a contract this chapter defines, and PlanNode's integer `risk_class` pre-teaches Ch 12/22 (map §4 row 33).
- The only place Ch 04 shows AgentStepRequest/Result is this unannounced listing.
- The inline CloudEvent/OutboxRecord code duplicates the § Event contract JSON with drift, and OutboxRecord is Ch 22's entity (`06-part-vi.md:871`).

**Template sections: § If this fails in production (`:305`), § What to verify before production (`:311`), § Put the idea to work (`:323`), § Questions to bring to design review (`:328`).**

- *If this fails:* three good, chapter-specific checks.
- *Verify:* item 4 (continue on pinned releases during control-plane disruption) has no supporting prose in this chapter; Ch 27 `:195` explains it.
- *Put the idea to work, item 1:* asks the reader to define Task, Tool, Approval, and Release contracts that are taught in Ch 18, 22, 14, and 27.
- *Design review:*
  - Q1 and Q3 are recall lists that restate the plane and boundary tables.
  - Q2 ≈ Ch 27 Q (`08-part-viii.md:455`).
  - Q5 (control-plane outage) is operational content that Ch 27 `:195` owns, and it forward-references kill switches (Ch 23) and last-known-good bundles (Ch 27).

**§ Where this leads next (`:338–340`).** *Verdict:* adequate. *Issues:* it says "knowledge plane" and "governed knowledge layer", but no plane has that name (T27). This is fixed by C04-R01.

## Sparse or Underdeveloped Content

- **RunManifest (`:172`).** JSON only. It needs 2–3 sentences: when it is written, what it references, and how it relates to ReleaseManifest, ContextManifest, and AgentStepRequest (C04-R07).
- **Regional execution cells (`:87`, `:95`).** This is the chapter's DESIGN CHOICE, yet the cell is defined only by a component list and Q&A answers. It needs 2–3 sentences on what is global versus regional, home-cell placement, and fail-closed high-risk admission, with Ch 27 for operations (C04-R12).
- **Event contract (`:206`).** There is no sentence on commands versus facts or on the reference-not-payload rule (C04-R09).
- **AgentRuntime placement.** It needs one sentence, not a section (C04-R02).

Do not expand the Artifact contract, the trust boundaries, or the store table. They are dense but complete.

## Missing Conceptual Connections

- **Ch 03 AgentRuntime → Ch 04 planes, missing "which plane runs the step".** At `:44` (after the plane table) and `:87`. The Runtime and workflow plane builds the AgentStepRequest; the Agent applications plane executes it through AgentRuntime and the framework adapter; the AgentStepResult returns to the workflow.
- **Figure 1-3 bands → Figure 4-1, missing a band-to-plane mapping.** At `:34`. Without one, Ch 01's "same picture" claim is false.
- **Plane table → later chapters, missing pointers.** At `:38–44` and `:93`. The reader cannot tell which chapter defines ContextManifest, CapabilityEnvelope, ToolManifest, or the others.
- **RunManifest → ContextManifest, missing granularity.** At `:172`. One RunManifest per run; one ContextManifest per model step, which references it. Ch 03's table puts `context_manifest` in the RunManifest, which blurs this.
- **Eligibility → proposal, missing ordering.** At `:53`. Eligibility is fixed in the AgentStepRequest before the model runs; authorization of the specific proposed action follows the proposal.
- **Store table → Ch 06 memory and conversation stores.** At `:230–240`.
- **Effect receipt → EffectRecord, missing the proof-versus-state split.** At `:204`.

## Transition Problems

- **In (Ch 03 → Ch 04).** Ch 03's last sentence promises to place "that boundary" in the architecture (`01-part-i.md:1312`). Ch 04 `:13` opens with "Principles become useful…" and never returns to the boundary. Fix with C04-R02.
- **Opening callouts mid-chapter (`:75–83`).** The reader meets the NORTHSTAR situation and the design choice after the plane table, the flow, and the ownership table.
- **Within the chapter.**
  - `:97–104` jumps back 68 lines to "the plane table above".
  - `:89` (Run API semantics) and `:159` (Run API table) are split.
  - `:157` is an empty H2 before the contracts.
- **Out (Ch 04 → Ch 05).** "Names a knowledge plane" refers to a plane that does not exist under that name. Ch 05's opening does not refer back to Ch 04 at all (see C05-R13).

## Redundant and Repetitive Concepts

- **"X is not Y" boundaries stated three times:** the plane table's Boundary column (`:38–44`), the Where truth lives "Model may not" column (`:63–69`), and `:242`. These are distinct axes (plane boundary, model limit, store role). Mild; keep all three and do not add a fourth.
- **Run API semantics:** `:89` and `:159–170` say overlapping things. Merge (C04-R08).
- **Event envelope:** JSON at `:210–225` and Python at `:270–290`. Keep one (C04-R09/R10).
- **Plane names:** recited again in Q1 (`:332`); trust boundaries recited again in Q3 (`:334`). Recall-only repetition (C04-R16).
- **Cells:** the state-owner table (`:26`), `:87`, the design choice (`:83`), Q2, and Q4. Five touches and no explanation. Consolidate them into one paragraph (C04-R12).

## Cross-Chapter Duplication

| Ch 04 location | Other location | Verdict | Recommended owner |
| --- | --- | --- | --- |
| § End-to-end responsibility flow (`:46–57`) | Ch 03 § The complete execution path (`01-part-i.md:1203`); Ch 15 § Canonical control flow (`04-part-iv.md:1156`); Ch 20 `06-part-vi.md:93`; Ch 22 § Invocation sequence | **D** with drift (8/9/10/6 steps) | Ch 04 overview annotated by plane; Ch 15 detail. Ch 03's list is trimmed to a pointer (Ch 03 review, map S5) |
| § Where truth lives | Ch 01 § Which component should own each uncertainty; Ch 02 § Where distributed systems must remain authoritative; Ch 03 § Runtime responsibility versus enterprise responsibility and § Responsibility map | D (same model-may / platform-owns axis) | Ch 04 for truth ownership; the others reference it |
| § Run API | Ch 15 § The contracts between components (`04-part-iv.md:1208`) | **D** with drift | Ch 15 owns the full operational table; Ch 04 keeps the public subset (C04-R08). I agree with the map |
| § RunManifest | Ch 03 § Framework upgrades are behavioral changes (`01-part-i.md:1225`); Ch 27 `08-part-viii.md:230`, `:299`; Appendix C | D with drift | Ch 04 canonical; Ch 03 references it; Ch 27 states the RunManifest → ReleaseManifest relation |
| § Effect receipt | Ch 22 `06-part-vi.md:671`, `:769`, `:857`, `:870` | **D**, and contradictory | Ch 22 |
| § Event contract + § CloudEvents and outbox contracts | Ch 15 § Event architecture (`04-part-iv.md:1198`, same field list); Ch 22 OutboxRecord/InboxReceipt (`06-part-vi.md:871–872`) | D | Envelope: Ch 04. Outbox and inbox delivery semantics: Ch 22. Ch 15 points to both |
| § Trust boundaries | Ch 20 § Follow the request across each trust boundary + Figure 20-2 | R (Ch 20 adds threats), but uncited | Ch 04 table; Ch 20 cites it (Ch 20 review) |
| Cells (`:87`), Q2, Q5 | Ch 27 § A production topology… (`08-part-viii.md:186–200`), Q (`:455`) | D | Ch 04 design rationale (Q2 stays); Ch 27 operations (receives Q5, drops its `:455` Q) |
| § Where each kind of state belongs | Ch 06 § State taxonomy and storage (`02-part-ii.md:679`); Ch 15 § Records worth preserving | Partial D, on different axes | **I disagree with the map** (which says Ch 06 absorbs the Ch 04 table). Ch 04's table is about physical stores, consistency, secrets, KMS, broker, cache, and WORM. These are platform-wide and fit no context chapter, and Ch 01's exercise at `:594` ("label every authoritative store") is served by this table. [verified: softened — `:594` does not name Ch 04; it is an exercise this table answers] Keep it canonical in Ch 04; Ch 06 trims its taxonomy to context sources and points here (C06-R03) |
| Figure 4-2 | Figure 20-3 `guardrail-sequence` | Overlapping: both share the authorize → Tool Gateway → commit → receipt → effect-record tail; Figure 20-3 adds an input-guardrail hop and an approval hop, starts at the Agent Runtime rather than the user, and has no run-service opening [verified: softened — was "near-identical"; the two `.mmd` sources differ in participants and in their first half] | Ch 20 review decides; Ch 04's figure is the base |
| Layer table "Model plane / Capability plane" gateways | Ch 01 § Each control point…; Ch 19 LLM Gateway table | D on names | Names follow Ch 01's gateway set (T4). If map S4(a) is adopted, an LLM Gateway H3 lands after § Architecture layers |

## Structural Recommendations

Adopt map S7 with this concrete order (current line numbers in brackets):

1. Opening callouts: NORTHSTAR [`:77–79`] and a rewritten DESIGN CHOICE [`:81–83`], placed directly under the H1.
2. § Why the model cannot own the architecture [`:11`], with the Ch 03 bridge (C04-R02).
3. § Seven planes, one owner per record. This merges [`:20–26`] and [`:28–44`]: the planes-vs-layers paragraph, Figure 4-1 and its reading paragraph, the Figure 1-3 → 4-1 mapping, the plane table, the AgentRuntime sentence, and the state-owner table last.
4. § Where truth lives [`:59`].
5. § The decisions that shape the system [`:71–73`], paragraph only.
6. § From planes to deployable layers. The former [`:97–142`], minus the empty H2; "above" becomes "the plane table".
7. § Trust boundaries [`:144`], promoted to H2.
8. § Global control and regional cells. The former [`:85–87`, `:95`], expanded (C04-R12).
9. § End-to-end responsibility flow [`:46`], annotated by plane (C04-R11). It now comes after the reader knows the planes, layers, and boundaries.
10. § The contracts that hold the platform together, led by the authoritative-records table [`:91–93`] (C04-R04), then Run API (with [`:89`]), RunManifest, Artifact contract, Effect receipt (short), and Event contract (with the [`:75`] evidence box).
11. § Where each kind of state belongs [`:228`].
12. Evidence, start, and the template sections.

## Concrete Recommended Changes

1. **C04-R01 — High — Rewrite.**
   - *Location:* `02-part-ii.md:22`, `:30–44`, `:113–142`, `:340`; `assets/diagrams/src/reference-architecture.gv`.
   - *Issue:* three name sets for one architecture; five layers named "plane"; Skills owned by two planes.
   - *Why:* readers cannot hold one picture while the boxes keep changing names, and the "every record in one place" rule is broken by the chapter's own tables.
   - *Change:*
     - Rename the plane "Context, RAG, memory, Skills" to **"Knowledge, context, and memory"**. Move "Skill manifest" to the Agent applications row ("AgentSpec, Skill manifest, application release"); this matches Ch 08's Skill Registry.
     - At `:22`, replace "identity, policy, execution, knowledge, or operations" with examples drawn from the plane names.
     - Rename the layers so none is called "plane": Agent control plane → **Agent registry and release**; Run control plane → **Run control**; Model plane → **Model access**; Capability plane → **Tool and protocol access**; Execution plane → **Sandboxed execution**. Rename "Data and knowledge" → **Knowledge and context services** (components: Context Service, Knowledge Hub, search/vector index, catalog/lineage, memory service). Remove "RDBMS, object store" from that row and add the note "shared stores: see § Where each kind of state belongs".
     - In Figure 4-1, use the plane names: bands Experience and channels (edge and admission components as a sub-row), Agent applications, Runtime and workflow, Knowledge context and memory, Gateways and integration; spines **Security and governance** and **Evaluation and operations**; bottom band "Systems of record and providers — outside the trust boundary". Move the Skills node from `k3` to the agent band.
     - Rewrite `:34` "each layer names the components the plane owns" as "each band is one ownership plane and lists its main components".
     - Run `make diagrams`.
   - *Related:* map T2/T27; C04-R03, C04-R18; Ch 27 must say "regional execution cell", not "regional execution plane" (Ch 27 review owns that); for "global control plane" see C04-R12.

2. **C04-R02 — High — Add.**
   - *Location:* `:13–18` (§ Why the model cannot own the architecture); after `:44`; `:87`; `:93`.
   - *Issue:* the Ch 03 seam is never placed, and the Ch 03 → Ch 04 promise is unkept.
   - *Why:* the reader's newest mental model (AgentRuntime) has no box in the architecture.
   - *Change:*
     - At `:13`, open with two sentences: Chapter 3 drew one seam (AgentRuntime runs a bounded step from an AgentStepRequest and returns an AgentStepResult); this chapter places that seam and every service around it so that each record has one writer.
     - After the plane table, add one sentence: the Runtime and workflow plane builds the AgentStepRequest; the Agent applications plane executes it through AgentRuntime and its framework adapter; the typed AgentStepResult returns to the workflow, which alone decides the next transition.
     - At `:87`, change "bounded agent workers" to "bounded agent workers (AgentRuntime and its adapters, Chapter 3)".
     - In `:93`, replace "AgentStep" with "AgentStepRequest/AgentStepResult".
   - *Related:* C04-R04, C04-R10; Ch 07 review (RunContext → AgentStepRequest).

3. **C04-R03 — High — Add / Cross-reference.**
   - *Location:* after the Figure 4-1 reading paragraph (`:34`); `01-part-i.md:510–513`.
   - *Issue:* Ch 01's claim that Figure 4-1 is "this same picture at higher resolution" is false. Bands are renamed, split, merged, or dropped (Collaboration, Control points, and the Platform spine have no counterpart).
   - *Why:* the reader is told nothing new must be learned, then finds new names.
   - *Change:* add a compact two-column table "Figure 1-3 band → Chapter 4 plane":
     - Channels → Experience and channels
     - Agent runtime → Agent applications + Runtime and workflow
     - Collaboration → Runtime and workflow (child tasks) + Gateways and integration (A2A)
     - Knowledge → Knowledge, context, and memory
     - Control points → Gateways and integration (admission sits in Experience and channels; approval in Security and governance)
     - Security spine → Security and governance
     - Systems of record → outside the planes
     - Evidence → Evaluation and operations
     - Platform spine → Part III, not drawn here

     Ch 01 owns its own sentence: it should say "Figure 4-1 refines these bands into seven ownership planes; Chapter 4 maps one onto the other."
   - *Related:* C04-R01; Ch 01 review.

4. **C04-R04 — High — Rewrite.**
   - *Location:* `:91–93` (§ Core authoritative records) and the "Authoritative records" column at `:38–44`.
   - *Issue:* about 20 records with no owner, plane, or chapter; orphan and drifted names.
   - *Why:* this is the chapter's index function. Without pointers it reads as undefined jargon (map §4 rows 19–20).
   - *Change:* replace the `:93` sentence with a table, Record | Owning plane | Defined in. The rows are:

     | Record | Owning plane | Defined in |
     | --- | --- | --- |
     | RunManifest | Runtime and workflow | Ch 04 |
     | WorkflowExecution | Runtime and workflow | Ch 15 |
     | TaskEnvelope | Runtime and workflow | Ch 18 |
     | AgentStepRequest/Result | Runtime and workflow → Agent applications | Ch 03 |
     | ContextManifest, MemoryRecord | Knowledge, context, and memory | Ch 06 |
     | Skill manifest | Agent applications | Ch 08 |
     | CapabilityEnvelope, CredentialLease | Security and governance | Ch 21 |
     | PolicyDecision | Security and governance | Ch 21 |
     | ToolManifest, EffectRecord | Gateways and integration (Effect Service) | Ch 22 |
     | HumanActionAuthorizationRequest/Decision | Security and governance | Ch 14 |
     | Artifact | Runtime and workflow (the producing run owns the version; the artifact store holds the bytes) | Ch 04 |
     | EvaluationResult (replaces "EvaluationReport") | Evaluation and operations | Ch 25 |
     | ReleaseManifest, ChangeBundle | Evaluation and operations | Ch 27 |

     [verified: corrected — ChangeBundle was "Ch 27/25"; overall-book-review.md §D-05 has Ch 27 define both ChangeBundle and ReleaseManifest. Under §D-22 the HumanActionAuthorizationRequest/Decision row is written as ApprovalRequest/ApprovalDecision (Approval Service) when applied.]

     Keep the closing clause "each has one owner, version, retention policy, and consistency boundary". Move the scale paragraph (`:95`) to the cells section (C04-R12). Shorten the plane table's records column to names only, since pointers now live in this table.
   - *Related:* map T9, T23; C04-R02; and the human action authorization service placement at `:135` vs `:43`, which must name one owning plane.

5. **C04-R05 — High — Move.**
   - *Location:* whole chapter (`:11–257`).
   - *Issue:* callouts mid-chapter, empty H2s at `:97` and `:157`, the "above" back-reference, and the Run API split.
   - *Why:* the reader meets the flow and the ownership tables before the decomposition that explains them.
   - *Change:* **Reconciled (see overall-book-review.md §D-20):** Apply the order as stated, but the opening NORTHSTAR AT THIS POINT callout becomes a WHERE THE MORTGAGE CASE STANDS box, and "Northstar" becomes "the Harborlight platform" (Northstar is dropped book-wide). Original text: apply the order in Structural Recommendations. Delete the H2s `:97` (§ A practical reference architecture) and `:157` (§ The contracts that hold the platform together, which is re-headed over the records table). Rename § What the architecture is trying to protect to "Seven planes, one owner per record". Rewrite the DESIGN CHOICE as: "Give every authoritative record one owning plane and one writer; deploy global definitions and governance into regional execution cells connected by provider-neutral contracts."
   - *Related:* map S7.

6. **C04-R06 — High — Condense.**
   - *Location:* `:202–204` (§ Effect receipt).
   - *Issue:* the receipt both carries "unknown" and is absent when the outcome is unknown; it duplicates Ch 22 with a different state set.
   - *Why:* the effect-truth model is the book's core invariant, and an early contradiction undermines Ch 22.
   - *Change:* replace the paragraph with two sentences: "A mutating tool returns a receipt from the system of record (proof of what happened); the platform's EffectRecord, not the receipt or the model, holds the effect's state. A timeout without a receipt is Unknown, not failed; Chapter 22 defines the receipt fields and the effect state machine." The Ch 22 review should confirm that Ch 22's receipt definition (`06-part-vi.md:671`) includes the fields only Ch 04 lists today: verification query, audit link, actor/subject, and compensation reference.
   - *Related:* map T13; Ch 22 review.

7. **C04-R07 — Medium — Add / Rewrite.**
   - *Location:* `:172–196` (§ RunManifest).
   - *Issue:* no prose; drift from Ch 03; no runtime field; unclear relation to ReleaseManifest and ContextManifest.
   - *Why:* RunManifest is cited in 8+ chapters as the reproducibility anchor.
   - *Change:* **Reconciled (see overall-book-review.md §D-02, §D-27):** As stated, with three changes. (1) `"risk_tier": "T3"` (use-case tier, Chapter 26). (2) Add `"skills"` (resolved Skill digests) and `"skill_pack"` per C04-R20. (3) The RunManifest references the ReleaseManifest digest and records only what is resolved per run (Skill digests, knowledge snapshots, the model route chosen within the release's eligible set, capability envelope ID, budget, use-case tier); it does not re-list every release pin. Show it through the `platform` example region (C04-R10), not as inline JSON.
     - Add before the JSON: "The RunManifest is written once, at admission (step 2), and resolves every version the run may use. It references the promoted ReleaseManifest it was resolved from (Chapter 27). Every AgentStepRequest (Chapter 3) and every ContextManifest (Chapter 6) references it. It never changes; a run that needs different versions is a new run or an explicit migration (Chapter 15)."
     - In the JSON: add `"runtime": {"adapter": "...", "sdk": "openai-agents@..."}` and `"release_manifest": "sha256:..."`; rename `authority_envelope` → `capability_envelope`; replace `"risk_tier": "high"` with the book-wide named tier (T11 decision).
     - Use one identifier set shared with Ch 03 (T16). Ch 03 drops `context_manifest` from its RunManifest table (Ch 03 review).
   - *Related:* map T6, T7, T11, T16; C04-R10.

8. **C04-R08 — Medium — Merge / Move.**
   - *Location:* `:89` and `:159–170` (§ Run API); `04-part-iv.md:1208–1218`.
   - *Issue:* two Run API tables with drifted rows.
   - *Why:* readers cannot tell which surface is the contract.
   - *Change:* **Reconciled (see overall-book-review.md §D-03):** Ch 04 owns the one base Run API table. Keep POST /v1/runs (absorbing Ch 15's "returns 202, run ID, home region, pinned RunManifest, and status URL"), GET /v1/runs/{id}, GET /v1/runs/{id}/events, `:signal`, `:cancel`, `:update`, and `:fork`. Keep `:update`, because Ch 14's intervention "correct state" response uses it (C14-R02), and keep `:fork`, because Ch 24 owns its diagnostic semantics and points here (C24-R01, C24-R07); Ch 25's `:forkReplay` is deleted. Delete only GET /v1/runs/{id}/audit (trace: Chapter 24; evidence package: Chapter 26). Closing sentence: "Chapter 15 adds the durable-execution operations (events:ingest, :pause, :resume, :migrate) and the durable semantics of :signal and :cancel; Chapter 24 explains diagnostic replay and fork." Ch 15 does not add `:update`. Move the `:89` paragraph as stated. The items below are superseded where they conflict:
     - Move the `:89` paragraph under § Run API as its lead.
     - Keep only the public client surface: POST /v1/runs, GET /v1/runs/{id}, GET /v1/runs/{id}/events, `:signal`, `:cancel`.
     - Delete the `:update`, `:fork`, and `/audit` rows and add "Chapter 15 defines the full operational surface (update, pause, resume, migrate, event ingest); Chapter 24 owns replay and fork."
     - The Ch 15 review adds `:update` to Ch 15's table. The Ch 24/25 reviews settle one name for fork.
   - *Related:* map §5.2 API collisions.

9. **C04-R09 — Medium — Rewrite / Move.**
   - *Location:* `:75` (evidence box); `:206–226` (§ Event contract); `:258–303` (§ CloudEvents and outbox contracts).
   - *Issue:* two drifting envelope shapes, no prose, the evidence box stranded, OutboxRecord duplicating Ch 22.
   - *Why:* the envelope is canonical here and re-listed in Ch 15, so it must be one shape.
   - *Change:*
     - Move the `:75` evidence box to the top of § Event contract.
     - Add two sentences: "Events record facts that already happened (`run.status.changed`); commands go through the Run API and carry an expected state version. Payloads travel by `dataref` and `datahash`, never embedded."
     - Keep one envelope shape: the JSON's fields, with `correlation_id`, `causation_id`, `dataref`, and `datahash`, and `data` optional.
     - Delete OutboxRecord and replace it with "Producers publish through a transactional outbox and consumers deduplicate on (source, id); Chapter 22 defines both records."
     - The Ch 15 review replaces Ch 15 `:1198`'s field list with a pointer here and to Ch 22.
   - *Related:* C04-R10; map §4 row 59.

10. **C04-R10 — Medium — Move.**
    - *Location:* `:174–196`, `:208–226`, `:260–303`, `:254–256`; `examples/contracts.py`; `config/examples.json`.
    - *Issue:* the inline JSON and Python violate the `AGENTS.md` code policy, and `[[EXAMPLE:contracts]]` shows Ch 03/12 contracts instead of Ch 04's.
    - *Why:* "A sensible place to start" should run the chapter's own contracts.
    - *Change:*
      - Add a `platform` region to `examples/contracts.py` containing RunManifest, ArtifactRef, and CloudEvent (the single shape from C04-R09), with tests.
      - Change `:256` to `[[EXAMPLE:contracts#platform]]` and title the H3 "Run, artifact, and event contracts".
      - Show the RunManifest and event shapes through that example and remove the inline listings.
      - Keep AgentStepRequest/Result in the `step` region (Ch 01 already cites it). If Ch 04 shows them, it cites `#step` with the C04-R02 sentence.
      - Do not cite PlanNode/CandidatePlan from Ch 04.
    - *Related:* C04-R07, C04-R09.

11. **C04-R11 — Medium — Rewrite.**
    - *Location:* `:46–57` (§ End-to-end responsibility flow); `assets/diagrams/src/request-sequence.mmd`.
    - *Issue:* the steps lack owning planes; eligibility is ordered after the proposal; there is a fourth terminal vocabulary; the figure has the agent fetch its own context.
    - *Why:* this flow is Ch 04's unique contribution only if it shows who owns each step.
    - *Change:*
      - Convert the eight steps into a table, Step | Owning plane | Record produced | Developed in. For example: 2 → Runtime and workflow → RunManifest → Ch 04; 3 → Knowledge, context, and memory → ContextManifest → Ch 06; 6 → Gateways and integration → EffectRecord → Ch 22.
      - Rewrite step 3 as "Resolve eligible tools and models and build an authorized ContextManifest into the AgentStepRequest". Rewrite step 4 as "The model proposes a typed decision inside that bound". Rewrite step 5 as "Policy authorizes the exact proposed action; protected changes bind to an expiring human authorization".
      - Step 7: use the run-terminal vocabulary chosen for Ch 15 (T12) and point there.
      - In Figure 4-2, insert a Context Service participant: Run → Context Service ("assemble authorized context") → Run (manifest id) **before** "bounded step". Remove Agent → Pol "resolve authorized context". Add an optional approval hop between authorize and invoke.
    - *Related:* Ch 03 review (trim § The complete execution path to a pointer); Ch 15 review; Ch 20 review (Figure 20-3).

12. **C04-R12 — Medium — Rewrite / Move.**
    - *Location:* `:81–87`, `:95`, `:26`, Q2 (`:333`), Q4 (`:335`), Q5 (`:336`).
    - *Issue:* the headline design choice (cells) is unexplained, touched five times, and uses a third meaning of "plane".
    - *Why:* the reader is asked to accept a deployment model without its reasoning.
    - *Change:*
      - Under a new H2, § Global control and regional cells, write one paragraph: global services publish signed, immutable definitions (AgentSpec, policy bundles, ReleaseManifests); each run has a home cell holding its workflow, queues, context services, gateways, effect ledger, artifacts, and telemetry; cells bound residency and blast radius; a cell continues pinned in-flight work but fails closed on high-risk admission when it cannot verify freshness (operations in Chapter 27). Follow it with the `:95` scale sentences.
      - Rename "global definition and governance plane" and "global control plane" to **global control tier** here and in the state-owner table (`:26`). If the synthesizer keeps "control plane" as the industry term, define it here once as the deployment-only exception.
      - Keep Q2 and fold Q4 into Q2's answer. Move Q5 to Ch 27, and the Ch 27 review drops its duplicate Q at `08-part-viii.md:455`.
      - Add "(Chapter 27)" to verify item 4 (`:319`).
    - *Related:* map T2; Ch 27 review.

13. **C04-R13 — Medium — Add.**
    - *Location:* `:230–240` (§ Where each kind of state belongs).
    - *Issue:* there is no physical home for conversation turns or governed memory, which Ch 06 introduces.
    - *Why:* the store table must cover every authoritative record if it is to stay canonical.
    - *Change:* add one row: "Conversation and memory stores | Conversation turns (append-only); approved cross-run MemoryRecords | Tenant+subject partitioning, write policy, TTL, deletion tombstones (Chapter 6)". Keep the table canonical here (see the disagreement with the map above). Ch 06 then points to this table (C06-R03).
    - *Related:* C06-R03.

14. **C04-R14 — Low — Cross-reference.**
    - *Location:* `:146–155` (§ Trust boundaries).
    - *Issue:* the controls name later mechanisms with no pointers.
    - *Change:* add a fourth column, "Developed in": User/tenant → Ch 21; Knowledge → model → Ch 06; Model → orchestrator → Ch 02; Orchestrator → tool → Ch 21/22; Agent → agent → Ch 18/19; Sandbox → network → Ch 23; Platform → model vendor → Ch 19; Result → destination → Ch 14/22. The Ch 20 review makes § Follow the request across each trust boundary cite this table.
    - *Related:* map §4 row 21.

15. **C04-R15 — Low — Rewrite.**
    - *Location:* `:22`, `:87`, `:137` ("model gateway"); `:55` ("tool façade").
    - *Change:* "LLM Gateway" everywhere, and "Tool Gateway façade" at `:55`, matching Figure 4-1 and Ch 01 (T4).

16. **C04-R16 — Low — Rewrite.**
    - *Location:* `:325–326` (§ Put the idea to work); `:332`, `:334` (Q1, Q3).
    - *Issue:* the exercise asks for contracts taught later; Q1 and Q3 are recall lists.
    - *Change:*
      - Exercise 1 becomes "For one workflow you own, assign each record in the authoritative-records table to one plane and one writer; mark any record with two writers."
      - Q1 becomes "Which plane owns the run's terminal outcome, and why can the LLM Gateway not own it even though every call passes through it?" (strong answer: Runtime and workflow; path position ≠ authority).
      - Q3 becomes "Which trust boundary does indirect prompt injection cross, and which control there does not depend on detection?" (answer: knowledge → model; ACL before retrieval and instruction/data labeling, Chapter 6).

17. **C04-R17 — Low — Rewrite.**
    - *Location:* `:63`, `:66`, `:67` (§ Where truth lives).
    - *Change:* use the canonical component names, "Run Service", "Effect Service (Chapter 22)", and the human-authorization service name chosen under T3/T25 (Ch 14). Apply the same to `:135`. [verified: overall-book-review.md §D-22 settles the name as "Approval Service", with records ApprovalRequest / ApprovalDecision; Ch 14 currently says "Human Action Authorization Service" at `04-part-iv.md:884`]

18. **C04-R18 — Low — Rewrite.**
    - *Location:* `:340` (§ Where this leads next).
    - *Change:* "The reference architecture names a knowledge, context, and memory plane but not what fills it; Chapter 5 fills its knowledge half—the governed artifacts agents retrieve, reason over, are constrained by, and act through—and Chapter 6 its per-run context and memory."
    - *Related:* C04-R01, C05-R13.

19. **C04-R19 — High — Add (moved content).** *Added in reconciliation (see overall-book-review.md §D-08).*
   - **Location:** § From planes to deployable layers (C04-R05 order), directly after the layer table; source `05-part-v.md:554`, `:569–581`, `:593`.
   - **Issue:** C19-R01(b) moves the LLM Gateway contract into Ch 04, but no Ch 04 item received it.
   - **Change:** Add "### What the LLM Gateway enforces" in the Model access layer (Gateways and integration plane). Contents: the Ch 19 scope paragraph, keeping "It does not own business workflow, tool effects, agent delegation, or the external API perimeter"; the capability table, with the Caching row's control "Key every security and semantic dependency (Chapter 21)"; the latency sentence. Add one line: "It applies deterministic eligibility before any optimization; Chapter 28 treats routing as a cost decision." This resolves the Ch 01, 03, and 07 forward references to the LLM Gateway. Apply with C04-R15 ("model gateway" → "LLM Gateway").
   - **Related:** C19-R01, C04-R15, C28-R07, C07-R01.

20. **C04-R20 — Medium — Add / Rewrite.** *Added in reconciliation (see overall-book-review.md §D-27).*
   - **Location:** RunManifest (shown through the `platform` example region, C04-R10); layer table `02-part-ii.md:134` ("prompt/skill catalog").
   - **Issue:** The Ch 08 and Ch 09 reviews ask Ch 04 to record Skill and pack pins and to stop conflating prompts with Skills; no Ch 04 item did.
   - **Change:** Add `"skills": ["mortgage.evidence.read@0.1.0#sha256:…"]` and `"skill_pack": "mortgage-evidence@…#sha256:…"` to the RunManifest. At `:134`, replace "prompt/skill catalog" with "prompt bundle registry and Skill Registry (Chapter 8)" (in the layer C04-R01 renames "Agent registry and release").
   - **Related:** C08-R02, C08-R03, C09-R02(d), C09-R10, C04-R07, C27-R15.

## Verification log

Second pass against `source/parts/02-part-ii.md:1–340`, `01-part-i.md`, `03-part-iii.md`, `04-part-iv.md`, `05-part-v.md`, `06-part-vi.md`, `07-part-vii.md`, `08-part-viii.md`, `09-appendices.md`, `assets/diagrams/src/{reference-architecture.gv,request-sequence.mmd,system-overview.gv,guardrail-sequence.mmd}`, `examples/contracts.py`, `config/examples.json`, and overall-book-review.md §12.

**Line references:** 112 checked; 0 off by more than 3 lines; 0 renumbered. All quotations checked verbatim (`:22`, `:34`, `:53`, `:56`, `:89`, `:93`, `:101–107`, `:200`, `:204`, `:340`, `01-part-i.md:510`, `:1312`, `05-part-v.md:554`).

**Claims removed:** none.

**Claims softened (7):**

- "sixth meaning of plane" → third sense (ownership plane, layer-called-plane, deployment tier); two places.
- "five examples that match none of the seven plane names" → only "operations" echoes one.
- Figure 4-2 "shows no approval hop" → no *human*-approval hop; the policy hop exists (`request-sequence.mmd:20–21`).
- Effect receipt "contradicts itself" → blurs receipt and effect state; the two sentences are compatible.
- Event Python `data: dict` "contradicts" the by-reference rule → diverges from it; the rule is stated for large payloads.
- Ch 01 `:594` "points readers here" → an exercise this table serves; it does not name Ch 04.
- Figure 4-2 vs Figure 20-3 "near-identical" → overlapping tail only; different participants and opening.

**Claims corrected (4):** records in the plane table ~12 → 18; "EvaluationReport is an orphan" → also at `03-part-iii.md:299`, never defined; "R03 cited only in the evidence box" → also at `:250`; C04-R04 ChangeBundle "Ch 27/25" → Ch 27 (D-05).

**Important claims confirmed:**

- Ch 04 prose never names AgentRuntime, AgentStepRequest, or AgentStepResult (grep of `:9–340`; only "bounded agent workers" at `:87` and the "Agent Runtime" participant in `request-sequence.mmd:8`).
- No Figure 1-3 band name (`system-overview.gv`) survives unchanged in Figure 4-1 (`reference-architecture.gv:49–134`); Ch 01 `:510` claims "this same picture at higher resolution".
- Two empty H2 wrappers at `:97` and `:157`; `:104` "the plane table above" is 68 lines after `:36`; Run API paragraph `:89` is 70 lines before the table at `:159`.
- Figure 4-2 has the Agent Runtime resolve context from Policy & Identity *after* "bounded step" (`request-sequence.mmd:15–17`), against Ch 03 `01-part-i.md:1043` (AgentStepRequest already carries the authorized ContextManifest) and Ch 06 `:656–658`.
- Run API drift is exact: Ch 04 alone has `:update`, `:fork`, `/audit`; Ch 15 (`04-part-iv.md:1208–1218`) alone has `events:ingest`, `:pause`, `:resume`, `:migrate`, `/history`; `:forkReplay` is at `07-part-vii.md:366` (Ch 25).
- Ch 03's RunManifest table (`01-part-i.md:1225–1232`) pins `sdk` and `context_manifest`; the Ch 04 JSON has neither, and the identifiers differ (`reasoning-standard@18` vs `@4`; `enterprise-agent@2026.09.3` vs `mortgage-policy@2026.09`).
- Ch 22 has nine effect states (`06-part-vi.md:669`) and separates the receipt (`:671`) from the EffectRecord (`:769`, `:870`); OutboxRecord/InboxReceipt are Ch 22 records (`:871–872`).
- The event JSON (`:210–225`) has `correlation_id`, `causation_id`, `dataref`, `datahash`; the Python at `:270–283` has none and requires `data`.
- Ch 20 § Follow the request across each trust boundary (`06-part-vi.md:85–107`) cites no chapter.
- `examples/contracts.py` holds EvidenceRef, ToolCall, AgentDecision, AgentStepRequest/Result (region `step`, cited by Ch 01 at `01-part-i.md:572`), SkillRequirement, PlanNode, CandidatePlan; its docstring calls this "the full platform set" chapter 04 needs and `config/examples.json` registers it for chapters [1, 4]. ToolCall (`:42`) is the only overlap with the chapter's records; none of the chapter's own contracts (RunManifest, Artifact, receipt, event) is in it. This strengthens C04-R10.
- Ch 27 uses "regional execution planes" (`08-part-viii.md:186`, `:455`), so the C04-R01 note to Ch 27 is needed. Ch 27 `:195` explains continue-on-last-known-good; Ch 27 Q at `:455` duplicates Ch 04 Q2.
- RunManifest / "run manifest" appears in Ch 01, 03, 04, 05, 09, 15, 24, 27 and Appendices B, C: "8+ chapters" holds.
- Ch 06 introduces the conversation store (`:683`) and governed memory service (`:687`); the Ch 04 store table has no row for either.
- "Model gateway" at `:22`, `:87`, `:137`; "LLM Gateway" in `reference-architecture.gv:114`, Ch 01 and Ch 19.

**Recommendations amended:** C04-R04 (ChangeBundle owner → Ch 27; D-22 names noted); C04-R17 (D-22 settles the service name). All other recommendations were checked against §12: C04-R05 (D-20), C04-R07 (D-02, D-27), C04-R08 (D-03), C04-R09 (D-16), C04-R12 (D-09, D-24), C04-R13 (D-15), C04-R19 (D-08), C04-R20 (D-27) are consistent; the Structural Recommendations' "From planes to deployable layers" rename matches D-32. No recommendation breaks the 8/28/12 topology, puts code inline (C04-R10 moves code out), hand-edits a rendered diagram, or widens a citation scope.

**Not verified:** map T11/T16/T23 and §4 row numbers (the concept map was not in scope); the C04-R14 "Developed in" chapter assignments are reasonable but were not traced to each chapter's section headings.
