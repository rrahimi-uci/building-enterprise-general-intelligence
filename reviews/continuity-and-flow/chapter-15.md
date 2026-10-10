# Chapter 15 — Keep Long-Running Work Alive Through Failure: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:1113–1354`. Context read: Ch 14 close (`:1080–1111`), Ch 16 opening (`:1356–1373`), Part IV intro (`:1–7`), Ch 03 § The restart test and § The complete execution path (`01-part-i.md:1127–1131`, `:1203–1217`), Ch 04 § Run API, § Effect receipt, § Event contract (`02-part-ii.md:157–262`), Ch 19 § State mapping and ownership (`05-part-v.md:529–539`), Ch 22 § A reliable protocol… (`06-part-vi.md:665–681`), Ch 27 § Rollback and active runs and § Compatibility and long-running execution (`08-part-viii.md:162–166`, `:320–326`), `config/references.json` (R02, R04), `examples/runtime/durable_state.py`.

## Overall Assessment

This is the right chapter in the right place. Ch 14's waits create the need for it, and the reducer-versus-activity split is the clearest statement of durable execution in the book. These parts are strong:

- the design choice
- the determinism paragraph (`:1148`)
- the durable execution contract
- the execution and persistence rules, especially "persist a wait registration before acknowledging", `:1236`
- the design-review answers

Its problems are organizational and boundary-related, not conceptual:

1. **Heading structure does not match content.**
   - § Terminal correctness sits under § Durable state is more than chat history.
   - § The lifecycle of a durable run is an empty wrapper around one H3.
   - § Let events resume work without losing control holds a Required-analysis table, the execution contract, and the checkpoint policy, and only then reaches events.
   - § Event-driven resume flow is an empty heading. It was empty in the v3.0/v3.1 originals too (`source/original/…v3.1-source.md:3032`), so a lost diagram or list never arrived.
2. **It re-teaches neighbors instead of pointing at them:**
   - Ch 04's CloudEvents/outbox contract (`:1198`)
   - Ch 04's Run API (`:1208–1218`)
   - Ch 22's at-least-once/unknown-effect rule (PRODUCTION CONSIDERATION `:1253`)
   - Ch 27's regional recovery (`:1247`)
   - Ch 03's restart test, as a COMMON PITFALL (`:1265`)
3. **It never connects to the rest of Part IV.**
   - § Canonical control flow is where the Part's patterns compose into one run: plan → Ch 12, execute/ReAct → Ch 10/11, validate → Ch 13, wait → Ch 14. It names none of them.
   - The closing sentence, "The core patterns are now defined", is false. Ch 16's P-06, P-07, P-09, and P-10 are built in Ch 18–28, and P-08 and P-11 only partly in Ch 15 (see chapter-16.md's card table). [verified: softened — P-08 and P-11 are partly grounded by Ch 03/04/15]
4. **Terminal states have no canonical home.** The map assigns Ch 15 as the home for run terminals (§6 T12). § Terminal correctness gives three sentences. Meanwhile Ch 19 calls its state list "canonical local state" (`05-part-v.md:531`) with no earlier definition.

## Intended Reader Mental Model

After Ch 15 the reader should hold:

- **What.** A long-running run is a deterministic workflow history plus bounded, recorded activities, with durable waits (timers, signals, wait registrations) and checkpoints. Chat history is not state.
- **Why.** Runs outlive processes, deployments, credentials, and roles. Replay must not repeat effects.
- **How.**
  - The reducer never does I/O.
  - Activities carry effect keys.
  - The inbox is written before the signal.
  - Checkpoints are taken after visible effects.
  - Build-compatible workers are kept or migrated explicitly.
  - A run reaches Succeeded only through acceptance; reconciliation and InterventionRequired are legitimate endings.
- **When.** Use it for work with waits, multiple systems, or protected effects. Do not use it for one short idempotent read.
- **Trade-offs.** Determinism and versioning discipline plus operational cost, in exchange for removing bespoke recovery code.
- **Relationships.**
  - Ch 03 restart test → Ch 15 mechanism.
  - Ch 04 Run API and events → Ch 15 lifecycle verbs.
  - Ch 10–14 patterns run *inside* this lifecycle.
  - Ch 22 owns effect states and reconciliation.
  - Ch 27 owns release and rollback policy for in-flight runs.

The chapter delivers What, Why, How, When, and Trade-offs. The Relationships are almost entirely implicit.

## Section-by-Section Flow Review

**Opening callouts (`:1115–1123`).** The evidence context is properly scoped [R02][R36][R38]. The case box (nine-day wait, two deploys, policy change, role loss, one timeout) is the best case box in Part IV, because it lists exactly the failures the chapter handles. The design choice is precise. *Issue:* "employment document" (§6 T15).

**§ Why long-running work needs durable state (`:1125`).** Role: the thesis. Good, short.

**§ Model long-running work explicitly (`:1133`).** Role: a second framing H2 ("Durability is not achieved by serializing an in-memory agent object"). It adds the list of what must be durable (intent, transitions, obligations, timers, children, approvals, effects). It repeats `:1127–1131`'s "outlive processes, deployments". This is the double-why template (map §5.1). The state-owner table (`:1138–1140`) is the only other content.

**§ Durable state is more than chat history (`:1142`).** Role: the core distinction, plus Figure 15-1 and reducer determinism. It adds the deterministic reducer (`:1148`), the chapter's single most important idea. *Issues:*
- "Northstar uses event history to rebuild a canonical RunState" (`:1146`): RunState is not among the chapter's contracts (WorkflowEvent, Checkpoint, WaitRegistration).
- This is Ch 03's restart test (`01-part-i.md:1127–1131`) made operational, and it does not say so.

**### Terminal correctness (`:1150`).** Role: Succeeded only via acceptance; cancel with a possible write goes through reconciliation and compensation; InterventionRequired. It adds the terminal rule. *Issues:*
- It is misplaced under a chat-history heading. It belongs after § Canonical control flow step 9 (Complete).
- It is too thin to be the canonical terminal home, and the book has seven terminal vocabularies (§6 T12).
- Compensation is used before Ch 22 defines it, and Ch 01's vocabulary table wrongly says compensation is developed here (`01-part-i.md:445`).

**§ The lifecycle of a durable run (`:1154`).** An empty wrapper H2.

**### Canonical control flow (`:1156`).** Role: ten-step lifecycle. It adds the end-to-end sequence the reader will reuse. *Issues:*
- (a) There are no links to the Part IV patterns that occupy steps 4, 5, 7, and 8.
- (b) Step 1 "requested autonomy" uses the "autonomy level" concept, which Ch 02's design principles (`01-part-i.md:744`, `:750`) and Ch 04's Run API ("autonomy request", `02-part-ii.md:163`) name but no chapter defines as a scale (§4 row 4). [verified: softened — "orphan" overstated it; the term is used earlier, just never defined]
- (c) Step 2 "Snapshot" is the RunManifest (Ch 04) but is not named as such.
- (d) Step 3 "maximum capability envelope" and step 5 "downscoped credential" depend on Ch 21; step 4 "risk classes" depends on Ch 22 (§4 row 37).
- (e) Step 8 "propose → preview → approve → commit" is a fourth name for the six gates (§6 T14).
- (f) Step 10 "Learn safely" is Ch 25's subject and needs a pointer.
- (g) It is the third end-to-end walkthrough, after Ch 03 § The complete execution path (9 steps) and Ch 04 § End-to-end responsibility flow (8). The map designates Ch 15 as the detailed home.

**§ Let events resume work without losing control (`:1169`).** Role: Required-analysis table. It adds the alternatives (Temporal/DBOS/Restate/Durable Functions, graph checkpointers) and an on-thread enterprise example. *Issues:* the heading covers only the last two H3s; the table and the next two H3s are about durable execution generally. The "Failure scenarios" row is a good list but has no link to the controls that address each scenario.

**### Durable execution contract (`:1181`).** Role: definitions of workflow code, activity, checkpoint, signal, query, and update. It adds the vocabulary of the chapter. Flow: excellent. *Issues:*
- The Checkpoint bullet gives a field list that § Records `:1230` repeats with drift (effect ledger cursor vs artifact/effect cursors; version pins vs code compatibility range).
- The "Update" bullet is Ch 04's `:update` (`02-part-ii.md:167`) without the link.

**### Checkpoint policy (`:1190`).** Role: when to checkpoint. Unique and concise. Keep.

**### Event-driven resume flow (`:1194`).** **An empty heading.** The steps it should hold are scattered:
- § Who should own each decision (`:1204`): Event Ingress → Correlator → Timer/Signal services.
- § Execution and persistence rules (`:1236`): wait registration before acknowledging; inbox before signal.
- Ch 14 § Workflow integration (`:956–961`): the approval instance.

**### Event architecture (`:1196`).** Role: CloudEvents envelope, outbox/inbox, DLQ. *Issues:*
- It re-specifies Ch 04 § Event contract (`02-part-ii.md:206`) and § CloudEvents and outbox contracts (`:258`).
- Its field list differs from Ch 04's `CloudEvent` model (`02-part-ii.md:270–284`): Ch 15 adds correlation_id, causation_id, and a payload reference, and omits specversion and datacontenttype. [verified: corrected — Ch 04's envelope is the Python model in § CloudEvents and outbox contracts, not a JSON block]
- Outbox/inbox semantics are owned by Ch 22 (map §3).

Unique here: the correlation key must resolve to a wait registration, and "a dead-letter queue is quarantine and diagnosis—not a substitute for domain compensation".

**§ A workable implementation (`:1200`).** Wrapper.

**### Who should own each decision (`:1202`).** Prose, while Ch 12 and Ch 14 use a table (map §5.1). Content: the Run API, durable workflow, activity workers, Event Ingress, Correlator, Timer/Signal, and Version Router. Good roles. The format is inconsistent within Part IV.

**### The contracts between components (`:1206`).** Run API. *Issues:*
- Five of the nine rows overlap Ch 04 § Run API (POST runs, GET run, signal, cancel, history/events).
- Naming drifts (`GET …/events` in Ch 04 vs `GET …/history?cursor` here).
- `:pause`/`:resume`/`:cancel` collide with Ch 14's `:operatorAction` (`:938`).

New here: `events:ingest`, `:pause`, `:resume`, `:migrate`, and the 202/home-region/pinned-manifest response.

**### Records worth preserving (`:1220`).** Role: eight entities. It adds WaitRegistration, SignalInbox (with its uniqueness key), Timer, and WorkflowMigration, all of which are unique and valuable. Flow: fine. The Checkpoint row duplicates `:1185`.

**### Execution and persistence rules (`:1233`).** Role: five rules. It adds replay returning recorded results, the subscription race, effect key before invocation, logical time, and continue-as-new. Flow: the strongest implementation content in the chapter. Rule 3 ("persist intent/effect key before invocation and reconcile the receipt") is the right short recall of Ch 22.

**### Scalability and multi-region behavior (`:1241`).** Role: seven bullets. Unique and valuable:
- separate activity and workflow-task queues
- "waiting executions consume storage, not workers"
- autoscale on oldest-message age
- sticky caches not required for correctness
- signal coalescing that preserves receipts

Redundant: the home-region/failover bullet (`:1247`) restates Ch 27 § Rollback and active runs (`08-part-viii.md:166`). The build-compatibility bullet (`:1248`) overlaps Ch 27 § Compatibility and long-running execution (`:322–323`) and design-review row 5 (`:1350`).

**PRODUCTION CONSIDERATION (`:1251–1253`).** At-least-once delivery, the unknown outcome, stable keys, reconcile. This is the map's fourth of five pre-teachings of Ch 22's unknown-effect rule (§3). Rule `:1237` already covers it. Redundant.

**§ What the evidence lets us conclude (`:1255`).** The claim "Recovery objective" (RTO/RPO, worker availability, backup, failover, pending approvals and unknown effects in DR) cites R02 and R04. R04 (CloudEvents) `supports` "a portable event envelope and event identity semantics" and does not support a recovery-objective claim. R02 supports replay, timers, and long-running processes, not RTO/RPO. This is a citation-scope problem under `AGENTS.md` § Citation safety. The claim also concerns DR, which the chapter covers in one bullet and Ch 27 owns.

**COMMON PITFALL (`:1263–1265`).** "Storing conversation history and calling it durable state." This repeats § Durable state is more than chat history, sits after the evidence section, and duplicates AP-02. Its last clause ("resumable … even if every message is discarded") is the restart test and is worth keeping as the recall line.

**§ How Long-Running Agents work in practice (`:1267`) with ### How the pattern works (`:1273`), ### Where it helps—and what it costs (`:1287`), ### Where it can fail—and how to contain it (`:1294`), and ### What you need to see in production (`:1302`).** The template card. It is a compact restatement. The "Unknown mutation → Freeze dependents and reconcile" row is good recall. Acceptable.

**§ A sensible place to start (`:1312`) / ### Replay-safe workflow reducer (`:1315`).** An empty H2 followed by an H3 holding one example. Fine content; it needs one lead sentence ("The reducer folds recorded events into run state and does no I/O, so replay is a pure function").

**§ If this fails in production (`:1319`).** Three diagnostic steps. Good, and complementary to AP-01/AP-02/AP-05 (structural). There is no pointer.

**§ What to verify before production (`:1325`).** Five items. Item 3, "Each failure class has one retry owner", is taught in Ch 03 § One retry owner and Ch 22, not here. It needs a pointer.

**§ Put the idea to work (`:1337`).** Exercise 1 "ten-day wait" conflicts with the case box's nine days (`:1119`). Exercise 2 is good.

**§ Questions to bring to design review (`:1342`).** Five strong rows. Row 4 (cancellation with a possible write) is the best summary of terminal correctness. Row 5 overlaps Ch 27 and needs a pointer, not removal.

**§ Where this leads next (`:1352`).** "The core patterns are now defined; Chapter 16 compares them by the obligation each protects…" This is **inaccurate**:
- Ch 16's cards P-06, P-07, P-09, and P-10 rely on Ch 18–28, and P-08 and P-11 partly (§4 rows 39–45). [verified: softened]
- Ch 16's catalog omits routing, plan compilation, critique, and human review (Ch 11–14).

## Sparse or Underdeveloped Content

1. **§ Terminal correctness (`:1150–1152`).** It is the designated canonical home for run terminal states (map §6 T12) but has three sentences. It needs one compact table (C15-R04). This is the only expansion the chapter needs.
2. **§ Event-driven resume flow (`:1194`).** Empty. Fill it by *moving* existing sentences, not by writing new material (C15-R05).

## Missing Conceptual Connections

- **Ch 03 § The restart test → (missing: "this chapter is the mechanism that passes it") → Ch 15 § Durable state is more than chat history (`:1146`).**
- **Ch 10/11/12/13/14 patterns → (missing: where each runs in the lifecycle) → § Canonical control flow (`:1158–1167`).** Steps 4 (plan, Ch 12), 5 (execute: routed workers and bounded ReAct activities, Ch 11/10), 7 (wait or intervene, Ch 14), 8 (validate: acceptance and critique, Ch 13; the six gates, Ch 02).
- **Ch 04 RunManifest → (missing: "Snapshot resolves the RunManifest") → step 2 (`:1159`).**
- **Ch 10 step dispositions (`:49`), Ch 13 acceptance decisions, and Ch 22 effect states → (missing: how they determine run terminal state) → § Terminal correctness.**
- **Ch 14 intervention → (missing: "InterventionRequired opens an intervention task (Chapter 14)") → § Terminal correctness (`:1152`).**
- **Ch 15 build compatibility → (missing: "Chapter 27 turns this into release policy: rollback reassigns new work only") → § Questions row 5 (`:1350`) and § Scalability bullet `:1248`.**
- **Ch 15 § Terminal correctness → Ch 19 § State mapping and ownership** (Ch 19 should cite Ch 15 as the source of its "canonical local state"; owner: Ch 19).

## Transition Problems

- **In (Ch 14 → 15).** Strong ("Human control introduces waits…"). The case box picks up the same wait.
- **Within.**
  - Two framing H2s (`:1125`, `:1133`).
  - § Terminal correctness interrupts the durable-state explanation before the lifecycle that produces terminals.
  - § The lifecycle of a durable run is an empty wrapper.
  - § Let events resume work… opens with a general table before any event material.
  - An empty H3 (`:1194`) is followed immediately by a sibling H3.
  - The evidence table is wedged between two callout boxes (`:1251–1265`).
- **Out (Ch 15 → 16, `:1354`).** False claim (see above). The replacement depends on the Ch 16 decision (chapter-16.md C16-R01). It should say that Ch 10–15 have defined the loop and workflow patterns, that Ch 16 helps choose and compose them, and that Ch 17 names the failure shapes.

## Redundant and Repetitive Concepts

| Concept | Occurrences in Ch 15 | Verdict |
| --- | --- | --- |
| "State must outlive processes and deployments" | `:1127–1131`, `:1135`, `:1173`, `:1271` | `:1135` restates `:1127`. Merge the two framing H2s. The table and card are template (keep). |
| Transcript ≠ durable state | `:1146`, COMMON PITFALL `:1265` | The box repeats the section. Fold its last clause into `:1146` and delete the box. |
| Checkpoint field list | `:1185`, `:1230` | Two drifting lists. The contract gives purpose; the record gives fields. |
| Unknown effect / at-least-once | `:1237`, box `:1253`, card `:1300`, `:1323`, `:1331`, Q `:1349` | Delete the box. The rest are short recalls (keep). |
| Build compatibility for in-flight runs | `:1204` (Version Router), `:1248`, `:1333`, Q `:1350` | Internal reinforcement. Acceptable. The Ch 27 overlap is handled below. |

## Cross-Chapter Duplication

| Other location | What repeats | Verdict |
| --- | --- | --- |
| Ch 03 § The restart test (`01-part-i.md:1127–1131`) | The run must survive worker loss and SDK replacement | Reinforcement (Ch 03 states the test, Ch 15 the mechanism), but it needs the explicit link (C15-R02). |
| Ch 03 § The complete execution path (`01-part-i.md:1203–1217`), Ch 04 § End-to-end responsibility flow | End-to-end walkthrough | Three walkthroughs. Ch 15 is the canonical detailed version (agrees with map §3). Ch 03's should shrink to a pointer (owner: Ch 03). Ch 04 keeps its overview (owner: Ch 04). |
| Ch 04 § Run API (`02-part-ii.md:159–170`) | POST runs, GET run, signal, cancel, events/history | **Redundant.** I **disagree with the map** (§3 "Run API: Ch 15, with Ch 04 summarizing"). Ch 04 should hold the one base table, because it is the contracts chapter, the reader meets it eleven chapters earlier, and it already carries signal, cancel, update, and fork. Ch 15 should list only the durable-execution additions (`events:ingest`, `:pause`, `:resume`, `:migrate`) and the durable semantics of signal and cancel. Owner of the merged base table: Ch 04 (absorb Ch 15's "202, home region, pinned manifest" into its POST row). See C15-R08. |
| Ch 04 § Event contract / § CloudEvents and outbox contracts (`02-part-ii.md:206–262`) | CloudEvents envelope fields, outbox | **Redundant.** Ch 15 keeps only the correlation-to-wait rule and the DLQ sentence. |
| Ch 22 § A reliable protocol for changing the outside world (`06-part-vi.md:665–681`) | Unknown effects, at-least-once, stable key, reconcile | Ch 15 PRODUCTION CONSIDERATION is **redundant** pre-teaching. Rule `:1237` plus a "(Chapter 22)" pointer suffices. |
| Ch 27 § Rollback and active runs (`08-part-viii.md:162–166`) and § Compatibility and long-running execution (`:320–326`) | Active runs stay on compatible workers or tested migration; regional recovery fences, restores, reconciles, resumes | Split ownership. Ch 15 owns the *mechanism* (workflow versioning, replay compatibility, `WorkflowMigration`, continue-as-new). Ch 27 owns the *release policy* (rollback reassigns new work only) and regional recovery. The Ch 15 failover bullet (`:1247`) is **redundant** (shrink it to a pointer). The build-compatibility bullet and Q5 are reinforcement (keep, with a pointer). Ch 27's bullet "Workflow compatibility includes replay behavior, activity names/schemas…" (`08-part-viii.md:323`) should point back to Ch 15 (owner: Ch 27). |
| Ch 14 § Workflow integration (`:954–961`) | Approval wait, timers, outbox, resume | Reinforcement (a specific instance). Ch 15's resume flow should name it as an instance. |
| Ch 14 § What changes as usage grows `:971` | Home region, fence after failover | Redundant (handled in C14-R08). |
| AP-01, AP-02 (`:1550–1622`) | Lost work on restart; transcript as state | Reinforcement (anti-pattern framing). |
| P-02, P-11 (`:1387–1393`, `:1477–1483`) | Durable workflow spine; durable runtime | Redundant summaries (handled in chapter-16.md). |
| Ch 19 § State mapping and ownership (`05-part-v.md:531–539`) | "Canonical local state" names | Ch 19 uses a canonical list that nobody defines. Ch 15 should define it (C15-R04), and Ch 19 should cite it (owner: Ch 19). |

## Structural Recommendations

Re-sequence the H2s so that the headings match the content and the lifecycle comes before the terminal states. The current material maps as follows (only moves and merges; no new section trees):

1. **§ Why long-running work needs durable state.** Merge the current `:1125` and `:1133` into one framing H2, followed by the state-owner table.
2. **§ Durable state is more than chat history.** Figure 15-1, `:1146`, `:1148`, and the restart-test recall.
3. **§ The durable execution contract.** The Required-analysis table (`:1171–1179`), § Durable execution contract, and § Checkpoint policy.
4. **§ The lifecycle of a durable run.** § Canonical control flow, now with pattern pointers, and § Terminal correctness, moved here and expanded.
5. **§ Let events resume work without losing control.** § Event-driven resume flow (filled) and a condensed § Event architecture.
6. **§ A workable implementation and the template tail.** As now, with the condensations below.

## Concrete Recommended Changes

1. **C15-R01 · Medium · Merge.**
   - **Location:** `04-part-iv.md:1125–1140`, § Why long-running work needs durable state and § Model long-running work explicitly.
   - **Issue:** Double framing H2.
   - **Change:**
     - Keep the `:1125` heading and `:1127–1131`.
     - Append from `:1135` only the sentence listing what must be durable ("intent, state transitions, pending obligations, timers, child tasks, approvals, and external effects. Workers can then disappear and return without becoming the owners of truth.").
     - Delete the `:1133` heading and the rest of `:1135`.
     - Keep the state-owner table under the merged H2.

2. **C15-R02 · Medium · Cross-reference / Condense.**
   - **Location:** § Durable state is more than chat history (`:1146`); COMMON PITFALL (`:1263–1265`).
   - **Issue:** There is no link to Ch 03's restart test, and the pitfall box repeats the section.
   - **Change:**
     - Add after `:1146`: "This is Chapter 3's restart test made operational: a run must resume from its recorded decisions, approvals, and effect receipts even if every message and every worker is discarded."
     - Delete the COMMON PITFALL box.
     - Replace "Northstar uses event history to rebuild a canonical RunState" with "The platform rebuilds run state from event history" (or apply the §6 T1 decision).

3. **C15-R03 · High · Move/Rewrite.**
   - **Location:** § The lifecycle of a durable run (`:1154`) and ### Canonical control flow (`:1156–1167`).
   - **Issue:** The empty wrapper, the missing pattern links, the orphan "requested autonomy", the unnamed RunManifest, the fourth name for the six gates, and the unsignposted Ch 21/22/25 dependencies.
   - **Why it matters:** This list is where Part IV's six patterns compose into one run. Without the links, Part IV reads as six independent chapters.
   - **Change:** Keep the 10 steps and edit in place:
     - Step 1: replace "requested autonomy" with "requested scope".
     - Step 2: append "— the RunManifest (Chapter 4)".
     - Step 3: append "(capability envelopes, Chapter 21)".
     - Step 4: append "(plan compilation, Chapter 12; risk classes, Chapter 22)".
     - Step 5: append "routed workers (Chapter 11) and bounded ReAct activities (Chapter 10)" and "(credentials, Chapter 21)".
     - Step 7: append "(approval and intervention, Chapter 14)".
     - Step 8: replace "propose → preview → approve → commit" with "pass the six gates (Chapter 2); critique may revise a draft but acceptance decides (Chapter 13)".
     - Step 10: append "(Chapter 25)".
     - Give the H2 a one-sentence lead: "Every pattern in Chapters 10–14 runs inside this lifecycle."
     - Move ### Terminal correctness here, after the list (see C15-R04).
   - **Related:** Ch 03 § The complete execution path should shrink to a pointer to this list (owner: Ch 03).

4. **C15-R04 · High · Move/Expand.**
   - **Location:** ### Terminal correctness (`:1150–1152`), moved under § The lifecycle of a durable run after step 10.
   - **Issue:** It is the canonical run-terminal home but has only three sentences, and seven terminal vocabularies drift across the book (§6 T12).
   - **Change:** **Reconciled (see overall-book-review.md §D-14):** As stated, except the last bullet: use the same terminal names as Ch 18's task lifecycle (C18-R03). Ch 18 reuses this table's terminal states for tasks, and Ch 19 maps remote A2A states onto Ch 18 (C19-R04), so Ch 19 cites Ch 18, which cites this table.
     - Keep the three sentences.
     - Add one table, *Run state | Reached when | Never reached by*, with rows:
       - `Running/Waiting` (non-terminal; includes NeedsInput and approval waits)
       - `CancelRequested` (non-terminal until in-flight effects reconcile)
       - `Succeeded` (acceptance passes over authoritative state; never by model text, which is AP-07)
       - `Failed` (a permanent failure with no unknown effects)
       - `Canceled` (cancellation intent recorded and every effect committed, compensated, or declined)
       - `Expired` (deadline or wait expiry under explicit disposition)
       - `InterventionRequired` (correctness cannot be established automatically; opens an intervention task, Chapter 14)
     - Add one sentence relating the levels: step dispositions (Chapter 10) feed the workflow, acceptance decides (Chapters 2 and 13), and no run may close while an effect is Unknown (Chapter 22 owns effect states and compensation).
     - Use the names already used in Ch 19 `05-part-v.md:531–539`.
   - **Related:** Ch 19 cites this table (owner: Ch 19). AP-07's outcome list aligns to it (C17-R07). The Ch 01 vocabulary row "Compensation → Chapter 15" (`01-part-i.md:445`) should read "Chapter 22" (owner: Ch 01).

5. **C15-R05 · High · Rewrite (fill the empty heading by moving text).**
   - **Location:** ### Event-driven resume flow (`:1194`); ### Event architecture (`:1196–1198`); § Who should own each decision (`:1204`); § Execution and persistence rules bullet 2 (`:1236`).
   - **Issue:** There is an empty H3, the resume steps are scattered, and the event section re-specifies Ch 04.
   - **Change:**
     - Under ### Event-driven resume flow, write five numbered steps using existing sentences:
       1. Before reporting the run as waiting, the workflow persists a WaitRegistration (accepted sources, schemas, correlation keys, expiry).
       2. Event Ingress authenticates the event and writes the SignalInbox receipt (unique tenant, source, and event ID).
       3. The Correlator matches the event to the registration, or holds it as unmatched.
       4. The signal or timer wakes the workflow, which revalidates authorization and resource versions after the wait.
       5. The workflow continues from the last checkpoint, or supersedes stale approvals (Chapter 14 § Workflow integration is the approval instance).
     - Delete `:1236`'s duplicate wording, keeping a short rule: "Wait registration before acknowledgment; inbox before signal".
     - Condense ### Event architecture to: "Events use the Chapter 4 CloudEvents envelope; producers use a transactional outbox and consumers an inbox (Chapter 22). Durable execution adds one rule: every correlation key must resolve to a wait registration or an unmatched-event holding area. A dead-letter queue is quarantine and diagnosis—not a substitute for domain compensation."

6. **C15-R06 · Medium · Move/Rename.**
   - **Location:** § Let events resume work without losing control (`:1169–1192`).
   - **Issue:** The heading covers only the event H3s.
   - **Change:** Rename this H2 to `## The durable execution contract`. Keep the Required-analysis table, ### Durable execution contract (rename it `### Workflow, activity, signal, query, update`), and ### Checkpoint policy under it. Create `## Let events resume work without losing control` after § The lifecycle of a durable run, holding the two event H3s from C15-R05. In the contract's Checkpoint bullet (`:1185`), replace the field list with "the replay position and state reference from which a compatible worker resumes (fields in § Records worth preserving)".

7. **C15-R07 · Medium · Remove.**
   - **Location:** PRODUCTION CONSIDERATION (`:1251–1253`).
   - **Issue:** Pre-teaches Ch 22 for the fourth time. Rule `:1237` already covers it.
   - **Change:** Delete the box. Append "(Chapter 22)" to rule `:1237`.

8. **C15-R08 · Medium · Condense (cross-chapter).**
   - **Location:** ### The contracts between components (`:1206–1218`).
   - **Issue:** It duplicates the Ch 04 Run API with naming drift.
   - **Change:**
     - Keep the rows `POST /v1/events:ingest`, `:pause`, `:resume`, `:migrate`.
     - Replace the POST runs / GET run / signal / cancel / history rows with one sentence: "The base Run API is in Chapter 4. Durable execution adds these operations and two semantics: `:signal` carries event ID, correlation key, schema version, and expected state; `:cancel` is durable intent with propagation and compensation policy, never immediate termination."
     - Use Ch 04's `GET /v1/runs/{id}/events` name for history.
   - **Owner:** Ch 04 absorbs "returns 202, run ID, home region, pinned manifest, and status URL" into its POST row.
   - **Related:** C14-R09 removes `:operatorAction`. This is a disagreement with the map §3 (Run API row), explained above.

9. **C15-R09 · Medium · Condense.**
   - **Location:** ### Scalability and multi-region behavior (`:1247`, `:1248`).
   - **Issue:** Regional failover restates Ch 27.
   - **Change:**
     - Replace `:1247` with "Assign each run one home region with one writer per generation; Chapter 27 covers fencing, restore, reconciliation, and resume during regional recovery."
     - Keep `:1248` and append "Chapter 27 makes this release policy: rollback reassigns new work only."

10. **C15-R10 · Medium · Rewrite (citation scope).**
    - **Location:** § What the evidence lets us conclude (`:1257–1261`).
    - **Issue:** The "Recovery objective" claim cites R04 (CloudEvents envelope) and R02 (durable execution) beyond their recorded `supports`.
    - **Change:**
      - Either relabel the row as a book-authored recommendation, or replace it with a claim R02 does support ("Durable execution preserves workflow progress across crashes and long waits through replay and durable timers [R02]").
      - Move the RTO/RPO/DR statement to Ch 27, which owns regional recovery (owner: Ch 27 decides whether to keep it).
      - Drop R04 from the footer unless the condensed § Event architecture keeps a CloudEvents citation (it can cite R04 there for the envelope only).

11. **C15-R11 · Medium · Rewrite.**
    - **Location:** § Where this leads next (`:1354`).
    - **Issue:** False claim.
    - **Change:** Replace with: "Chapters 10–15 have defined the loop and workflow patterns; Chapter 16 helps choose among them and shows how they compose in one run, and Chapter 17 names the failure shapes that the rest of the book corrects."
    - **Related:** chapter-16.md C16-R01 (this wording assumes the slim Ch 16).

12. **C15-R12 · Low · Rewrite/Cross-reference.**
    - **Locations and changes:**
      - § Put the idea to work exercise 1 (`:1339`): change "ten-day" to "nine-day", matching the case box `:1119`.
      - § What to verify, item 3 (`:1331`): append "(Chapters 3 and 22)".
      - § If this fails in production (`:1319–1323`): add a fourth line, "If state lives in a transcript or in one process, the repair is structural; see AP-01 and AP-02 in Chapter 17."
      - § A sensible place to start (`:1312`): add the lead sentence "The reducer folds recorded events into run state and performs no I/O, so replaying the same history always yields the same state."
      - ### Who should own each decision (`:1204`): convert to the two-column Component | Responsibility table used in Ch 12 and Ch 14.

13. **C15-R13 · Low · Rewrite (terminology).**
    - **Location:** `:1119`, `:1179` ("employment document(s)"), `:1146` ("Northstar").
    - **Change:** Apply the synthesizer's §6 T15 and T1 decisions.

14. **C15-R14 — Low — Rewrite.** *Added in reconciliation (see overall-book-review.md §D-27).*
   - **Location:** `04-part-iv.md:1159` (Canonical control flow, step 2 Snapshot).
   - **Issue:** "prompt/skill bundle" conflates two release objects (Ch 08 thesis); the Ch 08 review asked Ch 15 to fix it.
   - **Change:** Write "…the agent, workflow, prompt bundle, resolved Skill digests (Chapter 8), policy, model route, tool schemas, and knowledge index". Apply together with C15-R03's step 2 change ("— the RunManifest (Chapter 4)").
   - **Related:** C15-R03, C04-R20, C27-R15.

15. **C15-R15 — Low — Rewrite (card policy).** *Added in reconciliation (see overall-book-review.md §D-04).*
   - **Location:** `04-part-iv.md:1267–1306`, § How Long-Running Agents work in practice.
   - **Issue:** The card policy (C10-R04) had no Ch 15 reciprocal.
   - **Change:** Retitle the H2 "Durable execution at a glance". Delete THE ENGINEERING PROBLEM box and the lead sentence. Keep the tables and signals, including the "Unknown mutation → Freeze dependents and reconcile" row. Appendix A's P-11 card points here (C16-R10).
   - **Related:** C10-R04, C16-R10.

## Verification log

Second-pass fact check against `source/parts/*.md`, `source/original/*-source.md`, `config/references.json`, `examples/runtime/durable_state.py`, and `config/examples.json`.

- **Line references checked / fixed:** 78 checked; 0 fixed. Ch 04 `:update` is at `02-part-ii.md:168` (review says `:167`; within tolerance). Ch 04 Run API `:159–170`, § Event contract `:206`, § CloudEvents and outbox contracts `:258`, Ch 27 `:162–166` and `:320–326`, Ch 19 `:529–539`, Ch 03 `:1127–1131` and `:1203–1217`, Ch 01 `:445` all confirmed.
- **Claims removed:** none.
- **Claims softened:**
  - "Ch 16's P-06–P-11 are built in Ch 18–28" (twice): P-08 (EffectRecord, named in Ch 03/04; unknown state previewed in Ch 04 `:204` and Ch 15 `:1253`) and P-11 (Ch 15) are partly grounded.
  - "orphan 'autonomy level' concept": the term appears in Ch 02's principles and Ch 04's Run API; it is undefined, not unused.
  - "Its field list differs from Ch 04's JSON": made precise (Ch 04's envelope is a Python model; the exact field differences are now listed).
- **Important claims confirmed:**
  - `### Event-driven resume flow` (`:1194`) is an empty heading followed directly by `### Event architecture` (`:1196`); it is equally empty in both originals (`v3.0-source.md:3030`, `v3.1-source.md:3032`).
  - `## The lifecycle of a durable run` (`:1154`) wraps exactly one H3; `## A sensible place to start` (`:1312`) is an empty H2 over one H3; `### Terminal correctness` (`:1150–1152`) is three sentences under § Durable state is more than chat history.
  - Checkpoint field drift: `:1185` "effect ledger cursor … version pins" vs `:1230` "artifact/effect cursors, code compatibility range".
  - Run API overlap: five of Ch 15's nine rows (POST runs, GET run, `:signal`, `:cancel`, history) match Ch 04 `02-part-ii.md:163–167`; Ch 04 names history `GET /v1/runs/{id}/events`, Ch 15 `GET …/history?cursor`.
  - R04 `supports` is "a portable event envelope and event identity semantics"; R02 is "crash-resilient workflow execution, replay, durable timers, and long-running processes". Neither mentions RTO/RPO, failover, or DR, so the `:1259` row exceeds both scopes.
  - Exercise 1 `:1339` says "ten-day"; the case box `:1119` says "nine days".
  - "Canonical local state" first appears in Ch 19 (`05-part-v.md:509`, `:531`); nothing earlier defines it. Ch 01 `:445` does route Compensation to Chapter 15, while the Compensating/Compensated states are defined in Ch 22 `06-part-vi.md:669`.
  - `:1247` restates Ch 27 `08-part-viii.md:166` (fence, restore, reconcile, resume); `:1248` overlaps `08-part-viii.md:322–323` and Q5 `:1350`.
  - "Chapter 16" is cited by number nowhere in the book except `:1354`; Ch 16 has no card for routing, plan compilation, critique, or human review.
- **Recommendations amended:** none in substance. C15-R04 already carries the D-14 reconciliation; C15-R08 matches D-03; C15-R09's heading pointer must follow D-32 ("Roll back assignment, not history") when applied.
- **Not verified:** the map's "fourth of five pre-teachings" count for the unknown-effect rule, and §4/§6 row identifiers, were taken as given.
