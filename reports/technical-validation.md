# Technical Validation Record — Book v2.1.0

**Result:** PASS; DOCX pagination QA BLOCKED
**Validated:** 2026-09-16

## Final measurements

- 8 Parts; 28 chapters; 12 appendices.
- 45 registered architecture diagrams; 54 DOCX inline images including cover.
- 71 fenced code blocks; 423 DOCX tables.
- 48 registered references; 107 citation occurrences; no unknown or uncited IDs.
- Canonical and distributable Markdown are byte-identical; canonical SHA-256 is
  `a6eeecae6532350b7493f5eb1071fedfa551c6770276ef304165bf5ffa48f4e8`
  (678,999 bytes).
- DOCX package opens successfully and contains required named styles and metadata.
- DOCX builds twice to the same SHA-256 hash
  `3d3b55ce27baeb83e403130b6938c1538ff886d77c17396d4a7ab82e40c54745`
  (24,409,801 bytes).
- Genuine XeLaTeX compile: 287 pages.
- 40 chapter/appendix headings are structurally represented in the current source and generated artifacts; the DOCX validator found 28 chapter and 12 appendix headings.
- LaTeX source validation passed for 45 diagrams, bundled fonts, contrast, citations, and cross-format contracts.
- XeLaTeX is expected to retain non-fatal overfull/underfull box warnings in dense tables and long labels; these remain a typography follow-up item for visual inspection.
- Example execution: 26 examples and 123 tests passed with no warnings.
- Mortgage platform-extension execution: 11 offline contract tests passed;
  these tests cover the partial `mortgage_case/platform/` slice and are not
  counted in the registered-example total above.
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
- `reports/release-package.json` — final 388-entry release ZIP, with its byte
  count and SHA-256 recorded by the package tool.
- `CHECKSUMS.sha256`
- `RELEASE-MANIFEST.json`

The final ZIP was generated from a clean detached worktree so unrelated local
untracked files were excluded. `tools/clean_package_test.py` extracted that ZIP
and passed assembly, DOCX/LaTeX rebuild, reference checks, structural
validation, LaTeX validation, and deterministic-build checks.

## Full-book review evidence

- Review contract and chapter-by-chapter matrix: `full-book-review-plan.md`.
- The running example is consistently Harborlight Mortgage; broader supplier, support, and procurement material is retained only as explicitly labeled comparative architecture evidence.
- The primary mortgage contract vocabulary uses `HumanActionAuthorizationRequest` and `HumanActionAuthorizationDecision` consistently across source, examples, diagrams, and generated artifacts.
- Example execution: 26 examples and 123 tests passed with no warnings.
- Representative XeLaTeX pages (cover, TOC, Part divider, chapter body/table, and closing page) were rendered and visually inspected; no clipping, overlap, or missing-glyph defects were observed.
