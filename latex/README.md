# XeLaTeX Publication Project — Book v2.1.0

This directory is the maintainable LaTeX representation of *Enterprise Agentic AI Architecture & Developer Platform Guide* by **Reza Rahimi, PhD**.

## Build

Run commands from the repository root, not from this directory:

```bash
make pdf          # validates the LaTeX source first, then compiles
./latex/compile.sh   # or the compile step on its own
```

The script prefers `latexmk -xelatex` and otherwise runs XeLaTeX three times to resolve the table of contents, bookmarks, references, and page count. The output is copied to:

```text
dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.1.0-LaTeX.pdf
```

### Container build

```bash
docker build -f Dockerfile.latex -t enterprise-agentic-ai-book .
docker create --name book-build enterprise-agentic-ai-book
docker cp book-build:/book/dist/Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.1.0-LaTeX.pdf .
docker rm book-build
```

A GitHub Actions workflow is also provided at `.github/workflows/latex.yml`.

## Project map

- `Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v2.1.0.tex` — publication entry point.
- `bookstyle.sty` — page geometry, embedded fonts, palette, headings, Part/chapter pages, tables, code, callouts, figures, headers, footers, links, and PDF metadata.
- `content/book-content.tex` — generated semantic content. Do **not** hand-edit.
- `fonts/` — bundled Liberation Sans and Liberation Mono files plus license.
- `reference/DOCX-layout-reference-v1.0.0.pdf` — the v1.0.0 cross-format visual baseline, rendered from DOCX. Kept for comparison; v2.1.0 changed the topology, so it no longer matches the current page count. Regenerate with `make qa-pdf` where LibreOffice is available.
- `compile.sh` — deterministic local build entry point.

## Regeneration

The canonical editable source remains `source/parts/*.md`. Rebuild LaTeX after assembling Markdown:

```bash
python3 tools/assemble_manuscript.py --root .
python3 tools/build_latex.py --root .
python3 tools/validate_latex.py --root .
```

The same source generates Markdown and DOCX. Change presentation in `bookstyle.sty`; change semantics in canonical Markdown/configuration.

## Quality contract

- XeLaTeX with bundled Liberation Sans/Mono avoids host-font substitution.
- US Letter geometry matches the DOCX contract.
- Cover is 2550 × 3300 pixels, 300 effective dpi.
- All 18 diagrams are 1800 × 1000 pixels and at least 255 effective dpi at publication width.
- Tables use repeatable long-table headers, dark high-contrast heading rows, alternating light body rows, and responsive font sizing.
- Code uses a line-numbered, wrap-safe, syntax-aware panel with an accessible light background.
- Parts use standalone full-page navy dividers; every chapter and appendix begins on a new page.
- Body, link, table, code, callout, and divider color pairs are tested at 4.5:1 or better; actual tested ratios are in `qa/latex-validation-report.json`.
- Color is never the sole carrier of meaning.

## Required TeX packages

A full TeX Live installation satisfies everything below. On a minimal
distribution, run `./tools/bootstrap_tex.sh` from the repository root: it
installs only what is missing, into your user texmf tree, without `sudo`.

**Direct dependencies** — requested by `bookstyle.sty`: `fontspec`, `microtype`,
`xcolor`, `graphicx`, `longtable`, `array`, `booktabs`, `ragged2e`, `enumitem`,
`fancyhdr`, `titlesec`, `caption`, `hyperref`, `bookmark`, `listings`,
`tcolorbox`, `needspace`, `setspace`, `lastpage`, `pdflscape`, `etoolbox`, and
`amssymb`.

**Transitive dependencies** — pulled in by `tcolorbox[most]` and easy to miss,
because the failure surfaces as a missing file inside a tcolorbox library rather
than as a missing package you asked for: `environ` and `trimspaces` (by
`tcolorbox` itself), `tikzfill` (by the `tcbskins` library), and `pdfcol` (by
the `tcbbreakable` library).

Note that several style files live in bundles under a different name —
`graphicx` is in `graphics`, `longtable` and `array` are in `tools`, `ragged2e`
is in `ms`, and `amssymb` is in `amsfonts`. `tools/bootstrap_tex.sh` holds the
authoritative style-file-to-package mapping.

### macOS (BasicTeX)

```bash
brew install --cask basictex     # then reopen your shell
./tools/bootstrap_tex.sh         # installs the ~7 packages BasicTeX omits
make pdf
```

BasicTeX installs to `/Library/TeX/texbin`; a non-login shell may not have it on
`PATH`. Both `compile.sh` and `bootstrap_tex.sh` add it themselves.

## Build status and the two PDFs

There are two PDFs in this project and they must never be confused:

| File | What it is |
|---|---|
| `latex/reference/DOCX-layout-reference-v1.0.0.pdf` | The **v1.0.0 cross-format visual baseline, rendered from DOCX**. Tracked in git. Never a XeLaTeX build, and must never be renamed as one. v2.1.0 changed the topology, so it is a historical comparison point, not a current gate. |
| `dist/…-LaTeX.pdf` | The genuine **XeLaTeX compilation**. Gitignored and regenerated on demand by `make pdf`, `Dockerfile.latex`, or CI. |

The XeLaTeX edition compiles cleanly with zero errors and zero undefined
references. Page count differs from the 213-page DOCX baseline because the two
engines break lines and pages differently; content and structure are identical
because both are generated from the same canonical Markdown.
