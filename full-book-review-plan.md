# Full-Book Review and Improvement Plan

**Scope:** Book v2.1.0, canonical source, registered examples, diagrams,
references, and generated publication artifacts.

**Objective:** Review the book as one coherent technical publication and one
reproducible system. Identify and fix substantive problems in the canonical
source and its supporting implementation, then regenerate and validate every
representation. The review must preserve the book's existing content and
architectural intent while removing contradictions, repairing broken
cross-references, clarifying the teaching path, and improving reader-visible
evidence.

## Review contract

The review will use this authority order:

1. `source/parts/*.md` is the editable prose source.
2. `config/*.json`, `examples/`, `mortgage_case/`, tests, and editable diagram
   sources are the implementation and metadata evidence.
3. `book/manuscript.md`, `dist/`, `latex/content/`, QA reports, and the release
   package are generated evidence and must be rebuilt rather than hand-edited.
4. `source/original/`, `source/part-visuals/`, and legacy tools are provenance,
   not editable review targets.

The review will preserve the enforced topology: 8 Parts, 28 chapters, and 12
appendices. The cumulative mortgage case remains the anchor implementation.
Supplier material may remain only when it is explicitly retained as a labeled
contrast; no retired supplier/refund scenario may silently reappear as the
running implementation.

## Review lanes

### 1. Content quality and technical accuracy

- Separate sourced fact, book-authored recommendation, illustrative example,
  estimate, and hypothesis.
- Check OpenAI Python SDK, OpenAI Agents SDK, MLflow, MCP, A2A, standards,
  security, regulation, and protocol claims against the recorded citation scope
  and pinned versions.
- Check formulas, units, dates, identifiers, state transitions, failure
  semantics, authorization boundaries, and terminology against the mortgage
  contracts and executable tests.
- Refuse unsupported certainty. Replace vague or absolute claims with bounded
  statements that name assumptions, ownership, and evidence.

### 2. Chapter structure and narrative flow

For each chapter, verify the sequence appropriate to its purpose:

`promise/prerequisites → problem → definitions/invariants → architecture →
implementation/example → failure/metrics/trade-offs → synthesis/transition`.

Pattern chapters additionally require:

`problem → anti-pattern → failure mechanism → recommended pattern →
architecture → mortgage example → detection metrics → trade-offs`.

The review will remove duplicate boilerplate only when the duplicated text adds
no chapter-specific value. It will not remove necessary recaps, prerequisites,
or transitions merely to shorten the manuscript.

### 3. Educational clarity and progressive disclosure

- Confirm that a reader can state the business problem, actors, inputs,
  outputs, constraints, and success criteria before implementation complexity.
- For every major concept, state what the system did before the concept, what is
  added, why it is needed, and what changes afterward.
- Distinguish model capability from platform authority and deterministic
  services from framework mechanics.
- Define uncommon acronyms before reuse and explain diagrams/tables in prose.
- Ensure exercises and review questions test the chapter's actual learning
  objective rather than repeat generic architecture advice.

### 4. Cross-book consistency

Audit these global contracts across prose, code, tests, diagrams, tables,
appendices, and registries:

- mortgage identifiers, actors, evidence states, workflow states, decision
  taxonomy, and non-negotiable invariants;
- `HumanActionAuthorization` versus `LendingDecision`;
- provider-neutral platform contracts versus OpenAI adapter types;
- C01–C28 chapter/checkpoint mapping and implemented-versus-target status;
- ownership of workflow state, evidence, calculations, policy, tools, effects,
  approvals, audit records, MLflow diagnostics, and evaluation;
- terminology, capitalization, hyphenation, version pins, status labels,
  cross-references, figure IDs, table captions, and example IDs;
- the front-matter table of contents versus actual H1 order and generated
  navigation.

### 5. Examples and code

- Every book listing must resolve to a registered source file and every
  registered example must have the declared verification mode and behavioral
  tests.
- All domain-specific Python must use the cumulative mortgage case. Generic
  algorithm demonstrations remain domain-neutral only where that is the lesson.
- Check imports, SDK APIs, type contracts, deterministic offline behavior,
  privacy-safe traces, error paths, retry ownership, idempotency, and executable
  output claims.
- Identify prose concepts with no demonstration and code/diagram components
  with no explanation. Add the smallest coherent mortgage extension or label the
  material explicitly as pseudocode/illustration.
- Confirm the code-gap roadmap is consistent with actual implementation status
  and does not imply that C04–C28 are already implemented.

### 6. Diagrams, tables, and visual communication

- Every visual must answer a reader question and match surrounding prose.
- Check trust boundaries, authority, data/control/evidence flows, ownership,
  failure states, and before/after progression.
- Check diagram registry IDs, captions, source/render synchronization, grayscale
  semantics, label legibility, and minimum resolution.
- Check tables for atomic cells, defined units/acronyms, consistent columns,
  repeated headers, useful comparison dimensions, and readable print scale.
- Replace dense prose disguised as a table or a diagram that merely decorates
  the page with the smallest clearer representation.

### 7. References and evidence

- Run reference resolution and verify that every registry entry is cited or
  explicitly retained for future use.
- Check each citation's permitted scope rather than treating a vendor document
  as proof of the book's architecture or business results.
- Record access dates and maturity caveats for living documentation.
- Remove or qualify claims that cannot be supported; do not fabricate sources.

### 8. Formatting, accessibility, and reader experience

- Check heading hierarchy, fresh-page chapter starts, standalone Part/divider
  pages, cover/title metadata, TOC order, page references, code language labels,
  captions, callout taxonomy, links, symbols, and line wrapping.
- Check color-independent meaning, contrast, font coverage, minimum table/code
  sizes, alt/caption text, and grayscale readability.
- Review representative generated Markdown, DOCX, and XeLaTeX pages for
  awkward breaks, clipped content, orphan headings, overfull code/tables, and
  inconsistent visual hierarchy.
- Treat LibreOffice-dependent DOCX pagination QA as a separate explicit gate;
  never call it passed when `soffice` is unavailable.

## Chapter-by-chapter review matrix

Each row will produce a short finding record during execution: `pass`, `fix`,
or `defer`, with file/section evidence and a regression test or validation
check where applicable.

| Unit | Learning objective and review focus | Mortgage continuity check |
|---|---|---|
| Front matter | Reader promise, audience, scope, claim discipline, authored TOC | Introduces Harborlight, C01, and the path without promising an autonomous lender |
| Part I / Ch 01 | From model call to governed agentic system; minimum viable boundary | C01 is simple, read-only, executable, and names the bottleneck |
| Ch 02 | Tools, structured outputs, deterministic shell, acceptance | C02 adds typed proposals/calculations without committing a lending decision |
| Ch 03 | Runtime/framework seam and provider ownership | C03 uses OpenAI Agents SDK through a provider-neutral adapter |
| Part II / Ch 04 | Reference architecture, boundaries, contracts, ownership | Extends the case into durable records, stores, events, and cells |
| Ch 05 | Knowledge governance, provenance, freshness, retrieval | Adds mortgage policy/evidence snapshots and refusal on stale/unauthorized sources |
| Ch 06 | Context engineering, RAG, memory, and state | Adds authorized context manifests and separates transient context from business state |
| Part III / Ch 07 | Developer platform, SDK, lifecycle, release gates | Maps the mortgage capability to reusable platform contracts and tests |
| Ch 08 | Versioned Skills and capability resolution | Resolves mortgage evidence capabilities with scope, owner, policy, and evaluation |
| Ch 09 | Skill Packs and domain platforms | Composes a mortgage evidence-review pack without broadening authority |
| Part IV / Ch 10 | Bounded ReAct and adaptive information gathering | Searches only authorized mortgage evidence under explicit budgets and stop rules |
| Ch 11 | Routing, triage, and handoffs | Transfers bounded ownership to evidence/policy specialists with inherited ceilings |
| Ch 12 | Planning and deterministic plan execution | Compiles model-proposed evidence work into validated mortgage tasks |
| Ch 13 | Reflection/evaluator-optimizer | Improves evidence summaries without allowing reflection to change authority |
| Ch 14 | Human-in-the-loop interruption and exact action authorization | Pauses for missing evidence or human operational authorization, not model credit approval |
| Ch 15 | Long-running durable execution | Survives waits, restart, replay, cancellation, and unknown effect reconciliation |
| Ch 16 | Enterprise pattern catalog | Catalog entries have selection criteria, mortgage mapping, metrics, and trade-offs |
| Ch 17 | Enterprise anti-pattern catalog | Failures are mechanism-based and connected to mortgage controls and tests |
| Part V / Ch 18 | Supervisor/worker collaboration and joins | Child tasks, grants, budgets, artifacts, and joins preserve case ownership |
| Ch 19 | MCP, A2A, gateways, and external trust | Mortgage artifacts cross external boundaries only through authenticated gateways |
| Part VI / Ch 20 | Threat model, guardrails, layered security | Malicious mortgage documents cannot reauthorize tools, data, or effects |
| Ch 21 | Identity, RBAC/ABAC, delegation, credential exchange | Subject, workload actor, case scope, purpose, and last-hop credentials are explicit |
| Ch 22 | Tool security, effects, idempotency, approval | Exact mortgage proposals, preconditions, receipts, and unknown states are durable |
| Ch 23 | Sandbox, egress, data security, governance | Synthetic/restricted mortgage data stays bounded; governance is executable |
| Part VII / Ch 24 | Distributed tracing and causal diagnostics | MLflow is diagnostic only; traces contain safe join keys, not applicant/document data |
| Ch 25 | Evaluation, learning, release improvement | Synthetic mortgage cohorts support deterministic, slice-aware, governed evaluation |
| Part VIII / Ch 26 | Governance, risk, operating model | Mortgage risk owners, exceptions, evidence, incidents, and review lifecycle are concrete |
| Ch 27 | Deployment, versioning, CI/CD, recovery | Case-version compatibility and rollback preserve in-flight mortgage runs |
| Ch 28 | Cost, latency, capacity, reliability | Metrics use verified underwriter-ready cases and bounded workload assumptions |
| Appendices A–C | Pattern index, runbooks, platform contract reference | Quick-reference material agrees with chapter names, states, and mortgage contracts |
| Appendices D–G | Framework landscape, research, limits, adoption roadmap | Claims are scoped; roadmap distinguishes implemented evidence from target work |
| Appendix H | Glossary | Terms match first-use definitions and stable contracts |
| Appendices I–J | Companion implementation guide and coding-agent acceptance criteria | No supplier code drift; implementation commands and acceptance gates are executable |
| Appendix K | References and traceability | Registry, in-text IDs, and claim scopes are synchronized |
| Appendix L / closing | Capacity/release acceptance and synthesis | Final checklist closes every production obligation without implying autonomous lending |

## Execution order

1. **Baseline and inventory:** capture branch/SHA, current generated hashes,
   structure counts, heading inventory, chapter transitions, example registry,
   diagram registry, reference audit, and existing reports.
2. **Front matter and global contracts:** repair reader promise, TOC, glossary,
   terminology, checkpoint mapping, and anchor-case definitions before local
   edits.
3. **Part-by-Part narrative review:** read each Part in order, including its
   opening orientation, all chapters, and transition into the next Part. Record
   duplicated arguments, missing prerequisites, abrupt technology changes, and
   unsupported claims.
4. **Implementation reconciliation:** compare every `[[EXAMPLE:id]]`, Python
   source, test, fixture, SDK import, MLflow call, diagram marker, registry
   record, and chapter claim. Apply fixes at the canonical source or source file.
5. **Visual and cross-format review:** regenerate diagrams if sources need
   changes, assemble Markdown, build DOCX and LaTeX source, and inspect
   representative pages/contact sheets where the environment permits.
6. **Full-book consistency pass:** search for stale names, contradictory state
   semantics, broken chapter references, undefined terms, duplicate guidance,
   ungrounded claims, and examples that regress to the old domain.
7. **Validation and release evidence:** run structural, citation, example,
   contrast, font, asset, deterministic, XeLaTeX, and package checks. Rebuild
   twice and validate from a clean extraction.
8. **Reviewable delivery:** update the changelog, create a self-contained PR
   using the repository template, request available reviewers, monitor CI, and
   leave the PR open for the author’s final review.

## Finding and fix policy

Use these severities:

- **Blocker:** misleading or unsafe architectural boundary, broken primary
  example, invalid generated output, missing source of truth, or a claim that
  can cause an unsafe lending interpretation.
- **Major:** chapter concept is materially wrong, disconnected from the case,
  technically stale, or contradicted elsewhere.
- **Moderate:** unclear explanation, missing failure/metric/example, stale
  cross-reference, or incomplete visual/table contract.
- **Editorial:** terminology, navigation, formatting, readability, or polish
  issue that can mislead or interrupt the reader.

For each finding, prefer the smallest coherent fix that improves all affected
consumers. Do not layer a new exception over contradictory prose. Preserve
content when possible by reframing, qualifying, relocating, or extending it.
Every substantive fix must have at least one of: a deterministic test, a
structural validator, a source/registry check, a rendered inspection, or an
explicit documented limitation.

## Definition of done

- The full 8-Part, 28-chapter, 12-appendix source has been reviewed against the
  matrix above.
- Blockers and majors are fixed or explicitly documented with owner and reason.
- The mortgage example progresses coherently from simple agent to production
  architecture without unexplained domain or technology jumps.
- All code, diagrams, tables, references, terminology, and cross-references
  agree with the canonical source and registries.
- Canonical Markdown, distributable Markdown, DOCX, LaTeX source, generated
  reports, manifests, checksums, and package are synchronized.
- Local tests/builds and remote CI results are reported separately. Missing
  optional tooling (especially `soffice`) remains visible as an unmet gate.
- A dedicated branch and open PR exist; the PR is not merged by the agent.
## Current execution ledger — 2026-09-16

This ledger is the handoff point for continuing the review. It records only
evidence present in the current checkout; a generated report or a prior PR is
not treated as proof that an unrun local gate has passed.

| Area | Status | Evidence or remaining action |
|---|---|---|
| Repository baseline | `pass` | Current review branch is based on `eca5f82`; preserve the unrelated untracked `mortgage_case/platform/` files. Re-capture SHA and status before any source edit. |
| Topology and structural contracts | `pass` | `reports/validation-summary.md` records 8 Parts, 28 chapters, 12 appendices, 45 registered diagrams, 48 references, and 107 citation occurrences with no validation errors. |
| Canonical/generated synchronization | `pass` | The same report records byte-identical canonical and distributable Markdown, a valid DOCX package, and synchronized generated reports/manifests/checksums. |
| Mortgage narrative and terminology | `pass with evidence` | `reports/technical-validation.md` records Harborlight Mortgage continuity and consistent `HumanActionAuthorizationRequest` / `HumanActionAuthorizationDecision` vocabulary. Recheck any future source edits against this contract. |
| Example and implementation reconciliation | `pass with evidence` | The technical validation record reports 26 examples and 123 tests passed. The next implementation pass must keep C04–C28 labelled as target work unless executable evidence is added. |
| References and claim scope | `pass` | `reports/citation-audit.md` records 48 registry entries, 107 occurrences, and no unknown or uncited IDs. Living sources and caveats remain release-time re-verification obligations. |
| XeLaTeX and source visual inspection | `pass with caveat` | Genuine XeLaTeX completed at 287 pages; source validation and representative XeLaTeX pages passed. Dense-table and long-label overfull warnings remain typography follow-up items. |
| DOCX pagination QA | `defer` | `make qa-pdf` is not complete because LibreOffice/`soffice` is absent. Do not promote this to `pass` from DOCX package validity or XeLaTeX inspection. |
| Matrix finding records | `in progress` | The matrix above defines review intent but does not yet contain one evidence-bounded `pass`, `fix`, or `defer` record for every row. Populate the record format below during the next Part-by-Part pass. |
| Review delivery | `pending` | Commit this plan update on its dedicated branch, open a PR, request available reviewers, and leave it open. Do not merge it or claim terminal CI until observed. |

### Finding record contract

Every matrix row must produce one compact record, even when the result is
`pass`. Keep records close to the source evidence so a later editor can tell
whether a statement was inspected, tested, rendered, or merely planned.

```text
ID: FB-<unit>-<number>
Status: pass | fix | defer
Severity: blocker | major | moderate | editorial | none
Scope: <chapter, appendix, or cross-book contract>
Finding: <one reader-visible or implementation-visible statement>
Evidence: <source/report/test/registry path and section or symbol>
Decision: <preserve | qualify | relocate | edit | add test | defer>
Regression check: <exact command, test, structural check, or rendered inspection>
Owner/exit condition: <person or concrete condition; required for defer>
```

Do not use `pass` to mean “no issue found in a quick search.” Use it only when
the stated evidence covers the row's learning objective and mortgage-continuity
check. Use `defer` only with an owner or an observable exit condition. A source
edit changes the status of every affected record to `needs-rerun` until its
regression check is repeated.

### Next review slices

Continue in these slices, committing only a coherent source or documentation
change per PR. A slice may be closed without a manuscript edit when its finding
records and checks show that the current text is adequate.

1. **Front matter and Part I:** reconcile the authored table of contents,
   Harborlight/C01–C03 progression, framework/platform boundary, glossary
   first use, and the runtime-boundary visual. Re-run structure, examples, and
   LaTeX-source checks after any edit.
2. **Parts II–III:** verify knowledge provenance, context/state ownership,
   provider-neutral contracts, capability resolution, and the C04–C09 roadmap.
   Compare prose claims with `config/examples.json`, mortgage contracts, and
   behavioral tests; do not infer implementation from a chapter's aspiration.
3. **Parts IV–V:** trace budgets, retry ownership, handoffs, joins, external
   gateways, and unknown-effect semantics through the durable mortgage case.
   Check that every pattern/anti-pattern has a failure mechanism, metric, and
   bounded example.
4. **Parts VI–VII:** audit identity, delegation, tool effects, privacy,
   sandboxing, MLflow diagnostics, evaluation cohorts, and release gates. Keep
   applicant/document data out of traces and keep authorization outside model
   output.
5. **Part VIII and appendices:** reconcile governance, recovery, capacity,
   glossary, runbooks, implementation commands, references, and closing
   acceptance criteria. Confirm the roadmap distinguishes implemented C01–C03
   evidence from target C04–C28 work.
6. **Cross-format closeout:** regenerate all required artifacts from canonical
   sources, run the complete local gate set, perform the second deterministic
   rebuild, and record `qa-pdf` separately as `pass` or `defer` according to
   actual `soffice` availability.

### Required handoff record for each slice

At the end of each slice, append or link a short result containing the slice
IDs, changed files, unresolved findings, commands and outcomes, generated
artifact status (Markdown, DOCX, LaTeX, and PDF separately), and the next exit
condition. This keeps a later PR review from confusing a validated source
change with a merely planned follow-up.

## Slice 1 handoff — Front matter and Part I — 2026-09-16

| ID | Status | Severity | Finding and decision | Evidence and regression check |
|---|---|---|---|---|
| `FB-front-01` | `fix` | moderate | The front matter and Part I opening made Harborlight sound like an additive case while Northstar callouts still looked like the implementation anchor. Make Harborlight/C01–C03 the explicit cumulative path and label Northstar as comparative architecture evidence. | `source/parts/00-front-matter.md`, `source/parts/01-part-i.md`; `make validate`, `make pdf`, and page-22/page-33/page-34 XeLaTeX inspection passed. |
| `FB-part1-01` | `fix` | editorial | Wrapped numbered-list items were emitted as three separate LaTeX lists, rendering `1, 1, 1` and exposing literal emphasis markers in the third item. Keep each item contiguous in canonical Markdown so the generated list renders as `1, 2, 3`. | `source/parts/01-part-i.md` production-problem questions; `make pdf` and page-33 XeLaTeX inspection passed. |

Changed canonical files are `source/parts/00-front-matter.md` and
`source/parts/01-part-i.md`. Synchronized outputs and evidence are the
assembled Markdown, distributable Markdown, DOCX, LaTeX content, validation
reports, technical validation record, changelog, and release notes. The local
XeLaTeX PDF was rebuilt at 286 pages but remains a regenerable, uncommitted
artifact. DOCX pagination QA remains `defer` because `soffice` is unavailable;
package validity and deterministic DOCX checks are not substitutes for that
gate. Notion synchronization is out of scope until all release gates pass.

Next exit condition: begin the Parts II–III slice by auditing knowledge
provenance, context/state ownership, provider-neutral contracts, capability
resolution, and the C04–C09 roadmap against their registries and tests.
