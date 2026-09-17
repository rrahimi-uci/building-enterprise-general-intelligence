[[COVER]]

# Building an Enterprise General Intelligence Platform

Book v2.1.0 · Publication Release · September 2026

**Reza Rahimi, PhD**

A practitioner’s guide for architects, platform engineers, DevOps engineers, and SREs building dependable agentic systems.

# Preface: The Engineering Perspective Behind This Book

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

## How to read the claims in this book

When this book relies on an external fact—about a technology, standard, research finding, or regulation—the claim is tied to a numbered reference such as [R05].

The architectural recommendations come from practical work on enterprise AI and agentic platforms in mortgage and financial environments, combined with established industry practice. They are shaped by systems in which reliability, security, compliance, auditability, scalability, and cost are constraints the design has to meet every day—not qualities that can be added after the prototype works.

Recommendations without citations are experience-based guidance, not universal laws. Test them against your workloads, security requirements, regulatory environment, threat model, providers, and operating constraints. A sound pattern in one organization can be the wrong trade-off in another.

The sources have limits too. Vendor documentation can tell you what a technology supports; it cannot prove that the technology is right for your environment. Community guidance is useful, but it is not law. A benchmark describes a result under particular conditions, not a promise that your workload will behave the same way.

Use the book as an engineering foundation rather than a prescription. Take the evidence, patterns, and hard-earned lessons, then adapt and validate them where your system will actually run.

## How this edition is maintained

A book about governed systems should be maintainable in the same disciplined way. The accompanying Book v2.1.0 package includes the canonical Markdown, generated DOCX, diagrams, cover assets, references, styles, templates, build and validation tools, and release evidence needed to reproduce this edition.

The canonical Markdown is the source of truth. Make substantive changes there and in the relevant registries, then regenerate the DOCX through the build process. That keeps references, diagrams, formatting, and structure aligned—even when people and AI agents both contribute.

The package README walks through build, validation, and release. Following it gives future contributors a safe way to extend the book without quietly breaking its structure, style, or evidence trail.

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

## The architecture in one view

Treat the architecture below as a map of responsibilities, not a prescribed product stack. Read it from the outside in: requests enter through controlled boundaries, reasoning happens inside explicit limits, and every durable decision or external effect returns to a system that can authorize it, record it, and recover it. The value of the diagram is not the number of boxes; it is the clarity of the ownership lines between them.

[[DIAGRAM:book-map|Figure 0-1 — Narrative map from foundations to production operations]]

## The engineering contract behind the architecture

The book returns to a small engineering contract again and again. Models may interpret ambiguity and propose a next step. Deterministic services decide whether the step is allowed, commit it exactly once, and preserve enough evidence to explain the outcome later. Each framework, tool, protocol, and model has to fit inside that contract rather than quietly redefine it.

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
03. Keep the Agent Framework in Its Lane

## Part II — Architecture, Knowledge, and Context

04. Design the Architecture Around the Model
05. Give Knowledge an Owner
06. Build Context Without Losing the Plot

## Part III — The Developer Platform

07. Build a Paved Road for Agent Teams
08. Package Capabilities as Versioned Skills
09. Turn Skills into a Coherent Domain Platform

## Part IV — Patterns That Work—and Those That Fail

10. Use ReAct Without Creating a Runaway Loop
11. Route the Work Without Losing Ownership
12. Turn Proposed Plans into Safe, Executable Work
13. Use Critique to Improve—Never to Self-Approve
14. Put People Where Their Judgment Matters
15. Keep Long-Running Work Alive Through Failure
16. Choose Patterns That Fit Real Enterprise Work
17. Architecture Patterns That Fail in Production

## Part V — Working Together Across Boundaries

18. Coordinate Specialists Without Losing Control
19. Crossing System Boundaries: MCP, A2A, and Local Control

## Part VI — Security, Identity, and Control

20. Security Starts Outside the Prompt
21. Carry Identity, Narrow Authority
22. Make External Effects Safe to Retry
23. Contain the Damage When a Model Is Manipulated

## Part VII — Evidence, Evaluation, and Improvement

24. Follow a Run from Request to Verified Outcome
25. Improve the System Without Handing It Control

## Part VIII — Running the System in the Real World

26. Make Governance Part of How the Platform Runs
27. Release New Behavior Without Breaking Work in Flight
28. Treat Performance as a Business Decision

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
