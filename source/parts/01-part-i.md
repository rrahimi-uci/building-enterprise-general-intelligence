# PART I — FOUNDATIONS

This Part defines the vocabulary and invariants used everywhere else. It begins with the progression from model call to production system, then turns model outputs into typed tool proposals, and finally places bounded reasoning behind a framework-neutral runtime contract. Read it before selecting orchestration patterns or products.

# 01 — From an LLM Call to a Production System

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Northstar Components wants to shorten supplier onboarding from twelve days to two. A prototype can summarize a supplier file, but production must also retrieve authorized records, request missing evidence, pause for people, screen sanctions, create auditable decisions, and survive days of inactivity. |

|  |
| --- |
| **DESIGN DECISION**  Start Northstar as a governed distributed application with one bounded reasoning component, not as an autonomous chatbot. |

## What this chapter delivers

Explain why an agentic application is a distributed system and assign every authoritative decision to the correct component.

## Solution blueprint


Figure 1. From an LLM Call to a Production System.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Run Service and durable workflow | User/edge, content/model, model/tool | run · tenant · regional cell | one run and one cell | RunManifest · AgentStep · Artifact |

## The progression: model, tool, agent, system

A language model maps input tokens to output tokens. A tool-using model can propose structured interaction with the environment. An agent chooses among steps using observations. An **enterprise agentic system** adds everything needed to make those choices safe and operational: durable state, identity, authorization, bounded resources, external-effect semantics, evidence, human control, deployment compatibility, evaluation, and incident recovery.

This distinction prevents a common category error. Better prompting can improve a reasoning step; it cannot provide transactional integrity, credential isolation, deterministic replay, tenant boundaries, or a provable audit trail. Those are properties of the surrounding system.

| **Uncertainty** | **Appropriate mechanism** | **Authoritative owner** |
| --- | --- | --- |
| Meaning of an ambiguous request | Model or classifier | Bounded agent step |
| Which known path applies | Router plus deterministic validation | Route service / workflow |
| Unknown task decomposition | Planner plus plan compiler | Plan service / workflow |
| Current business state | Database read through governed service | Domain system of record |
| Permission to act | RBAC/ABAC and delegated capability | Policy engine |
| Whether a write committed | Effect receipt or reconciliation | Effect ledger + downstream system |
| Whether the run is complete | Executable acceptance criteria | Workflow / acceptance engine |

### The Northstar domain thread

Throughout this book, Northstar builds a supplier-onboarding platform. The evolving system retrieves candidate records, validates documents, screens sanctions, requests corrections, coordinates specialists, waits for human decisions, creates supplier records, and preserves evidence. The use case is deliberately inconvenient: it crosses data boundaries, lasts days, includes ambiguous reasoning, performs protected writes, and requires audit. That makes it useful for testing whether an architecture is real.

### Anti-pattern — the autonomous monolith

A single process receives a prompt, holds a broad user token, queries databases, calls arbitrary APIs, stores memory, retries writes, and declares completion. It is easy to demonstrate and nearly impossible to operate safely. A production decomposition does not remove intelligence; it gives intelligence explicit contracts and failure boundaries.

## The production problem

An enterprise agent must translate an ambiguous goal into actions across systems that have strict identity, consistency, availability, privacy, cost, and compliance requirements. The LLM is nondeterministic; the environment is concurrent and partially failing; inputs may be adversarial; and many actions are irreversible. Production design therefore has to answer three questions for every step:

1. **May this principal perform this action on this resource now?**
2. **Can this step be retried, resumed, canceled, or compensated safely?**
3. **Can an operator later reconstruct what happened, why, under which versions and permissions?**

### Core problem matrix

| **Architectural problem** | **Why ordinary prototypes fail** | **Required production stance** |
| --- | --- | --- |
| Probabilistic control | A plausible model output is mistaken for a valid transition | Model proposes; deterministic code validates and commits |
| Long-lived execution | Process memory, chat history, and cron jobs lose progress or duplicate work | Durable state machine with event history, timers, signals, and checkpoints |
| Delegated authority | Shared service credentials turn an assistant into a privilege-escalation path | User + workload identity, token exchange, downscoping, audience binding |
| Untrusted context | Retrieved instructions can redirect the agent or exfiltrate data | Provenance labels, content/instruction separation, egress controls, approvals |
| Tool side effects | Retries repeat payments, emails, writes, or deployments | Idempotency key + effect ledger + preconditions + compensation |
| Multi-agent coordination | Conversational delegation obscures ownership and creates loops | Typed task contract, single owner, bounded fan-out, budgets, terminal states |
| Memory and knowledge | Embeddings become an ungoverned shadow database | Separate stores, explicit write policy, ACL filtering, retention, provenance |
| Model and vendor drift | Behavior changes without application code changing | Versioned model routes, eval gates, canaries, rollback, trace comparison |
| Operability | Logs show text but not causal execution | Distributed traces, structured events, replay, cost and policy telemetry |
| Compliance | Decisions cannot be reproduced or explained | Immutable audit package, evidence chain, approvals, retention and legal holds |

## The system in one view

Everything the rest of this book builds is one picture. Read it once now, before
any of it is justified, so that each Part has somewhere to land.

[[DIAGRAM:system-overview|Figure 1-2 — The whole system, and the Part that details each band]]

The Roman numerals are the reading map. Each band is one Part's subject, and the
book descends through them in order: the shape first, then the layers, then the
implementation inside each layer.

| Band | What it owns | Detailed in |
| --- | --- | --- |
| Channels | The request, the reviewer, and the returned result | Part I |
| Agent runtime | Bounded reasoning, loop patterns, durable run state | Parts I and IV |
| Collaboration | Specialist agents, peer agents, external protocols | Part V |
| Knowledge | Governed knowledge, rules, catalogs, per-run context | Part II |
| Control points | Which model may answer, and which effect may commit | Part V |
| Security | Identity, guardrails, approvals, containment | Part VI |
| Systems of record | Where effects actually commit and stay true | Throughout |
| Evidence | Traces, evaluation, and the loop into the next release | Part VII |
| Platform and operations | The paved road that builds, releases and runs it | Parts III and VIII |

Two properties of this picture matter more than any component in it. Authority
narrows downward: the agent proposes, the platform authorizes, and only the
bottom bands commit anything. And security is not a band you pass through once —
it spans every one of them, which is why it gets a Part of its own rather than a
box in a diagram.

## Four control points, four different questions

The architecture has several gateways, and they are routinely confused because
the word is the same. They are not alternatives, and none replaces another.

[[DIAGRAM:gateway-roles|Figure 1-3 — The control points, and the question each one answers]]

| Control point | The question it answers | What it does not decide |
| --- | --- | --- |
| API Gateway | Is this caller admitted to the platform at all? | Anything about agents or models |
| LLM Gateway | Which model may answer, under which data policy? | Whether an effect may happen |
| Tool Gateway | May this effect happen, for this subject, exactly once? | Which model produced the proposal |
| MCP Gateway | Is this external server and tool trusted and eligible? | Whether the resulting effect is authorized |

The **Tool Gateway** is the enterprise's control point for *effects*. It validates
the tool version and schema, re-authorizes the action and resource against the
caller's grant, mints a last-hop credential, enforces idempotency, and records
the receipt. It is deliberately protocol-agnostic, because effects arrive over
REST, gRPC, a database transaction, a queue, and MCP, and the control must be
the same for all of them.

The **MCP Gateway** terminates one protocol. It decides whether an external MCP
server is trusted, which of its tools are eligible, and what scoped credentials
it may use. That is a real and necessary job, and it is a different job.

|  |
| --- |
| **ARCHITECTURE GUIDANCE**  Do not rename the Tool Gateway after a protocol. A tool invoked over MCP still passes the Tool Gateway, because MCP describes how a tool is discovered and called — not who may call it, whether the effect is idempotent, or what evidence is recorded. Naming a control boundary after today's protocol is how the boundary disappears when the protocol is replaced. |


## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Grounding boundary | Separate model capability from system correctness. A benchmark or demo does not establish authorization, durability, privacy, or business acceptance. Every material output should carry evidence references and uncertainty. | NIST-GAI; REACT |

Evidence anchors: NIST-GAI; REACT. Full URLs, authority, version, and scope appear in Appendix K.

## Implementation reference


### Provider-neutral agent-step contracts

[[EXAMPLE:contracts#step]]

## Debugging playbook

1. Trace one request across model, workflow, tool, human, and record owners.
2. Find any place where prompt text is being treated as authoritative state.
3. Reproduce one partial failure and identify the missing durable fact.

## Production checklist

**✓** The model is a bounded reasoning component—not the owner of workflow state.

**✓** Identity, policy, state, effects, approvals, and acceptance each have an authoritative owner.

**✓** Autonomy is bounded independently across tools, data, time, cost, delegation, and publication.

**✓** Consequential effects are authorized, deduplicated, verified, and recoverable.

**✓** Operators can reconstruct the run from versions, evidence, decisions, and receipts.

## Exercises

1. Draw the minimum production architecture for Northstar and label every authoritative store.
2. Convert a chatbot feature list into measurable outcome, authority, duration, data, and effect requirements.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| What distinguishes an enterprise agentic system from a chatbot or an LLM-enabled workflow? | Model-directed step selection plus durable state, governed capabilities, bounded autonomy, recovery, and evidence; a chat interface alone is not an agent. |
| Why should an agent be treated as a distributed system? | Model, workflow, queues, tools, humans, and external systems fail independently; duplicate delivery, waits, concurrency, and uncertain effects must be explicit. |
| How would you choose an autonomy level for a new use case? | Start with measurable value and risk; decompose autonomy; grant the minimum tools, data, time, spend, delegation, and effect authority needed. |
| Which records must remain authoritative outside the model and prompt? | Run and workflow state, identity, policy decisions, budgets, approvals, business records, effect receipts, release versions, and audit evidence. |
| What would you require before calling an agent production-ready? | Evaluated outcomes and trajectories, bounded limits, delegated authorization, idempotent effects, recovery paths, observability, audit, release pinning, and operational controls. |

## Transition to Chapter 2

With the system boundary established, Chapter 2 converts model intent into typed, validated tool proposals and a deterministic commit path.

# 02 — Tools, Structured Outputs, and the Deterministic Shell

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  The prototype now proposes a call to create a supplier record. The JSON is valid and the rationale sounds convincing, yet the record may be stale, the user may lack write authority, and a retry could create a duplicate. Northstar introduces a deterministic shell around every model proposal. |

|  |
| --- |
| **DESIGN DECISION**  Treat every model output as a typed proposal; validate, authorize, commit, verify, and accept outside the model. |

## What this chapter delivers

Turn model output into typed proposals and place validation, authorization, effects, and acceptance behind deterministic boundaries.

## Solution blueprint


Figure 2. Tools, Structured Outputs, and the Deterministic Shell.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Tool Gateway and domain service | model proposal to authorized capability | tool class · connector · downstream limit | one logical effect | ToolManifest · ToolIntent · EffectRecord |

## Structured output is a protocol boundary

Structured output is valuable because it makes a model decision parseable, versionable, and testable. It is not proof. A valid ToolIntent can still reference an ineligible tool, exceed delegated authority, target stale state, omit required evidence, or propose a duplicate mutation. The platform therefore follows **propose → validate → authorize → commit → verify → accept**.

A useful proposal is small. It names one disposition, one tool or delegation target, canonical arguments, evidence references, uncertainty, and the expected resource version. It does not carry credentials, policy truth, or an instruction to bypass a failing control.

### Deterministic acceptance

Acceptance is not the model saying “done.” Northstar declares supplier onboarding complete only when required evidence artifacts exist, every screening result is fresh, approvals cover the exact proposal, all protected effects are committed with receipts, no unknown effect remains, and the supplier record satisfies domain invariants.

### Scaling the shell

Scale tool work by workload and risk class, not with one global queue. Read-only retrieval can use high concurrency. Browser sessions, code sandboxes, high-risk writes, and human approvals need independent quotas and backpressure. The Tool Gateway is stateless where possible; manifests, policy, effect records, and receipts live in durable stores. Downstream concurrency limits, not model throughput, usually determine safe capacity.

## Design principles

1. **Deterministic shell, agentic core.** Put LLM reasoning inside typed activities; keep authorization, state transitions, budgets, validation, approvals, and side-effect commits in code.
2. **Least agency.** Grant the minimum autonomy, tools, data, time, tokens, fan-out, and mutation scope needed for the task.
3. **One run, one accountable owner.** A run may delegate, but exactly one coordinator owns completion, user communication, cancellation, and result aggregation.
4. **State outside the prompt.** Prompts are projections of durable state, not the database. Reconstruct context from authoritative stores on each step.
5. **Capability by contract.** Every agent and tool publishes a typed, versioned manifest; discovery never implies authorization.
6. **Policy at every boundary.** Evaluate authorization at ingress, retrieval, delegation, tool execution, data egress, memory write, and artifact publication.
7. **At-least-once by default.** Assume retries and duplicates. Require idempotency or compensation before a mutating capability can be certified.
8. **Evidence before autonomy.** Autonomy level rises only after offline evals, sandbox simulation, adversarial testing, canary evidence, and stable SLOs.
9. **Bounded recursion.** Cap steps, wall-clock time, spend, tokens, tool calls, delegation depth, parallel branches, and repeated failures.
10. **Open telemetry and portable state.** Use standard trace/event envelopes and keep the authoritative run record outside a proprietary agent runtime.

|  |
| --- |
| **BEST PRACTICE**  Validate, authorize, and commit outside the model. A structured output is a *proposal*: parse it against a schema you own, check authority against the caller's grant, then commit through the same service path a human request would take. If a tool can be invoked without passing that gate, the gate is decorative. |

## Where distributed systems must remain authoritative

| **Traditional concept** | **What it should own** | **Appropriate LLM role** | **If replaced by the LLM** |
| --- | --- | --- | --- |
| State machine | Legal run states and transitions | Suggest next intent or plan node | Invalid/unreproducible transitions |
| Durable workflow | Checkpoints, retries, waits, signals, child lifecycles, cancellation | Execute bounded reasoning activities | Lost work and duplicate effects |
| Queue | Load leveling, delivery, prioritization, consumer scaling | Estimate task type/priority within policy | Unbounded fan-out and overload |
| Event sourcing/history | Ordered causal record and replay position | Summarize history for context | Narrative replaces evidence |
| Transaction/outbox/inbox | Atomic state/event publication and deduplication | Propose business change | Split-brain business state |
| Idempotency/effect ledger | One logical effect and reconciliation | Generate or interpret user intent | Duplicate payments/messages/writes |
| Schema and type system | Interface validity and compatibility | Populate structured fields | Silent semantic drift |
| Policy engine | Authorization, obligations, deny rules | Explain decision or request missing facts | Prompt-driven privilege escalation |
| Scheduler/timer | Precise durable wakeups and deadlines | Choose a policy-allowed schedule | Missed/duplicated jobs |
| Lock/lease/concurrency control | Mutual exclusion where unavoidable; ownership leases | Choose work candidate | Concurrent corruption or deadlock |
| Circuit breaker/rate limiter | Protect dependencies and enforce fairness | Select evaluated fallback | Retry storms and quota collapse |
| Database/search engine | Authoritative records and indexed retrieval | Natural-language query planning/synthesis | Hallucinated or stale state |
| Cryptography/KMS/secret broker | Keys, signatures, token issuance, rotation | None beyond requesting approved capability | Secret exposure and forged identity |
| Tests/rules engine | Deterministic invariants and objective acceptance | Generate candidates and explanations | Self-certified incorrect output |

|  |
| --- |
| **BOUNDARY RULE: IF AN OPERATION MUST BE CORRECT EVERY TIME, SURVIVE A CRASH, ENFO**  Boundary rule: If an operation must be correct every time, survive a crash, enforce a permission, coordinate concurrent writers, or create an auditable effect, it belongs to deterministic infrastructure. The LLM may decide what to attempt; deterministic systems decide whether and how it is committed. |

|  |
| --- |
| **COMMON PITFALL**  Treating schema validity as correctness. A response that parses cleanly can still name a stale record, a resource the caller cannot see, or an amount nobody approved. Schema validation rejects malformed proposals; it says nothing about whether the proposal should be allowed. Keep the two checks separate and run both. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Exactly-once wording | The recommendation is effect-level idempotency plus reconciliation under at-least-once delivery—not an end-to-end exactly-once guarantee. Timeout after dispatch is unknown until proved otherwise. | CLOUDEVENTS; OUTBOX |

Evidence anchors: CLOUDEVENTS; OUTBOX. Full URLs, authority, version, and scope appear in Appendix K.

## Pattern reference — Tool Use

|  |
| --- |
| **PROBLEM**  The model can identify an action or information need, but enterprise execution requires typed interfaces, current authorization, credentials, idempotency, and evidence. |

### Architecture and flow

The model proposes ToolIntent; the Tool Gateway validates the exact tool version and schema, reauthorizes the action and resource, mints a last-hop credential, invokes a connector, verifies the result, and records evidence.

1. Expose only tools eligible for the current run node.
2. Generate a minimal typed intent with evidence and uncertainty.
3. Validate schema, policy, risk, budget, approval, and resource version.
4. Invoke through a connector with timeout, idempotency, and egress controls.
5. Return a sanitized result or artifact reference and update durable state.

| **Use when** | **Do not use when** |
| --- | --- |
| Use whenever the agent must read external truth or request an external effect. | Do not expose raw SDKs, database handles, credentials, or broad generic tools directly to model-generated code. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Typed narrow tools | More interfaces to maintain; far stronger policy, testing, observability, and least privilege. |
| Dynamic discovery | Smaller prompts and flexible catalogs; requires deterministic eligibility and version resolution. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Hallucinated tool or arguments | Schema and eligibility rejection. |
| Duplicate mutation | Logical effect key, intent hash, downstream idempotency, and receipt. |
| Oversized or malicious output | Connector limits, content scanning, classification, and artifact indirection. |

### Minimum observability

* tool and version
* argument and result hashes
* policy decision
* credential lease ID
* latency and retries
* effect state and receipt

## Implementation reference


[[EXAMPLE:agent-tool-loop]]

### Governed Tool Gateway

PYTHON · implementation excerpt

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Awaitable, Callable, Literal
from pydantic import BaseModel, Field
from .approvals import ActionProposal, ApprovalGrant, verify_approval
from .effects import EffectOutcomeUnknown, InMemoryEffectLedger

class ToolManifest(BaseModel):
    tool_id:str; version:str; description:str
    risk_class:int=Field(ge=0,le=4); mutating:bool; required_action:str
    timeout_seconds:float=Field(gt=0,le=300); approval_required:bool=False
    idempotency_required:bool=False

class InvocationContext(BaseModel):
    tenant_id:str; subject_id:str; actor_id:str; run_id:str; purpose:str
    allowed_actions:frozenset[str]; eligible_tool_versions:frozenset[str]
    policy_digest:str="policy:unspecified"; region:str="unspecified"

class ToolResult(BaseModel):
    status:Literal["succeeded","declined","unknown"]
    output:dict[str,object]=Field(default_factory=dict); effect_key:str|None=None

class ToolGateway:
    def __init__(self,effect_ledger:InMemoryEffectLedger|None=None)->None:
        self._tools:dict[str,RegisteredTool]={}; self._effects=effect_ledger or InMemoryEffectLedger()
    def register(self,manifest:ToolManifest,connector:Connector)->None:
        key=f"{manifest.tool_id}@{manifest.version}"
        if key in self._tools: raise ValueError(f"tool already registered: {key}")
        if manifest.mutating and not manifest.idempotency_required:
            raise ValueError("mutating tools must declare idempotency_required")
        self._tools[key]=RegisteredTool(manifest,connector)
    def discover(self,ctx:InvocationContext)->tuple[ToolManifest,...]:
        return tuple(item.manifest for key,item in sorted(self._tools.items()) if key in ctx.eligible_tool_versions and item.manifest.required_action in ctx.allowed_actions)
    async def invoke(self,*,ctx:InvocationContext,tool_version:str,arguments:dict[str,object],logical_effect_key:str|None=None,proposal:ActionProposal|None=None,approval:ApprovalGrant|None=None,actual_resource_version:int|None=None)->ToolResult:
        if tool_version not in ctx.eligible_tool_versions: raise PermissionError("tool is not eligible for this run node")
        item=self._tools.get(tool_version)
        if item is None: raise LookupError("eligible tool version is not registered")
        m=item.manifest
        if m.required_action not in ctx.allowed_actions: raise PermissionError("required action is outside delegated authority")
        if m.approval_required:
            if proposal is None or approval is None or actual_resource_version is None: raise PermissionError("proposal-bound approval is required")
            if proposal.model_dump(mode="json",exclude={"expires_at"}) != ActionProposal(tenant_id=ctx.tenant_id,run_id=ctx.run_id,actor_id=ctx.actor_id,tool_version=tool_version,logical_effect_key=logical_effect_key or "",arguments=arguments,expected_resource_version=proposal.expected_resource_version,policy_digest=ctx.policy_digest,expires_at=proposal.expires_at).model_dump(mode="json",exclude={"expires_at"}): raise PermissionError("proposal does not match invocation")
            verify_approval(proposal,approval,now=datetime.now(timezone.utc),actual_resource_version=actual_resource_version)
        if not m.mutating:
            return ToolResult(status="succeeded",output=await item.connector(arguments,None))
        if not logical_effect_key: raise ValueError("mutating tools require a stable logical effect key")
        intent={"tool":tool_version,"arguments":arguments,"run_id":ctx.run_id,"tenant_id":ctx.tenant_id}
        effect=self._effects.begin(logical_effect_key,intent)
        if effect.state=="committed": return ToolResult(status="succeeded",output=effect.receipt or {},effect_key=logical_effect_key)
        if effect.state in {"executing","unknown","intervention_required"}: raise EffectOutcomeUnknown(logical_effect_key)
        if effect.state=="declined": return ToolResult(status="declined",output=effect.receipt or {},effect_key=logical_effect_key)
        self._effects.mark_executing(logical_effect_key,f"req:{logical_effect_key}")
        try: output=await item.connector(arguments,logical_effect_key)
        except Exception as exc:
            self._effects.mark_unknown(logical_effect_key)
            raise EffectOutcomeUnknown(logical_effect_key) from exc
        committed=self._effects.mark_committed(logical_effect_key,output)
        return ToolResult(status="succeeded",output=committed.receipt or {},effect_key=logical_effect_key)
```

## Debugging playbook

1. Compare the raw model proposal with the validated command and list rejected fields.
2. Inspect the policy decision and resource version immediately before commit.
3. Replay the same logical mutation and verify one receipt.

## Production checklist

**✓** Every model output is classified as a proposal by default.

**✓** State transitions, policy, budgets, business rules, and protected commits sit behind deterministic interfaces.

**✓** Proposals are minimal, typed, evidence-linked, and explicit about uncertainty.

**✓** Resource versions and obligations are rechecked immediately before commit.

**✓** Completion uses deterministic acceptance criteria.

## Exercises

1. Define a typed proposal and deterministic acceptance function for supplier screening.
2. Write five invariants that must be true before supplier activation can commit.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| What belongs in the agentic core versus the deterministic shell? | Semantic interpretation, evidence synthesis, and bounded planning in the core; authority, state, policy, concurrency, effects, and acceptance in the shell. |
| Explain propose–validate–commit. | The model emits a typed proposal; deterministic services validate schema, authority, risk, budget, evidence, and version; only a domain service commits and records a receipt. |
| Why is structured model output necessary but insufficient? | It reduces parsing ambiguity but does not prove truth, authorization, freshness, business validity, idempotency, or safety. |
| Where should completion be decided? | In an acceptance engine or workflow guard using required artifacts, effect states, policy obligations, and domain invariants—not from a model’s “done” message. |
| What is the trade-off of a stronger deterministic shell? | More contracts and platform complexity, but improved safety, replayability, testing, provider portability, incident recovery, and auditability. |

## Transition to Chapter 3

With tools bounded, Chapter 3 defines the runtime contract that keeps applications portable across agent frameworks and model providers.

# 03 — Agent Runtime and Framework Abstraction

> **Evidence note.** Concrete adapter examples use OpenAI Agents SDK v0.22.2 and its documented agent, tool, guardrail, handoff, result, and tracing surfaces; the platform contracts remain framework-neutral. [R29][R30]

> This chapter uses the OpenAI Agents SDK as a concrete adapter. Enterprise applications should compile platform-owned contracts into this or another framework through conformance-tested adapters; Chapters 4–7 define the portable architecture.

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Northstar adopts OpenAI Agents SDK for its compact agent loop, tools, handoffs, structured outputs, tracing, sessions, and human-interruption surfaces. The architecture team refuses to let SDK state become workflow truth or to expose raw enterprise credentials to the agent process. |

|  |
| --- |
| **DESIGN DECISION**  Place the OpenAI Agents SDK behind AgentRuntime; pin 0.22.2 and keep workflow, authority, credentials, effects, and audit platform-owned. |

## What this chapter delivers

Use OpenAI Agents SDK 0.22.2 as a bounded, replaceable runtime adapter rather than the enterprise control plane.

## Solution blueprint


Figure 3. Agent Runtime and OpenAI Agents SDK.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Durable workflow; SDK only owns one bounded step | platform contract to SDK adapter | worker pool · model route · tool class | one activity attempt | AgentRuntime · AgentStepRequest · RunState |

## Framework baseline and placement

This edition pins openai-agents==0.22.2 and openai>=2.25.0 as an implementation baseline. The SDK provides useful application-level primitives: Agent, Runner, function tools, agents-as-tools, handoffs, guardrails, structured output, sessions, tracing, MCP integration, deferred tool loading, ToolSearchTool, tool namespaces, human interruption, serializable RunState, and sandbox-oriented agent surfaces.

Northstar uses those primitives for **one bounded agent activity**. A durable workflow calls a platform-owned AgentRuntime; the OpenAI adapter builds the eligible agent and tool set, invokes Runner, and translates the result back into provider-neutral contracts. This makes the SDK valuable without making it the owner of long-lived business truth.

| **SDK concern** | **Northstar placement** |
| --- | --- |
| Agent instructions and structured output | SDK adapter, pinned in release manifest |
| Turn loop and local handoff | SDK worker, bounded by external limits |
| Sessions / RunState | Optional resumable runtime state; never canonical workflow state |
| Function tools and MCP | Narrow façades that call the Tool Gateway |
| Guardrails | Defense in depth; policy still enforced outside the model |
| Tracing | Exported and correlated with workflow/effect/audit IDs |
| Approval interruption | Mapped to durable ApprovalRequest and workflow wait |
| Credentials and business writes | Tool Gateway and domain services only |

### Upgrade discipline

An SDK upgrade is a behavior change even when public types remain compatible. Northstar runs adapter contract tests, recorded trajectory replay, tool-schema tests, approval interruption tests, model-route evaluations, load tests, and canary releases. Active workflows retain the SDK and agent-definition versions in their RunManifest.

## Architectural role

The OpenAI Agents SDK is best treated as a **bounded agent harness**, not the platform kernel. It contributes model-facing ergonomics—agent definitions, tools, structured outputs, local handoffs, run context, streaming, guardrails, and tracing hooks. Enterprise durability, delegated authorization, business transactions, approvals, effect reconciliation, tenant isolation, and audit remain platform responsibilities.

## Stable runtime contract

Keep public Run APIs and workflow history independent of SDK types. A platform-owned boundary can be expressed as:

TEXT · implementation excerpt

```text
AgentRuntime.execute(AgentStepRequest) -> AgentStepResult
```

AgentStepRequest pins run and node identity, state version, agent and model route, authorized context manifest, eligible tools, capability ceiling, output schema, resource limits, deadline, and trace context. AgentStepResult returns a typed disposition, immutable artifact references, proposed actions, a concise evidence-grounded summary, usage, trace references, and a structured error.

## One bounded step

1. The durable workflow schedules a reasoning activity with pinned versions and a deadline.
2. Context is materialized from an authorized ContextManifest.
3. The adapter creates SDK agents and only the tool façades eligible for this node.
4. External controls enforce turns, time, tokens, cost, tool calls, parallelism, and delegation depth.
5. The SDK executes the local model/tool loop.
6. The adapter validates the structured result and records usage and trace linkage.
7. Workflow code—not the SDK—chooses the next durable transition.

## Bounded Python adapter

[[EXAMPLE:step-execution#core]]

The model and SDK never receive a reusable production credential. The tool façade submits identifiers and typed arguments to the gateway, which reauthorizes the exact resource, mints a short-lived last-hop credential, enforces effects and quotas, and sanitizes the result.

## Handoffs and specialists

Use Agent.as\_tool() when a manager must retain control of the final result. Use an SDK handoff when conversational control genuinely transfers inside one bounded activity. Use a durable TaskEnvelope and child workflow when the work needs independent ownership, retries, waits, deadlines, scaling, cancellation, or a cross-service trust boundary. A conversational handoff must never silently transfer budget, authority, task ownership, or cancellation responsibility.

## Guardrails, state, and retries

SDK guardrails are valuable for early input, tool, and output checks. They do not replace canonical schema validation, a policy decision point, Tool Gateway authorization, or domain transaction rules. SDK sessions can assist local continuity, but run state, plan revisions, budgets, approvals, effects, policy decisions, and compliance evidence remain authoritative elsewhere.

Assign one retry owner per failure class: the workflow owns activity retries; the Model Gateway may perform short transport retries inside one recorded attempt; the Tool Gateway follows the tool manifest and effect protocol; an unknown mutation is reconciled before any retry.

|  |
| --- |
| **ARCHITECTURE GUIDANCE**  Let the framework own the agent loop, never the workflow truth. Run state, approvals, and effect records belong in your durable store, keyed by your identifiers. The SDK's session object is a convenience for one process; if losing it would lose the run, the boundary is in the wrong place. |

## Adoption test

Adopt the SDK only after proving that tools cannot bypass gateways, every invocation is externally bounded, handoffs map to durable ownership correctly, sensitive tracing is disabled or isolated, protected commits require deterministic validation, and another runtime could replace the adapter without migrating public APIs, workflow history, effects, artifacts, approvals, or audit.

|  |
| --- |
| **DEVELOPER GUIDELINE**  Depend on the adapter you wrote, not on the SDK's types, everywhere above the runtime boundary. One module should import the vendor package. That module is also the only thing you rewrite when a 0.x SDK changes its API, which it will. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Pinned SDK behavior | OpenAI Agents SDK 0.22.2 was released 9 September 2026. The project uses 0.Y.Z versioning and remains fast-moving. Deferred tool search is Responses-only, needs openai>=2.25.0, and requires exactly one ToolSearchTool when deferred function surfaces are used. | OAI-RELEASE; OAI-TOOLS |
| Pause/resume boundary | RunState is the SDK pause/resume object. Custom context serialization is conservative; rebuild live gateways and secrets rather than serializing them blindly. Independently restored states must not resume concurrently against one session history. | OAI-RUNSTATE |
| Scope of SDK approval | An SDK approval interruption pauses a call; it does not by itself prove enterprise authorization, separation of duties, resource freshness, or idempotent effect semantics. The gateway must verify those controls. | OAI-HITL |

Evidence anchors: OAI-RELEASE; OAI-TOOLS; OAI-RUNSTATE; OAI-HITL. Full URLs, authority, version, and scope appear in Appendix K.

## Implementation reference


### OpenAI Agents SDK enterprise adapter

PYTHON · implementation excerpt

```python
"""OpenAI Agents SDK 0.22.2 adapter.

Requires openai-agents==0.22.2 and openai>=2.25.0. Framework-owned approval
interrupts complement—but do not replace—the enterprise proposal and effect ledgers.
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Annotated, Any, Literal, Protocol
from agents import Agent, RunConfig, RunContextWrapper, Runner, ToolSearchTool, tool_namespace
from agents.decorators import tool
from pydantic import BaseModel, Field

class EnterpriseToolGateway(Protocol):
    async def invoke(self,*,tenant_id:str,subject_id:str,actor_id:str,run_id:str,tool_version:str,arguments:dict[str,object],logical_effect_key:str|None=None,approval_id:str|None=None,proposal_hash:str|None=None)->dict[str,object]: ...

@dataclass(frozen=True)
class PlatformContext:
    tenant_id:str; subject_id:str; actor_id:str; run_id:str; purpose:str; gateway:EnterpriseToolGateway

class SupplierDecision(BaseModel):
    disposition:Literal["request_evidence","ready_for_approval","reject"]
    rationale:str=Field(min_length=1,max_length=1_000)
    evidence_artifact_ids:list[str]

@tool(defer_loading=True)
async def get_supplier_profile(ctx:RunContextWrapper[PlatformContext],supplier_id:Annotated[str,"Canonical supplier candidate ID"])->dict[str,object]:
    """Load the authorized profile for one canonical supplier candidate."""
    return await ctx.context.gateway.invoke(tenant_id=ctx.context.tenant_id,subject_id=ctx.context.subject_id,actor_id=ctx.context.actor_id,run_id=ctx.context.run_id,tool_version="supplier.profile.read@2.1.0",arguments={"supplier_id":supplier_id})

@tool(defer_loading=True)
async def screen_supplier(ctx:RunContextWrapper[PlatformContext],supplier_id:Annotated[str,"Canonical supplier candidate ID"])->dict[str,object]:
    """Run the governed screening capability for one supplier candidate."""
    return await ctx.context.gateway.invoke(tenant_id=ctx.context.tenant_id,subject_id=ctx.context.subject_id,actor_id=ctx.context.actor_id,run_id=ctx.context.run_id,tool_version="supplier.screen@3.0.0",arguments={"supplier_id":supplier_id})

@tool(needs_approval=True)
async def create_supplier_record(ctx:RunContextWrapper[PlatformContext],supplier_id:str,expected_version:int,approval_id:str,proposal_hash:str)->dict[str,object]:
    """Commit only after SDK interruption and gateway verification of the exact proposal."""
    return await ctx.context.gateway.invoke(tenant_id=ctx.context.tenant_id,subject_id=ctx.context.subject_id,actor_id=ctx.context.actor_id,run_id=ctx.context.run_id,tool_version="supplier.create@1.4.0",arguments={"supplier_id":supplier_id,"expected_version":expected_version},logical_effect_key=f"{ctx.context.run_id}:supplier.create:{supplier_id}",approval_id=approval_id,proposal_hash=proposal_hash)

supplier_tools=tool_namespace(name="supplier_onboarding",description="Read-only supplier profile and screening capabilities.",tools=[get_supplier_profile,screen_supplier])

def build_supplier_agent()->Agent[PlatformContext]:
    model=os.environ["OPENAI_AGENT_MODEL"]
    return Agent[PlatformContext](name="Supplier onboarding analyst",model=model,instructions="Use only supplied, authorized evidence. Load the supplier_onboarding namespace when evidence is required. Protected writes require the direct create_supplier_record tool and must preserve approval IDs and proposal hashes. Never claim an external write without its receipt.",tools=[*supplier_tools,create_supplier_record,ToolSearchTool()],output_type=SupplierDecision)

async def execute_bounded_run(input_items:str|list[dict[str,object]],context:PlatformContext):
    """Return RunResult so the platform—not an exception string—owns pause/resume."""
    return await Runner.run(starting_agent=build_supplier_agent(),input=input_items,context=context,max_turns=6,run_config=RunConfig(workflow_name="northstar-supplier-onboarding",group_id=context.run_id,trace_include_sensitive_data=False,trace_metadata={"run_id":context.run_id,"purpose":context.purpose}))

def serialize_interrupted_run(result:Any)->str:
    if not result.interruptions: raise ValueError("run has no pending approval")
    # Custom PlatformContext contains a live gateway; configure an application serializer
    # or persist identifiers separately and rebuild context when restoring the snapshot.
    return result.to_state().to_string()

async def approve_in_memory_and_resume(result:Any,interruption_index:int=0):
    """Minimal SDK flow; production first verifies the enterprise ApprovalGrant."""
    state=result.to_state(); state.approve(result.interruptions[interruption_index])
    return await Runner.run(build_supplier_agent(),state)
```

## Debugging playbook

1. Capture the platform request and SDK adapter request and diff their responsibilities.
2. Verify which SDK state is persisted and whether its version is pinned.
3. Disable one tool at the gateway and confirm the agent cannot recover ambient access.

## Production checklist

**✓** The SDK sits behind a platform-owned AgentRuntime adapter.

**✓** Only governed tool façades enter the agent process.

**✓** Turns, time, tokens, cost, tool calls, and delegation have external limits.

**✓** Local handoffs are distinct from durable task ownership.

**✓** Retry, state, trace privacy, and release compatibility are coordinated outside the SDK.

## Exercises

1. Implement a minimal AgentRuntime protocol and an OpenAI Agents SDK adapter.
2. Design a compatibility test that proves an SDK upgrade preserves platform contracts.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Where should the OpenAI Agents SDK sit in an enterprise architecture? | Inside a bounded worker behind AgentRuntime, called by a durable workflow and connected to model and tool gateways through platform contracts. |
| What should the SDK not own? | Authoritative workflow state, delegated authorization, credentials, business transactions, effect reconciliation, enterprise approvals, and audit evidence. |
| When should you use an agent-as-tool, a handoff, or a durable child task? | Use an agent-as-tool when a manager retains control; a handoff when conversational control transfers; a durable task when work needs separate ownership, waits, retries, scaling, or recovery. |
| How do you make SDK tools safe? | Supply a minimal set, use typed façades, reauthorize exact resources at the Tool Gateway, mint last-hop credentials, enforce idempotency, and sanitize results. |
| How do you keep the SDK replaceable? | Store platform contracts, workflow history, artifacts, effects, approvals, and public APIs in provider-neutral forms; confine SDK types to the adapter. |

|  |
| --- |
| **PART II**  **AGENTIC DESIGN PATTERNS**  Choose and implement the smallest pattern that resolves the real uncertainty: ReAct, routing, planning, reflection, human control, and durable execution. |

04 ReAct: Bounded Reason–Act–Observe Loops

05 Routing, Triage, and Handoffs

06 Planning and Plan–Execute

07 Reflection and Evaluator–Optimizer

08 Human-in-the-Loop

09 Long-Running and Durable Agents

## Transition to Chapter 4

The runtime now has a stable boundary; Chapter 4 places it inside the complete enterprise reference architecture.
