# PART V — ANTI-PATTERNS

This Part reverses the lens. It exposes recurring architecture shapes that hide authority, state, effects, security, reliability, or operating cost, and pairs each failure with a measurable replacement pattern.

# 17 — Enterprise Anti-Pattern Catalog

## Field-guide method

Anti-patterns are recurring system shapes. Diagnose the failed responsibility boundary, not only the symptom. Each card supplies the same replacement sequence.

[[DIAGRAM:anti-before-after|Figure 17-1 — Autonomous monolith versus governed agentic architecture]]

## Reasoning

### AP-01 — Autonomous monolith

**Problem.** A prototype mixes reasoning, state, credentials, tools, retries, approval, completion.

**Anti-Pattern.** One unconstrained agent owns end-to-end control.

**Why It Fails.** Probabilistic behavior becomes the control plane and failures cannot be isolated.

**Recommended Pattern.** Bounded runtime inside durable workflow, policy, tool/effect, acceptance services.

**Architecture.** Monolith → direct tools → “done” versus workflow → semantic nodes → governed effects → acceptance.

**Enterprise Example.** Onboarding restarts and repeats vendor creation.

**Detection Metrics.** Direct protected calls, restart loss, false completion, mixed responsibilities.

**Trade-offs.** Decompose around highest-risk effects; more services add interfaces.

## Context engineering

### AP-02 — Prompt as database

**Problem.** Business state must survive.

**Anti-Pattern.** Chat history or summary is authoritative.

**Why It Fails.** Truncation, drift, concurrency, schema, and audit fail.

**Recommended Pattern.** Canonical typed state plus ContextManifest projection.

**Architecture.** Transcript state versus State Service → snapshot → prompt.

**Enterprise Example.** Renewal forgets legal approval after summarization.

**Detection Metrics.** Compaction loss, summary conflict, recovery mismatch.

**Trade-offs.** Typed state needs schema evolution.

## Security

### AP-03 — Ambient authority

**Problem.** Agents need access.

**Anti-Pattern.** Workers receive reusable broad credentials.

**Why It Fails.** Compromise obtains broad, long-lived authority.

**Recommended Pattern.** Subject+workload identity and narrowed capability leases.

**Architecture.** Broad token versus policy → scoped lease → enforcement.

**Enterprise Example.** Support token can export all customers.

**Detection Metrics.** Scope/age, unused privilege, expansion, cross-tenant attempts.

**Trade-offs.** Fine policy adds design/latency.

## Reliability

### AP-04 — Retry everywhere

**Problem.** Transient failures occur.

**Anti-Pattern.** SDK, gateway, workflow, connector, tool each retry.

**Why It Fails.** Attempts multiply, cost/load spike, mutations duplicate.

**Recommended Pattern.** One retry owner per failure class and shared attempt/deadline budget.

**Architecture.** Nested retries versus classified failure → one schedule → terminal.

**Enterprise Example.** 3×3×2 policies create 18 registry calls.

**Detection Metrics.** Attempts/logical operation, amplification, duplicates, deadline overrun.

**Trade-offs.** Central policy can be conservative.

## Reliability

### AP-05 — Timeout means failure

**Problem.** Response is lost after dispatch.

**Anti-Pattern.** Mark failed and retry immediately.

**Why It Fails.** First call may have committed.

**Recommended Pattern.** Unknown-effect terminal and reconciliation before retry/compensate.

**Architecture.** Timeout→failed→retry versus timeout→unknown→lookup→decide.

**Enterprise Example.** Vendor is created twice.

**Detection Metrics.** Unknown count/age, duplicate keys, post-timeout conflicts.

**Trade-offs.** Unknown may delay completion.

## Governance

### AP-06 — Boolean or conversational approval

**Problem.** Humans approve protected actions.

**Anti-Pattern.** A Boolean/chat message authorizes later current arguments.

**Why It Fails.** Effect, policy, actor, or version can change.

**Recommended Pattern.** Immutable proposal and expiring exact ApprovalGrant.

**Architecture.** approved=true versus proposal hash → grant → revalidate → commit.

**Enterprise Example.** $10k approval reused for $100k.

**Detection Metrics.** Hash mismatch, reuse, expiry, post-approval incident.

**Trade-offs.** Benign changes may require reapproval.

## Observability

### AP-07 — Model says done

**Problem.** Runs need completion.

**Anti-Pattern.** Model assertion sets success.

**Why It Fails.** Missing evidence, approval, effect, or obligation hides as success.

**Recommended Pattern.** Independent executable acceptance over authoritative state.

**Architecture.** Model text→success versus AcceptanceEngine→accepted/blocked/failed/unknown.

**Enterprise Example.** Onboarding says complete with stale sanctions check.

**Detection Metrics.** False completion, reopen rate, missing artifacts/effects.

**Trade-offs.** Rules require domain maintenance.

## Multi-agent collaboration

### AP-08 — Multi-agent chat as workflow

**Problem.** Specialists coordinate.

**Anti-Pattern.** Free-form messages own state, work, deadlines, joins.

**Why It Fails.** Duplicate work, cycles, lost cancellation/artifacts.

**Recommended Pattern.** TaskEnvelope, owner, child tasks, artifacts, deterministic join.

**Architecture.** Chat mesh versus supervisor workflow + task service.

**Enterprise Example.** Finance and legal each expect the other to approve.

**Detection Metrics.** Orphans, conflicts, depth, join age, late effects.

**Trade-offs.** Formal tasks reduce fluidity.

## Context engineering

### AP-09 — Vector store as source of truth

**Problem.** Relevant knowledge is needed.

**Anti-Pattern.** Similarity hit is current authoritative fact.

**Why It Fails.** Stale, unauthorized, poisoned, duplicated chunks drive action.

**Recommended Pattern.** Governed source/snapshot; index is derived locator with ACL/freshness verification.

**Architecture.** Vector hit→action versus source+ACL+snapshot→evidence→decision.

**Enterprise Example.** Old policy chunk applies obsolete limit.

**Detection Metrics.** Freshness, source disagreement, ACL/citation mismatch.

**Trade-offs.** Authoritative lookup may be slower.

## Security

### AP-10 — LLM judge as security gate

**Problem.** Ambiguous content needs review.

**Anti-Pattern.** Model score alone authorizes protected action.

**Why It Fails.** Judge is injectable, nondeterministic, biased, and drifts.

**Recommended Pattern.** Deterministic policy/invariant gate; judge only triages/evidences.

**Architecture.** score>threshold→execute versus policy→optional judge→human/escalation.

**Enterprise Example.** Judge calls excessive payment low risk.

**Detection Metrics.** Repeated-run disagreement, bypass, false negative, override.

**Trade-offs.** Rules cannot express all nuance.

## Reasoning

### AP-11 — Unbounded loops and recursive delegation

**Problem.** Complex work varies.

**Anti-Pattern.** Agents iterate/spawn without global limits.

**Why It Fails.** Runaway cost, cyclic delegation, queue saturation.

**Recommended Pattern.** Global decreasing budgets, acyclic ownership, depth/fan-out/progress limits.

**Architecture.** Recursion versus runtime-governed task graph.

**Enterprise Example.** Research supervisor spawns endless fact-checkers.

**Detection Metrics.** Depth, fan-out, repeated state, no progress, budget exhaustion.

**Trade-offs.** Caps may truncate rare work.

## Tools

### AP-12 — Ungated tool discovery and catalog dumping

**Problem.** Many tools exist.

**Anti-Pattern.** Every discovered tool/schema enters the prompt.

**Why It Fails.** Confusion, token load, malicious descriptions, excessive agency.

**Recommended Pattern.** Registry → eligibility/policy → task shortlist → schema validation.

**Architecture.** Full MCP catalog versus approved tool slice and lease.

**Enterprise Example.** Reporting agent finds admin delete tool.

**Detection Metrics.** Exposed/eligible/used, confusion, overhead, unauthorized discovery.

**Trade-offs.** Narrow list can omit needed tool.

## Memory

### AP-13 — Memory write by default

**Problem.** Personalization is desired.

**Anti-Pattern.** Every interaction/summary becomes durable memory.

**Why It Fails.** Secrets, errors, injections, bias, stale facts persist.

**Recommended Pattern.** Purpose-bound candidate with provenance, verification, scope, TTL, deletion.

**Architecture.** Transcript→memory versus candidate→gate→typed record.

**Enterprise Example.** Malicious email stores fake bank account.

**Detection Metrics.** Sensitive writes, stale retrieval, corrections, memory incidents.

**Trade-offs.** Strict writes reduce convenience.

## Observability

### AP-14 — Telemetry without causal/effect lineage

**Problem.** Teams instrument components.

**Anti-Pattern.** Logs cannot join versions, policy, effects, acceptance, outcome.

**Why It Fails.** Local optimization hides business regression.

**Recommended Pattern.** Causal run graph joining release, context, decisions, effects, outcome/cost.

**Architecture.** Separate dashboards versus correlated graph.

**Enterprise Example.** Lower model latency hides more retries and lower completion.

**Detection Metrics.** Outcome join, missing parents/versions, unattributed cost.

**Trade-offs.** Correlation increases governance burden.

## System architecture

### AP-15 — Model/provider swap as configuration

**Problem.** Teams seek cost/quality changes.

**Anti-Pattern.** Alias changes without behavioral validation.

**Why It Fails.** Tool, schema, refusal, safety, latency, cost behavior shifts.

**Recommended Pattern.** Versioned ChangeBundle with evaluation, security, load, canary, rollback.

**Architecture.** Edit alias versus immutable route policy→replay→approval→canary.

**Enterprise Example.** Cheaper model drops tool args in one language.

**Detection Metrics.** Schema/tool regression, refusal shift, slice drift, fallback.

**Trade-offs.** Validation slows experimentation.

## Operations

### AP-16 — In-place change and test after release

**Problem.** Fast edits are convenient.

**Anti-Pattern.** Prompts/Skills/tools/policy/routes mutate production.

**Why It Fails.** Runs are irreproducible; rollback/attribution fail.

**Recommended Pattern.** Immutable artifacts, ReleaseManifest, pretests, signed promotion, canary, rollback.

**Architecture.** Mutable console versus build→validate→approve→promote→monitor.

**Enterprise Example.** Prompt fix increases leakage and cannot roll back exactly.

**Detection Metrics.** Unversioned runs, out-of-band edits, rollback failure.

**Trade-offs.** Immutability needs good tooling.


## Transition to Chapter 18

After removing unsafe local architectures, Chapter 18 considers when multiple agents add justified specialization rather than accidental complexity.
