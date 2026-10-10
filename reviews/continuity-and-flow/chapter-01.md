# Chapter 01 — What Turns an LLM Call into a Production System: Continuity and Flow Review

Reviewed: `source/parts/01-part-i.md:1–614` (Part I orientation plus Chapter 01), all of `source/parts/00-front-matter.md`, and the opening of Chapter 02 (`01-part-i.md:616–660`).

## Overall Assessment

The thesis is right and the best passages are among the strongest in the book: the ten-line demo and its Monday–Friday week (`:57–146`), the four agent levels (`:196–311`), and the uncertainty-ownership table with its "series of refusals" reading (`:332–354`). Three problems weaken the chapter.

1. **It states the thesis too often.** The core sentence (model reasons, system owns state, authority, effects, evidence, recovery) appears at `:138–142`, again at `:150–161`, as the content of § Draw the boundary around the model (`:172–181`), as a blockquote at `:315–316`, and once more as the "category error" paragraph (`:306–311`). After the first statement, each repetition delays the next new idea.
2. **It is overloaded with maps and enumerations before any mechanism appears.** In order the reader gets five failures, four agent levels, a seven-row uncertainty table, four environment properties, three per-step questions, ten problems in four themes, a ten-term vocabulary, nine bands, and six control points. Each piece is defensible. Together they never tell the reader which of them to hold on to.
3. **The ending does not deliver the case it promises.** The closing says "the mortgage checkpoint ends with a useful but limited summary" (`:611`), but the chapter never shows checkpoint C01. Its only listing is `[[EXAMPLE:contracts#step]]` (`:572`): `AgentStepRequest`, `AgentStepResult`, `AgentDecision`, and `ToolCall.logical_effect_key`. That is Chapter 03 and Chapter 22 material, shown with no explanatory prose. The C01 region (`examples/mortgage/cumulative_case.py`, region `c01`) exists and is never used.

There is also case-continuity drift. The demo prints "Employment verification is missing." (`:81`), while the case says the second pay statement is missing (`:49–50`). Several pointers are wrong or orphaned: compensation → Ch 15, acceptance criteria → Ch 10/12, "autonomy level", "Agent Gateway", and "Appendix H carries the full glossary".

## Intended Reader Mental Model

After Chapter 01 the reader should hold:

- **What:** an enterprise agentic system is level four. It is a bounded reasoning component inside services that own state, authority, effects, evidence, and release.
- **Why:** the five non-intelligence failures (durability, trust boundaries, transactional effects, evidence, release control), which prompting cannot fix.
- **How (preview only):** three questions every step must answer (authority, retry safety, reconstructability). Each uncertainty has an authoritative owner. Control points sit on the request path.
- **When:** as soon as an agent can start a workflow, call a mutating tool, wait for a person, or touch an enterprise system (`:163–165`).
- **Relationships:** a reading map from each problem to the chapter that solves it.
- **Practical application:** the C01 checkpoint. It is a read-only summary that exposes a missing document and does nothing else.

The chapter delivers What, Why, and When well. "How" is diffuse because it is split across several parallel enumerations. "Relationships" is promised ("each row will have a chapter behind it", `:411–412`) but not delivered for the most important tables. "Practical application" is replaced by Chapter 03 code.

## Section-by-Section Flow Review

**Part I orientation (`:1–6`).** It frames Part I as the foundation, which is accurate. It names no chapter moves and does not say that C01–C03 are the book's only implemented checkpoints, which matters from Ch 04 onward. "Survive … waiting" overstates Part I: durable waits are Ch 15. Minor.

**Opening callouts (`:10–16`).** The case box and the design choice are both clear. The design choice ("not as an autonomous lender") sets the right stance.

**§ A mortgage case that grows with the architecture (`:18`).**
- *Role:* introduces the running case, its contract table, and Figure 1-1.
- *Adds:* the case ID, tenant, actors, constraints, and the first bottleneck (the missing second pay statement).
- *Verdict:* necessary content, but it comes before the hook.
- *Issues:*
  - `:20–25` is maintainer language ("the original supplier-onboarding material remains as explicitly comparative architecture evidence … not the runnable case or the implementation-status anchor"). A first-time reader has no "original" to compare against.
  - `:35–36` introduces **Northstar** in passing as a codename. That gives the reader two names for one system (T1).
  - The contract table (`:38–46`) uses idempotency key, receipt, and approval before any of them is motivated.
  - The "Workflow" row (`:44`) is re-listed with drift in Ch 03 (`:941–949`).

**§ Start with a demo that genuinely works (`:57`).**
- *Role:* the hook.
- *Adds:* the core claim that the gap is not intelligence, and the five failure properties.
- *Verdict:* excellent. This is the chapter's best section.
- *Issues:*
  - `:63–67` spends three sentences explaining why the sketch is not executable. The label at `:69` already says so.
  - `:81`: `# "Employment verification is missing."` contradicts `:49–50` (T15).
  - COMMON PITFALL (`:146`) adds a new angle ("80% hardening"). It is reinforcement, so keep it.

**§ The gap between a useful demo and a dependable system (`:148`).**
- *Role:* names the central mental model.
- *Adds:* the thesis sentence (`:160–161`).
- *Verdict:* redundant framing. `:150–156` restates `:138–142` almost clause for clause ("survive restarts, handle untrusted inputs, control transactional effects, preserve evidence…").
- *Issues:* the thesis sentence deserves to be stated once, prominently, at the end of the demo section. The H2 can then go.

**§ Draw the boundary around the model (`:167`).**
- *Role:* ownership boundary plus the first state-owner table.
- *Adds:* the state-owner table.
- *Verdict:* the prose (`:172–181`) is a third statement of the thesis, and `:324–330` (Level four) repeats its examples (workflow state, permission, write commit).
- *Issues:*
  - The five-column table (`:186–188`) is the template every later chapter uses (map §5.1), and this is the only place it could be explained. It is not explained.
  - The row uses unseen terms: "RunManifest · AgentStep · Artifact", "regional cell", and "Run Service". "AgentStep" should be AgentStepRequest/AgentStepResult (T9).
  - The pivot at `:193–194` ("With that boundary established…what exactly do we mean by an agent?") shows the order is backwards. The levels explain why the boundary exists.

**§ Four very different things we call an agent (`:196`).** The intro (`:198–214`) is tight and sets up Figure 1-2. Good.
- **§ Level one — a model (`:218`):** clear. Inline code (`:224–237`) conflicts with the `AGENTS.md` rule that code lives in `examples/`. That is a policy note, not a flow issue.
- **§ Level two — a model with tools (`:243`):** clear. It introduces "a tool call is a proposal" (`:260–263`) and forward-points to Ch 02. This is the right seed.
- **§ Level three — an agent (`:265`):** "termination is now a property of a text generator" (`:278`) is a key idea. It has no pointer to where termination moves outside the model (Ch 10 bounded loop; Ch 03 `AgentStepRequest` bounds).
- **§ Level four — an enterprise agentic system (`:284`):** the table (`:294–299`) and "the fourth level adds no intelligence at all" (`:301–304`) are strong. Then:
  - `:306–311` restates the demo conclusion.
  - The blockquote at `:315–316` restates the thesis.
  - The second blockquote (`:321–322`, "suggest … establish") is a new facet that leads naturally into the uncertainty table. Keep that one.
  - `:324–330` duplicates `:177–181`.
- **§ Which component should own each uncertainty (`:332`):** canonical (map). The refusal paragraph is the best teaching in the chapter. Issues:
  - "whether a payment succeeded" (`:352`) is off-case.
  - The owners (route service, plan service, policy engine, effect ledger, acceptance engine) have no chapter pointers. This table is the natural on-ramp to Part IV and VI.
- **§ The comparative supplier-onboarding thread (`:356`):**
  - *Role:* introduces a second domain.
  - *Verdict:* misplaced (it is not about agent levels) and largely redundant. `:367–377` re-describes level four as "governed execution".
  - The thread then appears only as Ch 02/03 boxes that restate their design choices, and as unlabeled "onboarding" examples in P-02, AP-03, and AP-07 (map S13).
  - `:378–379` ("from an agent that can perform work to a system that can reliably govern the work the agent performs") is a strong sentence worth keeping.

**§ What changes when the prototype meets production (`:381`).**
- *Role:* the environment properties and the three per-step questions.
- *Adds:* the three questions (`:399–401`), which are the chapter's operational test and canonical (map).
- *Verdict:* the questions are essential. The four-property bullets (`:391–394`) are the third enumeration of the same problem space; they could be one paragraph.
- *Issues:*
  - "it is Tuesday" (`:392`) collides with "Tuesday — Trust boundaries" (`:98`).
  - `:403–406` lists five mechanisms but does not say which question each answers, or where each is developed. The capability envelope is not in the vocabulary table.
- **§ Ten problems, four themes (`:408`):** a good map. The "start with effects" triage advice (`:419–420`) is valuable. However, `:411–412` promises "each row will have a chapter behind it", and the table has no chapter column. Nothing connects the five failures (`:92–136`) to their rows.
- **§ The vocabulary this book assumes (`:435`):** useful. Wrong pointers:
  - Compensation → "Chapter 15" (`:445`). The fullest treatment is Ch 22 § The mechanics that make retries safe and § Where transaction guarantees begin and end.
  - Acceptance criteria → "Chapters 10 and 12" (`:450`). The definition is Ch 02 § Deterministic acceptance, with Ch 13 and Ch 15 § Terminal correctness.
  - Missing terms used in this chapter: capability envelope (`:404`), last-hop credential (`:533`), and run manifest (`:405`).
  - "Appendix H carries the full glossary" (`:455`) is false. Appendix H has 15 terms and none of these.
- **§ Anti-pattern — the autonomous monolith (`:458`):** a good negative image that consolidates the chapter, with a correct pointer to AP-01. It is reinforcement and should stay.

**§ The system as a set of responsibilities (`:480`).**
- *Role:* the one-picture reading map (Figure 1-3 plus the band table).
- *Verdict:* useful orientation.
- *Issues:*
  - "Channels → Part I" (`:492`) is wrong. Part I does not develop channels; the experience plane is Ch 04 and the reviewer/operator console is Ch 14. The figure label (`system-overview.gv`, "I") has the same error.
  - `:510–513` claims Figure 4-1 is "this same picture at higher resolution". It is not. Figure 1-3 bands: Channels, Agent runtime, Collaboration, Knowledge, Control points, Systems of record, Evidence, plus spines Security and Platform. Figure 4-1 clusters: Experience and channels, Edge and admission, Run control…, Agent applications, Knowledge context and memory, Gateways and integration, Systems of record, plus spines Trust and governance and Evidence and improvement. Evidence changes from a band to a spine, and Collaboration disappears (T2).

**§ Each control point answers a different question (`:515`).**
- *Role:* canonical gateway taxonomy (map).
- *Adds:* Figure 1-4 and a six-row table.
- *Verdict:* keep the table and figure. They prevent real confusion. The four paragraphs after them (`:531–552`) are mostly detail that Ch 02 § How Tool Use works in practice re-teaches nearly verbatim. `:793` repeats `:531–534`'s pipeline.
- *Issues:*
  - "Agent Gateway" (`:525`) is never developed. Ch 19 uses both "Agent Gateway" (table `05-part-v.md:561`) and "A2A Gateway" (`:438`, `:455`, `:499`).
  - "mints a last-hop credential" and "records the receipt" are not in the vocabulary.
  - "behavior bundle" (`:550`) is a fourth release-artifact name (T7).
  - There is no sentence connecting these control points to the owners in the uncertainty table. Example: the Tool Gateway consults the policy engine and writes the effect ledger, and the acceptance gate is the acceptance engine. The reader gets two vocabularies for the same components.
  - The ARCHITECTURE GUIDANCE box (`:556`) adds the naming rationale. It is reinforcement and should stay.

**Template sections (`:559–605`).**
- **§ What the evidence lets us conclude (`:559`):** one claim row plus the stock sentence. Adequate.
- **§ A sensible place to start (`:567`) / § Provider-neutral agent-step contracts (`:570`):** an empty H2 wrapping an H3 whose listing is Chapter 03's contracts. The registry entry `config/examples.json` "contracts" has `book_chapters: [1, 4]`, and its docstring says "Chapter 02 needs the agent-step subset". All three disagree. The C01 checkpoint is missing (see Overall Assessment).
- **§ If this fails in production (`:574`):** three sensible steps.
- **§ What to verify before production (`:580`):** `:586` "Autonomy is bounded independently across tools, data, time, cost, delegation, and publication" uses an undefined "autonomy". It is fine once Ch 02 defines autonomy as a decomposed grant (see C02-R07).
- **§ Put the idea to work (`:592`):** exercise 1 says "for Northstar".
- **§ Questions to bring to design review (`:597`):** Q3 "How would you choose an autonomy level" (`:603`) refers to a scale the book never defines. The four levels are capability levels. The other questions are good.

**§ Where this leads next (`:607`).** Strong. The mortgage bridge is precise and correctly previews Ch 02.

## Sparse or Underdeveloped Content

- **The state-owner table** (`:186–188`) is the book's most repeated device (25 chapters) and is never explained. Two or three sentences defining the five columns would make every later instance readable. This is the one expansion the chapter needs.
- **The C01 checkpoint** is described in prose (`:48–53`, `:611–614`) but never shown with the Before/Added/After table that Ch 02 (`:840–842`) and Ch 03 (`:933–935`) use. Without it, Ch 02's "Before: C01 returns a candidate summary…" has no antecedent.
- **The mechanism-to-question mapping** (`:403–406`) is a single sentence where a short mapping would let the reader use the three questions as an index into the book.

Nothing else needs expansion. The chapter's problem is excess, not sparseness.

## Missing Conceptual Connections

- **Five failures → ten problems, missing row mapping** (`:138–142` → `:422–433`). Monday → Long-lived execution, Tuesday → Untrusted context, Wednesday → Tool side effects, Thursday → Compliance/Operability, Friday → Model and vendor drift. One sentence after the ten-problems intro closes it.
- **Three questions → mechanisms, missing "which mechanism answers which question, developed where"** (`:403–406`). Q1: capability envelope (Ch 21) and proposal-bound approval (Ch 14). Q2: durable execution (Ch 15) and effect ledger (Ch 22). Q3: run manifest (Ch 04) and causal trace (Ch 24).
- **Uncertainty owners → control points, missing "control points are where owners are consulted on the request path"** (`:340–348` → `:522–529`).
- **Level three termination → external bounds, missing the forward pointer** (`:278` → Ch 03 § The request is bounded before the model sees it; Ch 10).
- **Figure 1-3 → Figure 4-1, missing the band-to-plane mapping** (`:510–513`). Ch 01 should stop claiming identity. Ch 04 should own the mapping.
- **Front matter → Ch 01, missing the Northstar definition and the honest status of the comparative thread** (see Transition Problems).

## Transition Problems

- **Front matter → Part I.** The front matter introduces Harborlight and the checkpoint table (`00-front-matter.md:61–75`). Chapter 01 then re-introduces both with different emphasis. The front matter never mentions Northstar, but Ch 01 does (`:35`). The executive reader path skips Part I (`00-front-matter.md:79`), while the Part I intro says "This is the starting point for the whole book" (`:3`).
- **Case box → case section → demo.** The reader gets the case three times (box `:12`, section `:18–53`, demo `:63–82`) before the first hook lands. Putting the demo first removes one of those transitions (C01-R13).
- **`:193–194`.** "With that boundary established, we can answer another important question" is a forced pivot caused by section order.
- **`:378–381`.** The supplier thread ends on "the central transition at level four", then the next H2 starts the production-properties discussion. The thread interrupts the levels → uncertainty → production sequence.
- **Out to Ch 02 (`:609–614`).** Good. Ch 02's opening then restates its own intro three times (see chapter-02.md), which blunts this good handoff.

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict | Action |
| --- | --- | --- | --- |
| Thesis: model reasons, system owns state/authority/effects/evidence | `:138–142`, `:150–156`, `:160–161`, `:172–181`, `:306–311`, `:315–316` | Redundant (the map agrees) | State once at `:160–161` (relocated to the end of the demo section). Keep `:321–322` as the lead-in to the uncertainty table. Cut the rest. |
| Completion and write-commit examples | `:177–181` and `:324–330` | Redundant | Keep `:324–330` |
| Level four as "governed execution" | `:286–292` and `:367–377` | Redundant | Keep `:286–292`. Move `:378–379` into it. |
| Tool Gateway pipeline | `:531–536` and Ch 02 `:793` | Cross-chapter redundancy | Keep only the protocol-agnostic point in Ch 01 |
| Problem-space enumerations (5 failures, 4 properties, 10 problems) | `:92–136`, `:391–394`, `:422–433` | 5 failures and 10 problems are reinforcement (story vs. map). The 4 properties overlap both. | Condense the 4 properties to one paragraph |

Deliberate reinforcement to keep: the COMMON PITFALL (`:146`), the monolith anti-pattern (`:458–478`), and the ARCHITECTURE GUIDANCE box (`:556`).

## Cross-Chapter Duplication

| Ch 01 content | Other location(s) | Verdict | Owner / action |
| --- | --- | --- | --- |
| Core thesis | Ch 02 BOUNDARY RULE (`:779`); Ch 03 "let the framework run the agent…" (`:964`); Ch 04 § Where truth lives; Part VI intro; Closing Perspective | Reinforcement, since each adds a new lens. Ch 01's internal repeats are the redundancy. | Ch 01 canonical statement; others keep their framings |
| Uncertainty-ownership table (`:340–348`) | Ch 02 § Where distributed systems must remain authoritative; Ch 03 § Runtime responsibility versus enterprise responsibility and § Responsibility map; Ch 04 § Where truth lives; Ch 12 § What should be agentic? | Ch 02 and Ch 04 are reinforcement (different axes: DS primitives, truth stores). Ch 03 § Responsibility map is redundant. | Ch 01 owns uncertainty. Ch 03 removes § Responsibility map (C03-R10). |
| Control-point table (`:522–529`) | Ch 19 § What belongs at the LLM Gateway—and what does not (table `05-part-v.md:558–565`, adds "Orchestration layer"); Figure 19-1 | Ch 19 table is redundant with drift | **Ch 01 owns the taxonomy.** Ch 19 should reference it and keep only LLM-Gateway-specific rows (Ch 19 reviewer). Agent Gateway vs A2A Gateway: Ch 19 decides and Ch 01 follows (C01-R10). |
| Tool Gateway paragraph (`:531–536`) | Ch 02 § How Tool Use works in practice (`:793`); Ch 22 § Give tools explicit contracts / § Invocation sequence | Ch 02's version is redundant with Ch 01 | Ch 02 owns the introduction; Ch 22 owns the full contract. Ch 01 keeps one sentence. |
| Human approval gate (`:542–546`) | Ch 03 § Human approval… (`:1133–1154`); Ch 14 § Separate authorization from intervention | Ch 01 preview is reinforcement | Ch 14 canonical; Ch 01 keeps one sentence |
| Monday (restart) / Wednesday (timeout) / Tuesday (injection) / Friday (cheaper model) stories | Ch 03 § One retry owner, § Guardrails and authorization…; AP-01, AP-05; Ch 20 § Worked example — an injected mortgage document; Ch 22 case box and failure timeline; Ch 24 worked example; AP-15; Ch 27 | Ch 01 tellings are hooks (reinforcement). Ch 03's retellings are redundant. | Ch 01 keeps all five. Ch 03 cuts its retellings (C03-R03, C03-R04). |
| Monolith anti-pattern (`:458–478`) | Ch 17 AP-01; Figure 17-1 | Reinforcement | none |
| Vocabulary table pointers | Ch 22 (compensation), Ch 02/13/15 (acceptance) | Pointers are wrong | Fix in Ch 01 (C01-R03) |
| `[[EXAMPLE:contracts#step]]` (`:572`) | Ch 03 § The request is bounded before the model sees it (field table `:1039–1047`); `[[EXAMPLE:contracts]]` in Ch 04 | Misplaced | Move the listing to Ch 03 (C01-R01, C03-R08) |

**No chapter in Parts II–VIII refers back to Chapter 1, 2, or 3 by number.** A grep of `02-part-ii.md`–`09-appendices.md` finds none. Part I's canonical items are therefore never leveraged, and later chapters re-teach them standalone. When downstream chapters condense, they should add back-references such as "the control points of Chapter 1".

### Front matter (`00-front-matter.md`) — issues affecting the reader's starting model

| # | Location | Issue | Verdict |
| --- | --- | --- | --- |
| FM-1 | Preface `:26–30`; How to Use `:72–75` | Promises "comparative supplier-onboarding examples show how the same contracts travel to other domains". The thread has no artifact, code, or checkpoint. It appears only as boxes in Ch 01–03 and unlabeled in P-02/AP-03/AP-07. "Retained supplier-onboarding material" is maintainer language. | Promise not kept. Retire it (C01-R24). |
| FM-2 | How to Use, reader-path table `:77–84` | Paths contradict dependencies. **Executives** skip Part I, though Ch 01 is the thesis and Part I calls itself "the starting point" (`01-part-i.md:3`). **Platform engineers** skip Part I (they build AgentRuntime and the Tool Gateway, Ch 02–03) and Part IV (Ch 15 durable execution). **Application developers** skip Part VI (Ch 22 effect safety, needed when writing tools). **Security** skips Part V (MCP/A2A threats T-12/T-13). **SRE** skips Ch 15 (durable execution) and Ch 20/23 (incident lifecycle, kill switch). | Transition defect, High |
| FM-3 | § The architecture in one view `:86–94` | The prose says "follow a request through the system… controlled entry point… controls", but Figure 0-1 (`book-map.gv`) is a map of the eight Parts. The request view the prose describes is Figure 1-3 (`01-part-i.md:485`). | Prose/figure mismatch |
| FM-4 | Figure 0-1 labels | "Architecture and knowledge", "Patterns and anti-patterns", "Multi-agent and integration", "Security and guardrails", "Observability and evaluation", "Governance and operations" do not match the Part titles (T26). "Security and guardrails" also contradicts Ch 20's "guardrails are not the security boundary" (T10). | Diagram drift |
| FM-5 | § The engineering contract behind the architecture `:96–107` | Six principles, each a paragraph, that overlap but do not match Ch 02 § Design principles (ten). Contract 1 ≈ Ch 02 P1; contract 3 ≈ P3/P7; contract 4 = P6; contract 5 ≈ P8; contract 2 and contract 6 pre-teach Ch 24/25/27. The two lists are never cross-referenced. | Redundant with drift |
| FM-6 | How to Use `:56–58` | "Each major chapter moves from a concrete problem through boundaries, architecture, implementation, failure modes, measurement, and trade-offs" is not true of Ch 16, 17, or 26. | Minor over-promise |
| FM-7 | Find Your Way Through the Book `:109–176` | A bare TOC duplicating the generated one. No one-line purposes, no dependency notes, and the Closing Perspective is absent. | Low value |
| FM-8 | Preface § How this edition is maintained `:44–50` | Maintainer content (canonical Markdown, regenerate DOCX/LaTeX) inside the reader preface | Misplaced |
| FM-9 | Checkpoint table `:66–70` | Duplicates the Ch 02/03 checkpoint tables (acceptable). It correctly says C01 exposes "the missing second pay statement", which the chapters then contradict (T15). It never tells the reader that later "WHERE THE MORTGAGE CASE STANDS" boxes are roadmap scenarios; only `:72` hints at it. | Reinforcement; the continuity fix belongs in the chapters |
| FM-10 | Whole front matter | Northstar is never defined, although Ch 01–28 use it. | Follows the T1 decision (C01-R07) |

## Structural Recommendations

Proposed order for Chapter 01 (net effect: shorter, one thesis statement, one explained table template, and the C01 checkpoint shown):

1. Opening boxes (unchanged).
2. **§ Start with a demo that genuinely works.** The hook, Mon–Fri, and the pitfall. It ends with the thesis sentence (currently `:158–165`, moved here). § The gap between a useful demo and a dependable system is removed.
3. **§ A mortgage case that grows with the architecture**, moved after the demo. No supplier or Northstar paragraphs. The contract table and Figure 1-1 are unchanged.
4. **§ Four very different things we call an agent**, Levels 1–4. Delete `:306–316`. Keep `:321–330`. Move `:378–379` to the end of Level four.
   - § Which component should own each uncertainty, followed by the **explained state-owner table**, moved from the deleted § Draw the boundary around the model.
5. **§ What changes when the prototype meets production.** The properties are condensed. The three questions are mapped to mechanisms and chapters.
   - § Ten problems, four themes, with a chapter column.
   - § The vocabulary this book assumes, with pointers fixed.
   - § Anti-pattern — the autonomous monolith.
6. **§ The system as a set of responsibilities.** The Figure 4-1 claim is softened and the Channels row fixed.
7. **§ Each control point answers a different question.** Table and figure, condensed paragraphs, and a bridge to the uncertainty owners.
8. Template sections. § A sensible place to start shows C01.

Remove § The comparative supplier-onboarding thread entirely (C01-R06).

## Concrete Recommended Changes

1. **C01-R01 — High — Move / Rewrite**
   - **Location:** `01-part-i.md:567–572`, § A sensible place to start / § Provider-neutral agent-step contracts.
   - **Issue:** the only listing is Ch 03's step contracts. The C01 checkpoint is never shown, and the H2 is empty.
   - **Why it matters:** the chapter's practical application is missing, and Ch 02's "Before: C01 returns…" has no antecedent. Readers meet `AgentStepRequest` and `logical_effect_key` with no explanation.
   - **Change:**
     - Replace the H3 with "### Mortgage checkpoint: a read-only summary".
     - Add a one-paragraph lead-in: C01 reads metadata for `MORT-2026-000184`, reports the missing second pay statement, and computes, decides, and writes nothing.
     - Add a Before/Added/After table in the Ch 02/03 format. Before: no system. Added: `C01` read-only evidence summary. After: the missing document is visible; calculation, decision, and effects stay outside the model.
     - Insert `[[EXAMPLE:mortgage-cumulative-case#c01]]`.
     - Delete `[[EXAMPLE:contracts#step]]` here. Ch 03 receives it (C03-R08).
     - Update `config/examples.json` "contracts" `book_chapters` from `[1, 4]` to `[3, 4]`, and the `examples/contracts.py` docstring to "Chapter 03 needs the agent-step subset".
   - **Related:** C03-R08; FM-9.

2. **C01-R02 — High — Remove / Merge**
   - **Location:** `:148–165` § The gap between a useful demo and a dependable system; `:306–316` (Level four).
   - **Issue:** the thesis is restated four extra times.
   - **Why it matters:** repetition delays new ideas and blurs which sentence is the mental model.
   - **Change:**
     - Delete the H2 at `:148` and its paragraphs `:150–156`.
     - Move `:158–165` ("This gives us the central mental model…" through "…interact with an enterprise system.") to the end of § Start with a demo that genuinely works, after the COMMON PITFALL box.
     - Delete `:306–311` (the category-error paragraph; its list of guarantees is already in `:138–142`) and `:313–316` (the first blockquote).
     - Keep `:318–330`, starting "The boundary matters most when a run hits uncertainty…".
   - **Related:** C01-R05.

3. **C01-R03 — High — Rewrite**
   - **Location:** `:435–456` § The vocabulary this book assumes.
   - **Issue:** wrong pointers, missing terms used in the chapter, and a false glossary claim.
   - **Why it matters:** this table is the reader's index for the whole book. Wrong pointers send readers to chapters that do not develop the term.
   - **Change:** **Reconciled (see overall-book-review.md §D-12):** Acceptance criteria → "Chapters 2 and 13" (Chapter 2 defines the criteria, Chapter 13 the acceptance engine; Chapter 15 owns run terminal states, not criteria). Every other item below stands.
     - Compensation → "Chapter 22".
     - Acceptance criteria → "Chapters 2, 13 and 15".
     - Add three rows:
       - **Capability envelope:** the platform-computed maximum scope (tools, resources, purpose, budget) a run or child may use; never widened by the model. Chapter 21.
       - **Credential lease (last-hop credential):** a short-lived, audience-bound credential minted after authorization for one downstream call. Chapter 21.
       - **Run manifest:** the per-run record of pinned versions (agent, model route, policy, tools, knowledge). Chapters 4 and 27.
     - Change `:454–456` to "Appendix H defines further terms." The Appendix H expansion is owned by the appendices reviewer (map S15).
   - **Related:** C02-R05 (acceptance defined in Ch 02).

4. **C01-R04 — High — Rewrite**
   - **Location:** `:81` (demo comment).
   - **Issue:** prints "Employment verification is missing.", contradicting `:49–50`, front matter `:68`, and the implemented C01/C03 tests (`tests/mortgage_case/unit/test_c01.py:21` asserts `["pay_statement"]`; `tests/mortgage_case/contract/test_c03_runtime.py:76` says "A second pay statement is missing.").
   - **Why it matters:** the running case contradicts itself on its first page.
   - **Change:** set the comment to `# "A second pay statement is missing."`.
   - **Related:** C02-R04 and C03-R17 carry the same fix through Ch 02/03. Later-chapter occurrences belong to their reviewers: `04-part-iv.md:382, :898, :1119, :1179, :1711`, `06-part-vi.md`. The examples/tests using `employment_verification` also need it: `examples/tests/test_governed_tool_gateway.py`, `test_contracts.py`, `test_approval_gate.py`, `test_approval_verification.py`, `test_effect_idempotency.py`, `test_input_guardrail.py`, `examples/patterns/bounded_react_loop.py`, and `examples/observability/mortgage_agents_mlflow.py`.

5. **C01-R05 — Medium — Merge / Move**
   - **Location:** `:167–194` § Draw the boundary around the model.
   - **Issue:** the prose is a third thesis statement. The state-owner table is unexplained and uses undefined terms. The section order forces an awkward pivot.
   - **Why it matters:** the five-column table recurs in 25 chapters, and this is its only chance to be explained.
   - **Change:**
     - Delete the H2 and `:169–184` and `:193–194`.
     - Move the table to the end of § Which component should own each uncertainty (after `:354`), introduced by three sentences: "Each chapter summarizes its boundary in one row. *State owner* is the component that writes the authoritative record; *trust boundary* is where inputs must be revalidated; *scale unit* is what the component is partitioned and scaled by; *failure containment* is the largest thing one failure should damage; *core contracts* are the records that cross the boundary. For this chapter:"
     - Change the row's last cell to "RunManifest (Ch 4) · AgentStepRequest/AgentStepResult (Ch 3) · Artifact".
     - Change "regional cell" to "regional cell (Ch 4)".
     - Keep `:190–191` ("The specific technologies can change…") after the table.
   - **Related:** C01-R02; map S16.

6. **C01-R06 — Medium — Remove**
   - **Location:** `:356–379` § The comparative supplier-onboarding thread; `:20–25`.
   - **Issue:** a second domain that is promised but never carried. It is misplaced among the agent levels and re-describes level four.
   - **Why it matters:** readers are told to track two cases. Only one exists.
   - **Change:**
     - Delete the H3 and `:358–377`.
     - Move `:378–379` ("That is the central transition at level four…") to the end of § Level four (after `:330`).
     - Replace `:20–25` with: "The implementation follows one fictional mortgage case so the reader sees the same system acquire each capability."
   - **Cross-chapter:**
     - Ch 02 removes its supplier box (C02-R01) and Ch 03 removes its box (C03-R14).
     - The front matter edits are C01-R24.
     - The Ch 16/17 reviewers should relabel P-02, AP-03, and AP-07 "onboarding" examples to Harborlight or a generic domain (map T17).
     - If the synthesizer instead keeps the thread, it must be carried with labeled examples beyond Ch 03. Do not keep the current boxes either way.

7. **C01-R07 — Medium — Remove / Rewrite**
   - **Location:** `:35–36`; `:594`.
   - **Issue:** Northstar is a second name for the same system, defined only in passing (T1).
   - **Why it matters:** readers later see "NORTHSTAR AT THIS POINT" boxes and "Northstar admits 120 runs per minute" and wonder whether it is another organization.
   - **Change:**
     - Delete `:35–36`.
     - At `:594` write "Draw the minimum production architecture for the Harborlight platform…".
     - Ch 03's eleven uses are C03-R16. Later chapters follow the synthesizer's book-wide T1 decision.
     - If the synthesizer keeps Northstar, move its definition to the front matter (How to Use, after `:65`) and to Appendix H, and keep `:35–36` as a one-line recall.

8. **C01-R08 — Medium — Rewrite**
   - **Location:** `:403–406`.
   - **Issue:** five mechanisms are named with no mapping to the three questions or to chapters.
   - **Why it matters:** this turns the three questions into a usable index into the book.
   - **Change:** replace the sentence after "Hold these three questions in mind…" with: "Question 1 is answered by the capability envelope (Chapter 21) and proposal-bound approval (Chapter 14); question 2 by durable execution (Chapter 15) and the effect ledger (Chapter 22); question 3 by the run manifest (Chapters 4 and 27) and the causal trace (Chapter 24)."
   - **Related:** C01-R03.

9. **C01-R09 — Medium — Add**
   - **Location:** `:422–433` (Ten problems table).
   - **Issue:** `:411–412` promises a chapter behind every row, and none is given.
   - **Why it matters:** this makes the table the problem-oriented reading map, alongside the band table's architecture-oriented map.
   - **Change:** add a fourth column, "Developed in":
     - Probabilistic control → 2, 12, 13
     - Long-lived execution → 15
     - Delegated authority → 21
     - Untrusted context → 6, 20, 23
     - Tool side effects → 22
     - Multi-agent coordination → 18, 19
     - Memory and knowledge → 5, 6
     - Model and vendor drift → 25, 27
     - Operability → 24
     - Compliance → 24, 26

   Also add after `:420`: "The five failures of the demo week map onto rows two, four, five, ten and eight."
   - **Related:** C01-R19 is folded into this item.

10. **C01-R10 — Medium — Condense / Cross-reference**
    - **Location:** `:515–556` § Each control point answers a different question.
    - **Issue:**
      - The Tool Gateway paragraph duplicates Ch 02 `:793`.
      - "Agent Gateway" is undeveloped.
      - "Last-hop credential" and "receipt" are unglossed.
      - "Behavior bundle" is an unregistered term.
      - Nothing bridges control points to the uncertainty owners.
    - **Why it matters:** the reader should leave with six questions, not a partial pipeline taught twice.
    - **Change:** **Reconciled (see overall-book-review.md §D-07):** The gateway name is decided: adopt the recommended choice now. Rename the "Agent Gateway" row and the `gateway-roles.gv` label to "A2A Gateway" with the question "May this external agent receive or return this task?", and append "(Chapter 19; internal delegation: Task Service, Chapter 18)". "Agent Gateway" leaves the book. Every other item below stands.
      - Keep Figure 1-4, the table, and the ARCHITECTURE GUIDANCE box.
      - Replace `:531–546` with three sentences:
        - The Tool Gateway is the control point for effects and is protocol-agnostic, because effects arrive over REST, gRPC, queues, and MCP (Chapter 2 introduces it; Chapter 22 specifies it).
        - The MCP Gateway terminates one protocol and decides server trust and tool eligibility (Chapter 19).
        - The human approval gate binds an eligible reviewer's decision to one exact proposal and never replaces reauthorization at the Tool Gateway (Chapter 14).
      - Add one bridge sentence: "Control points are where the owners in the uncertainty table are consulted on the request path: the Tool Gateway asks the policy engine and records into the effect ledger, and the acceptance gate is the acceptance engine."
      - At `:550` replace "behavior bundle" with "release (Chapter 27)".
      - Rename the "Agent Gateway" row (and the `gateway-roles.gv` label) to whatever Ch 19's reviewer chooses. The recommended choice is "A2A Gateway: may this external agent receive or return this task?", with internal delegation left to the Task Service (Ch 18). **Ch 19 owns this decision.**
    - **Related:** Ch 19 table `05-part-v.md:558–565` (Ch 19 reviewer: reference this table instead of re-listing it).

11. **C01-R11 — Medium — Rewrite**
    - **Location:** `:487–513` § The system as a set of responsibilities.
    - **Issue:** "Channels → Part I" is wrong, and the Figure 4-1 claim is false (band names and spines differ).
    - **Why it matters:** readers who flip to Figure 4-1 expecting the same picture find different decompositions.
    - **Change:**
      - Band table row Channels: "Parts II and IV (Chapters 4 and 14)". Update the `system-overview.gv` band label from "I" to "II · IV".
      - Replace `:510–513` with: "Figure 4-1 in Chapter 4 opens these bands into planes and components; Chapter 4 maps its names to these. The notation carries over — solid is the request, dashed is control, dotted is evidence."
    - **Cross-chapter:** **Ch 04 owns** the band→plane mapping table or the figure alignment (map S7, T2).

12. **C01-R12 — Medium — Rewrite**
    - **Location:** `:586` (What to verify); `:603` (Questions, Q3).
    - **Issue:** "autonomy"/"autonomy level" is an orphan. The chapter's levels are capability levels.
    - **Why it matters:** a design-review question the chapter cannot answer undermines the review tool.
    - **Change:**
      - `:586` becomes "✓ The run's tools, data, time, cost, delegation, and publication authority are each bounded explicitly (least agency, Chapter 2)."
      - Q3 becomes "Which of the four levels does a new use case actually need?" with the answer "The lowest level that delivers measurable value; each level up adds a failure class, so grant the minimum tools, data, time, spend, delegation, and effect authority."
    - **Related:** C02-R07 defines autonomy in Ch 02 principle 2.

13. **C01-R13 — Medium — Move**
    - **Location:** `:18–55` § A mortgage case that grows with the architecture.
    - **Issue:** a seven-row contract table precedes the hook. Case vocabulary (idempotency key, receipt) arrives before the motivation.
    - **Why it matters:** the chapter's strongest hook is buried 40 lines down.
    - **Change:** move the whole section (as trimmed by C01-R06/R07) to after § Start with a demo that genuinely works. The opening case box already introduces Harborlight and the case ID, so the demo stands alone. Figure numbering is unaffected, since Figure 1-1 remains the first figure.
    - **Related:** C01-R02.

14. **C01-R14 — Low — Condense**
    - **Location:** `:63–67`.
    - **Issue:** a three-sentence explanation of why the sketch is not executable, duplicating the `:69` label.
    - **Change:** replace with "The sketch below is deliberately incomplete; its gateway and effect controls are missing, which is the point." Keep the `:69` label.

15. **C01-R15 — Low — Condense**
    - **Location:** `:388–394`.
    - **Issue:** the four-property bullets are the third enumeration of the problem space, and "it is Tuesday" collides with the demo's Tuesday.
    - **Change:** replace the bullets with one paragraph: "Four properties make this harder than ordinary development: the model is nondeterministic, the environment is concurrent and partially failing, inputs — including retrieved documents and tool descriptions — may be adversarial, and many actions are irreversible, so retry advice that is sound for a read is dangerous for a write." Keep `:396–401`.

16. **C01-R16 — Low — Rewrite / Cross-reference**
    - **Location:** `:340–354`.
    - **Issue:** owners have no chapter pointers, and "payment" is off-case.
    - **Change:**
      - Append chapter numbers to the "Authoritative owner" cells: Route service / workflow (Ch 11); Plan service / workflow (Ch 12); Policy engine (Ch 21); Effect ledger + downstream system (Ch 22); Workflow / acceptance engine (Ch 2, 13).
      - At `:352` replace "whether a payment succeeded" with "whether a document request committed".

17. **C01-R17 — Low — Cross-reference**
    - **Location:** `:278–282` (Level three).
    - **Change:** append "Chapter 3 moves those limits into the platform's step request, and Chapter 10 into an external loop controller."

18. **C01-R18 — Low — Rewrite**
    - **Location:** `:594` exercise 1.
    - **Change:** add "(Chapter 4 § Where each kind of state belongs lists the stores)" so the exercise is answerable on a second reading. Combine with C01-R07's Northstar fix.

19. **C01-R19 — Low** — merged into C01-R09.

20. **C01-R20 — Low — Rewrite**
    - **Location:** `01-part-i.md:3–6` (Part I orientation).
    - **Issue:** no chapter moves are named, and the implemented-checkpoint status is not stated.
    - **Change:** replace the second sentence with: "Chapter 1 names the pieces and draws the boundary around the model; Chapter 2 makes every model output a proposal that crosses six deterministic gates; Chapter 3 puts the agent framework behind a platform-owned runtime seam. These three chapters carry the companion repository's implemented checkpoints, C01–C03; later case boxes describe the target design." Drop "waiting".

21. **C01-R21 — High — Rewrite**
    - **Location:** `00-front-matter.md:77–84` (reader-path table).
    - **Issue:** paths skip prerequisite chapters (FM-2).
    - **Why it matters:** readers following the paths meet Ch 15/22 mechanisms and Part I vocabulary they skipped.
    - **Change:**
      - Executive: "Chapter 1, Parts II, III, VIII and Appendix G".
      - Platform engineer: "Parts I–III, Chapter 15, Parts V–VIII".
      - Application developer: "Parts I–IV, Chapter 22, Part VII".
      - Security: "Chapter 1, Parts II, V, VI, VIII and Appendices F, K".
      - SRE: "Chapter 1, Chapter 15, Parts VII, VIII and Appendices B, L".
      - Add one line under the table: "Every path assumes Chapter 1's vocabulary."

22. **C01-R22 — Medium — Rewrite**
    - **Location:** `00-front-matter.md:86–94` § The architecture in one view.
    - **Issue:** the prose describes a request flow, but the figure is a Parts map (FM-3).
    - **Change:**
      - Retitle to "## How the book is organized".
      - Replace `:88–92` with two sentences: "The map follows the book's argument from the boundary around the model (Part I) through architecture, the developer platform, patterns, collaboration, security, evidence, and operations. Chapter 1's Figure 1-3 shows the system itself — how a request descends from proposal to committed effect."
      - Diagram owner: align Figure 0-1 labels with the exact Part titles (FM-4, T26). This also removes "Security and guardrails".

23. **C01-R23 — Medium — Condense / Cross-reference**
    - **Location:** `00-front-matter.md:96–107` § The engineering contract behind the architecture.
    - **Issue:** six paragraph-length principles drift from Ch 02's ten and are not cross-referenced (FM-5).
    - **Change:**
      - Reduce each bullet to its bold sentence plus at most one clause.
      - Add after `:107`: "Chapter 2 § Design principles turns this contract into ten design rules used throughout the book."
      - Do not add the contract's "failures become governed evidence" to Ch 02. Chapter 25 owns it; keep the front-matter sentence pointing to Chapter 25.
    - **Related:** C02-R07.

24. **C01-R24 — Medium — Remove**
    - **Location:** `00-front-matter.md:29–30` ("Comparative supplier-onboarding examples show…") and `:73–75` ("The retained supplier-onboarding material…").
    - **Issue:** the promise is not kept (FM-1).
    - **Change:**
      - Delete both sentences.
      - At `:72` add: "From Chapter 4 onward, the WHERE THE MORTGAGE CASE STANDS boxes describe the target design for later checkpoints."
    - **Related:** C01-R06, C03-R15.

25. **C01-R25 — Low — Rewrite**
    - **Location:** `00-front-matter.md:56–58`.
    - **Change:** "Most chapters move from a concrete problem through boundaries, architecture, implementation, failure modes, measurement, and trade-offs; the pattern and anti-pattern catalogs (Chapters 16–17) are reference cards."

26. **C01-R26 — Low — Rewrite / Remove**
    - **Location:** `00-front-matter.md:109–176` Find Your Way Through the Book.
    - **Change:** either delete it (the generated TOC covers it) or add a one-line purpose after each chapter title and list the Closing Perspective after Appendix L. Use the "Where this leads next" sentences as the source of each purpose line.

27. **C01-R27 — Low — Move**
    - **Location:** `00-front-matter.md:44–50` § How this edition is maintained.
    - **Change:** move to the package README or Appendix I. In the preface, keep one sentence: "The book is maintained from canonical Markdown with registered references, diagrams and runnable examples; Appendix I describes the companion package."
