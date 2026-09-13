# PART XI — GOVERNANCE

This Part defines decision rights, risk tiers, evidence requirements, exceptions, accountability, and lifecycle oversight. It connects technical release controls to an operating model rather than treating governance as a review gate at the end.

# 29 — Governance, Risk, and Operating Model

> **Evidence note.** NIST AI RMF and its Generative AI Profile are voluntary risk guidance; ISO/IEC 42001 specifies an AI management system; the EU AI Act source provides official implementation context. Applicability and legal obligations require qualified jurisdiction-specific review. [R12][R13][R14][R40]

## Federated operating model

Governance makes decisions explicit, proportional, evidence-based, and reversible. It accelerates safe delivery with reusable risk tiers, policy, review paths, and evidence rather than sending every prompt edit to one committee.

[[DIAGRAM:governance-model|Figure 29-1 — Federated governance with centralized control services]]

| **Decision** | **Accountable owner** | **Evidence** |
| --- | --- | --- |
| Business outcome/acceptance | Domain/product owner | Outcome contract, tests, business SLO |
| Risk tier/autonomy | Risk owner | Threat/data/effect assessment and controls |
| Platform contracts | Platform product owner | RFC, compatibility/migration, SLO |
| Data/context/memory purpose | Data owner | Source, ACL, purpose, retention, deletion, quality |
| Tool/effect authorization | Resource owner | Tool contract, permission, idempotency/reconcile, approval policy |
| Model/provider/route | Model governance owner | Capability, evaluation, data terms, region, cost, resilience |
| Evaluator/dataset truth | Domain evaluation owner | Lineage, rubric, calibration, uncertainty |
| Production promotion | Release owner | ValidationReport, required approvals, canary, rollback |
| Exception | Named risk authority | Scope, rationale, compensating controls, expiry, monitoring |

## Risk tiers

| **Tier** | **Typical use** | **Minimum governance** |
| --- | --- | --- |
| 0 Deterministic/assistive | No model or harmless ideation | Standard engineering/data policy |
| 1 Bounded advisory | Low-impact content with verification | Owner, basic evaluation, data controls, monitoring |
| 2 Operational recommendation | Business decision support/internal tools | Domain acceptance, security/privacy, regression, recourse |
| 3 Protected action | Financial, identity, customer, employee, infrastructure effect | Least privilege, exact approval, effect ledger, strong eval, canary, incident plan |
| 4 High consequence/systemic | Regulated, safety-critical, large-scale autonomous/cross-boundary | Executive/risk approval, independent assurance, strict envelope, recovery exercise |

Assess incorrect-outcome impact, sensitive data, protected effects, legal relevance, autonomy, exposure, scale, reversibility, multi-agent/tool complexity, and human detectability. Risk is not the model name.

## Policy, review, and cadence

Principles define non-negotiable outcomes; standards define reusable contracts; policy-as-code decides eligible models, data, tools, actions, budgets, and approvals; application configuration selects within the envelope; exceptions are scoped, monitored, owned, and expiring. Review outcome/acceptance, deterministic boundary, state/effect ownership, identity/delegation, context/memory, tool/MCP/A2A trust, threats, evaluation truth, observability/privacy, recovery, release, capacity/cost, human oversight, and portability.

Operate per run (admission/policy/effects/acceptance), daily/weekly (SLO, quality, safety, cost, incidents, evaluator health), per release (classification, regression, security/privacy, compatibility, canary/rollback), quarterly (portfolio value/risk and platform roadmap), and annually/material change (policy, law, threat, recovery, independent assurance).


## Transition to Chapter 30

Governance defines who may release change; Chapter 30 makes releases immutable, promotable, observable, reversible, and recoverable.
