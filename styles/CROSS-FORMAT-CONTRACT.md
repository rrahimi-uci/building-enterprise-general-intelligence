# Cross-Format Synchronization Contract

Book v1.0.0 exists as synchronized Markdown, DOCX, and Notion representations. They share content and structure but may use representation-specific affordances.

## Authority order

1. `source/parts/*.md` — editable prose source.
2. `config/*.json` and `assets/*` — metadata, evidence, visual sources.
3. `book/manuscript.md` — generated canonical assembly.
4. `dist/*.md` — byte-identical release Markdown.
5. `dist/*.docx` — deterministic publication rendering.
6. Notion — approved publishing/synchronization target.

When representations disagree, fix the canonical source/configuration and regenerate. Do not repair only the derivative.

## Semantic mapping

| Concept | Canonical Markdown | DOCX | Notion |
|---|---|---|---|
| Part | H1 `Part …` | standalone Book Part page | H1 or child page with orientation |
| Chapter/appendix | H1 | Heading 1, new page | H1/child page, same title/order |
| Section | H2–H4 | Heading 2–4 | H2–H4 |
| Paragraph/list | CommonMark/GFM | Normal/List styles | native paragraph/list blocks |
| Table | GFM table | styled Word table | native simple table where feasible |
| Code | fenced block + language | styled line-numbered panel | code block + language |
| Callout | labeled block/table | named callout style | callout block or labeled paragraph |
| Diagram | registered marker | embedded image + Caption | image + caption/file reference |
| Citation | `[Rxx]` | linked/styled marker | literal stable marker |
| Reference | generated Appendix K | rendered bibliography | same text/order |

## Equivalence rules

- Title, author, version, release date, Part/chapter/appendix titles and order, prose, tables, captions, code, citation IDs, and reference entries must match semantically.
- Generated Markdown must match `book/manuscript.md` byte for byte.
- DOCX may contain page breaks, headers, footers, style metadata, fields, and syntax color not represented in Markdown.
- Notion may split the book into navigation pages and attach artifacts; it must not silently alter approved prose or evidence scope.
- Renderer-specific line wrapping and page counts may differ across Word/LibreOffice, but page-start and standalone-divider invariants must remain.

## Synchronization procedure

1. Edit source/config/assets.
2. Assemble Markdown and review diffs.
3. Build DOCX.
4. Validate structural counts, citations, asset registry, styles, metadata, and hashes.
5. Render PDF and visually approve release candidates.
6. Package and validate from a clean extraction.
7. Upload the exact package artifacts to Notion and update release metadata.
8. Reload Notion pages and verify title, author, version, attachments, counts, child-page preservation, and audience.

## Drift detection

A release fails if:

- canonical and distributable Markdown hashes differ;
- a reference ID is missing, duplicated, or outside its permitted scope;
- an asset marker is unresolved;
- DOCX heading/image counts differ from the canonical structure;
- stale version labels remain;
- Notion names a different version or links different artifact hashes;
- a generated file contains a manual edit not represented in source/configuration.

`tools/validate_book.py`, `tools/check_references.py`, `tools/deterministic_build_check.py`, and `tools/package_release.py` implement the local gates. Notion synchronization remains an explicit approved publishing action.

## Round-trip policy

There is no automatic DOCX-to-Markdown or Notion-to-Markdown round trip. Such conversion loses semantics and makes formatting non-deterministic. If an approved edit originates in Word or Notion, manually reconcile it into `source/parts`, regenerate all derivatives, and replace the derivatives. Record the origin and reconciliation in the changelog or review notes.
