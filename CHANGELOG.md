# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

### Part IV — patterns that work and those that fail (continuity review)

<!-- part4a bullets -->
- Chapter 14 names three human controls (approval, intervention, operator control) and adds an intervention contract. Every Part IV escalation now lands as a typed InterventionTask. The approval field list appears once, uses the `ApprovalRequest` / `ApprovalDecision` names, and the divergent inline code is gone.
- Chapter 15 is reordered so the lifecycle comes before its terminal states. It adds the book's run-state table, fills the empty event-driven resume section, links each lifecycle step to its Part IV pattern, and points to Chapters 4, 22, and 27 instead of repeating them. The recovery-objective claim, which exceeded its sources, is replaced.
- Chapter 16 is now a slim Part IV synthesis: a revised decision tree (Figure 16-1) with chapter-labelled leaves, a comparison table of the Chapter 10–15 patterns, and one Harborlight run that composes them. The twelve platform pattern cards move to Appendix A.
- Appendix A holds the twelve P-cards, each tagged with the chapter that builds it, with corrected pairings and rows for the Part IV patterns. P-09 is now "Causal run trace", and P-03 and P-04 follow Chapter 6's authorization order and memory taxonomy.
- Chapter 17 tags each card "Prevented in / Built in" (seven prevented, seven previewed, two built later), moves the prioritization into "How to read a card", and moves its six anti-pattern/correction listings into tested examples (`examples/antipatterns/`). The AP-05 correction no longer retries after a null lookup, and the AP-06 correction keys the commit by the logical effect.
- Terminology across Chapters 14–17: approval rather than "human action authorization", the second pay statement as the missing document, capability envelope plus credential lease (Figure 17-2), and no Northstar or supplier-onboarding examples.

### Shared contracts and examples (continuity review, Phase 1)

- `AgentDecision.disposition` gains `proposed_action`: `invoke_tool` is a read, and a mutation leaves the loop as a proposal.
- `ReActEngine.run` returns an `AgentStepResult`; a tripped bound is `status: failed` with `error_code` `budget_exhausted` or `no_progress`, not an exception.
- One `RiskClass` enum (R0–R4) replaces integer risk in `PlanNode`, `SkillRequirement`, `SkillManifest`, and `PlanEnvelope`; the Skill field is now `risk_ceiling`.
- The Skill registry keeps lifecycle state (the six states of Chapter 8) in registry-side release records, so promotion never moves a manifest digest.
- The effect-idempotency example implements Unknown: a timeout is never re-applied until reconciliation; only a received decline releases the key.
- Approval records are `ApprovalRequest` / `ApprovalDecision`, issued by `ApprovalService`, in the examples and `mortgage_case/`.
- Examples and tests use the second pay statement (`pay_statement`) as the missing document.

### Cover artwork and version labels

- Removed printed release numbers from the book cover and all 28 chapter covers; regenerated the cover artwork and synchronized publication artifacts. The release identifier remains `v1.0.0` in metadata, filenames, title page, and running footers.
- Corrected the active continuity review map to identify the current book as v1.0.0.

### Repository maintenance

- Removed the closed full-book review plan and unreferenced `proposals/` draft, retaining their history in git.
- Added a whole-book continuity and flow review under `reviews/continuity-and-flow/`.

## [1.0.0] — 2026-09-13

First public release of *Building an Enterprise General Intelligence Platform* by Reza Rahimi, PhD. Earlier working drafts carried the labels v2.x and v3.x; those are retired, and 1.0.0 is the only release version. The draft changelog is in git history.

### The book

- 8 Parts, 28 chapters, and 12 appendices, each Part and chapter opening on a new page; every chapter is preceded by its full-page Letter cover (`cover-images/`) in the DOCX and XeLaTeX editions.
- One running example, the Harborlight mortgage case, carried through the chapters, with a cumulative implementation under `mortgage_case/` and the roadmap in `code-gap.md`.
- Canonical prose in `source/parts/*.md`; the DOCX, XeLaTeX, and distributable Markdown editions are generated from it, with a cross-format contract in `styles/`.
- Every citation resolves to `config/references.json` with a recorded scope; Appendix K is generated from it, with the claim-scope traceability matrix.
- Every diagram is rendered from an editable source in `assets/diagrams/src/` (vector PDF for XeLaTeX, PNG for DOCX) and registered in `config/diagrams.json`.
- Every code listing is a tested file under `examples/`, registered in `config/examples.json` and executed in CI.

### Versioning

- Book version is `1.0.0` in `config/book.json`, the title page, running footer, and the artifact names `Enterprise-General-Intelligence-v1.0.0.{md,docx,tex,pdf}`.
- The stale-label validator now rejects any `v2.x` or `v3.x` label in the manuscript.
- The pre-release DOCX layout baseline is renamed `latex/reference/DOCX-layout-reference-draft.pdf` so its name no longer implies it matches v1.0.0.
