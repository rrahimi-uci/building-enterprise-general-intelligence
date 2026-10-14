# PART IV — PATTERNS THAT WORK—AND THOSE THAT FAIL

Patterns are shortcuts for thinking, but they are only helpful when their
boundaries are visible. Every pattern here places a model step inside the
platform of Part III: the step receives a resolved slice of Skills and tools
(Chapters 8–9), its outputs cross the six gates (Chapter 2), and the framework
stays behind AgentRuntime (Chapter 3). Each pattern chapter answers three
questions: what the model may decide, what the controller owns, and how the
pattern stops and is accepted.

- **Chapters 10–15** run from the smallest bounded loop through routing, planning, reflection, and human review to durable work.
- **Chapter 16** compares and combines these patterns.
- **Chapter 17** names the failure shapes they prevent, several corrected by mechanisms Parts V–VIII build.

A design review can then ask not only “what could work?” but also “how would
this fail in production?”

# 10 — Use ReAct Without Creating a Runaway Loop

> **Evidence context:** ReAct was introduced as a prompting paradigm that interleaves reasoning and action; its reported benchmark results motivate the loop, not an assertion that unrestricted production autonomy is safe. **[R01]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** A loan officer asks why a mortgage case is not ready for underwriting. One retrieval is insufficient: the system may need the application projection, an income-verification artifact, and a policy explanation. A bounded ReAct loop is appropriate because the next information need depends on the previous observation. |

|  |
| --- |
| **THE DESIGN CHOICE** Use ReAct only when the next step depends on what the last observation returned, and let the controller—never the model—end the loop at a turn, tool-call, time, cost, or no-progress limit. |

The choice has two halves. The first decides whether to loop at all. ReAct
earns its cost only when the next action cannot be known until the last
observation arrives. When Harborlight's loan officer asks why a case is not
ready, whether the agent next needs the income-verification artifact or the
policy text depends on what the application projection showed. The next
section draws the line between that and a sequence a workflow should own.

The second half decides how the loop ends. A model asked whether it is done can
always find one more thing to check, so the stopping rules sit outside it, in
the controller that runs the loop. Each limit is fixed before the first turn,
from the Skill's `runtime` block and the step's budget in the AgentStepRequest
(Chapters 3 and 8), and the controller counts it on every turn. Nothing the
model writes can raise a limit or reset a counter.

| **Limit** | **What the controller counts** | **Harborlight setting** | **When it trips** |
| --- | --- | --- | --- |
| Turns | Model decisions in this activity | 6 (the Skill's `max_turns`) | Stop with `budget_exhausted` |
| Tool calls | Read-tool calls, across every tool | 4 | Refuse the next call; stop with `budget_exhausted` |
| Time | Wall-clock time since the activity started | 45 s (the Skill's `deadline_s`) | Stop with `budget_exhausted` |
| Cost | Tokens and spend, drawn from the run budget | The share of the run budget granted to this step | Stop with `budget_exhausted` |
| No progress | Repeats of the same action returning the same observation, and turns that add no accepted evidence | A second identical observation | Stop with `no_progress` |

A tripped limit is an expected outcome, not a crash: the controller returns it
as a typed stop reason, and the workflow decides what happens next
(§ Acceptance and failure semantics).

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| External loop controller and acceptance engine | observation/model and model/tool | turn · tool permit · run budget | one bounded loop | AgentDecision · Observation · AgentStepResult · ReActLimits |

## Use ReAct only when observations change the next step

If the sequence is already known—read the case, validate required fields, calculate a ratio, request approval—a durable workflow is clearer and usually cheaper. That avoids paying a model to rediscover a process the organization already understands. Even when ReAct is justified, the loop also ends when the evidence it needs cannot be obtained: the model returns `needs_input` rather than searching on. The tools a ReAct step can call are the slice resolved for that step from its pinned Skills (Chapter 8) and exposed through the Tool Gateway (Chapter 2); the loop never discovers tools on its own.

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

The discussion above draws on R01. Appendix J lists the complete sources and records their authority, version, and scope.

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

The discussion above draws on R29. Appendix J lists the complete sources and records their authority, version, and scope.

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
* A node that evaluates a rule or decision table binds to the run's pinned knowledge release; a node that needs an object the release does not hold as evaluable (absent, review-held, or Revoked) is refused here, naming the object (Chapter 5).
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
| Durable scheduling | Durable execution resumes work in a new process after a failure and supports reliable long waits; scheduling compiled plans through a workflow rather than an in-process loop is this book's recommendation. | R02 |

The discussion above draws on R27; R02. Appendix J lists the complete sources and records their authority, version, and scope.

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

Reflection asks, “What is missing or inconsistent?” Evaluation asks, “Does this candidate meet an acceptance rubric?” In the mortgage case, the contradictory address is caught by an executable check against the application projection; whether the recommendation overstates confidence is the kind of qualitative criterion a calibrated judge may assess. Combining reflection and evaluation can improve complex artifacts, but only if the roles are explicit and bounded. The platform runs executable checks before any model judge: schema, evidence presence, policy, effect state, resource version, arithmetic, and deterministic domain rules from the run's pinned knowledge release (Chapter 5).

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
| Evaluation tooling | MLflow's evaluation documentation covers evaluation datasets, custom code-based scorers, LLM judges, and human feedback attached to traces; using judges only as evidence for an independent acceptance decision is this book's recommendation. | R20 |

The discussion above draws on R20. Appendix J lists the complete sources and records their authority, version, and scope.

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
| **WHERE THE MORTGAGE CASE STANDS** A protected mortgage-case operation requires human approval. The reviewer must see the exact operation, destination, evidence, expected resource version, and risk—not a vague request to “approve the mortgage.” |

|  |
| --- |
| **THE DESIGN CHOICE** Persist proposal-bound approvals as durable workflow events and reauthorize immediately before commit. |

## Why human review must change system state

Human review is most useful when it resolves a decision the system cannot or
should not make alone. It becomes theater when the reviewer sees a summary
that can change after approval, or when a click is detached from the effect it
approves. This chapter binds approval to an immutable proposal, evidence,
identity, expiry, and a durable state transition.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Workflow plus Approval Service | machine proposal to human authority | approval and intervention queues · risk class · tenant | one immutable proposal | ApprovalRequest · ApprovalDecision · InterventionTask · EffectReceipt |

## Separate approval, intervention, and operator control

Three human controls carry different authority. **Approval** comes before an effect: it asks whether one exact proposal may proceed, so the interface shows the immutable proposal, evidence, consequences, and expiry. **Intervention** is raised by the system when a run cannot finish alone: a person diagnoses, corrects, supplies information, or chooses among unresolved alternatives, so the interface exposes uncertainty and viable alternatives. **Operator control** is a person acting on a run in flight through governed commands. Intervention and operator control both change a running run; neither approves an effect. Each control gets its own queue, role, form, SLO, and terminal semantics, because one generic approval queue encourages rubber-stamping and makes the audit record difficult to interpret.

[[DIAGRAM:pattern-hitl|Figure 14-1 — Approval and intervention: different triggers, different authority, different evidence]]

The Approval Service stores an immutable canonical proposal, which becomes invalid when any protected field changes, and the commit path rechecks it (§ Approval contract and § Records worth preserving give the fields). Chapter 3 showed that an SDK pause is only an interruption; this record is what turns it into an approval.

Human capacity is finite. Arrival rate, service time, queue age, dwell, abandonment, reassignment, rejection, correction, disagreement, and after-hours coverage are production metrics. A system that requires routine approval for low-risk deterministic work may be less safe because reviewers become fatigued.

## Design human review as part of the system

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Humans must understand, approve, correct, or stop consequential work without becoming a rubber stamp or breaking run integrity. |
| Why it is difficult | Too many approvals cause fatigue; too little context prevents informed decisions; approvals can go stale as data or plans change; edits must be attributable and replayable. |
| Design alternatives | Confirm every tool call; risk-based approvals; maker-checker; sampled review; exception-only review; fully manual commit. |
| Recommended architecture | Use policy-triggered gates based on risk, novelty, confidence, value, data sensitivity, reversibility, and destination. Present a concise preview, evidence, alternatives, changed fields, policy rationale, and blast radius. An ApprovalDecision approves a specific immutable proposal for a limited time. |
| Trade-offs | Human review adds latency and staffing cost but provides judgment and accountability where automation evidence is insufficient. Poor UX converts the control into theater. |
| Failure scenarios | Approval applies to a changed plan; approver lacks authority; agent hides uncertainty; request times out; two operators issue conflicting overrides; “approve all” becomes normal. |
| Enterprise example | A mortgage agent drafts a request to obtain the missing second pay statement. The underwriter sees the policy basis, case evidence, requested document, downstream effect, and alternatives; any case, document, or destination change invalidates the approval. |

### Approval contract

An ApprovalRequest contains what the approver must see: the proposal hash over the exact action and arguments, the resource and its `logical_effect_key`, the before/after diff, subject and actor, evidence links, uncertainty, the policy rule and its `policy_digest`, risk class, estimated impact or cost, the reversible flag, the `expected_resource_version`, expiry, the separation-of-duties requirement, and the allowed responses (approve, reject, edit-and-resubmit, request-evidence, cancel-run).

Approving a plan (Chapter 12) approves its scope, not its effects. Each protected effect still receives its own proposal-bound approval, unless the approved plan already fixed that effect's canonical proposal and the plan revision is unchanged at commit.

### Intervention contract

Every Part IV escalation lands in the intervention queue as a typed InterventionTask: no progress or an exhausted budget in a ReAct loop (Chapter 10), a route below threshold sent to human triage (Chapter 11), a plan that fails compilation or revision (Chapter 12), a generator and evaluator that keep disagreeing (Chapter 13), and a run that reaches InterventionRequired or holds an Unknown effect that reconciliation cannot settle (Chapters 15 and 22). The reviewer sees the uncertainty, the competing artifacts or alternatives, the current state version, and what is blocked. The allowed responses are to supply information (a typed signal to the workflow), choose an alternative (a plan revision under Chapter 12's rules), correct state (a governed update with an expected version), reassign, cancel, or declare an operational resolution with a reason. Responses use the run's signal and update endpoints (Chapter 4). An intervention response is an input to the run; it never approves an effect, and any protected effect it leads to still needs a proposal-bound approval.

### Operator console requirements

Operator control is the third human role: a person acts on a run in flight, and every action is a governed command recorded against the run.

* Live run graph (Chapter 24) with current owner, state, budgets, queues, waits, child tasks, and last committed effect.
* Redacted but causally complete trace; model/tool inputs available only to authorized incident roles.
* Pause, cancel, retry safe activity, skip with justification, patch plan, reassign approval, increase budget, trigger compensation (Chapter 22), and fork a sandbox replay (Chapter 24).
* Conflict detection and optimistic versions for operator edits.
* Immutable operator identity, reason, timestamp, before/after state, and linked ticket on every override.
* SLA timers and escalation paths for every queue.
* Review and intervention forms are tested against WCAG 2.2 [R41]. Conformance does not remove automation bias, so measure it: reviewer agreement on seeded cases and override rate.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Approval Policy Router | Convert policy obligations, risk, value, novelty, and confidence into approval requirements |
| Approval Service | Persist immutable proposal snapshots and authoritative decision state |
| Assignment/Queue Service | Resolve eligible approvers and intervention assignees, maker-checker rules, claim/reassign, priority, and SLA |
| Evidence Renderer | Produce role-redacted diff, sources, rationale, alternatives, uncertainty, and blast radius |
| Notification Service | Deliver idempotent channel notifications and deep links; it never owns the decision |
| Operator Control Service | Invoke the run lifecycle commands (Chapters 4 and 15) and effect reconciliation/compensation (Chapter 22) on an operator's behalf, recording an OperatorAction for each |
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

### Records worth preserving

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ApprovalRequest | approval ID, tenant/run/node/effect, required approver predicate/count, state/version, plus the contract fields above |
| ApprovalEvidenceSnapshot | approval, immutable source/artifact refs and hashes, policy/rationale, uncertainty, alternatives, impact, redaction profile, created version |
| ApprovalAssignment | approval, queue, eligible-role predicate, assignee/claim lease, SLA, escalation level, state |
| ApprovalDecision | approval, proposal hash, approver identity/role/assurance, decision, reason, signature/attestation, time; append-only |
| InterventionTask | run/node, trigger and the source chapter's reason code, evidence refs, alternatives, allowed responses, assignee, SLA, state/version, response; append-only |
| OperatorAction | action ID, run, command, actor/role, target/version, before/after refs, reason, linked ticket, result/effect; append-only |
| EscalationPolicy | queue/risk/value, warning/expiry timers, fallback roles, business calendar, timeout disposition; implicit approval is forbidden |
| NotificationDelivery | approval/action, channel, destination handle, idempotency key, attempts, delivered/acknowledged, error; contains no unredacted evidence |

A decision is valid only when the presented proposal hash equals the current proposal, the approver is authorized at decision time, required counts/separation rules are satisfied, and the approval has not expired or been superseded. A valid approval proves authority over this proposal; it does not stop a duplicate or a stale overwrite. Chapter 22 pairs it with idempotency, expected versions, and receipts.

### Workflow integration

1. The workflow persists the proposed effect and evidence snapshot, then creates the approval.
2. The Approval Service registers durable SLA/expiry timers and returns a wait correlation ID.
3. Assignment and notifications may retry independently; the workflow remains suspended without a worker.
4. A decision transaction records the immutable decision and emits an outbox event.
5. The workflow receives the event, revalidates policy/current resource version, and commits only the proposal whose hash was approved.
6. If the resource, amount, recipient, scope, or policy changed materially, the workflow supersedes the approval and generates a fresh preview. Chapter 15 generalizes this wait to every timer, signal, and callback.

### What changes as usage grows

* Serialize decisions per approval, scale across approvals, and drive SLA timers from durable timers (Chapter 15), never table scans.
* Materialize queue views by eligibility dimensions and age. Compute final authorization at read/claim/decision time so an index cannot leak work after role changes.
* Coalesce notifications and support digest/batched review for low-risk homogeneous actions, but preserve one proposal and decision record per effect.
* Approval capacity is part of end-to-end capacity planning; size queues and staffing from the production metrics above.
* Prevent approval stampedes during incidents with per-queue rate limits, prioritized critical items, bulk-action policy, and explicit incident-mode controls—never an unbounded “approve all.”
* Decisions are written only in the run's home region (Chapter 27 covers failover fencing).

|  |
| --- |
| **PRODUCTION CONSIDERATION**  Design the wait, not just the prompt. A run paused for approval may sit for days across deploys, token expiry, and staff changes. Persist the full decision context with the pause. |

## Approval and intervention at a glance

An approval follows § Approval contract; an intervention is an InterventionTask as defined in § Intervention contract. Both are durable waits that resume through authenticated signals.

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

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Approval integrity | Book-authored recommendation, informed by R15's mitigation guidance for agentic applications: approve the exact canonical proposal, not a natural-language summary, and revalidate policy, authority, proposal hash, expiry, destination, and resource version immediately before commit. | R15 |
| Review interfaces | Review and intervention forms should meet WCAG 2.2 success criteria; conformance does not by itself remove automation bias. | R41 |

The discussion above draws on R15; R41. Appendix J lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The first example persists the wait and verifies a signed, expiring decision; the second is the commit-time check that the decision still covers this exact proposal and current state.

[[EXAMPLE:approval-gate]]

### Verify the decision at commit

[[EXAMPLE:approval-verification#core]]

## If this fails in production

1. Recompute the proposal hash and expected resource version.
2. Verify approver authority, expiry, and separation-of-duty policy.
3. Trace the approval event through commit and effect receipt.
4. If approval is a Boolean or a chat reply rather than a bound record, the repair is structural; see AP-06 in Chapter 17.

## What to verify before production

**✓** Approval, intervention, and operator control use separate queues, roles, forms, and terminal semantics.

**✓** Every approval request has an expiry and an explicit timeout disposition; a timeout never becomes implicit approval.

**✓** Approval binds to an immutable proposal hash and current authority and resource state.

**✓** Every Part IV escalation opens a typed InterventionTask, and no intervention response approves an effect.

**✓** Reconciliation, compensation, pause, cancel, and intervention are governed commands.

**✓** Reviewer queue age, dwell, abandonment, and agreement are monitored as SLOs.

## Put the idea to work

1. For the Harborlight document-request proposal, list which field changes force supersession and which do not.
2. Define how edits, policy changes, and expired approvals invalidate an approval.
3. Design the intervention task raised when Chapter 13's generator and evaluator disagree twice.

## Questions to bring to design review

| **Question** | **Strong answer** |
| --- | --- |
| Why separate approval from intervention? | Approval asks whether one exact effect may proceed; intervention supplies missing judgment or corrects a run. Separate queues, roles, forms, and terminal semantics keep the audit record interpretable. |
| What happens when an approval request times out? | It follows an explicit escalation policy and timeout disposition; a timeout never becomes implicit approval. |
| How should approval be bound to an action? | Persist the exact canonical proposal, preview, destination, evidence, risk, and hash; verify the approver's authority; reject expiry, supersession, hash mismatch, or stale resource state. |
| What may an intervention change, and what may it never do? | Supply information, choose an alternative as a plan revision, or correct state with an expected version; it never approves a protected effect. |
| How do operator overrides stay accountable? | Governed lifecycle commands with expected state, operator identity, reason, and linked ticket in an append-only journal. |

## Where this leads next

Human control introduces waits and resumptions; Chapter 15 makes those waits durable and gives long-running work explicit state and recovery.

# 15 — Keep Long-Running Work Alive Through Failure

> **Evidence context:** Durable-execution systems let work resume after failures and long waits, and agent frameworks integrate with several such backends; that replay semantics differ by backend, and must be checked for each one, is this book's caution. **[R02][R36][R38]**

|  |
| --- |
| **WHERE THE MORTGAGE CASE STANDS** The applicant waits nine days to upload the second pay statement. During the wait, workers deploy twice, policy changes, the loan officer loses a role, and one earlier request times out. The run must resume safely rather than restart from a prompt transcript. |

|  |
| --- |
| **THE DESIGN CHOICE** Represent long-running work as replay-safe workflow history plus bounded activities, durable waits, and reconciliation. |

## Why long-running work needs durable state

An agent that must wait for a document, a person, or a downstream system is no
longer a request/response handler. Its state has to outlive processes,
deployments, retries, and partial effects. This chapter shows how to model that
work as durable execution, and why recovery is part of the design rather than
an operations add-on. The platform needs a stable account of intent, state
transitions, pending obligations, timers, child tasks, approvals, and external
effects. Workers can then disappear and return without becoming the owners of
truth.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Durable workflow engine | workflow activity to external I/O | history shard · activity queue · timer | one workflow execution | WorkflowEvent · Checkpoint · WaitRegistration |

## Durable state is more than chat history

[[DIAGRAM:pattern-durable|Figure 15-1 — The run outlives the process: checkpoint, die, replay, adopt]]

Chat history cannot reliably encode timers, retries, child ownership, approval waits, cancellation intent, resource versions, effect receipts, or deployment compatibility. The platform rebuilds run state from event history; model and tool calls are bounded activities whose inputs and outputs are recorded by reference. This is Chapter 3's restart test made operational: a run must resume from its recorded decisions, approvals, and effect receipts even if every message and every worker is discarded.

The workflow reducer must be deterministic. It cannot read the clock, call a model, query a database, generate randomness, or perform network I/O during replay. Those operations become activities, signals, or recorded events. This separation makes a crashed worker replaceable.

## The durable execution contract

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Why it is difficult | Process memory is ephemeral; replay can repeat nondeterministic calls and side effects; external systems deliver duplicates or callbacks out of order; code and schemas evolve while runs are active. |
| Design alternatives | Background job + database; queue consumers; graph checkpointing; cloud state machines; durable execution engines such as Temporal/DBOS/Restate/Durable Functions; event-sourced custom runtime. |
| Trade-offs | Durable engines impose determinism/versioning constraints and operational cost, but remove far more bespoke recovery code. Graph checkpointers are useful for agent state but may not replace a mature cross-service workflow engine. |
| Failure scenarios | Replay resends an email; worker dies after effect but before acknowledgment; old run cannot replay after code change; callback is spoofed; event arrives before subscription; retry storm exhausts provider quota. |
| Enterprise example | A mortgage-evidence agent waits days for the second pay statement and for human approval. The workflow is unloaded while idle, resumes on correlated events, rechecks authorization, and continues from the last committed effect. |

### Workflow, activity, signal, query, update

* **Workflow code:** deterministic control logic only. No wall-clock reads, random values, direct network calls, or model calls unless captured as replay-safe activities.
* **Activity:** one bounded external interaction with timeout, retry class, idempotency key, heartbeat, cancellation behavior, and structured result.
* **Checkpoint:** the replay position and state reference from which a compatible worker resumes (fields in § Records worth preserving).
* **Signal:** authenticated external input (approval.granted, document.received, callback.completed, user.clarified) carrying a correlation key and monotonic event ID.
* **Query:** read-only inspection of run state for users and operators; must not advance execution.
* **Update:** authorized mutation such as budget increase, plan patch, assignee change, or safe retry, through the Run API's `:update` (Chapter 4).

### Checkpoint policy

Checkpoint after every irreversible or externally visible effect, before long waits, after plan revisions, and at fan-in boundaries. Do not serialize full prompt histories into every checkpoint; persist canonical state and immutable artifact references. Encrypt by tenant and apply retention by data class.

## The lifecycle of a durable run

Every pattern in Chapters 10–14 runs inside this lifecycle.

### Canonical control flow

1. **Admit.** Authenticate the caller; bind tenant, subject, channel, purpose, data classification, requested scope, and a client idempotency key.
2. **Snapshot.** Resolve immutable versions of the agent, workflow, prompt bundle, resolved Skill digests (Chapter 8), policy, model route, tool schemas, and knowledge index — the RunManifest (Chapter 4).
3. **Authorize.** Evaluate the requested goal and maximum capability envelope (capability envelopes, Chapter 21); allocate token, cost, time, tool, delegation, and concurrency budgets.
4. **Plan.** The model may propose a typed plan. Code validates DAG constraints, allowed capabilities, risk classes, preconditions, and budgets (plan compilation, Chapter 12; risk classes, Chapter 22).
5. **Execute.** The workflow kernel schedules replay-safe activities: routed workers (Chapter 11) and bounded ReAct activities (Chapter 10). Each effect is individually authorized using fresh context and a downscoped credential (credentials, Chapter 21).
6. **Checkpoint.** Persist state after every externally visible effect and meaningful decision; store large artifacts by immutable reference and hash.
7. **Wait or intervene.** Suspend without a worker for timers, callbacks, clarification, or approval (approval and intervention, Chapter 14). Signals carry correlation and authorization metadata.
8. **Validate and commit.** Deterministic validators test outputs and invariants. Effects pass the six gates (Chapter 2); critique may revise a draft but acceptance decides (Chapter 13).
9. **Complete.** Produce a typed result, evidence bundle, final cost/quality metrics, retention class, and terminal event.
10. **Learn safely.** Feed de-identified traces and failures into curated datasets; never let production memory or prompts self-modify without review (Chapter 25).

### Terminal correctness

A run reaches Succeeded only through executable acceptance. A canceled run with a possibly committed write does not simply disappear; it moves through reconciliation and possibly compensation. If correctness cannot be established automatically, the run moves to InterventionRequired: automated work stops, an intervention task opens, and the run closes only through that task's response.

| **Run state** | **Reached when** | **Never reached by** |
| --- | --- | --- |
| Running / Waiting | Work is scheduled, or suspended on a timer, signal, NeedsInput request, or approval; non-terminal | Holding a worker or model session open |
| CancelRequested | Cancellation intent is recorded; non-terminal until in-flight effects reconcile | Killing workers mid-effect |
| Succeeded | Acceptance passes over authoritative state | Model text claiming completion (AP-07, Chapter 17) |
| Failed | A permanent failure occurs and no effect is Unknown | A timed-out mutation, which is Unknown |
| Canceled | Cancellation intent is recorded and every effect is committed, compensated, or declined | Leaving an effect Unknown |
| Expired | A deadline or wait expires under an explicit disposition | Implicit approval or silent abandonment |
| InterventionRequired | Correctness cannot be established automatically; an intervention task opens (Chapter 14); non-terminal until its response resolves the run | Retrying until something works |

Step dispositions (Chapter 10) feed the workflow, acceptance decides (Chapters 2 and 13), and no run may close while an effect is Unknown; Chapter 22 owns effect states and compensation.

## Let events resume work without losing control

### Event-driven resume flow

1. Before reporting the run as waiting, the workflow persists a WaitRegistration: accepted sources, schemas, correlation keys, and expiry.
2. Event Ingress authenticates the event and writes the SignalInbox receipt, unique by tenant, source, and event ID.
3. The Correlator matches the event to the registration, or holds it as unmatched.
4. The signal or timer wakes the workflow, which revalidates authorization and resource versions after the wait.
5. The workflow continues from the last checkpoint, or supersedes stale approvals; Chapter 14 § Workflow integration is the approval instance.

### Event architecture

Events use the Chapter 4 CloudEvents envelope [R04]; producers use a transactional outbox and consumers an inbox (Chapter 22). Durable execution adds one rule: every correlation key must resolve to a wait registration or an unmatched-event holding area. A dead-letter queue is quarantine and diagnosis—not a substitute for domain compensation.

## A workable implementation

### Who should own each decision

| **Component** | **Responsibility** |
| --- | --- |
| Run API | Persist intent and return quickly |
| Durable workflow | Own the run lifecycle |
| Activity workers | Perform model and tool I/O |
| Event Ingress | Authenticate external facts |
| Correlator | Map those facts to waiting runs |
| Timer/Signal services | Wake workflows |
| Version Router | Keep compatible workflow builds available for in-flight histories |

### The contracts between components

The base Run API is in Chapter 4. Durable execution adds these operations and two semantics: `:signal` carries event ID, correlation key, schema version, and expected state; `:cancel` is durable intent with propagation and compensation policy, never immediate termination. History is read through Chapter 4's `GET /v1/runs/{id}/events`, role-redacted, with content referenced rather than embedded.

| **API** | **Purpose and contract** |
| --- | --- |
| POST /v1/events:ingest | Authenticate a CloudEvent, store inbox receipt, then route to a waiting workflow or unmatched-event holding area |
| POST /v1/runs/{run\_id}:pause | Administrative gate that prevents new activities while preserving timers/signals according to policy |
| POST /v1/runs/{run\_id}:resume | Resume after authorization/version checks; requires expected state version and reason |
| POST /v1/runs/{run\_id}:migrate | Apply an approved deterministic state/code migration with dry-run report and rollback boundary |

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

* Record model and external tool calls as activities whose results are persisted before workflow continuation. Replay returns the recorded result; it does not call the model or tool again. An attempt that fails before its result is recorded is retried even if its external call already succeeded, which is why side effects carry an effect key (below; Chapter 22).
* Wait registration before acknowledgment; inbox before signal. Together they close the “event arrived before subscription” race.
* For a side effect, persist intent/effect key before invocation and reconcile the receipt before an activity is considered complete (Chapter 22).
* Use logical workflow time for decisions. Wall-clock access, random IDs, and dynamic configuration are provided as recorded events/side effects.
* Continue-as-new or history compaction starts a new generation with a verified state snapshot when history size or event count reaches an engine-specific threshold; preserve an audit link to prior generations.

### Scalability and multi-region behavior

* Shard workflows by stable run ID and timers by time bucket + shard. Activity queues are separate from workflow-task queues so slow tools cannot starve state transitions.
* Waiting executions consume storage, not workers. Capacity planning distinguishes active workflow tasks, scheduled activities, open waits, timer cardinality, and history-write throughput.
* Autoscale activity workers on oldest-message age, arrival rate, observed service time, provider quota, and downstream health. CPU is only a secondary signal for I/O-heavy agent tasks.
* Use sticky execution caches for latency but require correctness without them; any compatible worker must rebuild state from history after eviction or failure.
* Assign each run one home region with one writer per generation; Chapter 27 covers fencing, restore, reconciliation, and resume during regional recovery.
* Separate task queues by workflow build compatibility. Keep old workers available for in-flight runs or migrate explicitly; never replay old history against untested new code. Chapter 27 makes this release policy: rollback reassigns new work only.
* Rate-limit external signals per tenant/source and coalesce superseding updates where domain semantics allow. Preserve individual inbox receipts even when only the latest value wakes the workflow.

## Durable execution at a glance

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

## What the evidence lets us conclude

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Durable progress | Durable execution is crash-proof execution: work resumes in a new process after a failure and can wait reliably for long periods. Rebuilding state by replaying recorded history, as this chapter's reducer does, is one engine design, not something the source specifies. | R02 |

The discussion above draws on R02; R04. Appendix J lists the complete sources and records their authority, version, and scope.

## A sensible place to start

The reducer folds recorded events into run state and performs no I/O, so replaying the same history always yields the same state.

### Replay-safe workflow reducer

[[EXAMPLE:durable-state#core]]

## If this fails in production

1. Replay workflow history with the pinned build and locate nondeterminism.
2. Inspect pending timers, signals, activities, and child tasks.
3. Resolve unknown effects before replaying dependent commands.
4. If state lives in a transcript or in one process, the repair is structural; see AP-01 and AP-02 in Chapter 17.

## What to verify before production

**✓** Workflow decisions are replay-safe; I/O, clocks, randomness, models, and tools are recorded activities.

**✓** Waits, signals, timers, cancellation, and child lifecycles are durable protocol state.

**✓** Each failure class has one retry owner; unknown effects route to reconciliation (Chapters 3 and 22).

**✓** Active histories stay pinned to compatible workflow builds and activity contracts.

**✓** Workflow tasks, activities, timers, waits, history writes, and reconciliation are capacity-planned separately.

## Put the idea to work

1. Model a nine-day wait with role revocation and policy change.
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

Chapters 10–15 have defined the loop and workflow patterns; Chapter 16 helps choose among them and shows how they compose in one run, and Chapter 17 names the failure shapes that the rest of the book corrects.

# 16 — Choose Patterns That Fit Real Enterprise Work

## How to choose a pattern for the problem you actually have

Pattern names are useful only when they help a team make a safer decision. The
same words can describe very different obligations: one workflow may need
adaptive evidence gathering, while another needs a durable process with
explicit ownership and compensation.

The patterns are decision aids, not recipes. Start with the obligation the system cannot violate: perhaps an external write must take effect once, even when the call is retried, or a task must survive a nine-day wait. Then choose the smallest pattern that protects that obligation. Combining every pattern produces ceremony and cost; choosing by fashion leaves the real failure mode exposed. The trade-off in each pattern is therefore as important as the recommended design.

Answer the questions in Figure 16-1 in order to choose the shape of the work; the dashed edge means every shape then takes the checks below it, adding one pattern for each yes.

[[DIAGRAM:pattern-decision-tree|Figure 16-1 — Pattern selection decision tree]]

## Choose among the Part IV patterns

Start from the obligation, then take the smallest row that protects it. The rule behind the table is Chapter 12 § What should be agentic?: give the model only the work whose value is semantic judgment, and keep validation, authorization, and calculation in deterministic code.

| **Pattern (chapter)** | **Obligation it protects** | **Choose it when** | **Do not choose it when** | **What it costs** |
| --- | --- | --- | --- | --- |
| Bounded ReAct (10) | Discovery that stops | The next step depends on the last observation, the eligible tool set is small, and stop conditions are measurable | The path is known, one retrieval suffices, or the step would commit a protected effect | Latency, cost, trajectory variance, and a wider attack surface from observations |
| Routing (11) | The right owner for each request | Candidate paths differ materially in capability, owner, SLO, cost, or risk | A stable deterministic rule is enough, or a misroute is unacceptable | Taxonomy, calibration, drift monitoring, and a fallback |
| Handoff (11) | Accountability that moves explicitly | Responsibility must pass across a specialist, trust, organizational, or channel boundary | The parent still owns the outcome, or needs only independent recovery (a child task) | Ownership transitions, context-transfer risk, and harder cancellation |
| Plan compilation (12) | An executable, validated structure | Heterogeneous, dependency-rich work gains measurably from semantic decomposition | The process is known, short, or risky enough to encode as a workflow | Validation, recovery, and evaluation complexity |
| Reflection and evaluator–optimizer (13) | Quality without self-certification | Measured results show that critique improves a specific quality dimension, and latency permits | Correctness is executable, the first pass meets the bar, or a judge would be the sole authority | Extra model calls, latency, correlated errors, and evaluator calibration |
| Approval and intervention (14) | Human authority and judgment where they matter | Decisions are high-risk, irreversible, regulated, ambiguous, or policy exceptions | The step is low-risk and already automated, or the reviewer would face raw model traces | Dwell time, queues, staffing, and fatigue |
| Durable execution (15) | Work that survives waits, failures, and deployments | Work waits, spans several systems, carries protected effects, or outlives one request | One short idempotent read needs no recovery or coordination | Determinism discipline, history compatibility, and retention and migration obligations |

## How the patterns compose in one run

In a Harborlight evidence review, the durable workflow is the spine (Chapter 15): it admits the run, pins its manifest, and holds every wait, using the steps in Chapter 15 § Canonical control flow. The plan compiler validates and freezes the evidence plan at step 4 (Chapter 12). At step 5, routing selects the evidence specialist from the eligible set (Chapter 11), and bounded ReAct activities gather evidence inside each node (Chapter 10). The request for the second pay statement waits at step 7 for proposal-bound approval, and any escalation from the earlier patterns lands in the intervention queue (Chapter 14). At step 8, an evaluator–optimizer revises the policy explanation while acceptance decides completion (Chapter 13). Each pattern owns one obligation; none of them owns the run.

## The patterns the rest of the book adds

Parts V–VIII add the platform patterns these loops rely on: typed task ownership (Chapter 18), capability envelopes (Chapter 21), effect reconciliation (Chapter 22), causal run traces (Chapter 24), evidence-based release gates (Chapters 25–27), and admission with backpressure (Chapter 28). Appendix A catalogs all twelve platform patterns with the chapter that builds each. The Part IV patterns keep their at-a-glance cards in Chapters 10–15; Appendix A indexes them.

## Where this leads next

Choosing well is easier when failure shapes are visible; Chapter 17 names sixteen of them, says which earlier chapter already prevents each one, and points forward to where Parts V–VIII build the rest.

# 17 — Architecture Patterns That Fail in Production

## Why failure patterns are easier to recognize than design rules

Production failures rarely arrive wearing the name of an anti-pattern. They
look like duplicate writes, missing approvals, unexplained cost, or a run that
cannot be reconstructed. This chapter turns those symptoms into recognizable
system shapes, then connects each shape to the boundary that should replace it
so the diagnosis leads to a design correction rather than another patch.

Anti-patterns are recurring system shapes, not isolated defects. Almost every card below is one mistake wearing different clothes: a probabilistic component was handed a job that belongs to deterministic infrastructure. Repair the failed responsibility boundary rather than the symptom, because fixing the symptom — a better prompt, one more retry, a stricter classifier — leaves the boundary intact and the failure returns under a new name.

Cards are grouped by the boundary they violate rather than by the technology involved, so that two candidates competing for the same fix sit next to each other. Seven cards describe failures that Chapters 1–15 already prevent. Seven more were previewed there, and Parts V–VIII complete their correction. The last two, AP-08 and AP-14, are corrected by mechanisms that only Parts V–VIII build. Each card says where.

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
| AP-06 | Boolean or conversational approval | An approval covers something nobody reviewed | Consent versus bound approval |
| AP-07 | Model says done | Runs close successfully with obligations outstanding | Narration versus acceptance |
| AP-08 | Multi-agent chat as workflow | Agents wait on each other and nobody owns completion | Conversation versus coordination |
| AP-14 | Telemetry without causal or effect lineage | Component metrics improve while outcomes get worse | Monitoring versus attribution |
| AP-15 | Model or provider swap as configuration | Behavior shifts with no code change and no release record | Configuration versus behavior |
| AP-16 | In-place change and test after release | A failing run cannot be reproduced or rolled back exactly | Convenience versus immutability |

### How to read a card

**How this failure starts** states what the team was legitimately trying to achieve — no card here describes carelessness — then names the shape that gets built and the mechanism by which it fails, which is what you need in order to recognize the same failure in an unfamiliar system. **What it looks like in practice** is a concrete instance, drawn from the Harborlight mortgage-evidence scenario where it fits and from another domain where that better shows transfer. **How to replace it** gives the fix and its migration path, and **How to know the repair worked** gives the signals that tell you whether you still have the problem and the honest cost of the correction. **Prevented in / Built in** names the chapter that already prevents the failure, or previews it, and the later chapter that builds its replacement.

The cost sentence in each card matters. Every correction in this catalog costs something — latency, flexibility, or engineering time — and applying all sixteen to a read-only internal assistant would be malpractice. Correct in order of the blast radius of the effects involved. Start with AP-04, AP-05, and AP-06: they produce duplicate payments, duplicate records, and unauthorized effects while looking like ordinary diligence. IDs are stable identifiers; cards are ordered by the boundary they violate.

## Reasoning and control flow

These two failures share a root cause: the model is allowed to decide when to stop. Once stopping is a model decision, termination, budget, and blast radius all become probabilistic properties of a text generator, and no amount of prompt tuning makes them deterministic again. The correction in both cases is to move the stopping decision into code that the model cannot reach.

### AP-01 — Autonomous monolith

[[DIAGRAM:anti-before-after|Figure 17-1 — Autonomous monolith versus governed agentic architecture]]

**How this failure starts.** A prototype that worked convincingly in a notebook is promoted toward production. It mixes reasoning, run state, credentials, tool invocation, retries, approval, and its own completion signal in a single process, because nothing in the prototype phase forced those concerns apart. The tempting shortcut is “One unconstrained agent owns end-to-end control. The loop decides what to do, does it, and then declares the outcome.” It breaks down because probabilistic behavior becomes the control logic. There is no boundary at which a failure can be isolated, so a flawed reasoning step and a failed database write are indistinguishable from outside the process. Run state lives in memory, so a restart loses work that has already had external effects. Nothing can be replayed, because nothing durable was recorded — the transcript is a narrative, not a ledger.

**What it looks like in practice.** Mortgage evidence review restarts after a routine deploy and sends the same document request twice, because the only record of the first request was the agent's conversation history.

**How to replace it.** A bounded runtime inside a durable workflow, with policy, tool and effect, and acceptance services each owning their decision. Migrate in steps: Monolith → direct tools → "done" becomes workflow → semantic nodes → governed effects → acceptance.

**How to know the repair worked.** Track protected calls that bypass the gateway, work lost per restart, false-completion rate, and the number of distinct responsibilities living in one process. The cost: decomposition adds interfaces, deployment surface, and latency. Decompose around the highest-risk effects first; a read-only assistant does not need the full split.

**Prevented in / Built in.** Prevented in Chapters 1, 3, and 15.

### AP-11 — Unbounded loops and recursive delegation

**How this failure starts.** Work varies in complexity, and a fixed step count either truncates hard cases or wastes budget on easy ones, so the team lets the agent iterate and delegate as needed. The tempting shortcut is “Agents iterate and spawn children with per-call limits but no global ceiling. Each individual decision looks reasonable.” It breaks down because local limits do not compose. A depth limit of five with a fan-out of five is 3,125 leaf tasks, and each child inherits a fresh budget rather than a share of the parent's. Delegation graphs become cyclic when two specialists can each call the other, and no participant can detect the cycle from inside it. Queue saturation then degrades unrelated tenants, which is how one runaway research task becomes a platform incident.

**What it looks like in practice.** A research supervisor spawns fact-checkers that themselves spawn fact-checkers; the run consumes a day of tenant quota before a human notices, and every individual agent behaved exactly as instructed.

**How to replace it.** Global budgets that decrease monotonically across delegation, an acyclic ownership graph, and explicit depth, fan-out, and no-progress limits enforced by the runtime rather than by instructions. Migrate in steps: Recursion becomes a runtime-governed task graph.

[[EXAMPLE:ap-delegation-budget]]

**How to know the repair worked.** Track delegation depth and fan-out distributions, repeated state signatures, no-progress step count, and budget-exhaustion rate by tenant. The cost: caps truncate genuinely hard work. Set them from observed distributions rather than intuition, and make exhaustion a visible, escalatable terminal rather than a silent stop.

**Prevented in / Built in.** Previewed in Chapter 10; built in Chapters 18 and 28.

## Context, knowledge and memory

Everything an agent believes arrives through one of these three channels, and all three fail the same way: a convenient representation is mistaken for an authoritative one. A transcript is convenient. A similarity hit is convenient. A remembered fact is convenient. None of them is a system of record, and treating any of them as one moves business truth into a store with no owner, no schema, and no audit.

### AP-02 — Prompt as database

**How this failure starts.** Business state has to survive across turns, restarts, and handoffs, and the conversation already contains it. The tempting shortcut is “Chat history, or a rolling summary of it, is treated as the authoritative record of what has happened.” It breaks down because every mechanism that keeps a context window viable is lossy. Truncation drops the oldest facts, which are often the decisions; summarization paraphrases, and a paraphrase of "legal approved with conditions" is not a legal approval. There is no concurrency control, so two turns that both update a value silently diverge. There is no schema, so nothing detects that a field went missing. And there is no audit trail an investigator can read.

**What it looks like in practice.** A contract renewal forgets that legal approved with conditions, because the approval was three summarization rounds ago and the summary kept the outcome but dropped the conditions.

**How to replace it.** Canonical typed state in a service that owns it, with the prompt receiving a projection built fresh from that state on every step. Migrate in steps: Transcript-as-state becomes State Service → snapshot → prompt.

[[EXAMPLE:ap-state-projection]]

**How to know the repair worked.** Track facts lost across compaction boundaries, disagreement between summary and store, and state mismatches discovered on recovery. The cost: typed state requires schema design and migration discipline. It lands early and visibly, which is precisely why it gets deferred.

**Prevented in / Built in.** Prevented in Chapters 6 and 15.

### AP-09 — Vector store as source of truth

**How this failure starts.** Relevant knowledge has to be found across a corpus too large to pass into a prompt. The tempting shortcut is “A similarity hit is treated as a current, authorized, authoritative fact.” It breaks down because similarity measures resemblance, not currency, authority, or permission. An index contains what was ingested, including superseded policies, duplicated drafts, documents the caller may not read, and anything an attacker managed to insert. Nothing in a cosine score distinguishes the approved policy from its withdrawn predecessor, and a confident citation of the wrong document is more damaging than no citation at all.

**What it looks like in practice.** An obsolete policy chunk applies a superseded spending limit, and the answer cites the document by name, which is what makes the reviewer believe it.

**How to replace it.** Governed sources and snapshots hold authority, and the snapshot is a pinned knowledge release (Chapter 5); the index is a derived locator whose hits are verified for ACL, freshness, and supersession before the content reaches the model. Migrate in steps: Vector hit → action becomes source + ACL + snapshot → evidence → decision.

**How to know the repair worked.** Track evidence age at decision time, source disagreement rate, ACL mismatches at retrieval, and citations pointing at superseded revisions. The cost: authoritative lookup adds latency to every retrieval. Apply it in proportion to what the answer will be used for; drafting assistance and payment authorization do not need the same guarantee.

**Prevented in / Built in.** Prevented in Chapter 5.

### AP-13 — Memory write by default

**How this failure starts.** Personalization is genuinely valuable, and the cheapest way to get it is to remember everything. The tempting shortcut is “Every interaction, or a summary of it, becomes a durable memory record.” It breaks down because writing by default means writing without provenance, purpose, or verification. Secrets get persisted. Model errors get persisted and then retrieved as established fact, which is how one hallucination becomes a standing belief. Injected instructions from a document become durable instructions. And because nothing recorded why a memory was written, nothing can decide when it should expire or who may delete it — which turns a retention obligation into an archaeology project.

**What it looks like in practice.** A malicious mortgage document is processed, and the bank account it contains is stored as an applicant fact. Every subsequent run retrieves it as if it were verified evidence for the mortgage case.

**How to replace it.** Memory writes are candidates, not side effects: purpose-bound, carrying provenance, verified before promotion, scoped to a tenant and subject, with a TTL and a deletion path. Migrate in steps: Transcript → memory becomes candidate → gate → typed record.

[[EXAMPLE:ap-memory-gate]]

**How to know the repair worked.** Track sensitive-data writes caught by DLP, retrieval of stale records, correction and deletion rates, and incidents traceable to a single memory record. The cost: a strict write path reduces the perceived magic of personalization and requires someone to own purpose definitions. The alternative is an unowned database of unverified claims about your customers.

**Prevented in / Built in.** Prevented in Chapter 6.

## Security and delegated authority

The three cards here are the difference between *can* and *may*. An agent that can reach a resource, can see a tool, or can produce a plausible safety score has demonstrated capability, not permission. Each card is a case where capability was allowed to stand in for a policy decision, and in each the correction is the same: make the authorization decision explicitly, in code, at the moment of use.

[[DIAGRAM:anti-ambient-authority|Figure 17-2 — Ambient authority versus a narrowed capability envelope and a short-lived credential lease]]

### AP-03 — Ambient authority

**How this failure starts.** Agents need access to enterprise systems, and provisioning narrow credentials for every task and tenant is laborious. The tempting shortcut is “Workers receive broad, long-lived, reusable credentials — often a service account that predates the agent and was already over-scoped.” It breaks down because the credential's scope, not the task's need, defines the blast radius. Any compromise — prompt injection, a malicious tool, a leaked log — yields durable authority over everything the credential can reach. Because the same credential serves every run, nothing in the audit trail distinguishes which subject's work caused which effect, so attribution fails exactly when it is needed. And a credential that never expires cannot be revoked faster than someone notices.

**What it looks like in practice.** The mortgage evidence agent runs under a service account that can export every applicant record; the evidence-review task needs one case. The account was reused because it already existed.

**How to replace it.** Preserve both subject and workload identity, derive a capability envelope by intersection, and mint a short-lived, audience-bound credential lease at the moment of use. Migrate in steps: Broad token becomes policy → capability envelope → credential lease → enforcement at the resource.

**How to know the repair worked.** Track credential scope and age distributions, granted-but-unused privilege, scope-expansion attempts, and cross-tenant access denials. The cost: fine-grained policy adds design effort and a policy-decision hop per call. The hop is cacheable; the design effort is not, and it is the part teams underestimate.

**Prevented in / Built in.** Previewed in Chapters 1 and 3; built in Chapter 21.

### AP-10 — LLM judge as security gate

**How this failure starts.** Some content is genuinely ambiguous, and a model is better than a regular expression at recognizing nuance. The tempting shortcut is “A model-produced score alone authorizes a protected action — if risk_score < 0.3: execute().” It breaks down because a judge is an injectable, nondeterministic component being asked to make a binding decision. The same input can score differently across runs, so the gate is not reproducible and an incident cannot be explained. The content being judged can address the judge directly, which makes the attacker a participant in their own authorization. And judge behavior drifts with model updates, silently moving the threshold without any release event.

**What it looks like in practice.** The judge classifies an unusually large payment as low risk because the request text explains, persuasively, why it is routine.

**How to replace it.** A deterministic policy and invariant gate makes the decision. The judge triages, prioritizes, and supplies evidence for a human — it never holds the authorization. Migrate in steps: score < threshold → execute becomes policy → optional judge → human escalation.

**How to know the repair worked.** Track disagreement rate across repeated runs of identical input, gate bypass attempts, false negatives found downstream, and human override frequency. The cost: deterministic rules genuinely cannot express every nuance, and some legitimate work will be escalated unnecessarily. That is the correct direction to fail.

**Prevented in / Built in.** Prevented in Chapter 13; Chapter 20 develops it for security detectors.

### AP-12 — Ungated tool discovery and catalog dumping

**How this failure starts.** A mature platform has many tools, and the agent cannot use what it cannot see. The tempting shortcut is “Every discovered tool and its full schema is placed into the prompt, often straight from an MCP server's advertised catalog.” It breaks down because discovery is being used as authorization. Selection gets harder as the catalog grows, because the model is choosing among near-neighbours it has no basis to distinguish. Schemas consume context that evidence should occupy. Worse, tool descriptions are untrusted text from a third party, so a malicious server can write a description engineered to attract calls — the agent is reading attacker-controlled instructions and treating them as a menu.

**What it looks like in practice.** A reporting agent discovers an administrative delete tool, because the catalog was filtered by connectivity rather than by the caller's authority.

**How to replace it.** Registry → eligibility and policy evaluation → task-specific shortlist → schema validation at call time. Eligibility is computed from the subject, purpose, tenant, and risk class, never from what the server happens to advertise. Migrate in steps: Full MCP catalog becomes an approved tool slice bound to the run's capability envelope.

**How to know the repair worked.** Track tools exposed versus eligible versus actually used, selection-confusion rate, schema token overhead per run, and unauthorized discovery attempts. The cost: a narrow shortlist will sometimes omit a tool that would have helped. Make the omission observable so the shortlist can be improved deliberately, rather than widening it by default.

**Prevented in / Built in.** Previewed in Chapter 8; built in Chapters 19 and 22.

## Effects, retries and recovery

These two cards are among the most expensive in the catalog, because they produce duplicate real-world effects — duplicate mortgage-document requests, duplicate payments, or duplicate emails to customers. Both stem from confusing the transport layer with the effect layer: a failed call is not a failed effect, and an unacknowledged call is not an absent one.

[[DIAGRAM:anti-retry-storm|Figure 17-3 — Layered retries and timeout-as-failure versus one retry owner with an unknown-effect terminal]]

### AP-04 — Retry everywhere

**How this failure starts.** Transient failures are real and common, and every layer in the stack offers a retry setting that looks like diligence. The tempting shortcut is “The SDK, the gateway, the workflow engine, the connector, and the tool each retry independently.” It breaks down because retries compose multiplicatively, not additively. Three layers at 3, 3, and 2 attempts produce eighteen calls for one logical operation, and each layer believes it made a modest choice. The amplification arrives precisely when a dependency is already degraded, converting a slow dependency into an outage. If any layer retries a non-idempotent call, the duplicates are permanent.

**What it looks like in practice.** A single mortgage evidence review produces eighteen calls to the payroll provider that verifies the second pay statement, and the provider rate-limits the lender for the rest of the day.

**How to replace it.** One retry owner per failure class, with a shared attempt and deadline budget that every layer reads and no layer resets. Migrate in steps: Nested retries become classified failure → one schedule → terminal.

[[EXAMPLE:ap-retry-owner]]

**How to know the repair worked.** Track attempts per logical operation, amplification factor against dependencies, duplicate effect keys, and deadline overruns caused by retry time. The cost: a single central policy is necessarily more conservative than a hand-tuned one per call site. Express the variation as failure classes rather than as per-layer settings.

**Prevented in / Built in.** Previewed in Chapter 3; built in Chapter 22.

### AP-05 — Timeout means failure

**How this failure starts.** A response is lost after a request was dispatched, and the run has to decide what to do next. The tempting shortcut is “The call is marked failed and retried immediately.” It breaks down because a timeout describes the response, not the effect. The first call may have committed, may be committing, or may never have arrived, and the caller cannot distinguish these from the outside. Treating that state as failure asserts knowledge the system does not have, and the retry then creates the duplicate that the timeout only made possible.

**What it looks like in practice.** The mortgage document request is recorded twice: the first call committed just after the client gave up waiting.

**How to replace it.** An explicit Unknown effect state that blocks retry until reconciliation settles it against the downstream system of record. Only proven absence permits a retry, and the retry reuses the same key; a request still executing stays Unknown, and an outcome that cannot be proven goes to InterventionRequired. Migrate in steps: timeout → failed → retry becomes timeout → Unknown → lookup → decide.

[[EXAMPLE:ap-unknown-effect]]

**How to know the repair worked.** Track count and age of unresolved unknown effects, duplicate idempotency keys observed downstream, and conflicts discovered after a timeout. The cost: unknown effects delay completion and need somewhere to go when reconciliation cannot resolve them. That queue is the price of not creating duplicate financial records.

**Prevented in / Built in.** Previewed in Chapters 1, 3, and 15; built in Chapter 22.

## Approval and acceptance

Both cards here concern the moment a system decides that something is allowed, or that something is finished. In each, a cheap signal — a Boolean, a sentence of model output — was allowed to carry a decision that the enterprise will later be asked to defend. The correction is to make the decision an artifact: something with a hash, an owner, an expiry, and an independent check.

[[DIAGRAM:anti-approval-binding|Figure 17-4 — Boolean consent versus proposal-bound, expiring approval]]

### AP-06 — Boolean or conversational approval

**How this failure starts.** Humans must approve protected actions, and a chat interface makes approval feel natural. The tempting shortcut is “A Boolean flag or a chat message — "yes, go ahead" — approves whatever the arguments happen to be at execution time.” It breaks down because approval is being bound to a conversation rather than to an effect. Between consent and commit, the amount, the recipient, the policy version, the acting workload, or the underlying record can all change, and nothing detects it. The approver reviewed a description; the system executes a payload. A Boolean also cannot express scope or expiry, so a single "yes" silently approves later, larger, and unrelated actions.

**What it looks like in practice.** An approval given to submit the evidence package for case version 3 is reused after the case moved to version 5 and the package gained a document nobody reviewed.

**How to replace it.** An immutable proposal, hashed over the exact effect, with an ApprovalDecision bound to that hash, scoped to one action, and carrying an expiry. Revalidate policy and resource version immediately before commit, and key the commit by the logical effect, not by the proposal hash. Migrate in steps: approved=true becomes proposal hash → ApprovalDecision → revalidate → commit.

[[EXAMPLE:ap-bound-approval]]

**How to know the repair worked.** Track proposal-hash mismatches at commit, approval reuse attempts, expiry rate, and incidents occurring after a recorded decision. The cost: benign changes force reapproval, which reviewers experience as friction. Tune by making the diff visible — showing what changed is cheaper than widening the approval.

**Prevented in / Built in.** Prevented in Chapter 14.

### AP-07 — Model says done

**How this failure starts.** A run needs a completion signal, and the model produces a confident, well-formed one for free. The tempting shortcut is “The model's assertion sets the run to success.” It breaks down because the model is reporting on its own work using the same faculty that produced it. A missing evidence artifact, a skipped approval, an uncommitted effect, or an unmet obligation all present as success, because none of them changes what the model believes it did. Failures therefore surface downstream — in reconciliation, in audit, or in a customer complaint — long after the trace has aged out.

**What it looks like in practice.** The evidence review reports complete while the second pay statement's verification is stale, because the model saw a verification result in context and did not evaluate its freshness.

**How to replace it.** An independent, executable acceptance check over authoritative state returns an AcceptanceDecision—accepted, rejected with typed defects, or escalated (Chapter 13); only an accepted decision lets the run reach Succeeded (Chapter 15). While an effect is Unknown or required input is missing, acceptance is not attempted. The model may propose completion; it may not declare it. Migrate in steps: Model text → success becomes acceptance engine → AcceptanceDecision → run state.

**How to know the repair worked.** Track false-completion rate found by audit, reopen rate, and runs closed with missing artifacts or uncommitted effects. The cost: executable acceptance criteria need domain ownership and maintenance. Without them the completion signal has no author, which is worse and merely less visible.

**Prevented in / Built in.** Prevented in Chapters 2, 13, and 15.

## Multi-agent collaboration

### AP-08 — Multi-agent chat as workflow

**How this failure starts.** Specialists need to coordinate, and a shared conversation is the fastest coordination mechanism to build. The tempting shortcut is “Free-form messages between agents own state, work assignment, deadlines, and completion.” It breaks down because a conversation has no notion of ownership, so two agents can both believe the other is acting — or both act. It has no join semantics, so nothing knows when parallel work has finished. Cancellation cannot propagate, because there is no structure to propagate through, and artifacts produced mid-conversation are lost when the window compacts. The system behaves like a meeting with no chair and no minutes.

**What it looks like in practice.** The income-verification and policy specialists each wait for the other's artifact. The run sits open for three days and neither agent is wrong.

**How to replace it.** A typed TaskEnvelope with exactly one accountable owner, explicit child tasks, artifacts stored by reference, and a deterministic join evaluated by the coordinator rather than inferred from messages. Migrate in steps: Chat mesh becomes supervisor workflow plus task service.

**How to know the repair worked.** Track orphaned tasks, conflicting concurrent effects, delegation depth, join wait age, and effects landing after a run was considered complete. The cost: formal task envelopes reduce the fluidity that makes agent conversations appealing to demonstrate. The fluidity is what fails in production.

**Prevented in / Built in.** Built in Chapter 18.

## Observability and evidence

### AP-14 — Telemetry without causal or effect lineage

**How this failure starts.** Teams instrument what they own, and each component's dashboard looks healthy. The tempting shortcut is “Logs, metrics, and traces cannot be joined to versions, policy decisions, effects, acceptance, or business outcome.” It breaks down because without a join key, every measurement is local. A component can improve on its own metric while degrading the outcome, and nothing in the telemetry can express the relationship. Cost cannot be attributed to a tenant, a release, or a decision, so optimization targets whatever is easiest to measure. When an incident happens, the investigation has to reconstruct causality by hand from timestamps.

**What it looks like in practice.** A retrieval cache raises its hit rate and cuts latency, while stale-evidence rejections at acceptance double. Both facts are true and neither dashboard contains both.

**How to replace it.** One causal run trace joining release version, context manifest, model and policy decisions, tool effects, acceptance decision, business outcome, and cost. Migrate in steps: Separate dashboards become one correlated trace.

**How to know the repair worked.** Track percentage of runs joinable to a business outcome, spans missing parent or version identifiers, and unattributed spend. The cost: correlation requires disciplined identifier propagation across every component and raises the governance burden on telemetry, including redaction. Retrofitting it after an incident costs considerably more.

**Prevented in / Built in.** Built in Chapter 24.

## Platform, release and operations

Both cards describe the same instinct — change should be fast — applied where it removes the ability to explain, reproduce, or undo what happened. Speed is not the problem; unversioned speed is.

### AP-15 — Model or provider swap as configuration

**How this failure starts.** Teams want better cost or quality, and the routing layer makes the change a one-line edit. The tempting shortcut is “A model alias is repointed without behavioral validation, because no application code changed.” It breaks down because the model is the behavior. Tool-calling reliability, schema adherence, refusal boundaries, safety posture, latency distribution, and cost per task all shift together, and they shift unevenly across slices — a change that is neutral in aggregate can be severe for one language, one document type, or one tenant. Because no release event was recorded, the resulting regression has no obvious cause and cannot be rolled back precisely.

**What it looks like in practice.** A cheaper model drops tool arguments for one language only. Aggregate evaluation stays green; that market's completion rate halves.

**How to replace it.** A versioned ChangeBundle (the versioned change proposal that Chapter 25 evaluates and Chapter 27 promotes) carrying evaluation across slices, security testing, load testing, canary exposure, and a named rollback target. Migrate in steps: Edit alias becomes immutable route policy → replay → approval → canary.

**How to know the repair worked.** Track schema and tool-call regression rate, refusal-rate shift, per-slice quality drift, and fallback-route activation. The cost: validation slows experimentation, so make the fast path cheap: pre-built replay sets and automated slice reports, rather than an approval meeting.

**Prevented in / Built in.** Previewed in Chapters 3 and 7; built in Chapters 25 and 27.

### AP-16 — In-place change and test after release

**How this failure starts.** A production issue needs a fix now, and the console offers an edit box. The tempting shortcut is “Prompts, Skills, tool definitions, policy, and routes are mutated directly in production.” It breaks down because a run can no longer be reproduced, because the artifacts it used no longer exist in the form it used them. Attribution fails, since two runs a minute apart may have used different behavior with no record of the boundary. Rollback becomes guesswork about what the previous state was. And the edit itself is untested by construction — the test is the production traffic.

**What it looks like in practice.** A prompt edit intended to reduce verbosity increases data leakage. Neither the previous prompt nor the exact leak conditions can be reconstructed.

**How to replace it.** Immutable artifacts, a ReleaseManifest that pins everything a run resolves, pre-promotion tests, signed promotion, canary exposure, and a rollback target that is verified rather than assumed. Migrate in steps: Mutable console becomes build → validate → approve → promote → monitor.

**How to know the repair worked.** Track runs executing unversioned artifacts, out-of-band edit events, and rollback rehearsal failures. The cost: immutability needs genuinely good tooling, or people will route around it under pressure. If the emergency path is slower than the console, the console wins — so make the fast path immutable rather than making immutability optional.

**Prevented in / Built in.** Previewed in Chapters 7 and 8; built in Chapter 27.

## Where this leads next

Several of these failures are corrected by mechanisms the rest of the book builds. Chapter 18 starts with AP-08 and AP-11: how specialists can share work with one owner per task, narrowed authority, explicit joins, and a bounded task tree.
