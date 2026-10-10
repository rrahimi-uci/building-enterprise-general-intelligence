# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

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

### Part III — developer platform (continuity review, WP-III)

- The Part III orientation names the three owners and frames Chapter 7 as a forward map. The capability table gains a "Taught in" column, merges workflow and durable execution, and moves "action policy" out of Guardrails.
- Chapter 7 adds a third owner (domain-capability owners of Skills and Skill Packs). It points to Chapter 3 for the runtime seam, Chapter 25 for test levels, and Chapter 24 for debugging, and § If this fails becomes platform-failure triage. Figures `developer-lifecycle` and `test-pyramid` are retired; the golden-path figure shows the table's eight stages.
- Chapter 7's inline SDK and CLI listings become prose using the case identifiers. A new `adapter-conformance` example makes the portability evidence executable.
- Chapter 8 removes lifecycle and `side_effect_class` from the manifest and uses `risk_ceiling: R1`. It defines what a Skill version promises, separates Skill, tool, agent, and pack, explains how a resolved Skill reaches the step without authorizing its calls, and reconciles the four binding moments. Discovery is "broad", not "permissive".
- Chapter 9 explains the CompatibilityReport checks, pack lifecycle versus aliases, ownership, and the ReleaseManifest-to-RunManifest link. Its broken inline excerpt is replaced by the new `skills-registry#packs` region (`SkillPackRegistry`).
- The Northstar box becomes a mortgage-case box; deployment terms follow "global control tier" and "regional execution cell".

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
