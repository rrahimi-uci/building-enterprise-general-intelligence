# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

### Chapter 8 and Chapter 10 review comments (DOCX review, 2026-10-14)

- **Discovery is not permission (Chapter 8)** is explained step by step for one Harborlight need: what discovery returns and who runs it, the SkillRequirement it hands on, resolution's five ordered filters with what each removes, how a version is pinned or refused, and why a resolved Skill's calls still pass the Tool Gateway. The comparison table gains a "When" row.
- **Figure 8-1** (`skill-resolution`) is redrawn as that worked example: candidates, the requirement, the filters with the versions each leaves, the pin or refusal, binding into the AgentStepRequest, and the Tool Gateway.
- **Correction:** the release-stage filter now admits a Staged release for runs in its staging, shadow, or canary cohort, matching the lifecycle table; the earlier text implied only Active releases ever resolve.
- **Chapter 10's design choice** is reworded and explained: when ReAct is worth a loop, and a table of the five external limits (what the controller counts, Harborlight's settings from the Skill manifest and the reference loop, and the stop reason each produces). Figure 10-1 and the Chapter 10 cover now list all five limits.

### Unified enterprise architecture

- The Closing Perspective now contains Figure S-1, a publication-size TikZ synthesis of the book's global control tier, regional execution cell, external dependencies, cross-cutting trust controls, and offline evidence-to-release loop. It distinguishes pinned KnowledgeReleases from the full behavior ReleaseManifest and bounded AgentRuntime steps from durable workflow ownership.
- The accompanying legend, seven-plane layer explanation, runtime and knowledge lifecycles, improvement loop, and chapter map connect the figure to the 28 chapters. `reviews/unified-architecture.md` records the source inventory, directed-edge contracts, chapter traceability, reconciliation decisions, and final critique.
- Chapter 28's transition now names Appendices A–L in their current order. The diagram source, PNG/PDF renders, registry digest, manuscript, DOCX, and XeLaTeX sources are regenerated from canonical inputs.

### Part II review comments (DOCX review, 2026-10-13)

- **"Seam" becomes "runtime interface".** Chapter 3's `AgentRuntime` boundary is called the runtime interface everywhere: Part I and III prose, the front-matter checkpoint table, the Chapter 3 cover, README, example and companion-code docstrings.
- **Chapter 4 opening.** The "return to it" sentence now names the two design-review symptoms it is for (overlapping authority; a fact with no named owner) with a Harborlight example of each.
- **Figure 4-1** (`reference-architecture`): a key beneath the figure names the three line styles and expands every abbreviation (A2A, IdP, MCP, OTel, PDP, PEP, SLO, STS, WAF, WORM); runtime and workflow and the knowledge plane now feed evidence to evaluation and operations through one evidence bus; the control edge reaches the gateway plane rather than the LLM Gateway alone; the request-path label into the Tool Gateway reads "Proposed action", since the gateway checks it before anything commits.
- **Centralize/federate rewritten.** "The decisions that shape the system" becomes "What the platform team owns and what domain teams own": a table of what each side owns, why, and a Harborlight example, plus what the platform standardizes (interfaces and evidence, not frameworks). Chapter 7's cross-reference follows.
- **Planes and layers without repetition.** The planes-versus-layers explanation appears once; the Figure 1-3 band mapping is a column of the plane table instead of a separate table; the plane-to-layer split table and the layer table are merged into one layer table with a Plane column; abbreviations in it are expanded.
- **Chapter 4 "What the evidence lets us conclude"** removed (one row; its sources stay cited in the Event contract callout).
- **Chapter 5:** the author-reported 44% rejection figure is removed from the prose and the evidence table, and R48's permitted scope no longer covers any measurement. A short paragraph explains how the semantic index and the knowledge graph complement each other.
- **Chapter 5 cover** shows the semantic index and the knowledge graph side by side in the Knowledge Hub, with the typed rule, the pinned release, and enforcement at the effect boundary; the cover renderer gains a `graph` component kind.
- **Chapter 6:** the "Where the mortgage case stands" box is rewritten in plain language.

### Part I review comments (DOCX review, 2026-10-13)

- **Title-page date is the build month.** The front matter carries `{{BUILD_DATE}}`; `tools/build_info.py` resolves it for the Markdown, DOCX and LaTeX editions (the LaTeX entry point no longer hard-codes "September 2026"). `SOURCE_DATE_EPOCH` pins it for byte-for-byte rebuilds.
- **Preface:** removed the sentence about canonical Markdown and the companion package.
- **Glossary last, and a book index.** The glossary moves to Appendix L; Appendices I–L become H–K (companion guide H, coding-agent prompt I, references J, capacity K), and every cross-reference, the reader-path table, the source TOC, tools and docs follow. A new index after Appendix L is generated from `config/index-terms.json` (97 terms, every glossary term included) by `tools/book_index.py`: chapter and appendix locators in Markdown, a two-column makeindex page index in the PDF, and Word XE fields under an INDEX field in the DOCX whose cached result is the Markdown list. `make validate` checks that all three carry the same 663 locators.
- **Part pages are structured.** Every Part intro is now a lead paragraph, one bullet per chapter (or chapter group), and a closing line; both renderers set it ragged right on the Part page. Part VI's second paragraph, which used to fall off its Part page onto a page of its own, is now on it.
- **Level three corrected (Chapter 1, Figure 1-2).** "Runs forever; loses everything on restart" overstated the failure: the OpenAI Agents SDK stops a run at a turn limit (ten by default), can persist conversation history in sessions, serializes paused runs, and lists durable-execution integrations. The text, the levels table and Figure 1-2 now say the loop stops only at a turn limit and that a restart loses state the runtime did not save, and that restored conversation state is not business truth. R29's scope was widened to the documented defaults and re-verified against the docs and the v0.22.2 source.
- **Stale reasoning (Chapter 2).** The principle no longer reads as permission to reason from stale data: every context is a snapshot, the platform reduces staleness by rebuilding context from authoritative stores, and the version check at commit is the guarantee.
- **Why the SDK sits behind AgentRuntime (Chapter 3)** gains a concrete example: five teams meeting the SDK's defaults (turn-limit exception, tracing on with sensitive data) separately, and what that does to one event's meaning, trace data and upgrades.
- **Figure 3-2** (`boundary-tests`, TikZ): the restart test and the replaceability test as two decision flows.

### No empty pages before chapters

- **PDF:** every chapter used to be preceded by a blank page (28 in all) because the chapter-cover macro switched the page geometry, which forced an extra page break. The cover is now placed with a page-sized overlay, so each cover is one full page followed directly by the chapter; the PDF drops from 364 to 336 pages with no blank pages.
- **DOCX:** the cover, Part and title pages no longer rely on paragraphs that hold a page break; they start with `page_break_before` (a one-point anchor paragraph for Part pages), so a full page can no longer push an empty page or a stray empty line in front of a chapter.
- Markdown and the TeX entry file contain no page layout, so they are unchanged; the LaTeX fix is in `latex/bookstyle.sty`.

### Diagram modernization: all 44 figures in TikZ

- The remaining 41 figures are redrawn in the shared TikZ design system, so every diagram now has an editable `assets/diagrams/src/<id>.tikz.tex` source and no Graphviz or Mermaid sources remain in use. Content is unchanged: each figure keeps its nodes, labels, edge directions and styles, groups and annotations (checked element by element against the original).
- Groups converted: stacks, ladders and maps; decision trees; before/after pairs (one shared panel template, `_before-after.tex`); flows with feedback loops; pipelines and state machines; layered and plane architectures including Figure 4-1 (40 chips, 9 groups); and both sequence diagrams (a native TikZ sequence kit, `_sequence-kit.tex`, replaces Mermaid).
- About a dozen figures that the book used to shrink to 69–85 % (labels printing at 7.5–9 pt) are redrawn compactly and placed at full size, so text is 9 pt or larger throughout.
- Fixed `tools/validate_latex.py` holding `release-recovery.png` to the chapter-cover resolution because its id contains the word "cover"; it now matches the `assets/cover/` prefix.
- Review material in `reviews/diagram-modernization/`: per-group reports, before/after pairs and the technical content observations raised for separate review (none acted on).

### PDF in dist

- `make all` now ends with a `dist-pdf` step that keeps `dist/Enterprise-General-Intelligence-v1.0.0-LaTeX.pdf` current next to the Markdown, DOCX and TeX files: it compiles only when the PDF is missing or the content of the generated LaTeX, styles, diagram and cover renders or fonts changed since the last compile (compared by hash), and skips with a notice when XeLaTeX is not installed. `make release` now runs `make pdf`. The PDF stays gitignored and is never committed (CI publishes it as a build artifact).

### Diagram modernization, pilot: a TikZ design system and three restyled figures

- New shared design system `latex/styles/professional-diagrams.sty`: semantic pastel palette (the book's existing house hues plus `navy` and `green`), card, decision, store, chip, pill, callout and group styles, rounded connectors, FontAwesome icons, Liberation Sans type scale (nothing under 9 pt at final size). Documented in `reviews/diagram-modernization/style-guide.md` with a style sheet; inventory of all 44 figures and a conversion plan in `reviews/diagram-modernization/inventory.md` and `pilot-report.md`.
- `tools/render_diagrams.py` accepts `assets/diagrams/src/<id>.tikz.tex` as an editable source: XeLaTeX renders the vector PDF, the DOCX PNG is rasterised from it at the 255 dpi contract. A compile error, an unembedded font, or a figure that would be placed below 95 percent scale fails `make diagrams`. The registry's `source` is authoritative and the renderer keeps `sha256` equal to the render. `tools/validate_latex.py` checks TikZ sources load the package, have a vector render and embed their fonts; `tools/bootstrap_tex.sh --diagrams` installs `standalone` and `fontawesome5`.
- Figures 13-1 (`pattern-reflection`), 22-1 (`effect-lifecycle`) and 26-1 (`governance-model`) restyled in TikZ with unchanged content; their `.gv` sources are removed (history keeps them). The other 41 figures still render from Graphviz and Mermaid. Technical doubts about the originals are recorded in `reviews/diagram-modernization/content-observations.md`, not changed.

### LaTeX PDF output

- The generated XeLaTeX build script now creates `dist/` when needed, verifies both the compiled and final PDF are non-empty, and reports the final `dist/Enterprise-General-Intelligence-v1.0.0-LaTeX.pdf` path. TeX auxiliaries and the intermediate PDF remain in `latex/build/`.

### Chapter 5: compliance knowledge as a governed release (step 2 of the compliance-knowledge update)

- Chapter 5 now treats compliance knowledge (requirement, obligation, control, constraint, definition) as a versioned asset. New sections cover the layer model, the two planes (control plane and runtime plane, with the knowledge registry, release, live pointer, and per-run pin), "Change compliance knowledge the way you change software" (change unit, nine gates in the reference implementation's order, routed findings, the lifecycle Draft → Certified → Approved → Active → Deprecated → Revoked, and activation as the publication boundary), and "Obligations enforced at every control point" with the Harborlight thread. The ontology subsection defines the schema and conformance checks in plain graph terms; the only standards are BPMN, DMN, SBVR, and CMMN. Figure 5-4 (`knowledge-lifecycle`) added; Figures 5-1 and 5-3 gain "release" labels.
- § Combine knowledge without flattening its differences folds into the consistency gate; the capability catalog and its example move to Chapter 8; the PRODUCTION CONSIDERATION box is replaced by the control-point section.
- Chapter 27 gains § Knowledge releases: the CI/CD stage table, tenant extensions, publication, promotion, and rollback; the Knowledge release row replaces Knowledge snapshot, and "current under freshness policy" is restricted to the retrieval index.
- Examples: `rule-as-guardrail` renamed `enforced-rule` with a `pinned` region and six new tests (two adapted from Policy Logic Forge [R48]); `knowledge-graph#shapes`; new `gate-record` (regions `routes`, `budget`, adapted from Policy Logic Forge with credit) and `knowledge-release` (regions `publish`, `promote`).
- Touch points in Chapters 3, 4, 6, 7, 8, 9, 12, 13, 17, 20, 21, 22, 24, 25, 26; Appendix A gains P-13 and a Knowledge row, Appendix B a triage row, Appendix C KnowledgeRelease and KnowledgeBinding, Appendix H twelve terms. Four paragraphs that began with "Figure N", and so rendered as captions in LaTeX, are reworded (Chapters 1, 4, 26; Appendix A).

### Chapter 5: document ingestion (step 1 of the compliance-knowledge update)

- New § Ingest documents the way you extract rules: the second pay statement goes through intake, extraction, verification against its pinned bytes, routing, and one KnowledgeArtifact record, so the age-window rule reads only supported facts. Forged, tampered, resubmitted, and instruction-carrying statements are refused. Figure 5-3 (`document-ingestion`) added.
- New `document-ingestion` example (regions `record`, `verify`) with ten behavioural tests. `grounding-verifier`, adapted from Policy Logic Forge [R48] with credit, now admits a claim only on a literal span and records the evidence sliced from the bytes; two tests added. The guardrail and policy-to-rule tests gain the pay-statement age window.
- R48 widened to the pinned commit c22dc450 and the elements the book points at; the 44% sentence and evidence row say "model-proposed" claims and "a single structural screen". One-line pointers added in Chapters 4, 6, 18, 20, 22, 24, 25 and Appendices C (KnowledgeArtifact) and H (KnowledgeArtifact, Verification status).

### Correctness validation, pass 2

- Citations: evidence rows that cited a source beyond its scope are split into the sourced fact and a labelled book recommendation (Chapters 1, 6, 7, 9, 12, 13, 15, 21, 23, 25, 27); Chapter 21 no longer cites R06 for workload identity.
- Factual fixes: valid CloudEvents extension names (Chapter 4, Appendix C, and the `CloudEvent` example, which now serializes `tenantid`, `correlationid`, `causationid`); the OpenAI Agents SDK ships skills at 0.22.2 (Chapter 8); MLflow 3.15.2's `disable_openai_agent_tracer` explained correctly (Chapter 24 and example comments); R02 no longer cited for replay.
- Appendix D: unsupported CrewAI, Dapr, Pydantic AI and ADK claims removed; A2A pinned to 1.0.1; OWASP ranking stated precisely.
- Consistency: InterventionRequired is non-terminal in Chapters 15, 18 and 19; Chapter 22 calls its effect states "outcome states"; Chapter 26's cadence matches its table; Chapter 2's proposal JSON is labelled as a flattened view of the contract.
- Registry: corrected years, titles and labels; version-specific links pinned; living documentation dated `n.d.` unless the page shows a date, enforced by `tools/check_references.py`; all 58 entries verified 2026-10-11; R29, R31 and R33 scopes widened and R02's narrowed after re-reading the sources.
- Appendix K's source copy is a generated-section stub; its standards group is "Protocols and technical standards".
- XeLaTeX edition: 0 overfull lines (was 478); table headers never doubled or stranded; headings and code labels kept with what follows; curly quotes restored.
- Diagrams and covers: 18 figures reworked for legibility and agreement with their chapters; 35 cover labels in 10 chapters reworded to their chapter's own text; alt text on every DOCX image; Figure 23-1's caption names DLP.

### Correctness review corrections

All 21 findings of the correctness review (PR #81) were re-verified against the source; 20 are corrected here and one (the R48 run artifact) is labelled and left open. Dispositions are recorded under each finding in `reviews/content-correctness-validation/`.

- Chapter 1: the level-one model "has no reliable way of knowing what it does *not* know"; the Tool Gateway row no longer promises "exactly once", and the idempotency key is defined as platform-derived and never model-chosen (also in Appendix H).
- Chapter 5: the intersection of two knowledge sets is "corroborated, not verified" — scope, freshness and permission checks still apply before action (table and `set-operations` docstring); the 44% figure is labelled author-reported, from one run of the author's own pipeline.
- Chapter 6: the "most systems are past the point where more retrieval helps" claim becomes a measure-on-your-own-workload recommendation.
- Chapter 7: `agentctl` is identified as an illustrative command surface, not a tool the book ships.
- Chapter 13: the `evaluator-optimizer` example never accepts a candidate that overran the spend cap and starts no call once spend reaches it; every configured criterion needs a finite score, and executable checks are decided before judge evidence; the one-call overrun that remains is documented on `RevisionLimits`. Three tests added.
- Figure 13-1 redrawn: the judge feeds only the acceptance engine, which owns every exit — accepted, rejected to revise, escalated to a person.
- Chapter 15: an activity that fails before its result is recorded is retried even if its external call succeeded, which is why side effects carry an effect key.
- Chapter 20: the T-04 and T-05 first refusals state their residual risk (provenance is not truth; poison inside an approved source) and point to corroboration, human review and Chapter 23.
- Chapter 22: `effect-idempotency` checks the intent hash before any state handling, so a declined or proven-absent key re-applies only the same intent and rejects a different one with `EffectConflict`; Declined-by-absence requires a manifest-declared visibility window, otherwise InterventionRequired (ToolManifest Effects row and Appendix B step 4 aligned). Tests added.
- Chapter 24: the worked trace "took twelve minutes to return its summary" and the run cannot close while the effect is Unknown; a fork is a sandbox run with mocked or read-only effects, and acting again is a new, separately authorized run.
- Chapter 25: pass^k is defined as the empirical all-k pass rate; the independence assumption behind p^k is stated.
- Chapter 28 and Appendix L: R43 supports only L = λW and the sizing method is a book-authored recommendation; λ_eff = λ_external × E[attempted activities per external run], measured from traces, with the retry multiplier reserved for when traces are unavailable.
- Appendix D: R55–R58 (Claude Agent SDK, Claude Managed Agents (beta), CrewAI, Restate) registered as `n.d.` living documentation with narrow scopes; the Claude row describes documented capabilities with a beta caution. The registry grows to 58 references and 147 citation occurrences.
- Metadata: the 22 stale chapter titles in `config/book.json` now match the manuscript, and `make validate` fails on any title drift between the manuscript, `config/book.json` and `config/chapter-covers.json`.
- Review folder: example-id lists and the QA-date statement corrected by an accuracy audit; dispositions, an implementation-status section and updated counts added.

### Appendices and final cross-Part pass (continuity review, WP-A)

- Appendix B names the Chapter 17 card behind each symptom and classifies a missing receipt in Chapter 22's effect states.
- Appendix C lists the contracts the chapters now define (28 rows, from RunManifest to BudgetReservation), each with its owner and a "Defined in" chapter; AgentStep and the HumanActionAuthorization records are gone.
- Appendix D merges its two framework tables into one, absorbs Chapter 27's stack table as its own section, and drops the uncited MLflow MCP Registry claim; unsourced rows are flagged.
- Appendix E cites six newly registered, verified papers (R49–R54: AutoGen, AgentBench, GAIA, SWE-bench, τ-bench, AgentDojo); the uncited long-horizon row becomes a stated hypothesis.
- Appendix H grows to 61 terms with the chapter that develops each; Appendix I drops its bash fences, the uncited "3.15.0 introduced" sentence, and the correction notes (moved to the README); Appendix J uses Chapter 4's layer names; Appendix K files ISO/IEC 42001 under governance, shows each reference's own access date, and carries its full title.
- Cross-Part fixes: Figure 17-4 shows the evidence-package case and an approval keyed by logical effect; Figure 23-1 names the Access Broker/STS; broken § pointers in Chapters 18 and 26 and Appendix A resolve; Chapter 4's model-vendor boundary and Chapter 22's model fallback point to the chapters that now own them; `code-gap.md` uses approval terminology (D-22).

### Part V (Chapters 18–19, continuity review)

- Chapter 18 defines the task lifecycle and owns the one TaskEnvelope: its eight field groups move in from Chapter 19, and the code becomes the tested `contracts#task` region (idempotent creation, depth and budget withdrawal, envelope-subset hook).
- Handoff follows Chapter 11: `:handoff` proposes a pending OwnershipTransfer that only `:accept` commits. Plan revision belongs to Chapter 12 (`plans:revise` removed).
- The duplicate capability-envelope proof leaves Chapter 18 (Chapter 21 owns it); the two pattern cards merge into "Supervisor/Worker at a glance"; Figure 18-1 uses the mortgage specialists.
- Chapter 19 becomes the federated delta: the LLM Gateway material leaves (enforcement to Chapter 4, routing and metrics to Chapter 28), Figure 19-1 and `gateway-position` are retired, and A2ATaskEnvelope is deleted.
- MCP mutations continue to the Tool Gateway; the A2A Gateway is related to Chapter 1's gateway table and to the Task Service; remote states map onto the pinned A2A 1.0.1 task-state names.
- The artifact-adoption check moves from Chapter 6 into Chapter 19 as the tested `artifact-adoption` example, now with a content-hash check. The uncited MLflow MCP Registry version claim and untested adapter are removed.

### Part II (Chapters 4–6) continuity pass

- Chapter 4 is now the book's map: it opens on the mortgage case and the Chapter 3 seam, uses the seven plane names in the tables and in Figure 4-1, maps Figure 1-3's bands onto them, renames layers so none is called "plane", and indexes every authoritative record to its owning plane and defining chapter.
- Chapter 4 receives the LLM Gateway contract from Chapter 19, explains the global control tier and regional execution cells in one section, annotates the end-to-end flow by owning plane (Figure 4-2 now assembles context before the step and shows the optional approval hop), and owns one base Run API table (`/audit` removed).
- The RunManifest gains prose and moves, with the artifact reference and the single CloudEvent shape, into the new `contracts#platform` example; the inline JSON and Python listings are gone and the effect receipt no longer contradicts Chapter 22.
- Chapter 5 uses "enforced rule" rather than "guardrail" (text, Figure 5-2, and the example class), adds the owner **Approve** step, moves the Knowledge Hub after provenance with a mode mapping and its two callers, and receives index freshness from Chapter 6.
- Chapter 6 has one ten-stage pipeline, five context sources, one segment `kind` enum mapped to trust tiers, memory in one section, and one ContextManifest schema in the new `context-manifest` example; the artifact-adoption listing leaves for Chapter 19.
- Approval terminology, Harborlight case boxes (Northstar removed), "Strong answer" and ✓ template forms, and Chapter 17 anti-pattern pointers are applied across Part II; the Chapter 4–6 covers follow the renamed components.

### Front matter and Part I (continuity review, WP-FM and WP-I)

- Front matter: reader paths now include their prerequisites; "How the book is organized" matches Figure 0-1, whose labels are now the exact Part titles; the engineering contract is condensed and points to Chapter 2's principles; maintainer content and the supplier-onboarding promise are gone; the Closing Perspective is listed.
- Chapter 1 opens with the demo, states the thesis once, explains the state-owner table that later chapters reuse, shows checkpoint C01, maps the three per-step questions and the ten problems to the chapters that answer them, and fixes vocabulary pointers. "Agent Gateway" becomes the A2A Gateway (Figure 1-4); Figure 1-3 shows Channels as Parts II and IV.
- Chapter 1's prototype and level sketches are now a tested example (`prototype-levels`), whose test reproduces the Wednesday duplicate write.
- Chapter 2 names the six gates as the deterministic shell, gives each gate an owner, places human approval inside Authorize, defines acceptance criteria and the acceptance engine, and uses `proposed_action` and the second pay statement in its proposal.
- Chapter 3 is about a quarter shorter: previews of approval, handoff, guardrails, retries, and the write path collapse into one section that points to the owning chapters; AgentRuntime is defined before the checkpoint; the step status enum and the step-to-gate bridge are stated; the restart and replaceability tests are paired; `contracts#step` moves here from Chapter 1.
- Northstar and the supplier-onboarding thread are retired from Part I; approval terminology follows Chapter 14.

### Part VII — evidence, evaluation, and improvement (continuity review, WP-VII)

- Chapter 24 is the home of observability: one decision-centric span schema (decision, memory, and security-control spans; `effect.state` on tool spans), the single metric scorecard, and the telemetry implementation (collector, trace index, content vault, audit ledger writer) moved in from Chapter 25.
- Chapter 24 states the four authoritative records (trace, workflow history, effect ledger, audit ledger), names the causal run trace and trajectory, separates workflow replay, diagnostic replay, and fork, and absorbs Chapter 7's first-divergence steps into a five-step § Debugging method that the worked example now follows.
- Chapter 25 is reordered: release gate, test layers, worked example, runtime/offline boundary (now with a test, placements, and a Harborlight example), the learning loop with defined records and an automate/govern/never table, then evaluation-only implementation.
- Chapter 25 defines EvaluationResult, ValidationReport, and ReleaseGateDecision; one test-layer table replaces the pyramid list; the waiver path and the Chapter 13 versus release-gate distinction are explained.
- MLflow claims are limited to what R20/R21 support; the Agents SDK tracer default is now a tested statement about the pinned package.
- The trajectory example adds a deterministic `forbidden_tool_absent` scorer, and its judge no longer assesses authorization.
- Figures 25-2 and 25-3: runtime lane matches the prose; Approve reads "owner or pre-approved class".

### Part IV — patterns that work and those that fail (continuity review)

- The Part IV orientation now links the patterns to the Part III platform and states the three questions every pattern chapter answers.
- Chapter 10 separates stopping (controller) from acceptance (acceptance engine), aligns its typed decisions with the shared contracts, and defines observations and information gain.
- Chapter 11 is now the home of handoff: framework handoff versus accountable handoff, the ownership table, and the acknowledgment protocol. Figure 11-1 shows eligibility before classification, and a new tested `route-validation` example replaces the inline router.
- Chapter 12 is reordered around the Plan IR: a risk-class gloss, a node-kind map to Part IV, compile-time checks next to the IR, and one revision section.
- Chapter 13 defines the acceptance engine and `AcceptanceDecision`. A tested `evaluator-optimizer` example replaces the inline listing that let the evaluator approve its own work, and Figure 13-1 runs executable checks before an advisory judge.
- Chapters 10–13 use "<Pattern> at a glance" cards, claim rows instead of generic evidence boxes, and drop R13/R07 citations that supported no claim.
- Chapter 14 names three human controls (approval, intervention, operator control) and adds an intervention contract. Every Part IV escalation now lands as a typed InterventionTask. The approval field list appears once, uses the `ApprovalRequest` / `ApprovalDecision` names, and the divergent inline code is gone.
- Chapter 15 is reordered so the lifecycle comes before its terminal states. It adds the book's run-state table, fills the empty event-driven resume section, links each lifecycle step to its Part IV pattern, and points to Chapters 4, 22, and 27 instead of repeating them. The recovery-objective claim, which exceeded its sources, is replaced.
- Chapter 16 is now a slim Part IV synthesis: a revised decision tree (Figure 16-1) with chapter-labelled leaves, a comparison table of the Chapter 10–15 patterns, and one Harborlight run that composes them. The twelve platform pattern cards move to Appendix A.
- Appendix A holds the twelve P-cards, each tagged with the chapter that builds it, with corrected pairings and rows for the Part IV patterns. P-09 is now "Causal run trace", and P-03 and P-04 follow Chapter 6's authorization order and memory taxonomy.
- Chapter 17 tags each card "Prevented in / Built in" (seven prevented, seven previewed, two built later), moves the prioritization into "How to read a card", and moves its six anti-pattern/correction listings into tested examples (`examples/antipatterns/`). The AP-05 correction no longer retries after a null lookup, and the AP-06 correction keys the commit by the logical effect.
- Terminology across Chapters 14–17: approval rather than "human action authorization", the second pay statement as the missing document, capability envelope plus credential lease (Figure 17-2), and no Northstar or supplier-onboarding examples.

### Shared contracts and examples (continuity review, Phase 1)

- `AgentDecision.disposition` gains `proposed_action`: `invoke_tool` is a read, and a mutation leaves the loop as a proposal.
- `ReActEngine.run` returns an `AgentStepResult`; a tripped bound is `status: failed` with `error_code` `budget_exhausted` or `no_progress`, not an exception.
- One `RiskClass` enum (R0–R4) replaces integer risk in `PlanNode`, `SkillRequirement`, `SkillManifest`, and `PlanEnvelope`; the Skill field is now `risk_ceiling`.
- The Skill registry keeps lifecycle state (the six states of Chapter 8) in registry-side release records, so promotion never moves a manifest digest.
- The effect-idempotency example implements Unknown: a timeout is never re-applied until reconciliation; only a received decline releases the key.
- Approval records are `ApprovalRequest` / `ApprovalDecision`, issued by `ApprovalService`, in the examples and `mortgage_case/`.
- Examples and tests use the second pay statement (`pay_statement`) as the missing document.

### Part VIII and the Closing Perspective (continuity review, WP-VIII)

- Chapter 26 now holds governance's own mechanism: use-case tiers T0–T4 related to effect risk classes R0–R4 and change classes, a release review-depth rule, control-hierarchy and cadence tables, an expiring-exception lifecycle, and the governance inventory, exception API, GovernanceRecord, and ExceptionWaiver moved from Chapters 23 and 27.
- Chapter 27 defines one release chain (ChangeBundle → ReleaseManifest → EnvironmentBinding → RunManifest), teaches release contents once, adds a seven-step regional recovery sequence, uses "global control tier" and "regional execution cell", and moves the baseline technology stack to Appendix D.
- Chapter 28 is reordered to measure → optimize → admit → degrade, separates permit-holding work from waiting runs in its Little's Law example, receives Chapter 19's policy-first model routing, and merges its duplicated concurrency lists.
- Inline Python in Chapters 27 and 28 is replaced by tested examples: `release-compatibility` (typed `WorkerProfile`), `release-attestation` (binds verified identities to the artifact), and `admission-permit` (grant, defer, or reject).
- Northstar boxes become mortgage-case boxes; numeric "guardrails" become "starting limits"; Figures 26-1, 27-1, and 28-1 and the Chapter 26 cover are corrected.
- The Closing Perspective now follows Chapter 28, replays Chapter 1's Monday–Friday failures against the controls that contain them, and states that only checkpoints C01–C03 are implemented.

### Part VI — Security, Identity, and Control (continuity review, WP-VI)

- The Part VI orientation states the "assume manipulation" premise once and maps Chapters 20–23, replacing a control order the chapters contradicted.
- Chapter 20 keeps "guardrail" in its detector sense only, has one nine-layer model (Figure 20-1 redrawn to match), and gives every threat card a first deterministic refusal layer. Figure 20-3 now shows the detector feeding the policy engine. It gains opening boxes and an incident section cited to NIST SP 800-61 [R42].
- Chapter 21 is reordered: subject, actor, and purpose; then the decision; then how authority travels, with capability envelope (scope) and credential lease (proof) defined. The subset proof is the new `capability-envelope` example.
- Chapter 22 is one argument with one implementation block. It defines Unknown canonically, relates risk classes to use-case tiers, and drops the inline ledger in favor of the `effect-idempotency` example. Figure 22-1 reserves the effect before approval.
- Chapter 23 continues the Chapter 20 example rather than retelling it. It drops its duplicate layer list, threat table, and credentials API, and adds kill-switch and data-lineage/privacy sections. Its code is now the `egress-url` and `kill-switch` examples, without the unrelated RTO/RPO class. The governance record moves to Chapter 26.
- Approval terminology replaces "human action authorization" throughout the Part. Chapter 21 and 23 cover labels follow the revised text.

### Part III — developer platform (continuity review, WP-III)

- The Part III orientation names the three owners and frames Chapter 7 as a forward map. The capability table gains a "Taught in" column, merges workflow and durable execution, and moves "action policy" out of Guardrails.
- Chapter 7 adds a third owner (domain-capability owners of Skills and Skill Packs). It points to Chapter 3 for the runtime seam, Chapter 25 for test levels, and Chapter 24 for debugging, and § If this fails becomes platform-failure triage. Figures `developer-lifecycle` and `test-pyramid` are retired; the golden-path figure shows the table's eight stages.
- Chapter 7's inline SDK and CLI listings become prose using the case identifiers. A new `adapter-conformance` example makes the portability evidence executable.
- Chapter 8 removes lifecycle and `side_effect_class` from the manifest and uses `risk_ceiling: R1`. It defines what a Skill version promises, separates Skill, tool, agent, and pack, explains how a resolved Skill reaches the step without authorizing its calls, and reconciles the four binding moments. Discovery is "broad", not "permissive".
- Chapter 9 explains the CompatibilityReport checks, pack lifecycle versus aliases, ownership, and the ReleaseManifest-to-RunManifest link. Its broken inline excerpt is replaced by the new `skills-registry#packs` region (`SkillPackRegistry`).
- The Northstar box becomes a mortgage-case box; deployment terms follow "global control tier" and "regional execution cell".

### Cover artwork and version labels

- Removed printed release numbers from the book cover and all 28 chapter covers; regenerated the cover artwork and synchronized publication artifacts. The release identifier remains `v1.0.0` in metadata, filenames, title page, and running footers.
- Corrected the active continuity review map to identify the current book as v1.0.0.

### Repository maintenance

- Removed the closed full-book review plan and unreferenced `proposals/` draft, retaining their history in git.
- Added a whole-book continuity and flow review under `reviews/continuity-and-flow/`.

## [1.0.0] — 2026-09-13

First public release of *Building an Enterprise General Intelligence Platform* by Reza Rahimi, PhD. Earlier working drafts carried the labels v2.x and v3.x; those are retired, and 1.0.0 is the only release version. The draft changelog is in git history.

### The book

- 8 Parts, 28 chapters, and 12 appendices, each Part and chapter opening on a new page; every chapter is preceded by its full-page Letter cover (`cover-images/`) in the DOCX and XeLaTeX editions.
- One running example, the Harborlight mortgage case, carried through the chapters, with a cumulative implementation under `mortgage_case/` and the roadmap in `code-gap.md`.
- Canonical prose in `source/parts/*.md`; the DOCX, XeLaTeX, and distributable Markdown editions are generated from it, with a cross-format contract in `styles/`.
- Every citation resolves to `config/references.json` with a recorded scope; Appendix K is generated from it, with the claim-scope traceability matrix.
- Every diagram is rendered from an editable source in `assets/diagrams/src/` (vector PDF for XeLaTeX, PNG for DOCX) and registered in `config/diagrams.json`.
- Every code listing is a tested file under `examples/`, registered in `config/examples.json` and executed in CI.

### Versioning

- Book version is `1.0.0` in `config/book.json`, the title page, running footer, and the artifact names `Enterprise-General-Intelligence-v1.0.0.{md,docx,tex,pdf}`.
- The stale-label validator now rejects any `v2.x` or `v3.x` label in the manuscript.
- The pre-release DOCX layout baseline is renamed `latex/reference/DOCX-layout-reference-draft.pdf` so its name no longer implies it matches v1.0.0.
