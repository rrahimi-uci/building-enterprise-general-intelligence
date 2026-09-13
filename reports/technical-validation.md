# Technical Validation Record — Book v1.0.0

**Result:** PASS  
**Validated:** 2026-09-13

## Final measurements

- 12 Parts; 31 chapters; 15 appendices.
- 18 registered architecture diagrams; 19 DOCX inline images including cover.
- 43 fenced code blocks; 316 DOCX tables.
- 43 registered references; 94 citation occurrences; no unknown or uncited IDs.
- Canonical and distributable Markdown are byte-identical.
- DOCX package opens successfully and contains required named styles and metadata.
- DOCX builds twice to the same SHA-256 hash.
- LibreOffice reference render: 213 Letter-size pages.
- 46 chapter/appendix headings found on 46 unique start pages.
- 13 standalone divider pages (12 Parts plus appendices).
- No unintended blank PDF pages.

## Technical corrections incorporated

- Temporal durable-execution source year corrected to 2025 after primary-page verification.
- Amazon Bedrock Agents source and framework table identify Bedrock Agents Classic maintenance mode, closure to new customers, and AgentCore direction.
- MLflow 3.15.2 is described only as the book's reproducibility baseline; unsupported exact release-date/latest-version assertions were removed.
- Undated living documentation uses `n.d.` plus access date.
- External sources are limited to explicit supported claim scopes and do not validate book-authored architecture recommendations.

## Executable evidence

See:

- `qa/validation-report.json`
- `qa/pagination-report.json`
- `qa/determinism/determinism-report.json`
- `reports/citation-verification.json`
- `reports/citation-audit.md`
- `qa/render/visual-contact-sheet.png`
- `CHECKSUMS.sha256`
- `RELEASE-MANIFEST.json`
