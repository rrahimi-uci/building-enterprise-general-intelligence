# Mortgage Running Example — Code Gap and Implementation Roadmap

**Source actually supplied and reviewed:** *Building an Enterprise General Intelligence Platform*, Book v1.0.0, September 2026
**Course alignment:** *Building Enterprise-Grade Agentic Systems — Course*, 14 lessons
**Scope:** one cumulative mortgage case across Book Chapters 1–28, cross-mapped to the 14 course lessons
**Audit date:** 2026-09-16
**Status:** corrected implementation roadmap; the foundation slice for `C01`–`C03`, the targeted C24 OpenAI/Agents SDK/MLflow grounding slice, and an offline platform-contract slice spanning C04–C28 are implemented on this branch. Full chapter-integrated checkpoint execution, CLI wiring, and release evidence for C04–C28 remain planned.

## Executive decision

Replace the supplier-onboarding code thread with one fictional, synthetic mortgage **anchor case** and evolve that case one bounded capability at a time. Controlled variants and synthetic cohorts may be added for failure, fairness, evaluation, and capacity tests, but they must never replace the anchor narrative. A reader should be able to run Chapter 1, understand its deliberate weaknesses, and then run every later chapter to see exactly what changed, why it changed, which component now owns the new responsibility, and which new failure modes and tests were introduced.

The running implementation is **not** an autonomous mortgage underwriter. It prepares and verifies an evidence package, proposes conditions and next actions, coordinates human review, and records human-authorized effects. A model must never independently approve or deny credit, set authoritative eligibility, invent an adverse-action reason, use protected characteristics, or commit a loan-origination-system decision.

The implementation contract is:

1. **One anchor case:** the same case ID, people, document lineage, policy family, and target outcome recur in every chapter; controlled variants and cohorts exist only for explicit tests.
2. **One additive package:** later chapters add modules and composition; they do not silently replace the domain or start unrelated demos.
3. **One chapter-to-checkpoint mapping:** `C01` means Chapter 1 and `C28` means Chapter 28. There is no off-by-one “Stage 0.”
4. **One visible learning delta:** every checkpoint prints or documents **before → added → after**.
5. **One safe authority model:** models propose; deterministic services validate, calculate, authorize, transition, commit, verify, and accept; an authorized human owns the final lending decision.
6. **One offline path:** all required tests and demonstrations run without credentials, network access, a hosted MLflow server, or a real mortgage system.
7. **Optional real adapters:** direct OpenAI Python SDK, OpenAI Agents SDK, MLflow, MCP, A2A, and durable-engine integrations are opt-in adapters with separate contract tests.
8. **One command convention:** every checkpoint runs as `python -m mortgage_case --chapter N --scenario NAME --offline`; output always conforms to `StageReport`.
9. **Progressive hardening without premature authority:** early chapters may introduce forward-compatible identity, approval, task, and effect contracts, but no protected connector can execute until the chapter that owns its enforcement has landed.

## Additive-content preservation contract

The mortgage migration must preserve the book as a learning system. No chapter,
appendix, explanation, example, diagram, table, code listing, exercise, review
question, or architectural principle may be silently removed because the
running domain changes.

The implementation may improve clarity, correct contradictions, tighten names,
or move a passage to the place where it is taught, but each original concept
must remain traceable to one of these outcomes:

| Preservation outcome | Meaning |
| --- | --- |
| Mortgage extension | The concept is demonstrated through the cumulative mortgage case and its bottleneck. |
| Retained contrast | The original supplier, refund, payment, or support example remains because it teaches a distinct boundary; it is labeled as a contrast rather than allowed to compete with the anchor case. |
| Cross-domain principle | The original material is already framework- or domain-neutral and remains unchanged except for terminology and cross-reference repair. |
| Corrected explanation | The original instructional intent is retained while an unsafe, contradictory, or technically inaccurate statement is clarified. |

Every implementation PR must include a preservation ledger covering the affected
source chapters and generated code listings. The ledger records the original
concept, its mortgage extension, the bottleneck it exposes, the new owner, and
the acceptance test or reader-facing evidence. A review is incomplete if it can
show what was added but cannot show where the retained material went.

Each chapter transition uses the same additive shape:

`before capability → bottleneck → added mortgage capability → after capability → retained limitations → next dependency`

The mortgage case is the cumulative code path. Existing supplier material may
remain as a clearly labeled contrast during migration, but it must not introduce
a second untracked implementation, a conflicting authority model, or a second
meaning for a shared identifier.

## What was reviewed

The review covered the supplied Book v1.0.0 Markdown, the 14-lesson course, the original `code-gap.md`, the repository implementation, and the public API names referenced by the book. Static extraction found 54 Python fenced snippets in the original book; all parse as Python syntax when considered individually, but many are teaching excerpts rather than standalone programs. Syntax validity therefore does not prove that imports, names, external services, or end-to-end behavior work. The implementation audit runs the pinned offline environment and tests the provider boundaries with fakes or the scripted Agents SDK model.

The companion implementation guide (then Appendix I, now Appendix H) originally described a `northstar` package and supplier-onboarding demo that do not match the repository’s canonical `mortgage_case` package. The appendix is now corrected to distinguish the framework-neutral architecture from the implemented mortgage slice. The registry and generated reports, rather than hand-maintained prose counts, are authoritative for the complete example suite.

## Bugs and design defects corrected across both critique passes

| Severity | Defect found | Correction |
| --- | --- | --- |
| Blocker | The original roadmap explicitly prohibited mortgage as the primary case and made supplier onboarding canonical. | Mortgage evidence orchestration is now the only cumulative case; supplier examples may remain only as clearly labeled contrasts during migration. |
| Blocker | Chapter 1 presents an `Agent` with `lookup_supplier`, `create_supplier`, and `send_email`, while the first listing does not define all three tools. | `C01` has a complete offline baseline with no undefined symbol and no write-capable tool. |
| Major | “Stage 0 = Chapter 1” creates an avoidable off-by-one mapping through all 28 chapters. | Checkpoints are `C01` through `C28`, exactly matching chapter numbers. |
| Major | The roadmap claimed repository inventory and test counts that were not present in the supplied artifacts. | Evidence is labeled as **verified in source**, **claimed by Appendix H**, or **target implementation**. |
| Major | The original Chapter 2 stage introduced a protected supplier creation before approvals, durable effects, and identity were taught. | Early mortgage checkpoints remain read-only or draft-only. The canonical protected LOS mutation is introduced only after approval, durability, identity, and effect semantics exist. |
| Major | A mortgage case is a high-impact lending context, but the roadmap had no explicit boundary preventing model-owned approve/deny decisions. | Final lending decisions, eligibility, authoritative calculations, and adverse-action reasons are human/domain-service responsibilities and are executable negative-test invariants. |
| Major | “OpenAI SDK” and “OpenAI agentic SDK” were not separated by package or role. | The roadmap distinguishes the OpenAI Python SDK (`openai`) from the OpenAI Agents SDK (`openai-agents`). “OpenAI Agentic SDK” is not treated as a third library. |
| Major | The source gives `openai>=2.25.0`, which does not match the pinned OpenAI Agents SDK 0.22.2 environment (`openai-agents` declares the compatible OpenAI Python SDK 3.x range). | The offline profile now pins `openai==3.13.0` explicitly, and the adapter contract test proves the Responses API request shape without a network call. |
| Major | Model-extracted values were not cleanly separated from verified facts and deterministic mortgage calculations. | `ExtractedFactCandidate`, `VerifiedEvidence`, `CalculationResult`, and `UnderwritingRecommendation` have different owners and acceptance rules. Money and ratios use `Decimal`, not binary floating point. |
| Major | Mortgage PII, document sensitivity, and fair-lending risks were not addressed. | All fixtures are synthetic; SSNs/account numbers are tokenized; raw document bytes stay outside prompts and traces; protected attributes are excluded from runtime decisions and isolated, when authorized, for governed fairness evaluation only. |
| Major | MLflow could be read as the audit system or as permission to capture prompts automatically. | MLflow is diagnostic/evaluation infrastructure only. Sensitive input/output capture is off by default, and audit/effect/approval evidence remains in separate authoritative stores. |
| Moderate | Each stage proposed many new files without a stable cumulative package contract. | A stable domain package, additive platform modules, and immutable chapter entry points prevent copy/paste drift while preserving earlier checkpoints. |
| Moderate | Acceptance criteria often described success without a reader-visible command or expected evidence. | Every checkpoint requires an offline command, expected `StageReport`, at least one failure/refusal scenario, and named behavioral tests. |
| Moderate | The attached book’s cover title and Appendix H companion title are inconsistent. | This roadmap uses the supplied cover title and refers to the companion package generically; manuscript title normalization remains a source-edit follow-up. |
| Major | The first revision placed the package under `examples/mortgage_case/` but invoked it as `python -m mortgage_case`; that import does not work from a clean checkout without extra packaging configuration. | The target package now lives at repository root as `mortgage_case/`, so the documented module command and compile command agree. |
| Major | “One case” conflicted with multi-case fairness, reliability, and capacity evaluation. | `MORT-2026-000184` is the anchor case; controlled variants and versioned synthetic cohorts are permitted for tests and never replace the narrative. |
| Major | Bare `ApprovalRequest`/`ApprovalDecision` is dangerously ambiguous in a mortgage context because readers may confuse a platform approval of one operational effect with credit approval. | The platform records are `ApprovalRequest`/`ApprovalDecision` (review decision D-22, Chapter 14): an approval permits one exact operational effect and is never credit approval; `LendingDecision` remains a separate underwriter/domain record. |
| Major | Chapters 14, 18, and 19 used approval/grant semantics before Chapter 21 fully introduced identity and delegated authorization. | A minimal `PrincipalContext` and non-executable `CapabilityScope` begin in `C04`; pre-`C21` tasks are synthetic/read-only, and `C21` upgrades and revalidates the contracts before `C22` permits the first protected write. |
| Moderate | The canonical calculation fixture named LTV/DTI but did not state deterministic inputs, expected outputs, precision, or serialization. | A versioned synthetic calculation oracle now specifies `Decimal` inputs, formulas, four-decimal outputs, rounding, and string serialization. |
| Moderate | Trace guidance allowed business identifiers without requiring pseudonymization and did not explicitly exclude hidden reasoning. | `C24` requires opaque/pseudonymous correlation IDs, a protected lookup map, and no raw PII, document text, credentials, or hidden chain-of-thought in telemetry. |
| Moderate | Fairness and release evaluation lacked explicit sample-size, uncertainty, and leakage controls. | `C25` adds cohort provenance, holdout separation, minimum sample rules, confidence intervals/uncertainty, repeated-run variance, and the rule that synthetic results prove pipeline behavior—not real-world fairness or legal compliance. |

### Severity definitions

| Severity | Meaning |
| --- | --- |
| **Blocker** | The first case cannot run, the primary domain is wrong, or the system can imply an unsafe lending decision. |
| **Major** | A chapter’s production boundary is absent, bypassable, or not connected to the cumulative case. |
| **Moderate** | The concept exists but lacks a mortgage integration, failure path, documentation, or executable evidence. |
| **Editorial** | Naming, numbering, versioning, or navigation can mislead readers even though the underlying design is sound. |

## Canonical mortgage case

### Business problem

**Harborlight Home Finance** is a fictional lender. Its loan teams spend several days collecting and reconciling application documents before an authorized underwriter can review a case. The target is to prepare an accurate, explainable, underwriter-ready evidence package within one business day for routine synthetic cases without weakening identity, privacy, policy, human oversight, audit, or recovery controls.

The stable training fixture is:

| Field | Synthetic value |
| --- | --- |
| Tenant | `harborlight-us-west` |
| Case ID | `MORT-2026-000184` |
| Applicant | `Alex Morgan` |
| Property | `101 Example Avenue, Portland, OR 97205` |
| Purpose | `mortgage_pre_underwriting_review` |
| Loan scenario | Fictional conventional, owner-occupied purchase |
| Purchase price | `USD 625000.00` |
| Requested principal | `USD 500000.00` |
| Evidence set | Application, consent, pay statements, tax forms, bank statements, employment verification, credit artifact, purchase agreement, title artifact, and appraisal artifact |
| Expected outcome | A verified review package, explicit unresolved conditions, an underwriter recommendation, and a recorded human/domain-system disposition—not an autonomous credit decision |

All names, addresses, identifiers, documents, policies, scores, and amounts are synthetic. The repository must include a conspicuous `SYNTHETIC TRAINING DATA — NOT FOR CREDIT DECISIONS` marker in every fixture and rendered example output.

Tokens and masked values remain classified as restricted data in the example; tokenization is not treated as anonymization.

### Deterministic calculation oracle

The following values become usable only after their supporting synthetic evidence has been verified. They are calculation test vectors, not eligibility rules or lending guidance.

| Item | Canonical value | Rule | Expected result |
| --- | --- | --- | --- |
| Purchase price | `Decimal("625000.00")` | Input from verified purchase agreement | — |
| Requested principal | `Decimal("500000.00")` | Input from verified application | — |
| Verified gross monthly income | `Decimal("12500.00")` | Available only after required income evidence is accepted | — |
| Total monthly obligations | `Decimal("4200.00")` | Versioned deterministic aggregation, including proposed housing obligation | — |
| LTV | Principal ÷ purchase price | Quantize to `Decimal("0.0001")` | `Decimal("0.8000")` |
| DTI | Total monthly obligations ÷ verified gross monthly income | Quantize to `Decimal("0.0001")` | `Decimal("0.3360")` |
| Rounding/serialization | `ROUND_HALF_EVEN`; canonical decimal strings | Never round-trip through JSON floating point | Stable across supported platforms |

The training policy may evaluate these outputs, but a numeric result by itself never creates eligibility, a lending decision, or an adverse-action reason.

### Narrative shown to the reader

At `C01`, Alex’s case has a mortgage application, one pay statement, and a purchase agreement. A small model call can summarize the file and suggest that evidence is missing, but it cannot prove the facts, calculate authoritative debt-to-income or loan-to-value ratios, access the loan-origination system, or make a lending decision.

Each chapter repairs one concrete limitation. By `C28`, the anchor case can survive document waits and worker crashes, use bounded specialist tasks, authorize exact resources, resist a malicious document, reconcile an uncertain LOS update, produce a privacy-safe MLflow trace, run a release evaluation, and report cost and reliability per verified underwriter-ready case. From `C25` onward, a separate versioned synthetic cohort supplies the multiple cases required for slice, repeated-run, and capacity analysis.

### Actors and authority

| Actor or component | Owns | Must never own |
| --- | --- | --- |
| Applicant | Supplies application data and evidence; responds to requests | Platform policy, system permissions, or final system transitions |
| Loan officer | Initiates and monitors the case for an allowed purpose | Unreviewed model authority or unrestricted cross-case access |
| Durable mortgage workflow | State, waits, retries, deadlines, obligations, joins, cancellation, and completion | Interpretation of ambiguous documents or final credit judgment |
| Evidence agent | Extracts candidate facts, identifies gaps, synthesizes cited evidence, proposes next work | Fact certification, authorization, protected effects, or approve/deny decisions |
| Specialist agents | Perform bounded document, income, asset, property, or policy tasks | Parent ownership, broader access, or final case disposition |
| Calculation and policy services | Canonical calculations, rules, reason codes, freshness, and deterministic eligibility gates | Free-form model interpretation or unsupported legal conclusions |
| Policy decision point and credential broker | Exact subject+actor authorization and short-lived connector credentials | Business commits or disclosure of reusable credentials to models |
| Authorized underwriter | Reviews the exact evidence/recommendation and records the lending decision | Reusing approval for changed evidence, policy, amount, or case version |
| Tool Gateway and connectors | Validate, authorize, invoke, sanitize, verify, and record reads/effects | Broadening authority or translating model confidence into permission |
| Loan-origination system | Authoritative case and decision record | Agent workflow history, prompt state, or evaluation truth |
| Operator, security reviewer, and auditor | Recovery, containment, evidence review, and governed intervention | Rewriting immutable history or silently bypassing policy |

### Information and decision taxonomy

| Type | Example | Owner and rule |
| --- | --- | --- |
| Candidate extraction | Employer name inferred from a pay statement | Model may propose; never treated as verified without source/provenance and deterministic checks |
| Verified evidence | Employment verification artifact with source revision and digest | Verification/domain service owns status and freshness |
| Deterministic calculation | LTV, DTI, document age, totals, and consistency checks | Typed calculation service using `Decimal`, explicit rounding, and versioned formulas |
| Policy result | Required evidence, threshold result, approval obligation, reason code | Versioned policy service; model may explain only from the returned result |
| Recommendation | `ready_for_underwriter`, `needs_evidence`, or `intervention_required` | Model may propose; evaluator and workflow validate evidence and obligations |
| Approval | Permit one exact operational effect such as sending a condition request | Authorized reviewer plus platform policy; never a lending decision |
| Lending decision | Approve, deny, suspend, or counteroffer | Authorized human and/or regulated deterministic decision service outside the model runtime |
| External effect | Create a condition, mark case ready for review, or record the human decision | Gateway/domain service under idempotency, concurrency, approval, and receipt controls |

### Terminology: an approval is not credit approval

Use `ApprovalRequest` and `ApprovalDecision` (Chapter 14) only for permission to execute one exact platform effect. The allowed responses are approve, reject, edit-and-resubmit, request-evidence, and cancel-run; an unanswered request expires. Use `LendingDecision` only for the authoritative mortgage disposition recorded by the underwriter/domain system. Never record a credit disposition as an `ApprovalDecision`, and never present an “Approve” button without saying which kind of decision it represents.

### Stable workflow

```text
APPLICATION_RECEIVED
  -> DOCUMENTS_PENDING
  -> EVIDENCE_REVIEW
  -> VERIFICATION_PENDING
  -> CONDITIONS_PENDING
  -> ACTION_REVIEW_PENDING
  -> READY_FOR_UNDERWRITER
  -> UNDERWRITER_DECISION_PENDING
  -> DECISION_RECORDED
  -> WORKFLOW_COMPLETED
```

Non-success or waiting dispositions are `NEEDS_INPUT`, `POLICY_BLOCKED`, `UNKNOWN_EFFECT`, `INTERVENTION_REQUIRED`, `CANCELED`, and `FAILED`. `WORKFLOW_COMPLETED` means that required workflow obligations were discharged and the external disposition was verified; it does **not** mean that the mortgage was approved.

### Non-negotiable mortgage invariants

1. A model cannot emit or commit a final `approve`, `deny`, `counteroffer`, interest rate, or authoritative adverse-action reason; it may only produce bounded non-dispositive recommendations such as `ready_for_underwriter`.
2. Candidate facts never become verified evidence merely because they are well formed or repeated by another model.
3. DTI, LTV, totals, dates, thresholds, and money use deterministic versioned code with `Decimal`, timezone-aware dates/times, explicit rounding, and canonical string serialization.
4. Protected characteristics are not runtime decision features and do not enter planning, tool choice, recommendation, or model context. Separately governed data may be collected for authorized compliance/fairness analysis, and proxy-feature and outcome-disparity tests remain required.
5. Tenant and case authorization happens before document content reaches a model.
6. No raw SSN, bank account, credential, complete document, unrestricted prompt, or hidden chain-of-thought is placed in a normal trace, log, exception, or MLflow tag.
7. Every write has one logical effect key, one canonical intent hash, a current case precondition, a receipt or `UNKNOWN_EFFECT`, and a reconciliation path.
8. Every approval is bound to the exact case version, evidence set, policy version, proposal hash, actor, and expiry. The final `LendingDecision` is a separate authoritative record with its own actor, evidence, policy, and case version.
9. A timeout after a write never becomes an ordinary retry.
10. Terminal workflow completion is impossible while required evidence, approval, lending decision, or effect obligations are missing or unknown.

### Success criteria

The cumulative demonstration succeeds when the system produces an underwriter-ready package containing verified evidence references, deterministic calculations, policy results, unresolved conditions, model recommendation, human/domain disposition, effect receipts, and joinable audit/trace IDs. The business-time target is illustrative. Tests assert safety and correctness; performance claims must state workload, hardware, model route, provider quotas, and measurement method.

## Cumulative architecture

```text
Loan officer / event
        | authenticated tenant + case request
        v
Run API and durable workflow
        | state, waits, retries, joins, cancellation, acceptance
        v
AgentRuntime adapter
        | OpenAI Agents SDK for bounded reasoning and tool-loop mechanics
        | optional direct OpenAI Python SDK adapter for the C01 baseline
        v
Context + knowledge + calculation + policy services
        | typed candidate facts, verified evidence, exact authorization
        v
Tool Gateway + approval + effect ledger
        | scoped credentials, idempotency, preconditions, receipts
        v
Synthetic document / verification / LOS connectors
        |
        +--> OpenTelemetry-compatible trace and MLflow diagnostics/evaluation
        +--> separate authoritative audit, approval, lending-decision, and effect evidence
```

The OpenAI SDKs own model-facing mechanics only. MLflow owns diagnostics and evaluation mechanics only. Custom Python and the selected durable runtime own platform contracts, workflow state, authority, calculations, effects, recovery, and tests.

## Course-to-book implementation crosswalk

The course has 14 lessons, while the supplied book has 28 chapters. The executable checkpoints follow book chapter numbers; this crosswalk keeps the code useful to readers following either sequence.

| Course lesson | Primary book checkpoints | Mortgage capability demonstrated |
| --- | --- | --- |
| 01 — Enterprise Agentic Systems | `C01` | Honest read-only prototype and explicit production gaps |
| 02 — Deterministic Shell, Agentic Core | `C02` | Typed proposals, deterministic calculations, validation, and no autonomous lending decision |
| 03 — Reference Architecture | `C04`, `C07` | Stable records, owners, stores, events, and a developer-facing package |
| 04 — OpenAI Agents SDK | `C03` | Provider-neutral `AgentRuntime` implemented with OpenAI Agents SDK |
| 05 — Run Lifecycle and Durable Execution | `C15` | Document wait, restart, replay, signal, cancellation, and reconciliation |
| 06 — Planning and Deterministic Execution | `C12` | Model-proposed mortgage plan compiled before scheduling |
| 07 — Multi-Agent Systems and Delegation | `C18`, `C19` | Bounded specialists, child grants, joins, MCP, and A2A gateways |
| 08 — Events, Failures, and Recovery | `C04`, `C15`, `C22` | Outbox/inbox, unknown effect, recovery, and operator action |
| 09 — Identity and Delegated Authorization | `C21` | Loan-officer subject, workload actor, exact case scope, last-hop credential |
| 10 — Context, Knowledge, and Memory | `C05`, `C06` | Governed policy, document provenance, context manifest, and safe memory |
| 11 — Tools, Effects, and Human Approval | `C02`, `C14`, `C22` | Tool façade, exact preview, approval binding, protected LOS effect |
| 12 — Security and Safety | `C20`, `C23` | Malicious-document containment, sandbox, egress, DLP, and privacy |
| 13 — APIs, Data Models, Scalability, and Deployment | `C04`, `C27`, `C28` | Stable APIs, release compatibility, cells, queues, capacity, and cost |
| 14 — Observability, Evaluation, and Governance | `C24`, `C25`, `C26` | MLflow trace/evaluation, release gates, fairness, and operating controls |

## Technology ownership and dependency policy

| Technology | Target use | Explicit boundary |
| --- | --- | --- |
| Python 3.11+ | Domain contracts, deterministic workflow model, adapters, fixtures, CLI, and tests | Replayable workflow code cannot read the clock, call I/O, or generate uncontrolled randomness |
| Pydantic 2 | Public/internal schemas and validation | A valid schema is not proof of truth, authorization, or acceptance |
| OpenAI Python SDK (`openai==3.13.0`) | Optional direct Responses API baseline and provider adapter | Does not own tools, workflow, policy, effects, approvals, or durable state |
| OpenAI Agents SDK (`openai-agents==0.22.2`) | `Agent`, `Runner`, function tools, structured output, local handoffs, limits, HITL state, and SDK tracing inside `AgentRuntime` | Does not own enterprise workflow truth, connector credentials, lending decisions, or audit |
| MLflow (`mlflow==3.15.2`) | Local/remote traces, experiments, datasets, scorers, comparisons, and evaluation evidence; its OpenAI integration also records Agents SDK spans when explicitly enabled | Not the approval store, policy source, effect ledger, LOS, or audit ledger |
| OpenTelemetry-compatible context | Cross-process trace propagation and semantic span envelope | Trace sampling or loss cannot erase required audit evidence |
| SQLite/in-memory stores | Deterministic local teaching implementation | Clearly labeled as test stores, not production persistence claims |
| Durable workflow abstraction | Pure reducer and activity contracts in required offline path | A production adapter may use Temporal, DBOS, Restate, or another engine after conformance tests |
| MCP/A2A adapters | Optional external tool/agent protocol demonstrations | Protocol success does not establish peer trust, business authorization, or artifact safety |
| Synthetic connectors | Document store, verification providers, notification service, and LOS | Never described as production security or regulatory certification |

### Naming correction

Use these exact names in prose, code, dependency files, and logs:

- **OpenAI Python SDK** — distribution/import family `openai`; used for direct API access.
- **OpenAI Agents SDK** — distribution `openai-agents`, imported as `agents`; used for the bounded agent runtime.
- **MLflow** — tracing and evaluation integration.

Do not use “OpenAI SDK” when the specific package matters, and do not introduce a fictional third dependency called “OpenAI Agentic SDK.”

### Reproducibility rules

- Pin `openai==3.13.0`, `openai-agents==0.22.2`, and `mlflow==3.15.2` for the Book v1.0.0 offline reproduction profile, then verify their transitive compatibility in CI. Do not describe the old `openai>=2.25.0` floor as the supported runtime baseline for this profile.
- Separate extras: `offline`, `openai`, `agents`, `mlflow`, `protocols`, and `all`.
- The mandatory test job uses the scripted model and synthetic connectors. Live OpenAI and remote MLflow jobs are opt-in and never the only evidence.
- Record Python, OS, package lock digest, model route, tool schema, prompt/Skill, policy, dataset, scorer, and workflow build in every release manifest.
- Never put an API key, access token, account number, reusable credential, raw protected attribute, or hidden chain-of-thought in source, fixtures, serialized SDK state, trace tags, or sample output.

## Target package layout

```text
README.md                      # business story, safety boundary, quickstart
pyproject.toml                 # compatibility ranges and optional extras
requirements.lock             # exact reproducible dependency resolution
mortgage_case/
  __init__.py
  __main__.py                  # python -m mortgage_case ...
  cli.py                       # --chapter, --scenario, --offline, --json
  stage_report.py              # visible before/added/after contract
  domain/
    __init__.py
    ids.py                     # typed IDs and canonical resource URIs
    money.py                   # Decimal money/ratio/rounding rules
    case.py                    # mortgage case and state contracts
    evidence.py                # candidate vs verified evidence
    decisions.py               # recommendation vs human/domain decision
    errors.py                  # typed safe errors
  fixtures/
    case_000184.json
    documents/                 # synthetic documents and malicious variants
    policies/                  # explicitly fictional, versioned training rules
    provider_responses/        # deterministic OpenAI/connector test responses
  stages/
    __init__.py
    c01_baseline.py
    c02_deterministic_shell.py
    ...
    c28_capacity.py
  platform/
    __init__.py
    runtime.py                 # provider-neutral AgentRuntime
    workflow.py                # replay-safe reducer and activity commands
    context.py
    knowledge.py
    planning.py
    delegation.py
    authorization.py
    tools.py
    action_authorization.py
    effects.py
    events.py
    security.py
    observability.py
    evaluation.py
    releases.py
  adapters/
    __init__.py
    scripted_model.py
    openai_responses.py
    openai_agents.py
    mlflow_tracking.py
    workflow_test_engine.py
    mcp_gateway.py
    a2a_gateway.py
    synthetic_los.py
    synthetic_verification.py
  docs/
    C01.md ... C28.md           # chapter delta, diagram, commands, outputs, limits

tests/mortgage_case/
  __init__.py
  unit/__init__.py
  contract/__init__.py
  workflow/__init__.py
  security/__init__.py
  evaluation/__init__.py
  integration_optional/__init__.py

config/mortgage_stages.json     # chapter, entry point, scenarios, tests, concepts
```

Paths beginning with `domain/`, `stages/`, `platform/`, `adapters/`, `fixtures/`, or `docs/` in checkpoint tables are relative to `mortgage_case/`; paths beginning with `tests/` or `config/` are repository-relative.

### Command convention

From the repository root, every landed checkpoint uses the same interface:

```bash
python -m mortgage_case --chapter 1 --scenario happy_path --offline
python -m mortgage_case --chapter 14 --scenario action_authorization_changed_case --offline --json
```

The CLI accepts integer chapter numbers, emits `StageReport.chapter` as zero-padded `C01`–`C28`, rejects an unregistered scenario, and defaults to offline mode. A live adapter requires both an explicit adapter flag and an environment opt-in; it can never be selected by a fixture or model output.

Earlier entry points must remain runnable. Shared modules can grow additively, but a later semantic change cannot alter an earlier checkpoint without an explicit compatibility test and documentation update.

## Reader-facing documentation contract

Every `Cxx` checkpoint must include:

1. **Case at this point:** facts available, state, owner, and unresolved question.
2. **Before:** the exact limitation inherited from the prior checkpoint.
3. **Added:** one primary capability and its authoritative owner.
4. **After:** the new state/records and what still remains intentionally unsafe or absent.
5. **Run it:** one offline command and one optional integration command where relevant.
6. **Expected output:** a redacted `StageReport` with stable IDs and a concise explanation.
7. **Failure demonstration:** at least one refusal, stale-state, duplicate, timeout, attack, or recovery scenario.
8. **Code tour:** entry point, contracts, adapters, authoritative stores, and test names.
9. **Production boundary:** what the teaching implementation does not prove.
10. **Next chapter:** the exact remaining limitation that motivates the next capability.

### Code quality rules

- Use complete runnable listings; no undefined tools, ellipses standing in for control logic, or imports that exist only in prose.
- Public classes/functions have concise docstrings covering **purpose**, **authority**, **side effects**, and **failure semantics** where applicable.
- Prefer domain types over `dict[str, Any]` at service boundaries.
- Use enums/literals for states and error codes; never branch on model prose.
- Use `Decimal` for money and ratios; define currency and rounding policy explicitly; serialize decimal values as canonical strings or documented minor units, never JSON floats.
- Use timezone-aware UTC `datetime` values and explicit domain `date` values; inject clock, ID factory, model, stores, connectors, and failure injector. Workflow reducers remain pure and never call `datetime.now()` directly.
- Canonical hashes use one documented serializer that fixes schema/version, Unicode normalization, field order, decimal/date rendering, absent-vs-null behavior, and excluded mutable fields.
- Distinguish candidate, verified, accepted, committed, and observed states in names.
- Errors expose stable safe codes. Raw provider/document payloads remain behind protected references.
- Comments explain architectural **why**; they should not paraphrase obvious syntax.
- Each example has type, unit, contract, and behavior tests proportional to its risk. Add property/invariant tests for decimal calculations, grant narrowing, canonical hashing, idempotency, event folding, and duplicate delivery.
- Unsafe anti-patterns live only in test fixtures and cannot be selected by the normal CLI.

## Stable contracts introduced across the progression

| Contract | First introduced | Key invariant |
| --- | --- | --- |
| `MortgageCase` / `CaseVersion` | `C01` | Synthetic marker and stable case ID are mandatory |
| `CaseSummaryCandidate` | `C01` | Cannot contain a final lending decision |
| `AgentProposal` / `WorkflowCommand` | `C02` | Model proposal requires deterministic mapping and validation |
| `CalculationResult` | `C02` | Formula/version/inputs/rounding are recorded and recomputable |
| `AgentStepRequest` / `AgentStepResult` | `C03` | No SDK type crosses the platform boundary |
| `RunManifest` / `PrincipalContext` / `CapabilityScope` / `Artifact` / `Event` | `C04` | Identity and scope are carried from the start, but scope is not an executable credential and protected writes remain disabled |
| `KnowledgeObject` / `Rule` | `C05` | Source, scope, effective interval, digest, and owner are required |
| `ContextManifest` / `MemoryRecord` | `C06` | Authorization precedes model exposure; prompt is a projection |
| `SkillManifest` / `SkillPackManifest` | `C08`–`C09` | Resolution is deterministic and does not grant authority |
| `PlanRevision` / `PlanNode` | `C12` | Model proposes; compiler validates and scheduler executes |
| `ApprovalRequest` / `ApprovalDecision` | `C14` | Exact operational proposal/evidence/policy/case version and expiry are bound; this is not credit approval |
| `WorkflowEvent` / `Checkpoint` / `WaitRegistration` | `C15` | Replay never repeats unrecorded I/O or an uncertain effect |
| `TaskEnvelope` / `OwnershipTransfer` | `C18` | One owner; child `CapabilityScope` is a strict subset; tasks remain synthetic/read-only until `C21` revalidates authority |
| `PrincipalChain` / `CapabilityEnvelope` | `C21` | Subject is preserved and each delegation narrows authority |
| `EffectRecord` / `EffectReceipt` | `C22` | One logical intent; unknown outcome blocks retry and completion |
| `TraceEnvelope` / `EvalDatasetVersion` | `C24`–`C25` | Diagnostics are privacy-safe and release evidence is versioned |
| `ReleaseBundle` / `PromotionDecision` | `C27` | Active runs remain pinned to compatible immutable behavior |
| `StageReport` | Every checkpoint | Shows chapter, scenario, before, added, after, evidence, failures, and limitations |

## Required scenario matrix

| Scenario ID | Introduced by | Expected result |
| --- | --- | --- |
| `happy_path` | `C01` | Underwriter-ready package after all later controls are present |
| `missing_income_document` | `C01` | Typed `NEEDS_INPUT`; no invented fact |
| `contradictory_employer` | `C05`/`C13` | Contradiction remains explicit; targeted evidence or intervention |
| `stale_credit_artifact` | `C05` | Policy/freshness block; no model override |
| `appraisal_delayed` | `C15` | Durable wait and authenticated resume |
| `employment_changed_during_wait` | `C15`/`C21` | Reauthorization and re-verification before continuing |
| `duplicate_document_event` | `C04`/`C15` | Inbox deduplication; one state transition |
| `los_timeout_after_commit` | `C22` | `UNKNOWN_EFFECT`, no blind retry, successful reconciliation or intervention |
| `malicious_document_instruction` | `C20`/`C23` | Untrusted text cannot change tools, policy, destination, or expose data |
| `cross_tenant_case_reference` | `C06`/`C21` | Denied before content materialization; security evidence recorded |
| `revoked_loan_officer` | `C21` | Resume/write denied after current entitlement check |
| `action_authorization_reuse_after_case_change` | `C14`/`C22` | Proposal hash or version mismatch requires a new approval |
| `evaluation_cohort_v1` | `C25` | Versioned synthetic multi-case holdout supports trajectory, reliability, and slice analysis |
| `fairness_slice_regression` | `C25` | Candidate release blocked under governed evaluation policy; result proves gate behavior, not real-world fairness |
| `provider_outage` | `C10`/`C28` | Bounded fallback or safe partial result; no control bypass |
| `incompatible_worker` | `C27` | Work is routed to compatible code or stopped; history is not rewritten |

The anchor fixture is used for the narrative and most fault demonstrations. `evaluation_cohort_v1` and capacity workloads are separate, immutable synthetic datasets with provenance, generation method, seed, intended use, prohibited use, and leakage checks. Their outcomes validate the implementation and release-gate mechanics only; they do not establish real-world model fairness, legal compliance, or lending performance.

## Current implementation evidence and limitations

| Evidence class | What the supplied material shows | What remains unproven |
| --- | --- | --- |
| Verified in supplied Markdown | 28 chapter headings, 54 syntactically parseable Python fences, OpenAI Agents SDK 0.22.2 baseline, MLflow 3.15.2 baseline | Runtime imports, package installation, network calls, end-to-end behavior, generated artifacts |
| Verified defect in supplied Markdown | Initial agent listing references write/email tools not defined in that listing; cumulative narrative is supplier onboarding | A runnable mortgage baseline and chapter-by-chapter mortgage progression |
| Corrected implementation baseline | `mortgage_case` package, `C01`–`C03`, offline scenarios, direct OpenAI Responses contract, OpenAI Agents SDK runtime, and MLflow Agent tracing/evaluation examples | Live provider calls, later checkpoint composition, and production tracking deployment remain unproven |
| Implemented foundation slice | `mortgage_case` package, `C01`–`C03`, offline scenarios, optional OpenAI/Agents SDK adapters | 19 focused mortgage tests and the registered example suite are validated locally on this branch; later checkpoint composition remains unproven |
| Implemented platform-contract slice | `mortgage_case/platform/enterprise.py`, 24 focused facades, and `tests/mortgage_case/unit/test_platform_extensions.py` cover deterministic contracts for events, context, plans, delegation, authorization, effects, security, tracing, evaluation, release, and capacity | 11 offline tests cover the slice; it is not yet wired into chapter stage entry points, `StageReport`, the CLI, or per-checkpoint generated evidence |
| Remaining full-checkpoint target | `C04`–`C28` chapter-integrated execution, durable workflow composition, registry entries, CLI scenarios, reader transitions, and release evidence | The platform-contract slice is partial evidence; complete checkpoint implementation remains to be created and reviewed |

## Progressive-hardening dependency rule

The book teaches some concepts after earlier chapters need their vocabulary. Avoid both circular dependencies and premature claims with these gates:

- `C04` introduces `PrincipalContext` and non-executable `CapabilityScope` so IDs and intended scope are present from the start. They are not credentials and cannot authorize protected work.
- `C14` proves proposal hashing, durable waiting, expiry, and decision binding with a synthetic reviewer. Full current-identity and entitlement enforcement is not claimed until `C21`.
- `C18` and `C19` demonstrate only synthetic/read-only child tasks and protocol calls. Their scope-intersection checks are re-run against the enforceable `CapabilityEnvelope` in `C21`.
- `C20` demonstrates containment with policy and credential façades but no reusable secret or production endpoint.
- `C21` upgrades identity, authorization, revocation, and last-hop credential exchange, then revalidates the `C14`, `C18`, and `C19` flows.
- `C22` is the first checkpoint permitted to execute a protected synthetic LOS mutation. No earlier normal stage can import or resolve a mutating connector.

Each pre-enforcement stage must label its control as a **contract/mechanics demonstration**, not a complete security or authorization implementation.

## Chapter-by-chapter implementation register

Each checkpoint has one primary teaching delta. Later chapters may compose earlier controls, but they may not skip or silently replace them.

### C01 — Chapter 1: What Turns an LLM Call into a Production System

| Field | Roadmap |
| --- | --- |
| Severity | **Blocker** |
| Learning goal | Start with an honest mortgage evidence-summary prototype and expose the gap between a model response and a production system. |
| Before | No executable mortgage case. The source prototype names tools that are not all defined in its first listing and can be read as if the agent owns writes. |
| Add for the mortgage case | Create the stable synthetic fixture, `MortgageCase`, `CaseSummaryCandidate`, a scripted offline model, and an optional direct OpenAI Python SDK Responses adapter. The baseline is read-only and reports its limitations. |
| Reader-visible walkthrough | Run `MORT-2026-000184`; summarize available documents, identify the absent second pay statement, and print actors, inputs, candidate output, unsupported claims, and next control needed. |
| Required failure or refusal | `missing_income_document` returns `NEEDS_INPUT`; the candidate cannot contain approve/deny/rate/adverse-action fields, and no write tool exists. |
| Implementation and technology | Custom Python + Pydantic; scripted model is mandatory; direct `openai` adapter is optional and must return the same schema. |
| Acceptance criteria | Fresh offline checkout runs one command; output is deterministic and redacted; all names resolve; tests prove the stage cannot claim a verified fact, committed effect, or lending decision. |
| Target files | `mortgage_case/stages/c01_baseline.py`, `mortgage_case/domain/case.py`, `mortgage_case/fixtures/case_000184.json`, `mortgage_case/adapters/scripted_model.py`, optional `mortgage_case/adapters/openai_responses.py`, `tests/mortgage_case/unit/test_c01.py` |

### C02 — Chapter 2: From Model Output to Safe Action

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Turn model output into typed proposals and keep calculation, state, policy, authorization, and acceptance deterministic. |
| Before | The baseline can summarize but offers no trustworthy contract for candidate facts, calculations, evidence requests, or workflow transitions. |
| Add for the mortgage case | Introduce `AgentProposal`, `ExtractedFactCandidate`, `CalculationResult`, `WorkflowCommand`, schema validation, fictional training rules, and a read-only Tool Gateway façade. A safe draft condition may be proposed but not sent or committed. |
| Reader-visible walkthrough | The model proposes a missing-document request and candidate income facts; deterministic code validates citations, calculates illustrative LTV/DTI with `Decimal`, checks case version, and emits the next workflow command. |
| Required failure or refusal | Reject an unsupported fact, float-based amount, stale case version, unknown tool, unauthorized case, or proposal containing a final lending decision. |
| Implementation and technology | Pydantic 2, `Decimal`, canonical JSON/hash helpers, custom deterministic validator/gateway; no live API required. |
| Acceptance criteria | Same inputs reproduce the same calculations and command; schema-valid but unauthorized/stale proposals are refused before dispatch; acceptance never depends on model confidence. |
| Target files | `mortgage_case/stages/c02_deterministic_shell.py`, `mortgage_case/domain/money.py`, `mortgage_case/domain/evidence.py`, `mortgage_case/platform/tools.py`, `tests/mortgage_case/unit/test_c02.py` |

### C03 — Chapter 3: Keep the Framework in Its Lane

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Place OpenAI Agents SDK behind a provider-neutral `AgentRuntime` while preserving platform ownership. |
| Before | The direct model adapter and deterministic shell are separate; no bounded tool loop translates a platform request into SDK objects and back. |
| Add for the mortgage case | Implement `AgentStepRequest/Result`, `OpenAIAgentsRuntime`, governed function-tool façades, structured output, external turn/tool/time limits, trace privacy defaults, and adapter conformance tests. The first implementation keeps `ScriptedRuntime` mandatory for offline execution and uses the class in `mortgage_case/adapters/openai_agents.py` only when the optional SDK path is enabled. |
| Reader-visible walkthrough | The workflow submits one evidence-review step; the SDK can call only `mortgage.case.read@1` and `mortgage.policy.read@1`; its result becomes a provider-neutral proposal consumed by `C02`. |
| Required failure or refusal | Tool allowlist escape, max-turn breach, malformed output, cancellation, provider error, and accidental serialization of credentials all fail with typed results. |
| Implementation and technology | OpenAI Agents SDK `0.22.2`; scripted SDK model for CI; optional provider-backed run; platform types remain independent of `agents` classes. |
| Acceptance criteria | Replacing the runtime with a test adapter changes no caller; SDK state is absent from canonical business/effect records; no tool can bypass the gateway. |
| Target files | `mortgage_case/stages/c03_agent_runtime.py`, `mortgage_case/platform/runtime.py`, `mortgage_case/adapters/openai_agents.py`, `tests/mortgage_case/contract/test_c03_runtime.py` |

### C04 — Chapter 4: The Architecture Around the Model

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Make the architecture executable through records, owners, stable APIs, events, and stores. |
| Before | One bounded step exists, but the case has no durable run identity, authoritative record map, artifacts, status projection, or outbox. |
| Add for the mortgage case | Create `RunManifest`, minimal `PrincipalContext`, non-executable `CapabilityScope`, `Run`, `Artifact`, `WorkflowExecution`, `Event`, outbox/inbox records, an in-memory composition root, and idempotent start/status/signal/cancel façades. Register a hard write lock for all pre-`C22` normal stages. |
| Reader-visible walkthrough | Start the mortgage run with an idempotency key; write the manifest and first event; store document references as immutable artifacts; publish a deduplicated status event. |
| Required failure or refusal | Duplicate start/signal, payload-hash conflict, wrong tenant, stale command version, and outbox redelivery are demonstrated. |
| Implementation and technology | Custom Python/Pydantic, SQLite or in-memory teaching stores, CloudEvents-shaped envelopes; no SDK type appears in public contracts. |
| Acceptance criteria | Every record has one writer; state and event commit atomically in the test store; projections are rebuildable; duplicate delivery produces one logical transition; identity/scope travel with the run, but no mutating connector is discoverable or callable. |
| Target files | `stages/c04_reference_architecture.py`, `platform/events.py`, `platform/workflow.py`, `tests/workflow/test_c04.py` |

### C05 — Chapter 5: Give Knowledge an Owner

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Represent mortgage policy and domain knowledge as governed, versioned artifacts rather than an unscoped corpus. |
| Before | The agent can read text but cannot distinguish a policy source, fictional rule, revision, jurisdiction, effective interval, or enforceable result. |
| Add for the mortgage case | Create fictional training-policy artifacts, ontology terms, source spans, digests, owners, effective dates, contradiction handling, and a deterministic rule projection used by the shell. |
| Reader-visible walkthrough | Retrieve the rule governing required income evidence; cite it in the explanation; independently enforce freshness and evidence requirements before the case can advance. |
| Required failure or refusal | Contradictory employer data, stale credit artifact, unknown required fact, out-of-scope rule, and changed policy revision fail closed. |
| Implementation and technology | Typed knowledge/rule graph and provenance store; retrieval adapter optional; model may identify candidate applicability but never certify policy truth. |
| Acceptance criteria | Every rule result points to source revision and span; a policy change invalidates affected recommendations/approvals; no prompt text can override an enforceable rule. |
| Target files | `stages/c05_knowledge.py`, `platform/knowledge.py`, `fixtures/policies/`, `tests/unit/test_c05.py` |

### C06 — Chapter 6: Build Context Without Losing the Plot

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Build a reproducible, authorized context projection and separate it from workflow state, knowledge, working memory, and long-term memory. |
| Before | The runtime lacks a manifest showing which case fields/documents/policies were authorized, redacted, ordered, and shown to the model. |
| Add for the mortgage case | Implement `ContextManifest`, segment trust labels, ACL decisions, source revisions, redactions, token budgets, digest, run-scoped working memory, and governed memory policy. |
| Reader-visible walkthrough | Assemble only the permitted fields and document excerpts for one income-review step; pass references to the SDK; reproduce the exact manifest after replay. |
| Required failure or refusal | Cross-tenant reference, unauthorized field, stale snapshot, retrieved instruction, unsupported durable memory, and deleted-source cache hit are blocked. |
| Implementation and technology | Custom context builder and memory test store; optional hybrid retrieval adapter; no raw SSN/account number enters model context or normal telemetry. |
| Acceptance criteria | Pinned inputs produce the same manifest digest; authorization occurs before bytes are materialized; memory cannot become instruction or authority; deletion invalidates derivatives. |
| Target files | `stages/c06_context.py`, `platform/context.py`, `platform/memory.py`, `tests/security/test_c06.py` |

### C07 — Chapter 7: Build the Paved Road for Agent Teams

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Give readers one documented golden path for building and running the cumulative case. |
| Before | Modules exist but there is no stable CLI, stage registry, release manifest, local profile, or conformance workflow. |
| Add for the mortgage case | Create the package CLI, `mortgage_stages.json`, build/runtime manifest, offline/live profiles, compatibility checks, generated example index, and actionable developer errors. |
| Reader-visible walkthrough | Run `python -m mortgage_case --chapter 7 --scenario happy_path --offline --json`; inspect exact versions, stage delta, records, and limitations. |
| Required failure or refusal | Missing fixture, incompatible schema, unpinned adapter, accidental network request in offline mode, and unknown stage fail before execution. |
| Implementation and technology | Custom Python CLI and manifest loader; SDK adapters selected by configuration; lock digest recorded; no secret-bearing `.env` sample. |
| Acceptance criteria | One command runs each landed checkpoint; offline mode is network-deny tested; manifests are complete and deterministic; help text explains the business case. |
| Target files | `cli.py`, `__main__.py`, `config/mortgage_stages.json`, `README.md`, `tests/contract/test_c07_cli.py` |

### C08 — Chapter 8: Package Capabilities as Versioned Skills

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Learning goal | Package reusable mortgage capabilities as immutable, policy-resolved Skills. |
| Before | Instructions and tools are assembled manually; the run cannot prove which reusable capability version it used. |
| Add for the mortgage case | Define Skills such as `mortgage.document.extract`, `mortgage.income.reconcile`, `mortgage.policy.explain`, and `mortgage.review.prepare`, with owners, schemas, tools, policy, tests, eval refs, lifecycle, and digests. |
| Reader-visible walkthrough | Resolve one exact income-reconciliation Skill for tenant, purpose, region, data class, and risk; bind its version/digest into the run manifest. |
| Required failure or refusal | Revoked, incompatible, unevaluated, wrong-region, or overly privileged Skill versions are not resolved for new runs. |
| Implementation and technology | Custom Skill registry and semantic-version resolver; Agents SDK is only the execution adapter for the resolved contract. |
| Acceptance criteria | Resolution is deterministic and explainable; discovery grants nothing; only resolved eligible tools/knowledge reach the runtime; replay policy is explicit. |
| Target files | `stages/c08_skills.py`, `platform/skills.py`, `fixtures/skills/`, `tests/contract/test_c08.py` |

### C09 — Chapter 9: From Skills to a Domain Platform

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Compose compatible Skills and shared controls into one mortgage pre-underwriting domain pack. |
| Before | Individual Skills resolve, but a reader cannot install one coherent, evaluated domain experience. |
| Add for the mortgage case | Create `mortgage-preunderwriting@1.x` with document, income, asset, property, policy-explanation, condition-draft, and review-package Skills plus workflow, policy, evaluation, dashboard, and runbook references. |
| Reader-visible walkthrough | Install and resolve the pack; show which parts are domain-owned versus platform-shared; store exact pack version/digest in the run. |
| Required failure or refusal | Skill/policy/workflow/eval incompatibility, revoked dependency, duplicate pack version, or unsupported region prevents activation. |
| Implementation and technology | Custom immutable pack manifest/resolver; MLflow evaluation reference is metadata until `C25`. |
| Acceptance criteria | The pack is internally compatible, active, and fully pinned; installation does not authorize a case; active-run and replay behavior are documented. |
| Target files | `stages/c09_skill_pack.py`, `fixtures/skill_packs/`, `tests/contract/test_c09.py` |

### C10 — Chapter 10: ReAct Without the Runaway Loop

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Learning goal | Use a bounded loop only where the next evidence need depends on the previous observation. |
| Before | The workflow can make one evidence step but cannot adaptively inspect a contradiction without a new hard-coded path. |
| Add for the mortgage case | Add a read-only evidence ReAct controller with external turn, tool, token, time, cost, and repeated-observation limits. All calls use the existing context and Tool Gateway path. |
| Reader-visible walkthrough | Investigate the employer mismatch by reading the application, then the authorized pay statement, then stop with a cited request for verification. |
| Required failure or refusal | Repeated/empty observation, provider outage, budget exhaustion, unapproved tool, or attempt to write terminates as `NEEDS_INPUT` or `INTERVENTION_REQUIRED`. |
| Implementation and technology | OpenAI Agents SDK loop or custom controller behind `AgentRuntime`; platform-owned budget and no-progress detector. |
| Acceptance criteria | Limits are enforced outside prompts; every observation is authorized and artifact-linked; no write or final decision capability is exposed. |
| Target files | `stages/c10_react.py`, `platform/react.py`, `tests/workflow/test_c10.py` |

### C11 — Chapter 11: Route the Work—and Transfer Ownership

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Route mortgage tasks by explicit eligibility and distinguish local specialization from durable ownership transfer. |
| Before | One evidence agent handles every request, even when document, income, asset, property, or policy boundaries differ. |
| Add for the mortgage case | Define route taxonomy, deterministic eligibility/fallback, local Agents SDK specialist handoffs, `RouteDecision`, and `OwnershipTransfer` semantics. |
| Reader-visible walkthrough | Route the employer contradiction to income review and an appraisal question to property review; parent retains ownership for local specialists. |
| Required failure or refusal | Ambiguous/unsupported route, specialist tool escape, stale owner, and cancellation after attempted handoff are explicit. |
| Implementation and technology | Custom router/ownership records; Agents SDK local handoffs only when interaction ownership semantics are clear. |
| Acceptance criteria | Every route has one owner, reason, eligible capability set, fallback, and trace event; prompt text cannot select an ineligible specialist. |
| Target files | `stages/c11_routing.py`, `platform/routing.py`, `tests/workflow/test_c11.py` |

### C12 — Chapter 12: Plans Are Proposals Until the System Compiles Them

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Treat the mortgage plan as typed data compiled against authority, evidence, policy, budgets, and dependencies. |
| Before | Adaptive work is a sequence of agent choices with no inspectable DAG, validation, reservation, or revision rules. |
| Add for the mortgage case | Create mortgage `PlanIR`: collect missing evidence, verify employment/assets/property, run deterministic calculations, resolve contradictions, prepare human review, and record human-authorized effects. |
| Reader-visible walkthrough | The model proposes a plan for `MORT-2026-000184`; the compiler rejects illegal nodes, binds exact capabilities, computes a digest, and schedules only ready nodes. |
| Required failure or refusal | Cycle, unknown capability, protected decision node, excessive cost/fan-out, missing prerequisite, or revision that replays a committed effect is rejected. |
| Implementation and technology | Pydantic Plan IR and pure compiler; SDK may propose candidate nodes but never schedules them. |
| Acceptance criteria | Compiled order and digest are deterministic; completed effects/artifacts are frozen across revisions; conditional approval/effect nodes remain blocked until prerequisites hold. |
| Target files | `stages/c12_planning.py`, `platform/planning.py`, `tests/unit/test_c12.py` |

### C13 — Chapter 13: Use Critique to Improve, Not to Self-Approve

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Use bounded reflection for targeted revision and an independent evaluator for evidence-package acceptance. |
| Before | A coherent recommendation can overlook the employer contradiction or overstate confidence. |
| Add for the mortgage case | Separate candidate, critique, revision, evaluation, and accepted artifact; add deterministic checks for required evidence/citations/calculations and a bounded optional model evaluator for explanation quality. |
| Reader-visible walkthrough | The first recommendation misses the contradiction; the evaluator identifies the exact gap; one revision asks for verification and retains both candidate versions. |
| Required failure or refusal | Self-approval, evaluator tool access, policy modification, unsupported certainty, or revision-budget exhaustion is refused or escalated. |
| Implementation and technology | Custom deterministic evaluators; optional Agents SDK evaluator; MLflow dataset linkage deferred to `C25`. |
| Acceptance criteria | Reflection cannot broaden authority or erase prior output; accepted result records evaluator/rule versions and evidence; hard checks outrank model score. |
| Target files | `stages/c13_reflection.py`, `platform/evaluation_contracts.py`, `tests/evaluation/test_c13.py` |

### C14 — Chapter 14: Put People Where Judgment Matters

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Persist exact proposal-bound approval and keep it distinct from the final lending decision. |
| Before | The system can prepare a recommendation but cannot safely ask a human to authorize a condition request or readiness transition. |
| Add for the mortgage case | Create `ApprovalRequest`, immutable evidence snapshot, proposal hash, synthetic eligible-reviewer policy, expiry, allowed responses, decision event, and resume lease. Full current entitlement enforcement is intentionally deferred to `C21`. |
| Reader-visible walkthrough | Present the exact proposed condition-send or `mark_ready_for_underwriter` operation, source evidence, calculations, policy version, case version, uncertainty, and before/after preview. The interface says “Authorize this operation,” never “Approve the mortgage.” |
| Required failure or refusal | Changed case/evidence/policy/arguments, expired request, ineligible/self reviewer, replayed decision, or reused approval after mutation blocks resume. |
| Implementation and technology | Custom Approval Service/signature test double and durable wait; Agents SDK HITL state may pause local tools but is not the enterprise approval record or a lending decision. |
| Acceptance criteria | The authorized proposal hash and current state must match before resume; rejection/needs-evidence/expiry are durable dispositions; the normal stage still has no protected connector, and no final loan decision is delegated to the model. |
| Target files | `stages/c14_human_review.py`, `platform/action_authorization.py`, `tests/workflow/test_c14.py` |

### C15 — Chapter 15: Keep Work Alive Across Time and Failure

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Survive document waits, worker failure, deployment, cancellation, and uncertain effects through replay-safe execution. |
| Before | The case cannot wait days for an appraisal or employment response without relying on process memory. |
| Add for the mortgage case | Add pure event reducer, recorded activities, wait registration, fake clock, authenticated signals, inbox deduplication, checkpoints, worker restart, version pin, cancellation, and reconciliation states. |
| Reader-visible walkthrough | Pause for the appraisal, terminate the worker, start a compatible worker, receive the document signal, revalidate employment/authority, and continue without repeating completed work. |
| Required failure or refusal | Duplicate/early signal, stale signal schema, crash after activity result but before acknowledgment, cancellation during a simulated effect boundary, or incompatible worker goes to safe recovery. The protected LOS write remains disabled until `C22`. |
| Implementation and technology | Mandatory custom deterministic test engine; optional Temporal/DBOS/Restate adapter later under the same contracts. |
| Acceptance criteria | Replay reproduces state/commands; no I/O occurs during replay; unknown effect blocks completion; active runs remain pinned; waits consume no worker. |
| Target files | `stages/c15_durable.py`, `platform/workflow.py`, `adapters/workflow_test_engine.py`, `tests/workflow/test_c15.py` |

### C16 — Chapter 16: Patterns for Real Enterprise Work

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Learning goal | Show why each pattern is selected for the mortgage case and preserve a simpler baseline. |
| Before | Readers see implemented mechanisms but not the decision criteria that justified them. |
| Add for the mortgage case | Create an executable pattern decision registry: structured call for extraction, deterministic workflow for known steps, bounded ReAct for evidence uncertainty, Plan IR for adaptive decomposition, approval for protected changes, and durable tasks only for real ownership boundaries. |
| Reader-visible walkthrough | Print the chosen pattern, rejected alternatives, owner, risk, expected value, added failure modes, and test for each mortgage stage. |
| Required failure or refusal | A request to use peer swarm, unbounded loop, or dynamic planning for a deterministic calculation is rejected by the decision policy. |
| Implementation and technology | Documentation-backed metadata and tests; no new framework layer. |
| Acceptance criteria | Every pattern has a concrete mortgage problem, simpler alternative, trade-off, authoritative owner, and regression test. |
| Target files | `stages/c16_patterns.py`, `platform/pattern_choices.py`, `tests/unit/test_c16.py` |

### C17 — Chapter 17: The Shapes That Fail in Production

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Turn unsafe mortgage designs into executable negative tests. |
| Before | Anti-patterns exist as prose, so a future refactor could accidentally reintroduce them. |
| Add for the mortgage case | Add test-only unsafe examples: autonomous approve/deny output, direct broad LOS client, hidden protected attribute, ambient service credential, layered retry after timeout, unscoped boolean action approval, shared scratchpad, and unbounded self-reflection. |
| Reader-visible walkthrough | Run the anti-pattern suite and show which deterministic boundary refuses each exploit/failure. |
| Required failure or refusal | The unsafe module is never importable by the normal stage registry; removing a guard causes a named regression test to fail. |
| Implementation and technology | Custom failure fixtures and policy tests; no real credential or external endpoint. |
| Acceptance criteria | Each anti-pattern maps to a safe replacement checkpoint; CI proves the platform refuses it; examples cannot accidentally execute production-like writes. |
| Target files | `stages/c17_anti_patterns.py`, `tests/security/test_c17_anti_patterns.py` |

### C18 — Chapter 18: Coordinate Specialists Without Losing Control

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Use durable child tasks only for mortgage subtasks with distinct ownership, tools, data, or scaling. |
| Before | Local specialists exist, but long-running income, asset, property, and document checks have no durable task ownership or join contract. |
| Add for the mortgage case | Implement `TaskEnvelope`, narrowed read-only child `CapabilityScope`, task store, worker acceptance, immutable result artifacts, all/quorum/fallback join, deadlines, cancellation, and conflict handling. Full enforceable child grants arrive in `C21`. |
| Reader-visible walkthrough | Fan out income, asset, and property verification; accept only schema/provenance-valid artifacts; join them into the underwriter package. |
| Required failure or refusal | Duplicate completion, child scope expansion, straggler, conflicting fact, canceled parent, or partial result follows an explicit policy. |
| Implementation and technology | Custom durable task scheduler/store; optional Agents SDK agents inside each bounded child step. |
| Acceptance criteria | One current owner per task; child scope is a strict intersection; join waits for its declared condition; conflicts become typed intervention; no child has a write tool or production credential. |
| Target files | `stages/c18_multi_agent.py`, `platform/delegation.py`, `tests/workflow/test_c18.py` |

### C19 — Chapter 19: Crossing the Boundary: MCP, A2A, and Local Control

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Demonstrate protocol interoperability without confusing it with enterprise trust or authorization. |
| Before | Child tasks use local synthetic services; remote tool/agent boundaries, peer identity, and artifact adoption are absent. |
| Add for the mortgage case | Add a read-only synthetic verification MCP server and synthetic appraisal-partner A2A peer behind local gateways with pinned metadata, peer policy, quotas, downscoped non-executable scopes, callback deduplication, artifact scanning, and local state mapping. |
| Reader-visible walkthrough | Resolve the allowed endpoint, invoke a read-only verification tool, receive a remote appraisal artifact, validate/adopt it, and link the child task. |
| Required failure or refusal | Changed server/card digest, wrong audience, untrusted peer, invalid schema, malicious artifact, token passthrough, or ambiguous cancellation is denied/recorded. |
| Implementation and technology | Custom protocol façades and fake transports; live libraries/endpoints are optional; registry metadata never decides business authorization. |
| Acceptance criteria | No upstream token or live connector credential exists in this checkpoint; all remote artifacts have local digest/classification/adoption decisions; local effect and acceptance rules remain authoritative. |
| Target files | `stages/c19_protocols.py`, `adapters/mcp_gateway.py`, `adapters/a2a_gateway.py`, `tests/contract/test_c19.py` |

### C20 — Chapter 20: Security Starts Beyond the Prompt

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Contain a manipulated model through layered controls rather than relying on prompt refusal. |
| Before | The runtime labels retrieved data but lacks a full attack path and independent containment evidence. |
| Add for the mortgage case | Create a malicious synthetic appraisal/document with an instruction to disclose bank data, plus ingestion scan, trust labels, minimal context, capability confinement, schema validation, policy, egress denial, DLP, incident record, and kill switch. |
| Reader-visible walkthrough | Run the attack with detector both enabled and intentionally bypassed; show that unauthorized data, credentials, destinations, and effects remain unreachable. |
| Required failure or refusal | Direct/indirect injection, tool-output injection, memory poisoning, recursive delegation, and cost attack are blocked or contained. |
| Implementation and technology | Agents SDK guardrail as one detector; custom deterministic policy/egress/DLP/incident test doubles; no real exfiltration. |
| Acceptance criteria | Security holds even when the model follows malicious text; legitimate evidence still flows; incident evidence excludes raw sensitive content. |
| Target files | `stages/c20_security.py`, `platform/security.py`, `fixtures/documents/malicious_*`, `tests/security/test_c20.py` |

### C21 — Chapter 21: Carry Identity and Narrow Authority

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Preserve loan-officer subject and workload actor, authorize the exact case/action/purpose, and issue credentials only at the connector hop. |
| Before | `PrincipalContext` and non-executable scopes have traveled with the run since `C04`, and `C14`/`C18`/`C19` demonstrated mechanics, but there is no enforceable principal chain, current entitlement check, child-grant proof, revocation, or credential lease. |
| Add for the mortgage case | Upgrade `PrincipalContext`/`CapabilityScope` into enforceable `PrincipalChain`/`CapabilityEnvelope`; implement ABAC/PDP decisions, grant derivation, revalidation, revocation, entitlement freshness, and fake short-lived audience-bound credential exchange. Re-run the `C14`, `C18`, and `C19` contract tests under current identity. |
| Reader-visible walkthrough | Carry subject, actor, tenant, purpose, region, risk, case resource, and action from admission through child task to LOS connector. |
| Required failure or refusal | Cross-case/tenant access, changed subject, broader child scope, wrong purpose/audience/region, expired grant, or revoked loan officer is denied before data/effect. |
| Implementation and technology | Custom policy and STS doubles; optional OAuth token-exchange adapter only in integration tests; no bearer token reaches model or serialized state. |
| Acceptance criteria | Child authority only narrows action/resource/data/purpose/risk/time/cost/depth; exact invocation is reauthorized; deny/invalidation wins over cache; all earlier approval, child-task, and protocol flows pass the upgraded checks. |
| Target files | `stages/c21_identity.py`, `platform/authorization.py`, `tests/security/test_c21.py` |

### C22 — Chapter 22: Make Effects Safe to Retry

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Prove one protected mortgage effect can receive approval, commit once, be verified, and reconcile uncertainty. |
| Before | Approval, durable workflow, and enforceable identity exist, but no end-to-end mortgage mutation composes gateway, case version, effect ledger, connector, receipt, and acceptance. |
| Add for the mortgage case | Make `loan_case.mark_ready_for_underwriter@1` the first canonical protected effect. Use logical key `{tenant}:case:{case_id}:mark_ready:v{target_case_version}`; hash schema, action, canonical resource, arguments, and expected version; record policy decision, `ApprovalDecision`, downstream request ID, receipt, observed projection, and reconciliation state. |
| Reader-visible walkthrough | Submit the exact human-authorized readiness transition to the synthetic LOS and verify the case projection. Recording the later human lending decision is a separate domain-owned effect and never a model action. |
| Required failure or refusal | Timeout after commit becomes `UNKNOWN_EFFECT`; replay, changed intent under the same logical key, stale case, approval mismatch, or unauthorized caller never duplicates or bypasses the effect. |
| Implementation and technology | Custom Tool Gateway/effect ledger plus synthetic LOS connector and failure injector; Agents SDK only proposes. |
| Acceptance criteria | Happy path produces one receipt and one LOS call; replay returns the receipt; a reused key with a different intent is a conflict; reconciliation proves committed/absent/intervention; completion waits for the verified effect. |
| Target files | `stages/c22_effects.py`, `platform/effects.py`, `adapters/synthetic_los.py`, `tests/workflow/test_c22.py` |

### C23 — Chapter 23: Contain a Manipulated Model

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Protect mortgage documents and helper execution with enforceable sandbox, egress, DLP, retention, and deletion contracts. |
| Before | Security checks exist, but document/OCR/code helpers have no executable resource, filesystem, network, or lifecycle boundary. |
| Add for the mortgage case | Add sandbox profile/lease façade, read-only input mounts, ephemeral output, CPU/memory/time/process limits, default-deny egress, canonical destinations, secret lease boundary, DLP/redaction, retention, deletion, and legal-hold metadata. |
| Reader-visible walkthrough | Process the synthetic appraisal and bank statement; publish only redacted structured evidence; deny the malicious external URL and prevent raw account data from leaving. |
| Required failure or refusal | Runaway helper, archive bomb, private/metadata address, redirect, secret request, oversized output, wrong classification/region, or deletion resurrection is blocked. |
| Implementation and technology | Deterministic control-contract doubles in mandatory tests; an isolated container/proxy integration may be added but cannot justify production claims by itself. |
| Acceptance criteria | No unauthorized host/data/secret is reachable; resources are bounded; deletion propagates through indexes/memory/artifacts; audit stores references, not secrets. |
| Target files | `stages/c23_containment.py`, `platform/sandbox.py`, `platform/privacy.py`, `tests/security/test_c23.py` |

### C24 — Chapter 24: Follow One Run from Request to Receipt

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Link the complete mortgage trajectory while keeping PII and authoritative audit evidence out of ordinary telemetry. |
| Before | Stage reports and local logs exist, but there is no causal trace across workflow, SDK, retrieval, policy, tasks, approvals, effects, and connectors. |
| Add for the mortgage case | Add OpenTelemetry-compatible trace context and MLflow 3.15.2 adapter with opaque/pseudonymous run/node/task/context/policy/approval/effect/release IDs, safe span attributes, asynchronous links, completeness checks, and a protected lookup map outside telemetry. |
| Reader-visible walkthrough | Trace one appraisal wait and readiness effect; identify queue, model, tool, and human dwell time without exposing full prompts/documents/SSN/account data. |
| Required failure or refusal | Broken propagation, dropped required span, raw PII tag, secret-like value, excessive cardinality, or trace-store outage triggers a typed signal; protected audit remains complete. |
| Implementation and technology | MLflow tracing with local SQLite-compatible test profile where supported; explicit platform spans; autologging configured so sensitive capture is disabled/default-safe. |
| Acceptance criteria | Trace joins all opaque IDs and shows unknown-effect/wait states; privacy scanner finds no applicant name, address, raw document text, protected attribute, credential, or hidden reasoning; audit/effect/decision records remain separate and authoritative. |
| Target files | `stages/c24_tracing.py`, `platform/observability.py`, `adapters/mlflow_tracking.py`, `tests/contract/test_c24.py` |

### C25 — Chapter 25: Improve the System Without Losing Control

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Convert failures into immutable evaluation cases and block unsafe candidate releases with executable gates. |
| Before | Traces exist, but there is no mortgage dataset, scorer contract, baseline comparison, fairness review, or promotion decision. |
| Add for the mortgage case | Create `evaluation_cohort_v1` as a versioned synthetic multi-case holdout with provenance/leakage review; add deterministic outcome/trajectory/security/effect graders, calibrated optional judges, repeated-run variance, approved fairness/proxy slices, minimum sample rules, uncertainty/confidence intervals, baseline deltas, and a custom release gate. |
| Reader-visible walkthrough | Evaluate a candidate that writes clearer summaries but misses an authorization check or regresses on a sufficiently supported governed slice; reject it despite a better average text score, and report inconclusive slices instead of forcing a claim. |
| Required failure or refusal | Unauthorized tool path, unsupported adverse-action explanation, missing citation, protected-feature use, unknown effect, dataset leakage, high repeated-run variance, or supported slice regression is a hard failure; underpowered slices are explicitly inconclusive. |
| Implementation and technology | MLflow datasets/traces/scorers plus custom deterministic gate; optional OpenAI judge is versioned, blinded, calibrated, and never sole authority. |
| Acceptance criteria | Scorers are actually invoked; cohort/candidate/baseline/rubric/judge/statistical-policy versions are recorded; holdout leakage is checked; failures become curated cases only after de-identification and approval; synthetic results are not presented as real-world fairness evidence; runtime cannot self-promote. |
| Target files | `stages/c25_evaluation.py`, `platform/evaluation.py`, `fixtures/evaluation/`, `tests/evaluation/test_c25.py` |

### C26 — Chapter 26: Make Governance an Operating System

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Assign accountable owners and evidence to a high-impact mortgage use case without claiming legal compliance. |
| Before | Evaluation gates exist, but the case lacks a governed use-case record, model-risk controls, exception lifecycle, review cadence, recourse, and incident ownership. |
| Add for the mortgage case | Create governance manifest with intended/prohibited uses, owners, risk tier, data map, human oversight, fairness review, model/vendor inventory, control evidence, exception expiry, incident route, recourse/contact path, and review dates. |
| Reader-visible walkthrough | Open the evidence package for a blocked/stale/unknown case and show who owns policy, model, security, effect recovery, human decision, and release approval. |
| Required failure or refusal | Expired waiver, missing owner, open exception used as authority, unsupported legal claim, or absent human-review/recourse metadata blocks release. |
| Implementation and technology | Custom governance records and validators; MLflow/trace links are evidence pointers only. |
| Acceptance criteria | Every material decision/control has owner, policy, evidence, escalation, and expiry; the documentation explicitly disclaims legal/regulatory certification. |
| Target files | `stages/c26_governance.py`, `platform/governance.py`, `tests/contract/test_c26.py` |

### C27 — Chapter 27: Release Without Breaking Work in Flight

| Field | Roadmap |
| --- | --- |
| Severity | **Major** |
| Learning goal | Release immutable compatible bundles, canary new starts, and preserve active mortgage histories. |
| Before | The case records versions but has no signed bundle, exact dependency lock, compatibility router, rollout state, rollback, migration, or recovery rehearsal. |
| Add for the mortgage case | Package agent/Skill/pack/workflow/policy/model/tool/schema/scorer/adapter/runtime versions and digests; add worker compatibility, canary assignment, active-run pin, rollback, kill switch, replay tests, and recovery evidence. |
| Reader-visible walkthrough | Canary a changed document schema for new runs while `MORT-2026-000184` resumes on compatible code; roll back new assignment without rewriting history. |
| Required failure or refusal | Incompatible worker, missing artifact/signature, mutable alias drift, failed migration, region loss during unknown effect, or rollback without old capacity is refused/contained. |
| Implementation and technology | Custom release/compatibility code and CI; exact lock digest records OpenAI Agents SDK/MLflow/OpenAI SDK resolution. |
| Acceptance criteria | Bundle is immutable and complete; active runs do not change unexpectedly; rollback changes assignment only; recovery fences writers and reconciles effects before resume. |
| Target files | `stages/c27_release.py`, `platform/releases.py`, `tests/workflow/test_c27.py`, CI/release manifests |

### C28 — Chapter 28: Make Performance a Business Decision

| Field | Roadmap |
| --- | --- |
| Severity | **Moderate** |
| Learning goal | Optimize cost and latency per verified underwriter-ready case without weakening safety, fairness, or human oversight. |
| Before | The anchor case can run safely, but one case cannot establish workload behavior, queueing, retry amplification, provider limits, human dwell, or tenant fairness. |
| Add for the mortgage case | Build a versioned synthetic workload from the anchor plus controlled cohort variants; create deterministic simulator, resource permits, queue/admission model, model/tool/human cost events, repeated-run reliability, deadline/fairness metrics, safe degradation policy, and baseline comparison. |
| Reader-visible walkthrough | Replay routine, missing-document, attack, provider-outage, and threefold-spike cohort workloads; report sample size, p50/p95, cost per verified package, human-review burden, unknown-effect backlog, deadline misses, and uncertainty where estimated. |
| Required failure or refusal | Provider outage, quota exhaustion, hot tenant, approval backlog, retry storm, or proposed degradation that bypasses a control results in backpressure or a safe partial state. |
| Implementation and technology | Custom deterministic simulator and metrics; MLflow may store experiment results but does not define acceptance. |
| Acceptance criteria | Metrics use the verified workflow-completion denominator, state assumptions and cohort generation method, show distributions/slices/uncertainty, preserve tenant/risk fairness, and never degrade authorization/approval/effect/privacy controls. |
| Target files | `stages/c28_capacity.py`, `platform/capacity.py`, `platform/simulation.py`, `tests/evaluation/test_c28.py` |

## Source and navigation changes required during implementation

The cumulative code and the teaching narrative must tell the same story. When each checkpoint lands:

| Surface | Required change |
| --- | --- |
| Book chapter source | Add the chapter’s mortgage checkpoint and label retained supplier material as a short contrast; preserve one canonical mortgage transition without silently deleting instructional content. |
| 14-lesson course | Update the running-example sections, proposal JSON, diagrams, and practical code so mortgage terms and safety boundaries are consistent. |
| Appendix H / companion guide | Rename the package map to `mortgage_case`, list actual files/tests, and report test counts generated from CI rather than hand-maintained claims. |
| Example registry | Add `checkpoint`, `book_chapter`, `course_lesson`, `scenario`, `entry_point`, `tests`, `offline`, and `optional_dependencies`; validate uniqueness and file existence. |
| Example README | Add the `C01`–`C28` progression, quickstart, expected output, synthetic-data warning, and optional integration profiles. |
| Diagrams and generated outputs | Rebuild from canonical source; do not hand-edit generated Markdown, DOCX, LaTeX, images, manifests, or checksums. |
| References | Keep vendor/version claims scoped to the supplied baseline; re-verify release/API claims before a new edition. |

Do not leave mixed names such as supplier IDs in mortgage code, `northstar` imports in the new package, or a `supplier.create` tool in an approval/effect example. A migration check should scan source, examples, tests, diagrams, and outputs for stale primary-case terminology while allowing explicitly marked contrast examples.

## Implementation order and review boundaries

Use one chapter-aligned change set per checkpoint until the foundational package is stable. The code may be reviewed in grouped pull requests, but each `Cxx` must have its own registry entry, stage report, tests, and reader transition.

| Sequence | Checkpoints | Outcome |
| --- | --- | --- |
| Foundation | `C01`–`C03` | Runnable mortgage baseline, deterministic shell, OpenAI Agents SDK adapter |
| Platform core | `C04`–`C07` | Records, events, knowledge, context, package, CLI, manifests; offline contract doubles are present, chapter entry-point integration remains |
| Reusable capability | `C08`–`C09` | Skills and mortgage domain pack; offline registry contracts are present, chapter integration remains |
| Reasoning patterns | `C10`–`C13` | Bounded ReAct, routing, planning, reflection/evaluation |
| Human and durable control | `C14`–`C15` | Proposal-bound review, waits, replay, cancellation, recovery |
| Decision discipline | `C16`–`C17` | Pattern rationale and executable anti-pattern refusals |
| Delegation and protocols | `C18`–`C19` | Durable child tasks, joins, MCP/A2A gateways |
| Trust and effects | `C20`–`C23` | Security, identity, protected LOS effect, sandbox/egress/privacy |
| Evidence and governance | `C24`–`C26` | MLflow tracing/evaluation and governed operating model |
| Production engineering | `C27`–`C28` | Immutable release, compatibility, recovery, capacity, and cost |

A change set must not silently reimplement earlier contracts. If a shared contract changes, update compatibility tests and every affected earlier checkpoint in the same review.

## Agent-executable implementation protocol

For every checkpoint:

1. Read the complete affected book chapter, mapped course lesson, previous/next transition, repository instructions, current contracts, and this checkpoint entry.
2. Inspect existing code/tests/registry before creating a module. Reuse a contract only when semantics and authority match.
3. Write the **before** behavioral test showing the inherited limitation.
4. Implement the smallest **added** capability while keeping lending decisions, business state, policy, credentials, effects, and audit outside the model/SDK.
5. Add the **after** happy path and at least one failure/refusal/replay/recovery test.
6. Produce a deterministic redacted `StageReport` and update the chapter’s `Cxx.md` code tour.
7. Register the entry point, scenarios, tests, chapter/lesson mapping, and optional dependencies. Validate that referenced files exist.
8. Run syntax, type/lint if configured, unit, contract, workflow, security, stage-registry, and offline CLI checks before optional live integrations.
9. For OpenAI/Agents/MLflow changes, run adapter conformance against the exact lock and verify no secret or sensitive fixture value appears in serialized state or telemetry.
10. Rebuild manuscript and generated artifacts from canonical source, then validate headings, links, diagrams, code extraction, package map, test counts, and checksums.
11. Record architecture decision, risk, tests, release evidence, and unresolved limitations in the review description. Do not claim production readiness from teaching doubles.

## Required validation profiles

### Mandatory offline profile

```bash
python -m compileall -q mortgage_case tests/mortgage_case
python -m unittest discover -s tests/mortgage_case -v
python -m mortgage_case --chapter 1 --scenario missing_income_document --offline
python -m mortgage_case --chapter 28 --scenario happy_path --offline
python tools/validate_mortgage_stage_registry.py
python tools/scan_example_output.py --deny-sensitive-fixture-values
```

These commands are target commands; add them only when their files exist. CI must fail if the stage registry cites a missing entry point/test, an offline run attempts network access, a normal stage imports an unsafe anti-pattern module, or a sensitive fixture value appears in output.

### Optional integration profiles

| Profile | Purpose | Gate |
| --- | --- | --- |
| Direct OpenAI Python SDK | Verify `C01` structured response adapter | Explicit environment flag, bounded cost, synthetic prompt, no effect tools |
| OpenAI Agents SDK | Verify real package imports, tool schemas, structured output, HITL serialization, trace privacy, and cancellation | Exact lock, synthetic context, gateway doubles, no real LOS |
| MLflow | Verify traces, datasets, scorers, and comparisons in local or configured tracking backend | Redaction scan, no raw document content, audit separation |
| Durable engine | Verify activity/replay/signal/cancel/build compatibility | Same provider-neutral workflow/effect contracts and fault suite |
| MCP/A2A | Verify protocol adapter conformance | Synthetic endpoint/peer, pinned metadata, no inbound-token passthrough |

Optional jobs may skip cleanly when dependencies or credentials are absent, but their skipped status must be visible. A skipped optional job cannot satisfy a mandatory architecture or safety gate.

## Full-course acceptance gates

The roadmap is complete only when a new reader can follow `MORT-2026-000184` from `C01` through `C28` and all of the following are true:

- Every chapter and mapped course lesson states **before**, **added**, **after**, remaining limitations, and the next dependency.
- The same synthetic tenant, anchor case, applicant, document lineage, and purpose remain recognizable across all checkpoints; controlled variants/cohorts are separately versioned and cannot replace the anchor narrative.
- Every checkpoint has one offline command, deterministic expected output, named tests, and at least one appropriate failure/refusal/recovery case.
- No listing references an undefined symbol or an unstated external service; snippets cited as executable are extracted from tested source.
- Direct OpenAI Python SDK and OpenAI Agents SDK responsibilities are named accurately and isolated behind provider/platform contracts.
- Exact package locks, model routes, prompts/Skills, policies, schemas, tools, workflow builds, datasets, scorers, and release digests are recorded.
- A model cannot approve/deny credit, set authoritative terms, calculate authoritative financial ratios, generate unsupported adverse-action reasons, grant authority, commit effects, certify evidence, or promote a release.
- All financial calculations use deterministic code, documented inputs, `Decimal`, explicit rounding, formula version, and recomputation tests.
- Runtime decision paths do not use protected characteristics as decision features; governed fairness/proxy evaluation is isolated, approved, privacy-reviewed, statistically qualified, and release-gating. Synthetic results are labeled as mechanism tests, not real-world fairness evidence.
- Authorization filters tenant/case/field/source/purpose before document bytes reach the model; context and memory have provenance, trust, retention, correction, and deletion rules.
- Delegation preserves subject identity, records actor/owner, narrows authority/budget/time/depth, and defines cancellation/join behavior.
- An approval binds the exact operational proposal, evidence, policy, case version, reviewer, and expiry; material change requires a new approval. The separate `LendingDecision` remains human/domain-owned.
- Protected LOS effects use idempotency, intent hash, optimistic precondition, receipt, unknown state, reconciliation, and one retry owner.
- Duplicate delivery, stale state, provider outage, timeout-after-write, cancellation, revoked access, approval expiry, child failure, prompt injection, cross-tenant access, PII leakage, incompatible worker, and fairness regression have executable tests and an operator disposition.
- MLflow and OpenTelemetry evidence joins to platform IDs while raw sensitive content is excluded by default and authoritative audit/effect/approval records remain separate.
- Evaluation covers evidence accuracy, calculations, trajectory/tool use, authorization, safety, fairness, repeated-run reliability, latency, cost, human burden, and worst slices with executable release gates.
- The book/course source, example registry, README, diagrams, code, tests, generated artifacts, manifests, checksums, and release package agree after each release.
- The documentation clearly states that synthetic teaching code is not legal advice, a credit policy, a production security control, or a system authorized to make lending decisions.

Until these gates are met, the material may describe the target architecture, but it must not claim that the mortgage implementation is production-ready or suitable for real lending decisions.
