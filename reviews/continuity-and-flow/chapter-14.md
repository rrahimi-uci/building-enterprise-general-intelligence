# Chapter 14 — Put People Where Their Judgment Matters: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:852–1111`. Context read: Ch 13 close (`:815–850`), Ch 15 opening (`:1113–1135`), Part IV intro (`:1–7`), Ch 03 § Human approval: interruption versus record and § Bind approval to the exact proposal (`01-part-i.md:1133–1154`), Ch 01 human approval gate (`01-part-i.md:542–546`), Ch 22 § A reliable protocol… and § Questions (`06-part-vi.md:665–688`, `:1014`), AP-06 (`04-part-iv.md:1774–1807`), `examples/patterns/approval_gate.py`, `examples/patterns/approval_verification.py`, `assets/diagrams/src/pattern-hitl.gv`.

## Overall Assessment

The chapter's core argument is sound and well placed. Human review only matters if it changes system state. Authorization and intervention are different controls. An authorization is bound to an immutable proposal, expires, and is rechecked before commit. Reviewer capacity is a production constraint. The Ch 13 → Ch 14 → Ch 15 bridges are among the best in the book.

There are three structural problems:

1. **Approval is taught three times inside the chapter, and Ch 03 already pre-taught it.** The request fields are enumerated at `:884`, `:902`, `:944`, and again in inline code at `:1048`. The four lists use four different field sets. Ch 03 (`01-part-i.md:1137`, `:1154`) had already given the field list and the hash check. A reader reaches § Approval contract with nothing new to learn about the binding itself.
2. **Intervention, the concept that is distinctive to this chapter, is named and then abandoned.** All contracts, APIs, records, code, and checklist items concern authorization. `InterventionTask` (`:994`) is never defined. Ch 10 ("terminates or escalates", `:45`), Ch 11 ("human triage", `:193`, `:199`), Ch 12 ("escalate", "human amendment", `:468`, `:544`), and Ch 13 ("escalates with both artifacts", `:678`) all escalate to a human. [verified: corrected — the Ch 11/12/13 line numbers were off by 2–8 lines (`:191`, `:670` are diagram markers; `:460`, `:536` carry neither quoted phrase); the quotations themselves are verbatim at the corrected lines] Ch 14 never says that these escalations land in its intervention queue. That is the most important missing connection in Part IV.
3. **Intervention means two different things.** The prose defines intervention as a system request for human judgment ("asks a person to diagnose, correct, supply information, or choose", `:878`, `:882`). Figure 14-1 defines it as operator-initiated control ("Operator observes a run in flight → Pause · cancel · redirect · adjust budget", `pattern-hitl.gv:21–24`). § Operator console requirements and the Operator Control Service then add a third human role, the operator, without naming it. The reader leaves with an unresolved model of who the humans are.

The chapter is otherwise solid reference material. Its implementation block is heavy on generic scaling bullets, though, and it carries a duplicated design-review answer shared verbatim with Ch 22.

## Intended Reader Mental Model

After Ch 14 the reader should hold:

- **What.** There are three human controls with different authority. *Authorization* approves one exact, immutable proposal before an effect. *Intervention* supplies judgment or correction to a run the system cannot finish alone. *Operator control* is governed commands on a run in flight. None of them substitutes for policy authorization or effect verification.
- **Why.** A click that is detached from the effect, or a summary that can change after approval, makes review theater. Too many approvals cause fatigue, which also degrades safety.
- **How.** A proposal hash, expiry, expected resource version, and separation of duties. Recheck at commit. Supersede on material change. Durable waits with explicit timeout dispositions. Separate queues.
- **When.** Use review for high-risk, irreversible, regulated, ambiguous, or exception decisions. Do not add it for low-risk deterministic work.
- **Trade-offs.** Latency, staffing, and fatigue in exchange for accountable judgment.
- **Relationships.** It builds on Ch 02 (the authorize gate), Ch 03 (an SDK interruption is not an approval), and Ch 10–13 (escalation sources). It feeds Ch 15 (durable waits), Ch 21 (approver authority and revocation), and Ch 22 (approval does not make a write retry-safe).

The chapter currently delivers the authorization part fully. Intervention, operator control, and the Ch 10–13 and Ch 22 relationships are thin or missing.

## Section-by-Section Flow Review

**Opening callouts (`:854–862`).** The evidence context cites WCAG 2.2 and automation bias [R41]. The case box is precise and on-thread. The design choice is clear. *Issue:* the chapter body never mentions accessibility or automation bias again, so the evidence context promises something the chapter does not deliver (see C14-R07).

**§ Why human review must change system state (`:864`).** Role: the thesis ("theater" when a click is detached from its effect). It adds the framing. Flow: good. The state-owner table (`:872–874`) is the usual unexplained template. Its "authorization queue" scale unit omits the intervention queue.

**§ Separate authorization from intervention (`:876`).** Role: the chapter's key distinction. Issues:
- (a) Paragraph `:878` and paragraph `:882` define the same pair twice, back to back, around Figure 14-1.
- (b) Paragraph `:884` enumerates the Human Action Authorization Service's stored fields and commit-time rechecks. § Approval contract (`:902`) and § Records worth preserving (`:944`) re-list them.
- (c) Figure 14-1's intervention column is operator-initiated, while the prose says system-requested.
- (d) Paragraph `:886` (human capacity) is unique and valuable, but it is restated in § What changes as usage grows (`:969`).

Verdict: right section, but overwritten and internally inconsistent with its own figure.

**§ Design human review as part of the system (`:888`).** Role: the Required-analysis table plus two H3s. It adds the gate triggers (risk, novelty, confidence, value, sensitivity, reversibility, destination), the design alternatives, and the failure scenarios. Flow: the table is useful, and its enterprise example stays on the Harborlight thread. *Issue:* the heading promises "the system" but the content is an analysis table, a contract, and a console list. "Failure scenarios" lists "approval applies to a changed plan", yet the chapter never says whether a human approves plans (Ch 12 `:544` says plans can be "inspected and approved") or effects (see C14-R05). [verified: corrected — the quote is in the ARCHITECTURE GUIDANCE box at `:544`, not `:536`]

**### Approval contract (`:900`).** Role: the canonical field list for the authorization request. It adds allowed responses (authorize, reject, edit-and-resubmit, request-evidence, cancel-run), the reversible flag, and the separation-of-duties requirement. Flow: this is the right single home for the field list. *Issue:* it is the second of four lists, and none of the four agree.

**### Operator console requirements (`:904`).** Role: the operator surface. It adds pause, cancel, safe retry, plan patch, budget, compensation, replay, conflict detection, and override journaling. *Issues:*
- It introduces an operator role that § Separate authorization from intervention never names.
- Its forward references (live run graph → Ch 24, compensation → Ch 22, sandbox replay → Ch 24) are unsignposted.
- The last bullet ("a timed-out approval follows explicit policy, never implicit approval", `:911`) is an approval rule, not a console requirement. It is the first of four statements of the same rule (`:911`, `:949`, `:1090`, `:1106`).

**§ A workable implementation (`:913`).** A wrapper H2. Its intro sentence is missing.

**### Who should own each decision (`:915`).** Role: the components. Seven rows. It distinguishes Notification ("never owns the decision"), which is good. Flow: fine.

**### The contracts between components (`:927`).** Role: the approval API. The approval endpoints are coherent. *Issue:* `POST /v1/runs/{run_id}:operatorAction` (`:938`) collides with Ch 04's `:update`/`:cancel`/`:fork` (`02-part-ii.md:166–169`) and Ch 15's `:pause`/`:resume`/`:cancel` (`:1214–1216`). It also duplicates `:cancel`. The record names (HumanActionAuthorization*) disagree with the API names (`/v1/approvals`) (§6 T3).

**### Records worth preserving (`:940`).** Role: entities. It adds ApprovalEvidenceSnapshot, ApprovalAssignment, OperatorAction, EscalationPolicy, and NotificationDelivery. The validity sentence at `:952` is the clearest statement of the binding rule in the book. *Issues:* this is the third field list for the request. There is no entity for intervention.

**### Workflow integration (`:954`).** Role: the six-step approval wait-and-resume sequence. It adds the concrete sequence. Flow: good, and it is the concrete instance that Ch 15 generalizes. *Issue:* it uses durable timers, wait correlation IDs, and a suspended workflow without a worker before Ch 15 defines them (the outbox event it also names is already defined in Ch 04 § CloudEvents and outbox contracts, `02-part-ii.md:258–292`). That is acceptable because the next chapter does define them, but a one-clause pointer is missing. [verified: corrected — "outbox events" removed from the list of terms Ch 15 defines first; Ch 04 defines `OutboxRecord`]

**### What changes as usage grows (`:963`).** Role: scaling. The unique bullets are approval capacity in end-to-end planning (`:969`), stampede prevention (`:970`), authorization computed at claim/decision time (`:967`), and digest batching that keeps one decision per effect (`:968`). The generic bullets repeat every Part IV implementation block: partition by tenant (`:965`), durable timers (`:966`), regional replication and fencing (`:971`), cache by hash (`:972`). The regional bullet duplicates Ch 15 `:1247` and Ch 27 `08-part-viii.md:166`.

**PRODUCTION CONSIDERATION (`:974–976`).** "Design the wait, not just the prompt". This is a good bridge to Ch 15, but it restates the design choice and the expiry rule a third time.

**§ What the evidence lets us conclude (`:978`).** One claim, cited to R15 (OWASP Top 10 for Agentic Applications). R15's registry `supports` is "major agentic-application security risks and mitigations". Exact-proposal hashing and "Never transport serialized run state inside exception text" read as book-authored recommendations. The last clause is also unrelated to anything the chapter teaches. R41 is listed in the footer but supports no claim in the table.

**§ How Human-in-the-Loop works in practice (`:986`) with ### How the pattern works (`:992`), ### Where it helps—and what it costs (`:1006`), ### Where it can fail—and how to contain it (`:1013`), and ### What you need to see in production (`:1021`).** The template card. It re-summarizes the chapter (a fourth statement of hash binding and recheck). Its only new item is the "Do not use when" cell. "InterventionTask" (`:994`) appears here for the first and only time. Verdict: acceptable as a scannable card, but it exposes the intervention gap.

**§ A sensible place to start (`:1030`).** An empty H2 followed directly by `[[EXAMPLE:approval-gate]]` with no introductory sentence.

**### Proposal-bound approval contract (`:1035`).** Inline Python. It defines a *fourth* `HumanActionAuthorizationRequest` shape: approval_id, destination, canonical_arguments, evidence_ids, proposal_sha256. That shape differs from `approval_verification.py` (tenant_id, actor_id, tool_version, logical_effect_key, policy_digest). It also defines a second `proposal_hash` function with inputs that differ from `approval_gate.py`'s. It puts `approval_id` inside the request, which mixes request and decision. It also breaks `AGENTS.md` ("never write code directly into `source/parts/`"). Verdict: remove.

**### Executable proposal-bound approval (`:1076`).** The `approval-verification#core` example: decision model, fail-closed verification, no self-approval. Flow: good, and it is the right "verify at commit" companion to the gate example. The heading does not tell the reader how it differs from the gate example.

**§ If this fails in production (`:1080`).** Three diagnostic steps: recompute the hash, verify authority, trace to the receipt. These are runtime diagnostics. AP-06 is the structural diagnosis. The two are complementary; there is no pointer between them.

**§ What to verify before production (`:1086`).** Four items. Missing: reviewer capacity and fatigue (the chapter's own "production metrics", `:886`), accessibility (the evidence context), and plan versus effect approval.

**§ Put the idea to work (`:1096`).** Exercise 1 asks the reader to design the object the chapter already gives in full. Exercise 2 is good. There is no intervention exercise.

**§ Questions to bring to design review (`:1101`).** Three rows, against five in the neighboring chapters. Row 3 (`:1107`) is word-for-word identical to Ch 22 (`06-part-vi.md:1014`). Nothing covers intervention or operator overrides.

**§ Where this leads next (`:1109`).** "Human control introduces waits and resumptions; Chapter 15 makes those waits durable…" Strong and accurate.

## Sparse or Underdeveloped Content

1. **The intervention contract** (`:876–886`, `:994`). Missing: the triggers, what the person sees, the allowed responses, how the run resumes, and the terminal semantics. This is the half of the chapter's thesis with no mechanism. It needs one H3 of roughly 6–8 lines, not a new section tree (C14-R02).
2. **Operator control as a named third role** (`:904–911`, `:924–925`). The material exists. Only the framing sentence and the figure alignment are missing (C14-R03).
3. **Plan approval versus effect authorization.** Ch 12 lets humans approve plans, Ch 18 (`05-part-v.md:82`) requires "new consent or approval" for broader scope, and Ch 14 authorizes "one proposed effect". One or two sentences are needed (C14-R05).
4. **Accessibility and automation bias.** These are promised by the evidence context and never treated. One console bullet and one metric are needed (C14-R07).

Nothing else needs expansion. The implementation block should shrink.

## Missing Conceptual Connections

- **Ch 10/11/12/13 escalations → (missing: "these land in the intervention queue as typed InterventionTasks") → Ch 14 intervention.** Location: § Separate authorization from intervention (`:882`) and the new § Intervention contract.
- **Ch 15 `InterventionRequired` terminal (`:1152`) and Ch 22 unknown effects → (missing: "an operational terminal that opens an intervention task") → Ch 14.** Ch 14 precedes Ch 15, so the link must be a forward clause in Ch 14 and a back-reference in Ch 15 § Terminal correctness (owned by Ch 15, see C15-R04).
- **Ch 03 SDK interruption (`01-part-i.md:1135–1148`) → (missing: "Chapter 3 showed that an SDK pause is not an approval; this chapter defines the approval record") → Ch 14 § Approval contract.** Location: `:884` once it is condensed.
- **Ch 14 approval → (missing: "approval proves authority over the proposal, not that the write happens once or against fresh state; idempotency and expected versions do that (Chapter 22)") → Ch 22 property table (`06-part-vi.md:683–688`).** Location: the end of § Approval contract or the validity sentence at `:952`.
- **Ch 12 plan approval → (missing: plan approval authorizes scope; each protected effect still needs its own proposal-bound authorization unless its canonical proposal was fully fixed in the approved plan) → Ch 14.** Location: § Approval contract.
- **Ch 14 § Workflow integration → (missing: "Chapter 15 generalizes this wait to every signal and timer") → Ch 15 § Event-driven resume flow.** Location: the end of `:961`.
- **Ch 14 § If this fails → (missing: "if approval is a Boolean or chat reply, the structural repair is AP-06") → Ch 17.** Location: after `:1084`.

## Transition Problems

- **In (Ch 13 → 14, `:850`).** Good. "Recourse" in Ch 13's closing sentence is never developed in Ch 14 (no appeal or contest path). Either drop the word (owner: Ch 13 reviewer) or accept it as loose usage. Ch 14 should not add a recourse section.
- **Within.** `:878` → Figure 14-1 → `:882` loops: definition, figure, definition. § Design human review as part of the system moves from analysis to contract to console with no connecting sentence. § A sensible place to start opens on a bare example marker.
- **Out (Ch 14 → 15, `:1111`).** Strong. Keep it.

## Redundant and Repetitive Concepts

| Concept | Occurrences in Ch 14 | Verdict |
| --- | --- | --- |
| Authorization vs intervention definition | `:878`, `:882`, checklist `:1088`, Q `:1105` | `:882` is redundant with `:878`. The checklist and Q are template reinforcement (keep). |
| Authorization request field list | `:884`, `:902`, `:944`, code `:1048` | Redundant. Keep `:902` (contract) and `:944` (record fields), cut `:884` to one sentence, and remove the code. |
| Commit-time recheck list | `:884`, `:952`, `:960`, `:1000`, `:1017`, `:1107` | `:952` is canonical. `:884` is redundant. The others are template recall. |
| Timeout ≠ implicit approval | `:911`, `:949`, box `:976`, `:1090`, `:1106` | Keep `:949`, the checklist, and the Q. Remove `:911` and trim the box. |
| Reviewer capacity and fatigue | `:886`, `:969`, `:1010` | `:969` restates `:886`. Merge the metrics list into `:886`, and keep `:969`'s "approval capacity is part of end-to-end capacity planning". |
| Proposal hashing code | `approval-gate`, inline `:1039–1074`, `approval-verification#core` | The inline excerpt is redundant and divergent. |

## Cross-Chapter Duplication

| Other location | What repeats | Verdict |
| --- | --- | --- |
| Ch 01 § Each control point answers a different question, human approval gate paragraph (`01-part-i.md:542–546`) | Gate presents the exact proposal and binding expires; gateway still reauthorizes | Reinforcement (short preview). Keep. |
| Ch 03 § Human approval: interruption versus record (`01-part-i.md:1133–1148`) | Full request field list (`:1137`) and verification list | **Redundant pre-teaching.** The 4-row interruption / approval / reauthorization / receipt table (`:1141–1146`) is a framework-boundary point unique to Ch 03 and should stay there. The field list belongs to Ch 14. Owner: Ch 03. |
| Ch 03 § Bind approval to the exact proposal (`01-part-i.md:1150–1154`) | Proposal hash, pre-commit equality, expiry, version | **Redundant.** Condense to two sentences that keep the `MORT-2026-000999` example and add a pointer to Ch 14. Owner: Ch 03. Agrees with map §9 S5. |
| Ch 22 property table (`06-part-vi.md:683–688`) and `:673` | Approval ≠ idempotency ≠ preconditions ≠ receipt | Reinforcement (a new facet). Keep in Ch 22, and add a one-clause forward pointer in Ch 14 (C14-R06). |
| Ch 22 § Questions to bring to design review row 4 (`06-part-vi.md:1014`) | Word-for-word identical to Ch 14 `:1107` | **Redundant.** Ch 14 keeps the row (canonical). Ch 22 deletes its row; its row 5 already covers the effect-side reasoning. Owner: Ch 22. |
| AP-06 (`04-part-iv.md:1774–1807`) and Figure 17-4 | Boolean vs proposal-bound approval, with code | Reinforcement (anti-pattern framing, symptom metrics). Keep. Its code issues are in chapter-17.md. |
| Ch 15 § Scalability and multi-region behavior (`:1247`), Ch 27 § Rollback and active runs (`08-part-viii.md:166`) | Fence the prior writer after failover | Redundant in Ch 14 `:971`. Regional recovery belongs to Ch 27. |
| Appendix B row "Run stuck after approval" (`09-appendices.md:45`) | Hash, expiry, version, signal | Reinforcement (desk aid). |
| Ch 04 Run API (`02-part-ii.md:159–170`), Ch 15 Run API (`:1208–1218`) | `:operatorAction` overlaps `:cancel`/`:update`/`:fork`/`:pause`/`:resume` | Redundant API (C14-R09). |

## Structural Recommendations

1. Restructure § Separate authorization from intervention into a **three-role model**: authorization, intervention (system-raised), and operator control (human-initiated). Use one definition paragraph and drop the duplicate (C14-R01, C14-R03).
2. Add **### Intervention contract** after ### Approval contract (C14-R02). Do not add intervention APIs or records beyond one entity row and one queue note. The point is the semantics, not a second implementation block.
3. Make § Approval contract the single field-list home, and let § Records hold the stored invariants. Remove the inline code (C14-R04, C14-R10).
4. Trim § What changes as usage grows to the approval-specific bullets (C14-R08).
5. Do **not** swap Ch 14 and Ch 15. I considered it, because Ch 14 uses durable-wait mechanics before Ch 15 defines them. But the concrete-then-general order works, the outbound bridge is strong, and a swap would renumber two chapters, two figures, covers, and every "Chapter 14/15" reference (e.g. `01-part-i.md:1107`, `:1201`, `:445`) for a modest gain. A forward clause solves it (C14-R11).

## Concrete Recommended Changes

1. **C14-R01 · High · Rewrite/Condense.**
   - **Location:** `04-part-iv.md:876–886`, § Separate authorization from intervention.
   - **Issue:** Paragraphs `:878` and `:882` define the same pair twice. `:884` duplicates § Approval contract.
   - **Why it matters:** The reader meets the key distinction three times before learning anything new, and the field list hides the distinction.
   - **Change:**
     - Keep `:878`, extended with the three-role framing from C14-R03.
     - Delete `:882`, but move its "separate queues, roles, forms, SLOs, and terminal semantics" clause into `:878` and drop "Northstar" per §6 T1.
     - Replace `:884` with two sentences. First: authorization stores an immutable canonical proposal and becomes invalid when any protected field changes, and the commit path rechecks it (§ Approval contract and § Records worth preserving give the fields). Second: Chapter 3 showed that an SDK pause is only an interruption, and this record is what turns it into an approval.
     - Move the metrics list from `:969` into `:886`.
   - **Related:** Ch 03 (owner of the Ch 03 trim), C14-R03.

2. **C14-R02 · High · Add.**
   - **Location:** a new `### Intervention contract` after `### Approval contract` (`:902`).
   - **Issue:** Intervention has no contract. `InterventionTask` (`:994`) is an orphan. The Ch 10–13 escalations have no destination.
   - **Why it matters:** This is the chapter's distinctive concept and the convergence point of every Part IV "escalate". Without it the reader cannot see how the bounded patterns hand off to people.
   - **Change:** One paragraph of 6–8 lines covering:
     - **Triggers:** Ch 10 no-progress or budget exhaustion, Ch 11 below-threshold routing to human triage, Ch 12 plan compile or revision failure, Ch 13 repeated generator/evaluator disagreement, and Ch 15/22 `InterventionRequired` or an unresolvable unknown effect.
     - **What the reviewer sees:** the uncertainty, the competing artifacts or alternatives, the current state version, and what is blocked.
     - **Allowed responses:**
       - supply information (a typed signal to the workflow)
       - choose an alternative (becomes a plan revision under Ch 12's revision rules)
       - correct state (a governed update with expected version)
       - reassign
       - cancel
       - declare an operational resolution with reason
     - **Invariant:** an intervention response is an *input* to the run; it never authorizes an effect. Any protected effect it leads to still needs a proposal-bound authorization.
   - Add one Records row `InterventionTask` (run/node, trigger and source chapter's reason code, evidence refs, alternatives, allowed responses, assignee, SLA, state/version, response; append-only). Add one checklist item and one design-review row (see C14-R12).
   - Do not add a second API table. State that intervention responses use the run's signal and update endpoints (Ch 04).
   - **Related:** Ch 10 `:45`, Ch 11 `:199`, Ch 12 `:468`, Ch 13 `:678`, Ch 15 `:1152` (C15-R04 adds the back-reference). [verified: corrected — line numbers]

3. **C14-R03 · High · Rewrite (prose and figure).**
   - **Location:** `:878`; Figure 14-1 (`assets/diagrams/src/pattern-hitl.gv:21–24`); § Operator console requirements (`:904`).
   - **Issue:** The prose defines intervention as system-requested judgment, the figure as operator-initiated control, and the console introduces operators without naming them.
   - **Why it matters:** The reader's model of "who are the humans and what may each change" stays contradictory.
   - **Change:**
     - In `:878`, name three controls: authorization (before an effect, one exact proposal), intervention (the system asks for judgment), and operator control (a human acts on a run in flight through governed commands).
     - State that intervention and operator control both change a running run and neither authorizes an effect.
     - Edit Figure 14-1's lower column so its trigger reads "Run raises InterventionRequired / escalation, or operator acts on a run in flight", and keep "Workflow signal, not a message" and "Recorded as an operational event". Update the caption to match: "Approval and intervention: different triggers, different authority, different evidence" can stay. Run `make diagrams`.
     - Add one lead sentence to § Operator console requirements: "Operator control is the third human role…".
   - **Related:** C14-R02.

4. **C14-R04 · Medium · Condense.**
   - **Location:** `### Approval contract` (`:902`) and `### Records worth preserving` (`:944`).
   - **Issue:** There are two request field lists in prose and table, and both differ from the examples.
   - **Change:** **Reconciled (see overall-book-review.md §D-22):** As stated, with the T3 choice made: the human decision is an **approval**. Rename HumanActionAuthorizationRequest/Decision to ApprovalRequest/ApprovalDecision and the Human Action Authorization Service to Approval Service, matching `/v1/approvals`; update `examples/patterns/approval_gate.py`, `approval_verification.py`, and their tests in the same PR. Reserve "authorization" for policy decisions (Chapter 21). Ch 14's three roles become approval, intervention, and operator control, and C14-R01, R02, R03, and R05 use that wording. If the author declines the record rename (Phase 0), keep the record names and still use "approval" in prose.
     - Keep `:902` as the conceptual contract: what the approver sees and the allowed responses.
     - In the `:944` row, keep only the stored fields that `:902` does not name (IDs, state/version, approver predicate/count) and add "plus the contract fields above".
     - Align field names with `examples/patterns/approval_verification.py` (`logical_effect_key`, `policy_digest`, `expected_resource_version`) so the prose and the runnable example agree.
   - Apply whichever approval/authorization naming pair the synthesizer picks for §6 T3 to `:874`, `:900`, `:902`, `:919–920`, `:931–937`, `:944–947`. Today `/v1/approvals` serves `HumanActionAuthorization*` records.

5. **C14-R05 · Medium · Add (2 sentences).**
   - **Location:** the end of `### Approval contract` (`:902`).
   - **Issue:** The chapter never says whether humans approve plans or effects, though Ch 12 `:536` and Ch 18 `05-part-v.md:82` mention plan approval and `:897` lists "approval applies to a changed plan".
   - **Change:** "Approving a plan (Chapter 12) authorizes its scope, not its effects. Each protected effect still receives its own proposal-bound authorization, unless the approved plan already fixed that effect's canonical proposal and the plan revision is unchanged at commit."
   - **Related:** Ch 12 (no change needed there).

6. **C14-R06 · Medium · Cross-reference.**
   - **Location:** after the validity sentence (`:952`).
   - **Issue:** There is no link to Ch 22's point that approval does not make a write safe.
   - **Change:** Add one sentence: "A valid authorization proves authority over this proposal; it does not stop a duplicate or a stale overwrite. Chapter 22 pairs it with idempotency, expected versions, and receipts."
   - **Related:** Ch 22 property table (`06-part-vi.md:683`).

7. **C14-R07 · Medium · Add (1 bullet and 1 metric).**
   - **Location:** `### Operator console requirements` (`:904–911`) and § What to verify before production (`:1086`).
   - **Issue:** The evidence context (WCAG 2.2, automation bias) is never connected to the body.
   - **Change:**
     - Add a console bullet: "Review and intervention forms are tested against WCAG 2.2 [R41]. Conformance does not remove automation bias, so measure it: reviewer agreement on seeded cases and override rate."
     - Add a checklist item: "Reviewer queue age, dwell, abandonment, and agreement are monitored as SLOs."

8. **C14-R08 · Medium · Condense.**
   - **Location:** `### What changes as usage grows` (`:963–972`).
   - **Issue:** Generic scaling bullets repeat across all Part IV implementation blocks. The regional bullet duplicates Ch 15 and Ch 27.
   - **Change:**
     - Keep `:967`, `:968`, `:969` (minus the metrics, which move to `:886`), and `:970`.
     - Merge `:965` and `:966` into one bullet: "Serialize decisions per approval, scale across approvals, and drive SLA timers from durable timers (Chapter 15), never table scans."
     - Replace `:971` with "Decisions are written only in the run's home region (Chapter 27 covers failover fencing)."
     - Delete `:972`.

9. **C14-R09 · Medium · Remove/Rewrite.**
   - **Location:** `### The contracts between components`, row `POST /v1/runs/{run_id}:operatorAction` (`:938`); `### Who should own each decision`, Operator Control Service row (`:924`).
   - **Issue:** The endpoint overlaps Ch 04 `:cancel`/`:update`/`:fork` and Ch 15 `:pause`/`:resume`.
   - **Change:** Delete the row. Change `:924` to "Invoke the run lifecycle commands (Chapters 4 and 15) and effect reconciliation/compensation (Chapter 22) on an operator's behalf, recording an OperatorAction for each." Keep the `OperatorAction` record.
   - **Related:** C15-R08 (Run API ownership).

10. **C14-R10 · High · Remove.**
    - **Location:** `### Proposal-bound approval contract` (`:1035–1074`).
    - **Issue:** The inline code is a fourth, divergent `HumanActionAuthorizationRequest` with a second `proposal_hash`, and it breaks the `AGENTS.md` rule against inline code.
    - **Change:**
      - Delete the H3 and its code block.
      - Under § A sensible place to start, add one sentence before `[[EXAMPLE:approval-gate]]`: "The first example persists the wait and verifies a signed, expiring decision; the second is the commit-time check that the decision still covers this exact proposal and current state."
      - Retitle `### Executable proposal-bound approval` (`:1076`) to `### Verify the decision at commit`.
    - **Related:** `config/examples.json` (no change needed).

11. **C14-R11 · Low · Cross-reference.**
    - **Location:** `### Workflow integration`, step 6 (`:961`).
    - **Change:** Append "Chapter 15 generalizes this wait to every timer, signal, and callback."

12. **C14-R12 · Medium · Rewrite.**
    - **Location:** § Questions to bring to design review (`:1101–1107`) and § Put the idea to work (`:1096–1099`).
    - **Issue:** There are only three rows, and none covers intervention or operator control. Exercise 1 repeats the chapter's own artifact.
    - **Change:** Keep the three rows. Ch 14 is canonical for `:1107`, and Ch 22 deletes its copy. Add:
      - "What may an intervention change, and what may it never do?" — Strong answer: "Supply information, choose an alternative as a plan revision, or correct state with an expected version; it never authorizes a protected effect."
      - "How do operator overrides stay accountable?" — Strong answer: "Governed lifecycle commands with expected state, operator identity, reason, and linked ticket in an append-only journal."
      - Replace exercise 1 with "For the Harborlight document-request proposal, list which field changes force supersession and which do not."
      - Add exercise 3: "Design the intervention task raised when Chapter 13's generator and evaluator disagree twice."

13. **C14-R13 · Low · Rewrite.**
    - **Location:** § What the evidence lets us conclude (`:980–984`).
    - **Issue:** The claim is attributed to R15 beyond R15's recorded scope. The last clause ("Never transport serialized run state…") is unrelated to the chapter.
    - **Change:**
      - Label the hashing and recheck guidance as a book-authored recommendation informed by R15's mitigation guidance, or narrow the cell to what R15 supports.
      - Delete the exception-text clause.
      - Add a row for R41 that matches the evidence context.
    - **Related:** `config/references.json` (verify R15 scope; do not broaden it).

14. **C14-R14 · Low · Cross-reference.**
    - **Location:** § If this fails in production (`:1080–1084`).
    - **Change:** Add a fourth line: "If approval is a Boolean or a chat reply rather than a bound record, the repair is structural; see AP-06 in Chapter 17."
    - **Related:** chapter-17.md C17-R03 (forward tags).

15. **C14-R15 · Low · Rewrite (terminology).**
    - **Location:** `:882` ("Northstar"), `:898` ("missing employment evidence").
    - **Change:** Apply the synthesizer's §6 T1 (Northstar) and T15 (missing-document) decisions. If "second pay statement" is chosen, `:898` reads "a request to obtain the missing second pay statement".

16. **C14-R16 — Low — Rewrite (card policy).** *Added in reconciliation (see overall-book-review.md §D-04).*
   - **Location:** `04-part-iv.md:986–1025`, § How Human-in-the-Loop works in practice.
   - **Issue:** The card policy (C10-R04) had no Ch 14 reciprocal, and the card restates hash binding a fourth time.
   - **Change:** Retitle the H2 "Approval and intervention at a glance". Delete THE ENGINEERING PROBLEM box and the lead sentence. Replace the hash-binding steps with a pointer to § Approval contract, and name InterventionTask as defined in § Intervention contract (C14-R02). Keep the Use when, costs, failure, and signals blocks. Place it before § What the evidence lets us conclude.
   - **Related:** C10-R04, C14-R02, C14-R04.

## Verification log

Second-pass fact check against `source/parts/*.md`, `examples/patterns/*.py`, `assets/diagrams/src/pattern-hitl.gv`, `config/references.json`, and the Ch 22 / Appendix B passages cited.

- **Line references checked / fixed:** 71 checked; 6 fixed (Ch 11 `:191`→`:193`/`:199`, Ch 12 `:460`→`:468` and `:536`→`:544` in two places, Ch 13 `:670`→`:678` in two places). Ch 04 `:166–169` for `:cancel`/`:update`/`:fork` is actually `:167–169` (within tolerance; left).
- **Claims removed:** none.
- **Claims softened:**
  - § Workflow integration "uses … outbox events before Ch 15 defines them": the outbox is defined in Ch 04 (`02-part-ii.md:258–292`, `OutboxRecord`); only timers, correlation IDs, and the worker-less wait are Ch 15's.
- **Important claims confirmed:**
  - The design-review row at `:1107` is byte-identical to Ch 22 `06-part-vi.md:1014` (question and answer); diffed directly.
  - Four distinct request field sets at `:884`, `:902`, `:944`, and the inline code `:1048–1057`; no two agree. The inline `proposal_hash` (action, destination, arguments, evidence_ids, expected_version) differs from `approval_gate.py:25` (`proposal_hash(action, arguments)`), and `approval_verification.py:23–33` uses tenant_id / actor_id / tool_version / logical_effect_key / policy_digest, none of which the inline model has.
  - `InterventionTask` occurs exactly once in the book (`04-part-iv.md:994`); `InterventionRequired` never appears in Parts I–III.
  - Figure 14-1 source `pattern-hitl.gv:21–24` reads "Operator observes a run in flight → Pause · cancel · redirect · adjust budget"; the file's header comment also defines intervention as "changes a run already in flight", so the prose/figure split (system-requested vs operator-initiated) is real.
  - R15 `supports` = "Prioritizes major agentic-application security risks and mitigations"; R41 = WCAG success criteria. The evidence table at `:982` cites only R15; the footer at `:984` lists R15 and R41, so R41 supports no table row.
  - Ch 03 `01-part-i.md:1137` gives the full `HumanActionAuthorizationRequest` field list and `:1154` the hash/expiry/version recheck; the interruption/approval/reauthorization/receipt table is at `:1141–1146`.
  - Ch 14 has 3 design-review rows; Ch 13 (`:836–846`) and Ch 15 (`:1346–1350`) have 5 each.
  - `:1030` is an empty H2 followed by the example marker at `:1033`; `:913` is a wrapper H2 with no intro sentence.
  - `:operatorAction` (`:938`) overlaps Ch 04 `:cancel`/`:update`/`:fork` (`02-part-ii.md:167–169`) and Ch 15 `:cancel`/`:pause`/`:resume` (`:1214–1216`).
  - Appendix B "Run stuck after approval" is at `09-appendices.md:45`; Ch 22 property table at `06-part-vi.md:683–688`; Ch 22 `:673` "Approval proves a person authorized the proposal; it does not prove the write happened once."
- **Recommendations amended:** C14-R02 Related line numbers only. All recommendations remain consistent with overall-book-review.md §12 (D-03 removes `:operatorAction` = C14-R09; D-22 approval naming = C14-R04; D-23 inline code = C14-R10; D-30(f) sensible-place lead = C14-R10).
- **Not verified:** the concept-map section/row references (§6 T1, T3, T15; §9 S5; map §3) were taken as given; the "five pre-teachings" style map counts were not re-counted here.
