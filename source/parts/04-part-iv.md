# PART IV — PATTERNS AND ANTI-PATTERNS

This Part is the working catalogue. It moves from the loop shapes that solve real problems to the architecture shapes that quietly create them, and pairs every failure with a measurable replacement.

# 10 — ReAct: Bounded Reason–Act–Observe Loops

> **Evidence note.** ReAct was introduced as a prompting paradigm that interleaves reasoning and action; its reported benchmark results motivate the loop, not an assertion that unrestricted production autonomy is safe. [R01]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  An analyst asks why a supplier is blocked. One retrieval is insufficient: the system may need the profile, a screening artifact, and a policy explanation. A bounded ReAct loop is appropriate because the next information need depends on the previous observation. |

|  |
| --- |
| **DESIGN DECISION**  Use ReAct only for information-dependent next steps and impose external turn, tool, time, cost, and no-progress limits. |

## What this chapter delivers

Implement ReAct with external budgets, governed tools, no-progress detection, and deterministic acceptance.

## Solution blueprint


Figure 4. ReAct: Bounded Reason–Act–Observe Loops.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| External loop controller and acceptance engine | observation/model and model/tool | turn · tool permit · run budget | one bounded loop | AgentDecision · Observation · ReActLimits |

## Why ReAct is useful—and expensive

[[DIAGRAM:pattern-react|Figure 10-1 — Bounded ReAct: the loop is inside, the limits are outside]]

Read the figure for what is *not* in the loop. The controller admits each turn and owns the budgets; a mutation leaves as a proposal rather than executing inline; and the decision to stop belongs to the acceptance engine, not to the model's wording.

ReAct interleaves reasoning, action, and observation. Its value is conditional adaptivity: after reading the supplier profile, the agent may decide that a regional registry lookup is unnecessary, or that a contradictory address requires another source. The pattern becomes harmful when it substitutes an unconstrained loop for a known process.

Northstar stores only typed decisions, tool intents, observations, evidence references, and stop reasons—not private chain-of-thought. The external controller maintains counters and normalized signatures. If an agent repeats the same tool and canonical arguments against the same source revision, or if accepted evidence does not change across turns, the controller records no progress and terminates or escalates.

### Acceptance and failure semantics

A ReAct activity can return answer, needs\_input, delegate, proposed\_action, budget\_exhausted, or failed. A mutating action never executes inside the unconstrained loop; it becomes a proposal for deterministic policy, approval, effect, and workflow processing. If a read tool times out, bounded retry may be safe. If a mutation times out, the loop stops because the effect is unknown.

### Capacity model

Plan capacity in turns per successful outcome, not only requests per second. Track model tokens, tool calls, connector time, observation bytes, and repeated-action rate. Per-tenant permits and hard per-run limits prevent one pathological loop from consuming a worker pool.

|  |
| --- |
| **PERFORMANCE AND COST**  A ReAct loop's cost is set by its trajectory, not its prompt. Each observation re-enters the context, so an n-step loop is roughly quadratic in tokens. Cap the step count, summarize observations before they re-enter, and measure cost per *completed task* rather than per call — a cheap call that loops eight times is not cheap. |

## Grounding, corrections, and evidence boundary

|  |
| --- |
| **EVIDENCE BOUNDARY**  This chapter presents an architectural recommendation, not a protocol mandate. Validate the pattern against the workload, threat model, evaluation set, and strongest simpler baseline. |

Evidence anchors: REACT; NIST-GAI. Full URLs, authority, version, and scope appear in Appendix K.

|  |
| --- |
| **COMMON PITFALL**  Unbounded retries disguised as reasoning. When a tool fails and the model is free to try again, the loop can burn its whole budget rediscovering the same error. Return failures as typed data the model can read, cap attempts per tool, and make the cap a run-level budget rather than a per-call one. |

## Pattern reference — ReAct

|  |
| --- |
| **PROBLEM**  The system cannot know every information-gathering step in advance because the next action depends on the previous observation. |

### Architecture and flow

A bounded controller alternates model decision and governed tool invocation. The controller—not the model—owns turns, budgets, state, repeated-action detection, and acceptance.

1. Load goal, authorized context, budgets, and acceptance criteria.
2. Ask for one typed action or terminal disposition.
3. Validate and execute the action at the Tool Gateway.
4. Sanitize and append the observation.
5. Accept, continue, request input, or terminate on an external rule.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for exploratory retrieval, diagnosis, or research with a small eligible tool set and measurable stop conditions. | Avoid for known workflows, single retrievals, protected commits, or open-ended browsing without meaningful limits. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Adaptivity | Handles unknown paths; increases latency, cost, and trajectory variance. |
| Intermediate observations | Improves grounding; increases attack surface and context pressure. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Tool ping-pong | Normalized repeat signatures and no-progress threshold. |
| Context poisoning | Treat observations as untrusted, provenance-labeled data. |
| Budget exhaustion | External turn, call, token, time, and cost enforcement. |

### Minimum observability

* turn index
* decision type
* eligible tools
* action-observation hash
* information gain
* remaining budgets
* stop reason

## Implementation reference


[[EXAMPLE:bounded-react-loop]]

### Bounded ReAct controller

[[EXAMPLE:react-engine#core]]

## Debugging playbook

1. List every turn with normalized action, observation, token, time, and cost deltas.
2. Identify the first repeated action-observation signature.
3. Check whether the stop decision came from acceptance criteria or model wording.

## Production checklist

**✓** The information need truly requires iterative observation.

**✓** The controller owns limits, state, tool invocation, and acceptance.

**✓** Observations are typed, sanitized, versioned, and provenance-linked.

**✓** Repeat-action and no-progress signatures are detected.

**✓** Unknown effects or budget exhaustion terminate safely.

## Exercises

1. Add information-gain and repeat-signature stopping to the reference ReAct loop.
2. Compare a one-shot retrieval design with ReAct for the same supplier question.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| When is ReAct the right pattern? | When the next information need genuinely depends on a verified prior observation and the loop can be bounded. |
| Why must the controller sit outside the model? | It owns budgets, tool eligibility, invocation, state, no-progress detection, and terminal transitions. |
| How do you stop a ReAct loop that keeps rephrasing the same request? | Normalize action-observation signatures, count repeats, evaluate information gain, and terminate or escalate at a deterministic threshold. |
| What should an observation contain? | A typed, sanitized result or artifact reference with provenance, version, classification, and explicit error semantics. |
| When should ReAct not be used? | For a known workflow, a single retrieval, a protected transaction, or a task whose acceptance can be computed directly. |

## Transition to Chapter 11

A bounded reason–act loop handles local uncertainty; Chapter 11 adds routing and handoff when known paths or specialists should own the work.

# 11 — Routing, Triage, and Handoffs

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Some requests are policy questions, others are document defects, screening disputes, or protected onboarding actions. Northstar needs routing, but it also needs to know when responsibility actually transfers and who owns cancellation, deadlines, and the final response. |

|  |
| --- |
| **DESIGN DECISION**  Use deterministic route eligibility and fallback; record handoff as an explicit ownership transition. |

## What this chapter delivers

Distinguish route selection from ownership transfer and design confidence, fallback, and authority semantics.

## Solution blueprint


Figure 5. Routing, Triage, and Handoffs.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Route service and workflow ownership record | classifier to privileged route; owner transfer | route class · specialist queue | one route or handoff | RouteDecision · Handoff · CapabilityEnvelope |

## Selection is not authority

[[DIAGRAM:pattern-routing|Figure 11-1 — Routing selects a specialist; policy decides whether it may act]]

A router reduces heterogeneity by selecting an implementation: policy explanation, document validation, sanctions review, or human triage. The model may classify semantic intent, but the eligible set is assembled first from purpose, authority, risk, data region, release status, service health, and capacity. A route cannot grant a capability that was absent from the run envelope.

A **handoff** is a different event. It changes the current owner of an interaction or task. Northstar records old owner, new owner, state version, unresolved obligations, artifact references, child capability envelope, deadline, and cancellation lineage. The recipient acknowledges or rejects the transfer. Until acknowledgment, the previous owner remains accountable.

### Confidence and fallback

Confidence is calibrated on a versioned domain dataset. Below a threshold, the route service requests clarification, applies a deterministic safe default, or sends the request to human triage. High confidence does not bypass policy. For privileged routes, both route eligibility and exact invocation authorization are required.

### Anti-patterns

* **Persona routing:** selecting among nearly identical prompts with no different capability boundary.
* **Handoff by chat message:** telling another agent “you own this now” without durable state.
* **Privilege through selection:** showing a model an admin route and treating its selection as authorization.
* **No fallback:** forcing a best guess even when the request is out of distribution.

## Grounding, corrections, and evidence boundary

|  |
| --- |
| **EVIDENCE BOUNDARY**  This chapter presents an architectural recommendation, not a protocol mandate. Validate the pattern against the workload, threat model, evaluation set, and strongest simpler baseline. |

Evidence anchors: OAI-TOOLS; A2A-101. Full URLs, authority, version, and scope appear in Appendix K.

## Pattern reference — Routing

|  |
| --- |
| **PROBLEM**  Different requests need different workflows, models, Skills, agents, risk controls, or human queues. |

### Architecture and flow

A classifier proposes a route from a precomputed eligible catalog. A deterministic validator checks confidence, policy, health, capacity, and fallback before selection.

1. Build the eligible route set.
2. Classify the request and return route, confidence, and reason.
3. Validate thresholds and constraints.
4. Select the route or deterministic fallback.
5. Measure outcome by route and slice.

| **Use when** | **Do not use when** |
| --- | --- |
| Use when candidate paths have materially different capabilities, owners, SLOs, cost, or risk. | Avoid model routing when a stable deterministic rule is sufficient or misrouting has unacceptable consequences. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Specialization | Can improve quality and cost; creates taxonomy, calibration, and drift work. |
| Learned classification | Handles semantic ambiguity; requires fallback and monitoring. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Low-confidence guess | Clarify, default, or human triage. |
| Route drift | Versioned datasets and confusion-matrix monitoring. |
| Privileged route selection | Eligibility before classification and exact authorization after selection. |

### Minimum observability

* candidate routes
* eligibility removals
* confidence
* validator reason
* fallback
* route outcome

## Pattern reference — Handoffs

|  |
| --- |
| **PROBLEM**  Another agent or human must become the current interaction or task owner rather than merely provide an answer to the original controller. |

### Architecture and flow

The current owner creates a typed transfer containing state references, unresolved obligations, narrowed authority, deadline, cancellation lineage, and acceptance contract.

1. Decide that ownership—not just expertise—must transfer.
2. Persist the handoff proposal.
3. Validate recipient, authority, compatibility, and capacity.
4. Atomically change owner and emit an event.
5. Require the new owner to acknowledge or reject.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for explicit responsibility transfer across specialist, trust, organizational, or channel boundaries. | Use an agent-as-tool when the parent still owns the outcome; use a durable child task when independent recovery is required without conversational transfer. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Clear specialization | Introduces ownership transitions and context-transfer risk. |
| Independent interaction | Reduces supervisor bottlenecks; complicates cancellation and accountability. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Orphaned task | Atomic ownership state and acknowledgment timeout. |
| Authority expansion | Child grant intersection and exact reauthorization. |
| Context loss | Typed artifact and obligation references instead of transcript copying. |

### Minimum observability

* old and new owner
* handoff reason
* grant lineage
* state and artifact refs
* acknowledgment
* deadline and cancellation

## Implementation reference


[[EXAMPLE:routing-handoff]]

### Deterministic route validation

🐍 · implementation excerpt

```python
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol
from .contracts import AgentDecision

class Route:
    name: str
    capability: str
    maximum_risk: int

class DeterministicRouter:
    def __init__(self, routes: tuple[Route, ...]) -> None:
        self.routes = {route.name: route for route in routes}

    def accept_model_route(
        self, proposed: str, allowed_capabilities: frozenset[str], risk: int
    ) -> Route:
        route = self.routes[proposed]
        if route.capability not in allowed_capabilities or risk > route.maximum_risk:
            raise PermissionError("proposed route is outside the run envelope")
        return route
```

## Debugging playbook

1. Recompute the eligible route set from recorded purpose, authority, health, and risk.
2. Inspect the confidence threshold and fallback actually used.
3. Verify ownership and cancellation after a handoff.

## Production checklist

**✓** The eligible route set is computed before model selection.

**✓** Confidence, ambiguity, fallback, and default-deny behavior are explicit.

**✓** Routing and handoff are separate contracts.

**✓** Ownership, state, authority, deadlines, and cancellation transfer atomically.

**✓** Route decisions and outcomes are measured by slice.

## Exercises

1. Design a route contract with confidence, reason codes, fallback, and version.
2. Model a handoff that transfers a task without broadening authority.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| How does routing differ from a handoff? | Routing selects an eligible implementation; handoff transfers responsibility and therefore requires ownership, state, authority, and cancellation semantics. |
| Should the model see every route? | No. Give it a minimal eligible set derived from purpose, authority, health, region, risk, and release policy. |
| What should happen below a confidence threshold? | Use a deterministic default, request clarification, or route to a human queue; do not select a privileged specialist by guesswork. |
| How do you make routing debuggable? | Record candidates, eligibility filters, proposed route, confidence, validator decision, fallback, version, latency, and outcome. |
| When is a static router better? | When classes are stable, risk is high, compliance requires predictability, or a simple rule already separates the work. |

## Transition to Chapter 12

Routing selects among known capabilities; Chapter 12 addresses tasks whose decomposition must itself be proposed and validated.

# 12 — Planning and Plan–Execute

> **Evidence note.** Published engineering guidance distinguishes predefined workflows from model-directed agents and recommends adding complexity only when simpler compositions are insufficient. [R27]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  A supplier with four subsidiaries, missing tax evidence, and two regional checks requires adaptive sequencing. Northstar lets a planner propose a graph but compiles that graph before any node becomes schedulable. |

|  |
| --- |
| **DESIGN DECISION**  Use a typed Plan IR and deterministic compiler; freeze committed past work across plan revisions. |

## What this chapter delivers

Compile model-proposed plans into authorized, resource-feasible, replayable execution graphs.

## Solution blueprint


Figure 6. Planning and Plan–Execute.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Plan Service and durable workflow | planner proposal to deterministic compiler | plan node · workload queue | one node and one plan revision | CandidatePlan · CompiledPlan · PlanRevision |

## Planning is compilation, not permission

[[DIAGRAM:pattern-planning|Figure 12-1 — A candidate plan becomes typed IR and is validated before any step runs]]

The planner describes desired work; the compiler determines whether that work is legal and executable. Northstar Plan IR nodes name capability requirements rather than concrete credentials. Compilation binds each requirement to an eligible Skill and tool release, verifies input/output schemas, calculates critical path and maximum cost, checks graph and terminal properties, and emits a signed immutable plan revision.

Resource feasibility matters. A valid graph can still miss the deadline if it requires too many browser sessions, serialized vendor calls, or human approvals. The compiler checks workload queues, concurrency classes, rate limits, regional placement, and time windows before committing a plan. Scheduling remains a workflow responsibility.

### Replanning contract

New evidence can invalidate future work. Replanning starts from an explicit set of immutable facts: accepted artifacts, committed effects, approval decisions, and current resource versions. The new revision includes a diff, rationale, superseded nodes, reused artifacts, changed budget, and compiler evidence. It cannot rewrite history.

## Planning, dynamic execution, and deterministic boundaries

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Allow useful adaptation without letting the model rewrite policy, invent capabilities, or turn every step into expensive nondeterministic reasoning. |
| Why it is difficult | A plan is based on incomplete information; tool results change the world; models confuse a coherent narrative with a feasible, authorized execution graph. |
| Design alternatives | Fixed workflow; rules engine; model router; plan-and-execute; ReAct loop; graph search; planner/executor/critic; code generation. |
| Recommended architecture | Use a typed, versioned plan IR. The model proposes goals, dependencies, and candidate capabilities; deterministic validators compile the plan into workflow nodes. Runtime adaptation creates an auditable plan revision bounded by the original authority and budget. |
| Trade-offs | Fixed workflows maximize predictability but cover less ambiguity. Dynamic planning increases task coverage and maintenance flexibility while raising evaluation, security, and cost burdens. |
| Failure scenarios | Infinite replan loop; plan references nonexistent tool; planner broadens scope; stale precondition; generated code bypasses gateway; critic repeatedly rewrites a correct result. |
| Enterprise example | An incident agent may choose which diagnostic queries to run and revise hypotheses as evidence arrives, but production changes remain pre-modeled operations with change-window, policy, and approval checks. |

### What should be agentic?

| **Work** | **Recommended mechanism** | **Reason** |
| --- | --- | --- |
| Interpret ambiguous intent | LLM with structured output | Semantic ambiguity is the value of the model |
| Retrieve and synthesize heterogeneous evidence | LLM + governed retrieval | Requires semantic selection and explanation |
| Propose decomposition or hypotheses | LLM planner | Subtasks are not fully known in advance |
| Choose among a small stable set of routes | Rules/classifier first; LLM fallback | Lower cost and variance for common cases |
| Validate types, required fields, ranges, invariants | Deterministic code/schema | Must be complete, fast, and reproducible |
| Authorization and tenant checks | Policy engine | Security decisions cannot rely on persuasion |
| Calculate money, eligibility, limits, dates | Domain service/rules engine | Precision, auditability, regulatory ownership |
| Commit records, payments, deployments | Deterministic service | Transaction and concurrency semantics matter |
| Retries, timers, joins, cancellation | Workflow engine | Distributed-systems control, not language reasoning |
| Content classification at ambiguous edge | Dedicated model plus deterministic thresholds | Useful probabilistic signal; policy remains external |
| Summarization and user explanation | LLM grounded in evidence | Natural-language generation is appropriate |
| Acceptance tests and reconciliation | Code/tests; model judge only as a supplement | Avoid self-certification and judge bias |

### Plan IR

JSON · implementation excerpt

```json
{
  "plan_id": "plan_...",
  "revision": 3,
  "goal": "...",
  "authority_envelope_id": "cap_...",
  "budget": {"usd": 12, "steps": 40, "wall_clock_seconds": 7200},
  "nodes": [{
    "id": "n7",
    "kind": "llm_activity | tool_activity | child_task | gate | wait | join",
    "capability_ref": "tool://crm/get-account@2.1.0",
    "depends_on": ["n4"],
    "input_refs": ["artifact://..."],
    "output_schema": "schema://account-summary@1",
    "risk_class": "R1",
    "retry_policy": "read-transient-v2",
    "acceptance_checks": ["schema", "freshness", "tenant"],
    "on_failure": "retry | fallback | partial | escalate | compensate | fail"
  }]
}
```

A deterministic compiler rejects cycles unless explicitly permitted, missing schemas, unbounded loops, unauthorized capabilities, budget overflow, inconsistent data classification, and unhandled terminal paths. A dynamic node may choose among an allowlisted capability set; it cannot call arbitrary network endpoints.

### Detailed design — APIs, data model, and scalability

### Component boundaries

| **Component** | **Responsibility** |
| --- | --- |
| Planner Activity | Produce a typed candidate plan from goal, constraints, eligible capabilities, and current evidence |
| Plan Store | Persist immutable revisions and current committed pointer |
| Capability Binder | Resolve abstract capabilities to pinned agents/tools/endpoints |
| Plan Compiler | Validate graph, types, authority, budgets, effects, failure paths, and determinism boundaries |
| Scheduler | Materialize ready nodes into workflow activities/child tasks under concurrency and quota |
| Replan Controller | Decide when replanning is allowed and define the unchanged/reusable subgraph |
| Acceptance Engine | Run deterministic checks and policy-approved model graders before satisfying nodes/goals |

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/runs/{run\_id}/plans:propose | Invoke the planner with state version, reason, planning horizon, and eligible capability snapshot; result is uncommitted |
| POST /v1/plans/{plan\_id}/revisions/{revision}:validate | Run schema, DAG, authority, budget, compatibility, data-flow, risk, and terminal-path validation |
| POST /v1/plans/{plan\_id}/revisions/{revision}:commit | Atomically select a validated revision using expected current revision/state version and reserve budgets |
| POST /v1/plans/{plan\_id}:revise | Create a diff-based revision from changed evidence/failure; cannot widen authority without a new grant |
| GET /v1/plans/{plan\_id}/revisions/{revision} | Return immutable plan, validation report, bindings, estimated cost/latency, and provenance |
| GET /v1/runs/{run\_id}/ready-nodes | Operator/debug view of satisfied dependencies, blockers, reservations, and dispatch state |
| POST /v1/nodes/{node\_execution\_id}:accept | Apply acceptance checks to outputs and transition only if expected node version still matches |

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| Plan | plan ID, run, goal hash, current committed revision, authority envelope, lifecycle state |
| PlanRevision | plan/revision, parent revision, trigger/rationale, planner/model/prompt/context versions, graph hash, created by/time; immutable |
| PlanNode | stable logical node ID, revision, kind, capability requirement/binding, input selectors, output schema, risk, retry/timeout, acceptance, failure strategy |
| PlanEdge | revision, from/to node, condition, artifact/data mapping; compiler verifies type compatibility and acyclicity unless loop is explicitly bounded |
| CapabilityBinding | abstract requirement, chosen agent/tool version, eligibility decision, health snapshot, regional endpoint, expiry |
| BudgetReservation | run/plan/node, resource type, reserved/consumed/released amount, expiry, ledger version |
| ValidationFinding | rule ID/severity, object path, message, evidence, required remediation; errors block commit |
| NodeExecution | logical node, plan revision, workflow/activity/task ID, attempt, state, inputs/outputs, accepted result hash, timing/cost |

### Compile-time checks

* Every node has a pinned implementation or an allowlisted runtime selector, typed inputs/outputs, timeout, retry owner, budget, risk class, acceptance rule, and terminal failure path.
* Data-flow classification can stay equal or become more restrictive. A node cannot send restricted data to a capability whose manifest/region/purpose is incompatible.
* Mutating nodes require idempotency/effect semantics and any policy-required preview/approval/compensation. R4 commit remains a deterministic domain operation.
* Loops require a deterministic guard plus maximum iterations, wall time, cost, and no-progress detector. Delegation depth and parallel fan-out are statically bounded.
* The compiler estimates critical path, maximum fan-out, worst-case calls/cost, and required quota. Admission may reject, defer, or require approval before commit.

### Runtime revision algorithm

1. Persist the triggering observation/failure and current state version.
2. Freeze completed effects and accepted artifacts; mark nodes whose assumptions changed as invalidated.
3. Ask the planner only for the affected horizon, not the entire run.
4. Compile and diff the candidate against the committed revision.
5. Reuse nodes only when implementation, inputs, policy, data revisions, and acceptance remain compatible.
6. Obtain new consent/approval if risk, purpose, destination, spend, or authority expands.
7. Atomically commit the revision and reservations, then schedule newly ready nodes.

### Scalability and performance

* Planner workers are stateless and queue driven. Plan storage is partitioned by tenant + run; immutable revisions can be cached by graph hash.
* Cache tool/agent schemas and compatibility matrices by digest. Policy and health are time-sensitive and must be rechecked at commit/dispatch.
* Validate incrementally: a plan revision carries changed nodes/edges, allowing graph, type, cost, and policy analysis to recompute only impacted regions.
* The scheduler scans no global table. Workflow events enqueue newly ready node IDs; conditional updates ensure each logical node is dispatched once per accepted attempt.
* For large DAGs, store canonical graph blobs by hash and keep indexed node/dependency projections in the relational store. Operator views are materialized asynchronously.
* Apply per-run ready-node limits and weighted fair scheduling across tenants. Planning cannot reserve unbounded future capacity; reservations expire and are reclaimed.
* Use deterministic routing for common/high-confidence cases and invoke the planner only at entry, material uncertainty, or failure boundaries. This reduces model cost and plan churn.

|  |
| --- |
| **ARCHITECTURE GUIDANCE**  Separate the plan from its execution. A plan is data: persist it, version it, and let it be inspected and approved before any step commits an effect. Once execution is a separate pass over a stored plan, replay, partial resume, and human amendment all become ordinary operations instead of special cases. |

## Grounding, corrections, and evidence boundary

|  |
| --- |
| **EVIDENCE BOUNDARY**  This chapter presents an architectural recommendation, not a protocol mandate. Validate the pattern against the workload, threat model, evaluation set, and strongest simpler baseline. |

Evidence anchors: TEMPORAL; NIST-GAI. Full URLs, authority, version, and scope appear in Appendix K.

## Pattern reference — Planning

|  |
| --- |
| **PROBLEM**  The task requires adaptive decomposition or dependency ordering that cannot be fully encoded upfront. |

### Architecture and flow

A planner emits a typed Plan IR. A deterministic compiler validates graph integrity, capabilities, schemas, risk, effects, budgets, resources, and terminal paths before the workflow schedules nodes.

1. Create a CandidatePlan with bounded nodes and dependencies.
2. Compile against the run envelope and release catalog.
3. Freeze a plan digest and revision.
4. Schedule ready nodes through durable workflow state.
5. Replan only the uncommitted future when observations invalidate assumptions.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for heterogeneous, dependency-rich tasks where semantic decomposition provides measurable value. | Avoid for known processes, short tasks, or high-risk paths that should be encoded as deterministic workflows. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Flexible decomposition | More validation, recovery, and evaluation complexity. |
| Parallel execution | Lower latency; higher resource use and conflict risk. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Invalid graph | Cycle, reference, terminal, and reachability checks. |
| Invented authority | Capability and grant subset checks. |
| Plan churn | Revision, no-progress, and cost limits; freeze committed facts. |

### Minimum observability

* plan digest and revision
* compiler decisions
* ready set
* node states
* critical path
* replan diff and reason

## Implementation reference


### Plan IR compiler

[[EXAMPLE:plan-compilation#core]]

## Debugging playbook

1. Re-run the plan compiler against the exact release and policy versions.
2. Find the first node whose capability, budget, or schema became invalid.
3. Compare plan revisions and ensure committed facts did not change.

## Production checklist

**✓** Model planning is used only for genuine semantic uncertainty.

**✓** Plans are typed, immutable, versioned graphs with explicit limits and acceptance.

**✓** Graph, authority, security, resource, schema, and effect constraints compile before commit.

**✓** Completed effects and accepted artifacts are frozen across revisions.

**✓** Revisions, loops, fan-out, depth, time, cost, and no-progress behavior are bounded.

## Exercises

1. Extend the Plan IR with deadlines and fallback paths.
2. Construct a plan that passes schema validation but must fail authority validation.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| When should you use a deterministic workflow instead of model planning? | When paths, invariants, and recovery semantics are known; use planning only for real semantic uncertainty or environmental adaptation. |
| Why create a typed Plan IR? | It makes nodes, dependencies, capabilities, schemas, risk, budgets, and failure behavior inspectable, compilable, versionable, and schedulable. |
| What must a plan compiler validate? | Graph integrity, schema compatibility, authority subset, data and region policy, effect and approval semantics, capacity, cost, deadlines, and terminal paths. |
| How should replanning handle completed work? | Treat committed effects and accepted artifacts as immutable facts; revise only the affected future horizon and append a new version with rationale and diff. |
| How do you prevent plausible but endless planning? | External revision, loop, step, cost, time, delegation, and no-progress limits plus deterministic acceptance and terminal transitions. |

## Transition to Chapter 13

Planning creates an executable structure; Chapter 13 adds independent evaluation and bounded revision without self-certification.

# 13 — Reflection and Evaluator–Optimizer

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  The first recommendation is coherent but omits a contradictory address and overstates confidence. Northstar adds bounded reflection for revision and an independently defined evaluator for acceptance. |

|  |
| --- |
| **DESIGN DECISION**  Use reflection for targeted revision and independent, calibrated acceptance for protected outcomes. |

## What this chapter delivers

Use critique and evaluation to improve outputs without self-certification, unbounded loops, or hidden cost.

## Solution blueprint


Figure 7. Reflection and Evaluator–Optimizer.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Acceptance Engine | generator/evaluator and evaluator/commit | candidate · scorer pool · slice | one revision cycle | EvaluationResult · Rubric · AcceptanceDecision |

## Improvement without self-certification

[[DIAGRAM:pattern-reflection|Figure 13-1 — A bounded revise loop whose verdict is advisory; promotion happens outside it]]

Reflection asks, “What is missing or inconsistent?” Evaluation asks, “Does this candidate meet an acceptance rubric?” Combining them can improve complex artifacts, but only if the roles are explicit and bounded. Northstar runs executable checks before any model judge: schema, evidence presence, policy, effect state, resource version, arithmetic, and deterministic domain rules.

Qualitative criteria—clarity, completeness, grounded synthesis, or policy-explanation quality—may use calibrated judges. Judge prompt, model route, examples, sampling parameters, and rubric are versioned. Northstar measures variance, human agreement, and failure slices. A model score is evidence for a release or review decision; it is not permission to access data or commit a transaction.

### Bounded optimization loop

Each revision targets structured feedback and carries a diff. The loop stops on pass, maximum revisions, maximum spend, deadline, or no-progress. If the evaluator and generator repeatedly disagree, the workflow escalates with both artifacts rather than silently choosing the more persuasive prose.

## Grounding, corrections, and evidence boundary

|  |
| --- |
| **EVIDENCE BOUNDARY**  This chapter presents an architectural recommendation, not a protocol mandate. Validate the pattern against the workload, threat model, evaluation set, and strongest simpler baseline. |

Evidence anchors: MLFLOW-EVAL; NIST-GAI. Full URLs, authority, version, and scope appear in Appendix K.

## Pattern reference — Reflection

|  |
| --- |
| **PROBLEM**  A first candidate may contain omissions, contradictions, or weak reasoning that targeted critique can expose. |

### Architecture and flow

A reflector reviews a candidate against explicit evidence and rubric, emits structured defects, and proposes a bounded revision. It does not commit or certify protected outcomes.

1. Generate a candidate.
2. Compare it with evidence and rubric.
3. Emit defect types and references.
4. Revise only supported defects.
5. Stop on pass, no-progress, or revision budget.

| **Use when** | **Do not use when** |
| --- | --- |
| Use when measured offline results show critique improves a specific quality dimension. | Avoid if correctness is executable, the first pass already meets it, or added latency has no measured benefit. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Better completeness | Additional model calls, correlated errors, and longer latency. |
| Structured critique | More debuggable; requires defect taxonomy and evaluation. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Self-confirmation | Different rubric, evidence, or evaluator and deterministic checks. |
| Stylistic churn | Diff limits and no-progress detection. |
| Evidence invention | Require evidence references and reject unsupported additions. |

### Minimum observability

* candidate version
* defect taxonomy
* evidence refs
* diff size
* quality delta
* stop reason

## Pattern reference — Evaluator–Optimizer

|  |
| --- |
| **PROBLEM**  A generated artifact must reach a quality threshold that mixes executable and semantic criteria. |

### Architecture and flow

A generator creates candidates; deterministic scorers and calibrated evaluators produce typed feedback; an optimizer revises within a strict iteration budget; an acceptance engine decides.

1. Generate candidate v1.
2. Run deterministic checks first.
3. Run calibrated qualitative evaluation if needed.
4. Apply actionable feedback to one revision.
5. Accept, reject, or escalate at a bounded threshold.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for documents, plans, code, or analyses where iterative quality gain is measurable and latency permits. | Do not use a model judge as sole authority for permissions, transaction success, security, or computable correctness. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Higher quality | Higher cost and latency, plus evaluator calibration work. |
| Explicit rubric | Improves governance; can overfit to benchmark or judge preferences. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Reward hacking | Hidden holdout tests, diverse scorers, and human calibration. |
| Judge variance | Repeated runs, confidence intervals, ensembles, and thresholds. |
| Endless revision | Maximum revisions, cost, time, and no-progress stop. |

### Minimum observability

* scorer versions
* per-criterion scores
* judge rationale
* candidate diffs
* variance
* acceptance decision

## Implementation reference


### Bounded evaluator–optimizer

🐍 · implementation excerpt

```python
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol
from .contracts import AgentDecision

class Evaluation:
    accepted: bool
    score: float
    feedback: str

class EvaluatorOptimizer:
    def __init__(
        self, generator: Generator, evaluator: Evaluator, maximum_revisions: int = 2
    ) -> None:
        self.generator = generator
        self.evaluator = evaluator
        self.maximum_revisions = maximum_revisions

    async def run(self, task: str) -> tuple[str, Evaluation]:
        feedback: str | None = None
        for _ in range(self.maximum_revisions + 1):
            candidate = await self.generator(task, feedback)
            evaluation = await self.evaluator(task, candidate)
            if evaluation.accepted:
                return candidate, evaluation
            feedback = evaluation.feedback
        raise RuntimeError("candidate did not pass bounded evaluation")
```

## Debugging playbook

1. Compare generator and evaluator evidence to detect shared blind spots.
2. Inspect score variance across repeated judge runs and slices.
3. Detect revisions that change wording but not the failing invariant.

## Production checklist

**✓** Generator and evaluator roles, prompts, models, and evidence are distinguishable.

**✓** Computable invariants use code, not a model judge.

**✓** Revision count, spend, time, and no-progress are bounded.

**✓** Judge calibration and inter-rater agreement are measured.

**✓** Failed candidates and feedback enter a regression corpus.

## Exercises

1. Implement a bounded evaluator-optimizer with one deterministic and one qualitative scorer.
2. Create a case where reflection worsens a correct answer and define the stop rule.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| How is reflection different from evaluation? | Reflection proposes improvements; evaluation applies an acceptance rubric and should be independently calibrated or deterministic where possible. |
| Why is self-evaluation dangerous? | The same model can repeat the same blind spots and produce confident rationales without independent evidence. |
| How do you bound evaluator–optimizer? | Limit revisions, cost, time, and accepted feedback types; stop on pass, no-progress, or escalation. |
| What should always be checked deterministically? | Schema, policy, authority, evidence presence, effect state, resource versions, arithmetic, and other computable invariants. |
| When should you not add reflection? | When the first result already meets an executable specification, latency is critical, or critique adds no measured improvement. |

## Transition to Chapter 14

Automated evaluation can improve candidates; Chapter 14 identifies decisions that require explicit human authority, correction, or recourse.

# 14 — Human-in-the-Loop

> **Evidence note.** Human-review interfaces should be tested against WCAG 2.2 accessibility criteria; accessibility conformance does not by itself eliminate automation bias or establish decision fairness. [R41]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  A protected supplier activation requires approval. An approver must see the exact action, destination, evidence, expected resource version, and risk—not a vague request to “approve the agent.” |

|  |
| --- |
| **DESIGN DECISION**  Persist proposal-bound approvals as durable workflow events and reauthorize immediately before commit. |

## What this chapter delivers

Bind approval and intervention to immutable proposals and durable state transitions.

## Solution blueprint


Figure 8. Human-in-the-Loop.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Workflow plus Approval Service | machine proposal to human authority | approval queue · risk class · tenant | one immutable proposal | ApprovalRequest · ApprovalDecision · EffectReceipt |

## Two distinct human controls

[[DIAGRAM:pattern-hitl|Figure 14-1 — Approval and intervention: different triggers, different authority, different evidence]]

**Approval** authorizes one proposed effect. **Intervention** asks a person to diagnose, correct, supply information, or choose among unresolved alternatives. Combining them creates audit ambiguity. Northstar uses separate queues, roles, forms, SLOs, and terminal semantics.

The Approval Service stores a canonical proposal, human-readable preview, destination, evidence and policy references, risk, expected resource version, expiry, and proposal hash. Approval becomes invalid when any protected field changes. A commit path rechecks approver authority, separation of duties, current policy, grant freshness, and resource version.

Human capacity is finite. Queue age, dwell, abandonment, reassignment, disagreement, and after-hours coverage are production metrics. A system that requires routine approval for low-risk deterministic work may be less safe because reviewers become fatigued.

## Human-in-the-loop and operational control

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Humans must understand, approve, correct, or stop consequential work without becoming a rubber stamp or breaking run integrity. |
| Why it is difficult | Too many approvals cause fatigue; too little context prevents informed decisions; approvals can go stale as data or plans change; edits must be attributable and replayable. |
| Design alternatives | Confirm every tool call; risk-based approvals; maker-checker; sampled review; exception-only review; fully manual commit. |
| Recommended architecture | Use policy-triggered gates based on risk, novelty, confidence, value, data sensitivity, reversibility, and destination. Present a concise preview, evidence, alternatives, changed fields, policy rationale, and blast radius. Approval authorizes a specific immutable proposal for a limited time. |
| Trade-offs | Human review adds latency and staffing cost but provides judgment and accountability where automation evidence is insufficient. Poor UX converts the control into theater. |
| Failure scenarios | Approval applies to a changed plan; approver lacks authority; agent hides uncertainty; request times out; two operators issue conflicting overrides; “approve all” becomes normal. |
| Enterprise example | A customer-service agent drafts a high-value refund. The supervisor sees policy basis, customer history, amount, downstream effect, and alternatives; any amount or recipient change invalidates the approval. |

### Approval contract

An ApprovalRequest contains: proposal/artifact hash, exact action and resource, before/after diff, subject and actor, evidence links, uncertainty, policy rule, risk class, estimated impact/cost, reversible flag, expiry, separation-of-duties requirement, and allowed responses (approve, reject, edit-and-resubmit, request-evidence, cancel-run).

### Operator console requirements

* Live run graph with current owner, state, budgets, queues, waits, child tasks, and last committed effect.
* Redacted but causally complete trace; model/tool inputs available only to authorized incident roles.
* Pause, cancel, retry safe activity, skip with justification, patch plan, reassign approval, increase budget, trigger compensation, and fork a sandbox replay.
* Conflict detection and optimistic versions for operator edits.
* Immutable operator identity, reason, timestamp, before/after state, and linked ticket on every override.
* SLA timers and escalation paths; a timed-out approval follows explicit policy, never implicit approval.

### Detailed design — APIs, data model, and scalability

### Component boundaries

| **Component** | **Responsibility** |
| --- | --- |
| Approval Policy Router | Convert policy obligations, risk, value, novelty, and confidence into approval requirements |
| Approval Service | Persist immutable proposal snapshots and authoritative decision state |
| Assignment/Queue Service | Resolve eligible approvers, maker-checker rules, claim/reassign, priority, and SLA |
| Evidence Renderer | Produce role-redacted diff, sources, rationale, alternatives, uncertainty, and blast radius |
| Notification Service | Deliver idempotent channel notifications and deep links; it never owns the decision |
| Operator Control Service | Perform authorized pause, cancel, retry, plan patch, budget, and compensation commands |
| Override Journal | Append operator actions and linked incident/change records to immutable evidence |

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/approvals | Idempotently create approval from proposal hash, exact action/resource, evidence snapshot, required roles/count, expiry, and allowed responses |
| GET /v1/approvals/{approval\_id} | Return current state, immutable proposal, redacted evidence view, assignments, SLA, and decision history |
| POST /v1/approvals/{approval\_id}:claim | Claim work using expected version; verifies current eligibility and separation of duties |
| POST /v1/approvals/{approval\_id}:decide | Approve/reject/request-evidence using proposal hash, expected version, reason, and strong approver authentication |
| POST /v1/approvals/{approval\_id}:requestEvidence | Suspend decision and signal the workflow with a typed evidence request |
| POST /v1/approvals/{approval\_id}:supersede | Close stale approval and create a new one when proposal, target state, policy, or material evidence changes |
| GET /v1/approval-queues/{queue\_id}/items | Cursor query by skill/role, priority, age, risk, tenant, value, and region; no unauthorized evidence leakage |
| POST /v1/runs/{run\_id}:operatorAction | Pause, cancel, safe-retry, patch plan, extend budget, trigger reconciliation/compensation, or fork replay with reason and expected state |

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ApprovalRequest | approval ID, tenant/run/node/effect, proposal hash, action/resource, before/after refs, risk/value, policy decision, required approver predicate/count, expiry, state/version |
| ApprovalEvidenceSnapshot | approval, immutable source/artifact refs and hashes, policy/rationale, uncertainty, alternatives, impact, redaction profile, created version |
| ApprovalAssignment | approval, queue, eligible-role predicate, assignee/claim lease, SLA, escalation level, state |
| ApprovalDecision | approval, proposal hash, approver identity/role/assurance, decision, reason, signature/attestation, time; append-only |
| OperatorAction | action ID, run, command, actor/role, target/version, before/after refs, reason, linked ticket, result/effect; append-only |
| EscalationPolicy | queue/risk/value, warning/expiry timers, fallback roles, business calendar, timeout disposition; implicit approval is forbidden |
| NotificationDelivery | approval/action, channel, destination handle, idempotency key, attempts, delivered/acknowledged, error; contains no unredacted evidence |

A decision is valid only when the presented proposal hash equals the current proposal, the approver is authorized at decision time, required counts/separation rules are satisfied, and the approval has not expired or been superseded.

### Workflow integration

1. The workflow commits the proposed effect and evidence snapshot, then creates the approval.
2. The Approval Service registers durable SLA/expiry timers and returns a wait correlation ID.
3. Assignment and notifications may retry independently; the workflow remains suspended without a worker.
4. A decision transaction records the immutable decision and emits an outbox event.
5. The workflow receives the event, revalidates policy/current resource version, and commits only the proposal hash that was approved.
6. If the resource, amount, recipient, scope, or policy changed materially, the workflow supersedes the approval and generates a fresh preview.

### Scalability and operations

* Partition approvals by tenant + business queue/region while keeping a direct index by approval/run ID. Strongly serialize decisions for one approval; scale independently across approvals.
* Use workflow timers or a durable timer service for SLA/escalation—never scan an approvals table each minute at enterprise scale.
* Materialize queue views by eligibility dimensions and age. Compute final authorization at read/claim/decision time so an index cannot leak work after role changes.
* Coalesce notifications and support digest/batched review for low-risk homogeneous actions, but preserve one proposal and decision record per effect.
* Apply queue admission and staffing metrics: arrival rate, service time, oldest age, abandonment, reassignment, rejection, and correction. Approval capacity is part of end-to-end capacity planning.
* Prevent approval stampedes during incidents with per-queue rate limits, prioritized critical items, bulk-action policy, and explicit incident-mode controls—never an unbounded “approve all.”
* Replicate redacted queue projections for availability, but keep the authoritative decision write in the run’s home/legal region. After failover, fence the prior writer before accepting decisions.
* Cache immutable evidence by hash and render role-specific views on demand; large source material remains in governed artifact storage.

|  |
| --- |
| **PRODUCTION CONSIDERATION**  Design the wait, not just the prompt. A run paused for approval may sit for days across deploys, token expiry, and staff changes. Persist the full decision context with the pause, expire it explicitly, and define what happens when it lapses — an approval request with no expiry becomes an approval nobody can safely grant. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Approval integrity | Approve the exact canonical proposal, not a natural-language summary. Revalidate policy, authority, proposal hash, expiry, destination, and resource version immediately before commit. Never transport serialized run state inside exception text or ordinary logs. | OAI-HITL; OWASP-AGENT |

Evidence anchors: OAI-HITL; OWASP-AGENT; WCAG22. Full URLs, authority, version, and scope appear in Appendix K.

## Pattern reference — Human-in-the-Loop

|  |
| --- |
| **PROBLEM**  A person must authorize, correct, or resolve work whose risk or ambiguity exceeds autonomous authority. |

### Architecture and flow

The workflow persists a proposal-bound ApprovalRequest or InterventionTask, pauses, receives an authenticated decision, revalidates current authority and resource state, then commits or replans.

1. Create an immutable proposal and preview.
2. Identify allowed approver roles and separation-of-duty rules.
3. Persist the wait and notify through a durable channel.
4. Authenticate and record decision, reason, and timestamp.
5. Reauthorize and verify proposal hash immediately before commit.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for high-risk, irreversible, regulated, ambiguous, or policy-exception decisions. | Do not add a cosmetic click for already-automated low-risk steps or ask a human to review unreadable raw model traces. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Risk control | Adds dwell time, queues, fatigue, and staffing requirements. |
| Human judgment | Handles ambiguity; can be inconsistent and needs calibration. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Approval drift | Hash binding, expiry, expected version, and reapproval. |
| Wrong approver | RBAC/ABAC and separation of duties. |
| Queue abandonment | SLA, escalation, reassignment, cancellation, and safe timeout. |

### Minimum observability

* proposal hash
* risk and policy basis
* approver authority
* queue and dwell time
* decision and reason
* commit receipt

## Implementation reference


[[EXAMPLE:approval-gate]]

### Proposal-bound approval contract

🐍 · implementation excerpt

```python
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    approval_id: str
    run_id: str
    action: str
    destination: str
    canonical_arguments: dict[str, object]
    evidence_ids: tuple[str, ...]
    expected_resource_version: str
    expires_at: datetime
    proposal_sha256: str


def proposal_hash(action: str, destination: str,
                  arguments: dict[str, object],
                  evidence_ids: tuple[str, ...],
                  expected_version: str) -> str:
    body = {
        "action": action,
        "destination": destination,
        "arguments": arguments,
        "evidence_ids": evidence_ids,
        "expected_version": expected_version,
    }
    encoded = json.dumps(body, sort_keys=True,
                         separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()
```

### Executable proposal-bound approval

[[EXAMPLE:approval-verification#core]]

## Debugging playbook

1. Recompute the proposal hash and expected resource version.
2. Verify approver authority, expiry, and separation-of-duty policy.
3. Trace the approval event through commit and effect receipt.

## Production checklist

**✓** Every capability has an immutable manifest covering interface, security, risk, effects, runtime, ownership, and lifecycle.

**✓** Discovery is minimal and exact resource authorization happens at invocation.

**✓** Mutations have logical keys, intent hashes, preconditions, receipts, reconciliation, compensation, and one retry owner.

**✓** Approval binds to an immutable proposal hash and current authority and resource state.

**✓** Reconciliation, compensation, pause, cancel, and intervention are governed commands.

## Exercises

1. Design an approval object for a $100,000 supplier activation.
2. Define how edits, policy changes, and expired grants invalidate approval.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why put a Tool Gateway between agents and enterprise systems? | Central schema, policy, credentials, rate limits, risk, approval, effect semantics, result sanitation, observability, and lifecycle enforcement. |
| Why is tool discovery not authorization? | Eligibility is temporary and often coarse; the gateway must check current subject, actor, purpose, resource, arguments, risk, and policy immediately before execution. |
| How should approval be bound to an action? | Persist the exact canonical proposal, preview, destination, evidence, risk, and hash; authorize the approver; reject expiry, supersession, hash mismatch, or stale resource state. |
| Why are both idempotency and optimistic concurrency needed? | Idempotency prevents duplicate logical intent; expected versions prevent an otherwise valid action from overwriting newer state. |
| What should happen when a mutating tool times out? | Mark the effect unknown, block dependent work and blind retry, reconcile using downstream identifiers or observed state, then conclude committed, absent, partial, or intervention required. |

## Transition to Chapter 15

Human control introduces waits and resumptions; Chapter 15 makes those waits durable and gives long-running work explicit state and recovery.

# 15 — Long-Running and Durable Agents

> **Evidence note.** Durable-execution systems preserve workflow progress across failures and long waits; concrete integrations and replay semantics vary by backend. [R02][R36][R38]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  The supplier waits nine days to upload a certificate. During the wait, workers deploy twice, policy changes, a user loses a role, and one earlier external request timed out. The run must resume safely rather than restart from a prompt transcript. |

|  |
| --- |
| **DESIGN DECISION**  Represent long-running work as replay-safe workflow history plus bounded activities, durable waits, and reconciliation. |

## What this chapter delivers

Preserve weeks-long work across waits, failures, deployments, retries, cancellations, and uncertain effects.

## Solution blueprint


Figure 9. Long-Running and Durable Agents.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Durable workflow engine | workflow activity to external I/O | history shard · activity queue · timer | one workflow execution | WorkflowEvent · Checkpoint · WaitRegistration |

## Durable state is more than chat history

[[DIAGRAM:pattern-durable|Figure 15-1 — The run outlives the process: checkpoint, die, replay, adopt]]

Chat history cannot reliably encode timers, retries, child ownership, approval waits, cancellation intent, resource versions, effect receipts, or deployment compatibility. Northstar uses event history to rebuild a canonical RunState; model and tool calls are bounded activities whose inputs and outputs are recorded by reference.

The workflow reducer must be deterministic. It cannot read the clock, call a model, query a database, generate randomness, or perform network I/O during replay. Those operations become activities, signals, or recorded events. This separation makes a crashed worker replaceable.

### Terminal correctness

A run reaches Succeeded only through executable acceptance. A canceled run with a possibly committed write does not simply disappear; it moves through reconciliation and possibly compensation. If correctness cannot be established automatically, InterventionRequired is a valid terminal operational state.

## Execution lifecycle

### Canonical run state machine

### Canonical control flow

1. **Admit.** Authenticate the caller; bind tenant, subject, channel, purpose, data classification, requested autonomy, and a client idempotency key.
2. **Snapshot.** Resolve immutable versions of the agent, workflow, prompt/skill bundle, policy, model route, tool schemas, and knowledge index.
3. **Authorize.** Evaluate the requested goal and maximum capability envelope; allocate token, cost, time, tool, delegation, and concurrency budgets.
4. **Plan.** The model may propose a typed plan. Code validates DAG constraints, allowed capabilities, risk classes, preconditions, and budgets.
5. **Execute.** The workflow kernel schedules replay-safe activities. Each effect is individually authorized using fresh context and a downscoped credential.
6. **Checkpoint.** Persist state after every externally visible effect and meaningful decision; store large artifacts by immutable reference and hash.
7. **Wait or intervene.** Suspend without a worker for timers, callbacks, clarification, or approval. Signals carry correlation and authorization metadata.
8. **Validate and commit.** Deterministic validators test outputs and invariants. High-risk effects use propose → preview → approve → commit.
9. **Complete.** Produce a typed result, evidence bundle, final cost/quality metrics, retention class, and terminal event.
10. **Learn safely.** Feed de-identified traces and failures into curated datasets; never let production memory or prompts self-modify without review.

## Long-running agents and event-driven execution

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Runs lasting minutes to months must survive crashes, deployments, expired credentials, human waits, rate limits, and external callbacks without restarting from scratch. |
| Why it is difficult | Process memory is ephemeral; replay can repeat nondeterministic calls and side effects; external systems deliver duplicates or callbacks out of order; code and schemas evolve while runs are active. |
| Design alternatives | Background job + database; queue consumers; graph checkpointing; cloud state machines; durable execution engines such as Temporal/DBOS/Restate/Durable Functions; event-sourced custom runtime. |
| Recommended architecture | Use a durable workflow engine as the authoritative run kernel. Put model and tool calls in activities/tasks, record their results, persist checkpoints after meaningful steps, and use durable timers/signals for waits. Feed external events through an event bus and correlate them to existing runs. |
| Trade-offs | Durable engines impose determinism/versioning constraints and operational cost, but remove far more bespoke recovery code. Graph checkpointers are useful for agent state but may not replace a mature cross-service workflow engine. |
| Failure scenarios | Replay resends an email; worker dies after effect but before acknowledgment; old run cannot replay after code change; callback is spoofed; event arrives before subscription; retry storm exhausts provider quota. |
| Enterprise example | A supplier-onboarding agent waits days for KYC documents and approvals. The workflow is unloaded while idle, resumes on correlated events, refreshes authorization, and continues from the last committed effect. |

### Durable execution contract

* **Workflow code:** deterministic control logic only. No wall-clock reads, random values, direct network calls, or model calls unless captured as replay-safe activities.
* **Activity:** one bounded external interaction with timeout, retry class, idempotency key, heartbeat, cancellation behavior, and structured result.
* **Checkpoint:** workflow-state snapshot plus event-history position, plan version, effect ledger cursor, artifact references, and version pins.
* **Signal:** authenticated external input (approval.granted, document.received, callback.completed, user.clarified) carrying a correlation key and monotonic event ID.
* **Query:** read-only inspection of run state for users and operators; must not advance execution.
* **Update:** authorized mutation such as budget increase, plan patch, assignee change, or safe retry.

### Checkpoint policy

Checkpoint after every irreversible or externally visible effect, before long waits, after plan revisions, and at fan-in boundaries. Do not serialize full prompt histories into every checkpoint; persist canonical state and immutable artifact references. Encrypt by tenant and apply retention by data class.

### Event-driven resume flow

### Event architecture

Use a CloudEvents-compatible envelope with id, source, type, subject, time, dataschema, tenant\_id, correlation\_id, causation\_id, traceparent, and a payload reference. Keep sensitive or large content in an access-controlled object store; events carry references and hashes. Use transactional outbox on producers and inbox/deduplication on consumers. A dead-letter queue is quarantine and diagnosis—not a substitute for domain compensation.

### Detailed design — APIs, data model, and scalability

### Component boundaries

The Run API persists intent and returns quickly; the durable workflow owns lifecycle; activity workers perform model/tool I/O; Event Ingress authenticates external facts; the Correlator maps those facts to waiting runs; Timer/Signal services wake workflows; and a Version Router keeps compatible workflow builds available for in-flight histories.

### High-level APIs

| **API** | **Purpose and contract** |
| --- | --- |
| POST /v1/runs | Idempotent admission; returns 202, run ID, home region, pinned manifest, and status URL |
| GET /v1/runs/{run\_id} | Read a materialized projection with state\_version, waits, deadlines, budget, and latest checkpoint |
| POST /v1/runs/{run\_id}:signal | Deliver typed user/system signal with event ID, correlation key, schema version, subject authorization, and expected state |
| POST /v1/events:ingest | Authenticate a CloudEvent, store inbox receipt, then route to a waiting workflow or unmatched-event holding area |
| POST /v1/runs/{run\_id}:cancel | Durable cancellation request with propagation and compensation policy; never implies immediate termination |
| POST /v1/runs/{run\_id}:pause | Administrative gate that prevents new activities while preserving timers/signals according to policy |
| POST /v1/runs/{run\_id}:resume | Resume after authorization/version checks; requires expected state version and reason |
| POST /v1/runs/{run\_id}:migrate | Apply an approved deterministic state/code migration with dry-run report and rollback boundary |
| GET /v1/runs/{run\_id}/history?cursor=... | Paginated, role-redacted event history; content is referenced rather than embedded |

### Core data model

| **Entity** | **Key fields and invariants** |
| --- | --- |
| WorkflowExecution | run ID, tenant, workflow type/build, home region/shard, state, state version, history generation, start/close times; one active execution per run generation |
| WorkflowEvent | execution ID, monotonically ordered event sequence, type, logical time, payload reference/hash, causation/correlation, producer; append-only |
| ActivityAttempt | activity ID, logical effect key, type/version, task queue, attempt, timeout set, heartbeat, result/error reference, retry disposition |
| WaitRegistration | run ID, wait type, correlation keys, accepted event schemas/sources, expiry, resume node, current status |
| SignalInbox | tenant, source, event ID, payload hash, received time, verification result, routed run; unique (tenant, source, event\_id) |
| Timer | workflow ID, timer ID, due time, purpose, cancellation state; durable and sharded by due-time bucket |
| Checkpoint | execution ID, event sequence, canonical state hash/reference, plan revision, artifact/effect cursors, code compatibility range |
| WorkflowMigration | from/to build, applicable state/schema, deterministic transformer digest, approval, test evidence |

### Execution and persistence rules

* Record model and external tool calls as activities whose results are persisted before workflow continuation. Replay returns the recorded result; it does not recall the model or tool.
* Persist a wait registration before acknowledging that the run is waiting. Event Ingress writes the inbox receipt before signaling the workflow, closing the “event arrived before subscription” race.
* For a side effect, persist intent/effect key before invocation and reconcile the receipt before an activity is considered complete.
* Use logical workflow time for decisions. Wall-clock access, random IDs, and dynamic configuration are provided as recorded events/side effects.
* Continue-as-new or history compaction starts a new generation with a verified state snapshot when history size or event count reaches an engine-specific threshold; preserve an audit link to prior generations.

### Scalability and multi-region behavior

* Shard workflows by stable run ID and timers by time bucket + shard. Activity queues are separate from workflow-task queues so slow tools cannot starve state transitions.
* Waiting executions consume storage, not workers. Capacity planning distinguishes active workflow tasks, scheduled activities, open waits, timer cardinality, and history-write throughput.
* Autoscale activity workers on oldest-message age, arrival rate, observed service time, provider quota, and downstream health. CPU is only a secondary signal for I/O-heavy agent tasks.
* Use sticky execution caches for latency but require correctness without them; any compatible worker must rebuild state from history after eviction or failure.
* Assign a run to one home region. Replicate encrypted history and projections for DR, but allow only one writer region per generation. On failover, fence the old region, restore/verify history, reconcile external effects, then resume.
* Separate task queues by workflow build compatibility. Keep old workers available for in-flight runs or migrate explicitly; never replay old history against untested new code.
* Rate-limit external signals per tenant/source and coalesce superseding updates where domain semantics allow. Preserve individual inbox receipts even when only the latest value wakes the workflow.

|  |
| --- |
| **PRODUCTION CONSIDERATION**  Assume at-least-once delivery and make effects idempotent. Exactly-once is not available end to end; a dispatch that times out leaves the outcome genuinely unknown. Give every logical effect a stable key, record its receipt, and reconcile rather than retrying blind. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Recovery objective | Durability is incomplete without measured RTO/RPO, compatible worker availability, backup restoration, region failover, and explicit treatment of pending approvals and unknown effects during disaster recovery. | TEMPORAL; CLOUDEVENTS |

Evidence anchors: TEMPORAL; CLOUDEVENTS. Full URLs, authority, version, and scope appear in Appendix K.

|  |
| --- |
| **COMMON PITFALL**  Storing conversation history and calling it durable state. Transcripts record what was said, not what was decided or committed. Persist decisions, approvals, and effect receipts as first-class records; a run must be resumable from them even if every message is discarded. |

## Pattern reference — Long-Running Agents

|  |
| --- |
| **PROBLEM**  Business work lasts longer than a process lifetime and must survive waits, worker loss, retries, deployments, and partial external failures. |

### Architecture and flow

A durable workflow records deterministic decisions and schedules bounded activities. Timers, signals, children, approvals, effects, and release pins are durable history.

1. Admit and pin the run manifest.
2. Record each state transition before scheduling work.
3. Execute models and tools as bounded idempotent activities.
4. Persist waits and resume through authenticated signals or timers.
5. Reconcile effects and verify terminal criteria before closing.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for work with waits, multiple systems, protected effects, independent failures, or duration beyond one request. | Avoid a workflow engine for a single short idempotent read with no recovery or coordination requirement. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Failure recovery | Requires deterministic workflow discipline and history compatibility. |
| Long waits | Preserves state; creates lifecycle, retention, and migration obligations. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Nondeterministic replay | Move I/O, clocks, randomness, and model calls to activities. |
| Stuck wait | Durable deadline, accepted signal sources, escalation, and visibility. |
| Unknown mutation | Freeze dependents and reconcile before retry or close. |

### Minimum observability

* workflow build
* history event
* activity attempt
* timer and wait state
* signal source
* effect reconciliation
* terminal reason

## Implementation reference


### Replay-safe workflow reducer

[[EXAMPLE:durable-state#core]]

## Debugging playbook

1. Replay workflow history with the pinned build and locate nondeterminism.
2. Inspect pending timers, signals, activities, and child tasks.
3. Resolve unknown effects before replaying dependent commands.

## Production checklist

**✓** Workflow decisions are replay-safe; I/O, clocks, randomness, models, and tools are recorded activities.

**✓** Waits, signals, timers, cancellation, and child lifecycles are durable protocol state.

**✓** Each failure class has one retry owner; unknown effects route to reconciliation.

**✓** Active histories stay pinned to compatible workflow builds and activity contracts.

**✓** Workflow tasks, activities, timers, waits, history writes, and reconciliation are capacity-planned separately.

## Exercises

1. Model a ten-day wait with role revocation and policy change.
2. Design cancellation semantics for a run with a possibly committed external write.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| How is durable execution different from a background job? | Control decisions and waits are recorded as replayable history; workers can disappear without restarting the business process or losing timers and signals. |
| What belongs in workflow code versus an activity? | Deterministic coordination in workflow code; models, databases, APIs, tools, clocks, randomness, and other external interactions in bounded activities. |
| How do you represent a wait that may last weeks? | Persist a typed wait registration, accepted sources and correlation, deadline, authorization, and resume node; wake through an authenticated signal or durable timer. |
| What happens if cancellation arrives while a write may have committed? | Persist cancellation intent, stop new work, mark the effect unknown if needed, reconcile the source system, then compensate or require intervention before closing. |
| How do you deploy new workflow code safely? | Preserve compatible workers, use explicit version markers, test replay, migrate deterministically when supported, or start a new linked generation when semantics cannot be preserved. |

## Transition to Chapter 16

The core patterns are now defined; Chapter 16 compares them across uncertainty, authority, latency, evidence, and operating cost.

# 16 — Enterprise Pattern Catalog

## How to use the cards

Choose by hidden obligation, uncertainty, and risk—not fashionable terminology. Every card uses one review sequence so teams can compare alternatives consistently.

[[DIAGRAM:pattern-decision-tree|Figure 16-1 — Pattern selection decision tree]]

## Reasoning

### P-01 — Bounded ReAct

**Problem.** Adaptive evidence is needed.

**Anti-Pattern.** Unbounded think–act loop.

**Why It Fails.** The model owns stopping, budget, and success.

**Recommended Pattern.** Bound ReAct with step/time/token/tool/evidence limits and deterministic acceptance.

**Architecture.** Run Service → reason → eligible tool → observation → stop/accept.

**Enterprise Example.** Supplier screening queries two approved registries, asks once for missing ID, then stops.

**Detection Metrics.** Steps, no-progress loops, repeat queries, budget exhaustion, evidence coverage.

**Trade-offs.** Bounds can stop useful exploration; tune by risk.

## Orchestration

### P-02 — Deterministic spine with semantic nodes

**Problem.** Known obligations include a few judgment points.

**Anti-Pattern.** A conversational agent owns the process.

**Why It Fails.** Retries, waits, joins, approval, and compensation become ambiguous.

**Recommended Pattern.** Durable workflow with bounded semantic nodes.

**Architecture.** Workflow state → semantic task → typed result → deterministic transition.

**Enterprise Example.** Onboarding always validates, screens, approves, creates, and notifies.

**Detection Metrics.** Transcript-only state, orphan tasks, duplicate effects, recovery time.

**Trade-offs.** Workflow modeling adds upfront cost.

## Context engineering

### P-03 — Typed ContextManifest

**Problem.** The model needs authorized fresh evidence under budget.

**Anti-Pattern.** Dump top-k and chat history into the prompt.

**Why It Fails.** Selection, ACL, freshness, poisoning, and truncation are not reproducible.

**Recommended Pattern.** Manifest source, ACL, snapshot, provenance, rank, freshness, token allocation.

**Architecture.** Planner → retrieval → policy → ranking/dedup → manifest → model.

**Enterprise Example.** Contract review receives clauses from authorized agreements and effective policy.

**Detection Metrics.** ACL rejects, freshness, recall/precision, lost-position, unsupported claims.

**Trade-offs.** Snapshotting adds storage and latency.

## Memory

### P-04 — Provenance-bound tiered memory

**Problem.** Useful facts must persist safely.

**Anti-Pattern.** Write every interaction to one vector store.

**Why It Fails.** Errors, secrets, stale facts, and injected instructions persist.

**Recommended Pattern.** Separate working/episodic/semantic/profile memory with purpose, scope, TTL, provenance, verification, deletion.

**Architecture.** Candidate → gate → MemoryRecord → scoped retrieval → revalidation.

**Enterprise Example.** Store a verified communication preference, not inferred sensitive identity.

**Detection Metrics.** Write acceptance, stale retrieval, corrections, cross-scope access, memory failures.

**Trade-offs.** Strict eligibility reduces personalization.

## Tools

### P-05 — Proposal–authorize–commit tool façade

**Problem.** An agent must cause a business effect.

**Anti-Pattern.** Direct broad CRUD call with ambient credentials.

**Why It Fails.** Language becomes authorization and retries duplicate work.

**Recommended Pattern.** Typed tool, least privilege, policy, proposal/grant, idempotency, reconciliation.

**Architecture.** Proposal → policy/approval → façade → effect → receipt → acceptance.

**Enterprise Example.** Payment proposal binds invoice, amount, account, policy, expiry, version.

**Detection Metrics.** Denials, invalid args, grant mismatch, duplicates, unknown effects.

**Trade-offs.** Controls add latency; automate low-risk checks.

## Multi-agent collaboration

### P-06 — Typed task ownership and join

**Problem.** Specialists collaborate under one outcome.

**Anti-Pattern.** Free-form agent chat owns work.

**Why It Fails.** Duplicate owners, cycles, lost artifacts, premature completion.

**Recommended Pattern.** TaskEnvelope, one owner, authority, deadline, artifacts, cancellation, deterministic join.

**Architecture.** Supervisor → task service → specialists → accepted artifacts → join.

**Enterprise Example.** Finance, legal, and security deliver required due-diligence artifacts.

**Detection Metrics.** Orphans, owner conflicts, fan-out, join age, late effects.

**Trade-offs.** Formal tasks reduce spontaneity.

## Security

### P-07 — Least-privilege capability envelope

**Problem.** Agents need sensitive access.

**Anti-Pattern.** One reusable token follows the chain.

**Why It Fails.** Injection or compromise gains broad authority.

**Recommended Pattern.** Subject+workload identity and short-lived audience/purpose/resource/spend/time scope.

**Architecture.** Identity → policy → capability lease → gateway/tool enforcement.

**Enterprise Example.** Procurement may read supplier and propose screening, not approve payment.

**Detection Metrics.** Scope/age, expansion, cross-tenant attempts, denials.

**Trade-offs.** Fine-grained policy needs templates/simulation.

## Reliability

### P-08 — Effect ledger and reconciliation

**Problem.** Timeout may follow a committed external effect.

**Anti-Pattern.** Timeout means failure and retry.

**Why It Fails.** Logical effect can execute twice.

**Recommended Pattern.** Prepared EffectRecord, stable key, unknown terminal, authoritative reconciliation.

**Architecture.** Prepare → dispatch → receipt/unknown → reconcile → accept.

**Enterprise Example.** Vendor creation timeout is queried by idempotency key before retry.

**Detection Metrics.** Unknown rate/age, duplicate effects, reconcile latency.

**Trade-offs.** Requires downstream receipts/query.

## Observability

### P-09 — Causal run graph

**Problem.** Diagnosis spans model, context, policy, tools, humans, effects.

**Anti-Pattern.** Independent logs and transcripts.

**Why It Fails.** First divergence and outcome/cost attribution are lost.

**Recommended Pattern.** Correlated graph linking request, release, context, decisions, effects, acceptance, outcome.

**Architecture.** Trace IDs + domain IDs → spans/events → evidence/evaluation join.

**Enterprise Example.** Trace reveals stale retrieval before a correct but misinformed tool call.

**Detection Metrics.** Unlinked spans, missing versions, outcome join, diagnosis time.

**Trade-offs.** Capture is costly/sensitive; sample and reference payloads.

## Governance

### P-10 — Risk-tiered evidence gates

**Problem.** Behavior changes often but review is finite.

**Anti-Pattern.** Manual-review everything or auto-deploy from one score.

**Why It Fails.** Fatigue or self-certification hides risk.

**Recommended Pattern.** Classify risk and require proportional tests, reviewers, canary, rollback.

**Architecture.** ChangeBundle → risk → validation → approval → staged release.

**Enterprise Example.** Typo auto-promotes; hiring memory/model changes require domain/privacy/risk approval.

**Detection Metrics.** Bypass, fatigue, exception age, regression escape.

**Trade-offs.** Risk classification needs calibration.

## Operations

### P-11 — Durable runtime with backpressure

**Problem.** Runs face bursts, waits, humans, unreliable dependencies.

**Anti-Pattern.** Synchronous workers retry locally.

**Why It Fails.** State is lost and outages amplify queues/retries.

**Recommended Pattern.** Durable state, leases, timers, bounded retries, permits, quotas, circuits, degraded mode.

**Architecture.** Ingress → admission → durable queue/workflow → bounded workers → bulkheads.

**Enterprise Example.** During registry degradation, protected writes pause and queues stay bounded.

**Detection Metrics.** Queue age, permits, retry amplification, saturation, recovery.

**Trade-offs.** Durability adds operational complexity.

## System architecture

### P-12 — Portable contracts and adapters

**Problem.** Multiple frameworks/providers must coexist.

**Anti-Pattern.** App code depends on provider-native objects.

**Why It Fails.** Migration rewrites apps and controls diverge.

**Recommended Pattern.** Platform-owned contracts and normalized events with conformance-tested adapters.

**Architecture.** Application contracts → adapters → shared services → providers/protocols.

**Enterprise Example.** Framework migration preserves tools, policy, traces, evaluation, release.

**Detection Metrics.** Native leakage, conformance failures, migration effort.

**Trade-offs.** Abstraction may lag novel features; allow negotiated extensions.

## Transition to Chapter 17

Pattern selection is easier when failure shapes are visible; Chapter 17 recasts recurring anti-patterns as measurable replacement decisions.

# 17 — Enterprise Anti-Pattern Catalog

## Field-guide method

Anti-patterns are recurring system shapes, not isolated defects. Almost every card below is one mistake wearing different clothes: a probabilistic component was handed a job that belongs to deterministic infrastructure. Diagnose the failed responsibility boundary rather than the symptom, because fixing the symptom — a better prompt, one more retry, a stricter classifier — leaves the boundary intact and the failure returns under a new name.

[[DIAGRAM:anti-before-after|Figure 17-1 — Autonomous monolith versus governed agentic architecture]]

Cards are grouped by the boundary they violate rather than by the technology involved, so that two candidates competing for the same fix sit next to each other. Every card carries the same eight fields, which makes them comparable without re-reading prose.

### Catalog index

| **ID** | **Anti-pattern** | **First symptom you will see** | **Boundary it violates** |
| --- | --- | --- | --- |
| AP-01 | Autonomous monolith | Work is lost on restart and repeated on retry | Reasoning versus execution |
| AP-11 | Unbounded loops and recursive delegation | Cost and step count have a long tail with no ceiling | Reasoning versus budget |
| AP-02 | Prompt as database | Behaviour changes after a long conversation is summarized | Context versus state |
| AP-09 | Vector store as source of truth | Confident answers cite superseded documents | Retrieval versus authority |
| AP-13 | Memory write by default | A wrong fact persists across sessions and spreads | Convenience versus provenance |
| AP-03 | Ambient authority | One credential can reach far more than the task needs | Identity versus authorization |
| AP-10 | LLM judge as security gate | The same input is allowed on one run and blocked on the next | Evaluation versus enforcement |
| AP-12 | Ungated tool discovery and catalog dumping | Token cost rises and the agent selects irrelevant tools | Discovery versus eligibility |
| AP-04 | Retry everywhere | One logical operation produces many downstream calls | Failure handling versus ownership |
| AP-05 | Timeout means failure | Duplicate records appear after a slow dependency | Transport versus effect |
| AP-06 | Boolean or conversational approval | An approval authorizes something nobody reviewed | Consent versus grant |
| AP-07 | Model says done | Runs close successfully with obligations outstanding | Narration versus acceptance |
| AP-08 | Multi-agent chat as workflow | Agents wait on each other and nobody owns completion | Conversation versus coordination |
| AP-14 | Telemetry without causal or effect lineage | Component metrics improve while outcomes get worse | Monitoring versus attribution |
| AP-15 | Model or provider swap as configuration | Behaviour shifts with no code change and no release record | Configuration versus behaviour |
| AP-16 | In-place change and test after release | A failing run cannot be reproduced or rolled back exactly | Convenience versus immutability |

### How to read a card

**Problem** states what the team was legitimately trying to achieve — no card here describes carelessness. **Anti-Pattern** is the shape that gets built. **Why It Fails** gives the mechanism, which is what you need in order to recognise the same failure in an unfamiliar system. **Enterprise Example** is a concrete instance from the Northstar supplier-onboarding scenario used throughout this book. **Recommended Pattern**, **Architecture**, **Detection Metrics** and **Trade-offs** then give the fix, its shape, the signals that tell you whether you still have the problem, and the honest cost of the correction.

The trade-off field matters. Every correction in this catalog costs something — latency, flexibility, or engineering time — and applying all sixteen to a read-only internal assistant would be malpractice. Correct in order of the blast radius of the effects involved.

## Reasoning and control flow

These two failures share a root cause: the model is allowed to decide when to stop. Once stopping is a model decision, termination, budget, and blast radius all become probabilistic properties of a text generator, and no amount of prompt tuning makes them deterministic again. The correction in both cases is to move the stopping decision into code that the model cannot reach.

### AP-01 — Autonomous monolith

**Problem.** A prototype that worked convincingly in a notebook is promoted toward production. It mixes reasoning, run state, credentials, tool invocation, retries, approval, and its own completion signal in a single process, because nothing in the prototype phase forced those concerns apart.

**Anti-Pattern.** One unconstrained agent owns end-to-end control. The loop decides what to do, does it, and then declares the outcome.

**Why It Fails.** Probabilistic behaviour becomes the control plane. There is no boundary at which a failure can be isolated, so a flawed reasoning step and a failed database write are indistinguishable from outside the process. Run state lives in memory, so a restart loses work that has already had external effects. Nothing can be replayed, because nothing durable was recorded — the transcript is a narrative, not a ledger.

**Enterprise Example.** Supplier onboarding restarts after a routine deploy and creates the vendor a second time, because the only record that the vendor already existed was the agent's own conversation history.

**Recommended Pattern.** A bounded runtime inside a durable workflow, with policy, tool and effect, and acceptance services each owning their decision.

**Architecture.** Monolith → direct tools → "done" becomes workflow → semantic nodes → governed effects → acceptance.

**Detection Metrics.** Protected calls that bypass the gateway, work lost per restart, false-completion rate, and the number of distinct responsibilities living in one process.

**Trade-offs.** Decomposition adds interfaces, deployment surface, and latency. Decompose around the highest-risk effects first; a read-only assistant does not need the full split.

### AP-11 — Unbounded loops and recursive delegation

**Problem.** Work varies in complexity, and a fixed step count either truncates hard cases or wastes budget on easy ones, so the team lets the agent iterate and delegate as needed.

**Anti-Pattern.** Agents iterate and spawn children with per-call limits but no global ceiling. Each individual decision looks reasonable.

**Why It Fails.** Local limits do not compose. A depth limit of five with a fan-out of five is 3,125 leaf tasks, and each child inherits a fresh budget rather than a share of the parent's. Delegation graphs become cyclic when two specialists can each call the other, and no participant can detect the cycle from inside it. Queue saturation then degrades unrelated tenants, which is how one runaway research task becomes a platform incident.

**Enterprise Example.** A research supervisor spawns fact-checkers that themselves spawn fact-checkers; the run consumes a day of tenant quota before a human notices, and every individual agent behaved exactly as instructed.

**Recommended Pattern.** Global budgets that decrease monotonically across delegation, an acyclic ownership graph, and explicit depth, fan-out, and no-progress limits enforced by the runtime rather than by instructions.

**Architecture.** Recursion becomes a runtime-governed task graph.

🐍 · anti-pattern and correction

```python
# Anti-pattern: every child starts fresh, so the ceiling is depth x fan-out.
async def delegate(task):
    child = Budget(tokens=20_000, usd=1.00, depth=3)   # reset on every hop
    return await worker.run(task, budget=child)

# Correction: the parent's remaining budget is the source, and delegation is
# a withdrawal from it. A child can never be granted more than its parent
# still holds, so the whole subtree is bounded by the root's admission.
async def delegate(task, parent: Budget):
    if parent.depth <= 0:
        raise DelegationDepthExceeded(task.id)
    share = parent.reserve(tokens=task.estimate, fraction=0.4)
    child = share.narrowed(depth=parent.depth - 1)
    if task.owner in parent.ancestors:         # acyclic ownership
        raise DelegationCycle(task.owner)
    return await worker.run(task, budget=child)
```

**Detection Metrics.** Delegation depth and fan-out distributions, repeated state signatures, no-progress step count, and budget-exhaustion rate by tenant.

**Trade-offs.** Caps truncate genuinely hard work. Set them from observed distributions rather than intuition, and make exhaustion a visible, escalatable terminal rather than a silent stop.

## Context, knowledge and memory

Everything an agent believes arrives through one of these three channels, and all three fail the same way: a convenient representation is mistaken for an authoritative one. A transcript is convenient. A similarity hit is convenient. A remembered fact is convenient. None of them is a system of record, and treating any of them as one moves business truth into a store with no owner, no schema, and no audit.

### AP-02 — Prompt as database

**Problem.** Business state has to survive across turns, restarts, and handoffs, and the conversation already contains it.

**Anti-Pattern.** Chat history, or a rolling summary of it, is treated as the authoritative record of what has happened.

**Why It Fails.** Every mechanism that keeps a context window viable is lossy. Truncation drops the oldest facts, which are often the decisions; summarization paraphrases, and a paraphrase of "legal approved with conditions" is not a legal approval. There is no concurrency control, so two turns that both update a value silently diverge. There is no schema, so nothing detects that a field went missing. And there is no audit trail an investigator can read.

**Enterprise Example.** A contract renewal forgets that legal approved with conditions, because the approval was three summarization rounds ago and the summary kept the outcome but dropped the conditions.

**Recommended Pattern.** Canonical typed state in a service that owns it, with the prompt receiving a ContextManifest projection built fresh from that state on every step.

**Architecture.** Transcript-as-state becomes State Service → snapshot → prompt.

🐍 · anti-pattern and correction

```python
# Anti-pattern: the transcript is the record, so whatever survives
# compaction is what the system believes.
messages.append({"role": "assistant", "content": "Legal approved with conditions."})
context = summarize(messages, max_tokens=4_000)

# Correction: state is written to a typed store and the prompt is a
# projection of it. Compaction can lose the sentence without losing the fact,
# and the approval remains queryable, auditable, and concurrency-safe.
await state.record(ApprovalEvent(
    run_id=run.id, authority="legal", disposition="approved_with_conditions",
    conditions=["indemnity_cap_2m", "termination_notice_90d"],
    version=state.version,                     # optimistic concurrency
))
context = ContextManifest.project(await state.snapshot(run.id), budget=4_000)
```

**Detection Metrics.** Facts lost across compaction boundaries, disagreement between summary and store, and state mismatches discovered on recovery.

**Trade-offs.** Typed state requires schema design and migration discipline. The cost lands early and visibly, which is precisely why it gets deferred.

### AP-09 — Vector store as source of truth

**Problem.** Relevant knowledge has to be found across a corpus too large to pass into a prompt.

**Anti-Pattern.** A similarity hit is treated as a current, authorized, authoritative fact.

**Why It Fails.** Similarity measures resemblance, not currency, authority, or permission. An index contains what was ingested, including superseded policies, duplicated drafts, documents the caller may not read, and anything an attacker managed to insert. Nothing in a cosine score distinguishes the approved policy from its withdrawn predecessor, and a confident citation of the wrong document is more damaging than no citation at all.

**Enterprise Example.** An obsolete policy chunk applies a superseded spending limit, and the answer cites the document by name, which is what makes the reviewer believe it.

**Recommended Pattern.** Governed sources and snapshots hold authority; the index is a derived locator whose hits are verified for ACL, freshness, and supersession before the content reaches the model.

**Architecture.** Vector hit → action becomes source + ACL + snapshot → evidence → decision.

**Detection Metrics.** Evidence age at decision time, source disagreement rate, ACL mismatches at retrieval, and citations pointing at superseded revisions.

**Trade-offs.** Authoritative lookup adds latency to every retrieval. Apply it in proportion to what the answer will be used for; drafting assistance and payment authorization do not need the same guarantee.

### AP-13 — Memory write by default

**Problem.** Personalization is genuinely valuable, and the cheapest way to get it is to remember everything.

**Anti-Pattern.** Every interaction, or a summary of it, becomes a durable memory record.

**Why It Fails.** Writing by default means writing without provenance, purpose, or verification. Secrets get persisted. Model errors get persisted and then retrieved as established fact, which is how one hallucination becomes a standing belief. Injected instructions from a document become durable instructions. And because nothing recorded why a memory was written, nothing can decide when it should expire or who may delete it — which turns a retention obligation into an archaeology project.

**Enterprise Example.** A malicious email is processed, and the bank account it contains is stored as the supplier's preferred payment detail. Every subsequent run retrieves it as a remembered fact about a known supplier.

**Recommended Pattern.** Memory writes are candidates, not side effects: purpose-bound, carrying provenance, verified before promotion, scoped to a tenant and subject, with a TTL and a deletion path.

**Architecture.** Transcript → memory becomes candidate → gate → typed record.

🐍 · anti-pattern and correction

```python
# Anti-pattern: the model decides what is worth remembering, and the write
# path has no provenance, no purpose, and no way to expire.
memory.write(user_id, summarize(conversation))

# Correction: a write is a proposal that must survive a gate. Untrusted
# provenance cannot become durable memory, and every record carries the
# purpose that justifies its retention.
candidate = MemoryCandidate(
    subject=case.case_id, tenant=run.tenant, purpose="mortgage_evidence_review",
    claim=extracted.claim, provenance=extracted.source,   # which document, which ACL
    confidence=extracted.confidence, ttl_days=180,
)
if gate.admits(candidate):        # source trust, purpose match, no secrets, corroboration
    memory.write(candidate.as_record())
else:
    audit.rejected(candidate, reason=gate.reason)
```

**Detection Metrics.** Sensitive-data writes caught by DLP, retrieval of stale records, correction and deletion rates, and incidents traceable to a single memory record.

**Trade-offs.** A strict write path reduces the perceived magic of personalization and requires someone to own purpose definitions. The alternative is an unowned database of unverified claims about your customers.

## Security and delegated authority

The three cards here are the difference between *can* and *may*. An agent that can reach a resource, can see a tool, or can produce a plausible safety score has demonstrated capability, not permission. Each card is a case where capability was allowed to stand in for a policy decision, and in each the correction is the same: make the authorization decision explicitly, in code, at the moment of use.

[[DIAGRAM:anti-ambient-authority|Figure 17-2 — Ambient authority versus a narrowed, short-lived capability lease]]

### AP-03 — Ambient authority

**Problem.** Agents need access to enterprise systems, and provisioning narrow credentials for every task and tenant is laborious.

**Anti-Pattern.** Workers receive broad, long-lived, reusable credentials — often a service account that predates the agent and was already over-scoped.

**Why It Fails.** The credential's scope, not the task's need, defines the blast radius. Any compromise — prompt injection, a malicious tool, a leaked log — yields durable authority over everything the credential can reach. Because the same credential serves every run, nothing in the audit trail distinguishes which subject's work caused which effect, so attribution fails exactly when it is needed. And a credential that never expires cannot be revoked faster than someone notices.

**Enterprise Example.** The support agent's token can export the full customer table. Nothing in the onboarding task requires it; the token was reused because it already existed.

**Recommended Pattern.** Preserve both subject and workload identity, derive a capability envelope by intersection, and mint a short-lived, audience-bound credential lease at the moment of use.

**Architecture.** Broad token becomes policy → scoped lease → enforcement at the resource.

**Detection Metrics.** Credential scope and age distributions, granted-but-unused privilege, scope-expansion attempts, and cross-tenant access denials.

**Trade-offs.** Fine-grained policy adds design effort and a policy-decision hop per call. The hop is cacheable; the design effort is not, and it is the part teams underestimate.

### AP-10 — LLM judge as security gate

**Problem.** Some content is genuinely ambiguous, and a model is better than a regular expression at recognising nuance.

**Anti-Pattern.** A model-produced score alone authorizes a protected action — `if risk_score < 0.3: execute()`.

**Why It Fails.** A judge is an injectable, nondeterministic component being asked to make a binding decision. The same input can score differently across runs, so the gate is not reproducible and an incident cannot be explained. The content being judged can address the judge directly, which makes the attacker a participant in their own authorization. And judge behaviour drifts with model updates, silently moving the threshold without any release event.

**Enterprise Example.** The judge classifies an unusually large payment as low risk because the request text explains, persuasively, why it is routine.

**Recommended Pattern.** A deterministic policy and invariant gate makes the decision. The judge triages, prioritizes, and supplies evidence for a human — it never holds the authorization.

**Architecture.** `score > threshold → execute` becomes policy → optional judge → human escalation.

**Detection Metrics.** Disagreement rate across repeated runs of identical input, gate bypass attempts, false negatives found downstream, and human override frequency.

**Trade-offs.** Deterministic rules genuinely cannot express every nuance, and some legitimate work will be escalated unnecessarily. That is the correct direction to fail.

### AP-12 — Ungated tool discovery and catalog dumping

**Problem.** A mature platform has many tools, and the agent cannot use what it cannot see.

**Anti-Pattern.** Every discovered tool and its full schema is placed into the prompt, often straight from an MCP server's advertised catalog.

**Why It Fails.** Discovery is being used as authorization. Selection accuracy falls as the catalog grows, because the model is choosing among near-neighbours it has no basis to distinguish. Schemas consume context that evidence should occupy. Worse, tool descriptions are untrusted text from a third party, so a malicious server can write a description engineered to attract calls — the agent is reading attacker-controlled instructions and treating them as a menu.

**Enterprise Example.** A reporting agent discovers an administrative delete tool, because the catalog was filtered by connectivity rather than by the caller's authority.

**Recommended Pattern.** Registry → eligibility and policy evaluation → task-specific shortlist → schema validation at call time. Eligibility is computed from the subject, purpose, tenant, and risk tier, never from what the server happens to advertise.

**Architecture.** Full MCP catalog becomes an approved tool slice bound to a lease.

**Detection Metrics.** Tools exposed versus eligible versus actually used, selection-confusion rate, schema token overhead per run, and unauthorized discovery attempts.

**Trade-offs.** A narrow shortlist will sometimes omit a tool that would have helped. Make the omission observable so the shortlist can be improved deliberately, rather than widening it by default.

## Effects, retries and recovery

These two cards are the most expensive in the catalog, because they produce duplicate real-world effects — duplicate payments, duplicate vendors, duplicate emails to customers. Both stem from confusing the transport layer with the effect layer: a failed call is not a failed effect, and an unacknowledged call is not an absent one.

[[DIAGRAM:anti-retry-storm|Figure 17-3 — Layered retries and timeout-as-failure versus one retry owner with an unknown-effect terminal]]

### AP-04 — Retry everywhere

**Problem.** Transient failures are real and common, and every layer in the stack offers a retry setting that looks like diligence.

**Anti-Pattern.** The SDK, the gateway, the workflow engine, the connector, and the tool each retry independently.

**Why It Fails.** Retries compose multiplicatively, not additively. Three layers at 3, 3, and 2 attempts produce eighteen calls for one logical operation, and each layer believes it made a modest choice. The amplification arrives precisely when a dependency is already degraded, converting a slow dependency into an outage. If any layer retries a non-idempotent call, the duplicates are permanent.

**Enterprise Example.** A single supplier screening produces eighteen calls to the sanctions registry, and the vendor rate-limits the enterprise for the rest of the day.

**Recommended Pattern.** One retry owner per failure class, with a shared attempt and deadline budget that every layer reads and no layer resets.

**Architecture.** Nested retries become classified failure → one schedule → terminal.

🐍 · anti-pattern and correction

```python
# Anti-pattern: each layer is independently "resilient". 3 x 3 x 2 = 18.
client = HttpClient(retries=3)
gateway = ToolGateway(client, retries=3)
workflow.call(gateway, retry_policy=RetryPolicy(max_attempts=2))

# Correction: exactly one owner retries, chosen by failure class, and the
# budget travels with the run so no layer can restart the count.
client  = HttpClient(retries=0)                 # transport never retries
gateway = ToolGateway(client, retries=0)        # gateway never retries
workflow.call(gateway, retry_policy=RetryPolicy(
    owner="workflow",
    classify=classify_failure,                  # transient | permanent | unknown
    retry_on={"transient"},                     # permanent fails fast, unknown reconciles
    budget=run.attempt_budget,                  # shared, decreasing, deadline-aware
))
```

**Detection Metrics.** Attempts per logical operation, amplification factor against dependencies, duplicate effect keys, and deadline overruns caused by retry time.

**Trade-offs.** A single central policy is necessarily more conservative than a hand-tuned one per call site. Express the variation as failure classes rather than as per-layer settings.

### AP-05 — Timeout means failure

**Problem.** A response is lost after a request was dispatched, and the run has to decide what to do next.

**Anti-Pattern.** The call is marked failed and retried immediately.

**Why It Fails.** A timeout describes the response, not the effect. The first call may have committed, may be committing, or may never have arrived, and the caller cannot distinguish these from the outside. Treating that state as failure asserts knowledge the system does not have, and the retry then creates the duplicate that the timeout only made possible.

**Enterprise Example.** The vendor is created twice: the first call committed just after the client gave up waiting.

**Recommended Pattern.** An explicit unknown-effect terminal that blocks retry until reconciliation resolves it against the downstream system of record.

**Architecture.** timeout → failed → retry becomes timeout → unknown → lookup → decide.

🐍 · anti-pattern and correction

```python
# Anti-pattern: timeout is treated as proof that nothing happened.
try:
    return await mortgage_documents.request(payload)
except TimeoutError:
    return await mortgage_documents.request(payload)  # may now exist twice

# Correction: unknown is a first-class terminal. Nothing retries a mutation
# until the downstream record has been consulted about what actually landed.
try:
    return await mortgage_documents.request(payload, idempotency_key=effect.key)
except TimeoutError:
    effect.mark(EffectState.UNKNOWN)            # durable, visible, blocks retry
    actual = await mortgage_documents.lookup(idempotency_key=effect.key)
    if actual is not None:
        return effect.resolve(committed=actual)  # it did land; adopt it
    return effect.resolve(committed=None)        # genuinely absent; now safe to retry
```

**Detection Metrics.** Count and age of unresolved unknown effects, duplicate idempotency keys observed downstream, and conflicts discovered after a timeout.

**Trade-offs.** Unknown terminals delay completion and need somewhere to go when reconciliation cannot resolve them. That queue is the price of not creating duplicate financial records.

## Approval, acceptance and governance

Both cards here concern the moment a system decides that something is allowed, or that something is finished. In each, a cheap signal — a Boolean, a sentence of model output — was allowed to carry a decision that the enterprise will later be asked to defend. The correction is to make the decision an artifact: something with a hash, an owner, an expiry, and an independent check.

[[DIAGRAM:anti-approval-binding|Figure 17-4 — Boolean consent versus a proposal-bound, expiring approval grant]]

### AP-06 — Boolean or conversational approval

**Problem.** Humans must approve protected actions, and a chat interface makes approval feel natural.

**Anti-Pattern.** A Boolean flag or a chat message — "yes, go ahead" — authorizes whatever the arguments happen to be at execution time.

**Why It Fails.** Approval is being bound to a conversation rather than to an effect. Between consent and commit, the amount, the recipient, the policy version, the acting workload, or the underlying record can all change, and nothing detects it. The approver reviewed a description; the system executes a payload. A Boolean also cannot express scope or expiry, so a single "yes" silently authorizes later, larger, and unrelated actions.

**Enterprise Example.** An approval given for a $10,000 payment is reused, entirely within policy as implemented, for a $100,000 one.

**Recommended Pattern.** An immutable proposal, hashed over the exact effect, with an ApprovalGrant bound to that hash, scoped to one action, and carrying an expiry. Revalidate immediately before commit.

**Architecture.** `approved=true` becomes proposal hash → grant → revalidate → commit.

🐍 · anti-pattern and correction

```python
# Anti-pattern: consent is a flag on the run, detached from what executes.
if run.approved:
    await underwriting.submit_evidence_package(case_id=current.case_id)

# Correction: the grant is bound to a hash of the exact proposal and cannot
# authorize a payload the approver never saw.
proposal = Proposal(
    action="underwriting.submit_evidence_package",
    args=args,
    policy_version=policy.version,
)
grant = await approvals.await_grant(proposal.digest(), ttl_s=900)

if grant.digest != proposal.digest():      # arguments moved since approval
    raise ApprovalMismatch(proposal.digest(), grant.digest)
if grant.expired(now()):                   # consent has a shelf life
    raise ApprovalExpired(grant.id)
await underwriting.submit_evidence_package(
    **proposal.args, idempotency_key=proposal.digest()
)
```

**Detection Metrics.** Proposal-hash mismatches at commit, grant reuse attempts, expiry rate, and incidents occurring after a recorded approval.

**Trade-offs.** Benign changes force reapproval, which approvers experience as friction. Tune by making the diff visible — showing what changed is cheaper than widening the grant.

### AP-07 — Model says done

**Problem.** A run needs a completion signal, and the model produces a confident, well-formed one for free.

**Anti-Pattern.** The model's assertion sets the run to success.

**Why It Fails.** The model is reporting on its own work using the same faculty that produced it. A missing evidence artifact, a skipped approval, an uncommitted effect, or an unmet obligation all present as success, because none of them changes what the model believes it did. Failures therefore surface downstream — in reconciliation, in audit, or in a customer complaint — long after the trace has aged out.

**Enterprise Example.** Onboarding reports complete while the sanctions screening is stale, because the model saw a screening result in context and did not evaluate its freshness.

**Recommended Pattern.** An independent, executable acceptance check evaluated over authoritative state, returning accepted, blocked, needs-input, failed, or unknown-effect. The model may propose completion; it may not declare it.

**Architecture.** Model text → success becomes AcceptanceEngine → typed terminal.

**Detection Metrics.** False-completion rate found by audit, reopen rate, and runs closed with missing artifacts or uncommitted effects.

**Trade-offs.** Executable acceptance criteria need domain ownership and maintenance. Without them the completion signal has no author, which is worse and merely less visible.

## Multi-agent collaboration

### AP-08 — Multi-agent chat as workflow

**Problem.** Specialists need to coordinate, and a shared conversation is the fastest coordination mechanism to build.

**Anti-Pattern.** Free-form messages between agents own state, work assignment, deadlines, and completion.

**Why It Fails.** A conversation has no notion of ownership, so two agents can both believe the other is acting — or both act. It has no join semantics, so nothing knows when parallel work has finished. Cancellation cannot propagate, because there is no structure to propagate through, and artifacts produced mid-conversation are lost when the window compacts. The system behaves like a meeting with no chair and no minutes.

**Enterprise Example.** Finance and legal each wait for the other to approve. The run sits open for three days and neither agent is wrong.

**Recommended Pattern.** A typed TaskEnvelope with exactly one accountable owner, explicit child tasks, artifacts stored by reference, and a deterministic join evaluated by the coordinator rather than inferred from messages.

**Architecture.** Chat mesh becomes supervisor workflow plus task service.

**Detection Metrics.** Orphaned tasks, conflicting concurrent effects, delegation depth, join wait age, and effects landing after a run was considered complete.

**Trade-offs.** Formal task envelopes reduce the fluidity that makes agent conversations appealing to demonstrate. The fluidity is what fails in production.

## Observability and evidence

### AP-14 — Telemetry without causal or effect lineage

**Problem.** Teams instrument what they own, and each component's dashboard looks healthy.

**Anti-Pattern.** Logs, metrics, and traces cannot be joined to versions, policy decisions, effects, acceptance, or business outcome.

**Why It Fails.** Without a join key, every measurement is local. A component can improve on its own metric while degrading the outcome, and nothing in the telemetry can express the relationship. Cost cannot be attributed to a tenant, a release, or a decision, so optimization targets whatever is easiest to measure. When an incident happens, the investigation has to reconstruct causality by hand from timestamps.

**Enterprise Example.** A model swap lowers median latency by 15%, which the dashboard celebrates, while retries rise and task completion falls. Both facts are true and neither dashboard contains both.

**Recommended Pattern.** One causal run graph joining release version, context manifest, model and policy decisions, tool effects, acceptance terminal, business outcome, and cost.

**Architecture.** Separate dashboards become one correlated graph.

**Detection Metrics.** Percentage of runs joinable to a business outcome, spans missing parent or version identifiers, and unattributed spend.

**Trade-offs.** Correlation requires disciplined identifier propagation across every component and raises the governance burden on telemetry, including redaction. Retrofitting it after an incident costs considerably more.

## Platform, release and operations

Both cards describe the same instinct — change should be fast — applied where it removes the ability to explain, reproduce, or undo what happened. Speed is not the problem; unversioned speed is.

### AP-15 — Model or provider swap as configuration

**Problem.** Teams want better cost or quality, and the routing layer makes the change a one-line edit.

**Anti-Pattern.** A model alias is repointed without behavioural validation, because no application code changed.

**Why It Fails.** The model is the behaviour. Tool-calling reliability, schema adherence, refusal boundaries, safety posture, latency distribution, and cost per task all shift together, and they shift unevenly across slices — a change that is neutral in aggregate can be severe for one language, one document type, or one tenant. Because no release event was recorded, the resulting regression has no obvious cause and cannot be rolled back precisely.

**Enterprise Example.** A cheaper model drops tool arguments for one language only. Aggregate evaluation stays green; that market's completion rate halves.

**Recommended Pattern.** A versioned ChangeBundle carrying evaluation across slices, security testing, load testing, canary exposure, and a named rollback target.

**Architecture.** Edit alias becomes immutable route policy → replay → approval → canary.

**Detection Metrics.** Schema and tool-call regression rate, refusal-rate shift, per-slice quality drift, and fallback-route activation.

**Trade-offs.** Validation slows experimentation, so make the fast path cheap: pre-built replay sets and automated slice reports, rather than an approval meeting.

### AP-16 — In-place change and test after release

**Problem.** A production issue needs a fix now, and the console offers an edit box.

**Anti-Pattern.** Prompts, Skills, tool definitions, policy, and routes are mutated directly in production.

**Why It Fails.** A run can no longer be reproduced, because the artifacts it used no longer exist in the form it used them. Attribution fails, since two runs a minute apart may have used different behaviour with no record of the boundary. Rollback becomes guesswork about what the previous state was. And the edit itself is untested by construction — the test is the production traffic.

**Enterprise Example.** A prompt edit intended to reduce verbosity increases data leakage. Neither the previous prompt nor the exact leak conditions can be reconstructed.

**Recommended Pattern.** Immutable artifacts, a ReleaseManifest that pins everything a run resolves, pre-promotion tests, signed promotion, canary exposure, and a rollback target that is verified rather than assumed.

**Architecture.** Mutable console becomes build → validate → approve → promote → monitor.

**Detection Metrics.** Runs executing unversioned artifacts, out-of-band edit events, and rollback rehearsal failures.

**Trade-offs.** Immutability needs genuinely good tooling, or people will route around it under pressure. If the emergency path is slower than the console, the console wins — so make the fast path immutable rather than making immutability optional.

|  |
| --- |
| **COMMON PITFALL**  The most expensive anti-patterns in this catalog are not the exotic ones. AP-04, AP-05, and AP-06 produce duplicate payments, duplicate records, and unauthorized effects, and all three look like ordinary engineering diligence while they are being built. Audit those three first. |

## Transition to Chapter 18

After removing unsafe local architectures, Chapter 18 considers when multiple agents add justified specialization rather than accidental complexity.
