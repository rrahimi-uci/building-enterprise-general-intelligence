# Changelog

All notable changes follow semantic versioning and are recorded here.

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
