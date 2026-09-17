# Book v2.1.0 Release Notes

Book v2.1.0 is the canonical foundation for *Building Enterprise General Intelligence Platform* by Reza Rahimi, PhD.

## Full-book style and readability pass — 2026-09-16

This publication-wide editorial pass rewrites the reader-facing layer of the
book without weakening its contracts. It gives the front matter, Part
orientations, all 28 chapter titles, and the appendices a clearer practitioner
voice; replaces repeated specification-like headings with meaningful signposts;
and adds concise explanations of why each boundary matters, when it becomes
important, and what can fail without it. The technical architecture,
identifiers, citations, diagrams, examples, and 8-Part / 28-chapter /
12-appendix topology remain intact.

The canonical source and derived Markdown, DOCX, and XeLaTeX source were
rebuilt. `make validate`, the 123-example test suite plus 30 mortgage-case
tests, and deterministic DOCX comparison pass. Genuine XeLaTeX compilation
passes at 288 Letter-size pages, with representative pages visually
inspected. DOCX pagination QA remains deferred because LibreOffice / `soffice`
is not installed; the XeLaTeX result is not treated as a substitute for that
gate.

## Full-book review closeout — 2026-09-16

The remaining review-plan items are complete in one coherent source and
publication closeout. The final pass reconciled the Harborlight mortgage
narrative, human action authorization vocabulary, example-to-chapter metadata,
diagram source/render/checksum state, Appendix I title, and Northstar/Harborlight
distinction. Canonical Markdown, distributable Markdown, DOCX, LaTeX source,
diagrams, and QA reports were regenerated.

Local evidence: `make validate`, `make examples-run` (123 tests / 26 examples),
`make deterministic`, `make diagrams`, and genuine `make pdf` (287 Letter-size
pages) pass. `make qa-pdf` remains explicitly deferred because LibreOffice /
`soffice` is unavailable. The final 388-entry release ZIP was generated from a
clean detached worktree; its byte count and SHA-256 are recorded in
`reports/release-package.json`, and the clean-extraction rebuild passed.

The cumulative mortgage implementation has stage-registered executable
evidence for C01–C03. This PR also includes a tested offline platform-contract
slice under `mortgage_case/platform/` spanning the later architecture, but C04–
C28 remain the separately tracked checkpoint-integration roadmap in
`code-gap.md`; this closeout does not claim production readiness for those
incomplete checkpoints.

This release combines the canonical Markdown source with synchronized DOCX and XeLaTeX representations, editable cover and diagram sources, machine-readable registries, deterministic builders, validators, PDF/visual QA, templates, reusable maintenance skills, a design system, cross-format contract, contribution guidance, release checklist, manifest, and checksums.

The book is organized as eight Parts, 28 chapters, and 12 appendices. It is edited by changing `source/parts/*.md`, configuration, and assets, then regenerating every derivative. Manual editing of the final DOCX, distributable Markdown, or Notion copy is prohibited because it creates drift.

The editorial review through page 30 has been generalized across the full book, including terminology, control-point architecture, navigation, front matter, and governed learning. The first implementation slice now makes the Harborlight mortgage case and implemented `C01`–`C03` checkpoints explicit in the front matter and Part I, while retaining Northstar supplier material as comparative architecture evidence. Full validation results for this working tree are recorded in the generated reports after the rebuild; living external sources must be re-verified in future releases.
