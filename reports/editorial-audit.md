# Editorial Audit — Full-Book Review and Running-Example Gap Audit

## Addendum — Cumulative Northstar implementation review

**Reviewed:** 2026-09-16
**Roadmap:** [code-gap.md](../code-gap.md)

### Scope and finding

The earlier editorial reconciliation generalized the supplied first-30-page
review across the manuscript. This addendum audits a different learning-system
property: whether the Northstar supplier-onboarding example is one executable
system that grows chapter by chapter. The full book was inspected at the Part,
chapter-opening, transition, implementation-reference, appendix, registry,
example, and test levels.

The primary finding is **one blocker and multiple major integration gaps**: the
book has a strong cumulative prose narrative, but its 23 registered examples are
mostly isolated pattern demonstrations. The Chapter 1 prototype references
undefined tools, and no canonical Northstar fixture, workflow composition,
domain connector, approval/effect path, or end-to-end trace/evaluation joins
the examples. Existing code is valuable evidence for individual controls, but it
does not yet let a reader run the system described across the chapters.

### Resolutions for this audit

- Created [code-gap.md](../code-gap.md) as the implementation roadmap rather
  than making a speculative large code change in this review PR.
- Defined one canonical Northstar case, actors, inputs, outputs, state machine,
  constraints, success criteria, technology ownership, and cumulative
  architecture.
- Mapped all 28 chapters to a before/add/after implementation contract with
  severity, dependencies, PR order, acceptance criteria, and relevant files.
- Distinguished OpenAI API, OpenAI Agents SDK, MLflow, custom Python, and test
  doubles so framework mechanics do not become enterprise truth.
- Preserved the existing focused examples as reusable pattern evidence while
  identifying the Northstar modules and tests required to connect them.
- Added explicit offline, failure-injection, trace/audit separation, registry,
  generated-artifact, PR, and full-book acceptance gates.

### Residual risks

- The roadmap is not implementation. Until its staged PRs land, the example
  remains partly narrative and the Chapter 1 inline listing remains unsuitable
  as a runnable source unless relabeled or replaced.
- Current examples and chapter labels may reflect different historical chapter
  numbers; the examples README and registry should gain stage metadata during
  the first implementation PR.
- Pagination QA remains unavailable without LibreOffice/`soffice`, as recorded
  below. This roadmap adds no manuscript prose or diagram assets, so no new
  visual claim is made here.

### Release recommendation

**Do not call the running example production-ready yet.** Accept this PR as the
implementation plan, then implement PR-NS-00 through PR-NS-27 incrementally,
with each PR independently reviewed and validated. The manuscript’s existing
publication artifacts remain valid for the current v2.1.0 source; the cumulative
example should be treated as an explicit next-workstream until the full-book
acceptance gates in `code-gap.md` pass.

## Addendum — Mortgage foundation implementation slice

**Reviewed:** 2026-09-16
**Implementation scope:** `C01`–`C03` only

The first implementation slice establishes the reviewed plan without deleting
the original instructional material. It adds a synthetic Harborlight mortgage
case, an explicit business/actor/input/output contract, a missing-evidence
bottleneck, before/added/after transitions, a portrait-friendly lifecycle
diagram, and a tested cumulative code façade. Existing supplier passages remain
in the manuscript as labeled contrast material while later checkpoint PRs
extend the mortgage path through workflow, authorization, effects, observability,
evaluation, and operations.

### Evidence added

- `mortgage_case/` provides `C01` read-only summary, `C02` typed deterministic
  shell, and `C03` provider-neutral runtime contracts.
- `config/mortgage_stages.json` preserves the exact `C01`–`C28` chapter mapping;
  only `C01`–`C03` are marked implemented.
- `tests/mortgage_case/` covers synthetic-fixture invariants, missing evidence,
  Decimal LTV/DTI calculations, stale proposals, protected-decision rejection,
  tool allowlist enforcement, and the actual optional Agents SDK translation.
- `examples/mortgage/cumulative_case.py` is registered and cited from the three
  Part I checkpoint sections, so the book listing is sourced from tested code.
- `assets/diagrams/src/mortgage-case-lifecycle.gv` is the editable source for
  the new registered vector/raster figure.

### Residual risks

- The cumulative implementation is intentionally incomplete after `C03`; it
  does not yet provide durable workflow, identity, approval, protected LOS
  effects, MLflow tracing/evaluation, or production capacity controls.
- Part I now introduces the mortgage anchor, but supplier material remains in
  later chapters until their checkpoint-aligned migration PRs land. A full-book
  stale-term and preservation review is required after each subsequent slice.
- The checked-in v2.1.0 output is synchronized and structurally valid, but DOCX
  pagination QA still requires LibreOffice/`soffice` in the validation
  environment.

### Recommendation

Accept this as the foundation PR only when its generated artifacts and tests
remain synchronized. Do not describe the mortgage implementation as
production-ready until `C04`–`C28` and the full-book acceptance gates in
`code-gap.md` are complete.

## Scope and evidence

This audit records the full-book response to the supplied review document:

`reviews-comments/Enterprise-General-Intelligence-v2.1.0 - review till page 30.docx`

The document contained 23 anchored comments covering the cover, front matter,
the opening chapters, terminology, diagrams, and chapter structure. The review
was treated as a set of editorial principles rather than as a page-local patch.
Those principles were checked against all eight Parts, 28 chapters, 12
appendices, the configuration registries, diagram sources, and repository
documentation.

## Resolutions

### Reader promise and front matter

- The title is now **Building Enterprise General Intelligence Platform**.
- The audience line names architects, platform engineers, DevOps engineers, and
  SREs.
- The Preface now presents a clear progression from model call to governed
  production platform.
- Scope and claim discipline distinguish numbered-source claims from
  book-authored guidance and identify the author’s practical enterprise
  experience without presenting it as external evidence.
- The reproducible-edition and reference-guide sections now state the
  canonical-source, deterministic-build, evidence, ownership, trust-boundary,
  reversibility, and improvement-loop contracts.
- The appendix list is formatted as a readable bullet list, and the redundant
  standalone canonical-source subsection was removed.

### Terminology, topology, and navigation

- “Rung” is consistently replaced with “level” in the capability model, its
  prose, and the editable diagram source.
- Chapter 1, Part II, Chapter 22, Part VII, Chapter 24, and Chapter 25 titles
  now match the reviewed terminology and the canonical source.
- The configuration registry, README, and pull-request template now describe
  the actual eight-Part, 28-chapter, 12-appendix topology.
- A stale Chapter 4 figure reference was corrected to the current Chapter 1
  figure identifier.
- Stale embedded Part maps in Parts I, IV, and V were removed; the assembled
  front matter remains the single navigation map.

### Architecture and diagrams

- The control-point explanation now distinguishes API admission, agent/task
  admission and delegation, model selection, tool/effect authorization, MCP
  server trust, and human approval.
- Human approval is represented as a bounded approval gate for the exact
  proposal, while acceptance, evaluation, and release gates remain explicit
  lifecycle controls rather than being conflated with runtime gateways.
- The system overview and gateway-roles diagrams were updated from their
  editable Graphviz sources; the capability ladder terminology was updated in
  its source and registry description.
- Cover metadata and generation logic were updated so the five-line title fits
  without colliding with the subtitle.

### Chapter-level writing and structure

- The redundant grounding/evidence, implementation-reference, debugging,
  production-checklist, and exercises boilerplate was removed from the early
  Chapter 3 review because the direct comment called for its removal there.
  Later chapters retain sections with those labels only where they provide
  distinct chapter-specific implementation or decision utility; they were not
  removed mechanically from the whole book.
- Chapter 25 now frames continuous learning as a governed loop that observes,
  measures, detects, diagnoses, recommends, validates, approves, deploys,
  monitors, and curates improvements.
- Cross-references, labels, diagrams, tables, and configuration titles were
  reviewed together so the revised concepts are not isolated from later
  architecture, security, observability, and operations chapters.

## Validation status

The canonical source, registries, generated Markdown/DOCX/LaTeX artifacts,
editable diagrams, cover, manifests, checksums, and release ZIP have been
rebuilt. Assembly, references, example registry checks, LaTeX structural
validation, DOCX integrity, genuine XeLaTeX compilation, deterministic DOCX
rebuilds, runnable example tests, packaging, and the extracted-package rebuild
all pass. The final XeLaTeX output is 277 Letter-size pages.

The supplied DOCX could be structurally extracted and its 23 comments read, but
the documents skill’s render-and-inspect step was unavailable in this
environment: the bundled renderer requires the missing `pdf2image` package,
and neither LibreOffice nor `soffice` is installed. The repository’s
pagination-QA gate therefore remains explicitly unavailable; no pagination
pass is claimed.

Notion synchronization and merge are out of scope for this PR. The PR remains
open for the author’s review.
