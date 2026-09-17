# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

### Apply the reviewed v2.1.0 DOCX edits across publication formats

- Reconciled the reviewed DOCX wording into the canonical Markdown parts and
  regenerated the distributable Markdown, DOCX, and XeLaTeX source while
  preserving the 8-Part / 28-chapter / 12-appendix topology.
- Applied the reviewed reader-facing headings, evidence callouts, chapter and
  appendix transitions, pattern catalog, and threat catalog consistently
  across the book.
- Updated the generated claim-traceability heading and its structural
  validator contract; preserved code listings, diagrams, citations, examples,
  and stable identifiers.

### Full-book style, tone, and readability pass

- Reworked the front matter, Part orientations, all 28 chapter titles, and the
  appendix titles in a clearer practitioner voice while preserving the
  eight-Part / 28-chapter / 12-appendix topology.
- Replaced repetitive specification-like section labels with reader-facing
  headings and gave every chapter a concise explanation of why its boundary
  matters, when it becomes important, and what can fail without it.
- Expanded the chapter openings and transitions so the Harborlight case and
  the architecture story remain connected from model output through operation.
- Synchronized the title registry and implementation roadmap with the revised
  chapter names; no citations, diagram identifiers, contracts, or code-example
  identifiers were changed.

### Complete the full-book review and publication closeout

- Reconciled human action authorization terminology across the primary source,
  runnable examples, tests, Appendix C, and the proposal-binding diagram while
  preserving `LendingDecision` as a separate underwriter-owned record.
- Corrected example registry chapter metadata and the examples README, fixed
  the Appendix I companion title, and clarified Northstar versus Harborlight in
  the closing perspective.
- Added evidence-bounded finding records for every review-matrix row and
  documented the explicit DOCX pagination limitation (`soffice` unavailable)
  and the remaining C04–C28 implementation roadmap boundary.
- Regenerated source-derived Markdown, DOCX, LaTeX, diagram renders, QA
  reports, and final release evidence from the canonical source.
- Added and tested the previously untracked offline platform-contract slice
  under `mortgage_case/platform/`, wired its mortgage tests into
  `make examples-run` and CI, and documented that it is partial C04–C28
  evidence rather than complete stage-registered checkpoint implementation.

### Make the cumulative Harborlight path explicit in the foundations

- Added a front-matter checkpoint map for implemented `C01`–`C03` and clearly
  separated those implemented foundations from the `C04`–`C28` roadmap.
- Reframed the opening of Part I so Harborlight Home Finance is the cumulative
  runnable case and the retained Northstar supplier material is explicitly
  comparative architecture evidence.
- Regenerated the canonical Markdown, distributable Markdown, DOCX, XeLaTeX
  source, and validation reports without changing the 8-Part / 28-chapter /
  12-appendix topology.

### Full-book end-to-end review and mortgage narrative reconciliation

- Added `full-book-review-plan.md`, a complete review plan covering content,
  technical accuracy, chapter structure, narrative flow, education,
  consistency, examples, diagrams, references, formatting, and reader
  experience.
- Reconciled the primary narrative and chapter transitions around the
  Harborlight mortgage case `MORT-2026-000184`, while preserving broader
  enterprise scenarios as labeled comparative examples.
- Aligned primary examples, exercises, security/effect walkthroughs, and
  Appendix I with the mortgage implementation and clarified the distinction
  between human action authorization and an underwriter-owned lending decision.
- Regenerated the four edited diagrams and updated the diagram registry
  checksums; removed stale manual figure captions and historical fixed counts
  from the style contract.
- Removed duplicate imports in validation/package tooling and rebuilt the
  synchronized Markdown, DOCX, LaTeX, QA, manifest, checksum, and package
  artifacts.

### Align all book code with the mortgage case

- Migrated the domain-specific runnable examples, tests, and inline code
  identifiers from the retired supplier/refund scenarios to the cumulative
  Harborlight mortgage case `MORT-2026-000184`.
- Connected tool loops, bounded ReAct, handoffs, guardrails, approvals,
  idempotency, capability and Skill resolution, policy rules, durable events,
  MLflow traces/evaluation, and runtime fixtures to mortgage evidence review,
  missing employment-verification evidence, and human underwriting handoff.
- Kept algorithmic examples framework- and domain-neutral where that is the
  lesson, while ensuring their executable tests use the mortgage case at the
  domain boundary.
- Regenerated the canonical Markdown, DOCX, LaTeX source, validation reports,
  and release evidence after the migration.

### OpenAI SDK and MLflow grounding audit

- Pinned the offline example profile to `openai==3.13.0`,
  `openai-agents==0.22.2`, and `mlflow==3.15.2`, and aligned the registered
  examples with those package boundaries.
- Added an offline mortgage integration that executes the real OpenAI Agents
  SDK runner with a scripted model and records its runtime spans in MLflow
  without exposing raw synthetic case content.
- Added real `mlflow.genai.evaluate` and trajectory-evaluation examples,
  direct OpenAI Responses API adapter contract coverage, and corrected source
  sketches for SDK invocation, trace privacy, guardrails, and Decimal money.
- Preserved the provider-neutral platform contracts and documented the
  remaining cumulative-example implementation gaps in `code-gap.md`.

### Mortgage cumulative-example foundation

- Added the synthetic Harborlight mortgage anchor case `MORT-2026-000184` and
  the first three executable checkpoints: read-only evidence summary, typed
  deterministic proposal shell, and a provider-neutral bounded runtime.
- Added offline unit/contract coverage, an opt-in OpenAI Responses adapter, an
  opt-in OpenAI Agents SDK adapter, the `C01`–`C28` checkpoint registry, and a
  reader-facing cumulative example listing.
- Extended Part I with the business problem, actors, inputs, workflow,
  constraints, success criteria, visible bottlenecks, and before/added/after
  transitions. Existing supplier material remains retained as labeled contrast
  content.
- Added the registered mortgage lifecycle diagram and regenerated synchronized
  Markdown, DOCX, and XeLaTeX source artifacts. The 8-Part / 28-chapter /
  12-appendix topology remains unchanged.

### Northstar cumulative-example implementation roadmap

- Added `code-gap.md`, a chapter-by-chapter implementation roadmap for evolving
  one runnable Northstar supplier-onboarding example from a simple bounded agent
  into a production-grade enterprise agentic system.
- Recorded the current gap between the book’s cumulative prose narrative and
  its 23 isolated, tested examples; defined the canonical case, technology
  ownership, stage dependencies, PR order, failure scenarios, acceptance gates,
  and relevant implementation modules.
- Added a full-book editorial-audit addendum that keeps the current publication
  artifacts separate from the future cumulative-example implementation work.

### Chapter 3 review reconciliation and cross-book consistency

- Rebuilt Chapter 3 around the Northstar supplier-onboarding scenario, carrying one concrete execution path from durable workflow request through bounded agent reasoning, gateway authorization, approval, business effect, receipt, and audit evidence.
- Clarified the ownership boundary between the AgentRuntime adapter, the agent framework, and the enterprise platform: framework mechanics stay local, while workflow state, identity, authorization, credentials, policy, budgets, approvals, effects, receipts, artifacts, and audit remain durable platform contracts.
- Added practical guidance for exact-resource authorization, proposal-versus-effect semantics, restart recovery, approval-hash binding, handoff meanings, retry ownership, SDK upgrade manifests, replaceability testing, production readiness, and boundary-focused debugging.
- Reused the existing registered and tested bounded-step example, added the registered editable `runtime-boundary` diagram, and tightened the responsibility matrix for print-scale scanning. Preserved the eight-Part / 28-chapter / 12-appendix topology, and verified the table of contents and reference contracts during the rebuild.

### Chapter 2 review reconciliation and cross-book consistency

- Reworked Chapter 2's deterministic-shell flow so the single gate table follows the concrete proposal, while the surrounding prose explains the distinct validation, authorization, resource-version, and deterministic-acceptance boundaries without repetition.
- Removed the redundant Chapter 2 grounding subsection and replaced its debugging playbook with an intent-to-execution trace, final-boundary verification, and idempotent-replay checks.
- Replaced the unreadable, non-runnable Tool Gateway excerpt with a readable, offline-tested example covering tool eligibility, delegated authority, stale-state rejection, durable-effect semantics, and unknown outcomes; all instructions and control decisions are visible line by line.
- Standardized Python listing labels as 🐍 across the canonical book and generated renderers, including the portable XeLaTeX fallback, and synchronized the examples guide and generated release artifacts.
- Preserved and verified the authored 8-Part, 28-chapter, 12-appendix table of contents and all reference/cross-reference contracts.

### Generalized the first-30-page editorial review across the book

- Retitled the book and aligned its audience promise, preface, scope discipline, reproducible-edition explanation, and reference-guide contract with the reviewed direction.
- Standardized the progression vocabulary from “rung” to “level,” corrected chapter and Part labels, and removed stale embedded topology maps and redundant early chapter boilerplate.
- Expanded the control-point model to include agent admission and human approval, clarified lifecycle acceptance/evaluation gates, and synchronized the related prose and diagrams.
- Reframed Chapter 25 as governed continuous learning and updated the cover configuration, repository map, and chapter registry to the canonical eight-Part, 28-chapter, 12-appendix topology.

### Part VIII teaches governance, release recovery, and operating economics

- Expanded Chapters 26–28 with a governance control-loop explanation, a decision-and-evidence table, an immutable release walkthrough, and a quarter-end capacity-planning scenario.
- Added practical explanations of risk ownership, active-run compatibility, rollback boundaries, Little’s Law as a planning estimate, fair scheduling, safe degradation, and cost per verified successful outcome.
- Added two editable, registered diagrams: release promotion and recovery without rewriting active history, and admission/execution feedback for outcome-based optimization.
- Preserved the existing Part VIII contracts, implementation references, citations, and eight-Part / 28-chapter / 12-appendix topology.

### Part VII teaches traces, evaluation gates, and governed learning

- Expanded Chapters 24–25 with progressive explanations of causal traces versus audit evidence, outcome versus trajectory evaluation, deterministic checks versus calibrated judges, and slice-aware release decisions.
- Added a worked Northstar slow-refund trace walkthrough, a protected-slice regression scenario, trace/evidence tables, and a candidate evaluation gate that turns failures into reviewed regression cases.
- Added two editable, registered diagrams: asynchronous causal tracing with a separate audit ledger, and risk-tiered evaluation with deterministic checks, calibrated quality evidence, and release feedback.
- Preserved the existing continuous-learning and runtime/offline boundary diagrams, examples, citations, and the eight-Part / 28-chapter / 12-appendix topology.

### Part VI teaches security as containment, identity as delegation, and effects as evidence

- Expanded chapters 20–23 with progressive explanations of detector, policy, and enforcement boundaries; RBAC versus ABAC; approval, idempotency, preconditions, and reconciliation; and the difference between prevention and blast-radius containment.
- Added a worked Northstar supplier-document attack path, an incident-response phase table, a subject/actor/purpose table, an effect-property comparison, invocation stages, and a sandbox/egress boundary table.
- Added three editable, registered diagrams: subject and actor delegation, the protected-effect lifecycle, and containment across sandbox, egress, credential, DLP, and effect boundaries.
- Removed stale unregistered figure labels and the duplicated Part V orientation that followed chapter 23, preserving the eight-Part / 28-chapter / 12-appendix topology.

### A whole-system view before the details

- Chapter 01 gains **"The system in one view"**: one diagram of the complete architecture, annotated with the Part that details each band, plus a table mapping band to Part. A reader now has somewhere to put every later chapter before any of it is justified.
- Two properties are stated up front because they govern everything after: authority narrows downward — the agent proposes, the platform authorizes, and only the bottom bands commit — and security spans every band rather than being one of them.

### Tool Gateway and MCP Gateway are different components

- The book used both names without ever saying how they relate, and the gateway comparison table that distinguishes API, Agent, LLM and MCP gateways **omitted the Tool Gateway entirely** — the book's most-referenced control point. That omission is why the relationship was unclear.
- Chapter 01 gains **"Four control points, four different questions"**, naming what each gateway decides and what it does not: API admits the caller, LLM chooses the model, Tool authorizes the effect, MCP establishes server trust.
- The Tool Gateway is deliberately protocol-agnostic. Effects arrive over REST, gRPC, a database transaction, a queue and MCP, and the control must be identical for all of them. A tool invoked over MCP still passes the Tool Gateway, because MCP describes how a tool is discovered and called — not who may call it, whether the effect is idempotent, or what evidence is recorded.
- The Tool Gateway row is added to the gateway comparison table in chapter 19.

## [2.1.0] — 2026-09-14

### Every diagram redesigned, from editable sources

- All 20 diagrams are rebuilt from scratch as **editable sources** in `assets/diagrams/src/` — Graphviz `.gv` for structure and flow, Mermaid `.mmd` where a sequence diagram genuinely reads better. A contributor changes the source and runs `make diagrams`; nobody has to recreate a figure from its rendered image again.
- Each source renders twice: a **vector PDF that XeLaTeX embeds**, so figures stay sharp at any zoom and in print, and a raster PNG for the DOCX edition, which cannot embed PDF. The book's figures were previously 1800×1000 rasters that softened when scaled.
- A shared house style in `_theme.gv` is spliced in at render time, so restyling the book is one edit. **Role is carried by colour and shape together** — teal runtime, blue service, indigo store, cyan knowledge, amber decision, slate external, plum effect, red anti-pattern — so a figure is readable without a legend and survives greyscale print.
- Diagram form now follows the concept rather than one template: layered models for planes, sequence diagrams for protocols, decision trees for selection, a cycle for the improvement loop, side-by-side clusters for before-and-after.
- Raster dpi is computed per diagram from its natural width, because a narrow figure stretched to the column would otherwise fall below the resolution contract. Every render now measures 291 dpi or better.
- `validate_latex.py` gates that each diagram keeps an editable source and a vector render, so a future figure cannot be added as an orphan image.
- **Fixed a figure-caption defect affecting all 20 figures.** LaTeX's automatic `Figure N:` label printed in front of the book's own chapter-relative number, so every caption read "Figure 2: Figure 4-1 — …". The automatic label is suppressed; the book's numbering, which the prose cross-references, stands alone.
- Fixed Mermaid renders being written with a transparent background, which composites as black anywhere a consumer flattens without a white ground. Caught by reviewing all twenty together on a contact sheet.
- Removed `tools/generate_diagram.py`, superseded by `tools/render_diagrams.py`. Keeping two generators is the drift problem this release has been removing everywhere else.

### Retitled

- The book is now *Enterprise General Intelligence: Architecting Governed Agentic Systems for the Enterprise*, replacing *Enterprise Agentic AI Architecture & Developer Platform Guide*.
- Artifact filenames follow the title: `Enterprise-General-Intelligence-v2.1.0.{md,docx,tex,pdf}`.
- The cover, title page, PDF and DOCX metadata, and the running header now read their wording from `config/book.json` rather than from strings hard-coded in three generators, so the next retitle is one edit. The cover subtitle is set at 44pt, measured to stay inside the darkened zone rather than running across the illustration.
- `validate_book.py` derives the expected DOCX title and cover path from configuration instead of asserting literals that a retitle would silently invalidate.

### New chapter: Enterprise Knowledge Management for Agents

- Added chapter 05, arguing that an agent needs a governed knowledge layer rather than a retrieval index, and separating the four ways agents consume knowledge — context, reasoning, constraints, and action — each with its own failure mode.
- Covers semantic knowledge, ontology and graph, rules as enforceable constraints, business data and capability catalogs, BPMN/DMN/CMMN/SBVR, the extract–prove–project pipeline, a knowledge algebra, and governance metadata, closing on a knowledge-hub reference architecture.
- Six runnable, CI-executed examples: typed rules with provenance, independent grounding verification, bounded graph traversal, a rule enforced at the effect boundary, union/intersection/difference/contradiction over rule sets, and capability discovery filtered by effect, grant, prerequisite and data class.
- Two new diagrams and five new citations. The four OMG standards were verified against their specification index pages: BPMN 2.0.2 (2014), DMN 1.5 (August 2024), CMMN 1.1 (2016), SBVR 1.5 (2019). The 44% grounding-rejection figure is recorded as one run of one pipeline, not a general rate.

### Chapter 19 moved into Part II

- *Context Engineering, RAG, Memory, and State* had sat in the security Part since v1.0.0 despite being neither security nor identity. It is now chapter 06, beside the knowledge chapter: durable governed knowledge first, per-run context second, which is the boundary the two chapters draw between themselves.
- Part II grows from one chapter to three and is retitled *Enterprise Reference Architecture & Knowledge*. Part VI is left as four security chapters.
- Three transitions were rewritten rather than renumbered, because the chapter each one hands to changed.

### Gates that were literals are now derived

- Diagram count, diagram paths, citation occurrences, and reference targets all follow their registries instead of asserting 18, 18, 94 and 43. Adding a figure or a citation is now a registry edit rather than a validator edit.
- Fixed `tools/generate_diagram.py`, which had been unusable: it passed a bare hex string to Pillow, which newer versions reject.

### Part divider artwork

- The eight Part dividers now carry an illustrated panel alongside the Part number, title, and orientation paragraph, in both the DOCX and XeLaTeX editions at the same 4.8in width.
- Source artwork is kept as immutable provenance in `source/part-visuals/`; `tools/prepare_part_visuals.py` crops it into `assets/parts/` deterministically, and `config/part-visuals.json` records the mapping and each panel's digest.
- **Only the artwork panel is used, not the supplied full-page visual.** The source images were authored for the v1.0.0 twelve-Part structure and bake in their own PART badge, Part title, focus line and a "BOOK v1.0.0" footer. Used whole, five of the eight would have shown the wrong Roman numeral and all eight a stale release. Cropping to the artwork lets the renderers draw Part identity from the canonical Markdown, where it is correct by construction.
- Where v2.0.0 merged two Parts, the visual of the dominant subject is used. Four Parts are therefore represented by component labels that cover most, not all, of their chapters — see the note in `config/part-visuals.json`.
- The DOCX image-count check is now derived (cover + registered diagrams + registered panels) instead of asserting a fixed 19, and both validators verify panel digests and the 255 dpi effective-resolution contract.

## [2.0.0] — 2026-09-13

### Every oversized listing promoted to a verified example

- The six listings too long to fit a page (82–153 lines) are now real files under `examples/`, shown through named regions. Page splits fell from 9 to **3**, and all 51 listings are verified rather than 9.
- Added **named regions** (`[[EXAMPLE:id#region]]`), so one verified file can serve two chapters at two depths.
- **Removed a genuine duplication:** the agent-step contracts were defined twice, in chapters 01 and 04, and the copies had already drifted — the shorter was not even a prefix of the longer. Both now render from one tested `examples/contracts.py`: chapter 01 shows the five-type step region, chapter 04 the full eight-type platform set.

### Defects found by making the listings run

- **`ReActLimits` was missing its `@dataclass` decorator.** `dataclass` was imported but never applied, so `__post_init__` never ran and the "all ReAct limits must be positive" validation was dead code. The class could not be constructed with arguments either.
- **`DecisionModel` and `ToolInvoker` were referenced but never defined.** The ReAct listing imported `Protocol`, `Awaitable`, and `Callable` to declare them, but the declarations were absent — the code as printed did not run.
- **The step adapter read `os.environ["OPENAI_AGENT_MODEL"]` at import time**, making the module unimportable wherever that variable is unset. It now reads with a default, and takes an injectable model so a platform can test a step without a provider.

### Verified examples across the book

- Nine runnable, CI-executed examples now appear in nine chapters, covering the OpenAI Agents SDK and MLflow: a bounded agent loop with a typed tool (ch 02), a ReAct loop with an explicit run budget (ch 08), routing by handoff (ch 09), a human approval gate that survives the wait (ch 12), an input guardrail that trips before any tool runs (ch 18), an effect-idempotency ledger (ch 21), MLflow trace configuration and tracing (ch 23), and dataset evaluation with scorers (ch 24).
- Agent examples run offline against the scripted-model harness, so CI executes the real SDK control flow with no API key. The guardrail test asserts the model was never consulted at all — the property the architecture actually claims.
- Code listings rose from 43 to 51, and split listings fell from 20 to 9.
- Added `asyncio_mode = "auto"` so the book's async listings carry no per-test markers that teach nothing about agents.

### Validator fixes found while wiring the examples

- **`validate_book.py` read Python comments as Markdown headings.** The heading-level check scanned the raw manuscript, so a line like `# Captures OpenAI calls` inside a fenced block counted as an H1 and produced spurious "skips from H1 to H3" errors. Fenced code is now masked before the scan, with line numbers preserved.
- **The code-block count is now derived from the manuscript**, like the table count, instead of asserting a fixed 43. Both checks exist to prove every block reached the PDF; a literal only proved the book had not changed.

### Topology: 12 Parts / 31 chapters / 15 appendices → 8 / 27 / 12

- Dissolved the four Parts that held a single thin chapter each. Part V (anti-patterns) joins Part IV as *Patterns and Anti-Patterns*; Part VII (LLM Gateway) joins integration; Part X (continuous learning) joins observability and evaluation; Part XI (governance) joins production operations. A full-page navy divider for a 471-word chapter was structure the content did not earn.
- Merged four chapter pairs where one member was too thin to stand alone: 04+05 → *Enterprise Reference Architecture, Boundaries, and Contracts*; 06+07 → *Agentic Developer Platform, SDK, and Delivery Lifecycle*; 19+20 → *External Integration: MCP, A2A, and the Model Control Plane*; 27+28 → *Evaluation, Debugging, and Continuous Improvement with MLflow*. Chapter sizes now range 1,064–3,393 words instead of 471–3,393.
- All 27 chapter-to-chapter transitions are preserved and retargeted. Only the four inner transitions of merged pairs were dropped, because they pointed at a chapter the reader is now already inside.
- Cut Appendix L (release history) and Appendix N (assurance coverage): both recorded build process rather than reader-facing material. Folded the former Appendix M (claim traceability matrix) into Appendix K as a section, next to the entries it scopes — the 23 chapter references to "Appendix M" now point at Appendix K, which actually contains the matrix.
- Refilled Appendix I. It was a seven-word stub followed by a stray H1 that broke the appendix's own heading hierarchy; the Northstar reference-implementation content is now the appendix body where it belonged.
- Rebuilt the table of contents and the reader map from the real structure rather than maintaining them by hand.
- Every cross-reference remapped: 62 chapter references, 12 Part references, 37 appendix references.

### Build and validation

- Version bumped to 2.0.0 across metadata, artifact filenames, page furniture, and PDF metadata. The v1.0.0 cross-format baseline PDF is retained and relabelled `DOCX-layout-reference-v1.0.0.pdf`; it is no longer asserted against the current page count, because the topology deliberately changed.
- The LaTeX validator now derives the expected table count from the manuscript instead of asserting a magic 260. The check exists to prove every Markdown table reached the PDF; a fixed number only proved the book had not changed.
- Tightened the stale-release-label guard, which matched the real `v2.0.0` string against the legacy `v2.0` pattern.
- 232 pages, down from 244, with 0 errors and 0 undefined references.
- Removed `qa/render/` — 20 page images and a contact sheet rendered from the v1.0.0 pagination. They document a layout the book no longer has. Regenerate with `make qa-pdf` on a machine with LibreOffice before cutting the v2.0.0 release.

### Callout taxonomy and a DOCX accessibility fix

- Added eight guidance-box kinds — best practice, architecture guidance, developer guideline, production consideration, security and governance, common pitfall/anti-pattern, performance and cost, and observability tip — and used all eight across fourteen chapters.
- Moved the taxonomy into `tools/callouts.py`, which both renderers import. A duplicated mapping in two renderers drifts the first time a kind is added to one, and the cross-format contract forbids that.
- **Fixed a shipped accessibility defect in the DOCX edition.** All 44 `NORTHSTAR AT THIS POINT` and `DESIGN DECISION` callouts were shaded navy `#102A4C` while `Book Callout` inherits Normal's ink `#12233F` — a contrast ratio of **1.09:1** against the 4.5:1 requirement, making them effectively invisible. They now use the pale ground at 13.99:1. The LaTeX contrast gate never caught it because it only reads the LaTeX palette.
- Added `docx_callout_contrast()` to `tools/validate_book.py` so every shaded callout cell is gated in the DOCX edition too, and added ten pairs to the LaTeX contrast gate. 23 pairs are now tested; the lowest is 6.08:1.
- Documented the taxonomy in `styles/DESIGN-SYSTEM.md` with the test for whether a box earns its place, and recorded the palette in `config/style-tokens.json`.

### Runnable, CI-verified code examples

- Added `examples/`: code listings are now real files that CI executes, not prose. `config/examples.json` registers each one, and `tools/assemble_manuscript.py` expands `[[EXAMPLE:id]]` markers at assembly time so the Markdown, DOCX, and XeLaTeX editions all carry identical code and no listing can drift from the file under test.
- Added `examples/_harness/scripted_model.py`, which implements the OpenAI Agents SDK `Model` interface and replays a fixed script. Agent examples therefore exercise real tool dispatch, structured output parsing, and the run loop with no network and no API key. It must subclass `Model`: the runner resolves `RunConfig.model` with an `isinstance` check, so a duck-typed double is silently ignored and the run reaches the real provider.
- Added `tools/check_examples.py`, wired into `make validate`: every `[[EXAMPLE:id]]` resolves, every registered example is cited, every excerpt region closes, and `--run` executes the suite.
- Pinned `openai-agents==0.22.2`, `mlflow==3.15.2`, `pydantic==2.13.5` in `examples/requirements.txt`, deliberately separate from the book's own dependencies so the manuscript still builds without them.
- Migrated chapter 26's MLflow listing to the new mechanism as the reference case. Verified the chapter's existing API claims hold against the pinned MLflow: `mlflow.genai.judges.make_judge`, `ToolCallCorrectness`, `ToolCallEfficiency`, and `mlflow.openai.autolog` all exist.
- Recorded two MLflow 3.15 behaviours the examples must respect: the filesystem tracking store is in maintenance mode for traces, so a database backend is required; and trace export is asynchronous by default, so assertions must force synchronous export or flush.

### LaTeX page composition

- Code listings that fit on a page are no longer split across one. `render_code` reserves the listing's height with `\needspace`, capped at 643pt because `\textheight` is 698.85pt and a longer listing must break however much space is reserved. Splits fell from 20 to 10; the remaining ones are listings of 82–153 lines, which are editorial debt to be trimmed with example region markers.
- Long tables no longer strand a header at the foot of a page: `render_table` reserves the header plus several body rows. Stranded headers fell from 17 to 6.
- Page count moved from 235 to 242, and mean page fill *improved* from 95.0% to 95.6%.

### Repository structure

- Consolidated the two parallel copies of the v1.0.0 package into a single tree. The repository previously held the Development Package at the root and a complete-with-LaTeX duplicate in `book-latex/`; the LaTeX edition is now the only tree, and `book-latex/` is gone.
- Archived the stray v3.0 Markdown and DOCX exports as `source/original/Enterprise-Agentic-AI-Guide-v3.0-source.*`, completing the v3.0 → v3.1 → v1.0.0 provenance lineage.
- Gitignored `latex/build/` and `dist/*.pdf`. The compiled PDF is published as a CI artifact and attached to GitHub Releases on tag, rather than committed.

### Build and tooling

- Added `tools/bootstrap_tex.sh`, which installs the TeX packages a minimal distribution omits into the user texmf tree without `sudo`, and documents the style-file-to-package mapping.
- Documented four previously unrecorded transitive TeX dependencies pulled in by `tcolorbox[most]`: `environ`, `trimspaces`, `tikzfill`, and `pdfcol`.
- Added `make setup`, `make draft`, `make pdf`, `make help`, and `make distclean`. `make` now defaults to `help`, and every target prefers `.venv/bin/python` when a project virtualenv exists.
- Taught `latex/compile.sh` to find a macOS TeX installation at `/Library/TeX/texbin` and to fail with an actionable message when no engine is present.
- Fixed `tools/package_release.py`, which walked every file under the root and would have packaged `.git/`, `.venv/`, and `latex/build/` now that the package lives in a git repository.

### Continuous integration

- Removed the duplicated source-validation job; the LaTeX workflow now regenerates the LaTeX source, fails the build if the committed generated files are stale, and passes the regenerated source to the compile job.
- Added release publishing: pushing a tag attaches the compiled PDF, DOCX, and Markdown to the GitHub Release.
- Added `workflow_dispatch` and `concurrency` cancellation to both workflows.

### Documentation

- Added `.github/pull_request_template.md` covering goal, approach, architectural decisions, manuscript impact, testing evidence, risks, and deployment implications.
- Rewrote the README repository map around the authored-versus-generated boundary, and added an authoring-loop section, a requirements matrix, and TeX troubleshooting entries.
- Corrected `latex/README.md`, which stated that the package had been built without a TeX engine and that only a DOCX reference PDF existed.

## [1.0.0] — 2026-09-13

### Publication foundation

- Established the first canonical Book v1.0.0 release under the title *Enterprise General Intelligence: Architecting Governed Agentic Systems for the Enterprise* by Reza Rahimi, PhD.
- Re-reviewed the complete book as one narrative: 12 Parts, 31 chapters, and 15 appendices.
- Added explicit Part orientations and 31 curated chapter-to-chapter transitions.
- Removed 22 repeated companion-package paragraphs and stale v2.x/v3.x release labels.
- Preserved the enterprise progression from intent and platform layers through reasoning, orchestration, context, memory, tools, multi-agent collaboration, security, reliability, observability, governance, operations, and evolution.

### Technical and citation quality

- Added a professional numbered References section and a claim-scope traceability matrix.
- Registered 43 primary/credible references and 94 citation occurrences; all reference IDs resolve and all registry entries are cited.
- Scoped evidence so external sources do not implicitly validate book-authored architecture recommendations.
- Corrected the Temporal durable-execution publication year to 2025.
- Added the Amazon Bedrock Agents Classic maintenance-mode/new-customer caveat and AgentCore direction.
- Reframed MLflow 3.15.2 as a reproducibility pin without an unsupported release-date or “latest version” claim.
- Standardized undated living documentation as `n.d.` with access dates.

### Design and rendering

- Created an agent-focused cover and a unified navy/cyan publication system.
- Rebuilt DOCX deterministically from Markdown rather than editing legacy Word XML.
- Added fixed styles for headings, body text, code, tables, callouts, captions, headers, footers, and page numbers.
- Ensured every Part, chapter, and appendix starts on a new page; Part and appendices dividers are standalone.
- Included all 18 teaching diagrams and 19 total inline images.

### Maintainability

- Established `source/parts/*.md` as the editable canonical source and added deterministic assembly.
- Added machine-readable book, diagram, style-token, and reference registries.
- Added reusable build, validation, reference, diagram, QA, deterministic-check, and packaging tools.
- Added a DOCX style template, Markdown component templates, four agent skills, design-system documentation, cross-format rules, contribution guidance, release checklist, checksums, and manifest.
- Preserved original v3.1 sources and legacy generation tools for provenance.

### Validation

- Validated DOCX package integrity, metadata, styles, headings, tables, images, citations, and canonical-Markdown equivalence.
- Rendered and inspected a 213-page Letter-size PDF: 46 chapter/appendix starts on unique pages, 13 standalone divider pages, and no unintended blank pages.
- Added clean-extraction rebuild and deterministic hash checks as release gates.

[1.0.0]: ./
