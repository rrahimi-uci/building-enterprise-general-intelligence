# Chapter 06 — Build Context Without Losing the Plot: Continuity and Flow Review

Reviewed: `source/parts/02-part-ii.md:587–947`. For transitions and boundaries I also read:

- Ch 03 § The request is bounded before the model sees it and the RunManifest table (`01-part-i.md:1035–1053`, `:1225–1232`);
- Ch 04 § Where each kind of state belongs and § RunManifest (`02-part-ii.md:172–242`);
- all of Ch 05;
- the opening of Ch 07 (`03-part-iii.md:1–58`);
- Ch 15 § Durable state is more than chat history through § Records worth preserving (`04-part-iv.md:1142–1231`);
- P-03/P-04 (`04-part-iv.md:1397–1415`) and AP-02/AP-13 (`:1595`, `:1634`);
- Ch 19 artifact adoption (`05-part-v.md:438`, `:513`, `:696`);
- Ch 21 § Data-plane controls (`06-part-vi.md:429`);
- `assets/diagrams/src/context-pipeline.gv`.

## Overall Assessment

Ch 06 has the right ideas, and two of them are among the book's most important security claims:

- the prompt is a disposable, authorized projection;
- authorization precedes retrieval, and bytes materialize last.

The four-tier instruction hierarchy is also canonical and clear.

The chapter has, however, been assembled from at least three overlapping drafts, and the duplication is internal:

- **Two pipelines.** Ten stages at `:621–632` (evidence admission) and eight steps at `:694–701` (window composition), with different scopes and orders.
- **Three ContextManifest shapes:** the record table (`:729`), JSON (`:739–755`), and Python (`:855–862`). They use three trust-label vocabularies, and a fourth appears at `:700`.
- **Three state classifications:** "four kinds" (`:667`), an 8-row taxonomy (`:681–690`), and Q2's different "four" (`:940`).
- **Memory in five places:** `:661–663`, the taxonomy rows (`:686–687`), the APIs (`:717–720`), the consistency bullet (`:762`), and the How Memory card (`:787–829`). The card's first sentence (`:795`) restates `:663`'s obligation list in different words (the same seven items, plus "subject" and "retrieval authorization"). [verified: softened — was "almost word for word"; the lists match in content, not wording]

There are also two unexplained code listings (`:834–910`, one of which belongs to Ch 19) and a 7-row Required-analysis table that restates the surrounding prose with an off-thread claims-handling example.

The chapter's boundaries with Ch 04 (stores), Ch 05 (the Hub), Ch 03 (AgentStepRequest), and Ch 15 (durable state) are implicit. Consolidating them would make the chapter shorter and clearer, with nothing new to write.

## Intended Reader Mental Model

On arrival the reader knows three things from earlier chapters: the AgentStepRequest carries an "authorized ContextManifest" (Ch 03); the RunManifest pins knowledge snapshots and the store table separates stores (Ch 04); and governed knowledge comes with metadata and a Hub (Ch 05).

The reader should leave with:

- **What:** context is a per-step projection. It is assembled from separately owned sources (workflow state, conversation, enterprise knowledge, working memory, long-term memory) and recorded in a ContextManifest.
- **Why:** mixing sources makes authorization, deletion, freshness, and recovery ambiguous.
- **How:** one ordered pipeline (authorize before fetch; materialize last); one trust hierarchy covering every segment; governed memory writes; deletion propagation.
- **When:** remember only stable, governed facts.
- **Relationships:**
  - The ContextManifest is the record the Ch 03 AgentStepRequest references.
  - It references the Ch 04 RunManifest.
  - Knowledge arrives through the Ch 05 Hub.
  - Workflow state is the Ch 15 RunState, seen through a projection.
- **Practical application:** reconstruct any model call by reference, and delete a fact everywhere.

## Section-by-Section Flow Review

**Opening callouts (`:589–595`).** *Role:* NORTHSTAR box and design choice. *Verdict:* good. The design choice is the chapter's thesis. *Issues:* NORTHSTAR versus a case box (map T1/S12) is a book-wide decision and is not repeated here.

**§ Why context needs an architecture of its own (`:597–604`).** *Role:* intro. *Adds:* "the prompt is the model's working view, not the system's memory." *Verdict:* good. *Issues:* there is no bridge from Ch 05's closing ("how a single request gets exactly the knowledge it needs"), and no mention that this chapter defines the ContextManifest that Ch 03's AgentStepRequest already referenced (`01-part-i.md:1043`; map §4 row 12).

**§ What the model is allowed to see (`:606–611`).** *Role:* only the state-owner table, with two stray blank lines (`:607–608`). *Verdict:* an empty heading (map §5.1). *Issues:* the heading promises content it does not have. The table's "Context Service" conflicts with § Who should own each decision's "Context Assembler" (`:707`).

**§ How context is assembled (`:613–639`).** *Role:* the canonical 10-stage pipeline (Figure 6-1). *Adds:* ordering as a security property, and the two load-bearing ordering rules. *Verdict:* the chapter's best section; make it the only pipeline. *Issues:*

- The stages describe how *evidence sources* are admitted, but not which sections compose the window. Instructions, the workflow-state projection, the conversation window, and memory appear only in the second pipeline (`:694–698`).
- Stage 5 says "Label trust tier", but the tiers (`:647–652`) do not cover workflow state, conversation, or memory.
- Stage 8 allocates tokens after ranking, while `:771` says "Allocate a fixed context budget before retrieval". Both are true (caps are fixed first, allocation happens after ranking), but the text never says so.
- Stage 4 ("immutable snapshots") does not name its source: the RunManifest's `knowledge_snapshots` (Ch 04 `:190`).
- Stage 7's "source authority" does not point to Ch 05's governance metadata.

**§ The trust hierarchy of instructions (`:641–659`).** *Role:* four tiers; content cannot promote itself; eligibility is fixed before the step. *Verdict:* canonical and excellent (map §3). *Issues:*

- *Missing placement:* workflow-state projections, conversation history (including prior agent turns), and memories are not assigned to a tier. A reader cannot tell whether a remembered "preference" can direct behavior.
- Tier 2 (Skills) precedes Ch 08 with no pointer (map §4 row 23).

**§ Memory is not a bag of embeddings (`:661–663`).** *Role:* memory writes as governed data effects. *Adds:* the key invariant "canonical state wins". *Verdict:* the right content under the wrong parent. *Issues:*

- Memory writes are not a stage of context assembly, yet this H3 sits under § How context is assembled.
- Its obligation list is restated at `:795` (the card) and `:762`.
- Its pointer to AP-13 and AP-02 is good.

**§ Four kinds of state that should not be collapsed into one store (`:665–677`).** *Role:* separates workflow state, knowledge, memory, and context. *Verdict:* the central distinction, but the number does not hold. *Issues:*

- The heading says four. The table below has eight classes, and Q2 lists a different four (conversation, knowledge, working memory, long-term memory).
- "Context" is listed as a kind of *state*, but the paragraph rightly calls it a temporary projection, not stored state.
- The Required-analysis table (`:669–677`) restates the paragraph (Problem, Recommended architecture) and pre-states § Where it can fail (Failure scenarios). Its "claims handling" example is off-thread (map §5.1, S16). Its only unique content is the Design alternatives row.

**§ State taxonomy and storage (`:679–690`).** *Role:* eight information classes, each with a system of record and rules. *Verdict:* partly redundant with Ch 04 and Ch 15. *Issues:*

- "Durable execution state" (`:685`) is Ch 15's subject (`04-part-iv.md:1146`, `:1224–1230`).
- "Artifacts" (`:689`) restates Ch 04 § Artifact contract.
- "Telemetry and audit" (`:690`) restates Ch 04's trace and WORM rows (`:237–238`).
- The rows unique to Ch 06 are Conversation context, Short-term working memory, Long-term memory, and (from the context-facing angle) Workflow state and Enterprise knowledge.

**§ Context assembly pipeline (`:692–701`).** *Role:* the second pipeline. *Verdict:* **D**; merge it into § How context is assembled. *Issues:*

- Its unique content: section composition (steps 1–3, 5), a separate policy gate for memory (step 5), the segment-label vocabulary (step 7), and a manifest hash on the model span (step 8).
- Its order partly conflicts with the 10-stage pipeline: step 7 labels each segment after deduplication (step 6), while the 10-stage pipeline classifies and labels at stage 5, before deduplication at stage 6. [verified: removed — the claimed "dedup after retrieval" conflict is not one: both pipelines fetch first (stage 4 / steps 4–5) and deduplicate afterwards (stage 6 / step 6); the labeling order is the real difference]

**§ A workable implementation (`:703`) / § Who should own each decision (`:705–707`).** *Role:* seven owning services. *Verdict:* useful. *Issues:*

- "Context Assembler" versus "Context Service" (`:611`, Figure 4-1).
- The "Retrieval Broker" is never related to Ch 05's Enterprise Knowledge Hub ("They ask one service", `:526`).
- The "Provenance Service" overlaps the Hub's Governance view (`:530`).
- The rule "No component can silently promote a conversation statement into workflow truth or long-term memory" is excellent; keep it.

**§ The contracts between components (`:709–721`).** *Role:* nine APIs. *Verdict:* mostly sound. *Issues:*

- `GET /v1/runs/{run_id}/state` is a third run-read endpoint, beside Ch 04 `GET /v1/runs/{id}` and Ch 15's projection read (`04-part-iv.md:1211`).
- `POST /v1/knowledge:search` has no owner. Under C05-R02 it is the Hub's query surface.

**§ Records worth preserving (`:723–756`).** *Role:* seven entities plus an example manifest. *Verdict:* the canonical ContextManifest home (map §3), but it carries two of the three shapes. *Issues:*

- The record table (`:729–730`), the JSON (`:739–755`, with `kind`, `trust: "untrusted-content"`, `acl_decision_id`), and the Python at `:846–862` (`trust_role ∈ {instruction, user_intent, evidence}`, `release_id`, `omitted_candidate_ids`) disagree on fields.
- None of them references the RunManifest.
- None of them says whether there is one manifest per AgentStepRequest or one per model call. The table says "run/node/model call", yet a Ch 03 step runs up to `max_turns` model calls whose context grows with tool results.
- Ch 03's RunManifest table puts `context_manifest` in the *run* manifest (`01-part-i.md:1232`), which compounds the confusion.

**§ Retrieval and memory consistency (`:758–763`).** *Role:* four consistency bullets. *Verdict:* mixed ownership. *Issues:*

- Bullet 1 (index as disposable projection) is knowledge-plane content and moves to Ch 05 (C05-R08).
- Bullet 2 (search order) is fine.
- Bullet 3 (memory write as governed operation) belongs with memory.
- Bullet 4 (correction and deletion lineage) is Ch 06's to keep.

**§ Scalability and token economics (`:765–777`).** *Role:* seven scale bullets and the PERFORMANCE AND COST box. *Verdict:* mostly generic scale content (map §5.1 pattern). *Issues:*

- The ingestion bullet (`:769`) moves to Ch 05.
- The cache bullet (`:770`) is the first of four statements of authorization-scoped caching. Map: canonical in Ch 21; keep the bullet with a pointer.
- The budget bullet (`:771`) needs reconciling with stage 8.
- The PERFORMANCE box restates stages 9–10 ("record a context manifest identifier rather than the context body"). It is short; keep only its unique claim ("measure answer quality against context size").

**§ What the evidence lets us conclude (`:779–785`).** A privacy-lifecycle claim (R13, R39). *Verdict:* fine. *Issues:* it sits between the implementation and the memory card, splitting memory content from its own implementation.

**§ How Memory works in practice (`:787–829`) with § How the pattern works (`:793`), § Where it helps—and what it costs (`:807`), § Where it can fail—and how to contain it (`:814`), and § What you need to see in production (`:822`).** *Role:* the pattern card. *Adds:*

- the five-step lifecycle (`:797–801`), which is unique;
- Use when / Do not use when (`:805`), which is unique and valuable ("facts already authoritative elsewhere");
- the cost and failure rows, which overlap § Four kinds of state (Failure scenarios) and § Retrieval and memory consistency;
- the production telemetry bullets, which are unique.

*Verdict:* keep the card, but place it inside one memory section. *Issues:*

- `:795` restates `:663`.
- The card is separated from the memory prose by 125 lines.
- The working/long-term distinction is stated here, at `:686–687`, and at `:762`.
- The relation to Ch 04 § Where each kind of state belongs is absent: memory has no row there (C04-R13).
- The relation to Ch 15 durable state is absent. "Stale memory overrides state" is controlled by "canonical state precedence", and that canonical state is Ch 15's RunState and the domain system of record, which the card does not say.

**§ A sensible place to start (`:831`) / § Auditable context projection (`:834–863`) / § Cross-boundary artifact adoption policy (`:865–910`).** *Verdict:* two inline listings with no prose, against `AGENTS.md`. *Issues:*

- The first listing is the third ContextManifest shape.
- The second has no explanation anywhere in Ch 06 (map §4 row 24). Its concerns (tenant, region, data class, purpose, provenance digest, expiry for an artifact from another boundary) are Ch 19's: `adoptResult` (`05-part-v.md:513`) and Q "How should a remote artifact be adopted?" (`:696`).
- There are two stray blank lines at `:832–833`.

**§ If this fails in production (`:912–916`).** Three good checks, especially "reconstruct one ContextManifest without relying on logged plaintext". Keep.

**§ What to verify before production (`:918–928`).** Good. *Issues:* item 1 lists eight domains, a third enumeration. Align it with the source set (C06-R03) and say that artifacts, telemetry, and audit are Ch 04 stores.

**§ Put the idea to work (`:930–933`).** Good. Exercise 2 ties to the mortgage case. Keep.

**§ Questions to bring to design review (`:935–943`).** *Issues:*

- Q2's "four" contradicts the § Four kinds of state heading.
- Q4 introduces "taint", which the chapter never uses (taint lineage is Ch 23's term). Say "provenance and untrusted-content labels", or add "(Chapter 23)".

**§ Where this leads next (`:945–947`).** *Verdict:* adequate Part transition. *Issues:* Ch 07 immediately lists ContextManifest, MemoryRecord, TaskEnvelope, and others as the stable contracts teams build on (`03-part-iii.md:58`). The closing could name that hand-off: Part II's contracts become Part III's paved road.

## Sparse or Underdeveloped Content

- **ContextManifest granularity.** Per step versus per in-loop model call is undefined. One sentence is needed (C06-R02).
- **Trust placement of non-retrieved segments.** Workflow state, conversation, and memory need one sentence (C06-R05).
- **Two retrieval paths.** Pre-step assembly versus in-step read tools (Ch 03 `:1061`) is never stated (C06-R06).

Nothing else needs expanding. The chapter's problem is excess, not thinness.

## Missing Conceptual Connections

- **Ch 03 AgentStepRequest "authorized ContextManifest" → Ch 06 ContextManifest, missing "this is that record".** At `:599–604`.
- **Ch 04 RunManifest → ContextManifest, missing granularity and the reference.** At `:723–756`. One RunManifest per run (pinned versions, including `knowledge_snapshots`); one ContextManifest per AgentStepRequest, which references the RunManifest digest. Each in-loop model call appends tool-result segments as a manifest revision recorded on the model span.
- **Ch 05 Hub → Ch 06 Retrieval Broker, missing "the broker is the Hub's client".** At `:707` and `:716`.
- **Trust hierarchy → state, conversation, and memory segments, missing their tier.** At `:652–654`. They are data: workflow state is authoritative as fact, memory is advisory, and neither ever directs behavior.
- **Memory "canonical state wins" → Ch 15 RunState and the domain system of record, missing the name of what wins.** At `:663` and `:818`.
- **Stage 4 snapshots → Ch 04 RunManifest `knowledge_snapshots`.** At `:626`.
- **Stage 7 authority → Ch 05 governance metadata (owner, version, effective dates).** At `:629`.

## Transition Problems

- **In (Ch 05 → Ch 06).** Ch 05 closes on how a request gets "exactly the knowledge it needs". Ch 06 opens with NORTHSTAR and a generic intro that never mentions knowledge artifacts, the Hub, or Ch 03's ContextManifest. Fix with C06-R06.
- **Within the chapter.**
  - § How context is assembled → § The trust hierarchy → § Memory is not a bag of embeddings (an H3 that is not about assembly) → § Four kinds of state → its second pipeline. The reader leaves assembly, returns to it 30 lines later with a different order, then meets memory again 125 lines later in the card.
  - § What the evidence lets us conclude splits the implementation from the memory card.
  - § A sensible place to start contains a listing that belongs to another chapter.
- **Out (Ch 06 → Ch 07).** Adequate. See C06-R12.

## Redundant and Repetitive Concepts

| Repeated concept | Locations | Verdict |
| --- | --- | --- |
| Context pipeline | `:621–632` vs `:694–701` | D with partly conflicting order (labeling before vs after dedup) and different scope; merge into the first [verified: softened — see § Context assembly pipeline] |
| ContextManifest shape | `:729`, `:739–755`, `:855–862` | D with drift; one schema in `examples/` |
| Trust-label vocabulary | tiers 1–4 (`:647–652`); `instruction/user_input/enterprise_data/tool_result/memory` (`:700`); `"trust": "untrusted-content"` (`:749`); `trust_role` (`:851`) | D (map T19); one enum mapped to tiers |
| State classification | "four kinds" (`:667`); 8-row taxonomy (`:681–690`); Q2's four (`:940`); checklist's eight (`:920`) | D; one source set |
| Memory obligations | `:663`, `:795`, `:762`, `:717`, `:926` | `:663` + `:795` D; the API and checklist entries are R |
| "Reference, don't log plaintext" | `:637–639`, `:701`, `:768`, `:777`, `:914`, `:941` | Mostly reinforcement of one principle; drop `:701` (merged) and trim the `:777` box |
| Required-analysis table | `:669–677` vs § Four kinds paragraph and § Where it can fail | D; delete |
| Authorization before retrieval | `:625`, `:634–636`, `:697`, `:761`, `:819`, `:922` | R. The chapter's core safety claim, but `:697` goes with the merged pipeline |

## Cross-Chapter Duplication

| Ch 06 location | Other location | Verdict | Recommended owner |
| --- | --- | --- | --- |
| § State taxonomy and storage (`:679–690`) | Ch 04 § Where each kind of state belongs (`:228–242`) | Partial D, on different axes | **Disagreement with the map** (which makes Ch 06 canonical and has it absorb Ch 04's table). Ch 04 keeps the physical-store table; Ch 06 keeps only the context sources and points to Ch 04 for stores (C06-R03, C04-R13) |
| Workflow-state and durable-execution rows (`:684–685`); "canonical state wins" (`:663`) | Ch 15 § Durable state is more than chat history (`04-part-iv.md:1142–1148`), § Records worth preserving (`:1220–1231`) | D (Ch 15 owns the RunState) | Ch 15. Ch 06 owns only the RunStateProjection that context reads |
| `GET /v1/runs/{run_id}/state` (`:714`) | Ch 15 `GET /v1/runs/{run_id}` (`04-part-iv.md:1211`); Ch 04 `:164` | D | Ch 15. Ch 06 refers to "the run projection (Chapter 15)" |
| § Memory is not a bag of embeddings + § How Memory works in practice | P-04 (`04-part-iv.md:1413`, working/episodic/semantic/profile) [verified: corrected — was `:1407`, the "## Memory" heading; the taxonomy is at `:1413`]; AP-13; T-06; Appendix F #7 | P-04 taxonomy drift (map T18); AP-13 R | Ch 06's working/long-term taxonomy. The Ch 16 review aligns P-04 |
| § How context is assembled | P-03 runtime flow "retrieval → policy" (`04-part-iv.md:1401`) | Contradiction | Ch 06. The Ch 16 review fixes P-03 to authorize → retrieve |
| ContextManifest | AP-02 code `ContextManifest.project`; Ch 20 T-04; Ch 24; Appendix C | R once unified | Ch 06 (one schema) |
| Trust hierarchy | Ch 20 T-01/T-02 and § Worked example; Ch 23 threats row 1; Ch 03 protection-stack step 1 | R (threat view) | Ch 06 for the mechanism, Ch 20 for the threat |
| Cache bullet (`:770`) | Ch 19 Caching row; Ch 21 § Consistency and revocation policy; Ch 28 #6 | D (four statements) | Ch 21; Ch 06 keeps one line with a pointer |
| Ingestion and index bullets (`:760`, `:769`) | Ch 05 (absent there) | Misplaced | Ch 05 (C05-R08) |
| § Cross-boundary artifact adoption policy (`:865–910`) | Ch 18 rule 4 (`05-part-v.md:218`); Ch 19 `adoptResult` + Q (`:513`, `:696`) | Misplaced | Ch 19 (map S8 says "Ch 18/19"; I choose Ch 19 because the checks are cross-tenant, region, and provenance-trust, which are federated concerns) |
| Retrieval Broker / `knowledge:search` | Ch 05 § Reference architecture: the Enterprise Knowledge Hub | Unreconciled | Ch 05 owns the Hub; Ch 06 names the broker as its client |

## Structural Recommendations

Target order:

1. Opening callouts → § Why context needs an architecture of its own, with the state-owner table moved here and the empty § What the model is allowed to see deleted.
2. § Five sources, one disposable projection. This replaces § Four kinds of state: paragraph, trimmed taxonomy, no Required-analysis table.
3. § How context is assembled: one merged pipeline, then § The trust hierarchy of instructions as its H3, covering every segment kind.
4. § Memory is a governed write. The current H3 at `:661`, promoted to H2, absorbs `:762` and the How Memory card (keep the card's H3s as its sub-sections).
5. § A workable implementation: owners, contracts, records (one ContextManifest), deletion and consistency, and scale (trimmed).
6. § What the evidence lets us conclude → § A sensible place to start (one `[[EXAMPLE:context-manifest]]`) → the template sections.

## Concrete Recommended Changes

1. **C06-R01 — High — Merge.**
   - *Location:* `:692–701` (§ Context assembly pipeline) into `:613–639` (§ How context is assembled); `assets/diagrams/src/context-pipeline.gv` if the stage labels change.
   - *Issue:* two pipelines with different scopes and orders.
   - *Why:* the chapter says stage order is a security property, and then gives two orders.
   - *Change:*
     - Keep the 10-stage table. Add one sentence before it: "The pipeline admits five kinds of source—pinned instructions and policy constraints, the run's state projection, a minimal conversation window, enterprise knowledge, and memory—and each passes every stage."
     - Stage 2: "Choose candidate sources, including memory, which passes its own policy gate."
     - Stage 4: "Read immutable snapshots named in the RunManifest (Chapter 4)."
     - Stage 5: "Label each segment's kind and trust tier (see the hierarchy below)."
     - Stage 7: "…source authority and effective dates (Chapter 5)."
     - Stage 8: "Allocate tokens within per-section caps fixed before retrieval."
     - Stage 10: "…and record its hash on the model span."
     - Delete § Context assembly pipeline. Delete the budget bullet at `:771`, which is now stated in stage 8.
   - *Related:* C06-R05; the Ch 16 review (P-03 order).

2. **C06-R02 — High — Rewrite / Move.**
   - *Location:* `:729–730`, `:735–756`, `:834–863`; new `examples/context_manifest.py` registered in `config/examples.json` with a behavioural test.
   - *Issue:* three ContextManifest shapes; no RunManifest reference; undefined granularity.
   - *Why:* the ContextManifest is the chapter's central record and is reused in Ch 16, 17, 20, and 24.
   - *Change:*
     - Define one schema in the example with these fields: `context_id`, `run_id`, `run_manifest_digest`, `node_id`, `step_request_id`, `revision`, `policy_version`, `budget` (per-section caps and allocation), ordered `segments` (each with `segment_id`, `kind`, `trust_tier`, `source_uri`, `source_revision`, `sha256`, `authorization_decision_id`, `freshness`, `tokens`), `omitted_candidate_ids`, `redactions`, `manifest_sha256`, and `created_at`.
     - Keep the `:729–730` table rows as the field summary, aligned to the example. Delete the JSON (`:735–756`) and the Python (`:834–863`). Cite `[[EXAMPLE:context-manifest]]` under § A sensible place to start.
     - Add two sentences under § Records worth preserving: "There is one RunManifest per run and one ContextManifest per AgentStepRequest; the ContextManifest references the RunManifest digest. Tool results observed inside the step's loop are appended as tier-four segments in a new manifest revision recorded on each model span."
     - The Ch 03 review removes `context_manifest` from Ch 03's RunManifest table (`01-part-i.md:1232`) or relabels it as the step's ContextManifest.
   - *Related:* C04-R07, C04-R10, map T19.

3. **C06-R03 — High — Rewrite / Condense.**
   - *Location:* `:665–690` (§ Four kinds of state that should not be collapsed into one store; § State taxonomy and storage); `:920`; `:940`.
   - *Issue:* "four" contradicts the 8-row table and Q2; the table re-teaches Ch 04 stores and Ch 15 durable state; the Required-analysis table is redundant.
   - *Why:* readers need one stable set of sources, with ownership pointed to its true homes.
   - *Change:*
     - Retitle the H2 "Five sources, one disposable projection". Rewrite the paragraph: workflow state (what must happen next; canonical in the durable run, Chapter 15), conversation (interaction history), enterprise knowledge (governed facts and rules, Chapter 5), working memory (run-scoped hypotheses), and long-term memory (approved reusable facts). Context is the temporary projection of these for one step.
     - Trim the taxonomy table to those five rows. The Workflow state row's system of record becomes "durable run history (Chapter 15); context reads the RunStateProjection".
     - Delete the Durable execution state, Artifacts, and Telemetry and audit rows, and add one line: "Artifacts, telemetry, audit, secrets, and caches live in the stores of Chapter 4 § Where each kind of state belongs."
     - Delete the Required-analysis table (`:669–677`). If the author wants to keep its Design alternatives row, fold it into one sentence in the paragraph.
     - Q2 becomes "How do the five sources of context differ?" Checklist item 1 lists the five plus "and the Chapter 4 stores".
   - *Related:* C04-R13; map S8, S16.

4. **C06-R04 — High — Move / Merge.**
   - *Location:* `:661–663`, `:686–687`, `:762`, `:787–829`.
   - *Issue:* memory is spread across five places, nested under the assembly section, and duplicated.
   - *Why:* memory is the one *write* path in a read-oriented chapter, and readers need it in one place.
   - *Change:*
     - Promote § Memory is not a bag of embeddings to an H2 placed after the merged pipeline section.
     - Keep `:663` as its prose. Append the `:762` bullet's two unique clauses ("validate contradiction and sensitivity"; "derived guesses default to run-scoped working memory").
     - Move § How Memory works in practice with its four H3s directly beneath it, and drop the H2 wrapper and the THE ENGINEERING PROBLEM box. Its first sentence (`:795`) becomes "Working memory is run-scoped; long-term memory carries the obligations above."
     - In the § Where it can fail row "Stale memory overrides state", write "Canonical precedence: the run state (Chapter 15) and the domain system of record win; freshness checks."
     - Delete `:762`.
   - *Related:* map T18; Ch 16 review (P-04).

5. **C06-R05 — Medium — Rewrite.**
   - *Location:* `:647–659` (§ The trust hierarchy of instructions); stage 5.
   - *Issue:* four label vocabularies; workflow state, conversation, and memory have no tier.
   - *Why:* readers must be able to classify every segment the pipeline admits.
   - *Change:*
     - After the tier table, add: "Workflow-state projections, conversation history, and memories are tier-four data with different authority as facts: run state is canonical, conversation is a record of what was said, and memory is advisory. None of them can direct behavior."
     - Define one segment `kind` enum: `system_instruction` (tier 1), `skill_instruction` (tier 2), `user_request` (tier 3), and `run_state`, `conversation`, `enterprise_data`, `tool_result`, `memory` (tier 4). Use it in the example (C06-R02).
     - Add "(Chapter 8)" after "Skill instructions".

6. **C06-R06 — Medium — Add / Rewrite.**
   - *Location:* `:599–604` (intro); `:611`; `:707`; `:716`.
   - *Issue:* no bridges to Ch 03 or Ch 05; Context Service/Assembler naming; the broker is unrelated to the Hub; the two retrieval paths are unstated.
   - *Why:* the Part's three chapters should read as one plane.
   - *Change:*
     - Append to the intro: "Chapter 3's AgentStepRequest carries an authorized ContextManifest; this chapter defines how it is built and recorded. Knowledge arrives through the Enterprise Knowledge Hub of Chapter 5."
     - Use "Context Service" as the component (matching Figure 4-1) and describe "the Context Service's assembler" in `:707`.
     - Rename "Retrieval Broker" to "the Context Service's Hub client" or keep the name with "(the client of the Chapter 5 Hub)".
     - Mark `POST /v1/knowledge:search` as "the Hub's query surface (Chapter 5)".
     - Add one sentence at the end of § How context is assembled: "Retrieval can also happen inside a step, through a read-only tool behind the Tool Gateway (Chapter 3); it calls the same Hub, and its results enter the next model call as tier-four segments in a new manifest revision."
   - *Related:* C05-R02, C06-R02.

7. **C06-R07 — Medium — Move.**
   - *Location:* `:865–910` (§ Cross-boundary artifact adoption policy).
   - *Issue:* the code has no prose, and it belongs to federated adoption.
   - *Change:* move it to Ch 19 as an `examples/` file cited near `adoptResult` (`05-part-v.md:513`). The Ch 19 review owns placement. In Ch 06, add one sentence to § Five sources (C06-R03): "Artifacts produced by other agents or boundaries enter context only after adoption (Chapters 18–19)."
   - *Related:* map S8, §4 row 24.

8. **C06-R08 — Medium — Remove.**
   - *Location:* `:606–608` (§ What the model is allowed to see) and `:832–833`.
   - *Change:* delete the heading and the blank lines, and move the state-owner table to the end of § Why context needs an architecture of its own. Change its "Context Service; workflow remains canonical" only if C06-R06 renames the component.

9. **C06-R09 — Low — Cross-reference.**
   - *Location:* `:714`.
   - *Change:* replace the row with "GET /v1/runs/{run_id} (Chapter 15) — the canonical state projection and `state_version` that context reads; never the transcript." Alternatively, delete the row and mention it in § Who should own each decision.

10. **C06-R10 — Low — Move / Condense.**
    - *Location:* `:760`, `:769`, `:770`, `:777`.
    - *Change:*
      - Delete `:760` and `:769`, which move to Ch 05 (C05-R08).
      - At `:770`, append "(Chapter 21 owns authorization-scoped caching)".
      - Cut the PERFORMANCE AND COST box to its unique claim: "Measure answer quality against context size—most systems are past the point where more retrieval helps."

11. **C06-R11 — Low — Rewrite.**
    - *Location:* `:942` (Q4).
    - *Change:* replace "provenance and taint" with "provenance and untrusted-content labels", or add "(taint lineage, Chapter 23)".

12. **C06-R12 — Low — Rewrite.**
    - *Location:* `:947` (§ Where this leads next).
    - *Change:* "Context assembly completes Part II: every model call now has an owned plane, a pinned RunManifest, governed knowledge, and a recorded ContextManifest. Chapter 7 packages these contracts as a paved road so teams build on them rather than rebuilding them."

13. **C06-R13 — Low — Cross-reference.** This is owned by the Ch 16 review.
    - *Location:* P-04 (`04-part-iv.md:1411`) and P-03 (`:1401`).
    - *Change:* P-04 adopts Ch 06's working/long-term taxonomy and drops working/episodic/semantic/profile. P-03's flow becomes "authorize → retrieve pinned snapshots → rank/dedup → manifest → model". Ch 06 needs no change.

14. **C06-R14 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** End of § If this fails in production.
   - **Issue:** Same request as C05-R16.
   - **Change:** Add one line: "If the transcript is the state or memory is written by default, the repair is structural; see AP-02 and AP-13 in Chapter 17."
   - **Related:** C17-R03.

## Verification log

Second pass against `source/parts/02-part-ii.md:587–947`, `01-part-i.md`, `03-part-iii.md`, `04-part-iv.md`, `05-part-v.md`, `06-part-vi.md`, `07-part-vii.md`, `08-part-viii.md`, `09-appendices.md`, `assets/diagrams/src/context-pipeline.gv`, `examples/contracts.py`, and overall-book-review.md §12.

**Line references:** 118 checked; 1 off by more than 3 lines and renumbered (P-04 `04-part-iv.md:1407` → `:1413`). Quotations checked verbatim (`:599`, `:634–637`, `:663`, `:707`, `:777`, `:795`, `:805`, `:818`, `:914`, `:942`, `01-part-i.md:1043`, `04-part-iv.md:1401`).

**Claims removed (1):** "the second pipeline deduplicates after retrieval while the first fetches at stage 4 and deduplicates at stage 6" — both pipelines fetch first and deduplicate after; not a conflict.

**Claims softened (2):** the Memory card restates `:663` "almost word for word" → same obligations, different wording; "D with conflicting order" → partly conflicting (labeling order only).

**Important claims confirmed:**

- Two pipelines: ten stages at `:621–632` (Figure 6-1, `context-pipeline.gv:17–26` matches the stage labels) and eight steps at `:694–701`; the labeling order differs (stage 5 before dedup vs step 7 after).
- Three ContextManifest shapes (`:729`, `:739–755`, `:855–862`) with four trust-label vocabularies (`:647–652`, `:700`, `:749`, `:851`); none references the RunManifest; `:729` says "run/node/model call" while `AgentStepRequest.max_turns` (`examples/contracts.py:41`) allows up to 20 model calls per step.
- Heading "Four kinds" (`:665`) vs an 8-row taxonomy (`:683–690`), Q2's four (`:940`), and the checklist's eight (`:920`).
- Memory in five places (`:661–663`, `:686–687`, `:717–720`, `:762`, `:787–829`); the card is 124 lines after the prose.
- Stage 8 allocates tokens after ranking; `:771` says "Allocate a fixed context budget before retrieval".
- "Durable execution state" (`:685`) is Ch 15's (`04-part-iv.md:1146`, `:1224–1230`); Artifacts (`:689`) and Telemetry/audit (`:690`) restate Ch 04 (`:200`, `:237–238`).
- `GET /v1/runs/{run_id}/state` (`:714`) beside Ch 04 `GET /v1/runs/{id}` (`:164`) and Ch 15 `GET /v1/runs/{run_id}` (`04-part-iv.md:1211`).
- Ch 03's RunManifest table has `context_manifest` (`01-part-i.md:1232`); its AgentStepRequest table already says "Authorized ContextManifest" (`:1043`).
- P-03's flow is "Planner → retrieval → policy → ranking/dedup → manifest → model" (`04-part-iv.md:1401`), which contradicts stage 3 before stage 4; P-04 uses working/episodic/semantic/profile (`:1413`).
- The adoption listing (`:865–910`) matches Ch 19's `adoptResult` (`05-part-v.md:513`), its Q (`:696`), and Ch 18 rule 4 (`:218`); nothing in Ch 06 explains it.
- "taint" occurs in Ch 06 only at `:942`; TaintEdge and "tainted content" are Ch 23 (`06-part-vi.md:1135`, `:1270`).
- ContextManifest is reused in Ch 16 (P-03), Ch 17 (`04-part-iv.md:1601`, `:1619` `ContextManifest.project`), Ch 20 (five mentions incl. T-04), Ch 24 (lowercase, `07-part-vii.md:154`), and Appendices A, B, C, H, L.
- Ch 07 `03-part-iii.md:58` lists ContextManifest, MemoryRecord, TaskEnvelope, etc. as stable contracts; Ch 06 `:947` does not name the hand-off.
- Ch 21 § Data-plane controls (`06-part-vi.md:429–431`), Ch 19 Caching row (`05-part-v.md:577`), Ch 28 item 6 (`08-part-viii.md:578`), Appendix F #7 (`09-appendices.md:161`) all exist as cited.

**Recommendations amended:** none in substance. Checked against §12: C06-R02 (D-23(b): the Ch 06 JSON goes), C06-R03 (D-15 store table stays in Ch 04; D-30(a) deletes the Required-analysis table), C06-R04 (D-04 dissolves the Memory card into its H2), C06-R07 (D-18: Ch 19 canonical, code becomes a registered example), C06-R14 (D-29) are all consistent. C06-R01's stage-order rationale ("gives two orders") still holds on the labeling difference. C06-R06 asks for "Context Service", which matches Figure 4-1 (`reference-architecture.gv:102`) and Appendix C (`09-appendices.md:69`). No recommendation touches topology, keeps code inline (C06-R02 and C06-R07 move it to `examples/`), hand-edits a rendered diagram, or widens a citation scope.

**Not verified:** map §3/§4/§5 row numbers, T18/T19, and S8/S16; the Ch 16 and Ch 19 reviews' matching items (C06-R13, C06-R07's placement) were not read.
