# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

### Shared contracts and examples (continuity review, Phase 1)

- `AgentDecision.disposition` gains `proposed_action`: `invoke_tool` is a read, and a mutation leaves the loop as a proposal.
- `ReActEngine.run` returns an `AgentStepResult`; a tripped bound is `status: failed` with `error_code` `budget_exhausted` or `no_progress`, not an exception.
- One `RiskClass` enum (R0–R4) replaces integer risk in `PlanNode`, `SkillRequirement`, `SkillManifest`, and `PlanEnvelope`; the Skill field is now `risk_ceiling`.
- The Skill registry keeps lifecycle state (the six states of Chapter 8) in registry-side release records, so promotion never moves a manifest digest.
- The effect-idempotency example implements Unknown: a timeout is never re-applied until reconciliation; only a received decline releases the key.
- Approval records are `ApprovalRequest` / `ApprovalDecision`, issued by `ApprovalService`, in the examples and `mortgage_case/`.
- Examples and tests use the second pay statement (`pay_statement`) as the missing document.

### Part VI — Security, Identity, and Control (continuity review, WP-VI)

- The Part VI orientation states the "assume manipulation" premise once and maps Chapters 20–23, replacing a control order the chapters contradicted.
- Chapter 20 keeps "guardrail" in its detector sense only, has one nine-layer model (Figure 20-1 redrawn to match), and gives every threat card a first deterministic refusal layer. Figure 20-3 now shows the detector feeding the policy engine. It gains opening boxes and an incident section cited to NIST SP 800-61 [R42].
- Chapter 21 is reordered: subject, actor, and purpose; then the decision; then how authority travels, with capability envelope (scope) and credential lease (proof) defined. The subset proof is the new `capability-envelope` example.
- Chapter 22 is one argument with one implementation block. It defines Unknown canonically, relates risk classes to use-case tiers, and drops the inline ledger in favor of the `effect-idempotency` example. Figure 22-1 reserves the effect before approval.
- Chapter 23 continues the Chapter 20 example rather than retelling it. It drops its duplicate layer list, threat table, and credentials API, and adds kill-switch and data-lineage/privacy sections. Its code is now the `egress-url` and `kill-switch` examples, without the unrelated RTO/RPO class. The governance record moves to Chapter 26.
- Approval terminology replaces "human action authorization" throughout the Part. Chapter 21 and 23 cover labels follow the revised text.

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
