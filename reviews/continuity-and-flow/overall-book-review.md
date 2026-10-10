# Whole-Book Continuity and Flow Review — Synthesis

Lead-editor synthesis of the 28 chapter reviews in this folder. It reconciles them, records the book-level decisions, and turns roughly 425 recommendations into an implementation plan. No book file was changed.

---

## 1. Scope and method

**What was read.**
- The reviewer hand-back notes (cross-chapter requests, disagreements with the map, 16 orchestrator-flagged conflicts).
- For all 28 reviews: Overall Assessment, Cross-Chapter Duplication, Structural Recommendations, and every Concrete Recommended Change. Other sections were consulted where a conflict depended on them.
- `book-concept-map.md` §3 (registry), §4 (dependency problems), §6 (terminology), §8 (front matter and appendices), §9 (structural candidates).
- Book source and code, wherever a conflict depended on the actual text:
  - `examples/contracts.py` (dispositions, risk types);
  - both Run API tables (`02-part-ii.md:159–170`, `04-part-iv.md:1206–1218`);
  - the Ch 04 and Ch 27 review questions;
  - Ch 18 `:handoff` and the OwnershipTransfer record;
  - `effect_idempotency.py` and its test;
  - `governed_tool_gateway.py`;
  - the AP-05 code and the Ch 13 evaluator code;
  - the Ch 18/Ch 21 envelope code (`diff` confirms the two copies are identical);
  - `tools/callouts.py`;
  - `tools/validate_book.py` and `tools/check_examples.py`;
  - an inventory of every fenced block in `source/parts`;
  - a grep of chapter-number back-references.

**How the reviews were produced.**
- Nine reviewers wrote one review per chapter on a common template.
- Part orientations are reviewed in the first chapter review of each Part. The front matter is reviewed in `chapter-01.md`.
- **No review covers the appendices.** Their findings arrive only as cross-chapter requests and through map §8. This document therefore supplies the Appendices work package (§15, WP-A).

**How they were reconciled.**
- Each conflict is decided in §12 (D-01 … D-32).
- A superseded recommendation is amended in place. Its Change field now starts with **"Reconciled (see overall-book-review.md §D-nn):"** followed by the final instruction (54 amendments).
- A cross-chapter request that no owning review picked up has been added to the owner's file, marked *"Added in reconciliation"* (24 additions).
- Seven factual or canonical-home statements in `book-concept-map.md` are marked *Corrected in synthesis* or *Superseded in synthesis*.

**Line references.** `file:line` means `source/parts/<file>` at commit `0361350`. Within a file, apply edits bottom-up, or re-locate each passage by its quoted text, because earlier edits shift line numbers. Content that is moved remains recoverable from that commit and from the review text.

**Files in this folder.**

| File | Content |
| --- | --- |
| `book-concept-map.md` | Whole-book map: spine, chapter summaries, concept registry, dependency table, terminology T1–T28, structural candidates S1–S17 (seven entries corrected in synthesis) |
| `chapter-01.md` … `chapter-28.md` | Per-chapter reviews; recommendation IDs `Cnn-Rnn`. Front matter in `chapter-01.md`; Part orientations in chapters 01, 04, 07, 10, 18, 20, 24, 26 |
| `overall-book-review.md` | This synthesis |

---

## 2. Overall narrative assessment

The thesis is right, consistent, and well argued. The model supplies bounded reasoning, and the surrounding system owns state, authority, effects, evidence, and recovery. The spine (boundary → six gates → runtime seam → owned architecture → platform → bounded patterns → collaboration → security → evidence → operations) is the right order, and **no Part or chapter needs to move.**

The best passages are the material later chapters should lean on, not re-teach:
- Ch 01's Monday–Friday week and the uncertainty-ownership table;
- Ch 02's one proposal crossing six gates;
- Ch 03's framework-vs-platform table and its restart test;
- Ch 05's governed-knowledge taxonomy;
- Ch 08's "discovery is not permission";
- Ch 12's "planning is compilation, not authorization";
- Ch 17's anti-pattern cards;
- Ch 20's injected-document walkthrough;
- Ch 22's property table;
- Ch 24's twelve-minute diagnosis;
- Ch 27's rollback of *assignment*, not history.

Seven book-level problems weaken the flow.

1. **The chapters are written as if each stood alone.** No chapter in Parts II–VIII refers back to Chapters 1–9 by number (verified by grep). Nearly every "Chapter N" reference points forward. Later chapters therefore re-teach Part I–III mechanisms instead of recalling them, and the reader never feels the book accumulate. About 150 of the recommendations add a "(Chapter N)" back-pointer or a one-sentence recall.
2. **Pre-teaching, and canonical homes that come late.**
   - Ch 03 previews seven mechanisms at near-full depth.
   - The Unknown-effect rule is taught six times before Ch 22.
   - R0–R4 risk classes are used ten chapters before they are defined.
   - The LLM Gateway is used in Ch 01, 03, 04, and 07 and defined in Ch 19.
   - The acceptance engine is never defined at all.
3. **The book's central distinctions drift in its own vocabulary.** It argues that a guardrail is a detector, then names an enforced rule, a whole security architecture, and a set of numeric limits "guardrails". It also has three meanings of "handoff", four meanings of "plane", "authorization" covering both policy decisions and human approval, two unlabeled 0–4 risk scales, seven terminal-state vocabularies, and several names for the same record.
4. **Template boilerplate creates redundancy.** Fifteen chapters open with a double "why". There are twelve "How X works in practice" cards (ReAct is described four times), thirteen "Required analysis" tables that mostly restate the prose, 24 state-owner tables whose format is never explained, empty H2 wrappers, and stock phrasing in the catalogs.
5. **The book stops rather than ends.** Ch 28's closing is inaccurate, and the Closing Perspective is buried after the references. Nothing returns to Ch 01's model.
6. **The running case drifts after C03.**
   - "Employment verification" contradicts the second pay statement.
   - Northstar is a second name for the platform.
   - The promised supplier-onboarding comparison never arrives.
   - Identifiers change between adjacent chapters.
   - The checkpoint C01 is never shown.
7. **Code contradicts the text** in three places (DF-01–DF-03, §13). In addition, 38 fenced code blocks sit in chapter prose, against AGENTS.md.

Net effect: the recommended changes are mostly moves, renames, pointers, and deletions, and the book gets shorter.
- **Largest cuts:** Ch 03 pre-teaching (~110 lines), two-thirds of Ch 16, the Ch 19 LLM Gateway section, Ch 22's second implementation block, and Ch 23's framing and threat table.
- **Largest additions** (each fills a verified gap):
  - Skill and pack mechanism in Ch 08/09 (~700 words);
  - the acceptance decision in Ch 13 and the intervention contract in Ch 14;
  - Ch 26's implementation section (moved from Ch 27);
  - a real Closing Perspective.

---

## 3. Concept progression assessment

The graph lists the major concepts in the order the reader should meet them. `→` means "depends on". **[BREAK]** marks where the current book violates the order; each break names the recommendations that fix it.

```
FRONT MATTER  reader paths, how the book is organized ............ [BREAK: paths skip prerequisites → C01-R21; prose describes a request flow, Figure 0-1 is a Parts map → C01-R22]
PART I — BOUNDARY
 01 Model reasons; system owns state/authority/effects/evidence/recovery
    ├ uncertainty owners; state-owner table template ............... [BREAK: template never explained → C01-R05]
    ├ control points: API · A2A · LLM · Tool · MCP gateways ........ [BREAK: Agent Gateway orphan → D-07; LLM Gateway contract only in Ch 19 → D-08]
    └ vocabulary: capability envelope, credential lease, RunManifest (defined briefly here) [BREAK: missing/wrong pointers → C01-R03]
 02 Proposal → six gates (deterministic shell) → 01
    ├ gate owners; approval sits inside Authorize .................... [BREAK: approval has no place → C02-R03]
    ├ effect risk class R0–R4 (gloss here; canonical Ch 22) ......... [BREAK: used in Ch 02/12/21 before Ch 22 → D-01]
    └ acceptance criteria (definition) → component in Ch 13 ......... [BREAK: engine never defined → C02-R05, C13-R02]
 03 AgentRuntime seam: AgentStepRequest/Result; step status; framework vs business state; restart test → 02
    └ pre-teaches approval, handoff, guardrails, retries, write path [BREAK → C03-R01..R07]
PART II — ARCHITECTURE (→ I)
 04 Seven ownership planes; one writer per record; RunManifest; base Run API; event envelope; stores; trust boundaries; global control tier / regional cells
    └ ........................................................................ [BREAK: AgentRuntime not placed → C04-R02; three decompositions → C04-R01/R03; records without owners → C04-R04]
 05 Governed knowledge; Enterprise Knowledge Hub; content provenance → 04
 06 Context = authorized, disposable projection; ContextManifest; trust tiers; memory as a governed write → 03, 04, 05
PART III — PLATFORM (→ I, II)
 07 Paved road; three owners; golden path with evidence (an explicit forward map) [BREAK: unlabeled forward refs → C07-R01, C07-R13]
 08 Skill: manifest, digest, version promise, discovery ≠ permission, runtime path, four binding moments [BREAK: missing → C08-R01..R03, R07]
 09 Skill Pack: compatibility, install ≠ grant, pack lifecycle → 08 .... [BREAK: compatibility undefined → C09-R01, R02]
PART IV — PATTERNS (each runs inside 02 + 03 + 08)
 10 Bounded ReAct: limits outside; stop ≠ accept; step decisions → 03 [BREAK: no Part III link → C10-R01, R07]
 11 Routing (eligibility first) ≠ Handoff (acknowledged ownership transfer) → 08, 10 [BREAK: three meanings → D-06]
 12 Plan compilation: Plan IR; node kinds map onto 10/13/02+22/14/15/18 → 02, 11
 13 Reflection revises; the acceptance engine decides (AcceptanceDecision) → 02, 10, 12
 14 Approval (proposal-bound) · intervention (system-raised) · operator control → 13 [BREAK: intervention undefined → C14-R02/R03]
 15 Durable execution; run lifecycle; canonical run terminal states → 10–14 [BREAK: "core patterns are now defined" is false → C15-R11]
 16 Choose and compose the Part IV patterns (slim) ..................... [BREAK: whole-book catalog placed here → D-04]
 17 Anti-patterns as problem statements, each with Prevented in / Built in → 01–15, previews 18–28
PART V — COLLABORATION
 18 TaskEnvelope; task lifecycle; joins; cancellation; Ownership Service → 11, 15 (21 previewed) [BREAK: envelope proof before Ch 21 → C18-R01]
 19 Protocols do not transfer trust; MCP Gateway; A2A Gateway; FederatedTask; artifact adoption → 18
PART VI — SECURITY
 20 Detector ≠ policy point ≠ enforcement point; 9 layers; threats; incident lifecycle → 04, 06
 21 Subject + actor + purpose; authorization tuple; capability envelope (scope) vs credential lease (proof) → 20
 22 Effect protocol: logical key, intent hash, Unknown, reconciliation, receipt; R0–R4; ToolManifest → 02, 21
 23 Containment: sandbox, egress, last-hop secrets, taint, kill switch → 20–22
PART VII — EVIDENCE
 24 Causal run trace: decision-centric span schema; debugging method → 15, 22 [BREAK: implementation lives in Ch 25 → D-10, C24-R01]
 25 Release evaluation (EvaluationResult, ValidationReport, ReleaseGateDecision); learning loop; runtime vs offline → 13, 24
PART VIII — OPERATIONS
 26 Governance: use-case tier T0–T4 (floored by R-class) × change class; exceptions → 22, 25 [BREAK: unrelated scales → D-02]
 27 Release chain: ChangeBundle → ReleaseManifest → EnvironmentBinding → RunManifest; rollback of assignment; regional recovery → 04, 15, 25, 26
 28 Admission, budgets, permits; cost per verified successful outcome; model-routing economics → 10, 12, 14, 15, 19→04
CLOSING PERSPECTIVE  Ch 01's week, resolved ............................. [BREAK: placed after Appendix L → D-26]
```

**Forward references that remain, by design.**
- Ch 07 is an explicit forward map.
- Six Ch 17 cards preview Parts V–VIII and say so.
- The capability envelope is used in Ch 03, 11, 12, 15, and 18 before Ch 21. It is defined briefly in the Ch 01 vocabulary (C01-R03) and in Ch 18 (C18-R01), and every earlier use gets "(Chapter 21)" (C03-R07, C03-R12, C11-R08, C12-R11, C15-R03).
- The Unknown rule is stated as a rule in Ch 02, 10, and 15, with pointers, and Ch 22 announces that it now gives the full treatment (C22-R03).

---

## 4. Major continuity problems

| # | Problem | Evidence | Fix |
| --- | --- | --- | --- |
| CP-1 | Chapters never recall earlier chapters by number | Grep: zero references to Ch 1–9 from Parts IV–VIII | Recall pointers throughout; Ch 01 "Developed in" column (C01-R09); Ch 07 "Taught in" column (C07-R01); Ch 04 records table (C04-R04); Ch 17 "Prevented in / Built in" lines (C17-R03); AP pointers (§12 D-29) |
| CP-2 | "Handoff" has three meanings (Critical) | Ch 03 `:1163`, Ch 11 `:182`, Ch 18 `:78`, `:104`, `:377`; the example's docstring | D-06 |
| CP-3 | "Guardrail" contradicts the book's own thesis | Ch 05 `:388`+; Ch 20 `:58`, `:65`, Fig 20-1/20-3, `:331`; Ch 28 `:639`; Ch 07 `:46`; Fig 0-1 | C05-R01, C20-R02, R04, R06, C28-R04, C07-R01, C01-R22 |
| CP-4 | Risk scales unlabeled and unrelated | R0–R4 (Ch 22), tiers 0–4 called "risk classes" (Ch 26), `min_risk_tier: 1`, `"risk_tier": "high"`, integer risk in code | D-01, D-02 |
| CP-5 | Acceptance and terminal vocabularies conflict | Seven vocabularies (map T12); acceptance engine undefined | D-12, D-13, D-14 |
| CP-6 | Record names drift | RunContext, AgentStep, ToolSpec, AgentManifest, EvaluationReport, ValidationReport (orphan), ReleaseBundle, SecretLease, A2ATaskEnvelope | §11; D-05, D-27 |
| CP-7 | The running case drifts | T15 (missing document), T1 (Northstar), T16 (identifiers), supplier promise unkept, C01 checkpoint unshown | D-20, D-21, D-31, C01-R01, C01-R04 |
| CP-8 | Transition promises broken | Ch 01's "Figure 4-1 is the same picture"; Ch 03 → Ch 04 AgentRuntime promise; Ch 09 → Ch 10 platform thread; Ch 15 → Ch 16 false claim; Part VI order contradicts Ch 20; Ch 28 closing | C01-R11, C04-R03, C04-R02, C03-R15, C09-R09, D-28, C15-R11, C20-R01, C28-R10 |
| CP-9 | Code teaches the opposite of the text | DF-01–DF-03, DF-05, DF-09 | §13 |
| CP-10 | Section titles promise content they lack | Ch 08 title promises versioning; Ch 09's thesis (compatibility) undefined; Ch 25's "loop" heading holds a gate; Ch 17 governance group holds no governance card | C08-R07, C09-R01, C25-R10, C17-R08 |

---

## 5. Major structural problems

| # | Problem | Decision / IDs |
| --- | --- | --- |
| SP-1 | Ch 16 is a whole-book catalog at the end of Part IV; half its cards depend on Parts V–VIII; it omits Ch 11–14 | Split: a slim Part IV synthesis plus cards moved to Appendix A (D-04; C16-R01–R10) |
| SP-2 | Ch 03 spends ~120 lines on previews of other chapters | One consolidated H2, "Where the framework meets the rest of the platform" (C03-R01–R07, R10, R11) |
| SP-3 | Ch 19 contains an LLM Gateway mini-chapter | Split between Ch 04 and Ch 28 (D-08; C19-R01, C04-R19, C28-R07) |
| SP-4 | Ch 22 is two chapters stacked (two implementation blocks, two analysis tables) | One argument, one implementation block (C22-R01–R03) |
| SP-5 | Ch 20 and Ch 23 overlap (premise, layer lists, threat catalogs, injected-document story) | Division of labour (D-19; C20-R01, R04, R07, R08, R10; C23-R01–R04) |
| SP-6 | Ch 24's implementation lives in Ch 25, and Ch 25's evaluation material leaks into Ch 24 | Swap (C24-R01, R08; C25-R01) |
| SP-7 | Ch 26's implementation lives in Ch 27 and Ch 23 | Move into Ch 26 (C26-R03, C27-R05, C23-R05) |
| SP-8 | Ch 04 uses three decompositions in a confusing order | Reorder and rename (C04-R01, R03, R05) |
| SP-9 | Ch 06 is internally duplicated (two pipelines, three manifest shapes, memory in five places) | C06-R01–R04 |
| SP-10 | TaskEnvelope specification and task lifecycle sit in Ch 19 | Move to Ch 18 (C18-R03, R04; C19-R03–R05) |
| SP-11 | Template elements (double-why openings, empty H2 wrappers, Required-analysis tables, cards, unexplained state-owner tables) | D-30, D-04 |
| SP-12 | The Closing Perspective is unreachable | D-26 |

---

## 6. Major sparse areas

| Area | Gap | Fill (IDs) |
| --- | --- | --- |
| Acceptance engine | Named in 8 chapters, defined nowhere | C02-R05 (criteria), C13-R02 (component, AcceptanceDecision) |
| Intervention | InterventionTask is an orphan; Part IV escalations have no destination | C14-R02, R03, R12 |
| Skill mechanism | No version promise, no runtime path, binding moments unreconciled, no unit comparison | C08-R01, R02, R03, R07, R10 |
| Pack mechanism | Compatibility, governance, and lifecycle missing | C09-R01, R02, R06, R07 |
| Run and task states | Run terminal states get three sentences; task states are absent from Ch 18 | C15-R04, C18-R03, C19-R04 |
| Runtime vs offline adaptation | A core invariant in one paragraph | C25-R04 |
| Governance operating model | Review depth, tiers × change class, exceptions | C26-R01, R02, R04, R05 |
| Event-driven resume | Empty heading since v3.0 | C15-R05 |
| Reconciliation without native keys; Partial | No guidance | C22-R14 |
| Data lineage and privacy | Buried; the privacy promise is barely kept | C23-R06, R10 |
| Paved-road trade-offs; conformance proof | Missing | C07-R09, R14 |
| Glossary | 15 terms; Ch 01 says "full glossary" | WP-A item H |
| Ending | None | C28-R10, R11 |
| Front matter reader paths | Paths skip prerequisites | C01-R21 |

---

## 7. Repeated concepts across the book

R = reinforcement (a new lens, keep); D = redundancy (cut or point).

| Concept | Where taught now | R vs D | Action |
| --- | --- | --- | --- |
| Core thesis | Ch 01 (×5), Ch 02 BOUNDARY RULE, Ch 03 principle, Ch 04, Part VI intro, Closing | Ch 01's internal repeats are D; the others are R | C01-R02, C01-R05 |
| Six gates sequence | Ch 02; Ch 03 (8 and 9 steps); Ch 04 (8); Ch 15 step 8; Ch 20 `:93`; Ch 22 § Invocation sequence; P-05 | Ch 03 and Ch 20 `:93` are D; Ch 04 and Ch 22 are R once they name the gates | C03-R05, R06; C20-R05; C04-R11; C15-R03; C22-R06; C16-R04(b) |
| Unknown effect | Ch 01, 02, 03, 04, 10, 15, AP-05, 22, 24, App B | Ch 03 table, Ch 15 box, and Ch 04 field list are D; the rest R | C03-R04, C15-R07, C04-R06, C22-R03 |
| Proposal-bound approval | Ch 01; Ch 03 (×2); Ch 14 (×4 plus code); AP-06; Ch 22 Q4 | Ch 03 field list, Ch 14's internal repeats, and Ch 22 Q4 are D | C03-R01; C14-R01, R04, R10; C22-R11 |
| Guardrails ≠ authorization, injected document | Ch 01 Tuesday, Ch 03, Ch 20, Ch 23 | Ch 03 and Ch 23 retellings are D | C03-R03, C23-R02 |
| Defense layers | Ch 03 (7), Ch 20 figure (6) and table (9), Ch 23 (8 + 5), Part VI intro | D with drift | C20-R04, C23-R03, C20-R01 |
| Threat catalog | Ch 20 T-cards; Ch 23 table | D | C23-R04, C20-R07 |
| "Assume compromise" | Ch 20; Ch 23 (×3 plus table row) | D | C20-R01, C23-R01 |
| Retry ownership | Ch 03, AP-04, Ch 22 | Ch 03 is D | C03-R04, C22-R15 |
| End-to-end lifecycle | Ch 03, Ch 04, Ch 15, Ch 20 | Ch 03 and Ch 20 are D; Ch 04 (overview) and Ch 15 (detail) stay | C03-R06, C20-R05 |
| Run API | Ch 04, Ch 15, Ch 14 `:operatorAction` | D | D-03 |
| RunManifest | Ch 03 table, Ch 04, Ch 27, App C | D with drift | C03-R13, C04-R07, C27-R01, D-27 |
| Event envelope and outbox | Ch 04 (×2), Ch 15, Ch 22 | D | C04-R09, C15-R05, D-16 |
| Capability-envelope proof | Ch 18 and Ch 21, byte-identical | D | C18-R01, C21-R07 |
| TaskEnvelope | Ch 18 (4 shapes), Ch 19 (2), App C | D | C18-R04, C19-R03 |
| Handoff | Ch 03, Ch 11, Ch 18, three questions | Conflict | D-06 |
| Part IV pattern descriptions | Prose, How-X card, P-card, App A | ReAct ×4 is D; others appear twice | D-04 |
| Discovery ≠ permission | Ch 02 P5, Ch 05, Ch 08, Ch 11, Ch 19, Ch 22, AP-12, Ch 20 Q3 | R (new instances), except Ch 20 Q3 | C20-R11; pointers C05-R15, C19-R15, C22-R16 |
| Test layering | Ch 07 figure and text; Ch 25 (×2) | D | C07-R06, C25-R06 |
| Debugging method | Ch 07, Ch 24, Ch 03 (boundary-specific) | Ch 07 is D; Ch 03 is R | C07-R07, C24-R04 |
| Metric catalog | Ch 24 scorecard, Ch 25 `:432` | D | C25-R05, C24-R02 |
| Judge discipline | Ch 13 (×4), Ch 25 (×6) | D until the run-vs-release distinction is stated | C13-R05, C25-R02 |
| Gateway table | Ch 01, Ch 19 | D | C19-R01 |
| Policy-first model routing | Ch 19, Ch 28 (×3) | D | C28-R07 |
| Authorization-scoped caching | Ch 06, Ch 19, Ch 21 (×3), Ch 28 (×3) | D | Ch 21 canonical: C06-R10, C19-R01, C21-R02, C28-R08 |
| Cost per verified success | Ch 10, Ch 28 (12 occurrences) | Item 10 and the box are D; checklist and Q recall are R | C10-R06, C28-R05 |
| Credentials API | Ch 21, 22, 23 | D | C22-R07, C23-R07 |
| Sandbox lease | Ch 22, 23 | D | C22-R07 |
| Governance record and inventory | Ch 23, 25, 26, 27 | Misplaced | C26-R03, C23-R05, C27-R05, C25-R13 |
| Release content list | Ch 27 (×6) | D | C27-R09 |
| Regional recovery | Ch 14, Ch 15, Ch 27 (×3) | D | C27-R07, C14-R08, C15-R09 |
| Learning loop | Ch 25, Ch 27 Learn row | D | C27-R04 |
| Little's Law | Ch 28 (×3, one wrong), App L | D and an error | C28-R01, R06 |
| Multi-agent justification rule | Ch 18 (×7, verified) | Four statements D; checklist and Q R | C18-R02, R06, R07 |
| Intersection rule | Ch 21 (×5, verified) | D | C21-R02 |
| Memory | Ch 06 (×5), P-04, AP-13, T-06 | Ch 06 internal D; P-04 conflicts | C06-R04, C16-R04(b) |
| Monday–Friday stories | Ch 01, AP-01/05/15, Ch 20, 22, 24, 27, Closing | R | Keep; make the callbacks explicit (C27-R11, C28-R11) |
| Uncertainty / authority tables | Ch 01, Ch 02, Ch 03 (×2), Ch 04, Ch 12 | R (different axes), except Ch 03 § Responsibility map | C03-R10 |

---

## 8. Recommended canonical locations

§ names are current headings; *(new)* or *(renamed)* follow the cited recommendation.

| Concept / record / term | Canonical | Other chapters |
| --- | --- | --- |
| Core thesis | Ch 01 § Start with a demo that genuinely works (end; C01-R02) | Recall in their own framing |
| Control-point gateways | Ch 01 § Each control point answers a different question | Ch 19 points back; its table is deleted |
| State-owner table format | Ch 01 § Which component should own each uncertainty (C01-R05) | Use it without re-explaining |
| Six gates / deterministic shell | Ch 02 § One proposal, six gates | Name "the six gates (Chapter 2)" and expand only one gate (Ch 22 Commit/Verify) |
| Acceptance criteria | Ch 02 § Deterministic acceptance | Recall |
| Acceptance engine / AcceptanceDecision | Ch 13 *(new)* § The acceptance decision | Ch 10, 12, 15, 18, AP-07 point here |
| Run terminal states | Ch 15 § Terminal correctness (moved under § The lifecycle of a durable run) | Ch 18 reuses the names; Ch 19 maps onto Ch 18 |
| Step status / model decision | Ch 03 § The request is bounded… (status); Ch 10 § Acceptance and failure semantics (decisions, stop reasons) | Ch 02 JSON uses `proposed_action` |
| AgentRuntime, AgentStepRequest/Result | Ch 03 § Why the SDK sits behind AgentRuntime | Ch 04 places it; Ch 07 cites it; App C uses these names |
| Restart and replaceability tests | Ch 03 *(new)* § Two tests for the boundary | Ch 15 recalls the restart test |
| Planes; one writer per record | Ch 04 § Seven planes, one owner per record *(renamed)* | Use the plane names (§11) |
| Record index (owner, plane, chapter) | Ch 04 § The contracts that hold the platform together (C04-R04 table) | App C mirrors the "Defined in" column |
| Base Run API (including `:update`, `:fork`) | Ch 04 § Run API | Ch 15 adds operations only; Ch 14 uses it; Ch 24 explains fork |
| RunManifest | Ch 04 § RunManifest | Ch 03 lists its framework pins; Ch 27 relates it to ReleaseManifest |
| Event envelope | Ch 04 § Event contract | Ch 15, Ch 22 point here |
| Physical stores | Ch 04 § Where each kind of state belongs | Ch 06, Ch 24 point here |
| Trust-boundary table | Ch 04 § Trust boundaries | Ch 20 cites it |
| Global control tier / regional execution cell | Ch 04 *(new)* § Global control and regional cells | Ch 27 holds the operational view |
| LLM Gateway contract | Ch 04 *(new)* § What the LLM Gateway enforces (C04-R19) | Ch 01, 03, 07 recall; Ch 19 bridges |
| Model-routing economics | Ch 28 § Optimize in the order that changes outcomes, item 4 | Ch 11 points here |
| Governed knowledge, Hub, content provenance, index freshness | Ch 05 (§ Reference architecture: the Enterprise Knowledge Hub; § Why provenance determines what you can trust) | Ch 06 Hub client; Ch 27 build provenance |
| ContextManifest, trust tiers, five sources, memory | Ch 06 | P-03, P-04, AP-02, AP-13, Ch 20, Ch 24 recall |
| Paved road, three owners, golden path | Ch 07 | — |
| Skill, discovery ≠ permission, binding moments | Ch 08 § The Skill manifest / § Discovery is not permission | Ch 05, 11, 12, 19, 22, AP-12 apply it |
| Skill Pack, compatibility, install ≠ grant | Ch 09 | Ch 27 Versioned objects (C27-R15) |
| Bounded loop limits; stop ≠ accept | Ch 10 § Keep the feedback loop inside external limits | AP-11, Ch 28 |
| Routing (eligibility first); handoff | Ch 11 § A routing decision cannot grant permission; *(new)* § Handoff transfers accountability | Ch 03 term mapping; Ch 18 implements; Ch 19 federated case |
| Plan IR, compile checks, revision protocol | Ch 12 § Plan IR, § Compile-time checks, *(new)* § Revise without rewriting history | Ch 18 points here |
| "What should be agentic?" selection rule | Ch 12 § What should be agentic? | Ch 16 cites it |
| Approval, intervention, operator control | Ch 14 § Approval contract, *(new)* § Intervention contract | Ch 01/03 preview; Ch 26 tier rows |
| Durable execution, replay, waits | Ch 15 | Ch 14 recalls (workflow integration); Ch 24 separates diagnostic replay |
| Anti-patterns | Ch 17 | Home chapters point (D-29) |
| TaskEnvelope, task lifecycle, joins, cancellation | Ch 18 § Durable child-task contract, *(new)* § Task lifecycle | Ch 19, App C |
| MCP/A2A gateways, FederatedTask, artifact adoption | Ch 19 | Ch 06, 18, 22 point here |
| Detector / policy point / enforcement point; layers; threats; incident lifecycle | Ch 20 | Ch 03 previews; Ch 21–23 deepen |
| Subject/actor/purpose; capability envelope vs credential lease; envelope proof; caching | Ch 21 | Ch 18 points; Ch 23 injects leases |
| Effect protocol, Unknown, receipts, R0–R4, ToolManifest, retry ownership, outbox/inbox records | Ch 22 | Ch 02 glosses; Ch 03, 04, 15 point |
| Containment, kill switch, taint | Ch 23 | Ch 27 Emergency Control points here |
| Causal run trace, span schema, scorecard, debugging method | Ch 24 | Ch 07, 14, 25, P-09, AP-14 |
| Release evaluation records, test layers, learning loop | Ch 25 | Ch 07, 08, 13, 26, 27 |
| Use-case tier, review depth, exceptions, governance record | Ch 26 | Ch 08, 25, 27, 28 |
| Release chain, rollback of assignment, regional recovery | Ch 27 | Ch 04, 14, 15 point here |
| Admission, budgets, BudgetReservation, permits | Ch 28 | Ch 12 points |

---

## 9. Cross-chapter dependency problems (used before defined), prioritized

**High**
1. R0–R4 used in Ch 02 `:734`, Ch 12 `:465`/`:518`, and Ch 21 `:495` before Ch 22 `:714` (map #9, #33, #58). Fixed by C02-R13, C12-R01, C12-R03 (D-01).
2. Ch 16 P-06–P-11 rest on Ch 18–28 mechanisms (map #40–45). Fixed by C16-R01, C16-R04, C16-R10.
3. Ch 15's "The core patterns are now defined" is false (map #39). Fixed by C15-R11.
4. The LLM Gateway is used in Ch 01/03/04/07 and defined in Ch 19. Fixed by C04-R19, C04-R15, C07-R01 (D-08).
5. The acceptance engine is deferred to by Ch 01, 10, and 12 but never defined (map #5). Fixed by C13-R02, C02-R05, C01-R03, C10-R03.
6. The capability envelope is used in Ch 03, 11, 12, 15, and 18 before Ch 21 (map #12, #13, #32, #37, #52). Fixed by C01-R03 (vocabulary definition), C18-R01, and pointers C03-R07, C03-R12, C11-R08, C12-R11, C15-R03.

**Medium**

| Map # / source | Problem | Fix |
| --- | --- | --- |
| #1 | State-owner table format never explained | C01-R05 |
| #3 | Agent Gateway orphan | C01-R10, C19-R07 (D-07) |
| #4 | "Autonomy level" orphan | C01-R12, C02-R07 |
| #5 | Vocabulary pointers wrong | C01-R03 |
| #7 | Gates justified before they are named | C02-R02 |
| #12, #15 | Ch 03 field groups and TaskEnvelope used early | C03-R12, C03-R02 |
| #19, #20 | Ch 04 records listed without owners or pointers | C04-R04 |
| #24 | Adoption code with no prose | D-18 |
| #25 | RunContext orphan | C07-R03 |
| #29 | `side_effect_class` / `min_risk_tier` | C08-R06 |
| #36 | InterventionTask orphan | C14-R02 |
| #52 | Envelope proof before Ch 21 | C18-R01 |
| #61 | Ch 25 cites release bundle and inventory before Ch 26/27 | C25-R13 |
| #62 | ValidationReport orphan | C25-R08 (D-05) |
| #63 | Appendix C contradicts the chapters | WP-A item C |
| Review finding | Ch 19 "canonical local state" defined nowhere | C18-R03, C15-R04 |
| Review finding | Ch 10 relies on Skills and the Tool Gateway implicitly | C10-R07 |
| Review finding | Ch 09 compatibility confused with Ch 27's compatibility | C09-R01 |

**Low.** Map #2, 6, 8–11, 14, 16–18, 21–23, 26–28, 30, 31, 34, 35, 38, 47, 53–57, 59, and 60 are each closed by the pointer recommendations in the owning chapter review. Ch 14's use of durable waits before Ch 15 is accepted, with a forward clause (C14-R11).

**Orphans, all resolved:**

| Orphan | Resolution |
| --- | --- |
| Agent Gateway | D-07 |
| autonomy level | C02-R07 |
| RunContext | C07-R03 |
| ToolIntent | C02-R02 |
| InterventionTask | C14-R02 |
| ValidationReport, EvaluationReport | D-05 |
| AgentManifest | C18-R10 |
| side-effect class | C08-R06 |
| UseCaseRecord | C23-R05 |
| ObservationRecord, DetectionEvent, LearningRecord | C25-R08 |

---

## 10. Chapters or sections to reorder, move, merge, or split

**Topology impact of the whole plan:** none. The book keeps 8 Parts, 28 chapters, and 12 appendices. The Closing Perspective is not counted by `validate_book.py`.

| Candidate | Decision | Rationale | Topology / asset impact |
| --- | --- | --- | --- |
| Ch 16 (map S1) | **Split**: a slim synthesis stays in place, and the 12 cards move to Appendix A (D-04) | Part IV needs a synthesis; the cards are appendix-shaped | None. An optional retitle needs `config/chapter-covers.json` and a cover re-check [J] |
| Move Ch 16/17 after Ch 28 (S1a, S2) | Reject | Breaks the Part structure, renumbers 11 chapters, leaves Part IV without a synthesis | — |
| Merge Ch 16 into App A and delete the chapter (S1b) | Reject | 28 → 27 chapters | — |
| Ch 17 | Keep in place; add Prevented in / Built in lines (C17-R03) | Problem statements survive early reading | None |
| Move Ch 22 to Part IV or I (S6b) | Reject; one framing sentence instead (C22-R03) | The security Part ends at the effect boundary | None |
| Merge Ch 09 into Ch 08 | Reject (C09) | Distinct question; topology | — |
| Move Part III after Part IV | Reject (C07) | Part IV binds to Skills | — |
| Swap Ch 14 and Ch 15 | Reject (C14) | Renumbering cost for little gain | — |
| LLM Gateway, Ch 19 → Ch 04 + Ch 28 | Adopt (D-08) | The contract is architecture; routing is cost | Fig 19-1 retired (`gateway-position`); Fig 19-2 becomes a Ch 28 figure |
| Telemetry implementation Ch 25 → Ch 24; evaluation content Ch 24 → Ch 25 | Adopt | Each chapter owns its own system | None |
| Governance implementation Ch 27/Ch 23 → Ch 26 | Adopt | One job per chapter | None |
| TaskEnvelope and task lifecycle Ch 19 → Ch 18 | Adopt | Local contract before its federated delta | None |
| Handoff comparison table Ch 03 → Ch 11 | Adopt | Canonical home | None |
| Artifact adoption code Ch 06 → Ch 19 (as an example) | Adopt | Federated concern | New example |
| Index freshness Ch 06 → Ch 05 | Adopt | Belongs with provenance | None |
| Baseline stack Ch 27 → App D | Adopt | Duplicate | None |
| Closing Perspective → directly after Ch 28 (top of `09-appendices.md`) | Adopt pending a build check (D-26) [J] | The ending must be reachable | Check H1 handling in the DOCX and LaTeX builders |
| Ch 07 figures | Retire Fig 7-3 (`developer-lifecycle`) and Fig 7-5 (`test-pyramid`) | Duplicate journeys and pyramid | Renumber; remove registry entries or mark them retained |
| Internal reorders | Adopt each chapter's Structural Recommendations: Ch 01, 02, 03, 04, 05, 06, 07, 08, 09, 12, 13, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28 | — | Re-check chapter covers for 03, 16, 19, 22, 23, 26, whose arguments change materially (AGENTS.md) |

---

## 11. Terminology inconsistencies and canonical term decisions

| # | Term family | Canonical decision | Defined in | Notes / IDs |
| --- | --- | --- | --- | --- |
| T1 | Northstar vs Harborlight | Drop Northstar; use "the Harborlight platform", then "the platform" | — | D-20; C01-R07, C03-R16, C10-R13, and the others |
| T2/T27 | Plane, layer, band, cell | **Plane** means ownership domain only. The seven planes are Experience and channels; Agent applications; Runtime and workflow; Knowledge, context, and memory; Gateways and integration; Security and governance; Evaluation and operations. Layers carry no "plane" in their names. Deployment uses **global control tier** and **regional execution cell** | Ch 04 | D-09; C04-R01, R12; C27-R02; C28-R09 |
| T3/T25 | Approval vs authorization | **Approval** is the human, proposal-bound decision (records ApprovalRequest / ApprovalDecision, Approval Service, `/v1/approvals`). **Authorization** is the policy decision (Ch 21) | Ch 14 | D-22 [J] |
| T4 | Gateways | Five control-point gateways: API, **A2A**, LLM, Tool, MCP. Everything else is a proxy or service: egress proxy, Telemetry Collector, content inspection service | Ch 01 | D-07; C23-R12, C24-R01, C21-R04 |
| T5/T28 | Run, workflow, task, activity, step, node | Run ⊃ workflow execution ⊃ nodes → activities / agent steps / child tasks; federated task = child task across a trust boundary | App H | WP-A item H |
| T6 | Authority scope names | **Capability envelope** (scope, identified by `grant_id`) and **credential lease** (proof) | Ch 21 | C21-R03; C11-R08, C12-R11, C18-R10, C17-R09 |
| T7 | Release artifacts | ChangeBundle → ReleaseManifest → EnvironmentBinding → RunManifest | Ch 27 | D-27; C27-R01 |
| T8 | Agent definition | AgentSpec | Ch 04 / 07 | C18-R10, C03-R12 |
| T9 | Step contract | AgentStepRequest / AgentStepResult | Ch 03 | C04-R02, C07-R03 |
| T10 | Guardrail | A probabilistic **detector** only. Ch 05 uses "enforced rule"; Ch 28 "starting limits"; Fig 20-1 "Defense-in-depth layers"; Fig 20-3 "content detector" | Ch 20 | CP-3 |
| T11 | Risk numbering | **Effect risk class R0–R4** (Ch 22); **use-case tier T0–T4** (Ch 26), floored by the most dangerous eligible effect; **change class** (Ch 25). Never bare numbers; one `RiskClass` enum in code | Ch 22 / 26 / 25 | D-01, D-02 |
| T12 | Terminal states | Model decisions: answer, needs_input, invoke_tool (read), proposed_action, delegate. Stop reasons: budget_exhausted, no_progress. Step status: completed, needs_input, proposed_action, failed. AcceptanceDecision: accepted, rejected, escalated. Run states: Ch 15 table. Task states: Ch 18 | Ch 10 / 03 / 13 / 15 / 18 | D-12–D-14 |
| T13 | Effect states | Ch 22's list (including Partial). Appendix B maps absent → Declined, unprovable → InterventionRequired, executing → Executing | Ch 22 | C22-R04; WP-A item B |
| T14 | Proposal pipeline | "The six gates", contained in the "deterministic shell" | Ch 02 | C02-R02, C15-R03, C16-R04(b) |
| T15 | Missing document | The second pay statement (`document_kind: pay_statement`) | Ch 01 case | D-31 |
| T16 | Case identifiers | `MORT-2026-000184`; run `RUN-98217`; agent `mortgage-evidence-agent@0.1.0`; Skill `mortgage.evidence.read@0.1.0`; tools `mortgage.case.read@1` and `mortgage.document.request@1`; policy bundle `policy://mortgage@2026.09`; knowledge snapshot `mortgage-policy@approved-2026.09`; model route `reasoning-standard@4` | — | D-31 [J] |
| T17 | Unlabeled "onboarding" | Retire the supplier thread; move the examples to Harborlight | — | D-21 |
| T18 | Memory taxonomy | Ch 06's working / long-term memory | Ch 06 | C16-R04(b) |
| T19 | Context trust labels | One segment `kind` enum mapped to tiers 1–4 | Ch 06 | C06-R05 |
| T20 | Identity triad | Subject and actor (identities) plus purpose (context) | Ch 21 | C21-R01 |
| T21 | Acceptance vocabulary | Acceptance engine (component), acceptance criteria (specification), AcceptanceDecision (record); not "acceptance gate" | Ch 02 / 13 | C13-R04 |
| T22 | Trace vocabulary | **Causal run trace** for the operational view; **trajectory** for the evaluation view; P-09 retitled | Ch 24 | C24-R06, C16-R04, C16-R08 |
| T23 | Evaluation records | EvaluationResult, ValidationReport, ReleaseGateDecision (Ch 25); PromotionDecision (Ch 27) | Ch 25 / 27 | D-05 |
| T24 | Effect component | Effect Service (component) owning the effect ledger (store) | Ch 22 | C03-R12, C04-R17 |
| T26 | Part titles in Fig 0-1 | The exact Part titles | Front matter | C01-R22 |
| — | Run economics | "Cost per verified successful outcome" (short form "cost per verified success") | Ch 28 | C10-R06 |
| — | Context component | Context Service (its assembler; "Hub client" for the retrieval broker) | Ch 06 | C06-R06 |
| — | Records | RoutingDecision, OwnershipTransfer, CapabilityEnvelope | Ch 11 / 18 / 21 | C11-R12 |

---

## 12. Reconciliation decisions

Each entry lists the conflict, the options, the decision, the rationale, and the recommendations amended. [J] marks a decision the author should confirm in Phase 0.

**D-01 — R0–R4: home and representation.**
- *Conflict:* the Ch 10–13 review proposed moving the class table to Ch 02. The Ch 20–23 and Ch 26–28 reviews keep it in Ch 22 with glosses.
- *Options:* move the table to Ch 02; keep it in Ch 22 with glosses at first use.
- *Decision:* Ch 22 § Risk classes stays canonical. Ch 02 § Scaling the shell (moved by C02-R13) and Ch 12 carry a one-clause gloss. Code uses one `R0`–`R4` enum (C12-R03, C11-R06).
- *Rationale:* Ch 02 is already overloaded, and a gloss removes the dependency problem without moving the table.
- *Amended:* C02-R13, C12-R01, C08-R06.

**D-02 — Three risk scales.**
- *Conflict:* Ch 26 calls its 0–4 tiers "risk classes". Ch 08 was asked to render `min_risk_tier` as a T-tier, but C08-R06 makes it an R-class ceiling. C22-R05's sentence allowed a low-tier use case to hold an R3 tool, which contradicts C26-R01's floor rule. C26-R02 re-listed Ch 25's human-approval list and pointed to a section that C25-R09 deletes. Several reviews wrote "governance tier" or "governance risk tier".
- *Decision:* effect risk class R0–R4 (Ch 22); use-case tier T0–T4 (Ch 26), never lower than the most dangerous eligible effect requires (R3/R4 ⇒ ≥T3; R2 ⇒ ≥T2); change class (Ch 25); review depth = use-case tier × change class. The Skill field is `risk_ceiling: R1`; the RunManifest field is `"risk_tier": "T3"`.
- *Rationale:* each scale has its own subject, and the code semantics (`maximum_risk` as a ceiling) favour an R-class for Skills.
- *Amended:* C07-R15, C08-R08, C16-R04, C25-R08, C26-R01, C26-R02, C22-R05, C04-R07.

**D-03 — Run API ownership and fork.**
- *Conflict:* C04-R08 gave Ch 15 the full operational table and deleted `:update`, `:fork`, and `/audit` from Ch 04. The Ch 14–17 review (C15-R08) keeps a Ch 04 base table with Ch 15 additions. C24-R01 points to Ch 04's `:fork`, which C04-R08 deleted. C14-R02 relies on `:update`.
- *Decision:*
  - Ch 04 owns the one base table: POST (absorbing Ch 15's 202 semantics), GET, events, `:signal`, `:cancel`, `:update`, `:fork`.
  - Only `/audit` is deleted.
  - Ch 15 lists `events:ingest`, `:pause`, `:resume`, `:migrate`, plus the durable semantics of `:signal` and `:cancel`.
  - Ch 14's `:operatorAction` is removed (C14-R09).
  - Ch 24 explains fork; `:forkReplay` is deleted.
- *Rationale:* Ch 04 is the contracts chapter, and two recommendations depend on its endpoints.
- *Amended:* C04-R08.

**D-04 — Pattern catalog and cards.**
- *Conflict:* Ch 14–17 proposed the split. Ch 10–13 wanted P-cards for routing, handoff, planning, and acceptance, or the chapter cards declared the catalog. A plain move would keep a second full description of each pattern. The card policy reached only Ch 10–13 and 18. P-09's name clashed with T22.
- *Decision:*
  - Split Ch 16 (C16-R01–R04).
  - The per-chapter cards, retitled "<Pattern> at a glance", are the canonical pattern summaries book-wide (C10-R04, C11-R05, C12-R05, C13-R03, plus C02-R19, C14-R16, C15-R15, C18-R17). Ch 06's Memory card is dissolved into its H2 (C06-R04).
  - Appendix A cards for patterns that have a chapter card reduce to Use when / Shortcut that fails / one-sentence design / pointer.
  - Routing and handoff, plan compilation, reflection and acceptance, and approval and intervention get obligation-table rows, not new cards (C16-R10).
  - P-09 becomes "Causal run trace".
- *Rationale:* removes one layer of the four-fold repetition without creating a fifth.
- *Amended:* C16-R04, C16-R08, C24-R06. *Added:* C16-R10, C02-R19, C14-R16, C15-R15, C18-R17. [J: Ch 16 retitle]

**D-05 — Evaluation and release record names.**
- *Conflict:* Ch 25 defines EvaluationResult and ValidationReport. Ch 26–28 assumed ReleaseGateDecision. Ch 08 used EvaluationReport and ReleaseDecision. Ch 27 emitted a DetectionEvent that Ch 25 drops. Ch 26 deferred.
- *Decision:* Ch 25 defines EvaluationResult (replacing EvalScore and EvaluationReport), ValidationReport (the evidence), and ReleaseGateDecision (the gate output). Ch 27 defines ChangeBundle, ReleaseManifest, EnvironmentBinding, and PromotionDecision. DetectionEvent, LearningRecord, and ObservationRecord are dropped.
- *Rationale:* define once, in the chapter that produces each record.
- *Amended:* C07-R15, C08-R10, C26-R10, C27-R10.

**D-06 — Handoff.**
- *Conflict:* Ch 03 ("same activity remains accountable"), Ch 11 (accountability changes on acknowledgment), and Ch 18 (atomic transfer, no acknowledgment; Q2 "conversational control transfer") disagree. C03-R19 kept Ch 18's comparison question canonical, but C18-R05 deletes it. No Ch 18 item changed `:handoff` or OwnershipTransfer.
- *Decision:*
  - Ch 11 is canonical. Ch 03 keeps a term mapping (C03-R02's text), and its table moves to Ch 11 (C11-R02).
  - Ch 18's `:handoff` creates a pending transfer that `:accept` commits; OwnershipTransfer gains obligations, deadline, and acknowledgment state.
  - Ch 11 Q4 is the one comparison question; Ch 18 Q2 becomes a cancellation question; Ch 03 Q6 keeps the framework angle.
- *Amended:* C03-R19. *Added:* C18-R16.

**D-07 — Agent Gateway vs A2A Gateway.**
- *Conflict:* C01-R10 recommends renaming Ch 01's row to A2A Gateway but defers to Ch 19. C19-R07 keeps "Agent Gateway" as an umbrella with the A2A Gateway as its "external face".
- *Decision:* one name, the **A2A Gateway** (external peers). Internal delegation decisions belong to the Task Service (Ch 18). "Agent Gateway" leaves the book, including `gateway-roles.gv` and T-12.
- *Rationale:* "Agent Gateway" is an orphan used three times, and the book's own warning is about confusing gateway names.
- *Amended:* C01-R10, C19-R07.

**D-08 — LLM Gateway placement.**
- *Conflict:* map S4 offered Ch 04 or Ch 28. The Ch 18–19 review split the material. Ch 04's review had no receiving item. C28-R07 was conditional. C19-R01 used heading and plane names that C04-R01/R05 remove. C07-R01 and C11-R08 pointed to Ch 19.
- *Decision:* the enforcement contract goes to a new Ch 04 H3 (C04-R19), and routing, the route record, Fig 19-2, and metrics go to Ch 28 item 4 (C28-R07). Ch 19 keeps one bridge sentence.
- *Amended:* C19-R01, C28-R07, C07-R01, C11-R08. *Added:* C04-R19.

**D-09 — Deployment vocabulary.**
- *Conflict:* C04-R12 proposes "global control tier" (or keeping "control plane" as a defined exception). C27-R02 writes "Global control plane".
- *Decision:* **global control tier** and **regional execution cell**; "plane" means ownership domain only.
- *Rationale:* C04-R01 strips "plane" from layer names for exactly this reason. [J: the alternative is "global control plane", defined once in Ch 04]
- *Amended:* C27-R02.

**D-10 — Debugging method.**
- *Conflict:* C24-R04 wanted Ch 07 reduced to a one-line pointer; C07-R07 rewrites Ch 07's list for platform failures.
- *Decision:* Ch 24 is canonical and absorbs Ch 07's steps. Ch 07 keeps platform-failure triage plus one pointer step. Ch 25 and Ch 24 If-fails sections point to it. Ch 03's boundary-specific order stays.
- *Amended:* C24-R04.

**D-11 — Test layering and Fig 7-5.**
- *Conflict:* C25-R06 expected Ch 07 to keep Fig 7-5 pointing to Ch 25; C07-R04/R06 retire it. C07-R06 pointed to the § Evaluation pyramid that C25-R06 deletes.
- *Decision:* one table in Ch 25 § Layer tests from contracts to outcomes; no figure; `test-pyramid` retired.
- *Amended:* C25-R06, C07-R06.

**D-12 — Acceptance.**
- *Conflict:* C02-R05 and C17-R07 list acceptance outcomes "accepted, blocked, needs-input, failed, unknown-effect". C13-R02 defines AcceptanceDecision as accepted / rejected / escalate. C01-R03 points acceptance criteria to Ch 2, 13, and 15; C13-R08 to Ch 2 and 13.
- *Decision:* Ch 02 owns the criteria; Ch 13 owns the engine and the AcceptanceDecision values (accepted, rejected with typed defects, escalated); Ch 15 owns run states. Acceptance is not attempted while an effect is Unknown or input is missing; the run stays waiting. The vocabulary row reads "Chapters 2 and 13".
- *Rationale:* the five-value list is a mix of run states and preconditions (map T12).
- *Amended:* C01-R03, C02-R05, C17-R07.

**D-13 — Step and decision vocabulary.**
- *Conflict:* C02-R09 put `"invoke_tool"` on a mutation proposal. C10-R02 reserves `invoke_tool` for reads and adds `proposed_action`. C03-R09 wanted `delegate` and `budget_exhausted` treated as loop-level additions. `delegate` already exists in `AgentDecision` (verified).
- *Decision:*
  - `AgentDecision.disposition` = answer | needs_input | invoke_tool (read) | proposed_action | delegate.
  - Controller stop reasons budget_exhausted | no_progress are returned as `status: failed` with that `error_code`.
  - `AgentStepResult.status` is Ch 03's enum.
  - The Ch 02 JSON uses `proposed_action`.
- *Amended:* C02-R09, C10-R02.

**D-14 — Run states vs task lifecycle vs remote mapping.**
- *Conflict:* C15-R04 wanted to use "the names in Ch 19" and to be cited by Ch 19. C18-R03 moves those names into Ch 18. C19-R04 maps onto Ch 18.
- *Decision:* Ch 15 owns run states. Ch 18's task lifecycle reuses Ch 15's terminal names and adds task-only states. Ch 19 cites Ch 18.
- *Amended:* C15-R04.

**D-15 — Store table.**
- *Conflict:* map S7 had Ch 06 absorb Ch 04's store table. Both Part II reviews keep it in Ch 04. C24-R01 and C24-R12 pointed audit storage to a Ch 06 row that C06-R03 deletes.
- *Decision:* Ch 04 keeps the physical-store table (C04-R13); Ch 06 keeps five context sources (C06-R03). Inbound pointers go to Ch 04.
- *Amended:* C24-R01, C24-R12; map rows marked superseded.

**D-16 — Outbox and inbox records.**
- *Conflict:* C04-R09 deletes OutboxRecord from Ch 04 ("Chapter 22 defines both"). C22-R13 defined it as "fields per Chapter 4's outbox contract". Each points at the other.
- *Decision:* Ch 04 owns the CloudEvent envelope; Ch 22 owns OutboxRecord and InboxReceipt fields.
- *Amended:* C22-R13.

**D-17 — Envelope proof example.**
- *Conflict:* C21-R07 registers the example for chapters 18 and 21; C18-R01 leaves Ch 18 with prose and no marker.
- *Decision:* `book_chapters: [21]` only.
- *Amended:* C21-R07.

**D-18 — Artifact adoption.**
- *Decision:* Ch 19 is canonical (the Ch 06, 18, and 19 reviews and map S8 agree). The code becomes a registered example; C19-R16's "ideally" becomes mandatory.
- *Amended:* C19-R16.

**D-19 — Ch 20 / Ch 23 division; the "assume compromise" premise.**
- *Conflict:* the map placed the premise in Ch 23. The Ch 20–23 review placed it in the Part VI intro. C26-R03 asked Ch 23 to keep a "Layer 8" sentence that C23-R03 deletes.
- *Decision:*
  - The premise is stated once in the Part VI intro (C20-R01).
  - Ch 20 owns the detector/policy/enforcement split, the 9-layer table, the T-cards (with refusal layers), the worked example, and the incident lifecycle.
  - Ch 23 owns containment mechanisms and its fail-closed table, with no layer list and no threat table.
  - The governance record moves wholly to Ch 26.
- *Amended:* C26-R03.

**D-20 — Northstar and box type.** [J]
- *Decision:* drop Northstar. The 5 NORTHSTAR AT THIS POINT boxes (Ch 04, 06, 08, 27, 28) become WHERE THE MORTGAGE CASE STANDS. Registering that marker in `tools/callouts.py` is optional; unregistered markers keep their own title.
- *Rationale:* two names for one system; no front matter or glossary definition.
- *Amended:* C04-R05. The conditional branches in C01-R07, C03-R16, C10-R13, C14-R15, C15-R02, C15-R13, and C24-R14 resolve to "drop".

**D-21 — Supplier-onboarding thread.** [J]
- *Decision:* retire it (C01-R06, C01-R24, C02-R01, C03-R14). P-02, AP-03, and AP-07 move to Harborlight.
- *Rationale:* promised, never carried; no artifact.
- *Amended:* C09-R04, C16-R04, C17-R11.

**D-22 — Approval terminology.** [J]
- *Conflict:* reviews deferred T3, and several wrote "human authorization" in replacement text.
- *Decision:* "approval" (human, proposal-bound); records ApprovalRequest / ApprovalDecision; Approval Service. "Authorization" is reserved for policy decisions. Rename the code in `approval_gate.py`, `approval_verification.py`, and their tests. Fallback if the rename is declined: keep the record names and still say "approval" in prose.
- *Rationale:* "approval" appears about 250 times against about 20 for "human action authorization"; the API is `/v1/approvals`.
- *Amended:* C14-R04, C12-R06, C26-R06. Replacement wording in C03-R01, C12-R04, C14-R01/R02/R03/R05, and C22-R06 follows this term when applied.

**D-23 — Inline code policy.** [J]
- *Conflict:* AGENTS.md forbids code in `source/parts`; the chapters contain 38 fenced blocks (29 Python, 1 bash, 1 YAML, 7 JSON). C07-R05 asked for a pseudocode exemption. C17 deferred its six anti-pattern blocks. C18-R04 kept the TaskEnvelope code inline.
- *Decision:*
  - (a) No exemption: every Python and bash listing moves to `examples/` with a behavioural test, or is deleted. This covers Ch 07 (C07-R05 as amended), Ch 18 TaskEnvelope (as region `contracts#task`), Ch 17's six blocks (a separate examples work package, after fixing DF-03/DF-04), and Ch 01's four level sketches (convert to examples, or the author records an explicit exemption for deliberately non-runnable sketches).
  - (b) Short JSON and YAML payloads that illustrate a contract (Ch 02 proposal, Ch 08 manifest, Ch 12 Plan IR, Ch 21 decision) may stay inline as data, each followed by a pointer to the registered model that defines it. The Ch 04, 06, and 18 JSON blocks go, per C04-R10, C06-R02, and C18-R04.
- *Amended:* C07-R05, C18-R04.

**D-24 — Duplicate review question (Ch 04 Q2 / Q5 vs Ch 27 Q3).**
- *Conflict:* C04-R12 moves Q5 to Ch 27 and drops Ch 27's duplicate. C27-R14 kept Q3 renamed, and C27-R02's Related said Ch 04's Q stays.
- *Decision:* Ch 27's Q3 becomes Ch 04's moved Q5 (control-tier outage); Ch 04 keeps Q2.
- *Amended:* C27-R14, C27-R02.

**D-25 — BudgetReservation and plan revision.**
- *Conflict:* C12-R11 added "(budget ledger, Chapter 28)" to Ch 12's record row; C28-R15 asks for the row to be replaced with a pointer.
- *Decision:* Ch 28 is canonical and Ch 12 points. Plan revision: Ch 12 is canonical and Ch 18 deletes `plans:revise` (C12-R13, C18-R08 agree).
- *Amended:* C12-R11.

**D-26 — Closing Perspective.** [J]
- *Decision:* adopt C28-R10 and C28-R11. Place it at the top of `09-appendices.md`, before `# PART REFERENCE — APPENDICES`, rebuilt around the Monday–Friday replay with an honest C01–C03 scope line, and list it in the front matter (C01-R26).
- *Validation:* `validate_book.py` counts only `# PART`, `# NN —`, and `# Appendix X —` headings, so the counts hold. Verify that `build_book.py` and `build_latex.py` render an H1 before the appendix divider on its own page, with no chapter cover.

**D-27 — Manifest chain and Skill binding.**
- *Conflict / unowned:* Ch 08/09 requested Skill digests in the RunManifest, the Ch 03 Capabilities row, the Ch 12 pointer, a Ch 15 Snapshot fix, and the Ch 27 row split; no owner picked them up. C04-R07 said the RunManifest "resolves every version", while C27-R01 has it reference the ReleaseManifest.
- *Decision:* the RunManifest references the ReleaseManifest digest and records only what is resolved per run. The ReleaseManifest fixes the eligible Skill and pack set. Each later binding only narrows the earlier one (C08-R03).
- *Amended:* C04-R07. *Added:* C03-R22, C04-R20, C12-R14, C15-R14, C27-R15.

**D-28 — Part IV orientation, merged.** C10-R01, the Part IV half of C09-R09, and C16-R06 edit the same paragraph. Apply this paragraph once:

> Patterns are shortcuts for thinking, but they are only helpful when their boundaries are visible. Every pattern in Chapters 10–15 places a model step inside the platform of Part III: the step receives a resolved slice of Skills and tools (Chapters 8–9), its outputs cross the six gates (Chapter 2), and the framework stays behind AgentRuntime (Chapter 3). Each chapter answers three questions: what the model may decide, what the controller owns, and how the pattern stops and is accepted. The Part starts with the smallest bounded loop, then follows routing, planning, reflection, human review, and durable work. It ends by comparing and combining these patterns, then naming the failure shapes they prevent—several corrected by mechanisms Parts V–VIII build—so a design review can ask not only "what could work?" but also "how would this fail in production?"

*Amended:* C10-R01, C09-R09, C16-R06.

**D-29 — Cross-chapter requests that had no owner.** Added to the owners' files:
- C05-R15 (discovery pointer);
- C22-R16 (Discovery Service cites Ch 08);
- C26-R13 (governance-sources evidence row);
- the anti-pattern pointer lines requested by the Ch 14–17 review (mapping from C17-R03): C05-R16, C06-R14, C10-R14, C13-R12, C18-R18, C21-R11, C22-R17, C24-R17, C27-R16. Ch 14 and Ch 15 already had them (C14-R14, C15-R12).

Additions made under other decisions: C03-R22, C04-R19, C04-R20, C12-R14, C15-R14, C16-R10, C18-R16, C27-R15, and the card items in D-04.

**D-30 — Recurring template elements.** [J]
- (a) **Required-analysis tables (13).**
  - Delete where they restate the prose: Ch 06, 12, 18, 21, 23, 27, 28, and Ch 22's first (C06-R03, C12-R08, C18-R06, C21-R05, C23-R04, C27-R09, C28-R02, C22-R02).
  - Trim where they carry unique rows: Ch 15, Ch 19, Ch 22's second, and Ch 24 (C15-R06, C19-R11, C22-R02, C24-R08).
  - Ch 14's stays.
  - The template stops requiring one. Alternative: delete all 13.
- (b) **State-owner tables (24):** keep them all. They are explained once (C01-R05) and placed after each chapter's framing paragraph. The "or drop" options in C10-R08 and C12-R09 resolve to "keep".
- (c) **Double-why openings:** merge them, per C02-R01, C03-R14, C07-R08, C08-R09, C09-R08, C10-R08, C11-R09, C13-R04, C15-R01, C17-R01, C19-R09, C20-R03, C21-R01, C23-R01, C26-R07.
- (d) **Generic EVIDENCE BOUNDARY boxes:** replace them with a claim row (C10-R10–C13-R10).
- (e) **Review sections:** use ✓ checklist items and a "Strong answer" header book-wide (C05-R12, C03-R18).
- (f) **"A sensible place to start":** add a one-sentence lead and no empty H2 wrapper (C08-R12, C10-R12, C14-R10, C21-R07, C22-R04, C23-R09, C27-R13, C28-R12).
- (g) **Opening boxes:** every chapter has a case box and THE DESIGN CHOICE (C07-R08, C20-R08, C26-R11).
- (h) **Catalog stock phrasing:** remove it (C16-R04, C17-R04, C20-R07).

**D-31 — Case continuity after C03.**
- *T15:* use the second pay statement everywhere. C01-R04 lists the eight example and test files. C02-R04, C03-R17, C14-R15, and C15-R13 cover their chapters. The remaining `04-part-iv.md:382` and `:1711` and the `06-part-vi.md` occurrences are mechanical edits in the Part IV and Part VI PRs.
- *Roadmap labels:* from Ch 04 onward, case boxes are labeled as the target design (C01-R24, C03-R15, C24-R11).
- *Identifiers:* §11 T16 [J].
- *Part IV cumulative case thread* (C13-R11): optional [J].

**D-32 — Heading renames that break inbound "§" pointers.** When a recommendation renames, merges, or deletes a heading, the implementer updates every inbound pointer. Known cases:

| Old § | New § | Inbound pointers fixed |
| --- | --- | --- |
| Ch 25 Evaluation pyramid | Layer tests from contracts to outcomes | C07-R06, C08-R08 |
| Ch 25 Automate only when regressions are contained | Close the loop without handing control to the model | C26-R02 |
| Ch 25 A safe improvement loop starts with evidence | A release gate starts with evidence | — |
| Ch 23 Scoped operational kill switch | Stop new risky work without abandoning effects | C08-R08 |
| Ch 27 Rollback and active runs | Roll back assignment, not history | C08-R08; still to fix in C09-R02(b) and C15-R09 when applying |
| Ch 22 The lifecycle of an external effect | A reliable protocol for changing the outside world | C18-R14 |
| Ch 06 State taxonomy and storage (audit row removed) | Ch 04 § Where each kind of state belongs | C24-R01, C24-R12 |
| Ch 20 Respond as if the model can be compromised | Respond to an incident from evidence, not from the model's account | — |
| Ch 21 Three identities every decision should preserve | Subject, actor, and purpose | — |
| Ch 04 A practical reference architecture | From planes to deployable layers | C19-R01 |
| Ch 12 Replanning contract | Revise without rewriting history | — |
| Ch 28 Optimize the whole journey | Measure the whole journey | — |
| Ch 28 Illustrative starting guardrails | Illustrative starting limits | — |

---

## 13. Defects beyond flow found during review

**Code and examples that contradict the text**

| ID | Defect | Fix |
| --- | --- | --- |
| DF-01 | `examples/foundations/effect_idempotency.py` releases the key on any exception; `test_failure_does_not_poison_the_key` asserts a downstream 500 is retryable. This is AP-05 (verified) | C22-R04 |
| DF-02 | Ch 13 inline evaluator–optimizer: `if evaluation.accepted: return`, no deterministic check first, raises instead of escalating (verified) | C13-R01 |
| DF-03 | AP-05 code: "genuinely absent; now safe to retry" after a null lookup (verified `04-part-iv.md:1756–1764`) | C17-R05 |
| DF-04 | AP-06 code uses the proposal digest as the idempotency key; prose (payment) and code (evidence package) disagree | C17-R06 |
| DF-05 | `routing_handoff.py` docstring "authority transfer"; inline `DeterministicRouter` lacks `@dataclass`, has unused imports, uses integer risk | C11-R06 |
| DF-06 | `AgentDecision` lacks `proposed_action`; `ReActEngine` raises instead of returning typed outcomes; Ch 02's JSON `"propose_effect"` matches no enum | C10-R02, C02-R09 |
| DF-07 | Risk is an integer 0–4 in `contracts.py` (PlanNode, SkillRequirement), `plan_compilation.py`, and the router, but "R1" in prose | C12-R03, C11-R06 |
| DF-08 | `skills_registry.py`: `status` included in the digest; 4 states vs 6. Ch 09's inline pack excerpt calls undefined `_semver_key` | C08-R05, C09-R05 |
| DF-09 | `mlflow_trajectory_evaluation.py` uses a model judge for "authorized trajectory"; `mlflow_evaluation.py` reports means only | C25-R11 |
| DF-10 | Ch 14 inline HumanActionAuthorizationRequest is a fourth divergent shape with a second `proposal_hash` | C14-R10 |
| DF-11 | Ch 06 has three ContextManifest shapes | C06-R02 |
| DF-12 | Ch 27 `compatible()` types a worker as a ReleaseManifest; the attestation check compares identity strings while the prose says "verify signatures" | C27-R13 |
| DF-13 | Ch 28 admission permit raises, with no defer path, contradicting the `quotas:acquire` dispositions | C28-R12 |
| DF-14 | Ch 23 kill-switch excerpt carries unrelated RecoveryObjectives; the URL check returns addresses without requiring their use (DNS rebinding) | C23-R09, C23-R13 |
| DF-15 | Ch 18 and Ch 21 envelope code is byte-identical (verified with `diff`) | C18-R01, C21-R07 |
| DF-16 | Ch 01's only listing is Ch 03's contract; C01 is never shown; `examples.json` `book_chapters` is wrong | C01-R01 |
| DF-17 | Ch 04's `[[EXAMPLE:contracts]]` shows step and plan contracts, none of Ch 04's | C04-R10 |
| — | Checked and not defective: `governed_tool_gateway.py` marks any exception Unknown, which is conservative and correct (the check C22-R04 asked for) | — |

**Citation-scope overreach (AGENTS.md § Citation safety)**

| ID | Overreach | Fix |
| --- | --- | --- |
| DC-01 | Ch 14 attributes its hashing and recheck guidance to R15 beyond scope | C14-R13 |
| DC-02 | Ch 15 recovery-objective claim on R02/R04 | C15-R10 |
| DC-03 | Ch 18 R28 overclaim; R33 omitted | C18-R12 |
| DC-04 | Ch 19 "MLflow 3.15.0 introduced" MCP Registry, uncited | C19-R06 |
| DC-05 | Ch 21 R06/R09/R10 misaligned with claims | C21-R09 |
| DC-06 | Ch 22 R03/R04 do not support "no retry on unknown"; "absent" undefined | C22-R12 |
| DC-07 | Ch 23 R17/R18/R39 support no claim; R42 listed without a claim | C23-R10 |
| DC-08 | Ch 24 MLflow 3.15.2 tracing default beyond R21 | C24-R15 |
| DC-09 | Ch 25 3.15.2 features beyond R21; AgentDojo uncited; Phoenix without R23 | C25-R12, C25-R06, C25-R05 |
| DC-10 | Ch 27 cites NIST SP 800-61 [R42] for regional recovery | C27-R06 |
| DC-11 | Ch 10–13 cite R13 with no claim; Ch 11 cites R07 | C10-R10–C13-R10 |
| DC-12 | Appendix E names AutoGen, AgentBench, GAIA, SWE-bench, τ-bench, and AgentDojo with no registry entries | WP-A item E |
| DC-13 | Ch 08 "Agent Skills" (SKILL.md) mention only with a registered source | C08-R11 [J] |
| DC-14 | Ch 20 incident lifecycle uncited; add R42 within scope | C20-R10 |

**Figure–prose contradictions**

| ID | Figure | Fix |
| --- | --- | --- |
| DG-01 | Fig 0-1 labels ≠ Part titles | C01-R22 |
| DG-02 | Fig 1-3 vs 4-1 "same picture"; Channels band "I" | C01-R11, C04-R03 |
| DG-03 | Fig 4-1 band names; Skills node | C04-R01 |
| DG-04 | Fig 4-2 agent fetches its own context; eligibility after the proposal | C04-R11 |
| DG-05 | Fig 5-2 "policy-to-guardrail" | C05-R01 |
| DG-06 | Fig 7-1/7-2 use RunContext and ToolSpec; Fig 7-1 lacks domain owners; Fig 7-4 stages ≠ table; Fig 7-3/7-5 retired | C07-R02–R04 |
| DG-07 | Fig 8-1 "semantic, permissive" | C08-R04 |
| DG-08 | Fig 10-1 edge "stop?" | C10-R03 |
| DG-09 | Fig 11-1 omits the eligibility stage | C11-R04 |
| DG-10 | Fig 13-1 judge before checks; "promotion" vocabulary | C13-R06 |
| DG-11 | Fig 14-1 intervention drawn as operator control | C14-R03 |
| DG-12 | Fig 16-1 leaves ≠ cards | C16-R05 |
| DG-13 | Fig 17-2 "capability lease" | C17-R09 |
| DG-14 | Fig 18-1 labels off the case | C18-R09 |
| DG-15 | Fig 19-1 duplicates Fig 1-4 with drift | C19-R01 |
| DG-16 | Fig 20-1 6 vs 9 layers; Fig 20-3 guardrail as the refusing gate | C20-R04, C20-R06 |
| DG-17 | Fig 22-1 approval before Reserved | C22-R06 |
| DG-18 | Fig 25-2 Approve "human"; Fig 25-3 runtime lane ≠ prose | C25-R08, C25-R04 |
| DG-19 | Fig 26-1 tiers called "risk class"; off-thread domains | C26-R01, C26-R11 |
| DG-20 | Fig 27-1 "resume by risk tier" | C27-R07 |
| DG-21 | Fig 28-1 verify → degrade edge | C28-R13 |

**Inline code against AGENTS.md (38 blocks in chapter prose)**

| Location | Blocks | Fix |
| --- | --- | --- |
| Ch 01 | 4 Python sketches | Unowned; D-23(a) [J] |
| Ch 02 | 1 JSON | D-23(b) |
| Ch 04 | 2 JSON, 1 Python | C04-R10 |
| Ch 06 | 1 JSON, 2 Python | C06-R02; C06-R07 / C19-R16 |
| Ch 07 | 1 Python, 1 bash | C07-R05 |
| Ch 08 | 1 YAML | D-23(b) |
| Ch 09 | 1 Python | C09-R05 |
| Ch 11 | 1 Python | C11-R06 |
| Ch 12 | 1 JSON | D-23(b) |
| Ch 13 | 1 Python | C13-R01 |
| Ch 14 | 1 Python | C14-R10 |
| Ch 17 | 6 Python | D-23(a), WP-X |
| Ch 18 | 1 JSON, 2 Python | C18-R04, C18-R01 |
| Ch 19 | 2 Python | C19-R03, C19-R06 |
| Ch 21 | 1 JSON, 1 Python | D-23(b); C21-R07 |
| Ch 22 | 1 Python | C22-R04 |
| Ch 23 | 2 Python | C23-R09 |
| Ch 27 | 2 Python | C27-R13 |
| Ch 28 | 1 Python | C28-R12 |

The bash and text blocks in Appendices I and J are maintainer content; see WP-A item I.

---

## 14. Highest-priority improvements (ranked)

| Rank | Improvement | IDs |
| --- | --- | --- |
| 1 | Make the code stop teaching the opposite of the book | DF-01 C22-R04; DF-02 C13-R01; DF-03 C17-R05; with DF-06/DF-07 C10-R02, C12-R03 |
| 2 | Settle "handoff" | D-06: C11-R01–R03, C03-R02, C18-R05, C18-R16 |
| 3 | Fix "guardrail" everywhere the book contradicts itself | C20-R02, R04, R06; C05-R01; C28-R04; C07-R01; C01-R22 |
| 4 | Make the three risk scales explicit and related | D-01, D-02: C02-R13, C12-R01, C22-R05, C26-R01, C26-R02, C08-R06 |
| 5 | Define the acceptance engine and the intervention contract; one run-state table | C02-R05, C13-R02, C14-R02, C14-R03, C15-R04, C18-R03 |
| 6 | Turn Ch 16 into a real Part IV synthesis; move the cards to Appendix A; fix Ch 15's false hand-off | C16-R01–R05, R10; C15-R11; D-28 |
| 7 | Make Ch 04 the map | C04-R01–R08, R19, R20 |
| 8 | Cut Ch 03's pre-teaching into one framework-boundary section | C03-R01–R08 |
| 9 | Make Ch 22 one argument with the canonical Unknown | C22-R01, R03, R10, R04 |
| 10 | Split Ch 20 and Ch 23 cleanly | C20-R01, R07, R08, R10; C23-R01–R04 |
| 11 | Rebalance Ch 24 and Ch 25 (decision-centric span schema; evaluation in its own chapter) | C24-R01, R02, R04; C25-R01, R02, R04, R05, R08 |
| 12 | Fill Ch 08/09's missing mechanism | C08-R01, R02, R03, R05, R06, R07; C09-R01, R02 |
| 13 | Give Ch 26 its implementation and exceptions; one release record chain in Ch 27 | C26-R02, R03, R05; C27-R01, R05; D-05 |
| 14 | Give the book an ending and fix Ch 28's central quantitative model | C28-R10, R11, R01 |
| 15 | Restore case continuity and back-references | C01-R01, R04 (+ examples), D-20, D-21, D-31; C01-R03, R09; C07-R01; C17-R03 |

---

## 15. Prioritized implementation plan

**Conventions.**
- [J] = author judgement; [M] = mechanical once Phase 0 is settled.
- One PR per Part, each based on `main` (no stacked PRs). Each PR follows AGENTS.md: fill in the PR template, run all validators, update the changelog.
- **Moves across Parts** are executed entirely in the receiving Part's PR: add at the receiver, delete at the source, add the pointer. The exception is noted in WP-IV. All moved text is recoverable from commit `0361350` or quoted in the reviews, so PR order never loses content.
- Apply edits within a file bottom-up, or re-locate them by quoted text.

### Phase 0 — book-wide decisions for the author to confirm

| # | Decision | Default in this plan |
| --- | --- | --- |
| 0.1 | Northstar (D-20) | Drop; convert the 5 boxes |
| 0.2 | Supplier thread (D-21) | Retire |
| 0.3 | Approval terminology and record rename (D-22) | "Approval"; rename the records and code |
| 0.4 | Deployment term (D-09) | Global control tier / regional execution cell |
| 0.5 | Ch 16 split and title (D-04) | Split; title optional ("Choose and Combine the Part IV Patterns") |
| 0.6 | Card policy book-wide (D-04) | Adopt "<Pattern> at a glance" |
| 0.7 | Closing Perspective placement (D-26) | Top of `09-appendices.md` |
| 0.8 | Inline code (D-23) | No exemption for Python/bash; Ch 01 sketches converted or exempted explicitly; short contract JSON/YAML may stay |
| 0.9 | Required-analysis tables (D-30a) | Delete or trim per review; stop requiring them |
| 0.10 | Case identifiers (T16, D-31) | The §11 set |
| 0.11 | MLflow version claims (C19-R06, C24-R15, C25-R12) | Verify against the release notes and extend R21's scope, or remove |
| 0.12 | Agent Skills mention (C08-R11) | Only with a registered source |
| 0.13 | Optional ID renames (`rule-as-guardrail`, `policy-to-guardrail`, `guardrail-sequence`) | Caption-only change unless the author wants the renames |

### Phase 1 — shared contracts and code (land first; examples and config only)

Change shared code that several Parts' prose will describe. Examples or regions cited by only one chapter ride with that chapter's Part PR, because `check_examples.py` warns on uncited entries.

1. `examples/contracts.py`:
   - add `proposed_action` to `AgentDecision.disposition` (C10-R02, D-13);
   - add a `RiskClass` R0–R4 enum used by PlanNode and SkillRequirement (C12-R03), optionally renaming `maximum_risk` → `risk_ceiling` (C08-R06);
   - update tests. [M]
2. `examples/patterns/react_engine.py`: typed stop reasons (C10-R02); `plan_compilation.py` adopts `RiskClass` (C12-R03). [M]
3. `examples/foundations/effect_idempotency.py` and its test: Unknown semantics (C22-R04 code part, DF-01). [M]
4. `examples/platform/skills_registry.py`: status outside the digest, six states (C08-R05). The `packs` region (C09-R05) rides with Part III. [M]
5. `pay_statement` replaces `employment_verification` in the 8 example and test files listed in C01-R04. [M]
6. Approval record rename in `approval_gate.py`, `approval_verification.py`, and tests (D-22), if 0.3 is confirmed. [J→M]
7. `config/examples.json`: `contracts` `book_chapters` [1,4] → [3,4] and its docstring (C01-R01). [M]

### Phase 2 — cross-cutting rules applied inside every Part PR

These are mechanical once Phase 0 is settled.
- **Terminology:** apply §11 in every chapter touched.
- **T15 missing document; Northstar; case identifiers.**
- **Back-reference pointers:** the "(Chapter N)" recalls listed in each review.
- **D-32 inbound pointer fixes.**
- **Template rules:** D-30 (c)–(h).
- **Run `make diagrams`** after any `.gv`/`.mmd` edit, and `make chapter-covers` after any cover-spec edit.

### Phase 3 — one work package per Part

Recommendation IDs are listed in apply order: structure first, then definitions and rewrites, then terminology and pointers, then template sections, then examples and diagrams. "→" marks a dependency on another work package.

**WP-FM — Front matter and Part I orientation** (`00-front-matter.md`, `01-part-i.md:1–6`). Can travel with WP-I.
1. Structure: C01-R27 [J], C01-R22 (with the `book-map.gv` labels).
2. Rewrites: C01-R21, C01-R23, C01-R24, C01-R25, C01-R20.
3. Template: C01-R26 (list the Closing Perspective → WP-VIII/D-26).

**WP-I — Part I (Ch 01–03)**
- **Ch 01.** Structure: C01-R13, R02, R05, R06. Pointers: R01 (→ Phase 1 item 7), R03, R04, R07, R08, R09, R10 (A2A rename, `gateway-roles.gv`), R11 (`system-overview.gv`), R12, R14–R18.
- **Ch 02.** Structure: C02-R01, R02, R07, R13 (with the gloss). Rewrites: R03, R05, R06, R08, R09 (→ Phase 1 item 1), R10, R04. Template: R11, R12, R14–R18, R19.
- **Ch 03.**
  1. Structure: C03-R08, R11, R10, R14, R06.
  2. The consolidated "Where the framework meets the rest of the platform" section: R01, R03, R04, R05, R07. C03-R02 and R19 are applied in WP-IV (they move with the handoff table).
  3. Definitions: R09, R12, R13, R22.
  4. Case: R16, R17, R15.
  5. Template: R18, R20, R21.

**WP-II — Part II (Ch 04–06)**
- **Ch 04.**
  1. C04-R05 (order; case box per D-20), R01 (with `reference-architecture.gv`), R03, R12.
  2. R02, R04, R06, R07, R08, R09, R11 (with `request-sequence.mmd`), R13.
  3. R19: receives the LLM Gateway contract and deletes the Ch 19 source text (`05-part-v.md:554`, `:569–581`, `:593`).
  4. R20.
  5. R10 (the `platform` example region with RunManifest/ArtifactRef/CloudEvent and tests; → Phase 1 item 1).
  6. R14–R18.
- **Ch 05.** C05-R03, R05 (Hub move), R04, R02, R01 (`policy-to-guardrail.gv`), R06 with R15, R08 (receives freshness from Ch 06), R07, R09–R14, R16.
- **Ch 06.** C06-R08, R03, R01 (`context-pipeline.gv` if labels change), R04, R05, R06, R02 (new `context-manifest` example), R10, R09, R11, R12, R14, R13 (no-op). C06-R07 is executed in WP-V.

**WP-III — Part III (Ch 07–09)**
- **Ch 07.**
  1. C07-R13, R08, R04 (retire `developer-lifecycle` and `test-pyramid` in `config/diagrams.json`; relabel `dx-golden-path.gv`).
  2. R01, R02 (`developer-platform.gv`), R03 (`portability.gv`), R10, R09, R06, R05 [J per D-23].
  3. R07, R14 (new `adapter-conformance` example), R11, R12, R15.
- **Ch 08.** C08-R09, R07, R01, R02, R03, R04 (`skill-resolution.gv`), R05 (→ Phase 1 item 4), R06, R08, R10, R12, R11 [J], R13, R14.
- **Ch 09.** C09-R08, R01, R03, R06, R07, R02, R04 (retired branch), R05 (`packs` region), R09, R10.

**WP-IV — Part IV (Ch 10–17).** Includes the Part IV orientation (D-28) and, as the one exception to the receiver rule, the Ch 16 → Appendix A move.
- **Orientation:** the D-28 paragraph, one edit, covering C10-R01, C16-R06, and the C09-R09 Part IV half.
- **Ch 10.** C10-R08, R04, R02 (→ Phase 1 items 1–2), R03 (`pattern-react.gv`), R05, R06, R07, R09, R10, R12, R13, R14. C10-R11 is applied through C16-R10.
- **Ch 11.**
  1. C11-R09.
  2. R02 (receives the table from Ch 03 and applies C03-R02 and C03-R19 in `01-part-i.md`), R01, R03, R05, R07.
  3. R04 (`pattern-routing.gv`), R08, R06 (router example; docstring), R10, R11, R12.
- **Ch 12.** C12-R09, R08, R02, R04, R06, R07, R01, R03 (→ Phase 1 item 2), R05, R10, R11, R12, R14. C12-R13 is executed in WP-V.
- **Ch 13.** C13-R04, R02, R07, R05, R03, R06 (`pattern-reflection.gv`), R01 (new `evaluator-optimizer` example), R08 (applied in WP-I), R09–R12.
- **Ch 14.** C14-R01, R03 (`pattern-hitl.gv`), R02, R04 [J per D-22], R05, R06, R07, R08, R09, R10, R16, R11–R15.
- **Ch 15.** C15-R01, R06, R03, R14, R04, R05, R02, R07, R08, R09, R10, R11, R15, R12, R13.
- **Ch 16.** C16-R07, R01, R05 (`pattern-decision-tree.gv`), R02, R03, R08, R09; R04 and R10 (Appendix A rebuild in `09-appendices.md`).
- **Ch 17.** C17-R01, R02, R08, R03, R05, R06, R07, R09 (`anti-ambient-authority.gv`), R04, R10, R11. R12 goes to WP-A. Moving the six code blocks to examples is WP-X [J].
- **Mechanical T15** fixes at `04-part-iv.md:382` and `:1711`.

**WP-V — Part V (Ch 18–19)**
- **Ch 18.**
  1. C18-R07, R06, R02, R17, R03 (receives the lifecycle from Ch 19), R04 (receives the field-group table; `contracts#task` region), R01 (delete the code), R16, R05, R08 (deletes `plans:revise`, closing C12-R13).
  2. R09 (`supervisor-worker.gv`), R10–R15, R18.
- **Ch 19.**
  1. C19-R09.
  2. C19-R01(a) and (d): delete Fig 19-1 and the table; retire `gateway-position`; add the bridge. Parts (b) and (c) are executed in WP-II and WP-VIII.
  3. R03, R05, R04, R02, R07, R08, R06, R10, R11, R13, R15.
  4. R16: receives the adoption code from Ch 06 as a new `artifact-adoption` example and deletes `02-part-ii.md:865–910` (C06-R07).
  5. R12, R14.

**WP-VI — Part VI (Ch 20–23)**
- **Orientation:** C20-R01.
- **Ch 20.** C20-R03, R08, R04 (`security-depth.gv`), R02, R05, R06 (`guardrail-sequence.mmd`), R07 (receives the T-08/T-16 rows from Ch 23), R10, R09, R11, R12.
- **Ch 21.** C21-R01, R02, R03, R05, R04, R06, R08, R07 (new `capability-envelope` example, `book_chapters` [21]), R09, R10, R11.
- **Ch 22.** C22-R01, R02, R03, R08, R05, R06 (`effect-lifecycle.gv`), R07, R09, R13, R14, R15, R16, R04 (prose part; code in Phase 1), R10, R11, R12, R17. Mechanical T15 fixes in `06-part-vi.md`.
- **Ch 23.** C23-R01, R02, R03, R04, R06, R08, R07, R05, R12, R09 (new `egress-url` and `kill-switch` examples), R13, R10, R11.

**WP-VII — Part VII (Ch 24–25)**
- **Orientation:** C24-R13.
- **Ch 24.**
  1. C24-R03.
  2. R01: receives the telemetry implementation from Ch 25 and deletes it there.
  3. R02, R04 (absorbs Ch 07's debugging steps), R05, R06, R07, R08, R10, R12.
  4. R09, R11, R14, R15 [J], R16, R17.
- **Ch 25.**
  1. C25-R03 (order), R01 (deletion side), R10, R02, R05, R06, R04 (`runtime-offline.gv`), R09, R08 (`learning-loop.gv`), R07, R14, R15.
  2. R11 (example change: `forbidden_tool_absent` scorer), R12 [J], R13.

**WP-VIII — Part VIII (Ch 26–28) and the Closing Perspective**
- **Orientation:** C26-R12.
- **Ch 26.**
  1. C26-R07, R08.
  2. R01 (`governance-model.gv`), R06, R02, R04, R05.
  3. R03: receives Ch 27's governance implementation and Ch 23's field list, and deletes it in Ch 27 (C27-R05).
  4. R13, R09, R10, R11.
- **Ch 27.**
  1. C27-R09, R01, R15, R08, R04, R05 (deletion side), R02, R03 (moves the stack to Appendix D), R07 (`release-recovery.gv`), R06, R10, R11, R12.
  2. R13 (new `release-compatibility` and `release-attestation` examples), R14 (receives Ch 04's Q5 and deletes it there, closing C04-R12), R16.
- **Ch 28.**
  1. C28-R02, R01, R03.
  2. R07: receives the routing material, Fig 19-2, and metrics from Ch 19 and deletes them there.
  3. R05, R06, R08, R04, R09, R13 (`reliability-economics.gv`), R14, R15, R12 (new `admission-permit` example).
  4. R10, then R11: the Closing Perspective move and rewrite in `09-appendices.md` [J per D-26].

**WP-A — Appendices.** This consolidates requests that had no reviewer.

| Item | Change | Source |
| --- | --- | --- |
| A | Rebuild per C16-R04 and C16-R10 (pairing table, Built-in chapters, Part IV pattern rows) | Executed in WP-IV |
| B | Add an Anti-pattern column; map effect states (absent → Declined, unprovable → InterventionRequired, executing → Executing) | C17-R12; C22 Cross-Chapter Duplication |
| C | Align with the chapters: RunManifest and ReleaseManifest rows (C27-R01); AgentStepRequest/Result (C03); TaskEnvelope (C18-R04); Effect Service owner (T24); approval records (D-22). Add a "Defined in" column matching C04-R04. Add the missing contracts: Plan IR, SkillManifest, SkillPackManifest, PolicyDecision, CredentialLease, MemoryRecord, ChangeBundle, RoutingDecision, OwnershipTransfer, AcceptanceDecision, EvaluationResult, ValidationReport, ReleaseGateDecision | Map §8 |
| D | Absorb the Ch 27 baseline stack (C27-R03); merge the two overlapping tables; settle the MLflow MCP Registry citation (C19-R06); keep the A2A AgentSkill and Skills-over-MCP distinction in sync with C08-R11 | Map §7.2 |
| E | Register sources for the named research systems or soften the claims | DC-12 |
| H | Expand the glossary: every term in Ch 01's vocabulary table; the five gateways; RunManifest, ReleaseManifest, ChangeBundle, EnvironmentBinding; capability envelope and credential lease; TaskEnvelope, FederatedTask; the run/workflow/node/activity/step/child-task hierarchy (T5, T28); effect risk class, use-case tier, change class; approval; plane, layer, cell; causal run trace and trajectory; AcceptanceDecision. No Northstar entry. This makes C01-R03's "Appendix H defines further terms" true | — |
| I | Move maintainer content (C01-R27; § Corrections and closure notes) [J] | — |
| J | Align its 12-layer list with C04-R01's layer names, or decide whether J belongs in the reader edition [J] | — |
| K | Check the generator's category for R14 (map §8) | — |
| L | Keep the formulas; Ch 28 points here (C28-R01, R06) | — |

### Phase 4 — examples, diagrams, and registry work

- **New examples**, each registered in `config/examples.json` with a behavioural test and riding with its Part PR:

  | Example | From |
  | --- | --- |
  | `contracts#platform` | C04-R10 |
  | `contracts#task` | C18-R04 |
  | `context-manifest` | C06-R02 |
  | `adapter-conformance` | C07-R14 |
  | Ch 07 SDK builder (optional) | C07-R05 |
  | `skills-registry#packs` | C09-R05 |
  | router region | C11-R06 |
  | `evaluator-optimizer` | C13-R01 |
  | `artifact-adoption` | C19-R16 |
  | `capability-envelope` | C21-R07 |
  | `egress-url`, `kill-switch` | C23-R09 |
  | `release-compatibility`, `release-attestation` | C27-R13 |
  | `admission-permit` | C28-R12 |
  | Ch 17 anti-pattern/correction pairs (WP-X) | D-23 |
  | Ch 01 level sketches | [J] |

- **Retire diagrams:** `developer-lifecycle`, `test-pyramid`, `gateway-position`. Remove them from `config/diagrams.json` or mark them retained.
- **Edit diagram sources** (then run `make diagrams` and update checksums and captions): `book-map`, `gateway-roles`, `system-overview`, `reference-architecture`, `request-sequence`, `policy-to-guardrail`, `context-pipeline` (if needed), `developer-platform`, `portability`, `dx-golden-path`, `skill-resolution`, `pattern-react`, `pattern-routing`, `pattern-reflection`, `pattern-hitl`, `pattern-decision-tree`, `anti-ambient-authority`, `supervisor-worker`, `security-depth`, `guardrail-sequence`, `effect-lifecycle`, `runtime-offline`, `learning-loop`, `governance-model`, `release-recovery`, `reliability-economics`.
- **Chapter covers:** re-check `config/chapter-covers.json` labels for Ch 03, 07, 16, 19, 20, 22, 23, 26, and 28 against the revised text, then run `make chapter-covers`.
- **References:** apply the DC-01–DC-14 fixes within each source's recorded scope; never broaden a scope without verifying the source.

### Phase 5 — validation

Run per PR, and for the release candidate:

1. `make assemble` and inspect the Markdown diff.
2. `make diagrams` and `make chapter-covers` (if sources changed).
3. `make validate` = build + references + examples + latex-validate. This includes the 8/28/12 counts, balanced fences, citation resolution, and example citation and regions.
4. `make examples-run`.
5. `make deterministic` (two builds, hashes compared).
6. `make qa-pdf` and `make pdf` with real XeLaTeX. Inspect pages around the Closing Perspective, the Ch 16 and Appendix A pages, and every changed figure.
7. Update the changelog and release notes; `make package`; validate from the extracted package.
8. Notion sync only after all gates pass (AGENTS.md).

Grep checks before merging the last Part:
- no remaining "Northstar", "Agent Gateway", "RunContext", "ToolSpec", "AgentStep\b", "EvaluationReport", "employment verification", "propose_effect", or ":forkReplay";
- "guardrail" appears only in its detector sense;
- no ` ```python ` blocks in `source/parts` beyond the D-23 exemptions.

---

## 16. Quality-gate results

**What was verified**

| Check | Result |
| --- | --- |
| Every chapter reviewed | 28/28 present; the front matter and all 8 Part orientations are covered; appendices have no dedicated review → covered here (WP-A) |
| Every `##`/`###` heading considered | Script over 666 non-fenced headings: all matched in their review except the 14 T-cards of Ch 20, which C20-R07 covers as a group (accepted) |
| Recommendations concrete and located | All 401 original recommendations have a Location and a Change (C15-R12 and C17-R11 combine them under "Locations and changes"); ID sequences have no gaps or duplicates; 14 sampled line references matched the source exactly |
| Contradictions | 32 decisions; 54 amendments; 24 additions (§12) |
| Reinforcement vs redundancy (spot checks against source) | Ch 18's "seven statements" of the justification rule (7 confirmed; recommendations correctly spare the checklist and Q); Ch 21 intersection (5 found against 6 claimed; recommendations unaffected); Ch 28 cost per verified success (12 occurrences; recommendations cut only item 10 and the box, keep the recall); the "no back-references to Ch 1–3/7–9" claims (confirmed: zero); Ch 18/21 code identity (confirmed by `diff`); DF-01–DF-03 (confirmed). No misclassification found that would delete legitimate recall |
| New duplication from additions | Found and fixed: C22-R05 vs C26-R01 scale relation (now consistent); C26-R02 re-listing Ch 25's automation list (now a pointer); Appendix A cards vs chapter cards (C16-R10); Ch 18 and Ch 11 comparison questions (D-06); the Part IV orientation edited three times (D-28). Accepted: index columns on different axes (C01-R09 problems, C07-R01 services, C04-R14 boundaries, C26-R04 review areas, C04-R04 records) |
| Coherent learning progression | §3 graph; every break has a fixing ID; remaining forward references are deliberate and signposted |

**What was changed in review files**

- **54 "Reconciled" amendments:**
  - C01-R03, R10;
  - C02-R05, R09, R13;
  - C03-R19;
  - C04-R05, R07, R08;
  - C07-R01, R05, R06, R15;
  - C08-R06, R08, R10;
  - C09-R04, R09;
  - C10-R01, R02;
  - C11-R08;
  - C12-R01, R06, R11;
  - C14-R04;
  - C15-R04;
  - C16-R04, R06, R08;
  - C17-R07, R11;
  - C18-R04, R14;
  - C19-R01, R07, R16;
  - C21-R07;
  - C22-R05, R13;
  - C24-R01, R04, R06, R12;
  - C25-R06, R08;
  - C26-R01, R02, R03, R06, R10;
  - C27-R02, R10, R14;
  - C28-R07.
- **24 additions:** C02-R19, C03-R22, C04-R19, C04-R20, C05-R15, C05-R16, C06-R14, C10-R14, C12-R14, C13-R12, C14-R16, C15-R14, C15-R15, C16-R10, C18-R16, C18-R17, C18-R18, C21-R11, C22-R16, C22-R17, C24-R17, C26-R13, C27-R15, C27-R16.
- **Ch 16's Option C fallback** is marked not applicable.
- **`book-concept-map.md`:** 7 entries marked *Corrected in synthesis* (AgentRuntime in Fig 4-2; Ch 08 lifecycle drift; A2ATaskEnvelope shares 8 fields, not 10; only ReAct appears 4×; six, not ten, Ch 17 cards depend on Parts V–VIII) or *Superseded in synthesis* (Run API home; store table, two places).

**Residual risks and limitations**

- Rendered DOCX and PDF output was not inspected, and no build was run. Diagram and cover changes are specified, not previewed.
- Line references go stale as soon as the first edit lands. Implementers must re-locate passages by quoted text.
- Reviewers' word-count deltas and several per-chapter factual claims were accepted without independent re-verification. Only the conflicting or highest-impact claims were checked against source.
- The appendices were never reviewed section by section. WP-A rests on map §8 and cross-chapter requests and may miss local issues.
- Several decisions depend on the author (§15 Phase 0). If one is reversed (for example, keeping Northstar, keeping "control plane", or keeping HumanActionAuthorization record names), the listed amendments must be re-applied the other way.
- The D-26 placement of the Closing Perspective needs a builder check; the validators' heading counts are safe.
- The D-23(b) JSON/YAML allowance interprets AGENTS.md and is the author's to confirm.
- The citation fixes (DC-xx) require verifying each primary source. Where verification fails, the claim must be weakened or removed, never re-cited speculatively.
