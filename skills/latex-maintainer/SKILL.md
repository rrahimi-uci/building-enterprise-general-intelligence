# Skill: LaTeX Publication Maintainer

## Use when

Changing the XeLaTeX converter, publication style, font assets, table/code/figure behavior, compile workflow, or LaTeX quality gates.

## Required reading

1. `AGENTS.md`
2. `styles/DESIGN-SYSTEM.md`
3. `styles/CROSS-FORMAT-CONTRACT.md`
4. `styles/LATEX-STYLES.md`
5. `latex/README.md`
6. `tools/build_latex.py` and `tools/validate_latex.py`

## Procedure

1. Confirm whether the request changes semantics or presentation. Semantic edits belong in `source/parts`; presentation edits belong in `bookstyle.sty` or the converter.
2. Assemble canonical Markdown and run the ordinary Markdown/DOCX validators first.
3. Run `python3 tools/build_latex.py --root .`.
4. Run `python3 tools/validate_latex.py --root .`; resolve every error.
5. Compile with `./latex/compile.sh` or `Dockerfile.latex`. Never call the reference PDF a LaTeX build.
6. Inspect the compiled PDF: cover, title, linked TOC, all standalone dividers, all chapter/appendix starts, dense tables, long tables across pages, code wrapping, callouts, diagrams, references, headers/footers, and blank/orphan pages.
7. Compare structural counts and representative text with Markdown and DOCX.
8. Update style documentation, changelog, release reports, manifest, and checksums.
9. Package and validate from a clean extraction before publishing.

## Guardrails

- Do not hand-edit `latex/content/book-content.tex`.
- Do not depend on host fonts, network resources, shell escape, or nonredistributable assets.
- Do not reduce table/code text below the design-system minimum to hide layout defects.
- Do not remove visible semantic labels when changing color.
- Do not claim a genuine LaTeX PDF exists unless XeLaTeX completed successfully.
- Do not modify canonical prose only in `.tex`.

## Output

A reproducible XeLaTeX project, passing static validation, a genuine compiled PDF when an engine is available, updated QA evidence, and synchronized package documentation.
