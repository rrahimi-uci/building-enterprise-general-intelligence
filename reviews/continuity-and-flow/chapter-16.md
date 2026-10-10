# Chapter 16 — Choose Patterns That Fit Real Enterprise Work: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:1356–1497`. Context read: Part IV intro (`:1–7`), Ch 10–15 pattern cards and closings, Ch 15 close (`:1352–1354`), Ch 17 opening (`:1499–1544`), Appendix A (`09-appendices.md:8–35`), Figure 16-1 source (`assets/diagrams/src/pattern-decision-tree.gv`), the home chapters of each P-card (Ch 02, 03, 06, 07, 18, 21, 22, 24, 25–28) at the headings listed in the concept map.

## Overall Assessment

Ch 16 does not do the job its position requires. A reader finishing Ch 15 has just learned six loop and workflow patterns:

- bounded ReAct (Ch 10)
- routing and handoff (Ch 11)
- plan compilation (Ch 12)
- reflection and evaluator–optimizer (Ch 13)
- human authorization and intervention (Ch 14)
- durable execution (Ch 15)

The Part IV intro promises that the Part "ends with a catalog of patterns" (`:6`). What Ch 16 delivers is a *whole-book* catalog organized by platform concern. It is not a synthesis of Part IV:

- Of the twelve cards, only P-01 (Ch 10) corresponds to a Part IV chapter. P-02 and P-11 partly correspond to Ch 12 and Ch 15.
- Routing, plan compilation, critique, and human review have **no card**.
- P-06 to P-11 rest on mechanisms taught in Ch 18–28. Their "better design" lines are dense with terms the reader has met only as names in contract lists, never as mechanisms: "TaskEnvelope… deterministic join" (TaskEnvelope is listed in Ch 03 `01-part-i.md:1164` and Ch 04 `02-part-ii.md:93`; deterministic join first appears here), "capability lease… audience/purpose/resource/spend/time scope", "Prepared EffectRecord… unknown terminal" (EffectRecord is listed in Ch 03/04; the unknown state is previewed in Ch 04 `:204` and Ch 15 `:1253`), "ChangeBundle → risk → validation" (ChangeBundle is listed in Ch 04 `:44` and Ch 07 `03-part-iii.md:108`) (map §4 rows 40–45). [verified: softened — "terms the reader has not met" overstated it; three of the four records are named earlier but defined only in Ch 18/22/27]
- P-03, P-04, P-05, and P-12 summarize Part I–III chapters, so they are recaps, not Part IV content.

Figure 16-1 is the only element that matches its position. Its leaves are the Part IV patterns ("Deterministic workflow", "Bounded ReAct", "Plan–Execute", "Durable agent", "Human-in-the-loop"). But they **only partly match the cards below it**. "Bounded ReAct" is P-01's exact title and "Deterministic workflow" loosely matches P-02 "Deterministic spine with semantic nodes"; the other three leaves have no card ("Plan–Execute" and "Human-in-the-loop" have none, and "Durable agent" differs from P-11 "Durable runtime with backpressure"). The figure also omits routing and critique. [verified: corrected — the original "do not match" ignored the P-01 match]

Form problems:

- 12 single-child H2s.
- Each card's **When it helps** paragraph mostly holds the *tempting shortcut and why it fails*, not when the pattern helps.
- **A better design. A safer design looks like this:** doubles its own label.
- Identical stock phrasing throughout (map §5.1).
- There are no review sections.

Each pattern is now described four times: chapter prose, How-X card, P-card, Appendix A (map §5.2).

**Decision (with evidence below):** split the chapter.

- Keep a slim Ch 16 in place as the actual Part IV synthesis: choose among and compose the Ch 10–15 patterns.
- Move the twelve concern cards, corrected and tagged with the chapter that builds each one, into Appendix A, merged with Appendix A's existing list and pairing table.
- This keeps the 8 Parts / 28 chapters / 12 appendices topology (`AGENTS.md` § Structural invariants) and removes a whole layer of the four-fold repetition.

## Intended Reader Mental Model

After Ch 16 the reader should hold:

- **What.** The Part IV patterns are complementary tools, each protecting one obligation:
  - bounded discovery (ReAct)
  - correct ownership (routing and handoff)
  - an executable structure (plan compilation)
  - quality without self-certification (critique)
  - human authority and judgment (authorization and intervention)
  - survival over time (durable execution)
- **Why.** Choosing by fashion leaves the real failure exposed, and stacking every pattern adds ceremony and cost.
- **How.** Start from the obligation the system cannot violate, pick the smallest pattern that protects it, and know what it costs.
- **When.** There is a decision path (Figure 16-1), plus a signal for when *not* to use each pattern.
- **Relationships.** In one Harborlight run they compose. The durable workflow is the spine (Ch 15). Routing picks a worker (Ch 11). The plan compiler fixes the structure (Ch 12). Bounded ReAct activities gather evidence (Ch 10). Critique revises the explanation while acceptance decides (Ch 13). Protected effects wait for proposal-bound authorization, and escalations land in intervention (Ch 14). Parts V–VIII add the platform patterns that Appendix A catalogs.

Today the chapter delivers only "start from the obligation", plus a catalog the reader cannot yet fully read.

## Section-by-Section Flow Review

**H1 and opening (`:1356`).** There is no case box and no design choice, unlike every chapter from Ch 10 to Ch 15. For a synthesis chapter this is acceptable, but nothing ties it to the Harborlight thread until P-01.

**§ How to choose a pattern for the problem you actually have (`:1358`).** Role: framing ("the same words can describe very different obligations"). Adds: the obligation-first idea. Flow: fine. It is one of two framing H2s.

**§ How to use these patterns without turning them into recipes (`:1367`).** Role: second framing H2. Adds: "smallest pattern that protects that obligation", "combining every pattern produces ceremony". It is the chapter's best paragraph.
- *Issue:* its two examples come from Ch 22 and Ch 15. "An external write must be exactly-once from the business perspective" also conflicts in wording with Ch 22's "exactly once is the wrong cross-system assumption" (`06-part-vi.md:1011`).
- *Issue:* "Every card uses one review sequence" introduces cards whose labels do not match their contents.

**Figure 16-1 (`:1373`).** Role: the decision tree. It is right in kind, but:
- (a) it has no routing/handoff or critique leaf;
- (b) three of its five leaf names correspond to no card, and none carries a card ID or chapter number; [verified: corrected — "Bounded ReAct" is P-01's title]
- (c) the dashed "then" edge from q2 to q3 (`pattern-decision-tree.gv`) is unexplained in the prose.

**The twelve concern H2/H3 pairs.** Every H2 below wraps exactly one card:

- § Reasoning (`:1375`)
- § Orchestration (`:1385`)
- § Context engineering (`:1395`)
- § Memory (`:1405`)
- § Tools (`:1415`)
- § Multi-agent collaboration (`:1425`)
- § Security (`:1435`)
- § Reliability (`:1445`)
- § Observability (`:1455`)
- § Governance (`:1465`)
- § Operations (`:1475`)
- § System architecture (`:1485`)

That is twelve single-child H2s. The H2 layer adds only the category word, which Appendix A's table already carries. Card by card:

| Card | Built in | Readable at Ch 16? | Issues |
| --- | --- | --- | --- |
| ### P-01 — Bounded ReAct (`:1377`) | Ch 10 | Yes | Recap of Ch 10 § How ReAct works in practice. "Missing employment document" (§6 T15). |
| ### P-02 — Deterministic spine with semantic nodes (`:1387`) | Ch 12 (§ What should be agentic?), Ch 15 | Yes | Example "Onboarding always validates, screens, approves…" is the unlabeled supplier thread (§6 T17). |
| ### P-03 — Typed ContextManifest (`:1397`) | Ch 06 | Yes (recap) | Runtime flow "Planner → retrieval → policy → ranking/dedup → manifest → model" puts retrieval **before** policy, which contradicts Ch 06's "authorization precedes retrieval" (map §3, context-pipeline row). Off-thread example (contract review). |
| ### P-04 — Provenance-bound tiered memory (`:1407`) | Ch 06 | Yes (recap) | "working/episodic/semantic/profile" does not match Ch 06's taxonomy (conversation, knowledge, run-scoped working memory, governed long-term memory; `02-part-ii.md:686`, `:795`, `:940`) (§6 T18). [verified: softened — a different split, not a contradiction] |
| ### P-05 — Proposal–authorize–commit tool façade (`:1417`) | Ch 02, Ch 22 | Mostly | Fourth name for the six gates (§6 T14). "Grant" (§6 T6). |
| ### P-06 — Typed task ownership and join (`:1427`) | Ch 18 | **No** | TaskEnvelope is named in Ch 03/04 contract lists but defined only in Ch 18; deterministic join first appears here. Off-thread example (due diligence). [verified: corrected — TaskEnvelope is named earlier] |
| ### P-07 — Least-privilege capability envelope (`:1437`) | Ch 21 | **No** | "Capability lease" conflates envelope (scope) and credential lease (proof) (§6 T6). |
| ### P-08 — Effect ledger and reconciliation (`:1447`) | Ch 22 | Partly (previewed in Ch 03/15) | EffectRecord is named in Ch 03/04 and the unknown state previewed (Ch 04 `:204`, Ch 15 `:1253`), but the Reserved → Executing → Committed/Unknown lifecycle is defined only in Ch 22 `06-part-vi.md:669`. [verified: softened — "not yet defined" → named but not defined] |
| ### P-09 — Causal run graph (`:1457`) | Ch 24 | **No** | Trace-vocabulary drift (§6 T22). |
| ### P-10 — Risk-tiered evidence gates (`:1467`) | Ch 25–27 | **No** | ChangeBundle is named in Ch 04 `:44` and Ch 07 `:108` but defined in Ch 27 (D-05); use-case tiers come from Ch 26. "Risk classification" collides with R0–R4 (§6 T11). Off-thread example (hiring). [verified: corrected — ChangeBundle is named earlier] |
| ### P-11 — Durable runtime with backpressure (`:1477`) | Ch 15, Ch 28 | Partly | Permits, quotas, circuits, and degraded mode come from Ch 28/22. |
| ### P-12 — Portable contracts and adapters (`:1487`) | Ch 03, Ch 07 | Yes (recap) | — |

Card form, for every card: *When it helps* contains the shortcut and its failure, *A better design* repeats its label, and the stock phrases are identical across all twelve.

**§ Where this leads next (`:1495`).** "Pattern selection is easier when failure shapes are visible; Chapter 17 recasts recurring anti-patterns as measurable replacement decisions." Fine.

## Sparse or Underdeveloped Content

1. **Choosing among the Part IV patterns.** There is no side-by-side comparison of the six patterns the reader just learned. The pieces exist in each chapter's "Use when / Do not use when" and "Where it helps—and what it costs" tables. They need to be *consolidated*, not newly written (C16-R02).
2. **Composition.** Nowhere in Part IV does the reader see the patterns working together in one run. This is the single most useful thing a Part-closing chapter can add. Map it onto Ch 15 § Canonical control flow rather than writing a new walkthrough (C16-R03).

Nothing else should be expanded. The concern cards should shrink when they move.

## Missing Conceptual Connections

- **Ch 10–15 patterns → (missing: a comparison of the obligation each protects and when not to use it) → pattern choice.** Location: the new § Choose among the Part IV patterns.
- **Ch 15 § Canonical control flow → (missing: which pattern runs at which step in a Harborlight run) → composition.** Location: the new § How the patterns compose in one run. It depends on C15-R03 adding the step pointers. Ch 16 then refers to that list instead of repeating it.
- **Figure 16-1 leaves → (missing: chapter numbers) → the chapters.** Location: the figure.
- **Ch 16 → (missing: "Parts V–VIII add the platform patterns; Appendix A catalogs all twelve with the chapter that builds each") → Appendix A.** Location: the end of the slim chapter.
- **P-cards → (missing: "Built in Chapter N") → home chapters.** Location: Appendix A cards.

## Transition Problems

- **In (Ch 15 → 16, `:1354`).** "The core patterns are now defined" is false (C15-R11 replaces it).
- **Within.** There are two framing H2s. The figure has no lead-in explaining how to read it. The "Every card uses one review sequence" sentence sits between the framing and the figure, then twelve one-card H2s run with no connective prose.
- **Out (Ch 16 → 17, `:1497`).** Adequate. After the split it should still hand off to failure shapes, adding that Ch 17's cards point forward to Parts V–VIII.
- **Part IV intro (`:3–7`).** "It ends with a catalog of patterns and failure shapes" must change to match the split. Proposed wording is in C16-R06. Coordinate with the Ch 10 reviewer, who also owns the Part IV intro context.

## Redundant and Repetitive Concepts

- Two framing H2s that make one point (`:1358`, `:1367`).
- Stock phrases repeated twelve times: "The tempting shortcut is…", "That fails because…", "A safer design looks like this:", "The runtime flow is:", "The cost is real:".
- H2 category labels that duplicate the card titles and Appendix A's "Category" column.

## Cross-Chapter Duplication

| Other location | What repeats | Verdict |
| --- | --- | --- |
| Appendix A (`09-appendices.md:8–35`) | Same purpose ("Choosing the Right Pattern: A Decision Guide" vs "Choose Patterns That Fit…"). The obligation list (items 1–3 = Figure 16-1). The P↔AP table names the same 12 cards. | **Redundant.** Merge: the concern cards move into Appendix A (C16-R04). |
| How-X cards in Ch 02, 06, 10, 11, 12, 13, 14, 15, 18 | P-01/P-02/P-03/P-04/P-05/P-06/P-11 restate them | **Redundant** (third description). Removing the cards from Ch 16 takes out one of the four layers. The Appendix A copies are desk-aid reinforcement. |
| Ch 18 § Topology decision table (`05-part-v.md:61–72`) | Pattern selection for multi-agent topologies | Reinforcement (a different scope). Keep. Appendix A's P-06 card points to it. |
| Ch 06 § How context is assembled; § Memory is not a bag of embeddings | P-03 flow order; P-04 taxonomy | **Contradiction**, not duplication. Fix the card text to match Ch 06 when it moves. |
| Ch 02 § Six gates before anything changes | P-05 flow and name | Use "the six gates" by name. |
| Ch 21 § Records worth preserving and Q (`06-part-vi.md:625`) | P-07 "capability lease" | Use "capability envelope (scope) + credential lease (proof)". |

## Structural Recommendations

**The decision, and the options considered.**

| Option | Evidence for | Evidence against | Verdict |
| --- | --- | --- | --- |
| A. Move Ch 16 (and Ch 17) after Ch 28 as a closing review Part (map S1a) | All mechanisms are known by then | Breaks the 8-Part invariant, or forces Part VIII to absorb a catalog that does not fit "Running the System in the Real World". Renumbers 11 chapters, their figures, chapter covers, and the forward references at `01-part-i.md:477` and `02-part-ii.md:663`. Leaves Part IV with no synthesis. At the end the cards are pure recap. | Reject |
| B. Merge Ch 16 wholly into Appendix A, delete the chapter (map S1b) | Same purpose. Cards are appendix-shaped (single-H3 sections, no review sections, stock phrasing). | 28 → 27 chapters, renumbering Ch 17–28. Part IV loses its synthesis, and Figure 16-1 has no home. | Reject on cost. Part IV needs a synthesis. |
| C. Keep Ch 16 in place, rewrite the cards as forward-referenced previews | No topology change | A preview of a *solution* in compressed jargon teaches little (P-07, P-08). The catalog still omits Ch 11–14. Four-fold repetition remains. | Fallback only |
| **D. Split: slim Ch 16 = Part IV synthesis; concern cards → Appendix A** | Figure 16-1 already targets Part IV. The comparison and composition gaps are real. Appendix A already has the same purpose. Topology preserved. | Appendix A grows. Cross-references to "Chapter 16" for the P-cards must change (none exist outside Ch 15's closing, per grep of `source/parts/`). | **Recommend** |

**The slim Ch 16, in order:**

1. One framing H2: merge `:1358` and `:1367`.
2. Figure 16-1, revised.
3. § Choose among the Part IV patterns: one table.
4. § How the patterns compose in one run: one paragraph.
5. § The patterns the rest of the book adds: two sentences pointing to Appendix A.
6. § Where this leads next.

The target length is roughly a third of today's chapter. No template review sections are needed. If the synthesizer wants parity with other chapters, a three-row § Questions to bring to design review on composition is the only optional addition.

## Concrete Recommended Changes

1. **C16-R01 · Critical · Move/Rewrite (structural).**
   - **Location:** `04-part-iv.md:1375–1493`, all twelve § <category> / ### P-NN pairs.
   - **Issue:** The whole-book concern catalog sits at the end of Part IV. Half of it depends on Parts V–VIII, it omits Ch 11–14, and it duplicates the How-X cards and Appendix A.
   - **Why it matters:** The reader cannot use it at this point, and the Part's own patterns go unsynthesized.
   - **Change:** Delete the twelve H2/H3 pairs from Ch 16 and move the card content to Appendix A as specified in C16-R04. Keep the chapter title, or retitle it "Choose and Combine the Part IV Patterns" (the synthesizer decides; covers config `config/chapter-covers.json` must follow).
   - **Owner:** Ch 16 for the removal; Appendix A owner for the insertion, using C16-R04's spec.
   - **Related:** C15-R11, C16-R06.

2. **C16-R02 · High · Merge/Add (consolidation).**
   - **Location:** the new `## Choose among the Part IV patterns` after Figure 16-1.
   - **Issue:** There is no side-by-side comparison of Ch 10–15.
   - **Change:** One table, *Pattern (chapter) | Obligation it protects | Choose it when | Do not choose it when | What it costs*. Fill each row from the source chapter's existing "Use when / Do not use when" and "Where it helps—and what it costs" cells, paraphrased in one line and not pasted verbatim. Seven rows:
     - Bounded ReAct (10)
     - Routing (11)
     - Handoff (11)
     - Plan compilation (12)
     - Reflection / evaluator–optimizer (13)
     - Human authorization and intervention (14)
     - Durable execution (15)
   - Add one sentence above the table: "Start from the obligation, then take the smallest row that protects it."
   - **Related:** if the Ch 10–13 reviewer recommends removing the per-chapter How-X cards, this table becomes the only comparison. Keep it at one line per cell either way.

3. **C16-R03 · High · Add.**
   - **Location:** the new `## How the patterns compose in one run` after C16-R02's table.
   - **Issue:** Part IV never shows the patterns working together.
   - **Change:** One paragraph of 5–7 sentences on a Harborlight evidence-review run, referring to the step numbers in Ch 15 § Canonical control flow rather than restating them:
     - the durable workflow is the spine (Ch 15)
     - routing selects the evidence specialist from the eligible set (Ch 11)
     - the plan compiler validates and freezes the evidence plan (Ch 12)
     - bounded ReAct activities gather evidence inside each node (Ch 10)
     - an evaluator–optimizer revises the policy explanation while acceptance decides completion (Ch 13)
     - the document request waits for proposal-bound authorization, and any escalation from the earlier patterns lands in the intervention queue (Ch 14)
   - End with: "Each pattern owns one obligation; none of them owns the run."
   - **Related:** C15-R03 (the step pointers); C14-R02 (the intervention triggers).

4. **C16-R04 · High · Merge (spec for the Appendix A owner).**
   - **Location:** `09-appendices.md:8–35`, Appendix A.
   - **Issue:** Duplicate purpose. Pairings in the table are wrong.
   - **Change:** **Reconciled (see overall-book-review.md §D-02, §D-04, §D-21):** As stated, with four overrides. (b) P-10 "risk" → "change class × use-case tier (Chapter 26)". (b) P-02's example moves to Harborlight; the supplier thread is retired. (b) P-09's title becomes "Causal run trace" (T22). (a) P-06 is built in Ch 11 and Ch 18. Every card whose pattern already has a chapter "at a glance" card also follows C16-R10. Original text: Appendix A becomes:
     - (i) § Start with the outcome the system must protect: keep the 7-item list unchanged, and add a pointer that Figure 16-1 and Ch 16 cover the Part IV subset.
     - (ii) The new § Pattern cards: the twelve cards from Ch 16 as H3s under one H2, with no category H2s. Relabel the fields as **Use when** (the obligation), **Shortcut that fails** (shortcut plus why), **Better design** (design plus runtime flow plus example), **Watch and cost**, and **Built in**. Drop the stock phrases.
     - (iii) § Match the obligation to a pattern: keep the table and fix the pairings and chapter columns as in (b) and (c) below.
   - **(a) Built in, per card:**
     - P-01: Ch 10
     - P-02: Ch 12, 15
     - P-03: Ch 06
     - P-04: Ch 06
     - P-05: Ch 02, 22
     - P-06: Ch 18
     - P-07: Ch 21
     - P-08: Ch 22
     - P-09: Ch 24
     - P-10: Ch 25–27
     - P-11: Ch 15, 28
     - P-12: Ch 03, 07
   - **(b) Text fixes while moving:**
     - P-03 flow → "Planner → authorization → retrieval → ranking/dedup → manifest → model" (Ch 06 order).
     - P-04 → Ch 06's memory taxonomy.
     - P-05 title → "Tool façade behind the six gates", flow → "propose → validate → authorize → commit → verify → accept".
     - P-07 → "capability envelope (scope) and short-lived credential lease (proof)".
     - P-10 "risk" → "governance risk tier (Chapter 26)".
     - P-02 example → label "(supplier onboarding)", or switch to Harborlight per the §9 S13 decision.
     - P-01 → apply the §6 T15 document name.
   - **(c) Pairing table rows:**
     - P-01 ↔ AP-11
     - P-02 ↔ AP-01, AP-07
     - P-03 ↔ AP-02, AP-09
     - P-04 ↔ AP-13
     - P-05 ↔ AP-06, AP-12
     - P-06 ↔ AP-08
     - P-07 ↔ AP-03, AP-10
     - P-08 ↔ AP-04, AP-05
     - P-09 ↔ AP-14
     - P-10 ↔ AP-15, AP-16
     - P-11 ↔ AP-04 (amplification under load)
     - P-12 ↔ none (or AP-15 secondary)

     Today's table pairs AP-07 with Observability and AP-06 with Governance (`09-appendices.md:32–33`), which mis-files an acceptance anti-pattern and an approval anti-pattern. Replace "Primary chapters" with the Built-in chapters plus 17. The Tools row must include Ch 21.
   - Move Figure 16-1? **No.** It stays in Ch 16.
   - **Owner:** Appendix A reviewer implements. Ch 16 review supplies the spec.

5. **C16-R05 · Medium · Rewrite (figure).**
   - **Location:** Figure 16-1 (`assets/diagrams/src/pattern-decision-tree.gv`; caption at `:1373`).
   - **Issue:** There are no routing or critique leaves, three of the five leaf names match no card title and none names a chapter, and the dashed "then" edge is unexplained. [verified: corrected — "Bounded ReAct" matches P-01]
   - **Change:**
     - Add a decision "Several known specialists or paths?" leading to the leaf "Routing / handoff (Ch 11)".
     - Add a post-step check "Draft quality needs revision?" leading to "Evaluator–optimizer (Ch 13)".
     - Suffix every leaf with its chapter: "Deterministic workflow (Ch 12/15)", "Bounded ReAct (Ch 10)", "Plan compilation (Ch 12)" (rename from "Plan–Execute"), "Durable execution (Ch 15)", "Human authorization / intervention (Ch 14)".
     - Add a one-sentence lead-in before the figure: "Answer the questions in order; the dashed edge means every path then asks whether the work outlives one request."
     - Run `make diagrams` and update `config/diagrams.json` alt text.
   - **Owner:** Ch 16.

6. **C16-R06 · Medium · Rewrite (Part intro, cross-reference).**
   - **Location:** Part IV intro (`04-part-iv.md:3–7`).
   - **Issue:** It promises "a catalog of patterns and failure shapes" at the end of the Part.
   - **Change:** **Reconciled (see overall-book-review.md §D-28):** Apply the merged Part IV paragraph in overall-book-review.md §D-28, which carries this item's replacement last sentence; do not edit the paragraph separately from C10-R01. Original text: Replace the last sentence with: "It ends by comparing and combining these patterns, then naming the failure shapes they prevent—several of which are corrected by mechanisms Parts V–VIII build—so a design review can ask not only 'what could work?' but also 'how would this fail in production?'"
   - **Owner:** coordinate with the Ch 10 reviewer. One edit only.

7. **C16-R07 · Medium · Merge/Condense.**
   - **Location:** § How to choose a pattern for the problem you actually have (`:1358`) and § How to use these patterns without turning them into recipes (`:1367–1371`).
   - **Issue:** Two framing H2s, plus the "Every card uses one review sequence" sentence, which is obsolete once the cards move.
   - **Change:**
     - Keep the `:1358` heading.
     - Body: `:1360–1365` trimmed to two sentences, followed by `:1369`.
     - Change "an external write must be exactly-once from the business perspective" to "an external write must take effect once, even when the call is retried", to avoid contradicting Ch 22 `06-part-vi.md:1011`.
     - Delete the `:1367` heading and `:1371`.

8. **C16-R08 · Low · Add.**
   - **Location:** the new `## The patterns the rest of the book adds`, before § Where this leads next.
   - **Change:** **Reconciled (see overall-book-review.md §D-04):** As stated, but write "causal run traces (Chapter 24)" instead of "causal run graphs" (T22), and add: "The Part IV patterns keep their at-a-glance cards in Chapters 10–15; Appendix A indexes them." Original text: Two sentences: "Parts V–VIII add the platform patterns these loops rely on: typed task ownership (Chapter 18), capability envelopes (Chapter 21), effect reconciliation (Chapter 22), causal run graphs (Chapter 24), risk-tiered release gates (Chapters 25–27), and admission with backpressure (Chapter 28). Appendix A catalogs all twelve platform patterns with the chapter that builds each."

9. **C16-R09 · Low · Rewrite.**
   - **Location:** § Where this leads next (`:1497`).
   - **Change:** "Choosing well is easier when failure shapes are visible; Chapter 17 names sixteen of them, says which earlier chapter already prevents each one, and points forward to where Parts V–VIII build the rest."
   - **Related:** C17-R03.

10. **C16-R10 — High — Add (spec for the Appendix A owner and Ch 16).** *Added in reconciliation (see overall-book-review.md §D-04).*
   - **Location:** Appendix A (`09-appendices.md:8–35`) as rebuilt by C16-R04; Ch 16 § Choose among the Part IV patterns (C16-R02).
   - **Issue:** The Ch 10–13 review asked either for P-cards for routing, handoff, planning, and acceptance, or for the chapter cards to serve as the catalog. Moving the twelve P-cards to Appendix A without a rule keeps a second full description of every pattern that already has a chapter card.
   - **Change:** (a) Moved P-cards whose pattern has a chapter "at a glance" card keep **Use when**, **Shortcut that fails**, a one-sentence **Better design**, **Built in**, and "Card: Chapter N § <card title>"; they do not restate steps or failure tables. This applies to P-01 (Ch 10), P-03 and P-04 (Ch 06), P-05 (Ch 02), P-06 (Ch 18, Supervisor/Worker at a glance), and P-11 (Ch 15). (b) Add rows, not cards, to § Match the obligation to a pattern for the Part IV patterns without P-cards: Routing and handoff → Ch 11, AP-08, AP-12; Plan compilation → Ch 12, AP-11; Reflection, evaluator–optimizer, and acceptance → Ch 13, AP-07, AP-10; Approval and intervention → Ch 14, AP-06. (c) C16-R02's lead sentence cites Ch 12 § What should be agentic? as the selection rule behind the table. (d) The Option C fallback below does not apply; the split is adopted.
   - **Related:** C16-R02, C16-R04, C10-R11, C18-R02.

**Fallback if the synthesizer rejects the split (Option C).** *(Not applicable: the split is adopted; see overall-book-review.md §D-04.)* Keep the twelve cards in Ch 16 but:

- add the "Built in" line to each;
- apply C16-R04(b)'s text fixes and the field relabeling;
- delete the twelve category H2s;
- still add C16-R02 and C16-R03.

Then reduce Appendix A to the 7-item list plus the corrected pairing table with a pointer to Ch 16. Either way, apply C15-R11 and C16-R06.

## Verification log

Second-pass fact check against `source/parts/*.md`, `assets/diagrams/src/pattern-decision-tree.gv`, `config/examples.json`, and `config/chapter-covers.json`.

- **Line references checked / fixed:** 52 checked; 0 fixed. All twelve H2/H3 pairs (`:1375–1487`), the framing H2s (`:1358`, `:1367`), the figure marker (`:1373`), the Part IV intro (`:3–7`), Appendix A (`09-appendices.md:8–35`, pairings at `:32–33`), Ch 18's topology table (`05-part-v.md:61–72`), Ch 21's Q (`06-part-vi.md:625`), Ch 22's Q (`06-part-vi.md:1011`), and the Ch 01/Ch 06 forward references (`01-part-i.md:477`, `02-part-ii.md:663`) confirmed.
- **Claims removed:** none.
- **Claims softened:**
  - Figure 16-1 leaves "do not match the cards" / "do not correspond to any card ID" / "do not match any text" (three places): "Bounded ReAct" is P-01's exact title and "Deterministic workflow" loosely matches P-02; three leaves match nothing.
  - "terms the reader has not met": TaskEnvelope, EffectRecord, and ChangeBundle are named in Ch 03/04/07 contract lists before Ch 16; they are undefined, not unseen.
  - P-04 "contradicts Ch 06's taxonomy" → "does not match"; Ch 06 splits conversation / knowledge / working memory / long-term memory and never uses episodic/semantic/profile.
  - P-06, P-08, P-10 table cells: "undefined"/"not yet defined" → named earlier, defined later (sources given in each cell).
- **Important claims confirmed:**
  - `pattern-decision-tree.gv` leaves are exactly "Deterministic workflow", "Bounded ReAct", "Plan–Execute", "Durable agent", "Human-in-the-loop"; there is no routing or critique node; the q2 → q3 edge is `style=dashed, label=" then "` and the prose never explains it.
  - Twelve single-child H2s, each wrapping one P-card; no case box, design choice, or review sections in the chapter.
  - P-03's flow at `:1401` places retrieval before policy; Ch 06 states the opposite twice (`02-part-ii.md:149` "ACL filters before retrieval", Figure 6-1 caption `:619` "authorization precedes retrieval").
  - "Chapter 16" is cited by number only at `04-part-iv.md:1354`, so the split renames no inbound cross-reference.
  - Appendix A today pairs AP-07 with Observability (`:32`) and AP-06 with Governance (`:33`).
  - How-X cards exist in Ch 02 (`01-part-i.md:785`), Ch 06 (`02-part-ii.md:787`), Ch 10–15, and Ch 18 (two), as claimed.
  - "exactly-once from the business perspective" (`:1369`) vs Ch 22 Q1 (`06-part-vi.md:1011`): a wording clash only; Ch 22's answer itself targets "one idempotent logical business effect".
- **Recommendations amended:** none in substance. C16-R04's reconciled overrides match D-02, D-04, D-21; C16-R06 matches D-28; C16-R10 matches D-04. C16-R05's leaf-rename list stands (the softening does not change the fix).
- **Not verified:** the map §4/§5/§6 row identifiers and the "four descriptions per pattern" count were taken as given.
