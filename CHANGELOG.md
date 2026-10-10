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

### Part VIII and the Closing Perspective (continuity review, WP-VIII)

- Chapter 26 now holds governance's own mechanism: use-case tiers T0–T4 related to effect risk classes R0–R4 and change classes, a release review-depth rule, control-hierarchy and cadence tables, an expiring-exception lifecycle, and the governance inventory, exception API, GovernanceRecord, and ExceptionWaiver moved from Chapters 23 and 27.
- Chapter 27 defines one release chain (ChangeBundle → ReleaseManifest → EnvironmentBinding → RunManifest), teaches release contents once, adds a seven-step regional recovery sequence, uses "global control tier" and "regional execution cell", and moves the baseline technology stack to Appendix D.
- Chapter 28 is reordered to measure → optimize → admit → degrade, separates permit-holding work from waiting runs in its Little's Law example, receives Chapter 19's policy-first model routing, and merges its duplicated concurrency lists.
- Inline Python in Chapters 27 and 28 is replaced by tested examples: `release-compatibility` (typed `WorkerProfile`), `release-attestation` (binds verified identities to the artifact), and `admission-permit` (grant, defer, or reject).
- Northstar boxes become mortgage-case boxes; numeric "guardrails" become "starting limits"; Figures 26-1, 27-1, and 28-1 and the Chapter 26 cover are corrected.
- The Closing Perspective now follows Chapter 28, replays Chapter 1's Monday–Friday failures against the controls that contain them, and states that only checkpoints C01–C03 are implemented.

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
