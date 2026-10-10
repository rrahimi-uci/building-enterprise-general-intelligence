# Book v1.0.0 Release Notes

Book v1.0.0 is the canonical foundation for *Building an Enterprise General Intelligence Platform* by Reza Rahimi, PhD.

## Chapter 1 review-comment reconciliation — 2026-09-18

Sixteen reviewer comments left on the distributed v1.0.0 DOCX were reconciled
into the canonical Markdown. The front matter's "architecture in one view"
paragraph and four of its six engineering-contract principles were rewritten
per the review, and a redundant "small engineering contract" paragraph was
removed. Chapter 1's Monday-through-Friday failure narrative now names each
day's failure theme (Durability, Trust boundaries, Transactional effects,
Evidence and auditability, Release control), and "The gap between a useful
demo and a dependable system" plus the renamed "Draw the boundary around the
model" section carry the reviewer's expanded narrative. A redundant
Before/After checkpoint table and code callout were removed from the chapter
opening, and its code listing's stated line count was corrected from fifteen
to ten lines to match the actual example. Two other unqualified "reproducible"
claims elsewhere in the book were aligned with the front matter's revised
reconstructable-and-explainable framing for nondeterministic model behavior.
The 8-Part / 28-chapter / 12-appendix topology, citations, examples, diagrams,
and stable identifiers remain intact.

Local evidence: `make validate`, `make examples-run` (123 example tests and 30
mortgage-case tests), `make deterministic`, and genuine `make pdf` pass; the
XeLaTeX output is 286 Letter-size pages. `make package` produced the
417-entry release ZIP. `make qa-pdf` remains unavailable because LibreOffice /
`soffice` is not installed, so DOCX pagination QA is not claimed as passed.

## Reviewed DOCX reconciliation — 2026-09-17

The reviewed v1.0.0 DOCX was reconciled into the canonical Markdown parts and
regenerated into the distributable Markdown, DOCX, and XeLaTeX source. The
reviewed reader-facing headings, evidence callouts, chapter and appendix
transitions, pattern catalog, and threat catalog now agree across formats. The
latest review pass also reconciles the title metadata and cover wording,
reviewed body typography and pagination behavior, and the two reviewed
spellings in the canonical prose. The
8-Part / 28-chapter / 12-appendix topology, citations, examples, diagrams, and
stable identifiers remain intact.

Local evidence: `make validate`, `make examples-run` (123 example tests and 30
mortgage-case tests), `make deterministic`, and genuine `make pdf` pass; the
XeLaTeX output is 286 Letter-size pages and representative pages were
inspected. `make package` produced the 414-entry release ZIP, and checksum,
rebuild, and validation checks passed from a clean extraction. `make qa-pdf`
remains unavailable because LibreOffice / `soffice` is not installed, so DOCX
pagination QA is not claimed as passed.

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
