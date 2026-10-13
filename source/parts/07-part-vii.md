# PART VII — EVIDENCE, EVALUATION, AND IMPROVEMENT

You cannot improve a system you cannot explain, and you cannot call a change an
improvement by looking only at its average score. Earlier chapters listed what
each pattern must emit and how a run accepts its own result; this Part puts
those signals to work:

- **Chapter 24** joins them into one causal trace of each run.
- **Chapter 25** turns traces into evaluation, slices, regression cases, and release evidence for governed improvement.

The aim is not more telemetry for its own sake; it is evidence that helps a team
decide what to fix, what to release, and what to leave alone.

# 24 — Follow a Run from Request to Verified Outcome

> **Evidence context:** OpenTelemetry GenAI semantic conventions remain in Development and have moved to a dedicated repository; isolate them behind an internal mapping layer. Phoenix is one implementation option for OpenInference/OTel-based tracing and evaluation. **[R19][R23]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** An evidence review completes slowly and expensively. Operators can see a final summary but cannot tell whether the delay came from queues, retrieval, policy, model turns, retries, human dwell, or a slow connector. Harborlight's target is one trace that links the entire run. |

|  |
| --- |
| **THE DESIGN CHOICE** Adopt OpenTelemetry-compatible causal traces and MLflow 3.15.2 (pinned) for diagnostics; retain complete protected audit evidence separately. |

## Why a trace must explain decisions, not just latency

A final answer tells you what the user saw; it rarely tells you why the system
got there. When a mortgage review is slow, expensive, or wrong, the useful
question is causal: which queue, retrieval, model turn, retry, approval, or
connector created the outcome? This chapter builds one trace across those
boundaries while keeping protected audit evidence in its proper store.

## A useful trace tells the story of the run

Observability answers two different questions. Diagnostics ask, “Why was this
run slow, wrong, or expensive?” Audit asks, “Which protected decision and effect
must the enterprise be able to prove later?” A causal trace is optimized for
the first question: it links activity across services, retries, queues, and
remote agents. The audit ledger is optimized for the second: it preserves the
complete, integrity-protected records required for protected decisions and
effects. A trace may point to an audit record, but it should not become the
only copy of that record.

Appendix A's P-09 and Chapter 17's AP-14 name this object and what its absence
costs; this book calls it the causal run trace, and Chapter 25 calls the same
run's ordered decisions its trajectory. Three other records remain
authoritative: workflow history for execution state (Chapter 15), the effect
ledger for effect state (Chapter 22), and the audit ledger for proof. The trace
links to all three and replaces none.

[[DIAGRAM:causal-trace|Figure 24-1 — A causal run trace links asynchronous work while protected decisions and effects enter a separate audit ledger]]

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Trace pipeline; separate audit ledger | sensitive runtime to operations access | trace shard · regional collector | one span/export batch | W3C trace context · SpanEnvelope · TraceIndex · AuditEvent |

An operator should be able to ask a trace four questions without opening every
log line. Which run was this, and which release handled the request? Which
decision changed the path: what context the model saw, and which policy
decision narrowed the eligible actions? Which activity consumed the time or
budget? Which effect was committed, which receipt proves it, and did the
business obligation succeed? The answers come from stable identifiers and typed
links, not from copying every prompt and response into a search index.
Long-running runs need span links as well as nesting, because queues, retries,
resumptions, and fan-out do not form one in-process call stack.

## Follow one decision from request to outcome

### Debugging method

1. Start from the violated outcome or SLO, not from the final prose.
2. Walk the critical path and split elapsed time into queue, execution, human dwell, retry delay, and reconciliation.
3. Find the first divergent span: input classification, source or freshness, context manifest, prompt, route, model, tool, arguments, policy, approval, effect, or acceptance.
4. Diff the failing run against the nearest accepted run — run manifest, context and evidence versions, and every pinned version — before comparing final prose.
5. Change nothing, especially the prompt, until the evidence locates the failing responsibility. A prompt change that hides a policy or contract defect removes the signal without removing the fault.

### Worked example — diagnosing a slow mortgage-evidence review

Harborlight reports that a mortgage evidence review took twelve minutes to
return its summary. The summary looks plausible, so a request log alone would
make the incident appear closed. The causal trace instead shows a three-minute
queue wait, two retrieval attempts caused by a stale index, a four-minute human
approval wait, and a loan-origination connector timeout whose effect record is
**Unknown**, so the run cannot close (Chapter 15 § Terminal correctness). The
operator now has a safe next step: reconcile the LOS before retrying, then
decide whether the latency problem belongs to capacity, retrieval freshness,
human workflow, or effect recovery.

| **Trace segment** | **Time and category** | **What the operator learns** | **Action or evidence** |
| --- | --- | --- | --- |
| Admission and queue | 3 min · queue | The run waited before any model work began | Queue age, capacity class, and assignment event |
| Retrieval | 2 min · retry delay | The first context snapshot was stale and a second attempt ran | Knowledge release digest and index build, extraction record versions, ACL-filter count, freshness, query hash |
| Approval | 4 min · human dwell | Human dwell dominated model latency | Proposal hash, approver role, wait and expiry timestamps |
| Connector | 3 min · execution | The downstream call timed out after dispatch | Tool span, idempotency key, downstream request ID |
| Effect ledger | open · reconciliation | The mortgage document request cannot yet be called successful or declined | LOS receipt or reconciliation case; no blind retry |

The first divergent decision is the stale index snapshot; the Unknown effect is
the first state that blocks a safe retry.

This example also shows why “trace everything” is not a sufficient design. The
trace needs the identifiers and state transitions that explain the run, while
the sensitive document payload remains in a controlled content or audit store
with an authorized reference.

## Build observability around decisions and effects

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Explain and improve a distributed probabilistic trajectory, not merely log the final text. |
| Why it is difficult | One outcome spans models, prompts, retrievals, tools, policies, queues, agents, humans, and retries; full content may contain secrets or PII; identical inputs may produce different paths. |
| Design alternatives | Application logs; framework traces; vendor APM; OpenTelemetry; event-sourced audit. |
| Recommended architecture | Emit one causal trace per run with spans for every call and decision (schema below). Separate operational telemetry from immutable audit. |
| Trade-offs | Rich traces improve diagnosis but increase storage, privacy, and access-control burden. |
| Failure scenarios | Trace breaks at an A2A boundary; model prompts leak secrets; replay repeats a live side effect. |
| Enterprise example | A mortgage platform traces evidence routing, knowledge citations, tool arguments, policy decisions, approval latency, and LOS effects; a failed document request becomes a regression fixture and sandbox replay. |

### What the trace needs to connect

Map spans to OpenTelemetry-compatible context and GenAI semantic conventions
through an internal layer, with organization-specific attributes where the
standards are still evolving. A run is the root span; every call and decision
below is a child span or a linked asynchronous trace.

| **Span type** | **Essential attributes** |
| --- | --- |
| Run | tenant, subject hash, agent/workflow/version set, purpose, risk class, status, budget, token and cost totals, stop reason, correlation ID |
| Model | provider, model route/version, prompt-template hash, context-manifest hash, input/output tokens, latency, cache, finish/error type |
| Retrieval | knowledge release digest and index build, extraction record versions, query hash, ACL-filter count, documents returned, freshness, latency |
| Decision | kind (route, plan compile/revision, step disposition, acceptance, critique); candidates and eligibility removals; chosen option; validator or compiler reason; scorer/rubric versions for acceptance; plan digest/revision and replan diff; turn index, information gain, remaining budgets, stop reason |
| Policy | policy bundle/version, decision ID, action/resource hash, decision, obligations, rule ids, reason code, latency |
| Tool | tool/version, risk class, arguments hash, grant ID, credential lease ID, idempotency key, retries, effect state (`effect.state`), effect receipt, artifact references, latency |
| Memory | memory ID/version, operation (read/write/delete), scope/tenant, purpose and policy basis, provenance, TTL |
| Agent task | caller/callee versions, task ID, protocol, ownership transition, grant lineage, budget transfer, join condition, terminal status |
| Approval | request hash, policy reason, approver role, wait time, decision, expiry, modification flag |
| Security control | control (detector, egress, DLP, kill switch), rule/version, taint label of the input, decision, action |
| Workflow | node/attempt, workflow build, queue delay, checkpoint, timer/wait state, retry class and owner, signal/event IDs and source, cancel and replay flags |

The “What you need to see in production” lists in Chapters 2, 6, 10–15, and 18
are attributes on these span types; this table is their common schema.

Do not treat hidden chain-of-thought as required observability. Record concise decision summaries, selected alternatives, evidence references, structured plans, policy outputs, and tool trajectories. This is more stable, safer, and more operationally useful.

|  |
| --- |
| **OBSERVABILITY TIP**  Trace the decision, not only the call. Latency and token counts tell you a run was slow; they never tell you why it was wrong. Record which context manifest was authorized, which policy applied, and which branch was taken — those attributes are what let a trace answer a question weeks later. |

### A scorecard operators can actually use

| **Dimension** | **Representative metrics** |
| --- | --- |
| Outcome quality | Task success, groundedness, faithfulness / unsupported-claim rate, factual precision/recall, business acceptance, human correction rate |
| Trajectory quality | Correct route/tool/handoff, tool-selection precision/recall, argument correctness, plan adherence, unnecessary steps, plan churn, evidence coverage, policy adherence |
| Reliability | Completion rate, retry recovery, retry amplification, duplicate-effect rate, ambiguous-effect rate, stuck-run age, compensation success |
| Safety/security | Unauthorized-attempt block rate, prompt-injection utility/security scores, DLP events, cross-tenant violations, approval bypasses |
| Latency | End-to-end p50/p95/p99, time to first useful update, queue delay, model/tool latency, approval wait |
| Cost | Cost/successful outcome, input/output tokens, tool/API cost, cache hit, wasted retry cost, specialist fan-out cost |
| Human load | Approval frequency, approval dwell time, escalation rate, override rate, reviewer agreement, reviewer fatigue |
| Operations | SLO attainment, trace completeness, rollback time, mean time to diagnose/recover, dead-letter backlog |

Chapter 25 explains how the outcome and trajectory rows are scored offline and
per slice.

### Trace and replay semantics

* Propagate W3C traceparent/tracestate across HTTP, queues, MCP, and A2A. Use span links when work is triggered asynchronously or crosses an independently rooted remote trace.
* Workflow replay (Chapter 15) re-executes history using recorded activity results. Diagnostic replay renders a recorded run without calling models or tools. A fork (Chapter 4 § Run API, `:fork`) is a sandbox run from a checkpoint with explicitly changed versions; its external effects are mocked or read-only. None of the three may create a live effect; work that must change the outside world again is a new, separately authorized run under Chapter 22, not a replay.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Telemetry Collector | Receive OTLP traces, metrics, and logs; enrich with tenant/run metadata; redact and route |
| Trace Index | Fast causal lookup by run, task, effect, version, error, tenant, and time |
| Content Vault | Separately encrypted optional prompt/output/tool payloads referenced by hash |
| Metrics/SLO Pipeline | Aggregate low-cardinality service, quality, safety, cost, and human-load indicators |
| Replay/Fork Service | Reconstruct a safe sandbox run from manifest, history, artifacts, and recorded effects |
| Audit ledger writer | Append-only, integrity-protected, loss-intolerant path for protected decisions and effects; see Chapter 4 § Where each kind of state belongs |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /otlp/v1/traces, /metrics, /logs | Standard OTLP ingestion with workload authentication, tenant binding, size/rate limits, and redaction |
| GET /v1/runs/{run\_id}/trace | Return role-redacted causal graph, span summaries, links, and authorized content handles |

Forks use Chapter 4's `POST /v1/runs/{id}:fork`: a sandbox run whose external
effects are mocked or read-only; a run that must act again starts through
`POST /v1/runs` with its own authorization. The Chapter 14
operator console reads the trace API; its live run graph is a role-redacted
view of this trace.

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| TraceIndex | trace/run IDs, tenant, start/end, root service, manifest/version set, status/risk, error/effect/approval flags, cost/tokens; no sensitive body by default |
| SpanEnvelope | trace/span/parent or links, kind, service/operation, start/duration, status, normalized attributes/events, content refs, sampling class |
| ContentBlob | encrypted URI/hash, tenant/key, classification, redaction profile, authorized roles, retention, source span; stored separately |
| AuditEvent | run/effect/decision ID, actor and subject, policy/approval reference, integrity hash, retention class; never sampled |

### Privacy and reliability

Raw prompts, retrieved documents, credentials, and protected tool payloads do
not automatically belong in traces. Record governed artifact references,
hashes, classifications, and redaction metadata; content that must be captured
is selective, redacted, encrypted, and role restricted in the Content Vault.
Regional collectors buffer, redact, batch, compress, retry, and spill encrypted
data, so application latency is decoupled from backend analytics. Diagnostic
telemetry may be sampled; protected effect and audit events follow a separate
loss-intolerant path with completeness and integrity controls plus monitoring.

### What changes as usage grows

* Partition trace storage by tenant + time; index only operationally useful low-cardinality fields. Put high-cardinality attributes and content in columnar/object storage with controlled query paths.
* Use tiered sampling: 100% metadata for runs/effects/policy/approvals; 100% detailed traces for failures, security findings, canaries, R3/R4, and operator-selected runs; adaptive/statistical detail for routine success.
* Move older traces from hot index to compressed object storage, preserving searchable summaries and evidence pointers. Retention differs for telemetry, evaluation fixtures, and legal/audit records.
* Compute metrics from events/spans through streaming aggregation rather than querying raw traces for dashboards. Control label cardinality; never use user IDs, prompts, or URLs as metric labels.
* Preserve sampling weights and selection reasons for online estimates.
* Monitor the observability system itself: collector drop rate, redaction failure, trace completeness, broken links, ingest lag, and hot-store cost.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Telemetry maturity | OTLP and the general span model are mature, but the dedicated OpenTelemetry GenAI semantic conventions are still in Development. Version the mapping and retain a stable internal event schema. | R19 |

The discussion above draws on R19. Appendix J lists the complete sources and records their authority, version, and scope.

## A sensible place to start

Start by instrumenting what the platform owns: the first example places manual
agent and tool spans and records a decision attribute.

[[EXAMPLE:mlflow-tracing]]

### MLflow tracing integration

The examples use OpenTelemetry-compatible context propagation and MLflow 3.15.2
(pinned) tracing. `mlflow.openai.autolog()` captures OpenAI calls, while
explicit spans cover platform-owned boundaries; the example below records the
context-manifest ID, not the context body. In the pinned 3.15.2, `autolog`
registers MLflow's Agents SDK trace processor whatever the setting;
`disable_openai_agent_tracer`, true by default, decides whether it first
removes the SDK's own exporter to OpenAI's tracing backend. The examples pass
`False`, which keeps that exporter beside MLflow's; it sends nothing without an
API key, but a deployment that must keep traces in-house should leave the
default. `RunConfig(trace_include_sensitive_data=False)` remains a separate
privacy control.

[[EXAMPLE:mlflow-trace-configuration]]

### Mortgage Agents SDK integration

The cumulative mortgage runtime makes the boundary concrete: the OpenAI Agents
SDK performs one bounded, read-only tool loop; the Tool Gateway owns the
synthetic projection; MLflow records the causal AgentRunner, agent, and tool
spans. The scripted model keeps the example offline, so a trace proves the
integration and redaction mechanics without claiming a live provider call. The
queue, policy, approval, and effect spans in the worked example are not here;
they are platform spans you add with the explicit-span pattern above. That is
exercise 1.

[[EXAMPLE:mortgage-agents-mlflow]]

## If this fails in production

1. A trace breaks at a queue, resume, or A2A boundary: check traceparent propagation and span links, and fall back to domain-ID joins.
2. Spans lack release or policy versions: block the release, because runs cannot be compared.
3. The collector drops data or redaction fails: confirm protected audit events took the loss-intolerant path, quarantine leaked content, and alert on the observability SLOs.

To debug a failed run, use the method in § Debugging method. If telemetry cannot join a run to its release, decisions, and effects, see AP-14 in Chapter 17.

## What to verify before production

**✓** Every span type in the schema carries stable causal identifiers.

**✓** Asynchronous relationships use span links and domain IDs.

**✓** Sensitive content is excluded, tokenized, or access-controlled.

**✓** Collector outage does not stop protected workflow state or required audit evidence.

**✓** SLOs expose critical-path latency, cost, errors, retries, human dwell, and unknown effects.

## Put the idea to work

1. Starting from the mortgage Agents SDK example, add the queue, policy, approval, and effect spans the schema requires, so the worked example's five segments appear.
2. Create a dashboard that separates machine latency from human dwell.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| What is the root trace for a long-running run? | One causal run trace linked across workflow tasks, model calls, tools, messages, approvals, effects, and restarts using stable IDs and span links, because queues, retries, fan-out, resumed waits, and remote agents are not one call stack. |
| Which data should not be put blindly into traces? | Secrets, credentials, raw sensitive prompts, retrieved content, tool payloads, and regulated identifiers; record governed references and hashes where possible. |
| How do traces support debugging? | They expose critical path, state transitions, versions, policy decisions, retries, cost, evidence lineage, and the first divergent step. |
| Why keep audit separate? | Audit has stronger completeness, integrity, access, and retention obligations than sampled diagnostic telemetry. |
| Which record do you trust when the trace and the effect ledger disagree? | The effect ledger for effect state and workflow history for execution state; the trace is diagnostic and may be sampled, so a disagreement is an observability defect to fix, not a fact to act on. |

## Where this leads next

Tracing explains what happened; Chapter 25 determines whether the trajectory and outcome were acceptable and whether a change is safe to ship.

# 25 — Improve the System Without Handing It Control

> **Evidence context:** The evaluation architecture maps to current capabilities documented by MLflow, DeepEval, Ragas, LangSmith, and OpenAI. Tool names and APIs are examples; the durable contract is dataset + release manifest + scorer versions + trace/effect evidence. **[R20][R21][R22][R24][R25][R26]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** A prompt change improves average evidence-summary quality but, in one low-volume region, attempts an LOS lookup outside the case's eligible tool set. Aggregate accuracy hides the regression; slice-aware trajectory evaluation blocks the release. |

|  |
| --- |
| **THE DESIGN CHOICE** Gate releases on immutable datasets, executable trajectory checks, calibrated judges, slices, failures, and baseline comparisons. |

## Why improvement needs a governed feedback loop

Production evidence is only useful if it can change the system safely. This
chapter follows a failure from trace to evaluation case to candidate release,
and keeps outcome quality separate from trajectory safety. The distinction
matters when an average score improves while a small tenant, language, or tool
path becomes less safe. Chapter 24's traces are the starting evidence; a failed
run such as its unresolved document request becomes a reviewed case here.

## A release gate starts with evidence

An evaluation compares a candidate against an explicit contract, a baseline,
and the slices where failure matters. The candidate is not just a prompt: it is
the versioned set of prompt, model route, workflow, tools, policies, context strategy,
and runtime configuration that could change the trajectory. A release gate
combines deterministic checks with calibrated quality evidence, then records a
decision that another operator can reproduce.

Chapter 13 evaluated one candidate artifact inside a run to decide whether that
run's result is accepted. This chapter evaluates a candidate version of the
system across a dataset to decide whether it may be promoted. The discipline is
the same — deterministic checks first, calibrated judges only for nuance, no
self-certification — but the release decision adds immutable datasets,
baselines, slices, and repeated runs. Evaluation is the Measure and Validate
stages of the governed learning loop described later in this chapter.

[[DIAGRAM:evaluation-gate|Figure 25-1 — Candidate evaluation combines deterministic checks, calibrated judges, slices, and a risk-tiered release gate]]

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Evaluation Registry and release gate | production evidence to development corpus | dataset version · scorer pool · slice | one case and candidate release | EvalCase · EvaluationResult · ReleaseGateDecision |

The gate is deliberately not a single score. A candidate can improve a
language-quality metric while violating an authorization invariant, increasing
unknown effects, or regressing a small but high-consequence slice. Deterministic
failure therefore blocks promotion; a model judge can add useful evidence about
nuanced quality, but it cannot override a protected invariant. Normalize every
framework score into a platform-owned EvaluationResult; no framework score is
release authority. A gate may return waiver-required for residual risk outside
a protected invariant; the waiver is a Chapter 26 exception — scoped, owned,
compensated, and expiring — never a way past a deterministic failure.

## Use evaluation to guide engineering decisions

A release dataset needs immutable cases, explicit slices, and trajectory evidence—not just one score. The release decision should show where the system improved, where uncertainty remains, and which regressions are severe enough to stop promotion.

An agent evaluation case includes input, initial state, user simulation or messages, expected outcome properties, allowed and forbidden tools, required evidence, maximum budgets, failure injections, and slice tags. The result includes final output, complete trajectory, artifacts, policy decisions, effects, human events, latency, cost, and terminal state.

### Judge the outcome and the path separately

Outcome evaluation asks whether the user-visible result satisfies the task
contract: was the answer correct, grounded, complete, and accepted? Trajectory
evaluation asks how the system got there: did it retrieve only authorized
context, choose the permitted tool, respect the budget, request approval, and
leave a verifiable effect? Both are necessary because a lucky final answer can
hide an unsafe path, while a safe path can still produce an unhelpful result.
Chapter 24's scorecard lists the outcome and trajectory metrics; here they are
computed per case, per slice, against a baseline.

Apply Chapter 13's rule for which properties are checked deterministically and
which may use a calibrated judge; at release level, also record the evaluator
type and version in every result so a probabilistic opinion is never mistaken
for a proof.

### Layer tests from contracts to outcomes

| **Level** | **What to test** | **Method** |
| --- | --- | --- |
| Unit | Schemas, plan compiler, policy rules, context filters, budget logic, redaction, idempotency | Deterministic tests and property-based fuzzing |
| Contract | Tool/MCP/A2A schemas, auth scopes, errors, compatibility, effect receipts | Consumer/provider contract tests against mocks and sandboxes |
| Component | Agent behavior with controlled models/tools; trajectory constraints (tools, order, evidence, budgets, handoffs) | Seeded scenarios, golden trajectories, metamorphic tests |
| Workflow | Retries, replay, pause/resume, cancellation, compensation, code-version migration | Fault injection and workflow-engine test harness |
| Simulation | Multi-turn users, changing data, delayed events, partial failures | Stateful environment and user simulators; many seeds |
| Security/adversarial | Prompt injection, malicious files/tools/agents, exfiltration, privilege escalation | Prompt-injection benchmark suites, red-team corpora, sandbox escape and DLP tests |
| Performance | Queue age, tokens, tool calls, latency, cost per accepted outcome, fairness | Load and soak tests per slice |
| Regression | Known wins/failures across pinned versions | Offline datasets; outcome + trace graders; statistical confidence |
| End-to-end | Real identity, source ACLs, queues, approvals, effects, audit | Staging tenant with synthetic data; canary in production with stop conditions |
| Continuous | Drift, novel failures, cost/latency, policy incidents | Sampled online evals, human review, alerts, incident-to-test loop |

Measure repeated-run reliability as the share of tasks that pass on all k repeated trials (pass^k), not just best-of-one success; compute it from the trials themselves rather than raising a single-run pass rate to the k, which assumes independent trials.

### Worked example — average improvement, protected-slice regression

Suppose a Harborlight prompt revision makes routine evidence summaries clearer,
but in one low-volume region the candidate now attempts an LOS lookup outside
the case's eligible tool set in a simulated trajectory. The aggregate score is
better, yet the candidate is not a safe release. Slice-aware evaluation makes
the disagreement visible and gives the release owner a concrete decision
record.

| **Evidence** | **Candidate result** | **Release interpretation** |
| --- | --- | --- |
| Routine answer quality | Improved against the baseline | Useful quality evidence, not sufficient for promotion |
| Protected-action trajectory | One forbidden lookup appears | Deterministic safety regression; block the candidate |
| Region/risk slice | Regression is low volume but high consequence | Volume cannot dilute the risk tier |
| Diagnosis | New context or routing path selects the LOS tool | Compare trace, policy decision, context manifest, and release manifest (Chapter 24 § Debugging method) |
| Next candidate | Narrow retrieval/tool eligibility and add the case to the regression set | Re-run held-out, adversarial, and protected-effect checks |

In production the Tool Gateway would deny the call, but the attempt is still a
deterministic trajectory failure: the candidate's context or routing now pushes
the model toward a forbidden action, and shipping it would turn a release
defect into production denials and incidents that each depend on one control
holding.

The important habit is to preserve the failing trace as a versioned case after
privacy and purpose review. Otherwise the next improvement can repeat the same
failure while the dashboard reports only the improved average.

## Separate runtime adaptation from offline improvement

Runtime adaptation chooses among options approved before the run started:
pre-approved routes and fallbacks, additional authorized context or dropping
optional context, retry within budget, stopping a loop, asking for input,
escalating, and shedding load. It cannot expand permissions, purpose, data
access, spend, tools, or model allowlists. Offline improvement creates a new
immutable release and may change prompts, context/RAG, memory policy, tools,
skills, model selection, routing, deterministic code, agent topology,
workflows, and system architecture after evaluation and approval.

The test is simple: if a change outlives the run, or widens the envelope, it is
an offline release. Chapter 13's bounded revision improves an artifact inside
the run, so it is runtime. A memory write within memory policy is a governed
runtime data effect (Chapter 6); changing that policy is offline. Chapter 28's
degraded modes and Chapter 23's kill switches are runtime controls inside a
pre-approved envelope.

For Harborlight, falling back to the pre-approved secondary model route when
the primary is rate-limited is runtime adaptation. Making the cheaper route the
default is an offline release that needs slice evaluation (AP-15). Runtime
outcomes feed the offline loop as evidence, never as a change.

[[DIAGRAM:runtime-offline|Figure 25-2 — Runtime adaptation and offline improvement boundary]]

## Close the loop without handing control to the model

Continuous improvement joins production evidence to versioned change and release. It does not let an agent rewrite its prompt, memory policy, permissions, evaluator, or code and then certify itself.

[[DIAGRAM:learning-loop|Figure 25-3 — Observe → Measure → Detect → Diagnose → Recommend → Validate → Approve → Deploy → Monitor → Learn]]

| **Stage** | **Work and durable output** | **Automation boundary** |
| --- | --- | --- |
| Observe | Join traces, context, tools/effects, feedback, corrections, incidents, cost, latency, outcome into ProductionSample linked to TraceIndex (Chapter 24), including failed candidates from Chapter 13 | Capture/redact/sample automatically; approve sensitive purpose/access |
| Measure | Run deterministic invariants and quality, safety, retrieval, tool, trajectory, SLO, economics metrics into EvaluationResult | Approved scorers automate; humans define truth/threshold/calibration |
| Detect | Rules, anomaly, drift, slice regression, recurring corrections into an alert or containment action | Alert/contain within approved envelope |
| Diagnose | Compare successful/failed traces, first divergence, structural/semantic clusters into an owner-confirmed causal hypothesis | Tools rank; accountable owner confirms cause/business meaning |
| Recommend | Smallest candidate, predicted benefit, risk, affected contracts, rollback into ChangeBundle draft (Chapter 27) | Generate drafts; never self-approve/mutate production |
| Validate | Replay, simulation, unit/contract/security/privacy/adversarial/load/cost/compatibility tests into ValidationReport | CI automates; owners approve datasets, exceptions, residual risk |
| Approve | Use-case tier × change class (Chapter 26) and domain/security/privacy/operations decision into ReleaseGateDecision; PromotionDecision is recorded at promotion (Chapter 27) | Only pre-approved low-risk change classes auto-approve; never self-authored behavior |
| Deploy | Immutable build, bindings, shadow/canary, rollback into ReleaseManifest (Chapter 27) | Progressive delivery within approved policy |
| Monitor | Compare canary/production to baseline across quality, safety, reliability, cost, business | Auto-halt/rollback on tested stop condition |
| Learn | Record causal result, curate regressions, update taxonomy/runbook into a reviewed EvalCase proposal and runbook update | Metadata may automate; data/policy/architecture changes require governance |

Chapter 27 executes the Deploy and Monitor stages as signed promotion through
shadow and canary.

The worked example travels the same loop. Slice evaluation detects the
forbidden-tool attempt, and comparing traces and context manifests diagnoses
the new retrieval path. The recommendation narrows retrieval and tool
eligibility; held-out, adversarial, and protected-effect suites validate it,
and the domain owner approves. The failing trace becomes a reviewed case.

| **What the loop may do** | **Changes** |
| --- | --- |
| Automate within the envelope | Capture, approved redaction and scoring, anomaly detection, clustering, draft recommendations, tests, sandbox runs, approved canaries, halt, rollback |
| Require human governance | Permission, policy, data, memory purpose, protected effects, model allowlist, topology, architecture, evaluator truth, training data, exceptions, wider promotion |
| Never permitted | Expanding authority, disabling controls, editing audit evidence, changing approval requirements, promoting self-authored behavior |

|  |
| --- |
| **BEST PRACTICE**  Grow the evaluation set from production failures, not only from imagined ones. Every incident should end by contributing a reviewed case. A suite assembled up front measures what you expected to be hard; a suite grown from incidents measures what actually is. |

## Choose the right improvement path

The Diagnose stage selects the row. Change the lowest layer that removes the
cause, and prefer deterministic code when the decision has become stable.

| **Layer** | **Evidence** | **Candidate** | **Validation / approval** |
| --- | --- | --- | --- |
| Prompts | Omissions, conflicts, unsupported claims | Clarify responsibility, examples, evidence, stop rules | Golden/adversarial replay; behavior/policy review |
| Context/RAG | Recall/precision, stale/poisoned source, injection correlation | ACL/freshness/ranking/dedup/token/source changes | Retrieval/faithfulness/security tests; data-owner approval |
| Document extraction | Field accuracy on a labelled document set; review-route rate and verification rejections over a fixed denominator | Extractor or prompt version, consistency checks, verification thresholds | Re-extraction replay on golden documents; data-owner approval |
| Knowledge | Unknown-under-policy refusals per rule, runtime contradictions, citations of superseded releases, SME corrections, held and refused objects per release against a fixed integer budget | A new knowledge release: rule, vocabulary, ontology, or tenant extension | Knowledge test-suite replay, grounding, consistency, and independent SME approval (Chapter 5) |
| Memory | Correction, leakage, stale/poisoned retrieval | Eligibility, purpose, scope, TTL, verification, deletion | Privacy/security/longitudinal replay; memory-purpose approval |
| Tools | Wrong choice/args, timeout/retry/unknown effect | Narrow schema/catalog, preconditions, idempotency/reconcile | Contract/failure/load/security; effect/permission approval |
| Skills | Version-specific or inconsistent behavior | New immutable Skill/dependencies/examples/acceptance | Skill certification and domain owner |
| Model selection | Quality/cost/latency/refusal/schema drift | Eligibility, threshold, cascade, fallback, context window | Full route evaluation, privacy/residency, canary; allowlist approval |
| Routing | Misroute/escalation/capacity imbalance | Calibrate, deterministic pre-router, fallback/escalation | Shadow/counterfactual; authority/ownership review |
| Deterministic code | Repeated stable low-entropy model decision | Extract rule, lookup, calculation, parser, transform | Unit/property/exception tests and domain approval |
| Agent topology | Duplicate work, fan-out/handoff, unclear owner | Merge agents, supervisor/task service, specialization change | Simulation, ownership/authority, migration review |
| Workflows | Loops, stuck joins, weak recovery | State, deadline, join, stop, compensation, degraded mode | Replay/concurrency/recovery/RTO-RPO and operations |
| System architecture | Failure recurs across apps/controls | Platform service, contract, gateway, boundary, policy redesign | Architecture/security/privacy and migration evidence |
| Evaluators and datasets | Judge–human disagreement, leakage, missing slice | New scorer/rubric version, new cases, re-partition | Calibration on held-out human labels; evaluation-owner approval (Chapter 26) |

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Evaluation Registry | Version datasets, cases, rubrics, graders, baselines, and release thresholds |
| Evaluation Orchestrator | Run candidates across seeds/environments, grade, compare, and produce confidence intervals |
| Failure Mining Service | Cluster traces/incidents and propose curated regression cases for human review |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/eval-datasets | Create immutable/versioned dataset from approved cases and provenance |
| POST /v1/eval-runs | Evaluate a release candidate against dataset/rubric, seeds, model routes, environment, and budget |
| GET /v1/eval-runs/{eval\_run\_id}/comparison | Compare candidate/baseline metrics, confidence intervals, slices, regressions, cost, and trace deltas |
| POST /v1/release-gates:evaluate | Apply risk-tiered thresholds and return pass/fail/waiver-required with evidence |
| POST /v1/regression-cases:propose | Submit a production failure/cluster for de-identification, labeling, leakage review, and dataset approval |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| EvalDatasetVersion | dataset/version/digest, purpose, cases, slices, provenance, license/privacy/leakage review, owner, lifecycle |
| EvalCase | case ID, input/environment fixtures, expected invariants/artifacts/trajectory constraints, rubric, risk tags, source/provenance |
| EvalRun | candidate/baseline manifest digests, dataset, seeds, grader versions, environment, status, aggregate resource usage |
| EvaluationResult | eval/case/attempt, metric, score, confidence/evidence, deterministic or grader type/version, latency/cost |
| ValidationReport | candidate digest, EvalRun comparisons, non-evaluation test results (contract, security, load, compatibility), slice regressions, ReleaseGateDecision ref; immutable |
| ReleaseGateDecision | candidate, risk tier, thresholds, slice results, decision, waiver, approvers, evidence refs; immutable |
| ProductionSample | run/trace, sampling reason/weight, consent/privacy handling, evaluation status, incident/failure cluster |

### What changes as usage grows

* Run evaluations on dedicated queues with tenant/candidate budgets, reproducible seeds, provider-rate awareness, and early stop when statistical or hard safety failure criteria are met.

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| MLflow baseline | This book pins MLflow 3.15.2 as a reproducibility baseline for its examples. It is not labeled latest; feature availability, experimental status, and compatibility must be re-verified against release notes and current documentation before implementation. | R21 |
| Evaluation limit | R20 documents model judges alongside human feedback attached to traces; R13 asks evaluators to document possible train/test contamination of benchmarks. The book's recommendation, not a sourced finding, is that a passing judge is probabilistic evidence, not proof, and that security, authorization, schema, budget, effect, and acceptance invariants remain deterministic release blockers. | R20; R13 |

The discussion above draws on R13; R20; R21. Appendix J lists the complete sources and records their authority, version, and scope.

|  |
| --- |
| **COMMON PITFALL**  Trusting an LLM judge you have not calibrated against human labels. A judge is a model with its own failure modes and its own drift. Measure its agreement with human raters on a held-out set, re-measure when you change the judge's model, and report the agreement alongside any score it produces. |

## A sensible place to start

MLflow 3.x documents evaluation datasets, feedback, judges, systematic
evaluation, and production monitoring [R20]. This book pins 3.15.2 as its
reproducibility baseline [R21]; newer releases may exist and require separate
compatibility validation. The first example uses deterministic scorers over a
two-case synthetic dataset and reports means; a real gate also compares each
slice against a pinned baseline, as the worked example shows.

[[EXAMPLE:mlflow-evaluation]]

### MLflow trajectory evaluation

The deterministic `no_unknown_effects` and `forbidden_tool_absent` scorers read
the `effect.state` attribute and the tool spans that Chapter 24's schema
records; they are release blockers. The judge and built-in scorers add quality
evidence and cannot override them.

[[EXAMPLE:mlflow-trajectory-evaluation]]

## If this fails in production

1. The gate passed but production regressed: check whether the failing slice exists in the dataset, with enough cases.
2. Check for train/test or benchmark leakage, and for judge drift since calibration.
3. Run the scorer against a known-bad case to confirm it can fail.
4. Add the production trace as a reviewed case before shipping a fix.

To debug the failing run itself, use Chapter 24 § Debugging method.

## What to verify before production

**✓** Runtime adaptation stays inside a fixed envelope; every other behavior change ships as an evaluated, approved release.

**✓** Evaluation covers outcome, trajectory, reliability, security, latency, cost, human load, and operations by slice.

**✓** Every promoted candidate has an immutable ValidationReport and ReleaseGateDecision; Chapter 27 pins them in the release bundle.

**✓** Datasets are versioned and immutable, and each production-derived case passed privacy, purpose, and leakage review.

**✓** Judges report agreement with held-out human labels and are recalibrated when their model changes.

**✓** Every protected slice has a minimum case count and its own threshold.

## Put the idea to work

1. Create a five-case immutable evaluation dataset with trajectory expectations.
2. Add a deterministic scorer that fails any case whose trace attempts a tool outside its eligible set, then show that a candidate with a better mean still fails the gate on one slice.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why is final-answer evaluation insufficient for agents? | A plausible answer can hide unauthorized retrieval, wrong tools, excessive cost, retry waste, unsafe handoffs, duplicate effects, or missing approval; evaluate the complete trajectory. |
| What may runtime adaptation change? | Only pre-approved routes and fallbacks, optional context, loop stops, input requests, and escalation inside a fixed envelope; permissions, data access, tools, and model allowlists change only through an evaluated, approved release. |
| What separates Chapter 13's evaluator from a release gate? | Chapter 13 judges one artifact to decide one run's acceptance; a release gate judges a system version across a dataset, with baselines and slices, to decide promotion. |
| Why can a low-volume slice block a candidate that improves the average? | Volume cannot dilute a risk tier; deterministic protected-action failures block regardless of their share of cases. |
| How does a production failure become a regression case without leaking data or the test set? | De-identification, purpose and leakage review, reduction to the smallest reproducible case, held-out partitioning, and dataset approval. |

## Where this leads next

The improvement loop proposes and validates change; Chapter 26 assigns decision rights, risk tiers, approvals, exceptions, and accountability.
