# Chapter 03 — Keep the Agent Framework in Its Lane: Continuity and Flow Review

Reviewed: `source/parts/01-part-i.md:900–1312`, plus the Ch 02 closing (`:892–898`), the Ch 04 opening (`02-part-ii.md:1–95`), and the downstream sections Ch 03 pre-teaches. Those are Ch 11 (`04-part-iv.md:172–301`), Ch 14 (`:864–951`), Ch 15 (`:1125–1192`), Ch 18 (`05-part-v.md:21–82`, `:377`), Ch 20 (`06-part-vi.md:20–98`, `:236–256`), Ch 21 (`:389–427`), and Ch 22 (`:644–845`).

## Overall Assessment

Chapter 03 owns one argument that no other chapter makes: **the agent framework runs one bounded step behind a platform contract, and framework state never becomes enterprise truth.** The material that carries this argument is strong and canonical:

- the principle "let the framework run the agent; let the platform run the business" (`:964`)
- the four-row boundary table (`:957–962`)
- the 16-row framework-vs-platform table (`:991–1008`)
- the AgentRuntime rationale (`:1012–1033`)
- the AgentStepRequest field groups (`:1039–1053`)
- the adapter section and example (`:1055–1065`)
- framework state vs. business state (`:1109–1125`)
- the restart test (`:1127–1131`) and the replaceability test (`:1236–1242`)
- upgrades as behavior changes (`:1219–1234`)

The chapter then spends about 120 lines (`:1067–1217`) previewing mechanisms other chapters own, at near-full depth: the Tool Gateway questions (Ch 21/22), the protected write path (Ch 02/22), the approval record and proposal hash (Ch 14), handoff semantics (Ch 11/18), the guardrail layer stack (Ch 20), retry ownership (Ch 22), and a nine-step execution path (Ch 04/15). I checked these against the downstream text:

- **Duplicates.** § Bind approval to the exact proposal restates Ch 14 `:884` and Ch 14's own enterprise example (`:898`, the same employment-evidence scenario). § Guardrails and authorization… restates Ch 20 § Guardrails help, but they are not the security boundary, with the same injected-document scenario and a seven-layer stack against Ch 20's nine. § One retry owner restates Ch 22 `:839` and § Choose the response that matches the failure. § The same rule applies to writes and § The complete execution path re-sequence Ch 02's gates (8 and 9 steps).
- **Terminology conflict.** § Three meanings of handoff calls an SDK "framework handoff" a transfer in which "the same activity remains accountable" (`:1163`). Ch 11 defines a handoff as the event in which accountability *changes*, on acknowledgment (`04-part-iv.md:182`, `:195`). Ch 18 says a handoff "atomically transfer[s] the conversation owner and issue[s] a new capability envelope" (`05-part-v.md:78`). These are three meanings of one term.
- **Unique and worth keeping:**
  - The SDK-interruption vs. platform-approval event table (`:1141–1146`). No later chapter discusses SDK interruptions.
  - The SDK-handoff distinction, once reframed.
  - The unsafe vs. governed tool path and the `MORT-2026-000999` exact-resource example (`:1071–1090`), which no other chapter uses.
  - The six-step boundary debugging order (`:1279–1286`).

**No chapter in Parts II–VIII refers back to Chapter 3** (grep of `02-part-ii.md`–`09-appendices.md`). The pre-teaching is therefore not leveraged anywhere, and trimming it removes nothing later chapters depend on.

Ordering defects compound the length:

- AgentRuntime and `AgentStepResult` are used (`:912`, `:931`, `:960`) before § Why the SDK sits behind AgentRuntime defines them (`:1018–1022`).
- The C03 checkpoint code appears before the reader has seen the contract it implements.
- The chapter has three ownership tables (`:957`, `:991`, `:1248`), introduces the replaceability test twice (`:1010`, `:1236`), and repeats the restart test in § What this chapter established (`:1294`).

The template deviates from Ch 01 and Ch 02 in four ways: no § A sensible place to start, What-to-verify placed before If-this-fails, plain bullets, and no § Put the idea to work.

## Intended Reader Mental Model

After Chapter 03 the reader should hold:

- **What:** `AgentRuntime.execute(AgentStepRequest) → AgentStepResult` is a platform-owned seam. Inside it, a framework adapter runs one bounded reasoning step.
- **Why:** applications that each integrate an SDK directly develop incompatible assumptions, and SDK state leaks into workflow truth (`:1016`, `:1024–1029`).
- **How:**
  - The workflow builds a bounded request: identity, behavior pins, authorized context, capabilities, bounds, output contract.
  - The adapter translates the request into the SDK and maps the result back.
  - The result's proposed action enters Chapter 2's gates.
  - Framework tools are façades.
  - SDK interruptions, guardrails, handoffs, and retries are local mechanics, and the platform owns their enterprise meaning.
- **When:** at every framework adoption, upgrade, restart, and migration.
- **Trade-offs:** an adapter layer and conformance tests in exchange for replaceability and recoverability.
- **Relationships:**
  - The step result is the Propose gate (Ch 02).
  - Pins come from the RunManifest (Ch 04).
  - Context comes from the ContextManifest (Ch 06).
  - Scope comes from the capability envelope (Ch 21).
  - Durability comes from Ch 15.
  - Approval, handoff, guardrails, and retries are owned by Ch 14, 11/18, 20, and 22.
- **Practical application:** C03, the last implemented checkpoint.

What, Why, How, and the two tests are delivered well. The bridge from the step result to the Propose gate is missing, and the Relationships are blurred: Ch 03 re-teaches neighboring mechanisms instead of handing them off, so the reader cannot tell which ideas are this chapter's and which are previews.

## Section-by-Section Flow Review

**Opening (`:902–912`).**
- *Role:* evidence scope, supplier comparison, design choice.
- *Verdict:* cluttered.
  - Two blockquotes (`:902`, `:904`) both scope the SDK use. The second is unattributed and promises "Chapters 4–7 place that boundary". Ch 04 never names AgentRuntime, and Ch 07 renames it AgentSpec/RunContext (`03-part-iii.md:27`, `:58`).
  - The supplier box (`:908`) restates the design choice.
  - There is no case box, although C03 is the case's final implemented checkpoint (map).

**§ Why the framework boundary matters (`:914`).**
- *Role:* the "why" H2.
- *Adds:* "the boundary becomes important when a framework changes, a run pauses, or a connector needs to prove who authorized an effect" (`:920–921`), a useful trio of triggers.
- *Verdict:* mostly restates the design choice (map: double-why). Merge it into the chapter intro.

**§ Start with a concrete scenario (`:923`).**
- **§ Mortgage checkpoint: the runtime seam (`:925`):** misplaced. The Before/Added/After table and `[[EXAMPLE:mortgage-cumulative-case#c03]]` show `AgentStepRequest`/`AgentStepResult` and "an allowlist escape fails before execution" before any of those is explained. Ch 01 and Ch 02 put their checkpoints near the end under § A sensible place to start.
- **`:939–953` (scenario prose):**
  - Re-introduces the case as new ("Consider Harborlight mortgage case MORT-2026-000184, a synthetic purchase application for Alex Morgan"), although the reader has followed it for two chapters.
  - The seven-step workflow (`:943–949`) re-lists Ch 01's case "Workflow" row (`:44`) with drift.
  - `:951` ("Before an agent runs, the platform already knows…") is excellent and should stay.
  - `:953` defines the agent's narrow task (sufficient / insufficient / additional evidence). § What the agent actually does repeats it at `:972`.
- **Boundary table (`:957–962`) + principle (`:964`) + Figure 3-1 (`:966–968`):** canonical. Keep. "This gives Northstar a durable shape" uses the second name (T1). AgentRuntime appears in the table before it is defined.

**§ What the agent actually does (`:970`).**
- *Role:* contrasts the agent's job with the platform's questions.
- *Adds:* the six questions the framework must not answer (`:978–983`), which is concrete and useful.
- *Verdict:* `:972` duplicates `:953`. `:974` (the framework capabilities the platform should use rather than rebuild) is new.
- *Issues:*
  - The disposition vocabulary (sufficient / insufficient / additional evidence) is not reconciled with `AgentStepResult.status` (`completed | needs_input | proposed_action | failed`, `examples/contracts.py:45`). Ch 02's JSON uses `propose_effect`.
  - The C03 test returns `status: needs_input` with summary "A second pay statement is missing." (`tests/mortgage_case/contract/test_c03_runtime.py:76`). That is the reconciliation the prose never states: the domain assessment travels inside a step status.

**§ Runtime responsibility versus enterprise responsibility (`:987`).**
- *Role:* the canonical 16-row framework/platform table.
- *Adds:* per-feature ownership. It is the most complete statement of the boundary.
- *Verdict:* keep, but it is the second ownership table in 30 lines and arrives before AgentRuntime is defined.
- *Issues:*
  - `:1010` introduces the replaceability test, which § The replaceability test then re-introduces at `:1236`.
  - Nothing links the table to Ch 01's uncertainty table or Ch 02's distributed-systems table (the same "who owns it" question on a different axis).

**§ Why the SDK sits behind AgentRuntime (`:1012`).**
- *Role:* defines AgentRuntime and justifies it.
- *Adds:* the multi-team divergence problem, the call chain (`:1020`), and the direct-vs-boundary table.
- *Verdict:* strong. It should come before the responsibility tables, since everything above it uses the term. The ARCHITECTURE GUIDANCE box (`:1033`) adds "control of responsibility, not only vendor lock-in". That is reinforcement; keep it.

**§ The request is bounded before the model sees it (`:1035`).**
- *Role:* the canonical AgentStepRequest/AgentStepResult contract.
- *Adds:* field groups, result contents, and the conceptual interface (`:1053`).
- *Verdict:* core. Keep.
- *Issues:*
  - Forward terms appear without pointers: "Authorized `ContextManifest`" (Ch 06), "trust labels" (Ch 06), "capability ceiling" (a sixth name for the capability envelope, T6; Ch 21), "cancellation lineage" (Ch 18).
  - "Agent definition" is not AgentSpec (T8).
  - The registered contract listing that matches this table (`examples/contracts.py` region `step`) is shown in Ch 01 instead of here.
  - The result paragraph (`:1051`) lists contents but not the status enum.
  - Ch 01 Level three's "termination is a property of a text generator" (`01-part-i.md:278`) is answered by the Bounds row, and the text never says so.

**§ The adapter builds one bounded runtime (`:1055`).**
- *Role:* adapter mechanics plus `[[EXAMPLE:step-execution#core]]`.
- *Verdict:* good. The scoping paragraph (`:1065`) is appropriate.

**§ A tool is not the enterprise API (`:1067`).**
- *Role:* SDK function tools as façades.
- *Adds:* the unsafe path vs. the governed path (`:1071–1073`). This is framework-specific (what may live inside an SDK tool function) and unique.
- *Verdict:* keep the paths and "Tool availability is not authorization" (`:1082`).
- *Issues:* the six gateway questions (`:1075–1080`) restate Ch 21's authorization tuple (`06-part-vi.md:403–407`) and Ch 22 § Invocation sequence steps 1–2 (`:780–782`). They are redundant here.

**§ Reauthorize the exact resource (`:1084`).**
- *Role:* the exact-resource check.
- *Adds:* the `MORT-2026-000999` example. It is concrete, used nowhere else in this form, and the clearest illustration of "valid schema ≠ authorized resource" in the book.
- *Verdict:* keep, and merge it with the previous section (same argument, one step further).
- *Issues:*
  - "capability envelope" (`:1088`) has no pointer (Ch 21).
  - `:1090` (data reads) is reinforcement of Ch 06/21. Keep it as one sentence.

**§ The same rule applies to writes (`:1092`).**
- *Role:* the protected write path.
- *Verdict:* redundant. The eight steps (`:1098–1105`) re-sequence Ch 02's six gates with approval inserted and ledger and receipt split.
- *Issues:*
  - "employment-verification" (`:1094`) conflicts with the case (T15).
  - `:1107` is the one framework-specific point: "successful SDK run is not the business record". Keep it.
  - The chapter pointers at `:1107` are good.

**§ Framework state versus business state (`:1109`).**
- *Role:* core distinction, with a table.
- *Verdict:* canonical. Keep.
- *Issues:* the evidence-status row (`:1118`) says "Mortgage application and purchase agreement available; employment-verification evidence missing". It omits the first pay statement and names the wrong missing document (T15).

**§ The restart test (`:1127`).**
- *Role:* the first operational test of the boundary.
- *Verdict:* canonical. Keep.
- *Issues:* no forward pointer to Ch 15, which makes this survivable with event history and durable waits.

**§ Human approval: interruption versus record (`:1133`).**
- *Role:* SDK interruption vs. enterprise approval.
- *Adds:* the four-row event table (`:1141–1146`) and the closing line (`:1148`). These are unique; Ch 14 never discusses SDK interruptions.
- *Verdict:* keep the table and closing line.
- *Issues:*
  - The `HumanActionAuthorizationRequest` field list (`:1137`) duplicates Ch 14 § Approval contract (`04-part-iv.md:902`) and Records (`:944`), with drift: Ch 14 adds before/after diff, separation of duties, and edit-and-resubmit.
  - "Platform approval" is yet another name (T3).

**§ Bind approval to the exact proposal (`:1150`).**
- *Role:* proposal-hash binding.
- *Verdict:* redundant. It duplicates Ch 14 `:884` ("Human action authorization becomes invalid when any protected field changes. A commit path rechecks…") and Ch 14's enterprise example (`:898`), which uses the same employment-evidence scenario and the same invalidation rule. AP-06 and Ch 22 `:673` repeat it again.

**§ Three meanings of handoff (`:1156`).**
- *Role:* distinguishes framework delegation from platform delegation.
- *Adds:* the useful rule "Use framework delegation for reasoning structure. Use platform delegation for operational ownership." (`:1166`).
- *Verdict:* the framework angle is legitimate and unique, but the table pre-teaches Ch 11 and Ch 18 and conflicts with them on what "handoff" means (see Overall Assessment).
- *Issues:* "Durable `TaskEnvelope` and child workflow" (`:1164`) is undefined (Ch 18).

**§ Guardrails and authorization solve different problems (`:1168`).**
- *Role:* SDK guardrails are not enforcement.
- *Verdict:* redundant with Ch 20 § Guardrails help… (`06-part-vi.md:28–45`), which makes the same argument with the same injected-document scenario and adds the detector / policy point / enforcement point distinction.
- *Issues:*
  - The seven-layer stack (`:1174–1180`) is a fourth layer count (Ch 20 has nine in its table and six in Figure 20-1; Ch 23 has eight).
  - This is the second of five tellings of the injected document.
  - The framework-specific point — SDK guardrails run inside the component being protected against — is implied but never stated.

**§ One retry owner (`:1184`).**
- *Role:* retry ownership.
- *Verdict:* redundant with Ch 22 `:839` (retry ownership), § Choose the response that matches the failure (`:823–834`), and AP-04. The framework-specific point (SDK transport retries must be disabled or declared) is absent.
- *Issues:*
  - The key-composition example uses `RUN-98217` (`:1197`), while Ch 06/18 use `run_42` (T16).
  - "effect layer" (`:1199`) vs. "effect service" (`:1194`) vs. "effect ledger" (`:1104`) is T24 drift.
  - "LLM Gateway may retry" (`:1192`) refers to Ch 19 with no pointer.

**§ The complete execution path (`:1203`).**
- *Role:* end-to-end walkthrough.
- *Verdict:* redundant. Figure 3-1 and its reading (`:966–968`) already show the flow, Ch 04 § End-to-end responsibility flow and Ch 15 § Canonical control flow repeat it, and the map recommends dropping Ch 03's. Only steps 3, 4, and 8 are framework-specific.
- *Issues:* none beyond duplication. The closing sentence (`:1217`) is good.

**§ Framework upgrades are behavioral changes (`:1219`).**
- *Role:* the SDK upgrade as a release event.
- *Verdict:* canonical. Keep.
- *Issues:*
  - The RunManifest table (`:1225–1232`) disagrees with Ch 04 § RunManifest (`02-part-ii.md:176–195`). Ch 04 has no `sdk`/adapter version, and Ch 03 puts `context_manifest` (a per-step record, Ch 06) in a per-run manifest.
  - `reasoning-standard@4` vs. Ch 04's `route://reasoning-standard@18` (T16).

**§ The replaceability test (`:1236`).**
- *Role:* the second operational test.
- *Verdict:* canonical, but its question was already posed at `:1010`. Pair it with the restart test.

**§ Responsibility map (`:1244`).**
- *Role:* summary table.
- *Verdict:* redundant. Its nine rows are a lower-resolution copy of the 16-row table (`:991–1008`). The closing sentence "Shared participation is not shared authority" (`:1260`) is new; keep it.

**§ What to verify before production (`:1262`).**
- *Role:* checklist.
- *Verdict:* good content.
- *Issues:* it sits before If-this-fails (every other chapter has the reverse order) and uses plain bullets instead of ✓. The approval and mutation items should carry pointers once those sections are condensed.

**§ If this fails in production (`:1277`).**
- *Role:* debugging the boundary in order.
- *Verdict:* reinforcement, not duplication of Ch 24 § Debugging method. It is specific to the request → adapter → model → gateway → effect → retry chain. Keep it. Item 6 is where the retry-owner point survives after condensing § One retry owner.

**§ What this chapter established (`:1288`).**
- *Role:* chapter summary (unique to Ch 03).
- *Verdict:* redundant. Paragraph 3 (`:1294`) restates the restart and replaceability tests a third time. The last line (`:1296`) is a strong closing.

**§ Questions to bring to design review (`:1298`).**
- *Role:* review questions.
- *Verdict:* good, except Q6 "When is a handoff actually a new task?" (`:1307`), which near-duplicates Ch 18's Q (`05-part-v.md:377`).

**§ Where this leads next (`:1310`).**
- *Role:* outbound transition.
- *Verdict:* incomplete.
  - "Chapter 4 places that boundary inside the complete enterprise reference architecture." Ch 04 never names AgentRuntime; it says "bounded agent workers" (`02-part-ii.md:87`) and lists "AgentStep" (`:93`).
  - There is no mortgage bridge (Ch 01 and Ch 02 have one).
  - It does not say that C03 is the last implemented checkpoint, so readers cannot tell that later case boxes are roadmap scenarios (map §8, S12).

## Sparse or Underdeveloped Content

- **Step status vs. domain assessment.** One or two sentences in § The request is bounded… would reconcile the three disposition vocabularies in Part I (C03-R09).
- **The step-to-gate bridge.** One sentence saying `AgentStepResult.proposed_action` is the Propose gate's output (C03-R05).
- **Template gaps.** There is no § Put the idea to work. Two exercises would test the chapter's own tests (C03-R18). There is no state-owner row. It is optional and Low priority, but every neighbor has one and C01-R05 explains the format.

Nothing else is thin. The chapter's problem is breadth, not depth.

## Missing Conceptual Connections

- **Ch 02 six gates → AgentRuntime, missing "the step result is the proposal"** (`:931`, `:1051–1053`, `:1094`). The design choice and checkpoint say the platform uses the result "as a proposal for the deterministic shell" (`:931`). The body never says which field enters which gate.
- **Ch 01 uncertainty table / Ch 02 DS table → Ch 03 16-row table, missing the axis statement** (`:989`). Something like: "Chapter 1 asked who owns each uncertainty; this table asks the same of each framework feature."
- **Ch 01 Level three termination → Bounds row, missing a recall** (`:1045`).
- **AgentStepRequest → RunManifest, missing "pins are copied from the run manifest (Chapter 4)"** (`:1042`).
- **Framework state → durable execution, missing the forward pointer to Ch 15** (`:1131`).
- **SDK handoff → Ch 11 handoff → Ch 18 child task, missing an explicit term mapping** (`:1156–1166`).
- **AgentRuntime → Ch 04 planes, missing outbound.** Ch 04 must name AgentRuntime in its agent/runtime plane (Ch 04 reviewer).
- **C03 → roadmap, missing the implemented/roadmap boundary** (`:1310–1312`).

## Transition Problems

- **In from Ch 02.** Ch 02 ends on "the execution seam" (`:896–898`). Ch 03 opens with two evidence blockquotes and a supplier box before its design choice, then a "why" H2 that restates it. The seam metaphor returns only at `:925`.
- **`:935–939`.** The checkpoint table and example are followed by "Consider Harborlight mortgage case…", which re-introduces the case after the reader has just seen its code.
- **`:1010` → `:1012`.** The replaceability test is posed and then dropped for 226 lines.
- **`:1065` → `:1067` → … → `:1203`.** Seven consecutive H2s each open a new concern (tools, resources, writes, state, restart, approval, handoff, guardrails, retry) with no signpost that this is a tour of where the boundary meets the rest of the platform. The reader cannot tell the canonical sections (state, restart) from the previews.
- **`:1234` → `:1236`.** The replaceability test follows the upgrade section without reference to the restart test (`:1127`), its natural pair.
- **Out to Ch 04 (`:1312`).** The promise is not kept by Ch 04's opening (`02-part-ii.md:11–18`, no AgentRuntime). Part II's intro (`02-part-ii.md:3`) says "The first Part established that the model is not the system of record", which is a fair recall but does not mention the runtime seam.

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict | Action |
| --- | --- | --- | --- |
| Agent's narrow task (sufficient / insufficient / additional evidence) | `:953`, `:972` | Redundant | Merge into `:953` |
| Ownership tables | `:957–962` (components), `:991–1008` (features), `:1248–1258` (summary) | The first two are complementary. The third is redundant. | Remove § Responsibility map (C03-R10) |
| Replaceability test | `:1010`, `:1236–1242`, `:1294` | Redundant | One statement, paired with the restart test (C03-R11) |
| Restart test | `:1127–1131`, `:1294` | Redundant | Keep `:1127–1131` |
| Request flow | Figure 3-1 reading `:968`, `:1020`, § The complete execution path `:1205–1217` | Redundant | Remove § The complete execution path (C03-R06) |
| "Receipt, not the model, proves the effect" | `:968`, `:1105–1107`, `:1146`, `:1285` | Reinforcement; each adds a framework angle | Keep `:1107`, `:1146`, `:1285` |
| Approval semantics | `:981`, `:1005`, `:1101–1102`, `:1133–1154`, `:1256`, `:1271` | Approval is previewed six times | Keep the `:1005` row, the `:1141–1146` table, and the `:1271` checklist item. Condense the rest. |

## Cross-Chapter Duplication

Assessment of each Ch 03 section that the map (S5) flags, against the downstream text:

| Ch 03 section | Downstream canonical | Verdict | Keep in Ch 03 | Hand off |
| --- | --- | --- | --- | --- |
| § A tool is not the enterprise API (`:1067`) | Ch 21 § What an authorization decision must answer (`06-part-vi.md:401–416`); Ch 22 § Invocation sequence (`:775–792`) | Paths are reinforcement (framework-specific). The six questions are redundant. | Unsafe vs. governed path; "Tool availability is not authorization" | The gateway question list → one sentence citing Ch 21/22 |
| § Reauthorize the exact resource (`:1084`) | Ch 22 Invocation step 2; Ch 20 worked example | Reinforcement (unique example) | All of it, merged with the previous section | Pointer for capability envelope → Ch 21 |
| § The same rule applies to writes (`:1092`) | Ch 02 § One proposal, six gates; Ch 22 § Invocation sequence | Redundant with drift (8 vs. 6 steps) | `:1107` "successful SDK run is not the business record" plus pointers | The 8-step list → "the six gates (Chapter 2)" |
| § Human approval: interruption versus record (`:1133`) | Ch 14 § Approval contract (`04-part-iv.md:900–902`), § Records worth preserving (`:944`) | Field list redundant; event table unique | The event table (`:1141–1146`) and `:1148` | The field list → Ch 14 |
| § Bind approval to the exact proposal (`:1150`) | Ch 14 `:884`, `:898`; AP-06; Ch 22 `06-part-vi.md:673` | Redundant (same scenario) | One sentence | All mechanics → Ch 14 |
| § Three meanings of handoff (`:1156`) | Ch 11 § Routing and handoff are different events (`04-part-iv.md:180–195`), § How Handoff works in practice (`:260–301`); Ch 18 § Topology decision table (`05-part-v.md:69–70`), rules (`:77–78`), Q (`:377`) | Redundant *and* conflicting on what "handoff" means | The framework rule (`:1166`), reframed as a term mapping | Ownership transfer → Ch 11; durable child task → Ch 18 |
| § Guardrails and authorization solve different problems (`:1168`) | Ch 20 § Guardrails help, but they are not the security boundary (`06-part-vi.md:28–45`), layer table (`:73–83`), § Worked example (`:236–256`) | Redundant (same argument and scenario, conflicting layer count) | Two sentences on SDK guardrails as in-loop detectors | The layer stack and scenario → Ch 20 |
| § One retry owner (`:1184`) | Ch 22 § The mechanics that make retries safe (`06-part-vi.md:839–840`), § Choose the response that matches the failure (`:821–834`); AP-04 | Redundant | One paragraph on SDK-local retries | Table and key composition → Ch 22 |
| § The complete execution path (`:1203`) | Figure 3-1 (same chapter); Ch 04 § End-to-end responsibility flow (`02-part-ii.md:46–57`); Ch 15 § Canonical control flow (`04-part-iv.md:1156–1167`) | Redundant | The closing sentence (`:1217`), moved to the Figure 3-1 reading | Lifecycle → Ch 04 (overview), Ch 15 (detail) |
| § Framework state versus business state; § The restart test | Ch 15 § Durable state is more than chat history (`04-part-iv.md:1142–1148`); AP-02 | Reinforcement (Ch 03 = SDK session vs. workflow record; Ch 15 = event history and replay) | All of it | Add a pointer to Ch 15; Ch 15 recalls the restart test in one clause (Ch 15 reviewer) |
| § Framework upgrades are behavioral changes | Ch 04 § RunManifest; Ch 27 release | Reinforcement, but the field set drifts | All of it | Ch 04 adds an adapter/SDK version field (Ch 04 reviewer) |
| § If this fails in production (`:1277`) | Ch 24 § Debugging method; Ch 07 § If this fails (`03-part-iii.md:143`) | Reinforcement (boundary-specific) | All of it | none |
| AgentRuntime / AgentStepRequest/Result (canonical) | Ch 07 § Keep contracts stable while frameworks change (`03-part-iii.md:58`: AgentSpec, **RunContext**); Ch 07 state table (`:27`); Ch 04 "AgentStep" (`02-part-ii.md:93`); Appendix C "AgentStep" (`09-appendices.md:67`) | Ch 07 is redundant with renaming; RunContext is an orphan | Canonical here | Ch 07 replaces RunContext with AgentStepRequest/AgentStepResult and cites Ch 03 (Ch 07 reviewer). Ch 04 and Appendix C use the same names (their reviewers). |
| Step disposition / status | Ch 10 dispositions (`04-part-iv.md:49`: answer, needs_input, delegate, proposed_action, budget_exhausted, failed) | Drift (T12) | Ch 03 defines the step status enum (C03-R09) | Ch 10 references it and adds `budget_exhausted` as its loop-level extension (Ch 10 reviewer) |
| Injected-document scenario (`:1170`) | Ch 01 Tuesday (hook); Ch 20 § Worked example (canonical); Ch 23 | Redundant | none | Ch 20 |

**Map disagreement (minor).** Map S5 lists § A tool is not the enterprise API and § Reauthorize the exact resource for trimming to a two- or three-sentence preview. I recommend keeping their framework-specific core (the façade paths and the `MORT-2026-000999` example), because no later chapter makes the "what may live inside an SDK tool function" point, and the 999 example is the book's clearest exact-resource illustration. Only the gateway question list should go. I also classify § Three meanings of handoff as a **terminology conflict**, not just duplication: Ch 03 says the framework handoff keeps the same activity accountable, while Ch 11 defines handoff as the change of accountable owner.

## Structural Recommendations

Proposed order. The canonical framework-boundary argument stays intact; previews collapse into one signposted section. The estimated result is about 300 lines, down from 413.

1. **Intro.** Merge the evidence blockquotes and `:916–921` into one intro paragraph. Remove the supplier box. Keep THE DESIGN CHOICE. Optionally add a case box: "C02 validates proposals; C03 adds the runtime seam."
2. **§ Start with a concrete scenario.** `:941` ("Return to MORT-2026-000184…"), `:951`, `:953`, the condensed six questions from `:976–985`, the four-row boundary table, the principle, and Figure 3-1 with its reading (absorbing `:1217`). § What the agent actually does is merged here.
3. **§ Why the SDK sits behind AgentRuntime** (moved up, unchanged).
4. **§ The request is bounded before the model sees it.** Adds pointers, the status enum, the step→gate bridge, and `[[EXAMPLE:contracts#step]]` (moved from Ch 01).
5. **§ The adapter builds one bounded runtime** (unchanged).
6. **§ Runtime responsibility versus enterprise responsibility.** The 16-row table, with an axis sentence. Remove `:1010`.
7. **§ Framework state versus business state** (case fix).
8. **§ Two tests for the boundary.** Merges § The restart test and § The replaceability test, with a Ch 15 pointer.
9. **§ Framework upgrades are behavioral changes** (RunManifest table relabeled).
10. **§ Where the framework meets the rest of the platform.** A new H2 replacing seven H2s, with short H3s:
    - *Framework tools are façades* (merged tool and exact-resource sections, minus the question list)
    - *Writes leave the step as proposals* (two sentences plus pointers)
    - *SDK interruption is not approval* (event table plus one sentence pointing to Ch 14)
    - *An SDK handoff is not an ownership handoff* (term mapping)
    - *SDK guardrails detect; gateways enforce* (two sentences pointing to Ch 20)
    - *One retry owner, and it is rarely the SDK* (one paragraph pointing to Ch 22)
11. **§ A sensible place to start.** The C03 checkpoint, moved from `:925–937`.
12. **§ If this fails in production**, then **§ What to verify before production** (✓ format), then **§ Put the idea to work** (new), then **§ Questions to bring to design review**, then **§ Where this leads next** (with mortgage bridge and roadmap note).

Remove § The same rule applies to writes, § Bind approval to the exact proposal, § The complete execution path, § Responsibility map, and § What this chapter established.

## Concrete Recommended Changes

1. **C03-R01 — High — Condense / Remove**
   - **Location:** `01-part-i.md:1133–1154`, § Human approval: interruption versus record and § Bind approval to the exact proposal.
   - **Issue:** the approval record field list and the proposal-hash mechanics duplicate Ch 14 (`04-part-iv.md:884`, `:898`, `:902`, `:944`) with drift.
   - **Why it matters:** the reader learns approval binding twice, with different field lists, and Ch 14 then reads as review.
   - **Change:**
     - Retitle § Human approval… to the H3 "SDK interruption is not approval" under the new § Where the framework meets the rest of the platform.
     - Replace `:1135–1137` with: "An SDK may pause when a protected tool call needs a human response. That interruption is runtime control, not an enterprise approval: the platform records a durable, expiring human action authorization bound to the exact proposal, and revalidates it before commit (Chapter 14)."
     - Keep the event table (`:1141–1146`) and `:1148`.
     - Delete the H2 at `:1150` and `:1152–1154`. Append to `:1148`: "Chapter 14 binds that record to a proposal hash so it cannot be reused for a different document, case, or destination."
     - Use the approval term the synthesizer chooses for T3 in the table's second row (currently "Platform approval").
   - **Related:** Ch 14 keeps the canonical contract (no Ch 14 change needed).

2. **C03-R02 — High — Rewrite / Condense**
   - **Location:** `:1156–1166` § Three meanings of handoff.
   - **Issue:** it pre-teaches Ch 11 and Ch 18, and its "framework handoff … same activity remains accountable" conflicts with Ch 11's definition of handoff as the change of accountable owner (`04-part-iv.md:182`, `:195`) and with Ch 18's rule (`05-part-v.md:78`).
   - **Why it matters:** a core term gets two incompatible meanings within ten chapters.
   - **Change:**
     - Replace the H2 with the H3 "An SDK handoff is not an ownership handoff".
     - Replace the table and `:1158` with: "Frameworks make it easy for one agent to involve another, and the SDK calls one form of this a *handoff*. Inside AgentRuntime, an SDK handoff — or a specialist invoked as a tool — is local control flow: the same step keeps its budget, cancellation boundary, and accountability. When accountability for finishing the work must change, the platform records an ownership handoff that the recipient acknowledges (Chapter 11). When work needs its own waits, retries, deadlines, or trust boundary, the platform creates a durable child task (Chapter 18)."
     - Keep `:1166` as the closing.
   - **Cross-chapter:** Ch 11 owns "handoff" and should add one clause recalling that an SDK handoff is not one (Ch 11 reviewer). Ch 18's "Handoff" rule should match Ch 11.
   - **Related:** C03-R19.

3. **C03-R03 — High — Condense**
   - **Location:** `:1168–1182` § Guardrails and authorization solve different problems.
   - **Issue:** it duplicates Ch 20 § Guardrails help… (`06-part-vi.md:28–45`), retells the injected document, and introduces a seven-layer stack against Ch 20's nine and six.
   - **Why it matters:** this is the second of five tellings, it gives a conflicting layer count, and it pre-empts Ch 20's canonical treatment.
   - **Change:**
     - Replace the H2 with the H3 "SDK guardrails detect; gateways enforce".
     - Replace `:1170–1182` with: "SDK input, output, and tool guardrails are useful early detectors, but they run inside the very loop they protect against and can be fooled. The enforcement that matters sits outside the step — tool eligibility, policy, exact-resource authorization, and effect controls — so a manipulated proposal still cannot become an unauthorized effect. Chapter 20 develops the detector, policy-point, and enforcement-point distinction."
     - Delete the seven-step list.

4. **C03-R04 — High — Condense**
   - **Location:** `:1184–1201` § One retry owner.
   - **Issue:** it duplicates Ch 22 (`06-part-vi.md:821–840`) and AP-04, and omits the framework-specific point.
   - **Why it matters:** the reader gets the failure-class table twice, with ID drift (`RUN-98217`).
   - **Change:**
     - Replace the H2 with the H3 "One retry owner, and it is rarely the SDK".
     - Replace `:1186–1201` with: "Frameworks and model clients retry on their own. If the SDK, the LLM Gateway, the Tool Gateway, and the workflow all retry, a single timeout becomes several attempts — and a timed-out write may already have committed. Configure SDK retries off, or declare them as the single owner for transport failures of reads; mutations are never retried inside the step. Chapter 22 assigns one retry owner per failure class and reconciles unknown outcomes before any retry."
     - Delete the table and the key example (`:1197–1200`). The Ch 22 reviewer owns key derivation.
   - **Related:** C02-R10; § If this fails item 6 (`:1286`) stays.

5. **C03-R05 — High — Remove / Add**
   - **Location:** `:1092–1107` § The same rule applies to writes; `:1051–1053`.
   - **Issue:** an eight-step list re-sequences Ch 02's six gates. The step-result → gate bridge is missing.
   - **Why it matters:** a third gate sequence (with different counts) undermines Ch 02's canonical model, and the reader never learns where AgentRuntime meets the gates.
   - **Change:**
     - Replace the H2 with the H3 "Writes leave the step as proposals".
     - Replace `:1094–1105` with: "If the agent concludes that the second pay statement must be requested, the SDK tool call means only that the model proposes it. The step returns it as `AgentStepResult.proposed_action`, and from there it crosses Chapter 2's six gates outside the framework."
     - Keep `:1107`.
     - In § The request is bounded… after `:1053` add: "A `proposed_action` result is the output of the Propose gate; nothing inside the adapter validates, authorizes, or commits it."
   - **Related:** C02-R03.

6. **C03-R06 — Medium — Remove**
   - **Location:** `:1203–1217` § The complete execution path.
   - **Issue:** a nine-step walkthrough duplicating Figure 3-1, Ch 04 § End-to-end responsibility flow, and Ch 15 § Canonical control flow.
   - **Why it matters:** it is the third end-to-end lifecycle the reader meets, each with a different step count.
   - **Change:**
     - Delete the H2 and list.
     - Append to the Figure 3-1 reading (`:968`): "In the middle of that flow the framework-specific steps are three: AgentRuntime passes the request to the adapter, the SDK runs the local loop against narrow façades, and the adapter maps the outcome to `AgentStepResult`. At every other stage authority narrows or is re-established outside the framework."
     - The full lifecycle is owned by Ch 04 (overview) and Ch 15 (detail).

7. **C03-R07 — Medium — Merge / Condense**
   - **Location:** `:1067–1090` § A tool is not the enterprise API and § Reauthorize the exact resource.
   - **Issue:** two H2s make one argument, and the six gateway questions restate Ch 21's tuple and Ch 22's invocation steps.
   - **Change:**
     - Merge both into the H3 "Framework tools are façades".
     - Keep `:1069–1073`, `:1082`, `:1086–1090`.
     - Replace `:1073` (second sentence) through `:1080` with: "At the gateway, deterministic controls re-establish who is asking, for which tenant, purpose and resource, with which tool version and budget (Chapter 21 § What an authorization decision must answer; Chapter 22 § Invocation sequence)."
     - At `:1088` write "capability envelope (Chapter 21)".

8. **C03-R08 — High — Move**
   - **Location:** `:925–937` (§ Mortgage checkpoint: the runtime seam); `:1012–1033` (§ Why the SDK sits behind AgentRuntime); `:1035–1053`.
   - **Issue:** AgentRuntime and `AgentStepResult` are used before they are defined, and checkpoint code precedes the contract it implements.
   - **Why it matters:** the reader meets the chapter's central term four times before its definition.
   - **Change:**
     - Move § Why the SDK sits behind AgentRuntime to directly after § Start with a concrete scenario, before § Runtime responsibility versus enterprise responsibility.
     - Move the H3 § Mortgage checkpoint: the runtime seam (`:925–937`) into a new "## A sensible place to start" placed before § If this fails in production.
     - Insert `[[EXAMPLE:contracts#step]]` (moved from Ch 01, C01-R01) at the end of § The request is bounded… with the lead-in: "The registered contract below is the minimal subset of these field groups the companion code enforces."
   - **Related:** C01-R01 (registry `book_chapters` update).

9. **C03-R09 — High — Add**
   - **Location:** `:953`, `:972`, `:1051`.
   - **Issue:** the domain dispositions (sufficient / insufficient / additional evidence) are never reconciled with the step status enum (`examples/contracts.py:45`) or with Ch 02's JSON disposition.
   - **Why it matters:** three disposition vocabularies in Part I. Ch 10 then adds a fourth (T12).
   - **Change:**
     - Delete `:972`'s first sentence (it duplicates `:953`).
     - Rewrite `:1051` to: "`AgentStepResult` has a platform-defined status — `completed`, `needs_input`, `proposed_action`, or `failed` — plus a typed payload: an evidence-grounded summary, immutable artifact references, any proposed action, usage, trace references, and a structured error. The domain assessment (sufficient, insufficient, or additional evidence required) travels in the payload; C03, for example, returns `needs_input` with 'A second pay statement is missing.' It is never a vendor-native `RunResult`."
   - **Cross-chapter:** the Ch 10 reviewer should reference this enum and present `budget_exhausted` and `delegate` as loop-level additions.
   - **Related:** C02-R09.

10. **C03-R10 — Medium — Remove**
    - **Location:** `:1244–1260` § Responsibility map.
    - **Issue:** a nine-row copy of the 16-row table.
    - **Change:** delete the H2 and table. Move `:1260` ("Where both layers participate… Shared participation is not shared authority…") to the end of § Runtime responsibility versus enterprise responsibility (after `:1008`).

11. **C03-R11 — Medium — Merge / Remove**
    - **Location:** `:1010`; `:1127–1131` § The restart test; `:1236–1242` § The replaceability test; `:1288–1296` § What this chapter established.
    - **Issue:** the replaceability test is posed twice, and both tests are restated in the summary.
    - **Change:**
      - Delete `:1010`.
      - Create "## Two tests for the boundary" after § Framework state versus business state, containing the restart test (`:1129–1131`) and the replaceability test (`:1238–1242`) as two short paragraphs, with the `:1010` question as the replaceability test's opening sentence.
      - Add at the end: "Chapter 15 makes the restart survivable with durable event history, timers, and signals."
      - Delete § What this chapter established. Move `:1296` ("That is the difference between running an agent and operating an enterprise agentic system.") to the start of § Where this leads next.
    - **Related:** C03-R15.

12. **C03-R12 — Medium — Rewrite**
    - **Location:** `:1044` "capability ceiling"; `:1041` "Agent definition"; `:1104`, `:1194`, `:1199` effect ledger / effect service / effect layer; `:1144` "Platform approval".
    - **Issue:** T6, T8, T24, and T3 drift inside one chapter.
    - **Change:**
      - "capability envelope (Chapter 21)".
      - "AgentSpec version" (T8 canonical).
      - "Effect Service" for the component and "effect ledger" for its store.
      - Use the T3 choice for approval.
      - Add pointers in the field-group table: "Authorized `ContextManifest` (Chapter 6)", "trust labels (Chapter 6)", "cancellation lineage (Chapter 18)".

13. **C03-R13 — Medium — Rewrite**
    - **Location:** `:1223–1232` (RunManifest table).
    - **Issue:** the field set conflicts with Ch 04 § RunManifest. `context_manifest` is per-step, not per-run. The model-route version conflicts (T16).
    - **Change:**
      - Introduce the table with: "The run manifest (Chapter 4) must include the framework-boundary pins below."
      - Remove the `context_manifest` row and add after the table: "Each step's `ContextManifest` is recorded with its `AgentStepRequest`, not in the run manifest."
      - Use the case identifiers the synthesizer standardizes (T16) for `run_id` and `model_route`.
    - **Cross-chapter:** the Ch 04 reviewer adds `"adapter": {"framework": "openai-agents", "version": "0.22.2"}` (or equivalent) to the RunManifest JSON (`02-part-ii.md:176–195`).

14. **C03-R14 — Medium — Condense / Remove**
    - **Location:** `:902–921`; `:939–953`.
    - **Issue:**
      - Two scope blockquotes, a supplier box, and a "why" H2 restate the design choice.
      - The case is re-introduced as new.
      - The workflow list duplicates Ch 01's case row.
    - **Change:**
      - Merge `:904` into `:902` as one blockquote, and change "Chapters 4–7 place that boundary…" to "Chapter 4 places the runtime in the architecture; Chapter 7 packages it for delivery teams."
      - Delete the supplier box (`:906–908`).
      - Delete the H2 at `:914` and keep `:920–921` as the intro's last sentence.
      - Replace `:939–949` with: "Return to `MORT-2026-000184`. The durable workflow owns the business sequence from Chapter 1 — receive, identify missing evidence, verify, calculate, review, authorize effects, reconcile, accept — and calls the agent for one node of it."
      - Keep `:951` and `:953`.
    - **Related:** C01-R06.

15. **C03-R15 — Medium — Add**
    - **Location:** `:1310–1312` § Where this leads next.
    - **Issue:**
      - No mortgage bridge.
      - The fact that C03 is the last implemented checkpoint goes unstated.
      - The Ch 04 promise is unmet because Ch 04 never names AgentRuntime.
    - **Change:** after the existing paragraph (and the line moved by C03-R11), add: "For the mortgage case, C03 is the last checkpoint the companion code implements: one bounded evidence-review step behind a provider-neutral seam, with every protected effect still outside it. From Chapter 4 onward, the case boxes describe the target design the later chapters build toward."
    - **Cross-chapter:** **the Ch 04 reviewer must name AgentRuntime.** Example for `02-part-ii.md:87`: "bounded agent workers (AgentRuntime, Chapter 3)". Ch 04 should also list AgentStepRequest/AgentStepResult instead of "AgentStep" at `:93`.
    - **Related:** C01-R24.

16. **C03-R16 — Medium — Rewrite**
    - **Location:** "Northstar" at `:955`, `:974`, `:1018`, `:1022`, `:1057`, `:1129`, `:1154`, `:1221`, `:1238`, `:1290`, `:1294`.
    - **Issue:** the second name for the system (T1).
    - **Change:** replace with "the Harborlight platform" on first use in the chapter and "the platform" thereafter, following C01-R07. If the synthesizer keeps Northstar, leave these uses as they are.

17. **C03-R17 — Medium — Rewrite**
    - **Location:** `:1094`, `:1118`, `:1152`, `:1199` (employment verification).
    - **Issue:** contradicts the case and the C03 test (T15).
    - **Change:** `:1118` becomes "Application, first pay statement, and purchase agreement available; second pay statement missing". The other three lines become "second pay statement" / `pay_statement`, unless they are already removed by C03-R01, R04, or R05.
    - **Related:** C01-R04, C02-R04.

18. **C03-R18 — Low — Move / Add**
    - **Location:** `:1262–1286`; after `:1286`.
    - **Issue:** template order and format differ from Ch 01/02, and there is no § Put the idea to work.
    - **Change:**
      - Place § If this fails in production before § What to verify before production.
      - Convert the What-to-verify bullets to ✓ items.
      - Add "## Put the idea to work" with:
        1. "Apply the restart test to an existing agent: list every fact that is lost if all workers and SDK sessions are deleted, and name the platform record that should own it."
        2. "Write the `AgentStepRequest` for one node of your workflow and mark each field the platform, not the framework, must supply."
      - Optionally add a state-owner row after Figure 3-1: "AgentRuntime and durable workflow | platform contract to framework adapter | agent step · worker pool | one agent step | AgentStepRequest · AgentStepResult · RunManifest".

19. **C03-R19 — Low — Rewrite**
    - **Location:** `:1307` (Q6).
    - **Issue:** near-duplicates Ch 18's Q (`05-part-v.md:377`).
    - **Change:** **Reconciled (see overall-book-review.md §D-06):** Keep the new Q6 as written. Replace the closing line "Ch 18 keeps its comparison question as canonical": Ch 11's Q4 (C11-R11) is the book's one agent-as-tool / handoff / child-task comparison, and Ch 18 replaces its comparison question with a cancellation question (C18-R05).
      - Question: "When is an SDK handoff not enough?"
      - Answer: "When accountability for finishing must change (record an acknowledged ownership handoff, Chapter 11) or the work needs its own waits, retries, deadlines, or trust boundary (create a durable child task, Chapter 18)."
    - Ch 18 keeps its comparison question as canonical.

20. **C03-R20 — Low — Cross-reference**
    - **Location:** `:1045` (Bounds row) or `:1049`.
    - **Change:** append to `:1049`: "The bounds are where Chapter 1's observation that termination had become 'a property of a text generator' is reversed: the platform, not the model, decides when the step must stop."

21. **C03-R21 — Low — Add**
    - **Location:** `:989`.
    - **Change:** prefix with "Chapter 1 asked which component owns each uncertainty; this table asks the same of each framework feature."

22. **C03-R22 — Low — Rewrite.** *Added in reconciliation (see overall-book-review.md §D-27).*
   - **Location:** `01-part-i.md:1044` (Capabilities row of the AgentStepRequest field-group table).
   - **Issue:** The Ch 08 review asks Ch 03 to show that the step receives resolved Skill digests; no Ch 03 item did.
   - **Change:** Make the Capabilities cell read "Resolved Skill digests (Chapter 8), eligible tool versions, and the capability envelope (Chapter 21)…". Apply it together with C03-R12, which already replaces "capability ceiling".
   - **Related:** C08-R02, C03-R12.
