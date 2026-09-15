# Technical Validation Record — Book v2.1.0

**Result:** PASS  
**Validated:** 2026-09-13

## Final measurements

- 8 Parts; 28 chapters; 12 appendices.
- 43 registered architecture diagrams; 52 DOCX inline images including cover.
- 68 fenced code blocks; 409 DOCX tables.
- 48 registered references; 104 citation occurrences; no unknown or uncited IDs.
- Canonical and distributable Markdown are byte-identical.
- DOCX package opens successfully and contains required named styles and metadata.
- DOCX builds twice to the same SHA-256 hash.
- Genuine XeLaTeX compile: 277 pages.
- 40 chapter/appendix headings are structurally represented in the current source and generated artifacts; the DOCX validator found 28 chapter and 12 appendix headings.
- LaTeX source validation passed for 43 diagrams, bundled fonts, contrast, citations, and cross-format contracts.
- Pagination QA is pending because LibreOffice/soffice is not installed in this environment.

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
