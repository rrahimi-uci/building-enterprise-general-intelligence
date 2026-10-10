# Chapter 26 — Make Governance Part of How the Platform Runs: Continuity and Flow Review

Reviewed: `source/parts/08-part-viii.md:1–124` (Part VIII orientation at `:1–7`, Chapter 26 at `:9–124`). Context read: Ch 25 close (`07-part-vii.md:387–495`), Ch 27 (`08-part-viii.md:126–461`), Ch 22 § Risk classes (`06-part-vi.md:714–722`), Ch 23 governance paragraph (`06-part-vi.md:1068–1070`), P-10 (`04-part-iv.md:1467–1473`), Ch 08 Skill manifest (`03-part-iii.md:233`), Ch 04 RunManifest (`02-part-ii.md:183`), Figure 26-1 source (`assets/diagrams/src/governance-model.gv`).

## Overall Assessment

Chapter 26 has the right thesis: governance is a control loop with named decision owners, proportional tiers, and expiring exceptions. Its opening (the control loop, the Harborlight owner paragraph, and the "If the team asks…" table) is among the clearest framing in Part VIII. After that the chapter thins out quickly. § Make review predictable and proportional, which should carry the operating model, is two run-on sentences packing about 30 list items with no explanation (`:74`, `:76`). Exceptions are characterized six times (and named in about 13 lines of the chapter) but their lifecycle is never explained. [verified: corrected — "named six times" undercounted; six is the number of definitional restatements, see § Redundant] The chapter's implementation (inventory, exception API, GovernanceRecord, ExceptionWaiver) sits in Ch 27 (`:266–274`, `:288`, `:302–303`, `:316–317`), and the governance-record field list sits in Ch 23 (`06-part-vi.md:1070`).

The most serious continuity defect is risk numbering. The chapter defines a 0–4 tier scale for use cases (`:62–68`) but never relates it to the R0–R4 effect risk classes the reader learned in Ch 22 (`06-part-vi.md:714`) and has seen in Ch 12, 21, 23, and 24. It calls its own tiers "risk classes" at `:44` and in Figure 26-1. It also never relates either scale to the *change* risk that Ch 25's Approve stage and P-10 use to decide auto-promotion. A reader therefore reaches Ch 27's "risk-tiered eval gates" (`:230`, `:258`) without knowing which scale decides gate depth.

The chapter is short in proportion to its importance. That is a problem only where shortness removes the mechanism. The fix is to move its own implementation home from Ch 27 and Ch 23, and to add three short bridges (tier ↔ effect class, tier × change class → review depth, exception lifecycle). No new conceptual material is needed.

## Intended Reader Mental Model

By the end of the chapter the reader should hold:

- **What:** governance is an owned control loop: outcome → hazard → proportional control → evidence → revision. It is not a committee.
- **Why:** central boards lack local knowledge and become bottlenecks. Federate decisions to accountable owners and centralize control services.
- **How:** each decision class gets one accountable owner and its required evidence. Each use case gets a tier that sets minimum governance. Principles, standards, policy-as-code, and configuration form a hierarchy. Exceptions are scoped, compensated, and expiring. Reviews run on a fixed cadence.
- **When:** review depth is a function of the use case's tier and the class of change, not of which team asks.
- **Relationships (currently missing):** the use-case tier is distinct from the effect risk class (Ch 22) and is bounded by it. The release gate (Ch 25) consumes the tier. An exception is the governed form of Ch 25's "waiver-required" gate result. The governance record is the same inventory Ch 23 and Ch 25 refer to.
- **Practical:** classify three use cases, retire one exception, and know which decision lacks an owner when a release blocks.

## Section-by-Section Flow Review

**Part VIII orientation (`:1–7`).** Role: frame Part VIII. It states the operating problem well ("a run is still active during a deployment"). Issues: it does not say what each of the three chapters answers, and it does not connect back to Part VII's output (evidence and candidate changes). It also lists "reliability", but Part VIII does not own the reliability mechanisms (Ch 15, Ch 22 do). Verdict: adequate, but it misses the handoff from Part VII. See C26-R12.

**§ Why governance belongs in the operating model (`:13–19`).** Role: chapter intro. It adds the claim that governance must change behavior, plus the multi-team motivation. Flow: there is no inbound bridge from Ch 25, whose loop has an "Approve" stage (`07-part-vii.md:401`) that defers the decision to governance [verified: corrected — the loop does not end at Approve; Deploy, Monitor, and Learn follow at `:402–404`] and whose closing promises "decision rights, risk tiers, approvals, exceptions, and accountability" (`:495`). This section is the natural place to say that Ch 26 answers *who approves, how deeply, and what happens when a control cannot be met*. It forms a double "why" opening with the first paragraph of the next H2 (`:23`), which restates it. Verdict: needs the bridge and a merge (C26-R07).

**§ Governance starts with clear decisions and owners (`:21–40`).** Role: the core framing. It adds the state-owner table, the control loop (`:29`), the Harborlight owner paragraph (`:31`), the four-question table (`:33–38`), and the central-board argument (`:40`). Flow: strong. The control loop is the chapter's best mental model. Issues:
- The Harborlight paragraph names the same owners as the accountability table 17 lines later, but appears before that table exists, so the reader meets the example before the structure (C26-R08).
- The state-owner table and the four-question table cite "ValidationReport", an orphan that Ch 25 names only as the Validate-stage output (`07-part-vii.md:400`) and never defines as a record (C26-R10).
- The closing sentence (`:40`) transitions well into federation.

**§ Share responsibility without losing accountability (`:42–58`).** Role: the federated split, Figure 26-1, and the nine-row accountability table. It adds the decision-class → owner → evidence mapping. Flow: good. Issues:
- `:44` and Figure 26-1 (`governance-model.gv` node `c3` "Risk classes and exceptions"; board label "proportional to risk class") use "risk class", which is Ch 22's effect-scale term, for Ch 26's use-case tiers (C26-R01).
- The figure's domains (Finance / Supply chain / Service) are off-thread from Harborlight. This is acceptable for showing federation, but one mortgage domain would tie it to `:31` (C26-R11).

**§ Match the control to the risk (`:60–70`).** Role: the tier table plus one sentence of assessment factors. It adds tiers 0–4 with minimum governance. Flow: this is the chapter's weakest load-bearing section.
- There is no statement of how a tier is assigned, by whom, or what re-tiers a use case.
- There is no relation to R0–R4 (Ch 22) or to Ch 08's `min_risk_tier: 1` (`03-part-iii.md:233`). Tier 3 "Protected action — financial, identity…" visibly overlaps R3/R4 (`06-part-vi.md:721–722`).
- "Exact approval" (Tier 3) means Ch 14's proposal-bound human authorization, while "Executive/risk approval" (Tier 4) means governance sign-off. The same table uses "approval" in two senses.
- The factor list at `:70` is the canonical one but drifts in its three restatements (`:92`, `:99`, `:117`).

Verdict: rewrite (C26-R01, R06, R09).

**§ Make review predictable and proportional (`:72–76`).** Role: the operating model (control hierarchy, review scope, cadence). Flow: severely compressed.
- `:74` packs a five-layer normative hierarchy and a 14-area review list into two sentences.
- `:76` packs five cadences into one.
- The best explanation of the hierarchy is in the design-review answer (`:119`, "Only the first two are argued; the last two are executed"), not in the body.
- Governance health measures appear only in Q5 (`:120`) and in P-10's "What to watch" (`04-part-iv.md:1473`).
- The section never says how tier and change class set release review depth, which is the bridge Ch 27 needs.

Verdict: rewrite into three small tables plus one rule (C26-R02, R04, R05).

**§ What the evidence lets us conclude (`:78–84`).** Role: regulatory applicability. Flow: fine and correctly scoped. It becomes the natural home for the EU AI Act timeline caveat now in Ch 27 § Governance controls (`:269`) once that bullet moves (C26-R03).

**§ If this fails in production (`:86–93`).** Role: governance failure diagnosis. It adds "governance fails as queues and exceptions". Item 2 (recurring exception → missing standard) and item 4 (hand-assembled evidence) are genuinely useful. Verdict: keep. After C26-R05, item 2 links to the exception lifecycle.

**§ What to verify before production (`:95–105`).** The checks are appropriate. `:99` restates the factor list (C26-R09). `:101` repeats the exception definition and can shrink once the lifecycle exists. Verdict: keep, trimmed.

**§ Put the idea to work (`:107–110`).** Both exercises are good and practical. Verdict: keep.

**§ Questions to bring to design review (`:112–120`).**
- Q1 and Q3 are good.
- Q2 restates the factor list a fourth time (C26-R09).
- Q4's answer holds content the body lacks (move it into the body via C26-R04; the Q can stay as recall).
- Q5 introduces governance metrics found nowhere in the body (C26-R04).

Verdict: keep after moving the content.

**§ Where this leads next (`:122–124`).** "Governance defines who may release change; Chapter 27 makes releases immutable…" This transition is accurate. Verdict: keep. After C26-R02 it may add "at the depth the tier sets".

## Sparse or Underdeveloped Content

- **Tier assignment and re-tiering** (`:60–70`). The reader is not told who assigns the tier (the accountability table says the risk owner, `:51`, but § Match the control to the risk does not), when it is re-scored, or how it relates to effect classes. Two or three sentences plus the floor rule in C26-R01 are enough.
- **Release review depth** (`:72–76`). This is the mechanism that makes governance "predictable", and it is absent. C26-R02 adds it as one short rule tied to Ch 25.
- **Exception lifecycle.** Exceptions are characterized at `:38`, `:58`, `:74`, `:101`, `:110`, and `:118` (and named in passing at `:17`, `:27`, `:44`, `:88`, `:91`, `:120`), but the request → approve → monitor → expire/absorb sequence is never stated. The fields exist in Ch 27's ExceptionWaiver (`:317`). C26-R05.
- **Control hierarchy and cadence** (`:74`, `:76`). The content is present but unreadable as prose lists. A tabular conversion is enough (C26-R04).
- **Implementation.** Ch 26 has no "A workable implementation" and no "A sensible place to start". The implementation material exists in Ch 27 and Ch 23; moving it fills the gap (C26-R03). I do not recommend adding new inline code.

## Missing Conceptual Connections

- **Ch 25 Approve stage → Ch 26 decision rights**, missing the bridge "who approves, at what depth". Location: `:13–19`. Ch 25's loop table has an Approve row (`07-part-vii.md:401`) reading "Risk class and domain/security/privacy/operations decision into PromotionDecision". [verified: corrected — the row is the seventh of ten, not the last] Ch 26 never says it is answering that row. (C26-R07)
- **Effect risk class R0–R4 (Ch 22) → use-case tier**, missing a statement that they are different subjects and that the tier is bounded below by the highest eligible effect class. Location: `:60–70`. (C26-R01)
- **Use-case tier → release gate depth (Ch 25 `ReleaseGateDecision.risk tier`, `07-part-vii.md:380`; Ch 27 "risk-tiered eval gates", `:230`, `:258`)**, missing the rule combining tier × change class (Ch 25 "pre-approved low-risk change classes", `07-part-vii.md:401`; P-10 "A typo fix auto-promotes", `04-part-iv.md:1471`). Location: `:72–76`. (C26-R02)
- **Ch 25 gate result "waiver-required" (`07-part-vii.md:365`) → Ch 26 exception**, missing the statement that a waiver *is* a Ch 26 exception with an ExceptionWaiver record. Location: the new exception lifecycle (C26-R05).
- **Tier 3 "exact approval" → Ch 14 proposal-bound authorization; "effect ledger" → Ch 22**, missing pointers. Location: `:67`. (C26-R06)
- **"Policy-as-code decides … budgets" (`:74`) → Ch 28 QuotaDefinition/BudgetReservation (`:608–610`)**, missing a pointer. (C26-R04)
- **Governance record → Ch 23 containment layer 8 (`06-part-vi.md:1068–1070`) and Ch 25 checklist "use-case inventory" (`07-part-vii.md:476`)**, missing the statement that these are the same record and its home is here. (C26-R03)

## Transition Problems

- **Inbound (Ch 25 → Ch 26).** Ch 25 closes with a precise promise (`07-part-vii.md:495`). Ch 26 opens generically and never picks up "approvals". Fix in C26-R07.
- **Within the chapter.** The double "why" opening (`:13–19` and `:23`) restates itself. The Harborlight example precedes the table it illustrates (`:31` vs `:48–58`). The jump from § Match the control to the risk to § Make review predictable has no sentence connecting the tier to the review process.
- **Outbound (Ch 26 → Ch 27).** The sentence is accurate. However, Ch 27 then re-implements governance (§ Governance controls) instead of consuming it, so the boundary between the chapters blurs. Fixed by C26-R03 together with C27-R05.
- **Part VIII orientation.** It does not bridge from Part VII (C26-R12).

## Redundant and Repetitive Concepts

- **Consequence factor list ×4 with drift:** `:70` (10 factors including legal relevance and multi-agent/tool complexity), `:92` (3), `:99` (8), `:117` (7). Keep `:70` as canonical and replace the others with references (C26-R09).
- **Exception definition ×6:** `:38`, `:58`, `:74`, `:101`, `:110`, `:118`. Once the lifecycle exists (C26-R05), `:74` and `:101` can shrink to one clause each. Q3 (`:118`) is acceptable reinforcement.
- **Owner lists ×2:** the Harborlight paragraph (`:31`) and the accountability table (`:48–58`). This is deliberate reinforcement (worked example vs structure). Keep both, reordered (C26-R08).
- **Principles/standards/policy/config ×3:** `:74`, `:103` (checklist), `:119` (Q4). The checklist and Q are acceptable once the body explains the hierarchy (C26-R04).

## Cross-Chapter Duplication

| Other location | Content | Verdict | Owner / action |
| --- | --- | --- | --- |
| Ch 27 § Governance controls (`08-part-viii.md:266–274`) | Inventory, control mapping (NIST/ISO/EU AI Act [R40]), pre-release documentation, evidence package, explanations, no auto-training | Misplaced implementation of Ch 26 (D) | Move bullets 1, 2, 3, 4, 6 to Ch 26; delete 5 and 7 (see C27-R05) |
| Ch 27 § Who should own each decision row Governance Inventory (`:288`); APIs `governance/exceptions`, `governance/inventory` (`:302–303`); records GovernanceRecord, ExceptionWaiver (`:316–317`) | Ch 26's implementation | D (wrong home) | Move to new Ch 26 § A workable implementation (C26-R03) |
| Ch 23 § Containment layers, governance layer and record paragraph (`06-part-vi.md:1068–1070`) | Governance-record field list | D | Ch 23 keeps layer 8 as one line with a pointer to Ch 26. Merge the field list into GovernanceRecord (C26-R03; Ch 23 reviewer implements the pointer) |
| Ch 25 § What to verify before production (`07-part-vii.md:476`) | Use-case inventory check | D | Ch 25 replaces it with "Use-case inventory is current (Chapter 26)" (Ch 25 reviewer) |
| Ch 16 P-10 (`04-part-iv.md:1467–1473`) | Risk-tiered evidence gates; "ChangeBundle → risk → validation…"; metrics "bypass, fatigue, exception age, regression escape" | R (decision card), but "risk" is ambiguous | Ch 16 reviewer: write "change class × use-case tier (Chapter 26)". Ch 26 absorbs the metrics (C26-R04) |
| Ch 22 § Risk classes (`06-part-vi.md:714–722`) | R0–R4 effect classes | Different scale, unrelated in text | Ch 26 adds the relation (C26-R01). Ch 22 stays canonical for R-classes |
| Ch 08 Skill manifest `min_risk_tier: 1` (`03-part-iii.md:233`) | Uses Ch 26's scale before definition, with no pointer | Dependency | Ch 08 reviewer: render it as `min_risk_tier: T1` with a pointer to Ch 26 [verified: superseded by D-02 — the field becomes `risk_ceiling: R1`, an effect class (C08-R06), so it no longer depends on Ch 26] |
| Ch 04 RunManifest `"risk_tier": "high"` (`02-part-ii.md:183`) | A third, non-numeric vocabulary | Drift | Ch 04 reviewer: use `"T3"` (or the named tier) |
| Appendix A row "Governance P-10 ↔ AP-06 … 14, 17, 26" (`09-appendices.md:33`) | Pairs governance with Boolean approval | Mismatch (map §8) | Appendices reviewer |
| Appendix G Phase 0 inventory (`09-appendices.md:179`) | Use-case/risk inventory | R | Keep |

## Structural Recommendations

1. Give Ch 26 its own implementation section by moving the governance implementation out of Ch 27 and Ch 23 (agrees with map S10 and S3). This turns the chapter from the book's leanest into a complete operating-model chapter without adding new concepts.
2. Proposed order:
   - § Why governance belongs in the operating model (with the Ch 25 bridge)
   - § Governance starts with clear decisions and owners (control loop, four questions)
   - § Share responsibility without losing accountability (figure, table, *then* the Harborlight example)
   - § Match the control to the risk (T-tiers, relation to R-classes, assignment)
   - § Make review predictable and proportional (control hierarchy table, review-depth rule, review-scope index, cadence table, exceptions H3)
   - § A workable implementation (moved)
   - § What the evidence lets us conclude
   - the template sections
3. Do not add a "A sensible place to start" code listing. The moved records and "Put the idea to work" serve that role. If the author wants one, register it under `examples/` per `AGENTS.md`; do not write it inline.

**Disagreement with the concept map:** none of substance. The map lists ValidationReport as "never defined". It is *named* as the Validate-stage output in Ch 25's loop table (`07-part-vii.md:400`), in Ch 07's golden path (`03-part-iii.md:106`), and in Ch 20's supply-chain row (`06-part-vi.md:82`), though it has no record definition anywhere (verified by grep). The fix is the same: point to Ch 25's records.

## Concrete Recommended Changes

1. **C26-R01 — High — Rewrite.** Location: `08-part-viii.md:60–70`, § Match the control to the risk; also `:44` (§ Share responsibility…) and `assets/diagrams/src/governance-model.gv` (node `c3`, node `board`).
   - **Issue:** a 0–4 tier scale is introduced with no relation to the R0–R4 effect classes (Ch 22) or to change risk (Ch 25/P-10). Ch 26 also calls its tiers "risk classes".
   - **Why it matters:** the reader has learned R0–R4 as the risk scale. Two unlabeled 0–4 scales with overlapping words ("protected", "financial", "irreversible") make every later "risk-tiered" reference ambiguous.
   - **Change:** **Reconciled (see overall-book-review.md §D-02):** Change as stated. In Related, replace the Ch 08 bullet: Ch 08 renders the Skill field as `risk_ceiling: R1`, an effect risk class (C08-R06), not as a T-tier. Ch 25 uses "use-case tier × change class" in its Approve row (C25-R08).
     - Label the tiers T0–T4 in the table's first column ("T0 Deterministic/assistive" … "T4 High consequence/systemic").
     - Add three sentences after the table, in substance: "Three risk scales recur in the platform, each with its own subject. Effect risk classes R0–R4 (Chapter 22 § Risk classes) classify each tool action and are enforced at dispatch. Use-case tiers T0–T4 classify a use case and set its governance and release depth. Change classes (Chapter 25's Approve stage) classify a proposed change. A use case's tier is never lower than its most dangerous eligible effect demands: any eligible R3 or R4 tool implies at least T3 controls, and any R2 tool at least T2." Mark this as a book-authored recommendation.
     - Add one sentence on assignment: "The risk owner assigns the tier from the factors below, and re-scores it whenever eligible tools, data classes, autonomy, or exposure change."
     - At `:44` and in Figure 26-1, replace "risk class" with "risk tier".
   - **Related sections:**
     - Ch 08 reviewer renders `min_risk_tier: 1` as `T1` with a pointer.
     - Ch 04 reviewer changes the RunManifest to `"risk_tier": "T3"`.
     - Ch 25 reviewer uses "risk tier" in ReleaseGateDecision and "change class" in the Approve row.
     - Ch 27 and Ch 28 follow C27-R07 and C28-R09.
     - Ch 22 remains the canonical R-class home (or wherever map S6 moves it).

2. **C26-R02 — High — Add.** Location: `08-part-viii.md:72–76`, § Make review predictable and proportional, a new paragraph after the control hierarchy.
   - **Issue:** nothing says how review depth is decided, although the chapter promises predictability and Ch 27 uses "risk-tiered gates".
   - **Why it matters:** this is the bridge from governance to release. Without it, "proportional" is a slogan.
   - **Change:** **Reconciled (see overall-book-review.md §D-02):** As stated, but do not re-list the human-approval change types: write "A change in Chapter 25's 'Require human governance' row (§ Close the loop without handing control to the model) always requires a named approver, whatever the tier." C25-R09 deletes § Automate only when regressions are contained and owns that list. Original text: add a short rule, in substance: "The release gate (Chapter 25 ReleaseGateDecision) takes two inputs: the use case's tier and the change class. In T0–T2 use cases, pre-approved low-risk change classes (metadata, documentation, evaluated prompt wording) may promote automatically on passing gates. A change that touches permissions, data purpose, protected effects, the model allowlist, or evaluator truth always requires a named human approver, whatever the tier (Chapter 25 § Automate only when regressions are contained). In T3–T4 use cases every behavior change needs the release owner's recorded approval and a canary; T4 adds independent assurance." These sentences restate existing Ch 25/P-10 rules in one place. Do not add a new matrix.
   - **Related sections:** Ch 25 `:401`, `:436`; P-10 `04-part-iv.md:1471` (Ch 16 reviewer adds a pointer here); Ch 27 `:230`, `:258`.

3. **C26-R03 — High — Move.** Location: create `## A workable implementation` in Ch 26, inserted after § Make review predictable and proportional (before `:78`).
   - **Issue:** Ch 26's implementation lives in Ch 27 and Ch 23.
   - **Why it matters:** readers looking for the governance record, the inventory API, or the exception record find them in the release chapter, and Ch 26 reads as policy without mechanism.
   - **Change:** **Reconciled (see overall-book-review.md §D-19):** Move as stated. In Related, Ch 23 deletes its containment-layer list (C23-R03) and the `:1070` paragraph (C23-R05) outright, so there is no "Layer 8" sentence to add there. Original text: move into Ch 26:
     - (a) the Governance Inventory row from Ch 27 `:288` into an H3 "Who should own each decision" table, adding rows for the Exception Service (named risk authority) and the Policy Bundle Registry (standards → policy-as-code);
     - (b) APIs `POST /v1/governance/exceptions` and `GET /v1/governance/inventory` from Ch 27 `:302–303`;
     - (c) records GovernanceRecord and ExceptionWaiver from Ch 27 `:316–317`, merging into GovernanceRecord the extra fields of Ch 23's paragraph (`06-part-vi.md:1070`: model and vendor dependencies, release, approvers, retirement plan);
     - (d) Ch 27 § Governance controls bullets 1 (inventory), 2 (control mapping, including the EU AI Act [R40] timeline caveat; keep the citation), 3 (documented intended/prohibited use before release), 4 (evidence package per material run, adding "the audit ledger itself is Chapter 24's"), and 6 (explanations at the right level), as a short H3 "What governance requires before release".
     - Update the state-owner table's Core contracts (`:27`) to "risk tier · PolicyDecision · ReleaseGateDecision · GovernanceRecord · ExceptionWaiver".
   - **Related sections:** C27-R05 (deletes them from Ch 27); the Ch 23 reviewer replaces `06-part-vi.md:1070` with "Layer 8 is the governance record defined in Chapter 26"; the Ch 25 reviewer points its `:476` check here.

4. **C26-R04 — Medium — Rewrite.** Location: `08-part-viii.md:74` and `:76`, § Make review predictable and proportional.
   - **Issue:** two sentences carry the hierarchy, the 14 review areas, and five cadences. The best explanation sits in Q4. Governance metrics exist only in Q5.
   - **Why it matters:** this is the chapter's operating model, and as written it cannot be absorbed.
   - **Change:** replace `:74–76` with:
     - (a) a five-row table "Layer | What it decides | Who changes it | How it is enforced": Principles (argued, non-negotiable outcomes; executive/risk; review), Standards (argued, reusable contracts; platform owner; RFC), Policy-as-code (executed, eligibility of models, data, tools, actions, budgets, approvals; policy owner; PDP, Ch 21; budget/quota policy, Ch 28 QuotaDefinition), Application configuration (executed, selection within the envelope; team; release pipeline), Exceptions (time-bound gap; risk authority; ExceptionWaiver).
     - (b) one sentence: "A design review covers each area below; the chapter in parentheses holds its controls". List the 14 areas from `:74` with their canonical chapters: outcome/acceptance (2, 13); deterministic boundary (2); state/effect ownership (15, 22); identity/delegation (21); context/memory (6); tool/MCP/A2A trust (19); threats (20); evaluation truth (25); observability/privacy (24); recovery and release (27); capacity/cost (28); human oversight (14); portability (3).
     - (c) a cadence table "Cadence | Input | Owner | Output" using the existing five cadences.
     - (d) a closing sentence on governance health with the Q5 measures (time from evidence-complete to approved; exception count and age trending down; the same evidence reused by engineering, risk, and audit) plus P-10's bypass and regression-escape rates.
   - Keep Q4 and Q5 as recall.
   - **Related sections:** P-10 `04-part-iv.md:1473` (Ch 16 reviewer points here for metrics).

5. **C26-R05 — Medium — Add.** Location: new `### Exceptions that expire` at the end of § Make review predictable and proportional.
   - **Issue:** exceptions are characterized six times but their lifecycle is never given.
   - **Why it matters:** "an exception without an expiry is a silent policy change" is the chapter's sharpest claim, and the reader is never shown the mechanism.
   - **Change:** four or five sentences:
     - a request names the exact control gap, scope, and compensating controls;
     - the named risk authority approves it with an expiry, recorded as an ExceptionWaiver;
     - a release gate returning "waiver-required" (Chapter 25 `POST /v1/release-gates:evaluate`) is satisfied only by a matching unexpired waiver;
     - usage is monitored;
     - at expiry the gap is closed or absorbed into a changed standard, and a recurring exception is treated as a missing standard (§ If this fails, item 2).
   - Then shorten `:101` to "Exceptions follow the expiring lifecycle above; none is open-ended."
   - **Related sections:** C26-R03 (record); Ch 25 `07-part-vii.md:365`, `:380`.

6. **C26-R06 — Medium — Rewrite.** Location: `08-part-viii.md:66–68`, tier table rows 2–4.
   - **Issue:** "approval" means two different things in rows 3 and 4. The controls are not linked to their chapters.
   - **Why it matters:** this is the T3 collision (map §6) inside a single table.
   - **Change:** **Reconciled (see overall-book-review.md §D-22):** Row 3: "Least privilege (Ch 21), proposal-bound approval of each protected action (Ch 14), effect ledger (Ch 22), strong evaluation, canary, incident plan". Rows 2 and 4 as stated.
     - Row 3 minimum governance: "Least privilege (Ch 21), proposal-bound human authorization of each protected action (Ch 14), effect ledger (Ch 22), strong evaluation, canary, incident plan".
     - Row 4: "Executive/risk sign-off of the use case, independent assurance, strict capability envelope, recovery exercise".
     - Row 2 "recourse" → "recourse (Ch 14)".
   - **Related sections:** map T3; the Ch 14 reviewer's approval-terminology decision.

7. **C26-R07 — Medium — Rewrite/Merge.** Location: `08-part-viii.md:13–23`, § Why governance belongs in the operating model and the first paragraph of § Governance starts with clear decisions and owners.
   - **Issue:** there is no inbound bridge, and the opening is a double "why".
   - **Why it matters:** readers arrive from Ch 25's Approve stage and need to know that this chapter answers it.
   - **Change:**
     - Replace the second sentence of `:15–19` with, in substance: "Chapter 25's improvement loop defers its Approve stage to governance; this chapter decides who approves, how deeply, and what happens when a required control cannot be met." [verified: corrected — "ends at an Approve stage" was false; Ch 25's loop continues through Deploy, Monitor, and Learn]
     - Move paragraph `:23` into § Why governance belongs… as its second paragraph, and delete the sentence "Start by naming the decision, the accountable role, the evidence needed, and the time boundary. Then scale review to the risk.", which restates `:16–17`. Keep its last sentence (predictability), which is the section's thesis and does not restate `:16`. [verified: corrected — the original named the wrong sentence as the restatement]
     - § Governance starts with clear decisions and owners then begins with the control loop (`:29`).
   - **Related sections:** Ch 25 `07-part-vii.md:401`, `:495`.

8. **C26-R08 — Low — Move.** Location: `08-part-viii.md:31` (Harborlight paragraph), currently in § Governance starts with clear decisions and owners.
   - **Issue:** the example precedes the accountability table it instantiates.
   - **Why it matters:** example after structure lets the reader map each owner to a table row.
   - **Change:** move the paragraph to directly after the accountability table (after `:58`) and open it with "In Harborlight's mortgage-evidence assistant, the table resolves as follows:". No wording change otherwise.
   - **Related sections:** none.

9. **C26-R09 — Low — Condense.** Locations: `:92` (If-fails item 3), `:99` (checklist), `:117` (Q2).
   - **Issue:** the consequence factor list is restated three times with drift.
   - **Why it matters:** drifting lists make the reader wonder which factors count.
   - **Change:**
     - Keep `:70` as canonical.
     - `:99` → "Risk tier is derived from the consequence factors in § Match the control to the risk, and bounded below by the highest eligible effect class — never from the model name."
     - `:117` answer → "Consequence and reversibility, scored with the chapter's factors and bounded by the eligible effect classes, rather than the model or framework in use."
     - Leave `:92` as is (it names a diagnostic subset deliberately).
   - **Related sections:** C26-R01.

10. **C26-R10 — Low — Rewrite.** Locations: `:27`, `:37`, `:57`.
    - **Issue:** "ValidationReport" is used as a record but defined nowhere.
    - **Why it matters:** this is an orphan contract in the chapter's own state table.
    - **Change:** **Reconciled (see overall-book-review.md §D-05):** Ch 25 defines ValidationReport (C25-R08). Where these lines mean the go/no-go output, write "ReleaseGateDecision (Chapter 25)"; where they mean the validation evidence (the release question at `:37`), keep "ValidationReport (Chapter 25)". C26-R03's Core contracts list stands. Original text: replace with "ReleaseGateDecision (Chapter 25)", or whatever single name the Ch 25 reviewer settles for the gate output under map T23. Keep "ValidationReport" only if Ch 25 adds it to § Records worth preserving.
    - **Related sections:** Ch 25 records (`07-part-vii.md:369–381`); Ch 27 C27-R10.

11. **C26-R11 — Low — Add.** Location: before `:13` (an opening box), and `governance-model.gv` domain nodes.
    - **Issue:** Ch 26 is one of five chapters with no THE DESIGN CHOICE box, and its figure uses off-thread domains.
    - **Why it matters:** this is template consistency. The tie to the case is optional.
    - **Change:**
      - Add a one-line box: "THE DESIGN CHOICE: Govern by decision class — one accountable owner, proportional tiers, evidence produced by the pipeline, and exceptions that expire."
      - Optionally relabel `d1` "Finance agents" as "Mortgage evidence agents" so Figure 26-1 matches the Harborlight paragraph.
    - **Related sections:** map §5.1.

12. **C26-R12 — Low — Rewrite.** Location: `08-part-viii.md:3–7`, Part VIII orientation.
    - **Issue:** there is no handoff from Part VII and no per-chapter roles. "Reliability" is overclaimed.
    - **Why it matters:** this is the reader's map into the final Part.
    - **Change:** keep the first two sentences, then replace the third with, in substance: "Part VII produced evidence and candidate changes. This Part decides who may approve them (Chapter 26), how approved change reaches production without disturbing work in flight (Chapter 27), and how much work the platform admits, and at what cost, when demand peaks (Chapter 28)."
    - **Related sections:** C28-R10 (the closing mirrors this framing).

13. **C26-R13 — Low — Move (receive).** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** § What the evidence lets us conclude (`08-part-viii.md:80–82`); source Ch 23 `06-part-vi.md:1186`.
   - **Issue:** C23-R05 moves Ch 23's governance-sources row here, but no Ch 26 item received it.
   - **Change:** Merge it into the existing "Regulatory applicability" row rather than adding a second row. Add only what Ch 26's row lacks (NIST AI RMF under revision as of 2026; OWASP as community security guidance), keep each claim inside its registry scope (R12, R14, R15, R40), and update the "draws on" sentence. Run `make references`.
   - **Related:** C23-R05.

## Verification log

- **Line references checked:** 62 (all references to `08-part-viii.md`, `07-part-vii.md`, `06-part-vi.md`, `04-part-iv.md`, `03-part-iii.md`, `02-part-ii.md`, `09-appendices.md`, and `governance-model.gv`); 0 fixed. All quoted phrases (`:44`, `:119`, `:124`, `07-part-vii.md:401`, `:495`, `04-part-iv.md:1471`) are verbatim.
- **Claims removed:** none.
- **Claims corrected or softened:**
  - "Ch 25's loop ends at an Approve stage" (Overall § Why governance, Missing connections, C26-R07 replacement text) — Ch 25's loop continues through Deploy, Monitor, Learn (`07-part-vii.md:402–404`); reworded to "defers its Approve stage to governance".
  - "Exceptions are named six times" — the chapter names exceptions in 13 lines; six is the count of definitional restatements. Reworded in three places.
  - C26-R07 named the wrong sentence of `:23` as the restatement of `:16`; corrected to the "Start by naming the decision…" sentences.
  - Cross-chapter row for Ch 08 `min_risk_tier` marked superseded by D-02 (`risk_ceiling: R1`), consistent with the Reconciled note already in C26-R01.
- **Important claims confirmed:**
  - `:44` and `governance-model.gv` (node `c3` "Risk classes and exceptions", node `board` "proportional to risk class") use "risk class" for Ch 26's use-case tiers; Ch 22 § Risk classes (`06-part-vi.md:714–722`) owns R0–R4 — confirmed by reading both.
  - R0–R4 is seen in Ch 12 (`04-part-iv.md:518`), Ch 21 (`06-part-vi.md:495`), Ch 23 (`:1178`), Ch 24 (`07-part-vii.md:145`) before Ch 26 — grep confirmed.
  - Factor-list drift: `:70` 10 factors, `:92` 3, `:99` 8, `:117` 7 — counted.
  - `:74` holds a 5-layer hierarchy plus 14 review areas; `:76` five cadences — counted.
  - ValidationReport has no record definition anywhere in the book (grep: named only at `03-part-iii.md:106`, `06-part-vi.md:82`, `07-part-vii.md:400`, and Ch 26 `:27`, `:37`, `:57`).
  - Ch 27 holds the governance implementation at `:266–274`, `:288`, `:302–303`, `:316–317`; Ch 23's field list is at `06-part-vi.md:1070` — confirmed.
  - Ch 26 has no THE DESIGN CHOICE box; 23 of 28 chapters have one (grep count), so "one of five" holds.
  - Ch 08 `min_risk_tier: 1` (`03-part-iii.md:233`) and Ch 04 `"risk_tier": "high"` (`02-part-ii.md:183`) are the only numeric/string tier fields — grep confirmed.
- **Recommendations amended:** C26-R07 (two wording fixes, above). All others consistent with §12 D-02, D-05, D-19, D-22, D-29 as already annotated; none breaks the 8/28/12 topology, moves code inline, or hand-edits a rendered diagram.
- **Not verified:** whether Ch 23's reviewer (C23-R05) actually routes the governance-sources row to C26-R13 was taken from §12 D-29, not re-read.
