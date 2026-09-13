# Enterprise Agentic AI Architecture & Developer Platform Guide

**Book v1.0.0 development system**  
Author: **Reza Rahimi, PhD**  
Release date: 2026-09-13

This package is both the publication release and the reproducible source system for future editions. A new maintainer should be able to edit, validate, rebuild, and package the book using only this repository.

## Canonical-source contract

1. **Edit:** `source/parts/*.md` in numeric order.
2. **Reference metadata:** edit `config/references.json`; cite sources as `[Rxx]` in prose.
3. **Assets:** add diagrams to `assets/diagrams/` and register them in `config/diagrams.json`.
4. **Assemble:** `tools/assemble_manuscript.py` generates `book/manuscript.md` and the distributable Markdown file.
5. **Render:** `tools/build_book.py` generates DOCX from the assembled manuscript and configuration.
6. **Validate before release:** never hand-edit generated DOCX or distributable Markdown.

`source/original/` is immutable provenance. `tools/prepare_manuscript.py` is the one-time v3.1-to-v1.0.0 migration/bootstrap tool; do not use it during ordinary future editing because it regenerates `source/parts` from the legacy source.

## Quick start

Requirements: Python 3.13, `python-docx 1.2.0`, Pillow 12.3.0, PyMuPDF 1.28.2, pdfplumber 0.11.10, Microsoft core fonts or metric-compatible substitutes. LibreOffice is optional but required for PDF/pagination QA.

```bash
python3 -m pip install -r requirements.txt
make build
make validate
make qa-pdf      # optional; requires LibreOffice
make package
```

The release ZIP is written next to the repository root by default. All commands accept paths derived from their script location and do not depend on `/data`.

## Repository map

```text
Book-v1.0.0/
├── AGENTS.md                     # mandatory workflow for AI maintainers
├── README.md                     # this guide
├── CHANGELOG.md
├── CONTRIBUTING.md
├── RELEASE-CHECKLIST.md
├── Makefile
├── requirements.txt
├── book/
│   └── manuscript.md             # generated canonical assembly; do not hand-edit
├── source/
│   ├── parts/                    # canonical editable Markdown sources
│   └── original/                 # immutable v3.1 DOCX/Markdown/cover provenance
├── dist/                         # final v1.0.0 DOCX and Markdown
├── assets/
│   ├── cover/                    # source artwork and generated cover
│   └── diagrams/                 # publication diagrams
├── config/
│   ├── book.json                 # metadata, layout, typography, colors
│   ├── diagrams.json             # diagram registry
│   ├── references.json           # source-of-truth citation registry
│   └── style-tokens.json         # portable design tokens
├── styles/                       # design system and synchronization rules
├── templates/                    # chapter, pattern, threat, reference, diagram templates
├── skills/                       # reusable AI-agent maintenance procedures
├── tools/                        # deterministic build, validation, QA, packaging utilities
├── qa/                           # machine-readable and visual QA evidence
├── reports/                      # assembly/editorial/citation/release reports
└── provenance/legacy-tools/      # preserved historical generators
```

## Safe edit workflow

1. Read `AGENTS.md`, `styles/DESIGN-SYSTEM.md`, and `styles/CROSS-FORMAT-CONTRACT.md`.
2. Create a working branch or copy of the repository.
3. Edit one or more canonical files under `source/parts/`.
4. If adding a cited claim, update `config/references.json`, allocate the next stable `Rxx`, and add `[Rxx]` at the sentence or paragraph that needs support.
5. If adding a diagram, add its source/export to `assets/diagrams/`, update `config/diagrams.json`, and place `[[DIAGRAM:id|caption]]` on its own line.
6. Run `make assemble`, review the Markdown diff, then run `make build`.
7. Run `make validate`. Resolve all errors; do not suppress a check without recording the rationale.
8. Run `make qa-pdf` for release candidates. Inspect the contact sheet and chapter-start report.
9. Update `CHANGELOG.md`, version metadata, and release notes.
10. Run `make package`, extract the ZIP into a clean folder, and run `make validate` there.
11. Only after the clean-package test passes, synchronize the approved manuscript and attachments to Notion.

## Editing topology

- `00-front-matter.md`: title marker, publication preface, reader map, table of contents.
- `01-part-i.md` … `12-part-xii.md`: one Part divider plus its chapters.
- `13-appendices.md`: appendix divider and Appendices A–O.
- Every Part, chapter, and appendix begins with an H1. DOCX rendering inserts a new page before each and makes Part/appendix dividers standalone.
- H2 is a major section, H3 a subsection, and H4 a local subtopic. Do not skip levels.
- Keep transitions at chapter endings so prerequisites and next steps remain explicit.

## References and claim discipline

`config/references.json` defines each source, version/date, URL, permitted support scope, verification date, and source class. Appendix K and Appendix M are generated from this registry during assembly. Cite only what the recorded scope supports. Book-authored patterns, estimates, examples, architectures, and formulas must be identified as guidance unless a reference explicitly validates them. Living documentation uses `n.d.` plus an access date. Maturity-sensitive claims must state pins and re-verification requirements rather than claiming a framework is “latest.”

Run:

```bash
python3 tools/check_references.py --root .
```

Online link checking is intentionally optional because reproducible offline builds must not depend on network access.

## Build outputs

- `dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0.md`
- `dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0.docx`
- `assets/cover/cover-v1.0.0.png`
- `templates/book-style-template.docx`
- `qa/render/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0.pdf` (QA only)
- `qa/render/visual-contact-sheet.png` (QA only)

## Determinism

The assembler normalizes line endings. The DOCX builder fixes metadata, package timestamps, ZIP member order, styles, page geometry, and media insertion order. The packager fixes ZIP entry timestamps and ordering. A deterministic build check compiles DOCX twice in isolated output directories and compares SHA-256 hashes.

Expected differences are allowed only after canonical source, configuration, assets, dependencies, or build tools change. Record those changes in the changelog and release manifest.

## Notion synchronization

Notion is a published representation, not the build source. Publish only after local validation. The Notion release page must identify Book v1.0.0, author, release date, structure counts, citation count, checksums, QA status, and attach the exact ZIP/DOCX/Markdown/cover produced by this package. Preserve child-page blocks and permissions. If private source material would be copied to a broader destination, obtain confirmation first.

## Troubleshooting

- **DOCX differs after rebuild:** verify exact dependency versions, fonts, assets, and that no one edited generated files.
- **Citation missing/unknown:** run `check_references.py`; add the registry entry or remove the unsupported marker.
- **Diagram missing:** confirm the marker ID exists in `config/diagrams.json` and the registered file exists.
- **Unexpected pagination:** compare fonts and LibreOffice/Word versions; content and DOCX structure remain canonical even when renderer pagination differs slightly.
- **Assembler overwrote an edit:** edits belong in `source/parts`, not `book/manuscript.md` or `dist/`.
- **Need to alter layout:** change `config/book.json` and `build_book.py`, update the design system, rebuild, and visually re-approve representative pages.

## Release integrity

See `RELEASE-MANIFEST.json`, `CHECKSUMS.sha256`, `qa/validation-report.json`, `reports/citation-audit.md`, and `CHANGELOG.md`. Treat the package as invalid if required checks fail or if release artifacts do not match the manifest.
