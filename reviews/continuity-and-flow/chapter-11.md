# Chapter 11 — Route the Work Without Losing Ownership: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:162–374`. Context read: Ch 10 close (`:158–160`), Ch 12 opening (`:376–416`), Ch 03 § Three meanings of handoff (`01-part-i.md:1156–1166`) and its Q (`:1307`), Ch 18 (`05-part-v.md:9–150`, `:377`), Ch 19 § Two protocols, two responsibilities and § Filter for policy before optimizing cost or quality (`05-part-v.md:416–430`, `:583–589`), Ch 16 P-06, Ch 17 AP-08/AP-12, Appendix A, Appendix H "Handoff" (`09-appendices.md:213`), the `routing-handoff` example, and `assets/diagrams/src/pattern-routing.gv`.

## Overall Assessment

The chapter's thesis is valuable and stated well in § Routing and handoff are different events (`:182`): routing answers "who is best placed", handoff answers "who is now accountable". The chapter has four significant problems.

1. **"Handoff" means two different things across Ch 03, Ch 11, Ch 18, and the example.**
   - Ch 03's table (`01-part-i.md:1163`) defines a framework "conversational transfer" in which "control changes locally but the same activity remains accountable".
   - Ch 11 defines handoff as a change of the accountable owner, with recipient acknowledgment (`:182`, `:195`, `:273–274`).
   - Ch 18's rule and API (`05-part-v.md:78`, `:104`) transfer the owner "atomically" with no acknowledgment step.
   - Ch 18's design-review answer (`:377`) reverts to Ch 03's "conversational control transfer".
   - The chapter's own example, `routing-handoff`, uses an OpenAI Agents SDK handoff. That is Ch 03's conversational transfer, with no ownership record and no acknowledgment. Yet its docstring calls it "an authority transfer", which Ch 03 explicitly forbids ("A local handoff must not silently transfer authority").

   The reader cannot tell whether the SDK primitive they will actually use is a Ch 11 handoff.
2. **Figure 11-1 omits the chapter's key step.** The prose says the eligible set is assembled *before* classification (`:193`, `:226`, checklist `:347`). The diagram (`pattern-routing.gv`) shows Request → Classify → Specialist → Policy, with no eligibility stage.
3. **Two pattern cards, an anti-pattern list, and a design-review question all restate the same controls.** The § Anti-patterns bullets (`:203–206`) duplicate the failure tables (`:247–249`, `:291–293`). Routing Q4 (`:369`) duplicates the routing signals list (`:253–258`).
4. **Implementation is thin and in the wrong form.** There is no implementation section. The handoff protocol has no record definition here (Ch 18's `OwnershipTransfer` has different fields). The inline "Deterministic route validation" excerpt is not registered under `examples/`: `Route` lacks `@dataclass`, every import is unused (all five import lines, seven names, including the `dataclass` that is imported but never applied), and it uses an integer `risk`, a third risk representation alongside "R1" (Ch 12) and 0–4 (`plan_compilation.py`). [verified: corrected — "five imports" undercounted; `:314–319` import seven names and none is used]

"Model routing" (`:234`) also collides with Ch 19's model routing. And "run envelope" (`:193`) is one of five names for the capability envelope (map T6).

## Intended Reader Mental Model

- **Before:** Ch 10 says a ReAct step may return `delegate`. Ch 03 § Three meanings of handoff gives three ownership models. Ch 08 says discovery is not permission. Ch 02 says proposals are validated deterministically.
- **After:**
  - (a) Routing chooses an implementation from a pre-filtered eligible set; a route grants no authority.
  - (b) Confidence is calibrated, and low confidence has a deterministic fallback.
  - (c) A handoff is an explicit, acknowledged ownership transfer; until acknowledgment the old owner stays accountable.
  - (d) Agent-as-tool, handoff, and durable child task are three choices with different ownership.
- **Missing pieces:**
  - (c) conflicts with what the SDK example does.
  - (d) is assumed from Ch 03 and appears here only in one table cell (`:278`).
  - The reader is not told where the handoff's durable mechanics live (Ch 18 Ownership Service, `tasks/{id}:handoff`).

## Section-by-Section Flow Review

**WHERE THE MORTGAGE CASE STANDS / THE DESIGN CHOICE (`:164–170`).** Good. The box asks exactly the chapter's question: who owns cancellation, deadlines, and the final response. There is no evidence-context blockquote; acceptable.

**§ Why choosing a worker is different from handing off responsibility (`:172`).**
- *Role:* intro.
- *Verdict:* first of two framing H2s. It previews `:182` almost line for line ("a handoff from becoming a message that nobody owns" ≈ "work disappearing into a queue"). Redundant opening.

**§ Routing and handoff are different events (`:180`).**
- *Role:* thesis.
- *Adds:* the two questions and the "until acknowledged, the coordinator owns it" rule.
- *Verdict:* the best paragraph in the chapter.
- *Issues:*
  - It does not tell the reader that Ch 03 already split "handoff" three ways, or which of those three Ch 11 means.
  - The state-owner table (`:185–187`) names `RouteDecision · Handoff` while Ch 04/20 use `RoutingDecision` and Ch 18 uses `OwnershipTransfer`.

**§ A routing decision cannot grant permission (`:189`).**
- *Role:* mechanism for routing and for handoff.
- *Adds:* Figure 11-1, the eligible-set inputs, "a route cannot grant a capability absent from the run envelope", and the handoff record fields (`:195`).
- *Verdict:* the content is right, but the heading covers only the first paragraph. The second paragraph (`:195`) is the chapter's only prose description of the handoff record, and it sits under a routing heading.
- *Issues:*
  - The figure contradicts the eligibility-first order.
  - "run envelope" (T6) and "child capability envelope" / "cancellation lineage" are used here with no pointer to Ch 18 or Ch 21 (map §4 row 32). Ch 11 is not the first use, though: "capability envelope" already appears in Ch 01 (`01-part-i.md:404`) and Ch 03 (`:1088`), and "cancellation lineage" in Ch 03's bounds table (`:1045`); Ch 21 defines the envelope (`06-part-vi.md:424`), and "cancellation lineage" is never defined anywhere. [verified: softened — the terms predate Ch 11; the missing pointer stands]
  - There is no link to Ch 08 § Discovery is not permission, which is the same principle.

**§§ Confidence and fallback (`:197`).**
- *Role:* low-confidence behavior.
- *Adds:* calibration on a versioned dataset; clarify / safe default / human triage; for privileged routes, both eligibility and exact authorization.
- *Verdict:* good and specific.
- *Issues:* "human triage" (already named at `:193` in the router's target list, and here as the fallback) is the first Part IV appearance of a human queue, which is a natural forward pointer to Ch 14 that is not taken. [verified: corrected — the first occurrence is `:193`, not `:199`]

**§§ Anti-patterns (`:201`).**
- *Role:* a local anti-pattern list.
- *Adds:* persona routing (unique), handoff by chat (≈ AP-08), privilege through selection (≈ AP-12/AP-03), no fallback.
- *Verdict:* three of the four bullets repeat the failure tables below.
- *Issues:* it is the only in-chapter anti-pattern list in Ch 10–13, which is inconsistent with the template. "Persona routing" is the only unique item.

**§ What the evidence lets us conclude (`:208`).**
- *Verdict:* generic EVIDENCE BOUNDARY box.
- *Issues:*
  - R29 (OpenAI Agents SDK; scope covers handoffs) supports no sentence; the chapter never mentions the SDK primitive in prose.
  - R07 (A2A spec) supports no claim here; A2A ownership transfer is Ch 19.

**§ How Routing works in practice (`:216`) and H3s (`:222`, `:236`, `:243`, `:251`).**
- *THE ENGINEERING PROBLEM box (`:220`):* lists "models" among routing targets. Model selection is the LLM Gateway's job (Ch 19 § Filter for policy before optimizing cost or quality). This is scope creep.
- *How the pattern works:* the five steps are the only ordered routing procedure and belong in the mechanism section. Step 5 ("Measure outcome by route and slice") is new and good.
- *Use when / Do not use when (`:234`):* "Avoid model routing" means "avoid a learned router", but readers will read it as Ch 19's model routing.
- *Costs:* useful; it is the chapter's only routing trade-off.
- *Failure table:* rows 1 and 3 duplicate § Anti-patterns. Row 2 (route drift → confusion-matrix monitoring) is unique.
- *Signals:* useful, but duplicated by Q4 (`:369`).
- *Verdict:* keep as a compact at-a-glance block; move the steps up.

**§ How Handoff works in practice (`:260`) and H3s (`:266`, `:280`, `:287`, `:295`).**
- *THE ENGINEERING PROBLEM box (`:264`):* "become the current interaction or task owner rather than merely provide an answer" is the agent-as-tool contrast, and it is good. It is the only place the chapter frames the distinction.
- *How the pattern works (`:266–274`):* this is the canonical handoff protocol of the book (persist → validate → acknowledge/reject → atomic owner change → event). It is better than anything in Ch 18 and is buried in a card.
- *Use when / Do not use when (`:278`):* the only place the three-way choice (agent-as-tool / handoff / durable child task) appears in Ch 11. It is compressed into one cell.
- *Costs, failure, signals:* good and specific. "Typed artifact and obligation references instead of transcript copying" is unique.
- *Verdict:* this card does real work, because its step list is the protocol. The step list should become prose under its own heading.

**§ A sensible place to start (`:304`) / §§ Deterministic route validation (`:309`).**
- *Verdict:* this is where the conflict is most visible.
  - `[[EXAMPLE:routing-handoff]]` shows an SDK triage agent with `handoffs=[…]`. That is routing implemented *as* a framework handoff, the conflation the chapter warns against. It has no ownership record, acknowledgment, or authority narrowing.
  - The inline excerpt shows envelope checking but not eligibility-before-classification or fallback. It is inline code, against the AGENTS.md rule, and has defects (no `@dataclass`, unused imports `hashlib`, `json`, `dataclass`, `Awaitable`, `Callable`, `Protocol`, `AgentDecision`; integer risk). [verified: corrected — `dataclass` added to the unused list]
- *Issues:* the empty H2 wrapper.

**§ If this fails in production (`:339`).** Steps 1–2 are good. Step 3 ("Verify ownership and cancellation after a handoff") is vague: verify what? It should say "check that the old owner remained accountable until the recipient's acknowledgment was recorded".

**§ What to verify before production (`:345`).** Good. Item 4 says ownership, state, authority, deadlines, and cancellation "transfer atomically", which omits the acknowledgment precondition that is the chapter's distinctive rule.

**§ Put the idea to work (`:357`).** Good. Exercise 2 ("transfers a task without broadening authority") tests the right invariant.

**§ Questions to bring to design review (`:362`).** Q1 and Q2 are good. Q4 restates the routing signals list. Q5 (static router) adds a good "when not". There is no question about agent-as-tool versus handoff versus child task, although Ch 03 (`01-part-i.md:1307`) and Ch 18 (`05-part-v.md:377`) both ask one. The question belongs here.

**§ Where this leads next (`:372`).** "Routing selects among known capabilities; Chapter 12 addresses tasks whose decomposition must itself be proposed and validated." Good. It mentions only routing, not handoff, but that is acceptable.

## Sparse or Underdeveloped Content

- **The three ownership choices.** The chapter's distinctive claim depends on contrasting agent-as-tool, handoff, and durable child task. Today that contrast is one table cell (`:278`) plus Ch 03's table. Bring the Ch 03 table here (C11-R02), not new prose.
- **Handoff record.** `:195` lists fields, but there is no record or state set. One short line is enough: proposed → acknowledged | rejected | expired, and on acknowledgment the owner pointer changes. Defer the full record and API to Ch 18 by cross-reference.
- **Calibration.** "Calibrated on a versioned domain dataset" (`:199`) is the right depth. Point to Ch 25 for dataset governance; do not expand.

## Missing Conceptual Connections

- **Ch 10 `delegate` disposition → Ch 11 routing, missing "a `delegate` decision is a routing request the controller validates."** Location: `:182` or `:193`.
- **Ch 08 discovery ≠ permission → Ch 11 "a route cannot grant a capability," missing "the eligible route set is the same deterministic resolution as Skill resolution."** Location: `:193`.
- **Ch 03 three meanings of handoff → Ch 11 handoff, missing "Ch 11's handoff is the accountable kind; a framework handoff becomes one only when the platform records it and the recipient acknowledges."** Location: `:182`/`:195`. This is the central gap.
- **Ch 11 handoff protocol → Ch 18 Ownership Service and `tasks/{id}:handoff` / `:accept` APIs, missing a forward pointer.** Location: end of the handoff section.
- **Ch 11 "child capability envelope" → Ch 21, missing a forward pointer.** Location: `:195`.
- **Ch 11 eligibility-first routing → Ch 19 policy-first model routing, missing "the same rule applies to choosing a model; that is the LLM Gateway's job."** Location: `:220`/`:234`. **Ch 19 owner:** add the reverse pointer at `05-part-v.md:587`.
- **Ch 11 "human triage" → Ch 14, missing a forward pointer.** Location: `:199`.
- **Ch 11 handoff-by-chat → AP-08; privilege through selection → AP-12, missing card IDs.** Location: `:203–206`.

## Transition Problems

- **In (Ch 10 → Ch 11):** Ch 10's closing promises "routing and handoff when known paths or specialists should own the work". Ch 11 opens without connecting to `delegate`. Add the bridge (C11-R08).
- **Within:**
  - The double framing opening (`:172`/`:180`).
  - The handoff record paragraph (`:195`) sits under a routing heading.
  - Two cards in a row, then a code section that shows something different from either card.
- **Out (Ch 11 → Ch 12):** sound. Optionally add: "when no stable route exists and the work must be decomposed, Chapter 12 …". Ch 12's last scalability bullet (`:540`, "use deterministic routing for common cases; invoke the planner only at entry…") is the real link back to Ch 11, and Ch 12 should promote it (see C12-R07).

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict |
| --- | --- | --- |
| Routing ≠ handoff | `:172–178`; `:182`; `:195`; card `:264`; checklist `:351`; Q1 `:366` | `:182` is canonical. `:172` is redundant. The others are acceptable. |
| Eligibility before classification | `:193`; card `:224`, `:226`; failure row `:249`; checklist `:347`; Q2 `:367`; If-fails `:341` | `:193` is canonical. The others are acceptable reuse, but the figure contradicts them. |
| Low confidence → clarify/default/human | `:199`; anti-pattern "No fallback" `:206`; failure row `:247`; Q3 `:368` | Merge the anti-pattern bullet into the table. |
| Privilege via selection | `:193`, `:199`; anti-pattern `:205`; failure row `:249`; excerpt `:335` | Merge the anti-pattern bullet into the table. |
| Handoff by chat / orphaned task | anti-pattern `:204`; failure row `:291` | Merge. |
| Routing telemetry | signals `:253–258`; Q4 `:369` | Q4 is redundant. Replace it with the three-way ownership question. |

## Cross-Chapter Duplication

| Concept | Here | Elsewhere | Verdict |
| --- | --- | --- | --- |
| Three meanings of handoff | `:278` (one cell) | Ch 03 § Three meanings of handoff (`01-part-i.md:1156`), full table; Ch 03 Q (`:1307`); Ch 18 Q (`05-part-v.md:377`) | **Redundancy, and semantic conflict.** Ch 03 calls a framework handoff a transfer in which accountability stays with the activity. Ch 11 calls handoff an accountability transfer. Canonical home: **Ch 11** (agrees with map §3 and S5). **Requires Ch 03 owner:** reduce Ch 03's section to a two-sentence preview ("framework delegation structures reasoning; platform delegation transfers operational ownership; Chapter 11 distinguishes agent-as-tool, handoff, and durable child task") and delete the Ch 03 Q at `:1307` or point it to Ch 11. |
| Handoff mechanics | `:266–274` protocol; `:195` fields | Ch 18 § Recommended orchestration rules "Handoff" (`05-part-v.md:78`); topology row "Handoff" (`:70`); Ownership Service (`:93`); `tasks/{id}:handoff` (`:104`); `OwnershipTransfer` (`:138`) | **Reinforcement with drift.** Ch 18 implements it, but its `:handoff` API and rule omit acknowledgment, and its record fields differ (no obligations, deadline, or acknowledgment state). **Requires Ch 18 owner:** (a) make `:handoff` create a pending transfer that the recipient commits via `:accept`; (b) align `OwnershipTransfer` with Ch 11's fields plus acknowledgment state; (c) replace the orchestration-rule bullet with a pointer to Ch 11; (d) change Q `:377`'s "conversational control transfer" to "acknowledged ownership transfer (Chapter 11)". |
| Router component | Routing card | Ch 18 Router row (`05-part-v.md:94`); topology "Router + specialists" (`:68`) | **Reinforcement.** Ch 18 places the router in a topology. A pointer from Ch 18 to Ch 11 is enough (Ch 18 owner). |
| Eligibility-first selection | `:193` | Ch 19 § Filter for policy before optimizing cost or quality (`05-part-v.md:587`) | **Reinforcement:** the same principle applied to a different subject (work versus model). Cross-reference both ways; do not merge. |
| Ownership transfer across protocol boundaries | — | Ch 19 § Two protocols, two responsibilities (A2A "Transfers to the peer") and § Ownership and failure rules | **Reinforcement.** Ch 19 is the federated case of Ch 11's handoff. Ch 19 should cite Ch 11 (Ch 19 owner). Ch 11 should not mention A2A beyond a pointer (and drop R07). |
| Handoff by chat | `:204` | AP-08 (`04-part-iv.md:1821`); P-06 (`:1427`) | **Reinforcement.** Point to AP-08. **Requires Ch 16/17 owner:** P-06 should cite Ch 11 for the ownership-transfer protocol (P-06 currently names no chapter at all; its "TaskEnvelope, one owner … deterministic join" design is Ch 18's). [verified: corrected — P-06 does not cite Ch 18 either] |
| Privilege through selection / catalog exposure | `:205` | AP-12 (`:1691`); Ch 08 § Discovery is not permission | **Reinforcement.** Point to AP-12 and Ch 08. |
| Pattern catalog coverage | Routing and Handoff cards | Ch 16 has no routing or handoff P-card; Appendix A has no routing row (map §8) | **Gap, not duplication.** **Requires Ch 16/17 owner:** overall-book-review.md §D-04 resolves this: no new P-card; routing and handoff get an obligation-table row (C16-R10), and the chapter cards retitled "at a glance" are the canonical summaries. Appendix A should gain a routing/handoff row pointing to Ch 11 and AP-08/AP-12. [verified: the two options offered here are superseded by D-04] |
| Glossary | — | Appendix H "Handoff: Explicit transfer of interaction or task ownership" (`09-appendices.md:213`) | Consistent with Ch 11; keep. |

## Structural Recommendations

1. **Re-sequence the chapter around its thesis:** routing (eligibility → classify → validate → fallback), then a separate § Handoff transfers accountability section containing the Ch 03 three-way table (moved here), the protocol steps (moved from the card), and the record fields (moved from `:195`), then the two at-a-glance cards, then code.
2. **Apply the shared card policy** (C10-R04): delete both THE ENGINEERING PROBLEM boxes and lead sentences, move the steps into prose, and keep the rest as "Routing at a glance" and "Handoff at a glance". Keep both cards, because routing and handoff are different patterns and the chapter says so.
3. **Fold § Anti-patterns into the failure tables.** Keep "persona routing" as a new routing failure row.
4. **Make the code match the claims.** One registered example should demonstrate eligibility → model proposal → validation → fallback, and one should demonstrate the acknowledgment protocol, or the current SDK example should be described honestly as the framework mechanism that the platform wraps.

## Concrete Recommended Changes

**C11-R01 — Priority: Critical — Action: Rewrite**
- **Location:** `04-part-iv.md:182` (§ Routing and handoff are different events) and `:195`.
- **Issue:** "handoff" conflicts with Ch 03's "conversational transfer" (accountability stays) and with the SDK primitive the example uses.
- **Why it matters:** the reader cannot tell whether a framework handoff satisfies Ch 11's rule. That is the exact failure the chapter is meant to prevent.
- **Change:** after the first sentence of `:182`, add:

  > "Agent frameworks also use the word handoff for passing a conversation to another agent inside one run (Chapter 3). That framework handoff moves control, not accountability. It becomes a handoff in this chapter's sense only when the platform records the transfer and the recipient acknowledges it."

  Keep the rest of `:182`.
- **Related:** C11-R02; Ch 03 (requires Ch 03 owner); C11-R06 (the example).

**C11-R02 — Priority: High — Action: Move (requires Ch 03 owner)**
- **Location:** source `01-part-i.md:1156–1166` (§ Three meanings of handoff); destination `04-part-iv.md`, a new H2 "Handoff transfers accountability" inserted after § Confidence and fallback (before § Anti-patterns).
- **Issue:** the three-way ownership comparison lives in Ch 03 and appears in Ch 11 only as one cell (`:278`).
- **Why it matters:** the "when" of handoff (versus agent-as-tool and child task) is the decision the reader must make, and Ch 11 is its canonical home (map §3).
- **Change:**
  - Move the Ch 03 table into the new section and relabel row 2 "Framework handoff (control only)".
  - Add a row "Accountable handoff (this chapter)", with correct abstraction "Recorded, acknowledged ownership transfer".
  - Keep row 3 "Durable delegation → TaskEnvelope and child workflow (Chapter 18)".
  - Move `:195` (the record fields) into this section, after the table.
  - Leave Ch 03 a two-sentence preview with a pointer to Ch 11 (Ch 03 owner).
- **Related:** C11-R01, C11-R03.

**C11-R03 — Priority: High — Action: Move**
- **Location:** `04-part-iv.md:266–274`, § How Handoff works in practice → § How the pattern works.
- **Issue:** the book's canonical handoff protocol is inside a card.
- **Change:**
  - Move the definition sentence and the five steps into the new § Handoff transfers accountability, after the record fields.
  - Add one sentence: "A transfer is proposed, then acknowledged, rejected, or expired; only acknowledgment changes the owner."
  - End the section with: "Chapter 18 implements this protocol as the Ownership Service and its `tasks/{id}:handoff` and `:accept` operations; Chapter 21 explains how the child capability envelope is derived."
  - Delete the card's THE ENGINEERING PROBLEM box but keep its contrast sentence ("become the owner rather than merely provide an answer") as the section's first line.
- **Related:** Ch 18 alignment (requires Ch 18 owner, see Cross-Chapter Duplication).

**C11-R04 — Priority: High — Action: Rewrite (diagram)**
- **Location:** `assets/diagrams/src/pattern-routing.gv`; Figure 11-1 at `04-part-iv.md:191`.
- **Issue:** the figure omits eligibility-before-classification and puts "risk" in the classifier.
- **Why it matters:** the figure teaches the opposite order from the text and checklist.
- **Change:**
  - Add a node "Eligible set — purpose · authority · region · health · release" between `req` and `cls`.
  - Relabel `cls` to "Classify — intent · confidence".
  - Keep the policy node after selection, labeled "Exact authorization — may this subject invoke it?".
  - Run `make diagrams`. Update the caption in `config/diagrams.json` if its alt text describes the old flow.
- **Related:** `:193`, `:347`.

**C11-R05 — Priority: Medium — Action: Condense / Move**
- **Location:** `04-part-iv.md:216–258`, § How Routing works in practice.
- **Issue:** the card restates the prose.
- **Change:**
  - Delete the THE ENGINEERING PROBLEM box (`:218–220`).
  - Move the five steps (`:226–230`) into § A routing decision cannot grant permission, after `:193`, introduced by "In order:".
  - Retitle the H2 "Routing at a glance".
  - In the Do not use when cell (`:234`), replace "Avoid model routing" with "Avoid a learned router".
  - Add a failure row "Persona routing | Route only between implementations with different capabilities, owners, or controls."
  - Apply the same treatment to the Handoff card (retitle "Handoff at a glance" after C11-R03). Place both after the mechanism sections and before § What the evidence lets us conclude.
- **Related:** shared card policy C10-R04.

**C11-R06 — Priority: High — Action: Rewrite (code + prose)**
- **Location:** `04-part-iv.md:304–337`, § A sensible place to start and § Deterministic route validation; `examples/patterns/routing_handoff.py`.
- **Issue:**
  - The registered example is routing implemented as a framework handoff, with no ownership record or acknowledgment.
  - Its docstring ("A handoff is an authority transfer") contradicts Ch 03 and Ch 11.
  - The inline excerpt violates the no-inline-code rule and has defects.
- **Why it matters:** the code is the reader's model of practice, and it currently demonstrates the conflation the chapter warns against.
- **Change:**
  - (a) Before `[[EXAMPLE:routing-handoff]]`, add: "This uses the SDK's framework handoff to switch agents within one run. It moves control, not accountability; the platform records ownership around it (see § Handoff transfers accountability)."
  - (b) Change the example docstring to say the same, and remove "authority transfer".
  - (c) Move the `DeterministicRouter` excerpt into `examples/patterns/` (e.g., as a `region:router` in a new or existing file). Add `@dataclass(frozen=True)` to `Route`, remove the unused imports, type `maximum_risk` with the same R0–R4 representation as `examples/contracts.py` `risk_class`, register it in `config/examples.json` with a test, and replace the fenced block with `[[EXAMPLE:<id>#router]]`.
- **Related:** C12-R03 (risk representation); AGENTS.md code-listing rule.

**C11-R07 — Priority: Medium — Action: Merge**
- **Location:** `04-part-iv.md:201–206`, § Anti-patterns.
- **Issue:** three of the four bullets duplicate the failure tables.
- **Change:**
  - Delete the § Anti-patterns H3.
  - Move "Persona routing" into the Routing failure table (C11-R05).
  - Add "(AP-08)" to the Handoff failure row "Orphaned task", and "(AP-12)" to the Routing row "Privileged route selection".
- **Related:** Ch 17 § AP-08, § AP-12.

**C11-R08 — Priority: Medium — Action: Add (one sentence each)**
- **Location:** `04-part-iv.md:193` and `:199`.
- **Issue:** missing bridges to Ch 10, Ch 08, Ch 19, and Ch 14.
- **Change:** **Reconciled (see overall-book-review.md §D-08):** As stated, but end the `:193` sentence "…belongs to the LLM Gateway (Chapter 4), and model-routing economics to Chapter 28." The reverse pointer to this chapter goes into Ch 28 item 4 (C28-R07), not Ch 19, whose routing text moves to Ch 28.
  - At `:193`, after the first sentence, add: "A ReAct step that returns `delegate` (Chapter 10) arrives here as a routing request. The eligible set is computed the same way Skill resolution is (Chapter 8): deterministically, before any model sees the options."
  - Replace "run envelope" with "capability envelope (Chapter 21)".
  - At the end of `:193`, add: "Choosing which model serves a step follows the same eligibility-first rule but belongs to the LLM Gateway (Chapter 19)."
  - At `:199`, change "human triage" to "a human triage queue (Chapter 14)".
- **Related:** Ch 19 owner should add the reverse pointer at `05-part-v.md:587`.

**C11-R09 — Priority: Medium — Action: Merge**
- **Location:** `04-part-iv.md:172–182`.
- **Issue:** double framing opening.
- **Change:** delete the `:172` H2 heading, keep its first two sentences as unheaded intro text, and delete its last sentence ("That is what prevents…"), which `:182` restates.
- **Related:** C10-R08.

**C11-R10 — Priority: Low — Action: Rewrite**
- **Location:** `04-part-iv.md:208–214`, § What the evidence lets us conclude.
- **Issue:** a generic box, with R07 and R29 cited without claims.
- **Change:**
  - Replace the box with a one-row claim table. Claim: "Framework handoff". Grounded statement: "The OpenAI Agents SDK documents handoffs as a framework primitive for passing control between agents; recording ownership, acknowledgment, and authority narrowing around it is this book's recommendation." Sources: R29.
  - Remove R07 from this chapter's source line (A2A is cited in Ch 19).
- **Related:** C10-R10.

**C11-R11 — Priority: Low — Action: Rewrite**
- **Location:** `04-part-iv.md:343` (If-fails step 3), `:353` (checklist item 4), `:369` (Q4).
- **Change:**
  - Step 3 → "Confirm the old owner remained accountable until the recipient's acknowledgment was recorded, and that cancellation reached the current owner."
  - Checklist 4 → "Ownership changes only on recorded acknowledgment; state, narrowed authority, deadlines, and cancellation move with it atomically."
  - Replace Q4 with "When is a handoff the wrong choice? | When the parent still owns the outcome (agent-as-tool) or the work needs independent recovery without conversational transfer (durable child task, Chapter 18)."
- **Related:** C11-R02; it removes the duplicate Q in Ch 03/18 once those owners point here.

**C11-R12 — Priority: Low — Action: Rewrite (terminology)**
- **Location:** `04-part-iv.md:187`, state-owner table.
- **Issue:** `RouteDecision` versus `RoutingDecision` (Ch 04 `02-part-ii.md:42`, Ch 20 `06-part-vi.md:77`), and `Handoff` versus `OwnershipTransfer` (Ch 18).
- **Change:** use `RoutingDecision · OwnershipTransfer · CapabilityEnvelope`.
- **Related:** Ch 18 record alignment (Ch 18 owner).

## Verification log

- **Line references checked:** 96 (every `:n` in this file, plus the Ch 03, Ch 18, Ch 19, Ch 04, Ch 20, Ch 16/17, Appendix A/H, example, and diagram pointers). Fixed: 1 (first "human triage" is `:193`, not `:199`). All others resolved within ±3 lines.
- **Claims removed:** none.
- **Claims softened:**
  - "child capability envelope / cancellation lineage are used before Ch 18 and Ch 21" → both terms already appear in Ch 01/Ch 03; the missing forward pointer stands, and "cancellation lineage" has no definition anywhere.
  - Catalog-coverage row: the "add a P-card or note in Ch 16's intro" options are superseded by D-04 (obligation-table row, C16-R10).
- **Claims corrected:**
  - Unused imports in the inline excerpt: all seven imported names (`hashlib`, `json`, `dataclass`, `Awaitable`, `Callable`, `Protocol`, `AgentDecision`) are unused, not five.
  - P-06 cites no chapter at all (the review implied it cites Ch 18).
- **Claims confirmed (most consequential):**
  - Ch 03 `01-part-i.md:1163` "control changes locally but the same activity remains accountable" and `:1166` "A local handoff must not silently transfer authority" are verbatim; `routing_handoff.py:3` says "A handoff is an authority transfer"; the example uses `handoffs=[…]` with no ownership record or acknowledgment, and `test_routing_handoff.py:16` asserts only `last_agent.name`.
  - Ch 18 `:78` "atomically transfer the conversation owner" and `:104` `:handoff` "Atomically transfer owner" carry no acknowledgment step; `OwnershipTransfer` (`05-part-v.md:138`) has no obligations, deadline, or acknowledgment state; Ch 18 Q `:377` says "conversational control transfer".
  - `pattern-routing.gv` is `req -> cls -> {s1,s2,fb}`, `cls` labeled "Classify\nintent · risk · confidence", with no eligibility node; `:193`, `:226`, `:347` all put eligibility first.
  - `RouteDecision` (`:187`) vs `RoutingDecision` (`02-part-ii.md:42`, `06-part-vi.md:77`): confirmed; `RouteDecision` appears nowhere else in the book.
  - Ch 16 P-01…P-12 contain no routing or handoff card; Appendix A's table has no routing row (its "Orchestration" row cites 11–15).
  - R29's registry scope includes "handoffs"; the SDK is never named in Ch 11 prose (`:162–374`); R07 stays cited in Ch 08 and Ch 19 if dropped here.
  - "model routing" at `:234` collides with Ch 19's "Model routing" row (`05-part-v.md:572`).
- **Recommendations amended:** the catalog-coverage row (D-04). C11-R08 was already reconciled (D-08). No other change.
- **Not verifiable here:** "one of five names for the capability envelope (map T6)" (map count not checked; four variants were found in the source: run envelope, authority envelope, capability envelope, child capability envelope).
