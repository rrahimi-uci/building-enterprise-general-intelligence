# Changelog

All notable changes follow semantic versioning and are recorded here.

## [Unreleased]

### Part V (Chapters 18–19, continuity review)

- Chapter 18 defines the task lifecycle and owns the one TaskEnvelope: its eight field groups move in from Chapter 19, and the code becomes the tested `contracts#task` region (idempotent creation, depth and budget withdrawal, envelope-subset hook).
- Handoff follows Chapter 11: `:handoff` proposes a pending OwnershipTransfer that only `:accept` commits. Plan revision belongs to Chapter 12 (`plans:revise` removed).
- The duplicate capability-envelope proof leaves Chapter 18 (Chapter 21 owns it); the two pattern cards merge into "Supervisor/Worker at a glance"; Figure 18-1 uses the mortgage specialists.
- Chapter 19 becomes the federated delta: the LLM Gateway material leaves (enforcement to Chapter 4, routing and metrics to Chapter 28), Figure 19-1 and `gateway-position` are retired, and A2ATaskEnvelope is deleted.
- MCP mutations continue to the Tool Gateway; the A2A Gateway is related to Chapter 1's gateway table and to the Task Service; remote states map onto the pinned A2A 1.0.1 task-state names.
- The artifact-adoption check moves from Chapter 6 into Chapter 19 as the tested `artifact-adoption` example, now with a content-hash check. The uncited MLflow MCP Registry version claim and untested adapter are removed.

### Part II (Chapters 4–6) continuity pass

- Chapter 4 is now the book's map: it opens on the mortgage case and the Chapter 3 seam, uses the seven plane names in the tables and in Figure 4-1, maps Figure 1-3's bands onto them, renames layers so none is called "plane", and indexes every authoritative record to its owning plane and defining chapter.
- Chapter 4 receives the LLM Gateway contract from Chapter 19, explains the global control tier and regional execution cells in one section, annotates the end-to-end flow by owning plane (Figure 4-2 now assembles context before the step and shows the optional approval hop), and owns one base Run API table (`/audit` removed).
- The RunManifest gains prose and moves, with the artifact reference and the single CloudEvent shape, into the new `contracts#platform` example; the inline JSON and Python listings are gone and the effect receipt no longer contradicts Chapter 22.
- Chapter 5 uses "enforced rule" rather than "guardrail" (text, Figure 5-2, and the example class), adds the owner **Approve** step, moves the Knowledge Hub after provenance with a mode mapping and its two callers, and receives index freshness from Chapter 6.
- Chapter 6 has one ten-stage pipeline, five context sources, one segment `kind` enum mapped to trust tiers, memory in one section, and one ContextManifest schema in the new `context-manifest` example; the artifact-adoption listing leaves for Chapter 19.
- Approval terminology, Harborlight case boxes (Northstar removed), "Strong answer" and ✓ template forms, and Chapter 17 anti-pattern pointers are applied across Part II; the Chapter 4–6 covers follow the renamed components.

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

### Part IV — patterns that work and those that fail (continuity review)

- The Part IV orientation now links the patterns to the Part III platform and states the three questions every pattern chapter answers.
- Chapter 10 separates stopping (controller) from acceptance (acceptance engine), aligns its typed decisions with the shared contracts, and defines observations and information gain.
- Chapter 11 is now the home of handoff: framework handoff versus accountable handoff, the ownership table, and the acknowledgment protocol. Figure 11-1 shows eligibility before classification, and a new tested `route-validation` example replaces the inline router.
- Chapter 12 is reordered around the Plan IR: a risk-class gloss, a node-kind map to Part IV, compile-time checks next to the IR, and one revision section.
- Chapter 13 defines the acceptance engine and `AcceptanceDecision`. A tested `evaluator-optimizer` example replaces the inline listing that let the evaluator approve its own work, and Figure 13-1 runs executable checks before an advisory judge.
- Chapters 10–13 use "<Pattern> at a glance" cards, claim rows instead of generic evidence boxes, and drop R13/R07 citations that supported no claim.
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

### Part VI — Security, Identity, and Control (continuity review, WP-VI)

- The Part VI orientation states the "assume manipulation" premise once and maps Chapters 20–23, replacing a control order the chapters contradicted.
- Chapter 20 keeps "guardrail" in its detector sense only, has one nine-layer model (Figure 20-1 redrawn to match), and gives every threat card a first deterministic refusal layer. Figure 20-3 now shows the detector feeding the policy engine. It gains opening boxes and an incident section cited to NIST SP 800-61 [R42].
- Chapter 21 is reordered: subject, actor, and purpose; then the decision; then how authority travels, with capability envelope (scope) and credential lease (proof) defined. The subset proof is the new `capability-envelope` example.
- Chapter 22 is one argument with one implementation block. It defines Unknown canonically, relates risk classes to use-case tiers, and drops the inline ledger in favor of the `effect-idempotency` example. Figure 22-1 reserves the effect before approval.
- Chapter 23 continues the Chapter 20 example rather than retelling it. It drops its duplicate layer list, threat table, and credentials API, and adds kill-switch and data-lineage/privacy sections. Its code is now the `egress-url` and `kill-switch` examples, without the unrelated RTO/RPO class. The governance record moves to Chapter 26.
- Approval terminology replaces "human action authorization" throughout the Part. Chapter 21 and 23 cover labels follow the revised text.

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
