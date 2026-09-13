# PART VIII — SECURITY & GUARDRAILS

This Part applies defense in depth to untrusted content, identity, delegated authority, tools, code, data, memory, multi-agent traffic, MCP servers, and the software supply chain. Each control is tied to a trust boundary, runtime decision, detection signal, and recovery path.

# 21 — Agentic AI Security and Guardrails Architecture

> **Evidence note.** The threat catalog is cross-checked against OWASP agentic-security guidance, while the trust-boundary model follows zero-trust principles that require explicit policy decisions around protected resources. [R11][R15][R16]

## Defense in depth

Agentic systems combine untrusted language, privileged tools, dynamic context, durable memory, third-party protocols, and autonomous timing. Security cannot be one prompt or classifier. It constrains what enters, which capabilities become eligible, what may leave, which effects commit, and how the enterprise detects and recovers.

[[DIAGRAM:security-depth|Figure 21-1 — Defense-in-depth guardrails architecture]]

| **Layer** | **Controls** | **Evidence** |
| --- | --- | --- |
| Channel/input | Authentication, abuse, injection/jailbreak detection, normalization | Identity, session risk, classifier/version, decision |
| Context/memory | Source trust, ACL, provenance, freshness, poisoning, TTL, correction/deletion | ContextManifest and MemoryRecord lineage |
| Model/output | Approved route, instruction integrity, schema, content safety, evidence, DLP | RoutingDecision and guard results |
| Agent/workflow | Least-agentic topology, budgets, deadlines, loop/fan-out caps, durable terminals | Run/task graph and budget ledger |
| Identity/policy | Subject/workload identity, least privilege, RBAC/ABAC, purpose/spend/time | PolicyDecision and CapabilityEnvelope |
| Tools/effects | Eligible tool, schema/precondition, proposal/approval, idempotency, reconcile | ToolCall, ApprovalGrant, EffectRecord |
| Execution/egress | Sandbox, network/file/syscall, secrets isolation, destination policy, DLP | Sandbox and egress decisions |
| Supply chain/release | Locks, SBOM, signatures, provenance, tests, canary, rollback | ReleaseManifest and ValidationReport |
| Detection/response | Monitoring, auditing, containment, revocation, incident response | Alert, timeline, recovery and learning record |

## Trust boundaries and runtime sequence

[[DIAGRAM:security-boundaries|Figure 21-2 — Agentic security trust boundaries]]

Trust is not inherited through a chain. User authentication does not authorize the agent; discovery does not authorize a tool; retrieved text is not instruction; an agent message does not prove peer identity; HTTP success does not prove business acceptance.

[[DIAGRAM:guardrail-sequence|Figure 21-3 — Runtime guardrail and protected-effect sequence]]

Authenticate subject/workload; classify/minimize input; build authorized labeled context; choose eligible model; validate structured output; authorize eligible tool and exact arguments; obtain proposal-bound approval when required; execute through sandbox/gateway with scoped credentials and DLP; reconcile effects and run deterministic acceptance; monitor, audit, contain, revoke, recover, and learn.

|  |
| --- |
| **SECURITY AND GOVERNANCE**  Treat every retrieved document, tool result, and page as untrusted input. Injected instructions arrive as ordinary content, so guardrails placed only around the user's prompt miss them entirely. Enforce at the effect boundary, where intent becomes action, not at the point of text entry. |

## Threat catalog

### T-01 — Direct prompt injection

**Attack scenario.** A user tells the model to ignore policy, reveal instructions, or invoke a forbidden tool.

**Enterprise impact.** Unauthorized action, disclosure, or policy bypass.

**Detection signals.** Override phrases, hierarchy conflicts, anomalous tool requests, denial spikes.

**Prevention mechanisms.** Separate trusted instructions/untrusted input, typed intent, least privilege, adversarial tests.

**Runtime controls.** Input classifier, eligible-tool policy, schema/output/DLP guards, bounded runtime, approval.

**Recovery strategy.** Block/degrade, revoke run capability, preserve trace, notify owner, add regression.

### T-02 — Indirect prompt injection

**Attack scenario.** A document, web page, email, or tool result contains instructions aimed at the agent.

**Enterprise impact.** Compromised decision/effect through authorized retrieval.

**Detection signals.** Instruction-like retrieved text, risky source, divergence after one source, unusual tool chain.

**Prevention mechanisms.** Treat retrieval as data, provenance/allowlists, isolation, sanitization, injection tests.

**Runtime controls.** Context labels, tool eligibility independent of content, evidence checks, least privilege.

**Recovery strategy.** Quarantine source/snapshot, invalidate context/memory/cache, replay affected runs.

### T-03 — Jailbreaks

**Attack scenario.** Obfuscation, role-play, encoding, multilingual or multi-turn probing evades safeguards.

**Enterprise impact.** Harmful output or progressive acquisition of restricted information.

**Detection signals.** Classifier disagreement, encoded payloads, repeated reformulation, near-miss patterns.

**Prevention mechanisms.** Layered policies/classifiers, rate limits, restricted capabilities, behavior tests.

**Runtime controls.** Session risk, capability reduction, refusal/redirect, human escalation, output filter.

**Recovery strategy.** Suspend session/capability, investigate campaign, rotate defenses, add variants.

### T-04 — Malicious context

**Attack scenario.** Authorized-looking context is crafted to mislead or override the task.

**Enterprise impact.** High-confidence incorrect decisions or manipulated outcomes.

**Detection signals.** Source disagreement, semantic drift, weak provenance, unsupported claims, metadata outlier.

**Prevention mechanisms.** ContextManifest, trust tiers, corroboration, signatures, freshness.

**Runtime controls.** Risk-weighted retrieval, claim-evidence verifier, abstain/escalate on conflict.

**Recovery strategy.** Quarantine artifact, invalidate snapshot/cache, correct downstream decisions.

### T-05 — Retrieval/RAG poisoning

**Attack scenario.** Poisoned documents/chunks enter or are promoted in the corpus/index.

**Enterprise impact.** Systematic misinformation, exfiltration, or unsafe actions across runs.

**Detection signals.** Ingestion anomaly, rank manipulation, source drift, failures tied to new source.

**Prevention mechanisms.** Signed/approved ingestion, source/index separation, ACL, provenance, poisoning tests.

**Runtime controls.** Source/snapshot/ACL filter, anomaly ranking, evidence diversity/corroboration.

**Recovery strategy.** Remove data, rebuild trusted index, invalidate caches, replay affected runs.

### T-06 — Memory poisoning

**Attack scenario.** A user, document, tool, or model creates malicious durable memory.

**Enterprise impact.** Persistent compromise across sessions and future decisions.

**Detection signals.** Unusual writes, instruction-like memory, corrections, failures tied to one record.

**Prevention mechanisms.** Candidate-write gate, purpose/scope/TTL, provenance, verification, user control.

**Runtime controls.** Confidence/freshness checks, no authority from memory, read/write audit.

**Recovery strategy.** Quarantine/delete record and derivatives, notify, replay, tighten eligibility.

### T-07 — Tool misuse

**Attack scenario.** The model selects the wrong tool or unsafe arguments.

**Enterprise impact.** Corruption, financial loss, privacy violation, disruption.

**Detection signals.** Low tool precision, argument/precondition failures, denied calls, effect anomaly.

**Prevention mechanisms.** Narrow catalog, typed schemas, semantic constraints, risk labels, contract tests.

**Runtime controls.** Policy/precondition, preview, idempotency, approval, effect ledger, acceptance.

**Recovery strategy.** Pause tool, revoke credentials, reconcile/compensate, repair contract/tests.

### T-08 — Excessive agency

**Attack scenario.** Agent has excessive tools, time, budget, autonomy, or delegation.

**Enterprise impact.** Runaway cost, unintended effects, large blast radius.

**Detection signals.** Long-tail steps/fan-out, budget exhaustion, no-progress loops, broad unused scope.

**Prevention mechanisms.** Least-agentic design, budgets, tool slicing, depth/fan-out limits, approval.

**Runtime controls.** Admission/stop conditions, capability leases, circuits, human escalation.

**Recovery strategy.** Pause/terminate, revoke, reconcile effects, redesign topology and budgets.

### T-09 — Privilege escalation

**Attack scenario.** Agent or child expands resource, action, purpose, spend, or time scope.

**Enterprise impact.** Cross-tenant or high-impact unauthorized access.

**Detection signals.** Delegation expansion, audience mismatch, policy denials, unusual role assumption.

**Prevention mechanisms.** Subject+workload identity, monotonic delegation, RBAC/ABAC, short-lived credentials.

**Runtime controls.** Reauthorize each hop, intersect scope, just-in-time lease, gateway/tool enforcement.

**Recovery strategy.** Revoke, isolate, audit/repair resources, fix policy and delegation tests.

### T-10 — Data exfiltration

**Attack scenario.** Sensitive data is sent to unauthorized model, tool, agent, URL, or channel.

**Enterprise impact.** Regulatory breach, IP loss, customer harm.

**Detection signals.** Egress anomaly, unknown domain/tool, high-entropy output, cross-region route.

**Prevention mechanisms.** Classify, minimize/tokenize, egress allowlist, provider terms, private endpoints, DLP.

**Runtime controls.** Egress proxy, network/DNS policy, destination auth, output DLP, volume limits.

**Recovery strategy.** Block, revoke keys, contain, preserve evidence, breach workflow.

### T-11 — Sensitive-data leakage

**Attack scenario.** PII/secrets appear in responses, logs, traces, caches, or evaluations.

**Enterprise impact.** Privacy/security incident and credential compromise.

**Detection signals.** DLP/canary-secret hit, redaction failure, sensitive cache/log, access anomaly.

**Prevention mechanisms.** Minimize, structured redaction/tokenization, secret scan, encryption, retention.

**Runtime controls.** Input/output/log guard, protected payload references, role-based trace access.

**Recovery strategy.** Rotate secrets, delete/repair copies, rights/incident process, improve detectors.

### T-12 — Insecure agent-to-agent communication

**Attack scenario.** Agents accept unauthenticated tasks, artifacts, callbacks, or delegation.

**Enterprise impact.** Spoofing, confused deputy, leakage, cross-tenant effect.

**Detection signals.** Unknown issuer, signature/audience failure, replay, task/artifact mismatch.

**Prevention mechanisms.** Mutual workload identity, signed envelope, audience/tenant, nonce/idempotency, schema.

**Runtime controls.** Agent gateway validates identity, authority, deadline, provenance, cancellation.

**Recovery strategy.** Reject/quarantine, revoke trust, audit/reconcile, rotate credentials.

### T-13 — Malicious MCP servers

**Attack scenario.** Server advertises deceptive tools, changes behavior, steals data, injects output.

**Enterprise impact.** Credential theft, tool misuse, persistent injection, supply-chain compromise.

**Detection signals.** Manifest/schema drift, unsigned version, unexpected egress, anomalous output.

**Prevention mechanisms.** Approved registry, signing/provenance, sandbox, network policy, version pinning.

**Runtime controls.** MCP gateway filters discovery, scopes credentials, validates output, records effects.

**Recovery strategy.** Disable/quarantine version, revoke, inspect traces/effects, restore trusted version.

### T-14 — Unsafe code execution

**Attack scenario.** Generated/retrieved code runs with host, network, secret, or persistence access.

**Enterprise impact.** RCE, theft, lateral movement, resource abuse.

**Detection signals.** Unexpected syscall/egress/file, resource spike, prohibited import, escape signal.

**Prevention mechanisms.** Avoid when possible; ephemeral sandbox, read-only base, no secrets, allowlists, signed deps.

**Runtime controls.** Time/resource/syscall/network/file controls, scanning, artifact validation.

**Recovery strategy.** Kill/isolate, revoke, preserve forensic evidence, patch/rotate base.

### T-15 — Identity spoofing

**Attack scenario.** Request/tool call misrepresents user, workload, tenant, or approver.

**Enterprise impact.** Unauthorized access and non-repudiation failure.

**Detection signals.** Issuer/audience/token mismatch, impossible actor chain, unsigned context.

**Prevention mechanisms.** Strong auth, workload identity, signed context, channel binding, approver auth.

**Runtime controls.** Revalidate at gateways/tools; never trust model-supplied identity fields.

**Recovery strategy.** Revoke sessions, invalidate approvals, audit/repair effects, strengthen proofing.

### T-16 — Supply-chain attacks

**Attack scenario.** Compromised SDK, package, model, Skill, container, prompt, evaluator, or pipeline enters release.

**Enterprise impact.** Widespread execution, hidden behavior, leakage, corrupted assurance.

**Detection signals.** Hash/signature mismatch, dependency drift, provenance gap, anomalous build/egress.

**Prevention mechanisms.** Locks, SBOM, signed provenance, trusted builders/signers, scanning, immutable registry.

**Runtime controls.** Admission verifies digest/provenance; runtime pins artifact and limits privilege/egress.

**Recovery strategy.** Revoke artifact/key, halt/rollback, scope releases, rotate secrets, disclose.

## Incident response

Use Detect → Contain → Revoke → Reconcile → Eradicate → Recover → Learn. Containment can pause a tool, MCP server, model route, Skill, memory namespace, tenant, or agent. Revoke credentials, capabilities, approvals, artifacts, signing keys, and trust. Reconcile which effects actually occurred; never infer from the model's final message. Restore a known release and authoritative state, then create privacy-reviewed regression cases.


## Transition to Chapter 22

The threat model is established; Chapter 22 applies it to context, retrieval, memory, and state—the data surfaces most likely to carry hidden instructions.

# 22 — Context Engineering, RAG, Memory, and State

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  As runs grow, prompts become a mixture of chat, workflow state, retrieved documents, summaries, and learned preferences. Northstar separates these domains and records exactly which authorized projection reached each model call. |

|  |
| --- |
| **DESIGN DECISION**  Treat prompts as disposable authorized projections; keep canonical state, knowledge, artifacts, and memory in distinct stores. |

## What this chapter delivers

Assemble authorized context from distinct state and knowledge domains and govern reusable memory as a data product.

## Solution blueprint


Figure 14. Context Engineering, Memory, and State.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Context Service; workflow remains canonical | authorized sources to model prompt | tenant · source · context budget | one context projection | ContextManifest · MemoryRecord · EvidenceRef |

## The context build pipeline

Northstar assembles context in stages: parse the request, calculate source candidates, enforce tenant and resource authorization, fetch immutable versions, classify and sanitize content, deduplicate, rank, allocate tokens, produce ordered references, and record a ContextManifest. Only the final authorized boundary materializes bytes into the model request.

Instructions have a trust hierarchy. System and application instructions are code-like release artifacts. Skill instructions are pinned capability artifacts. User requests express intent within authority. Retrieved documents and tool outputs are untrusted evidence. Content cannot promote itself to a higher trust role by saying “ignore previous instructions.”

Memory is not a bag of embeddings. Long-term memory creation is a protected data write with owner, scope, provenance, confidence, policy basis, TTL, correction, and deletion. Canonical business state always wins over a memory summary.

## Context, workflow state, memory, and enterprise knowledge

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | “Memory” often conflates prompts, conversation history, task state, preferences, learned facts, documents, and recovery data—causing leakage, stale decisions, and unreproducible runs. |
| Why it is difficult | Each type has different scope, consistency, privacy, retention, freshness, and retrieval semantics; models can misclassify or invent memories. |
| Design alternatives | Full transcript replay; summarization; graph checkpoints; key/value memory; vector memory; knowledge graph; source-grounded retrieval; event-sourced state. |
| Recommended architecture | Separate stores and APIs by semantic role. Build the model context as a policy-filtered projection of authoritative workflow state, recent conversation, relevant source-grounded knowledge, and explicitly approved memories. |
| Trade-offs | Separation requires more schemas and retrieval logic, but enables correct ACLs, deletion, freshness, replay, and bounded context. |
| Failure scenarios | Stale summary overwrites a current constraint; private memory leaks across tenants; model treats retrieved text as instruction; vector result lacks source ACL; deletion does not remove derived memory. |
| Enterprise example | In claims handling, the chat transcript supports interaction, the workflow record tracks claim steps, policy documents remain in governed search, and any remembered customer preference has consent, provenance, TTL, and deletion linkage. |

### State taxonomy and storage

| **Information class** | **Scope and examples** | **System of record** | **Rules** |
| --- | --- | --- | --- |
| Conversation context | Recent messages, channel state, current clarification | Conversation service / document DB | Append-only turns; compact with source links; not authoritative business state |
| Workflow state | Current node, variables, child tasks, budgets, approvals | Durable workflow history + relational projection | Strong transition rules; versioned; queryable; replay-safe |
| Durable execution state | Event history, timers, activity results, checkpoint cursor | Workflow engine persistence | Engine-owned; encrypted; retention aligned to run evidence |
| Short-term working memory | Scratch notes, candidate plan, intermediate hypotheses | Run-scoped state or object artifacts | TTL; no automatic cross-run reuse; label confidence and provenance |
| Long-term memory | Approved preferences, reusable facts, learned procedures | Governed memory service / relational + search index | Explicit write policy, consent, provenance, TTL, ACL, correction/deletion |
| Enterprise knowledge | Policies, contracts, code, tickets, records, catalogs | Source systems + governed search/vector/graph indexes | Source remains authoritative; ACL filter before retrieval; freshness and lineage |
| Artifacts | Reports, patches, extracted tables, evidence packages | Versioned object store | Immutable versions, content hash, classification, owner, retention |
| Telemetry and audit | Traces, metrics, policy decisions, effect records | Trace store + SIEM + append-only/WORM archive | Redaction; role-separated access; retention/legal hold |

### Context assembly pipeline

1. Start with agent instructions and policy-owned constraints from pinned versions.
2. Load canonical workflow state and unresolved obligations—not the raw event history.
3. Select the smallest recent conversation window needed for continuity.
4. Retrieve enterprise knowledge only after identity/tenant/ACL filtering; attach source, timestamp, classification, and confidence metadata.
5. Retrieve long-term memory through a separate policy gate; prefer verified facts and user-approved preferences.
6. Remove duplicates, stale items, secrets, and content outside the task purpose; summarize only with links to originals.
7. Label each segment as instruction, user\_input, enterprise\_data, tool\_result, or memory; the model must not promote data into instructions.
8. Record a context-manifest hash on the model span so the call can be reconstructed without logging sensitive plaintext by default.

### Detailed design — APIs, data model, and scalability

### Component boundaries

The Conversation Service owns turns; the Workflow Projection Service owns canonical run state; the Context Assembler creates an ephemeral model-input projection; the Retrieval Broker queries governed knowledge; the Memory Service owns approved cross-run memory; the Provenance Service tracks lineage; and the Compaction Service produces source-linked summaries. No component can silently promote a conversation statement into workflow truth or long-term memory.

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/context:assemble | Build a token-bounded context from pinned instructions, run state, conversation, knowledge, and memory under a policy and data budget |
| GET /v1/runs/{run\_id}/state | Return the canonical typed state projection and state\_version; separate from transcript/history |
| POST /v1/conversations/{id}/turns | Append an immutable user/agent/tool turn with provenance, classification, and client idempotency key |
| POST /v1/knowledge:search | Hybrid search with subject+actor context, source allowlist, freshness, filters, top-k, and required citations |
| POST /v1/memories | Propose/write a governed memory with scope, provenance, confidence, consent, TTL, and deduplication key; policy may require review |
| GET /v1/memories:search | Search only memories visible to the subject/purpose/run; returns confidence and source lineage |
| PATCH /v1/memories/{memory\_id} | Correct via optimistic version; preserves previous version and reason |
| DELETE /v1/memories/{memory\_id} | Create deletion tombstone and enqueue removal from indexes, caches, summaries, and derived artifacts |
| POST /v1/context:compact | Produce a source-linked summary/checkpoint under a target token budget; never overwrites source turns |

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ConversationTurn | conversation/turn IDs, role/type, content reference/hash, producer, created time, classification, source/trace refs; append-only |
| RunStateProjection | run ID, schema/version, state version, variables, obligations, unresolved questions, budgets, artifact refs; derived from workflow history |
| ContextManifest | context ID, run/node/model call, token budget/allocation, policy/version pins, ordered segment refs/hashes, redaction summary, total tokens |
| ContextSegment | segment ID/type, source URI/revision, content hash, trust label, instruction flag, classification, ACL decision, freshness, token count |
| MemoryRecord | memory ID, tenant, subject/team scope, type, canonical value, provenance, confidence, consent, purpose allowlist, TTL, status, supersedes |
| KnowledgeObject | source URI/revision, object/chunk IDs, text/blob reference, embedding version, metadata, ACL pointer, ingestion cursor, deletion state |
| SummarySnapshot | input segment hashes, summary hash/reference, model/prompt version, coverage map, unresolved facts, expiry; immutable |

Example context-manifest shape:

JSON · implementation excerpt

```json
{
  "context_id": "ctx_...",
  "run_id": "run_42",
  "node_id": "n7",
  "budget": {"max_tokens": 24000, "instructions": 3000, "state": 4000, "evidence": 14000, "conversation": 3000},
  "segments": [{
    "kind": "enterprise_data",
    "uri": "doc://policy/91@rev17",
    "sha256": "...",
    "trust": "untrusted-content",
    "acl_decision_id": "dec_...",
    "tokens": 1840
  }],
  "redactions": ["pii:ssn"],
  "manifest_sha256": "..."
}
```

### Retrieval and memory consistency

* The source system revision is authoritative. Index entries are disposable projections and must carry source revision, ACL pointer, ingestion time, and deletion state.
* Search performs tenant/source pruning, exact ACL filtering, hybrid lexical/vector scoring, reranking, freshness filtering, and diversity/deduplication before context selection.
* A memory write is a governed business operation: validate type, scope, consent, provenance, contradiction, retention, and sensitivity. Derived guesses default to run-scoped working memory, not long-term memory.
* Correcting or deleting a source creates lineage events that invalidate affected memories, summaries, embeddings, model caches, and evidence packages according to retention/legal-hold policy.

### Scalability and token economics

* Partition conversations and memories by tenant + subject/team; partition knowledge by tenant + source + region. Use routing metadata so a query touches only eligible partitions.
* Store content in object storage and metadata in relational/search stores. Context APIs exchange references; only the assembler materializes bytes for the authorized model call.
* Run ingestion as an asynchronous CDC/event pipeline with separate extract, classify, ACL, chunk, embed, and index stages. Track independent cursors so failed embedding does not block ACL deletion.
* Cache retrieval candidates by tenant, source revision, normalized query, policy scope, and embedding/reranker version; re-run exact authorization on cache hit.
* Allocate a fixed context budget before retrieval. Use maximum marginal relevance/source diversity, per-source caps, and evidence-quality thresholds rather than filling the entire window.
* Compact long conversations asynchronously and incrementally. Keep recent turns plus source-linked summaries; rebuild summaries when covered inputs change.
* Enforce deletion SLOs across primary metadata, vector/search indexes, caches, and derived summaries. Tombstones must outlive the longest replica/cache lag to prevent resurrection.

|  |
| --- |
| **PERFORMANCE AND COST**  Retrieve less, and cite what you retrieved. Context is the dominant cost in most agentic systems and the dominant cause of distraction. Record a context manifest identifier rather than the context body, and measure answer quality against context size — most systems are past the point where more retrieval helps. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Privacy lifecycle | Context and memory need purpose limitation, consent or other legal basis where applicable, data-subject request handling, deletion propagation, legal-hold precedence, residency, provider retention controls, and proof that derived summaries/indexes were handled too. | NIST-GAI; GDPR |

Evidence anchors: NIST-GAI; GDPR. Full URLs, authority, version, and scope appear in Appendix M.

## Pattern reference — Memory

|  |
| --- |
| **PROBLEM**  The system should reuse useful information across turns or runs without confusing stale summaries with canonical truth or retaining data indefinitely. |

### Architecture and flow

Working memory is run-scoped; long-term memory is a governed write with subject, scope, provenance, confidence, policy basis, TTL, correction, deletion, and retrieval authorization.

1. Identify a candidate reusable fact.
2. Validate evidence, subject, purpose, consent or policy basis, and sensitivity.
3. Write a versioned memory record with TTL and provenance.
4. Retrieve only after authorization and trust labeling.
5. Correct, supersede, expire, or delete through propagation workflows.

| **Use when** | **Do not use when** |
| --- | --- |
| Use for stable preferences, repeated domain facts, or learned operational hints with clear value and governance. | Do not persist transient chain-of-thought, secrets, unverified hypotheses, protected data without basis, or facts already authoritative elsewhere. |

### Trade-offs

| **Choice** | **Consequence** |
| --- | --- |
| Continuity | Creates privacy, staleness, correction, and deletion obligations. |
| Reduced context cost | May lose nuance or introduce summary drift. |

### Failures and controls

| **Failure** | **Control** |
| --- | --- |
| Stale memory overrides state | Canonical state precedence and freshness checks. |
| Cross-tenant leakage | Tenant-partitioned keys and authorization before retrieval. |
| Deletion gaps | Lineage graph, tombstones, cache invalidation, and rebuild. |

### Minimum observability

* memory ID and version
* source provenance
* scope and tenant
* policy basis
* confidence and TTL
* retrieval and deletion events

## Implementation reference


### Auditable context projection

PYTHON · implementation excerpt

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class ContextSegmentRef(BaseModel):
    artifact_id: str
    source_revision: str
    sha256: str
    authorization_decision_id: str
    trust_role: Literal["instruction", "user_intent", "evidence"]
    token_count: int


class ContextManifest(BaseModel):
    context_id: str
    run_id: str
    release_id: str
    policy_version: str
    segments: tuple[ContextSegmentRef, ...]
    omitted_candidate_ids: tuple[str, ...]
    created_at: datetime
```

### Cross-boundary artifact adoption policy

PYTHON · implementation excerpt

```python
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class ArtifactDescriptor(BaseModel):
    artifact_id: str
    tenant_id: str
    data_classes: frozenset[str]
    region: str
    allowed_purposes: frozenset[str]
    provenance_digest: str
    expires_at: datetime
    legal_hold: bool = False


class AdoptionPolicy(BaseModel):
    tenant_id: str
    allowed_data_classes: frozenset[str]
    allowed_regions: frozenset[str]
    purpose: str
    trusted_provenance_digests: frozenset[str]


def authorize_artifact_adoption(
    artifact: ArtifactDescriptor, policy: AdoptionPolicy, *, now: datetime
) -> None:
    if artifact.tenant_id != policy.tenant_id:
        raise PermissionError("cross-tenant artifact adoption denied")
    if not artifact.data_classes <= policy.allowed_data_classes:
        raise PermissionError("artifact classification exceeds policy")
    if artifact.region not in policy.allowed_regions:
        raise PermissionError("artifact region is not allowed")
    if policy.purpose not in artifact.allowed_purposes:
        raise PermissionError("artifact purpose is not allowed")
    if artifact.provenance_digest not in policy.trusted_provenance_digests:
        raise PermissionError("artifact provenance is not trusted")
    if now > artifact.expires_at and not artifact.legal_hold:
        raise PermissionError("artifact expired")
```

## Debugging playbook

1. Reconstruct one ContextManifest without relying on logged plaintext.
2. Compare canonical state with summaries and working memory.
3. Trace a corrected or deleted fact through indexes, cache, memory, and artifacts.

## Production checklist

**✓** Conversation, workflow state, working memory, long-term memory, knowledge, artifacts, telemetry, and audit are separate domains.

**✓** Authorization occurs before content materialization.

**✓** Context records ordered references, hashes, trust labels, decisions, versions, redactions, and token allocation.

**✓** Memory creation is a governed write with scope, provenance, confidence, lawful basis, TTL, correction, and deletion.

**✓ Final implementation and deletion propagate through indexes, caches, summaries, memories, contexts, and artifacts.**

## Exercises

1. Design a token budget across instructions, state, evidence, memory, and reserve.
2. Define the lifecycle of a reusable supplier preference memory.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why call the prompt a projection rather than state? | It is a temporary, token-bounded view assembled from authoritative stores for one model call; it can be rebuilt, audited by reference, and discarded. |
| How do conversation, knowledge, working memory, and long-term memory differ? | Interaction history; source-backed enterprise facts; run-scoped hypotheses; and approved reusable facts—each with different ownership, retention, authority, and deletion. |
| What problem does a ContextManifest solve? | Reproducibility and diagnosis through ordered source, version, and hash references, authorization decisions, trust labels, redactions, and budget without logging all plaintext. |
| How should retrieved instructions be handled? | As untrusted data with provenance and taint; they cannot alter system instructions, tool eligibility, policy, credentials, or destination grants. |
| How do you delete a fact from an agentic system? | Tombstone and revoke the source, remove derived indexes, invalidate caches, rebuild summaries and contexts, clean governed memory and affected artifacts, and preserve permitted audit evidence. |


## Transition to Chapter 23

Context and state are bounded; Chapter 23 determines whose authority may flow through the system and how that authority narrows across hops.

# 23 — Identity, RBAC/ABAC, and Delegated Authorization

> **Evidence note.** The delegated-authority examples use OAuth token exchange, resource indicators, and protected-resource metadata as protocol building blocks; deployment still requires workload-specific issuer, audience, proof, revocation, and policy controls. [R08][R09][R10]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  A procurement user starts the run, a platform agent reasons, a connector calls an ERP, and a specialist agent receives a child task. Northstar must preserve both initiating subject and acting workload without turning a broad user token into ambient authority. |

|  |
| --- |
| **DESIGN DECISION**  Carry subject plus actor identity; exchange for short-lived last-hop credentials only after exact resource authorization. |

## What this chapter delivers

Carry subject and actor identity end to end and prove that every delegated grant is narrower.

## Solution blueprint


Figure 15. Identity, RBAC/ABAC, and Delegated Authorization.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Policy Engine and security-token service | subject/actor to protected resource | policy shard · tenant · resource | one decision and lease | CapabilityEnvelope · PolicyDecision · CredentialLease |

## Subject, actor, and purpose

Every protected request carries the initiating **subject**, acting **workload**, purpose, tenant, capability envelope, and trace/run identifiers. RBAC supplies coarse role membership; ABAC evaluates resource, purpose, data class, risk, region, time, and current state. Neither the model nor a remote agent invents these attributes.

A child grant is derived by intersection, not by copying the parent token. It shortens lifetime and delegation depth and narrows actions, resources, data classes, regions, risk, and budget. Immediately before a tool call, the gateway canonicalizes the exact resource and reauthorizes it. Only then does a security-token service mint a short-lived audience-bound credential lease for the connector.

Authorization caches must fail safely. Keys include tenant, subject, actor, resource version or ACL epoch, purpose, policy version, action, and relevant context. Revocation and policy updates invalidate or bypass stale positive decisions. After a long wait, authorization is recomputed.

## Enterprise data access, identity, and delegated authorization

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Let agents act across enterprise systems without exceeding the initiating user’s rights or collapsing all access into a powerful shared bot account. |
| Why it is difficult | Identity crosses user, service, agent, tool, and vendor boundaries; source systems express permissions differently; long runs outlive tokens; service credentials can erase user accountability. |
| Design alternatives | Shared service account; user token passthrough; impersonation; on-behalf-of/token exchange; capability tokens; brokered connector with policy enforcement. |
| Recommended architecture | Carry a dual principal: subject (initiating user/system) and actor (agent/workload). At each hop, intersect requested scope with user grants, agent policy, tool policy, resource policy, tenant, purpose, risk, and current context. Mint a short-lived audience-bound credential for one downstream resource/action; never forward the inbound token. |
| Trade-offs | Fine-grained delegation increases identity-plane complexity and may require connector-specific adapters. It sharply reduces blast radius and makes audit attribution possible. |
| Failure scenarios | Confused deputy; cross-tenant retrieval; stale group membership; token logged in a trace; sub-agent gets parent’s broad credential; background run continues after user access is revoked. |
| Enterprise example | A sales agent may read accounts the user can view, but updating pricing requires an attribute-based policy and manager approval; the CRM connector receives a five-minute token scoped to that account and operation. |

### Authorization decision

Every retrieval, delegation, tool call, memory write, and publication evaluates a tuple:

allow(subject, actor, action, resource, tenant, purpose, data\_class, environment, risk, run\_id, time, device/session assurance, requested\_scope)

The effective permission is the intersection—not the union—of all applicable grants. Explicit deny wins. Cache only low-risk decisions for short periods and invalidate on identity or policy change.

### Identity propagation sequence

### Data-plane controls

* Resolve tenant before any search; enforce row, document, and field-level authorization *before* retrieval or embedding results reach the model.
* Separate indexes, encryption keys, namespaces, queues, caches, and rate limits by tenant or by risk tier; use database row-level security as defense in depth.
* Bind credentials to audience and preferably sender; rotate frequently; store only handles in workflow state; refresh after long waits and re-check revocation.
* Use workload identity (for example SPIFFE/SVID or cloud workload federation) so workers do not carry static secrets.
* Run the policy decision point independently from the LLM. OPA/Rego, Cedar/Verified Permissions, or a comparable engine can express RBAC/ABAC and emit replayable decision logs.
* Treat document-level ACL changes as index invalidation events. Never assume a vector store filter alone is sufficient if the source of truth denies access.

### Detailed design — APIs, data model, and scalability

### Component boundaries

| **Component** | **Responsibility** |
| --- | --- |
| Identity Adapter | Validate enterprise user/session claims and normalize subject identity |
| Workload Identity Agent | Attest runtime and issue/rotate workload credentials |
| Authorization Service/PDP | Evaluate RBAC/ABAC/relationship/purpose policies and obligations |
| Access Broker/STS | Exchange subject+actor context for one audience-bound, downscoped credential |
| Connector Gateway/PEP | Enforce decisions, inject credentials, validate resources/effects, and strip secrets |
| Entitlement Indexer | Convert source ACL/group changes into queryable snapshots and invalidation events |
| Data Access Broker | Run policy-filtered search/query against sources and return provenance-rich references |

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/authorization:check | Evaluate one subject+actor+action+resource request; returns allow/deny, obligations, reason, policy version, TTL, and decision ID |
| POST /v1/authorization:batchCheck | Vectorized filtering for retrieval candidates; preserves per-resource decision IDs |
| POST /v1/capability-envelopes | Create the maximum run authority from user consent, agent policy, tenant policy, risk, and purpose |
| POST /v1/credentials:exchange | Internal-only exchange of an approved grant for a short-lived audience/resource/action token or opaque credential handle |
| POST /v1/data:query | Execute a typed source query with tenant, purpose, filters, projection, limit, freshness, and authority envelope |
| POST /v1/data:retrieve | Hybrid retrieval; performs pre-retrieval ACL filtering and returns source revision, classification, and provenance per item |
| POST /v1/grants/{grant\_id}:revalidate | Recheck membership, revocation, purpose, policy version, and remaining lifetime before resume or high-risk use |
| POST /v1/grants/{grant\_id}:revoke | Revoke a run or child grant and emit cancellation/re-evaluation events to affected workflows |

Representative authorization response:

JSON · implementation excerpt

```json
{
  "decision_id": "dec_...",
  "allowed": true,
  "effective_scope": ["crm.account:read:acct_17"],
  "obligations": ["redact:ssn", "log:regulated", "approval:pricing-write"],
  "policy_version": "enterprise-agent@2026.09.3",
  "valid_until": "2026-09-11T03:05:00Z",
  "cacheable": false
}
```

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| PrincipalChain | tenant, subject ID/type, actor workload/agent ID, delegation chain, assurance, auth time; chain is append-only and depth bounded |
| CapabilityEnvelope | grant ID, run/task, permitted actions/resources/data classes, explicit denies, purpose, regions, max risk, expiry, parent grant; child is a provable subset |
| PolicyDecision | decision ID, input hash, result, obligations, reason codes, policy digest, identity/entitlement versions, evaluated time; immutable |
| CredentialLease | opaque handle, grant/decision IDs, audience, resource/action scope, issue/expiry, sender binding, status; secret/token body is never stored in run state |
| ResourceDescriptor | canonical resource URI, tenant, owner/source, type, classification, region, ACL/version, relationship attributes |
| EntitlementSnapshot | subject/group/resource relationship, source revision, effective interval, ingestion cursor, stale-after |
| AccessEvent | decision, connector, downstream request/audit ID, bytes/records, redactions, result, trace ID |

### Consistency and revocation policy

* Writes, R3/R4 actions, secret access, external publication, and post-wait resumes require a current online decision. Low-risk reads may use a short, policy-bounded cache if the source and tenant permit it.
* Cache keys include tenant, subject, actor, action, canonical resource, purpose, policy digest, entitlement version, and assurance—not merely user and role.
* Group/ACL/policy changes emit invalidation events. The authorization service maintains a high-water mark per source; if freshness exceeds the action’s tolerance, deny or query the source of truth.
* Connector calls preserve both subject and actor in downstream claims or audit metadata. When a source cannot express delegated identity, the gateway records the mapping and compensating control; it does not pretend service-account access is user delegation.

### Scalability and isolation

* Keep PDP instances stateless and horizontally scalable; distribute signed policy bundles and keep tenant/resource relationship data in a partitioned authorization store.
* Batch authorization for search results and field projections to avoid one network call per chunk. Apply coarse candidate pruning first, then exact resource checks before returning content.
* Partition entitlement and resource data by tenant + source, with regional replicas inside residency boundaries. Large enterprise group expansion should use indexed relationships rather than embedding group lists in tokens.
* Isolate connectors by source, tenant tier, and risk. Apply per-connector queues, circuit breakers, concurrency caps, and rate-limit feedback to planners.
* Use independent encryption keys and audit streams for high-risk tenants. A shared physical service is acceptable only when tenant binding is enforced at every API, data partition, cache key, trace, and credential exchange.
* Model a regional IdP/STS outage explicitly: existing low-risk read grants may follow a documented grace policy, while new or mutating grants fail closed and runs checkpoint for later resume.

|  |
| --- |
| **SECURITY AND GOVERNANCE**  Delegation must narrow monotonically. A sub-agent may act for a different actor, but never for a broader subject, resource set, or action set than its parent held. Prove the narrowing in code at each handoff; a chain that can widen anywhere can widen everywhere. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Non-human identity | Workload identity proves the actor; delegation proves whose authority and purpose it uses. Rotate and revoke both credentials and capability grants. A valid service identity is not sufficient authorization. | RFC8693; MCP-AUTH |

Evidence anchors: RFC8693; RFC8707. Full URLs, authority, version, and scope appear in Appendix M.

## Implementation reference


### Capability-envelope subset proof

PYTHON · implementation excerpt

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def _resource_within(child: str, parent: str) -> bool:
    if parent.endswith("://"):
        return child.startswith(parent)
    normalized = parent.rstrip("/")
    return child == normalized or child.startswith(normalized + "/")


@dataclass(frozen=True)
class CapabilityEnvelope:
    grant_id: str
    subject_id: str
    actor_id: str
    actions: frozenset[str]
    resource_prefixes: frozenset[str]
    purposes: frozenset[str]
    data_classes: frozenset[str]
    regions: frozenset[str]
    maximum_risk: int
    maximum_cost_usd: float
    delegation_depth: int
    expires_at: datetime

    def assert_current(self, now: datetime | None = None) -> None:
        current = now or datetime.now(timezone.utc)
        if self.expires_at <= current:
            raise PermissionError("capability envelope expired")


def derive_child(
    parent: CapabilityEnvelope,
    child: CapabilityEnvelope,
    *,
    now: datetime | None = None,
) -> CapabilityEnvelope:
    """Prove monotonic narrowing; actor identity may change, subject may not."""

    parent.assert_current(now)
    if child.subject_id != parent.subject_id:
        raise PermissionError("subject cannot change")
    if not child.actions <= parent.actions:
        raise PermissionError("actions broadened")
    if not child.purposes <= parent.purposes:
        raise PermissionError("purposes broadened")
    if not child.data_classes <= parent.data_classes:
        raise PermissionError("data classes broadened")
    if not child.regions <= parent.regions:
        raise PermissionError("regions broadened")
    if child.maximum_risk > parent.maximum_risk:
        raise PermissionError("risk ceiling raised")
    if child.maximum_cost_usd > parent.maximum_cost_usd:
        raise PermissionError("cost ceiling raised")
    if child.delegation_depth >= parent.delegation_depth:
        raise PermissionError("delegation depth was not reduced")
    if child.expires_at > parent.expires_at:
        raise PermissionError("lifetime extended")
    for resource in child.resource_prefixes:
        if not any(_resource_within(resource, allowed) for allowed in parent.resource_prefixes):
            raise PermissionError("resource scope broadened")
    return child
```

## Debugging playbook

1. Trace subject, actor, purpose, grant, policy version, and credential lease end to end.
2. Canonicalize the exact resource and recompute child subset checks.
3. Simulate role revocation during a wait and verify post-wait denial.

## Production checklist

**✓** Both initiating subject and acting workload cross every protected boundary.

**✓** Delegated authority is a bounded capability envelope, never a reusable bearer credential.

**✓** Child grants narrow actions, resources, purpose, data class, region, risk, time, budget, and delegation.

**✓** Exact action and resource are reauthorized at the gateway before a last-hop credential is minted.

**✓** Revocation, freshness, cache invalidation, post-wait revalidation, and tenant isolation are first-class.

## Exercises

1. Create a capability envelope for a read-only specialist task.
2. Write tests that attempt purpose, resource, region, risk, and time escalation.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why preserve both subject and actor identity? | The subject provides delegated user or system authority; the actor identifies the workload performing the action, enabling policy, attribution, and confused-deputy defense. |
| What is the difference between a capability envelope and a credential? | The envelope states maximum allowed scope and lineage; a credential is short-lived proof minted for one audience, action, and resource and delivered only to the connector. |
| How do you prove a child grant is safe? | Verify subset or intersection across actions, canonical resources, purposes, data classes, regions, risk, expiry, budget, and delegation depth with explicit deny precedence. |
| Why reauthorize after a long wait? | User roles, ACLs, policy, resource state, risk, and credentials may have changed; original admission is not perpetual authority. |
| Where must authorization occur in retrieval? | Before content reaches the model, with tenant and source routing, exact resource and field checks, freshness, redaction obligations, and provenance. |


## Transition to Chapter 24

Identity and delegated authority answer who may ask; Chapter 24 proves whether a specific tool effect may execute, commit, retry, or recover.

# 24 — Tool Security, Effects, Idempotency, and Approval

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  The ERP times out after Northstar requests supplier creation. Retrying might duplicate the supplier; treating the call as failed might cause conflicting remediation. The platform records an unknown effect and reconciles before continuing. |

|  |
| --- |
| **DESIGN DECISION**  Use one logical effect key, intent hash, expected version, downstream request ID, receipt, and reconciliation state per mutation. |

## What this chapter delivers

Make external writes replay-safe through manifests, exact authorization, logical effect keys, preconditions, receipts, and reconciliation.

## Solution blueprint


Figure 16. Tool Security, Effects, Idempotency, and Approval.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Tool Gateway, Effect Ledger, domain writer | agent intent to external mutation | logical effect key · connector | one business effect | EffectRecord · EffectReceipt · ReconciliationTask |

## The effect protocol

A protected mutation moves through Reserved → Executing → Committed, with branches for Declined, Unknown, Partial, Compensating, Compensated, and InterventionRequired. The logical effect key represents business intent; the intent hash prevents the key from being reused for a different action. An expected version prevents valid intent from overwriting newer state.

The gateway persists Executing before the downstream call and includes a stable idempotency key when supported. Success is not inferred from HTTP 200 alone; a receipt includes downstream resource ID, resulting version, response hash, timestamp, and verification evidence. After timeout, the state becomes Unknown, dependent actions stop, and a reconciler queries the downstream system using request ID, idempotency key, or business predicates.

Approval and effect control are complementary. Approval proves a person authorized the proposal; it does not prove the write happened once. Idempotency prevents duplicate intent; it does not prevent stale overwrite. A robust protected write often needs all three: proposal-bound approval, idempotency, and optimistic concurrency.

## Tool and capability management

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Agents need broad connectivity, but each tool expands the attack surface, authorization surface, and number of ways a model can cause irreversible harm. |
| Why it is difficult | Tool descriptions are part API design and part model interface; discovery can expose dangerous capabilities; schemas and downstream semantics change; model-generated arguments may be syntactically valid but unsafe. |
| Design alternatives | In-process functions; direct SaaS SDKs; plugin registry; MCP servers; API gateway wrappers; isolated remote capabilities; browser/computer use. |
| Recommended architecture | Put every capability behind a Tool Gateway and immutable registry. Discovery returns only tools allowed for the run. Invocation follows validate → authorize → optionally preview/approve → mint credential → execute in isolation → verify effect → sanitize result → record telemetry. |
| Trade-offs | A gateway adds latency and implementation work, but centralizes policy, secret brokering, quotas, compatibility, and effect semantics while allowing multiple agent frameworks. |
| Failure scenarios | Tool-name collision; schema drift; prompt injection selects an admin tool; timeout hides a committed effect; unrestricted browser exfiltrates data; malicious MCP server returns instructions or captures tokens. |
| Enterprise example | An HR assistant sees a read-only employee lookup tool by default. Compensation change is a separate high-risk tool with field constraints, dual approval, idempotency, and a connector-specific scoped token. |

### Required ToolManifest fields

| **Field group** | **Required contents** |
| --- | --- |
| Identity | tool\_id, semantic version, owner, implementation digest, environment |
| Interface | Purpose, JSON input/output schemas, examples, error schema, compatibility range |
| Security | Authentication mode, required scopes, resource model, tenant behavior, data classes |
| Risk | read\_only, reversible, idempotent, destructive, financial/legal impact, approval policy |
| Runtime | Timeout, retry class, concurrency key, rate limit, sandbox profile, egress allowlist |
| Effects | Idempotency-key location, precondition/version field, effect receipt, compensation tool |
| Operations | SLO, health endpoint, trace semantics, cost unit, deprecation date, support contact |

### Risk classes

| **Class** | **Capability** | **Default control** |
| --- | --- | --- |
| R0 | Pure deterministic transform | Schema validation and resource limits |
| R1 | Read approved low-sensitivity data | User-scoped authorization and audit |
| R2 | Read sensitive data or write reversible draft | Fine-grained policy, DLP, explicit destination scope |
| R3 | External communication or material reversible change | Preview, user confirmation/approval, idempotency, effect verification |
| R4 | Irreversible, privileged, financial, legal, production, or safety-critical action | Deterministic service owns commit; dual control or out-of-band approval; agent may only propose |

Use MCP as an interoperability surface for tools and resources, not as the authorization authority. The gateway must validate audience-bound tokens, prohibit token passthrough, isolate untrusted servers, and apply enterprise policy independently of protocol-level OAuth.

### Detailed design — APIs, data model, and scalability

### Component boundaries

| **Component** | **Responsibility** |
| --- | --- |
| Tool Registry | Immutable manifests, versions, owners, compatibility, risk and lifecycle |
| Discovery Service | Return the smallest policy-eligible capability set for a run/node |
| Tool Gateway | Validate, authorize, rate-limit, dispatch, sanitize, and trace every invocation |
| Credential Broker | Mint or fetch one short-lived downstream credential after authorization |
| Connector Runtime | Translate canonical requests/errors/effect semantics to a source-specific API |
| Sandbox Broker | Lease isolated code/browser environments with resource and egress policy |
| Effect Service | Allocate logical effect IDs, deduplicate, store receipts, reconcile, and compensate |
| Health/Quota Service | Track provider limits, latency, error state, breaker status, and queue pressure |

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/tools:discover | Return manifests eligible for subject, actor, run, plan node, risk, data class, region, and remaining budget |
| GET /v1/tools/{tool\_id}/versions/{version} | Resolve immutable schema, risk/effect contract, compatibility, and digest |
| POST /v1/tools/{tool\_id}:preview | Validate arguments, resolve target, calculate before/after diff and impact without committing |
| POST /v1/tools/{tool\_id}:invoke | Invoke with run/node IDs, manifest version, typed arguments, authority grant, idempotency key, precondition, deadline, and trace context |
| GET /v1/invocations/{invocation\_id} | Return asynchronous status, attempts, sanitized result, and effect state |
| POST /v1/invocations/{invocation\_id}:cancel | Best-effort cancel execution; reports whether an external effect may already exist |
| GET /v1/effects:lookup?tool\_id=...&idempotency\_key=... | Find prior logical effect before a retry |
| POST /v1/effects/{effect\_id}:reconcile | Query downstream system and move unknown to verified committed/declined/partial state |
| POST /v1/effects/{effect\_id}:compensate | Start an authorized compensating workflow; never deletes the original receipt |

Invocation behavior:

* Return 200 only for short, completed pure/read operations with no unresolved effect.
* Return 202 plus an operation URL for long-running, queued, browser/code, or mutating work.
* Return a typed policy denial, validation error, capacity response, dependency error, or effect\_unknown; do not collapse every failure into free-form text.

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| ToolVersion | tenant/global tool ID, semantic version, manifest/content/image digest, schemas, owner, risk/effect metadata, auth type, limits, lifecycle state; immutable after release |
| ToolEligibility | run/node, tool version, decision ID, constraints, valid-until; discovery cache only, not final invocation authorization |
| ToolInvocation | invocation ID, tenant/run/node, logical key, tool version, arguments hash/ref, grant/decision, state, deadline, attempt count, queue, trace |
| InvocationAttempt | invocation ID/attempt, worker/connector, credential lease, start/end, normalized error, downstream request ID, response hash/ref |
| EffectRecord | effect ID, tenant, tool, idempotency key, target resource, intent hash, precondition, state, downstream IDs, before/after versions, receipt, compensation |
| SandboxLease | lease ID, immutable image/profile, run/node, CPU/memory/time/disk/network limits, egress grants, start/expiry, attestation |
| ToolHealth | tool/provider/region, rolling latency/error/quota, breaker state, observed time, freshness |

A unique constraint on (tenant\_id, tool\_id, idempotency\_key) protects logical effects. The arguments hash must match on reuse; the same key with different intent is a conflict, not a retry.

### Invocation sequence

### Scalability and operations

* Keep registry/discovery/gateway front ends stateless. Cache immutable manifests by digest and distribute them regionally; always perform a current authorization check at invocation.
* Partition invocation and effect records by tenant + tool, but route all uses of one logical idempotency key to the same consistency domain.
* Use dedicated queues/pools for read connectors, write connectors, browser/code sandboxes, high-risk operations, and very slow providers. Enforce fairness and reservations independently.
* Exchange large inputs/outputs through authorized object references. Queue messages carry IDs, hashes, classification, and deadlines—not document bodies.
* Apply concurrency and rate limits at organization, tenant, run, tool, connector account, target resource, and provider levels. Feed retry-after and breaker state back to the scheduler.
* Prewarm only common sandbox images; use immutable snapshot pools and capped warm capacity. Scrub or destroy every lease, and never reuse tenant-writable layers across trust boundaries.
* Publish health changes as events so planners avoid unavailable tools before dispatch. Do not allow a model to bypass a breaker by selecting a semantically identical unapproved endpoint.
* Separate gateway availability from connector availability: if a connector is degraded, queue within bounded age or return capacity status so the workflow can wait, degrade, or escalate.

|  |
| --- |
| **DEVELOPER GUIDELINE**  Give every tool a versioned manifest: interface, risk class, whether it mutates, whether it needs approval, and its timeout. Resolve the manifest at dispatch, not at import. A tool whose risk class lives only in a reviewer's memory cannot be enforced, audited, or safely changed. |

## Reliability and failure handling

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Preserve correct outcomes despite nondeterministic models, partial infrastructure failures, duplicates, rate limits, and uncertain external effects. |
| Why it is difficult | A timeout does not reveal whether an external mutation committed; retries can amplify harm; model failures may be semantic rather than exceptions; cross-system transactions rarely exist. |
| Design alternatives | Best-effort retries; queue redelivery; distributed transactions; idempotent activities; effect ledger; saga compensation; reconciliation; human exception queue. |
| Recommended architecture | Classify every operation by effect semantics. Use bounded exponential backoff with jitter for transient failures; stable idempotency keys; outbox/inbox; precondition versions; effect receipts; sagas and reconciliation for multi-system changes; circuit breakers and provider fallbacks tested in advance. |
| Trade-offs | Reliability metadata and compensation increase implementation work. They are the cost of safely connecting probabilistic planners to real systems. |
| Failure scenarios | Duplicate refund; two runs edit the same case; fallback model violates output schema; compensating action itself fails; poison event cycles forever; global retry storm. |
| Enterprise example | An invoice agent creates a payment proposal with an idempotency key, checks ledger version, awaits approval, submits once, reconciles provider receipt, and opens an exception case if final state is ambiguous. |

### Failure policy matrix

| **Failure** | **Default response** | **Never do** |
| --- | --- | --- |
| Model 429/5xx | Retry with jitter under per-provider budget; route only to an evaluated compatible fallback | Retry every branch simultaneously |
| Invalid structured output | One constrained repair attempt, then fallback or fail | Silently coerce materially ambiguous fields |
| Tool transient error before effect | Retry if manifest declares safe/idempotent | Assume all reads and writes are equivalent |
| Timeout with unknown effect | Query by idempotency key or reconcile effect ledger before retry | Blindly repeat the mutation |
| Optimistic concurrency conflict | Reload authorized current version and replan/merge | Last-write-wins on business records |
| Child task failure | Apply join policy: fail-fast, quorum, substitute, partial, or escalate | Let the child choose parent outcome |
| Poison message | Bound attempts, quarantine with evidence, alert owner | Infinite redelivery |
| Policy denial | Stop that path; explain permitted alternatives | Ask the model to reinterpret the policy |
| Budget exhausted | Checkpoint, produce partial result, request budget extension if allowed | Hide overrun or continue on a different account |
| Compensation failure | Mark InterventionRequired, freeze dependent effects, page operator | Claim rollback succeeded |

### Reliability mechanics

* **Timeout hierarchy:** model/tool request \< activity \< child task \< stage \< overall run. A parent timeout must not silently abandon a still-running child.
* **Retry ownership:** exactly one layer owns retries for a given failure; otherwise SDK, gateway, queue, and workflow retries multiply.
* **Idempotency:** derive keys from tenant + run + logical effect, persist before invocation, and return an effect receipt containing downstream request and resource IDs.
* **Concurrency:** use optimistic versions for records. Use short distributed leases only to coordinate scarce work; never hold a lock across model calls or human waits.
* **Sagas:** define forward and compensating activities. Compensation is a business action, not history deletion; keep both in the audit trail.
* **Circuit breaking:** break by provider/tool/tenant/risk class; expose health to the planner so it selects only evaluated alternatives.
* **Graceful degradation:** degrade from write → draft, deep analysis → partial evidence, premium model → approved fallback, live data → clearly labeled cached data. Never degrade authorization, tenant isolation, or audit.

### Detailed design — APIs, data model, and scalability

### Component boundaries

The workflow engine owns retry timing and saga order; the Effect Service owns idempotency and external outcome state; Outbox/Inbox adapters own atomic publication and consumer deduplication; the Reconciliation Service resolves unknown outcomes; the Compensation Executor performs domain reversals; the Dependency Health Service owns breakers; and the Exception Service owns manual intervention cases.

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/effects:begin | Atomically allocate/load a logical effect using tenant, tool, idempotency key, intent hash, target, and precondition |
| POST /v1/effects/{effect\_id}:recordReceipt | Append signed/verified downstream receipt and transition with expected effect version |
| POST /v1/effects/{effect\_id}:markUnknown | Record timeout/transport ambiguity and prohibit blind reinvocation |
| POST /v1/effects/{effect\_id}:reconcile | Start/query a deterministic reconciliation strategy using downstream request/idempotency/resource data |
| POST /v1/effects/{effect\_id}:compensate | Start the versioned compensation workflow after fresh authorization |
| POST /v1/dependencies/{dependency\_id}:report | Internal health signal used to update breaker/admission/routing state |
| GET /v1/dependencies/{dependency\_id}/availability | Return current breaker, quota, latency, and evaluated fallback routes |
| POST /v1/exceptions | Open idempotent operator case with run/effect, evidence, severity, owner, and prohibited automatic actions |
| POST /v1/dlq/{message\_id}:redrive | Redrive only after schema/policy/version checks; produces a new delivery attempt linked to the quarantine record |

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| EffectRecord | effect ID/version, tenant, logical key, intent hash, target/precondition, state, invocation IDs, downstream IDs, before/after versions, receipt and compensation refs |
| OutboxRecord | aggregate/id/version, event ID/type/schema, payload ref/hash, destination, created/published attempts; written in same DB transaction as aggregate change |
| InboxReceipt | consumer, source/event ID, payload hash, status, first/last seen, processing result; unique (consumer, source, event\_id) |
| RetryPolicy | failure class, owner layer, max attempts/elapsed time, exponential parameters, jitter, retryable codes, budget and breaker interaction |
| CompensationStep | saga/effect, reverse capability/version, prerequisite, state/attempt, receipt, irreversibility notes |
| ReconciliationCase | effect, strategy/version, evidence, observations, next check, terminal conclusion, human case |
| CircuitState | dependency/scope, closed/open/half-open, counters/windows, opened-until, probe budget, version |
| QuarantineRecord | original message/ref/hash, error history, schema/policy versions, owner, resolution/redrive links; immutable evidence |

### Effect state machine

### Transaction boundaries

* In a local database transaction, update the aggregate/effect state and insert its outbox event together. A publisher retries until the broker acknowledges; consumers deduplicate in an inbox before applying state.
* An external API call cannot share that transaction. Use preconditions and idempotency, then store/reconcile the external receipt. “Exactly once” is a business protocol, not a queue setting.
* A workflow transition that depends on an effect reads the Effect Service’s verified state; a model/tool return string is not sufficient proof.
* Compensation is separately authorized against current state and may itself be idempotent, fail, or require human approval.

### Scalability and resilience

* Partition effect/outbox/inbox data by tenant + logical target/tool. Maintain the idempotency unique index in the same shard that accepts begin.
* Stream outbox records by monotonically increasing shard cursor; avoid a single global publisher. Track oldest unpublished age and backlog bytes as primary SLOs.
* Run reconcilers as queue workers grouped by downstream provider and strategy. Apply strict per-provider concurrency and spread checks with jitter to avoid recovery storms.
* Scope circuit breakers correctly: global provider, region, tenant account, endpoint, or operation. Over-broad breakers cause unnecessary outage; over-narrow breakers fail to protect the dependency.
* Bound every retry by attempt, elapsed time, spend, and deadline. A shared retry budget across workflow, SDK, gateway, and connector prevents multiplicative retries.
* Separate quarantine storage from live queues. Redrive in controlled batches with canaries; compare schema/policy/tool versions and regenerate credentials.
* Replicate effect metadata for DR but preserve one writer for a logical key. After regional failover, reconcile all Executing/Unknown effects before releasing dependent mutations.
* Use append-only receipts and state-transition records for audit, plus compact current projections for fast lookup. Archive old evidence by retention class without deleting required idempotency tombstones.

|  |
| --- |
| **SECURITY AND GOVERNANCE**  Authorize at invocation, against the end user's grant — never against the agent's own identity. A service account broad enough for every tool is a confused deputy waiting for a prompt injection. Narrow the grant per run, pass it explicitly, and re-check it at the tool boundary rather than at the start of the conversation. |

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Effect correctness | Idempotency is scoped to one stable logical intent. Reusing a key with different arguments is a conflict; retrying an unknown write is prohibited until reconciliation establishes committed or absent. | OUTBOX; CLOUDEVENTS |

Evidence anchors: OUTBOX; CLOUDEVENTS. Full URLs, authority, version, and scope appear in Appendix M.

## Implementation reference


### Effect-state ledger

PYTHON · implementation excerpt

```python
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from typing import Literal

EffectState = Literal["reserved", "executing", "committed", "declined", "unknown",
                      "compensating", "compensated", "intervention_required"]

class EffectConflict(RuntimeError): pass
class EffectOutcomeUnknown(RuntimeError): pass

@dataclass(frozen=True)
class EffectRecord:
    logical_key: str
    intent_hash: str
    state: EffectState
    receipt: dict[str, object] | None = None
    downstream_request_id: str | None = None
    reconciliation_evidence: dict[str, object] | None = None

class InMemoryEffectLedger:
    """Reference implementation; production uses a transactional durable store."""
    def __init__(self) -> None: self._records: dict[str, EffectRecord] = {}
    @staticmethod
    def hash_intent(intent: dict[str, object]) -> str:
        payload=json.dumps(intent,sort_keys=True,separators=(",",":"),default=str).encode()
        return "sha256:"+hashlib.sha256(payload).hexdigest()
    def begin(self, logical_key: str, intent: dict[str, object]) -> EffectRecord:
        digest=self.hash_intent(intent); existing=self._records.get(logical_key)
        if existing:
            if existing.intent_hash != digest: raise EffectConflict("logical key reused with a different intent")
            return existing
        record=EffectRecord(logical_key,digest,"reserved"); self._records[logical_key]=record; return record
    def _transition(self,key:str,allowed:set[str],state:EffectState,**changes) -> EffectRecord:
        current=self._records[key]
        if current.state not in allowed: raise EffectConflict(f"cannot move {current.state} to {state}")
        updated=replace(current,state=state,**changes); self._records[key]=updated; return updated
    def mark_executing(self,key:str,request_id:str)->EffectRecord:
        return self._transition(key,{"reserved"},"executing",downstream_request_id=request_id)
    def mark_committed(self,key:str,receipt:dict[str,object])->EffectRecord:
        return self._transition(key,{"executing","unknown"},"committed",receipt=dict(receipt))
    def mark_unknown(self,key:str)->EffectRecord:
        return self._transition(key,{"executing"},"unknown")
    def mark_declined(self,key:str,receipt:dict[str,object]|None=None)->EffectRecord:
        return self._transition(key,{"reserved"},"declined",receipt=dict(receipt or {}))
    def reconcile(self,key:str,*,outcome:Literal["committed","absent","unprovable"],evidence:dict[str,object])->EffectRecord:
        if outcome=="committed": return self._transition(key,{"unknown"},"committed",receipt=dict(evidence),reconciliation_evidence=dict(evidence))
        if outcome=="absent": return self._transition(key,{"unknown"},"declined",reconciliation_evidence=dict(evidence))
        return self._transition(key,{"unknown"},"intervention_required",reconciliation_evidence=dict(evidence))
    def get(self,key:str)->EffectRecord:return self._records[key]
```

## Debugging playbook

1. Locate the logical effect key, intent hash, expected version, and downstream request ID.
2. Classify the current state as reserved, executing, committed, absent, partial, or unknown.
3. Block dependent actions until reconciliation produces evidence.

## Production checklist

**✓** Commands and facts are distinct and events use versioned envelopes.

**✓** Transactional outbox and inbox close state and message gaps.

**✓** Each retry class has one bounded owner.

**✓** Every capability has an immutable manifest covering interface, security, risk, effects, runtime, ownership, and lifecycle.

**✓** Discovery is minimal and exact resource authorization happens at invocation.

## Exercises

1. Extend the effect ledger with partial and compensated states.
2. Design a reconciliation algorithm for an API without native idempotency keys.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why is “exactly once” the wrong cross-system assumption? | Brokers, networks, workers, and external systems cannot share one transaction; target at-least-once delivery with one idempotent logical business effect. |
| How do outbox and inbox patterns work together? | The producer commits state plus outbox locally; the publisher retries; the consumer records source and event ID plus payload hash before processing. |
| What is an unknown effect? | A mutating request whose outcome cannot be proven, often after timeout or lost acknowledgment; dependent work freezes until reconciliation or intervention. |
| How should approval be bound to an action? | Persist the exact canonical proposal, preview, destination, evidence, risk, and hash; authorize the approver; reject expiry, supersession, hash mismatch, or stale resource state. |
| Why are both idempotency and optimistic concurrency needed? | Idempotency prevents duplicate logical intent; expected versions prevent an otherwise valid action from overwriting newer state. |


## Transition to Chapter 25

Protected effects are governed; Chapter 25 contains the remaining execution, egress, data, privacy, and supply-chain blast radius.

# 25 — Sandboxing, Egress, Data Security, and Governance

> **Evidence note.** SBOM inventory and SLSA build provenance answer different supply-chain questions. Privacy obligations depend on jurisdiction; the GDPR source is cited only for EU legal context, not as universal legal advice. [R17][R18][R39]

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  A supplier document contains a hidden instruction to upload contracts to an external site. Northstar assumes the model may obey it and relies on sandbox, egress, capability, credential, DLP, and approval controls to prevent harm. |

|  |
| --- |
| **DESIGN DECISION**  Design so prompt injection may manipulate reasoning but cannot reach unauthorized data, credentials, network destinations, or effects. |

## What this chapter delivers

Contain a manipulated model with capability, credential, execution, network, supply-chain, and governance controls.

## Solution blueprint


Figure 17. Sandboxing, Egress, Data Security, and Governance.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Sandbox service, egress proxy, governance registry | untrusted content/code to network and data | sandbox pool · destination · tenant | one sandbox and grant | SandboxProfile · EgressGrant · UseCaseRecord |

## Security assumption: the model may be manipulated

Northstar’s security case remains valid even if a supplier document successfully changes the model’s behavior. The compromised model can only choose among the minimal tools and data already eligible for the current node. It cannot read credentials, create arbitrary clients, reach an unapproved host, weaken policy, bypass approval, or mark an effect committed.

### Defense layers

1. **Capability:** narrow tools, resources, risk, time, spend, and delegation.
2. **Data:** authorize before retrieval, label provenance and trust, minimize fields, and enforce tenant partitions.
3. **Credential:** short-lived, audience-bound, action- and resource-scoped leases at the last hop.
4. **Execution:** immutable sandbox profiles, non-root isolation, quotas, ephemeral storage, and no ambient secrets.
5. **Network:** default-deny egress, canonical destinations, DNS and redirect controls, byte/time limits, and DLP.
6. **Effects:** policy, approval, idempotency, preconditions, receipts, and reconciliation.
7. **Supply chain:** signed agents, Skills, prompts, tools, images, dependencies, policy, schemas, and attestations.
8. **Governance:** use-case inventory, accountable owner, risk tier, exception workflow, incident process, review cadence, and evidence.

A governance record should name business purpose, autonomy, data, tools, external effects, human controls, model and vendor dependencies, region, risk classification, evaluations, release, owner, approvers, exceptions, incidents, review date, and retirement plan. Governance is an executable lifecycle, not a slide deck.

## Security and safety

| **Required analysis** | **Design conclusion** |
| --- | --- |
| Problem | Agents combine untrusted language inputs with privileged tools, creating novel paths for instruction hijacking, data exfiltration, lateral movement, and unsafe automation. |
| Why it is difficult | Prompt injection is a semantic attack and remains unsolved by filtering alone; the model cannot reliably distinguish trusted instructions from malicious content; tool chains expand blast radius. |
| Design alternatives | Prompt-only defenses; content classifiers; sandboxing; capability security; policy gateways; taint tracking; human approval; isolated two-model architectures. |
| Recommended architecture | Assume model compromise. Constrain capabilities outside the model using least privilege, provenance/taint labels, policy enforcement, secret brokering, sandbox isolation, egress controls, structured outputs, effect previews, and risk-based approvals. Combine preventive, detective, and recovery controls. |
| Trade-offs | Strong isolation and approvals reduce flexibility and increase latency. The alternative is an unacceptable dependency on a model’s ability to resist adversarial language. |
| Failure scenarios | Document instructs agent to email secrets; tool output poisons memory; malicious MCP/A2A endpoint steals a token; generated code scans the network; PII enters prompts or traces; supply-chain update changes a tool. |
| Enterprise example | A legal-research agent reads opposing-party documents in a no-write, default-deny sandbox. Retrieved text cannot grant tools; outbound domains are allowlisted; citations are preserved; publishing externally requires counsel approval. |

### Threats and required controls

| **Threat** | **Primary controls** |
| --- | --- |
| Direct/indirect prompt injection | Instruction/data separation, provenance labels, task-scoped retrieval, independent policy checks, no secrets in context, adversarial evals |
| Data exfiltration | Egress proxy, destination allowlist, DLP, field-level redaction, per-run byte budget, approval for external publication |
| Excessive agency/tool abuse | Capability envelope, risk-tiered tools, per-call PDP, step/fan-out/spend caps, deterministic commit services |
| Credential theft/confused deputy | Workload identity, token exchange, audience binding, sender constraints, short TTL, no token passthrough/logging |
| Malicious tool or remote agent | Signed manifests, allowlist, sandbox/network isolation, schema validation, reputation/owner, quarantine and kill switch |
| Memory/knowledge poisoning | Source trust score, write approval, immutable provenance, contradiction detection, TTL, correction/deletion propagation |
| Generated-code escape | Ephemeral microVM/container, seccomp, non-root, read-only base image, resource quotas, default-deny network, no host mounts |
| PII/secrets exposure | Data classification, minimization, tokenization/redaction, customer-managed keys, residency, selective telemetry |
| Model/vendor compromise | Provider isolation, encrypted transport, retention controls, output validation, fallback/disable switch, contractual controls |
| Supply-chain compromise | Pinned dependencies and images, signed artifacts, SBOM, SLSA-style provenance, reproducible builds, staged rollout |
| Cost/availability denial | Admission quotas, tenant budgets, rate limits, queue backpressure, recursion limits, circuit breakers |

Security must be tested against the current OWASP agentic threat taxonomy and organization-specific abuse cases, but compliance with a list is not proof of safety. Prompt-injection defenses remain probabilistic; architecture must limit what a successfully manipulated model can see and do.

### Detailed design — APIs, data model, and scalability

### Component boundaries

The Content Security Gateway scans/classifies inbound and retrieved content; policy enforcement points mediate each trust boundary; the Secret/Credential Broker prevents secret exposure; the Sandbox Control Plane attests and leases isolated execution; the Egress Gateway resolves and filters outbound destinations; DLP inspects structured and unstructured payloads; the Peer/Tool Trust Registry validates supply-chain identity; and the Kill-Switch Service revokes capabilities independently of agent code.

### High-level APIs

| **API** | **Purpose and key semantics** |
| --- | --- |
| POST /v1/security/content:inspect | Scan content reference for malware, active content, secrets, PII, injection indicators, classification, and taint labels |
| POST /v1/security/decisions:authorize | Evaluate trust-boundary action and return allow/deny plus obligations such as redaction, sandbox, approval, and egress limits |
| POST /v1/sandboxes | Lease an attested immutable runtime using profile, tenant/run/node, image digest, resource limits, mounts, TTL, and network policy |
| POST /v1/sandboxes/{lease\_id}:execute | Run a bounded command/browser job; inputs and outputs are artifact references and all network access is mediated |
| POST /v1/egress:authorize | Resolve destination, classify payload, apply purpose/DLP policy, and issue a one-use egress grant |
| POST /v1/credentials:lease | Exchange an authorized decision for an opaque short-lived secret/token handle delivered only to the bound workload |
| POST /v1/security/findings | Record normalized detection with evidence, severity, affected run/capability, containment, and incident link |
| POST /v1/kill-switches | Disable model route, agent/tool/version, peer, destination, tenant action, or risk class and emit immediate invalidation events |
| POST /v1/security/incidents/{id}:contain | Revoke grants, stop dispatch, isolate sandboxes, block egress, checkpoint runs, and preserve evidence |

### Core data model

| **Entity** | **Required fields and invariants** |
| --- | --- |
| SecurityLabel | label ID/type/value, source, confidence, policy provenance, effective time, applies-to artifact/segment/field |
| TaintEdge | source object/label → derived context/artifact/effect, transform/run/node, content hashes; append-only lineage for containment/deletion |
| SandboxProfile | profile/version, image allowlist, CPU/memory/disk/process/time limits, syscall/device/filesystem rules, network policy, telemetry, risk approval |
| SandboxLease | lease/workload identity, run/node/tenant, image digest, profile, egress grants, start/expiry, attestation, destruction proof |
| EgressGrant | one-use/bounded grant, destination canonical ID/IP/cert, method, payload class/hash/byte cap, purpose, decision, expiry |
| SecretLease | opaque handle, secret class/version, bound workload/audience/action, issue/expiry/use count, revocation; plaintext is never persisted here |
| SecurityFinding | finding type/severity, source detector/version, run/artifact/tool/peer, evidence refs, disposition, owner, SLA, incident |
| KillSwitch | scope selector, reason, issuer, effective interval, precedence, rollback approver; explicit deny takes priority over cached allows |
| SupplyChainAttestation | artifact/image/tool digest, builder/source, SBOM/provenance/signature, verification policy/result, promotion state |

### Defense-in-depth request path

### Sandboxing and egress rules

* Default to ephemeral non-root workloads, read-only base images, isolated writable overlays, no host mounts/devices, syscall filtering, resource quotas, no cloud metadata, and default-deny network.
* Canonicalize and resolve destinations at the egress proxy to defend against redirect, DNS-rebinding, IPv6/private-range, URL-parser, and alternate-protocol bypasses.
* Bind egress grants to workload identity, method, canonical destination, purpose, payload classification/size/hash constraints, expiry, and maximum uses.
* Inject secrets at the last possible hop through memory/file descriptor/sidecar mechanisms and redact process/environment dumps. The model and generated code receive capability handles, not secret values.
* Scan outputs and derived artifacts before memory writes, model reuse, cross-agent transfer, or publication; untrusted tool/peer responses remain tainted.

### Scalability and availability

* Place lightweight PEPs, kill-switch caches, and signed policy bundles close to gateways/workers. Keep central policy/control writes low volume and strongly audited; distribute invalidations through a high-priority channel.
* Stateless content/DLP workers scale by bytes and document complexity, with separate pools for archive expansion, OCR, code, images, and low-latency request checks. Set decompression and recursion limits.
* Scale sandboxes by profile-specific pools. Admission considers warm capacity, startup latency, risk isolation, regional capacity, and egress-proxy limits—not only worker CPU.
* Shard egress gateways by region/risk/tenant tier and maintain shared deny intelligence without sharing payloads. A gateway outage fails closed for new external writes and checkpoints affected workflows.
* Stream security telemetry asynchronously where possible, but block a protected action until required inspection/authorization completes. Audit delivery failure cannot silently permit an R3/R4 effect.
* Use bounded caches only for immutable attestations and low-risk allow decisions. Revocation, high-risk actions, secrets, and external publication require current checks.
* Quarantine suspect peers/tools/artifacts by digest so healthy versions continue operating. Kill switches target the narrowest safe scope and are tested as part of disaster exercises.

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Authority of governance sources | NIST AI RMF is voluntary and under revision as of 2026; ISO/IEC 42001:2023 is a management-system standard; OWASP is community security guidance; the EU AI Act is law with phased applicability. None substitutes for jurisdiction-specific legal analysis. | NIST-RMF; ISO42001; OWASP-AGENT; EU-AI-ACT |
| Incident control | Pre-wire kill switches by tenant, agent release, tool, connector, model route, and data source. A kill switch must stop new risky work while preserving evidence and effect reconciliation. | OWASP-AGENT |

Evidence anchors: OWASP-AGENT; NIST-IR; NIST-RMF; ISO42001; EU-AI-ACT. Full URLs, authority, version, and scope appear in Appendix M.

## Implementation reference


### Default-deny URL authorization

PYTHON · implementation excerpt

```python
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit


def authorize_url(raw_url: str, allowed_hosts: frozenset[str]) -> tuple[str, tuple[str, ...]]:
    parsed = urlsplit(raw_url)
    if parsed.scheme.lower() != "https" or parsed.username or parsed.password:
        raise PermissionError("invalid egress URL")
    if not parsed.hostname:
        raise ValueError("host required")
    host = parsed.hostname.encode("idna").decode("ascii").rstrip(".").lower()
    port = parsed.port or 443
    if port != 443 or host not in allowed_hosts:
        raise PermissionError("destination outside egress grant")
    addresses: set[str] = set()
    for item in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM):
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global:
            raise PermissionError(f"non-public address blocked: {address}")
        addresses.add(address.compressed)
    canonical = urlunsplit(("https", f"{host}:443", parsed.path or "/", parsed.query, ""))
    return canonical, tuple(sorted(addresses))
```

### Scoped operational kill switch

PYTHON · implementation excerpt

```python
from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class KillSwitchRule(BaseModel):
    tenant_id: str | None = None
    agent_version: str | None = None
    tool_version: str | None = None
    model_route: str | None = None
    reason: str = Field(min_length=1)

    @model_validator(mode="after")
    def at_least_one_scope(self) -> "KillSwitchRule":
        if not any((self.tenant_id, self.agent_version, self.tool_version, self.model_route)):
            raise ValueError("kill switch requires a scope")
        return self

    def blocks(self, *, tenant_id: str, agent_version: str, tool_version: str | None,
               model_route: str) -> bool:
        checks = (
            self.tenant_id in (None, tenant_id),
            self.agent_version in (None, agent_version),
            self.tool_version in (None, tool_version),
            self.model_route in (None, model_route),
        )
        return all(checks)


class RecoveryObjectives(BaseModel):
    tier: str
    rto_seconds: int = Field(gt=0)
    rpo_seconds: int = Field(ge=0)
    maximum_degraded_minutes: int = Field(ge=0)
    minimum_safe_capabilities: frozenset[str]
```

## Debugging playbook

1. Follow the tainted content to every capability and network boundary.
2. Verify no credentials entered prompt, generated code, logs, or sandbox files.
3. Review DLP, redirect, DNS, egress, artifact, and kill-switch evidence.

## Production checklist

**✓** The design remains safe even if the model follows a malicious instruction.

**✓** Credentials, arbitrary network access, production clients, and authorization authority stay outside model reach.

**✓** Untrusted content is labeled, minimized, and constrained through capability, sandbox, egress, DLP, and effect controls.

**✓** Prompts, models, tools, peers, packages, images, schemas, and attestations are pinned and verified.

**✓** Targeted emergency denies, revocation, isolation, quarantine, and incident evidence are available.

## Exercises

1. Threat-model an injected supplier PDF using an attack tree.
2. Write a default-deny egress policy for the code-execution sandbox.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why can prompt engineering not be the primary security boundary? | Prompt injection is semantic and probabilistic; a model may follow malicious content, so deterministic identity, capability, data, sandbox, and network controls must contain it. |
| What is the correct threat-model assumption for the agent? | Treat the model as potentially compromised while still preventing unauthorized data access, credential retrieval, privileged effects, and exfiltration. |
| How would you secure generated code or browser automation? | Immutable sandbox profile, non-root isolation, resource limits, ephemeral storage, no ambient secrets, default-deny egress, approved artifacts, monitoring, and destruction. |
| How should credentials reach a tool? | Validate subject and actor policy, exchange for a short-lived audience, action, and resource-bound lease, inject at the connector’s final hop, and never expose the secret to prompts or generated code. |
| What makes a useful kill-switch design? | Narrow scopes, emergency-deny precedence, independent high-priority distribution, measurable propagation, governed issuer and rollback, workflow checkpointing, and evidence preservation. |

|  |
| --- |
| **PART V**  **PRODUCTION ENGINEERING**  Trace and evaluate complete trajectories, deploy a scalable platform, recover safely, and optimize verified outcomes. |

18 Observability and Tracing with MLflow

19 Evaluation, Testing, and Debugging with MLflow

20 Enterprise Platform Architecture, APIs, and Data Models

21 Deployment, Versioning, CI/CD, and Recovery

22 Cost, Latency, Capacity, and Reliability Optimization


## Transition to Chapter 26

Security controls now produce events and evidence; Chapter 26 turns those signals into end-to-end traces that operators can reconstruct.
