# PART X — CONTINUOUS LEARNING

This Part closes the evidence-to-change loop. It separates bounded runtime adaptation from governed offline improvement and defines who may recommend, validate, approve, deploy, monitor, and reverse changes to prompts, models, tools, memory, routing, workflows, and architecture.

# 28 — Continuous Learning and Improvement Architecture

## Closed-loop capability

Continuous improvement joins production evidence to versioned change and release. It does not let an agent rewrite its prompt, memory policy, permissions, evaluator, or code and then certify itself.

[[DIAGRAM:learning-loop|Figure 28-1 — Observe → Measure → Detect → Diagnose → Recommend → Validate → Approve → Deploy → Monitor → Learn]]

| **Stage** | **Work and durable output** | **Automation boundary** |
| --- | --- | --- |
| Observe | Join traces, context, tools/effects, feedback, corrections, incidents, cost, latency, outcome into ObservationRecord | Capture/redact/sample automatically; approve sensitive purpose/access |
| Measure | Run deterministic invariants and quality, safety, retrieval, tool, trajectory, SLO, economics metrics into EvaluationResult | Approved scorers automate; humans define truth/threshold/calibration |
| Detect | Rules, anomaly, drift, slice regression, recurring corrections into DetectionEvent | Alert/contain within approved envelope |
| Diagnose | Compare successful/failed traces, first divergence, structural/semantic clusters into causal hypothesis | Tools rank; accountable owner confirms cause/business meaning |
| Recommend | Smallest candidate, predicted benefit, risk, affected contracts, rollback into ChangeBundle draft | Generate drafts; never self-approve/mutate production |
| Validate | Replay, simulation, unit/contract/security/privacy/adversarial/load/cost/compatibility tests into ValidationReport | CI automates; owners approve datasets, exceptions, residual risk |
| Approve | Risk class and domain/security/privacy/operations decision into PromotionDecision | Only pre-approved low-risk changes auto-approve |
| Deploy | Immutable build, bindings, shadow/canary, rollback into ReleaseManifest/deployment | Progressive delivery within approved policy |
| Monitor | Compare canary/production to baseline across quality, safety, reliability, cost, business | Auto-halt/rollback on tested stop condition |
| Learn | Record causal result, curate regressions, update taxonomy/runbook into LearningRecord | Metadata may automate; data/policy/architecture changes require governance |

## Runtime adaptation versus controlled offline improvement

[[DIAGRAM:runtime-offline|Figure 28-2 — Runtime adaptation and offline improvement boundary]]

Runtime adaptation selects only pre-approved routes/fallbacks, reduces optional context, sheds load, stops a loop, asks for input, escalates, or rolls back inside a fixed envelope. It cannot expand permissions, purpose, data access, spend, tools, or model allowlists. Offline improvement creates a new immutable release and may change prompts, context/RAG, memory, tools, skills, model selection, routing, deterministic code, agent topology, workflows, and system architecture after evaluation and approval.

## Improvement matrix

| **Layer** | **Evidence** | **Candidate** | **Validation / approval** |
| --- | --- | --- | --- |
| Prompts | Omissions, conflicts, unsupported claims | Clarify responsibility, examples, evidence, stop rules | Golden/adversarial replay; behavior/policy review |
| Context/RAG | Recall/precision, stale/poisoned source, injection correlation | ACL/freshness/ranking/dedup/token/source changes | Retrieval/faithfulness/security tests; data-owner approval |
| Memory | Correction, leakage, stale/poisoned retrieval | Eligibility, purpose, scope, TTL, verification, deletion | Privacy/security/longitudinal replay |
| Tools | Wrong choice/args, timeout/retry/unknown effect | Narrow schema/catalog, preconditions, idempotency/reconcile | Contract/failure/load/security; effect/permission approval |
| Skills | Version-specific or inconsistent behavior | New immutable Skill/dependencies/examples/acceptance | Skill certification and domain owner |
| Model selection | Quality/cost/latency/refusal/schema drift | Eligibility, threshold, cascade, fallback, context window | Full route evaluation, privacy/residency, canary |
| Routing | Misroute/escalation/capacity imbalance | Calibrate, deterministic pre-router, fallback/escalation | Shadow/counterfactual; authority/ownership review |
| Deterministic code | Repeated stable low-entropy model decision | Extract rule, lookup, calculation, parser, transform | Unit/property/exception tests and domain approval |
| Agent topology | Duplicate work, fan-out/handoff, unclear owner | Merge agents, supervisor/task service, specialization change | Simulation, ownership/authority, migration review |
| Workflows | Loops, stuck joins, weak recovery | State, deadline, join, stop, compensation, degraded mode | Replay/concurrency/recovery/RTO-RPO and operations |
| System architecture | Failure recurs across apps/controls | Platform service, contract, gateway, boundary, policy redesign | Architecture/security/privacy and migration evidence |

## Evaluation ecosystem and metrics

OpenTelemetry/OpenInference traces provide portable telemetry. DeepEval and Ragas cover trajectory, component, tool, RAG, faithfulness, and goal metrics. MLflow supports datasets, evaluators, human/programmatic feedback, experiments, and monitoring. Phoenix supports traces, annotations, datasets, prompt experiments, and replay. LangSmith supports offline/online evaluation and production-trace-to-dataset workflows. Normalize all into platform-owned EvaluationResult; no framework score is release authority.

Measure task success and deterministic acceptance, correctness, faithfulness, hallucination/unsupported-claim rate, tool-selection precision/recall/F1, argument correctness, retrieval relevance/precision/recall/freshness/evidence coverage, plan quality/adherence, step efficiency, p50/p95/p99 latency by component, tokens, cost per request/accepted outcome, retry amplification, failure/unknown effect, human correction/override/escalation/fatigue, user satisfaction, and business outcome.

## Regression and safe automation

Every material failure/correction becomes a candidate case after privacy/security/purpose review. Reduce to smallest reproducible cause, define expected outcome/invariants/trajectory/cost/latency, version dataset/evaluator, and run in CI, staging, shadow, and canary. Automate capture, approved redaction/scoring, anomaly detection, clustering, draft recommendations, tests, sandbox/canary, halt, and rollback within envelope. Require human governance for permission/policy/data/memory purpose/protected effects/model allowlist/topology/architecture/evaluator truth/training data/exceptions/wider promotion. Prohibit expanding authority, disabling controls, editing audit evidence, changing approval requirements, or promoting self-authored behavior.


## Transition to Chapter 29

The improvement loop proposes and validates change; Chapter 29 assigns decision rights, risk tiers, approvals, exceptions, and accountability.
