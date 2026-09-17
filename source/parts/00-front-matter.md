[[COVER]]

# Building Enterprise General Intelligence Platform

Book v2.1.0 · Publication Release · September 2026

**Reza Rahimi, PhD**

A practical, structured enterprise reference for architects, platform engineers, DevOps engineers, and SREs.

# Preface: A Practical Way to Read This Book

This edition starts from a deliberately unfashionable premise: an agentic
application is still a distributed system. The model may propose a useful next
step, but deterministic services must own authority, state, effects, evidence,
acceptance, and release. That is the line between a convincing demo and a
system people can safely depend on.

The book follows that idea from the first model call to a system that has to run
for years. We begin with the boundaries that make an agent predictable, then
define the architecture and turn it into reusable platform capabilities. From
there, the chapters work through the patterns, security controls, evidence,
governance, and operating decisions that appear once real people, real data,
and real consequences enter the picture.

The examples use a fictional Harborlight mortgage case as a thread. It is not a
claim that mortgage underwriting can be delegated to a model; it is a useful
stress test because the case has sensitive evidence, human judgment, policy,
long waits, and protected effects. Comparative Northstar examples show how the
same contracts travel to supplier onboarding and other domains.

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

# How to Use the Book

Read this as one architecture story, not as a stack of unrelated technology
surveys. Start with the map, then choose the reader path that matches your
decision. Each major chapter moves from a concrete problem through boundaries,
architecture, implementation, failure modes, measurement, and trade-offs; you
can use the review questions to test whether the idea survives contact with
your own system.

The cumulative implementation path follows one synthetic Harborlight Home
Finance case so the architecture grows without changing applications between
chapters. The first three checkpoints are implemented and deliberately stop
before any model-owned lending decision or protected loan-origination write:

| Checkpoint | Chapter | What it adds | What remains outside the model |
| --- | --- | --- | --- |
| `C01` | 1 | A read-only evidence summary that exposes the missing second pay statement | Evidence truth, authoritative calculations, lending decisions, and effects |
| `C02` | 2 | Typed candidate facts, deterministic calculation metadata, and a case-scoped workflow command | Validation, authorization, commit, verification, and acceptance |
| `C03` | 3 | A provider-neutral bounded runtime seam with an optional OpenAI adapter | Workflow state, policy, credentials, approvals, effects, receipts, and audit |

Later checkpoints are roadmap targets, not claims that the corresponding
production platform has already been implemented. The retained Northstar
supplier-onboarding material is comparative architecture evidence; the
Harborlight mortgage case is the cumulative runnable path.

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

## The Contract Behind the Architecture

The architectures and practices in this book are built around a small set of principles for operating agentic systems safely and reliably in production:

- **AI can propose; deterministic systems decide and commit.** Models and agents may reason, recommend, generate, and plan, but important actions should pass through deterministic rules, policies, and validation before they change enterprise state.
- **Every production run must be reproducible.** Record the exact versions of the prompts, Skills, workflows, policies, model routes, tools, evaluators, and knowledge used for each run. When something goes wrong, teams should be able to determine exactly what produced the result.
- **Every action must have clear ownership.** Any action that changes external state—such as updating a database, sending a message, or calling a business API—should have one responsible owner, protection against duplicate execution, a record of what happened, and a clear way to verify that it succeeded.
- **Never assume trust across system boundaries.** Whenever data or an action crosses a trust boundary, revalidate who is making the request, what they are allowed to do, whether the content is safe, and whether the data can be used in that context.
- **Production changes must be controlled and reversible.** Material changes should be evaluated before release, approved according to their level of risk, introduced gradually through canary deployments when appropriate, monitored after deployment, and designed so they can be rolled back safely.
- **Production failures should improve the system.** Significant failures should not end with incident resolution. When appropriate and authorized, they should become regression tests, evaluation cases, or improvement candidates so the system can learn from real production experience.

Together, these principles establish a simple operating contract: agents provide intelligence and flexibility, while deterministic controls provide authority, safety, traceability, and reliability.

# Find Your Way Through the Book

## Part I — Foundations

01. What Turns an LLM Call into a Production System
02. From Model Output to Safe Action
03. Keep the Framework in Its Lane

## Part II — Architecture, Knowledge, and Context

04. The Architecture Around the Model
05. Give Knowledge an Owner
06. Build Context Without Losing the Plot

## Part III — The Developer Platform

07. Build the Paved Road for Agent Teams
08. Package Capabilities as Versioned Skills
09. From Skills to a Domain Platform

## Part IV — Patterns That Work—and Those That Fail

10. ReAct Without the Runaway Loop
11. Route the Work—and Transfer Ownership
12. Plans Are Proposals Until the System Compiles Them
13. Use Critique to Improve, Not to Self-Approve
14. Put People Where Judgment Matters
15. Keep Work Alive Across Time and Failure
16. Patterns for Real Enterprise Work
17. The Shapes That Fail in Production

## Part V — Working Together Across Boundaries

18. Coordinate Specialists Without Losing Control
19. Crossing the Boundary: MCP, A2A, and Local Control

## Part VI — Security, Identity, and Control

20. Security Starts Beyond the Prompt
21. Carry Identity and Narrow Authority
22. Make Effects Safe to Retry
23. Contain a Manipulated Model

## Part VII — Evidence, Evaluation, and Improvement

24. Follow One Run from Request to Receipt
25. Improve the System Without Losing Control

## Part VIII — Running the System in the Real World

26. Make Governance an Operating System
27. Release Without Breaking Work in Flight
28. Make Performance a Business Decision

## Appendices

- A. Choosing a Pattern: Decision Tree and Catalog
- B. When Things Go Wrong: Triage and Runbooks
- C. Platform Contracts at a Glance
- D. Choosing a Framework
- E. What This Architecture Means for Research
- F. Known Limits—and the Controls That Contain Them
- G. A Practical Enterprise Adoption Roadmap
- H. Glossary
- I. Companion Implementation Guide: Harborlight Mortgage
- J. Coding-Agent Prompt and Acceptance Criteria
- K. References and Evidence Scope
- L. Capacity, resilience, and release acceptance
