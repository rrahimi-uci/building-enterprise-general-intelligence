[[COVER]]

# Building an Enterprise General Intelligence Platform

Book v1.0.0 · Publication Release · {{BUILD_DATE}}

**Reza Rahimi, PhD**

A practitioner’s guide for architects, platform engineers, DevOps engineers, and SREs building dependable agentic systems.

# Preface

I wrote this book because I kept watching the same thing happen. A team builds an agent demo, and it is genuinely impressive: it reads the documents, calls the right tools, and answers in a way that makes everyone in the room lean forward. Then the harder questions start. Who approved that action? What happens if the process restarts halfway through? Why did it behave differently yesterday? Which version of the policy did it use? Can we reproduce the decision six months from now?

Too often, the demo has no good answers, because nobody designed the system to have them.

For the past several years, I have worked in highly regulated enterprise environments, particularly healthcare and financial services, including mortgage systems. I have led the architecture and development of multiple enterprise AI and agentic applications where models operate alongside sensitive data, complex business processes, evolving policies, regulatory requirements, and human decision-makers.

This book grew directly out of the last three years of that experience.

In these environments, reliability, security, privacy, compliance, auditability, explainability, and cost are not theoretical architecture qualities or features that can be added after a prototype succeeds. They are constraints you encounter from the beginning. An impressive answer is not enough. You need to know what information produced it, which policy and knowledge versions were used, what the agent was authorized to do, what actions it actually took, how those actions can be audited, and whether the result can be evaluated and reproduced.

That experience led me to a view that may sound unfashionable in an era dominated by increasingly capable models: an agentic application is still a distributed system.

The model can reason, interpret context, and propose a useful next step, and that is an important capability. But the model should not become the system of record or the ultimate source of authority. Identity, authorization, durable state, side effects, evidence, policy enforcement, acceptance, and release need to live in deterministic services and governed boundaries that engineers and operators can reason about.

That distinction is one of the most important differences between a convincing AI demo and an enterprise system that people can safely depend on. This book is my attempt to make that distinction concrete and show how to build around it.

We start where almost every agent starts: with a model call. From there, we progressively work outward toward a system that may need to operate reliably for years.

The early chapters establish the boundaries and primitives that make agent behavior controllable and predictable. We then develop the architecture around those principles and turn it into reusable platform capabilities so that individual teams do not have to reinvent security, knowledge, orchestration, evaluation, observability, governance, and release mechanisms for every new agent.

From there, we address what happens when these systems meet the real enterprise: real users, real data, changing knowledge, long-running workflows, failures, security boundaries, regulatory obligations, and actions with consequences. I cover the architectural patterns that have held up, the approaches that tend to fail, and the practical concerns around identity, security, knowledge, evidence, evaluation, governance, observability, and operating these systems in production.

To keep these ideas concrete, I follow one fictional organization throughout the book: Harborlight, a mortgage lender.

I chose mortgage lending deliberately. It reflects many of the architectural pressures I have encountered in regulated financial systems: sensitive documents and personal information, complex workflows, human judgment, changing policies and regulations, external systems, processes that can remain active for days or weeks, and decisions whose consequences cannot simply be rolled back.

I am not suggesting that mortgage underwriting—or any other consequential decision—should simply be handed over to a model. The point is precisely the opposite. It provides a demanding environment in which we can ask what an enterprise agent should be allowed to reason about, what it should be allowed to do, where deterministic controls must exist, when humans must remain involved, and what evidence must survive after the agent has finished.

If an agentic architecture can remain secure, governed, observable, reproducible, and dependable under those conditions, the same principles can carry surprisingly far across the rest of the enterprise.

This book is therefore not a collection of patterns derived from idealized agent demos. It is an attempt to capture what I have learned while architecting and building agentic systems in environments where trust has to be engineered, not assumed.

Reza Rahimi, Jazzx AI, Palo Alto, California

## How to read the claims in this book

When I rely on an outside fact, about a technology, a standard, a research result, or a regulation, I tie it to a numbered reference such as [R05]; the references appendix lists each source in full.

Everything without a citation is my own judgment, drawn from my work building enterprise AI systems and from established engineering practice. Treat it as guidance, not law, and test it against your own workloads, regulators, threat model, and constraints; a pattern that is right for one organization can be wrong for another. Sources have limits too: vendor documentation says what a product supports, not whether it suits you, and a benchmark describes one result under particular conditions.

So please use this book as a foundation rather than a prescription, and adapt and test it where your system will actually run.

# How to Use the Book

Read this as one architecture story, not as a stack of unrelated technology
surveys. Start with the map, then choose the reader path that matches your
decision. Most chapters move from a concrete problem through boundaries,
architecture, implementation, failure modes, measurement, and trade-offs; the
pattern cards (Appendix A) and anti-pattern catalog (Chapter 17) are reference cards. You
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
| `C03` | 3 | A provider-neutral bounded runtime interface with an optional OpenAI adapter | Workflow state, policy, credentials, approvals, effects, receipts, and audit |

Later checkpoints are roadmap targets, not claims that the corresponding
production platform has already been implemented. From Chapter 4 onward, the
WHERE THE MORTGAGE CASE STANDS boxes describe the target design for later
checkpoints.

| **Reader** | **Primary path** | **Decision supported** |
| --- | --- | --- |
| Executive and product leader | Chapter 1, Parts II, III, VIII and Appendix G | Investment, operating model, risk appetite, platform scope, and outcome governance |
| Enterprise / solution architect | Parts I–VIII | Boundaries, contracts, topology, integration, security, and lifecycle |
| Platform engineer | Parts I–III, Chapter 15, Parts V–VIII | Reusable platform services, SDKs, gateways, telemetry, release, and operations |
| Application developer | Parts I–IV, Chapter 22, Part VII | Agent design, knowledge, tools, Skills, tests, debugging, and improvement |
| Security / risk / privacy | Chapter 1, Parts II, V, VI, VIII and Appendices F, I | Knowledge governance, threat controls, evidence, approvals, exceptions, and assurance |
| SRE / operations | Chapter 1, Chapter 15, Parts VII, VIII and Appendix B | SLOs, incidents, recovery, capacity, and verified-success economics |

Every path assumes Chapter 1's vocabulary. If you want the whole picture before
the details, look at Figure S-1 in the Closing Perspective, the unified
architecture, and keep Appendix C's contracts beside it; the chapters then fill
in each part of that picture. Its labels will make full sense only after the
chapters that define them.

## How the book is organized

The map follows the book's argument from the boundary around the model (Part I)
through architecture, the developer platform, patterns, collaboration,
security, evidence, and operations. Chapter 1's Figure 1-3 shows the system
itself — how a request descends from proposal to committed effect.

[[DIAGRAM:book-map|Figure 0-1 — Narrative map from foundations to production operations]]

## The engineering contract behind the architecture

The architectures and practices in this book are built around a small set of principles for operating agentic systems safely and reliably in production:

- **AI can propose; deterministic systems decide and commit.** Important actions pass deterministic rules, policies, and validation before they change enterprise state.
- **Every production run must be reconstructable and explainable.** Preserve enough evidence to reconstruct what happened, even when the model's output cannot be reproduced exactly.
- **Every action must have clear ownership.** A state-changing action has one owner, protection against duplicate execution, and a verifiable record.
- **Trust must be explicitly established at every system boundary.** The receiving component enforces its own controls rather than trusting the sender.
- **Agentic behavior changes must be controlled, observable, and recoverable.** Models, prompts, Skills, tools, policies, and knowledge are versioned, evaluated, released progressively, and reversible.
- **Production failures should become governed evidence for improvement.** They become evaluation cases that pass the normal release process before anything changes (Chapter 25).

Together, these principles establish a simple operating contract: agents provide intelligence and flexibility, while deterministic controls provide authority, safety, traceability, and reliability. Chapter 2 § Design principles turns this contract into ten design rules used throughout the book.

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

## Closing Perspective

- What Production-Grade Intelligence Requires

## Appendices

- A. Choosing the Right Pattern: A Decision Guide
- B. When Things Go Wrong: Triage and Runbooks
- C. Core Platform Contracts at a Glance
- D. Choosing an Agent Framework
- E. What This Architecture Means for Research
- F. Known Limits and the Controls That Contain Them
- G. A Practical Roadmap for Enterprise Adoption
- H. Companion Implementation Guide: Harborlight Mortgage
- I. References
- J. Glossary

## Index

- Key terms and where the book discusses them
