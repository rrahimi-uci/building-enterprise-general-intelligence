# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

### Front matter and Part I (continuity review, WP-FM and WP-I)

- Front matter: reader paths now include their prerequisites; "How the book is organized" matches Figure 0-1, whose labels are now the exact Part titles; the engineering contract is condensed and points to Chapter 2's principles; maintainer content and the supplier-onboarding promise are gone; the Closing Perspective is listed.
- Chapter 1 opens with the demo, states the thesis once, explains the state-owner table that later chapters reuse, shows checkpoint C01, maps the three per-step questions and the ten problems to the chapters that answer them, and fixes vocabulary pointers. "Agent Gateway" becomes the A2A Gateway (Figure 1-4); Figure 1-3 shows Channels as Parts II and IV.
- Chapter 1's prototype and level sketches are now a tested example (`prototype-levels`), whose test reproduces the Wednesday duplicate write.
- Chapter 2 names the six gates as the deterministic shell, gives each gate an owner, places human approval inside Authorize, defines acceptance criteria and the acceptance engine, and uses `proposed_action` and the second pay statement in its proposal.
- Chapter 3 is about a quarter shorter: previews of approval, handoff, guardrails, retries, and the write path collapse into one section that points to the owning chapters; AgentRuntime is defined before the checkpoint; the step status enum and the step-to-gate bridge are stated; the restart and replaceability tests are paired; `contracts#step` moves here from Chapter 1.
- Northstar and the supplier-onboarding thread are retired from Part I; approval terminology follows Chapter 14.

### Part VII — evidence, evaluation, and improvement (continuity review, WP-VII)

- Chapter 24 is the home of observability: one decision-centric span schema (decision, memory, and security-control spans; `effect.state` on tool spans), the single metric scorecard, and the telemetry implementation (collector, trace index, content vault, audit ledger writer) moved in from Chapter 25.
- Chapter 24 states the four authoritative records (trace, workflow history, effect ledger, audit ledger), names the causal run trace and trajectory, separates workflow replay, diagnostic replay, and fork, and absorbs Chapter 7's first-divergence steps into a five-step § Debugging method that the worked example now follows.
- Chapter 25 is reordered: release gate, test layers, worked example, runtime/offline boundary (now with a test, placements, and a Harborlight example), the learning loop with defined records and an automate/govern/never table, then evaluation-only implementation.
- Chapter 25 defines EvaluationResult, ValidationReport, and ReleaseGateDecision; one test-layer table replaces the pyramid list; the waiver path and the Chapter 13 versus release-gate distinction are explained.
- MLflow claims are limited to what R20/R21 support; the Agents SDK tracer default is now a tested statement about the pinned package.
- The trajectory example adds a deterministic `forbidden_tool_absent` scorer, and its judge no longer assesses authorization.
- Figures 25-2 and 25-3: runtime lane matches the prose; Approve reads "owner or pre-approved class".

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
