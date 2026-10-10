# Chapter 18 — Coordinate Specialists Without Losing Control: Continuity and Flow Review

Reviewed: `source/parts/05-part-v.md:1–384` (Part V orientation and Chapter 18). For transitions I also read Ch 17 § AP-11, § AP-08, and § Where this leads next (`04-part-iv.md:1560–1873`) and the opening of Ch 19 (`05-part-v.md:386–446`). For duplication I checked Ch 03 § Three meanings of handoff, Ch 11 (whole), Ch 12 § The contracts between components, Ch 15 § Terminal correctness, Ch 16 P-06, Ch 21 § Capability-envelope subset proof, Ch 06 § Cross-boundary artifact adoption policy, Appendix A/C, and `assets/diagrams/src/supervisor-worker.gv`.

## Overall Assessment

The chapter has the right thesis: multi-agent collaboration is durable task ownership, not conversation. Its best material is unique to it: the topology decision table, the explicit fan-in contract (all / quorum / first-valid / fallback), durable cancellation that reconciles an executing mutation first, the Task Service APIs, and the hot-run scale notes. Five structural problems weaken it:

1. **It promises a state machine and never shows one.** The chapter says it "makes collaboration a durable state machine" (`:25`), but no task states appear anywhere in Ch 18. The canonical local task states sit in Ch 19 § State mapping and ownership (`:531–539`).
2. **TaskEnvelope has four shapes in one chapter.** There is the Delegation rule (`:77`), the JSON child-task request (`:115–127`), the `Task` record (`:135`), and the `TaskEnvelope` code (`:261–274`). Field names drift between them (`authority_ceiling` vs `capability_grant_id`, `acceptance` vs `acceptance_contract`, `receiver` vs `owner_agent`, `budget.usd` vs `maximum_cost_usd`). The fullest field specification is in Ch 19 (`:473–484`), not here.
3. **The capability-envelope proof is duplicated.** § Monotonic child authority (`:280–347`) is byte-identical to Ch 21 § Capability-envelope subset proof (`06-part-vi.md:528–595`), which I verified with `diff`. It also arrives before the reader has been told what a capability envelope is.
4. **The two "How X works in practice" cards nearly coincide.** The Multi-Agent Collaboration card's distinct content (peers, message reordering, remote tasks that never complete) is Ch 19's subject, and Ch 19 already covers it.
5. **Handoff and plan revision are re-specified with drift.** Handoff is defined against Ch 11, and plan revision against Ch 12 (a different endpoint and a different owner).

The section-level redundancy is also high. "Add a specialist only when boundaries differ" is stated seven times (`:27`, `:32`, `:56`, `:157`, `:179`, `:357`, `:376`).

## Intended Reader Mental Model

On leaving the chapter the reader should hold this model. A multi-agent system is a **task tree**, not a conversation:

- Each node is a durable task with exactly one current owner, a TaskEnvelope, and a capability envelope that is a provable subset of its parent's.
- Each node moves through a deterministic lifecycle.
- A parent joins children only through an explicit fan-in contract and adopts their artifacts only after validation.
- Cancellation is durable intent that propagates down the tree. A child with a running mutation reconciles before it acknowledges.
- Topology is chosen by the smallest structure that fits: single agent, workflow, router, manager-as-tools, handoff, fan-out, and only experimentally a swarm.

The reader arrives having seen AP-08 (chat as workflow) and AP-11 (budgets reset per hop) in Ch 17, and handoff semantics in Ch 03 and Ch 11. The chapter should build on those, not re-derive them.

## Section-by-Section Flow Review

**Part V orientation (`:1–7`).** It frames Part V as "the conversation becomes a distributed protocol" and puts "a protocol can move a message without granting permission to act" in view. That is tight and accurate for Ch 18 and Ch 19's MCP/A2A material. It does not mention the LLM Gateway, which supports moving that material out of Ch 19 (C19-R01). There is no bridge from Part IV. That is acceptable, because Ch 17's closing sentence does the job. **No change.**

**Opening callouts (`:11–19`).** The evidence context cites R28 and R33. The case box names the four specialists (document extraction, income verification, property review, policy). The design choice is crisp. **Good.** The case box and `:43` agree on the specialists, but Figure 18-1 does not (see `:41`).

**§ Why more agents do not automatically make a better system (`:21–28`).** *Role:* the motivation. *Adds:* three unanswered questions (who owns, who cancels, which result wins). That is a good hook. *Issue:*
- `:25–28` restates the design-choice box ("one owner per task, narrowed child authority, explicit joins").
- The section does not acknowledge that AP-08 and AP-11 (read one chapter earlier) already named the failure. The reader meets "conversation is not coordination" for the third time without being told this chapter is the *replacement design*.

*Verdict:* keep the hook and replace the restatement with the Ch 17 bridge (C18-R07).

**§ What every collaboration must make explicit (`:30–37`).** *Role:* the cost argument plus the state-owner table. *Adds:* "every additional agent introduces another scheduler, context boundary, identity, budget, and failure mode". This is the chapter's best statement of the justification rule. *Verdict:* make this the canonical statement of "when another agent is justified" and cut the others (C18-R06). The state-owner row's "Core contracts" (TaskEnvelope · CapabilityEnvelope · JoinPolicy) matches the body. **Good.**

**§ Treat collaboration as durable work, not conversation (`:39–47`).** *Role:* the core mechanism, with Figure 18-1. *Adds:* durable child tasks with scoped inputs; fan-in strategies; conflict-resolution rules; tree-wide caps; cancellation as durable intent with mutation reconciliation. *Issues:*
- Figure 18-1's child tasks are labeled "screening", "tax", and "security" (`supervisor-worker.gv`). These are supplier-onboarding labels, not the Harborlight specialists named in `:43` (C18-R09).
- `:47` "Northstar caps depth, children, …" restates AP-11's correction without pointing to it (C18-R14).
- "a child with an executing mutation must reconcile" needs a forward pointer to Ch 22's unknown-outcome reconciliation.

*Verdict:* strong. Needs the figure fix and two pointers.

**§ Choose a topology—and define how the work ends (`:49–59`).** *Role:* an H2 wrapper holding a seven-row Required-analysis table. *Issues:*
- Every row restates content nearby. Problem and Why it is difficult restate `:32`. Design alternatives are the first column of the topology table. Recommended architecture restates `:32` and the topology table. Enterprise example restates `:43`.
- Only the Trade-offs row (central vs decentralized) and the Failure scenarios row (ping-pong handoffs, orphaned tasks, two agents mutating one record, circular delegation, premature "done", incompatible artifacts) add anything.
- The heading promises "define how the work ends", but the only termination content is one bullet at `:81`.

*Verdict:* remove the table and keep its two useful rows elsewhere (C18-R06). Add the task lifecycle here so the heading's promise is kept (C18-R03).

**### Topology decision table (`:61–72`).** *Role:* selection aid. *Adds:* eight topologies with use/avoid/control model. It is unique, and it is the canonical topology aid (Ch 16's decision tree and Appendix A select patterns, not topologies). Rows 1–2 reinforce Ch 01's four levels. That is acceptable. *Issue:* the "Router + specialists" and "Handoff" rows re-teach Ch 11 without a pointer, and the "Handoff" control model ("Ownership token transfers explicitly") omits Ch 11's acknowledgment rule. *Verdict:* keep, and add a one-line Ch 11 pointer (C18-R05).

**### Recommended orchestration rules (`:74–82`).** *Role:* normative rules. *Issues:*
- **Creation** uses "AgentManifest". That name is undefined; the book's term is AgentSpec (map T8).
- **Delegation** is a third field list for the child task.
- **Handoff** says "atomically transfer … and issue a new capability envelope" but omits Ch 11's acknowledge/reject step and "the previous owner remains accountable until acknowledgment" (`04-part-iv.md:195`, `:273`). That is drift.
- **Termination** lists causes but no states.
- **Plan changes** re-specifies Ch 12 § Runtime revision.
- **Coordination** and **Shared state** are good and unique in this form.

*Verdict:* keep Coordination and Shared state. Point Handoff to Ch 11 and Plan changes to Ch 12. Replace Termination with the lifecycle (C18-R03, R05, R08).

**## A workable implementation (`:84`) → ### Who should own each decision (`:86–95`).** *Adds:* six components in a clear table. *Issues:*
- The **Run Coordinator** "owns … plan revision". Ch 12 assigns plan revisions to the Plan Service / Plan Store (`04-part-iv.md:482`). That is two owners for one record.
- The **Router** re-describes Ch 11's route service without a pointer.
- The **Agent Registry** overlaps Ch 19's Agent Directory with no relationship stated (see C19-R07).

*Verdict:* fix the owner conflict (C18-R08).

**### The contracts between components (`:97–128`).** *Adds:* the Task Service API, which is the most concrete artifact in the chapter and the only implementation anywhere of Ch 11's handoff (Ch 11 has no implementation section). *Issues:*
- `POST /v1/runs/{run_id}/plans:revise` (`:108`) collides with Ch 12's `POST /v1/plans/{plan_id}/revisions/{revision}:validate|:commit` (`04-part-iv.md:494–495`).
- The JSON child-task request (`:115–127`) uses field names that disagree with the TaskEnvelope code 140 lines later.

*Verdict:* keep the API table, delete the plan-revise row, and drop or align the JSON (C18-R04, R08).

**### Records worth preserving (`:130–140`).** *Adds:* AgentVersion, Task, TaskDependency, TaskAttempt, OwnershipTransfer, TaskArtifact, JoinPolicy. The set is coherent. `Task.state` has no enumerated values (C18-R03). OwnershipTransfer is the record Ch 11 implies but never names, so add "(the handoff record of Chapter 11)". *Verdict:* good.

**### State, consistency, and scale (`:142–151`).** *Adds:*
- Unique and valuable: per-run serialization, dispatch keys, manifest-level delegation defaults, hot-run mitigation, immutable terminal state plus artifact hash.
- Generic boilerplate repeated across chapters (map §5.1): partition by tenant + run, no global lock, strong vs eventual consistency.

`risk_class` (`:146`) is used before Ch 22 defines it. *Verdict:* condense (C18-R11).

**§ What the evidence lets us conclude (`:153–159`).** *Issues:*
- The one claim ("Multi-agent structure does not inherently improve quality … evaluate against the strongest single-agent baseline") is attributed to R28. R28's recorded scope is "Reports multi-agent research architecture and token/context trade-offs". The quality claim and the baseline rule are book-authored recommendations, so the citation over-reaches its scope (AGENTS.md § Citation safety).
- The "draws on" sentence omits R33, although the evidence context cites it.

*Verdict:* rewrite (C18-R12).

**§ How Supervisor/Worker works in practice (`:161–203`)** with its § How the pattern works, § Where it helps—and what it costs, § Where it can fail—and how to contain it, and § What you need to see in production. *Adds:* a compact summary. The useful failure rows are runaway fan-out, conflicting artifacts, and child leakage. *Issue:* it is the near-twin of the next card. *Verdict:* keep as the single merged card (C18-R02).

**§ How Multi-Agent Collaboration works in practice (`:205–247`)** with the same four H3s. *Adds:*
- Two things not in the first card: the artifact-adoption step (`:218`) and the split-ownership / message-duplication failure rows.
- Its "Use when: across teams, regions, vendors, trust domains" is Ch 19's subject.
- Its "Remote task never completes" row and the "peer identity" signal duplicate Ch 19 § Scalability, federation, and failure isolation (`:550`) and § Records worth preserving (`PeerObservation`).

The card's definition ("conversation is advisory, while workflow state determines truth") restates `:45`. *Verdict:* merge into the first card and delete (C18-R02).

**## A sensible place to start (`:249`).** This is an empty wrapper H2 with two blank lines (map §5.3 pattern). It is acceptable only if it keeps at least one child.

**### Durable child-task contract (`:252–274`).** *Adds:* the TaskEnvelope code. *Issues:*
- It lacks the fields that the JSON request, the Delegation rule, and Ch 19's field-group table require: idempotency key, output schema, dependencies, delegation depth, trace context.
- It has `capability` and `capability_grant_id` side by side with no explanation.

*Verdict:* make it the canonical TaskEnvelope, aligned to the field groups (C18-R04).

**### Monotonic child authority (`:276–347`).** *Adds:* nothing that Ch 21 does not repeat verbatim. *Issues:*
- The reader meets a 12-field `CapabilityEnvelope` dataclass before any chapter has defined the envelope (map §4 row 52).
- This is inline code duplicated across chapters, contrary to the AGENTS.md code policy.

*Verdict:* remove, and add a three-sentence bridge (C18-R01).

**Template close: § If this fails in production (`:349–353`), § What to verify before production (`:355–365`), § Put the idea to work (`:367–370`), § Questions to bring to design review (`:372–380`).**
- *If this fails* is three concrete steps that fit the chapter. Step 2 should point to Ch 21's subset proof.
- *Verify:* items 1–4 are good. Item 5 (MCP/A2A gateways, `:365`) verifies Ch 19 content inside Ch 18 and duplicates Ch 19's first checklist item.
- *Put the idea to work:* two good exercises. #2 deliberately bridges to Ch 19's remote task.
- *Questions:*
  - Q1 reinforces the chapter's core claim. That is acceptable.
  - Q2 (`:377`) duplicates Ch 03's Q (`01-part-i.md:1307`) and Ch 11's Handoff card "Do not use when" (`04-part-iv.md:278`). Its answer defines handoff as "conversational control transfer", which is Ch 03's meaning and contradicts Ch 11's (durable, acknowledged ownership transfer).
  - Q3 is good as a bridge to Ch 21.
  - Q4 is good.
  - Q5 (`:380`, "What does an A2A or MCP protocol not solve?") is answered by Ch 19 § Two protocols, two responsibilities and belongs there.

*Verdict:* rewrite Q2 and Q5 and remove verify item 5 (C18-R05, R13).

**§ Where this leads next (`:382–384`).** "Chapter 19 extends those controls to external tools, agents, and model providers." The "model providers" clause commits Ch 19 to the LLM Gateway material that C19-R01 moves out. *Verdict:* rewrite (C18-R15).

## Sparse or Underdeveloped Content

- **Task lifecycle (missing).** The chapter's central claim is a "durable state machine" (`:25`), yet no state set exists. The `:accept` / `:complete` / `:fail` / `:cancel` APIs and `Task.state` imply one. The canonical local states (Created/Dispatched, Accepted/Running, NeedsInput, CompletedPendingValidation, Succeeded, CancelRequested, Failed/Expired/InterventionRequired) are in Ch 19 (`:531–539`), where they are framed as a *federated* mapping. Bring them home (C18-R03). This is the only expansion recommended, and it is net-neutral because the states move from Ch 19.
- **Capability envelope at point of use.** Once the duplicate code goes, the reader needs a two-sentence working definition (scope ceiling: actions, resources, purposes, data classes, regions, risk, cost, depth, expiry), with Ch 21 as the full treatment (C18-R01).
- **Artifact adoption** is in the state-owner row's trust boundary (`:37`) and in a card step (`:218`), but it gets no prose. Point to Ch 19's `:adoptResult` and the adoption check (C19-R16) rather than expanding here.

## Missing Conceptual Connections

- **"Narrowed child authority" (`:19`, `:26`, `:43`) → `derive_child` code (`:316`), missing B: what a capability envelope is.** Location: `:276`. Bridge: a short definition plus a pointer to Ch 21 § Three identities every decision should preserve and § Capability-envelope subset proof.
- **"Durable state machine" (`:25`) → task APIs (`:103–107`), missing B: the task state set and who may make each transition.** Location: after `:82` (C18-R03).
- **Ch 11 handoff (acknowledge or reject; previous owner accountable) → Ch 18 `:handoff` API and OwnershipTransfer, missing B: "this is the implementation of Ch 11's handoff, including the acknowledgment wait".** Location: `:78`, `:104`, `:138`.
- **Ch 12 plan revision → Ch 18 plan-change rule, missing B: the revision is Ch 12's protocol, invoked by the coordinator.** Location: `:82`, `:91`, `:108`.
- **Child task → Ch 15 durable child workflow, missing B: "a child task runs as a child workflow with the durable waits, timers, and cancellation of Chapter 15".** Location: `:103` ("starts or binds a child workflow") is the only mention.
- **Cancellation of an executing mutation (`:47`) → unknown-outcome reconciliation, missing B: a forward pointer to Ch 22 § The lifecycle of an external effect.**
- **AP-11's monotonic budget withdrawal → Ch 18's tree-wide caps (`:47`, `:148`), missing B: "this is the AP-11 correction made concrete".**

## Transition Problems

- **In (Ch 17 → Ch 18).** Ch 17 closes with "Chapter 18 considers when multiple agents add justified specialization", but AP-08 and AP-11 have already given Ch 18's conclusions. Ch 18's opening never acknowledges them, so the reader feels a restart. Fix in Ch 18 § Why… (C18-R07). No change is needed in Ch 17.
- **Within.** The § Choose a topology—and define how the work ends heading promises termination semantics that never come (C18-R03). The jump from § Records/§ State to the two pattern cards is a template seam, acceptable once the cards are merged.
- **Out (Ch 18 → Ch 19).** The closing promises "model providers", a commitment C19-R01 removes. Ch 19 opens with its own "why" and never references Ch 18's TaskEnvelope or task tree, although its A2A Gateway "translates local TaskEnvelope" (`:438`). The bridge belongs in Ch 19 (C19-R03, C19-R12).

## Redundant and Repetitive Concepts

| Concept | Occurrences in Ch 18 | Verdict |
| --- | --- | --- |
| Justification for another agent | `:27–28`, `:32`, `:56` (Recommended architecture), `:157` (evidence), `:179` (card), `:357` (verify), `:376` (Q1) | Redundant. Keep `:32` (prose), the topology table, `:357`, and Q1. Cut `:27–28`, `:56`, and the second card (C18-R06, R02, R07). |
| One owner / durable task, not chat | Design choice, `:25`, `:32`, `:45`, `:213`, `:223`, Required-analysis row | Redundant across the two cards and the table. Resolved by C18-R02 and R06. |
| Child task field list | `:77`, `:102`, `:115–127`, `:135`, `:261–274` | Five lists with drift (C18-R04) |
| Envelope narrowing | `:47`, `:78`, `:172`, `:194`, `:316–346`, `:352`, `:361`, `:378` | Short reminders are reinforcement. The code block is redundancy (C18-R01). |
| Join semantics | `:45`, `:95`, `:140`, `:174`, `:363`, `:379` | Mostly reinforcement. Acceptable. |

## Cross-Chapter Duplication

| Ch 18 location | Other location | Verdict | Action / owner |
| --- | --- | --- | --- |
| § Monotonic child authority (`:280–347`) | Ch 21 § Capability-envelope subset proof (`06-part-vi.md:528–595`); identical by `diff` | **Redundancy** (exact duplicate) | Ch 21 is canonical (agrees with concept map S11). Ch 18 removes it (C18-R01). Ch 21 should keep its code and add a back-pointer to Ch 18's Task Service (Ch 21 review). |
| `TaskEnvelope` code (`:261`) | Ch 19 `A2ATaskEnvelope` (`:621`); Ch 19 § What the TaskEnvelope needs to carry (`:473`); Appendix C row (`09-appendices.md:68`) | **Redundancy with drift.** The map says the first ten fields are identical, but I count eight shared fields: `owner_agent`→`owner`, `state_version`→`expected_version`, and `capability` and `cancellation_parent_id` dropped in the A2A version. | Ch 18 canonical (agrees with map). Ch 18 receives the field-group table (C18-R04). Ch 19 drops its copies (C19-R03). |
| Handoff rule (`:78`), topology row (`:70`), Q2 (`:377`), `:handoff` API, OwnershipTransfer | Ch 03 § Three meanings of handoff; Ch 11 § Routing and handoff are different events, § How Handoff works in practice | Topology row and API = reinforcement / application. Rule `:78` = drift (no acknowledgment). Q2 = redundancy that also contradicts Ch 11. | Ch 11 owns handoff semantics. Ch 18 owns the task-service implementation (C18-R05). The Ch 03 vs Ch 11 meaning of "handoff" needs reconciling by the Part I/IV reviews. |
| Router component (`:94`) | Ch 11 route service (`04-part-iv.md:187`, `:224`) | Reinforcement | Add a pointer (C18-R05) |
| Plan-change rule (`:82`), `plans:revise` (`:108`), Run Coordinator "plan revision" (`:91`) | Ch 12 § The contracts between components (`04-part-iv.md:494–495`), Plan Store (`:482`) | **Redundancy with conflicting endpoint and owner** | Ch 12 canonical (C18-R08) |
| Termination bullet (`:81`) | Ch 15 § Terminal correctness; Ch 10 dispositions; Ch 19 state mapping | Drift (map T12) | Use Ch 15's run terminals. Task lifecycle in Ch 18 (C18-R03). |
| Both pattern cards | Ch 16 P-06 (`04-part-iv.md:1427`); Appendix A item 4; AP-08 | One pattern, five descriptions (map §5.2) | Merge to one card (C18-R02). P-06 and Appendix A should point to it (Ch 16/Appendix reviews). |
| Tree-wide caps (`:47`, `:148`) | AP-11 correction (`04-part-iv.md:1566–1582`) | Reinforcement (AP is diagnosis, Ch 18 is design) | Add a pointer (C18-R14) |
| Q5 (`:380`) and verify item (`:365`) | Ch 19 § Two protocols…, Ch 19 Q1–Q3 and verify item 1 | Redundancy (pre-teaches Ch 19) | Remove from Ch 18 (C18-R13) |
| Figure 18-1 narrowing | Figure 17-2, Figure 21-1 | Reinforcement (three views of narrowing, map §7.1). Acceptable once 18-1 uses the case's labels. | C18-R09 |
| Artifact adoption step (`:218`) | Ch 06 § Cross-boundary artifact adoption policy (code with no prose); Ch 19 `:adoptResult`, RemoteArtifact, Q4 | Concept with no prose home | Canonical home Ch 19 (C19-R16). Ch 18 points to it. |

## Structural Recommendations

1. **One envelope proof, one TaskEnvelope.** Ch 21 owns the proof. Ch 18 owns the TaskEnvelope, including the field-group table moved from Ch 19.
2. **Add the task lifecycle under § Choose a topology—and define how the work ends** and remove that H2's Required-analysis table. The H2 then holds: the topology table, the orchestration rules, and the task lifecycle.
3. **One pattern card** (Supervisor/Worker) instead of two.
4. **Point, don't re-specify,** for handoff (Ch 11), plan revision (Ch 12), child workflow durability (Ch 15), and the envelope (Ch 21).
5. Resulting order: opening → § Why (with the Ch 17 bridge) → § What every collaboration must make explicit → § Treat collaboration as durable work → § Choose a topology… (topology table, rules, lifecycle) → § A workable implementation → evidence → one card → § A sensible place to start (TaskEnvelope only) → template close.

## Concrete Recommended Changes

1. **C18-R01 — High — Remove + Cross-reference**
   - **Location:** `05-part-v.md:276–347`, § Monotonic child authority.
   - **Issue:** The code is byte-identical to Ch 21 § Capability-envelope subset proof and is shown before envelopes are defined.
   - **Why it matters:** The reader parses a 12-field security dataclass without its model, then meets it again three chapters later as if new.
   - **Change:** Delete the H3 and its code block. In § Treat collaboration as durable work (after `:43`), add: "Each child's authority is a *capability envelope*: the maximum actions, resources, purposes, data classes, regions, risk, cost, delegation depth, and lifetime it may use. The Task Service derives it from the parent's envelope by intersection and refuses any child envelope that is not a provable subset. Chapter 21 defines the envelope and gives the subset proof." In § If this fails step 2 (`:352`), append "(Chapter 21 § Capability-envelope subset proof)".
   - **Related:** Ch 21 keeps the code. The Ch 21 review should add one clause such as "the Task Service in Chapter 18 calls this before creating a child task" and must not remove its copy.

2. **C18-R02 — High — Merge**
   - **Location:** `:161–247`, § How Supervisor/Worker works in practice and § How Multi-Agent Collaboration works in practice.
   - **Issue:** The two cards describe one pattern. The second card's distinct material is Ch 19's.
   - **Why it matters:** Two cards imply two patterns, and the reader cannot tell when to pick which.
   - **Change:** Keep the Supervisor/Worker card and delete the Multi-Agent Collaboration H2 and its four H3s.
     - **Steps:** change step 4 to "Collect artifacts under explicit join semantics and adopt them only after schema, provenance, quality, and policy validation".
     - **Do not use when:** append "or when free-form conversation would be the only coordination record".
     - **Failure table:** add "Split ownership → single current owner and versioned OwnershipTransfer" and "Duplicate or reordered status → idempotent task creation/completion and expected versions". Drop "Remote task never completes"; Ch 19 covers it.
     - **What you need to see in production:** task tree; current owner and owner version; grant lineage; child state and budget; join condition and outcome; artifact lineage; conflicts and resolution.
   - **Related:** Ch 16 P-06 and Appendix A item 4 should point to this one card (Ch 16/Appendix reviews).

3. **C18-R03 — High — Add (moved content)**
   - **Location:** After `:82`, § Recommended orchestration rules, under § Choose a topology—and define how the work ends. Also `:81`, the Termination rule.
   - **Issue:** The chapter claims a durable state machine but defines no states. The canonical local states live in Ch 19 `:531–539`.
   - **Why it matters:** Ownership, joins, and cancellation are all transitions. Without the state set, the API table has nothing to transition.
   - **Change:** Add H3 "### Task lifecycle" with a three-column table (State | Entered when | Who may move it on):
     - Created/Dispatched
     - Accepted/Running
     - NeedsInput
     - CompletedPendingValidation (artifacts quarantined)
     - Succeeded (only after join/acceptance; see Chapter 15 § Terminal correctness)
     - CancelRequested → Canceled (after any executing mutation reconciles)
     - Failed / Expired / InterventionRequired

     Follow it with the two general rules moved from Ch 19 § Ownership and failure rules bullets 2–3 (`:489–490`): the receiver may reject, accept, request input, produce partial artifacts, complete, fail, or acknowledge cancellation, and terminal tasks accept no new work; cancellation propagates downward by default, while compensation follows domain policy. Rewrite the Termination bullet (`:81`) to: "Terminal transitions follow the task lifecycle below; the model may recommend completion but cannot make the transition."
   - **Related:** C19-R04 and C19-R05 (Ch 19 keeps only the remote-interpretation mapping).

4. **C18-R04 — High — Move + Rewrite**
   - **Location:** `:77` (Delegation rule), `:111–128` (JSON child-task request), `:252–274` (§ Durable child-task contract). Source: `:473–484` (Ch 19 § What the TaskEnvelope needs to carry).
   - **Issue:** There are five child-task field lists with drifting names. The fullest specification is in Ch 19.
   - **Why it matters:** TaskEnvelope is the core contract of Part V. The reader should meet one definition, here.
   - **Change:** **Reconciled (see overall-book-review.md §D-23):** As stated, but the aligned TaskEnvelope code leaves the chapter: add it as region `task` in `examples/contracts.py` with a behavioural test (idempotent creation, depth limit, envelope-subset hook), register the region in `config/examples.json` for chapter 18, and cite `[[EXAMPLE:contracts#task]]` under § Durable child-task contract. Ch 19 refers to the same region instead of its deleted A2ATaskEnvelope.
     - Move the Ch 19 field-group table to § Durable child-task contract, above the code, introduced as "A TaskEnvelope carries eight field groups:".
     - Align the code to it: add `idempotency_key`, `output_schema`, `depends_on`, `delegation_depth`, and `trace_context`. Rename to the book's capability-envelope term (keep `capability_grant_id` as the envelope reference, and explain `capability` as the requested capability name or remove it).
     - Delete the JSON excerpt (`:111–128`); the API row `:102` and the code now cover it.
     - Rewrite the Delegation rule (`:77`) to "create a child task carrying a TaskEnvelope (§ Durable child-task contract)".
   - **Related:** C19-R03 removes Ch 19's copies. Appendix C's TaskEnvelope row should match (Appendix review).

5. **C18-R05 — Medium — Cross-reference + Rewrite**
   - **Location:** `:61` (topology table intro), `:70`, `:78`, `:94`, `:138`, `:377`.
   - **Issue:** Handoff is re-specified without Ch 11's acknowledgment rule. Q2 duplicates Ch 03/Ch 11 and defines handoff as "conversational control transfer", contradicting Ch 11.
   - **Why it matters:** The reader learned in Ch 11 that the old owner stays accountable until acknowledgment. Ch 18 silently drops that rule.
   - **Change:**
     - Add before the topology table: "Routing and handoff keep the meanings from Chapter 11: routing chooses a worker; handoff transfers accountability and completes only when the recipient acknowledges."
     - Rule `:78` → "**Handoff:** follow Chapter 11's acknowledged transfer; the Ownership Service records it as an OwnershipTransfer and issues a narrowed capability envelope; the prior owner remains accountable until acknowledgment and is kept as history afterward."
     - Router row `:94`: append "(Chapter 11's route service)".
     - Replace Q2 with "What must happen before a parent cancellation is reported complete?" Strong answer: "Cancellation is persisted as durable intent and propagated to every child; children with executing mutations reconcile before acknowledging; the API distinguishes requested, acknowledged, and completed."
   - **Related:** The Part I/IV reviews should reconcile Ch 03's "conversational transfer" with Ch 11's handoff. Ch 18 follows Ch 11.

6. **C18-R06 — Medium — Remove**
   - **Location:** `:49–59`, the Required-analysis table under § Choose a topology—and define how the work ends.
   - **Issue:** Five of seven rows restate `:32`, `:43`, and the topology table.
   - **Why it matters:** It is the fourth statement of the justification rule in 60 lines.
   - **Change:** Delete the table. Insert the Trade-offs row as one sentence before the topology table: "Central coordination is easier to govern but can bottleneck; decentralized collaboration may widen coverage at the cost of determinism, auditability, and cost control." Move the Failure scenarios items not already in the merged card's failure table (ping-pong handoffs, circular delegation, two agents mutating one record, premature "done") into that table as one row: "Ping-pong or circular delegation → acyclic ownership graph and depth limits". Concurrent mutation of one record is covered by the Shared state rule.

7. **C18-R07 — Medium — Rewrite**
   - **Location:** `:25–28`, § Why more agents do not automatically make a better system.
   - **Issue:** The passage restates the design-choice box and ignores AP-08 and AP-11.
   - **Change:** Replace `:25–28` with: "Chapter 17 showed the two ways this goes wrong: chat used as the workflow (AP-08) and budgets that reset at every hop (AP-11). This chapter builds the replacement: a task tree with one owner per task, narrowing authority, explicit joins, and durable cancellation."

8. **C18-R08 — Medium — Cross-reference + Remove**
   - **Location:** `:82` (Plan changes), `:91` (Run Coordinator), `:108` (`plans:revise`).
   - **Issue:** This duplicates Ch 12 with a different endpoint and a second owner.
   - **Change:**
     - Delete API row `:108`.
     - Rule `:82` → "**Plan changes:** use Chapter 12's revision protocol; new nodes are validated against the original capability envelope, and materially broader scope needs new approval."
     - Run Coordinator "Owns" → "Goal lifecycle, child-task policy, terminal decision; requests plan revisions from the Plan Service (Chapter 12)".

9. **C18-R09 — Medium — Rewrite (diagram source)**
   - **Location:** `:41`, Figure 18-1; `assets/diagrams/src/supervisor-worker.gv` (t1–t3 labels).
   - **Issue:** The children are "screening", "tax", and "security". The prose and case use document extraction, income verification, property review, and policy.
   - **Change:** Relabel t1–t3 (or add t4) as "Child task / document extraction", "income verification", "property review" (optionally "policy explanation"). Run `make diagrams` and update the alt text in `config/diagrams.json` if it names the tasks.

10. **C18-R10 — Low — Rewrite (terminology)**
    - **Location:** `:32` "authority envelope", `:76` "AgentManifest", `:77`/`:102`/`:122` "authority ceiling", `:82` "authority envelope", `:104` "capability grant".
    - **Change:** Use "capability envelope" (map T6) and "AgentSpec" (map T8) throughout. Keep `capability_grant_id` only as a field name, glossed once.

11. **C18-R11 — Low — Condense**
    - **Location:** `:142–151`, § State, consistency, and scale.
    - **Change:** Merge bullets 1, 2, 4, and 6 into one: "Partition by tenant + run so a run's tasks are shard-local; let the run's durable workflow serialize its control decisions; use strongly consistent transactions for task creation, owner transfer, terminal transition, and budget reservation, and eventually consistent projections for the graph and analytics." Keep bullets 3, 5, 7, and 8 as written. Replace `risk_class` in bullet 3 with "risk class (Chapter 22)".

12. **C18-R12 — Low — Rewrite (citation scope)**
    - **Location:** `:157–159`, § What the evidence lets us conclude.
    - **Issue:** The row claims more than R28's recorded scope, and R33 is omitted.
    - **Change:** Grounded statement → "R28 reports a supervisor/specialist research architecture and its token and context costs; R33 documents a managed supervisor/collaborator pattern. The book's recommendation, not a sourced finding, is to add specialists only when capability, ownership, trust, isolation, or parallelism justifies the cost, and to evaluate against the strongest single-agent baseline." Source IDs: R28; R33. The fixed sentence becomes "draws on R28; R33".

13. **C18-R13 — Low — Remove**
    - **Location:** `:365` (verify item 5) and `:380` (Q5).
    - **Issue:** Both teach and verify Ch 19 content before Ch 19.
    - **Change:** Delete verify item 5. Replace Q5 with "How do you keep a task tree inside its budget?" Strong answer: "Children withdraw from the parent's remaining budget rather than receive fresh limits; depth, children, concurrency, and plan revisions are capped by manifest defaults that risk policy may lower; per-run semaphores bound ready nodes."

14. **C18-R14 — Low — Cross-reference**
    - **Location:** `:47`.
    - **Change:** **Reconciled (see overall-book-review.md §D-32):** As stated, but the second pointer reads "(Chapter 22 § A reliable protocol for changing the outside world)"; C22-R03 deletes § The lifecycle of an external effect. Original text: After "…across the entire task tree", add "(the AP-11 correction)". After "must reconcile before acknowledging final cancellation", add "(Chapter 22 § The lifecycle of an external effect)". At `:103`, after "starts or binds a child workflow", add "(Chapter 15)".

15. **C18-R15 — Low — Rewrite**
    - **Location:** `:384`, § Where this leads next.
    - **Change:** "Inside one platform, the Task Service enforces these rules directly. Chapter 19 carries the same ownership and narrowing rules to tools and agents outside the platform, where a protocol moves the message but not the trust." This depends on C19-R01. If the LLM Gateway stays in Ch 19, keep "model providers".

16. **C18-R16 — High — Rewrite (API and record).** *Added in reconciliation (see overall-book-review.md §D-06).*
   - **Location:** `05-part-v.md:102` (`:accept` row), `:104` (`:handoff` row), `:138` (OwnershipTransfer).
   - **Issue:** The Ch 11 review asks Ch 18 to make `:handoff` a pending transfer committed by `:accept` and to align OwnershipTransfer with Ch 11. C18-R05 fixed only the rule and the question.
   - **Change:** `:handoff` → "Propose an ownership transfer to a target agent/version with rationale, obligations, deadline, remaining budget, and narrowed capability envelope; the transfer stays pending until the recipient calls `:accept` with expected_version; rejection or expiry leaves the current owner accountable." `:accept` → "Receiver accepts a new child task or a pending ownership transfer using expected_version; starts or binds a child workflow (Chapter 15)." OwnershipTransfer: add obligations, deadline, and acknowledgment state (proposed, accepted, rejected, expired); replace "authority grant" with "capability envelope"; change "transactionally updates Task.owner" to "updates Task.owner only on acceptance".
   - **Related:** C11-R03, C11-R12, C18-R05.

17. **C18-R17 — Low — Rewrite (card policy).** *Added in reconciliation (see overall-book-review.md §D-04).*
   - **Location:** The merged card from C18-R02 (`05-part-v.md:161`).
   - **Issue:** The card policy (C10-R04) had no Ch 18 reciprocal.
   - **Change:** Retitle the merged card "Supervisor/Worker at a glance" and delete its THE ENGINEERING PROBLEM box and lead sentence. Keep C18-R02's step, failure-table, and signal edits.
   - **Related:** C18-R02, C10-R04, C16-R10.

18. **C18-R18 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** End of § If this fails in production.
   - **Issue:** Same request as C05-R16.
   - **Change:** Add one line: "If chat is the coordination record or each child gets fresh limits, see AP-08 and AP-11 in Chapter 17."
   - **Related:** C17-R03, C18-R07.
