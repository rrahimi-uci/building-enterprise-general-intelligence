# PART VII — LLM GATEWAY

This Part isolates model-provider concerns behind a control plane for routing, authorization, policy, privacy, budgets, resilience, telemetry, and evaluation hooks. It also distinguishes the LLM Gateway from API, agent, MCP, and workflow layers.

# 20 — LLM Gateway and Model Control Plane

## Position and boundaries

The LLM Gateway is the controlled boundary between enterprise workloads and model providers or self-hosted inference. It normalizes model access and enforces model-specific routing, policy, privacy, economics, observability, and release governance. It does not own business workflow, tool effects, agent delegation, or the external API perimeter.

[[DIAGRAM:gateway-position|Figure 20-1 — LLM Gateway position relative to adjacent gateways]]

| **Component** | **Primary boundary** | **Owns** | **Does not own** |
| --- | --- | --- | --- |
| API Gateway | External client → enterprise API | API auth, routing, quota, WAF, protocol termination | Agent semantics or model routing |
| Agent Gateway | Agent/workload → agent platform | Workload identity, task admission, delegation, tenancy, agent audit | Provider inference controls |
| LLM Gateway | Workload → model/inference | Provider abstraction, model routing, content/data policy, token/cost control | Durable workflow or business acceptance |
| MCP Gateway | Platform → MCP server | Server trust, discovery, tool eligibility, scoped credentials, protocol audit | General model inference |
| Orchestration layer | Run → tasks/activities | State, deadlines, retries, joins, cancellation, compensation | Provider perimeter or policy truth |

## Required capabilities

| **Capability** | **Behavior** | **Control** |
| --- | --- | --- |
| Provider abstraction | Normalize requests, streaming, errors, usage, capabilities | Preserve provider/model/version and raw evidence references |
| Model routing | Select by task, risk, region, quality, latency, cost, health | Deterministic eligibility before optimization; record reason |
| Authentication and authorization | Authenticate workload and subject context | Audience, tenant, purpose, approved models |
| Policy enforcement | Enforce use, data, region, model, output, risk rules | External policy decision; never prompt-only policy |
| PII/secrets protection | Classify, minimize, redact/tokenize, block | Authorized reversible boundary; never log secrets |
| Rate limits and budgets | Tenant/workload/user quotas, tokens, spend, concurrency, deadline | Hierarchical budgets before provider charge |
| Caching | Reuse only policy-safe, semantically equivalent results | Key tenant, policy, model/version, prompt, context snapshot, safety |
| Retries and fallbacks | Classify transient failures; use approved alternatives | One retry owner and shared deadline/budget |
| Content filtering | Input/output safety, injection, DLP, schema, evidence checks | Filters are evidence; policy still authorizes actions |
| Model/version governance | Allowlist, aliases, deprecation, eval, canary, rollback | Alias change is a versioned routing release |
| Logging, tracing, evaluation hooks | Normalized spans, route, usage, policy, cache, scorers | Redaction, evaluator version, scope, uncertainty, override lineage |

## Policy-first routing

[[DIAGRAM:model-routing|Figure 20-2 — Policy-first model-routing decision tree]]

Filter by tenant, purpose, data class, residency, risk, required capabilities, context length, tool/JSON behavior, and approved version. Only then optimize expected accepted-outcome quality under latency and cost budgets. Health and quota further constrain selection. Fallbacks obey the same invariants; “any available model” is not a safe fallback.

Record candidate routes, exclusions/reasons, selected provider/model/version/region, policy digest, budgets, fallback chain, and experiment cohort. Cache keys must include every security and semantic dependency. Never cache a protected decision that depends on current authorization or resource version without preserving that dependency.

## Gateway metrics and trade-offs

Measure route distribution and eligibility, task success/quality by route, schema/tool correctness, refusal/safety, p50/p95/p99 latency, queue/retry amplification, cache hits and unsafe-key rejection, tokens/cost per accepted outcome, policy denials, PII/secrets detections, provider error/fallback, alias/version drift, and trace completeness. Centralization adds latency and blast-radius risk; deploy regionally, isolate tenants/risk classes, use bulkheads, and retain platform-owned contracts even when buying a gateway.


## Transition to Chapter 21

The gateway controls model access, but not the entire attack surface; Chapter 21 introduces defense in depth across all agentic trust boundaries.
