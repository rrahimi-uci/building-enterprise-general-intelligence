# Chapter 02 — From Model Output to Safe Action: Continuity and Flow Review

Reviewed: `source/parts/01-part-i.md:616–898`, plus the Ch 01 closing (`:607–614`) and the Ch 03 opening (`:900–968`).

## Overall Assessment

This chapter carries the book's most reused mechanism, the six gates (propose → validate → authorize → commit → verify → accept). Its worked example (`:675–726`) is excellent: one JSON proposal, one table of what each gate rejects, and the "stale reasoning" principle (`:721`). The chapter has four problems.

1. **The opening repeats itself.** An intro paragraph, three callout boxes, two bridging sentences, and § Why a valid-looking output is not enough all say the same thing. Then § Six gates before anything changes refers to "the gates" before they are named (`:660`). The list first appears at `:669`.
2. **The gates are never connected to Chapter 01's components.** The reader just learned the control points (Tool Gateway, human approval gate, acceptance gate) and the uncertainty owners (policy engine, effect ledger, acceptance engine). The gate table does not say which component runs which gate. Approval does not appear in the six gates at all, yet Ch 03 inserts it (`:1101`), Ch 15 renames the sequence "propose → preview → approve → commit" (`04-part-iv.md:1165`), and Ch 22 adds "optionally preview/approve" (`06-part-vi.md:697`).
3. **The Tool Use card contradicts the chapter.** It collapses validation, authorization, and approval into one step ("Validate schema, policy, risk, budget, approval, and resource version", `:797`). That undoes the chapter's central distinction (`:706–711`, `:783`).
4. **The general sections are badly placed and sparse.** The ten design principles, a book-wide list, interrupt the gates-to-tools flow. § Deterministic acceptance, which should define acceptance (map: no single home), is one sentence.

The case also drifts. The JSON requests `employment_verification` (`:688–702`), while the case box and the C02 checkpoint prose say "second pay statement" (`:628`, `:834`).

## Intended Reader Mental Model

After Chapter 02 the reader should hold:

- **What:** every model output is a typed proposal. The six gates, together called the **deterministic shell**, stand between a proposal and any effect.
- **Why:** each gate answers a different operational question (well-formed, permitted, executed once, actually landed, obligations met). Collapsing them makes incident response guesswork (`:660`).
- **How:**
  - Validation is not authorization.
  - The expected version blocks stale writes.
  - The shell derives idempotency.
  - Verification can return *unknown*.
  - Acceptance is an executable predicate over authoritative state.
- **When:** whenever a model output can trigger an action.
- **Trade-offs:** more contracts and platform complexity in exchange for safety, replay, and portability (`:890`).
- **Relationships:**
  - Gates map to Ch 01's control points and owners.
  - The distributed-systems primitives back each gate.
  - Ch 14 (approval), Ch 22 (effects), and Ch 13/15 (acceptance) expand individual gates.
- **Practical application:** C02 implements Propose and Validate plus deterministic calculation, and stops before Authorize/Commit.

What, Why, the How of validate/authorize/version, and the trade-offs are delivered. The Relationships and Practical application parts are not: the reader does not learn which gates C02 covers.

## Section-by-Section Flow Review

**Intro paragraph and callouts (`:618–646`).**
- *Role:* chapter framing.
- *Adds:* the gap between "parses cleanly" and "safe to execute" (`:618–624`), which is strong.
- *Verdict:* redundant layering. WHAT BLOCKS THE NEXT STEP (`:632`) restates the intro, and no other chapter uses this box type. The sentence at `:634–636` and the supplier box (`:640`) restate it again for another domain, and "Both cases resolve the same way." (`:642`) bridges to the design choice. That is five framing elements before the first heading.
- *Issues:*
  - The supplier box uses "deterministic shell" before the term is defined.
  - The case box (`:628`) says "second pay statement". The JSON at `:688` says employment verification.

**§ Why a valid-looking output is not enough (`:648`).**
- *Role:* the "why" H2.
- *Adds:* only "This chapter follows one proposal through all six gates" (`:653–656`).
- *Verdict:* redundant. It restates the intro paragraph and the design choice, which is the map's "double why" pattern.

**§ Six gates before anything changes (`:658`).**
- *Role:* explains why the gates are separate, plus the state-owner table.
- *Adds:* `:660` is the best paragraph on why the gates must stay distinct.
- *Verdict:* misplaced. The paragraph argues for distinctions between gates the reader has not seen yet. Placed after the gate table (`:695–702`), it would be a conclusion instead of an abstraction.
- *Issues:*
  - The state-owner row (`:665`) uses ToolManifest and EffectRecord (Ch 22) and ToolIntent (never formally defined; the registered contract is `AgentDecision`/`ToolCall`, `examples/contracts.py:22–32`).
  - The heading wraps only a paragraph and a table.

**§ Structured output is a protocol boundary (`:667`).**
- *Role:* names the six gates.
- *Adds:*
  - Structured output makes a decision parseable, versionable, and testable, but it is not proof.
  - What a minimal proposal carries (`:671`).
  - Figure 2-1.
- *Verdict:* good. This should open the chapter body.
- *Issues:*
  - "Deterministic shell" is only named in the Figure 2-1 caption. The text never says "these six gates are the deterministic shell", although principle 1, the Q&A (`:886`), and Ch 03 all use the term.
  - `:671` says a proposal names "one disposition", but the JSON's `"disposition": "propose_effect"` matches no enum in the registered contracts. Those are `answer | needs_input | invoke_tool | delegate` (`examples/contracts.py:28`) and `completed | needs_input | proposed_action | failed` (`:45`).

**§ One proposal, six gates (`:675`).**
- *Role:* the worked example (canonical).
- *Adds:* the gate table, validation ≠ authorization, and expected version.
- *Verdict:* excellent.
- *Issues:*
  - The JSON (`:688`, `:691`) and the Accept row (`:702`) use employment verification (T15).
  - The Commit row says "via the idempotency key" but does not say who creates it. The proposal has none, and the reader may assume the model supplies one. Ch 22 derives keys from tenant + run + logical effect (`06-part-vi.md:840`).
  - Accept is run-level (it concerns the run's obligations), while the other five gates act on this one proposal. The table presents all six as parallel.
  - There is no Owner column, so nothing connects to Ch 01's control points.
  - Approval is absent. The reader cannot tell where Ch 01's "human approval gate" sits.

**§ Deterministic acceptance (`:728`).**
- *Role:* defines the Accept gate.
- *Adds:* one sentence listing Harborlight's acceptance conditions.
- *Verdict:* sparse for a concept used in Ch 10, 12, 13, 15, 18, AP-07, and Appendix B with no other definition (map: "Scattered, no single home").
- *Issues:*
  - It does not say what evaluates acceptance (the acceptance engine/workflow guard), what the possible outcomes are, or how acceptance differs from Verify.
  - "Human action authorizations cover the exact proposal" is a forward reference to Ch 14 with no pointer.

**§ Scaling the shell (`:732`).**
- *Role:* capacity note.
- *Adds:* queues by workload and risk class; downstream limits set capacity.
- *Verdict:* a reasonable point in the wrong place. Capacity is unrelated to "structured output is a protocol boundary".
- *Issues:* uses risk class (Ch 22 § Risk classes), quotas, and backpressure (Ch 28) without pointers.

**§ Design principles (`:736`).**
- *Role:* the book-wide principles (canonical per map).
- *Adds:* ten principles in three groups.
- *Verdict:* valuable, but it interrupts the chapter's flow (gates → authoritative primitives → tool use) and generalizes before the reader has seen the primitives.
- *Issues:*
  - P2 lists autonomy dimensions without naming them "autonomy". P8 then uses "Autonomy level", which is never defined (map orphan; Ch 01 `:586`, `:603`).
  - P5 "certified" refers to Ch 08. P6 "memory write, artifact publication" refers to Ch 06 and Ch 18.
  - It is never cross-referenced with the front matter's six-principle contract (`00-front-matter.md:96–107`).
  - The BEST PRACTICE box (`:756`) restates the gate sequence and "same service path a human request would take" (already `:700`). Its last sentence ("If a tool can be invoked without passing that gate, the gate is decorative.") is the only new line.

**§ Where distributed systems must remain authoritative (`:758`).**
- *Role:* maps classic distributed-systems primitives to their LLM role.
- *Adds:* fourteen primitives with "If replaced by the LLM" consequences, which is the book's "agent is a distributed system" premise made concrete.
- *Verdict:* reinforcement, on a different axis from Ch 01's uncertainty table and Ch 04's truth table, so keep it. It has no lead-in prose and no link back to the gates it backs.
- *Issues:*
  - The BOUNDARY RULE (`:779`) is a useful summary, so keep it.
  - The COMMON PITFALL (`:783`) re-teaches `:706–711` about 75 lines later. That is mild redundancy; only its example ("an amount nobody approved") is new.

**§ How Tool Use works in practice (`:785`) and its four H3s.**
- *Role:* the scannable pattern card.
- *Adds:* the Tool Gateway pipeline; use / do-not-use; costs; failures; production signals.
- *Verdict:* this is the right home for the Tool Gateway introduction (map: Ch 02 introduces, Ch 22 specifies). Its pattern sentence (`:793`) repeats Ch 01 `:531–534` almost verbatim, so Ch 01 should cut its copy (C01-R10).
- *Issues:*
  - **§ How the pattern works (`:791`):** step 3 conflates validate, authorize, and approve, contradicting the chapter. The five steps do not line up with the six gates: no explicit Authorize, Commit, Verify, or Accept.
  - **§ Where it helps—and what it costs (`:805`):** fine.
  - **§ Where it can fail—and how to contain it (`:812`):** "Logical effect key, intent hash" refers to Ch 22 and is acceptable as a preview.
  - **§ What you need to see in production (`:820`):** "credential lease ID" (Ch 21) appears with no pointer, as does "last-hop credential" (`:793`).

**§ A sensible place to start (`:829`).**
- **§ Mortgage checkpoint: a proposal, not a decision (`:831`):** a good Before/Added/After. "Another pay statement" (`:834`) is consistent with C01 but contradicts the JSON above. The section does not say which gates C02 implements: it validates case version and evidence (Validate), computes LTV deterministically, and emits a read-only command, so it stops before Authorize and Commit. That one sentence would anchor the gates in runnable code.
- `[[EXAMPLE:agent-tool-loop]]` (`:847`) has no heading or lead-in. The next section's "The previous listing shows the model-facing loop" is the only explanation.
- **§ Governed Tool Gateway (`:849`):** good lead-in. The "in-memory ledger" note is correct scoping.

**Template sections (`:859–890`).**
- **§ If this fails in production (`:859`):** three good checks, written as bullets where other chapters use numbered steps (template drift, Low).
- **§ What to verify before production (`:865`):** good.
- **§ Put the idea to work (`:877`):** good. Exercise 2 ("five invariants") fits.
- **§ Questions to bring to design review (`:882`):** Q2 "Explain propose–validate–commit" is the second name for the sequence (T14), and its answer omits verify and accept. The other questions are good.

**§ Where this leads next (`:892`).** Good, with an accurate mortgage bridge ("execution seam"). "Portable across agent frameworks and model providers" slightly overstates Ch 03, which covers framework portability. Model-provider portability is route pinning, with the LLM Gateway in Ch 19.

## Sparse or Underdeveloped Content

- **§ Deterministic acceptance (`:728–730`).** This is the canonical home the book lacks. It needs four short statements (see C02-R05):
  - Acceptance criteria are executable predicates over authoritative state.
  - The acceptance engine (or workflow guard) evaluates them.
  - A run's outcome is accepted, blocked, needs-input, failed, or unknown-effect (the set Ch 04 `02-part-ii.md:56` already uses).
  - Model-judged quality enters only as evidence (Ch 13). Run terminal states are Ch 15's.

  Keep it to one paragraph and a short list.
- **Gate ownership.** One column in the gate table resolves the biggest bridge gap (C02-R03).
- **C02 coverage.** One sentence (C02-R11).

No other expansion is warranted.

## Missing Conceptual Connections

- **Ch 01 control points → six gates, missing "which component runs which gate"** (`:695–702`). Propose: agent step. Validate: Tool Gateway against the registered schema. Authorize: policy engine via the Tool Gateway, plus human approval when policy requires. Commit: domain service through its normal path. Verify: effect ledger and downstream receipt. Accept: workflow/acceptance engine (Ch 01's "acceptance gate").
- **Ch 01 human approval gate → six gates, missing "approval sits inside Authorize and never replaces it"** (`:699–700`). Without this, Ch 03/15/22 each invent their own placement.
- **Ch 01 Wednesday (timeout) → Verify, missing a recall** (`:701`). "A timeout resolves to unknown" is the Wednesday story; a three-word recall ("Chapter 1's Wednesday") links them.
- **Distributed-systems primitives → gates, missing the lead-in** (`:758`). Schema/type system → Validate; policy engine → Authorize; transaction/outbox and idempotency → Commit; effect ledger → Verify; tests/rules engine → Accept.
- **Design principles → front matter contract, missing the cross-reference** (`:738`).
- **Six gates → Ch 03 AgentRuntime, outbound missing.** Ch 03 should say that `AgentStepResult.proposed_action` is what enters Validate (owned by C03-R05).
- **Six gates → later chapters, missing back-references.** No chapter in Parts II–VIII cites "Chapter 2". Ch 04 § End-to-end responsibility flow, Ch 15 § Canonical control flow step 8, Ch 20 `06-part-vi.md:93`, and Ch 22 § Invocation sequence should name "the six gates (Chapter 2)" and say which gate they expand (owners: those chapters' reviewers).

## Transition Problems

- **In from Ch 01.** Ch 01 closes with a precise handoff (`:609–614`). Ch 02 then spends `:618–656` re-opening the same idea five ways, so the strong handoff loses momentum.
- **`:656` → `:658` → `:667`.** The order "here is what we will do" → "why the gates are separate" → "here are the gates" is backward. The reader meets the justification before the thing justified.
- **`:734` → `:736`.** The jump from a capacity note to ten book-wide principles has no bridge.
- **`:775` → `:777–783`.** The DS table ends, and two callouts follow before the Tool Use card, with no prose connecting the DS primitives to tool use.
- **`:847`.** The example marker appears with no transition.
- **Out to Ch 03 (`:892–898`).** Good. Ch 03 then opens with a supplier box and two evidence blockquotes before its own design choice (see chapter-03.md).

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict | Action |
| --- | --- | --- | --- |
| "Output is a proposal; validate…accept outside the model" | `:618–624`, `:632`, `:634–636`, `:640`, `:646`, `:650–656` | Redundant | Keep the intro paragraph and the design choice; remove the rest (C02-R01) |
| Validation ≠ authorization | `:706–711`, COMMON PITFALL `:783` | Mild redundancy; the pitfall is the scannable recall | Trim the pitfall to its new example (C02-R12) |
| Gate sequence restated | `:653`, `:669`, BEST PRACTICE `:756`, Q2 `:887` | Redundant, with naming drift in Q2 | Remove BEST PRACTICE; rename Q2 |
| "Same path a human request takes" | `:700`, `:756` | Redundant | Keep `:700` |
| Tool Gateway pipeline | `:793` and Ch 01 `:531–534` | Cross-chapter redundancy | Ch 02 keeps it (C01-R10 cuts Ch 01) |

## Cross-Chapter Duplication

| Ch 02 content | Other location(s) | Verdict | Owner / action |
| --- | --- | --- | --- |
| Six gates | Ch 03 § The same rule applies to writes (8 steps, `:1096–1105`) and § The complete execution path (9, `:1205–1215`); Ch 04 § End-to-end responsibility flow (8, `02-part-ii.md:50–57`); Ch 15 § Canonical control flow step 8 (`04-part-iv.md:1165`); P-05 "Proposal–authorize–commit"; Ch 20 `06-part-vi.md:93`; Ch 22 Required-analysis row (`:697`) and § Invocation sequence (`:777–792`); Appendix A item 6 | Ch 03 lists are redundant (cut, C03-R05/R06). Ch 04 and Ch 20 are reinforcement but should name the gates. Ch 15 step 8 and P-05 are naming drift. Ch 22 § Invocation sequence is reinforcement (it expands Commit/Verify). | **Ch 02 canonical.** Each later chapter names "the six gates (Chapter 2)" and lists only the gate it expands. |
| Deterministic acceptance | Ch 10 `04-part-iv.md:41`, `:81`; Ch 12 Acceptance Engine row `:487`; Ch 13 § Give evaluation its own independent path; Ch 15 § Terminal correctness; AP-07; Ch 18 "Termination" rule (`05-part-v.md:81`) | Scattered | **Ch 02 owns the definition** (C02-R05). Ch 13 owns evaluating qualitative criteria as evidence. Ch 15 owns run terminal states. The Ch 01 vocabulary row points here (C01-R03). |
| Expected version / stale write | Ch 22 § A reliable protocol… and property table (`06-part-vi.md:669`, `:687`); Ch 18 "Shared state" rule | Reinforcement | Ch 22 canonical; Ch 02 introduces |
| Idempotency on Commit | Ch 22 `06-part-vi.md:773`, `:840` | Reinforcement | Ch 22 owns key derivation; Ch 02 states the shell (not the model) derives it (C02-R10) |
| Verify → unknown | Ch 01 Wednesday; Ch 22 § A reliable protocol…; AP-05 | Reinforcement | Ch 22 canonical |
| Design principles | Front matter § The engineering contract (`00-front-matter.md:96–107`); Closing Perspective | Redundant with drift | **Ch 02 canonical**; the front matter condenses and points here (C01-R23) |
| Where distributed systems must remain authoritative | Ch 01 § Which component should own each uncertainty; Ch 03 16-row table; Ch 04 § Where truth lives | Reinforcement (distinct axis: DS primitives) | Keep; add lead-in (C02-R08) |
| Tool Use card | P-05 (Ch 16); Appendix A item 6; Ch 22 § Give tools explicit contracts… | P-05/Appendix A are the third and fourth descriptions (map S1) | Ch 16 / appendices reviewers |
| `[[EXAMPLE:governed-tool-gateway]]` (in-memory ledger) | `[[EXAMPLE:effect-idempotency]]` and inline `InMemoryEffectLedger` in Ch 22 (`06-part-vi.md:952`); AP-05 code | Ch 02 example is reinforcement (introductory). Ch 22's inline ledger is redundant with drift. | Ch 22 reviewer |
| Risk class in § Scaling the shell | Ch 22 § Risk classes (`06-part-vi.md:714–722`) | Used before definition | Add pointer (C02-R13); Ch 22 or the synthesizer decides on moving risk classes earlier (map S6) |

## Structural Recommendations

Proposed order (same content, about 40 fewer lines):

1. Intro paragraph, the case box, and THE DESIGN CHOICE. Remove WHAT BLOCKS THE NEXT STEP, `:634–636`, the supplier box, and `:642`.
2. **§ Structured output is a protocol boundary.** Names the six gates and defines "deterministic shell", followed by Figure 2-1 and the state-owner table (moved from `:663–665`).
   - § One proposal, six gates: JSON, the gate table with an Owner column, the approval sentence, then `:660` (why the gates are separate), then the two distinctions and the stale-reasoning principle.
   - § Deterministic acceptance, expanded.
3. **§ Where distributed systems must remain authoritative**, with a lead-in mapping primitives to gates, plus the BOUNDARY RULE and a trimmed pitfall.
4. **§ Design principles**, moved here as the generalization. Autonomy is defined in P2, and the BEST PRACTICE box is removed.
5. **§ How Tool Use works in practice**, with steps aligned to the gates. § Scaling the shell becomes its final H3.
6. **§ A sensible place to start.** C02 with gate coverage; an H3 for the model-facing loop; Governed Tool Gateway.
7. Template sections.

Remove the H2s § Why a valid-looking output is not enough and § Six gates before anything changes. Their content is relocated.

## Concrete Recommended Changes

1. **C02-R01 — High — Remove**
   - **Location:** `01-part-i.md:630–642` and `:648–656` (§ Why a valid-looking output is not enough).
   - **Issue:** five framing elements and a "why" H2 restate the intro paragraph.
   - **Why it matters:** the reader reaches the first gate about 40 lines late, and Ch 01's handoff loses force.
   - **Change:**
     - Delete the WHAT BLOCKS THE NEXT STEP box (`:630–632`), `:634–636`, the supplier box (`:638–640`), and `:642`.
     - Delete the H2 at `:648` and `:650–656`.
     - Append to the intro paragraph (after `:624`): "The chapter follows one Harborlight proposal through each gate to show what it rejects."
   - **Related:** C01-R06 (supplier thread retired).

2. **C02-R02 — High — Move / Rewrite**
   - **Location:** `:658–665` § Six gates before anything changes; `:667–673` § Structured output is a protocol boundary.
   - **Issue:** "the gates" are justified before they are named, and "deterministic shell" is never defined in prose.
   - **Why it matters:** the reader cannot follow an argument about distinctions between things not yet introduced, and the shell name used across the book has no definition.
   - **Change:**
     - Delete the H2 at `:658`.
     - Move the paragraph `:660` to directly after the gate table in § One proposal, six gates (after `:702`), opening it with "Each gate rejects something different because…".
     - Move the state-owner table (`:663–665`) to after Figure 2-1 (`:673`). Change its "Core contracts" cell to "ToolCall/AgentDecision (proposal) · ToolManifest (Ch 22) · EffectRecord (Ch 22)", dropping the undefined "ToolIntent".
     - At the end of `:669` add: "Together these six gates are the **deterministic shell** around the model's agentic core."
   - **Related:** C02-R09.

3. **C02-R03 — High — Add**
   - **Location:** `:695–702` (gate table) and `:704`.
   - **Issue:** the gates are not tied to Ch 01's control points or owners, and approval has no place in them.
   - **Why it matters:** this is the bridge from the Ch 01 vocabulary to the mechanism. Without it, Ch 03, 15, and 22 each re-sequence approval differently.
   - **Change:**
     - Add an "Owner" column:
       - Propose → agent step (Chapter 3)
       - Validate → Tool Gateway, against a schema the platform owns
       - Authorize → policy engine via the Tool Gateway
       - Commit → domain service
       - Verify → effect ledger and downstream receipt (Chapter 22)
       - Accept → workflow acceptance engine
     - Add one sentence before "Two distinctions are important here": "When policy requires a person, Authorize also requires a proposal-bound human approval (Chapter 14); the approval never replaces the policy check, and the Tool Gateway reauthorizes after it."
     - Add a clause after the table: "The first five gates act on this proposal; Accept acts on the run as a whole."
   - **Cross-chapter:** Ch 15 step 8 (`04-part-iv.md:1165`) and Ch 22 `06-part-vi.md:697` should adopt this placement and name (their reviewers).

4. **C02-R04 — High — Rewrite**
   - **Location:** `:688`, `:691`, `:702`.
   - **Issue:** employment verification vs. the second pay statement (T15).
   - **Why it matters:** the running case contradicts its own C01 and C03 tests within one chapter.
   - **Change:**
     - `"document_kind": "pay_statement"`.
     - `"uncertainty": "high — the second pay statement is missing"`.
     - Accept row: "Income evidence older than policy allows".
     - The examples/tests using `employment_verification` must change in step (list in C01-R04).
   - **Related:** C01-R04, C03-R17.

5. **C02-R05 — Medium — Rewrite (expand)**
   - **Location:** `:728–730` § Deterministic acceptance.
   - **Issue:** a one-sentence treatment of a concept used in about eight later chapters with no other definition.
   - **Why it matters:** readers meet "acceptance engine", "acceptance criteria", and "AcceptanceDecision" throughout Part IV with no definition.
   - **Change:** **Reconciled (see overall-book-review.md §D-12):** Replace list item (1) with: "The engine records an AcceptanceDecision—accepted, rejected with typed defects, or escalated (Chapter 13). Acceptance is not attempted while an effect is Unknown or required input is missing; the run stays waiting." Items (2) and (3) and the paragraph stand. Do not list run terminal states here (Chapter 15 owns them). Original text: replace with one paragraph and a three-item list.
     - Paragraph: "Acceptance is not the model saying 'done.' **Acceptance criteria** are executable predicates over authoritative state, declared with the workflow; the **acceptance engine** (or a workflow guard) evaluates them and records the outcome."
     - List:
       - (1) The outcomes are accepted, blocked, needs-input, failed, or unknown-effect. An unresolved effect always blocks acceptance.
       - (2) Verify asks whether one effect landed; Accept asks whether every obligation of the run is met.
       - (3) Qualitative checks, such as whether a summary is faithful, enter only as evidence from an independent evaluator (Chapter 13). How a run reaches its terminal state is Chapter 15 § Terminal correctness.
     - Keep the Harborlight example sentence. Change "human action authorizations cover the exact proposal" to add "(Chapter 14)".
   - **Related:** C01-R03 (vocabulary pointer → Ch 2, 13, 15). The Ch 13 and Ch 15 reviewers should recall this definition rather than re-define it.

6. **C02-R06 — Medium — Rewrite**
   - **Location:** `:791–799` § How the pattern works.
   - **Issue:** step 3 merges validate, authorize, and approve, and the five steps do not map to the six gates.
   - **Why it matters:** the card is what readers scan later, and it currently teaches the opposite of `:706–711`.
   - **Change:** replace steps 1–5 with:
     1. Expose only tools eligible for the current run node (eligibility is not authorization).
     2. The model proposes a minimal typed intent with evidence and uncertainty (Propose).
     3. Validate the schema and tool version (Validate).
     4. Authorize the subject, action, resource, and version, with proposal-bound approval when policy requires it (Authorize).
     5. Commit once through the domain service with the shell-derived idempotency key, and record the receipt or *unknown* (Commit, Verify).
     6. Return a sanitized result or artifact reference. The workflow evaluates acceptance (Accept).

   Change `:793` "mints a last-hop credential" to "mints a last-hop credential (Chapter 21)".

7. **C02-R07 — Medium — Move / Rewrite**
   - **Location:** `:736–756` § Design principles.
   - **Issue:** it interrupts the gates → primitives → tools flow, "autonomy level" is undefined, and it is not linked to the front-matter contract.
   - **Why it matters:** the reader generalizes before seeing the primitives, and the autonomy orphan propagates to Ch 01 and Ch 27.
   - **Change:**
     - Move the H2 and list to directly after § Where distributed systems must remain authoritative (after `:783`).
     - Reword P2: "**Least agency.** A run's *autonomy* is the set of tools, data, time, tokens, fan-out, delegation, and mutation scope it is granted; grant the minimum the task needs."
     - Reword P8: "**Evidence before autonomy.** Widen any of those grants only after…".
     - Add after `:741`: "The front matter's engineering contract states the same commitments in operating terms."
     - Delete the BEST PRACTICE box (`:754–756`) and move its last sentence to the end of the Commit discussion in § One proposal, six gates.
   - **Related:** C01-R12, C01-R23.

8. **C02-R08 — Medium — Add**
   - **Location:** `:758` § Where distributed systems must remain authoritative (no lead-in).
   - **Issue:** the table is unconnected to the gates.
   - **Why it matters:** it makes the "agent is a distributed system" premise concrete for the gates.
   - **Change:** add a lead-in of up to two sentences before the table: "Each gate is backed by a primitive distributed systems already trust: schemas validate, the policy engine authorizes, transactions, the outbox and idempotency commit, the effect ledger verifies, and tests and rules engines accept. The table lists where each primitive must stay authoritative and what the model may contribute."

9. **C02-R09 — Medium — Rewrite**
   - **Location:** `:685`; `:671`.
   - **Issue:** `"disposition": "propose_effect"` matches neither registered enum (`examples/contracts.py:28`, `:45`).
   - **Why it matters:** the reader sees three disposition vocabularies across Ch 02, Ch 03, and the code (T12).
   - **Change:** **Reconciled (see overall-book-review.md §D-13):** Use `"disposition": "proposed_action"`: the Ch 02 proposal is a mutation, and `invoke_tool` is reserved for read-only calls inside the step. `proposed_action` is added to `AgentDecision.disposition` once, by C10-R02. Add: "A `proposed_action` is a request; nothing runs until the shell commits it." Drop the `propose_tool` alternative. Original text, superseded: use the registered `AgentDecision` value `"invoke_tool"` and add one sentence: "Despite its name, `invoke_tool` is a request; nothing runs until the shell commits it." If the author prefers a proposal-flavored name, rename the enum value in `examples/contracts.py` and its tests to `propose_tool` and use it here and in Ch 03.
   - **Related:** C03-R09 (Ch 03 reconciles step status vs. domain assessment).

10. **C02-R10 — Medium — Rewrite**
    - **Location:** `:700` (Commit row) and `:671`.
    - **Issue:** the source of the idempotency key is unstated, and the proposal has no key.
    - **Why it matters:** readers may conclude the model generates idempotency keys, which contradicts the chapter's own principle 1.
    - **Change:**
      - Commit row: "A duplicate arriving from a retry, caught by the logical effect key the shell derives from run, action, and resource (Chapter 22)".
      - Add to `:671`: "It does not carry credentials, policy truth, an idempotency key, or an instruction to bypass a failing control."
    - **Related:** C03-R04 (Ch 03 drops its key-composition example).

11. **C02-R11 — Medium — Add**
    - **Location:** `:833–838` § Mortgage checkpoint: a proposal, not a decision.
    - **Issue:** it does not say which gates C02 implements.
    - **Why it matters:** this ties the abstract gates to runnable code.
    - **Change:** append to `:838`: "In gate terms, C02 implements Propose and Validate, plus a deterministic calculation; it stops before Authorize and Commit, which is why its workflow command is read-only."

12. **C02-R12 — Low — Condense**
    - **Location:** `:781–783` COMMON PITFALL.
    - **Change:** reduce to: "**COMMON PITFALL** Treating schema validity as correctness. A response that parses cleanly can still name an amount nobody approved. Run validation and authorization as separate checks."

13. **C02-R13 — Low — Move / Cross-reference**
    - **Location:** `:732–734` § Scaling the shell.
    - **Change:** **Reconciled (see overall-book-review.md §D-01):** Move as stated, but write the first use as a gloss, not a bare pointer: "risk class (R0 pure transform through R4 irreversible or privileged action; Chapter 22 § Risk classes)". Keep the quotas and backpressure pointer (Chapter 28). This is the Ch 02 half of C22-R05; the class table stays in Ch 22. Original text, superseded where it conflicts: move to become the last H3 of § How Tool Use works in practice (after `:827`). Add pointers: "risk class (Chapter 22 § Risk classes)" and "quotas and backpressure (Chapter 28)".

14. **C02-R14 — Low — Cross-reference**
    - **Location:** `:825`.
    - **Change:** "credential lease ID (Chapter 21)".

15. **C02-R15 — Low — Add**
    - **Location:** `:847` `[[EXAMPLE:agent-tool-loop]]`.
    - **Change:** insert before it the heading "### The model-facing loop" and one sentence: "The loop below gives the model one typed read tool; its output is a proposal the next listing's gateway receives."

16. **C02-R16 — Low — Rewrite**
    - **Location:** `:887` (Q2).
    - **Change:**
      - Question: "Walk one proposal through the six gates."
      - Answer: "The model proposes a typed intent; the shell validates schema and version, authorizes subject, action and resource (with proposal-bound approval where required), commits once through the domain service, verifies the receipt or records unknown, and accepts the run only when its criteria hold."

17. **C02-R17 — Low — Rewrite**
    - **Location:** `:861–863` (If this fails).
    - **Change:** convert the bullets to a numbered list, matching the other chapters.

18. **C02-R18 — Low — Rewrite**
    - **Location:** `:894`.
    - **Change:** "With tools bounded, Chapter 3 defines the runtime contract that keeps applications portable across agent frameworks and pins the model route each step uses."

19. **C02-R19 — Low — Rewrite (card policy).** *Added in reconciliation (see overall-book-review.md §D-04).*
   - **Location:** `01-part-i.md:785–799`, § How Tool Use works in practice.
   - **Issue:** The book-wide card policy (C10-R04) covers every "How X works in practice" card, but this file had no reciprocal item.
   - **Change:** Retitle the H2 "Tool Use at a glance". Delete THE ENGINEERING PROBLEM box (`:789`) and the card's lead sentence. Keep the six gate-aligned steps from C02-R06: here they are the only ordered tool-use sequence, so they stay in the card. Keep the Use when, costs, failure, and signals blocks. Appendix A's P-05 card points here (C16-R10).
   - **Related:** C02-R06, C10-R04, C16-R10.
