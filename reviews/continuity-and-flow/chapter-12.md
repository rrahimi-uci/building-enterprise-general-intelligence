# Chapter 12 — Turn Proposed Plans into Safe, Executable Work: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:376–640`. Context read: Ch 11 close (`:372–374`), Ch 13 opening (`:642–678`), Ch 22 § Risk classes (`06-part-vi.md:714–722`), Ch 18 § Recommended orchestration rules and APIs (`05-part-v.md:74–110`), Ch 28 BudgetReservation (via map §5.2), Ch 16 P-02, Ch 17 AP-11, Appendix A, `examples/patterns/plan_compilation.py`, `examples/contracts.py` (`PlanNode.risk_class: int`), and `assets/diagrams/src/pattern-planning.gv`.

## Overall Assessment

The chapter is the strongest technical chapter of Ch 10–13. "Planning like compilation—not authorization" is a memorable, correct mental model, and the Plan IR, compile-time checks, and runtime revision algorithm give the reader real machinery. Its problems are about organization and dependencies, not ideas.

1. **Risk classes are used before they exist, in three incompatible representations.**
   - The Plan IR JSON says `"risk_class": "R1"` (`:465`).
   - The compile checks say "R4 commit remains a deterministic domain operation" (`:518`).
   - The registered compiler uses an integer 0–4 (`PlanNode.risk_class: int`, `PlanEnvelope.maximum_risk`).
   - Ch 11's router uses `risk: int`.
   - R0–R4 are defined only in Ch 22 § Risk classes (`06-part-vi.md:714`), ten chapters later, with no pointer.

   The sentence at `:518` is unreadable without knowing that R4 means "irreversible or privileged; agent may only propose" (map §4 row 33, **High**).
2. **The same compiler checks and replanning rules are stated five to seven times.**
   - Compiler checks: `:406`, `:410`, `:473`, Plan Compiler row `:484`, validate API `:494`, § Compile-time checks `:516–520`, card `:562`, checklist `:617`, Q3 `:634`.
   - Replanning: § Replanning contract `:416`, Recommended-architecture row `:425`, § Runtime revision algorithm `:524–530`, card step 5 `:568`, checklist `:619`, Q4 `:635`, and the ARCHITECTURE GUIDANCE box `:544`.
3. **The heading structure hides the chapter's spine.**
   - § From candidate plan to executable work (`:397`) is a heading whose only content is the state-owner table.
   - The Plan IR (the chapter's central artifact) is an H3 under "Planning, dynamic execution, and deterministic boundaries", after a Required-analysis table and a 12-row "What should be agentic?" table.
   - § Compile-time checks, the canonical list, is four H3s deep inside § A workable implementation, 45 lines after the IR it checks.
4. **Bridges to the rest of Part IV are missing.** Plan node kinds (`llm_activity | tool_activity | child_task | gate | wait | join`, `:460`) map exactly onto Ch 10/13, Ch 02/22, Ch 18, Ch 14, Ch 15, and Ch 18 again. That mapping would make Ch 12 the hub of Part IV, but the chapter never states it.

The "What should be agentic?" table is valuable and is reinforcement, not redundancy (agrees with map §3). It is misframed as a sub-point of planning when it is really the selection rule for every Part IV pattern.

## Intended Reader Mental Model

- **Before:**
  - Ch 10: a bounded loop for local uncertainty.
  - Ch 11: routing among known capabilities, with a capability envelope.
  - Ch 08: Skills resolve to pinned digests.
  - Ch 02: proposals are validated, then authorized, then committed.
- **After:**
  - (a) Use planning only when decomposition is genuinely unknown.
  - (b) A plan is typed data (Plan IR) that the model proposes and a deterministic compiler validates and binds.
  - (c) Compilation checks graph, types, authority subset, data-flow classification, effects, budgets, capacity, and terminal paths.
  - (d) A committed plan revision is immutable; replanning freezes committed facts and revises only the affected horizon.
  - (e) Compilation is not authorization; runtime checks still run at dispatch.
- **Missing pieces:**
  - (c) relies on risk classes and capability envelopes the reader has not met.
  - The reader is never told that plan nodes are the units the next three chapters (13–15) and Ch 18 execute.

## Section-by-Section Flow Review

**Evidence context / WHERE THE MORTGAGE CASE STANDS / THE DESIGN CHOICE (`:378–386`).**
- Good. The R27 evidence context ("adding complexity only when simpler compositions are insufficient") frames the chapter well.
- The case box (missing employment evidence, asset discrepancy, property check) is a standalone vignette, not a continuation of Ch 10–11's case (map S12). "Employment evidence" is the T15 drift.

**§ Why a plausible plan still needs to be compiled (`:388`).**
- *Role:* intro.
- *Adds:* "validate, authorize, compile, freeze".
- *Verdict:* adequate.
- *Issues:* it lists "authorize" as a compiler step, which slightly undercuts the heading at `:404` ("not authorization"). The intended meaning is "check the plan stays inside the run's authority", and the wording should say that.

**§ From candidate plan to executable work (`:397`).**
- *Role:* none beyond holding the state-owner table.
- *Verdict:* an empty heading (map §5.1). Remove the heading and move the table.

**§ Treat planning like compilation—not authorization (`:404`).**
- *Role:* the mechanism.
- *Adds:* the compiler analogy, Figure 12-1, what compilation binds (`:410`), resource feasibility (`:412`).
- *Verdict:* good and the right place for the mental model.
- *Issues:*
  - `:406` and `:410` each list compiler duties, and `:473` lists them a third time.
  - "Northstar Plan IR nodes" (`:410`) reaches for the IR before the reader has seen it (it appears at `:451`).
  - "emits a signed immutable plan revision" introduces signing without saying who signs or why. One clause would do: "signed by the compiler so the scheduler can verify it ran what was validated".

**§§ Replanning contract (`:414`).**
- *Role:* replanning invariants.
- *Adds:* immutable facts and the revision contents.
- *Verdict:* good, but it is separated from § Runtime revision algorithm (`:522`) by about 110 lines. The two describe one thing and should be merged.

**§ Planning, dynamic execution, and deterministic boundaries (`:418`).**
- *Role:* Required-analysis table.
- *Adds:*
  - Design alternatives (`:424`): eight alternatives, which is the only "spectrum" statement.
  - "models confuse a coherent narrative with a feasible, authorized execution graph" (`:423`): a strong line.
  - Trade-offs (`:426`).
- *Verdict:* most rows restate the prose.
  - "Recommended architecture" (`:425`) duplicates `:404–416`.
  - "Failure scenarios" (`:427`) duplicates the card's failure table, and "critic repeatedly rewrites a correct result" belongs to Ch 13.
  - "Enterprise example" (`:428`) is an off-thread incident agent (map §5.1).

**§§ What should be agentic? (`:430`).**
- *Role:* the work-type → mechanism rule.
- *Adds:* the book's clearest statement of what the model should and should not do, by work type.
- *Verdict:* high value.
- *Issues:*
  - It is placed as a sub-point of planning but applies to all of Part IV. The rows cover routing (Ch 11), evaluation (Ch 13), and retries/timers (Ch 15).
  - It does not connect to the Plan IR `kind` field, which is the same split expressed as data.
  - The map classifies it as reinforcement (R) of the Ch 01/02/03/04 ownership tables. I agree: it adds the work-type axis.

**§§ Plan IR (`:447`).**
- *Role:* the central artifact.
- *Adds:* the IR schema.
- *Verdict:* the most important thing in the chapter, but it is an H3 under the wrong H2.
- *Issues:*
  - `authority_envelope_id` is the T6 drift ("capability envelope").
  - `"risk_class": "R1"` is undefined.
  - `kind` values are not explained.
  - The paragraph after the JSON (`:473`) is a third compiler-duty list. Its unique items are unbounded loops, inconsistent data classification, and "a dynamic node may choose among an allowlisted capability set; it cannot call arbitrary network endpoints". They belong in § Compile-time checks.

**§ A workable implementation (`:475`) — §§ Who should own each decision (`:477`).**
- *Role:* components.
- *Adds:* seven components.
- *Verdict:* useful.
- *Issues:*
  - The Acceptance Engine row (`:487`, "policy-approved model graders") is Ch 13's subject and has no pointer to it.
  - Scheduler "workflow activities/child tasks" assumes Ch 15 (activities) and Ch 18 (child tasks).

**§§ The contracts between components (`:489`).**
- *Role:* API.
- *Adds:* the propose / validate / commit / revise / accept lifecycle.
- *Verdict:* coherent.
- *Issues:* `POST /v1/plans/{plan_id}:revise` collides with Ch 18's `POST /v1/runs/{run_id}/plans:revise` (`05-part-v.md:108`) (map §5.2). Ch 12 should be canonical.

**§§ Records worth preserving (`:501`).**
- *Role:* entities.
- *Verdict:* useful.
- *Issues:* `BudgetReservation` (`:510`) duplicates Ch 28's entity (map §5.2), and its canonical home is Ch 28. `ValidationFinding` is good and unique.

**§§ Compile-time checks (`:514`).**
- *Role:* the canonical check list.
- *Adds:* five precise rules, including "data-flow classification can stay equal or become more restrictive" (unique and important).
- *Verdict:* the best list in the chapter, placed too late.
- *Issues:*
  - "risk class" (`:516`) and "R4" (`:518`) are undefined.
  - "consent", "approval", and "compensation" are used before Ch 14 and Ch 22, with no pointers.
  - "Admission" (`:520`) is used before Ch 28.

**§§ Runtime revision algorithm (`:522`).**
- *Role:* replanning steps.
- *Verdict:* good and concrete. It should absorb § Replanning contract.
- *Issues:* step 6 ("new consent/approval if risk, purpose, destination, spend, or authority expands") is the hook to Ch 14, with no pointer.

**§§ Scalability and performance (`:532`).**
- *Role:* scale.
- *Verdict:* mixed.
  - Bullets 3, 6, and 7 are plan-specific and valuable (incremental validation; ready-node limits and expiring reservations; "invoke the planner only at entry, material uncertainty, or failure boundaries").
  - Bullets 1, 2, 4, and 5 are the generic scale bullets repeated across chapters (partition by tenant + run, cache by digest, no global table; map §5.1).
- *Issues:* bullet 7 is the real conceptual link to Ch 11 (route first, plan only when needed) and should be prose.

**ARCHITECTURE GUIDANCE box (`:542–544`).**
- *Verdict:* it restates `:406–416` ("a plan is data"). The only new idea is "human amendment" of a stored plan, which is unexplained. Remove the box, or reduce it to that one idea with a pointer to Ch 14.

**§ What the evidence lets us conclude (`:546`).**
- *Verdict:* generic EVIDENCE BOUNDARY box.
- *Issues:* R27 is already stated in the evidence context. R02 (durable execution) supports "the workflow schedules nodes" but no sentence is tied to it. R13 supports no claim.

**§ How Planning works in practice (`:554`) and H3s (`:560`, `:574`, `:581`, `:589`).**
- *THE ENGINEERING PROBLEM box:* restates `:390`.
- *How the pattern works:* the lead sentence restates `:406`/`:410`. The five steps restate compile + revision. There is nothing to move up, because the prose already has fuller lists.
- *Use when / Do not use when (`:572`):* useful. "high-risk paths that should be encoded as deterministic workflows" is the right "when not".
- *Costs:* useful ("Parallel execution | lower latency; higher resource use and conflict risk" is unique).
- *Failure table:* duplicates § Compile-time checks, but is acceptable as a scannable summary.
- *Signals:* useful and unique (critical path, replan diff).
- *Verdict:* this is the least necessary card in Ch 10–13. Its steps and lead add nothing; keep only Use/Avoid, costs, failure, and signals.

**§ A sensible place to start (`:598`) / §§ Plan IR compiler (`:601`).**
- *Verdict:* the example is good and directly teaches compile checks (capability allowlist, risk ceiling, unknown dependencies, cost reservation, cycle detection, digests).
- *Issues:*
  - The empty H2 wrapper and no lead-in.
  - The example title says "Compiling an *approved* plan" and its docstring says "provably the thing a reviewer saw". That implies human approval of plans, which the chapter treats only as a conditional (step 6). Reword it to "a validated plan".
  - It uses integer risk where the IR shows "R1".

**§ If this fails in production (`:605`).** Good and specific. Step 3 ("ensure committed facts did not change") tests the chapter's distinctive invariant.

**§ What to verify before production (`:611`).** Good. Item 1 ("used only for genuine semantic uncertainty") restates the opening; acceptable.

**§ Put the idea to work (`:623`).** Good. Exercise 2 ("passes schema validation but must fail authority validation") is the best exercise in Ch 10–13, because it tests Ch 02's validation ≠ authorization.

**§ Questions to bring to design review (`:628`).** Good. These are acceptable review reinforcement.

**§ Where this leads next (`:638`).** Good. It could add that compiled plans include `gate` and acceptance nodes, which Ch 13–14 define.

## Sparse or Underdeveloped Content

- **Risk classes.** These need a definition at first use (C12-R01). This is not optional: the compile-check rule at `:518` depends on it.
- **Node kinds.** `llm_activity | tool_activity | child_task | gate | wait | join` are listed once and never explained. A single sentence mapping each to its chapter fixes this and doubles as Part IV navigation (C12-R04).
- **"Compilation is not authorization."** The heading promises this distinction, but the body explains it in one clause ("Runtime checks still matter…", `:406`). One more sentence would make it concrete: a compiled plan proves that the steps are *within* the envelope; each dispatch still gets an exact authorization decision at the Tool Gateway (Chapter 2) against current resource versions. Add it; no further expansion.
- No other expansion is warranted. The chapter is already long.

## Missing Conceptual Connections

- **Ch 11 routing → Ch 12 planning, missing "route deterministically when a route exists; invoke the planner only at entry, material uncertainty, or failure."** This exists only as scale bullet 7 (`:540`). Location: `:390`.
- **Ch 22 risk classes → Ch 12 `risk_class`, missing a definition or pointer.** Location: `:465` / `:516`.
- **Ch 21 capability envelope → Ch 12 `authority_envelope_id` / "run's authority," missing the canonical name and pointer.** Location: `:406`, `:456`.
- **Ch 12 node kinds → Ch 10, 13, 14, 15, 18, missing the mapping.** Location: after the Plan IR JSON.
- **"What should be agentic?" → Plan IR `kind`, missing "the table's mechanism column is what the node kind encodes."** Location: `:430`/`:447`.
- **Ch 12 Acceptance Engine (`:487`) and `nodes:accept` (`:499`) → Ch 13, missing a pointer.** Ch 13 defines how acceptance uses deterministic checks before graders.
- **Ch 12 step 6 consent/approval → Ch 14, missing a pointer.** Location: `:529`.
- **Ch 12 BudgetReservation / admission → Ch 28, missing a pointer.** Location: `:510`, `:520`.
- **Ch 12 "loops require … no-progress detector" (`:519`) → Ch 10 no-progress signatures, missing a back-reference.** Location: `:519`. One clause, which also reinforces that the Ch 10 controller is reused inside plan loops.
- **Ch 12 delegation depth / fan-out bounds → AP-11, missing a pointer.** Location: `:519`.

## Transition Problems

- **In (Ch 11 → Ch 12):** Ch 11's closing ("tasks whose decomposition must itself be proposed") is good. But Ch 12's opening does not pick up routing, so the reader does not see that planning is the fallback when no stable route exists. Add the bridge at `:390` (C12-R07).
- **Within:**
  - The empty heading at `:397`.
  - The analysis table and agentic table sit between the mechanism and the IR.
  - § Replanning contract and § Runtime revision algorithm are 110 lines apart.
  - The ARCHITECTURE GUIDANCE box restates the opening after the implementation.
- **Out (Ch 12 → Ch 13):** "Planning creates an executable structure; Chapter 13 adds independent evaluation and bounded revision without self-certification." Adequate. It would be stronger if it said that every plan node ends in an acceptance check, and Chapter 13 defines what may decide it.

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict |
| --- | --- | --- |
| Compiler duties | `:406`; `:410`; `:473`; `:484`; `:494`; `:516–520`; card `:562`; Q3 `:634`; checklist `:617` | **Redundant.** Keep `:406` (one-sentence mental model) and § Compile-time checks (canonical). Merge `:473`'s unique items into Compile-time checks and delete `:473`. Trim `:410` to what compilation *binds* (Skill/tool release, critical path, signed revision) without re-listing checks. |
| Replanning freezes committed facts | `:416`; `:425`; `:524–530`; card `:568`; checklist `:619`; Q4 `:635` | Merge `:416` into § Runtime revision algorithm. The rest is acceptable. |
| A plan is data, separate from execution | `:392`; `:406`; ARCHITECTURE GUIDANCE `:544` | The box is redundant. |
| Use planning only for real uncertainty | `:390`; analysis row `:422`; card `:572`; checklist `:613`; Q1 `:632`; scale bullet `:540` | Acceptable. Promote `:540` into prose and drop it from scale. |
| Generic scale bullets | `:534`, `:535`, `:537`, `:538` | Book-wide boilerplate (map §5.1). Condense. |

## Cross-Chapter Duplication

| Concept | Here | Elsewhere | Verdict |
| --- | --- | --- | --- |
| Risk classes R0–R4 | `:465`, `:516`, `:518`; Ch 11 `risk: int`; `plan_compilation.py` | Ch 22 § Risk classes (`06-part-vi.md:714`), canonical; Ch 21 `:495` "(risk classes, Chapter 22)"; first book use of "risk class" is Ch 02 § Scaling the shell (`01-part-i.md:734`) | **Used before definition** (map §4 row 33, S6). **Preferred fix (requires Ch 02 and Ch 22 owners):** move the five-row class table, without the Default-control column, to Ch 02 § Scaling the shell or § One proposal, six gates, where proposals are first classified. Ch 22 keeps the class → default-control mapping and refers back. **Minimum fix in Ch 12** if they decline: C12-R01's inline gloss. Either way, unify the representation as `R0`–`R4` (map T11). |
| Plan revision API | `plans/{plan_id}:revise` (`:496`) | Ch 18 `runs/{run_id}/plans:revise` (`05-part-v.md:108`); Ch 18 rule "Plan changes" (`:82`) | **Redundancy with drift.** Ch 12 is canonical. **Requires Ch 18 owner:** delete Ch 18's API row and replace the rule bullet's body with "Plans change only through a compiled revision (Chapter 12)." |
| BudgetReservation | `:510` | Ch 28 (`08-part-viii.md:610`) | **Redundancy.** Canonical in Ch 28. Ch 12 keeps the row but adds "(defined in Chapter 28)", or drops it and references Ch 28 from `:495`. |
| "What should be agentic?" | `:430–445` | Ch 01 § Which component should own each uncertainty; Ch 02 § Where distributed systems must remain authoritative; Ch 03 § Responsibility map; Ch 04 § Where truth lives; Ch 18 § Topology decision table; Ch 16 Figure 16-1; Appendix A item 1 | **Reinforcement** (agrees with map §3). It adds the work-type axis and should be the one Part IV selection table. **Requires Ch 16/17 owner:** Ch 16 § How to use these patterns… should cite it rather than restate selection logic; Appendix A item 1 can point to it. |
| Deterministic spine with semantic nodes | Recommended-architecture row `:425`; agentic table | Ch 16 § P-02 (`:1387`); Appendix A row "Orchestration" | **Reinforcement.** P-02 is effectively this chapter's pattern, but it cites "Onboarding" (T17) and not Ch 12. **Requires Ch 16/17 owner:** P-02 should name Ch 12 (Plan IR) and Ch 15 (durable workflow) as its source chapters. Appendix A's "Orchestration" row already spans "11–15, 17–18" (`09-appendices.md:25`), so Ch 12 is covered by range; naming the Plan IR there is optional. Ch 16 has no "plan compilation" P-card; overall-book-review.md §D-04 resolves this to an obligation-table row (C16-R10), not a new card. [verified: softened — the Appendix A row does include Ch 12; the P-card option is superseded by D-04] |
| Loop/delegation bounds | `:519` | Ch 10 no-progress; AP-11 (`:1560`) | **Reinforcement.** Cross-reference both. |
| Planner/critic churn | `:427` "critic repeatedly rewrites a correct result" | Ch 13 § Bounded optimization loop; Ch 13 exercise 2 | Belongs to Ch 13. Delete it here along with the analysis-table condensation. |

## Structural Recommendations

Re-sequence the chapter so the artifact comes before its checks and the checks before the implementation:

1. Intro (`:388`). Delete the `:397` heading and move its table under the next H2.
2. § Treat planning like compilation—not authorization (`:404–412`), with the Ch 11 bridge, the "compilation ≠ dispatch authorization" sentence, and the alternatives and trade-off sentence condensed from the analysis table.
3. § What should be agentic? promoted to H2, with a lead-in linking it to node kinds.
4. § Plan IR promoted to H2, followed by the node-kind → chapter map, the risk-class gloss, and **§ Compile-time checks moved here** (merged with `:473`).
5. § Revise without rewriting history, formed by merging § Replanning contract with § Runtime revision algorithm.
6. § A workable implementation (owners, APIs, records, plan-specific scale bullets only).
7. Planning at a glance (card per the shared policy), evidence, code, and the review template.

Delete the Required-analysis table and the ARCHITECTURE GUIDANCE box after moving their few unique sentences.

## Concrete Recommended Changes

**C12-R01 — Priority: Critical — Action: Add (gloss) + Cross-reference**
- **Location:** `04-part-iv.md:465` (Plan IR) and `:516–518` (§ Compile-time checks).
- **Issue:** R1 and R4 are used ten chapters before Ch 22 defines them.
- **Why it matters:** the rule "R4 commit remains a deterministic domain operation" is meaningless without the class definitions, and the reader cannot judge the compiler's risk check.
- **Change:** **Reconciled (see overall-book-review.md §D-01):** The inline gloss is final. Ch 22 stays canonical and the class table does not move to Ch 02, so delete the conditional sentence "If the Ch 02/Ch 22 owners move the table earlier…". The "preferred fix" in this file's Cross-Chapter Duplication row is superseded. Original text: in the sentence after the JSON (rewritten per C12-R02), add:

  > "`risk_class` uses the book's five effect classes: R0 pure transform, R1 low-sensitivity read, R2 sensitive read or reversible draft, R3 external communication or material reversible change, R4 irreversible, privileged, or financial action, where the agent may only propose (full controls in Chapter 22 § Risk classes)."

  At `:518`, change "R4 commit" to "an R4 (irreversible or privileged) commit". If the Ch 02/Ch 22 owners move the table earlier (see Cross-Chapter Duplication), replace the gloss with "(risk classes, Chapter 2)".
- **Related:** C12-R03; map S6/T11.

**C12-R02 — Priority: High — Action: Move + Merge**
- **Location:** `04-part-iv.md:473` (paragraph after the Plan IR) and `:514–520` (§ Compile-time checks).
- **Issue:** the compiler duties are listed many times, and the canonical list is buried.
- **Why it matters:** the reader cannot tell which list is authoritative, and the checks are separated from the artifact they check.
- **Change:**
  - Move § Compile-time checks to directly after the Plan IR JSON (and after the node-kind map, C12-R04).
  - Add to its bullets the unique items from `:473`: "unbounded loops and unhandled terminal paths are rejected" (merge into bullet 4) and "a dynamic node may choose only among an allowlisted capability set; it cannot call arbitrary network endpoints" (new bullet).
  - Delete the `:473` paragraph.
  - Trim `:410` to: "Compilation binds each capability requirement to an eligible Skill and tool release, calculates critical path and maximum cost, and emits an immutable plan revision signed by the compiler so the scheduler can verify that what runs is what was validated."
  - Delete `:410`'s "verifies input/output schemas … checks graph and terminal properties", which Compile-time checks already covers.
- **Related:** C12-R06.

**C12-R03 — Priority: High — Action: Rewrite (code)**
- **Location:** `examples/contracts.py` (`PlanNode.risk_class: int`), `examples/patterns/plan_compilation.py` (`PlanEnvelope.maximum_risk`), and the Plan IR JSON `:465`.
- **Issue:** integer 0–4 in code versus `"R1"` in prose. Ch 11's router adds a third form (C11-R06).
- **Why it matters:** the reader cannot map the example's `maximum_risk = 4` onto "R4".
- **Change:**
  - Represent risk as an ordered enum `R0`–`R4` (e.g., `RiskClass(IntEnum)` with names R0…R4) in `examples/contracts.py`, used by both the plan compiler and the router example.
  - Keep the JSON as `"R1"`.
  - Update tests.
  - Change the example title in `config/examples.json` from "Compiling an approved plan" to "Compiling a validated plan…", and its docstring's "the thing a reviewer saw" to "the thing the compiler validated".
- **Related:** C12-R01, C11-R06.

**C12-R04 — Priority: High — Action: Add (one sentence)**
- **Location:** after the Plan IR JSON (`04-part-iv.md:471`).
- **Issue:** node kinds are unexplained, and the chapter does not connect to the rest of Part IV.
- **Why it matters:** it shows the reader that a compiled plan is the structure Ch 13–15 and Ch 18 execute, which makes Part IV cumulative.
- **Change:** add:

  > "Each node kind is executed by a mechanism defined elsewhere: `llm_activity` is a bounded model step (Chapter 10) whose output is accepted as in Chapter 13; `tool_activity` crosses the six gates (Chapter 2) with effect semantics from Chapter 22; `gate` is a human authorization (Chapter 14); `wait` is a durable timer or signal (Chapter 15); `child_task` and `join` are durable delegation and fan-in (Chapter 18)."

  [verified: per overall-book-review.md §D-22, write "`gate` is a human approval (Chapter 14)" when applying.]
- **Related:** C10-R01 (Part IV orientation).

**C12-R05 — Priority: Medium — Action: Condense**
- **Location:** `04-part-iv.md:554–596`, § How Planning works in practice.
- **Issue:** the card's problem box, lead sentence, and steps restate the prose.
- **Change:**
  - Delete the THE ENGINEERING PROBLEM box (`:556–558`), the lead sentence (`:562`), and the five steps (`:564–568`). Nothing moves up; the prose already has fuller lists.
  - Retitle the H2 "Planning at a glance" and keep the Use when table, the costs table, the failure table, and the signals list.
  - Place it before § What the evidence lets us conclude.
- **Related:** shared card policy C10-R04.

**C12-R06 — Priority: Medium — Action: Merge**
- **Location:** `04-part-iv.md:414–416` (§ Replanning contract) and `:522–530` (§ Runtime revision algorithm).
- **Issue:** one concept split across 110 lines.
- **Change:** **Reconciled (see overall-book-review.md §D-22):** As stated, but step 6 reads "a new approval (Chapter 14)".
  - Create one H2 "Revise without rewriting history" placed after § Compile-time checks. Open with `:416`'s text, then the seven steps.
  - In step 6, change "new consent/approval" to "a new human authorization (Chapter 14)".
  - Delete the § Replanning contract H3.
- **Related:** C12-R02.

**C12-R07 — Priority: Medium — Action: Move (sentence)**
- **Location:** source `04-part-iv.md:540` (last scalability bullet); destination `:390`, end of the intro paragraph.
- **Issue:** the route-first, plan-only-when-needed link to Ch 11 is buried in scale bullets.
- **Change:** add to `:390`: "When a stable route exists, route deterministically (Chapter 11); invoke the planner only at entry, at material uncertainty, or after a failure invalidates the current plan." Delete bullet `:540`.
- **Related:** C11 transition out.

**C12-R08 — Priority: Medium — Action: Condense / Remove**
- **Location:** `04-part-iv.md:418–428` (§ Planning, dynamic execution, and deterministic boundaries, the Required-analysis table) and `:542–544` (ARCHITECTURE GUIDANCE box).
- **Issue:** both restate the prose. The table's enterprise example is off-thread, and its failure row includes a Ch 13 failure.
- **Change:**
  - Move two sentences into § Treat planning like compilation: (a) "The alternatives run from a fixed workflow, rules engine, and router through plan-and-execute, ReAct, graph search, and planner/executor/critic to code generation; fixed workflows maximize predictability, dynamic planning increases coverage at a higher evaluation, security, and cost burden." (b) "Models confuse a coherent narrative with a feasible, authorized execution graph."
  - Delete the table and its H2.
  - Promote § What should be agentic? to H2, with the lead-in: "The same split decides every pattern in this Part; in a plan it is encoded as the node `kind`."
  - Delete the ARCHITECTURE GUIDANCE box. Its "human amendment" idea is already covered by step 6 (C12-R06).
  - Apply the book-wide decision on Required-analysis tables (map S16) consistently.
- **Related:** C12-R04.

**C12-R09 — Priority: Medium — Action: Remove (heading)**
- **Location:** `04-part-iv.md:397`, § From candidate plan to executable work.
- **Issue:** an empty heading.
- **Change:** delete the H2 and move the state-owner table to follow `:406`. [verified: the "or drop it" option is resolved to "keep" by overall-book-review.md §D-30(b)]
- **Related:** C10-R08.

**C12-R10 — Priority: Low — Action: Rewrite**
- **Location:** `04-part-iv.md:546–552`, § What the evidence lets us conclude.
- **Change:**
  - Replace the box with a one-row claim table. Claim: "Durable scheduling". Grounded statement: "Durable-execution systems preserve workflow progress, timers, and replay across failures, which is why compiled plans are scheduled through a workflow rather than an in-process loop." Sources: R02.
  - Change the source line to "R27; R02". Drop R13.
- **Related:** C10-R10.

**C12-R11 — Priority: Low — Action: Cross-reference**
- **Location:** `04-part-iv.md:487`, `:499`, `:510`, `:519`, `:520`, and `:406`/`:456`.
- **Change:** **Reconciled (see overall-book-review.md §D-25):** As stated, except at `:510`: replace the BudgetReservation row with "BudgetReservation — see Chapter 28 § Records worth preserving; the compiler requests one per plan node" (C28-R15), instead of adding "(budget ledger, Chapter 28)".
  - At `:487`, add "(Chapter 13)".
  - At `:510`, add "(budget ledger, Chapter 28)".
  - At `:519`, add "using the no-progress signatures of Chapter 10; see AP-11 for why per-child limits do not compose".
  - At `:520`, add "(admission, Chapter 28)".
  - At `:406`, change "the run's authority" to "the run's capability envelope (Chapter 21)".
  - Rename `authority_envelope_id` to `capability_envelope_id` in the JSON (`:456`) and "authority envelope" in the Plan record (`:505`) (map T6).
- **Related:** C11-R08.

**C12-R12 — Priority: Low — Action: Add (one sentence)**
- **Location:** `04-part-iv.md:406`, end of paragraph.
- **Issue:** "not authorization" is asserted but not explained.
- **Change:** add: "A compiled plan proves its steps fit inside the envelope; it does not authorize them. Each dispatch still receives an exact authorization decision at the Tool Gateway (Chapter 2) against the current resource version." Also change "authorize it" in `:392` to "check it stays within the run's authority".
- **Related:** Ch 02 § One proposal, six gates.

**C12-R13 — Priority: Low — Action: Rewrite (requires Ch 18 owner)**
- **Location:** `05-part-v.md:82`, `:108`.
- **Change:** see Cross-Chapter Duplication. Ch 18 drops its `runs/{id}/plans:revise` API and points to Ch 12's revision API.
- **Related:** map §5.2.

**C12-R14 — Priority: Low — Action: Cross-reference** *Added in reconciliation (see overall-book-review.md §D-27).*
- **Location:** The trimmed `04-part-iv.md:410` sentence (C12-R02) and § Compile-time checks.
- **Issue:** The Ch 08 and Ch 09 reviews ask Ch 12 to point to Ch 08 where compilation binds Skill releases; no Ch 12 item did.
- **Change:** In the C12-R02 sentence, write "…binds each capability requirement to an eligible Skill and tool release (Chapter 8)…". In § Compile-time checks, add to the eligibility bullet: "a pack Skill the run may not resolve is refused here, naming the rule, never mid-run (Chapter 9)."
- **Related:** C08-R03, C09-R07, C12-R02.

## Verification log

- **Line references checked:** 112 (every `:n` in this file, plus the Ch 02, Ch 11, Ch 13, Ch 16/17, Ch 18, Ch 21, Ch 22, Ch 28, Appendix A, example, and test pointers). Fixed: 0. All resolved within ±3 lines ("about 110 lines" between `:414` and `:522` is 108; "45 lines after the IR" is 43).
- **Claims removed:** none.
- **Claims softened:**
  - "Appendix A's Orchestration row should list Ch 12 explicitly" → the row already spans "11–15, 17–18"; naming the Plan IR is optional.
  - The "add a plan-compilation P-card" option is superseded by D-04 (obligation-table row).
- **Claims confirmed (most consequential):**
  - Three risk representations: `"risk_class": "R1"` (`:465`), "R4 commit" (`:518`), `PlanNode.risk_class: int = Field(ge=0, le=4)` (`examples/contracts.py:66`), `PlanEnvelope.maximum_risk: int = 4` (`plan_compilation.py:29`), Ch 11 `risk: int` (`:331`). `test_plan_compilation.py:46–48` uses `risk=4` against `maximum_risk=2`.
  - R0–R4 are defined only at `06-part-vi.md:714–722` (Ch 22). Book-wide grep: the first R-code is Ch 12 `:465`; later uses are Ch 21 `:495` (with a Ch 22 pointer), Ch 24 `07-part-vii.md:145`, Ch 23 `06-part-vi.md:1178`, and Appendix `09-appendices.md:446`. Ch 12 carries no pointer. "risk class" as a phrase first appears at `01-part-i.md:734` (Ch 02 § Scaling the shell), as stated.
  - Compiler-duty repetition at `:406`, `:410`, `:473`, `:484`, `:494`, `:516–520`, `:562`, `:617`, `:634`; replanning at `:416`, `:425`, `:524–530`, `:568`, `:619`, `:635`, `:544`: every location checked and present.
  - `:397` H2 contains only the state-owner table; Plan IR is an H3 (`:447`) under `:418`, after the 7-row analysis table and the 12-row agentic table; § Compile-time checks is the fourth H3 under § A workable implementation.
  - `POST /v1/plans/{plan_id}:revise` (`:496`) vs Ch 18 `POST /v1/runs/{run_id}/plans:revise` (`05-part-v.md:108`) and rule bullet `:82`; `BudgetReservation` at `:510` and `08-part-viii.md:610`.
  - `config/examples.json` title "Compiling an approved plan into a budget-bounded envelope"; docstring "provably the thing a reviewer saw" (`plan_compilation.py:1–5`).
  - Eight design alternatives at `:424`; `:427` includes "critic repeatedly rewrites a correct result"; scale bullet 7 (`:540`) is the route-first link.
  - P-02 (`:1387–1391`) cites "Onboarding" and no chapter.
- **Recommendations amended:** C12-R04 (D-22 wording note); C12-R09 (D-30(b) resolves "or drop" to keep); Cross-Chapter row on P-02/Appendix A (D-04).
- **Not verifiable here:** the claim that scale bullets 1, 2, 4, 5 are "book-wide boilerplate" (map §5.1 not re-checked across all chapters); "ten chapters later" is Ch 12 → Ch 22 and is exact.
