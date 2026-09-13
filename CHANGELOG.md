# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

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
