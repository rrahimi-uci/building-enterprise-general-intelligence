# Chapter 25 — Improve the System Without Handing It Control: Continuity and Flow Review

Reviewed: `source/parts/07-part-vii.md:224–495`. Context read: Ch 24 close (`:205–222`), Ch 26 opening (`08-part-viii.md:1–77`). Cross-checked against Ch 13 (`04-part-iv.md:642–850`), Ch 07 § Test the contracts before you test the model and golden path (`03-part-iii.md:100–116`), Ch 27 § Promotion and continuous-improvement loop and design-review questions (`08-part-viii.md:251–264`, `:449–458`), Ch 26 risk tiers and owner table (`:42–70`), Ch 17 AP-15, the `mlflow-evaluation` and `mlflow-trajectory-evaluation` examples, `config/references.json` (R20–R26), and the `evaluation-gate`, `learning-loop`, and `runtime-offline` diagram sources.

## Overall Assessment

The first half of the chapter is strong:

- The candidate is "the versioned set", not a prompt.
- Deterministic failure blocks promotion and a judge cannot override an invariant.
- Outcome and path are evaluated separately.
- The slice-regression worked example matches the case box exactly.

The **ten-stage learning loop** with its "automation boundary" column is the book's canonical statement of front-matter principle 6 and is genuinely new.

The chapter loses shape after the worked example. The brief asked whether the late sections (§ Close the loop… through § Automate only when regressions are contained, `:387–436`) are repetitive or underdeveloped. They are both, unevenly:

| Section | Verdict |
| --- | --- |
| § Close the loop… | Substantive and canonical. Its cells are telegraphic and use six record names that this chapter never defines (ObservationRecord, DetectionEvent, LearningRecord, ValidationReport, PromotionDecision, causal hypothesis); five are defined nowhere in the book, while PromotionDecision is defined in Ch 27's records table (`08-part-viii.md:313`). It previews itself at `:253–257`, 130 lines earlier. It never walks the Harborlight regression through its stages. [verified: corrected — PromotionDecision has a definition in Ch 27] |
| § Separate runtime adaptation from offline improvement | **Underdeveloped.** One dense sentence pair carries one of the book's top invariants. It has no example, no test the reader can apply, and no link to Ch 13's in-run revision loop, Ch 06 memory writes, Ch 28 degradation, or Ch 23 kill switches. Its figure's runtime lane does not match its prose list. [verified: softened — the lists differ; see the section review] |
| § Choose the right improvement path | Unique and useful. It lacks one sentence telling the reader how to use it. |
| § Measure both the outcome and the path | **Redundant.** It repeats § Judge the outcome and the path separately (concept), the evidence context (vendor list), and Ch 24's scorecard (metrics), and adds only the sentence "no framework score is release authority". |
| § Automate only when regressions are contained | **Redundant in its first half** (it restates the Learn stage, the BEST PRACTICE box, and `:337–339`). **Unique in its second half**: the require-human list and the prohibit list. The heading does not describe the content. |

Three structural problems sit around these sections:

1. § A workable implementation (`:341–381`) sits between the worked example and the loop. Half of it is Ch 24's telemetry infrastructure.
2. Ch 13's run-level evaluator and this chapter's release-level evaluation are never distinguished. As a result, the judge-discipline rules are restated six times in this chapter (`:269`, `:288–293`, `:319`, `:443`, `:447–449`, `:489`), on top of Ch 13's several statements (`04-part-iv.md:661`, `:672–674`, `:829`, `:842–845`). [verified: corrected — "Ch 13's four" undercounted; Ch 13 states the rule in prose, checklist, and three review questions]
3. The MLflow material is honest and pinned. But the evaluation example reports *means only*, which is the failure the chapter warns against. The trajectory example's only scorer that touches authorization is a model judge whose instruction asks whether tool calls stay "within the authorized trajectory"; its docstring positions the judge as evidence that "cannot override authorization… invariants", so it does not contradict the rule as a gate, but the example ships no deterministic authorization check at all. Neither example demonstrates the mortgage case's slice regression. [verified: softened — "contradicts" overstated; the module docstring already subordinates the judge]

## Intended Reader Mental Model

After this chapter the reader should hold:

- **What:** release-level evaluation compares an immutable *candidate system version* (prompt, route, workflow, tools, policy, context strategy, configuration) against a pinned baseline. It does this over an immutable dataset with slices, and records a reproducible ReleaseGateDecision.
- **How it differs from Ch 13:** Ch 13 evaluates one *artifact inside one run* to decide that run's acceptance. Ch 25 evaluates *the system across many runs* to decide promotion. The same discipline applies at both levels (deterministic first, calibrated judges for nuance, no self-certification). Ch 25 adds datasets, slices, baselines, repeated runs (pass^k), and judge calibration over time.
- **Why:** averages hide high-consequence slice regressions, and a lucky outcome can hide an unsafe path.
- **How:** layered tests from contracts to production, outcome and trajectory scorers over Ch 24 traces, slice comparison, and a risk-tiered gate whose deterministic failures cannot be waived away. Then the governed loop: Observe → … → Learn.
- **When (the boundary):**
  - **Runtime adaptation** chooses among pre-approved options inside a fixed envelope. It outlives no run and widens nothing.
  - **Any change that outlives the run** or alters the envelope is an offline release.
- **Trade-offs:** evaluation cost, judge variance, dataset leakage and privacy, and slower experimentation (made cheap by pre-built replay sets, per AP-15).
- **Relationships:**
  - Ch 24 supplies traces.
  - Ch 26 supplies the risk tier and exception (waiver) authority.
  - Ch 27 executes promotion and rollback.
  - Ch 13's failed candidates feed the regression corpus.
- **Practice:** build an immutable five-case dataset with trajectory expectations, plus deterministic scorers that block forbidden-tool attempts and unknown effects.

The text delivers What, Why, and the gate well. The Ch 13 relationship, the runtime/offline test, and the Ch 26 waiver link are missing.

## Section-by-Section Flow Review

**Opening callouts (`:226–234`)**
- The evidence context names five vendors and states the durable contract ("dataset + release graph + scorer versions + trace/effect evidence"). "Release graph" is an undefined T7 variant.
- The case box and design choice are precise and set up the worked example. Good.

**§ Why improvement needs a governed feedback loop (`:236–242`)**
- *Role:* intro, and the first statement of "average improves while a slice gets less safe."
- *Verdict:* fine.
- *Issue:* this is where the Ch 24 → Ch 25 bridge belongs: the trace is the evidence the loop starts from (C25-R02).

**§ A safe improvement loop starts with evidence (`:244–269`)**
- *Role:* defines the candidate, previews the loop, Figure 25-1 (evaluation gate), the state-owner table, and "the gate is not a single score."
- *Adds:* the candidate-as-versioned-set idea and the deterministic-blocks rule. Both are essential.
- *Issues:*
  - The heading says "loop", but the figure and two of the three paragraphs are about the *gate*.
  - The loop preview (`:253–257`) lists the stages that § Close the loop… details 130 lines later.
  - The state-owner table's "Feedback" contract is defined nowhere (it is an MLflow entity name).
  - Figure 25-1 shows a "Waiver required" path that the prose never explains. It is Ch 26's exception mechanism.
  - This is the right place to state the Ch 13 / Ch 25 distinction, and it is absent.
- See C25-R02, C25-R10, C25-R15.

**§ Use evaluation to guide engineering decisions (`:271–277`)**
- *Role:* eval-case anatomy and MLflow capability.
- *Adds:* `:275` (case inputs, fixtures, allowed and forbidden tools, budgets, failure injections, slice tags; result contents) is the most concrete definition in the chapter.
- *Issues:*
  - `:273` is the fourth statement of averages-hide-regressions (after the box `:230`, `:241`, and `:265–268`). [verified: corrected — the order was inverted; `:265–268` precedes `:273`]
  - `:277` (MLflow 3.15.x features, the 3.15.2 pin) is product detail inside a conceptual section and duplicates the evidence row at `:442`. Its feature claims ("adds immutable evaluation-dataset versions and scorer ensembles") exceed R21's recorded scope ("Pins the reproducibility baseline").
- See C25-R10, C25-R12.

**§ Judge the outcome and the path separately (`:279–293`)**
- *Role:* the canonical outcome-versus-trajectory distinction (agrees with the concept map).
- *Verdict:* paragraph 1 is excellent.
- *Issue:* paragraph 2 (`:288–293`) re-teaches Ch 13 § Give evaluation its own independent path (`04-part-iv.md:661`) and § Improve the answer… (`:672–674`). Only the final sentence (record the evaluator type in the result) is release-specific (C25-R02).

**§ Evaluation pyramid (`:295–303`) and § Layer tests from contracts to outcomes (`:305–319`)**
- *Role:* test layering.
- *Issue:* two lists with different level sets: 7 bullets (Contract/unit, Simulation, Trajectory, Threat, Reliability, Performance, Canary) against 9 table rows (Unit, Contract, Component, Workflow, Simulation, Security, Regression, E2E, Continuous). Ch 07 Figure 7-5 has a third (4 tiers). The reader cannot tell which is authoritative.
- `:319` restates the judge rules a third time. Only "pass^k or equivalent" is new.
- AgentDojo is named without a registry citation (concept map §8, Appendix E row).
- See C25-R06.

**§ Worked example — average improvement, protected-slice regression (`:321–339`)**
- *Role:* anchors the case box.
- *Verdict:* strong, and the "volume cannot dilute the risk tier" row is the chapter's best line.
- *Issues:*
  - "Unauthorized LOS lookup" will puzzle a reader fresh from Ch 20–22. The Tool Gateway would deny it at runtime, so why is it a release blocker? The chapter never says that the *attempt* is the deterministic trajectory failure, and why relying on the runtime deny is not acceptable.
  - "Release graph" (`:334`) is undefined (T7).
  - The diagnosis row is Ch 24's method, which the example does not cite.
- See C25-R07.

**§ A workable implementation (`:341–381`), with § Who should own each decision, § The contracts between components, § Records worth preserving**
- *Role:* the reference tables.
- *Issues:*
  - **Placement.** These tables sit in the middle of the argument, before the loop they implement.
  - **Content belonging to Ch 24.** Telemetry Gateway/Collector, Trace Index, Content Vault, Metrics/SLO Pipeline, Replay/Fork Service; OTLP ingest, `GET …/trace`, `:forkReplay` (which collides with Ch 04's `:fork`); TraceIndex, SpanEnvelope, ContentBlob.
  - **Record names.** The records table defines EvalScore, while the loop and `:430` use EvaluationResult (the name Ch 04, 07, and 13 use). ValidationReport (used by Ch 07, 20, and 26) is not defined here, although this chapter's Validate stage produces it.
- See C25-R01, C25-R08.

**BEST PRACTICE (`:383–385`)**
- Good content. It is the second of three statements of "grow the set from incidents" (`:337–339`, `:385`, `:436`). Keep it, placed with the Learn stage (C25-R09).

**§ Close the loop without handing control to the model (`:387–404`)**
- *Role:* the canonical learning loop.
- *Adds:* the automation-boundary column. This is unique and important.
- *Issues:*
  - Six undefined record names (see Overall Assessment).
  - "Risk class" in Approve should be the Ch 26 governance risk tier (T11).
  - Figure 25-2 labels Approve "human", while the row allows pre-approved low-risk classes to auto-approve.
  - The Deploy and Monitor rows overlap Ch 27 § Promotion and continuous-improvement loop (`08-part-viii.md:251–264`) without a cross-reference.
  - The Harborlight regression is never walked through the stages, so the loop reads as an abstract taxonomy.
- See C25-R08, C25-R09.

**§ Separate runtime adaptation from offline improvement (`:406–410`)**
- *Role:* states the boundary.
- *Verdict:* underdeveloped relative to its weight. It is the subject of checklist item 1 and Q2.
- *Issues:*
  - **Missing content:** a test the reader can apply; a Harborlight example; the relation to Ch 13 (in-run revision improves an *artifact* and is runtime), to Ch 06 (a memory write within policy is a governed runtime data effect, while changing memory policy is offline), and to Ch 28 degradation and Ch 23 kill switches (runtime controls inside the envelope).
  - **Figure 25-3 versus prose.** The runtime lane says "Retrieve more context, Retry within budget, Escalate to a human" (`runtime-offline.gv:13–15`). The prose says "selects only pre-approved routes/fallbacks, reduces optional context, sheds load, stops a loop, asks for input, escalates, or rolls back". Only "Escalate" appears in both; "Retrieve more context" has no counterpart and points the opposite way from "reduces optional context"; "Retry within budget" is absent from the prose. The figure's key message, the dashed arrow "evidence, not a change" (`:28`), appears nowhere in the book's prose (grep). [verified: made precise]
  - **Order.** The section belongs *before* the loop: first establish what may change without a release, then describe the loop that governs everything else.
- See C25-R03, C25-R04.

**§ Choose the right improvement path (`:412–426`)**
- *Role:* maps evidence to the layer to change.
- *Verdict:* unique and valuable. The "Deterministic code" row reinforces Ch 12 § What should be agentic.
- *Issues:* no lead-in explaining how the table is used (the Diagnose output selects the row; fix at the lowest layer that removes the cause). No row for evaluators and datasets, even though `:436` and Ch 26 (`08-part-viii.md:56`, "Evaluator/dataset truth") treat them as governed changes (C25-R14).

**§ Measure both the outcome and the path (`:428–432`)**
- *Role:* a vendor survey plus a metric list.
- *Verdict:* redundant. The concept is § Judge… (`:279`). The vendors are the evidence context (`:226`), and it names Phoenix, which Ch 25 does not cite (R23 is cited only in Ch 24). The metrics overlap Ch 24's scorecard.
- *Unique content:* "Normalize all into platform-owned EvaluationResult; no framework score is release authority."
- See C25-R05.

**§ Automate only when regressions are contained (`:434–436`)**
- *Role:* the automation policy.
- *Issues:*
  - Sentences 1–2 repeat the Learn stage, the BEST PRACTICE box, and the `regression-cases:propose` API.
  - Sentences 3–5 restate the automation-boundary column, then add genuinely new content: the require-human list (permission, policy, data, memory purpose, protected effects, model allowlist, topology, architecture, evaluator truth, training data, exceptions, wider promotion) and the prohibit list (expanding authority, disabling controls, editing audit evidence, changing approval requirements, promoting self-authored behavior).
  - The heading does not describe the content.
- See C25-R09.

**§ What the evidence lets us conclude (`:438–445`)**
- *Role:* two claims.
- *Verdict:* the MLflow baseline row is correctly worded ("not labeled latest"). The Evaluation-limit row is a fair evidence restatement.

**COMMON PITFALL (`:447–449`)**
- *Role:* judge calibration.
- *Verdict:* keep it as the *single* statement of judge discipline in Ch 25. It adds re-measurement when the judge's model changes and reporting agreement with every score. The other restatements should be cut.

**§ A sensible place to start (`:451–454`) and § MLflow trajectory evaluation (`:456–458`)**
- *Role:* the examples.
- *Issues:*
  - The H2 is empty and neither example has a lead-in.
  - `mlflow-evaluation` returns `…/mean` only, with no slices or baseline. That is the "average" the chapter warns about, and the text should say so.
  - `mlflow-trajectory-evaluation`'s `no_unknown_effects` reads the `effect.state` span attribute, which Ch 24 must name (C24-R02).
  - Its `tool_trajectory_judge` asks a model whether tool calls stay "within the authorized trajectory" (`mlflow_trajectory_evaluation.py:45–48`). By the chapter's own rule, authorization is a deterministic check; the example's docstring says the judge "cannot override authorization… invariants", but no deterministic scorer in the example checks authorization, so the judge is the only one that does. The test (`test_mlflow_trajectory_evaluation.py`) only asserts the judge's name and template variable. [verified: softened and made precise]
  - No example shows the worked example's forbidden-tool slice regression.
- See C25-R11.

**§ If this fails in production (`:460–464`)**
- Step 2 is Ch 24's first-divergence method. The section debugs a *run*, not the *evaluation system*. The failures that matter here are gate-passed-but-production-regressed failures: an unrepresentative dataset, a missing slice, leakage, judge drift, or a scorer bug (C25-R13).

**§ What to verify before production (`:466–476`)**
- Item 1 is good.
- Item 2 belongs to Ch 24.
- Item 4 ("release bundle") is Ch 27's term and concern.
- Item 5 (use-case inventory) is Ch 26's.
- No item checks dataset immutability and privacy review, judge calibration, or slice minimums (C25-R13).

**§ Put the idea to work (`:478–481`)**
- Exercise 1 is good.
- Exercise 2 ("rejects unknown effects and missing approvals") half-duplicates the shipped `no_unknown_effects` scorer. Point it at the forbidden-tool case instead (C25-R11).

**§ Questions to bring to design review (`:483–491`)**
- Q1 and Q2 are good.
- Q3 ≈ Ch 13's questions (`04-part-iv.md:842–845`).
- Q4 and Q5 ≈ Ch 27 Q1/Q2 (`08-part-viii.md:453–454`).
- Replace them with release-evaluation questions (C25-R13).

**§ Where this leads next (`:493–495`)**
- Accurate and a good handoff to Ch 26 (decision rights, tiers, exceptions).

## Sparse or Underdeveloped Content

- **§ Separate runtime adaptation from offline improvement (`:406–410`).** This is the only place in the book that operationalizes front-matter principle 6. It needs a test, an example, and links to Ch 06/13/23/28 (C25-R04). Do not add a new mechanism. The links are cross-references.
- **Loop walk-through.** The worked example's Diagnosis and Next-candidate rows are a mini-loop. One short paragraph after the loop table, mapping the Harborlight regression to Detect → Diagnose → Recommend → Validate → Approve → Learn, would make the loop concrete without new content (C25-R09).
- **Waiver.** The gate's third outcome appears in Figure 25-1, the `release-gates:evaluate` API ("waiver-required"), and ReleaseGateDecision ("waiver"), but no sentence explains it. One sentence linking it to Ch 26 exceptions is enough (C25-R15).
- **ValidationReport.** It is an orphan used by four chapters and produced by this chapter's Validate stage. Define it here in one record row (C25-R08).
- **Not sparse:** the test-layer table, the improvement-path table, and the records. Do not expand them.

## Missing Conceptual Connections

1. **Ch 13 run-level evaluation → Ch 25 release-level evaluation.** *Missing B:* "same discipline, different decision: Ch 13 accepts one artifact inside a run; Ch 25 promotes a system version across a dataset." Location: § A safe improvement loop starts with evidence (C25-R02). Without it, the repeated judge rules read as redundancy instead of reinforcement.
2. **Ch 13 failed candidates → regression corpus.** Ch 13's checklist says "Failed candidates and feedback enter a regression corpus" (`04-part-iv.md:831`). Ch 25 never names this as an Observe input. Location: the Observe row (C25-R08).
3. **Ch 24 trace → Ch 25 trajectory scorer.** *Missing B:* trajectory scorers read Ch 24 span attributes (e.g., `effect.state`), so missing attributes make a scorer blind. Location: § MLflow trajectory evaluation lead-in (C25-R11) and C24-R02.
4. **Ch 24 worked example → Ch 25 case.** Ch 24's Enterprise example row (`:102`) says a failed document request becomes a regression fixture. Ch 25 never picks this up. Location: § Why improvement needs a governed feedback loop (C25-R02).
5. **Runtime guard → release blocker.** *Missing B:* why an attempt the Tool Gateway would deny still fails the release. Location: worked example (C25-R07).
6. **Runtime adaptation → Ch 06 / 13 / 23 / 28 runtime controls.** Location: § Separate runtime adaptation… (C25-R04).
7. **Gate waiver → Ch 26 exception.** Location: § A safe improvement loop… (C25-R15).
8. **Loop Approve / Deploy / Monitor → Ch 26 tiers and Ch 27 promotion.** Location: loop table rows (C25-R08).
9. **Choose the right improvement path → Diagnose stage.** Location: the improvement-path lead-in (C25-R14).

## Transition Problems

- **In (Ch 24 → Ch 25).** The opening sentence ("follows a failure from trace to evaluation case to candidate release") is a good bridge. The case vignettes are disconnected, but one sentence fixes it (C25-R02).
- **Within:**
  - § Worked example → § A workable implementation drops from a decision story into reference tables, then resumes the argument with § Close the loop….
  - § Close the loop… → § Separate runtime adaptation… inverts the logical order: boundary first, then loop.
  - § Choose the right improvement path → § Measure both… goes back to measurement after the reader has moved on to change.
  - § Automate… ends the conceptual part with a run-on list rather than a conclusion.
- **Out (Ch 25 → Ch 26).** Good. Q4/Q5 (release bundle, rollback) and checklist items 4–5 pre-empt Ch 26/27 and blur the handoff. Removing them sharpens it (C25-R13).

## Redundant and Repetitive Concepts

| Concept | Occurrences in Ch 25 | Verdict / action |
| --- | --- | --- |
| Average improves, slice regresses | box `:230`, `:241`, `:265–268`, `:273`, worked example `:321–339` | Box, `:241`, and the example are R. `:265–268` is R (adds deterministic-blocks). `:273` sentences 1–2 are D; cut them. |
| Judge discipline (deterministic first, calibrate, never sole gate) | `:268–269`, `:288–293`, `:319`, evidence `:443`, pitfall `:447–449`, Q3 `:489` | Keep `:268–269` (gate rule), the evidence row, and the pitfall. Condense `:288–293` to a Ch 13 reference plus the evaluator-type rule. Cut `:319` to the pass^k sentence. Replace Q3. |
| Test layering | `:295–303`, `:305–318` | D. Merge into one table. |
| Outcome versus path | `:279–286`, `:428–432`, Q1 `:487` | `:428–432` is D (delete). Q1 is R. |
| Learning loop stages | `:253–257`, `:387–404`, Figure 25-2 | `:253–257` is D; reduce to one signposting sentence. |
| Failure → regression case | `:337–339`, BEST PRACTICE `:385`, Learn row `:404`, `:436` sentences 1–2, API `:367` | `:337–339` (example lesson), the box, and the API are R. `:436` sentences 1–2 are D. |
| Automation limits | Loop column `:395–404`, `:436`, Figure 25-3, checklist item 1, Q2 | Column and `:436` overlap; condense `:436` into a summary table (C25-R09). Checklist item 1 and Q2 are R. |
| Runtime adaptation list | `:410`, checklist `:468`, Q2 `:488` | R (short recall). Keep. |

## Cross-Chapter Duplication

| Other location | Overlap | Verdict | Owner / action |
| --- | --- | --- | --- |
| Ch 13 § Give evaluation its own independent path, § Improve the answer…, Evaluator–Optimizer card, Q (`04-part-iv.md:659–674`, `:732–774`, `:842–845`) | Deterministic-before-judge, calibration, no self-certification | R once the level distinction is stated; D as written (`:288–293`, `:319`, Q3) | Ch 13 owns run-level acceptance. Ch 25 owns release-level evaluation and adds the bridge (C25-R02). Ch 13 may add a forward pointer from its checklist item "Failed candidates… regression corpus" to Ch 25; the Ch 13 review decides. |
| Ch 07 Figure 7-5 and § Test the contracts before you test the model (`03-part-iii.md:112–116`) | Test pyramid (4 tiers) | D with drift | Ch 25 owns the single test-layer table (C25-R06). The Ch 07 review keeps its figure as a summary, captioned or pointed to Ch 25. |
| Ch 07 golden path "Evaluate" / "Improve" rows (`03-part-iii.md:104`, `:108`) | Eval and improvement in the developer path | R | Keep. |
| Ch 24 § A scorecard operators can actually use (`07-part-vii.md:121–132`) | Metric catalog | D with `:432` | Ch 24 owns the catalog (C24-R02). Ch 25 deletes `:432` and references it (C25-R05). |
| Ch 24 `:139`, `:147`, `:149–150`, Required-analysis cells | Grader calibration, eval queues, slices, leakage | Misplaced in Ch 24 | Ch 25 owns them. Ch 24 removes them (`:139` via C24-R07; the rest via C24-R08). The eval-queue bullet moves to Ch 25's implementation (C25-R01). [verified: corrected — `:139` is deleted by C24-R07, not C24-R08] |
| Ch 25 § A workable implementation telemetry rows | Ch 24's implementation | Misplaced | Move to Ch 24 (C25-R01 / C24-R01). |
| Ch 27 § Promotion and continuous-improvement loop "Learn" row and closing paragraph (`08-part-viii.md:262–264`); Ch 27 Q4 (`:455`) | Production evidence becomes a candidate, not a mutation | D | Ch 25 owns the learning loop. The Ch 27 review replaces the Learn row's explanation and Q4 with a reference to Ch 25 § Close the loop…. Ch 25's Deploy/Monitor rows point to Ch 27 for promotion mechanics (C25-R08). |
| Ch 27 Q1/Q2 (`08-part-viii.md:453–454`) | Release bundle, rollback | D with Ch 25 Q4/Q5 | Ch 27 owns them. Ch 25 removes Q4/Q5 (C25-R13). |
| Ch 26 risk tiers (`08-part-viii.md:60–70`), owner table "Evaluator/dataset truth" (`:56`) | Gate tiers; evaluator governance | R (forward reference) | Ch 25 uses "governance risk tier (Chapter 26)" and adds the evaluator row (C25-R08, C25-R14). |
| Ch 17 AP-15 (`04-part-iv.md:1845–1855`) | Model swap needs slice evaluation and replay sets | R | Keep. Cite AP-15 in the runtime/offline example (C25-R04). |
| Ch 04 § Run API `:fork` (`02-part-ii.md:169`) | `:forkReplay` | D (API collision) | Remove `:forkReplay` from Ch 25. Ch 24 references Ch 04 (C24-R01). |

## Structural Recommendations

Target order for Chapter 25:

1. Opening callouts.
2. § Why improvement needs a governed feedback loop, plus the Ch 24 bridge sentence.
3. § A safe improvement loop starts with evidence, retitled "A release gate starts with evidence". It gains:
   - the Ch 13 / Ch 25 distinction;
   - the waiver sentence;
   - "no framework score is release authority".

   The loop preview is cut to one sentence.
4. § Use evaluation to guide engineering decisions: the eval-case anatomy only. MLflow detail moves out.
5. § Judge the outcome and the path separately: paragraph 2 condensed; pointer to the Ch 24 scorecard.
6. § Layer tests from contracts to outcomes: one merged table; § Evaluation pyramid deleted.
7. § Worked example: attempt-versus-deny clarified.
8. *Moved up* § Separate runtime adaptation from offline improvement (expanded).
9. § Close the loop without handing control to the model:
   - the loop table with defined records;
   - a short Harborlight walk-through;
   - a three-row automation summary (absorbing § Automate only when regressions are contained);
   - the BEST PRACTICE box.
10. § Choose the right improvement path: lead-in plus an evaluator row.
11. *Moved down* § A workable implementation (evaluation components only).
12. Evidence, pitfall, § A sensible place to start (with lead-ins), and the rewritten If-fails, checklist, and questions; then next.

Delete § Measure both the outcome and the path and the § Automate only when regressions are contained H2 (its unique content is kept in step 9).

## Concrete Recommended Changes

**C25-R01 — Priority: High — Action: Move**
- **Location:** § A workable implementation (`:341–381`) and its three H3s.
- **Issue:** half of the rows are Ch 24's telemetry infrastructure. The section also interrupts the argument before the loop.
- **Change:**
  - Move these to Ch 24 per C24-R01: the owner rows Telemetry Gateway/Collector, Trace Index, Content Vault, Metrics/SLO Pipeline, and Replay/Fork Service; the API rows `POST /otlp/v1/traces…`, `GET /v1/runs/{run_id}/trace`, and `POST /v1/runs/{run_id}:forkReplay` (Ch 24 replaces the last with a reference to Ch 04 `:fork`); and the records TraceIndex, SpanEnvelope, and ContentBlob.
  - Keep Evaluation Registry, Evaluation Orchestrator, and Failure Mining Service; the eval-datasets, eval-runs, comparison, release-gates, and regression-cases APIs; and the records EvalDatasetVersion, EvalCase, EvalRun, EvalScore (renamed per C25-R08), ReleaseGateDecision, and ProductionSample.
  - Add a fourth H3, § What changes as usage grows, holding the bullet moved from Ch 24 `:147` (dedicated evaluation queues, tenant/candidate budgets, reproducible seeds, provider-rate awareness, early stop).
  - Move the whole H2 to just before § What the evidence lets us conclude (`:438`).
- **Owner:** Ch 24 receives the telemetry rows. Both reviews agree.

**C25-R02 — Priority: High — Action: Add / Condense**
- **Location:** § A safe improvement loop starts with evidence (after `:251`); § Judge the outcome and the path separately paragraph 2 (`:288–293`); § Layer tests… `:319`; § Why improvement needs a governed feedback loop (`:242`).
- **Issue:** the run-level versus release-level distinction is never stated, so the judge rules repeat as redundancy. The Ch 24 case is not picked up.
- **Why it matters:** the reader has just learned Ch 13's evaluator–optimizer. Without the distinction, Ch 25 looks like Ch 13 again.
- **Change:**
  - **Add the distinction.** Insert after `:251`: "Chapter 13 evaluated one candidate artifact inside a run to decide whether that run's result is accepted. This chapter evaluates a candidate version of the system across a dataset to decide whether it may be promoted. The discipline is the same — deterministic checks first, calibrated judges only for nuance, no self-certification — but the release decision adds immutable datasets, baselines, slices, and repeated runs."
  - **Condense Judge paragraph 2.** Replace `:288–293` with: "Apply Chapter 13's rule for which properties are checked deterministically and which may use a calibrated judge; at release level, also record the evaluator type and version in every result so a probabilistic opinion is never mistaken for a proof."
  - **Cut `:319`.** Keep only "Measure repeated-run reliability (pass^k or equivalent), not just best-of-one success." The calibration point stays in the COMMON PITFALL.
  - **Bridge from Ch 24.** Append to `:242`: "Chapter 24's traces are the starting evidence; a failed run such as its unresolved document request becomes a reviewed case here."
- **Related:** C25-R13 (Q3).

**C25-R03 — Priority: High — Action: Move (reorder)**
- **Location:** § Separate runtime adaptation from offline improvement (`:406–410`); § Close the loop… (`:387–404`); § Automate only when regressions are contained (`:434–436`); § A workable implementation (`:341`).
- **Issue:** the boundary comes after the loop it frames. Implementation sits mid-argument. The automation policy is a detached H2.
- **Change:** reorder to: worked example → § Separate runtime adaptation from offline improvement → § Close the loop without handing control to the model (absorbing § Automate… per C25-R09) → § Choose the right improvement path → § A workable implementation (per C25-R01). Delete § Measure both the outcome and the path (C25-R05).

**C25-R04 — Priority: High — Action: Rewrite (expand)**
- **Location:** § Separate runtime adaptation from offline improvement (`:406–410`) and Figure 25-3 (`assets/diagrams/src/runtime-offline.gv`).
- **Issue:** a core invariant gets one dense paragraph. The figure and prose disagree.
- **Why it matters:** readers need a test they can apply to any proposed change, and they need to place Ch 13's revision loop, memory writes, degradation, and kill switches on the right side of the line.
- **Change:** rewrite as four short paragraphs or one paragraph plus a two-column table.
  1. **Rule.** Runtime adaptation chooses among options that were approved before the run started (pre-approved routes and fallbacks, additional authorized context or dropping optional context, retry within budget, stopping a loop, asking for input, escalating, shedding load). It cannot expand permissions, purpose, data access, spend, tools, or model allowlists.
  2. **Test.** "If a change outlives the run, or widens the envelope, it is an offline release."
  3. **Placements.** Ch 13's bounded revision improves an artifact inside the run and is runtime. A memory write within memory policy is a governed runtime data effect (Ch 06), while changing that policy is offline. Ch 28 degraded modes and Ch 23 kill switches are runtime controls inside a pre-approved envelope.
  4. **Harborlight example.** Falling back to the pre-approved secondary model route when the primary is rate-limited is runtime adaptation. Making the cheaper route the default is an offline release that needs slice evaluation (AP-15).

  Then state the figure's message in prose: "Runtime outcomes feed the offline loop as evidence, never as a change."
- **Figure:** align the `runtime-offline.gv` runtime-lane labels with the rule's wording (e.g., "Use authorized context or drop optional context", "Retry or fall back within budget", "Stop, ask, or escalate"), then run `make diagrams`.
- **Related:** C25-R03. Checklist item 1 and Q2 stay as recall.

**C25-R05 — Priority: High — Action: Remove**
- **Location:** § Measure both the outcome and the path (`:428–432`).
- **Issue:** it duplicates § Judge…, the evidence context, and Ch 24's scorecard. It names Phoenix without citing R23 in this chapter.
- **Change:**
  - Delete the H2.
  - Move the sentence "Normalize all framework scores into a platform-owned EvaluationResult; no framework score is release authority" into § A safe improvement loop… after "it cannot override a protected invariant" (`:269`).
  - Delete the vendor survey (the evidence context `:226` already names the tools).
  - Delete the metric list. Ch 24's scorecard absorbs the metrics only listed here (C24-R02, as amended: tool-selection precision/recall, argument correctness, plan adherence, faithfulness/unsupported-claim rate, retrieval relevance/precision/recall/freshness, retry amplification, reviewer fatigue, user satisfaction). Add to the end of § Judge the outcome and the path separately paragraph 1: "Chapter 24's scorecard lists the outcome and trajectory metrics; here they are computed per case, per slice, against a baseline." [verified: amended — named the full set so the deletion is lossless]
- **Related:** C24-R02.

**C25-R06 — Priority: High — Action: Merge**
- **Location:** § Evaluation pyramid (`:295–303`) and § Layer tests from contracts to outcomes (`:305–318`).
- **Issue:** two test layerings in one chapter (7 versus 9 levels), plus Ch 07's 4-tier figure.
- **Change:** **Reconciled (see overall-book-review.md §D-11):** As stated, except the last bullet: Figure 7-5 (`test-pyramid`) is retired by C07-R04/R06 and not adopted here. Ch 07 points to this table (C07-R06); there is no figure.
  - Delete § Evaluation pyramid. Keep the table under § Layer tests from contracts to outcomes.
  - Fold in the bullets' unique items. Add "trajectory constraints (tools, order, evidence, budgets, handoffs)" to the Component row. Add a Performance row: "queue age, tokens, tool calls, latency, cost per accepted outcome, fairness | load and soak tests per slice". Add "canary with stop conditions" to End-to-end.
  - In the Security/adversarial row, either add a registry citation for AgentDojo or change it to "prompt-injection benchmark suites".
  - The Ch 07 review points Figure 7-5 to this table.
- **Related:** C25-R02 (`:319`).

**C25-R07 — Priority: Medium — Action: Rewrite**
- **Location:** case box (`:230`) and § Worked example — average improvement, protected-slice regression (`:321–339`).
- **Issue:** "unauthorized LOS lookup" conflicts with the reader's Ch 21–22 model, where the gateway denies it. "Release graph" is undefined.
- **Change:**
  - Change "produces an unauthorized LOS lookup" (`:324`) to "attempts an LOS lookup outside the case's eligible tool set". In the box (`:230`), change "introduces one unauthorized tool trajectory" to "introduces one attempted tool call outside the eligible set". [verified: amended — the box does not contain the "LOS lookup" phrase, so "the same change" needed its own wording]
  - After the table, add: "In production the Tool Gateway would deny the call, but the attempt is still a deterministic trajectory failure: the candidate's context or routing now pushes the model toward a forbidden action, and shipping it would turn a release defect into production denials and incidents that each depend on one control holding."
  - Replace "release graph" in the Diagnosis row with "release manifest" (T7). Add "(Chapter 24 § Debugging method)" to the same row.
  - Apply the same "release graph" fix to the evidence context (`:226`).

**C25-R08 — Priority: Medium — Action: Rewrite**
- **Location:** § Close the loop… table (`:393–404`); § Records worth preserving (`:369–381`); state-owner table (`:263`); Figure 25-2 (`learning-loop.gv`).
- **Issue:** orphan record names; T11 risk naming; overlap with Ch 27 not cross-referenced; figure/table mismatch on Approve.
- **Change:** **Reconciled (see overall-book-review.md §D-02):** As stated, except the Approve row: replace "Risk class" with "use-case tier × change class (Chapter 26)", not "governance risk tier".
  - **Loop table, output column:**
    - Observe → "ProductionSample linked to TraceIndex (Chapter 24), including failed candidates from Chapter 13".
    - Measure → "EvaluationResult".
    - Detect → "alert or containment action". Drop "DetectionEvent".
    - Diagnose → "causal hypothesis (owner-confirmed)".
    - Recommend → "ChangeBundle draft (Chapter 27)".
    - Validate → "ValidationReport".
    - Approve → "ReleaseGateDecision; PromotionDecision is recorded at promotion (Chapter 27)".
    - Deploy → "ReleaseManifest (Chapter 27)".
    - Learn → "reviewed EvalCase proposal and runbook update". Drop "LearningRecord".
  - **Approve row:** replace "Risk class" with "governance risk tier (Chapter 26)".
  - **Records table:**
    - Rename EvalScore to EvaluationResult, keeping the fields.
    - Add a ValidationReport row: "candidate digest, EvalRun comparisons, non-evaluation test results (contract, security, load, compatibility), slice regressions, ReleaseGateDecision ref; immutable". This defines the record Ch 07, 20, and 26 use.
  - **State-owner table:** replace "Feedback" with "EvaluationResult".
  - **Ch 27 cross-reference:** add one sentence after the loop table: "Chapter 27 executes the Deploy and Monitor stages as signed promotion through shadow and canary."
  - **Figure 25-2:** change the Approve label from "Approve\nhuman" to "Approve\nowner or pre-approved class", then run `make diagrams`.
- **Owner:** Ch 25 defines ValidationReport and EvaluationResult. The Ch 26 and Ch 27 reviews reference them rather than redefine them.

**C25-R09 — Priority: Medium — Action: Merge**
- **Location:** § Automate only when regressions are contained (`:434–436`); BEST PRACTICE (`:383–385`); § Close the loop… (`:387–404`).
- **Issue:** the automation H2 restates the loop column and the incident-to-case procedure. Its unique content is buried in a run-on paragraph, and the loop never touches the case.
- **Change:**
  - Delete the § Automate… H2.
  - At the end of § Close the loop…, add a three-row table, "What the loop may automate", built from `:436` sentences 3–5:
    - "Automate within the envelope": capture, approved redaction and scoring, anomaly detection, clustering, draft recommendations, tests, sandbox runs, approved canaries, halt, rollback.
    - "Require human governance": permission, policy, data, memory purpose, protected effects, model allowlist, topology, architecture, evaluator truth, training data, exceptions, wider promotion.
    - "Never permitted": expanding authority, disabling controls, editing audit evidence, changing approval requirements, promoting self-authored behavior.
  - Delete `:436` sentences 1–2.
  - Move the BEST PRACTICE box to directly after the new table.
  - Add one 3–4-sentence paragraph after the loop table walking the worked example. Slice evaluation *detects* the forbidden-tool attempt. Comparing traces and context manifests *diagnoses* the new retrieval path. The *recommendation* narrows retrieval and tool eligibility. Held-out, adversarial, and protected-effect suites *validate* it. The domain owner *approves*. The failing trace becomes a reviewed case (*learn*).

**C25-R10 — Priority: Medium — Action: Rewrite / Condense**
- **Location:** § A safe improvement loop starts with evidence (`:244–257`); § Use evaluation to guide engineering decisions (`:273`, `:277`).
- **Issue:** the heading does not match the content (gate, not loop). The loop is previewed 130 lines early. The averages point is restated a fourth time. MLflow product detail sits in a conceptual section.
- **Change:**
  - Retitle the H2 "A release gate starts with evidence".
  - Replace `:253–257` with one sentence: "Evaluation is the Measure and Validate stages of the governed learning loop described later in this chapter."
  - In `:273`, delete the first two sentences. Start at "That is why the dataset needs immutable cases…", rephrased as "The dataset therefore needs…".
  - Move `:277` to § A sensible place to start (C25-R11).

**C25-R11 — Priority: Medium — Action: Rewrite (and an example change)**
- **Location:** § A sensible place to start (`:451–454`), § MLflow trajectory evaluation (`:456–458`), § Put the idea to work exercise 2 (`:481`); examples `examples/observability/mlflow_evaluation.py`, `mlflow_trajectory_evaluation.py`.
- **Issue:** no lead-ins. The first example reports means only. The second checks authorization with a judge. The worked example's slice regression is not demonstrated.
- **Change:**
  - **Lead-in under § A sensible place to start.** Insert the `:277` paragraph (MLflow capabilities and the 3.15.2 pin), followed by: "The first example uses deterministic scorers over a two-case synthetic dataset and reports means; a real gate also compares each slice against a pinned baseline, as the worked example shows."
  - **Lead-in under § MLflow trajectory evaluation:** "The deterministic `no_unknown_effects` scorer reads the `effect.state` attribute that Chapter 24's tool spans record; it is a release blocker. The judge and built-in scorers add quality evidence and cannot override it."
  - **Example change** (repository change; it needs an updated behavioural test and the `config/examples.json` entry unchanged):
    - add a deterministic `forbidden_tool_absent` scorer that fails when a trace contains a TOOL span whose name is outside the case's `expectations["eligible_tools"]`;
    - reword `tool_trajectory_judge`'s instructions to judge necessity and efficiency only. Remove "stays within the authorized trajectory", which asks a probabilistic judge to rule on an invariant that `:288–293` and `:443` reserve for deterministic checks. [verified: softened — see Overall Assessment item 3]
  - **Exercise 2:** change to "Add a deterministic scorer that fails any case whose trace attempts a tool outside its eligible set, then show that a candidate with a better mean still fails the gate on one slice."
- **Related:** C24-R02 (the `effect.state` naming), C25-R07.

**C25-R12 — Priority: Medium — Action: Rewrite (citation scope)**
- **Location:** `:277` (moving per C25-R10/R11).
- **Issue:** "Version 3.15.2 adds immutable evaluation-dataset versions and scorer ensembles" and the list of 3.15.x capabilities exceed R21's recorded `supports` ("Pins the reproducibility baseline used for book examples"). R20 covers MLflow 3.x evaluation features generally.
- **Change:**
  - Attribute the general capabilities to R20.
  - For the 3.15.2-specific additions, either verify them against the 3.15.2 release notes and extend R21's `supports` in `config/references.json`, or remove the sentence.
  - If any vendor survey survives C25-R05, add R23 for Phoenix.
- **Related:** C24-R15.

**C25-R13 — Priority: Medium — Action: Rewrite**
- **Location:** § If this fails in production (`:460–464`), § What to verify before production (`:466–476`), § Questions to bring to design review (`:483–491`).
- **Issue:** the If-fails steps debug a run, not the evaluation system. Checklist items 2, 4, and 5 and questions Q3–Q5 belong to Ch 13, 24, 26, and 27.
- **Change:**
  - **If this fails in production.** Replace it with:
    1. The gate passed but production regressed: check whether the failing slice exists in the dataset, with enough cases.
    2. Check for train/test or benchmark leakage, and for judge drift since calibration.
    3. Run the scorer against a known-bad case to confirm it can fail.
    4. Add the production trace as a reviewed case before shipping a fix.

    Close with a pointer: "To debug the failing run itself, use Chapter 24 § Debugging method."
  - **Checklist.** Delete item 2 (Ch 24's checklist covers it). Reword item 4 to "Every promoted candidate has an immutable ValidationReport and ReleaseGateDecision; Chapter 27 pins them in the release bundle." Delete item 5 (Ch 26). Add:
    - "Datasets are versioned and immutable, and each production-derived case passed privacy, purpose, and leakage review."
    - "Judges report agreement with held-out human labels and are recalibrated when their model changes."
    - "Every protected slice has a minimum case count and its own threshold."
  - **Questions.** Replace Q3, Q4, and Q5 with:
    - "What separates Chapter 13's evaluator from a release gate?" — *one artifact and one run's acceptance versus a system version across a dataset with baselines and slices.*
    - "Why can a low-volume slice block a candidate that improves the average?" — *volume cannot dilute a risk tier; deterministic protected-action failures block regardless of share.*
    - "How does a production failure become a regression case without leaking data or the test set?" — *de-identification, purpose and leakage review, reduction to the smallest reproducible case, held-out partitioning, and dataset approval.*

**C25-R14 — Priority: Low — Action: Add**
- **Location:** § Choose the right improvement path (`:412–426`).
- **Issue:** no instruction for use, and no row for changing evaluators or datasets.
- **Change:**
  - Add a lead-in: "The Diagnose stage selects the row. Change the lowest layer that removes the cause, and prefer deterministic code when the decision has become stable."
  - Add a row: "Evaluators and datasets | Judge–human disagreement, leakage, missing slice | New scorer/rubric version, new cases, re-partition | Calibration on held-out human labels; evaluation-owner approval (Chapter 26)".

**C25-R15 — Priority: Low — Action: Add**
- **Location:** § A safe improvement loop starts with evidence, after `:269`.
- **Issue:** the waiver outcome in Figure 25-1 and the gate API is unexplained.
- **Change:** add one sentence: "A gate may return waiver-required for residual risk outside a protected invariant; the waiver is a Chapter 26 exception — scoped, owned, compensated, and expiring — never a way past a deterministic failure."

## Verification log

Second pass against `source/parts/07-part-vii.md:224–495`, the cited passages in Ch 04, 07, 13, 17, 22, 24, 26, 27, the `mlflow-evaluation` and `mlflow-trajectory-evaluation` examples and tests, `config/references.json` (R13, R20–R26), `config/examples.json`, `evaluation-gate.gv`, `learning-loop.gv`, `runtime-offline.gv`, `test-pyramid.gv`, and overall-book-review.md §11–§12.

- **Line references checked:** 71. Fixed: 0 (Ch 27 Q4 is at `08-part-viii.md:456`, cited as `:455`; within tolerance, left).
- **Claims removed:** none.
- **Claims softened / corrected:**
  - "Six record names that are never defined" → five; PromotionDecision is defined in Ch 27 (`08-part-viii.md:313`). Consistent with D-05, which gives PromotionDecision to Ch 27.
  - "Ch 13's four" judge-rule statements → "several" (prose `:661`, `:672`, `:674`; checklist `:829`; questions `:842`, `:843`, `:845`).
  - `:273` is the fourth, not the third, statement of averages-hide-regressions.
  - Trajectory judge "contradicts" the deterministic-authorization rule → the judge is already subordinated by the module docstring; the real gap is that no deterministic scorer checks authorization (Overall item 3, § A sensible place to start, C25-R11).
  - "Its figure disagrees with its prose" → the lists differ; only "Escalate" is shared.
  - C25-R07: the case box does not say "LOS lookup"; gave it its own replacement wording.
  - Cross-duplication row: Ch 24 `:139` is removed by C24-R07, not C24-R08.
- **Important claims confirmed (evidence):**
  - `mlflow_evaluation.py` `evaluate()` returns only `{scorer}/mean` (`:62–68`); DATASET has two cases, no slice tags, no baseline.
  - `no_unknown_effects` reads `span.attributes.get("effect.state")` (`mlflow_trajectory_evaluation.py:30`).
  - `tool_trajectory_judge` is a `make_judge` with the instruction "stays within the authorized trajectory" (`:43–50`).
  - R21 `supports` = "Pins the reproducibility baseline used for book examples"; R20 covers "evaluation datasets, feedback, judges, systematic evaluation, and production monitoring". The `:277` sentence "Version 3.15.2 adds immutable evaluation-dataset versions and scorer ensembles" has no scoped source (C25-R12 stands).
  - R23 (Phoenix) is cited only at `07-part-vii.md:11` (Ch 24); Ch 25's evidence context lists R20, R21, R22, R24, R25, R26.
  - AgentDojo appears at `:314` and `09-appendices.md:140` with no entry in `config/references.json`.
  - `learning-loop.gv:15` labels the node `Approve\nhuman`; the table row `:401` allows pre-approved low-risk classes to auto-approve.
  - `evaluation-gate.gv:27,44–47` draws the waiver path; "waiver" appears in prose only inside the API row `:365` and the ReleaseGateDecision row `:380`.
  - "release graph" appears three times book-wide (`:226`, `:334`, `09-appendices.md:155`) and never defined; T7 is ChangeBundle → ReleaseManifest → EnvironmentBinding → RunManifest.
  - Capitalised "Feedback" appears only at `:263`; `mlflow.entities.Feedback` is the MLflow class the trajectory example imports.
  - EvaluationResult is used in Ch 04 (`02-part-ii.md:44`), Ch 07 (`03-part-iii.md:58`), Ch 13 (`04-part-iv.md:666`), and Ch 25 (`:396`, `:430`); the records table defines EvalScore (`:379`). ValidationReport is used in Ch 07 (`:106`), Ch 20 (`06-part-vi.md:82`), Ch 25 (`:400`), and Ch 26 (`08-part-viii.md:27`, `:37`, `:57`) and defined nowhere.
  - Seven bullets at `:297–303` versus nine rows at `:309–317`; `test-pyramid.gv` has four tiers (contract and unit, evaluation sets, scenario simulation, live canary).
  - `:forkReplay` at `:366` versus Ch 04 `:fork` at `02-part-ii.md:169`.
- **Recommendations amended:** C25-R05 (names the full metric set absorbed by Ch 24), C25-R07 (box wording), C25-R11 (judge rationale softened). C25-R08's record changes are consistent with D-05 (ObservationRecord, DetectionEvent, LearningRecord dropped; PromotionDecision recorded in Ch 27) and D-02; C25-R06 with D-11; the heading retitle in C25-R10 is in D-32. The example change in C25-R11 keeps code in `examples/` with a test, and the diagram changes in C25-R04/R08 go through the `.gv` sources; no invariant is broken.
- **Not verifiable here:** the MLflow 3.15.2 feature claims at `:277` (need the release notes; C25-R12 option 1). Whether `make_judge` in MLflow 3.15.2 would actually run against a trace at evaluation time was not executed (the test deliberately avoids a provider call).
- **Note for the synthesizer:** the `.gv` header comments for the three Part VII figures carry different figure numbers from the manuscript markers (see the Ch 24 verification log); fix the comments when C25-R04/R08 edit those files.
