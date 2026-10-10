# Chapter 24 — Follow a Run from Request to Verified Outcome: Continuity and Flow Review

Reviewed: `source/parts/07-part-vii.md:1–222` (Part VII orientation `:1–7` and Chapter 24 `:9–222`). Context read: close of Ch 23 (`06-part-vi.md:1267–1303`), opening of Ch 25 (`07-part-vii.md:224–269`), Ch 26 opening (`08-part-viii.md:1–60`). Cross-checked against Ch 02, 06, 10–15, 18 "What you need to see in production" cards, Ch 07 § If this fails in production, Ch 16 P-09, Ch 17 AP-14, Ch 04 § Run API, Ch 06 § State taxonomy and storage, the five MLflow examples, and the `causal-trace` diagram source.

## Overall Assessment

The chapter has the right thesis: a trace has to explain *decisions*, not just latency, and it is diagnostic evidence, not audit proof. The worked example (the twelve-minute review that ends in an **Unknown** LOS effect) is the best passage in Part VII. It applies Ch 15 waits, Ch 14 human dwell, and Ch 22 reconciliation in one operator story.

It does not yet work as the **canonical home for observability** that the rest of the book points to. Ch 01's vocabulary, Ch 14's "live run graph", Ch 16 P-09, Ch 17 AP-14, and twelve pattern cards with "What you need to see in production" lists all point here. Four problems block that:

1. **The span schema is call-centric, not decision-centric.** § What the trace needs to connect lists Run, Model, Retrieval, Policy, Tool, Agent task, Approval, and Workflow spans. It has nothing for the decisions the earlier chapters made observable: routing (Ch 11), plan compilation and revision (Ch 12), step disposition and information gain (Ch 10), critique and acceptance (Ch 13), memory reads and writes (Ch 06), and security controls (Ch 20/23). The chapter's own OBSERVABILITY TIP says "Trace the decision, not only the call", but its schema mostly traces calls.
2. **Its implementation lives in Ch 25.** The Telemetry Collector, Trace Index, Content Vault, Metrics/SLO pipeline, Replay/Fork Service, OTLP ingest, `GET /v1/runs/{id}/trace`, TraceIndex, SpanEnvelope, and ContentBlob are all at `07-part-vii.md:347–375`. Figure 24-1 already draws "Trace index", "Audit ledger", and "Content vault" (`assets/diagrams/src/causal-trace.gv`), yet Ch 24's prose never names the content vault or the trace index.
3. **Ch 25 material leaks in.** Eval datasets, trajectory grading, LLM-judge failure, grader calibration, evaluation queues, and dataset leakage appear at `:98–101`, `:139`, `:147`, `:149–150`.
4. **The same enumerations repeat.** Span kinds are listed six times (`:56`, `:99`, `:106`, `:108–117`, `:195`, `:214`). Attribute lists appear three times (`:58`, `:108–117`, `:137`). The "questions a trace must answer" appear twice (`:46–50`, `:54`).

The debugging method (`:64–66`) is thinner than Ch 07's version of it (`03-part-iii.md:141–146`), although the concept map makes Ch 24 its canonical home. The MLflow section is honest about scope, but the three examples get no lead-in prose, and the version-specific MLflow detail sits in a conceptual section (`:58`).

Net: keep the thesis, the diagnostics-versus-audit split, the worked example, the scorecard, and the replay rule. Consolidate the enumerations into one span schema. Pull the telemetry implementation in from Ch 25, and push evaluation content out to Ch 25.

## Intended Reader Mental Model

After this chapter the reader should hold:

- **What:** a *causal run trace* is one root per run. It links spans and asynchronous links across queues, retries, resumptions, fan-out, and remote agents, and it is keyed by stable domain IDs (run, task, effect, release). Ch 16/17 called it the "causal run graph". The *trajectory* is the evaluation view of the same run (Ch 25).
- **Why:** final text and latency cannot say which decision changed the path. Without join keys every metric stays local (AP-14).
- **How:** a span schema covering every call *and every decision*, carrying version, policy, effect, and cost attributes. Governed references stand in for payloads. Regional collectors handle redaction and tiered sampling.
- **When:** diagnosis starts from the violated outcome or SLO, walks the critical path, splits time into queue, execution, human dwell, retry delay, and reconciliation, and then finds the first divergent decision.
- **Trade-offs:** richer capture improves diagnosis but adds privacy, storage, and access burden. Sampled diagnostics and loss-intolerant audit take separate paths.
- **Relationships:** four distinct records, each with its own owner:
  - the trace explains;
  - the audit ledger proves;
  - the effect ledger (Ch 22) is authoritative for effect state;
  - workflow history (Ch 15) is authoritative for execution state.

  The trace points to the other three and replaces none. The Ch 14 operator console's live run graph is a role-redacted view of this trace. Ch 25's scorers read these spans.
- **Practice:** instrument the Harborlight runtime so the five worked-example segments appear, and separate machine latency from human dwell.

The text delivers What, Why, and Trade-offs well. How is fragmented across repeated lists. The Relationships bullet is mostly missing: effect ledger versus audit ledger versus workflow history is never stated, and P-09, AP-14, and Ch 14 are never referenced.

## Section-by-Section Flow Review

**Part VII orientation (`:1–7`)**
- *Role:* frames the Part as "evidence that helps a team decide what to fix, what to release, and what to leave alone."
- *Verdict:* good, and appropriately short.
- *Issue:* it does not connect to what the reader has already accumulated. Twelve pattern cards told the reader what to "see in production", and Ch 13 introduced run-level evaluation. One sentence would turn Part VII into the place where those scattered signals become one trace and then release evidence (C24-R13).

**Opening callouts (`:11–19`)**
- The evidence context (OTel GenAI conventions in Development; Phoenix as one option) is correct and scoped.
- The case box states the operator's problem well and sets up the worked example. "Harborlight links the entire trajectory" overstates what the `mortgage-agents-mlflow` example implements: one read-only agent/tool loop (C24-R11).
- The design choice says "MLflow 3.15.x", while `:58` says "pinned MLflow 3.15.2". Use one formulation.

**§ Why a trace must explain decisions, not just latency (`:21–27`)**
- *Role:* intro. It names the causal question and the trace/audit separation.
- *Verdict:* fine. It is a single short paragraph and does not repeat the box at length.

**§ A useful trace tells the story of the run (`:29–50`)**
- *Role:* diagnostics versus audit, Figure 24-1, the state-owner table, and four operator questions.
- *Adds:* the core split. This is the chapter's main mental model.
- *Issues:*
  - The four questions (`:46–50`) overlap the six questions in the next section (`:54`).
  - The state-owner table's core contracts (TraceContext · SpanLink · AuditEvent) are never defined in the body. AuditEvent is defined nowhere in the book.
  - The section never says how the audit ledger relates to Ch 22's effect ledger or Ch 15's workflow history, though the worked example uses the effect ledger (`:85`).
  - No back-reference to P-09 or AP-14, which the reader met about 500 lines earlier as "causal run graph" (T22).
  - See C24-R03 and C24-R06.

**§ Follow one decision from request to outcome (`:52–58`)**
- *Role:* the retell-the-run questions, what a production trace links, and MLflow configuration.
- *Issues:*
  - `:54` re-asks `:46–50`.
  - `:56` enumerates span kinds that the table at `:108–117` gives authoritatively.
  - `:58` mixes product configuration (`mlflow.openai.autolog()`, `disable_openai_agent_tracer=False`, `RunConfig(trace_include_sensitive_data=False)`) with a required-attribute list that duplicates the span table and `:137`. The version-specific material belongs with the examples. The "disabled by default" claim also has no registry source scoped to it (R21 supports only "Pins the reproducibility baseline").
  - "Northstar" appears here (T1).
- *Verdict:* merge it into the previous section and move the MLflow material out (C24-R03, C24-R15).

**§ Privacy and reliability (`:60–62`)**
- *Role:* what not to put in traces; the collector path; sampled diagnostics versus complete audit.
- *Verdict:* correct but misplaced. It is an implementation concern sitting under a "follow one decision" heading. It is repeated by the trade-offs row (`:100`), the first scale bullet (`:143`), the checklist (`:199`, `:201`), and Q3 (`:216`).
- *Fix:* move it under the implementation section next to the Content Vault (C24-R01, C24-R03).

**§ Debugging method (`:64–66`)**
- *Role:* the canonical first-divergence method, per the concept map.
- *Adds:* the five time categories (queue, execution, human dwell, retry delay, reconciliation), which are valuable.
- *Issues:*
  - Three sentences are too sparse for the canonical home.
  - Ch 07 § If this fails in production (`03-part-iii.md:141–146`) is richer: it lists the categories of first divergent span (input classification, source/freshness, prompt, route, model, tool, arguments, policy, effect, approval, acceptance), says to diff against the nearest accepted run, and gives the rule "do not edit the prompt until the evidence locates the failing responsibility."
  - § If this fails in production (`:189–191`) restates this method again.
- See C24-R04.

**§ Worked example — diagnosing a slow mortgage-evidence review (`:68–90`)**
- *Role:* applies the method to Harborlight.
- *Verdict:* strong. It is concrete, safe-next-step oriented, and correctly shows Unknown → reconcile before retry (Ch 22 reinforcement).
- *Issues:*
  - The example does not visibly *follow* the method. Only the queue (3 min) and approval (4 min) durations are given, so the critical-path decomposition into the five time categories is implicit.
  - It never names the first divergent decision (the stale index snapshot).
  - "Human action authorization wait" (`:73`) is the T3 term.
- See C24-R05.

**§ Build observability around decisions and effects (`:92–102`)**
- *Role:* the Required-analysis table.
- *Verdict:* mixed. The Enterprise example row is on-thread (Harborlight) and gives the useful bridge to Ch 25 ("a failed document request becomes a regression fixture and sandbox replay").
- *Issues:* three cells import Ch 25 content: Design alternatives ("black-box outcome evals; trace/trajectory grading; deterministic simulators"), Recommended architecture ("Build eval datasets… score both outcomes and trajectories"), and Failure scenarios ("average success hides long-tail failures; LLM judge rewards style over correctness") (C24-R08). The "Recommended architecture" span list is the fourth span-kind enumeration.

**§ What the trace needs to connect (`:104–119`)**
- *Role:* the span schema, which should be the canonical one.
- *Issues:*
  - The schema is missing decision, memory, and security rows, and missing attributes that earlier cards require:
    - Ch 10: turn index, information gain, stop reason.
    - Ch 11: candidate routes, eligibility removals.
    - Ch 12: plan digest, replan diff.
    - Ch 13: scorer versions, acceptance decision.
    - Ch 06: memory ID, TTL.
    - Ch 15: workflow build, timer/wait, signal source.
    - Ch 18: grant lineage, join condition.
    - Ch 23: taint label, egress decision.
  - The Tool row says "effect receipt" but not effect *state*. Ch 25's `no_unknown_effects` scorer reads `effect.state` from spans (`examples/observability/mlflow_trajectory_evaluation.py`).
  - The chain-of-thought paragraph (`:119`) is good and unique.
- See C24-R02.

**§ A scorecard operators can actually use (`:121–132`)**
- *Role:* the eight-dimension operator scorecard.
- *Verdict:* valuable. These are exactly the dimensions Ch 25's checklist requires evaluation to cover (`:472`).
- *Fix:* make this the book's single metric catalog. Fold in the metrics that only Ch 25 § Measure both the outcome and the path lists (`:432`): tool-selection precision/recall, argument correctness, plan adherence, faithfulness/unsupported-claim rate, retry amplification, reviewer fatigue. Then Ch 25 can delete that section (C24-R02, C25-R05).

**§ Trace and replay semantics (`:134–139`)**
- Bullet 1 (W3C propagation and span links) is unique and good.
- Bullet 2 repeats the attribute list.
- Bullet 3 states the replay rule correctly but does not distinguish Ch 15 workflow replay (recorded activity results, `04-part-iv.md:1235`) from diagnostic replay and from a fork (Ch 04 § Run API `POST /v1/runs/{id}:fork`, `02-part-ii.md:169`). Ch 25 later names the same operation `:forkReplay` (`:366`).
- Bullet 4 is evaluation (grader versions, calibration) and belongs to Ch 25.
- See C24-R07.

**§ What changes as usage grows (`:141–150`)**
- *Role:* scale guidance.
- *Verdict:* most bullets are telemetry-specific and good (tiered sampling, cardinality, retention).
- *Issues:* `:147` (evaluation queues) is Ch 25's Evaluation Orchestrator. `:149`'s slice-comparison sentence and `:150`'s "evaluator disagreement, and dataset leakage" are Ch 25 concerns. It should sit under the implementation H2 (C24-R01, C24-R08).

**OBSERVABILITY TIP (`:152–154`)**
- It restates the H2 title at `:21` and `:119`. It is acceptable as the one callout, but it is the third statement of the same line.

**§ What the evidence lets us conclude (`:156–162`)**
- A single scoped claim (R19). Fine.

**OBSERVABILITY TIP (`:164–166`)**
- Redundant. "Tag every trace with the identifiers your system of record uses" restates `:49` and the Run span row, and it sits awkwardly between the evidence and examples sections (C24-R10).

**§ A sensible place to start (`:168–171`)**
- An empty H2 followed directly by `[[EXAMPLE:mlflow-tracing]]` with no prose.
- The reader gets no statement of what the example shows: manual TOOL/AGENT spans plus a decision attribute.
- See C24-R11.

**§ MLflow tracing integration (`:173–175`)**
- Example only, with no lead-in.
- `mlflow-trace-configuration` shows autolog plus explicit platform spans, with the context-manifest ID recorded instead of the body. That is exactly the point `:58` and `:62` make in prose. Move the `:58` MLflow sentences here as its lead-in.

**§ Mortgage Agents SDK integration (`:177–185`)**
- The only example with prose, and the prose is clear and honest ("without claiming a live provider call").
- *Issue:* it does not say that the platform-owned spans the worked example depends on (queue, policy, approval, connector effect) are absent from this example. They are added with the explicit-span pattern of the previous example. That gap is the natural exercise.

**§ If this fails in production (`:187–191`)**
- It restates the debugging method.
- It should instead cover failures *of the observability system*: broken links at async/A2A boundaries, spans missing version attributes, collector drop or redaction failure, audit-path backpressure. The chapter already names these at `:101` and `:150` (C24-R09).

**§ What to verify before production (`:193–203`)**
- Good and specific.
- *Issue:* the first item enumerates span kinds again. Reword to "every span type in the schema" once that table is canonical.

**§ Put the idea to work (`:205–208`)**
- Both exercises are good and on-case.
- *Fix:* exercise 1 should point at the span schema. The mortgage example is the natural starting artifact.

**§ Questions to bring to design review (`:210–218`)**
- Five questions; Q1 and Q2 overlap (root trace versus why nesting is insufficient).
- Q5 is reinforcement.
- There is no question on the trace / effect ledger / audit distinction, which is the chapter's most important relationship (C24-R16).

**§ Where this leads next (`:220–222`)**
- Accurate. It sets up Ch 25's outcome/trajectory and release question.

## Sparse or Underdeveloped Content

- **§ Debugging method (`:64–66`).** This is the canonical home for first-divergence debugging, but it holds three sentences. It needs the divergence categories and the "diff against the nearest accepted run; don't edit the prompt first" rule, both currently in Ch 07 (`03-part-iii.md:143–146`). Write it as an ordered method the worked example visibly follows (C24-R04).
- **Implementation.** There is no owner/contract/record treatment. The components exist in Ch 25 and in Figure 24-1 (C24-R01).
- **Decision spans.** Routing, plan, step-disposition, and acceptance decisions are not in the schema (C24-R02).
- **Audit ledger.** It appears as a figure node and a contract name (AuditEvent) but is never described: who writes it, what makes it loss-intolerant, where it lives. A one-row record plus a cross-reference to Ch 06 § State taxonomy and storage (`02-part-ii.md:690`, "append-only/WORM archive") is enough (C24-R12). Do not add a new section.
- **Not sparse:** the scorecard and scale bullets. Do not expand them.

## Missing Conceptual Connections

1. **Pattern-card signals → span schema.** The twelve "What you need to see in production" lists (`01-part-i.md:820`, `02-part-ii.md:822`, `04-part-iv.md:106`, `:251`, `:295`, `:589`, `:723`, `:767`, `:1021`, `:1302`, `05-part-v.md:196`, `:240`) are never consolidated. *Missing B:* "those lists are attributes on these span types." Location: after the table in § What the trace needs to connect (C24-R02).
2. **P-09 / AP-14 → Ch 24.** P-09 (`04-part-iv.md:1457`) and AP-14 (`:1839`) promise "one causal run graph". Ch 24 never says it is that graph. *Missing B:* a one-sentence back-reference that adopts "causal run trace" as the term (T22). Location: § A useful trace tells the story of the run (C24-R06).
3. **Trace → effect ledger → audit ledger → workflow history.** The worked example consults the effect ledger (`:85`) and the prose talks about the audit ledger. The reader is never told these are different records with different owners (Ch 22 effect state, Ch 15 history, the protected audit store). *Missing B:* "the trace explains and points; the other three are authoritative." Location: § A useful trace… (C24-R06).
4. **Ch 14 operator console → trace API.** Ch 14 requires a "live run graph" and "fork a sandbox replay" (`04-part-iv.md:906–908`). *Missing B:* the console reads `GET /v1/runs/{id}/trace` (currently in Ch 25) and forks through Ch 04's `:fork`. Location: the new implementation section (C24-R01).
5. **Ch 15 replay → diagnostic replay → fork.** Three different meanings of replay. *Missing B:* an explicit distinction. Location: § Trace and replay semantics (C24-R07).
6. **Ch 23 taint and containment → trace.** Ch 23 closes with "follow the tainted content to every capability and network boundary" (`06-part-vi.md:1270`) and "Security controls now produce events and evidence". Ch 24 has no span or attribute for taint, egress, DLP, or kill-switch decisions, so the Part transition's promise is not cashed. *Missing B:* a security-control span row (C24-R02).
7. **Ch 24 trace attributes → Ch 25 trace-based scorers.** Ch 25's deterministic scorer reads `effect.state`. *Missing B:* Ch 24 names the attribute that scorers depend on, and its Tool row records effect state (C24-R02, C25-R11).

## Transition Problems

- **In (Ch 23 → Ch 24).** Ch 23's closing sentence is good, but Ch 24 never returns to security signals except the scorecard's Safety row. Adding the security-control span row (C24-R02) makes the transition true.
- **Within:**
  - § A useful trace… → § Follow one decision… repeats rather than advances.
  - § Follow one decision… → § Privacy and reliability shifts from narrative to infrastructure without a cue.
  - § Build observability… opens with a Required-analysis table, then jumps to standards ("Adopt OpenTelemetry-compatible…", `:106`). The reader has already heard about OTel at `:11`, `:19`, and `:58`.
  - The evidence section is sandwiched between two tips.
- **Out (Ch 24 → Ch 25).** "Where this leads next" is accurate. The two case vignettes are disconnected: a slow review with an Unknown effect, then a prompt revision with a forbidden lookup. The Enterprise-example row at `:102` already supplies the bridge (failed request → regression fixture). Ch 25 should pick it up (C25-R02 carries the sentence).

## Redundant and Repetitive Concepts

| Concept | Occurrences in Ch 24 | Verdict / action |
| --- | --- | --- |
| Span kinds to trace | `:56`, `:99`, `:106`, `:108–117`, `:195`, `:214` | D. Keep the table. Others become references or are cut (`:56`, `:99`). Checklist and Q may keep a short reference. |
| Required attributes | `:58`, `:108–117`, `:137` | D. Fold into the table. |
| Questions a trace answers | `:46–50`, `:54` | D. Merge into one list. |
| Sensitive content out of traces | `:62`, `:87–90`, `:100`, `:143`, `:199`, `:216` | `:62` + `:100` + `:143` are D (consolidate into one implementation paragraph). `:87–90` (example lesson), `:199` (checklist), and `:216` (Q) are R. |
| Debugging method | `:64–66`, `:189–191` | D. Rewrite If-fails as observability-system failures. |
| "Trace the decision" / join to the system of record | `:21`, `:49`, `:119`, `:154`, `:166` | Keep `:21` + `:119`. Keep one tip; delete `:164–166`. |
| Audit separation | `:31–38`, `:62`, `:143`, `:201`, `:218` | Mostly R (checklist and Q). `:143` folds into the implementation paragraph. |

## Cross-Chapter Duplication

| Other location | Overlap | Verdict | Owner / action |
| --- | --- | --- | --- |
| Ch 07 § If this fails in production (`03-part-iii.md:141–146`) | First-divergence debugging, more complete than Ch 24's | D, with the canonical home the thinner one | Ch 24 absorbs the content (C24-R04). The Ch 07 review cuts Ch 07's list to a one-line pointer. |
| Ch 07 platform table "Observability/Tracing: Unified run graph…" (`03-part-iii.md:49`); golden path "Debug" row (`:103`) | Run graph as a platform capability | R (platform framing) | Keep. Ch 07 may add "(Chapter 24)". |
| Ch 16 § P-09 — Causal run graph (`04-part-iv.md:1457`) | The same concept as a card | R (decision aid) | Keep. Ch 24 back-references it (C24-R06). |
| Ch 17 § AP-14 — Telemetry without causal or effect lineage (`04-part-iv.md:1839`) | The same concept as an anti-pattern; its metrics ("percentage of runs joinable to a business outcome, spans missing parent or version identifiers, unattributed spend") match Ch 24's `:150` | R | Keep. Ch 24 back-references it. |
| Pattern cards' "What you need to see in production" (12 locations listed above) | Pattern-specific attributes | R as card-local reminders, but they never converge | Ch 24 consolidates them into the schema (C24-R02). Card owners keep their lists. Optionally they append "(span attributes, Chapter 24)"; each chapter's review decides. |
| Ch 04 § Run API `:fork` (`02-part-ii.md:169`); Ch 14 console (`04-part-iv.md:906–908`, `:938`) | Fork / sandbox replay | R | Ch 24 owns diagnostic replay and fork semantics and cites Ch 04's endpoint. Ch 25's `:forkReplay` is removed (C24-R01, C25-R01). |
| Ch 15 replay (`04-part-iv.md:1148`, `:1235`) | Recorded activity results on replay | R | Ch 15 owns workflow replay. Ch 24 states the distinction (C24-R07). |
| Ch 06 § State taxonomy and storage "Telemetry and audit" row (`02-part-ii.md:690`); Ch 04 § Where each kind of state belongs (`:242`, "a trace store is not the audit ledger") | Trace store versus audit archive | R | Ch 24 cross-references them instead of redefining stores (C24-R12). |
| Ch 19 § Scalability… (`05-part-v.md:547`) | W3C trace context and span links across A2A | R (application, used before definition; low severity per map #55) | Keep. |
| Ch 25 § A workable implementation (`07-part-vii.md:347–375`) | Ch 24's own implementation | Misplaced | Move to Ch 24 (C24-R01 / C25-R01). |
| Ch 25 § Measure both the outcome and the path (`:432`) | Metric catalog overlapping the Ch 24 scorecard | D | Ch 24's scorecard is the single catalog (C24-R02); Ch 25 deletes the list (C25-R05). |
| Ch 25 `:319`, pitfall `:447–449` vs Ch 24 `:139` | Grader calibration | D | Delete from Ch 24. |
| Ch 22 effect states; Ch 24 worked example | Unknown → reconcile | R (application) | Keep. |

## Structural Recommendations

Target order for Chapter 24 (headings marked *new* or *moved*):

1. Opening callouts (unchanged except the MLflow version wording).
2. § Why a trace must explain decisions, not just latency.
3. § A useful trace tells the story of the run. It gains:
   - one merged question list;
   - the four-records paragraph;
   - the P-09/AP-14 back-reference and the "causal run trace" / "trajectory" terms.

   Absorbs `:54–56`.
4. § Follow one decision from request to outcome, now containing:
   - § Debugging method (expanded, absorbing Ch 07);
   - § Worked example (with time categories).

   § Privacy and reliability moves out.
5. § Build observability around decisions and effects, containing:
   - the Required-analysis table (evaluation clauses removed);
   - § What the trace needs to connect (canonical span schema with the new rows);
   - § A scorecard operators can actually use (canonical metric catalog);
   - § Trace and replay semantics (three-way replay distinction; grader bullet removed).
6. *New* § A workable implementation (from Ch 25), containing:
   - § Who should own each decision;
   - § The contracts between components;
   - § Records worth preserving;
   - *moved* § Privacy and reliability;
   - *moved* § What changes as usage grows, evaluation bullets removed.
7. One OBSERVABILITY TIP (keep `:152–154`, placed at the end of § What the trace needs to connect).
8. § What the evidence lets us conclude.
9. § A sensible place to start, with lead-in prose. § MLflow tracing integration receives the `:58` MLflow paragraph. § Mortgage Agents SDK integration gets a scope note.
10. If-fails rewritten; checklist, exercises, questions, next.

## Concrete Recommended Changes

**C24-R01 — Priority: High — Action: Move**
- **Location:** new H2 `## A workable implementation` in `07-part-vii.md`, inserted after § What changes as usage grows (`:150`) and before § What the evidence lets us conclude (`:156`). Source: Ch 25 § A workable implementation (`:341–381`).
- **Issue:** Ch 24 has no implementation section. Its components, APIs, and records sit in Ch 25, and Figure 24-1 already draws them.
- **Why it matters:** the reader learns what a trace must contain but not what system produces, stores, and serves it. In Ch 25 the same tables interrupt the evaluation argument.
- **Change:** **Reconciled (see overall-book-review.md §D-15):** As stated, but the Audit ledger writer row points to "Chapter 4 § Where each kind of state belongs"; C06-R03 removes the Telemetry and audit row from Ch 06's taxonomy. Original text: create H3s.
  - § Who should own each decision: move the Ch 25 rows Telemetry Gateway/Collector (rename "Telemetry Collector", per T4), Trace Index, Content Vault, Metrics/SLO Pipeline, and Replay/Fork Service. Add one row: "Audit ledger writer — append-only, integrity-protected, loss-intolerant path for protected decisions and effects; see Ch 06 § State taxonomy and storage."
  - § The contracts between components: move `POST /otlp/v1/traces, /metrics, /logs` and `GET /v1/runs/{run_id}/trace`. Replace `POST /v1/runs/{run_id}:forkReplay` with a sentence pointing to Ch 04 § Run API `POST /v1/runs/{id}:fork` (same semantics: sandbox, mocked or read-only effects unless separately authorized). Add: "The Ch 14 operator console reads the trace API; its live run graph is a role-redacted view of this trace."
  - § Records worth preserving: move TraceIndex, SpanEnvelope, and ContentBlob. Add AuditEvent: "run/effect/decision ID, actor and subject, policy/approval reference, integrity hash, retention class; never sampled."
  - Move § Privacy and reliability (`:60–62`) and § What changes as usage grows (`:141–150`) under this H2, minus the bullets removed in C24-R08.
- **Related:** C25-R01 (deletion side), C24-R03, C24-R12.

**C24-R02 — Priority: High — Action: Rewrite**
- **Location:** § What the trace needs to connect (`:104–119`), plus § A scorecard operators can actually use (`:121–132`).
- **Issue:** the span schema traces calls, not decisions. It omits the signals twelve earlier pattern cards require, omits Ch 23's security signals, and does not name the `effect.state` attribute Ch 25's scorer reads.
- **Why it matters:** this table should be the book's single answer to "what must a run emit". Without it the earlier lists stay disconnected, and the chapter contradicts its own "trace the decision" rule.
- **Change:**
  - **Table rows.** Add three rows:
    - Decision: "kind (route, plan compile/revision, step disposition, acceptance, critique); candidates and eligibility removals; chosen option; validator or compiler reason; scorer/rubric versions for acceptance; plan digest/revision and replan diff; turn index, information gain, remaining budgets, stop reason".
    - Memory: "memory ID/version, operation (read/write/delete), scope/tenant, purpose and policy basis, provenance, TTL".
    - Security control: "control (detector, egress, DLP, kill switch), rule/version, taint label of the input, decision, action".
  - **Attributes on existing rows.** Add "effect state (`effect.state`)" and "credential lease ID" to Tool. Add "workflow build, timer/wait state, signal source" to Workflow. Add "grant lineage, join condition" to Agent task.
  - **Mapping sentence.** After the table, add one sentence: "The 'What you need to see in production' lists in Chapters 2, 6, 10–15, and 18 are attributes on these span types; this table is their common schema."
  - **Cleanup.** Delete the attribute list at `:58` (from "Required attributes include…") and the bullet at `:137`; both are now in the table.
  - **Scorecard.** Add to Outcome quality "faithfulness / unsupported-claim rate". Add to Trajectory quality "tool-selection precision/recall, argument correctness, plan adherence". Add "retry amplification" to Reliability. Add "reviewer fatigue" to Human load. Add one sentence under the table: "Chapter 25 explains how the outcome and trajectory rows are scored offline and per slice."
- **Related:** C25-R05 (deletes Ch 25 `:432`), C25-R11. Ch 24 owns the schema and the metric catalog.

**C24-R03 — Priority: High — Action: Merge**
- **Location:** § A useful trace tells the story of the run (`:46–50`), § Follow one decision from request to outcome (`:54–58`), § Privacy and reliability (`:60–62`).
- **Issue:** two overlapping question lists. A span enumeration (`:56`) duplicates the table. Product configuration (`:58`) sits in a conceptual section. An implementation H3 sits under a narrative H2.
- **Why it matters:** the reader meets the same idea three times before any new mechanism appears.
- **Change:**
  - Replace `:46–50` with one list built from `:54`: which release handled the request; what context the model saw; which policy decision narrowed the eligible actions; which decision changed the path; which activity consumed the time or budget; which effect was committed and which receipt proves it; did the business obligation succeed. Keep the closing clause "stable identifiers and typed links, not copying every prompt".
  - Delete `:54` and `:56`, but keep `:56`'s final sentence (span links because queues, retries, and fan-out are not one call stack) and append it to the merged paragraph.
  - Move `:58`'s MLflow sentences (from "Northstar uses…" to "…separate privacy control.") to § MLflow tracing integration as its lead-in, with "Northstar" replaced by "the Harborlight platform".
  - § Follow one decision from request to outcome then opens directly with § Debugging method.
  - Move § Privacy and reliability per C24-R01, and merge it with the trade-offs cell (`:100`, keep the cell short) and the first scale bullet (`:143`).
- **Related:** C24-R01, C24-R04, C24-R15.

**C24-R04 — Priority: High — Action: Rewrite (canonical consolidation)**
- **Location:** § Debugging method (`:64–66`).
- **Issue:** the canonical method is thinner than Ch 07's version.
- **Why it matters:** first divergence is the operational skill the chapter teaches, and Ch 25's If-fails step 2 depends on it.
- **Change:** **Reconciled (see overall-book-review.md §D-10):** As stated. The Ch 07 side is C07-R07, which rewrites Ch 07's list for platform failures and keeps one step pointing to this method; it does not reduce Ch 07 to a bare one-line pointer. Original text: rewrite as five numbered steps:
  1. Start from the violated outcome or SLO.
  2. Walk the critical path and split elapsed time into queue, execution, human dwell, retry delay, and reconciliation.
  3. Find the first divergent span. Categories: input classification, source or freshness, context manifest, prompt, route, model, tool, arguments, policy, approval, effect, acceptance.
  4. Diff the run against the nearest accepted run: manifest, context and evidence versions, every pinned version. Do this before comparing final prose.
  5. Change nothing, especially the prompt, until the evidence locates the failing responsibility. A prompt change that hides a policy or contract defect removes the signal, not the fault.

  The Ch 07 review should reduce `03-part-iii.md:141–146` to "Debug from the outcome backward using the first-divergence method in Chapter 24."
- **Related:** C24-R05, C24-R09, C25-R13.

**C24-R05 — Priority: Medium — Action: Rewrite**
- **Location:** § Worked example — diagnosing a slow mortgage-evidence review (`:68–90`).
- **Issue:** the example does not visibly apply the method, the durations do not sum, and the first divergence is unnamed.
- **Why it matters:** the example is where the reader rehearses the method.
- **Change:**
  - Add a "Time and category" column to the table: queue → queue time; retrieval retry → retry delay; approval → human dwell; connector → execution plus reconciliation. Give durations that sum to twelve minutes (the author picks the numbers; they are illustrative).
  - Add one sentence after the table: "The first divergent decision is the stale index snapshot; the Unknown effect is the first state that blocks a safe retry."
  - Replace "human action authorization wait" with the canonical approval term chosen under T3.
- **Related:** C24-R04.

**C24-R06 — Priority: Medium — Action: Add / Cross-reference**
- **Location:** § A useful trace tells the story of the run, after the diagnostics/audit paragraph (`:38`).
- **Issue:** the chapter never claims its role as the causal run graph of P-09/AP-14. It also never separates the trace from Ch 22's effect ledger and Ch 15's workflow history.
- **Why it matters:** readers carry "run graph" from Ch 07/14/16/17 and need to know this is that object. They also need to know which record is authoritative when the trace and the ledger disagree.
- **Change:** **Reconciled (see overall-book-review.md §D-04):** As stated, but the first sentence reads: "Appendix A's P-09 and Chapter 17's AP-14 name this object and what its absence costs; this book calls it the causal run trace, and Chapter 25 calls the same run's ordered decisions its trajectory." P-09 moves to Appendix A and is retitled (C16-R04). Original text: add three sentences.
  - "Chapter 16's P-09 called this the causal run graph and Chapter 17's AP-14 showed what its absence costs; this book calls it the causal run trace, and Chapter 25 calls the same run's ordered decisions its trajectory."
  - "Three other records remain authoritative: workflow history for execution state (Chapter 15), the effect ledger for effect state (Chapter 22), and the audit ledger for proof."
  - "The trace links to all three and replaces none."
- **Related:** C24-R12, the T22 terminology decision.

**C24-R07 — Priority: Medium — Action: Rewrite**
- **Location:** § Trace and replay semantics (`:134–139`).
- **Issue:** "replay" has three meanings. The grader bullet is Ch 25 content. The attribute bullet duplicates the table.
- **Change:**
  - Delete bullet 2 (`:137`, now in the table) and bullet 4 (`:139`; Ch 25 owns grader evidence, see C25-R02).
  - Rewrite bullet 3 as: "Workflow replay (Chapter 15) re-executes history using recorded activity results. Diagnostic replay renders a recorded run without calling models or tools. A fork (Chapter 4 `:fork`) is a new run from a checkpoint with explicitly changed versions; it mocks external effects or reauthorizes them. None of the three may create a live effect."
- **Related:** C24-R01.

**C24-R08 — Priority: Medium — Action: Remove / Move**
- **Location:** § Build observability around decisions and effects table (`:98–101`); § What changes as usage grows (`:147`, `:149`, `:150`).
- **Issue:** evaluation content belongs to Ch 25.
- **Change:**
  - In Design alternatives, delete "black-box outcome evals; trace/trajectory grading; deterministic simulators".
  - In Recommended architecture, cut it to: "Emit one causal trace per run with spans for every call and decision (schema below). Separate operational telemetry from immutable audit." This deletes the eval-dataset sentence and the span list.
  - In Failure scenarios, delete "average success hides long-tail failures; LLM judge rewards style over correctness".
  - Move bullet `:147` (evaluation queues) to Ch 25's implementation section as a scale note for the Evaluation Orchestrator.
  - In `:149`, keep "Preserve sampling weights and selection reasons for online estimates" and delete the slice sentence (Ch 25 owns it).
  - In `:150`, delete "evaluator disagreement, and dataset leakage".
  - Keep the Enterprise example row.
- **Related:** C25-R01.

**C24-R09 — Priority: Medium — Action: Rewrite**
- **Location:** § If this fails in production (`:187–191`).
- **Issue:** the section restates the debugging method.
- **Change:** replace the three steps with failures of the trace itself:
  1. A trace breaks at a queue, resume, or A2A boundary: check traceparent propagation and span links, and fall back to domain-ID joins.
  2. Spans lack release or policy versions: block the release, because runs cannot be compared.
  3. The collector drops data or redaction fails: confirm protected audit events took the loss-intolerant path, quarantine leaked content, and alert on the observability SLOs.

  Add a one-line pointer: "To debug a failed run, use the method in § Debugging method."
- **Related:** C24-R04.

**C24-R10 — Priority: Low — Action: Remove**
- **Location:** second OBSERVABILITY TIP (`:164–166`).
- **Issue:** it restates `:49` and the Run span row, and interrupts the evidence → examples sequence.
- **Change:** delete it. Move the first tip (`:152–154`) to the end of § What the trace needs to connect.

**C24-R11 — Priority: Medium — Action: Rewrite**
- **Location:** § A sensible place to start (`:168–185`) and the case box (`:15`).
- **Issue:** examples have no lead-ins. The mortgage example's scope is not stated against the worked example. The box overclaims.
- **Change:**
  - Under § A sensible place to start, add: "Start by instrumenting what the platform owns: the first example places manual agent and tool spans and records a decision attribute."
  - Under § MLflow tracing integration, insert the MLflow paragraph moved from `:58` (C24-R03).
  - Under § Mortgage Agents SDK integration, append: "The example traces the agent, runner, and tool spans only; the queue, policy, approval, and effect spans in the worked example are platform spans you add with the explicit-span pattern above. That is exercise 1."
  - In the box, change "Harborlight links the entire trajectory" to "Harborlight's target is one trace that links the entire trajectory." This keeps it consistent with the front-matter statement that later checkpoints are roadmap targets.
- **Related:** C24-R03, C24-R15.

**C24-R12 — Priority: Low — Action: Rewrite**
- **Location:** state-owner table (`:44`).
- **Issue:** the core contracts (TraceContext, SpanLink, AuditEvent) do not match the body. AuditEvent is defined nowhere.
- **Change:** **Reconciled (see overall-book-review.md §D-15):** As stated, but the store cross-reference in the Audit ledger writer row is "Chapter 4 § Where each kind of state belongs", not Ch 06 (see C24-R01). Original text: set Core contracts to "W3C trace context · SpanEnvelope · TraceIndex · AuditEvent", all defined in the new records table (C24-R01). Add the store cross-reference to Ch 06 § State taxonomy and storage in the Audit ledger writer row.

**C24-R13 — Priority: Low — Action: Add**
- **Location:** Part VII orientation (`:3–7`).
- **Issue:** no bridge to the signals and run-level evaluation the reader already holds.
- **Change:** add one sentence after "…governed learning.": "Earlier chapters listed what each pattern must emit and how a run accepts its own result; Chapter 24 joins those signals into one causal trace, and Chapter 25 turns traces into release evidence."

**C24-R14 — Priority: Low — Action: Rewrite (terminology)**
- **Location:** `:19`, `:58`, `:73`.
- **Change:**
  - Use "MLflow 3.15.2 (pinned)" in the design choice.
  - Replace "Northstar" (T1).
  - Apply the T3 approval term.
  - Adopt "causal run trace" (operations) and "trajectory" (evaluation view) per T22. Use "trajectory" in `:96` and Q1 (`:214`) only after C24-R06 defines it.

**C24-R15 — Priority: Medium — Action: Rewrite (citation scope)**
- **Location:** `:58` (moving to § MLflow tracing integration per C24-R03).
- **Issue:** "In the pinned MLflow 3.15.2 profile, Agents SDK tracing is disabled by default" has no registry source scoped to that claim. R21's `supports` is only "Pins the reproducibility baseline used for book examples". This conflicts with AGENTS.md citation safety.
- **Change:** do one of two things.
  - Verify the claim against the 3.15.2 release notes, then extend R21's `supports` in `config/references.json` to cover it.
  - Or recast it as a book-authored, tested statement: "the book's pinned example enables it explicitly; see `examples/tests/test_mortgage_agents_mlflow.py`".
- **Related:** C25-R12 (the same issue in Ch 25).

**C24-R16 — Priority: Low — Action: Rewrite**
- **Location:** § Questions to bring to design review, Q2 (`:215`).
- **Issue:** Q2 overlaps Q1, and no question tests the trace / ledger / audit relationship.
- **Change:**
  - Fold Q2's answer into Q1 ("…using stable IDs and span links, because queues, retries, fan-out, resumed waits, and remote agents are not one call stack").
  - Add the question "Which record do you trust when the trace and the effect ledger disagree?" Strong answer: "The effect ledger for effect state and workflow history for execution state; the trace is diagnostic and may be sampled, so a disagreement is an observability defect to fix, not a fact to act on."

**C24-R17 — Priority: Low — Action: Cross-reference** *Added in reconciliation (see overall-book-review.md §D-29).*
- **Location:** End of § If this fails in production (as rewritten by C24-R09).
- **Issue:** Same request as C05-R16.
- **Change:** Add one line: "If telemetry cannot join a run to its release, decisions, and effects, see AP-14 in Chapter 17."
- **Related:** C17-R03, C24-R09.
