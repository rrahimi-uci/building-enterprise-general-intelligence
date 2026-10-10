# PART IV — PATTERNS THAT WORK—AND THOSE THAT FAIL

Patterns are shortcuts for thinking, but they are only helpful when their
boundaries are visible. Every pattern in Chapters 10–15 places a model step
inside the platform of Part III: the step receives a resolved slice of Skills
and tools (Chapters 8–9), its outputs cross the six gates (Chapter 2), and the
framework stays behind AgentRuntime (Chapter 3). Each chapter answers three
questions: what the model may decide, what the controller owns, and how the
pattern stops and is accepted. The Part starts with the smallest bounded loop,
then follows routing, planning, reflection, human review, and durable work. It
ends by comparing and combining these patterns, then naming the failure shapes
they prevent—several corrected by mechanisms Parts V–VIII build—so a design
review can ask not only “what could work?” but also “how would this fail in
production?”

# 10 — Use ReAct Without Creating a Runaway Loop

> **Evidence context:** ReAct was introduced as a prompting paradigm that interleaves reasoning and action; its reported benchmark results motivate the loop, not an assertion that unrestricted production autonomy is safe. **[R01]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** A loan officer asks why a mortgage case is not ready for underwriting. One retrieval is insufficient: the system may need the application projection, an income-verification artifact, and a policy explanation. A bounded ReAct loop is appropriate because the next information need depends on the previous observation. |

|  |
| --- |
| **THE DESIGN CHOICE** Use ReAct only for information-dependent next steps and impose external turn, tool, time, cost, and no-progress limits. |

ReAct is valuable when the next question depends on the last observation. It
is dangerous when the loop is allowed to decide its own limits or call tools
without a clear stopping rule.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| External loop controller and acceptance engine | observation/model and model/tool | turn · tool permit · run budget | one bounded loop | AgentDecision · Observation · AgentStepResult · ReActLimits |

## Use ReAct only when observations change the next step

Use ReAct when a new observation can genuinely change the next useful question. If the sequence is already known—read the case, validate required fields, calculate a ratio, request approval—a durable workflow is clearer and usually cheaper. That avoids paying a model to rediscover a process the organization already understands. Even when ReAct is justified, the controller should stop when the loop repeats, exhausts its budget, or cannot obtain missing evidence. The tools a ReAct step can call are the slice resolved for that step from its pinned Skills (Chapter 8) and exposed through the Tool Gateway (Chapter 2); the loop never discovers tools on its own.

## Keep the feedback loop inside external limits

[[DIAGRAM:pattern-react|Figure 10-1 — Bounded ReAct: the loop is inside, the limits are outside]]

Read the figure for what is *not* in the loop. The controller admits each turn and owns the budgets; a mutation leaves as a proposal rather than executing inline; and the controller decides when the loop stops (limits, no progress, a terminal decision), while the acceptance engine—not the model's wording—decides whether the result is accepted (Chapter 13). Each turn follows the same sequence:

1. Load goal, authorized context, budgets, and acceptance criteria.
2. Ask for one typed action or terminal decision.
3. Validate the action at the Tool Gateway; execute reads and return mutations as proposals.
4. Sanitize and append the observation.
5. Continue, or end the activity on a terminal decision or an external rule; an answer goes to the acceptance engine.

ReAct interleaves reasoning, action, and observation. Its value is conditional adaptivity: after reading the application projection, the agent may decide that another income source is unnecessary, or that a contradictory address requires another authorized document. The pattern becomes harmful when it substitutes an unconstrained loop for a known process.

The platform stores only typed decisions, tool intents, observations, evidence references, and stop reasons—not private chain-of-thought. Each observation is a typed, sanitized result or artifact reference carrying provenance, version, and classification, and it re-enters context as untrusted data (Chapter 6). The external controller maintains counters and normalized signatures. If an agent repeats the same tool and canonical arguments against the same source revision, or if accepted evidence does not change across turns, the controller records no progress and terminates or escalates. Information gain is the new accepted evidence a turn produces; a turn with none counts toward the no-progress threshold.

### Acceptance and failure semantics

Each turn, the model returns one typed decision, carried in `AgentStepResult.decision` (Chapter 3): `invoke_tool` for a read, `proposed_action` for a mutation, `answer`, `needs_input`, or `delegate`. A read runs inside the loop; a proposed action leaves it as a proposal for the six gates of Chapter 2; `delegate` asks the controller for a route or handoff (Chapter 11). The controller ends the activity with the model's terminal decision or with its own stop reason, `budget_exhausted` or `no_progress`, returned as the Chapter 3 step status `failed` with that `error_code` rather than as an exception; the workflow, not the loop, decides whether a stop reason opens an intervention (Chapter 14). A read that times out may be retried within the run budget. A proposed mutation is executed by the workflow outside the loop; if that execution times out, the effect is unknown and is reconciled before the loop resumes (Chapter 22).

|  |
| --- |
| **COMMON PITFALL**  Unbounded retries disguised as reasoning. When a tool fails and the model is free to try again, the loop can burn its whole budget rediscovering the same error. Return failures as typed data the model can read, cap attempts per tool (see AP-04), and make the cap a run-level budget rather than a per-call one. |

### Capacity model

Plan capacity in turns per verified success (Chapter 28), not only requests per second. A loop's cost is set by its trajectory, not its prompt: each observation re-enters the context, so an n-step loop is roughly quadratic in tokens, and a cheap call that loops eight times is not cheap. Cap the step count, summarize observations before they re-enter, and track model tokens, tool calls, connector time, observation bytes, and repeated-action rate. Per-tenant permits and hard per-run limits prevent one pathological loop from consuming a worker pool. Per-loop caps do not compose across delegation; budgets must be withdrawn from the parent (AP-11).

## ReAct at a glance

| **Use when** | **Do not use when** |
| --- | --- |
| Use for exploratory retrieval, diagnosis, or research with a small eligible tool set and measurable stop conditions. | Avoid for known workflows, single retrievals, protected commits, or open-ended browsing without meaningful limits. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Adaptivity | Handles unknown paths; increases latency, cost, and trajectory variance. |
| Intermediate observations | Improves grounding; increases attack surface and context pressure. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Tool ping-pong | Normalized repeat signatures and no-progress threshold. |
| Context poisoning | Treat observations as untrusted, provenance-labeled data. |
| Budget exhaustion | External turn, call, token, time, and cost enforcement. |

### What you need to see in production

* turn index
* decision type
* eligible tools
* action-observation hash
* information gain
* remaining budgets
* stop reason

## What the evidence lets us conclude

The discussion above draws on R01. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

Two versions of the same loop follow. The first is an OpenAI Agents SDK version in which the run budget lives in the tool context.

[[EXAMPLE:bounded-react-loop]]

The second is the framework-neutral controller the chapter describes: it owns turns, tool budget, and repeat detection, runs only reads, and returns a typed stop reason instead of raising.

[[EXAMPLE:react-engine#core]]

## If this fails in production

1. List every turn with normalized action, observation, token, time, and cost deltas.
2. Identify the first repeated action-observation signature.
3. Check whether the loop stopped on an external rule and whether acceptance came from the acceptance criteria rather than the model's wording.

If limits reset at each delegation hop or every layer retries, see AP-11 and AP-04 in Chapter 17.

## What to verify before production

**✓** The information need truly requires iterative observation.

**✓** The controller owns limits, state, and tool invocation; acceptance is decided outside the loop.

**✓** Observations are typed, sanitized, versioned, and provenance-linked.

**✓** Repeat-action and no-progress signatures are detected.

**✓** Unknown effects or budget exhaustion terminate safely.

## Put the idea to work

1. Add information-gain and repeat-signature stopping to the reference ReAct loop.
2. Compare a one-shot retrieval design with ReAct for the same mortgage-evidence question.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| When is ReAct the right pattern? | When the next information need genuinely depends on a verified prior observation and the loop can be bounded. |
| Why must the controller sit outside the model? | It owns budgets, tool eligibility, invocation, state, no-progress detection, and terminal transitions. |
| How do you stop a ReAct loop that keeps rephrasing the same request? | Normalize action-observation signatures, count repeats, evaluate information gain, and terminate or escalate at a deterministic threshold. |
| What should an observation contain? | The observation contract in § Keep the feedback loop inside external limits, plus explicit error semantics. |
| When should ReAct not be used? | For a known workflow, a single retrieval, a protected transaction, or a task whose acceptance can be computed directly. |

## Where this leads next

A bounded reason–act loop handles local uncertainty. When a turn returns `delegate`, or a known path or specialist should own the work, Chapter 11 adds routing and handoff.

# 11 — Route the Work Without Losing Ownership

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** Some requests are policy questions, others are document defects, evidence disputes, or protected mortgage-case actions. Harborlight needs routing, but it also needs to know when responsibility actually transfers and who owns cancellation, deadlines, and the final response. |

|  |
| --- |
| **THE DESIGN CHOICE** Use deterministic route eligibility and fallback; record handoff as an explicit ownership transition. |

Routing sounds like a classification problem until a real request is late,
ambiguous, or already halfway through a workflow. This chapter separates the
choice of a specialist from the transfer of responsibility, then makes
fallbacks, deadlines, authority, and the final response explicit.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Route service and workflow ownership record | classifier to privileged route; owner transfer | route class · specialist queue | one route or handoff | RoutingDecision · OwnershipTransfer · CapabilityEnvelope |

## Routing and handoff are different events

A routing decision answers “who is best placed to do this?” A handoff answers “who is now accountable for finishing it?” Those are not the same event. Agent frameworks also use the word handoff for passing a conversation to another agent inside one run (Chapter 3). That framework handoff moves control, not accountability. It becomes a handoff in this chapter's sense only when the platform records the transfer and the recipient acknowledges it. If a specialist never acknowledges the task, the original coordinator still owns the deadline and user response. Recording the transfer prevents work from disappearing into a queue while every component assumes someone else has it.

## A routing decision cannot grant permission

[[DIAGRAM:pattern-routing|Figure 11-1 — Routing selects a specialist from an eligible set; authorization decides whether it may act]]

A router reduces heterogeneity by selecting an implementation: policy explanation, document validation, income verification, or human triage. A ReAct step that returns `delegate` (Chapter 10) arrives here as a routing request. The model may classify semantic intent, but the eligible set is assembled first from purpose, authority, risk, data region, release status, service health, and capacity—deterministically, before any model sees the options, the same way Skill resolution works (Chapter 8). A route cannot grant a capability that was absent from the run's capability envelope (Chapter 21). Choosing which model serves a step follows the same eligibility-first rule but belongs to the LLM Gateway (Chapter 4), and model-routing economics to Chapter 28. In order:

1. Build the eligible route set.
2. Classify the request and return route, confidence, and reason.
3. Validate thresholds and constraints.
4. Select the route or deterministic fallback.
5. Measure outcome by route and slice.

### Confidence and fallback

Confidence is calibrated on a versioned domain dataset. Below a threshold, the route service requests clarification, applies a deterministic safe default, or sends the request to a human triage queue (Chapter 14). High confidence does not bypass policy. For privileged routes, both route eligibility and exact invocation authorization are required.

## Handoff transfers accountability

A handoff is needed when another agent or human must become the current interaction or task owner rather than merely provide an answer to the original controller. Frameworks make it easy for one agent to involve another, but the word hides different ownership models.

| **Case** | **What happens** | **Correct abstraction** |
| --- | --- | --- |
| Specialist as a tool | The evidence agent asks a sanctions specialist for analysis and retains responsibility for the final disposition | Agent-as-tool or equivalent local delegation |
| Framework handoff (control only) | A triage agent transfers the bounded conversation to an income-verification specialist; control changes locally but the same activity remains accountable | Framework handoff, with the same external budget and cancellation boundary |
| Accountable handoff (this chapter) | A document-defect specialist takes over the case's evidence follow-up, including its deadline and the final response to the loan officer | Recorded, acknowledged ownership transfer |
| Durable delegation | A fraud investigation needs independent ownership, waits, retries, deadlines, human review, or a cross-service trust boundary | Durable `TaskEnvelope` and child workflow (Chapter 18) |

An accountable handoff changes the current owner of an interaction or task. The current owner creates a typed transfer that records old owner, new owner, state version, unresolved obligations, artifact references, child capability envelope, deadline, cancellation lineage, and acceptance contract.

1. Decide that ownership—not just expertise—must transfer.
2. Persist the handoff proposal.
3. Validate recipient, authority, compatibility, and capacity.
4. Require the recipient to acknowledge or reject; until then, the current owner stays accountable.
5. On acknowledgment, atomically change owner and emit an event; on rejection or timeout, keep the current owner.

A transfer is proposed, then acknowledged, rejected, or expired; only acknowledgment changes the owner. Chapter 18 implements this protocol as the Ownership Service and its `tasks/{id}:handoff` and `:accept` operations; Chapter 21 explains how the child capability envelope is derived.

## Routing at a glance

| **Use when** | **Do not use when** |
| --- | --- |
| Use when candidate paths have materially different capabilities, owners, SLOs, cost, or risk. | Avoid a learned router when a stable deterministic rule is sufficient or misrouting has unacceptable consequences. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Specialization | Can improve quality and cost; creates taxonomy, calibration, and drift work. |
| Learned classification | Handles semantic ambiguity; requires fallback and monitoring. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Low-confidence guess | Clarify, default, or human triage. |
| Route drift | Versioned datasets and confusion-matrix monitoring. |
| Privileged route selection (AP-12) | Eligibility before classification and exact authorization after selection. |
| Persona routing | Route only between implementations with different capabilities, owners, or controls. |

### What you need to see in production

* candidate routes
* eligibility removals
* confidence
* validator reason
* fallback
* route outcome

## Handoff at a glance

| **Use when** | **Do not use when** |
| --- | --- |
| Use for explicit responsibility transfer across specialist, trust, organizational, or channel boundaries. | Use an agent-as-tool when the parent still owns the outcome; use a durable child task when independent recovery is required without conversational transfer. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Clear specialization | Introduces ownership transitions and context-transfer risk. |
| Independent interaction | Reduces supervisor bottlenecks; complicates cancellation and accountability. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Orphaned task (AP-08) | Atomic ownership state and acknowledgment timeout. |
| Authority expansion | Child grant intersection and exact reauthorization. |
| Context loss | Typed artifact and obligation references instead of transcript copying. |

### What you need to see in production

* old and new owner
* handoff reason
* grant lineage
* state and artifact refs
* acknowledgment
* deadline and cancellation

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Framework handoff | The OpenAI Agents SDK documents handoffs as a framework primitive for passing control between agents; recording ownership, acknowledgment, and authority narrowing around it is this book's recommendation. | R29 |

The discussion above draws on R29. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The first listing uses the SDK's framework handoff to switch agents within one run. It moves control, not accountability; the platform records ownership around it (see § Handoff transfers accountability).

[[EXAMPLE:routing-handoff]]

The second computes the eligible set before the model proposes a route, then validates the proposal and falls back instead of guessing.

[[EXAMPLE:route-validation#router]]

## If this fails in production

1. Recompute the eligible route set from recorded purpose, authority, health, and risk.
2. Inspect the confidence threshold and fallback actually used.
3. Confirm the old owner remained accountable until the recipient's acknowledgment was recorded, and that cancellation reached the current owner.

## What to verify before production

**✓** The eligible route set is computed before model selection.

**✓** Confidence, ambiguity, fallback, and default-deny behavior are explicit.

**✓** Routing and handoff are separate contracts.

**✓** Ownership changes only on recorded acknowledgment; state, narrowed authority, deadlines, and cancellation move with it atomically.

**✓** Route decisions and outcomes are measured by slice.

## Put the idea to work

1. Design a route contract with confidence, reason codes, fallback, and version.
2. Model a handoff that transfers a task without broadening authority.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| How does routing differ from a handoff? | Routing selects an eligible implementation; handoff transfers responsibility and therefore requires ownership, state, authority, and cancellation semantics. |
| Should the model see every route? | No. Give it a minimal eligible set derived from purpose, authority, health, region, risk, and release policy. |
| What should happen below a confidence threshold? | Use a deterministic default, request clarification, or route to a human queue; do not select a privileged specialist by guesswork. |
| When is a handoff the wrong choice? | When the parent still owns the outcome (agent-as-tool) or the work needs independent recovery without conversational transfer (durable child task, Chapter 18). |
| When is a static router better? | When classes are stable, risk is high, compliance requires predictability, or a simple rule already separates the work. |

## Where this leads next

Routing selects among known capabilities; Chapter 12 addresses tasks whose decomposition must itself be proposed and validated.

# 12 — Turn Proposed Plans into Safe, Executable Work

> **Evidence context:** Published engineering guidance distinguishes predefined workflows from model-directed agents and recommends adding complexity only when simpler compositions are insufficient. **[R27]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** A mortgage application with a missing second pay statement, an asset discrepancy, and a property check requires adaptive sequencing. Harborlight lets a planner propose a graph but compiles that graph before any node becomes schedulable. |

|  |
| --- |
| **THE DESIGN CHOICE** Use a typed Plan IR and deterministic compiler; freeze committed past work across plan revisions. |

## Why a plausible plan still needs to be compiled

Planning earns its complexity only when the work cannot be known in advance.
When a stable route exists, route deterministically (Chapter 11); invoke the
planner only at entry, at material uncertainty, or after a failure invalidates
the current plan. Even then, a model-proposed plan is not permission to run
arbitrary steps. This chapter treats the plan as an intermediate
representation: validate it, check it stays within the run's authority, compile
it into executable nodes, and freeze the work that has already committed. The
distinction matters whenever the plan changes halfway through a long-running
case.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Plan Service and durable workflow | planner proposal to deterministic compiler | plan node · workload queue | one node and one plan revision | CandidatePlan · CompiledPlan · PlanRevision |

## Treat planning like compilation—not authorization

The compiler analogy is useful because a plan has the same gap as source code: it may express a sensible intention and still be unsafe or impossible to execute. Models confuse a coherent narrative with a feasible, authorized execution graph. The plan compiler resolves capabilities, checks dependencies, rejects cycles, attaches budgets and deadlines, and verifies that each step stays inside the run's capability envelope (Chapter 21). A compiled plan proves its steps fit inside the envelope; it does not authorize them. Each dispatch still receives an exact authorization decision at the Tool Gateway (Chapter 2) against the current resource version, because a case version, policy decision, or approval can become stale before a later step begins.

[[DIAGRAM:pattern-planning|Figure 12-1 — A candidate plan becomes typed IR and is validated before any step runs]]

The planner describes desired work; the compiler determines whether that work is legal and executable. Plan IR nodes name capability requirements rather than concrete credentials. Compilation binds each capability requirement to an eligible Skill and tool release (Chapter 8), calculates critical path and maximum cost, and emits an immutable plan revision signed by the compiler so the scheduler can verify that what runs is what was validated.

Resource feasibility matters. A valid graph can still miss the deadline if it requires too many browser sessions, serialized vendor calls, or human approvals. The compiler checks workload queues, concurrency classes, rate limits, regional placement, and time windows before committing a plan. Scheduling remains a workflow responsibility.

The alternatives run from a fixed workflow, rules engine, and router through plan-and-execute, ReAct, graph search, and planner/executor/critic to code generation. Fixed workflows maximize predictability; dynamic planning increases coverage at a higher evaluation, security, and cost burden.

## What should be agentic?

The same split decides every pattern in this Part; in a plan it is encoded as the node `kind`.

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

## Plan IR

JSON · implementation excerpt

```json
{
  "plan_id": "plan_...",
  "revision": 3,
  "goal": "...",
  "capability_envelope_id": "cap_...",
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

The shared contract models `CandidatePlan` and `PlanNode` (`examples/contracts.py`) define these fields; the compiler at the end of this chapter checks them.

Each node kind is executed by a mechanism defined elsewhere: `llm_activity` is a bounded model step (Chapter 10) whose output is accepted as in Chapter 13; `tool_activity` crosses the six gates (Chapter 2) with effect semantics from Chapter 22; `gate` is a human approval (Chapter 14); `wait` is a durable timer or signal (Chapter 15); `child_task` and `join` are durable delegation and fan-in (Chapter 18).

`risk_class` uses the book's five effect classes: R0 pure transform, R1 low-sensitivity read, R2 sensitive read or reversible draft, R3 external communication or material reversible change, R4 irreversible, privileged, or financial action, where the agent may only propose (full controls in Chapter 22 § Risk classes).

### Compile-time checks

* Every node has a pinned implementation or an allowlisted runtime selector, typed inputs/outputs, timeout, retry owner, budget, risk class, acceptance rule, and terminal failure path. A pack Skill the run may not resolve is refused here, naming the rule, never mid-run (Chapter 9).
* Every capability lies inside the run's capability envelope. A dynamic node may choose only among an allowlisted capability set; it cannot call arbitrary network endpoints.
* Data-flow classification can stay equal or become more restrictive. A node cannot send restricted data to a capability whose manifest/region/purpose is incompatible.
* Mutating nodes require idempotency/effect semantics (Chapter 22) and any policy-required preview, approval (Chapter 14), or compensation. An R4 (irreversible or privileged) commit remains a deterministic domain operation.
* Loops require a deterministic guard plus maximum iterations, wall time, cost, and a no-progress detector using the no-progress signatures of Chapter 10; unbounded loops and unhandled terminal paths are rejected. Delegation depth and parallel fan-out are statically bounded; see AP-11 for why per-child limits do not compose.
* The compiler estimates critical path, maximum fan-out, worst-case calls/cost, and required quota. Admission (Chapter 28) may reject, defer, or require approval before commit.

## Revise without rewriting history

New evidence can invalidate future work. Replanning starts from an explicit set of immutable facts: accepted artifacts, committed effects, approval decisions, and current resource versions. The new revision includes a diff, rationale, superseded nodes, reused artifacts, changed budget, and compiler evidence. It cannot rewrite history.

1. Persist the triggering observation/failure and current state version.
2. Freeze completed effects and accepted artifacts; mark nodes whose assumptions changed as invalidated.
3. Ask the planner only for the affected horizon, not the entire run.
4. Compile and diff the candidate against the committed revision.
5. Reuse nodes only when implementation, inputs, policy, data revisions, and acceptance remain compatible.
6. Obtain a new approval (Chapter 14) if risk, purpose, destination, spend, or authority expands.
7. Atomically commit the revision and reservations, then schedule newly ready nodes.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Planner Activity | Produce a typed candidate plan from goal, constraints, eligible capabilities, and current evidence |
| Plan Store | Persist immutable revisions and current committed pointer |
| Capability Binder | Resolve abstract capabilities to pinned agents/tools/endpoints |
| Plan Compiler | Validate graph, types, authority, budgets, effects, failure paths, and determinism boundaries |
| Scheduler | Materialize ready nodes into workflow activities/child tasks under concurrency and quota |
| Replan Controller | Decide when replanning is allowed and define the unchanged/reusable subgraph |
| Acceptance Engine | Run deterministic checks and policy-approved model graders before satisfying nodes/goals (Chapter 13) |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/runs/{run\_id}/plans:propose | Invoke the planner with state version, reason, planning horizon, and eligible capability snapshot; result is uncommitted |
| POST /v1/plans/{plan\_id}/revisions/{revision}:validate | Run schema, DAG, authority, budget, compatibility, data-flow, risk, and terminal-path validation |
| POST /v1/plans/{plan\_id}/revisions/{revision}:commit | Atomically select a validated revision using expected current revision/state version and reserve budgets |
| POST /v1/plans/{plan\_id}:revise | Create a diff-based revision from changed evidence/failure; cannot widen authority without a new grant |
| GET /v1/plans/{plan\_id}/revisions/{revision} | Return immutable plan, validation report, bindings, estimated cost/latency, and provenance |
| GET /v1/runs/{run\_id}/ready-nodes | Operator/debug view of satisfied dependencies, blockers, reservations, and dispatch state |
| POST /v1/nodes/{node\_execution\_id}:accept | Apply acceptance checks to outputs and transition only if expected node version still matches |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| Plan | plan ID, run, goal hash, current committed revision, capability envelope, lifecycle state |
| PlanRevision | plan/revision, parent revision, trigger/rationale, planner/model/prompt/context versions, graph hash, created by/time; immutable |
| PlanNode | stable logical node ID, revision, kind, capability requirement/binding, input selectors, output schema, risk, retry/timeout, acceptance, failure strategy |
| PlanEdge | revision, from/to node, condition, artifact/data mapping; compiler verifies type compatibility and acyclicity unless loop is explicitly bounded |
| CapabilityBinding | abstract requirement, chosen agent/tool version, eligibility decision, health snapshot, regional endpoint, expiry |
| BudgetReservation | See Chapter 28 § Records worth preserving; the compiler requests one per plan node |
| ValidationFinding | rule ID/severity, object path, message, evidence, required remediation; errors block commit |
| NodeExecution | logical node, plan revision, workflow/activity/task ID, attempt, state, inputs/outputs, accepted result hash, timing/cost |

### Scalability and performance

* Planner workers are stateless and queue driven. Plan storage is partitioned by tenant and run; immutable revisions, schemas, and large graph blobs are stored or cached by digest, while policy and health are rechecked at commit and dispatch.
* Validate incrementally: a plan revision carries changed nodes/edges, allowing graph, type, cost, and policy analysis to recompute only impacted regions.
* The scheduler scans no global table. Workflow events enqueue newly ready node IDs; conditional updates ensure each logical node is dispatched once per accepted attempt.
* Apply per-run ready-node limits and weighted fair scheduling across tenants. Planning cannot reserve unbounded future capacity; reservations expire and are reclaimed.

## Planning at a glance

| **Use when** | **Do not use when** |
| --- | --- |
| Use for heterogeneous, dependency-rich tasks where semantic decomposition provides measurable value. | Avoid for known processes, short tasks, or high-risk paths that should be encoded as deterministic workflows. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Flexible decomposition | More validation, recovery, and evaluation complexity. |
| Parallel execution | Lower latency; higher resource use and conflict risk. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Invalid graph | Cycle, reference, terminal, and reachability checks. |
| Invented authority | Capability and grant subset checks. |
| Plan churn | Revision, no-progress, and cost limits; freeze committed facts. |

### What you need to see in production

* plan digest and revision
* compiler decisions
* ready set
* node states
* critical path
* replan diff and reason

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Durable scheduling | Durable-execution systems preserve workflow progress, timers, and replay across failures, which is why compiled plans are scheduled through a workflow rather than an in-process loop. | R02 |

The discussion above draws on R27; R02. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The compiler below applies the checks above to a candidate plan: capability allowlist, risk ceiling, unknown dependencies, cost, cycles, and a digest of what was validated.

[[EXAMPLE:plan-compilation#core]]

## If this fails in production

1. Re-run the plan compiler against the exact release and policy versions.
2. Find the first node whose capability, budget, or schema became invalid.
3. Compare plan revisions and ensure committed facts did not change.

## What to verify before production

**✓** Model planning is used only for genuine semantic uncertainty.

**✓** Plans are typed, immutable, versioned graphs with explicit limits and acceptance.

**✓** Graph, authority, security, resource, schema, and effect constraints compile before commit.

**✓** Completed effects and accepted artifacts are frozen across revisions.

**✓** Revisions, loops, fan-out, depth, time, cost, and no-progress behavior are bounded.

## Put the idea to work

1. Extend the Plan IR with deadlines and fallback paths.
2. Construct a plan that passes schema validation but must fail authority validation.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| When should you use a deterministic workflow instead of model planning? | When paths, invariants, and recovery semantics are known; use planning only for real semantic uncertainty or environmental adaptation. |
| Why create a typed Plan IR? | It makes nodes, dependencies, capabilities, schemas, risk, budgets, and failure behavior inspectable, compilable, versionable, and schedulable. |
| What must a plan compiler validate? | Graph integrity, schema compatibility, authority subset, data and region policy, effect and approval semantics, capacity, cost, deadlines, and terminal paths. |
| How should replanning handle completed work? | Treat committed effects and accepted artifacts as immutable facts; revise only the affected future horizon and append a new version with rationale and diff. |
| How do you prevent plausible but endless planning? | External revision, loop, step, cost, time, delegation, and no-progress limits plus deterministic acceptance and terminal transitions. |

## Where this leads next

Planning creates an executable structure, and every plan node ends in acceptance checks; Chapter 13 defines what may decide them—independent evaluation and bounded revision without self-certification.

# 13 — Use Critique to Improve—Never to Self-Approve

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** The first draft recommendation for the mortgage case is coherent but omits a contradictory address and overstates confidence. Harborlight adds bounded reflection for revision and an independently defined evaluator for acceptance. |

|  |
| --- |
| **THE DESIGN CHOICE** Use reflection for targeted revision and independent, calibrated acceptance for protected outcomes. |

Critique can make a draft better, but a generator should not be allowed to
grade and approve its own work. This chapter gives reflection a bounded job—find a targeted defect and propose a revision—while an independently defined
evaluator and acceptance engine decide whether the result is good enough. That
separation controls both false confidence and runaway evaluation cost.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Acceptance Engine | generator/evaluator and evaluator/commit | candidate · scorer pool · slice | one revision cycle | EvaluationResult · Rubric · AcceptanceDecision |

## Give evaluation its own independent path

Independent evaluation does not mean asking the same model to reread its answer and declare it better. Generator and evaluator can share the same blind spot, especially when they use the same model family, context, or assumptions.

## Reflection revises; an acceptance engine decides

[[DIAGRAM:pattern-reflection|Figure 13-1 — A bounded revise loop whose verdict is advisory; acceptance happens outside it]]

Reflection asks, “What is missing or inconsistent?” Evaluation asks, “Does this candidate meet an acceptance rubric?” In the mortgage case, the contradictory address is caught by an executable check against the application projection; whether the recommendation overstates confidence is the kind of qualitative criterion a calibrated judge may assess. Combining reflection and evaluation can improve complex artifacts, but only if the roles are explicit and bounded. The platform runs executable checks before any model judge: schema, evidence presence, policy, effect state, resource version, arithmetic, and deterministic domain rules.

Qualitative criteria—clarity, completeness, grounded synthesis, or policy-explanation quality—may use calibrated judges. Judge prompt, model route, examples, sampling parameters, and rubric are versioned. A judge used at runtime must already be calibrated: Chapter 25 § Layer tests from contracts to outcomes defines how judges are measured against human labels and gated for release. Inside a run, a judge score is one input to the acceptance decision; it is never permission to access data or commit a transaction (see AP-10).

### The acceptance decision

The acceptance engine is the only component that may mark a candidate, a plan node (Chapter 12), or a ReAct answer (Chapter 10) as accepted. It takes the candidate, the authoritative state the candidate claims to satisfy, and a versioned set of criteria. It evaluates executable invariants first and calibrated judges only for criteria that cannot be computed. It returns an `AcceptanceDecision`: accepted, rejected with typed defects, or escalated. For each criterion the decision records the evaluator type—deterministic, or judge with its version—and evidence references. Chapter 2 § Deterministic acceptance lists what Harborlight checks; Chapter 15 § Terminal correctness maps the decision to the run's terminal state.

### Bounded optimization loop

Each revision targets structured feedback and carries a diff. In order:

1. Generate candidate v1.
2. Run deterministic checks first.
3. Run calibrated qualitative evaluation if needed.
4. Apply actionable feedback to one revision.
5. Let the acceptance engine accept, reject with defects, or escalate at a bounded threshold.

The loop stops on pass, maximum revisions, maximum spend, deadline, or no-progress (a revision that changes wording but not the failing invariant, the same signature test as Chapter 10). If the evaluator and generator repeatedly disagree, the workflow escalates with both artifacts to a human intervention queue (Chapter 14) rather than silently choosing the more persuasive prose. The loop is runtime adaptation inside a fixed envelope: it may revise the candidate, never the rubric, judge, or thresholds (Chapter 25 § Separate runtime adaptation from offline improvement).

## Reflection and evaluator–optimizer at a glance

| **Pattern** | **Use when** | **Do not use when** |
| --- | --- | --- |
| Reflection | Measured offline results show critique improves a specific quality dimension. | Correctness is executable, the first pass already meets the bar, or added latency has no measured benefit. |
| Evaluator–optimizer | Documents, plans, code, or analyses where iterative quality gain is measurable and latency permits. | Do not use a model judge as sole authority for permissions, transaction success, security, or computable correctness. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Better completeness | Additional model calls, correlated errors, and longer latency. |
| Structured critique | More debuggable; requires defect taxonomy and evaluation. |
| Explicit rubric | Improves governance; can overfit to benchmark or judge preferences. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Self-confirmation | Different rubric, evidence, or evaluator and deterministic checks. |
| Evidence invention | Require evidence references and reject unsupported additions. |
| Stylistic churn or endless revision | Diff limits, maximum revisions, cost, time, and no-progress stop. |
| Judge variance | Repeated runs and thresholds; calibration per Chapter 25. |
| Reward hacking | Holdout tests and diverse scorers; Chapter 25. |

### What you need to see in production

* candidate version and diff size
* defect taxonomy
* evidence refs
* scorer versions
* per-criterion scores and judge rationale
* quality delta and variance
* acceptance decision and stop reason

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Evaluation tooling | Current evaluation platforms support datasets, code-based and LLM judges, and human feedback; using judges only as evidence for an independent acceptance decision is this book's recommendation. | R20 |

The discussion above draws on R20. Appendix K lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The judge supplies evidence; only the acceptance engine decides.

[[EXAMPLE:evaluator-optimizer#core]]

## If this fails in production

1. Compare generator and evaluator evidence to detect shared blind spots.
2. Inspect score variance across repeated judge runs and slices.
3. Detect revisions that change wording but not the failing invariant.

If the model's own "done" or a judge score is the acceptance decision, see AP-07 and AP-10 in Chapter 17.

## What to verify before production

**✓** Generator and evaluator roles, prompts, models, and evidence are distinguishable.

**✓** Computable invariants use code, not a model judge.

**✓** Revision count, spend, time, and no-progress are bounded.

**✓** Judge calibration and inter-rater agreement are measured (Chapter 25).

**✓** Failed candidates and feedback enter a regression corpus (Chapter 25).

## Put the idea to work

1. Add a deadline stop to the evaluator–optimizer example and test that it escalates with both candidate versions.
2. Create a case where reflection worsens a correct answer and define the stop rule.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| How is reflection different from evaluation? | Reflection proposes improvements; evaluation applies an acceptance rubric and should be independently calibrated or deterministic where possible. |
| Why is self-evaluation dangerous? | The same model can repeat the same blind spots and produce confident rationales without independent evidence. |
| How do you bound evaluator–optimizer? | Limit revisions, cost, time, and accepted feedback types; stop on pass, no-progress, or escalation. |
| What should always be checked deterministically? | Schema, policy, authority, evidence presence, effect state, resource versions, arithmetic, and other computable invariants. |
| When should you not add reflection? | When the first result already meets an executable specification, latency is critical, or critique adds no measured improvement. |

## Where this leads next

Automated evaluation can improve a candidate but cannot settle every decision. When the evaluator and generator disagree, or the action is protected, Chapter 14 puts a person where their judgment matters.

# 14 — Put People Where Their Judgment Matters

> **Evidence context:** Human-review interfaces should be tested against WCAG 2.2 accessibility criteria; accessibility conformance does not by itself eliminate automation bias or establish decision fairness. **[R41]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** A protected mortgage-case operation requires human action authorization. The reviewer must see the exact operation, destination, evidence, expected resource version, and risk—not a vague request to “approve the mortgage.” |

|  |
| --- |
| **THE DESIGN CHOICE** Persist proposal-bound approvals as durable workflow events and reauthorize immediately before commit. |

## Why human review must change system state

Human review is most useful when it resolves a decision the system cannot or
should not make alone. It becomes theater when the reviewer sees a summary
that can change after approval, or when a click is detached from the effect it
authorizes. This chapter binds authorization to an immutable proposal,
evidence, identity, expiry, and a durable state transition.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Workflow plus Human Action Authorization Service | machine proposal to human authority | authorization queue · risk class · tenant | one immutable proposal | HumanActionAuthorizationRequest · HumanActionAuthorizationDecision · EffectReceipt |

## Separate authorization from intervention

Authorization and intervention place different demands on a reviewer. Authorization asks whether one exact effect may proceed; the interface should show the immutable proposal, evidence, consequences, and expiry. Intervention asks a person to supply missing judgment or correct a run; the interface must expose uncertainty and viable alternatives. Combining them into one generic approval queue encourages rubber-stamping and makes the audit record difficult to interpret.

[[DIAGRAM:pattern-hitl|Figure 14-1 — Approval and intervention: different triggers, different authority, different evidence]]

**Human action authorization** authorizes one proposed effect. **Intervention** asks a person to diagnose, correct, supply information, or choose among unresolved alternatives. Northstar uses separate queues, roles, forms, SLOs, and terminal semantics.

The Human Action Authorization Service stores a canonical proposal, human-readable preview, destination, evidence and policy references, risk, expected resource version, expiry, and proposal hash. Human action authorization becomes invalid when any protected field changes. A commit path rechecks approver authority, separation of duties, current policy, authorization freshness, and resource version.

Human capacity is finite. Queue age, dwell, abandonment, reassignment, disagreement, and after-hours coverage are production metrics. A system that requires routine approval for low-risk deterministic work may be less safe because reviewers become fatigued.

## Design human review as part of the system

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Humans must understand, approve, correct, or stop consequential work without becoming a rubber stamp or breaking run integrity. |
| Why it is difficult | Too many approvals cause fatigue; too little context prevents informed decisions; approvals can go stale as data or plans change; edits must be attributable and replayable. |
| Design alternatives | Confirm every tool call; risk-based approvals; maker-checker; sampled review; exception-only review; fully manual commit. |
| Recommended architecture | Use policy-triggered gates based on risk, novelty, confidence, value, data sensitivity, reversibility, and destination. Present a concise preview, evidence, alternatives, changed fields, policy rationale, and blast radius. A HumanActionAuthorizationDecision authorizes a specific immutable proposal for a limited time. |
| Trade-offs | Human review adds latency and staffing cost but provides judgment and accountability where automation evidence is insufficient. Poor UX converts the control into theater. |
| Failure scenarios | Approval applies to a changed plan; approver lacks authority; agent hides uncertainty; request times out; two operators issue conflicting overrides; “approve all” becomes normal. |
| Enterprise example | A mortgage agent drafts a request to obtain missing employment evidence. The underwriter sees the policy basis, case evidence, requested document, downstream effect, and alternatives; any case, document, or destination change invalidates the authorization. |

### Approval contract

HumanActionAuthorizationRequest contains: proposal/artifact hash, exact action and resource, before/after diff, subject and actor, evidence links, uncertainty, policy rule, risk class, estimated impact/cost, reversible flag, expiry, separation-of-duties requirement, and allowed responses (authorize, reject, edit-and-resubmit, request-evidence, cancel-run).

### Operator console requirements

* Live run graph with current owner, state, budgets, queues, waits, child tasks, and last committed effect.
* Redacted but causally complete trace; model/tool inputs available only to authorized incident roles.
* Pause, cancel, retry safe activity, skip with justification, patch plan, reassign approval, increase budget, trigger compensation, and fork a sandbox replay.
* Conflict detection and optimistic versions for operator edits.
* Immutable operator identity, reason, timestamp, before/after state, and linked ticket on every override.
* SLA timers and escalation paths; a timed-out approval follows explicit policy, never implicit approval.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Approval Policy Router | Convert policy obligations, risk, value, novelty, and confidence into approval requirements |
| Human Action Authorization Service | Persist immutable proposal snapshots and authoritative decision state |
| Assignment/Queue Service | Resolve eligible approvers, maker-checker rules, claim/reassign, priority, and SLA |
| Evidence Renderer | Produce role-redacted diff, sources, rationale, alternatives, uncertainty, and blast radius |
| Notification Service | Deliver idempotent channel notifications and deep links; it never owns the decision |
| Operator Control Service | Perform authorized pause, cancel, retry, plan patch, budget, and compensation commands |
| Override Journal | Append operator actions and linked incident/change records to immutable evidence |

### The contracts between components

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/approvals | Idempotently create approval from proposal hash, exact action/resource, evidence snapshot, required roles/count, expiry, and allowed responses |
| GET /v1/approvals/{approval\_id} | Return current state, immutable proposal, redacted evidence view, assignments, SLA, and decision history |
| POST /v1/approvals/{approval\_id}:claim | Claim work using expected version; verifies current eligibility and separation of duties |
| POST /v1/approvals/{approval\_id}:decide | Approve or reject using proposal hash, expected version, reason, and strong approver authentication |
| POST /v1/approvals/{approval\_id}:requestEvidence | Suspend decision and signal the workflow with a typed evidence request |
| POST /v1/approvals/{approval\_id}:supersede | Close stale approval and create a new one when proposal, target state, policy, or material evidence changes |
| GET /v1/approval-queues/{queue\_id}/items | Cursor query by skill/role, priority, age, risk, tenant, value, and region; no unauthorized evidence leakage |
| POST /v1/runs/{run\_id}:operatorAction | Pause, cancel, safe-retry, patch plan, extend budget, trigger reconciliation/compensation, or fork replay with reason and expected state |

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| HumanActionAuthorizationRequest | authorization ID, tenant/run/node/effect, proposal hash, action/resource, before/after refs, risk/value, policy decision, required approver predicate/count, expiry, state/version |
| ApprovalEvidenceSnapshot | approval, immutable source/artifact refs and hashes, policy/rationale, uncertainty, alternatives, impact, redaction profile, created version |
| ApprovalAssignment | approval, queue, eligible-role predicate, assignee/claim lease, SLA, escalation level, state |
| HumanActionAuthorizationDecision | authorization, proposal hash, approver identity/role/assurance, decision, reason, signature/attestation, time; append-only |
| OperatorAction | action ID, run, command, actor/role, target/version, before/after refs, reason, linked ticket, result/effect; append-only |
| EscalationPolicy | queue/risk/value, warning/expiry timers, fallback roles, business calendar, timeout disposition; implicit approval is forbidden |
| NotificationDelivery | approval/action, channel, destination handle, idempotency key, attempts, delivered/acknowledged, error; contains no unredacted evidence |

A decision is valid only when the presented proposal hash equals the current proposal, the approver is authorized at decision time, required counts/separation rules are satisfied, and the approval has not expired or been superseded.

### Workflow integration

1. The workflow persists the proposed effect and evidence snapshot, then creates the approval.
2. The Human Action Authorization Service registers durable SLA/expiry timers and returns a wait correlation ID.
3. Assignment and notifications may retry independently; the workflow remains suspended without a worker.
4. A decision transaction records the immutable decision and emits an outbox event.
5. The workflow receives the event, revalidates policy/current resource version, and commits only the proposal whose hash was approved.
6. If the resource, amount, recipient, scope, or policy changed materially, the workflow supersedes the approval and generates a fresh preview.

### What changes as usage grows

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

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Approval integrity | Approve the exact canonical proposal, not a natural-language summary. Revalidate policy, authority, proposal hash, expiry, destination, and resource version immediately before commit. Never transport serialized run state inside exception text or ordinary logs. | R15 |

The discussion above draws on R15; R41. Appendix K lists the complete sources and records their authority, version, and scope.

## How Human-in-the-Loop works in practice

|  |
| --- |
| **THE ENGINEERING PROBLEM** A person must authorize, correct, or resolve work whose risk or ambiguity exceeds autonomous authority. |

### How the pattern works

The workflow persists a proposal-bound HumanActionAuthorizationRequest or InterventionTask, pauses, receives an authenticated decision, revalidates current authority and resource state, then commits or replans.

1. Create an immutable proposal and preview.
2. Identify allowed approver roles and separation-of-duty rules.
3. Persist the wait and notify through a durable channel.
4. Authenticate and record decision, reason, and timestamp.
5. Reauthorize and verify proposal hash immediately before commit.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for high-risk, irreversible, regulated, ambiguous, or policy-exception decisions. | Do not add a cosmetic click for already-automated low-risk steps or ask a human to review unreadable raw model traces. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Risk control | Adds dwell time, queues, fatigue, and staffing requirements. |
| Human judgment | Handles ambiguity; can be inconsistent and needs calibration. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Approval drift | Hash binding, expiry, expected version, and reapproval. |
| Wrong approver | RBAC/ABAC and separation of duties. |
| Queue abandonment | SLA, escalation, reassignment, cancellation, and safe timeout. |

### What you need to see in production

* proposal hash
* risk and policy basis
* approver authority
* queue and dwell time
* decision and reason
* commit receipt

## A sensible place to start


[[EXAMPLE:approval-gate]]

### Proposal-bound approval contract

🐍 · implementation excerpt

```python
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pydantic import BaseModel


class HumanActionAuthorizationRequest(BaseModel):
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

## If this fails in production

1. Recompute the proposal hash and expected resource version.
2. Verify approver authority, expiry, and separation-of-duty policy.
3. Trace the approval event through commit and effect receipt.

## What to verify before production

**✓** Authorization and intervention use separate queues, roles, forms, and terminal semantics.

**✓** Every approval request has an expiry and an explicit timeout disposition; a timeout never becomes implicit approval.

**✓** Approval binds to an immutable proposal hash and current authority and resource state.

**✓** Reconciliation, compensation, pause, cancel, and intervention are governed commands.

## Put the idea to work

1. Design a human action authorization object for a protected mortgage-case operation.
2. Define how edits, policy changes, and expired grants invalidate approval.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why separate authorization from intervention? | Authorization asks whether one exact effect may proceed; intervention supplies missing judgment or corrects a run. Separate queues, roles, forms, and terminal semantics keep the audit record interpretable. |
| What happens when an approval request times out? | It follows an explicit escalation policy and timeout disposition; a timeout never becomes implicit approval. |
| How should approval be bound to an action? | Persist the exact canonical proposal, preview, destination, evidence, risk, and hash; authorize the approver; reject expiry, supersession, hash mismatch, or stale resource state. |

## Where this leads next

Human control introduces waits and resumptions; Chapter 15 makes those waits durable and gives long-running work explicit state and recovery.

# 15 — Keep Long-Running Work Alive Through Failure

> **Evidence context:** Durable-execution systems preserve workflow progress across failures and long waits; concrete integrations and replay semantics vary by backend. **[R02][R36][R38]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** The applicant waits nine days to upload an employment document. During the wait, workers deploy twice, policy changes, the loan officer loses a role, and one earlier request times out. The run must resume safely rather than restart from a prompt transcript. |

|  |
| --- |
| **THE DESIGN CHOICE** Represent long-running work as replay-safe workflow history plus bounded activities, durable waits, and reconciliation. |

## Why long-running work needs durable state

An agent that must wait for a document, a person, or a downstream system is no
longer a request/response handler. Its state has to outlive processes,
deployments, retries, and partial effects. This chapter shows how to model that
work as durable execution, and why recovery is part of the design rather than
an operations add-on.

## Model long-running work explicitly

Durability is not achieved by serializing an in-memory agent object. The platform needs a stable account of intent, state transitions, pending obligations, timers, child tasks, approvals, and external effects. Workers can then disappear and return without becoming the owners of truth. This matters as soon as a run lasts longer than a process lifetime—or waits on a person whose response arrives after several deployments and policy changes.


| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Durable workflow engine | workflow activity to external I/O | history shard · activity queue · timer | one workflow execution | WorkflowEvent · Checkpoint · WaitRegistration |

## Durable state is more than chat history

[[DIAGRAM:pattern-durable|Figure 15-1 — The run outlives the process: checkpoint, die, replay, adopt]]

Chat history cannot reliably encode timers, retries, child ownership, approval waits, cancellation intent, resource versions, effect receipts, or deployment compatibility. Northstar uses event history to rebuild a canonical RunState; model and tool calls are bounded activities whose inputs and outputs are recorded by reference.

The workflow reducer must be deterministic. It cannot read the clock, call a model, query a database, generate randomness, or perform network I/O during replay. Those operations become activities, signals, or recorded events. This separation makes a crashed worker replaceable.

### Terminal correctness

A run reaches Succeeded only through executable acceptance. A canceled run with a possibly committed write does not simply disappear; it moves through reconciliation and possibly compensation. If correctness cannot be established automatically, InterventionRequired is a valid terminal operational state.

## The lifecycle of a durable run

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

## Let events resume work without losing control

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Runs lasting minutes to months must survive crashes, deployments, expired credentials, human waits, rate limits, and external callbacks without restarting from scratch. |
| Why it is difficult | Process memory is ephemeral; replay can repeat nondeterministic calls and side effects; external systems deliver duplicates or callbacks out of order; code and schemas evolve while runs are active. |
| Design alternatives | Background job + database; queue consumers; graph checkpointing; cloud state machines; durable execution engines such as Temporal/DBOS/Restate/Durable Functions; event-sourced custom runtime. |
| Recommended architecture | Use a durable workflow engine as the authoritative run kernel. Put model and tool calls in activities/tasks, record their results, persist checkpoints after meaningful steps, and use durable timers/signals for waits. Feed external events through an event bus and correlate them to existing runs. |
| Trade-offs | Durable engines impose determinism/versioning constraints and operational cost, but remove far more bespoke recovery code. Graph checkpointers are useful for agent state but may not replace a mature cross-service workflow engine. |
| Failure scenarios | Replay resends an email; worker dies after effect but before acknowledgment; old run cannot replay after code change; callback is spoofed; event arrives before subscription; retry storm exhausts provider quota. |
| Enterprise example | A mortgage-evidence agent waits days for employment documents and human action authorization. The workflow is unloaded while idle, resumes on correlated events, refreshes authorization, and continues from the last committed effect. |

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

## A workable implementation

### Who should own each decision

The Run API persists intent and returns quickly; the durable workflow owns lifecycle; activity workers perform model/tool I/O; Event Ingress authenticates external facts; the Correlator maps those facts to waiting runs; Timer/Signal services wake workflows; and a Version Router keeps compatible workflow builds available for in-flight histories.

### The contracts between components

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

### Records worth preserving

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

* Record model and external tool calls as activities whose results are persisted before workflow continuation. Replay returns the recorded result; it does not call the model or tool again.
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

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Recovery objective | Durability is incomplete without measured RTO/RPO, compatible worker availability, backup restoration, region failover, and explicit treatment of pending approvals and unknown effects during disaster recovery. | R02; R04 |

The discussion above draws on R02; R04. Appendix K lists the complete sources and records their authority, version, and scope.

|  |
| --- |
| **COMMON PITFALL**  Storing conversation history and calling it durable state. Transcripts record what was said, not what was decided or committed. Persist decisions, approvals, and effect receipts as first-class records; a run must be resumable from them even if every message is discarded. |

## How Long-Running Agents work in practice

|  |
| --- |
| **THE ENGINEERING PROBLEM** Business work lasts longer than a process lifetime and must survive waits, worker loss, retries, deployments, and partial external failures. |

### How the pattern works

A durable workflow records deterministic decisions and schedules bounded activities. Timers, signals, children, approvals, effects, and release pins are durable history.

1. Admit and pin the run manifest.
2. Record each state transition before scheduling work.
3. Execute models and tools as bounded idempotent activities.
4. Persist waits and resume through authenticated signals or timers.
5. Reconcile effects and verify terminal criteria before closing.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for work with waits, multiple systems, protected effects, independent failures, or duration beyond one request. | Avoid a workflow engine for a single short idempotent read with no recovery or coordination requirement. |

### Where it helps—and what it costs

| **Choice** | **Consequence** |
| --- | --- |
| Failure recovery | Requires deterministic workflow discipline and history compatibility. |
| Long waits | Preserves state; creates lifecycle, retention, and migration obligations. |

### Where it can fail—and how to contain it

| **Failure** | **Control** |
| --- | --- |
| Nondeterministic replay | Move I/O, clocks, randomness, and model calls to activities. |
| Stuck wait | Durable deadline, accepted signal sources, escalation, and visibility. |
| Unknown mutation | Freeze dependents and reconcile before retry or close. |

### What you need to see in production

* workflow build
* history event
* activity attempt
* timer and wait state
* signal source
* effect reconciliation
* terminal reason

## A sensible place to start


### Replay-safe workflow reducer

[[EXAMPLE:durable-state#core]]

## If this fails in production

1. Replay workflow history with the pinned build and locate nondeterminism.
2. Inspect pending timers, signals, activities, and child tasks.
3. Resolve unknown effects before replaying dependent commands.

## What to verify before production

**✓** Workflow decisions are replay-safe; I/O, clocks, randomness, models, and tools are recorded activities.

**✓** Waits, signals, timers, cancellation, and child lifecycles are durable protocol state.

**✓** Each failure class has one retry owner; unknown effects route to reconciliation.

**✓** Active histories stay pinned to compatible workflow builds and activity contracts.

**✓** Workflow tasks, activities, timers, waits, history writes, and reconciliation are capacity-planned separately.

## Put the idea to work

1. Model a ten-day wait with role revocation and policy change.
2. Design cancellation semantics for a run with a possibly committed external write.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| How is durable execution different from a background job? | Control decisions and waits are recorded as replayable history; workers can disappear without restarting the business process or losing timers and signals. |
| What belongs in workflow code versus an activity? | Deterministic coordination in workflow code; models, databases, APIs, tools, clocks, randomness, and other external interactions in bounded activities. |
| How do you represent a wait that may last weeks? | Persist a typed wait registration, accepted sources and correlation, deadline, authorization, and resume node; wake through an authenticated signal or durable timer. |
| What happens if cancellation arrives while a write may have committed? | Persist cancellation intent, stop new work, mark the effect unknown if needed, reconcile the source system, then compensate or require intervention before closing. |
| How do you deploy new workflow code safely? | Preserve compatible workers, use explicit version markers, test replay, migrate deterministically when supported, or start a new linked generation when semantics cannot be preserved. |

## Where this leads next

The core patterns are now defined; Chapter 16 compares them by the obligation each protects, the shortcut it replaces, and what it costs.

# 16 — Choose Patterns That Fit Real Enterprise Work

## How to choose a pattern for the problem you actually have

Pattern names are useful only when they help a team make a safer decision. In
real design reviews, the same words can describe very different obligations:
one workflow may need adaptive evidence gathering, while another needs a
durable process with explicit ownership and compensation. This chapter gives
you a practical way to choose among the patterns, what each one buys you, and
where its cost or failure boundary appears.

## How to use these patterns without turning them into recipes

The patterns are decision aids, not recipes. Start with the obligation the system cannot violate: perhaps an external write must be exactly-once from the business perspective, or a task must survive a ten-day wait. Then choose the smallest pattern that protects that obligation. Combining every pattern produces ceremony and cost; choosing by fashion leaves the real failure mode exposed. The trade-off in each pattern is therefore as important as the recommended design.

Every card uses one review sequence so teams can compare alternatives consistently.

[[DIAGRAM:pattern-decision-tree|Figure 16-1 — Pattern selection decision tree]]

## Reasoning

### P-01 — Bounded ReAct

**When it helps.** Adaptive evidence is needed. The tempting shortcut is “Unbounded think–act loop.” That fails because the model owns stopping, budget, and success.

**A better design.** A safer design looks like this: Bound ReAct with step/time/token/tool/evidence limits and deterministic acceptance. The runtime flow is: Run Service → reason → eligible tool → observation → stop/accept. Mortgage evidence review queries two approved sources, asks once for the missing employment document, then stops.

**What to watch.** Track steps, no-progress loops, repeat queries, budget exhaustion, evidence coverage. The cost is real: bounds can stop useful exploration; tune by risk.

## Orchestration

### P-02 — Deterministic spine with semantic nodes

**When it helps.** Known obligations include a few judgment points. The tempting shortcut is “A conversational agent owns the process.” That fails because retries, waits, joins, approval, and compensation become ambiguous.

**A better design.** A safer design looks like this: Durable workflow with bounded semantic nodes. The runtime flow is: Workflow state → semantic task → typed result → deterministic transition. Onboarding always validates, screens, approves, creates, and notifies.

**What to watch.** Track transcript-only state, orphan tasks, duplicate effects, recovery time. The cost is real: workflow modeling adds upfront cost.

## Context engineering

### P-03 — Typed ContextManifest

**When it helps.** The model needs authorized fresh evidence under budget. The tempting shortcut is “Dump top-k and chat history into the prompt.” That fails because selection, ACL, freshness, poisoning, and truncation are not reproducible.

**A better design.** A safer design looks like this: Manifest source, ACL, snapshot, provenance, rank, freshness, token allocation. The runtime flow is: Planner → retrieval → policy → ranking/dedup → manifest → model. Contract review receives clauses from authorized agreements and effective policy.

**What to watch.** Track ACL rejects, freshness, recall/precision, lost-position, unsupported claims. The cost is real: snapshotting adds storage and latency.

## Memory

### P-04 — Provenance-bound tiered memory

**When it helps.** Useful facts must persist safely. The tempting shortcut is “Write every interaction to one vector store.” That fails because errors, secrets, stale facts, and injected instructions persist.

**A better design.** A safer design looks like this: Separate working/episodic/semantic/profile memory with purpose, scope, TTL, provenance, verification, deletion. The runtime flow is: Candidate → gate → MemoryRecord → scoped retrieval → revalidation. Store a verified communication preference, not inferred sensitive identity.

**What to watch.** Track write acceptance, stale retrieval, corrections, cross-scope access, memory failures. The cost is real: strict eligibility reduces personalization.

## Tools

### P-05 — Proposal–authorize–commit tool façade

**When it helps.** An agent must cause a business effect. The tempting shortcut is “Direct broad CRUD call with ambient credentials.” That fails because language becomes authorization and retries duplicate work.

**A better design.** A safer design looks like this: Typed tool, least privilege, policy, proposal/grant, idempotency, reconciliation. The runtime flow is: Proposal → policy/approval → façade → effect → receipt → acceptance. A mortgage document-request proposal binds the case, document kind, policy, expiry, and case version.

**What to watch.** Track denials, invalid args, grant mismatch, duplicates, unknown effects. The cost is real: controls add latency; automate low-risk checks.

## Multi-agent collaboration

### P-06 — Typed task ownership and join

**When it helps.** Specialists collaborate under one outcome. The tempting shortcut is “Free-form agent chat owns work.” That fails because it produces duplicate owners, cycles, lost artifacts, and premature completion.

**A better design.** A safer design looks like this: TaskEnvelope, one owner, authority, deadline, artifacts, cancellation, deterministic join. The runtime flow is: Supervisor → task service → specialists → accepted artifacts → join. Finance, legal, and security deliver required due-diligence artifacts.

**What to watch.** Track orphans, owner conflicts, fan-out, join age, late effects. The cost is real: formal tasks reduce spontaneity.

## Security

### P-07 — Least-privilege capability envelope

**When it helps.** Agents need sensitive access. The tempting shortcut is “One reusable token follows the chain.” That fails because injection or compromise gains broad authority.

**A better design.** A safer design looks like this: Subject+workload identity and short-lived audience/purpose/resource/spend/time scope. The runtime flow is: Identity → policy → capability lease → gateway/tool enforcement. A loan officer may read an authorized mortgage case and propose a document request, but cannot authorize the operation or make the lending decision.

**What to watch.** Track scope/age, expansion, cross-tenant attempts, denials. The cost is real: fine-grained policy needs templates/simulation.

## Reliability

### P-08 — Effect ledger and reconciliation

**When it helps.** Timeout may follow a committed external effect. The tempting shortcut is “Timeout means failure and retry.” That fails because the same logical effect can execute twice.

**A better design.** A safer design looks like this: Prepared EffectRecord, stable key, unknown terminal, authoritative reconciliation. The runtime flow is: Prepare → dispatch → receipt/unknown → reconcile → accept. Mortgage document-request timeout is queried by idempotency key before retry.

**What to watch.** Track unknown rate/age, duplicate effects, reconcile latency. The cost is real: requires downstream receipts/query.

## Observability

### P-09 — Causal run graph

**When it helps.** Diagnosis spans model, context, policy, tools, humans, effects. The tempting shortcut is “Independent logs and transcripts.” That fails because first divergence and outcome/cost attribution are lost.

**A better design.** A safer design looks like this: Correlated graph linking request, release, context, decisions, effects, acceptance, outcome. The runtime flow is: Trace IDs + domain IDs → spans/events → evidence/evaluation join. Trace reveals stale retrieval before a correct but misinformed tool call.

**What to watch.** Track unlinked spans, missing versions, outcome join, diagnosis time. The cost is real: capture is costly/sensitive; sample and reference payloads.

## Governance

### P-10 — Risk-tiered evidence gates

**When it helps.** Behavior changes often but review is finite. The tempting shortcut is “Manual-review everything or auto-deploy from one score.” That fails because fatigue or self-certification hides risk.

**A better design.** A safer design looks like this: Classify risk and require proportional tests, reviewers, canary, rollback. The runtime flow is: ChangeBundle → risk → validation → approval → staged release. A typo fix auto-promotes; hiring memory/model changes require domain/privacy/risk approval.

**What to watch.** Track bypass, fatigue, exception age, regression escape. The cost is real: risk classification needs calibration.

## Operations

### P-11 — Durable runtime with backpressure

**When it helps.** Runs face bursts, waits, humans, unreliable dependencies. The tempting shortcut is “Synchronous workers retry locally.” That fails because state is lost and outages amplify queues/retries.

**A better design.** A safer design looks like this: Durable state, leases, timers, bounded retries, permits, quotas, circuits, degraded mode. The runtime flow is: Ingress → admission → durable queue/workflow → bounded workers → bulkheads. During registry degradation, protected writes pause and queues stay bounded.

**What to watch.** Track queue age, permits, retry amplification, saturation, recovery. The cost is real: durability adds operational complexity.

## System architecture

### P-12 — Portable contracts and adapters

**When it helps.** Multiple frameworks/providers must coexist. The tempting shortcut is “App code depends on provider-native objects.” That fails because migration rewrites apps and controls diverge.

**A better design.** A safer design looks like this: Platform-owned contracts and normalized events with conformance-tested adapters. The runtime flow is: Application contracts → adapters → shared services → providers/protocols. Framework migration preserves tools, policy, traces, evaluation, release.

**What to watch.** Track native leakage, conformance failures, migration effort. The cost is real: abstraction may lag novel features; allow negotiated extensions.

## Where this leads next

Pattern selection is easier when failure shapes are visible; Chapter 17 recasts recurring anti-patterns as measurable replacement decisions.

# 17 — Architecture Patterns That Fail in Production

## Why failure patterns are easier to recognize than design rules

Production failures rarely arrive wearing the name of an anti-pattern. They
look like duplicate writes, missing approvals, unexplained cost, or a run that
cannot be reconstructed. This chapter turns those symptoms into recognizable
system shapes, then connects each shape to the boundary that should replace it
so the diagnosis leads to a design correction rather than another patch.

## Start with the first visible symptom

In an incident, teams rarely begin with a clean architecture label. They see a duplicate email, a case that nobody owns, a confident answer with no evidence, or a run that cannot be resumed. Start with that symptom and trace backward to the missing ownership or state boundary. The anti-pattern name is useful only if it leads to a concrete replacement and a metric that shows whether the repair worked.

Anti-patterns are recurring system shapes, not isolated defects. Almost every card below is one mistake wearing different clothes: a probabilistic component was handed a job that belongs to deterministic infrastructure. Repair the failed responsibility boundary rather than the symptom, because fixing the symptom — a better prompt, one more retry, a stricter classifier — leaves the boundary intact and the failure returns under a new name.

[[DIAGRAM:anti-before-after|Figure 17-1 — Autonomous monolith versus governed agentic architecture]]

Cards are grouped by the boundary they violate rather than by the technology involved, so that two candidates competing for the same fix sit next to each other. Every card carries the same four parts, which makes them comparable without re-reading prose.

### Find the failure by its first symptom

| **ID** | **Anti-pattern** | **First symptom you will see** | **Boundary it violates** |
| --- | --- | --- | --- |
| AP-01 | Autonomous monolith | Work is lost on restart and repeated on retry | Reasoning versus execution |
| AP-11 | Unbounded loops and recursive delegation | Cost and step count have a long tail with no ceiling | Reasoning versus budget |
| AP-02 | Prompt as database | Behavior changes after a long conversation is summarized | Context versus state |
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
| AP-15 | Model or provider swap as configuration | Behavior shifts with no code change and no release record | Configuration versus behavior |
| AP-16 | In-place change and test after release | A failing run cannot be reproduced or rolled back exactly | Convenience versus immutability |

### How to read a card

**How this failure starts** states what the team was legitimately trying to achieve — no card here describes carelessness — then names the shape that gets built and the mechanism by which it fails, which is what you need in order to recognize the same failure in an unfamiliar system. **What it looks like in practice** is a concrete instance, drawn from the Harborlight mortgage-evidence scenario where it fits and from another domain where that better shows transfer. **How to replace it** gives the fix and its migration path, and **How to know the repair worked** gives the signals that tell you whether you still have the problem and the honest cost of the correction.

The trade-off field matters. Every correction in this catalog costs something — latency, flexibility, or engineering time — and applying all sixteen to a read-only internal assistant would be malpractice. Correct in order of the blast radius of the effects involved.

## Reasoning and control flow

These two failures share a root cause: the model is allowed to decide when to stop. Once stopping is a model decision, termination, budget, and blast radius all become probabilistic properties of a text generator, and no amount of prompt tuning makes them deterministic again. The correction in both cases is to move the stopping decision into code that the model cannot reach.

### AP-01 — Autonomous monolith

**How this failure starts.** A prototype that worked convincingly in a notebook is promoted toward production. It mixes reasoning, run state, credentials, tool invocation, retries, approval, and its own completion signal in a single process, because nothing in the prototype phase forced those concerns apart. The tempting shortcut is “One unconstrained agent owns end-to-end control. The loop decides what to do, does it, and then declares the outcome.” It breaks down because probabilistic behavior becomes the control plane. There is no boundary at which a failure can be isolated, so a flawed reasoning step and a failed database write are indistinguishable from outside the process. Run state lives in memory, so a restart loses work that has already had external effects. Nothing can be replayed, because nothing durable was recorded — the transcript is a narrative, not a ledger.

**What it looks like in practice.** Mortgage evidence review restarts after a routine deploy and sends the same document request twice, because the only record of the first request was the agent's conversation history.

**How to replace it.** The replacement is explicit: A bounded runtime inside a durable workflow, with policy, tool and effect, and acceptance services each owning their decision. The migration path is clear: Monolith → direct tools → "done" becomes workflow → semantic nodes → governed effects → acceptance.

**How to know the repair worked.** Track protected calls that bypass the gateway, work lost per restart, false-completion rate, and the number of distinct responsibilities living in one process. The price of the safer design is clear: decomposition adds interfaces, deployment surface, and latency. Decompose around the highest-risk effects first; a read-only assistant does not need the full split.

### AP-11 — Unbounded loops and recursive delegation

**How this failure starts.** Work varies in complexity, and a fixed step count either truncates hard cases or wastes budget on easy ones, so the team lets the agent iterate and delegate as needed. The tempting shortcut is “Agents iterate and spawn children with per-call limits but no global ceiling. Each individual decision looks reasonable.” It breaks down because local limits do not compose. A depth limit of five with a fan-out of five is 3,125 leaf tasks, and each child inherits a fresh budget rather than a share of the parent's. Delegation graphs become cyclic when two specialists can each call the other, and no participant can detect the cycle from inside it. Queue saturation then degrades unrelated tenants, which is how one runaway research task becomes a platform incident.

**What it looks like in practice.** A research supervisor spawns fact-checkers that themselves spawn fact-checkers; the run consumes a day of tenant quota before a human notices, and every individual agent behaved exactly as instructed.

**How to replace it.** The replacement is explicit: Global budgets that decrease monotonically across delegation, an acyclic ownership graph, and explicit depth, fan-out, and no-progress limits enforced by the runtime rather than by instructions. The migration path is clear: Recursion becomes a runtime-governed task graph.

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

**How to know the repair worked.** Track delegation depth and fan-out distributions, repeated state signatures, no-progress step count, and budget-exhaustion rate by tenant. The price of the safer design is clear: caps truncate genuinely hard work. Set them from observed distributions rather than intuition, and make exhaustion a visible, escalatable terminal rather than a silent stop.

## Context, knowledge and memory

Everything an agent believes arrives through one of these three channels, and all three fail the same way: a convenient representation is mistaken for an authoritative one. A transcript is convenient. A similarity hit is convenient. A remembered fact is convenient. None of them is a system of record, and treating any of them as one moves business truth into a store with no owner, no schema, and no audit.

### AP-02 — Prompt as database

**How this failure starts.** Business state has to survive across turns, restarts, and handoffs, and the conversation already contains it. The tempting shortcut is “Chat history, or a rolling summary of it, is treated as the authoritative record of what has happened.” It breaks down because every mechanism that keeps a context window viable is lossy. Truncation drops the oldest facts, which are often the decisions; summarization paraphrases, and a paraphrase of "legal approved with conditions" is not a legal approval. There is no concurrency control, so two turns that both update a value silently diverge. There is no schema, so nothing detects that a field went missing. And there is no audit trail an investigator can read.

**What it looks like in practice.** A contract renewal forgets that legal approved with conditions, because the approval was three summarization rounds ago and the summary kept the outcome but dropped the conditions.

**How to replace it.** The replacement is explicit: Canonical typed state in a service that owns it, with the prompt receiving a ContextManifest projection built fresh from that state on every step. The migration path is clear: Transcript-as-state becomes State Service → snapshot → prompt.

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

**How to know the repair worked.** Track facts lost across compaction boundaries, disagreement between summary and store, and state mismatches discovered on recovery. The price of the safer design is clear: typed state requires schema design and migration discipline. The cost lands early and visibly, which is precisely why it gets deferred.

### AP-09 — Vector store as source of truth

**How this failure starts.** Relevant knowledge has to be found across a corpus too large to pass into a prompt. The tempting shortcut is “A similarity hit is treated as a current, authorized, authoritative fact.” It breaks down because similarity measures resemblance, not currency, authority, or permission. An index contains what was ingested, including superseded policies, duplicated drafts, documents the caller may not read, and anything an attacker managed to insert. Nothing in a cosine score distinguishes the approved policy from its withdrawn predecessor, and a confident citation of the wrong document is more damaging than no citation at all.

**What it looks like in practice.** An obsolete policy chunk applies a superseded spending limit, and the answer cites the document by name, which is what makes the reviewer believe it.

**How to replace it.** The replacement is explicit: Governed sources and snapshots hold authority; the index is a derived locator whose hits are verified for ACL, freshness, and supersession before the content reaches the model. The migration path is clear: Vector hit → action becomes source + ACL + snapshot → evidence → decision.

**How to know the repair worked.** Track evidence age at decision time, source disagreement rate, ACL mismatches at retrieval, and citations pointing at superseded revisions. The price of the safer design is clear: authoritative lookup adds latency to every retrieval. Apply it in proportion to what the answer will be used for; drafting assistance and payment authorization do not need the same guarantee.

### AP-13 — Memory write by default

**How this failure starts.** Personalization is genuinely valuable, and the cheapest way to get it is to remember everything. The tempting shortcut is “Every interaction, or a summary of it, becomes a durable memory record.” It breaks down because writing by default means writing without provenance, purpose, or verification. Secrets get persisted. Model errors get persisted and then retrieved as established fact, which is how one hallucination becomes a standing belief. Injected instructions from a document become durable instructions. And because nothing recorded why a memory was written, nothing can decide when it should expire or who may delete it — which turns a retention obligation into an archaeology project.

**What it looks like in practice.** A malicious mortgage document is processed, and the bank account it contains is stored as an applicant fact. Every subsequent run retrieves it as if it were verified evidence for the mortgage case.

**How to replace it.** The replacement is explicit: Memory writes are candidates, not side effects: purpose-bound, carrying provenance, verified before promotion, scoped to a tenant and subject, with a TTL and a deletion path. The migration path is clear: Transcript → memory becomes candidate → gate → typed record.

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

**How to know the repair worked.** Track sensitive-data writes caught by DLP, retrieval of stale records, correction and deletion rates, and incidents traceable to a single memory record. The price of the safer design is clear: a strict write path reduces the perceived magic of personalization and requires someone to own purpose definitions. The alternative is an unowned database of unverified claims about your customers.

## Security and delegated authority

The three cards here are the difference between *can* and *may*. An agent that can reach a resource, can see a tool, or can produce a plausible safety score has demonstrated capability, not permission. Each card is a case where capability was allowed to stand in for a policy decision, and in each the correction is the same: make the authorization decision explicitly, in code, at the moment of use.

[[DIAGRAM:anti-ambient-authority|Figure 17-2 — Ambient authority versus a narrowed, short-lived capability lease]]

### AP-03 — Ambient authority

**How this failure starts.** Agents need access to enterprise systems, and provisioning narrow credentials for every task and tenant is laborious. The tempting shortcut is “Workers receive broad, long-lived, reusable credentials — often a service account that predates the agent and was already over-scoped.” It breaks down because the credential's scope, not the task's need, defines the blast radius. Any compromise — prompt injection, a malicious tool, a leaked log — yields durable authority over everything the credential can reach. Because the same credential serves every run, nothing in the audit trail distinguishes which subject's work caused which effect, so attribution fails exactly when it is needed. And a credential that never expires cannot be revoked faster than someone notices.

**What it looks like in practice.** The support agent's token can export the full customer table. Nothing in the onboarding task requires it; the token was reused because it already existed.

**How to replace it.** The replacement is explicit: Preserve both subject and workload identity, derive a capability envelope by intersection, and mint a short-lived, audience-bound credential lease at the moment of use. The migration path is clear: Broad token becomes policy → scoped lease → enforcement at the resource.

**How to know the repair worked.** Track credential scope and age distributions, granted-but-unused privilege, scope-expansion attempts, and cross-tenant access denials. The price of the safer design is clear: fine-grained policy adds design effort and a policy-decision hop per call. The hop is cacheable; the design effort is not, and it is the part teams underestimate.

### AP-10 — LLM judge as security gate

**How this failure starts.** Some content is genuinely ambiguous, and a model is better than a regular expression at recognizing nuance. The tempting shortcut is “A model-produced score alone authorizes a protected action — if risk_score < 0.3: execute().” It breaks down because a judge is an injectable, nondeterministic component being asked to make a binding decision. The same input can score differently across runs, so the gate is not reproducible and an incident cannot be explained. The content being judged can address the judge directly, which makes the attacker a participant in their own authorization. And judge behavior drifts with model updates, silently moving the threshold without any release event.

**What it looks like in practice.** The judge classifies an unusually large payment as low risk because the request text explains, persuasively, why it is routine.

**How to replace it.** The replacement is explicit: A deterministic policy and invariant gate makes the decision. The judge triages, prioritizes, and supplies evidence for a human — it never holds the authorization. The migration path is clear: score < threshold → execute becomes policy → optional judge → human escalation.

**How to know the repair worked.** Track disagreement rate across repeated runs of identical input, gate bypass attempts, false negatives found downstream, and human override frequency. The price of the safer design is clear: deterministic rules genuinely cannot express every nuance, and some legitimate work will be escalated unnecessarily. That is the correct direction to fail.

### AP-12 — Ungated tool discovery and catalog dumping

**How this failure starts.** A mature platform has many tools, and the agent cannot use what it cannot see. The tempting shortcut is “Every discovered tool and its full schema is placed into the prompt, often straight from an MCP server's advertised catalog.” It breaks down because discovery is being used as authorization. Selection accuracy falls as the catalog grows, because the model is choosing among near-neighbours it has no basis to distinguish. Schemas consume context that evidence should occupy. Worse, tool descriptions are untrusted text from a third party, so a malicious server can write a description engineered to attract calls — the agent is reading attacker-controlled instructions and treating them as a menu.

**What it looks like in practice.** A reporting agent discovers an administrative delete tool, because the catalog was filtered by connectivity rather than by the caller's authority.

**How to replace it.** The replacement is explicit: Registry → eligibility and policy evaluation → task-specific shortlist → schema validation at call time. Eligibility is computed from the subject, purpose, tenant, and risk tier, never from what the server happens to advertise. The migration path is clear: Full MCP catalog becomes an approved tool slice bound to a lease.

**How to know the repair worked.** Track tools exposed versus eligible versus actually used, selection-confusion rate, schema token overhead per run, and unauthorized discovery attempts. The price of the safer design is clear: a narrow shortlist will sometimes omit a tool that would have helped. Make the omission observable so the shortlist can be improved deliberately, rather than widening it by default.

## Effects, retries and recovery

These two cards are among the most expensive in the catalog, because they produce duplicate real-world effects — duplicate mortgage-document requests, duplicate payments, or duplicate emails to customers (the latter two are comparative examples). Both stem from confusing the transport layer with the effect layer: a failed call is not a failed effect, and an unacknowledged call is not an absent one.

[[DIAGRAM:anti-retry-storm|Figure 17-3 — Layered retries and timeout-as-failure versus one retry owner with an unknown-effect terminal]]

### AP-04 — Retry everywhere

**How this failure starts.** Transient failures are real and common, and every layer in the stack offers a retry setting that looks like diligence. The tempting shortcut is “The SDK, the gateway, the workflow engine, the connector, and the tool each retry independently.” It breaks down because retries compose multiplicatively, not additively. Three layers at 3, 3, and 2 attempts produce eighteen calls for one logical operation, and each layer believes it made a modest choice. The amplification arrives precisely when a dependency is already degraded, converting a slow dependency into an outage. If any layer retries a non-idempotent call, the duplicates are permanent.

**What it looks like in practice.** A single mortgage evidence review produces eighteen calls to an employment-verification source, and the provider rate-limits the lender for the rest of the day.

**How to replace it.** The replacement is explicit: One retry owner per failure class, with a shared attempt and deadline budget that every layer reads and no layer resets. The migration path is clear: Nested retries become classified failure → one schedule → terminal.

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

**How to know the repair worked.** Track attempts per logical operation, amplification factor against dependencies, duplicate effect keys, and deadline overruns caused by retry time. The price of the safer design is clear: a single central policy is necessarily more conservative than a hand-tuned one per call site. Express the variation as failure classes rather than as per-layer settings.

### AP-05 — Timeout means failure

**How this failure starts.** A response is lost after a request was dispatched, and the run has to decide what to do next. The tempting shortcut is “The call is marked failed and retried immediately.” It breaks down because a timeout describes the response, not the effect. The first call may have committed, may be committing, or may never have arrived, and the caller cannot distinguish these from the outside. Treating that state as failure asserts knowledge the system does not have, and the retry then creates the duplicate that the timeout only made possible.

**What it looks like in practice.** The mortgage document request is recorded twice: the first call committed just after the client gave up waiting.

**How to replace it.** The replacement is explicit: An explicit unknown-effect terminal that blocks retry until reconciliation resolves it against the downstream system of record. The migration path is clear: timeout → failed → retry becomes timeout → unknown → lookup → decide.

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

**How to know the repair worked.** Track count and age of unresolved unknown effects, duplicate idempotency keys observed downstream, and conflicts discovered after a timeout. The price of the safer design is clear: unknown terminals delay completion and need somewhere to go when reconciliation cannot resolve them. That queue is the price of not creating duplicate financial records.

## Approval, acceptance and governance

Both cards here concern the moment a system decides that something is allowed, or that something is finished. In each, a cheap signal — a Boolean, a sentence of model output — was allowed to carry a decision that the enterprise will later be asked to defend. The correction is to make the decision an artifact: something with a hash, an owner, an expiry, and an independent check.

[[DIAGRAM:anti-approval-binding|Figure 17-4 — Boolean consent versus proposal-bound, expiring human action authorization]]

### AP-06 — Boolean or conversational approval

**How this failure starts.** Humans must approve protected actions, and a chat interface makes approval feel natural. The tempting shortcut is “A Boolean flag or a chat message — "yes, go ahead" — authorizes whatever the arguments happen to be at execution time.” It breaks down because approval is being bound to a conversation rather than to an effect. Between consent and commit, the amount, the recipient, the policy version, the acting workload, or the underlying record can all change, and nothing detects it. The approver reviewed a description; the system executes a payload. A Boolean also cannot express scope or expiry, so a single "yes" silently authorizes later, larger, and unrelated actions.

**What it looks like in practice.** An approval given for a $10,000 payment is reused, entirely within policy as implemented, for a $100,000 one.

**How to replace it.** The replacement is explicit: An immutable proposal, hashed over the exact effect, with a HumanActionAuthorizationDecision bound to that hash, scoped to one action, and carrying an expiry. Revalidate immediately before commit. The migration path is clear: approved=true becomes proposal hash → HumanActionAuthorizationDecision → revalidate → commit.

🐍 · anti-pattern and correction

```python
# Anti-pattern: consent is a flag on the run, detached from what executes.
if run.approved:
    await underwriting.submit_evidence_package(case_id=current.case_id)

# Correction: the decision is bound to a hash of the exact proposal and cannot
# authorize a payload the approver never saw.
proposal = Proposal(
    action="underwriting.submit_evidence_package",
    args=args,
    policy_version=policy.version,
)
decision = await human_action_authorization.await_decision(proposal.digest(), ttl_s=900)

if decision.proposal_hash != proposal.digest():  # arguments moved since authorization
    raise HumanActionAuthorizationMismatch(proposal.digest(), decision.proposal_hash)
if decision.expires_at <= now():                 # authorization has a shelf life
    raise HumanActionAuthorizationExpired(decision.authorization_id)
await underwriting.submit_evidence_package(
    **proposal.args, idempotency_key=proposal.digest()
)
```

**How to know the repair worked.** Track proposal-hash mismatches at commit, authorization reuse attempts, expiry rate, and incidents occurring after a recorded decision. The price of the safer design is clear: benign changes force reauthorization, which reviewers experience as friction. Tune by making the diff visible — showing what changed is cheaper than widening the authorization.

### AP-07 — Model says done

**How this failure starts.** A run needs a completion signal, and the model produces a confident, well-formed one for free. The tempting shortcut is “The model's assertion sets the run to success.” It breaks down because the model is reporting on its own work using the same faculty that produced it. A missing evidence artifact, a skipped approval, an uncommitted effect, or an unmet obligation all present as success, because none of them changes what the model believes it did. Failures therefore surface downstream — in reconciliation, in audit, or in a customer complaint — long after the trace has aged out.

**What it looks like in practice.** Onboarding reports complete while the sanctions screening is stale, because the model saw a screening result in context and did not evaluate its freshness.

**How to replace it.** The replacement is explicit: An independent, executable acceptance check evaluated over authoritative state, returning accepted, blocked, needs-input, failed, or unknown-effect. The model may propose completion; it may not declare it. The migration path is clear: Model text → success becomes AcceptanceEngine → typed terminal.

**How to know the repair worked.** Track false-completion rate found by audit, reopen rate, and runs closed with missing artifacts or uncommitted effects. The price of the safer design is clear: executable acceptance criteria need domain ownership and maintenance. Without them the completion signal has no author, which is worse and merely less visible.

## Multi-agent collaboration

### AP-08 — Multi-agent chat as workflow

**How this failure starts.** Specialists need to coordinate, and a shared conversation is the fastest coordination mechanism to build. The tempting shortcut is “Free-form messages between agents own state, work assignment, deadlines, and completion.” It breaks down because a conversation has no notion of ownership, so two agents can both believe the other is acting — or both act. It has no join semantics, so nothing knows when parallel work has finished. Cancellation cannot propagate, because there is no structure to propagate through, and artifacts produced mid-conversation are lost when the window compacts. The system behaves like a meeting with no chair and no minutes.

**What it looks like in practice.** Finance and legal each wait for the other to approve. The run sits open for three days and neither agent is wrong.

**How to replace it.** The replacement is explicit: A typed TaskEnvelope with exactly one accountable owner, explicit child tasks, artifacts stored by reference, and a deterministic join evaluated by the coordinator rather than inferred from messages. The migration path is clear: Chat mesh becomes supervisor workflow plus task service.

**How to know the repair worked.** Track orphaned tasks, conflicting concurrent effects, delegation depth, join wait age, and effects landing after a run was considered complete. The price of the safer design is clear: formal task envelopes reduce the fluidity that makes agent conversations appealing to demonstrate. The fluidity is what fails in production.

## Observability and evidence

### AP-14 — Telemetry without causal or effect lineage

**How this failure starts.** Teams instrument what they own, and each component's dashboard looks healthy. The tempting shortcut is “Logs, metrics, and traces cannot be joined to versions, policy decisions, effects, acceptance, or business outcome.” It breaks down because without a join key, every measurement is local. A component can improve on its own metric while degrading the outcome, and nothing in the telemetry can express the relationship. Cost cannot be attributed to a tenant, a release, or a decision, so optimization targets whatever is easiest to measure. When an incident happens, the investigation has to reconstruct causality by hand from timestamps.

**What it looks like in practice.** A model swap lowers median latency by 15%, which the dashboard celebrates, while retries rise and task completion falls. Both facts are true and neither dashboard contains both.

**How to replace it.** The replacement is explicit: One causal run graph joining release version, context manifest, model and policy decisions, tool effects, acceptance terminal, business outcome, and cost. The migration path is clear: Separate dashboards become one correlated graph.

**How to know the repair worked.** Track percentage of runs joinable to a business outcome, spans missing parent or version identifiers, and unattributed spend. The price of the safer design is clear: correlation requires disciplined identifier propagation across every component and raises the governance burden on telemetry, including redaction. Retrofitting it after an incident costs considerably more.

## Platform, release and operations

Both cards describe the same instinct — change should be fast — applied where it removes the ability to explain, reproduce, or undo what happened. Speed is not the problem; unversioned speed is.

### AP-15 — Model or provider swap as configuration

**How this failure starts.** Teams want better cost or quality, and the routing layer makes the change a one-line edit. The tempting shortcut is “A model alias is repointed without behavioral validation, because no application code changed.” It breaks down because the model is the behavior. Tool-calling reliability, schema adherence, refusal boundaries, safety posture, latency distribution, and cost per task all shift together, and they shift unevenly across slices — a change that is neutral in aggregate can be severe for one language, one document type, or one tenant. Because no release event was recorded, the resulting regression has no obvious cause and cannot be rolled back precisely.

**What it looks like in practice.** A cheaper model drops tool arguments for one language only. Aggregate evaluation stays green; that market's completion rate halves.

**How to replace it.** The replacement is explicit: A versioned ChangeBundle carrying evaluation across slices, security testing, load testing, canary exposure, and a named rollback target. The migration path is clear: Edit alias becomes immutable route policy → replay → approval → canary.

**How to know the repair worked.** Track schema and tool-call regression rate, refusal-rate shift, per-slice quality drift, and fallback-route activation. The price of the safer design is clear: validation slows experimentation, so make the fast path cheap: pre-built replay sets and automated slice reports, rather than an approval meeting.

### AP-16 — In-place change and test after release

**How this failure starts.** A production issue needs a fix now, and the console offers an edit box. The tempting shortcut is “Prompts, Skills, tool definitions, policy, and routes are mutated directly in production.” It breaks down because a run can no longer be reproduced, because the artifacts it used no longer exist in the form it used them. Attribution fails, since two runs a minute apart may have used different behavior with no record of the boundary. Rollback becomes guesswork about what the previous state was. And the edit itself is untested by construction — the test is the production traffic.

**What it looks like in practice.** A prompt edit intended to reduce verbosity increases data leakage. Neither the previous prompt nor the exact leak conditions can be reconstructed.

**How to replace it.** The replacement is explicit: Immutable artifacts, a ReleaseManifest that pins everything a run resolves, pre-promotion tests, signed promotion, canary exposure, and a rollback target that is verified rather than assumed. The migration path is clear: Mutable console becomes build → validate → approve → promote → monitor.

**How to know the repair worked.** Track runs executing unversioned artifacts, out-of-band edit events, and rollback rehearsal failures. The price of the safer design is clear: immutability needs genuinely good tooling, or people will route around it under pressure. If the emergency path is slower than the console, the console wins — so make the fast path immutable rather than making immutability optional.

|  |
| --- |
| **COMMON PITFALL**  The most expensive anti-patterns in this catalog are not the exotic ones. AP-04, AP-05, and AP-06 produce duplicate payments, duplicate records, and unauthorized effects, and all three look like ordinary engineering diligence while they are being built. Audit those three first. |

## Where this leads next

After removing unsafe local architectures, Chapter 18 considers when multiple agents add justified specialization rather than accidental complexity.
