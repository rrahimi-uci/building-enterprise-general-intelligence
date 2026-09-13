# Changelog

All notable changes follow semantic versioning and are recorded here.

## [2.0.0] — 2026-09-13

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

- Established the first canonical Book v1.0.0 release under the title *Enterprise Agentic AI Architecture & Developer Platform Guide* by Reza Rahimi, PhD.
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
