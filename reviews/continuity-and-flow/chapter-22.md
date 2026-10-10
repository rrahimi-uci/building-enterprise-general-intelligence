# Chapter 22 — Make External Effects Safe to Retry: Continuity and Flow Review

Reviewed: `source/parts/06-part-vi.md:634–1019`, plus the close of Ch 21 (`:597–632`), the opening of Ch 23 (`:1021–1051`), and the earlier teachings of the same concepts: Ch 02 (`01-part-i.md:698–734`), Ch 03 § The same rule applies to writes / § One retry owner (`01-part-i.md:1092–1202`), Ch 04 § Effect receipt / § CloudEvents and outbox contracts (`02-part-ii.md:202–258`), Ch 12 (`04-part-iv.md:465`, `:518`), Ch 15 (`04-part-iv.md:1253`, `:1300`, `:1349`), AP-04/AP-05 (`04-part-iv.md:1707–1766`), Ch 26 § Match the control to the risk (`08-part-viii.md:60`), and the examples behind `[[EXAMPLE:effect-idempotency]]` and `[[EXAMPLE:governed-tool-gateway]]`.

## Overall Assessment

Chapter 22 should be the book's canonical home for effect safety: the logical effect key, the intent hash, expected versions, receipts, the Unknown state, reconciliation, compensation, risk classes, and the ToolManifest. All the material is present, and much of it is excellent. In particular:

- the property table (`:683–688`): approval, idempotency, preconditions, and receipts each close a different failure;
- the failure-response table (`:823–834`);
- the transaction-boundary bullets (`:892–895`).

The chapter is, however, two chapters stacked on top of each other:

- **Two implementation sections.** There are two § A workable implementation blocks (`:726`, `:846`), each with owners, contracts, records, and a scale list. EffectRecord is defined twice with different fields (`:769` vs `:870`). `effects/{id}:reconcile` and `effects/{id}:compensate` appear in both API tables (`:752–753` vs `:859–860`). Two components with the same job appear under different names: "Health/Quota Service" (`:739`) and "Dependency Health Service" (`:850`).
- **Two Required-analysis tables** (`:692`, `:811`). The first carries an off-thread HR salary example.
- **Its concepts arrive pre-taught.** Unknown outcome is taught at least five times before this chapter (Ch 02 Verify gate, Ch 03 § One retry owner, Ch 04 § Effect receipt, Ch 15 PRODUCTION CONSIDERATION, AP-05). R0–R4 risk classes are used in Ch 12 and Ch 21 before they are defined here (`:714`). Ch 22 never acknowledges any of this. A reader arriving from Ch 21 meets the same explanations a sixth time, with no signal that this is now the full treatment.
- **The chapter's own runnable example does not model its central case, and its exception path would treat a timeout as a clean failure.** `examples/foundations/effect_idempotency.py` scopes itself (docstring) to at-least-once replay: "the ledger guarantees the intent commits once, even if the agent, the queue, or the operator retries it". Its only Unknown path is a concurrent in-flight key. When `apply()` raises *any* exception, the `finally` block releases the key and nothing is recorded, so a `TimeoutError` from a dispatched mutation would leave the key retryable: the AP-05 sequence (timeout → failed → retry). The test `test_failure_does_not_poison_the_key` exercises a `RuntimeError("downstream 500")`, which is a received response rather than a timeout, so the test itself is closer to the chapter's Declined case than to AP-05; what is missing is any test or code path for the ambiguous outcome. Below it, an inline InMemoryEffectLedger excerpt implements the Unknown semantics, so the section holds two ledgers with different behaviour on failure. [verified: softened — the test's 500 case is a defensible Declined; the AP-05 reading applies to the undifferentiated exception path, not to the asserted case; "teaches the opposite of its thesis" overstated]
- **The checklist omits the chapter's central rule.** § What to verify before production has no check for Unknown outcomes. It does have a check ("Commands and facts are distinct…", `:992`) that the chapter never teaches.

Verdict: keep Ch 22 in Part VI (see the disagreement with the map below). Merge it into one argument and one implementation block. Make it explicitly the canonical home for Unknown and for risk classes, and fix the example.

## Intended Reader Mental Model

After this chapter the reader should hold:

1. **A mutation is a recorded intent, not a call.** The logical effect key identifies the business intent. The intent hash stops the key being reused for a different action. The expected version stops a stale overwrite.
2. **Four controls, four failures.** Approval (authority), idempotency (duplication), preconditions (staleness), and receipt/reconciliation (proof). None substitutes for another.
3. **Unknown is a state, not an error.** A dispatched mutation without a receipt or proof of absence is Unknown. Dependent work stops, and a reconciler decides Committed, Declined, Partial, or InterventionRequired. Compensation is a new authorized effect and never an erasure.
4. **Risk classes R0–R4 set default controls per tool,** declared in an immutable ToolManifest and resolved at dispatch.
5. **Exactly one retry owner per failure class,** under a timeout hierarchy and a shared retry budget.

What the reader already has: the six gates (Ch 02), the effect-receipt fields (Ch 04), durable activities (Ch 15), AP-04 and AP-05, approval binding (Ch 14), and delegated grants (Ch 21).

## Section-by-Section Flow Review

**Opening boxes (`:636–642`).**
- The case box (LOS timeout) and design choice ("one logical effect key, intent hash, expected version, downstream request ID, receipt, and reconciliation state per mutation") are good.
- There is no evidence-context blockquote, unlike Ch 20, 21, and 23. That is acceptable, but it is a template gap.

**§ Why retries become dangerous when the outside world may have changed (`:644`).**
- *Role:* intro.
- *Adds:* "a write path that can be retried because its meaning—not just its network request—is recorded" (strong).
- *Missing:* the link to Ch 20, whose Figure 20-1 calls the effect boundary "the control that cannot be skipped". Also missing is any acknowledgement that Ch 02/03/15/AP-05 already introduced the Unknown rule (C22-R03).

**§ Follow a proposed action to a verified effect (`:652`).**
- *Role:* the gateway's two jobs plus the state-owner table.
- *Adds:* "protects the capability before dispatch, and proves the downstream outcome after dispatch" (an excellent mental model).
- *Issue:* `:657–659` (approval / idempotency / concurrency) is said again at `:673` and a third time in the property table (`:683`).
- *Also:* the state-owner table names "EffectReceipt" and "ReconciliationTask", but the chapter defines no EffectReceipt record and calls the record "ReconciliationCase" (`:875`).
- *Verdict:* condense (C22-R08, C22-R13).

**§ A reliable protocol for changing the outside world (`:665`).**
- *Role:* the core protocol: the state machine, receipt content, the Unknown path, the failure timeline, and the property table.
- *Verdict:* the chapter's best section, and it should be the canonical statement of Unknown.
- *Issues:*
  - The definition of Unknown is split: `:667` names it ("gives that ambiguity a name—unknown"), the one-clause definition sits in the second implementation block (`:884`, "**Unknown** means the system lacks proof and must stop dependent work"), and the fullest statement is design-review Q3 (`:1013`). None sits at the head of this section. [verified: corrected — "appears only in Q3" was wrong; `:884` defines it in the body]
  - Figure 22-1 and the terminal-state definitions (`:879–888`) sit inside the *second* implementation block, about 200 lines after the states are first listed (`:669`).
- *Fix:* C22-R03.

**§ Give tools explicit contracts and narrow authority (`:690`).**
- *Role:* the tool contract.
- *Contents:* the first Required-analysis table (`:692–700`), then H3s.
- *Issues:*
  - The table's "Recommended architecture" row gives an eight-stage invocation order that differs from § Invocation sequence (`:780–789`) and from Ch 02's six gates.
  - Its "Enterprise example" (HR salary change) is off-thread.
- *Verdict:* delete the table (C22-R02).

**§ What a ToolManifest must declare (`:702`).**
- *Role:* the manifest field groups.
- *Verdict:* good and canonical. Ch 02 names ToolManifest in its state-owner table (`01-part-i.md:665`) and its example defines only a minimal dataclass (`governed_tool_gateway.py:39`); the field groups are defined only here. Ch 05 (`02-part-ii.md:430`) points here. [verified: corrected — the Ch 02 example does define a `ToolManifest` class; the chapter prose does not define the field groups]
- *Issue:* the DEVELOPER GUIDELINE box (`:805–807`) restates this section 100 lines later. Its one new point, "resolve the manifest at dispatch, not at import", belongs here (C22-R09).

**§ Risk classes (`:714`).**
- *Role:* the R0–R4 definitions.
- *Verdict:* correct content, defined too late. Ch 12 uses `"risk_class": "R1"` and "R4 commit" (`04-part-iv.md:465`, `:518`), Ch 02 § Scaling the shell uses "risk class" (`01-part-i.md:734`), and Ch 21 forward-references it (`:495`).
- *Issues:*
  - The section does not distinguish R0–R4 from Ch 26's governance tiers 0–4 (`08-part-viii.md:62–68`, where Tier 3 "Protected action" roughly equals R3/R4).
  - The MCP paragraph (`:724`) restates Ch 19 (`05-part-v.md:600`).
- *Fix:* C22-R05, C22-R09.

**§ A workable implementation (`:726`), with § Who should own each decision (`:728`), § The contracts between components (`:741`), § Records worth preserving (`:761`), § Invocation sequence (`:775`), § What changes as usage grows (`:794`).**
- *Role:* first implementation block (tool side).
- *Owners:* "Credential Broker" is Ch 21's Access Broker/STS, and "Sandbox Broker" is Ch 23's Sandbox Control Plane.
- *Contracts:* good. The 200/202/typed-error bullets (`:757–759`) are unique and valuable.
- *Records:*
  - SandboxLease (`:770`) duplicates Ch 23 (`:1137`).
  - ToolHealth overlaps CircuitState (`:876`).
  - The unique-constraint sentence (`:773`) is excellent.
- *Invocation sequence:*
  - Good, but it is not mapped to the six gates.
  - Its order (create the effect record, step 3, *before* approval, step 4) contradicts Figure 22-1, where the approval gate comes before Reserved and "denied/expired → Declined" implies a record already exists.
- *Scale list:* its partitioning bullet (`:797`) and limits/breaker bullet (`:800`) overlap the second block's (`:899`, `:902`); the other six bullets are distinct from the second list. [verified: softened — "half its bullets" overstated; two of eight overlap]
- *Verdict:* merge with the second block (C22-R01, C22-R06, C22-R07).

**§ Design for ambiguous outcomes, not just clean failures (`:809`).**
- *Role:* the reliability half.
- *Contents:* a second Required-analysis table (`:811–819`), whose Enterprise example is Harborlight, which is good.
- *Verdict:* keep this table if any is kept (C22-R02).

**§ Choose the response that matches the failure (`:821`).**
- *Role:* the failure-response table.
- *Verdict:* excellent and canonical (map: one retry owner → Ch 22). It supersedes Ch 03's four-row table (`01-part-i.md:1190–1195`).
- *Note:* the rows for model 429, child task failure, and budget exhausted belong to Ch 19, Ch 18, and Ch 10/28. Keep them, because the table's value is that it puts every failure class in one place, but add chapter pointers in the cells.

**§ The mechanics that make retries safe (`:836`).**
- *Role:* seven mechanisms.
- *Verdict:* canonical for the timeout hierarchy, retry ownership, and sagas.
- *Issue:* the "Graceful degradation" bullet (`:844`) duplicates Ch 28 § Decide what the system may drop or defer (`08-part-viii.md:505`), which the map names canonical. Reduce it to a pointer (C22-R13).

**§ A workable implementation (`:846`), with § Who should own each decision (`:848`), § The contracts between components (`:852`), § Records worth preserving (`:866`), § The lifecycle of an external effect (`:879`), § Where transaction guarantees begin and end (`:890`), § What changes as usage grows (`:897`).**
- *Role:* second implementation block (effect side).
- *Owners:* given as prose rather than a table, which is inconsistent with the first block.
- *Contracts:* `effects:begin`, `:recordReceipt`, and `:markUnknown` are new; reconcile and compensate are duplicates.
- *Records:* EffectRecord is redefined. OutboxRecord duplicates Ch 04's outbox code (`02-part-ii.md:258`).
- *Lifecycle:* conceptual content in the wrong place (C22-R03).
- *Transaction guarantees:* excellent and unique. Keep.
- *Verdict:* merge (C22-R01).

**SECURITY AND GOVERNANCE box (`:908–910`).**
- "Authorize at invocation, against the subject's delegated grant intersected with the actor's policy." That is Ch 21's content (`:396`, `:407`, `:511`), placed after a scaling list.
- *Verdict:* remove it (C22-R09).

**§ What the evidence lets us conclude (`:912`).**
- *Role:* one claim.
- *Issues:*
  - "until reconciliation establishes committed or absent" uses "absent", which is the reconciler's outcome label in the inline ledger (`:977–979`, `outcome="absent"` → `declined`) and in Appendix B (`09-appendices.md:57`), not a state name. The row should use the state name Declined for consistency with `:669` and `:884`. [verified: softened — "absent" is a defined reconcile outcome, not an undefined word]
  - R03 (outbox) and R04 (CloudEvents) support atomic publication, duplicate-consumer handling, and event identity. They do not support "retrying an unknown write is prohibited". That half is a book-authored recommendation.
- *Fix:* C22-R12.

**§ A sensible place to start (`:920`) / § Effect-state ledger (`:925`).**
- *Role:* code. The empty H2 is followed by `[[EXAMPLE:effect-idempotency]]` and then an inline ledger.
- *Issues:*
  - The example contradicts the Unknown rule (see Overall Assessment).
  - The inline ledger is correct, but it is inline (contrary to AGENTS.md) and densely formatted (semicolon-chained statements).
  - The inline ledger omits Partial, which exercise 1 asks the reader to add. That omission is deliberate but unstated.
- *Verdict:* C22-R04.

**Template sections: § If this fails in production (`:984`), § What to verify before production (`:990`), § Put the idea to work (`:1002`), § Questions to bring to design review (`:1007`).**
- *If this fails:* good. Step 2's state list omits Compensating/Compensated/InterventionRequired. That is acceptable for triage.
- *Verify:*
  - The first check (`:992`) is untaught here; it is Ch 04's event contract.
  - There is no Unknown or reconciliation check, no intent-hash check, and no expected-version check.
  - Check 5 (`:1000`) is Ch 21 reinforcement.
  - *Fix:* C22-R10.
- *Put the idea to work:*
  - Exercise 1 depends on the code omitting Partial (C22-R04).
  - Exercise 2 (an API without native idempotency keys) is the practitioner's hardest case, and the chapter body gives it one phrase, "business predicates" (`:671`) (C22-R14).
- *Questions:* Q4 (`:1014`) is a verbatim copy of Ch 14's question (`04-part-iv.md:1107`) (C22-R11). The other questions are good.

**§ Where this leads next (`:1017`).**
- "Protected effects are governed; Chapter 23 contains the remaining execution, egress, data, privacy, and supply-chain blast radius." Fine.
- "privacy" overpromises against Ch 23's body (see C23-R10).

## Sparse or Underdeveloped Content

- **Reconciling without native idempotency keys.** The text gives only "business predicates" (`:671`) plus an exercise. Add two sentences: query the downstream system by a business predicate (target, intent fields, actor, time window, around the recorded dispatch time); one match is Committed, none after the provider's visibility window is Declined, and more than one or an ambiguous match is InterventionRequired. This is the case that most often defeats teams (C22-R14).
- **Partial.** It is defined in one clause (`:885–886`) and appears in the figure, but it has no Harborlight instance. Add one clause, for example: "the LOS created the document request but the borrower notification failed" (C22-R14).
- **EffectReceipt.** It is named in the state-owner table and described in prose (`:671`), but it has no record row. Ch 04 § Effect receipt has the fullest field list. Ch 22 should own it (C22-R13).
- **Do not expand** sagas, outbox/inbox, or circuit breaking. The bullets are tight and sufficient.

## Missing Conceptual Connections

1. **Unknown outcome (`:667`) → Ch 02 Verify gate (`01-part-i.md:701`), Ch 03 § One retry owner, Ch 15 PRODUCTION CONSIDERATION (`04-part-iv.md:1253`), AP-05.** No backward acknowledgement exists, so the reader cannot tell this is the canonical treatment (C22-R03).
2. **Effect boundary → Ch 20 Figure 20-1 / SECURITY box (`:97`, "Enforce at the effect boundary").** This is what justifies placing the chapter in Part VI, and it is never said (C22-R03).
3. **§ Invocation sequence → Ch 02's six gates.** There is no mapping, so the reader sees a sixth step list (C22-R06).
4. **Risk classes → Ch 12's earlier use and Ch 26's tiers.** There is no back-reference and no distinction (C22-R05).
5. **Property-table row "Approval" (`:685`) → Ch 14 § Approval contract (`04-part-iv.md:900`).** There is no pointer, which invites the duplicated Q4 (C22-R11).
6. **Credential minting (step 5, `:786`; Credential Broker) → Ch 21 Access Broker/STS and `credentials:exchange`.** There is no pointer (C22-R07).
7. **Sandbox Broker / SandboxLease → Ch 23 § Sandboxing and egress rules.** There is no pointer (C22-R07).
8. **OutboxRecord (`:871`) → Ch 04 § CloudEvents and outbox contracts.** There is no pointer. Ch 04 owns the envelope, and Ch 22 owns the delivery semantics (C22-R13).

## Transition Problems

- **Ch 21 → Ch 22.** The Ch 21 closing ("Chapter 22 proves whether a specific tool effect may execute, commit, retry, or recover") is good. The Ch 22 opening is self-contained but never says why a reliability topic sits in a security Part (C22-R03).
- **Within the chapter.**
  - The reader goes through protocol → tool contract → implementation → failure design → implementation again. The second § A workable implementation reads as a restart.
  - Figure 22-1 arrives after the scale bullets.
  - The SECURITY box changes topic after the scaling list.
- **Ch 22 → Ch 23.** Fine, apart from "privacy" (see above).

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict |
| --- | --- | --- |
| Approval ≠ idempotency ≠ concurrency | `:657–659`, `:673`, property table `:683–688`, Q5 `:1015` | Keep the table and Q5. Cut `:673` and shorten `:657–659` to "Each of these controls closes a different failure; the table below shows which." |
| Effect state list | `:669`, `:680–681`, figure, `:883–888`, code `:937`, If-fails step 2 | `:669` and `:883–888` are both canonical text in different places. Merge them (C22-R03). The code and If-fails lists are reinforcement. |
| EffectRecord fields | `:769`, `:870`, code `:944` | Redundant with drift. Keep one record row (C22-R01). |
| reconcile / compensate APIs | `:752–753`, `:859–860` | Redundant. Keep one each (C22-R01). |
| Health/breaker service and records | Health/Quota Service `:739`, Dependency Health Service `:850`, ToolHealth `:771`, CircuitState `:876` | Redundant. One service and one record (C22-R01). |
| Retry ownership | mechanics `:839`, scale `:903`, RetryPolicy `:873`, checklist `:996` | Keep the mechanics bullet (canonical), RetryPolicy, and the checklist. In the scale bullet, keep only the shared retry budget. |
| Invocation order | Required analysis `:697`, § Invocation sequence `:780`, figure | Redundant with drift. Keep the sequence (C22-R02, C22-R06). |
| Partition by tenant + tool/target; idempotency index in one shard | `:797`, `:899` | Redundant. Merge. |
| ToolManifest | § What a ToolManifest must declare, DEVELOPER GUIDELINE box `:807` | Box is redundant. Condense it into one sentence in the section. |
| Required-analysis tables | `:692`, `:811` | Redundant template. Keep at most one (C22-R02). |

## Cross-Chapter Duplication

| Concept | Ch 22 location | Other location | Verdict and owner |
| --- | --- | --- | --- |
| Unknown outcome / timeout ≠ failure | § A reliable protocol… `:665`, lifecycle `:879`, Q3 | Ch 01 Wednesday (`01-part-i.md:104`); Ch 02 Verify row (`:701`); Ch 03 § One retry owner (`:1184–1202`); Ch 04 § Effect receipt (`02-part-ii.md:204`); Ch 10 (`04-part-iv.md:49`); Ch 15 PRODUCTION CONSIDERATION (`:1253`), table row (`:1300`), Q (`:1349`); P-08 (`:1447`); AP-05 (`:1737`); Ch 24 worked example; Appendix B § When an effect may have happened… (`09-appendices.md:52`) | **Ch 22 is canonical.** Reinforcement (keep): Ch 01 narrative, the Ch 02 single-row preview, Ch 10's one sentence, Ch 15's table row and Q, AP-05 (anti-pattern view), Ch 24 (application). Redundant (owners shrink to pointers): Ch 03 § One retry owner table (Ch 03 owner, map S5); Ch 15 PRODUCTION CONSIDERATION box (Part IV owner); Ch 04 effect-receipt field list (Ch 04 owner, moves into Ch 22 per C22-R13). Appendix B: map "absent → Declined, unprovable → InterventionRequired, executing → Executing" to Ch 22's states (Appendix owner). |
| One retry owner per failure class | mechanics `:839`, failure table | Ch 03 § One retry owner; AP-04; Ch 15 checklist (`04-part-iv.md:1331`); Ch 19 LLM Gateway row; Ch 28 limits row | Ch 22 is canonical. AP-04 is reinforcement (it gives the 3×3×2 arithmetic). Ch 03 is redundant (Ch 03 owner). |
| Six-step write path | § Invocation sequence `:775` | Ch 02 § Six gates before anything changes (`01-part-i.md:658`); Ch 03 § The same rule applies to writes (8 steps, `01-part-i.md:1096–1105`); Ch 04 flow; Ch 15 step 8 (`04-part-iv.md:1165`) | Ch 02 owns the gates. Ch 22's sequence is the implementation of them and must say so (C22-R06). Ch 03's 8-step list is redundant (Ch 03 owner). [verified: corrected — Ch 02 heading name] |
| Effect receipt fields | prose `:671`; state table "EffectReceipt" | Ch 04 § Effect receipt (`02-part-ii.md:202–204`) | Move the field list to Ch 22 Records. Ch 04 keeps one sentence and a pointer (**requires Ch 04 owner**). |
| Outbox / inbox | § Where transaction guarantees… `:892`, OutboxRecord `:871` | Ch 04 § CloudEvents and outbox contracts (`02-part-ii.md:258`); Ch 15 § Event architecture | Ch 04 owns the envelope and code; Ch 22 owns the delivery semantics (agrees with map). OutboxRecord references Ch 04. |
| Risk classes R0–R4 | § Risk classes `:714` | Ch 12 (`04-part-iv.md:465`, `:518`); Ch 02 (`01-part-i.md:734`); Ch 15 step 4; Ch 21 `:495`; Ch 23 `:1178`; Ch 24 (`07-part-vii.md:145`); Ch 08 `side_effect_class`; figure "R3/R4 only" | Ch 22 is canonical. **Requires Ch 02 owner:** a one-sentence gloss at first use. **Requires Ch 12 owner:** a pointer. Distinguish from Ch 26 tiers here. **Ch 26 owner:** rename tiers per map T11 (C22-R05). |
| Governance tiers 0–4 | — | Ch 26 § Match the control to the risk | Collision (T11). Resolved by C22-R05 plus the Ch 26 owner. |
| Approval binding question | Q4 `:1014` | Ch 14 Q (`04-part-iv.md:1107`), verbatim | **Redundant.** Replace it in Ch 22 (C22-R11). |
| Credential broker | `:735`, step 5 | Ch 21 Access Broker/STS `:447`, `credentials:exchange` | Ch 21 is canonical (C22-R07). |
| Sandbox broker / SandboxLease | `:737`, `:770`, scale `:801` | Ch 23 Sandbox Control Plane `:1114`, SandboxLease `:1137`, § What changes as usage grows `:1176` | Ch 23 is canonical (C22-R07). |
| MCP authorization | `:724` | Ch 19 `05-part-v.md:600`; T-13 | Redundant. One-sentence pointer (C22-R09). |
| Authorize at invocation against grant ∩ actor | SECURITY box `:910` | Ch 21 `:396`, `:407`, `:511` | Redundant. Remove (C22-R09). |
| Graceful degradation | `:844` | Ch 28 § Decide what the system may drop or defer (`08-part-viii.md:505`); P-11 | Ch 28 is canonical. Pointer (C22-R13). |
| Effect-ledger code | `[[EXAMPLE:effect-idempotency]]`, inline ledger | `[[EXAMPLE:governed-tool-gateway]]` (Ch 02, its own ledger and EffectOutcomeUnknown); AP-05 code | Three ledgers. Ch 22's registered example should be the canonical runnable ledger (C22-R04). Ch 02's stays as an introduction. AP-05's code is the anti-pattern view. |

## Structural Recommendations

**Keep Ch 22 in Part VI. This disagrees with the map, which leaves moving the chapter open as option S6(b).** Evidence:

- Ch 20's layer model ends at the effect boundary ("the control that cannot be skipped", Figure 20-1).
- Ch 20's SECURITY box says "Enforce at the effect boundary" (`:97`).
- Ch 23's fail-closed table ends at "Effect" (`:1162`).
- Moving Ch 22 to Part IV would make both security chapters point across Parts to their final enforcement point.

The cost is real: the reliability rows of the failure table are broader than security. One framing sentence (C22-R03) handles that better than relocating the chapter. If the synthesizer prefers to move it, all recommendations below still apply.

**Target outline (one argument, one implementation):**

1. Opening boxes.
2. **§ Why retries become dangerous…**, plus the bridge to Ch 20 and the acknowledgement of earlier chapters.
3. **§ Follow a proposed action to a verified effect.** The two jobs, the state-owner table, and the property table (moved up from `:683`).
4. **§ A reliable protocol for changing the outside world.** The definition of Unknown; the state machine; Figure 22-1 and the terminal-state paragraph (moved from `:879–888`); receipt content; the failure timeline; reconciliation without native keys; a Partial example.
5. **§ Give tools explicit contracts and narrow authority.** The ToolManifest (with "resolve at dispatch"), Risk classes (with the Ch 26 distinction), and the MCP pointer.
6. **§ Design for ambiguous outcomes, not just clean failures.** At most one Required-analysis table (the mortgage one), the failure table with pointers, and the mechanics.
7. **§ A workable implementation** (single block): owners table; contracts; invocation behaviour; records; § Invocation sequence (mapped to the gates); § Where transaction guarantees begin and end; one § What changes as usage grows.
8. Template sections.

## Concrete Recommended Changes

1. **C22-R01 · Critical · Merge.**
   - *Location:* `:726–807` § A workable implementation (first) and `:846–910` § A workable implementation (second).
   - *Issue:* there are two implementation blocks, with duplicated APIs, a component under two names, two EffectRecord definitions, and two scale lists.
   - *Why it matters:* the reader cannot tell which EffectRecord or which reconcile API is authoritative, and the chapter restarts mid-way.
   - *Change:* keep one block, placed after § Design for ambiguous outcomes, with this content.
   - **Owners:** one table, with these rows:
     - Tool Registry
     - Discovery Service
     - Tool Gateway
     - Connector Runtime
     - Effect Service: logical effect IDs, deduplication, receipts, external outcome state
     - Reconciliation Service
     - Compensation Executor
     - Workflow engine: retry timing and saga order
     - Outbox/Inbox adapters
     - Dependency Health Service: provider limits, latency, error state, breaker status, queue pressure. This merges Health/Quota Service with Dependency Health Service.
     - Exception Service
     
     Replace the Credential Broker and Sandbox Broker rows with one sentence: "Credentials come from Chapter 21's Access Broker/STS; sandboxes from Chapter 23's Sandbox Control Plane."
   - **Contracts:** one table, in this order:
     - `tools:discover`
     - tool versions `GET`
     - `:preview`
     - `:invoke`
     - invocations `GET`
     - `:cancel`
     - `effects:lookup`
     - `effects:begin`
     - `:recordReceipt`
     - `:markUnknown`
     - `:reconcile`, with the merged text: "Query downstream by request ID, idempotency key, or business predicate; move Unknown to Committed, Declined, Partial, or InterventionRequired"
     - `:compensate`, with the merged text: "Start the versioned compensating workflow after fresh authorization; never deletes the original receipt"
     - `dependencies/{id}:report`
     - `dependencies/{id}/availability`
     - `exceptions`
     - `dlq/{id}:redrive`
     
     Keep the 200/202/typed-error bullets.
   - **Records:**
     - ToolVersion, ToolEligibility, ToolInvocation, InvocationAttempt.
     - One EffectRecord with the union of fields: effect ID/version, tenant, tool, logical key, idempotency key, intent hash, target resource, precondition/expected version, state, invocation IDs, downstream IDs, before/after versions, receipt ref, compensation refs.
     - EffectReceipt (new; C22-R13).
     - OutboxRecord (with a reference to Ch 04), InboxReceipt, RetryPolicy, CompensationStep, ReconciliationCase.
     - CircuitState, which absorbs ToolHealth's latency/error/quota/freshness fields.
     - QuarantineRecord.
     - Delete SandboxLease (Ch 23 is canonical).
     - Keep the unique-constraint sentence.
   - **Scale:** one list that merges `:796–803` and `:899–906`:
     - stateless front ends with a digest-cached manifest
     - one partitioning bullet (tenant + tool/target, with the idempotency index in the accepting shard)
     - dedicated pools
     - object references
     - layered limits feeding the scheduler, merged with breaker scope
     - health events
     - connector degradation
     - sharded outbox streaming
     - provider-grouped reconcilers with jitter
     - shared retry budget
     - quarantine redrive
     - post-failover reconciliation of Executing/Unknown
     - append-only receipts with projections
     
     Move "prewarm sandbox images" (`:801`) to Ch 23 § What changes as usage grows if it is not already covered there. Ch 23's `:1176` covers pools, so delete it here.
   - *Related:* C22-R03, C22-R07, C23-R07.

2. **C22-R02 · High · Remove.**
   - *Location:* the Required-analysis table at `:692–700` under § Give tools explicit contracts and narrow authority.
   - *Issue:* it is the second Required-analysis table in the chapter. Its invocation order conflicts with § Invocation sequence, and its HR salary example is off-thread.
   - *Change:*
     - Delete the table. § What a ToolManifest must declare then directly follows the H2. Add a one-sentence lead to the H2: "Every capability sits behind the Tool Gateway and an immutable manifest; discovery returns only what the run may use."
     - Keep the `:811` table (Harborlight example). If the book-wide S16 decision removes these tables, keep only its Enterprise example as a sentence under § Design for ambiguous outcomes.

3. **C22-R03 · High · Move, Add, and Cross-reference (canonical home for Unknown).**
   - *Locations:* `:644–651` § Why retries become dangerous…; `:665–688` § A reliable protocol…; `:879–888` § The lifecycle of an external effect; Q3 `:1013`.
   - *Issue:* Unknown has been taught five times already with no acknowledgement. Its definition sits in a Q table. The figure and terminal-state definitions are buried in the second implementation block. Placement in Part VI is unexplained.
   - *Change:*
     - At the end of § Why retries become dangerous…, add two sentences:
       - "Chapter 20 named the effect boundary as the control a manipulated model cannot skip; this chapter builds it."
       - "Earlier chapters stated the rule that a timeout is unknown, not failed (Chapters 2, 3, and 15; AP-05). This chapter gives it a state machine, records, and a recovery path."
     - Open § A reliable protocol… with the definition lifted from Q3: "An effect is **Unknown** when a mutating request may have reached the downstream system and the platform holds neither a verified receipt nor proof of absence."
     - Move Figure 22-1 and the terminal-state paragraph (`:881–888`) to directly after `:669`. Delete the § The lifecycle of an external effect H3.
     - Move the property table (`:683–688`) up to § Follow a proposed action…, replacing `:657–659`'s list (see C22-R08).
     - Keep Q3 as reinforcement.
   - *Related:* other owners shrink their versions to pointers: Ch 03 § One retry owner (Ch 03 owner), Ch 15 PRODUCTION CONSIDERATION (Part IV owner), Ch 04 § Effect receipt (Ch 04 owner), and the Appendix B state mapping (Appendix owner).

4. **C22-R04 · High · Rewrite (example code) and Move.**
   - *Location:* `:920–982` § A sensible place to start / § Effect-state ledger; `examples/foundations/effect_idempotency.py`; `examples/tests/test_effect_idempotency.py`.
   - *Issue:*
     - The registered example releases the key on any exception from `apply()` without distinguishing a received decline from a timeout, and has no Unknown path for a dispatched mutation (only for a concurrent in-flight key). Its test asserts that a downstream 500 makes the key retryable, which is defensible as a Declined case, but no test covers a timeout, and the code would treat one identically (AP-05's sequence). [verified: softened — see Overall Assessment]
     - The inline ledger has the correct semantics but is inline (contrary to AGENTS.md) and is formatted as semicolon-chained one-liners.
   - *Why it matters:* the chapter's only runnable code omits the chapter's central case, and its failure path does not fail safe for a timeout.
   - *Change:*
     - Replace the body of `effect_idempotency.py` with the inline ledger's semantics: reserved → executing → committed / declined / unknown; intent-hash conflict; reconcile to committed / declined / intervention_required.
     - Distinguish a typed `DownstreamDeclined` error (with proof of no effect → Declined, key released only for a new intent hash) from timeout or transport errors (→ Unknown; `commit()` refuses to re-apply until reconcile).
     - Replace `test_failure_does_not_poison_the_key` with two tests:
       - a declined call is recorded as Declined;
       - a timeout is recorded as Unknown, and a second `commit()` raises instead of re-applying.
     - Keep the existing replay and intent-conflict tests.
     - Delete the inline block and keep only `[[EXAMPLE:effect-idempotency]]` with one lead sentence under the H2, removing the empty-H2 + H3 pattern.
     - Add one sentence: "The example omits Partial and compensation; exercise 1 adds them."
   - *Related:* map §7.3 (effect-ledger code). The Ch 02 example (`governed_tool_gateway.py:222–224`) already marks every connector exception Unknown and raises `EffectOutcomeUnknown`, which is the conservative direction; its only gap is that it has no Declined path for a typed downstream refusal. The Ch 02 owner may align its exception taxonomy with the rewritten Ch 22 example, but there is no AP-05 conflation there. [verified: corrected — the Ch 02 example does not share the failure-vs-unknown conflation]

5. **C22-R05 · High · Add and Cross-reference (risk classes; requires Ch 02, Ch 12, and Ch 26 owners).**
   - *Location:* § Risk classes `:714–722`.
   - *Issue:* the classes are used in Ch 02, Ch 12, and Ch 21 before this definition, and they collide with Ch 26 tiers 0–4.
   - *Change:* **Reconciled (see overall-book-review.md §D-02):** As stated, but replace the added sentence with: "Risk classes classify one tool effect; Chapter 26's use-case tiers (T0–T4) classify a whole use case, and a use case's tier is never lower than its most dangerous eligible effect requires (any R3 or R4 tool means at least T3)." The old wording implied a low-tier use case could hold an R3 tool, which contradicts C26-R01's floor rule. The Ch 02 gloss text is in C02-R13.
     - Keep the table here as canonical.
     - Add after it: "Risk classes classify one tool effect; Chapter 26's governance tiers classify a whole use case. A low-tier use case that invokes an R3 tool still receives R3 controls."
     - **Ch 02 owner:** at § Scaling the shell (`01-part-i.md:734`), add a one-sentence gloss: "risk class (R0 pure transform through R4 irreversible or privileged action; Chapter 22)".
     - **Ch 12 owner:** add "(risk classes, Chapter 22)" at `04-part-iv.md:465` or `:518`.
     - **Ch 26 owner:** rename the governance tiers (for example T0–T4) per map T11.
     - Ch 21's existing forward reference (`:495`) can stay.
   - *Related:* the map lists moving the table earlier as an option. This review prefers a gloss at first use, because Ch 02 is already overloaded.

6. **C22-R06 · Medium · Add and Rewrite (diagram).**
   - *Location:* § Invocation sequence `:775–792`; Figure 22-1 `assets/diagrams/src/effect-lifecycle.gv`.
   - *Issue:* the sequence is not mapped to the six gates, and the figure puts approval before Reserved while the text reserves first.
   - *Change:*
     - Add after the list: "Steps 1–2 are Chapter 2's validate and authorize gates, step 4 its approval gate, steps 3 and 5 commit, and step 6 verify; acceptance stays with the workflow." (Chapter 2's section is § Six gates before anything changes, `01-part-i.md:658`; the gate name follows D-22's "approval" vocabulary.)
     - Edit the figure to proposal → Reserved → (R3/R4) Approval gate → Executing, with "denied/expired" going from the approval gate to Declined. Reserving first lets duplicate proposals awaiting approval share one logical key.
     - Run `make diagrams` and update the checksum.

7. **C22-R07 · Medium · Cross-reference and Remove.**
   - *Location:* owners `:735`, `:737`; record `:770`; scale bullet `:801`.
   - *Issue:* Ch 21's credential components and Ch 23's sandbox components are re-specified here under other names.
   - *Change:* as part of C22-R01:
     - Replace the Credential Broker row with a reference to Ch 21's Access Broker/STS and `credentials:exchange`.
     - Replace the Sandbox Broker row and the SandboxLease record with a reference to Ch 23.
     - In § Invocation sequence step 5, write "Obtain a last-hop credential lease from the Access Broker (Chapter 21)".
     - In the invoke API (`:748`), replace "authority grant" with "capability envelope ID".
   - *Related:* C21-R04, C21-R08, C23-R07.

8. **C22-R08 · Medium · Condense.**
   - *Location:* `:657–659`, `:673`.
   - *Issue:* the approval/idempotency/concurrency triad appears three times in 30 lines.
   - *Change:*
     - Replace `:657–659`'s last two sentences with "Approval, idempotency, preconditions, and receipts each close a different failure:" followed by the property table (moved from `:683`).
     - Delete `:673`.
     - Add a pointer in the Approval row: "(Chapter 14)".

9. **C22-R09 · Medium · Remove and Condense.**
   - *Location:* SECURITY AND GOVERNANCE box `:908–910`; DEVELOPER GUIDELINE box `:805–807`; MCP paragraph `:724`.
   - *Issue:* the security box is Ch 21 content, the guideline box restates the ToolManifest section, and the MCP paragraph restates Ch 19.
   - *Change:*
     - Delete the SECURITY box.
     - Delete the DEVELOPER GUIDELINE box and add its unique sentence to § What a ToolManifest must declare: "Resolve the manifest at dispatch, not at import; a risk class that lives only in a reviewer's memory cannot be enforced."
     - Replace `:724` with: "MCP servers are reached through the same gateway and manifest; Chapter 19 covers protocol-level authorization, including the ban on token passthrough."

10. **C22-R10 · High · Rewrite.**
    - *Location:* § What to verify before production `:990–1000`.
    - *Issue:* the chapter's central rule has no check, and check 1 is untaught here.
    - *Change:*
      - Replace check 1 (`:992`) with: "Every mutation has a logical effect key and intent hash persisted before dispatch; a timeout moves it to Unknown, blocks dependent mutations, and routes it to reconciliation."
      - Add: "Protected writes carry an expected version; a stale version is a conflict, not a retry."
      - Keep checks 2–4.
      - Check 5 may stay as Ch 21 reinforcement, or be cut if the list feels long.

11. **C22-R11 · Medium · Rewrite.**
    - *Location:* Q4 `:1014`.
    - *Issue:* it is a verbatim duplicate of Ch 14 (`04-part-iv.md:1107`).
    - *Change:* replace it with: Q "Why is a receipt, not an HTTP 200, the proof of an effect?" / A "Transport success proves the request was answered, not that the business change landed once at the expected version. A receipt carries the downstream resource ID, resulting version, response hash, and verification evidence that reconciliation can check independently."

12. **C22-R12 · Medium · Rewrite (citation scope).**
    - *Location:* § What the evidence lets us conclude `:916`.
    - *Issue:* "absent" is a reconcile-outcome label, not the state name (Declined), and R03/R04 do not support the prohibition on retrying an unknown write. [verified: softened]
    - *Change:*
      - Split the row in two:
        - "Event delivery | Transactional outbox and CloudEvents identity support at-least-once publication with consumer deduplication | R03; R04".
        - "Effect correctness (book-authored recommendation) | Idempotency is scoped to one logical intent; reusing a key with a different intent is a conflict; an unknown write is not retried until reconciliation establishes Committed or Declined | —". Follow Appendix K's convention for uncited recommendations.
      - Optionally add an evidence-context blockquote for template parity.

13. **C22-R13 · Low · Add, Cross-reference, and Condense.**
    - *Locations:* state-owner table `:663`; Records (merged block); Graceful degradation bullet `:844`; OutboxRecord `:871`.
    - *Issue:* EffectReceipt is named but not defined, ReconciliationTask is named but the record is called ReconciliationCase, degradation duplicates Ch 28, and OutboxRecord duplicates Ch 04.
    - *Change:* **Reconciled (see overall-book-review.md §D-16):** As stated, except the OutboxRecord bullet. Ch 22 owns the record, because Ch 04 deletes its OutboxRecord (C04-R09): "OutboxRecord: event ID, aggregate ID and version, CloudEvent envelope (Chapter 4), publish state, attempts; written in the same transaction as the aggregate change." Use the same wording for C22-R01's Records bullet "OutboxRecord (with a reference to Ch 04)".
      - Add an EffectReceipt record: logical effect ID, idempotency key, downstream request and resource IDs, before/after version, state (committed / declined / unknown), timestamp, actor/subject, response hash, verification query, compensation reference, audit link. These are Ch 04's fields. **Requires Ch 04 owner** to cut `02-part-ii.md:204` to one sentence plus a pointer.
      - Change "ReconciliationTask" to "ReconciliationCase" in the state-owner table.
      - Reduce the degradation bullet to: "Graceful degradation: never degrade authorization, tenant isolation, or audit; Chapter 28 defines what may drop or defer."
      - OutboxRecord: "fields per Chapter 4's outbox contract; written in the same transaction as the aggregate change."

14. **C22-R14 · Low · Add.**
    - *Location:* § A reliable protocol… (after the failure timeline, `:681`).
    - *Issue:* reconciling without native keys, and Partial, have no concrete guidance or case.
    - *Change:* add two to three sentences:
      - "When the downstream API has no idempotency key, reconcile by business predicate: target, intent fields, and a time window around the recorded dispatch. One match is Committed; none after the provider's visibility window is Declined; several, or an unverifiable match, is InterventionRequired."
      - "Partial looks like the LOS creating the document request while the borrower notification fails."

15. **C22-R15 · Low · Cross-reference.**
    - *Location:* § Choose the response that matches the failure `:823–834`.
    - *Issue:* the rows owned by other chapters lack pointers.
    - *Change:* append short pointers in the Default-response cells: model 429 → "(Chapter 19)", child task failure → "(Chapter 18)", budget exhausted → "(Chapter 28)", policy denial → "(Chapter 21)". Do not remove rows. This table is the canonical failure-class map, and **requires Ch 03 owner** to replace Ch 03's four-row table with a pointer here.

16. **C22-R16 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** `06-part-vi.md:733` (Discovery Service row).
   - **Issue:** The Ch 08 review asks Ch 22 to cite Ch 08 for the discovery principle; no Ch 22 item did.
   - **Change:** Append to the row: "—the discovery-is-not-permission rule of Chapter 8, applied to tools".
   - **Related:** C08 Cross-Chapter Duplication.

17. **C22-R17 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** End of § If this fails in production.
   - **Issue:** Same request as C05-R16.
   - **Change:** Add one line: "If every layer retries or a timeout is treated as failure, see AP-04 and AP-05 in Chapter 17."
   - **Related:** C17-R03.

## Verification log

- **Line references checked:** 94 (all `06-part-vi.md` refs for `:634–1019`, plus Ch 01–04, 10, 12, 14, 15, 17, 19, 21, 23, 24, 26, 28 and Appendix B cross-refs); 1 fixed (Ch 02 heading is § Six gates before anything changes, `01-part-i.md:658`, not "§ One proposal, six gates"; the `:258` ref for Ch 04's outbox heading is `:260`, within tolerance and left as is).
- **Claims removed:** none.
- **Claims softened:**
  - "The runnable example teaches the opposite of its thesis / that is AP-05" → the example's exception path does not distinguish a timeout from a received decline and has no Unknown path for a dispatched mutation; the test's 500 case is defensible as Declined. C22-R04 is still warranted, for the missing Unknown path and the undifferentiated `finally`.
  - "The precise definition of Unknown appears only in Q3" → `:884` defines it in the body; the problem is placement.
  - "Ch 02 uses ToolManifest in its example without defining it" → the example defines a minimal dataclass; the field groups are defined only in Ch 22.
  - "half its [scale] bullets duplicate" → two of eight overlap.
  - "'absent' is not a state" → it is the inline ledger's and Appendix B's reconcile-outcome label, mapped to Declined.
- **Important claims confirmed:**
  - Two § A workable implementation H2s (`:726`, `:846`), each with owners, contracts, records, and a scale list. `:reconcile` and `:compensate` appear in both API tables (`:752–753`, `:859–860`). "Health/Quota Service" (`:739`) and "Dependency Health Service" (`:850`) both own breaker state.
  - EffectRecord differs between `:769` (has tool, idempotency key; lacks effect version, logical key, invocation IDs) and `:870` (has effect ID/version, logical key, invocation IDs; lacks tool, idempotency key). The inline code `:944–950` has a third shape (logical_key, intent_hash, state, receipt, downstream_request_id, reconciliation_evidence). C22-R01's union list covers all three.
  - Figure 22-1 (`effect-lifecycle.gv`) routes `proposal -> approval` (R3/R4) `-> reserved`, with `approval -> declined` on "denied/expired"; § Invocation sequence creates the effect record at step 3 and obtains approval at step 4. The order conflict is real.
  - `effect_idempotency.py:34–37`: `try: receipt = apply() finally: self._in_flight.discard(effect_key)`; nothing is recorded on exception. `test_effect_idempotency.py:28–33` raises `RuntimeError("downstream 500")` and asserts the key is retryable. `EffectOutcomeUnknown` is raised only for an in-flight key (`:31–32`). The registry (`config/examples.json`) binds the example to chapter 22 only.
  - The inline ledger's `EffectState` (`:937–938`) omits `partial`; exercise 1 (`:1004`) asks the reader to add it.
  - Q4 `:1014` is byte-identical to Ch 14's `04-part-iv.md:1107` (`diff` empty).
  - Ch 22 contains no backward chapter reference (the only "Chapter" in `:634–1019` is the Ch 23 handoff at `:1019`). Unknown is pre-taught at `01-part-i.md:104`, `:701`, `:1194`; `02-part-ii.md:204`; `04-part-iv.md:49`, `:1253`, `:1300`, `:1349`, `:1737`.
  - R03 scope: "atomic state/event publication and duplicate-consumer considerations"; R04: "portable event envelope and event identity semantics". Neither covers the unknown-write prohibition; C22-R12's split is correct.
  - Ch 26 tiers 0–4 at `08-part-viii.md:62–68` ("3 Protected action"); Ch 12 uses `"risk_class": "R1"` (`04-part-iv.md:465`) and "R4 commit" (`:518`); Ch 02 "risk class" at `01-part-i.md:734`; Ch 21 `:495`.
  - Required-analysis `:697` lists an eight-stage order; `:700` is the HR salary example.
- **Recommendations amended:** C22-R04 (issue and rationale softened; Ch 02 cross-check note corrected: `governed_tool_gateway.py:222–224` already maps every exception to Unknown); C22-R06 (Ch 02 section name; "human authorization" → "approval gate" per D-22). The example rewrite itself still stands and is consistent with D-23. No §12 decision changes.
- **Not verified:** Ch 19 "LLM Gateway row" and Ch 28 "limits row" as retry-ownership restatements (existence of the rows confirmed, wording not compared); Ch 24's "worked example" is the Unknown effect at `07-part-vii.md:74` (confirmed by grep only).
