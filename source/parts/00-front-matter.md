[[COVER]]

# Building Enterprise General Intelligence Platform

Book v2.1.0 · Publication Release · September 2026

**Reza Rahimi, PhD**

A practical, structured enterprise reference for architects, platform engineers, DevOps engineers, and SREs.

# Preface to Book v2.1.0

Book v2.1.0 is the publication baseline for this guide and the canonical starting point for all future editions. It treats an agentic application as a governed distributed system: models may propose, while deterministic services own authority, state, effects, evidence, acceptance, and release.

The narrative follows a clear progression from foundations to production. It begins with the core principles and deterministic controls that make agentic systems predictable and governable. The reference architecture then defines the major components and their responsibilities, while the platform team turns these architectural principles into reusable capabilities for engineering teams through SDKs.

From there, patterns and anti-patterns guide how agents, tools, and workflows should be designed and connected. Gateways and security controls establish safe boundaries around models, data, tools, and external systems. Observability and evaluation provide the evidence needed to understand system behavior, quality, cost, and reliability. That evidence feeds into continuous learning, where improvements are introduced through controlled and governed processes. Finally, production operations ensure that the entire system remains reliable, scalable, secure, and cost-efficient over time.

## Scope and claim discipline

Throughout this book, claims about external facts, technologies, standards, research, and regulations are supported by numbered references such as [R05].

The architectural recommendations in this book are grounded in the author’s practical experience designing and building real-world enterprise AI and agentic platforms for mortgage and financial systems, combined with established industry best practices. They reflect lessons learned from working with systems where reliability, security, compliance, auditability, scalability, and cost are production requirements rather than theoretical concerns.

When an architectural recommendation does not include a citation, treat it as experience-based guidance, not a universal rule. Every enterprise environment is different. Validate these recommendations against your own workloads, security requirements, regulatory environment, threat model, technology providers, and operational constraints.

References should also be understood within their scope. Vendor documentation explains what a technology supports, but does not prove that it is suitable for your production environment. Community best practices provide useful guidance, but are not laws or regulations. Benchmarks demonstrate performance under specific conditions, but do not guarantee the same results in your environment.

In short, this book combines published evidence, industry best practices, and lessons from building real enterprise platforms. Use them as a foundation, then adapt and validate the architecture for your own organization.

## Reproducible edition

This book is designed to be reproducible, maintainable, and easy to extend. The accompanying Book v2.1.0 development package contains everything needed to rebuild and update the book consistently, including the canonical Markdown source, generated DOCX, diagrams, cover assets, references, style definitions, templates, skills, build tools, validation tools, and release evidence.

The Markdown file is the primary source of truth. When updating the book—whether manually or with an AI agent—changes should be made to the Markdown source and the relevant registries first. The DOCX should then be regenerated through the provided build process rather than edited or formatted manually. This helps prevent inconsistencies in formatting, references, diagrams, and document structure.

The package README explains how to build, validate, and release a new version of the book. Following this workflow ensures that future contributors and AI agents can extend the book without breaking its established structure, style, or quality.

# How to use this guide

This guide is organized as one architecture story rather than a collection of independent topics. Read the executive map, then follow the lane that matches the decision. Every major chapter moves from problem and boundaries to architecture, implementation, failure modes, metrics, trade-offs, and review questions.

| **Reader** | **Primary path** | **Decision supported** |
| --- | --- | --- |
| Executive and product leader | Parts II, III, VIII and Appendix G | Investment, operating model, risk appetite, platform scope, and outcome governance |
| Enterprise / solution architect | Parts I–VIII | Boundaries, contracts, topology, integration, security, and lifecycle |
| Platform engineer | Parts II, III, V–VIII | Reusable control planes, SDKs, gateways, telemetry, release, and operations |
| Application developer | Parts I, II, III, IV, VII | Agent design, knowledge, tools, Skills, tests, debugging, and improvement |
| Security / risk / privacy | Parts II, VI, VIII and Appendices F, K | Knowledge governance, threat controls, evidence, approvals, exceptions, and assurance |
| SRE / operations | Parts VII, VIII and Appendices B, L | SLOs, incidents, recovery, capacity, and verified-success economics |

## Architecture at a glance

[[DIAGRAM:book-map|Figure 0-1 — Narrative map from foundations to production operations]]

## Reference-guide contract

The architectures and practices in this book are built around a small set of principles for operating agentic systems safely and reliably in production:

- **AI can propose; deterministic systems decide and commit.** Models and agents may reason, recommend, generate, and plan, but important actions should pass through deterministic rules, policies, and validation before they change enterprise state.
- **Every production run must be reproducible.** Record the exact versions of the prompts, Skills, workflows, policies, model routes, tools, evaluators, and knowledge used for each run. When something goes wrong, teams should be able to determine exactly what produced the result.
- **Every action must have clear ownership.** Any action that changes external state—such as updating a database, sending a message, or calling a business API—should have one responsible owner, protection against duplicate execution, a record of what happened, and a clear way to verify that it succeeded.
- **Never assume trust across system boundaries.** Whenever data or an action crosses a trust boundary, revalidate who is making the request, what they are allowed to do, whether the content is safe, and whether the data can be used in that context.
- **Production changes must be controlled and reversible.** Material changes should be evaluated before release, approved according to their level of risk, introduced gradually through canary deployments when appropriate, monitored after deployment, and designed so they can be rolled back safely.
- **Production failures should improve the system.** Significant failures should not end with incident resolution. When appropriate and authorized, they should become regression tests, evaluation cases, or improvement candidates so the system can learn from real production experience.

Together, these principles establish a simple operating contract: agents provide intelligence and flexibility, while deterministic controls provide authority, safety, traceability, and reliability.

# Hierarchical Table of Contents

## Part I — Foundations

01. From an LLM Call to a Production Agentic System
02. Tools, Structured Outputs, and the Deterministic Shell
03. Agent Runtime and Framework Abstraction

## Part II — Enterprise Architecture & Knowledge

04. Enterprise Reference Architecture, Boundaries, and Contracts
05. Enterprise Knowledge Management for Agents
06. Context Engineering, RAG, Memory, and State

## Part III — Agentic Developer Platform & SDK

07. Agentic Developer Platform, SDK, and Delivery Lifecycle
08. Skills as Versioned Capabilities
09. Skill Packs and Domain Platforms

## Part IV — Patterns and Anti-Patterns

10. ReAct: Bounded Reason–Act–Observe Loops
11. Routing, Triage, and Handoffs
12. Planning and Plan–Execute
13. Reflection and Evaluator–Optimizer
14. Human-in-the-Loop
15. Long-Running and Durable Agents
16. Enterprise Pattern Catalog
17. Enterprise Anti-Pattern Catalog

## Part V — Multi-Agent Systems & External Integration

18. Supervisor/Worker and Multi-Agent Collaboration
19. External Integration: MCP, A2A, and the Model Control Plane

## Part VI — Security, Identity & Guardrails

20. Agentic AI Security and Guardrails Architecture
21. Identity, RBAC/ABAC, and Delegated Authorization
22. Tool Security, Side Effects, Idempotency, and Approval
23. Sandboxing, Egress, Data Security, and Governance

## Part VII — Observability, Evaluation & Learning

24. Distributed Tracing
25. Continuous Learning and Governed Improvement

## Part VIII — Governance & Production Operations

26. Governance, Risk, and Operating Model
27. Deployment, Versioning, CI/CD, and Recovery
28. Cost, Latency, Capacity, and Reliability Optimization

## Appendices

- A. Pattern Selection Decision Tree and Catalog Index
- B. Failure triage and operator runbooks
- C. Platform contracts quick reference
- D. Framework landscape
- E. Research implications
- F. Known limits and enforced mitigations
- G. Enterprise adoption roadmap
- H. Glossary
- I. Companion Implementation Guide: Harborlight Mortgage Reference
- J. Coding-agent prompt and acceptance criteria
- K. References
- L. Capacity, resilience, and release acceptance
