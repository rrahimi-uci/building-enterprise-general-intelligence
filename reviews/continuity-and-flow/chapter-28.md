# Chapter 28 — Treat Performance as a Business Decision: Continuity and Flow Review

Reviewed: `source/parts/08-part-viii.md:463–738`. Context read: Ch 27 close (`:426–461`); the appendices opening (`09-appendices.md:1–36`), Appendix L (`:533–557`), and the Closing Perspective (`:559–565`); Ch 01 Monday–Friday narrative (`01-part-i.md:88–161`); Ch 10 § Capacity model (`04-part-iv.md:51–57`); Ch 12 records and compile checks (`04-part-iv.md:505–520`); Ch 14 approval capacity (`04-part-iv.md:969`); Ch 15 canonical flow step 7 and records (`04-part-iv.md:1164`, `:1179`, `:1204–1259`); P-11 (`04-part-iv.md:1477–1483`); AP-11 (`04-part-iv.md:1560–1580`); Ch 19 LLM Gateway (`05-part-v.md:575–593`); Ch 21 caching (`06-part-vi.md:387`, `:495–496`); Ch 22 degradation (`06-part-vi.md:844`); Figure 28-1 source (`assets/diagrams/src/reliability-economics.gv`).

## Overall Assessment

Chapter 28 makes an important argument well: optimize cost and latency *per verified successful outcome*, and treat worker count as a symptom rather than as capacity. Its best material is unique to the book:

- the four-measurements table (`:513–518`);
- the observed-pressure table (`:526–531`);
- the layered scaling table (`:551–557`);
- "optimize in the order that changes outcomes" (`:571–582`);
- the seven-step scheduling algorithm (`:618–626`).

It is the correct canonical home for admission, budgets, permits, and backpressure (map §3).

The flow problems are structural and relational.

- **Structure.** The H2 § Optimize the trajectory, not the token contains five H3s that are not about trajectory: budgets, sharing, degradation, the four measurements, and the quarter-end example. § Optimize the whole journey holds only a figure and a table. The "What" (four measurements) therefore arrives after the "How" (budgets, permits).
- **Missing bridges.** The chapter never says that it composes mechanisms the reader has already met in pieces: Ch 10's per-run limits, Ch 12's compile-time cost estimate and BudgetReservation, Ch 14's approval capacity, Ch 15's suspended waits, and AP-11's monotonic budgets. Ch 15 contains no backpressure. That mechanism is first named in P-11 and lives only here.
- **An ambiguity in the Little's Law example that the quarter-end paragraph turns into a sizing error.** "An admitted run occupies the workflow system for four minutes" (`:520`) does not say whether four minutes is active service time or time in system (which, after Ch 15, includes days of durable waits); the same sentence then says the figure may "require more permits", and `:524` treats the 480 as "protected permits". Appendix L uses service time, which is the correct quantity for permits. [verified: softened — `:520` on its own is a correct Little's Law statement of runs in system; the conflation with permit-holding work happens in its last clause and at `:524`]
- **Repetition.** Cost per verified success is stated about twelve times (seven of them full restatements; see § Redundant). [verified: corrected — "seven" undercounted] Concurrency bullets appear twice (§ Control concurrency, § Scalability mechanics). Little's Law appears three times. Caching rules repeat Ch 21.
- **"Guardrails"** names numeric limits (`:639`), contradicting the book's own definition of a guardrail as a probabilistic detector (Ch 20).

**The ending.** Ch 28 is the last chapter, and the book does not end; it stops. § Where this leads next (`:736–738`) says "The architecture narrative is complete" and then lists the appendices inaccurately: "maintenance criteria" does not exist, and the list omits the glossary, research, limits, roadmap, companion guide, and coding-agent prompt. It never mentions the Closing Perspective. Nothing in Ch 28 returns to the end-to-end model the book opened with: Ch 01's five non-intelligence failures (`01-part-i.md:92–142`) and the invariant "the model provides bounded reasoning; the surrounding system owns state, authority, effects, evidence, and recovery" (`:160`).

The Closing Perspective, which partly does this, is buried after Appendix L and the references (`09-appendices.md:559`), where almost no reader will reach it. It is one callout box and one paragraph, and its "It ends as explicit contracts…" reads as a claim about the implemented case, although the companion code implements only C01–C03 (`00-front-matter.md:66–72`; Appendix I `09-appendices.md:263`, `:269`). [verified: corrected — "two short paragraphs" miscounted; "overclaims" softened, since the sentence is true of the book's design narrative and the front matter already states the code scope] The book needs a short, real ending immediately after Ch 28 that closes the loop opened in Ch 01 (C28-R10, C28-R11).

## Intended Reader Mental Model

- **What:** four distinct measures (latency, cost, capacity, reliability). Capacity is the scarce downstream permit, not CPU or worker count.
- **Why:** a cheap call that causes retries, escalations, or human work is an expensive outcome. The objective is cost and latency per verified success, constrained by safety and compliance.
- **How:**
  - Admission checks deadline, budget, risk, and permits.
  - Budgets are reserved for the near horizon and narrow down the delegation tree.
  - Queues are partitioned by real operational differences, with weighted fair scheduling and reserved capacity.
  - Permits are acquired before a worker is leased.
  - Backpressure starts at admission.
  - Degradation is explicit and never touches authorization, isolation, approval, verification, or audit.
- **When:** under pressure, defer, draft, reduce optional context, or switch to an evaluated cheaper route. Never add workers when the provider quota is the bottleneck.
- **Trade-offs:** more pools give isolation at operational cost. Managed runtimes give convenience at the cost of portability.
- **Relationships:** this chapter composes Ch 10/12/14/15/AP-11 limits into platform admission. It follows Ch 19's policy-first routing and Ch 21's authorization-scoped caching, and it owns degradation (Ch 22 previews it).
- **Practical:** size a quarter-end peak, decompose p95, and design a context-cost experiment.
- **Book-level:** the reader should finish knowing how Part VIII's three loops (governance, release, admission) close the system described in Ch 01.

## Section-by-Section Flow Review

**Opening (`:465–473`): evidence context, NORTHSTAR box, THE DESIGN CHOICE.** The evidence context correctly scopes Little's Law as an approximation [R43]. The boxes are good. "Northstar" follows the global T1 decision (`:469`, `:507`, `:520`, `:524`).

**§ Why cost and latency have to be designed into the workflow (`:475–481`).** Role: intro. The first sentence is strong. Missing: any recall of the earlier, scattered budget mechanisms (Ch 10, Ch 12, Ch 15, AP-11) and the inbound bridge from Ch 27 (release cohorts and canaries also consume capacity). Verdict: keep, and add a bridge paragraph (C28-R03).

**§ Optimize the whole journey (`:483–489`).** Figure 28-1 and the state-owner table, with no prose. In the figure, `verify -> degrade` is labeled "fail or budget": a failed verification routes into "Safe degradation (defer · draft · route)". That conflicts with the chapter's own rule at `:507`, where degradation is a response to *pressure* (the figure already has `admit -> degrade` "pressure" for that), and the figure offers no terminal or InterventionRequired outcome for a run that fails verification, which Ch 15 requires (`04-part-iv.md:1152`). Verdict: merge with § Start with the four measurements (C28-R02), and fix the figure (C28-R13). [verified: softened — the primary contradiction is with `:507`; Ch 15 is contradicted by omission, not by an opposite claim]

**§ Optimize the trajectory, not the token (`:491–495`).** The objective, defined clearly at `:495`. This is the canonical definition of cost per verified success. Verdict: keep as the "Why" H2, but move out the five H3s it currently parents (C28-R02).

**### Give each stage a latency and cost budget (`:497–499`).** Good and compact. "Each child task inherits a narrower budget" is AP-11's correction and Ch 21's narrowing, with no pointer. "The budget service issues permits; workers cannot exceed the lease" is good. Verdict: keep under a new "Admit work" H2, with pointers (C28-R03).

**### Share capacity without starving important work (`:501–503`).** Good. "Separate queues by workload and risk class" uses an ambiguous scale; read-only vs mutating maps to R-classes (C28-R09). "Approver queue" links to Ch 14 `:969` without saying so. Verdict: keep, with pointers.

**### Decide what the system may drop or defer (`:505–507`).** This is the canonical degradation rule (Ch 22 `06-part-vi.md:844` previews it). It deserves H2 status as the "When under pressure" step. Verdict: promote (C28-R02).

**### Start with the four measurements (`:509–520`).** The four-measures table is excellent. The Little's Law paragraph does not separate runs in the system from permit-holding work, and its last clause and `:524` then use the runs-in-system figure as permit capacity (C28-R01). This is the chapter's "What", and it is placed fourth. Verdict: move first and fix (C28-R01, R02).

**### A quarter-end planning example (`:522–533`).** A good worked application. The 25% reservation and the browser-pool deferral are concrete. The pressure table is the best synthesis in the chapter, and row 4 ties back to Ch 22's unknown effects. It depends on the 480-run estimate, which C28-R01 corrects. Verdict: keep as the practical-application section.

**§ Scale the workflow, not just the model call (`:535–545`).** A Required-analysis table (map S16).
- "Recommended architecture" introduces "stateless control plane", a third meaning after Ch 04 and Ch 27, and "Suspend idle workflows so they hold no workers", which is the key Ch 15 bridge buried in a table cell.
- "Failure scenarios" duplicates the pressure table.
- "Enterprise example: month-end finance" is off-thread.

Verdict: delete the table, keep two sentences, and lift the idle-workflow point into C28-R01 (C28-R02).

**### Scale by workload and failure boundary (`:547–559`).** Excellent. "Treating worker count as capacity" (`:559`) is the chapter's most transferable insight. Verdict: keep under "Admit work".

**### Control concurrency before queues control you (`:561–569`).** Its bullets overlap § Scalability mechanics (`:628–637`): queue partitioning (`:564`/`:631`), backpressure (`:566`/`:626`/`:633`), reserved capacity and fairness (`:568`/`:635`), bounded fan-out (`:567`/`:634`). Verdict: merge into the implementation section (C28-R06).

**### Optimize in the order that changes outcomes (`:571–582`).** Unique and well ordered.
- Item 1 echoes Ch 12 § What should be agentic?, without a pointer.
- Item 4 restates Ch 19's policy-first routing, with no pointer.
- Item 6 restates Ch 21's cache-key rule.
- Item 8 (ACI) relates to Ch 22 tool contracts.
- Item 10 is the objective, not an optimization step.
- The H3 sits under § Scale the workflow, but it is about optimization order.

Verdict: promote to H2 and add pointers (C28-R05, R07, R08).

**§ A workable implementation (`:584`).**
- **### Who should own each decision (`:586–588`).** Prose rather than a table, unlike Ch 27 and most other chapters (map §5.1). Verdict: convert to a table (C28-R14).
- **### The contracts between components (`:590–602`).** Good. `quotas:acquire` returning "granted, defer-until, or hard-limit" is the disposition model the code example should use (C28-R12).
- **### Records worth preserving (`:604–616`).** Good. BudgetReservation duplicates Ch 12 (`04-part-iv.md:510`) almost field for field. Ch 28 is canonical (C28-R15). QuotaDefinition carries a "policy version", the bridge to Ch 26's policy-as-code (C26-R04).
- **### Scheduling algorithm (`:618–626`).** Unique and clear. Verdict: keep.
- **### Scalability mechanics (`:628–637`).**
  - `:630` gives Little's Law a third time, as a concurrency formula.
  - `:637` restates cache-key rules a third time.
  - The rest overlaps § Control concurrency.

  Verdict: merge and trim (C28-R06, R08).
- **### Illustrative starting guardrails (`:639–649`).** The table is useful policy shapes. The heading uses "guardrail" for numeric limits (map T10). The Retry ownership row restates Ch 22's one-retry-owner rule, and the Context budget row restates Ch 06, both without pointers. Verdict: rename and add pointers (C28-R04).
- **PERFORMANCE AND COST box (`:651–653`).** Restates Ch 19 § Filter for policy before optimizing cost or quality (`05-part-v.md:583–589`) [verified: corrected — `:579–583` are gateway-table rows; the section heading is at `:583`]. Verdict: delete and cross-reference (C28-R07).

**§ What the evidence lets us conclude (`:655–661`).** One row [R43], correctly scoped. Verdict: keep.

**BEST PRACTICE box (`:663–665`).** Restates `:495`. Its one new detail (halving token spend while pushing 5% more runs to review) is a good example that belongs in the body. Verdict: fold into the body and delete the box (C28-R05).

**§ A sensible place to start (`:667–701`).** An empty H2 lead and an inline code block, contrary to `AGENTS.md`. The heading promises "Admission", but the code is a permit-subset check that raises exceptions. There is no defer or reject disposition, no deadline, and no reservation, so it teaches less than the `quotas:acquire` contract (`:596`). Verdict: move to `examples/` and align (C28-R12).

**Template sections (`:703–734`).**
- If-fails: good (p95 decomposition, per-success counts).
- Checklist: fine. `:711` and `:719` are acceptable reinforcement.
- Put the idea to work: good.
- Questions:
  - Q1 restates `:495` (acceptable).
  - Q3 restates Ch 21 caching (C28-R08).
  - Q4 restates `:507` (acceptable).
  - Q5 is good.

**§ Where this leads next (`:736–738`).** It should end the book. Instead, it gives an inaccurate appendix summary and does not point to the Closing Perspective (C28-R10).

## Sparse or Underdeveloped Content

- **Runs in the system vs permit-holding work.** This is absent, and it matters. After Ch 15, a Harborlight run can wait nine days (`04-part-iv.md:1119`) while holding no worker (`:1164`). Sizing must separate durable-state capacity (history, timers, approval queues) from scarce-permit capacity (service time). Two or three sentences fix it (C28-R01).
- **Budget inheritance across delegation.** One clause at `:499`. AP-11 (`04-part-iv.md:1560–1580`) already teaches the mechanism, so a pointer is enough. Do not expand.
- **The book's ending.** Missing entirely (C28-R10, R11).

Nothing else needs expansion. This chapter suffers from repetition, not thinness.

## Missing Conceptual Connections

- **Ch 10 § Capacity model ("turns per successful outcome", per-tenant permits, hard per-run limits) → Ch 28 platform admission**, missing "Chapter 10 bounded one loop; this chapter bounds the platform". Location: `:477–481` (C28-R03).
- **Ch 12 compiler estimate and BudgetReservation (`04-part-iv.md:510`, `:520`) → Ch 28 `budgets:reserve`**, missing "the plan compiler requests these reservations per node". Location: `:497–499` (C28-R03, R15).
- **Ch 15 durable waits ("Suspend without a worker", `04-part-iv.md:1164`) → Ch 28 sizing**, missing the distinction between runs in the system and permit-holding work. Location: `:520`, `:524`, `:542` (C28-R01).
- **Ch 15 has no backpressure; P-11 (`04-part-iv.md:1477–1483`) names "durable runtime with backpressure" → Ch 28**, missing: Ch 28 is P-11's mechanism home. Ch 16 should point to Ch 15 *and* Ch 28 (Ch 16 reviewer). Location: Ch 28 needs no P-11 mention. The fix is on the P-11 card.
- **AP-11 monotonic budgets → "Each child task inherits a narrower budget" (`:499`)**, missing a pointer (C28-R03).
- **Ch 14 approval capacity (`04-part-iv.md:969`) → "approver queue" (`:503`) and "approval capacity" (`:594`)**, missing a pointer (C28-R03).
- **Ch 19 policy-first routing → optimize item 4 and the PERFORMANCE box**, missing the cross-reference; restated instead (C28-R07).
- **Ch 21 authorization-scoped cache keys → item 6, `:637`, Q3**, restated instead (C28-R08).
- **Ch 22 R-classes → "risk class" queue partitions (`:503`, `:564`, `:611`)**, missing the scale identification (C28-R09).
- **Ch 26 policy-as-code ("decides … budgets") → QuotaDefinition "policy version" (`:608`)**, missing a pointer (C26-R04 owns it).
- **Ch 01 five failures → book ending**, missing entirely (C28-R10, R11).

## Transition Problems

- **Inbound (Ch 27 → Ch 28).** Ch 27's sentence is accurate. Ch 28's opening does not pick it up, which is acceptable. The bridge that matters is to Ch 10/12/15 (C28-R03).
- **Within the chapter.** The order is How (budgets) → When (degrade) → What (measures) → Example → Analysis table → Scaling → Optimization order → Implementation. A reader meets permits and reservations before being told what capacity *is*. C28-R02 restores What → Why → How → When → Example → Optimization order → Implementation.
- **Outbound (Ch 28 → appendices / end of book).** This is the book's final transition, and it is the weakest one: an inaccurate list, no synthesis, and no pointer to the Closing Perspective (C28-R10). The appendices divider (`09-appendices.md:3–6`) does its own job well, so Ch 28 need not re-describe the appendices in detail.

## Redundant and Repetitive Concepts

- **Cost per verified success ×12:** full restatements at `:473` (box), `:495` (definition, canonical), `:516` (table, keep), `:582` (item 10), `:665` (BEST PRACTICE), `:711` (checklist, keep), `:730` (Q1, keep); the phrase also appears in passing at `:469` (NORTHSTAR, "verified business outcomes"), `:530` (pressure table), `:653` (PERFORMANCE box, "cost per verified outcome"), `:659` (evidence row), and `:706` (If-fails). Delete `:582` and `:665` (C28-R05); the passing uses are acceptable. [verified: corrected — the count was 7; grep finds 12, matching the synthesizer's §16 count]
- **Little's Law ×3:** `:520` (canonical), `:630` (formula), and Appendix L `:540`. Delete `:630` and point to Appendix L (C28-R06).
- **Concurrency/queue controls ×2:** § Control concurrency (`:561–569`) and § Scalability mechanics (`:628–637`). Merge (C28-R06).
- **Backpressure ×4:** `:503`, `:566`, `:626`, `:633`, plus checklist `:715`. After the merge, keep `:503` (concept) and `:626` (algorithm step).
- **Cache keys ×3 in-chapter:** `:578`, `:637`, `:732` (C28-R08).
- **Degradation ×3:** `:505–507` (canonical), the figure, and Q4 `:733`. Acceptable reinforcement.

## Cross-Chapter Duplication

| Other location | Content | Verdict | Owner / action |
| --- | --- | --- | --- |
| Ch 10 § Capacity model + PERFORMANCE AND COST box (`04-part-iv.md:51–57`) | Turns per success; per-run limits; "cost per *completed task*" | R (single-loop case); term drift | Ch 10 reviewer: write "cost per verified successful outcome (Chapter 28)". Ch 28 adds the recall (C28-R03) |
| Ch 12 BudgetReservation (`04-part-iv.md:510`) and compile check (`:520`) | Same entity, near-identical fields | D | Ch 28 canonical. Ch 12 reviewer replaces the record row with "BudgetReservation (Chapter 28)" (C28-R15) |
| Ch 14 approval admission and staffing (`04-part-iv.md:969`) | Approval capacity is part of end-to-end capacity | R | Ch 28 adds a pointer (C28-R03) |
| Ch 15 step 7 and Enterprise example (`04-part-iv.md:1164`, `:1179`) | Suspend without a worker | R; bridge missing | C28-R01 |
| P-11 (`04-part-iv.md:1477–1483`) | Durable runtime with backpressure | R (card), mechanics here | Ch 16 reviewer: "Mechanics: Chapters 15 and 28" |
| AP-11 (`04-part-iv.md:1560–1580`) | Monotonic budgets across delegation | R | Ch 28 pointer at `:499` (C28-R03) |
| AP-04 (`04-part-iv.md:1709`) | Retry multiplication | R | The limits-table row points to Ch 22 (C28-R04) |
| Ch 02 § Scaling the shell (`01-part-i.md:734`) | Queues by workload and risk class; downstream limits | R (preview) | Keep |
| Ch 19 § Filter for policy… (`05-part-v.md:583–589`) and the Rate limits/Caching rows (`:576–577`) [verified: corrected line numbers] | Policy-first routing; hierarchical budgets; cache keys | Ch 28 box D | Delete the box (C28-R07). If the synthesizer adopts map S4(b) and moves model routing into Ch 28, the Ch 19 text moves here instead and Ch 28 becomes canonical |
| Ch 21 § Consistency and revocation policy (`06-part-vi.md:387`, `:495–496`) | Authorization cache keys | Ch 28 D ×3 | Ch 21 canonical (C28-R08) |
| Ch 22 graceful degradation bullet (`06-part-vi.md:844`) | Degradation ladder | D | Ch 28 canonical. Ch 22 reviewer replaces it with a pointer |
| Ch 23 Cost/availability denial row (`06-part-vi.md:1106`) | Quotas, backpressure as a security control | R | Keep |
| Ch 24 scorecard, Ch 25 performance tier (`07-part-vii.md:302`) | Cost per success, queue age | R | Keep |
| Appendix L § Quantitative sizing method (`09-appendices.md:535–544`) | Little's Law, permit pool, retry multiplier | R (formulas) | Ch 28 points to it (C28-R06). Appendices reviewer should not re-explain Little's Law prose |
| Closing Perspective (`09-appendices.md:559–565`) | Book coda | Misplaced; thin | C28-R11 |

## Structural Recommendations

Proposed order (headings in new or renamed form):

1. Opening boxes.
2. § Why cost and latency have to be designed into the workflow, plus the bridge paragraph (C28-R03).
3. § Measure the whole journey: Figure 28-1, the state-owner table, the four-measurements table, and the corrected Little's Law paragraph. (What)
4. § Optimize the trajectory, not the token: `:493–495`, plus the folded BEST PRACTICE example. (Why)
5. § Admit work against budgets and scarce capacity: H3s Give each stage a latency and cost budget; Share capacity without starving important work; Scale by workload and failure boundary; plus two sentences replacing the Required-analysis table. (How)
6. § Decide what the system may drop or defer. (When)
7. § A quarter-end planning example. (Practical application)
8. § Optimize in the order that changes outcomes (promoted to H2).
9. § A workable implementation: owners table, contracts, records, scheduling algorithm, merged scalability mechanics, illustrative starting limits.
10. Evidence, start (example), and the template sections.
11. § Where this leads next, rewritten as the book's handoff to the Closing Perspective.

Move the Closing Perspective so it immediately follows Ch 28. To avoid a topology change in the Part VIII file, place it at the top of `09-appendices.md`, before the `# PART REFERENCE — APPENDICES` divider, and rebuild it around Ch 01's Monday–Friday week (C28-R11).

**Disagreement with the concept map:** none. Two refinements.

- The map lists "Ch 15 backpressure" implicitly via P-11. Ch 15 actually contains no backpressure mechanism (verified: "backpressure" appears only at `01-part-i.md:734`, `04-part-iv.md:1477` (the P-11 title), `06-part-vi.md:1106`, Ch 28, and Appendices A, I, and J at `09-appendices.md:34`, `:329`, `:353`). [verified: corrected — `:1481` does not contain the word; the appendix occurrences were missing] The relevant Ch 15 content is "suspend without a worker", which bears on sizing rather than on backpressure.
- The map's Ch 28 closing note says the appendix summary is inaccurate. I add that the deeper problem is the absence of any ending that closes Ch 01's model.

## Concrete Recommended Changes

1. **C28-R01 — High — Rewrite.** Location: `08-part-viii.md:520` (### Start with the four measurements) and `:524` (### A quarter-end planning example); `:542` (Recommended architecture cell).
   - **Issue:** the Little's Law example treats "occupies the workflow system for four minutes" as the time that sizes permits. With Ch 15's durable waits, runs-in-system time includes waits that hold no worker.
   - **Why it matters:** a reader who has absorbed Ch 15's nine-day wait will either size workers for runs that are only waiting, or be confused by "480 active". This is the chapter's central quantitative model.
   - **Change:**
     - Rewrite `:520` so it distinguishes two populations, in substance: "Apply it to each scarce resource separately. Runs *in the system* include durable waits — a mortgage run waiting nine days for a document holds history, timers, and an approval slot but no worker (Chapter 15). Work *holding a permit* counts only active service time. If Northstar admits 120 runs per minute and each run spends four minutes of active service time holding a workflow-worker permit, about 480 permits are in use; waiting runs add to stored state and approval queues, not to that number."
     - In `:524`, change "480 active runs" to "480 worker permits in use".
     - Move the cell sentence "Suspend idle workflows so they hold no workers" (`:542`) into this paragraph, and delete it from the table (which C28-R02 removes anyway).
     - Point to Appendix L § Quantitative sizing method for E[service time] and the permit-pool formula.
   - **Related sections:** Ch 15 `04-part-iv.md:1164`; Appendix L `09-appendices.md:540–541`.

2. **C28-R02 — High — Restructure.** Location: `08-part-viii.md:483–582` (§ Optimize the whole journey, § Optimize the trajectory, not the token and its H3s, § Scale the workflow, not just the model call and its H3s).
   - **Issue:** five unrelated H3s sit under a "trajectory" H2. The "What" arrives after the "How". § Optimize the whole journey has no prose. The Required-analysis table duplicates the pressure table.
   - **Why it matters:** the reader should learn what capacity is before learning how to budget it.
   - **Change:** apply the order in Structural Recommendations.
     - Rename § Optimize the whole journey to "Measure the whole journey". Move § Start with the four measurements content (`:511–520`) under it, after Figure 28-1 and the table.
     - Leave § Optimize the trajectory, not the token with `:493–495` only.
     - Create § Admit work against budgets and scarce capacity containing `:497–503` and `:547–559`.
     - Promote § Decide what the system may drop or defer and § Optimize in the order that changes outcomes to H2.
     - Delete the Required-analysis table (`:537–545`). Keep two sentences under § Admit work: "A generic job queue or a synchronous monolith cannot express provider quotas, durable waits, or tenant fairness; partitioned queue-driven pools can, at the cost of more pools to operate. Managed runtimes reduce undifferentiated work but increase vendor dependency and can weaken trace and state portability."
     - Drop the off-thread "month-end finance" example.
   - **Related sections:** map S16.

3. **C28-R03 — High — Add.** Location: `08-part-viii.md:477–481` (§ Why cost and latency…), plus pointers at `:499` and `:503`.
   - **Issue:** the chapter never connects to the budget mechanisms already taught.
   - **Why it matters:** the reader has seen limits in Ch 10, a cost estimate and reservation in Ch 12, approval capacity in Ch 14, durable waits in Ch 15, and monotonic budgets in AP-11. Without a bridge, Ch 28 looks like a new subsystem rather than their composition.
   - **Change:**
     - Add a second paragraph to the intro, in substance: "The pieces already exist. Chapter 10 bounded one loop's turns and per-run spend; Chapter 12's compiler estimated a plan's worst-case cost and reserved budget per node; Chapter 14 counted approvers as capacity; Chapter 15 let waiting runs release their workers; AP-11 made budgets shrink down the delegation tree. This chapter composes them into one admission and scheduling system for the whole platform."
     - At `:499`, after "Each child task inherits a narrower budget", add "(AP-11; Chapter 21's narrowing applies to spend as well as authority)".
     - At `:503`, after "approver queue", add "(Chapter 14)".
   - **Related sections:** Ch 10 reviewer aligns its box term. Ch 12 reviewer (C28-R15).

4. **C28-R04 — High — Rename.** Location: `08-part-viii.md:639` (### Illustrative starting guardrails) and table rows `:645–646`.
   - **Issue:** "guardrail" names numeric limits, contradicting Ch 20 § Guardrails help, but they are not the security boundary (map T10, S17).
   - **Why it matters:** the book's last use of the term undoes its own distinction.
   - **Change:**
     - Rename the heading to "### Illustrative starting limits".
     - Retry ownership row rationale: append "(one retry owner per failure class, Chapter 22)".
     - Context budget row rationale: append "(Chapter 6)".
   - **Related sections:** map T10. The Ch 05/20 reviewers handle the other occurrences.

5. **C28-R05 — Medium — Condense.** Location: `08-part-viii.md:582` (item 10 of § Optimize in the order that changes outcomes); `:663–665` (BEST PRACTICE box).
   - **Issue:** cost per verified success is restated seven times. Item 10 is the objective, not a step.
   - **Why it matters:** repetition dilutes the one definition the reader must retain.
   - **Change:**
     - Delete item 10.
     - Append its clause to `:495`: "Token price alone ignores retries, human review, failed trajectories, and tool charges."
     - Delete the BEST PRACTICE box, and move its example to the end of `:493`: "A change that halves token spend while pushing five percent more runs into human review may well cost money."
   - **Related sections:** none.

6. **C28-R06 — Medium — Merge.** Location: `08-part-viii.md:561–569` (### Control concurrency before queues control you) and `:628–637` (### Scalability mechanics).
   - **Issue:** about half the bullets overlap. `:630` restates Little's Law.
   - **Why it matters:** the reader reads the same controls twice in two framings.
   - **Change:**
     - Merge into one "### Scalability mechanics" list in § A workable implementation, keeping each distinct item once:
       - hierarchical token buckets (`:563`);
       - partitions, merged from `:564` and `:631`, including "avoid per-tenant queues unless justified";
       - concurrency keys (`:565`);
       - backpressure and autoscaling signals, merged from `:566` and `:633`, keeping KEDA and "do not scale workers when provider quota is the bottleneck";
       - bounded fan-out and speculative execution with cancellation lag, merged from `:567` and `:634`;
       - reserved capacity with aging, merged from `:568` and `:635`;
       - prewarmed sandboxes (`:569`);
       - distributed rate limiting with no global lock (`:632`);
       - large tenants (`:636`).
     - Replace `:630` with "Size each pool with the permit-pool formula in Appendix L."
     - Delete the § Control concurrency heading.
   - **Related sections:** Appendix L `09-appendices.md:541`.

7. **C28-R07 — Medium — Cross-reference/Remove.** Location: `08-part-viii.md:651–653` (PERFORMANCE AND COST box); `:576` (item 4).
   - **Issue:** the box restates Ch 19's policy-first routing rule.
   - **Why it matters:** this is D (map S4), and it is the only place Ch 28 touches model routing.
   - **Change:** **Reconciled (see overall-book-review.md §D-08):** Map S4(b) is adopted for routing. Delete the box and replace item 4 with the material moved from Ch 19 (C19-R01(c)): the policy-first rule ("After policy fixes the eligible set—region, data class, tenant, purpose; the eligibility-first rule of Chapter 11—choose the cheapest evaluated model for the node; escalate by difficulty, uncertainty, or failed validation, not by habit"), the route-record sentence, Figure 19-2 renumbered as a Ch 28 figure, and the gateway metric list. The item 1 and item 8 pointers stand. Do not move Ch 19's cache sentences (C28-R08 covers caching).
     - Delete the box.
     - Item 4: "**Route models:** after Chapter 19's policy filter has fixed the eligible set, choose the cheapest evaluated model for the node; escalate by difficulty, uncertainty, or failed validation — not by habit."
     - Item 1: append "(Chapter 12 § What should be agentic?)".
     - Item 8: append "(tool contracts, Chapter 22)".
   - **Related sections:** if the synthesizer adopts map S4(b), Ch 19 § Filter for policy… moves into Ch 28 at item 4 and this pointer becomes the section itself. The Ch 19 reviewer coordinates.

8. **C28-R08 — Medium — Condense.** Location: `08-part-viii.md:578` (item 6), `:637` (scalability bullet), `:732` (Q3).
   - **Issue:** cache-key rules are stated three times here and again in Ch 19 and Ch 21.
   - **Why it matters:** this is D. Ch 21 owns authorization-scoped caching (map §3).
   - **Change:**
     - Item 6: "**Cache safely:** key every cache by the dimensions in Chapter 21 § Consistency and revocation policy, plus model/version, prompt hash, and knowledge snapshot; a hit still emits usage and provenance events."
     - Delete `:637`.
     - Replace Q3 with: "Why is worker count not capacity? — Capacity is the scarcest downstream permit: provider quota, browser slots, database writers, approvers. Adding workers when a provider quota is exhausted only increases contention and retries; keep work queued until the permit exists, and let admission decide whether waiting still meets the deadline." (from `:559`)
     - Keep checklist `:717`.
   - **Related sections:** Ch 21 `06-part-vi.md:387`, `:496`; the Ch 19 reviewer trims the cache sentences at `05-part-v.md:589` [verified: corrected — `:583` is the section heading].

9. **C28-R09 — Medium — Rewrite.** Location: `08-part-viii.md:503`, `:564`, `:611` (risk in queue partitions); `:542` ("stateless control plane").
   - **Issue:** "risk class" for queues names no scale. "Control plane" takes a third meaning.
   - **Why it matters:** these are the T2 and T11 collisions in the book's closing chapter.
   - **Change:**
     - `:503` "workload and risk class" → "workload and effect risk class (read-only versus mutating; Chapter 22)".
     - `:564` and `:611`: same term.
     - If the `:542` sentence survives C28-R02, write "stateless run-control services" instead of "stateless control plane".
   - **Related sections:** C26-R01; C27-R02.

10. **C28-R10 — High — Rewrite.** Location: `08-part-viii.md:736–738` (§ Where this leads next).
    - **Issue:** the last chapter's close is inaccurate ("maintenance criteria"; omitted appendices), does not synthesize, and does not point to the Closing Perspective.
    - **Why it matters:** this is the book's final transition. The reader leaves with no restatement of the end-to-end model.
    - **Change:** replace with three sentences, in substance:
      1. "Part VIII closes the operating loop: governance decides who may change behavior and how deeply it is reviewed, releases decide which behavior each run receives, and admission decides how much work runs and at what cost — each judged by verified outcomes."
      2. "The Closing Perspective that follows returns to Chapter 1's week of failures and shows where each is now contained."
      3. "The appendices are desk tools: pattern and triage guides (A, B), contracts and framework choice (C, D), research, limits, roadmap, and glossary (E–H), the Harborlight implementation and coding-agent prompt (I, J), and the evidence registry and acceptance gates (K, L)."
    - **Related sections:** C26-R12 (Part VIII orientation uses the same three-loop framing); C28-R11.

11. **C28-R11 — High — Move/Rewrite.** Location: `09-appendices.md:559–565` (Closing Perspective: What Production-Grade Intelligence Requires).
    - **Issue:** the book's coda is placed after Appendix L and the references, is one box and one paragraph long, and its "It ends as explicit contracts…" reads as a claim about the implemented case, although the companion implements only C01–C03 (`00-front-matter.md:66–72`; Appendix I `09-appendices.md:263`, `:269`). [verified: corrected — length miscounted; wording softened as in Overall]
    - **Why it matters:** without a reachable ending that revisits Ch 01, the book stops rather than closes. The reader never sees the five failures resolved by the architecture they have just learned.
    - **Change:**
      - Move the Closing Perspective H1 to the top of `09-appendices.md`, before `# PART REFERENCE — APPENDICES` (`:1`), so it directly follows Ch 28. Keep the THE PRODUCTION STANDARD box.
      - Replace its one paragraph (`09-appendices.md:565`; keep the box) with: [verified: corrected — there is no "second paragraph"]
        - (a) one sentence: "Chapter 1's prototype failed in one week for five reasons, none of them intelligence."
        - (b) a five-row table "Day | Failure | What now contains it":
          - Monday durability → durable run history, suspended waits, compatible workers (Ch 15, 27);
          - Tuesday injected instruction → content-instruction separation, boundary enforcement, containment (Ch 06, 20, 23);
          - Wednesday lost confirmation → effect ledger, intent hash, reconciliation of unknown outcomes (Ch 22);
          - Thursday audit question → causal trace plus a separate audit ledger (Ch 24);
          - Friday cheaper model → evaluated, immutable release with rollback of assignment (Ch 25, 27).
        - (c) one closing sentence restating Ch 01's line "the model provides bounded reasoning; the surrounding system owns state, authority, effects, evidence, and recovery".
        - (d) an honest scope line: "The companion code implements checkpoints C01–C03; the remaining contracts are specified here and tracked as a roadmap (Appendix I)." [verified: keep the front matter's wording — `code-gap.md` (status line) and `config/examples.json` also record a C24 OpenAI/MLflow grounding slice and an offline platform-contract slice for C04–C28, so write "the first three checkpoints are implemented; later checkpoints are roadmap targets" (as `00-front-matter.md:66–72` does) rather than "only", and do not claim C04–C28 are unimplemented outright]
    - **Validation needed:** the Closing Perspective is not counted as a Part, chapter, or appendix, so the 8/28/12 invariants should hold. Still, run the structural validators and check the DOCX/LaTeX divider and chapter-cover logic for an H1 placed before the appendices divider.
    - **Related sections:**
      - Appendices reviewer owns the Closing Perspective text and should reconcile with this placement.
      - Front-matter reviewer adds the Closing Perspective to "Find Your Way Through the Book" (map S14).
      - Ch 01 reviewer: no change needed (this is reinforcement of Ch 01, not duplication).

12. **C28-R12 — Low — Move/Rewrite.** Location: `08-part-viii.md:667–701` (§ A sensible place to start; ### Admission and capacity permit).
    - **Issue:**
      - Inline code violates `AGENTS.md`.
      - The heading promises admission, but the code is a permit-subset check that raises exceptions, with no defer path, deadline, or reservation.
      - The H2 has no lead.
    - **Why it matters:** the listing should model the chapter's own disposition contract (`quotas:acquire` → granted / defer-until / hard-limit, `:596`).
    - **Change:**
      - Move it to `examples/` with a behavioural test, register it in `config/examples.json`, and replace it with `[[EXAMPLE:admission-permit]]`.
      - Make the function return a typed decision (`granted`, `defer_until`, `rejected`) instead of raising for capacity shortfalls. Keep `PermissionError` for tenant/class mismatch.
      - Add a one-sentence lead under the H2.
      - If the code is not moved, at least rename the H3 to "Capacity permit check".
    - **Related sections:** C27-R13.

13. **C28-R13 — Medium — Rewrite.** Location: Figure 28-1 (`assets/diagrams/src/reliability-economics.gv`, edge `verify -> degrade` labeled "fail or budget").
    - **Issue:** a failed verification is routed to "Safe degradation (defer · draft · route)", although the chapter's own rule (`:507`) and the figure's existing `admit -> degrade` "pressure" edge make degradation a response to pressure, not to a failed result.
    - **Why it matters:** the figure gives a run that fails verification no terminal or InterventionRequired outcome, which Ch 15 § Terminal correctness requires (`04-part-iv.md:1152`). Re-routing to a cheaper path after failing verification is also the hidden-cost loop `:493` warns against. [verified: softened — the Ch 15 conflict is by omission; the direct contradiction is with `:507`]
    - **Change:**
      - Relabel the edge "budget or capacity pressure".
      - Add an edge `verify -> ` a new node "Terminal / intervention\nnot accepted", styled as a failure.
      - Run `make diagrams` and update the checksum and caption review per `AGENTS.md`.
    - **Related sections:** Ch 15 `04-part-iv.md:1152`.

14. **C28-R14 — Low — Rewrite.** Location: `08-part-viii.md:586–588` (### Who should own each decision).
    - **Issue:** owners are given as prose, unlike Ch 27 and most chapters (map §5.1).
    - **Change:** convert to a "Component | Responsibility" table with the seven components already named. No content change.
    - **Related sections:** map S16.

15. **C28-R15 — Low — Cross-reference.** Location: `08-part-viii.md:610` (BudgetReservation record).
    - **Issue:** Ch 12 defines the same entity (`04-part-iv.md:510`).
    - **Why it matters:** two definitions of one record drift.
    - **Change:** Ch 28 stays canonical. Append to the Ch 28 row "requested per plan node by the Chapter 12 compiler". Ch 12 reviewer replaces its row with "BudgetReservation — see Chapter 28 § Records worth preserving" and keeps only the plan-node binding.
    - **Related sections:** C28-R03.

## Verification log

- **Line references checked:** 131 (every reference to `08-part-viii.md`, `09-appendices.md`, `01-part-i.md`, `04-part-iv.md`, `05-part-v.md`, `06-part-vi.md`, `07-part-vii.md`, `00-front-matter.md`, and `reliability-economics.gv`); 3 fixed (Ch 19 § Filter for policy `:579–583` → `:583–589` in two places; the Ch 19 trim target `:583` → `:589`). Quoted phrases at `:520`, `:542`, `:559`, `:738`, `04-part-iv.md:57`, `:1152`, `:1164`, and the figure label "fail or budget" are verbatim.
- **Claims removed:** none.
- **Claims corrected or softened:**
  - "A conceptual error in the Little's Law example" → an ambiguity at `:520` that `:524` turns into a permit-sizing error (Overall, § Start with the four measurements). C28-R01 stands unchanged.
  - "Cost per verified success ×7" → 12 occurrences (7 full restatements, 5 passing). C28-R05 stands.
  - Closing Perspective "two short paragraphs" → one box and one paragraph; "overclaims" → "reads as a claim about the implemented case" (Overall, C28-R11). C28-R11's "replace its second paragraph" fixed.
  - Figure 28-1 contradiction: primary conflict is with `:507` (degradation on pressure); Ch 15 is contradicted by omission (§ Optimize the whole journey, C28-R13).
  - Backpressure grep locations corrected (`:1481` removed; appendix lines added).
  - C28-R11(d): scope line should follow the front matter's wording; `code-gap.md` and `config/examples.json` record additional C24 and offline C04–C28 slices.
- **Important claims confirmed:**
  - Ch 15 contains no backpressure mechanism; the word appears in Part IV only in the P-11 title (`04-part-iv.md:1477`) — grep.
  - § Optimize the trajectory parents five H3s (`:497`, `:501`, `:505`, `:509`, `:522`); § Optimize the whole journey has figure and table only — read.
  - `:738` names "maintenance criteria" (no such appendix) and omits Appendices E–J; the appendix headings are A pattern, B triage, C contracts, D framework, E research, F limits, G roadmap, H glossary, I companion, J coding-agent prompt, K references, L acceptance (`09-appendices.md:8–533`), so C28-R10's letter groupings are right.
  - Closing Perspective sits at `09-appendices.md:559–565`, after Appendix L and the references — read.
  - "Illustrative starting guardrails" (`:639`) vs Ch 20 § Guardrails help, but they are not the security boundary (`06-part-vi.md:28`) — read.
  - Appendix L `:540` uses `L = lambda_eff × E[service time]` — read.
  - The admission code (`:689–700`) raises on every shortfall and has no defer/deadline/reservation path; `:596` returns "granted, defer-until, or hard-limit" — read.
  - Ch 12 BudgetReservation (`04-part-iv.md:510`) and Ch 28's (`:610`) share every field but the ID — compared.
  - The seven owner components at `:588` are counted (Admission Controller, Hierarchical Quota Service, Queue/Scheduler, Worker Lease Service, Provider Limiters, Capacity Controller, Usage/Cost Ledger).
  - The companion code scope: `00-front-matter.md:66–72`, `examples/README.md:89–91`, `config/examples.json` (`"checkpoint": "C01-C03"`), Appendix I `09-appendices.md:263`, `:269` — read.
- **Recommendations amended:** C28-R08 (line number), C28-R11 (paragraph reference and scope-line wording), C28-R13 (issue/why wording). C28-R11's placement is consistent with §12 D-26; no recommendation breaks the 8/28/12 topology (the Closing Perspective is an uncounted H1), C28-R12 moves code to `examples/`, and C28-R13 edits the `.gv` source.
- **Not verified:** whether `build_book.py`/`build_latex.py` render an uncounted H1 before the appendices divider correctly (D-26 already flags this for the implementer).
