# PART IX — OBSERVABILITY & EVALUATION

This Part establishes the evidence plane. Traces reconstruct trajectories and effects; evaluations measure outcomes, safety, reliability, latency, cost, and human burden; debugging turns those signals into actionable diagnoses.

# 26 — Observability and Tracing with MLflow

> **Evidence note.** OpenTelemetry GenAI semantic conventions remain in Development and have moved to a dedicated repository; isolate them behind an internal mapping layer. Phoenix is one implementation option for OpenInference/OTel-based tracing and evaluation. [R19][R23]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  A run completes slowly and expensively. Operators can see a final answer but cannot tell whether the delay came from queues, retrieval, policy, model turns, retries, human dwell, or a slow connector. Northstar links the entire trajectory. |

|  |
| --- |
| **DESIGN DECISION**  Adopt OpenTelemetry-compatible causal traces and MLflow 3.15.x for diagnostics; retain complete protected audit evidence separately. |

## What this chapter delivers

Connect workflow, agent, model, retrieval, policy, tool, approval, effect, and human activity into one causal trajectory.

## Solution blueprint


Figure 18. Observability and Tracing with MLflow.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Trace pipeline; separate audit ledger | sensitive runtime to operations access | trace shard · regional collector | one span/export batch | TraceContext · SpanLink · AuditEvent |

## One causal trajectory

A production trace links admission, workflow tasks, AgentRuntime activities, model calls, retrieval, policy decisions, tool invocations, approvals, effects, waits, remote tasks, operator commands, and terminal acceptance. Long-running runs require stable domain IDs and span links because queues, retries, resumptions, and fan-out do not form one in-process call stack.

Northstar uses OpenTelemetry-compatible context propagation and MLflow 3.15.x tracing. mlflow.openai.autolog() can capture OpenAI calls, while explicit spans cover platform-owned boundaries. Required attributes include tenant-safe run and task IDs, release versions, workflow build, model route, tool and policy versions, risk class, token and cost usage, effect state, retry owner, artifact references, and stop reason.

### Privacy and reliability

Raw prompts, retrieved documents, credentials, and protected tool payloads do not automatically belong in traces. Record governed artifact references, hashes, classifications, and redaction metadata. Regional collectors buffer, redact, batch, and export. Diagnostic telemetry may be sampled; protected audit events are written separately with completeness and integrity controls plus monitoring.

### Debugging method

Start with the violated outcome or SLO, identify the critical path, then find the first divergent state transition or decision. Distinguish queue time, execution time, human dwell, retry delay, and reconciliation time. Compare the run manifest and context/evidence versions before comparing final prose.

## Observability, debugging, testing, and evaluation

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Explain and improve a distributed probabilistic trajectory, not merely log the final text. |
| Why it is difficult | One outcome spans models, prompts, retrievals, tools, policies, queues, agents, humans, and retries; full content may contain secrets or PII; identical inputs may produce different paths. |
| Design alternatives | Application logs; framework traces; vendor APM; OpenTelemetry; event-sourced audit; black-box outcome evals; trace/trajectory grading; deterministic simulators. |
| Recommended architecture | Emit one distributed trace per run with spans for every model, retrieval, policy, tool, workflow, handoff, approval, and effect. Separate operational telemetry from immutable audit. Build eval datasets from representative, adversarial, and production-failure cases; score both outcomes and trajectories. |
| Trade-offs | Rich traces improve diagnosis but increase storage, privacy, and access-control burden. Content capture must be selective, redacted, encrypted, and role restricted. |
| Failure scenarios | Trace breaks at an A2A boundary; model prompts leak secrets; average success hides long-tail failures; LLM judge rewards style over correctness; replay repeats a live side effect. |
| Enterprise example | A support platform traces intent routing, knowledge citations, tool arguments, policy decisions, approval latency, and CRM effects; a failed refund becomes a regression fixture and sandbox replay. |

### Trace model

Adopt OpenTelemetry-compatible context and GenAI semantic conventions, with organization-specific attributes where standards are still evolving. A run is the root span; workflow nodes, model calls, retrievals, policy checks, tool/A2A calls, approvals, checkpoints, and compensation are child spans or linked asynchronous traces.

| **Span type** | **Essential attributes** |
| --- | --- |
| Run | tenant, subject hash, agent/workflow/version set, purpose, risk, status, budget, correlation ID |
| Model | provider, model route/version, prompt-template hash, context-manifest hash, input/output tokens, latency, cache, finish/error type |
| Retrieval | source/index snapshot, query hash, ACL-filter count, documents returned, freshness, latency |
| Policy | policy bundle/version, action/resource hash, decision, obligations, reason code, latency |
| Tool | tool/version, risk, arguments hash, auth grant ID, idempotency key, retries, effect receipt, latency |
| Agent task | caller/callee versions, task ID, protocol, ownership transition, budget transfer, terminal status |
| Approval | request hash, policy reason, approver role, wait time, decision, expiry, modification flag |
| Workflow | node/attempt, queue delay, checkpoint, retry class, signal/event IDs, replay flag |

Do not treat hidden chain-of-thought as required observability. Record concise decision summaries, selected alternatives, evidence references, structured plans, policy outputs, and tool trajectories. This is more stable, safer, and more operationally useful.

### Production scorecard

| **Dimension** | **Representative metrics** |
| --- | --- |
| Outcome quality | Task success, groundedness, factual precision/recall, business acceptance, human correction rate |
| Trajectory quality | Correct route/tool/handoff, unnecessary steps, plan churn, evidence coverage, policy adherence |
| Reliability | Completion rate, retry recovery, duplicate-effect rate, ambiguous-effect rate, stuck-run age, compensation success |
| Safety/security | Unauthorized-attempt block rate, prompt-injection utility/security scores, DLP events, cross-tenant violations, approval bypasses |
| Latency | End-to-end p50/p95/p99, time to first useful update, queue delay, model/tool latency, approval wait |
| Cost | Cost/successful outcome, input/output tokens, tool/API cost, cache hit, wasted retry cost, specialist fan-out cost |
| Human load | Approval frequency, approval dwell time, escalation rate, override rate, reviewer agreement |
| Operations | SLO attainment, trace completeness, rollback time, mean time to diagnose/recover, dead-letter backlog |

### Trace and replay semantics

* Propagate W3C traceparent/tracestate across HTTP, queues, MCP, and A2A. Use span links when work is triggered asynchronously or crosses an independently rooted remote trace.
* Record model route/version, prompt/context hashes, tool/agent versions, policy decision IDs, artifact/effect references, retry/cancel/replay flags, cost, and timing. Do not require hidden chain-of-thought.
* Operational replay reuses recorded activity outputs and cannot create live effects. A fork with changed model/prompt/tool is a new run and explicitly mocks or reauthorizes external access.
* Deterministic correctness checks outrank model graders. Store grader prompt/model/version, raw score evidence, and inter-rater calibration so a later drift analysis is possible.

### Scalability, retention, and cost

* Decouple application latency from backend analytics with regional collectors, bounded queues, batching, compression, retry, and encrypted spill. Protected effect/audit events follow a loss-intolerant path distinct from sampled diagnostics.
* Partition trace storage by tenant + time; index only operationally useful low-cardinality fields. Put high-cardinality attributes and content in columnar/object storage with controlled query paths.
* Use tiered sampling: 100% metadata for runs/effects/policy/approvals; 100% detailed traces for failures, security findings, canaries, R3/R4, and operator-selected runs; adaptive/statistical detail for routine success.
* Move older traces from hot index to compressed object storage, preserving searchable summaries and evidence pointers. Retention differs for telemetry, evaluation fixtures, and legal/audit records.
* Run evaluations on dedicated queues with tenant/candidate budgets, reproducible seeds, provider-rate awareness, and early stop when statistical or hard safety failure criteria are met.
* Compute metrics from events/spans through streaming aggregation rather than querying raw traces for dashboards. Control label cardinality; never use user IDs, prompts, or URLs as metric labels.
* Preserve sampling weights and selection reasons for online estimates. Compare by task/risk/data/source/model slices so improvements in average score cannot hide a critical regression.
* Monitor the observability system itself: collector drop rate, redaction failure, trace completeness, broken links, ingest lag, hot-store cost, evaluator disagreement, and dataset leakage.

|  |
| --- |
| **OBSERVABILITY TIP**  Trace the decision, not only the call. Latency and token counts tell you a run was slow; they never tell you why it was wrong. Record which context manifest was authorized, which policy applied, and which branch was taken — those attributes are what let a trace answer a question weeks later. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Telemetry maturity | OTLP and the general span model are mature, but the dedicated OpenTelemetry GenAI semantic conventions are still Development. Version the mapping and retain a stable internal event schema. | OTEL-GENAI |

Evidence anchors: OTEL-GENAI; MLFLOW-TRACE. Full URLs, authority, version, and scope appear in Appendix M.

|  |
| --- |
| **OBSERVABILITY TIP**  Tag every trace with the identifiers your system of record uses — run, tenant, risk class. A trace that cannot be joined to the business record it affected is a performance artifact, not an audit trail. |

## Implementation reference


### MLflow tracing integration

[[EXAMPLE:mlflow-trace-configuration]]

## Debugging playbook

1. Start at the SLO violation and walk the critical path span by span.
2. Correlate queue, workflow, model, retrieval, tool, approval, and effect timing.
3. Compare diagnostic trace completeness with required audit evidence.

## Production checklist

**✓** Run, workflow, agent, model, retrieval, policy, tool, approval, effect, and human spans share stable causal identifiers.

**✓** Asynchronous relationships use span links and domain IDs.

**✓** Sensitive content is excluded, tokenized, or access-controlled.

**✓** Collector outage does not stop protected workflow state or required audit evidence.

**✓** SLOs expose critical-path latency, cost, errors, retries, human dwell, and unknown effects.

## Exercises

1. Define the canonical trace attributes for Northstar.
2. Create a dashboard that separates machine latency from human dwell.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| What is the root trace for a long-running run? | A durable run trajectory linked across workflow tasks, model calls, tools, messages, approvals, effects, and restarts using stable IDs and span links. |
| Why is parent-child nesting insufficient? | Asynchronous queues, retries, fan-out, resumed waits, and remote agents create causal relationships that require links and domain identifiers. |
| Which data should not be put blindly into traces? | Secrets, credentials, raw sensitive prompts, retrieved content, tool payloads, and regulated identifiers; record governed references and hashes where possible. |
| How do traces support debugging? | They expose critical path, state transitions, versions, policy decisions, retries, cost, evidence lineage, and the first divergent step. |
| Why keep audit separate? | Audit has stronger completeness, integrity, access, and retention obligations than sampled diagnostic telemetry. |


## Transition to Chapter 27

Tracing explains what happened; Chapter 27 determines whether the trajectory and outcome were acceptable and whether a change is safe to ship.

# 27 — Evaluation, Testing, and Debugging with MLflow

> **Evidence note.** The evaluation architecture maps to current capabilities documented by MLflow, DeepEval, Ragas, LangSmith, and OpenAI. Tool names and APIs are examples; the durable contract is dataset + release graph + scorer versions + trace/effect evidence. [R20][R21][R22][R24][R25][R26]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  A prompt change improves average answer quality but introduces one unauthorized tool trajectory in a low-volume region. Aggregate accuracy hides the regression; slice-aware trajectory evaluation blocks the release. |

|  |
| --- |
| **DESIGN DECISION**  Gate releases on immutable datasets, executable trajectory checks, calibrated judges, slices, failures, and baseline comparisons. |

## What this chapter delivers

Evaluate outcomes and trajectories using immutable datasets, executable scorers, calibrated judges, failure simulation, and release gates.

## Solution blueprint


Figure 19. Evaluation, Testing, and Debugging with MLflow.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Evaluation Service and release gate | production evidence to development corpus | dataset version · scorer pool · slice | one case and candidate release | EvaluationCase · Feedback · ReleaseDecision |

## Evaluation-driven development

An agent evaluation case includes input, initial state, user simulation or messages, expected outcome properties, allowed and forbidden tools, required evidence, maximum budgets, failure injections, and slice tags. The result includes final output, complete trajectory, artifacts, policy decisions, effects, human events, latency, cost, and terminal state.

MLflow 3.15.x supports GenAI evaluation, trace-based scorers, code-based scorers, LLM judges, human feedback, and OpenAI Agent tracing integration. Version 3.15.2 adds immutable evaluation-dataset versions and scorer ensembles within the requested 3.15 line. This book pins 3.15.2; newer overall MLflow releases may exist and require separate compatibility validation.

### Evaluation pyramid

* **Contract and unit:** schemas, reducers, compilers, capability subsets, idempotency, deterministic acceptance.
* **Simulation:** multi-turn users, tool fixtures, clock, failures, approvals, and remote peers.
* **Trajectory:** correct tools, order, evidence, policy, budgets, handoffs, waits, and effects.
* **Threat:** prompt injection, exfiltration, confused deputy, cross-tenant, SSRF, malicious artifact, approval tampering.
* **Reliability:** retries, timeouts, duplicates, out-of-order events, unknown effects, cancellation, replay, regional recovery.
* **Performance:** queue age, tokens, tool calls, latency, cost per success, concurrency, fairness.
* **Canary and production:** bounded exposure, online monitors, human feedback, failure mining, rollback.

Use executable scorers wherever the expected property is computable. Calibrate model judges against human labels, measure variance and bias, version their complete configuration, and never make them the sole authority for security or transaction correctness.

### Testing and evaluation pyramid

| **Level** | **What to test** | **Method** |
| --- | --- | --- |
| Unit | Schemas, plan compiler, policy rules, context filters, budget logic, redaction, idempotency | Deterministic tests and property-based fuzzing |
| Contract | Tool/MCP/A2A schemas, auth scopes, errors, compatibility, effect receipts | Consumer/provider contract tests against mocks and sandboxes |
| Component | Agent behavior with controlled models/tools | Seeded scenarios, golden trajectories, metamorphic tests |
| Workflow | Retries, replay, pause/resume, cancellation, compensation, code-version migration | Fault injection and workflow-engine test harness |
| Simulation | Multi-turn users, changing data, delayed events, partial failures | Stateful environment and user simulators; many seeds |
| Security/adversarial | Prompt injection, malicious files/tools/agents, exfiltration, privilege escalation | AgentDojo-style suites, red-team corpora, sandbox escape and DLP tests |
| Regression | Known wins/failures across pinned versions | Offline datasets; outcome + trace graders; statistical confidence |
| End-to-end | Real identity, source ACLs, queues, approvals, effects, audit | Staging tenant with synthetic data; canary in production |
| Continuous | Drift, novel failures, cost/latency, policy incidents | Sampled online evals, human review, alerts, incident-to-test loop |

Use deterministic validators as the gold standard where possible. LLM-as-judge is useful for nuanced rubrics but must be calibrated against humans, blinded to candidate identity, tested for variance/bias, and never be the sole gate for safety-critical correctness. Measure repeated-run reliability (pass^k or equivalent), not just best-of-one success.

### Detailed design — APIs, data model, and scalability

### Component boundaries

| **Component** | **Responsibility** |
| --- | --- |
| Telemetry Gateway/Collector | Receive OTLP traces, metrics, and logs; enrich with tenant/run metadata; redact and route |
| Trace Index | Fast causal lookup by run, task, effect, version, error, tenant, and time |
| Content Vault | Separately encrypted optional prompt/output/tool payloads referenced by hash |
| Metrics/SLO Pipeline | Aggregate low-cardinality service, quality, safety, cost, and human-load indicators |
| Evaluation Registry | Version datasets, cases, rubrics, graders, baselines, and release thresholds |
| Evaluation Orchestrator | Run candidates across seeds/environments, grade, compare, and produce confidence intervals |
| Replay/Fork Service | Reconstruct a safe sandbox run from manifest, history, artifacts, and recorded effects |
| Failure Mining Service | Cluster traces/incidents and propose curated regression cases for human review |

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /otlp/v1/traces, /metrics, /logs | Standard OTLP ingestion with workload authentication, tenant binding, size/rate limits, and redaction |
| GET /v1/runs/{run\_id}/trace | Return role-redacted causal graph, span summaries, links, and authorized content handles |
| POST /v1/eval-datasets | Create immutable/versioned dataset from approved cases and provenance |
| POST /v1/eval-runs | Evaluate a release candidate against dataset/rubric, seeds, model routes, environment, and budget |
| GET /v1/eval-runs/{eval\_run\_id}/comparison | Compare candidate/baseline metrics, confidence intervals, slices, regressions, cost, and trace deltas |
| POST /v1/release-gates:evaluate | Apply risk-tiered thresholds and return pass/fail/waiver-required with evidence |
| POST /v1/runs/{run\_id}:forkReplay | Create a sandbox fork at checkpoint; external effects are mocked/read-only unless separately authorized |
| POST /v1/regression-cases:propose | Submit a production failure/cluster for de-identification, labeling, leakage review, and dataset approval |

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| TraceIndex | trace/run IDs, tenant, start/end, root service, manifest/version set, status/risk, error/effect/approval flags, cost/tokens; no sensitive body by default |
| SpanEnvelope | trace/span/parent or links, kind, service/operation, start/duration, status, normalized attributes/events, content refs, sampling class |
| ContentBlob | encrypted URI/hash, tenant/key, classification, redaction profile, authorized roles, retention, source span; stored separately |
| EvalDatasetVersion | dataset/version/digest, purpose, cases, slices, provenance, license/privacy/leakage review, owner, lifecycle |
| EvalCase | case ID, input/environment fixtures, expected invariants/artifacts/trajectory constraints, rubric, risk tags, source/provenance |
| EvalRun | candidate/baseline manifest digests, dataset, seeds, grader versions, environment, status, aggregate resource usage |
| EvalScore | eval/case/attempt, metric, score, confidence/evidence, deterministic or grader type/version, latency/cost |
| ReleaseGateDecision | candidate, risk tier, thresholds, slice results, decision, waiver, approvers, evidence refs; immutable |
| ProductionSample | run/trace, sampling reason/weight, consent/privacy handling, evaluation status, incident/failure cluster |

|  |
| --- |
| **BEST PRACTICE**  Build the evaluation set from production failures, not from imagined ones. Every incident should end by contributing a case. A suite assembled up front measures what you expected to be hard; a suite grown from incidents measures what actually is. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| MLflow baseline | This book pins MLflow 3.15.2 as a reproducibility baseline for its examples. It is not labeled latest; feature availability, experimental status, and compatibility must be re-verified against release notes and current documentation before implementation. | MLFLOW-3152; MLFLOW-MCP |
| Evaluation limit | A passing model judge is probabilistic evidence, not proof. Security, authorization, schema, budget, effect, and acceptance invariants remain deterministic release blockers. Protect against benchmark leakage and tune judges with human feedback. | MLFLOW-EVAL; NIST-GAI |

Evidence anchors: MLFLOW-3152; MLFLOW-EVAL; NIST-GAI. Full URLs, authority, version, and scope appear in Appendix M.

|  |
| --- |
| **COMMON PITFALL**  Trusting an LLM judge you have not calibrated against human labels. A judge is a model with its own failure modes and its own drift. Measure its agreement with human raters on a held-out set, re-measure when you change the judge's model, and report the agreement alongside any score it produces. |

## Implementation reference


### MLflow trajectory evaluation

PYTHON · implementation excerpt

```python
from __future__ import annotations
import os
from typing import Literal
import mlflow
from mlflow.entities import Feedback, SpanType, Trace
from mlflow.genai import scorer
from mlflow.genai.judges import make_judge
from mlflow.genai.scorers import Correctness, Guidelines, ToolCallCorrectness, ToolCallEfficiency

def no_unknown_effects(trace: Trace) -> Feedback:
    unknown = [
        span for span in trace.search_spans()
        if span.attributes.get("effect.state") == "unknown"
    ]
    return Feedback(
        name="no_unknown_effects",
        value=not unknown,
        rationale="No unresolved effects" if not unknown else f"{len(unknown)} unknown effects remain",
    )

def evaluate_agent(predict_fn, dataset: list[dict[str, object]]):
    return mlflow.genai.evaluate(
        data=dataset,
        predict_fn=predict_fn,
        scorers=[
            Correctness(),
            Guidelines(name="grounded", guidelines="Every material claim cites authorized evidence."),
            ToolCallCorrectness(),
            ToolCallEfficiency(),
            no_unknown_effects,
            tool_trajectory_judge,
        ],
    )
```

## Debugging playbook

1. Reproduce the failing trace with exact dataset, release, model route, tool, and policy versions.
2. Find the first divergent decision rather than only comparing final text.
3. Slice scores by risk, region, tool, failure mode, and tenant class.

## Production checklist

**✓** All run components link into one causal trajectory.

**✓** Operational telemetry, restricted content, and complete immutable audit evidence are separated.

**✓** Evaluation covers outcome, trajectory, reliability, security, latency, cost, human load, and operations by slice.

**✓** Behaviorally relevant artifacts are pinned in a release bundle and promoted through executable gates.

**✓** Use-case inventory names owners, authority, data, vendors, controls, exceptions, incidents, review dates, and evidence.

## Exercises

1. Create a five-case immutable evaluation dataset with trajectory expectations.
2. Implement a deterministic scorer that rejects unknown effects and missing approvals.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why is final-answer evaluation insufficient for agents? | A plausible answer can hide unauthorized retrieval, wrong tools, excessive cost, retry waste, unsafe handoffs, duplicate effects, or missing approval; evaluate the complete trajectory. |
| How do telemetry and audit differ? | Telemetry diagnoses and may be sampled; audit proves required protected decisions and effects with stronger completeness, integrity, access separation, and retention. |
| When are model judges appropriate? | For nuanced quality with versioned rubrics, human calibration, bias tests, repeated runs, and blinding—not as sole authority for security, transactions, or computable correctness. |
| What belongs in a release bundle? | Agent and prompt, runtime adapter, workflow build, model route and fallbacks, tool and policy versions, schemas, images, knowledge strategy, evaluations, rollout, and rollback policy. |
| How do you roll back without breaking active runs? | Stop new assignment, restore the prior environment binding, keep build-compatible workers for pinned histories, reconcile side effects, and migrate only through an explicit tested plan. |


## Transition to Chapter 28

Evaluation supplies comparable evidence; Chapter 28 turns that evidence into a governed learning and improvement lifecycle.
