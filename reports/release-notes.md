# Book v2.1.0 Release Notes

Book v2.1.0 is the canonical foundation for *Building Enterprise General Intelligence Platform* by Reza Rahimi, PhD.

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
clean detached worktree at 140,553,588 bytes, SHA-256
`eecdaec618f0a994da0ad42a6b48929caee4cb0da865deac0ad552fff9457497`; the
clean-extraction rebuild passed.

The cumulative mortgage implementation is intentionally limited to executable
C01–C03 evidence. C04–C28 remain the separately tracked implementation roadmap
in `code-gap.md`; this closeout does not claim production readiness for those
unimplemented checkpoints.

This release combines the canonical Markdown source with synchronized DOCX and XeLaTeX representations, editable cover and diagram sources, machine-readable registries, deterministic builders, validators, PDF/visual QA, templates, reusable maintenance skills, a design system, cross-format contract, contribution guidance, release checklist, manifest, and checksums.

The book is organized as eight Parts, 28 chapters, and 12 appendices. It is edited by changing `source/parts/*.md`, configuration, and assets, then regenerating every derivative. Manual editing of the final DOCX, distributable Markdown, or Notion copy is prohibited because it creates drift.

The editorial review through page 30 has been generalized across the full book, including terminology, control-point architecture, navigation, front matter, and governed learning. The first implementation slice now makes the Harborlight mortgage case and implemented `C01`–`C03` checkpoints explicit in the front matter and Part I, while retaining Northstar supplier material as comparative architecture evidence. Full validation results for this working tree are recorded in the generated reports after the rebuild; living external sources must be re-verified in future releases.
