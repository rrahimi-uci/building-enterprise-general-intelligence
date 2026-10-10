# Chapter 13 — Use Critique to Improve—Never to Self-Approve: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:642–850`. Context read: Ch 12 close and Acceptance Engine references (`:487`, `:499`, `:638–640`), Ch 14 opening (`:852–880`), Ch 02 § Deterministic acceptance (`01-part-i.md:728–730`) and Q (`:889`), Ch 01 vocabulary table (`01-part-i.md:450`), Ch 25 (`07-part-vii.md:224–495`), Ch 17 AP-07 and AP-10 (`04-part-iv.md:1809`, `:1681`) [verified: corrected — the two line numbers were paired in the wrong order], Ch 16 (no reflection card), Appendix A item 7, and `assets/diagrams/src/pattern-reflection.gv`.

## Overall Assessment

The chapter's governing distinction is sharp and correct: reflection asks "what is missing?", and evaluation asks "does it meet the rubric?" (`:672`). Its rule is the book's thesis applied to quality: a model score is evidence, never permission (`:674`). The chapter falls short in five places.

1. **The code contradicts the chapter.** The inline "Bounded evaluator–optimizer" (`:783–813`) lets the evaluator decide acceptance (`if evaluation.accepted: return`). It runs no deterministic check first, has no no-progress stop, and raises instead of escalating with both artifacts, although `:678` says it must escalate. It is also unregistered inline code (against AGENTS.md), with every import unused (five import lines, seven names, including a `dataclass` that is imported but never applied), undefined `Generator`/`Evaluator` types, and `Evaluation` missing `@dataclass`. A reader who copies it reproduces exactly the self-certification the title forbids. [verified: corrected — "five unused imports" was by line; all seven imported names at `:785–789` are unused]
2. **The acceptance engine is named but never defined.** The state-owner table makes the Acceptance Engine the state owner, and `AcceptanceDecision` is a core contract (`:666`). Ch 10 (`:41`) and Ch 12 (`:487`, `:499`) defer to it. Ch 01's vocabulary sends readers to Ch 10 and Ch 12 for acceptance criteria (`01-part-i.md:450`). Yet no chapter gives one consolidated definition of the engine. The pieces are scattered: Ch 02 `:730` lists what Harborlight checks, Ch 13 `:672` gives the order (executable checks before any judge), AP-07 (`:1815`) lists a return set ("accepted, blocked, needs-input, failed, or unknown-effect"), Appendix H (`09-appendices.md:205`) has a one-line gloss, and Ch 01 names it as an owner (`01-part-i.md:348`, `:549`). None says what it takes in or who alone may issue the decision. Ch 13 is the natural canonical home. A compact definition fills a real gap and would not be padding. [verified: softened — "never defined" overstated; order and a return list exist, scattered and inconsistent (D-12 fixes the return set)]
3. **Three framing headings say the same thing.** § Why critique cannot certify its own answer (`:652`), § Give evaluation its own independent path (`:659`), and § Improve the answer without letting the system certify itself (`:668`) carry one idea. The "deterministic checks first, judges for qualitative criteria, scores are evidence" rule appears at `:661`, then `:672`, then `:674`.
4. **The two pattern cards largely overlap.** Reflection (`:688`) and Evaluator–Optimizer (`:732`) have the same stop rules, the same "endless revision / stylistic churn" control, and the same "deterministic checks" control. The prose already presents evaluator–optimizer as reflection plus an independent evaluator (§ Bounded optimization loop, `:676`).
5. **The boundary with Ch 25 is not drawn.** Ch 13 talks about "release" decisions (`:674`), judge calibration (`:674`, checklist `:829`), and a regression corpus (`:831`). Those are Ch 25's offline-evaluation subjects. "Evaluation" means per-run acceptance scoring here and release gating in Ch 25, and neither chapter says so.

Figure 13-1's caption ("promotion happens outside it") uses release vocabulary for a runtime decision. Its graph also places the advisory evaluator *before* the deterministic gate, while the prose says executable checks run *before* any judge.

## Intended Reader Mental Model

- **Before:**
  - Ch 02: acceptance is not the model saying "done" (§ Deterministic acceptance).
  - Ch 10: the loop stops on external rules.
  - Ch 12: every plan node ends in acceptance checks, and the Acceptance Engine runs "deterministic checks and policy-approved model graders".
- **After:**
  - (a) Reflection is a bounded revision tool; it never accepts.
  - (b) Acceptance is decided by an independent component that runs executable checks first and treats calibrated judge scores as evidence.
  - (c) The revise loop has hard stops (pass, revisions, spend, deadline, no-progress) and escalates disagreement to a human.
  - (d) A judge never grants access or commits.
- **Missing pieces:**
  - (b) has no defined inputs or outputs.
  - The link "escalate → Ch 14 human" is implicit.
  - The reader is not told that release-time evaluation (Ch 25) is a different use of the same judges with its own calibration discipline.

## Section-by-Section Flow Review

**WHERE THE MORTGAGE CASE STANDS / THE DESIGN CHOICE (`:644–650`).**
- Good. The contradictory address and overstated confidence give one defect that is executable (the address mismatch can be detected deterministically) and one that is qualitative (confidence calibration). That is exactly the split the chapter teaches, but the chapter never points this out.
- There is no evidence-context blockquote; acceptable.
- Ch 10 `:43` already mentions "a contradictory address requires another authorized document". This is an available continuity thread that is not used (map S12).

**§ Why critique cannot certify its own answer (`:652`).**
- *Role:* intro.
- *Verdict:* adequate. It is the first of three framing headings.
- *Issues:* "evaluator and acceptance gate" introduces a third name (map T21: acceptance engine / gate / decision).

**§ Give evaluation its own independent path (`:659`).**
- *Role:* the independence argument.
- *Adds:* the shared-blind-spot reason (same model family, context, assumptions).
- *Verdict:* the shared-blind-spot sentence is the chapter's best "why".
- *Issues:* the second half (deterministic checks first; judges for qualitative criteria; scores as evidence) is repeated at `:672–674`. The state-owner table follows.

**§ Improve the answer without letting the system certify itself (`:668`).**
- *Role:* the mechanism.
- *Adds:* Figure 13-1, the reflection/evaluation questions (`:672`), the executable-check list (`:672`), judge versioning (`:674`), and "evidence, not permission" (`:674`).
- *Verdict:* the core of the chapter.
- *Issues:*
  - Its heading restates `:652`.
  - "A model score is evidence for a release or review decision" mixes runtime acceptance with release (Ch 25).
  - "measures variance, human agreement, and failure slices" is calibration methodology owned by Ch 25 § Layer tests from contracts to outcomes (`07-part-vii.md:319`).
  - The figure order conflicts with the text (judge first, gate after).

**§§ Bounded optimization loop (`:676`).**
- *Role:* the evaluator–optimizer loop.
- *Adds:* targeted structured feedback with a diff; five stop conditions; escalation "with both artifacts rather than silently choosing the more persuasive prose".
- *Verdict:* precise and good.
- *Issues:*
  - The escalation is the hook into Ch 14, with no pointer.
  - No-progress here is not tied to Ch 10's signatures (the same idea: a revision that changes wording but not the failing invariant, If-fails step 3).

**§ What the evidence lets us conclude (`:680`).**
- *Verdict:* generic EVIDENCE BOUNDARY box.
- *Issues:* R20 (MLflow evaluation docs) supports "tooling supports judges, datasets, and human feedback", but no sentence is tied to it. R13 supports no claim.

**§ How Reflection works in practice (`:688`) and H3s (`:694`, `:708`, `:715`, `:723`).**
- *Problem box:* restates the case box.
- *How the pattern works:* "It does not commit or certify protected outcomes" restates `:655`. The five steps are acceptable, but steps 1–2 and 5 equal Evaluator–Optimizer steps 1, 3, and 5.
- *Use when / Do not use when:* "Use when measured offline results show critique improves a specific quality dimension" is unique and important (critique must earn its cost).
- *Costs:* "correlated errors" restates `:661`.
- *Failure table:* "Self-confirmation" and "Evidence invention" are unique. "Stylistic churn" equals Evaluator–Optimizer "Endless revision".
- *Signals:* "defect taxonomy" and "quality delta" are unique.
- *Verdict:* about half of it duplicates the second card.

**§ How Evaluator–Optimizer works in practice (`:732`) and H3s (`:738`, `:752`, `:759`, `:767`).**
- *How the pattern works:* the five steps are the only ordered statement of the deterministic-first rule (step 2 before step 3). That is the procedure the prose describes but never orders.
- *Use when / Do not use when (`:750`):* "Do not use a model judge as sole authority for permissions, transaction success, security, or computable correctness" is near-verbatim with Ch 25 Q (`07-part-vii.md:489`) and with AP-10's thesis.
- *Failure table:* "Reward hacking → hidden holdout tests" and "Judge variance → repeated runs, ensembles" are offline-evaluation controls, which Ch 25 owns.
- *Signals:* good and unique (per-criterion scores, judge rationale).
- *Verdict:* this is the more complete card. Merge Reflection into it.

**§ A sensible place to start (`:776`) / §§ Bounded evaluator–optimizer (`:779`).**
- *Verdict:* contradicts the chapter (Overall Assessment, item 1).
- *Issues:* the empty H2 wrapper. There is no registered example for Ch 13 in `config/examples.json`.

**§ If this fails in production (`:815`).** Good and specific. Step 3 ("revisions that change wording but not the failing invariant") is the best definition of no-progress in the chapter and should appear in § Bounded optimization loop. Step 2 (judge variance across repeated runs and slices) is a Ch 25 activity; acceptable as a first diagnostic.

**§ What to verify before production (`:821`).** Items 1–3 are runtime and correct. Items 4 (judge calibration, inter-rater agreement) and 5 (regression corpus) are release-time (Ch 25). Keep them, but tag them as Ch 25 prerequisites.

**§ Put the idea to work (`:833`).** Good. Exercise 2 (reflection worsens a correct answer) is the right adversarial exercise. It also absorbs Ch 12's "critic repeatedly rewrites a correct result" failure.

**§ Questions to bring to design review (`:838`).** Q1, Q2, and Q5 are good. Q4 restates `:672`, which is acceptable. Q3 is fine. There is no question about who issues the AcceptanceDecision, which is the chapter's state owner.

**§ Where this leads next (`:848`).** "Automated evaluation can improve candidates; Chapter 14 identifies decisions that require explicit human authority, correction, or recourse." Adequate. It would be stronger if it named the escalation: when the evaluator and generator disagree, or the decision is protected, the next step is a human (Chapter 14).

## Sparse or Underdeveloped Content

- **AcceptanceDecision / acceptance engine.** Add one short subsection, about six lines, under the mechanism H2. It should say what the engine takes in (the candidate, authoritative state, criteria/rubric version), the order of checks (executable invariants, then calibrated judges only for qualitative criteria), what it returns (an `AcceptanceDecision`: accepted / rejected with defects / escalate, with each criterion's evaluator type and evidence references), and who may issue it (only the engine; never the generator or the judge). Cross-reference Ch 02 § Deterministic acceptance for Harborlight's concrete criteria, and Ch 15 § Terminal correctness for how the decision maps to the run terminal. **Do not** re-list Harborlight's criteria (that is Ch 02's) or the run-terminal states (Ch 15's).
- **Runtime versus release evaluation.** One sentence, not a section (C13-R05).
- No other expansion. Judge calibration methodology belongs in Ch 25 and should be cut from here, not grown.

## Missing Conceptual Connections

- **Ch 10 "acceptance engine decides" and Ch 12 Acceptance Engine row → Ch 13, missing "this chapter defines that engine."** Location: `:659`/`:668`.
- **Ch 02 § Deterministic acceptance → Ch 13, missing the back-reference ("Chapter 2 listed what Harborlight checks; this chapter defines who checks it and in what order").** Location: the new AcceptanceDecision subsection.
- **Ch 13 escalation (`:678`) → Ch 14 intervention, missing a pointer.** Ch 14 § Separate authorization from intervention describes intervention as "supply missing judgment". That is exactly what an unresolved generator/evaluator disagreement needs.
- **Ch 13 judges → Ch 25 calibration, missing "Chapter 25 § Layer tests from contracts to outcomes defines how judges are calibrated and gated for release."** Location: `:674`.
- **Ch 13 bounded revise loop → Ch 25 § Separate runtime adaptation from offline improvement, missing "the revise loop is runtime adaptation inside a fixed envelope; it never changes rubrics, judges, or thresholds."** Location: `:678`. Ch 25 Q2 (`07-part-vii.md:488`) states the envelope.
- **Ch 13 no-progress → Ch 10 no-progress signatures, missing one clause.** Location: `:678`.
- **Ch 13 "a model score is not permission" → AP-10; "model says done" → AP-07, missing card IDs.** Location: `:674`.
- **Case box → chapter rule, missing "the address contradiction is caught by an executable check; the overstated confidence needs a calibrated judge."** Location: the first sentence of `:672` or the case box.

## Transition Problems

- **In (Ch 12 → Ch 13):** Ch 12 closes on "independent evaluation and bounded revision". Ch 13 opens with no mention of plans or of the Acceptance Engine that Ch 12 just named, so the reader does not see that Ch 13 defines what decides each plan node. Add the bridge (C13-R02).
- **Within:**
  - Three framing headings in a row (`:652`, `:659`, `:668`).
  - The evidence section sits between the mechanism and the cards.
  - Two consecutive near-duplicate cards.
  - Code that contradicts both.
- **Out (Ch 13 → Ch 14):** the closing is adequate. Make the escalation explicit (C13-R07). Ch 14 then opens on authorization (a protected operation), while Ch 13's escalation leads to *intervention*. Ch 14's § Separate authorization from intervention resolves this. No change is needed in Ch 14.

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict |
| --- | --- | --- |
| Generator must not certify itself | design choice `:650`; `:654–657`; `:661`; heading `:668`; card `:696`; Q2 `:843` | `:661` is canonical (shared blind spot). The `:668` heading is redundant. The others are acceptable. |
| Deterministic checks first, judges for qualitative criteria | `:661`; `:672`; `:674`; card E–O steps 2–3 `:743–744`; card `:750`; checklist `:825`; Q4 `:845` | **Redundant within prose.** Keep `:672–674`, delete the second half of `:661`, and move E–O steps 2–3 into prose as the ordered procedure. |
| Score is evidence, not permission | `:661`; `:674`; card `:750` | Keep `:674`. |
| Bounded revision / stop rules | `:678`; Reflection step 5 `:702`; E–O step 5 `:746`; failure rows `:720`, `:765`; checklist `:827`; Q3 `:844` | Keep `:678`. Merge the two cards. |
| Correlated / shared blind spots | `:661`; Reflection cost `:712`; If-fails step 1 `:817`; Q2 `:843` | Acceptable reuse. |

## Cross-Chapter Duplication

| Concept | Here | Elsewhere | Verdict |
| --- | --- | --- | --- |
| Judge use and limits | `:674`; E–O card `:750`, `:763–764`; checklist `:829`; Q `:843–845` | Ch 25 § Judge the outcome and the path separately (`07-part-vii.md:279–293`), `:319`, COMMON PITFALL `:449`, Q `:489` | **Partly reinforcement, partly redundancy.** Proposed split: **Ch 13 = runtime** (inside one run: the revise loop, per-run acceptance, a judge as one input to the AcceptanceDecision); **Ch 25 = release** (datasets, calibration against human labels, blinding, bias/variance testing, release gates). Ch 13's "measures variance, human agreement" (`:674`) and the "reward hacking / holdout" and "judge variance / ensembles" controls (`:763–764`) are Ch 25 content: keep them as pointers. **Requires Ch 25 owner:** Ch 25 `:319` and Q `:489` should cite Ch 13 for the runtime rule and not restate "never the sole gate…"; the near-verbatim Q pair (map §5.2: Ch 13 `:843–845` ≈ Ch 25 `:489`) should keep the Ch 25 version (release framing) and Ch 13's Q4 (deterministic checks), which differ in focus. |
| Outcome/evaluator type recorded with result | — | Ch 25 `:292` ("The evaluator type belongs in the result"); `EvalScore` "deterministic or grader type/version" (`:379`) | **Reinforcement opportunity.** The proposed AcceptanceDecision should record the evaluator type per criterion, with a pointer to Ch 25's `EvalScore` as its offline counterpart. Do not define a new evaluation record beyond AcceptanceDecision (map T23 already flags record proliferation). |
| Acceptance engine | State owner `:666` | Ch 02 § Deterministic acceptance (`01-part-i.md:728`); Ch 02 Q (`:889`); Ch 10 `:41`; Ch 12 `:487`, `:499`; Ch 15 § Terminal correctness; AP-07 (`04-part-iv.md:1815`); Ch 18 rule "Termination" (`05-part-v.md:81`) | **Scattered, with no home** (map §3: "Ch 02 (expand) or Ch 13"). **My recommendation:** Ch 02 keeps the *what* (Harborlight's criteria); Ch 13 becomes canonical for the *component* (inputs, order, AcceptanceDecision, sole issuer); Ch 15 owns the run terminals. AP-07's terminal list (`accepted, blocked, needs-input, failed, unknown-effect`) should then cite Ch 13/15 (**requires Ch 16/17 owner**). |
| Ch 01 vocabulary pointer | — | `01-part-i.md:450`: "Acceptance criteria … Chapters 10 and 12" | **Misdirection.** **Requires Ch 01 owner:** change it to "Chapters 2 and 13". |
| Judge as security gate | `:674`, `:750` | AP-10 (`04-part-iv.md:1681`) | **Reinforcement.** AP-10 adds the injection argument (the judged content can address the judge). Add "(AP-10)" at `:674`; do not import the argument. |
| Model says done | `:655–657` | AP-07 (`:1809`) | **Reinforcement.** Cross-reference. |
| Pattern catalog coverage | Two cards | Ch 16 has no reflection or evaluator–optimizer P-card; Appendix A item 7 covers only "post-deployment improvement" (`09-appendices.md:18`), which is Ch 25 | **Gap.** **Requires Ch 16/17 owner:** overall-book-review.md §D-04 resolves this: no new P-card; reflection and acceptance get an obligation-table row (C16-R10), and the "at a glance" chapter card is the canonical summary. Appendix A should gain a row "Quality / acceptance → Ch 13; AP-07, AP-10". [verified: the two options offered here are superseded by D-04] |
| Planner/critic churn | — | Ch 12 Required-analysis row `:427` ("critic repeatedly rewrites a correct result") | Belongs here (exercise 2 covers it). Removed from Ch 12 by C12-R08. |

## Structural Recommendations

1. **One framing H2, one mechanism H2.** Merge `:652` and `:659` into the intro, keep the shared-blind-spot argument, and rename `:668` to something that names the mechanism, e.g., "Reflection revises; an acceptance engine decides".
2. **Under the mechanism H2:** Figure 13-1; the reflection/evaluation questions; § The acceptance decision (new, about six lines); § Bounded optimization loop with the E–O steps moved in and the no-progress definition from If-fails step 3.
3. **Merge the two cards** into one "Reflection and evaluator–optimizer at a glance" (shared card policy, C10-R04).
4. **Replace the inline code** with a registered example that implements the chapter's rule.
5. **Draw the Ch 25 boundary** in one sentence and move calibration methodology there by pointer.

## Concrete Recommended Changes

**C13-R01 — Priority: Critical — Action: Rewrite (code)**
- **Location:** `04-part-iv.md:776–813`, § A sensible place to start / § Bounded evaluator–optimizer.
- **Issue:** the evaluator accepts its own verdict. There is no deterministic check first, no no-progress stop, and no escalation. It is unregistered inline code with defects.
- **Why it matters:** the only code in the chapter teaches the self-certification the title forbids.
- **Change:**
  - Create `examples/patterns/evaluator_optimizer.py`, register it in `config/examples.json` (chapter 13) with a behavioral test, and replace the fenced block with `[[EXAMPLE:evaluator-optimizer#core]]`.
  - The core region must show:
    - (a) `deterministic_checks(candidate)` runs first and its failures become structured feedback;
    - (b) a judge returns a score and rationale only (no `accepted` field);
    - (c) a separate `AcceptanceEngine.decide(candidate, checks, scores) -> AcceptanceDecision` (accepted / rejected / escalate);
    - (d) the loop stops on accepted, maximum revisions, spend or deadline, or no-progress (the same failing invariants as the previous revision);
    - (e) it returns `escalate` with both candidate versions instead of raising.
  - Use `@dataclass(frozen=True)` and import only what is used.
  - Add one lead-in line: "The judge supplies evidence; only the acceptance engine decides."
- **Related:** C13-R02; AGENTS.md code-listing rule.

**C13-R02 — Priority: High — Action: Add (short subsection)**
- **Location:** `04-part-iv.md`, a new H3 "The acceptance decision" inserted after `:674` (before § Bounded optimization loop).
- **Issue:** the Acceptance Engine and `AcceptanceDecision` are named (`:666`) and relied on by Ch 10 and Ch 12, but never defined.
- **Why it matters:** this is the component that turns "never self-approve" into an enforceable boundary, and readers have been deferred to it since Ch 01.
- **Change:** about six lines.
  - "The acceptance engine is the only component that may mark a candidate, a plan node (Chapter 12), or a ReAct answer (Chapter 10) as accepted."
  - It takes the candidate, the authoritative state it claims to satisfy, and a versioned set of criteria. It evaluates executable invariants first and calibrated judges only for criteria that cannot be computed.
  - It returns an `AcceptanceDecision`: accepted, rejected with typed defects, or escalate. For each criterion it records the evaluator type (deterministic or judge, with version) and evidence references.
  - "Chapter 2 § Deterministic acceptance lists what Harborlight checks; Chapter 15 § Terminal correctness maps the decision to the run's terminal state."
  - Do not re-list Harborlight's criteria or the terminal states.
- **Related:** C13-R08 (Ch 01 pointer); C10-R03; AP-07 (Ch 16/17 owner).

**C13-R03 — Priority: High — Action: Merge**
- **Location:** `04-part-iv.md:688–774`, § How Reflection works in practice and § How Evaluator–Optimizer works in practice.
- **Issue:** two overlapping cards.
- **Change:**
  - Delete both THE ENGINEERING PROBLEM boxes and both lead sentences.
  - Move the E–O five steps (`:742–746`) into § Bounded optimization loop as the ordered procedure, after its first sentence.
  - Create one H2 "Reflection and evaluator–optimizer at a glance" containing:
    - (a) a Use when / Do not use when table with two rows. Reflection: "when measured offline results show critique improves a specific quality dimension" / "when correctness is executable or the first pass meets the bar". Evaluator–optimizer: keep `:750`.
    - (b) one costs table: "Better completeness", "Structured critique", "Explicit rubric".
    - (c) one failure table: Self-confirmation, Evidence invention, Stylistic churn / endless revision (merged), Judge variance ("repeated runs and thresholds; calibration per Chapter 25"), and Reward hacking ("holdout tests and diverse scorers; Chapter 25").
    - (d) one signals list, the union of the two without duplicates.
  - Place it after the mechanism H2 and before § What the evidence lets us conclude.
- **Related:** shared card policy C10-R04, C11-R05, C12-R05.

**C13-R04 — Priority: Medium — Action: Merge / Rewrite (headings)**
- **Location:** `04-part-iv.md:652–674`.
- **Issue:** three framing headings carrying one idea, and the deterministic-first rule stated twice.
- **Change:**
  - Delete the `:652` heading and keep its paragraph as intro text. Change "evaluator and acceptance gate" to "evaluator and acceptance engine" (map T21).
  - Keep § Give evaluation its own independent path, but cut its last two sentences (`:661`, from "Start with deterministic checks…"), which `:672–674` cover.
  - Rename `:668` to "Reflection revises; an acceptance engine decides".
- **Related:** C10-R08.

**C13-R05 — Priority: High — Action: Rewrite (boundary with Ch 25)**
- **Location:** `04-part-iv.md:674`.
- **Issue:** runtime acceptance is mixed with release evaluation and calibration methodology.
- **Why it matters:** two chapters teach judge calibration, and the reader cannot tell which governs a per-run decision.
- **Change:** replace "Northstar measures variance, human agreement, and failure slices. A model score is evidence for a release or review decision; it is not permission to access data or commit a transaction" with:

  > "A judge used at runtime must already be calibrated: Chapter 25 § Layer tests from contracts to outcomes defines how judges are measured against human labels and gated for release. Inside a run, a judge score is one input to the acceptance decision; it is never permission to access data or commit a transaction (see AP-10)."

  At `:829`, append "(Chapter 25)" to checklist item 4. At `:831`, append it to item 5.
- **Related:** Ch 25 owner (Cross-Chapter Duplication).

**C13-R06 — Priority: Medium — Action: Rewrite (diagram)**
- **Location:** `assets/diagrams/src/pattern-reflection.gv`; Figure 13-1 caption at `04-part-iv.md:670` (and `config/diagrams.json`).
- **Issue:** release vocabulary ("promotion", "never self-promotes"), and the judge appears before deterministic checks.
- **Change:**
  - Caption: "Figure 13-1 — A bounded revise loop whose verdict is advisory; acceptance happens outside it".
  - Diagram: insert a node "Executable checks — schema · evidence · arithmetic · policy" between `pro` and `ev`. Relabel `ev` to "Judge — qualitative · advisory". Change the edge label " never self-promotes" to " never self-accepts". Relabel `gate` to "Acceptance engine — checks · judge evidence · human escalation".
  - Run `make diagrams`.
- **Related:** C10-R03 (a matching edge-label change in Figure 10-1).

**C13-R07 — Priority: Medium — Action: Add (clauses)**
- **Location:** `04-part-iv.md:678`, § Bounded optimization loop.
- **Issue:** missing links to Ch 10, Ch 14, and Ch 25.
- **Change:**
  - After "no-progress", add "(a revision that changes wording but not the failing invariant, the same signature test as Chapter 10)".
  - Change the last sentence to end "…escalates with both artifacts to a human intervention queue (Chapter 14) rather than silently choosing the more persuasive prose."
  - Add: "The loop is runtime adaptation inside a fixed envelope: it may revise the candidate, never the rubric, judge, or thresholds (Chapter 25 § Separate runtime adaptation from offline improvement)."
  - Then delete If-fails step 3's definition only if it becomes redundant. It reads as a diagnostic, so keep it.
- **Related:** C13-R09 (closing).

**C13-R08 — Priority: Medium — Action: Rewrite (requires Ch 01 owner)**
- **Location:** `01-part-i.md:450`, Ch 01 § The vocabulary this book assumes, row "Acceptance criteria".
- **Issue:** it points to Ch 10 and 12, which do not develop the concept.
- **Change:** set "Where it is developed" to "Chapters 2 and 13".
- **Related:** C13-R02; map §4 row 5.

**C13-R09 — Priority: Low — Action: Rewrite**
- **Location:** `04-part-iv.md:850`, § Where this leads next.
- **Change:** "Automated evaluation can improve a candidate but cannot settle every decision. When the evaluator and generator disagree, or the action is protected, Chapter 14 puts a person where their judgment matters."
- **Related:** C13-R07.

**C13-R10 — Priority: Low — Action: Rewrite**
- **Location:** `04-part-iv.md:680–686`, § What the evidence lets us conclude.
- **Change:**
  - Replace the box with a one-row claim table. Claim: "Evaluation tooling". Grounded statement: "Current evaluation platforms support datasets, code-based and LLM judges, and human feedback; using judges only as evidence for an independent acceptance decision is this book's recommendation." Sources: R20.
  - Drop R13 from the source line.
- **Related:** C10-R10.

**C13-R11 — Priority: Low — Action: Add (one sentence)**
- **Location:** `04-part-iv.md:672`, first sentence.
- **Issue:** the case box's two defects illustrate the rule, but this is not stated.
- **Change:** after "Reflection asks… Evaluation asks…", add: "In the mortgage case, the contradictory address is caught by an executable check against the application projection; whether the recommendation overstates confidence is the kind of qualitative criterion a calibrated judge may assess."
- **Related:** map S12 (case continuity). If the synthesizer adopts a cumulative Part IV case thread (Ch 10 finds the address contradiction at `:43` → Ch 13 catches its omission), this sentence is the Ch 13 end of it.

**C13-R12 — Priority: Low — Action: Cross-reference** *Added in reconciliation (see overall-book-review.md §D-29).*
- **Location:** End of § If this fails in production.
- **Issue:** Same request as C05-R16.
- **Change:** Add one line: "If the model's own 'done' or a judge score is the acceptance decision, see AP-07 and AP-10 in Chapter 17."
- **Related:** C17-R03, C13-R05.

## Verification log

- **Line references checked:** 104 (every `:n` in this file, plus the Ch 01, Ch 02, Ch 10, Ch 12, Ch 14, Ch 15, Ch 16/17, Ch 18, Ch 25, Appendix A/H, and diagram pointers). Fixed: 1 (AP-07/AP-10 line numbers were paired in the wrong order in the context line). All others resolved within ±3 lines.
- **Claims removed:** none.
- **Claims softened:**
  - "no chapter says what the engine takes in, in what order it checks, or what it returns" → the order is at Ch 13 `:672`, a return set is at AP-07 `:1815`, criteria at Ch 02 `:730`, a gloss at Appendix H `:205`; what is missing is one consolidated definition, the inputs, and the sole-issuer rule.
  - Catalog-coverage row: the "add a P-card or note in Ch 16's intro" options are superseded by D-04.
- **Claims corrected:** unused imports in the inline code: all seven imported names at `:785–789` (`hashlib`, `json`, `dataclass`, `Awaitable`, `Callable`, `Protocol`, `AgentDecision`), not five.
- **Claims confirmed (most consequential):**
  - The inline evaluator–optimizer (`:783–813`) returns on `evaluation.accepted` (`:809–810`), runs no deterministic check, has no no-progress stop, and raises `RuntimeError` (`:812`) while `:678` says the workflow "escalates with both artifacts". `Generator`/`Evaluator` are undefined; `Evaluation` has no `@dataclass`. `config/examples.json` registers no example with `book_chapters: [13]`.
  - `pattern-reflection.gv`: `pro -> ev -> rev`, `ev -> gate [label=" never self-promotes"]`, `gate` labeled "External gate\ntests · policy · human"; the judge precedes the tests/policy gate, while `:672` says "executable checks before any model judge". Caption `:670` says "promotion happens outside it".
  - Three framing H2s at `:652`, `:659`, `:668`; the deterministic-first rule at `:661`, `:672`, `:674` (all verbatim as quoted).
  - `:750` "Do not use a model judge as sole authority for permissions, transaction success, security, or computable correctness" vs Ch 25 Q `07-part-vii.md:489` "not as sole authority for security, transactions, or computable correctness": near-verbatim as claimed.
  - `:674` "Northstar measures variance, human agreement, and failure slices. A model score is evidence for a release or review decision" is verbatim; Ch 25 `:319` and COMMON PITFALL `:449` own calibration; `EvalScore` `:379` records "deterministic or grader type/version"; `:292` "The evaluator type belongs in the result".
  - `01-part-i.md:450` points acceptance criteria to "Chapters 10 and 12"; Ch 02 § Deterministic acceptance at `:728`; Ch 15 § Terminal correctness at `04-part-iv.md:1150`; Ch 14 § Separate authorization from intervention at `:876` with "supply missing judgment" at `:878`.
  - Ch 16 P-01…P-12 contain no reflection or evaluator–optimizer card; Appendix A item 7 (`:18`) is "Post-deployment improvement: governed learning; never self-certification".
  - R20's registry scope is "evaluation datasets, feedback, judges, systematic evaluation, and production monitoring"; R13 and R20 stay cited in Ch 25 if dropped or kept here.
- **Recommendations amended:** the catalog-coverage row (D-04). C13-R02's values (accepted / rejected with typed defects / escalate) match D-12. C13-R08 matches D-12's "Chapters 2 and 13". No other change.
- **Not verifiable here:** the claim that the Reflection card is "about half" duplicate of the E–O card (a judgement; the overlapping rows and steps listed are accurate), and map references T21/T23/S12.
