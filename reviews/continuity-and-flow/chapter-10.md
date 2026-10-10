# Chapter 10 — Use ReAct Without Creating a Runaway Loop: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:1–160`, covering the Part IV orientation (`:1–7`) and Chapter 10 (`:9–160`). Context read: the close of Ch 09 (`03-part-iii.md:356–502`), Ch 11–13 (`04-part-iv.md:162–851`), Ch 16 P-01 (`:1377`), Ch 17 AP-01/AP-11 (`:1550–1589`), Appendix A (`09-appendices.md:8–35`), and the examples `bounded-react-loop`, `react-engine`, and `examples/contracts.py`.

## Overall Assessment

The chapter is short and on-thesis. Its central idea is clear and correct: the loop runs inside, and the limits sit outside. Figure 10-1 and the sentence after it (`:41`) teach that idea well. The chapter has four problems.

1. **The disposition list mixes two kinds of outcome, and one sentence contradicts itself.** § Acceptance and failure semantics (`:49`) lists six dispositions. Some are model decisions (answer, needs_input, delegate, proposed_action). Others are controller outcomes (budget_exhausted, failed). The next sentence says a mutation "never executes inside the unconstrained loop". Two sentences later it says "If a mutation times out, the loop stops." The code contract does not match either: `AgentDecision.disposition` is `answer | needs_input | invoke_tool | delegate` (`examples/contracts.py:28`), and `ReActEngine` raises `RuntimeError` rather than returning `budget_exhausted` or `failed`.
2. **"Stop" and "accept" are conflated.** `:41` says "the decision to stop belongs to the acceptance engine". But the controller stops on limits and no-progress (`:45`, `:53`). The acceptance engine decides whether an answer is accepted. Ch 13 later separates these roles cleanly. Ch 10 should not blur them first.
3. **The "How ReAct works in practice" card mostly repeats the prose.** About 70% of it restates `:23–53`. Its unique content is the five-step loop, the context-poisoning control, and the signal list. The five-step loop is the only ordered description of the mechanism, and it sits 40 lines below the figure it explains. ReAct is also the one Part IV pattern that really is described four times: prose, card, P-01, and Appendix A item 2.
4. **The transition from Part III is missing.** Ch 09 closes on "The platform and capability model are complete". Ch 10 never mentions Skills or the AgentRuntime seam, and names the Tool Gateway only once, inside the card's step 3 (`:83`), although its "small eligible tool set" (`:89`) is exactly what Ch 08 resolution and the Ch 02 Tool Gateway produce. [verified: corrected — the review said the Tool Gateway is never mentioned; it is, at `:83`]

Lesser issues: "information gain" is used but never defined; the capacity guidance appears twice (`:53`, `:57`); the COMMON PITFALL is misplaced; there is a generic EVIDENCE BOUNDARY box; the two examples run back to back without lead-ins.

## Intended Reader Mental Model

- **Before:** Ch 02 says the model proposes and deterministic gates decide. Ch 03 says the framework runs one bounded step behind AgentRuntime. Ch 06 says observations entering context are untrusted. Ch 08–09 say tools and Skills reach a step only through deterministic resolution.
- **After:** (a) ReAct is justified only when the next information need depends on the last observation. (b) A controller outside the model owns turns, budgets, tool eligibility, and no-progress detection. (c) Mutations leave the loop as proposals. (d) Each turn ends in a typed disposition, and success is decided by acceptance criteria, not by the model's wording. (e) Cost scales with trajectory length.
- **Missing pieces:** (d) is muddled by the mixed disposition list. The reader is never told that the "eligible tools" are the step's resolved Skills and tools from Part III.

## Section-by-Section Flow Review

**Part IV orientation (`:1–7`).**
- *Role:* the Part divider.
- *What it adds:* the sequence (loops → routing → planning → reflection → human review → durable work → catalogs).
- *Verdict:* adequate as a list, but it gives no unifying model. It never says that every Part IV pattern is a different way to place a model step inside the six gates (Ch 02) and the runtime seam (Ch 03), and that each chapter answers the same three questions: what the model may decide, what the controller owns, and how the pattern stops.
- *Issues:* "loop shapes teams reach for" covers only Ch 10. There is no backward link to Part III. "It ends with a catalog" is true, but the catalog draws on Parts V–VIII (map §8).

**WHERE THE MORTGAGE CASE STANDS / THE DESIGN CHOICE (`:13–19`).** Good. The case box states why ReAct fits ("next information need depends on the previous observation"). The design choice is the chapter in one line.

**§ Why useful reasoning loops still need hard limits (`:21`).**
- *Role:* chapter intro.
- *Adds:* the list of what moves under external control.
- *Verdict:* this is the first of two framing H2s. It restates the design-choice box, and `:28` then restates it again. This is the book-wide "double why opening" (map §5.1).

**§ Use ReAct only when observations change the next step (`:28`).**
- *Role:* the "when" rule.
- *Adds:* the contrast with a known workflow and the cost argument.
- *Verdict:* strong. It is the chapter's best paragraph.
- *Issues:* the state-owner table (`:33–35`) is unexplained and breaks the flow from "when" to "how". It names `AgentDecision · Observation · ReActLimits` but not the disposition contract.

**§ Keep the feedback loop inside external limits (`:37`).**
- *Role:* the mechanism.
- *Adds:* Figure 10-1, the reading guide (`:41`), conditional adaptivity (`:43`), and normalized signatures plus no-progress (`:45`).
- *Verdict:* the core of the chapter, and it works.
- *Issues:*
  - `:41` assigns "the decision to stop" to the acceptance engine (see Overall Assessment, item 2).
  - `:45` describes no-progress as "accepted evidence does not change across turns". That is the definition of the "information gain" used at `:112`, `:145`, and `:154`, but the term itself never appears here.
  - The ordered loop the figure depicts is not given here; it sits in the card (`:81–85`).
  - "Northstar" (`:45`) is the T1 term (map §6).

**§§ Acceptance and failure semantics (`:47`).**
- *Role:* the typed outcomes.
- *Adds:* the disposition list and the read-retry versus mutation rule.
- *Verdict:* necessary, but internally inconsistent (Overall Assessment, item 1).
- *Issues:*
  - "delegate" is the hook for Ch 11, but nothing says so.
  - There is no "unknown" outcome, although the paragraph describes an unknown effect.
  - It does not connect "answer" to acceptance. Who accepts an answer? Ch 13 answers that.

**§§ Capacity model (`:51`) and PERFORMANCE AND COST box (`:57`).**
- *Role:* cost and capacity.
- *Adds:* turns per successful outcome, and the quadratic token growth.
- *Verdict:* useful.
- *Issues:* the two say the same thing twice ("turns per successful outcome" / "cost per completed task"). Ch 28's canonical metric is cost per *verified* success (map §3), and neither cross-references it.

**§ What the evidence lets us conclude (`:59`).**
- *Role:* citation.
- *Verdict:* the EVIDENCE BOUNDARY box is the generic Ch 10–13 boilerplate (map §5.1). R01's actual claim is already stated in the evidence-context blockquote (`:11`). R13 (NIST GenAI profile) supports no sentence in the chapter.

**COMMON PITFALL box (`:67–69`).**
- *Role:* the retry-as-reasoning pitfall.
- *Verdict:* good content in the wrong place. It belongs to § Acceptance and failure semantics (read retry) and sits after the evidence section instead. It previews AP-04 without naming it.

**§ How ReAct works in practice (`:71`) and its H3s.**
- *THE ENGINEERING PROBLEM box (`:75`):* restates `:23` and `:30`. Redundant.
- *§§ How the pattern works (`:77`):* the first sentence restates `:41`/`:45`. The five steps (`:81–85`) are the only ordered loop in the chapter and belong next to Figure 10-1. The Use when / Do not use when table restates `:30` and Q5 (`:156`).
- *§§ Where it helps—and what it costs (`:91`):* two rows. It is the only explicit trade-off statement in the chapter, so keep it. "increases attack surface" is new.
- *§§ Where it can fail—and how to contain it (`:98`):*
  - Ping-pong restates `:45`.
  - Budget exhaustion restates `:53`.
  - Context poisoning is new to the chapter. It is the one place Ch 06's untrusted-observation rule is applied, and it deserves a sentence in the prose.
- *§§ What you need to see in production (`:106`):* useful. It overlaps § If this fails step 1 but has a different purpose (signals versus diagnosis). Keep it.
- *Verdict:* the card earns its place only as a compact summary. The step list should move up, and the box and lead sentence should go.

**§ A sensible place to start (`:116`) / §§ Bounded ReAct controller (`:121`).**
- *Role:* code.
- *Verdict:* two examples with no lead-in, and an empty H2 wrapper (map §5.3).
- *Issues:*
  - `bounded-react-loop` is an OpenAI Agents SDK version in which the tool refuses after a budget.
  - `react-engine#core` is the framework-neutral controller the chapter describes.
  - The reader is not told why there are two.
  - `react-engine` hands every `invoke_tool` decision, including one carrying a `logical_effect_key` (a mutation), to the injected `invoke_tool` callable; neither the engine nor its tests distinguish a read from a mutation or return a mutation as a proposal, so the `:49` rule is left to whatever callable is injected rather than enforced by the controller the chapter describes. It also raises `RuntimeError` on budget, turn limit, and no-progress instead of returning typed outcomes, which does contradict `:49`. [verified: softened — the mutation point is "not enforced", not a direct contradiction; the raise-versus-typed-outcome point is confirmed against `examples/patterns/react_engine.py:81–104` and `test_react_engine.py:46–64`]

**§ If this fails in production (`:125`).**
- *Verdict:* good, and specific to the chapter.
- *Issues:* step 3 ("acceptance criteria or model wording") is the right check, and it relies on the stop/accept distinction that `:41` blurs.

**§ What to verify before production (`:131`).** Good, specific, five items. Item 2 again says "the controller owns … acceptance", which needs the same fix as `:41`.

**§ Put the idea to work (`:143`).** Good. Exercise 1 depends on "information gain" being defined.

**§ Questions to bring to design review (`:148`).** Good. Q1 and Q5 restate the "when" rule. That is acceptable reinforcement in a review aid.

**§ Where this leads next (`:158`).** Good bridge. It could name the hook: a ReAct turn that returns `delegate` is where routing begins.

## Sparse or Underdeveloped Content

- **Information gain** (`:112`, `:145`, `:154`) is never defined. One clause at `:45` fixes this: "information gain — new accepted evidence produced by the turn".
- **Disposition semantics** (`:49`) need two short lists, not one mixed one (C10-R02).
- **Observation contract.** Q4 (`:155`) gives the best definition of an observation in the chapter ("typed, sanitized result or artifact reference with provenance, version, classification, and explicit error semantics"), but it appears only in the review table. The prose never says what an Observation is, though it is a core contract (`:35`). Move one sentence into `:45`.
- No expansion is needed beyond these. The chapter's length suits the pattern.

## Missing Conceptual Connections

- **Ch 09 Skill Pack → Ch 10 eligible tools, missing "the step's tool set is the resolved Skill/tool slice."** Location: `:28` or `:43`. Without it, Part IV reads as detached from Part III (map §2, Ch 09 closing).
- **Ch 02 six gates → Ch 10 "mutation leaves as a proposal," missing "the proposal enters the six gates."** Location: `:49`. The sentence lists "policy, approval, effect, and workflow processing" without naming the gates the reader already knows.
- **Ch 06 untrusted context → Ch 10 observations, missing "observations re-enter as untrusted, provenance-labeled data."** This exists only in the card (`:103`). Location: `:45`.
- **Ch 10 `delegate` disposition → Ch 11 routing/handoff, missing "delegate is a request the controller turns into a route or handoff."** Location: `:49` and the closing `:160`.
- **Ch 10 "answer" → acceptance, missing "an answer is a candidate; the acceptance engine (Ch 13) decides."** Location: `:41`, `:49`.
- **Ch 10 budgets → Ch 28 admission and cost per verified success, missing a forward pointer.** Location: `:53`.
- **Ch 10 budgets → AP-11, missing "budgets must decrease across delegation."** Ch 10 caps one loop. AP-11 shows why a per-loop cap does not compose. A pointer at `:53` costs one clause.

## Transition Problems

- **Into the Part (Ch 09 → Part IV orientation → Ch 10):** abrupt. Ch 09 ends on Skill Packs. The orientation introduces "loop shapes". Ch 10 opens on ReAct with no mention of the platform it runs on. Fix in the orientation (C10-R01) and at `:28` (C10-R07).
- **Within the chapter:**
  - The `:21` → `:28` double opening.
  - Figure 10-1 (`:39`) is separated from its step list (`:81–85`) by 40 lines.
  - The COMMON PITFALL (`:67`) follows the evidence section, unrelated to what precedes it.
- **Out (Ch 10 → Ch 11):** sound, but it should name `delegate` as the bridge.

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict |
| --- | --- | --- |
| Use ReAct only when the next step depends on observation | design choice `:19`; `:23`; `:30`; card `:75`, `:89`; Q1 `:152`; Q5 `:156`; checklist `:133` | Prose `:30` is canonical. `:23` and `:75` are redundant. The Q/checklist entries are acceptable review reinforcement. |
| Controller owns limits/state/acceptance | `:26`; `:41`; `:45`; card `:79`; checklist `:135`; Q2 `:153` | `:41` is canonical. Card `:79` is redundant. |
| Cost per outcome | `:53`; `:57` | Merge. |
| Repeat-signature / no-progress | `:45`; card `:102`; If-fails `:128`; checklist `:139`; Q3 `:154`; exercise `:145` | `:45` is canonical. The others are acceptable task-specific reuse. |
| Retry of a failing tool | `:49`; PITFALL `:69` | Co-locate. |

## Cross-Chapter Duplication

| Concept | Here | Elsewhere | Verdict |
| --- | --- | --- | --- |
| Bounded ReAct as a pattern | Prose + card | Ch 16 § P-01 — Bounded ReAct (`:1377`); Appendix A item 2 and row "Reasoning" (`09-appendices.md:13`, `:24`) | **Redundancy.** The four-fold description is real for ReAct. P-01's only unique content is the "tempting shortcut" framing and the example "asks once for the missing employment document, then stops". **Requires Ch 16/17 owner:** reduce P-01 to the shortcut, why it fails, and a pointer to Ch 10's at-a-glance card. |
| Unbounded loops / delegation budgets | `:53` per-run limits | Ch 17 § AP-11 (`:1560`) | **Reinforcement.** AP-11 adds the composition argument and code. Add a cross-reference here and no new content. |
| Retry ownership | PITFALL `:69` | Ch 03 § One retry owner; AP-04; Ch 22 | **Reinforcement** (one-line application). Point to AP-04 / Ch 22. |
| Unknown effect on timeout | `:49` | Ch 22 (canonical); five earlier pre-teachings (map §3) | Ch 10's mention is one clause, and acceptable once it is corrected (C10-R02). Point to Ch 22. |
| Cost per outcome | `:53`, `:57` | Ch 28 § Optimize the trajectory, not the token | **Reinforcement**, but the term drifts: "completed task" versus "verified success". Align with Ch 28. |
| Terminal/disposition vocabulary | `:49` | Map T12 (seven vocabularies), Ch 15 § Terminal correctness, AP-07 | **Redundancy with drift.** Ch 10 should own the *step-disposition* list and Ch 15 the run-terminal list (map T12). |
| Ch 01 vocabulary pointer | — | `01-part-i.md:450` says acceptance criteria are developed in Ch 10 and 12 | Ch 10 does not develop them. See C13-R08 (Ch 01 owner). |

## Structural Recommendations

1. **Make the mechanism section self-contained.** Move the card's five steps directly under Figure 10-1 in § Keep the feedback loop inside external limits. Then the figure, its reading guide, and its step list sit together.
2. **Restructure the card as a compact summary.** This is a shared policy for Ch 10–13 and is proposed for all 12 How-X cards.
   - Delete THE ENGINEERING PROBLEM box and the card's lead sentence.
   - Retitle the card "ReAct at a glance".
   - Keep Use when / Do not use when, the cost table, the failure → control table, and the signals list.
   - Place it after § Capacity model and before § What the evidence lets us conclude.
   - Ch 16 P-01 and Appendix A then point to it (requires Ch 16/17 owner).
3. **Collapse the double opening.** Fold `:21` into `:28`.
4. **Give the orientation page a unifying sentence** (the three questions every Part IV pattern answers).

## Concrete Recommended Changes

**C10-R01 — Priority: High — Action: Rewrite**
- **Location:** `04-part-iv.md:3–7`, Part IV orientation.
- **Issue:** the orientation lists chapters but gives no shared model, and it does not link back to Part III.
- **Why it matters:** the reader enters six pattern chapters without the frame that makes them comparable, and loses the platform thread built in Ch 07–09.
- **Change:** **Reconciled (see overall-book-review.md §D-28):** C10-R01, the Part IV half of C09-R09, and C16-R06 all edit this one paragraph. Apply the merged paragraph given in overall-book-review.md §D-28 in a single edit; it keeps this item's two inserted sentences and wording change. Original text: keep the existing three sentences and insert two after the first.
  - Substance of the first: "Each pattern in Chapters 10–15 places a model step inside the same platform: the step receives a resolved slice of Skills and tools (Chapters 8–9), its outputs cross the six gates (Chapter 2), and the framework stays behind AgentRuntime (Chapter 3)."
  - Substance of the second: "Each chapter answers three questions: what the model may decide, what the controller owns, and how the pattern stops and is accepted."
  - Change "starts with the loop shapes teams reach for" to "starts with the smallest bounded loop".
  - Keep the result to one paragraph so the divider page stays standalone.
- **Related:** Ch 09 § Where this leads next (`03-part-iii.md:502`); C10-R07.

**C10-R02 — Priority: High — Action: Rewrite**
- **Location:** `04-part-iv.md:49`, § Acceptance and failure semantics.
- **Issue:** the paragraph mixes model decisions with controller outcomes. It says mutations never execute in the loop and then describes a mutation timing out in the loop. It disagrees with `AgentDecision` (`examples/contracts.py:28`).
- **Why it matters:** this is the chapter's typed-outcome contract. A reader cannot tell what the model may return, what the controller imposes, or where an unknown effect is handled.
- **Change:** **Reconciled (see overall-book-review.md §D-13):** As stated, and tie it to Ch 03's step contract: model decisions travel in `AgentStepResult.decision`; the controller's own outcomes (`budget_exhausted`, `no_progress`) are typed stop reasons returned as `status: failed` with that `error_code`, not exceptions. Sentence 2 cites "the step status of Chapter 3". The workflow, not the loop, decides whether a stop reason opens an intervention (Chapter 14). Original text: replace the paragraph with three sentences.
  1. Each turn, the model returns one typed decision: `invoke_tool` (read only), `proposed_action` (a mutation, which leaves the loop as a proposal for the six gates of Chapter 2), `answer`, `needs_input`, or `delegate`.
  2. The controller ends the activity with the model's terminal decision or with its own outcome: `budget_exhausted`, `no_progress`, or `failed`.
  3. A read that times out may be retried within the run budget. A proposed mutation is executed by the workflow outside the loop; if that execution times out, the effect is unknown and is reconciled before the loop resumes (Chapter 22).
- **Code:** add `proposed_action` to `AgentDecision.disposition` in `examples/contracts.py`. Make `ReActEngine.run` return typed `budget_exhausted` / `no_progress` outcomes instead of raising. Route mutating `tool_call`s out as proposals. Update `examples/tests/test_react_engine.py`.
- **Related:** map §6 T12 (Ch 10 owns step dispositions; Ch 15 owns run terminals); C10-R03.

**C10-R03 — Priority: High — Action: Rewrite**
- **Location:** `04-part-iv.md:41`, § Keep the feedback loop inside external limits; also checklist `:135`.
- **Issue:** "the decision to stop belongs to the acceptance engine" conflates stopping with accepting.
- **Why it matters:** Ch 13's core distinction (an independent acceptance decision) depends on the reader already separating "the loop stopped" from "the result was accepted".
- **Change:**
  - Rewrite the last clause of `:41`: "the controller decides when the loop stops (limits, no progress, a terminal decision), and the acceptance engine — not the model's wording — decides whether the result is accepted (Chapter 13)."
  - Change checklist `:135` to "The controller owns limits, state, and tool invocation; acceptance is decided outside the loop."
  - Change the diagram edge label `obs -> acc " stop?"` in `assets/diagrams/src/pattern-react.gv` to `" accept?"`, then run `make diagrams`.
- **Related:** C13-R02.

**C10-R04 — Priority: Medium — Action: Move + Remove**
- **Location:** `04-part-iv.md:71–114`, § How ReAct works in practice.
- **Issue:** the card restates the prose. Its only ordered step list is 40 lines from the figure.
- **Why it matters:** the reader meets the mechanism twice, and the steps are not where they are needed.
- **Change:**
  - Delete the THE ENGINEERING PROBLEM box (`:73–75`) and the card's lead sentence (`:79`).
  - Move the five numbered steps (`:81–85`) to directly after the reading-guide paragraph `:41`, introduced by "Each turn follows the same sequence:".
  - Retitle the H2 "ReAct at a glance" and keep the Use when table, the two tables, and the signals list under it.
  - Move the whole block to sit after § Capacity model / the PERFORMANCE box, before § What the evidence lets us conclude.
  - Move the context-poisoning control into prose (see C10-R05).
- **Related:** the shared card policy (C11-R05, C12-R05, C13-R04); Ch 16 P-01 (C10-R11).

**C10-R05 — Priority: Medium — Action: Rewrite**
- **Location:** `04-part-iv.md:45`.
- **Issue:** "information gain" is undefined, the Observation contract is undefined, and the untrusted-observation rule appears only in the card.
- **Why it matters:** the exercise (`:145`), Q3 (`:154`), and the signals list (`:112`) use these terms.
- **Change:**
  - Append to `:45`: "Information gain is the new accepted evidence a turn produces; a turn with none counts toward the no-progress threshold."
  - Add one sentence: "Each observation is a typed, sanitized result or artifact reference carrying provenance, version, and classification, and it re-enters context as untrusted data (Chapter 6)."
  - Then shorten Q4's strong answer (`:155`) to "See the observation contract above; plus explicit error semantics."
- **Related:** Ch 06 § The trust hierarchy of instructions.

**C10-R06 — Priority: Medium — Action: Merge**
- **Location:** `04-part-iv.md:51–57`, § Capacity model and the PERFORMANCE AND COST box.
- **Issue:** the same metric is stated twice, with drifting terms.
- **Why it matters:** this is minor duplication, but it introduces a metric name that Ch 28 later replaces.
- **Change:**
  - Keep § Capacity model and absorb the box's unique content (quadratic growth; summarize observations before re-entry).
  - Delete the box.
  - Replace "per successful outcome" with "per verified success (Chapter 28)".
  - Add: "Per-loop caps do not compose across delegation; budgets must be withdrawn from the parent (AP-11)."
- **Related:** Ch 28 § Optimize the trajectory, not the token; Ch 17 § AP-11.

**C10-R07 — Priority: Medium — Action: Add (one sentence)**
- **Location:** `04-part-iv.md:30`, § Use ReAct only when observations change the next step.
- **Issue:** there is no link to Part III.
- **Why it matters:** "small eligible tool set" (`:89`) is otherwise unexplained, and the Part III → IV thread breaks.
- **Change:** append: "The tools a ReAct step can call are the slice resolved for that step from its pinned Skills (Chapter 8) and exposed through the Tool Gateway (Chapter 2); the loop never discovers tools on its own."
- **Related:** C10-R01; Ch 08 § Discovery is not permission.

**C10-R08 — Priority: Medium — Action: Merge**
- **Location:** `04-part-iv.md:21–30`, § Why useful reasoning loops still need hard limits and § Use ReAct only when observations change the next step.
- **Issue:** double framing opening.
- **Why it matters:** the reader reads the design choice three times before the mechanism.
- **Change:**
  - Delete the `:21` H2 heading and keep its paragraph as unheaded chapter-intro text.
  - Drop its last sentence, which restates the design-choice box.
  - Move the state-owner table (`:33–35`) to after § Keep the feedback loop inside external limits' first paragraph. [verified: the "or drop it" option is resolved to "keep" by overall-book-review.md §D-30(b)]
  - Apply the same treatment to Ch 11–13 (C11-R09, C12-R09, C13-R09).
- **Related:** map §5.1 "Double why opening".

**C10-R09 — Priority: Low — Action: Move**
- **Location:** `04-part-iv.md:67–69`, COMMON PITFALL box.
- **Issue:** it is misplaced after the evidence section.
- **Change:** move it to directly after § Acceptance and failure semantics (`:49`). Add "(see AP-04)" after "cap attempts per tool".
- **Related:** Ch 17 § AP-04.

**C10-R10 — Priority: Low — Action: Rewrite**
- **Location:** `04-part-iv.md:59–65`, § What the evidence lets us conclude.
- **Issue:** the generic EVIDENCE BOUNDARY box, and R13 cited without a claim.
- **Change:** delete the box; the `:11` evidence context already scopes R01. Change the source line to "The discussion above draws on R01." Drop R13 from this chapter unless a sentence is tied to its scope (R13 stays cited in Ch 01, 04, 12, 13, 25, and 26, so the registry invariant holds).
- **Related:** C11-R10, C12-R10, C13-R10 (same treatment).

**C10-R11 — Priority: Medium — Action: Condense (requires Ch 16/17 owner)**
- **Location:** `04-part-iv.md:1377–1383`, Ch 16 § P-01 — Bounded ReAct; `09-appendices.md:13`.
- **Issue:** the fourth description of ReAct.
- **Change (for the Ch 16 owner):**
  - Keep P-01's "tempting shortcut" and "why it fails" sentences and its mortgage example.
  - Replace the "better design" and "what to watch" sentences with "See Chapter 10, ReAct at a glance."
  - Appendix A item 2 can stay as a one-liner.
- **Related:** C10-R04.

**C10-R12 — Priority: Low — Action: Rewrite**
- **Location:** `04-part-iv.md:116–123`, § A sensible place to start / § Bounded ReAct controller.
- **Issue:** two examples with no explanation, and an empty H2.
- **Change:** add one line before each marker.
  - Before `bounded-react-loop`: "An OpenAI Agents SDK version in which the run budget lives in the tool context."
  - Before `react-engine#core`: "The framework-neutral controller the chapter describes: it owns turns, tool budget, and repeat detection."
- **Related:** C10-R02 (fix the engine's mutation and raise behavior).

**C10-R13 — Priority: Low — Action: Rewrite (book-wide T1)**
- **Location:** "Northstar" at `04-part-iv.md:45`, `:195`, `:410`, `:672`, `:674`.
- **Issue:** two names for one platform (map §6 T1).
- **Change:** apply the book-wide T1 decision, which overall-book-review.md §D-20 resolves to "drop Northstar": use "Harborlight's platform" or "the platform". This one item covers all of Ch 10–13, so it is not repeated in the other files. [verified: the five locations are exact; the two further Part IV occurrences, `:882` and `:1146`, belong to Ch 14–15]

**C10-R14 — Priority: Low — Action: Cross-reference** *Added in reconciliation (see overall-book-review.md §D-29).*
- **Location:** End of § If this fails in production.
- **Issue:** Same request as C05-R16.
- **Change:** Add one line: "If limits reset at each delegation hop or every layer retries, see AP-11 and AP-04 in Chapter 17."
- **Related:** C17-R03, C10-R09.

## Verification log

- **Line references checked:** 78 (every `:n` in this file, plus the Ch 16/17, Appendix A, Ch 01–03, Ch 22, and Ch 28 pointers). Fixed: 0. All resolved within ±3 lines.
- **Claims removed:** none.
- **Claims softened:**
  - "`react-engine` executes every `invoke_tool` decision, including any mutation … contradict `:49`" → the engine does not enforce the read/mutation split; whether a mutation executes depends on the injected `invoke_tool` callable. The raise-instead-of-typed-outcome point stands.
  - "Ch 10 never mentions … the Tool Gateway" → it is named once, in card step 3 (`:83`); Skills and AgentRuntime are genuinely absent from `:9–160`.
- **Claims confirmed (most consequential):**
  - `:49` lists six dispositions mixing model decisions and controller outcomes; `AgentDecision.disposition` is `answer | needs_input | invoke_tool | delegate` (`examples/contracts.py:28`); `ReActEngine.run` raises `RuntimeError` for tool-call budget, no-progress, and turn limit (`react_engine.py:82`, `:103`, `:104`), and `test_react_engine.py` asserts those raises.
  - `:41` "the decision to stop belongs to the acceptance engine" is verbatim; `pattern-react.gv` has the edge `obs -> acc [label=" stop?"]`.
  - "information gain" appears only at `:112`, `:145`, `:154` (and Appendix B `09-appendices.md:42`); no definition anywhere in the book.
  - ReAct is described four times: prose, card (`:71`), P-01 (`:1377–1383`), Appendix A item 2 and row "Reasoning" (`09-appendices.md:13`, `:24`).
  - `01-part-i.md:450` sends "Acceptance criteria" to "Chapters 10 and 12".
  - Cost metric drift: `:53` "turns per successful outcome", `:57` "cost per *completed task*", Ch 28 "cost per verified successful outcome" (`08-part-viii.md:495`).
  - R13 (NIST AI 600-1, scope "cross-sector generative-AI risk considerations") is tied to no sentence in `:9–160`.
  - AP-11 at `:1560` is the composition argument; Ch 03 § One retry owner (`01-part-i.md:1184`) and AP-04 (`:1707`) exist as cited.
- **Recommendations amended:** C10-R08 (state-owner "or drop" resolved to keep per D-30(b)); C10-R13 (Northstar resolved to drop per D-20); C10-R10 (named where R13 stays cited).
- **Not verifiable here:** the "about 70%" card-overlap estimate (a judgement; the three unique items listed are accurate), the "five earlier pre-teachings" of unknown effect (depends on the concept map, not checked), and the "map T6 five names" count.
