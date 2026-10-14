# Unified enterprise architecture: synthesis and validation

This is the traceability record for `unified-enterprise-architecture`. The figure
is a **book-authored logical synthesis** of the current manuscript, not a claim
that the companion code implements Chapters 4–28. The delivered code covers
Harborlight checkpoints C01–C03 (Appendix H). Chapter 4's seven planes own the
records; the figure's four frames show design-time control, regional runtime,
external dependencies, and the offline improvement path. A frame groups
services for reading: it is not an extra plane or an extra source of authority.
The review traversed all ten canonical Part/front-matter files (about 8,000
lines), inventorying 634 section and subsection headings, 325 table blocks,
46 diagram markers, and 60 example markers before reconciling the chapter
contracts below. Architecture decisions were checked against the defining
prose, figures, tables, and representative runnable examples; the source files
remain the authority for each full contract.

## Element inventory before consolidation

| Area | Manuscript elements retained in the synthesis | Figure treatment |
| --- | --- | --- |
| Human and enterprise entry | End users, API clients, business events, domain owners, platform/security/risk owners, SMEs, operators, approvers; user interaction and recourse | People and teams; Channels; approval in the governance band |
| Agent applications | AgentSpec, instructions, Skill and Skill Pack releases, eligibility and resolution, application topology, framework adapter and bounded AgentRuntime | Build and validate; AgentRuntime |
| Runtime and workflow | Run API, RunManifest, workflow history, planner/Plan IR/compiler, deterministic transitions, timers, events, budgets, durable waits, cancellation, retry ownership, TaskEnvelope, child tasks, handoff, join, acceptance | Admission; Run and workflow; Task Service; Workflow gates |
| Knowledge and context | Source bytes/digests, KnowledgeArtifact, ontology and graph, rules, catalog, process/decision models, KnowledgeRelease/Binding, search and vector index, ContextManifest, conversation and MemoryRecord, provenance and ACLs | Source intake; Knowledge gates; KnowledgeRelease; Context Service |
| Model and tool integration | Model routing and allowlists, LLM Gateway, model providers, ToolManifest, Tool Gateway, MCP and A2A Gateways, Effect Service/Record/Receipt, connectors, sandbox and egress | LLM Gateway; Models; Access gateways; Enterprise systems; governance band |
| Governance and security | Subject plus actor, identity, policy decision/enforcement, capability envelope, credential lease, approval, data classification, guardrail signals, isolation, DLP, audit, exceptions | Admission; Workflow gates; cross-cutting trust and governance |
| Evaluation and operations | Causal traces, metrics/logs, content vault, separate audit ledger, SLO and cost, incident response, datasets, acceptance vs release evaluation, calibrated judges, SME feedback, release gates | Observe; Evaluate and calibrate; Change review |
| Engineering and lifecycle | Golden path, conformance tests, CI, ChangeBundle, signed immutable ReleaseManifest, knowledge activation, environment binding, canary, rollback, active-run compatibility, regional cells and backpressure | Build and validate; ReleaseManifest; Change review; regional boundary |
| Enterprise dependencies | Systems of record, databases, SaaS/APIs, event sources, external MCP servers and partner agents, hosted or provider models | Source intake; Models; Enterprise systems outside the regional cell |

The visual groups rather than independently boxes every contract. The nouns in
the middle column remain separately defined by the cited chapters and Appendix
C. The ontology and vector index, for example, are both in the knowledge area
but are not synonyms: Chapter 5 uses search for passages and bounded graph
traversal for relationships. A source copy in intake does not replace the
authoritative external source or domain system.

## Chapter-to-architecture map

The headings and figures below were checked against all eight Parts, the
Closing Perspective, and Appendices A–J. The relevant tables and examples
were used as contracts and counterexamples; their detailed fields remain in
the defining chapters and Appendix C.

| Chapter | Architectural contribution | Figure node or edge |
| --- | --- | --- |
| 1 | Four levels of agency, production responsibilities and control points; Figures 1-2 and 1-3 | Whole-system boundary; Channel → runtime → effect |
| 2 | Typed model proposal and six deterministic gates; Figure 2-1 | AgentRuntime → Workflow gates → Access gateways |
| 3 | AgentRuntime request/result and replaceable SDK adapter; Figures 3-1 and 3-2 | Bounded agent step, never run owner |
| 4 | Seven ownership planes, global tier, regional cells, RunManifest, request sequence; Figures 4-1 and 4-2 | Figure backbone, release pin, run and workflow |
| 5 | Source-to-KnowledgeRelease lifecycle, verification, ontology/graph, rules, four consumption modes; Figures 5-1–5-4 | Source intake → gates → release → Context Service |
| 6 | Authorized ContextManifest, trust tiers, provenance-bound memory; Figure 6-1 | Context Service → AgentRuntime |
| 7 | Platform contracts, conformance adapters, golden developer path; Figures 7-1–7-3 | People and teams → Build and validate |
| 8 | Immutable Skill manifest, policy-filtered discovery and resolution; Figure 8-1 | Build and validate → ReleaseManifest |
| 9 | Co-released, compatible Skill Packs and domain ownership | Build and validate → ReleaseManifest |
| 10 | ReAct bounded by time, tools, cost, turns, progress; Figure 10-1 | AgentRuntime within Run and workflow limits |
| 11 | Routing eligibility versus accountable handoff | Run and workflow; Task Service |
| 12 | Typed Plan IR, deterministic compilation, frozen committed history | Run and workflow; Workflow gates |
| 13 | Runtime reflection versus independent acceptance; Figure 13-1 | AgentRuntime proposal → Workflow gates; Run acceptance |
| 14 | Proposal-bound human approval, intervention and operator control; Figure 14-1 | Governance band; Workflow gates |
| 15 | Durable workflow history, events, retries, waits, recovery; Figure 15-1 | Run and workflow; Task Service |
| 16 | Composition and selection of bounded patterns; Figure 16-1 | Runtime grouping and branching |
| 17 | Production anti-patterns as negative tests, especially vector truth, ambient authority, retry storms, model-says-done | All controls and boundary placement |
| 18 | TaskEnvelope, narrowed delegation, one owner, deterministic join; Figure 18-1 | AgentRuntime → Task Service |
| 19 | MCP tools/resources and A2A remote tasks through local gateways | Task Service and Access gateways → external systems |
| 20 | Detector signals versus policy decisions and enforcement points; Figures 20-1–20-3 | Cross-cutting governance → gates/access |
| 21 | Subject plus actor, capability intersection, last-hop credential lease; Figure 21-1 | Admission, governance, access boundary |
| 22 | Effect ledger, one logical key, receipt, Unknown and reconciliation; Figure 22-1 | Access gateways ↔ enterprise systems → Run and workflow |
| 23 | Prompt-injection containment, sandbox and default-deny egress; Figure 23-1 | Governance band at untrusted external edges |
| 24 | Causal trace and metrics; audit ledger separate; Figure 24-1 | Runtime → Observe |
| 25 | Runtime adaptation versus offline changes; datasets, slices, calibrated judges and immutable gate evidence; Figures 25-1–25-3 | Observe → Evaluate and calibrate → Change review |
| 26 | Accountable governance owners, risk tiers, proportional gates, expiring exceptions; Figure 26-1 | People and teams; Workflow gates; Change review |
| 27 | Signed ReleaseManifest, promotion, canary, assignment rollback and compatible active runs; Figure 27-1 | Change review → ReleaseManifest → Run pin |
| 28 | Admission permits, model route eligibility, SLO and verified-success economics; Figures 28-1 and 28-2 | Admission; LLM Gateway; Observe |

Appendix A supplied the cross-chapter pattern inventory; B supplied failure and
reconciliation checks; C supplied authoritative record names; D kept
frameworks in their stated layers; E–G supplied limits, research implications,
and adoption gates; H bounded the companion-code claim; I supplied example
scenarios and acceptance criteria; J supplied the citation scope registry; K
supplied production acceptance evidence; L fixed terminology. No new external
factual claim was added to the architecture.

## Directed flow contract

`Runtime` denotes synchronous step calls or durable commands unless stated;
`offline` denotes reviewed and versioned activity. Where the figure groups
multiple services, this table names the real owner of the transfer.

| Source → destination | Payload / decision | Flow and timing | Book support |
| --- | --- | --- | --- |
| People and teams → Build and validate | Domain behavior, contracts, tests, policy and evaluation definitions | Offline authorship | 7–9, 25–27 |
| Build and validate → ReleaseManifest | Validated immutable version graph and gate evidence | Offline promotion | 25–27 |
| External enterprise sources → Source intake | Content bytes, revision, digest, ACL and origin; intake holds a governed copy | Offline or event-triggered intake | 4–5, 20 |
| Source intake → Knowledge gates | Candidate extracted fields, requirements, terms and provenance | Offline, extraction probabilistic | 5 |
| Knowledge gates → KnowledgeRelease | Complete gate record and independent SME approval of exact candidate digest | Offline, deterministic and human gate | 5, 27 |
| ReleaseManifest → Run and workflow | Promoted behavior graph resolved into a write-once RunManifest at admission | Runtime admission control | 4, 27 |
| KnowledgeRelease → Context Service | Run-pinned release digest and authorized search/traversal/evaluation views | Runtime read; no re-resolution mid-run | 5–6 |
| Channels → Admission → Run and workflow | Authenticated intent or event, tenant/purpose/risk/budget and idempotent run command | Runtime; API command or asynchronous event/signal | 4, 15, 21, 28 |
| Run and workflow → Context Service | Step request with run pin, identity, eligible capabilities and token budget | Runtime step | 3–4, 6 |
| Context Service → AgentRuntime | Authorized ContextManifest: ordered, provenance-labelled, token-bounded segments | Runtime read | 3, 6 |
| AgentRuntime ↔ LLM Gateway ↔ Models | Eligible inference request and normalized model result | Runtime synchronous or streamed call | 3–4, 28 |
| AgentRuntime → Task Service | Narrowed TaskEnvelope; Task Service owns child work, cancellation and join | Runtime durable child task, often asynchronous | 11, 18–19 |
| Task Service → Workflow gates | Typed joined child result returned to the run-owned workflow for validation and transition | Runtime result/event after child completion | 15, 18–19 |
| AgentRuntime → Workflow gates | Typed AgentStepResult / proposed action returned to workflow; the workflow invokes validation, policy and approval | Runtime control, may pause for human | 2–3, 13–14 |
| Governance → Workflow gates / Access gateways | Policy decision, capability envelope, proposal-bound approval and last-hop credential lease | Runtime enforcement, rechecked at commit | 14, 20–23 |
| Workflow gates → Access gateways | Validated, authorized effect intent with expected version and logical key | Runtime command | 2, 21–22 |
| Access gateways ↔ Enterprise systems | Tool/MCP invocation or federated task; returned receipt, artifact or status is revalidated | Runtime; may complete asynchronously | 19, 22–23 |
| Access gateways → Run and workflow | EffectRecord state and receipt, or Unknown/intervention; workflow decides next transition | Runtime result/event | 13, 15, 22 |
| Run and workflow → Channels | Accepted result, refused/escalated status or progress and authorized artifact references | Runtime response/event | 4, 13–15 |
| Runtime → Observe | Correlated trace and metrics plus separate protected audit writes; no sampled trace substitutes for audit | Runtime telemetry and durable evidence, often asynchronous | 4, 24 |
| Observe → Evaluate and calibrate | Reviewed production samples, incident cases, outcomes, cost and SME feedback | Offline evidence | 24–25 |
| Evaluate and calibrate → Change review | EvaluationResult, slices, baseline, deterministic failures, calibrated judge and ValidationReport | Offline gate | 25–26 |
| Change review → ReleaseManifest | Approved ChangeBundle promoted with canary, rollback and compatibility evidence | Offline controlled release | 26–27 |

The compact arrow from AgentRuntime to Workflow gates stands for a result
returning to the workflow's deterministic dispatch, not an agent calling a
policy or approval service with authority of its own. The pale external frame
contains remote systems and providers; its cards do not imply one shared
protocol or transaction. The returned cyan arrows are normal replies; the
effect receipt is additionally captured in the Effect Service before the run
can accept it.

## Print-scale visual revision

The second pass softened and separated the four architectural frames and gave
the behavior and knowledge release records distinct, readable names. It
restored the missing model-gateway return and
the child-task join result, so neither path visually ends at its downstream
service. The dotted evidence route now starts at the regional runtime boundary
rather than the governance card: telemetry and audit are produced across the
cell, while the audit record remains separate from sampled traces. The legend
calls a box a service or record because the two release boxes are immutable
records. The shared trust band names the governing services; the surrounding
prose specifies enforcement at admission, retrieval, inference, delegation,
and effects. The two short red taps identify protected action gates and do
not exhaust the enforcement points.

## Reconciliation decisions and remaining limits

1. **Seven planes versus four frames.** Chapter 4 owns the seven-plane model;
   these four frames are a reading aid for lifecycle and trust boundaries.
   Security and governance and evaluation and operations still cross every
   relevant plane; they have not been demoted to sequential runtime stages.
2. **Figure 1-3 versus Chapter 4 request sequence.** Figure 1-3's vertical
   authority axis is conceptual. Chapter 4's request-to-verified-outcome
   sequence governs actual execution order. The new figure follows that
   sequence and shows the knowledge and release loops alongside it.
3. **Framework versus workflow.** AgentRuntime executes one bounded step;
   Run Service and the durable workflow own state, retries, terminal status,
   and acceptance. A framework handoff does not transfer business ownership
   (Chapters 3, 11, and 15).
4. **KnowledgeArtifact versus KnowledgeObject, index versus source.** The
   former is a control-plane record, the latter a semantic projection; vector
   and graph indexes are derived views. The source bytes and approved release
   carry provenance and version authority (Chapters 4–6).
5. **Knowledge release versus full behavior release.** The registry publisher
   moves KnowledgeBinding; the Promotion Service moves EnvironmentBinding. A
   RunManifest pins the resolved knowledge streams and ReleaseManifest once.
   A rollback changes future assignment, not active run history (5, 27).
6. **Runtime acceptance versus offline evaluation.** The acceptance engine
   decides one run's candidate outcome; the release gate evaluates changed
   behavior across datasets and slices. Neither a model judge nor a trace can
   self-authorize a protected effect (13, 24–25).
7. **Guardrail versus policy.** Guardrails are detectors. Authorization lives
   at policy points and is enforced at gateways outside the model. The red
   band is a cross-cutting control, not a magic security layer (20–23).
8. **Source verification versus real-world truth.** Exact span and field
   verification proves what pinned bytes say; it does not prove a document is
   genuine. Independent corroboration or human review remains necessary when
   the decision needs that truth (5).
9. **Diagram abstraction.** Internal Plan IR, queue/broker, cache, memory
   lifecycle, per-protocol gateway, sandbox worker, incident tool and
   audit/WORM archive are grouped to keep 9 pt labels legible at 7.06 inches.
   Their distinct ownership and failure semantics remain in the manuscript.
10. **Implementation status.** This is a target reference architecture taught
    by the book, not a diagram of a completed production deployment. Appendix
    H and `code-gap.md` keep the C01–C03 code boundary explicit.

## Final critique

| Test | Finding |
| --- | --- |
| Completeness | All 28 chapters and the appendices were mapped; the inventory accounts for human, runtime, knowledge, model/tool, trust, evidence and lifecycle concerns. |
| Correctness and consistency | Chapter 4 owns records; the synthesis uses Chapter 3's step interface, Chapter 5's pinned knowledge, Chapter 22's effect semantics and Chapter 27's release assignment. |
| Traceability | Every named major box and directed flow is mapped above to chapters or Appendix C. |
| Connectivity and direction | Requests go to runtime, released definitions flow down, external replies return through gateways, and evidence flows to offline review. No feedback edge changes a live run's pins. |
| Layering and redundancy | Control tier, regional cell, external systems and offline loop remain distinct; closely related service details are consolidated within their owner. |
| Unsupported assumptions | No vendor, central all-knowing store, autonomous policy decision or cross-system exactly-once claim is introduced. The diagram is explicitly logical. |
| Readability | Render at final size, inspect at 100% and contact-sheet scale, verify grayscale and text extraction, and keep the figure's line-style legend in the visual. |

The source of truth remains the manuscript and registries. Revalidate this
record if a chapter changes an ownership boundary, a release pin, or an effect
contract.
