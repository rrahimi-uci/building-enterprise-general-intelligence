# Technical Validation Record — Book v2.1.0

**Result:** PASS; DOCX pagination QA BLOCKED
**Validated:** 2026-09-16

## Final measurements

- 8 Parts; 28 chapters; 12 appendices.
- 45 registered architecture diagrams; 54 DOCX inline images including cover.
- 71 fenced code blocks; 423 DOCX tables.
- 48 registered references; 107 citation occurrences; no unknown or uncited IDs.
- Canonical and distributable Markdown are byte-identical.
- DOCX package opens successfully and contains required named styles and metadata.
- DOCX builds twice to the same SHA-256 hash.
- Genuine XeLaTeX compile: 287 pages.
- 40 chapter/appendix headings are structurally represented in the current source and generated artifacts; the DOCX validator found 28 chapter and 12 appendix headings.
- LaTeX source validation passed for 45 diagrams, bundled fonts, contrast, citations, and cross-format contracts.
- XeLaTeX is expected to retain non-fatal overfull/underfull box warnings in dense tables and long labels; these remain a typography follow-up item for visual inspection.
- Example execution: 26 examples and 123 tests passed with no warnings.
- Representative XeLaTeX pages remain the visual evidence for this environment;
  DOCX pagination QA is pending because LibreOffice/soffice is not installed.
- This slice's changed pages were visually inspected in the XeLaTeX PDF:
  front-matter checkpoint table (page 22), Part I comparative-thread and
  numbered-question flow (page 33), and the adjacent Part I table/glossary
  page (page 34); no clipping, overlap, or missing-glyph defects were found.

## Technical corrections incorporated

- Temporal durable-execution source year corrected to 2025 after primary-page verification.
- Amazon Bedrock Agents source and framework table identify Bedrock Agents Classic maintenance mode, closure to new customers, and AgentCore direction.
- MLflow 3.15.2 is described only as the book's reproducibility baseline; unsupported exact release-date/latest-version assertions were removed.
- Undated living documentation uses `n.d.` plus access date.
- External sources are limited to explicit supported claim scopes and do not validate book-authored architecture recommendations.

## Executable evidence

See the current generated evidence:

- `qa/validation-report.json`
- `qa/determinism/determinism-report.json`
- `reports/citation-verification.json`
- `reports/citation-audit.md`
- `reports/latex-validation.md`
- `reports/editorial-audit.md`
- `CHECKSUMS.sha256`
- `RELEASE-MANIFEST.json`

## Full-book review evidence

- Review contract and chapter-by-chapter matrix: `full-book-review-plan.md`.
- The running example is consistently Harborlight Mortgage; broader supplier, support, and procurement material is retained only as explicitly labeled comparative architecture evidence.
- The primary mortgage contract vocabulary uses `HumanActionAuthorizationRequest` and `HumanActionAuthorizationDecision` consistently across source, examples, diagrams, and generated artifacts.
- Example execution: 26 examples and 123 tests passed with no warnings.
- Representative XeLaTeX pages (cover, TOC, Part divider, chapter body/table, and closing page) were rendered and visually inspected; no clipping, overlap, or missing-glyph defects were observed.
