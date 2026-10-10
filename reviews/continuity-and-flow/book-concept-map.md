# Book Concept Map — Continuity and Flow Review

Shared reference map for the per-chapter continuity reviews of *Building an Enterprise General Intelligence Platform* (v2.1.0). It was built from a full read of `source/parts/00-front-matter.md` through `09-appendices.md`, plus the diagram sources in `assets/diagrams/src/` wherever a figure comparison needed them.

**Conventions**

- `Ch 05 § Heading` means the chapter number plus the exact heading text. `04-part-iv.md:1417` means a file and line in `source/parts/`.
- "Re-taught" means a passage explains the concept again (definition, mechanism, or field list). A passing mention does not count.
- Severity in §4 means: **High** = a reader meets a mechanism or code they cannot interpret, or a chapter's claim is false given the order. **Medium** = an undefined term carries real weight in a table, contract, or checklist. **Low** = a forward reference that is signposted or easy to infer.
- This is a map, not a review verdict. Where a recommendation appears, it is the option the evidence supports, and it is labeled as such.

---

## 1. Narrative spine

**Overall argument (the spine in 13 lines)**

1. An agentic application is still a distributed system. The model is a bounded reasoning component that *proposes*, and deterministic services own state, authority, effects, evidence, acceptance, and release (Preface, `00-front-matter.md:13`; Ch 01 § The gap between a useful demo and a dependable system).
2. A demo that works fails in production for five non-intelligence reasons: durability, trust boundaries, transactional effects, evidence, and release control (Ch 01 § Start with a demo that genuinely works).
3. So every model output is a typed proposal that must pass six gates (propose → validate → authorize → commit → verify → accept) before anything changes (Ch 02).
4. The agent framework runs one bounded step behind a platform contract (AgentRuntime). Framework state never becomes business truth (Ch 03).
5. The platform around that step is a set of planes with single-owner records, trust boundaries, and regional cells (Ch 04). Knowledge is governed owned artifacts, not a corpus (Ch 05). Each model call receives an authorized, manifest-recorded projection of separately stored state (Ch 06).
6. Teams consume all of this through a paved road, versioned Skills, and Skill Packs (Ch 07–09).
7. Agent loop shapes are useful only inside external bounds: ReAct, routing/handoff, plan compilation, critique, human authorization, and durable execution (Ch 10–15). They are then catalogued as patterns and anti-patterns (Ch 16–17).
8. Collaboration, whether internal or across MCP/A2A, is durable task ownership with narrowing authority. A protocol does not transfer trust (Ch 18–19).
9. Security assumes the model can be manipulated: layered detection and enforcement, subject+actor identity with narrowing grants, retry-safe effects under unknown outcomes, and containment (Ch 20–23).
10. Runs must be causally explainable, and improvement must be evidence-gated without the model certifying itself (Ch 24–25).
11. Operating the system means proportional governance, releases that never rewrite in-flight history, and optimizing cost per *verified* success (Ch 26–28).
12. The invariants that recur everywhere: proposal ≠ permission; discovery ≠ authorization; timeout ≠ failure; transcript ≠ state; model "done" ≠ acceptance; framework state ≠ business state; trace ≠ audit; configuration change ≠ no release.
13. Structurally, nearly all of these invariants are introduced in Part I (often fully, in Ch 03) and then re-taught in their "home" chapter and again in Ch 16/17 and the appendices. The spine is coherent but repetition-heavy.

**Role of each Part**

| Part | Role in the argument |
| --- | --- |
| I — Foundations (Ch 01–03) | States the thesis, names the agent levels and control points, defines the six-gate shell and the runtime seam. Carries cumulative checkpoints C01–C03, the only implemented checkpoints. |
| II — Architecture, Knowledge, and Context (Ch 04–06) | Turns the boundary into an architecture (planes, contracts, stores), then fills the knowledge plane and the per-step context projection. |
| III — The Developer Platform (Ch 07–09) | Packages the architecture for delivery teams as a paved road, Skills, and Skill Packs. |
| IV — Patterns That Work—and Those That Fail (Ch 10–17) | Six bounded loop and workflow patterns, then a 12-card pattern catalog and a 16-card anti-pattern catalog. The catalogs reach well beyond Part IV's content. |
| V — Working Together Across Boundaries (Ch 18–19) | Multi-agent ownership, then external protocols (MCP, A2A). Ch 19 also hosts the LLM Gateway material. |
| VI — Security, Identity, and Control (Ch 20–23) | Threat model and layers, identity and delegation, effect safety, containment. |
| VII — Evidence, Evaluation, and Improvement (Ch 24–25) | Causal tracing versus audit, then evaluation and the governed learning loop. |
| VIII — Running the System in the Real World (Ch 26–28) | Governance operating model, release and recovery, performance economics. |
| Reference — Appendices A–L + Closing Perspective | Desk aids that mostly re-summarize the chapters. Some (I, J) are maintainer or tooling material. |

---

## 2. Chapter summaries

Each entry gives the chapter's **Purpose**, the **Mental model** it adds, what it **Assumes** the reader already knows, how its **Opening** works, and its **Closing** (the "Where this leads next" sentence, quoted, with a verdict).

### Ch 01 — What Turns an LLM Call into a Production System (`01-part-i.md:8`)
- **Purpose:** Show that the gap between a working agent demo and a dependable system is architectural, not intelligence.
- **Mental model:** "The model provides bounded reasoning. The surrounding system owns state, authority, effects, evidence, and recovery" (`01-part-i.md:160`). Adds the four agent levels; the uncertainty-ownership table; three per-step questions; the ten problems in four themes; the system "bands" (Figure 1-3); and control points (API, Agent, LLM, Tool, and MCP gateways, the human approval gate, the acceptance gate, and the evaluation/release gate).
- **Assumes:** LLM and tool-calling basics, Python, and distributed-systems vocabulary. The terms idempotency, effect ledger, RBAC/ABAC, and canary are glossed only by forward pointers (§ The vocabulary this book assumes).
- **Opening:** Strong. The case box, the design-choice box, the Harborlight contract table, then the Monday–Friday failure narrative.
- **Closing:** "With the system boundary established, Chapter 2 converts model intent into typed, validated tool proposals and a deterministic commit path." A mortgage bridge follows. **Sets up Ch 02 well.** The chapter itself is overloaded: three restatements of the thesis (`01-part-i.md:160`, `:315`, `:321`), plus the full gateway taxonomy, AP-01, and the supplier thread all before any mechanism.

### Ch 02 — From Model Output to Safe Action (`01-part-i.md:616`)
- **Purpose:** Make every model output a typed proposal that must cross deterministic gates before any effect.
- **Mental model:** The six gates. "Stale reasoning is not allowed to become an authoritative write" (`01-part-i.md:721`). Ten design principles in three groups. The "where distributed systems must remain authoritative" table. The Tool Use pattern card.
- **Assumes:** Ch 01's Tool Gateway and control points; JSON Schema; idempotency keys. It also uses ToolManifest, EffectRecord, and credential lease without definition.
- **Opening:** An intro paragraph, then four boxes (case, "what blocks", supplier, design choice), then § Why a valid-looking output is not enough, which restates the intro. That is a triple opening. § Six gates before anything changes names "the gates" before listing them (the list arrives at `01-part-i.md:669`).
- **Closing:** "With tools bounded, Chapter 3 defines the runtime contract that keeps applications portable across agent frameworks and model providers." A mortgage bridge names "the execution seam". **Good.**

### Ch 03 — Keep the Agent Framework in Its Lane (`01-part-i.md:900`)
- **Purpose:** Place the agent SDK behind AgentRuntime so framework state and objects never become enterprise truth.
- **Mental model:** "Let the framework run the agent; let the platform run the business" (`01-part-i.md:964`). Adds AgentStepRequest/AgentStepResult, the framework-versus-platform responsibility table, the restart test, the replaceability test, and SDK upgrades treated as behavior changes.
- **Assumes:** Ch 02's shell and OpenAI Agents SDK concepts. It silently also assumes ContextManifest, the capability envelope, TaskEnvelope, HumanActionAuthorizationRequest, RunManifest, the LLM Gateway, and the effect ledger.
- **Opening:** Two evidence/scope blockquotes, the supplier box, and the design choice, then C03. There is no "where the case stands" box, although C03 is the case's final implemented checkpoint.
- **Closing:** "Chapter 4 places that boundary inside the complete enterprise reference architecture." **Promise only partly kept.** Ch 04 never names AgentRuntime; it says "bounded agent workers" and "AgentSpec". *(Corrected in synthesis: the Ch 04 prose never names it, but Figure 4-2 has an "Agent Runtime" participant; see chapter-04.md.)* The chapter also pre-teaches large parts of Ch 11, 14, 15, 18, 20, and 22 (see §9 S5). Its template differs from every other chapter: no state-owner table, no evidence section, no "A sensible place to start", § What to verify before production *before* § If this fails in production, and a unique § What this chapter established.

### Ch 04 — Design the Architecture Around the Model (`02-part-ii.md:9`)
- **Purpose:** Turn the boundary rules into planes, layers, contracts, stores, trust boundaries, and regional cells.
- **Mental model:** Planes own decisions and layers carry the request path; every record has one authoritative writer. Adds the Run API, RunManifest, the artifact contract, the effect receipt, the CloudEvents event contract, and "where each kind of state belongs".
- **Assumes:** Nearly every later contract name. The plane table and § Core authoritative records list about 15 records defined in Ch 06–27, with no chapter pointers.
- **Opening:** No case box. The NORTHSTAR and DESIGN CHOICE boxes sit mid-chapter (`02-part-ii.md:79–83`). § Seven planes, eleven layers — which is which refers to "the plane table above", which is about 60 lines and four sections earlier.
- **Closing:** "The reference architecture names a knowledge plane but does not say what fills it; Chapter 5 defines the governed knowledge layer…" **Adequate, but the term mismatches.** No plane is called "knowledge plane". It is "Context, RAG, memory, Skills" in the table (`02-part-ii.md:41`), "Knowledge, context and memory" in Figure 4-1, and "Data and knowledge" among the layers.

### Ch 05 — Give Knowledge an Owner (`02-part-ii.md:342`)
- **Purpose:** Treat institutional knowledge as governed artifacts with owners, versions, scope, and provenance, so that retrieval is only one consumer.
- **Mental model:** Four consumption modes (context, reasoning, constraints, action). Extract → prove → project. Three-valued rule evaluation. Set operations over rule sets (union is not merge; contradiction is a result). Provenance fields. The Enterprise Knowledge Hub's six views.
- **Assumes:** RAG basics and Ch 04's planes. It is otherwise self-contained.
- **Opening:** Case box ("quotes the policy, then violates it") plus design choice. Good. § Treat knowledge as a set of products contains only a figure and a table; "products" is never defined.
- **Closing:** "Chapter 6 turns to the run itself: how context is assembled, how memory and workflow state differ…" **Good.** Template deviations: no "How X works", no "A workable implementation", and an If-fails symptom table. The H2 § Reference architecture: the Enterprise Knowledge Hub sits *after* § A sensible place to start.

### Ch 06 — Build Context Without Losing the Plot (`02-part-ii.md:587`)
- **Purpose:** Assemble each model call's context as an authorized, recorded projection, and keep workflow state, knowledge, memory, and context in separate stores.
- **Mental model:** Prompt = disposable projection. Authorization precedes retrieval and bytes materialize last. The four-tier instruction trust hierarchy. Memory writes are governed data effects. ContextManifest.
- **Assumes:** Ch 05 governance metadata. It also uses Skills (tier 2) before Ch 08 and artifact adoption before Ch 18/19.
- **Opening:** NORTHSTAR box plus design choice. Then § What the model is allowed to see, which contains only the state-owner table.
- **Closing:** "Context assembly completes the knowledge Part. Chapter 7 turns from what agents know to how teams build with it…" **Adequate Part transition.** Internal duplication: two context pipelines (10 stages at `02-part-ii.md:613` and 8 steps at `:692`, with different stage orders), three non-identical ContextManifest shapes (`:729`, `:739`, `:855`), and two state taxonomies (`:665`, `:679`).

### Ch 07 — Build a Paved Road for Agent Teams (`03-part-iii.md:9`)
- **Purpose:** Explain why a shared platform (contracts, adapters, golden path) beats each team rebuilding safety.
- **Mental model:** 16 platform capabilities split into platform and application responsibility; stable contracts behind replaceable adapters; the golden path from scaffold to improve; "test the contracts before you test the model".
- **Assumes:** Ch 03 AgentRuntime and Ch 04 contracts. It introduces RunContext, which is never defined, and mentions ChangeBundle, SBOM, and MCP/A2A ahead of their chapters.
- **Opening:** Evidence context only. No case box and no design choice, which breaks the Part III pattern (Ch 08 and Ch 09 have both).
- **Closing:** "The delivery path is established; Chapter 8 packages repeatable behavior as versioned Skills with explicit contracts and lifecycle controls." **Good.** Its § If this fails in production is the first-divergent-span debugging method that Ch 24 § Debugging method re-teaches.

### Ch 08 — Package Capabilities as Versioned Skills (`03-part-iii.md:179`)
- **Purpose:** Make the Skill (manifest, digest, lifecycle) the unit of reusable capability.
- **Mental model:** "Discovery is not permission": discovery is semantic, while resolution is deterministic and pins exactly one digest. The evidence-driven lifecycle Draft → Certified → Staged → Active → Deprecated → Revoked.
- **Assumes:** Ch 07. It uses `min_risk_tier`, `side_effect_class`, trajectory/threat tests, and A2A AgentSkill ahead of their chapters.
- **Opening:** NORTHSTAR box plus design choice. Good.
- **Closing:** "Individual Skills are governable; Chapter 9 composes them into domain packs without dissolving ownership or compatibility boundaries." **Good.**

### Ch 09 — Turn Skills into a Coherent Domain Platform (`03-part-iii.md:356`)
- **Purpose:** Ship compatible Skills, shared policy, and evaluations as an immutable Skill Pack.
- **Mental model:** A pack pins compatibility, and "installing a pack grants nothing".
- **Assumes:** Ch 08. Its code `status` set (`draft`, `active`, `deprecated`, `revoked`, at `03-part-iii.md:458`) silently drops Ch 08's Certified and Staged states.
- **Opening:** Case box plus design choice. Good.
- **Closing:** "The platform and capability model are complete; Chapter 10 begins the pattern sequence with the smallest bounded reasoning loop." **Abrupt Part transition.** Ch 10 never refers back to Skills or the platform, so readers lose the thread of how patterns run *on* the paved road.

### Ch 10 — Use ReAct Without Creating a Runaway Loop (`04-part-iv.md:9`)
- **Purpose:** Keep ReAct's adaptivity while moving turns, budgets, progress detection, and stopping outside the model.
- **Mental model:** The external controller owns limits; normalized repeat signatures and information gain; typed dispositions (answer, needs_input, delegate, proposed_action, budget_exhausted, failed); cost is set by the trajectory, not the prompt.
- **Assumes:** Ch 02 (mutations leave as proposals) and Ch 06 (observations are untrusted).
- **Opening:** Evidence context, case box, design choice. Good.
- **Closing:** "A bounded reason–act loop handles local uncertainty; Chapter 11 adds routing and handoff when known paths or specialists should own the work." **Good.** Note: Ch 01's vocabulary table claims Ch 10 develops "acceptance criteria" (`01-part-i.md:450`). It does not.

### Ch 11 — Route the Work Without Losing Ownership (`04-part-iv.md:162`)
- **Purpose:** Separate choosing a worker (routing) from transferring accountability (handoff).
- **Mental model:** The eligible set is computed before classification; "a routing decision cannot grant permission"; a handoff is acknowledged, atomic, and keeps the old owner accountable until it is accepted.
- **Assumes:** Ch 03 § Three meanings of handoff. It uses run envelope, child capability envelope, and cancellation lineage before Ch 18/21.
- **Opening:** Case box plus design choice. Good.
- **Closing:** "Routing selects among known capabilities; Chapter 12 addresses tasks whose decomposition must itself be proposed and validated." **Good.**

### Ch 12 — Turn Proposed Plans into Safe, Executable Work (`04-part-iv.md:376`)
- **Purpose:** Treat a model plan as typed IR that a deterministic compiler validates and freezes across revisions.
- **Mental model:** "Planning like compilation—not authorization". Plan IR; compile-time checks; replanning freezes committed facts. The "What should be agentic?" table.
- **Assumes:** Ch 08 bindings and Ch 11 envelopes. It uses risk classes `R1`/`R4` (`04-part-iv.md:465`, `:518`) and BudgetReservation/admission before Ch 22 and Ch 28.
- **Opening:** Evidence context, case box, design choice. Then § From candidate plan to executable work, which contains only a table.
- **Closing:** "Planning creates an executable structure; Chapter 13 adds independent evaluation and bounded revision without self-certification." **Good.**

### Ch 13 — Use Critique to Improve—Never to Self-Approve (`04-part-iv.md:642`)
- **Purpose:** Let reflection revise drafts, while independent, mostly deterministic acceptance decides.
- **Mental model:** Reflection asks "what is missing"; evaluation asks "does it meet the rubric". Executable checks run before any judge. A bounded optimization loop.
- **Assumes:** Ch 02 acceptance and Ch 12 acceptance engine.
- **Opening:** Case box plus design choice. Good.
- **Closing:** "Automated evaluation can improve candidates; Chapter 14 identifies decisions that require explicit human authority, correction, or recourse." **Good.**

### Ch 14 — Put People Where Their Judgment Matters (`04-part-iv.md:852`)
- **Purpose:** Bind human authorization to an immutable proposal, and separate it from intervention.
- **Mental model:** Authorization versus intervention (separate queues, roles, and terminal semantics); the proposal hash; expiry; supersession; reviewer fatigue as a production metric; operator console requirements.
- **Assumes:** Ch 03 § Bind approval to the exact proposal, which already taught most of this.
- **Opening:** Evidence context (WCAG), case box, design choice. Good.
- **Closing:** "Human control introduces waits and resumptions; Chapter 15 makes those waits durable and gives long-running work explicit state and recovery." **Strong.** Note: its design-review table has only 3 rows, against 5 elsewhere.

### Ch 15 — Keep Long-Running Work Alive Through Failure (`04-part-iv.md:1113`)
- **Purpose:** Model long-running work as replay-safe workflow history plus bounded activities, durable waits, and reconciliation.
- **Mental model:** Deterministic reducer versus activities; signals, timers, and checkpoints; terminal correctness (Succeeded only via acceptance; InterventionRequired); the ten-step canonical control flow.
- **Assumes:** Ch 04 Run API and CloudEvents. It uses capability envelope, downscoped credential, risk classes, and compensation before Ch 21/22.
- **Opening:** Evidence context, case box (the nine-day wait), design choice. Good.
- **Closing:** "The core patterns are now defined; Chapter 16 compares them by the obligation each protects, the shortcut it replaces, and what it costs." **Inaccurate.** Ch 16 catalogs P-06 through P-12, whose mechanics (task envelopes, capability envelopes, the effect ledger, run graphs, risk-tiered gates, admission and backpressure) are taught in Ch 18–28. Also, § Event-driven resume flow (`04-part-iv.md:1194`) is an empty heading.

### Ch 16 — Choose Patterns That Fit Real Enterprise Work (`04-part-iv.md:1356`)
- **Purpose:** Offer decision-aid cards P-01 through P-12, one per concern.
- **Mental model:** Start from the obligation, then choose the smallest pattern. Each card follows "tempting shortcut → better design → what to watch".
- **Assumes:** Everything in the book. Only P-01 through P-05 and P-12 rest on chapters already read.
- **Opening:** No boxes, two framing H2s, a decision-tree figure.
- **Closing:** "Pattern selection is easier when failure shapes are visible; Chapter 17 recasts recurring anti-patterns as measurable replacement decisions." **Fine.** Structurally, all 12 H2s contain exactly one H3, and there are no closing review sections.

### Ch 17 — Architecture Patterns That Fail in Production (`04-part-iv.md:1499`)
- **Purpose:** Turn production symptoms into named anti-patterns (AP-01 through AP-16), each with a replacement and repair metrics.
- **Mental model:** Each card is one mistake: "a probabilistic component was handed a job that belongs to deterministic infrastructure" (`04-part-iv.md:1513`). Cards are grouped by the boundary violated. The symptom-first lookup table.
- **Assumes:** The whole book. AP-03, AP-08, AP-12, AP-14, AP-15, and AP-16 correct with mechanisms from Part V–VIII.
- **Opening:** Two framing H2s plus Figure 17-1.
- **Closing:** "After removing unsafe local architectures, Chapter 18 considers when multiple agents add justified specialization rather than accidental complexity." **Fine**, but AP-08 and AP-11 have already given Ch 18's conclusions.

### Ch 18 — Coordinate Specialists Without Losing Control (`05-part-v.md:9`)
- **Purpose:** Make multi-agent collaboration a durable state machine: one owner per task, narrowed child authority, explicit joins.
- **Mental model:** The topology decision table; explicit fan-in (all, quorum, first-valid, fallback); the orchestration rules; monotonic child authority (with code).
- **Assumes:** Ch 03/11 handoff and Ch 12 plan revisions. It shows CapabilityEnvelope code before Ch 21 explains envelopes.
- **Opening:** Evidence context, case box, design choice. Good.
- **Closing:** "Multi-agent collaboration inside one platform is only part of the problem; Chapter 19 extends those controls to external tools, agents, and model providers." **Good**, though "model providers" foreshadows the misplaced LLM Gateway section.

### Ch 19 — Crossing System Boundaries: MCP, A2A, and Local Control (`05-part-v.md:386`)
- **Purpose:** Terminate MCP and A2A at local gateways and re-establish trust at each protocol boundary. It then (separately) defines the LLM Gateway.
- **Mental model:** MCP is for tools/resources (the caller owns the work); A2A is for tasks (ownership transfers). A registry entry does not grant trust. The federated-task state mapping. Then the LLM Gateway's scope, controls, policy-first routing, and metrics.
- **Assumes:** Ch 18 TaskEnvelope, Ch 01 gateway table, Ch 21 audience binding (`05-part-v.md:600`).
- **Opening:** Evidence context, case box, design choice. The intro sentence admits "It closes by placing the LLM Gateway among those boundaries" (`05-part-v.md:404`).
- **Closing:** "Gateways control protocol and model access, but not the entire attack surface; Chapter 20 introduces defense in depth across all agentic trust boundaries." **Good.**

### Ch 20 — Security Starts Outside the Prompt (`06-part-vi.md:16`)
- **Purpose:** Place detection, policy, and enforcement at boundaries; catalog the threats; define incident response.
- **Mental model:** Detector ≠ policy point ≠ enforcement point (`06-part-vi.md:32`). The nine defense layers. "Trust is not inherited through a chain." Threat cards T-01 through T-16. The worked injected-document example. Detect → Contain → Revoke → Reconcile → Eradicate → Recover → Learn.
- **Assumes:** Ch 03 § Guardrails and authorization solve different problems (same argument, earlier), and Ch 04 trust boundaries.
- **Opening:** Evidence context only (no case box, no design choice), then two framing H2s.
- **Closing:** "The guardrail architecture establishes defense in depth; Chapter 21 makes it enforceable per caller…" **Sets up Ch 21, but it labels Ch 20 a "guardrail architecture", which contradicts its own § Guardrails help, but they are not the security boundary.**

### Ch 21 — Carry Identity, Narrow Authority (`06-part-vi.md:333`)
- **Purpose:** Carry subject plus actor identity everywhere, and derive short-lived, narrowing grants.
- **Mental model:** The dual principal; RBAC for eligibility, ABAC for the exact request; the authorization tuple; capability envelope (scope) versus credential lease (proof); authorization by intersection; revocation after waits.
- **Assumes:** Ch 18's identical CapabilityEnvelope code, and risk classes R3/R4, forward-referenced as "(risk classes, Chapter 22)" (`06-part-vi.md:495`).
- **Opening:** Evidence context, case box, design choice. § Keep the user, workload, and grant distinct and § Three identities every decision should preserve name two different triads.
- **Closing:** "Identity and delegated authority answer who may ask; Chapter 22 proves whether a specific tool effect may execute, commit, retry, or recover." **Good.**

### Ch 22 — Make External Effects Safe to Retry (`06-part-vi.md:634`)
- **Purpose:** Make writes retry-safe with logical effect keys, intent hashes, preconditions, receipts, and reconciliation of unknown outcomes.
- **Mental model:** The effect state machine (Reserved → Executing → Committed, plus Declined, Unknown, Partial, Compensating, Compensated, and InterventionRequired). Approval, idempotency, preconditions, and receipts each close a different failure. ToolManifest. Risk classes R0–R4. Failure-response table. Sagas, outbox/inbox, graceful degradation.
- **Assumes:** Ch 02/03/15 and AP-04/05, which already taught the core idea.
- **Opening:** Case box plus design choice. Good.
- **Closing:** "Protected effects are governed; Chapter 23 contains the remaining execution, egress, data, privacy, and supply-chain blast radius." **Fine.** Internally duplicated: two § A workable implementation sections (`06-part-vi.md:726`, `:846`) and two Required-analysis tables (`:692`, `:811`). It is a reliability chapter sitting in the Security Part.

### Ch 23 — Contain the Damage When a Model Is Manipulated (`06-part-vi.md:1021`)
- **Purpose:** Limit what a manipulated plan can reach: capability, data, credentials, execution, network, effects, supply chain, governance.
- **Mental model:** Eight containment layers; sandbox and egress rules; taint lineage; the scoped kill switch; the governance record.
- **Assumes:** Ch 20 (same premise) and Ch 21/22.
- **Opening:** Evidence context, case box (the injected document again), design choice. Then three consecutive H2s restating "assume compromise" (`06-part-vi.md:1033`, `:1042`, `:1053`).
- **Closing:** "Security controls now produce events and evidence; Chapter 24 turns those signals into end-to-end traces that operators can reconstruct." **Good.**

### Ch 24 — Follow a Run from Request to Verified Outcome (`07-part-vii.md:9`)
- **Purpose:** Build one causal trace across asynchronous work, kept separate from the audit ledger.
- **Mental model:** Diagnostics (trace) versus proof (audit); span links; the debugging method; span types; the operator scorecard; replay that cannot create live effects.
- **Assumes:** Ch 15 histories and Ch 22 effect states.
- **Opening:** Evidence context, case box, design choice. Good.
- **Closing:** "Tracing explains what happened; Chapter 25 determines whether the trajectory and outcome were acceptable and whether a change is safe to ship." **Good.** Ch 24 has no "A workable implementation"; its implementation components ended up in Ch 25.

### Ch 25 — Improve the System Without Handing It Control (`07-part-vii.md:224`)
- **Purpose:** Gate change on immutable datasets, trajectory checks, calibrated judges, and slices, and close the learning loop without self-certification.
- **Mental model:** Outcome versus path; the evaluation pyramid; the slice regression worked example; the ten-stage learning loop; runtime adaptation versus offline improvement; improvement paths by layer.
- **Assumes:** Ch 07 test pyramid and Ch 13 judges. It uses "release bundle" (Ch 27) and "use-case inventory" (Ch 23/26/27).
- **Opening:** Evidence context, case box, design choice. Good.
- **Closing:** "The improvement loop proposes and validates change; Chapter 26 assigns decision rights, risk tiers, approvals, exceptions, and accountability." **Good.** Its design-review questions on release bundles and rollback (`07-part-vii.md:490–491`) belong to Ch 27.

### Ch 26 — Make Governance Part of How the Platform Runs (`08-part-viii.md:9`)
- **Purpose:** Make governance an owned control loop with proportional tiers, exceptions that expire, and review cadences.
- **Mental model:** Accountable owner per decision class; risk tiers 0–4; the distinction between principles, standards, policy-as-code, and configuration; review cadence.
- **Assumes:** Ch 23/25 governance records; ValidationReport (never defined).
- **Opening:** Evidence context only, then two framing H2s.
- **Closing:** "Governance defines who may release change; Chapter 27 makes releases immutable, promotable, observable, reversible, and recoverable." **Good.** It is the leanest chapter (no "A sensible place to start", no implementation section). Its implementation material (inventory, exceptions API, GovernanceRecord) sits in Ch 27.

### Ch 27 — Release New Behavior Without Breaking Work in Flight (`08-part-viii.md:126`)
- **Purpose:** Release immutable behavior bundles; roll back *assignment*, not history; recover regions safely.
- **Mental model:** "Treat the full behavior as the release"; the compatibility matrix; rollback of new work only; control plane versus regional execution planes; versioned objects; promotion as a chain of evidence.
- **Assumes:** Ch 15 compatibility, Ch 25 learning loop, Ch 04 cells.
- **Opening:** Evidence context (NIST SP 800-61 incident lifecycle, which the chapter barely covers; Ch 20 does), then the NORTHSTAR box and design choice.
- **Closing:** "The release lifecycle is controlled; Chapter 28 sizes the system and optimizes cost, latency, capacity, and reliability around verified outcomes." **Good.** It is overloaded: deployment topology, baseline technology stack, governance controls, and DR, alongside release.

### Ch 28 — Treat Performance as a Business Decision (`08-part-viii.md:463`)
- **Purpose:** Optimize cost and latency per verified successful outcome through admission, budgets, fair scheduling, and safe degradation.
- **Mental model:** Four measurements; Little's Law; reserved capacity; the scaling layers; "optimize in the order that changes outcomes"; illustrative starting limits.
- **Assumes:** Ch 19 model routing and Ch 22 degradation.
- **Opening:** Evidence context, NORTHSTAR box, design choice. Good.
- **Closing:** "The architecture narrative is complete. The appendices provide decision aids, runbooks, contracts, framework evidence, references, maintenance criteria, and production acceptance checks…" **Inaccurate summary of the appendices.** No appendix is about "maintenance criteria". It omits the glossary, research, limits, roadmap, companion guide, and coding-agent prompt, and does not mention the Closing Perspective.

---

## 3. Concept registry

The "Re-taught at" column lists only substantive re-explanations. Each one is classified as **R** (reinforcement: it adds a new facet or application) or **D** (redundancy: same content, often with drift).

| Concept | First introduced | Canonical / fullest | Re-taught at | Classification | Recommended home |
| --- | --- | --- | --- | --- | --- |
| Model proposes; deterministic systems commit (core thesis) | Front matter § The engineering contract behind the architecture (`00-front-matter.md:100`) | Ch 02 § Structured output is a protocol boundary / § Design principles | Ch 01 § The gap between a useful demo and a dependable system (`:160`); Ch 01 § Level four — an enterprise agentic system (`:315`, `:321`); Ch 02 BOUNDARY RULE (`01-part-i.md:779`); Ch 03 § Start with a concrete scenario (`:964`); Ch 04 § Where truth lives; Part VI intro (`06-part-vi.md:9`); Closing Perspective | Ch 01 three times = D; the others R (new framing) | Ch 02 |
| Four agent levels | Ch 01 § Four very different things we call an agent | same | Ch 18 § Topology decision table (rows 1–2) partially | R | Ch 01 |
| Who owns each uncertainty / model-may-vs-may-not tables | Ch 01 § Which component should own each uncertainty | Ch 04 § Where truth lives | Ch 02 § Where distributed systems must remain authoritative; Ch 03 § Runtime responsibility versus enterprise responsibility; Ch 03 § Responsibility map; Ch 12 § What should be agentic? | Six ownership tables = mostly D (same "model may / platform owns" axis); Ch 12 R (work types) | Ch 01 (uncertainty) + Ch 04 (truth); others reference |
| Three per-step questions (authority, retry safety, reconstructability) | Ch 01 § What changes when the prototype meets production | same | Ch 21 § What an authorization decision must answer (Q1 as a tuple) | R | Ch 01 |
| Ten problems / four themes | Ch 01 § Ten problems, four themes | same | Appendix F (12 limits); Appendix A | R | Ch 01 |
| Control points / gateway taxonomy | Ch 01 § Each control point answers a different question (`01-part-i.md:515`) | Ch 01 (only full definition) | Ch 19 § What belongs at the LLM Gateway—and what does not (table `05-part-v.md:558`, adds "Orchestration layer"); Ch 04 § Architecture layers (renames) | Ch 19 table D; Ch 04 D with drift | Ch 01 (or one gateway section in Ch 04) |
| Tool Gateway pipeline | Ch 01 § Each control point… (`01-part-i.md:531`) | Split: Ch 02 § How Tool Use works in practice + Ch 22 § Give tools explicit contracts and narrow authority / § Invocation sequence | Ch 03 § A tool is not the enterprise API, § Reauthorize the exact resource; Ch 21 "Connector Gateway/PEP" (`06-part-vi.md:448`); Ch 22 two implementation sections | Ch 02 restates Ch 01 almost verbatim = D; Ch 03 R (exact-resource example); Ch 21 D under another name | Ch 22 for the full contract; Ch 02 for the introduction only |
| MCP Gateway | Ch 01 § Each control point… (`:538`) | Ch 19 § Two protocols, two responsibilities | Ch 20 T-13; Ch 22 MCP paragraph (`06-part-vi.md:724`); AP-12 | Ch 22 D; T-13/AP-12 R | Ch 19 |
| LLM Gateway | Ch 01 control-point table (`:526`) | Ch 19 § What belongs at the LLM Gateway… through § What to measure at the LLM Gateway (`05-part-v.md:552–593`) | Ch 04 "model gateway" (`02-part-ii.md:22`, `:87`, `:137`); Ch 07 platform table; Ch 28 § Optimize in the order… item 4 and PERFORMANCE box (`08-part-viii.md:653`) | Ch 28 box D ("route on policy first" = Ch 19 § Filter for policy…) | Move out of Ch 19 (see §9 S4) |
| Agent Gateway | Ch 01 control-point table (`:525`) | **Never developed** | Ch 19 table row (`05-part-v.md:561`); T-12 "Agent gateway" lowercase | Orphan | Define once, or merge with "A2A Gateway" |
| Six gates (propose → validate → authorize → commit → verify → accept) | Ch 02 § Six gates before anything changes | Ch 02 § One proposal, six gates | Ch 03 § The same rule applies to writes (8 steps); Ch 03 § The complete execution path (9); Ch 04 § End-to-end responsibility flow (8); Ch 15 § Canonical control flow step 8 ("propose → preview → approve → commit"); Ch 16 P-05; Ch 20 § Follow the request across each trust boundary (`06-part-vi.md:93`); Ch 22 § Give tools… Required-analysis row (`:697`) and § Invocation sequence; Appendix A item 6 | D with drift (step counts 5–9, three names) | Ch 02; elsewhere "the six gates" by name |
| Validation ≠ authorization; schema validity ≠ correctness | Ch 02 § One proposal, six gates (`01-part-i.md:704`) | same + COMMON PITFALL (`:783`) | Ch 03 § Reauthorize the exact resource | R | Ch 02 |
| Expected version / optimistic concurrency | Ch 02 (`01-part-i.md:713`) | Ch 22 § A reliable protocol for changing the outside world + property table | Ch 18 § Recommended orchestration rules "Shared state"; Ch 22 Q (`06-part-vi.md:1015`) | R | Ch 22 (Ch 02 introduces) |
| Deterministic acceptance / acceptance engine / acceptance gate | Ch 01 uncertainty table (`:348`) and § Each control point (`:548`) | **Split:** Ch 02 § Deterministic acceptance; Ch 13 § Give evaluation its own independent path | Ch 10 § Acceptance and failure semantics; Ch 12 Acceptance Engine row (`04-part-iv.md:487`); Ch 15 § Terminal correctness; AP-07; Ch 18 rule "Termination" | Scattered, no single home; Ch 01 vocabulary points to Ch 10/12 incorrectly | Ch 02 (expand) or Ch 13 |
| Run/task terminal states and dispositions | Ch 03 dispositions (sufficient / insufficient / additional evidence) | **None** | Ch 04 step 7 (`02-part-ii.md:56`); Ch 10 (`04-part-iv.md:49`); Ch 15 § Terminal correctness; AP-07 (`04-part-iv.md:1815`); Ch 18 (`05-part-v.md:81`); Ch 19 § State mapping and ownership; Appendix B (`09-appendices.md:57`) | D with drift (§6 T12) | Ch 15 (run) + Ch 22 (effect) |
| Design principles (ten) / engineering contract (six) | Front matter § The engineering contract… | Ch 02 § Design principles | Ch 01 three questions; Closing Perspective | Front-matter list and Ch 02 list overlap but differ = D | Ch 02; front matter references it |
| Where distributed systems remain authoritative | Ch 02 § Where distributed systems must remain authoritative | same | (overlaps the ownership tables) | — | Ch 02 |
| AgentRuntime / AgentStepRequest / AgentStepResult | Ch 03 § Why the SDK sits behind AgentRuntime | Ch 03 § The request is bounded before the model sees it | Ch 07 § Keep contracts stable while frameworks change (as AgentSpec/RunContext); Ch 07 § SDK example note; P-12; Appendix C "AgentStep" | Ch 07 D with renaming | Ch 03 |
| Framework state vs business state; restart test; replaceability test | Ch 03 § Framework state versus business state | Ch 03 (`01-part-i.md:1109–1242`) | Ch 15 § Durable state is more than chat history; AP-02 | R | Ch 03 (framework) / Ch 15 (durability) |
| Handoff vs agent-as-tool vs durable child task | Ch 03 § Three meanings of handoff | Ch 11 § Routing and handoff are different events + § How Handoff works in practice | Ch 18 § Topology decision table (Manager / Handoff rows), § Recommended orchestration rules "Handoff", Q (`05-part-v.md:377`); Ch 03 Q (`01-part-i.md:1307`) | Ch 03 full preview = D; Ch 18 Q = D | Ch 11 |
| Guardrails ≠ authorization; detector / policy point / enforcement point | Ch 03 § Guardrails and authorization solve different problems | Ch 20 § Guardrails help, but they are not the security boundary | Ch 19 "Filters are evidence" (`05-part-v.md:579`); Part VI intro | Ch 03 D (same argument and example); conflicting usage in Ch 05/28 (§6) | Ch 20 |
| One retry owner per failure class | Ch 03 § One retry owner | Ch 22 § The mechanics that make retries safe | AP-04 (with the 3×3×2 math); Ch 15 checklist; Ch 19 LLM Gateway row; Ch 22 § Choose the response that matches the failure + scaling bullet (`06-part-vi.md:903`); Ch 28 limits row | AP-04 R; Ch 03 D (full table); Ch 22 internally ×3 = D | Ch 22 |
| Unknown outcome ("timeout ≠ failure") | Ch 01 Wednesday (`01-part-i.md:104`) | Ch 22 § A reliable protocol for changing the outside world + § The lifecycle of an external effect | Ch 02 Verify gate; Ch 04 § Effect receipt; Ch 03 § One retry owner; Ch 10; Ch 15 PRODUCTION CONSIDERATION (`04-part-iv.md:1253`); P-08; AP-05 (code); Ch 24 worked example; Ch 28 table; Appendix B runbook | Five pre-teachings before Ch 22 = D; Ch 24/28 R (application) | Ch 22 |
| Idempotency key / logical effect key / intent hash | Ch 01 vocabulary (`:443`) | Ch 22 (`06-part-vi.md:669`, `:773`, `:840`) | Ch 03 key composition (`01-part-i.md:1197`); Ch 15 activity; P-08; AP-05 | R | Ch 22 |
| Effect ledger / EffectRecord / effect receipt | Ch 01 vocabulary (`:444`) | Ch 22 § Records worth preserving (×2) + § Effect-state ledger | Ch 02 state table + Governed Tool Gateway example; Ch 03 § The same rule applies to writes; Ch 04 § Effect receipt; P-08; Appendix C | Ch 04 receipt D; Ch 22 internal D (two EffectRecord field lists, `:769` vs `:870`) | Ch 22 |
| Compensation / sagas | Ch 01 vocabulary → "Chapter 15" (`:445`) | Ch 22 § The mechanics that make retries safe ("Sagas") + § Where transaction guarantees begin and end | Ch 15 § Terminal correctness (mention only) | Vocabulary pointer is wrong | Ch 22 |
| Outbox / inbox / CloudEvents envelope | Ch 02 authority table (`01-part-i.md:766`) | Ch 04 § Event contract + § CloudEvents and outbox contracts; Ch 22 § Where transaction guarantees begin and end | Ch 14 § Workflow integration; Ch 15 § Event architecture; Ch 22 OutboxRecord/InboxReceipt + Q | Ch 15 D; Ch 04 code vs Ch 22 record = D | Ch 04 (envelope) + Ch 22 (delivery semantics) |
| RunManifest / per-run version pinning | Ch 01 state table (`01-part-i.md:188`, undefined) | Ch 04 § RunManifest | Ch 03 § Framework upgrades are behavioral changes (field table); Ch 05 PRODUCTION CONSIDERATION; Ch 07 § CLI and delivery workflow; Ch 15 Admit/Snapshot; Ch 27 § Treat the full behavior as the release + Required analysis (`08-part-viii.md:230`); Appendix C | Ch 03 and Ch 04 field sets differ (D with drift); Ch 27 conflates it with ReleaseManifest | Ch 04 (+ explicit relation to ReleaseManifest in Ch 27) |
| ReleaseManifest / release bundle / ChangeBundle | Ch 04 plane table (`02-part-ii.md:44`) | Ch 27 § Treat the full behavior as the release / § Release compatibility check | Ch 07 § How a capability moves… and golden path; AP-15/AP-16; Ch 25 learning loop + Q (`07-part-vii.md:490`) | Ch 25 Q D of Ch 27 Q (`08-part-viii.md:453`) | Ch 27 |
| Run API | Ch 04 § Run API | Ch 15 § The contracts between components (adds pause/resume/migrate) | — | D (two endpoint tables for the same resource) | Ch 15, with Ch 04 summarizing *(Superseded in synthesis: Ch 04 owns the one base table and Ch 15 lists only durable-execution additions; overall-book-review.md §D-03.)* |
| Planes vs layers / reference architecture | Ch 01 § The system as a set of responsibilities (bands) | Ch 04 § Seven planes, eleven layers — which is which | Ch 27 § A production topology that is easy to reason about; Appendix J deliverable 3 (12 layers) | D with drift (§6 T2) | Ch 04 |
| Global control plane vs regional execution cells | Ch 01 state table "regional cell" | Ch 04 § Turn the diagram into enforceable contracts | Ch 27 § A production topology… / § Deployment guidance / Q (`08-part-viii.md:455`) | Ch 27 D, renamed "regional execution plane" | Ch 04 design; Ch 27 operations, by reference |
| Trust boundaries | Front matter principle 4 | Ch 04 § Trust boundaries (8-row table) | Ch 20 § Follow the request across each trust boundary (Figure 20-2) | Ch 20 R (but never cites Ch 04's table) | Ch 04 table; Ch 20 cites it |
| State taxonomy / where state belongs | Ch 03 § Framework state versus business state | Ch 06 § State taxonomy and storage | Ch 04 § Where each kind of state belongs (9 stores); Ch 06 § Four kinds of state… (4 kinds); Appendix J deliverable 6 | Ch 04 vs Ch 06 D (store-centric vs class-centric) | Ch 06 (absorb the Ch 04 store table) *(Superseded in synthesis: Ch 04 keeps the physical-store table, Ch 06 keeps the five context sources and points to it; overall-book-review.md §D-15.)* |
| ContextManifest | Ch 03 § The request is bounded… (`01-part-i.md:1043`, undefined) | Ch 06 § Records worth preserving | Ch 06 JSON (`02-part-ii.md:739`) and code (`:855`) — three shapes in one chapter; P-03; AP-02 code; Ch 20; Ch 24; Appendix C | Internal D with drift | Ch 06 (unify into one shape) |
| Context assembly pipeline | Ch 06 § How context is assembled (10 stages) | same | Ch 06 § Context assembly pipeline (8 steps); P-03 runtime flow (retrieval *before* policy, `04-part-iv.md:1401`); Ch 21 § Data-plane controls | Ch 06 internal D; P-03 contradicts "authorization is stage three" | Ch 06 § How context is assembled |
| Instruction trust hierarchy / content–instruction separation | Ch 06 § The trust hierarchy of instructions | same | Ch 03 protection stack step 1; Ch 20 T-01/T-02 and § Worked example; Ch 23 § Threats and required controls row 1 | R; label vocabulary drifts (§6 T19) | Ch 06 (mechanism) / Ch 20 (threat) |
| Memory (working vs long-term; governed write) | Ch 06 § Memory is not a bag of embeddings | Ch 06 § How Memory works in practice | Ch 07 platform row; P-04 (working / episodic / semantic / profile); AP-13 (code); T-06; Ch 23 threats row; Ch 25 Memory row; Appendix F #7 | AP-13 R; P-04 taxonomy drift | Ch 06 |
| Knowledge as governed products; four consumption modes; Knowledge Hub | Ch 05 § Treat knowledge as a set of products | Ch 05 § Why similarity cannot tell you what to trust / § Reference architecture: the Enterprise Knowledge Hub | AP-09 | R | Ch 05 |
| Provenance | Ch 01 vocabulary → "Chapters 5 and 6" | Ch 05 § Why provenance determines what you can trust | Ch 06 (provenance service, segments); Ch 20/23 provenance labels; Ch 09/23/27 build provenance (SLSA) | Two meanings (content lineage vs build provenance), never distinguished | Ch 05 (content) / Ch 27 (supply chain) |
| Policy prose → enforceable rule (extract / prove / project; three-valued) | Ch 05 § Business rules as enforceable constraints | Ch 05 § Turn policy prose into logic the system can enforce | — | unique | Ch 05 |
| Knowledge set operations | Ch 05 § Combine knowledge without flattening its differences | same | — | unique | Ch 05 |
| Discovery ≠ permission / eligibility | Ch 02 principle 5 (`01-part-i.md:747`) | Ch 08 § Discovery is not permission | Ch 05 § Capability and API catalog; Ch 09 § Installing a pack grants nothing; Ch 11 eligible route set; Ch 19 § Registry model; AP-12; Ch 20 Q (`06-part-vi.md:325`); Ch 22 Discovery Service / ToolEligibility | Mostly R; Ch 20 Q D | Ch 08 (generalize to tools there or in Ch 22) |
| Skill / manifest / resolution / lifecycle | Ch 04 plane table | Ch 08 § The Skill manifest / § Skill lifecycle | Ch 06 trust tier 2; Ch 07 platform row; Ch 25 Skills row; Ch 27 versioned objects | R; lifecycle drift in Ch 09 code *(Corrected in synthesis: Ch 08's own example `skills_registry.py` has the same four-state `status`, and it is included in the digest; see C08-R05.)* | Ch 08 |
| Skill Pack | Ch 09 | Ch 09 § Installing a pack grants nothing | Appendix H | — | Ch 09 |
| Paved road / golden path | Ch 01 band "Platform and operations" | Ch 07 § Make the safe path the easy path | P-12 | R | Ch 07 |
| Test pyramid / evaluation pyramid | Ch 07 § Test the contracts before you test the model (Figure 7-5, 4 tiers) | Ch 25 § Evaluation pyramid (7) + § Layer tests from contracts to outcomes (9) | Ch 08 certification list; Appendix G minimum bar; Appendix L | Three pyramids with 4/7/9 levels = D | Ch 25 (Ch 07 points to it) |
| Bounded ReAct / no-progress detection | Ch 10 | Ch 10 § Keep the feedback loop inside external limits | P-01; AP-11; Appendix A/B | R | Ch 10 |
| Routing (work) | Ch 01 uncertainty table | Ch 11 § A routing decision cannot grant permission | Ch 18 Router component; Ch 25 Routing row | R | Ch 11 |
| Routing (model) | Ch 01 control-point table | Ch 19 § Filter for policy before optimizing cost or quality | Ch 28 § Optimize in the order… #4; PERFORMANCE box | Ch 28 D | wherever the LLM Gateway lands |
| Plan IR / compiler / replanning | Ch 12 | Ch 12 § Plan IR / § Compile-time checks / § Runtime revision algorithm | Ch 15 step 4; Ch 18 plan-change rule + `plans:revise` API (`05-part-v.md:108`, same as `04-part-iv.md:496`) | Ch 18 API D | Ch 12 |
| Reflection vs evaluation; judge limits | Ch 13 | Ch 13 § Improve the answer without letting the system certify itself | Ch 25 § Judge the outcome and the path separately; AP-10; Ch 12 last row; Ch 25 COMMON PITFALL | R | Ch 13 (runtime) / Ch 25 (release) |
| Human action authorization vs intervention; proposal-bound approval | Ch 01 § Each control point… (`:542`) | Ch 14 § Separate authorization from intervention / § Approval contract | Ch 03 § Human approval: interruption versus record + § Bind approval to the exact proposal; AP-06 (code); Ch 22 property table + Q (`06-part-vi.md:1014`, verbatim = `04-part-iv.md:1107`); Appendix B | Ch 03 near-full preview = D; Ch 22 Q verbatim D | Ch 14 |
| Operator console / operator actions | Ch 04 Experience layer | Ch 14 § Operator console requirements | Ch 23 kill switch; Appendix G | R | Ch 14 |
| Durable execution (workflow vs activity, replay, signals, timers, checkpoints) | Ch 01 ten-problems row "Long-lived execution" | Ch 15 § Durable execution contract / § Execution and persistence rules | Ch 03 § The restart test; P-11; AP-01; Ch 27 § Compatibility and long-running execution; Appendix D | R | Ch 15 |
| End-to-end run lifecycle walkthrough | Ch 03 § The complete execution path | Ch 15 § Canonical control flow | Ch 04 § End-to-end responsibility flow | Three walkthroughs = D | Ch 04 overview + Ch 15 detail; drop Ch 03's |
| Supervisor/worker, joins, task ownership | Ch 03 durable delegation row | Ch 18 | P-06; AP-08; Ch 19 § Ownership and failure rules; Ch 22 child-failure row | R | Ch 18 |
| TaskEnvelope | Ch 03 § Three meanings of handoff (undefined) | Ch 18 § Durable child-task contract + Ch 19 § What the TaskEnvelope needs to carry | Ch 19 A2ATaskEnvelope code (`05-part-v.md:621`, first ten fields identical to Ch 18 — *Corrected in synthesis: eight fields are shared; `owner_agent`→`owner` and `state_version`→`expected_version` are renamed, and `capability` and `cancellation_parent_id` are dropped; see chapter-18.md*); Appendix C | D | Ch 18 (local); Ch 19 federated delta only |
| Monotonic delegation / child narrowing | AP-11 (budgets) | Ch 21 § Three identities every decision should preserve (`06-part-vi.md:385`) + SECURITY box | Ch 18 § Monotonic child authority (code identical to Ch 21 § Capability-envelope subset proof); T-09 | Exact duplicate code = D | Ch 21 |
| Capability envelope | Ch 01 (`01-part-i.md:404`, undefined) | Ch 21 § Records worth preserving + Q (`06-part-vi.md:625`) | Ch 03; Ch 11; Ch 15; P-07; AP-03; Ch 18 | R, but under five names (§6 T6) | Ch 21 |
| Identity triad (subject / actor / purpose) | Ch 03 Identity field group (`01-part-i.md:1041`) | Ch 21 § Three identities every decision should preserve | Ch 04 RunManifest; Ch 21 § Keep the user, workload, and grant distinct (a different triad) | Internal drift | Ch 21 |
| Credential lease / last-hop credential / token exchange / audience binding | Ch 01 § Each control point… and vocabulary | Ch 21 § Carry identity all the way to the data / § Records worth preserving | Ch 02; Ch 03 credentials row; Ch 22 Credential Broker; Ch 23 SecretLease + `credentials:lease` API (vs Ch 21 `credentials:exchange`) | Ch 23 D (duplicate API and entity) | Ch 21 |
| RBAC/ABAC; authorization tuple; intersection | Ch 01 vocabulary | Ch 21 § What an authorization decision must answer | Ch 14 approver RBAC | R | Ch 21 |
| Risk classes R0–R4 | Ch 12 (`04-part-iv.md:465`, `:518`, unexplained) | Ch 22 § Risk classes | Ch 21 (`06-part-vi.md:495`); Ch 23 (`:1178`); Ch 24 (`07-part-vii.md:145`); Appendix J | Used before definition | Ch 22, or move earlier (§9 S6) |
| Governance risk tiers 0–4 | Ch 08 `min_risk_tier` (`03-part-iii.md:233`) | Ch 26 § Match the control to the risk | P-10; Ch 25 Approve stage | Collides with R0–R4 (§6 T11) | Ch 26 |
| Threat catalog T-01..T-16 | Ch 20 § How attacks show up in practice | same | Ch 23 § Threats and required controls (11 rows) | D | Ch 20 |
| Defense-in-depth layers | Ch 03 protection stack (7) | Ch 20 § How the layers reinforce one another (9) | Figure 20-1 (6); Ch 23 § Containment layers (8) + boundary table (5); Part VI intro order | D with inconsistent counts | Ch 20 (layers); Ch 23 (mechanisms) |
| "Assume the model is compromised" | Ch 20 § Respond as if the model can be compromised | Ch 23 § Start from the assumption that the model can be manipulated | Ch 23 § Why the model should be treated…, § Contain the blast radius…; Appendix F #1 | D (two chapters with the same premise; Ch 23 states it three times) | Ch 23 (premise) |
| Incident lifecycle (Detect → … → Learn) | Ch 20 § Respond as if the model can be compromised | same | Ch 23 `incidents:{id}:contain` API; Ch 27 evidence context cites NIST 800-61 without content; Appendix B | Misplaced relative to Ch 27's stated scope | Ch 20, or Part VIII |
| Kill switch | Ch 04 Q (`02-part-ii.md:336`) | Ch 23 § Scoped operational kill switch | Ch 20 Contain row; Ch 27 Emergency Control; Appendix G/L | R | Ch 23 |
| Sandbox and egress | Ch 02 § Scaling the shell | Ch 23 § Sandboxing and egress rules | Ch 04 Execution plane; T-14; Ch 22 Sandbox Broker + SandboxLease (`06-part-vi.md:770` vs Ch 23 `:1137`) | Ch 22 entity D | Ch 23 |
| Supply chain (SBOM, SLSA, signing) | Ch 07 § How a capability moves… | Ch 27 § Release attestation verification / evidence row | Ch 09 evidence row; T-16; Ch 23 layer 7 + SupplyChainAttestation | R | Ch 27 |
| Governance record / use-case inventory | Ch 23 § Containment layers (governance paragraph, `06-part-vi.md:1070`) | Ch 26 § Governance starts with clear decisions and owners | Ch 25 checklist (`07-part-vii.md:476`); Ch 27 § Governance controls + Governance Inventory + GovernanceRecord; Appendix G Phase 0 | D (four homes) | Ch 26 |
| Exceptions with expiry | Ch 26 | Ch 26 § Make review predictable and proportional | Ch 27 `governance/exceptions` API + ExceptionWaiver | Ch 27 holds the implementation of a Ch 26 concept | Ch 26 |
| Causal trace / run graph; trace vs audit | Ch 01 vocabulary (`:452`) | Ch 24 § A useful trace tells the story of the run | Ch 04 "a trace store is not the audit ledger" (`02-part-ii.md:242`); P-09; AP-14; Ch 25 implementation components | R | Ch 24 |
| Debug by first divergence | Ch 03 § If this fails in production (ordered checks) | Ch 24 § Debugging method | Ch 07 § If this fails in production (`03-part-iii.md:143`); Ch 25 If-fails step 2 | Ch 07 D | Ch 24 |
| Replay / fork (no live effects) | Ch 04 Run API `:fork` | Ch 24 § Trace and replay semantics | Ch 14 console "fork a sandbox replay"; Ch 15; Ch 25 `forkReplay` API + Replay/Fork Service | D | Ch 24 |
| Outcome vs trajectory evaluation; slices | Ch 24 § A scorecard operators can actually use | Ch 25 § Judge the outcome and the path separately | Ch 25 § Measure both the outcome and the path (same idea, separate H2) | Internal D | Ch 25 |
| Runtime adaptation vs offline improvement; learning loop | Front matter principle 6 | Ch 25 § Close the loop… / § Separate runtime adaptation from offline improvement | Ch 15 step 10; Ch 07 golden path "Improve"; Ch 27 § Promotion and continuous-improvement loop ("Learn" row) | Ch 27 D | Ch 25 |
| Immutable release; rollback of assignment | Ch 08 deprecation window | Ch 27 § Rollback and active runs | Ch 15 Version Router; Ch 25 Q (`07-part-vii.md:491`) | Ch 25 D | Ch 27 |
| Admission / budgets / permits / backpressure | Ch 02 § Scaling the shell | Ch 28 § Give each stage a latency and cost budget / § Scheduling algorithm | Ch 10 § Capacity model; Ch 12 BudgetReservation (`04-part-iv.md:510`, same entity as `08-part-viii.md:610`); P-11; AP-11 | Ch 12 entity D | Ch 28 |
| Cost per verified success | Ch 10 PERFORMANCE AND COST box ("per completed task") | Ch 28 § Optimize the trajectory, not the token | Ch 19 § What to measure…; Ch 24 scorecard; Ch 28 ×5 internally (`08-part-viii.md:495`, `:516`, `:582`, `:665`, checklist); Appendix L | Ch 28 internal D | Ch 28 |
| Little's Law / sizing | Ch 28 | Ch 28 § Start with the four measurements | Appendix L § Quantitative sizing method | R (Appendix L adds formulas) | Ch 28 |
| Graceful degradation | Ch 22 § The mechanics that make retries safe (`06-part-vi.md:844`) | Ch 28 § Decide what the system may drop or defer | P-11; Ch 28 Q (`08-part-viii.md:733`) | D | Ch 28 |
| Authorization-scoped caching | Ch 06 § Scalability and token economics | Ch 21 § Consistency and revocation policy | Ch 19 Caching row + `05-part-v.md:589`; Ch 28 #6 + scalability bullet + Q (`08-part-viii.md:732`) | D (four statements) | Ch 21 |
| Harborlight case; checkpoints C01–C03 | Front matter § How to Use the Book (`00-front-matter.md:61`) | Ch 01 § A mortgage case that grows with the architecture | Ch 02/03 checkpoint tables; Appendix I | Front-matter table D of chapter tables | Ch 01 |
| Supplier-onboarding comparative thread | Preface (`00-front-matter.md:29`) | Ch 01 § The comparative supplier-onboarding thread | Ch 02 and Ch 03 supplier boxes only | Thread abandoned after Ch 03 (§8, §9 S15) | Ch 01 (or retire) |
| Northstar codename | Ch 01 (`01-part-i.md:35`) | — | 5 NORTHSTAR boxes; prose in Ch 03, 04, 06, 10–15, 18, 19, 24, 27, 28 | §6 T1 | Remove, or define in front matter + glossary |

---

## 4. Dependency problems

These are places where a concept is used before it is defined or before its prerequisite is taught, in book order.

| # | Where used | What is used | Where actually defined | Severity |
| --- | --- | --- | --- | --- |
| 1 | Ch 01 § Draw the boundary around the model (`01-part-i.md:186–188`) | First "State owner / Trust boundary / Scale unit / Failure containment / Core contracts" table: "RunManifest · AgentStep · Artifact", "regional cell", "Run Service". The table format itself is never explained anywhere in the book. | Ch 04 § RunManifest; § Turn the diagram into enforceable contracts | Medium |
| 2 | Ch 01 § What changes when the prototype meets production (`:404`) | "the effect ledger, the capability envelope, the run manifest, proposal-bound approval, the causal trace graph". The capability envelope is missing from the vocabulary table. | Ch 21, Ch 22, Ch 04, Ch 14, Ch 24 | Low (signposted) |
| 3 | Ch 01 § Each control point answers a different question (`:522–552`) | Agent Gateway; "mints a last-hop credential"; "effect receipt"; acceptance gate; evaluation/release gate | Agent Gateway: never. Credentials: Ch 21. Receipts: Ch 22. Release gate: Ch 25/27. | Medium (Agent Gateway is an orphan) |
| 4 | Ch 01 § What to verify before production (`:586`); § Questions to bring to design review (`:603`) | "Autonomy is bounded independently across…", "autonomy level" | Never defined as a scale. Ch 01's four levels are capability levels, not autonomy levels. Also Ch 02 principle 8 (`:750`), Ch 27 (`08-part-viii.md:268`). | Medium (orphan) |
| 5 | Ch 01 § The vocabulary this book assumes (`:445`, `:450`) | Pointers: compensation → Ch 15; acceptance criteria → Ch 10 and 12 | Fullest: Ch 22 § The mechanics that make retries safe; Ch 02 § Deterministic acceptance / Ch 13 / AP-07 | Medium (misdirects readers) |
| 6 | Ch 01 § Put the idea to work (`:594`) | "label every authoritative store" for Northstar | Ch 04 § Where each kind of state belongs | Low |
| 7 | Ch 02 § Six gates before anything changes (`01-part-i.md:658–665`) | "The gates" before they are named; ToolManifest, ToolIntent, EffectRecord | Gates: next section (`:669`). ToolManifest/EffectRecord: Ch 22. ToolIntent: never formally defined. | Medium |
| 8 | Ch 02 § How Tool Use works in practice (`:793`, `:825`) | last-hop credential; "credential lease ID" | Ch 21 § Records worth preserving | Low |
| 9 | Ch 02 § Scaling the shell (`:734`) | risk class, quotas, backpressure | Ch 22 § Risk classes; Ch 28 | Low |
| 10 | Ch 02 § Design principles (`:748–750`) | memory write and artifact publication as policy points; "certified" capability; autonomy level | Ch 06; Ch 08; never | Low |
| 11 | Ch 02 § Deterministic acceptance (`:730`) | "human action authorizations cover the exact proposal" | Ch 14 | Low |
| 12 | Ch 03 § The request is bounded before the model sees it (`:1041–1047`) | Authorized ContextManifest, trust labels, redaction decisions, capability ceiling, delegation mode, cancellation lineage | Ch 06; Ch 21; Ch 18 | Medium |
| 13 | Ch 03 § Reauthorize the exact resource (`:1088`) | "capability envelope" | Ch 21 | Medium |
| 14 | Ch 03 § Human approval: interruption versus record (`:1137`) | Full HumanActionAuthorizationRequest field list, proposal hash, expiry semantics | Ch 14 (forward-referenced at `:1107`) | Low (signposted, but pre-teaches Ch 14) |
| 15 | Ch 03 § Three meanings of handoff (`:1164`) | "Durable `TaskEnvelope` and child workflow" | Ch 18/19 | Medium |
| 16 | Ch 03 § One retry owner (`:1192`) | "The workflow or LLM Gateway may retry" | LLM Gateway behavior: Ch 19 | Low |
| 17 | Ch 03 § Framework upgrades are behavioral changes (`:1225`) | RunManifest field table | Ch 04 § RunManifest (with different fields) | Low |
| 18 | Ch 03 § Guardrails and authorization solve different problems (`:1172–1180`) | Seven-layer protection stack incl. reconciliation | Ch 20, Ch 22 | Low |
| 19 | Ch 04 § What the architecture is trying to protect (`02-part-ii.md:38–44`) | AgentSpec, TaskEnvelope, ContextManifest, MemoryRecord, Skill manifest, RoutingDecision, PolicyDecision, CapabilityEnvelope, HumanActionAuthorizationRequest/Decision, EvaluationResult, ChangeBundle, ReleaseManifest | Ch 06, 07, 08, 11, 14, 18, 21, 25, 27, with no pointers given | Medium |
| 20 | Ch 04 § Core authoritative records (`:93`) | CredentialLease, ToolManifest, EvaluationReport, WorkflowExecution | Ch 21, Ch 22, (EvaluationReport never defined), Ch 15 | Medium |
| 21 | Ch 04 § Trust boundaries (`:151–152`) | "PDP decision, downscoped token", "signed task envelope, scope intersection" | Ch 21; Ch 19 | Low |
| 22 | Ch 04 § Questions to bring to design review (`:336`) | "last-known-good bundles… kill switches" | Ch 27; Ch 23 | Low |
| 23 | Ch 06 § The trust hierarchy of instructions (`02-part-ii.md:650`) | "Skill instructions… pinned, versioned capability artifact" | Ch 08 | Low |
| 24 | Ch 06 § Cross-boundary artifact adoption policy (`:865`) | Artifact adoption across tenant/region/purpose, as code with **no explanatory prose** | Adoption is taught in Ch 18 § How Multi-Agent Collaboration works in practice and Ch 19 (`adoptResult`) | Medium |
| 25 | Ch 07 § Keep contracts stable while frameworks change (`03-part-iii.md:58`); state table (`:27`) | AgentSpec, **RunContext**, ToolCall, EvaluationResult | RunContext is never defined (Ch 03 uses AgentStepRequest) | Medium (orphan) |
| 26 | Ch 07 § How a capability moves from idea to production (`:64`) | ChangeBundles, SBOM, provenance, ReleaseManifest | Ch 25; Ch 27 | Low |
| 27 | Ch 07 § Test the contracts before you test the model (`:114`) | "timeout/unknown-effect semantics", trajectory simulation | Ch 22; Ch 25 | Low |
| 28 | Ch 07 § What teams should be able to rely on (`:40–41`) | MCP Integration, Agent-to-Agent Communication rows | Ch 19 | Low |
| 29 | Ch 08 § The Skill manifest (`03-part-iii.md:219`, `:233`) | `side_effect_class: read_only`, `min_risk_tier: 1` | Risk tiers: Ch 26. Effect/risk classes: Ch 22. "side-effect class" is never defined. | Medium |
| 30 | Ch 08 § Skill lifecycle (`:292`) | Trajectory, threat, failure-injection certification | Ch 25 | Low |
| 31 | Ch 09 § What the evidence lets us conclude (`:430`) | SBOM, signed provenance, publisher trust | Ch 27 | Low |
| 32 | Ch 11 § A routing decision cannot grant permission (`04-part-iv.md:193–195`) | "run envelope", "child capability envelope", "cancellation lineage" | Ch 21; Ch 18 | Medium |
| 33 | Ch 12 § Plan IR (`:456`, `:465`) and § Compile-time checks (`:518`) | `authority_envelope_id`; `"risk_class": "R1"`; "R4 commit remains a deterministic domain operation" | Ch 21; **Ch 22 § Risk classes (`06-part-vi.md:714`)**, with no forward pointer | **High** |
| 34 | Ch 12 § Records worth preserving (`:510`) and § Compile-time checks (`:520`) | BudgetReservation; "Admission may reject, defer" | Ch 28 | Low |
| 35 | Ch 14 § Operator console requirements (`:906–908`) | "Live run graph", "trigger compensation", "fork a sandbox replay" | Ch 24; Ch 22; Ch 24 | Low |
| 36 | Ch 14 § How Human-in-the-Loop works in practice (`:994`) | "InterventionTask" | Never defined | Low (orphan) |
| 37 | Ch 15 § Canonical control flow (`:1160–1165`) | "maximum capability envelope", "downscoped credential", "risk classes" | Ch 21; Ch 22 | Medium |
| 38 | Ch 15 § Terminal correctness (`:1152`) | Compensation as a recovery path | Ch 22 (although the vocabulary table says Ch 15) | Medium |
| 39 | Ch 15 § Where this leads next (`:1354`) | "The core patterns are now defined" | P-06–P-11 are defined in Ch 18–28 | **High** (false claim) |
| 40 | Ch 16 § P-06 — Typed task ownership and join (`:1427`) | TaskEnvelope, deterministic join, owner conflicts | Ch 18 | **High** |
| 41 | Ch 16 § P-07 — Least-privilege capability envelope (`:1437`) | Capability lease, audience/purpose scope | Ch 21 | **High** |
| 42 | Ch 16 § P-08 — Effect ledger and reconciliation (`:1447`) | Prepared EffectRecord, unknown terminal | Ch 22 | **High** |
| 43 | Ch 16 § P-09 — Causal run graph (`:1457`) | Correlated graph of release, context, decisions, effects | Ch 24 | Medium |
| 44 | Ch 16 § P-10 — Risk-tiered evidence gates (`:1467`) | ChangeBundle, risk-tier review | Ch 25–27 | Medium |
| 45 | Ch 16 § P-11 — Durable runtime with backpressure (`:1477`) | Permits, quotas, circuits, degraded mode | Ch 28; Ch 22 | Medium |
| 46 | Ch 17 § AP-03 — Ambient authority (`:1677`) | "derive a capability envelope by intersection… credential lease" | Ch 21 | Medium |
| 47 | Ch 17 § AP-04 / § AP-05 (`:1707–1766`) | One retry owner per failure class; unknown-effect terminal | Ch 22 (previewed in Ch 03/15) | Low |
| 48 | Ch 17 § AP-08 — Multi-agent chat as workflow (`:1827`) | TaskEnvelope, deterministic join | Ch 18 | Medium |
| 49 | Ch 17 § AP-12 — Ungated tool discovery and catalog dumping (`:1693–1697`) | MCP advertised catalogs, approved tool slice "bound to a lease" | Ch 19; Ch 21 | Medium |
| 50 | Ch 17 § AP-14 — Telemetry without causal or effect lineage (`:1839`) | Causal run graph joining release, manifest, policy, acceptance | Ch 24 | Medium |
| 51 | Ch 17 § AP-15 / § AP-16 (`:1853`, `:1863`) | ChangeBundle, ReleaseManifest, signed promotion, canary | Ch 25; Ch 27 | Medium |
| 52 | Ch 18 § Monotonic child authority (`05-part-v.md:276`) | Full CapabilityEnvelope dataclass and subset proof | Ch 21 explains envelopes three chapters later and then repeats the same code | Medium |
| 53 | Ch 18 § Recommended orchestration rules (`:76`) | "immutable AgentManifest" | Not defined (Ch 07 uses AgentSpec) | Low |
| 54 | Ch 19 § What the evidence lets us conclude (`:600`) | Audience/resource binding, PKCE, token passthrough | Ch 21 | Low |
| 55 | Ch 19 § Scalability, federation, and failure isolation (`:547`) | W3C trace context, span links | Ch 24 | Low |
| 56 | Ch 20 § Respond as if the model can be compromised (`06-part-vi.md:280`) | "Narrow kill switch" | Ch 23 | Low |
| 57 | Ch 20 § Worked example — an injected mortgage document (`:250`) | EgressGrant | Ch 23 | Low |
| 58 | Ch 21 § Consistency and revocation policy (`:495`) | "R3/R4 actions (risk classes, Chapter 22)" | Ch 22, already used in Ch 12 | Medium (shows the misplacement of risk classes) |
| 59 | Ch 22 § What to verify before production (`:992`) | "Commands and facts are distinct" | Never taught in Ch 22; implied in Ch 04 § Event contract | Low |
| 60 | Ch 24 § Build observability around decisions and effects (`07-part-vii.md:99`) | Eval datasets, trajectory grading | Ch 25 | Low |
| 61 | Ch 25 § What to verify before production (`:474`, `:476`); § Questions to bring to design review (`:490–491`) | "release bundle", "use-case inventory", rollback without breaking active runs | Ch 27; Ch 26/27 | Medium |
| 62 | Ch 26 state table (`08-part-viii.md:27`), § Governance starts… (`:37`), accountability table (`:57`) | ValidationReport | Used in Ch 07, 20, 25; never defined | Low (orphan) |
| 63 | Appendix C § Core Platform Contracts at a Glance (`09-appendices.md:65–67`) | RunManifest fields "release, capability, region, deadline"; "AgentStep" | Not the fields in Ch 04 § RunManifest; Ch 03 uses AgentStepRequest/Result | Medium (reference contradicts chapters) |

**Orphan concepts** (used but never defined anywhere): Agent Gateway, autonomy level, RunContext, ToolIntent (as a contract), InterventionTask, ValidationReport, EvaluationReport, AgentManifest, side-effect class, UseCaseRecord (`06-part-vi.md:1051`), ObservationRecord / DetectionEvent / LearningRecord (`07-part-vii.md:395–404`).

---

## 5. Recurring boilerplate structures

### 5.1 Inventory

| Template | Chapters using it | Value | Repetition risk |
| --- | --- | --- | --- |
| **Opening callouts.** "Evidence context" blockquote; WHERE THE MORTGAGE CASE STANDS **or** NORTHSTAR AT THIS POINT; THE DESIGN CHOICE | Mortgage box: Ch 01, 02, 05, 09–15, 18, 19, 21–25 (17). NORTHSTAR box: Ch 04, 06, 08, 27, 28 (5). Neither: Ch 03, 07, 16, 17, 20, 26. Design choice: all but Ch 07, 16, 17, 20, 26. Ch 02 alone adds WHAT BLOCKS THE NEXT STEP. | High for orientation | Box type switches without reason. After Ch 03 the mortgage boxes are standalone vignettes, not cumulative checkpoints (§8). |
| **Double "why" opening.** First H2 "Why …" plus a second framing H2, both restating the design-choice box | Every chapter except Ch 01, 04, 16 | Low | Ch 02 § Why a valid-looking output is not enough restates the intro paragraph and box. Ch 20 § Why prompt defenses are not enough + § Guardrails help…. Ch 23 three framing H2s (`06-part-vi.md:1033`, `:1042`, `:1053`). |
| **State-owner table** (State owner / Trust boundary / Scale unit / Failure containment / Core contracts) | 25 chapters (missing in Ch 03, 16, 17) | Moderate: a compact ownership summary | Never explained. Often the only content of its heading (Ch 06 § What the model is allowed to see; Ch 12 § From candidate plan to executable work; Ch 02 § Six gates before anything changes). "Core contracts" names drift from the chapter body. |
| **"Required analysis \| Design conclusion"** seven-row table (Problem, Why it is difficult, Design alternatives, Recommended architecture, Trade-offs, Failure scenarios, Enterprise example) | Ch 06 (`02-part-ii.md:669`), 12 (`04-part-iv.md:420`), 14 (`:890`), 15 (`:1171`), 18 (`05-part-v.md:51`), 19 (`:450`), 21 (`06-part-vi.md:391`), 22 ×2 (`:692`, `:811`), 23 (`:1082`), 24 (`07-part-vii.md:94`), 27 (`08-part-viii.md:225`), 28 (`:537`): 13 tables | Moderate | It mirrors Appendix J's mandated structure (`09-appendices.md:331–341`), so it reads as research output pasted in. "Failure scenarios" duplicates the chapter's own failure sections. "Enterprise example" introduces off-thread domains: claims handling (Ch 06), incident agent (Ch 12), HR salary change (Ch 22), legal research (Ch 23), regulated underwriting (Ch 27), month-end finance (Ch 28). |
| **"How X works in practice."** THE ENGINEERING PROBLEM box + § How the pattern works (definition, 5 steps, Use when / Do not use when) + § Where it helps—and what it costs (2 rows) + § Where it can fail—and how to contain it (3 rows) + § What you need to see in production (6–7 bullets) | Ch 02 Tool Use; Ch 06 Memory; Ch 10 ReAct; Ch 11 Routing + Handoff; Ch 12 Planning; Ch 13 Reflection + Evaluator–Optimizer; Ch 14 Human-in-the-Loop; Ch 15 Long-Running Agents; Ch 18 Supervisor/Worker + Multi-Agent Collaboration (12 cards) | Good as a scannable card | Each card re-summarizes the prose directly above it. The pattern is then summarized a **third** time in a Ch 16 P-card, and a fourth in Appendix A (§5.2). Ch 18's two cards nearly coincide. |
| **"A workable implementation."** § Who should own each decision / § The contracts between components / § Records worth preserving + optional scale H3 | Ch 06, 12, 14, 15, 18, 19, 21, **22 ×2** (`06-part-vi.md:726`, `:846`), 23, 25, 27, 28 | High as reference (APIs, entities) | Format is inconsistent (owners as table in Ch 12, 14, 18, 21, 22a, 25, 27; as prose in Ch 06, 15, 19, 22b, 23, 28). APIs and entities collide across chapters (§5.2). The scale H3s ("What changes as usage grows" / "Scalability…") repeat the same bullets: partition by tenant + run, cache immutable manifests by digest, separate queues per workload, never a global lock. |
| **"What the evidence lets us conclude"** (claim table) + fixed sentence "The discussion above draws on … Appendix K lists the complete sources…" | 24 chapters (missing in Ch 02, 03, 16, 17) | Good citation discipline | Ch 10, 11, 12, 13 replace the table with an identical generic EVIDENCE BOUNDARY box (`04-part-iv.md:63`, `:212`, `:550`, `:684`) and list R-IDs that no claim uses. The fixed sentence appears verbatim 24 times. Placement wanders (before the pattern card in Ch 06 and Ch 10–15). |
| **"A sensible place to start"** (example listings) | All except Ch 03, 07, 16, 17, 26 | High (links to runnable code) | Often an empty H2 followed by an H3 (Ch 01 `01-part-i.md:567`). Often followed by an unrelated H2: Ch 05 → § Reference architecture: the Enterprise Knowledge Hub; Ch 20 → § Respond as if the model can be compromised. |
| **"If this fails in production"** (usually 3 steps) | 26 (missing in Ch 16, 17) | Moderate | Overlaps Ch 17's whole purpose and Appendix B's triage table. Ch 03 orders it after the checklist. Ch 05 uses a symptom table instead. |
| **"What to verify before production"** (✓ list) | 26 (missing in Ch 16, 17) | High | Aggregates repeat Appendix G § The minimum bar before an agent can write and Appendix L § Evidence for production acceptance. Ch 03 uses plain bullets. |
| **"Put the idea to work"** (2–4 exercises) | 25 (missing in Ch 03, 16, 17) | Good | Low |
| **"Questions to bring to design review"** (Q / Strong answer) | 26 (missing in Ch 16, 17) | Good | Verbatim duplicate: "How should approval be bound to an action?" in Ch 14 (`04-part-iv.md:1107`) = Ch 22 (`06-part-vi.md:1014`). Near-duplicates are listed in §5.2. |
| **"Where this leads next"** | All 28 | Good | Only Ch 01 and 02 carry a case bridge paragraph. |
| **P-card stock phrasing** ("The tempting shortcut is…", "That fails because…", "A safer design looks like this:", "The runtime flow is:", "The cost is real:") | Ch 16 ×12 | Comparable cards | The identical phrasing reads machine-templated. |
| **AP-card stock phrasing** ("The replacement is explicit:", "The migration path is clear:", "The price of the safer design is clear:") | Ch 17 ×16 | Comparable cards | Same templated feel |
| **T-card stock phrasing** ("The business risk is…", "Look for…", "Reduce the likelihood with these measures:", "At runtime, use these controls:", "If it happens, follow this recovery path:") | Ch 20 ×16 | Scannable | Same, and the content is terse fragments |
| **Callout boxes** (COMMON PITFALL ×7, SECURITY AND GOVERNANCE ×4, PRODUCTION CONSIDERATION ×4, ARCHITECTURE GUIDANCE ×4, PERFORMANCE AND COST ×3, BEST PRACTICE ×3, OBSERVABILITY TIP ×2, others ×1) | Scattered | Mixed | Placement is arbitrary: Ch 10 and Ch 15 put the pitfall *after* the evidence section, Ch 24 has two OBSERVABILITY TIPs, and the Ch 28 BEST PRACTICE box restates § Optimize the trajectory, not the token. |

### 5.2 Specific cases where template content repeats other chapters

- **Ch 22 has the implementation template twice.** § A workable implementation (`06-part-vi.md:726`) and § A workable implementation (`:846`) each contain § Who should own each decision, § The contracts between components, § Records worth preserving, and § What changes as usage grows (`:794`, `:897`). EffectRecord is defined in both with different fields (`:769` vs `:870`). `effects/{id}:reconcile` and `effects/{id}:compensate` appear in both API tables (`:752–753` vs `:859–860`). The chapter also has two Required-analysis tables (`:692`, `:811`).
- **One pattern, four descriptions.** ReAct: Ch 10 prose → § How ReAct works in practice → P-01 → Appendix A item 2. Durable execution: Ch 15 prose → § How Long-Running Agents work in practice → P-02/P-11 → Appendix A item 3. Tool use: Ch 02 → § How Tool Use works in practice → P-05 → Appendix A item 6. Memory: Ch 06 → § How Memory works in practice → P-04 → Appendix A. Multi-agent: Ch 18 → two cards → P-06 → Appendix A item 4.
- **API collisions across "contracts between components" tables:**
  - Run API: Ch 04 § Run API vs Ch 15 § The contracts between components.
  - Plan revise: `plans/{id}:revise` (Ch 12, `04-part-iv.md:496`) vs `runs/{id}/plans:revise` (Ch 18, `05-part-v.md:108`).
  - Credentials: `credentials:exchange` (Ch 21, `06-part-vi.md:459`) vs `credentials:lease` (Ch 23, `:1125`).
  - Replay: `runs/{id}:fork` (Ch 04) vs `runs/{id}:forkReplay` (Ch 25, `07-part-vii.md:366`).
  - Operator actions: `runs/{id}:operatorAction` (Ch 14) vs `:pause` / `:resume` (Ch 15).
- **Entity collisions in "Records worth preserving":** SandboxLease (Ch 22 `06-part-vi.md:770` vs Ch 23 `:1137`); BudgetReservation (Ch 12 `04-part-iv.md:510` vs Ch 28 `08-part-viii.md:610`); OutboxRecord (Ch 04 code `02-part-ii.md:292` vs Ch 22 `06-part-vi.md:871`); HumanActionAuthorizationRequest (Ch 03 prose, Ch 14 § Approval contract, Ch 14 records `04-part-iv.md:944`, Ch 14 code `:1048`).
- **Ch 25 holds Ch 24's implementation.** Ch 25 § A workable implementation lists the Telemetry Gateway/Collector, Trace Index, Content Vault, OTLP ingestion, `GET /v1/runs/{id}/trace`, TraceIndex, SpanEnvelope, and ContentBlob (`07-part-vii.md:347–375`). Ch 24 has no implementation section.
- **Ch 27 holds Ch 26's implementation:** Governance Inventory, `governance/exceptions`, `governance/inventory`, GovernanceRecord, and ExceptionWaiver (`08-part-viii.md:288`, `:302–303`, `:316–317`).
- **Near-duplicate design-review questions:**
  - Handoff vs child task: Ch 03 (`01-part-i.md:1307`) ≈ Ch 18 (`05-part-v.md:377`).
  - Discovery vs authorization: Ch 08 (`03-part-iii.md:347`) ≈ Ch 20 (`06-part-vi.md:325`).
  - Release bundle / rollback: Ch 25 (`07-part-vii.md:490–491`) ≈ Ch 27 (`08-part-viii.md:453–454`).
  - Model swap: Ch 07 (`03-part-iii.md:171`) ≈ AP-15 ≈ Ch 27 Q1.
  - Judge use: Ch 13 (`04-part-iv.md:843–845`) ≈ Ch 25 (`07-part-vii.md:489`).
  - Cache authorization: Ch 28 (`08-part-viii.md:732`) ≈ Ch 19 text ≈ Ch 21.
- **Symptom → first-check tables appear three times:** Ch 05 § If this fails in production (`02-part-ii.md:545`), Ch 17 § Find the failure by its first symptom (`04-part-iv.md:1519`), and Appendix B (`09-appendices.md:39`).

### 5.3 Heading and structure anomalies (for reviewers)

- Empty wrapper H2s or H3s:
  - Ch 01 § A sensible place to start (`01-part-i.md:567`)
  - Ch 04 § A practical reference architecture (`02-part-ii.md:97`) and § The contracts that hold the platform together (`:157`)
  - Ch 15 § The lifecycle of a durable run (`04-part-iv.md:1154`) and § Event-driven resume flow (`:1194`). The latter is an empty H3 followed immediately by § Event architecture; something (a diagram or steps) appears to be missing.
  - Ch 27 § A deployment shape that supports safe change (`08-part-viii.md:182`)
- Ch 16: all 12 H2s ("Reasoning", "Orchestration", …) wrap exactly one H3 card.
- Ch 04: the opening callouts are mid-chapter (`02-part-ii.md:79–83`).
- Ch 03: unique section order and set (see §2).
- The Closing Perspective lives inside `09-appendices.md:559`, after Appendix L. It is absent from "Find Your Way Through the Book".
- Ch 17's code blocks contain lines starting with `# ` (Python comments, e.g. `04-part-iv.md:1571`, `:1718`, `:1785`). Valid Markdown, but naive heading scanners treat them as H1s; validators should stay fence-aware.

---

## 6. Terminology inventory

| # | Term family | Variants and locations | Problem | Recommended canonical |
| --- | --- | --- | --- | --- |
| T1 | **Northstar vs Harborlight** | Northstar is defined as "the platform codename used for Harborlight's mortgage workflow" (`01-part-i.md:35`). It is used in Ch 01 (`:594`); Ch 03 (×11); Ch 04 (`02-part-ii.md:79`, `:87`); Ch 06 (`:591`, `:617`); Ch 08 (`03-part-iii.md:183`); Ch 10–15 (`04-part-iv.md:45`, `:195`, `:410`, `:672`, `:674`, `:882`, `:1146`); Ch 18 (`05-part-v.md:47`); Ch 19 (`:438`, `:446`, `:601`); Ch 24 (`07-part-vii.md:58`); Ch 27/28 (`08-part-viii.md:132`, `:158`, `:469`, `:507`, `:520`, `:524`). The front matter, Appendix H, and Appendix I never mention it. | Readers see two names. Box type (NORTHSTAR vs MORTGAGE CASE) changes arbitrarily, and Ch 28's "Northstar admits 120 runs per minute" reads like a different organization. | Drop Northstar ("the Harborlight platform"), or define it in the front matter and glossary and use it only for platform-level statements. |
| T2 | **Planes / layers / bands / spines / cells** | Ch 01 "bands" + two "spines" (security, platform) (`01-part-i.md:487–508`). Ch 04: 7 planes (`02-part-ii.md:36–44`); 11 layers, five of them named "…plane" (Agent control plane, Run control plane, Model plane, Capability plane, Execution plane, `:132–142`); Figure 4-1 bands (Experience and channels, Edge and admission, Agent applications, Run control and durable execution, Knowledge context and memory, Gateways and integration, Systems of record and providers) + spines "Trust and governance" and "Evidence and improvement". Ch 04 "global control plane" vs "regional execution cells" (`:87`). Ch 27 "control plane" vs "regional execution planes" (`08-part-viii.md:186–200`). Appendix J: 12 layers (`09-appendices.md:347`). | "Execution plane" means the sandbox layer in Ch 04 but a regional execution environment in Ch 27. Ch 01 claims Figure 4-1 is "this same picture at higher resolution" (`01-part-i.md:510`), yet the band names and spines differ. | Plane = ownership domain only (7 names, used in both figures). Layers get non-"plane" names. "Regional execution cell" everywhere. |
| T3 | **Approval / human action authorization / grant / consent** | Ch 01 "Human approval gate" + "human action authorization" (`01-part-i.md:529`, `:545`). Ch 03 "Platform approval" + HumanActionAuthorizationRequest (`:1137`, `:1144`). Ch 04 "Human action authorization" rows. Ch 14 "Approval contract" (`04-part-iv.md:900`), `/v1/approvals` APIs (`:931–937`), "Approval Policy Router", and an `approval_id` field inside `HumanActionAuthorizationRequest` (`:1049`). AP-06 "Consent versus grant". Figure 20-3 "Approval Service … signed grant". Appendix C. "Approval" appears ~250 times, "human action authorization" ~20. | "Authorization" also means policy authorization (Ch 21). The record name and API name disagree inside Ch 14. | Choose one pair: "approval" (human) with records ApprovalRequest/ApprovalDecision, keeping "authorization" for policy decisions; or keep HAA and rename APIs and fields to match. |
| T4 | **Gateway names** | "LLM Gateway" (Ch 01, 03, 07, 19) vs "model gateway" (`02-part-ii.md:22`, `:87`, `:137`). "Agent Gateway" (`01-part-i.md:525`, `05-part-v.md:561`) vs "A2A Gateway" (`05-part-v.md:438`, `:455`, `:499`; Ch 04 "A2A gateway"; Appendix G Phase 4). "Tool Gateway" vs "Connector Gateway/PEP" (`06-part-vi.md:448`) vs "tool façade" (`02-part-ii.md:55`, P-05). Added in Ch 23/25 without reconciliation: "Egress Gateway", "Content Security Gateway" (`06-part-vi.md:1114`), "Telemetry Gateway" (`07-part-vii.md:347`). | Ch 01 says "they are routinely confused because the word is the same" (`01-part-i.md:517`), then the book multiplies names. | Five control-point gateways (API, Agent/A2A — pick one, LLM, Tool, MCP). Call the others "proxy" or "service". |
| T5 | **Run / workflow / task / activity / step / node / work item** | Run (Run Service, RunManifest); workflow (WorkflowExecution, `02-part-ii.md:93`); task (TaskEnvelope, child task); activity (Ch 15); agent step (AgentStep); plan node / workflow node (Ch 12, Ch 03 "EVIDENCE_REVIEW node"); federated task (Ch 19); work item (Ch 28 `08-part-viii.md:597`). | Never defined relative to each other; the glossary has none of them. | One glossary entry and one diagram (run ⊃ workflow execution ⊃ nodes → activities / agent steps / child tasks). |
| T6 | **Authority scope names** | capability envelope (Ch 01, 03, 11, 15, P-07, Ch 18, 21); "run envelope" (`03-part-iii.md:262`, `04-part-iv.md:193`, `:565`); "authority envelope" (`04-part-iv.md:456`, `05-part-v.md:32`, `:82`, `06-part-vi.md:460`); `authority_envelope` (`02-part-ii.md:191`); "authority ceiling" (`05-part-v.md:102`, `:122`); `capability_grant_id` (`05-part-v.md:268`, `:627`); "capability lease" (P-07 `04-part-iv.md:1441`, Figure 17-2); "credential lease" (Ch 02, 21); "grant" generically | Five names for scope and two for proof | Capability envelope (scope) and credential lease (proof), as Ch 21's Q defines (`06-part-vi.md:625`). |
| T7 | **Release artifacts** | "behavior bundle" (`01-part-i.md:550`); ChangeBundle (Ch 04, 07, P-10, AP-15, Ch 25); ReleaseManifest (Ch 04, 07, AP-16, Ch 20, 25, 27); "release bundle" (Ch 25 `07-part-vii.md:474`, `:490`; Ch 27 ×5); "release graph" (`07-part-vii.md:226`, `:334`; Appendix F #4); Ch 27: "an immutable ReleaseManifest … pins the manifest to each run" (`08-part-viii.md:158`) vs "Resolve every run to an immutable RunManifest" (`:230`) | RunManifest and ReleaseManifest roles conflated | ChangeBundle = proposed change; ReleaseManifest = immutable promoted bundle; RunManifest = per-run resolution that references a ReleaseManifest. |
| T8 | **Agent definition** | AgentSpec (Ch 04 Figure, Ch 07); "AgentManifest" (`05-part-v.md:76`); AgentVersion record (Ch 18); "Agent manifest" (Ch 27 `08-part-viii.md:239`); "agent definition" (Ch 03); A2A "agent card" | Four names | AgentSpec |
| T9 | **Step contract** | AgentStepRequest / AgentStepResult (Ch 03); RunContext (Ch 07 `03-part-iii.md:27`, `:58`); AgentStep (Ch 04 `02-part-ii.md:93`, Appendix C); `step_request` (Ch 08 `03-part-iii.md:298`) | Drift | AgentStepRequest / AgentStepResult |
| T10 | **Guardrail** | Detector, not a security boundary (Ch 03 `01-part-i.md:1168`; Ch 20 `06-part-vi.md:28–37`). Enforced rule at the effect boundary (Ch 05 § Business rules as enforceable constraints, `02-part-ii.md:416–418`; Figure 5-2 "policy-to-guardrail"). Whole security architecture (Figure 20-1 "Defense-in-depth guardrails architecture"; Ch 20 closing "The guardrail architecture"; book-map Part VI "Security and guardrails"). Numeric limits (Ch 28 § Illustrative starting guardrails, `08-part-viii.md:639`). Platform capability including "action policy" (`03-part-iii.md:46`). | Directly contradicts the book's own distinction | "Guardrail" = probabilistic detector only. Ch 05: "enforced rule / constraint". Ch 28: "starting limits". Figure 20-1: "defense-in-depth controls". |
| T11 | **Risk numbering** | Tool/effect risk classes R0–R4 (Ch 22 `06-part-vi.md:714`; used in Ch 12, 21, 23, 24, Appendix J); governance risk tiers 0–4 (Ch 26 `08-part-viii.md:62`); `"risk_tier": "high"` (Ch 04 RunManifest); `min_risk_tier: 1` (Ch 08); `side_effect_class` (Ch 08); "risk class" as a queue dimension (Ch 02, 14, 28); adoption phases 0–5 (Appendix G); agent levels 1–4 (Ch 01) | Several 0–4 scales with different meanings | R0–R4 for effects and tools; T0–T4 (or named tiers) for use-case governance. Never use bare numbers. |
| T12 | **Terminal states** | accepted / blocked / needs-input / failed / unknown-effect (`02-part-ii.md:56`, AP-07 `04-part-iv.md:1815`); answer / needs_input / delegate / proposed_action / budget_exhausted / failed (`04-part-iv.md:49`); sufficient / insufficient / additional evidence required (Ch 03 `01-part-i.md:972`); Succeeded / InterventionRequired (Ch 15 `04-part-iv.md:1152`); acceptance satisfied / user canceled / policy denied / limit reached / unrecoverable error (Ch 18 `05-part-v.md:81`); Created … Failed/Expired/InterventionRequired (Ch 19 `05-part-v.md:531–539`); "accept, reject, or escalate" (Ch 13) | Seven vocabularies | One run-terminal table (Ch 15) plus a step-disposition table (Ch 03/10), cross-referenced. |
| T13 | **Effect states** | Reserved, Executing, Committed, Declined, Unknown, Partial, Compensating, Compensated, InterventionRequired (Ch 22 text `06-part-vi.md:669`); the same minus Partial in code (`:937`); committed / declined / unknown (Ch 04 receipt `02-part-ii.md:204`); "reserved, executing, committed, declined, partial, or unknown" (Ch 22 § If this fails in production, `06-part-vi.md:987`); "committed, absent, partial, executing, or unprovable" (Appendix B `09-appendices.md:57`); reconcile outcomes committed / absent / unprovable (code `:977`) | Drift, and code ≠ text | Ch 22 text list; add Partial to the code; map absent → Declined and unprovable → InterventionRequired explicitly. |
| T14 | **Proposal pipeline names** | "propose → validate → authorize → commit → verify → accept" (`01-part-i.md:669`); "propose–validate–commit" (`:887`); "deterministic shell" (`:673`, `:743`); "Proposal–authorize–commit" (P-05, Appendix A `09-appendices.md:17`, `:28`); "propose → preview → approve → commit" (`04-part-iv.md:1165`) | Four names | "The six gates" (with "deterministic shell" as the container) |
| T15 | **The missing document** | "second pay statement" (`00-front-matter.md:68`; `01-part-i.md:50`, `:628`, `:834`) vs "employment verification" (`01-part-i.md:81`, `:688`, `:691`, `:702`, `:1094`, `:1118`, `:1152`, `:1199`; `04-part-iv.md:382`, `:898`, `:1119`, `:1179`, `:1711`) | Continuity error inside the running case | Pick one (the second pay statement fits C01) and update the Ch 02 JSON and Ch 03 onward. |
| T16 | **Case identifiers** | Tool: `request_mortgage_document` (Ch 01, 03, 27), `mortgage.document.request@1` (Ch 02), `tool://mortgage-evidence/request@1.0.0` (Ch 04). Policy: `mortgage-policy@2026.09` (Ch 03), `policy://enterprise-agent@2026.09.3` (Ch 04), `US-2026-09` (Ch 18), `approved-2026.09` (Ch 07/08). Model route: `reasoning-standard@4` (Ch 03) vs `route://reasoning-standard@18` (Ch 04). Run: `RUN-98217` (Ch 03) vs `run_42` (Ch 06, 18). | Same case, different IDs in adjacent chapters | One identifier set, used in every case example. |
| T17 | **"Onboarding" without "supplier"** | P-02 "Onboarding always validates, screens, approves, creates, and notifies" (`04-part-iv.md:1391`); AP-03 "the onboarding task" (`:1675`); AP-07 "Onboarding reports complete while the sanctions screening is stale" (`:1813`) | The comparative thread resurfaces unlabeled | Label it "(supplier-onboarding comparison)", or switch to Harborlight. |
| T18 | **Memory taxonomy** | working vs long-term (+ conversation, workflow, etc.) (Ch 06 `02-part-ii.md:683–688`) vs working / episodic / semantic / profile (P-04 `04-part-iv.md:1411`) | Two taxonomies | Ch 06's |
| T19 | **Context trust labels** | tiers 1–4 (`02-part-ii.md:647–652`); labels instruction / user_input / enterprise_data / tool_result / memory (`:700`); `trust_role` instruction / user_intent / evidence (`:851`); `"trust": "untrusted-content"` (`:749`); Ch 03 "trust labels" | Four vocabularies in one chapter | One enum mapped to the four tiers |
| T20 | **Identity triad** | subject / actor / purpose (Ch 21 § Three identities every decision should preserve, `06-part-vi.md:365`) vs user / workload / grant (heading § Keep the user, workload, and grant distinct, `:353`) vs "dual principal" (`:396`). "Three identities" though purpose is not an identity. | Internal inconsistency | "Subject and actor (identities) plus purpose (context)" |
| T21 | **Acceptance vocabulary** | acceptance gate (Ch 01); acceptance engine (Ch 01, 02, 10, 12, 13); AcceptanceEngine (AP-07); AcceptanceDecision (Ch 13); "acceptance contract" (Ch 11 `04-part-iv.md:268`; TaskEnvelope `acceptance_contract`); "acceptance criteria" | Several names for one component | Acceptance engine (component), acceptance criteria (spec), AcceptanceDecision (record) |
| T22 | **Trace vocabulary** | "causal trace graph" (`01-part-i.md:405`); "Trace graph" (`02-part-ii.md:44`); "causal run graph" (P-09, `03-part-iii.md:143`); "run graph" (`03-part-iii.md:49`, `04-part-iv.md:906`); "unified run graph"; "trajectory" (Ch 24/25) | Loose | "Causal run trace" (operations) vs "trajectory" (evaluation view of the same run) |
| T23 | **Evaluation records** | EvaluationResult (Ch 04, 07, 13, 25); EvaluationReport (Ch 04, 08); EvalScore / EvalRun (Ch 25); ValidationReport (Ch 07, 20, 25, 26); EvaluationEvidence (Ch 27); ReleaseGateDecision (Ch 25) vs PromotionDecision (Ch 25 `07-part-vii.md:401`, Ch 27 `08-part-viii.md:313`) | Overlapping names | Define in Ch 25 and reuse in Ch 27 |
| T24 | **Effect component name** | "Effect Service" (Ch 22); "Effect Ledger" (Appendix C owner); "effect layer" (Ch 03 `01-part-i.md:1200`); "Tool/effect service" (Ch 04 `02-part-ii.md:66`) | Drift | Effect Service (component) owning the effect ledger (store) |
| T25 | **Approval service name** | Human Action Authorization Service (Ch 14); "Proposal and human action authorization service" (Ch 04 `02-part-ii.md:67`); "human action authorization service" in the run control plane layer (`:135`); "Approval Service" (Figure 20-3) | Drift | Follows T3 |
| T26 | **Part titles vs figure labels** | book-map labels: "Architecture and knowledge", "Patterns and anti-patterns", "Multi-agent and integration", "Security and guardrails", "Observability and evaluation", "Governance and operations". Actual titles: "Architecture, Knowledge, and Context"; "Patterns That Work—and Those That Fail"; "Working Together Across Boundaries"; "Security, Identity, and Control"; "Evidence, Evaluation, and Improvement"; "Running the System in the Real World". | Figure 0-1 does not use the Part names | Use the exact Part titles |
| T27 | **Knowledge plane naming** | "knowledge plane" (Ch 04 closing `02-part-ii.md:340`), "knowledge layer" (Ch 05 box), "Context, RAG, memory, Skills" (plane), "Knowledge, context and memory" (Figure 4-1), "Data and knowledge" (layer), "Knowledge" (Ch 01 band), "knowledge fabric" (Figure 5-1) | Five names | Align with T2 |
| T28 | **Delegated work names** | durable child task / child workflow (Ch 03, 18); federated task (Ch 19); remote task; A2A task | Fine, but undefined relative to each other | Glossary |

---

## 7. Duplicated diagrams, tables, and examples

### 7.1 Diagrams with overlapping messages

| Message | Figures | Notes |
| --- | --- | --- |
| Whole-system overview | Figure 0-1 `book-map` (`00-front-matter.md:94`); Figure 1-3 `system-overview` (`01-part-i.md:485`); Figure 4-1 `reference-architecture` (`02-part-ii.md:32`); also Figure 7-1 `developer-platform` | Three "one view" pictures with three decompositions (§6 T2). Figure 0-1 is a *Parts* map, but § The architecture in one view describes a request flowing through components (`00-front-matter.md:88–92`). Prose and figure mismatch. |
| Gateway roles | Figure 1-4 `gateway-roles` (`01-part-i.md:520`) + table; Figure 19-1 `gateway-position` (`05-part-v.md:556`) + table (`:558`) | Figure 19-1 shows only the API, Tool, and LLM gateways, while its table lists six components. It is a reduced duplicate of Figure 1-4. |
| Request → verified outcome sequences | Figure 2-1 `deterministic-shell`; Figure 3-1 `runtime-boundary`; Figure 4-2 `request-sequence` (Mermaid: User → Run → Agent → Policy → Tool → System of record); Figure 20-3 `guardrail-sequence` (Mermaid: Agent → Input Guardrail → Policy → Approval → Tool → System of record); Figure 22-1 `effect-lifecycle`; Figure 23-1 `sandbox-egress` | Figures 4-2 and 20-3 are near-identical sequences. Figure 20-3 inserts an "Input Guardrail" as the first gate, which contradicts "guardrails are not the security boundary". |
| Defense layers | Figure 20-1 `security-depth` (6 layers: input inspection, context authorization, output contract, policy evaluation, effect boundary, evidence and audit); table `06-part-vi.md:73` (9 layers); Ch 23 § Containment layers (8) + boundary table (5); Ch 03 protection stack (7) | Same idea, four counts |
| Trust boundaries | Figure 20-2 `security-boundaries`; Ch 04 § Trust boundaries table (8 rows) | Figure 20-2 shows 3–4 boundaries; the table shows 8. |
| Release and improvement pipelines | Figure 7-3 `developer-lifecycle`; Figure 7-4 `dx-golden-path`; Figure 25-1 `evaluation-gate`; Figure 25-2 `learning-loop`; Figure 27-1 `release-recovery`; plus the tables in Ch 07 § Make the safe path the easy path, Ch 25 § Close the loop…, and Ch 27 § Promotion and continuous-improvement loop | Three stage lists for promotion: Ch 07 (Scaffold … Improve), Ch 25 (Observe … Learn), Ch 27 (Build … Learn) |
| Testing pyramids | Figure 7-5 `test-pyramid` (4 tiers); Ch 25 § Evaluation pyramid (7) + § Layer tests from contracts to outcomes (9) | See §3 |
| Narrowing delegation | Figure 17-2 `anti-ambient-authority`; Figure 18-1 `supervisor-worker` ("narrowed child grants"); Figure 21-1 `identity-delegation` | Three views of the same narrowing |
| Approval binding | Figure 14-1 `pattern-hitl`; Figure 17-4 `anti-approval-binding` | R (pattern vs anti-pattern), acceptable |
| Retry / unknown | Figure 17-3 `anti-retry-storm`; Figure 22-1 `effect-lifecycle` | R, acceptable |
| Monolith vs governed | Figure 17-1 `anti-before-after`; Ch 01 § Anti-pattern — the autonomous monolith (prose) | R |
| Routing | Figure 11-1 `pattern-routing` (work); Figure 19-2 `model-routing` (model) | Different subjects under the same word (§6) |
| Pattern selection | Figure 16-1 `pattern-decision-tree`; Appendix A list + table; Ch 18 § Topology decision table | Three selection aids |

### 7.2 Tables communicating the same thing

- **Ownership "model may / must not":** Ch 01 § Which component should own each uncertainty; Ch 02 § Where distributed systems must remain authoritative; Ch 03 § Runtime responsibility versus enterprise responsibility and § Responsibility map; Ch 04 § Where truth lives; Ch 12 § What should be agentic?
- **End-to-end flows:** Ch 03 § The complete execution path (9), Ch 04 § End-to-end responsibility flow (8), Ch 15 § Canonical control flow (10), Ch 20 sentence (`06-part-vi.md:93`), Ch 22 § Invocation sequence (6).
- **Run API:** Ch 04 § Run API vs Ch 15 § The contracts between components.
- **State and store tables:** Ch 04 § Where each kind of state belongs vs Ch 06 § State taxonomy and storage.
- **TaskEnvelope fields:** Ch 18 code (`05-part-v.md:261`), Ch 19 field-group table (`:473`), A2ATaskEnvelope code (`:621`), Appendix C row.
- **Field-group tables:** Ch 03 AgentStepRequest field groups (`01-part-i.md:1039`) and Ch 19 TaskEnvelope field groups use the same Identity / Budgets / Trace shape (R; worth cross-linking).
- **Version-pin lists:** Ch 03 RunManifest table; Ch 04 RunManifest JSON; Ch 07 § CLI and delivery workflow (`03-part-iii.md:131`) and checklist; Ch 25 Q (`07-part-vii.md:490`); Ch 27 (`08-part-viii.md:158`) and § Versioned objects; Appendix G minimum bar; Appendix J acceptance.
- **Threats:** Ch 20 T-cards vs Ch 23 § Threats and required controls.
- **Failure response:** Ch 03 § One retry owner table vs Ch 22 § Choose the response that matches the failure.
- **Metrics:** Ch 19 § What to measure at the LLM Gateway; Ch 24 § A scorecard operators can actually use; Ch 25 § Measure both the outcome and the path; Ch 28 § Start with the four measurements.
- **Governance:** Ch 23 governance record paragraph; Ch 26 accountability table; Ch 27 § Governance controls.
- **Framework comparison:** Appendix D's two tables (`09-appendices.md:81` and `:98`), both covering OpenAI SDK, LangGraph, Microsoft, Google ADK, PydanticAI, and Temporal/DBOS, plus Ch 27 § Suggested baseline stack—not a mandate.
- **Degradation:** Ch 22 "Graceful degradation" bullet vs Ch 28 § Decide what the system may drop or defer.
- **Sizing:** Ch 28 Little's Law vs Appendix L § Quantitative sizing method.
- **Symptom → check:** Ch 05 If-fails table, Ch 17 § Find the failure by its first symptom, Appendix B.

### 7.3 Duplicated or overlapping examples and code

- **Identical code:** Ch 18 § Monotonic child authority (`05-part-v.md:280–347`) = Ch 21 § Capability-envelope subset proof (`06-part-vi.md:528–595`), the same `_resource_within`, `CapabilityEnvelope`, and `derive_child`.
- **Near-identical code:** Ch 18 TaskEnvelope (`05-part-v.md:261`) and Ch 19 A2ATaskEnvelope (`:621`).
- **Approval code:** Ch 14 holds `[[EXAMPLE:approval-gate]]` + an inline proposal-bound approval excerpt (`04-part-iv.md:1039`) + `[[EXAMPLE:approval-verification#core]]` in one section; AP-06 adds another inline version.
- **Effect-ledger code:** `[[EXAMPLE:governed-tool-gateway]]` (Ch 02; it has an in-memory ledger, per `01-part-i.md:854`), `[[EXAMPLE:effect-idempotency]]` (Ch 22), inline `InMemoryEffectLedger` (`06-part-vi.md:952`), and AP-05 code.
- **ReAct code:** `[[EXAMPLE:bounded-react-loop]]` and `[[EXAMPLE:react-engine#core]]` back-to-back (`04-part-iv.md:119–123`).
- **Routing code:** `[[EXAMPLE:routing-handoff]]` + inline "Deterministic route validation" (`04-part-iv.md:313`).
- **Contracts file used twice:** `[[EXAMPLE:contracts#step]]` (Ch 01) and `[[EXAMPLE:contracts]]` (Ch 04).
- **ContextManifest shapes:** Ch 06 ×3, plus AP-02 `ContextManifest.project`.
- **CloudEvents:** Ch 04 JSON (`02-part-ii.md:208`) + Pydantic model (`:270`); Ch 15 prose.
- **Inline code vs repository policy:** Inline "implementation excerpt" code appears in Ch 04, 06, 09, 11, 13, 14, 17, 18, 19, 21, 22, 23, 27, 28 even though `AGENTS.md` says code never goes in `source/parts/`. Reviewers should not resolve duplication by adding more inline code. Ch 13's evaluator–optimizer and the Ch 11 router excerpt import names they never use, and their classes lack `@dataclass`.
- **Repeated narrative scenarios:**
  - *Injected mortgage document* (5 tellings): Ch 01 Tuesday (`01-part-i.md:98`), Ch 03 § Guardrails and authorization… (`:1170`), Ch 20 § Worked example (`06-part-vi.md:236`), Ch 23 case box + § Start from the assumption… (`:1027`, `:1057`), AP-13 malicious bank-account document (`04-part-iv.md:1638`).
  - *Duplicate document request after timeout or restart*: Ch 01 Monday/Wednesday, Ch 03 § One retry owner, AP-01 (`04-part-iv.md:1554`), AP-05 (`:1741`), Ch 22 case box + failure timeline (`06-part-vi.md:675`), Ch 24 worked example, Ch 28 table row.
  - *Cheaper model silently regresses*: Ch 01 Friday, Ch 03 § Framework upgrades…, Ch 07, AP-14, AP-15, Ch 27 walkthrough.

---

## 8. Front matter and appendices

**Preface: The Engineering Perspective Behind This Book**
- It states the thesis well.
- § How to read the claims in this book duplicates Appendix K § Citation policy and the four-way claim taxonomy in `AGENTS.md`. A reader-facing duplicate is acceptable.
- § How this edition is maintained is maintainer content (canonical Markdown, regenerate DOCX/LaTeX) in a reader preface. So are Appendix I § Corrections and closure notes and § Rebuild and verify.
- It promises that "comparative supplier-onboarding examples show how the same contracts travel to other domains" (`00-front-matter.md:29`). After Ch 03 the thread survives only as unlabeled "onboarding" examples in Ch 16/17 (§6 T17). **Gap.**

**How to Use the Book**
- The checkpoint table (C01–C03) duplicates the chapter checkpoint tables. This is acceptable, but nothing tells chapter readers from Ch 04 onward that the "WHERE THE MORTGAGE CASE STANDS" boxes are roadmap vignettes, not implemented checkpoints. The only signals are `00-front-matter.md:72` ("Later checkpoints are roadmap targets") and Appendix I's mention of `code-gap.md`.
- Reader paths:
  - **Executives** skip Part I, although the Part I intro calls it "the starting point for the whole book" (`01-part-i.md:3`).
  - **Platform engineers** skip Part IV, which contains durable execution (Ch 15) and the catalogs.
  - **Application developers** skip Part VI, which holds the effect-safety chapter (Ch 22) they need when writing tools.
  - **SRE/operations** skip Ch 15 (durable execution, DR), Ch 20 (incident lifecycle), and Ch 23 (kill switch).
  - **Security** skips Part V (MCP/A2A), although T-12/T-13 depend on it.
- "Each major chapter moves from a concrete problem through boundaries, architecture, implementation, failure modes, measurement, and trade-offs" is untrue for Ch 16, 17, and 26.
- § The architecture in one view: the prose describes a request flowing through components, but Figure 0-1 is a map of Parts (§7.1). **Mismatch.**
- § The engineering contract behind the architecture gives six principles that overlap but do not match Ch 02's ten design principles. They are never cross-referenced.

**Find Your Way Through the Book**
- A bare table of contents with no one-line purposes, no dependency notes, and no Closing Perspective. It duplicates the generated TOC and adds little.

**Part intros**
- All present and brief. Part VI's second paragraph (control order) is unique and useful.
- The Part IV intro promises the Part "ends with a catalog of patterns and failure shapes". True, but the catalogs reach into Parts V–VIII.

**Appendices**

| Appendix | Relation to chapters | Duplication / gaps |
| --- | --- | --- |
| A — Choosing the Right Pattern | Re-summarizes Ch 16 + Ch 17 (P↔AP pairing) | Duplicates the Ch 16 cards. Odd pairings: P-09 Observability ↔ AP-07 "Model says done" (an acceptance anti-pattern); P-10 Governance ↔ AP-06 Boolean approval (an approval anti-pattern), citing Ch 14. No row for routing (Ch 11), planning (Ch 12), reflection (Ch 13), or human review (Ch 14) beyond chapter ranges. The Tools row omits Ch 21. |
| B — When Things Go Wrong | Compiles the chapters' If-fails steps | Third symptom table (§5.2). The § When an effect may have happened… runbook re-teaches Ch 22 and AP-05, with a different state vocabulary (§6 T13). Unique value: one-page triage. |
| C — Core Platform Contracts at a Glance | Summarizes contracts | Contradicts chapters: RunManifest fields, "AgentStep" name, "Effect Ledger" owner. Omits Plan IR, SkillManifest, SkillPackManifest, PolicyDecision, CredentialLease, MemoryRecord, ChangeBundle, RouteDecision, OwnershipTransfer. |
| D — Choosing an Agent Framework | Extends Ch 03's framework stance | Two overlapping tables (§7.2); overlaps the Ch 27 baseline stack; § Where the industry is heading is trend commentary. |
| E — What This Architecture Means for Research | New material | Cites AutoGen, AgentBench, GAIA, SWE-bench, τ-bench, AgentDojo, and "Emerging 2026 work" with **no [R] references**. Only ReAct (R01) is registered. Ch 25 (`07-part-vii.md:314`) also names AgentDojo without a citation. This is a citation-safety gap under `AGENTS.md`. |
| F — Known Limits | Synthesis of chapter caveats | Each limit is one fully bolded paragraph (formatting). Content is reinforcement, acceptable. |
| G — A Practical Roadmap | Synthesis; the executive entry point | Phases 0–5 add another numbered scale (§6 T11). The minimum bar duplicates Appendix L gates and chapter checklists. Otherwise valuable. |
| H — Glossary | Should anchor terminology | Only 15 terms, although Ch 01 says "Appendix H carries the full glossary" (`01-part-i.md:455`). Missing every term in Ch 01's own vocabulary table (idempotency key, effect ledger, compensation, downscoping, audience binding, RBAC/ABAC, provenance, acceptance criteria, canary, trace), all gateway names, RunManifest, ReleaseManifest, TaskEnvelope, ToolManifest, human action authorization, risk class/tier, planes/layers, Northstar, run/workflow/task. **Major gap.** |
| I — Companion Implementation Guide | Code for C01–C03 | § Corrections and closure notes reads as a changelog. The chapter roadmap for C04–C28 lives in `code-gap.md`, outside the book. |
| J — Prompt and Acceptance Criteria for a Coding Agent | Generator prompt for the platform design | Explains where the 13 "Required analysis" tables came from. Its 12-layer list differs from Ch 04's 11 layers. It restates acceptance criteria that the chapters teach. Questionable fit in a reader edition. |
| K — References and Evidence Scope | Generated from `config/references.json` | The source copy at `09-appendices.md:472` omits R44–R48, but the assembled `book/manuscript.md` includes them (verified), so this is not a defect. The source text files R14 (ISO/IEC 42001) under "Protocols, identity, and event standards" (`09-appendices.md:492`); check the generator's category. |
| L — Capacity, Resilience, and Release Acceptance | Extends Ch 28 + Ch 27 | Little's Law is repeated from Ch 28. The acceptance gates overlap Appendix G and the chapter checklists. |
| Closing Perspective | Book coda | Placed after Appendix L, not linked from Ch 28's closing or the front-matter TOC. "Harborlight began with one model call. It ends as explicit contracts…" overstates what the cumulative case implements (C01–C03). |

**Whether the appendices re-teach chapter material:** yes, for A, B, C, F, G, and L. They are useful as desk aids, but they are not reconciled with the chapters' current vocabulary. D, E, I, J, and K add new or maintainer material.

---

## 9. Candidate structural changes

Each item states the evidence and then the option the evidence supports. These are candidates for the per-Part reviews, not decisions.

**S1. Move or merge the Ch 16 pattern catalog.**
- *Evidence:*
  - P-06–P-11 depend on Ch 18–28 (§4 rows 40–45).
  - Ch 15's closing claim "The core patterns are now defined" is false.
  - Every Part IV pattern is described three or four times (prose, How-X card, P-card, Appendix A). *(Corrected in synthesis: only ReAct is described four times; routing, handoff, plan compilation, reflection, and human review have no P-card or Appendix A row, which is a catalog gap, not repetition. See chapter-10.md through chapter-13.md.)*
  - Appendix A duplicates Ch 16.
  - Ch 16 has no review sections and 12 single-child H2s.
- *Options:* (a) move Ch 16 (and Ch 17, see S2) after Ch 28 as a closing "Patterns and Anti-patterns in Review" Part, or (b) merge Ch 16 into Appendix A and drop the per-chapter How-X cards' overlap with it.

**S2. Reposition or slim the Ch 17 anti-pattern catalog.**
- *Evidence:*
  - AP-02/09/13 ↔ Ch 05/06; AP-03 ↔ Ch 21; AP-04/05 ↔ Ch 03/15/22; AP-06 ↔ Ch 03/14; AP-07 ↔ Ch 02/13; AP-08/11 ↔ Ch 18; AP-10 ↔ Ch 13; AP-12 ↔ Ch 08/19; AP-14 ↔ Ch 24; AP-15/16 ↔ Ch 07/27.
  - Ten of the sixteen corrections rely on Parts V–VIII (§4 rows 46–51). *(Corrected in synthesis: six cards depend on Parts V–VIII, three are adequately previewed, and seven are fully grounded in Ch 01–15, matching this map's own §2; see chapter-17.md.)*
  - Each chapter's own "If this fails in production" is a thin 3-step list that the matching AP card supersedes.
- *Option:* keep the catalog (it is the best-written diagnostic material) but place it after Part VIII. Replace the per-chapter "If this fails" lists with pointers to the relevant AP card.

**S3. Separate Ch 20 and Ch 23.**
- *Evidence:*
  - Both chapters' premise is "assume the model is compromised": Ch 20 § Respond as if the model can be compromised; Ch 23 § Why the model should be treated…, § Contain the blast radius…, § Start from the assumption….
  - Layer lists with counts 9 and 8 (plus the 6-layer Figure 20-1).
  - T-cards vs Ch 23 § Threats and required controls.
  - The injected-document example in both.
  - Incident containment in Ch 20 vs the kill switch and `incidents:contain` in Ch 23.
- *Option:* Ch 20 = threat model, boundaries, detector/policy/enforcement, incident lifecycle. Ch 23 = containment mechanisms only (sandbox, egress, secrets, DLP, taint, supply chain, kill switch). Delete Ch 23's threats table and two of its three framing H2s. Move the governance-record paragraph (`06-part-vi.md:1070`) to Ch 26.

**S4. Take the LLM Gateway out of Ch 19.**
- *Evidence:*
  - Ch 19's title and design choice cover MCP/A2A only, and its intro admits the add-on (`05-part-v.md:404`).
  - § What belongs at the LLM Gateway…, § What the LLM Gateway needs to enforce, § Filter for policy before optimizing cost or quality, and § What to measure at the LLM Gateway (`05-part-v.md:552–593`) plus Figures 19-1 and 19-2 duplicate Ch 01's gateway table.
  - The Ch 28 PERFORMANCE box restates the policy-first routing rule.
- *Options:* (a) a gateway section in Ch 04, next to the architecture, absorbing the Ch 01 table detail; or (b) a model-routing section in Ch 28. Retire Figure 19-1 in favor of Figure 1-4.

**S5. Trim Ch 03's pre-teaching.**
- *Evidence:* Ch 03 sections that re-teach later chapters:
  - § Human approval: interruption versus record and § Bind approval to the exact proposal (→ Ch 14)
  - § Three meanings of handoff (→ Ch 11/18)
  - § Guardrails and authorization solve different problems (→ Ch 20)
  - § One retry owner (→ Ch 22)
  - § The same rule applies to writes and § The complete execution path (→ Ch 22 § Invocation sequence, Ch 04 flow, Ch 15 flow)
  - § A tool is not the enterprise API and § Reauthorize the exact resource (→ Ch 21 § Carry identity all the way to the data, Ch 22 Tool Gateway)

  Ch 03 is the longest Part I chapter and carries six of §4's dependency problems.
- *Option:* reduce each of those sections to a two- or three-sentence preview with a forward pointer. Keep the runtime boundary, AgentStepRequest/Result, framework vs business state, the restart and replaceability tests, and upgrades as behavior changes.

**S6. Resolve Ch 22's placement and internal duplication.**
- *Evidence:*
  - Risk classes R0–R4 are used in Ch 12 and Ch 21 before Ch 22 defines them.
  - Unknown-effect is pre-taught five times.
  - Ch 22 is a reliability chapter inside the Security Part.
  - It has two implementation templates and two Required-analysis tables.
- *Options:* (a) minimum: merge the two § A workable implementation blocks and the two analysis tables; define risk classes earlier (Ch 02 § Scaling the shell or Ch 08) with Ch 22 as the full treatment. (b) Larger: move Ch 22 into Part IV after Ch 15 (durable execution + effects), or into Part I after Ch 02.

**S7. Restructure Ch 04.**
- *Evidence:*
  - Three decompositions (Figure 4-1 bands, plane table, layer table) plus Ch 01's bands.
  - Callouts sit mid-chapter.
  - § Seven planes… refers back across four sections.
  - The Run API is re-specified in Ch 15; the store table is re-specified in Ch 06. *(Superseded in synthesis: Ch 04 keeps both the base Run API and the physical-store table; Ch 15 and Ch 06 point to them. overall-book-review.md §D-03, §D-15.)*
  - AgentRuntime is never named, despite Ch 03's handoff.
- *Option:* order the chapter as opening boxes → plane table → layer split → trust boundaries → flow → contracts. Make Figure 4-1 use the plane names. Explicitly place AgentRuntime in the run/agent planes. Move the Run API detail to Ch 15 and the store table into Ch 06.

**S8. Deduplicate inside Ch 06.**
- *Evidence:* two pipelines (`02-part-ii.md:613`, `:692`), three ContextManifest shapes, two state taxonomies, and an unexplained artifact-adoption example.
- *Option:* one pipeline, one manifest schema, one taxonomy. Move the adoption policy to Ch 18/19.

**S9. Rebalance Ch 24, Ch 25, and Ch 07.**
- *Evidence:*
  - Ch 25 § A workable implementation is observability infrastructure; Ch 24 has none.
  - Ch 25's release-bundle and rollback questions duplicate Ch 27's.
  - Ch 25's checklist includes the use-case inventory.
  - Ch 25 has two "outcome and path" H2s and two test-layer lists.
  - Ch 07 has its own test pyramid and a debugging method that Ch 24 re-teaches.
- *Option:* move the telemetry components to Ch 24. Merge § Measure both the outcome and the path into § Judge the outcome and the path separately. Make one test/eval pyramid in Ch 25 and have Ch 07 point to it. Move Ch 07's debugging steps into Ch 24.

**S10. Rebalance Ch 26 and Ch 27.**
- *Evidence:*
  - Ch 27 § Governance controls, Governance Inventory, `governance/exceptions` and `governance/inventory` APIs, GovernanceRecord, and ExceptionWaiver implement Ch 26's concepts. Ch 26 has no implementation section.
  - Ch 27 also carries deployment topology (overlapping Ch 04 cells) and a technology stack (overlapping Appendix D).
  - Ch 27's evidence context promises the NIST 800-61 incident lifecycle, which Ch 20 covers.
- *Option:* move the governance implementation to Ch 26; move the baseline stack to Appendix D; reference Ch 04 for topology; fix or move the incident-lifecycle evidence context.

**S11. One TaskEnvelope, one envelope proof.**
- *Evidence:* duplicate code (§7.3); TaskEnvelope appears in four forms.
- *Option:* TaskEnvelope canonical in Ch 18; Ch 19 lists only federated additions; envelope code canonical in Ch 21; Ch 18 references it.

**S12. Fix the case's continuity.**
- *Evidence:*
  - The missing document drifts from "second pay statement" to "employment verification" (§6 T15).
  - Identifiers drift (§6 T16).
  - After C03, the boxes are disconnected vignettes: Ch 12's asset discrepancy, Ch 13's contradictory address, Ch 15's nine-day wait (vs a ten-day exercise at `04-part-iv.md:1339`), Ch 19's property-appraisal partner, Ch 24's twelve-minute review.
  - The Northstar boxes replace the case box in Ch 04, 06, 08, 27, 28.
- *Option:* either label boxes from Ch 04 onward as roadmap checkpoints (C04–C28, matching `code-gap.md`) with one cumulative case state, or say explicitly that they are independent scenarios. Unify the box type.

**S13. Decide the supplier thread.**
- *Evidence:* the supplier thread is promised in the Preface, How to Use, and Ch 01 § The comparative supplier-onboarding thread. It appears in the Ch 02 and Ch 03 boxes, then only unlabeled in P-02, AP-03, and AP-07. Meanwhile at least eight other domains appear in the Required-analysis rows and Ch 09.
- *Option:* either keep supplier onboarding as *the* comparative domain (relabel those examples and drop the others), or retire the promise in the Preface and Ch 01.

**S14. Repair the front matter.**
- *Evidence:* §8.
- *Option:*
  - Replace "Find Your Way Through the Book" with one-line chapter purposes plus a dependency note.
  - Fix the prose/figure mismatch in § The architecture in one view.
  - Reconcile the reader paths with the dependencies above.
  - Cross-reference the engineering contract with Ch 02's principles.
  - List the Closing Perspective.

**S15. Repair the appendices.**
- *Evidence:* §8.
- *Option:*
  - Merge A into the relocated Ch 16 (S1), or the reverse.
  - Merge B's symptom table with Ch 17's.
  - Expand H into the real glossary that Ch 01 promises, built from §6.
  - Reconcile C with the chapter contracts.
  - Dedupe D's two tables.
  - Add registry citations for E or weaken its claims.
  - Move J and I's corrections log to the companion repository.

**S16. Trim template boilerplate.**
- *Evidence:* §5.
- *Option:*
  - Explain the state-owner table once (Ch 01) or drop it where it is a heading's only content.
  - Remove the generic EVIDENCE BOUNDARY boxes in Ch 10–13, or replace them with real claims.
  - Convert the Required-analysis tables' "Enterprise example" rows to Harborlight, or delete them.
  - Unify the "Who should own each decision" format.
  - Fix the empty headings in §5.3.
  - Vary the P/AP/T-card stock phrases.

**S17. Fix the terminology collisions that contradict the thesis** (highest priority within §6).
- *Evidence and fixes:*
  - **Guardrail (T10):** the book argues guardrails are not enforcement, then names its whole security architecture and its numeric limits "guardrails".
  - **Planes (T2):** "execution plane" has two meanings.
  - **Approval vs authorization (T3):** collides with policy authorization.
  - **Risk numbering (T11):** two 0–4 scales.
  - **RunManifest vs ReleaseManifest (T7).**

  Fix these before prose-level edits, because every per-chapter review will touch them.
