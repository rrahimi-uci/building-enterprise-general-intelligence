# Chapter 07 — Build a Paved Road for Agent Teams: Continuity and Flow Review

Reviewed: `source/parts/03-part-iii.md:1–177` (Part III orientation at 1–7, Chapter 7 at 9–177). Transitions checked: the close of Ch 06 (`02-part-ii.md:945–947`) and the opening of Ch 08 (`03-part-iii.md:179–196`).

## Overall Assessment

Ch 07 is supposed to frame Part III. In practice it reads as a catalog. Its ~1,840 words are mostly lists: a 16-row capability table, three different stage lists for the same journey (Figure 7-3, Figure 7-4, the golden-path table), a test pyramid, a run-on sentence listing nine stages, and two pseudocode listings. It has only three explanatory paragraphs.

It makes four contributions no other chapter makes:
- the platform-versus-application responsibility split (`:35–52`);
- the adoption principle ("make the safe path easier to reuse than the clever shortcut", `:18`; Q at `:170`);
- a golden path where each stage must emit an evidence artifact (`:99–108`, `:158`);
- one immutable artifact across environments, with environment bindings applied at deployment (`:131`, `:150`).

These four should stay. Five problems weaken the chapter:

1. **It is a map without coordinates.** Twelve of the 16 capability rows are taught in Ch 14–27: Workflow, MCP, A2A, Skills, Identity, Guardrails, LLM Gateway, Evaluation, Observability, Durable Execution, HITL, and Deployment. The table points to none of them, so the reader meets a list of things they cannot interpret yet.
2. **It re-teaches its neighbors.** § Keep contracts stable while frameworks change restates Ch 03's AgentRuntime seam. § Test the contracts before you test the model is a third test pyramid (Ch 25 has two). § If this fails in production is the first-divergence debugging method that Ch 24 owns.
3. **The two-column ownership model is incomplete.** Ch 08–09 rely on a third owner, the domain-capability owner of Skills and Skill Packs. Ch 04 already federates Skills to "accountable owners" (`02-part-ii.md:73`). Ch 07 files Skill content under "application-specific", and Figure 7-1 lists no Skills on the team-owned layer.
4. **Contract names drift.** `RunContext` (`:27`, `:58`, and Figures 7-1/7-2) and `ToolSpec` (both figures) are orphans. Ch 03 uses AgentStepRequest/AgentStepResult, and Ch 22 uses ToolManifest.
5. **The opening has no case box and no design choice.** Ch 08 and Ch 09 both have them, so the Part's pattern breaks on its first page.

**Placement verdict (Part III before Part IV): keep it.** Part IV binds to Part III's units:
- Ch 12 compiles each plan node "to an eligible Skill and tool release" (`04-part-iv.md:410`).
- Ch 11's engineering problem lists Skills among routing targets (`04-part-iv.md:220`).
- Ch 15's Snapshot step pins the "prompt/skill bundle" (`04-part-iv.md:1159`).
- Ch 06's trust tier 2 already assumes Skills (`02-part-ii.md:650`).

Moving Part III later would put the Skill definition after its first five uses. The fix is to make Ch 07 an explicit forward map (C07-R01, C07-R13) and to stop it re-teaching Ch 03, 24, and 25.

The Part is under-developed in mechanism, not in length. Ch 07 should get shorter (about −300 words). The missing mechanism belongs in Ch 08 and Ch 09; see those reviews.

## Intended Reader Mental Model

**What the reader brings:** the six gates (Ch 02), the AgentRuntime seam and AgentStepRequest/AgentStepResult (Ch 03), planes and single-writer records (Ch 04, including the centralize/federate decision at `02-part-ii.md:73`), governed knowledge (Ch 05), and context projection (Ch 06).

**What the reader should leave with:**
- **What:** a paved road made of platform-owned contracts, conformance-tested adapters, shared services, and a golden path.
- **Why:** three teams that each build their own safety layer end up with three meanings of failure, audit, and authorization (`:23`).
- **How:** the platform owns the cross-cutting rows of the capability map. Teams own domain behavior. Domain-capability owners own the reusable Skills of Ch 08–09.
- **When:** adopt the road when a second team ships. Leave it only through a recorded, expiring exception (Ch 26).
- **Trade-offs:** the abstraction lags new framework features, and the platform team can become a bottleneck queue.
- **Relationships:** each capability row points to its home chapter. The Tool SDK is the authoring side of the Tool Gateway (Ch 02/22). Promotion detail belongs to Ch 27, and the test levels to Ch 25.
- **Practice:** every golden-path stage emits evidence, and one immutable artifact crosses every environment.

The current text covers What, Why, and the How tables. It leaves out When and Trade-offs; they appear only in P-12, "abstraction may lag novel features" (`04-part-iv.md:1493`). The Relationships are implicit at best.

## Section-by-Section Flow Review

**`# PART III — THE DEVELOPER PLATFORM` (`:1–7`).**
- *Role:* Part orientation.
- *Adds:* "paved road", and lists contracts, adapters, Skills, domain packs, and a lifecycle.
- *Verdict:* adequate but thin.
- *Issues:* It does not say that Ch 07 maps services the later Parts build. It does not name the three owners. It does not link back to Parts I–II ("the reference design" is the only link). See C07-R13.

**`# 07 — Build a Paved Road for Agent Teams` (`:9`) and Evidence context (`:11`).**
- *Role:* chapter opening.
- *Verdict:* the evidence blockquote is fine, but it is the chapter's only opener. There is no case box and no THE DESIGN CHOICE box, unlike Ch 08 (`:181–187`) and Ch 09 (`:358–364`). See C07-R08.

**`## Why teams should not each rebuild the safety layer` (`:13`).**
- *Role:* first "why".
- *Adds:* "make the safe path easier to reuse than the clever shortcut".
- *Verdict:* the content is good, but it is the first half of a double-why opening.
- *Issues:* "every fix arrives at a different speed" is asserted, while `:23` shows it concretely.

**`## When the need becomes obvious` (`:21`).**
- *Role:* second "why", with the three-teams scenario.
- *Adds:* the best concrete paragraph in the chapter.
- *Verdict:* merge it with `:13` (C07-R08).
- *State-owner table (`:25–27`):* "RunContext" is an orphan, and "applications own domain behavior" leaves out domain-capability owners (C07-R02, C07-R03).

**`## What teams should be able to rely on` (`:29`).**
- *Role:* the capability map. Figure 7-1 plus the 16-row table.
- *Adds:* the platform/application split. This is the chapter's core and it is reinforcement (R) of Ch 04's centralize/federate sentence (`02-part-ii.md:73`).
- *Verdict:* keep it, with additions.
- *Issues:*
  - (a) It has no "taught in" pointers. Twelve rows are forward references.
  - (b) "Workflow/Orchestration" (`:38`) and "Durable Execution" (`:50`) overlap: retries, replay, and compensation against checkpoints, recovery, and deduplication. The reader cannot tell why these are two capabilities.
  - (c) The Guardrails row's platform cell includes "action policy" (`:46`). That contradicts the book's own claim that guardrails are not enforcement (concept map §6 T10).
  - (d) The Skills row (`:44`) assigns "capability logic, knowledge, examples, acceptance suite" to the application. Ch 08 assigns them to a Skill owner (`owner: mortgage-platform-team`, `:218`).
  - (e) Figure 7-1 (`developer-platform.gv`) shows "Skill registry" in the platform layer and no Skills in "Team-owned", and it uses ToolSpec and RunContext.
  - (f) The Tool SDK row never says it produces the ToolManifest that the Tool Gateway enforces.

**`## Keep contracts stable while frameworks change` (`:54`).**
- *Role:* portability. Figure 7-2 plus one dense paragraph.
- *Adds:* little beyond Ch 03 § Why the SDK sits behind AgentRuntime (`01-part-i.md:1012`) and § The replaceability test (`:1236`). The one new item is the compatibility-suite list (cancellation, tools, streaming, approvals, errors, telemetry, usage, version behavior).
- *Verdict:* redundant (D). Condense it (C07-R03).
- *Issues:* its contract list drifts from Ch 03. It has no bridge from the capability table above it.

**`## How a capability moves from idea to production` (`:60`).**
- *Role:* lifecycle. Figure 7-3 plus a single 75-word sentence listing nine stages.
- *Verdict:* redundant inside the chapter.
- *Issues:* Figure 7-3's stages are Local, Test, Evaluate, Policy gate, Stage, Canary, Production, Rollback. Figure 7-4's six stages and the eight-row table at `:99–108` cover the same journey with different names. "ChangeBundles", "SBOM", and "provenance" appear with no pointer to Ch 25/27. Merge (C07-R04).

**`## SDK example` (`:66`).**
- *Role:* the first place a reader sees attach_skill, attach_tool, use_context, and use_memory together.
- *Verdict:* useful, but misplaced. It sits between two lifecycle sections, and the CLI listing that belongs with it is 50 lines later.
- *Issues:*
  - The identifiers drift from the case. The spec is `mortgage_evidence_review@0.1.0`, against `mortgage-evidence-agent@0.1.0` in Ch 03 (`01-part-i.md:1228`) and Ch 04 (`02-part-ii.md:184`). The skill is `mortgage-evidence-review@0.1.0`, against `mortgage.evidence.read` in Ch 08 (`:215`). The tool is `read_mortgage_case`, against `mortgage.case.read@1` (`:226`). `risk="regulated"` introduces yet another risk vocabulary.
  - `permissions=[...]` reads like a grant. It is a ceiling that the platform intersects with the caller's authority (Ch 21).
  - The disclaimer (`:85–91`) restates Ch 03 § The adapter builds one bounded runtime.
  - The listing is inline code in `source/parts/`, contrary to `AGENTS.md`.

**`## Make the safe path the easy path` (`:93`).**
- *Role:* golden path. Figure 7-4 plus an 8-stage table with an Evidence column.
- *Adds:* the "each stage emits evidence" model, which is unique and valuable.
- *Verdict:* keep it as the single stage list.
- *Issues:*
  - "Select template and risk tier" (`:101`) does not say which scale.
  - "ValidationReport" (`:106`) is an orphan (concept map §4 row 62).
  - Figure 7-4's labels (scaffold, run locally, add tools, evaluate, promote, operate) do not match the table's stages (Scaffold, Develop, Debug, Evaluate, Package, Promote, Operate, Improve).
  - The trade-offs and the escape hatch are missing (C07-R09).

**`## Test the contracts before you test the model` (`:110`).**
- *Role:* testing. Figure 7-5 (four tiers) plus a paragraph that lists six levels.
- *Verdict:* redundant against Ch 25 § Evaluation pyramid (7 levels, `07-part-vii.md:295`) and § Layer tests from contracts to outcomes (9 levels, `:305`). The figure and paragraph also disagree with each other (4 against 6).
- *Issues:* "timeout/unknown-effect semantics" is used before Ch 22. The platform-specific point, that the platform supplies the harnesses, is never stated. Condense (C07-R06).

**`## CLI and delivery workflow` (`:116`).**
- *Role:* the command-line view of the golden path, plus the pinning and binding paragraph.
- *Verdict:* the listing is useful next to the SDK example. The paragraph at `:131` is restated almost word for word in the checklist at `:150–154`.
- *Issues:* "A model/provider swap is a behavior change" appears at `:131`, `:154`, and `:171`, and again in Ch 03 (`01-part-i.md:1219`), AP-15, and Ch 27 (`08-part-viii.md:154`). The pin list duplicates Ch 27 § Versioned objects (`08-part-viii.md:235`).

**`## What the evidence lets us conclude` (`:133`).**
- *Role:* claim table.
- *Verdict:* fine.
- *Issues:* the conformance list appears here for the third of four times (`:58`, `:137`, `:156`, `:173`). The evidence row itself is the right home for the claim.

**`## If this fails in production` (`:141`).**
- *Role:* failure triage.
- *Verdict:* redundant against Ch 24 § Debugging method (`07-part-vii.md:64`) and Ch 03 § If this fails in production (`01-part-i.md:1277`). It also has nothing to do with platforms: none of the four steps diagnoses a paved-road failure such as a bypass, environment drift, or an adapter conformance gap. Rewrite (C07-R07).

**Template sections: `## What to verify before production` (`:148`), `## Put the idea to work` (`:160`), `## Questions to bring to design review` (`:165`).**
- The checklist is good. Items 1–3 deliberately reinforce `:131`, which is acceptable once `:131` is condensed. Item 5 is the chapter's best gate.
- The exercises are good. "Sixteen" in exercise 1 must track any row merge (C07-R01). Exercise 2 has no supporting example (C07-R14).
- In the questions, Q1 duplicates Ch 03's thesis, Q3 duplicates AP-15 and Ch 27, and Q5 duplicates the evidence row. Q2 and Q4 are good. See C07-R11.

**`## Where this leads next` (`:175`).**
- *Verdict:* accurate, but it does not name the gap Ch 08 fills: the road standardizes how an agent is built, not how reusable behavior travels between agents (C07-R12).

## Sparse or Underdeveloped Content

- **The When and Trade-offs of a paved road** are absent. The costs (abstraction lag, the platform team as a bottleneck queue, teams bypassing the road) and the sanctioned escape hatch (a Ch 26 exception) need about 60 words (C07-R09).
- **The third ownership tier.** Ch 08–09 depend on it, and Ch 07 never names it (C07-R02).
- **Tool SDK → ToolManifest → Tool Gateway.** The reader should learn here that the developer-facing SDK and the runtime gateway are two sides of one contract. Today that is left implicit (C07-R10).
- **No executable example.** The chapter's single evidence claim is that only conformance tests prove parity, and exercise 2 asks for such a test, yet the chapter shows none (C07-R14).
- **Not sparse, but over-listed:** the 75-word run-on stage sentence (`:64`) and the six-level test sentence (`:114`) pack too much into one sentence each. Both should be removed rather than expanded.

## Missing Conceptual Connections

- **Capability map → home chapters, missing "taught in" pointers.** The 16-row table (`:35–52`) needs a pointer to each row's chapter (C07-R01).
- **Ch 04 centralize/federate → Ch 07 platform/application split, missing a back-reference.** `02-part-ii.md:73` already decided the split. Ch 07 should say it is elaborating that decision.
- **Ch 03 AgentStepRequest → Ch 07 SDK "agent", missing "the fluent API compiles to AgentStepRequest".** The disclaimer says "compiled contracts" but never names them (`:89–91`).
- **Tool SDK (`:39`) → Tool Gateway (Ch 02 intro, Ch 22 contract), missing "the SDK emits the ToolManifest the gateway enforces"** (C07-R10).
- **Declared permissions (`:45`, `:74`) → effective authority (Ch 21), missing "declared permissions are a ceiling, intersected with the subject's grant".**
- **Golden-path "Promote" and "Improve" → Ch 27 § Promotion and continuous-improvement loop and Ch 25 § Close the loop…, missing pointers.** Without them the reader cannot tell that the developer view and the release view describe the same pipeline.
- **"Select template and risk tier" (`:101`) → Ch 26 § Match the control to the risk, missing the scale name.** Use "governance tier (Chapter 26)" so it does not collide with R0–R4.

## Transition Problems

- **Ch 06 → Ch 07 (`02-part-ii.md:947` → `03-part-iii.md:13`).** Ch 06's close works ("from what agents know to how teams build with it"). Ch 07 opens cold ("Without a platform…"), with no link to the contracts the reader has just learned. One bridging sentence in the Part orientation fixes this (C07-R13).
- **Within the chapter:**
  - § What teams should be able to rely on → § Keep contracts stable (`:52→:54`): no bridge from "what the platform offers" to "why the contracts must outlive frameworks".
  - § Keep contracts → § How a capability moves (`:58→:60`): no bridge.
  - § SDK example (`:66`) splits the lifecycle discussion (`:60`) from the golden path (`:93`).
  - § CLI and delivery workflow (`:116`) returns to the lifecycle after testing.
  - The fix is the reorder in Structural Recommendations.
- **Ch 07 → Ch 08 (`:177` → `:183`).** The closing promise is kept, and Ch 08's NORTHSTAR box ("teams begin copying prompts and tool wrappers") follows naturally from the three-teams scenario at `:23`. Ch 07 has barely motivated Skills (one table row and one `attach_skill` call), so the closing should name the gap (C07-R12).

## Redundant and Repetitive Concepts

| Concept | Occurrences in Ch 07 | Verdict |
| --- | --- | --- |
| Lifecycle / stage list | Figure 7-3 + `:64` sentence; Figure 7-4 + table `:99–108` | D: keep the table and Figure 7-4 only |
| Adapter conformance list | `:58`, `:137`, `:156`, `:173` | Keep the evidence row (`:137`) and the checklist item (`:156`). Shorten `:58` to a pointer. Q5 can stay as review reinforcement. |
| Model/provider swap is a behavior change | `:131`, `:154`, `:171` | Keep the checklist item. Remove it from `:131`. Replace Q3. |
| Pin list / one immutable artifact | `:131` ≈ `:150` + `:152` | Keep the checklist. Condense `:131` to one sentence pointing to Ch 27. |
| Opening "why" | `:13` and `:21` | Merge |
| Workflow vs Durable Execution rows | `:38`, `:50` | Merge into one row |
| "Convenient SDK hides…" | `:95`, `:172` | R (the review question). Keep both. |

## Cross-Chapter Duplication

| Ch 07 location | Other chapter | Verdict |
| --- | --- | --- |
| § Keep contracts stable while frameworks change (`:54–58`) | Ch 03 § Why the SDK sits behind AgentRuntime (`01-part-i.md:1012`), § The replaceability test (`:1236`); P-12 (`04-part-iv.md:1487`) | D. Ch 03 is canonical. Ch 07 keeps only the platform's added duty (it owns the adapter set and its conformance suite). P-12 is a catalog card (R). |
| § SDK example disclaimer (`:85–91`) | Ch 03 § The adapter builds one bounded runtime (`01-part-i.md:1055`) | Mild D. Condense to two sentences. |
| § CLI paragraph (`:131`) and checklist `:150–154` | Ch 03 § Framework upgrades are behavioral changes (`01-part-i.md:1219`); Ch 04 § RunManifest (`02-part-ii.md:172`); Ch 27 § Treat the full behavior as the release (`08-part-viii.md:154`) and § Versioned objects (`:235`); AP-15 | D in prose, R in the checklist. Ch 27 is canonical for the pin list. |
| § Test the contracts before you test the model (`:110–114`), Figure 7-5 | Ch 25 § Evaluation pyramid (`07-part-vii.md:295`), § Layer tests from contracts to outcomes (`:305`) | D. Ch 25 is canonical (concept map §3). Ch 07 keeps only the platform-harness point. |
| § If this fails in production (`:141–146`) | Ch 24 § Debugging method (`07-part-vii.md:64`); Ch 03 § If this fails in production (`01-part-i.md:1277`) | D. Ch 24 is canonical (concept map §3). Ch 07 is rewritten for platform failures. |
| § What teams should be able to rely on (`:29–52`), Figure 7-1 | Ch 04 § The decisions that shape the system (`02-part-ii.md:73`); § Architecture layers (`:130–142`); Figure 4-1 | R if Ch 07 frames the table as the ownership split and cites Ch 04. Figure 7-1 is a fourth "whole system" picture (concept map §7.1); acceptable only because its axis is ownership, not request flow. |
| Golden path (`:97–108`) | Ch 25 § A safe improvement loop starts with evidence (`07-part-vii.md:244`); Ch 27 § Promotion and continuous-improvement loop (`08-part-viii.md:251`) | R (the developer view) once "Promote" and "Improve" point to Ch 27 and Ch 25 |
| Capability table "LLM Gateway" row (`:47`) | Ch 19 § What belongs at the LLM Gateway… (`05-part-v.md:552`) | R; the pointer target follows wherever concept map S4 lands |
| Q3 model swap (`:171`) | AP-15; Ch 27 Q1 (concept map §5.2) | D. Replace. |

## Structural Recommendations

Reorder the chapter as follows. The template sections stay as they are.

1. Opening boxes (add a design choice), then one merged H2: § Why teams should not each rebuild the safety layer.
2. § What teams should be able to rely on: Figure 7-1, the table with a "Taught in" column, the three-tier paragraph, and the Tool SDK bridge.
3. § Keep contracts stable while frameworks change, condensed to a pointer to Ch 03 plus the platform's conformance duty.
4. § Make the safe path the easy path: Figure 7-4 and the table, absorbing § How a capability moves…, plus the trade-off and escape-hatch paragraph.
5. A new H2, § What the road looks like to a developer, combining the SDK example and the CLI listing, with the condensed binding sentence.
6. § Test the contracts before you test the model, condensed to the harness point plus a pointer to Ch 25.
7. Evidence, a sensible place to start (new), If this fails (rewritten), Verify, Put to work, Questions, Where this leads next.

Retire Figure 7-3 (`developer-lifecycle`) and Figure 7-5 (`test-pyramid`) from Ch 07, then renumber the remaining figures. Do not merge or move the chapter.

## Concrete Recommended Changes

1. **C07-R01**
   - **Priority:** High. **Action:** Add / Rewrite.
   - **Location:** `03-part-iii.md:29–52`, § What teams should be able to rely on.
   - **Issue:** Twelve of the 16 rows are forward references with no pointers. The Workflow and Durable Execution rows overlap. The Guardrails row claims "action policy".
   - **Why it matters to the reader's mental model:** Without pointers, the reader reads a list of unknowns as if it were known. With pointers, the same table becomes the Part's map of the book.
   - **Change:** **Reconciled (see overall-book-review.md §D-08):** LLM Gateway → "Ch 4 (contract), Ch 28 (routing and cost)". Every other item below stands.
     - Add one sentence before the table: "Most of these services are developed later in the book; the last column says where."
     - Add a fourth column, "Taught in":
       - Agent Runtime → Ch 3
       - Workflow and durable execution → Ch 15
       - Tool SDK → Ch 2 (introduction), Ch 22 (contract)
       - MCP Integration → Ch 19
       - Agent-to-Agent Communication → Ch 18–19
       - Context/RAG → Ch 5–6
       - Memory → Ch 6
       - Skills → Ch 8–9
       - Identity & Permissions → Ch 21
       - Guardrails → Ch 20
       - LLM Gateway → Ch 19, or wherever concept-map S4 relocates it
       - Evaluation → Ch 25
       - Observability/Tracing → Ch 24
       - Human-in-the-Loop → Ch 14
       - Deployment & Versioning → Ch 27
     - Merge the "Workflow/Orchestration" and "Durable Execution" rows into one "Workflow and durable execution" row. Platform cell: "Durable state, timers, joins, checkpoints, leases, deduplication, retries, replay, recovery, reconciliation". Application cell: "Domain process graph, deadlines, state machine, and compensation choices".
     - Change "sixteen" to "fifteen" in § Put the idea to work item 1 (`:162`).
     - In the Guardrails row, change the platform cell to "Injection and content detectors, input/output safety, DLP". Move "action policy" into the Identity & Permissions platform cell.
   - **Related sections:** Ch 20 § Guardrails help, but they are not the security boundary (T10). Concept map S4.

2. **C07-R02**
   - **Priority:** High. **Action:** Add.
   - **Location:** after the table at `:52`; the state-owner table at `:27`; Figure 7-1 (`assets/diagrams/src/developer-platform.gv`).
   - **Issue:** The two-tier ownership model has no place for the domain-capability owners that Ch 08 (`owner: mortgage-platform-team`, `:218`) and Ch 09 assume.
   - **Why it matters to the reader's mental model:** The reader enters Ch 08 believing Skills belong to the application team. Ch 08's model is that Skills are owned once and reused across applications.
   - **Change:**
     - Add after the table: "Two kinds of team sit on the application side. Application teams own an agent: its AgentSpec, topology, and acceptance. Domain-capability owners own Skills and Skill Packs that several applications reuse (Chapters 8–9). Chapter 4 § The decisions that shape the system already federates both to accountable owners."
     - Skills row (`:44`), application cell: prefix it with "Domain-capability owner:".
     - State-owner table (`:27`): change "applications own domain behavior" to "applications and domain-capability owners own domain behavior".
     - Figure 7-1: add "Skills · Skill Packs" to the "Team-owned · differentiated" band (for example as a "domain-owned" node), and keep "Skill registry" in the platform band.
   - **Related sections:** Ch 04 `02-part-ii.md:73`; Ch 08 C08-R01.

3. **C07-R03**
   - **Priority:** High. **Action:** Condense / Cross-reference.
   - **Location:** `:54–58`, § Keep contracts stable while frameworks change; the state-owner table at `:27`; Figures 7-1 and 7-2 (`developer-platform.gv`, `portability.gv`).
   - **Issue:** The section re-teaches Ch 03's seam, and its contract names drift. `RunContext` and `ToolSpec` are orphans.
   - **Why it matters to the reader's mental model:** The reader has just learned AgentStepRequest/AgentStepResult. New names suggest they are new contracts.
   - **Change:**
     - Replace the paragraph at `:58` with three sentences:
       - (1) "Chapter 3 put the framework behind `AgentRuntime.execute(AgentStepRequest) → AgentStepResult`; the platform's job is to own that seam for every team."
       - (2) "Stable contracts: AgentSpec (Chapter 4), AgentStepRequest/AgentStepResult (Chapter 3), ToolManifest (Chapter 22), ContextManifest and MemoryRecord (Chapter 6), TaskEnvelope (Chapter 18), EvaluationResult (Chapter 25), ReleaseManifest (Chapter 27)."
       - (3) Keep the existing compatibility-suite sentence verbatim.
     - In the state-owner table's Core contracts, use "AgentSpec · AgentStepRequest/Result · ToolManifest · ReleaseManifest".
     - In both figure sources, replace RunContext with AgentStepRequest and ToolSpec with ToolManifest.
   - **Related sections:** Ch 03 (canonical); concept map T9; P-12.

4. **C07-R04**
   - **Priority:** High. **Action:** Merge / Remove.
   - **Location:** `:60–64`, § How a capability moves from idea to production (Figure 7-3); `:93–108`, § Make the safe path the easy path (Figure 7-4); `assets/diagrams/src/dx-golden-path.gv`.
   - **Issue:** The same journey appears three times with three different stage sets.
   - **Why it matters to the reader's mental model:** The reader cannot tell whether "Stage/Canary" and "Package/Promote" are different steps.
   - **Change:**
     - Delete the § How a capability moves… heading, the Figure 7-3 marker, and the `:64` sentence. Every item in `:64` already appears in a golden-path table row.
     - Retire `developer-lifecycle`. This marker is its only use in the book, so remove its `config/diagrams.json` entry, its source, and its rendered assets as well (Ch 27 Figure 27-1 owns promotion and rollback). Retire `test-pyramid` the same way unless Ch 25 adopts it (C07-R06).
     - Relabel Figure 7-4's nodes to the table's eight stages: Scaffold, Develop, Debug, Evaluate, Package, Promote, Operate, Improve.
     - Add to the Promote row's Evidence cell "(promotion detail: Chapter 27)" and to the Improve row's "(learning loop: Chapter 25)".
     - Renumber the later figures.
   - **Related sections:** Ch 25 § A safe improvement loop…; Ch 27 § Promotion and continuous-improvement loop.

5. **C07-R05**
   - **Priority:** Medium. **Action:** Move / Merge / Rewrite.
   - **Location:** `:66–91`, § SDK example; `:116–131`, § CLI and delivery workflow.
   - **Issue:** The two listings are separated by the lifecycle and testing sections. Their identifiers drift from the case. The disclaimer re-teaches Ch 03. The `:131` paragraph is duplicated by the checklist.
   - **Why it matters to the reader's mental model:** The reader cannot trace the same agent, Skill, and tool from Ch 03 through Ch 08.
   - **Change:** **Reconciled (see overall-book-review.md §D-23):** No pseudocode exemption from the AGENTS.md code rule. Replace the SDK listing with a registered, behaviour-tested example (for example `examples/platform/paved_road_sdk.py`: a thin builder that compiles `attach_skill`/`attach_tool` into an AgentSpec and an AgentStepRequest from `examples/contracts.py`), keeping the identifiers listed below, and cite it as `[[EXAMPLE:...]]`. If the author prefers not to add code, delete the listing and keep only the replacement disclaimer sentence. Delete the bash CLI block; keep its three commands as inline code in the replacement sentence for `:131`. The identifier, comment, and `:131` items stand.
     - Combine both under one new H2, "What the road looks like to a developer", placed after § Make the safe path the easy path.
     - Identifiers:
       - `spec="mortgage-evidence-agent@0.1.0"`
       - `attach_skill("mortgage.evidence.read@^0.1")`, a requirement rather than a digest; see C08-R03
       - `attach_tool("mortgage.case.read@1", risk_class="R1", ...)`
       - `snapshot="mortgage-policy@approved-2026.09"`
       - CLI: `agentctl init mortgage-evidence-agent …` and `agentctl rollback mortgage-evidence-agent@0.1.0 --to 0.0.9`
     - Add the comment `# a ceiling, intersected with the caller's grants (Chapter 21)` on the `permissions=` line.
     - Replace the disclaimer (`:85–91`) with: "This is platform pseudocode, not an Agents SDK API. The fluent calls compile to the Chapter 3 contracts; those contracts, not these method names, are the stable interface."
     - Replace `:131` with one sentence: "Build one immutable artifact, pin everything listed in Chapter 27 § Versioned objects, and bind endpoints, identities, secrets, sources, quotas, regions, and review queues only at deployment."
     - Flag for the synthesizer: both listings are inline code in `source/parts/`, contrary to `AGENTS.md`. Either move them to `examples/` as clearly non-executable pseudocode with a registry entry, or record an explicit pseudocode exemption. Do not add more inline code.
   - **Related sections:** concept map T16; Ch 08 C08-R03.

6. **C07-R06**
   - **Priority:** High. **Action:** Condense / Cross-reference.
   - **Location:** `:110–114`, § Test the contracts before you test the model; Figure 7-5.
   - **Issue:** This is the third test pyramid in the book, and its figure (4 tiers) and paragraph (6 levels) disagree with each other.
   - **Why it matters to the reader's mental model:** The reader holds three non-matching level schemes.
   - **Change:** **Reconciled (see overall-book-review.md §D-11):** As stated, but the pointer reads "Chapter 25 § Layer tests from contracts to outcomes"; C25-R06 deletes § Evaluation pyramid. Figure 7-5 (`test-pyramid`) is retired, not adopted by Ch 25.
     - Keep the heading.
     - Replace `:114` with: "Most defects are cheaper to catch without a model. The platform makes the cheap tiers cheap by supplying the harnesses: tool mocks, seeded simulation, a controllable clock, fault injection, and recorded-trace replay. The full set of evaluation levels, and which gate each feeds, is defined in Chapter 25 § Evaluation pyramid."
     - Remove the Figure 7-5 marker. If Ch 25's review wants a figure, it adopts `test-pyramid` relabeled to Ch 25's levels; Ch 25 owns that decision.
   - **Related sections:** Ch 25 § Evaluation pyramid; § Layer tests from contracts to outcomes.

7. **C07-R07**
   - **Priority:** High. **Action:** Rewrite.
   - **Location:** `:141–146`, § If this fails in production.
   - **Issue:** These are generic run-debugging steps (canonical in Ch 24) and diagnose no platform failure.
   - **Why it matters to the reader's mental model:** The section should teach how the paved road itself fails.
   - **Change:** Replace with:
     1. "Check that the run carries a ReleaseManifest whose every pin resolves. A run without one bypassed the road."
     2. "Compare the artifact digest across environments. A difference means the one-artifact rule broke at build or binding."
     3. "Run the adapter conformance suite against the deployed adapter version. A gap such as dropped cancellation is a platform defect, not an application defect."
     4. "For behavior inside a run, follow Chapter 24 § Debugging method. Do not edit the prompt until the evidence locates the failing responsibility." This keeps the current step 4's second sentence.
   - **Related sections:** Ch 24 § Debugging method (canonical).

8. **C07-R08**
   - **Priority:** Medium. **Action:** Merge / Add.
   - **Location:** `:11–23`: the Evidence context, § Why teams should not each rebuild the safety layer, § When the need becomes obvious.
   - **Issue:** The opening says "why" twice, and the Part III opening boxes are missing.
   - **Why it matters to the reader's mental model:** The concrete three-teams case is the hook. Right now it comes second.
   - **Change:**
     - Keep the `:13` heading. Its body becomes the `:23` paragraph followed by `:18–19` ("The goal is not… clever shortcut.").
     - Delete the `:21` heading and the first two sentences at `:15–17` ("Without a platform…" and "This chapter describes… delivery practices.").
     - Add a THE DESIGN CHOICE box after the evidence context: "Give teams platform-owned contracts, conformance-tested adapters, and a golden path that emits evidence at every stage; leave domain behavior, topology, and acceptance to the team."
     - If the synthesizer standardizes on case boxes (concept map T1/S12), add one too: "A second Harborlight team begins an agent for the compliance review and starts copying the mortgage team's SDK wrapper."
   - **Related sections:** Ch 08 `:181–187`; Ch 09 `:358–364`.

9. **C07-R09**
   - **Priority:** Medium. **Action:** Add.
   - **Location:** the end of § Make the safe path the easy path (after `:108`).
   - **Issue:** There is no When or Trade-offs content.
   - **Why it matters to the reader's mental model:** A reader who is told the road is always better will either over-centralize or bypass it silently.
   - **Change:** Add about 60 words: "A paved road has costs. Its abstractions lag new framework features, and the platform team can become a queue. Allow negotiated extensions behind the same contracts (P-12), and route any deviation through a scoped, expiring exception (Chapter 26 § Make review predictable and proportional) rather than an unrecorded bypass."
   - **Related sections:** P-12 (`04-part-iv.md:1493`); Ch 26.

10. **C07-R10**
    - **Priority:** Medium. **Action:** Add / Cross-reference.
    - **Location:** after the C07-R02 paragraph in § What teams should be able to rely on.
    - **Issue:** The Tool SDK's relationship to the Tool Gateway is not stated.
    - **Why it matters to the reader's mental model:** It links Part III's developer view to the enforcement point the reader learned in Ch 02.
    - **Change:** Add: "The Tool SDK is the authoring side of the Tool Gateway. A developer writes a typed operation; the SDK emits the ToolManifest (Chapter 22 § What a ToolManifest must declare) that the gateway enforces on every call (Chapter 2)."
    - **Related sections:** Ch 02 § How Tool Use works in practice; Ch 22.

11. **C07-R11**
    - **Priority:** Low. **Action:** Rewrite.
    - **Location:** `:165–173`, § Questions to bring to design review.
    - **Issue:** Q1 and Q3 duplicate Ch 03, AP-15, and Ch 27.
    - **Why it matters to the reader's mental model:** Review questions should test this chapter's model.
    - **Change:**
      - Replace Q1 with "Who owns a Skill: the platform, the domain, or the application?" Strong answer: "The platform owns the registry, manifest schema, signing, and resolution; the domain-capability owner owns content, evaluation suite, and support window; the application declares requirements and acceptance."
      - Replace Q3 with "How do you detect a team bypassing the paved road?" Strong answer: "Runs without a ReleaseManifest, tools unknown to the gateway registry, SDK calls outside AgentRuntime in dependency scans, and traces without platform correlation."
      - Keep Q2, Q4, and Q5.
    - **Related sections:** C07-R02, C07-R07.

12. **C07-R12**
    - **Priority:** Low. **Action:** Rewrite.
    - **Location:** `:177`, § Where this leads next.
    - **Issue:** The closing does not name the gap Ch 08 fills.
    - **Why it matters to the reader's mental model:** The reader needs to arrive at Ch 08 knowing which problem it solves.
    - **Change:** "The paved road standardizes how an agent is built, tested, and released. It does not yet say how reusable behavior travels between agents without copy-and-paste; Chapter 8 packages it as versioned Skills with explicit contracts and lifecycle controls."
    - **Related sections:** Ch 08 NORTHSTAR box (`:183`).

13. **C07-R13**
    - **Priority:** Medium. **Action:** Rewrite.
    - **Location:** `:3–7`, Part III orientation.
    - **Issue:** The orientation does not say that Ch 07 is a forward map. It does not name the owners or link back to Parts I–II.
    - **Why it matters to the reader's mental model:** It sets the reader's expectation that forward references are signposts, not gaps.
    - **Change:** Replace with about 80 words: "Parts I and II defined the contracts; this Part decides who builds them once. Chapter 7 describes the paved road (platform-owned contracts, adapters, services, and a golden path) and doubles as a map: most of its services are developed in Parts IV–VIII. Chapters 8 and 9 define what teams reuse on that road: the versioned Skill and the Skill Pack. Three owners share it: the platform team, domain-capability owners, and application teams."
    - **Related sections:** Ch 06 closing (`02-part-ii.md:947`).

14. **C07-R14**
    - **Priority:** Medium. **Action:** Add.
    - **Location:** a new `## A sensible place to start`, between `:139` and `:141`.
    - **Issue:** The chapter has no executable example, although its only evidence claim is that conformance tests prove parity and exercise 2 asks for one.
    - **Why it matters to the reader's mental model:** It makes "conformance-tested adapter" concrete.
    - **Change:**
      - Add `examples/runtime/adapter_conformance.py`, a conformance suite that drives the existing step-execution adapter with a test model. It asserts that cancellation propagates, a typed disposition is returned, usage and trace fields are present, and SDK errors map to the platform error shape.
      - Register it in `config/examples.json` with `book_chapters: [7]` and a test, and cite it as `[[EXAMPLE:adapter-conformance]]`.
      - Do not duplicate `[[EXAMPLE:step-execution#core]]` (Ch 03).
    - **Related sections:** Ch 03 § The adapter builds one bounded runtime.

15. **C07-R15**
    - **Priority:** Low. **Action:** Rewrite.
    - **Location:** `:101` (Scaffold row) and `:106` (Promote row).
    - **Issue:** "risk tier" has no scale, and "ValidationReport" is an orphan.
    - **Why it matters to the reader's mental model:** It avoids a third unexplained risk scale and an undefined record.
    - **Change:** **Reconciled (see overall-book-review.md §D-02, §D-05):** `:101` → "Select template and use-case tier (Chapter 26)". `:106` Evidence → "ValidationReport and ReleaseGateDecision (Chapter 25); risk approval". Also `:108` (Improve row) Evidence: replace "learning record" with "reviewed regression case (Chapter 25)"; Ch 25 drops LearningRecord. Original text, superseded:
      - `:101`: change "Select template and risk tier" to "Select template and governance tier (Chapter 26)".
      - `:106`: change "ValidationReport and risk approval" to "Promotion decision with evaluation evidence and risk approval". Use whatever record name the Ch 25 review makes canonical (concept map T23).
    - **Related sections:** Ch 26 § Match the control to the risk; Ch 25.
