# Chapter proposal — Enterprise Knowledge Management for Agents

**Status:** proposal, not yet written
**Proposed for:** Book v2.1.0
**Author of proposal:** drafted for Reza Rahimi, PhD
**Grounded in:** [`rrahimi-uci/policy-logic-forge`](https://github.com/rrahimi-uci/policy-logic-forge) and [`rrahimi-uci/policy-to-knowledge`](https://github.com/rrahimi-uci/policy-to-knowledge)

---

## 1. The proposition

An enterprise agent that can only retrieve documents can only ever answer
questions. To *act*, it needs to know what the organization knows, how the
organization operates, what constrains it, and what it is permitted to do — and
it needs all four in forms a machine can traverse, evaluate, and enforce.

The chapter argues that this is a distinct architectural layer, an **Enterprise
Knowledge Fabric for Agents**, and that RAG is one component of it rather than
the whole of it.

The claim that carries the chapter:

> Retrieving information, reasoning over it, deciding what is permitted, and
> executing an action are four different responsibilities with four different
> failure modes. An architecture that serves all four from one semantic index
> has not separated them; it has hidden them.

---

## 2. Why this chapter, and why now

The book already covers retrieval. Chapter 19 (*Context Engineering, RAG,
Memory, and State*) builds the context window and owns the retrieval pipeline.
What the book does not yet have is the layer **above** retrieval: the
organization's own semantics, rules, processes, data definitions, and
capability contracts as first-class, governed, machine-consumable artifacts.

Concretely, the book currently has no answer to:

- How does an agent know that "material exposure" means one thing in credit
  risk and another in insurance underwriting?
- How does a policy stop being prose an agent *reads* and become a constraint
  the platform *enforces*?
- How does an agent discover that a business entity exists, what its fields
  mean, who owns it, and whether it may see them?
- When two policies disagree, what does the platform do — and who decides?

That last question is where most enterprise knowledge programmes actually fail,
and it is the one this chapter can answer with real implementation evidence.

---

## 3. Placement, and the boundary with existing chapters

**Recommended placement: a new chapter 05 in Part II — Enterprise Reference
Architecture**, immediately after chapter 04 (*Enterprise Reference
Architecture, Boundaries, and Contracts*), renumbering the current 05–27.

Two reasons. First, this is architecture, not a pattern: it defines a layer and
its contracts. Second, Part II currently holds a single chapter, which the
v2.0.0 review flagged as the weakest structural spot in the book — a Part whose
title promises breadth and delivers one chapter. This fills it properly rather
than adding a ninth Part.

**The boundary must be drawn explicitly in the chapter's opening**, or it will
duplicate chapter 19. The proposed split:

| Concern | Chapter |
|---|---|
| Building the context window for one run; chunking, embedding, reranking, memory, workflow state | **19** (existing) |
| What the organization knows, as governed artifacts that outlive any run | **new 05** |
| Retrieval *mechanics* | 19 |
| Knowledge *representation, governance, and consumption contracts* | new 05 |

A one-line test for the author while writing: **if it changes per run, it is
chapter 19; if it is versioned, owned, and audited, it is this chapter.**

Adjacent chapters to cross-reference rather than re-explain:

- **04** — the platform contracts this layer plugs into
- **06** (*Skills as Versioned Capabilities*) — the capability catalog is the
  knowledge-side view of the same artifact; do not define Skills twice
- **20** (*Identity, RBAC/ABAC, and Delegated Authorization*) — permissions on
  knowledge are enforced there, described here
- **21** (*Tool Security, Effects, Idempotency, and Approval*) — guardrail
  enforcement at the effect boundary
- **25** (*Governance, Risk, and Operating Model*) — who owns knowledge
  artifacts organizationally

---

## 4. The conceptual model

The chapter's spine, to appear as its first diagram:

```text
Institutional Knowledge
  → Semantic Knowledge        (documents, embeddings, retrieval)
  → Business Semantics        (ontology, vocabulary, entities, relationships)
  → Rules & Decisions         (SBVR, DMN, executable constraints)
  → Processes                 (BPMN, CMMN)
  → Data                      (business data catalog, lineage, sensitivity)
  → Capabilities / APIs       (tool and action catalog, effects, prerequisites)
  → Agent Context & Guardrails
  → Agent Reasoning & Action
```

The important property is that **each layer is derived from the one above it and
carries provenance back to it**. A guardrail that cannot name the policy
sentence it came from is an opinion.

---

## 5. Four ways agents consume knowledge

This is the chapter's organizing distinction and should appear early, as a
table, then recur as a lens on every representation that follows.

| Mode | Question it answers | Typical representation | Failure mode when it is wrong |
|---|---|---|---|
| **Context** | *What is the situation?* | RAG, embeddings, semantic search | Plausible but stale or unauthorized grounding |
| **Reasoning** | *What should happen?* | Ontology, knowledge graph, DMN, SBVR | Correct facts, invalid inference |
| **Constraints** | *What am I permitted to do?* | Policies, permissions, regulations as enforceable rules | The agent explains the rule and then violates it |
| **Action** | *How do I do it?* | API/tool catalog, BPMN, capability contracts | Right decision, wrong or unauthorized effect |

The fourth column is what makes this more than taxonomy. Each mode fails
differently, so each needs different evidence, different tests, and different
guardrails — and an architecture that conflates them cannot tell you which one
broke.

---

## 6. Representation forms to cover

Each subsection follows the same shape: **what it represents → how agents
consume it → how it is governed → what it costs → when not to use it.**

### 6.1 Unstructured and semantic knowledge
Documents, policies, procedures, standards, historical decisions. RAG,
embeddings, hybrid and semantic search. **Cross-reference chapter 19 for
mechanics; cover here only what makes retrieval *governed*** — source
authority, effective dates, jurisdiction, supersession, and the difference
between "found in a document" and "authoritative".

### 6.2 Knowledge graphs and ontologies
Entities, concepts, relationships, dependencies, organizational semantics.
Traversal as an alternative to similarity. Where an ontology earns its cost and
where it becomes a modelling project that never ships. Property graphs versus
RDF/OWL, stated as a trade-off rather than a verdict.

### 6.3 Business rules and guardrails
The core of the chapter. Policy as **executable or enforceable constraint**,
not passive documentation. Rule typing (obligation, permission, prohibition),
conditions, outcomes, exceptions, hit policies, scope. The distinction between a
rule an agent *reads* and a rule the platform *enforces at the effect boundary*.

### 6.4 Agent-friendly business data catalog
Business entities, schemas, fields, definitions, relationships, ownership,
lineage, sensitivity, access constraints — described so an agent can discover,
understand, query, and reason about data *safely*. Semantic layer over physical
schema. Why a column name is not a definition.

### 6.5 Agent-friendly API and capability catalog
APIs, tools, services, actions, input/output contracts, permissions, **side
effects**, prerequisites, idempotency, operational constraints. Explicitly
connect to chapter 06's Skills and chapter 21's tool manifests: this is the
discovery view of artifacts the book already defines, not a new one.

### 6.6 Business process and decision models
**BPMN** (processes), **DMN** (decisions), **CMMN** (case management), **SBVR**
(vocabulary and rules) — evaluated honestly as machine-readable knowledge
agents can reason over. Where each standard genuinely helps, where it is
ceremony, and what an agent actually does with a BPMN file at planning time.
This section must avoid becoming a standards tutorial; the question is always
*what can an agent do with this that it could not do with prose?*

### 6.7 Governance and provenance
Ownership, versioning, provenance, effective dates, confidence, permissions,
lifecycle. The mechanism by which an agent distinguishes **authoritative** from
**contextual**, **inferred**, or **outdated** knowledge. This subsection should
read as the chapter's conscience: every representation above is only as good as
its provenance.

---

## 7. Knowledge algebra: union, intersection, difference, contradiction

**This is the most original section available to the chapter and should be
positioned as such.** Enterprises do not have one knowledge base; they have many
overlapping ones — two regulators, two business units, two versions of the same
policy. Agents must operate across them, and that requires defined operations.

| Operation | Meaning | What an agent may do with the result |
|---|---|---|
| **Intersection** (G₁ ∩ G₂) | Rules present in both sources | Highest-confidence knowledge; safe to act on |
| **Difference** (G₁ − G₂, G₂ − G₁) | Rules exclusive to one source | Scope-dependent; requires jurisdiction check |
| **Union** (G₁ ∪ G₂) | All unique rules, provenance preserved per source | Complete coverage; conflicts still possible |
| **Contradiction** | Rule pairs that cannot both be satisfied | **Stop. Escalate. Never auto-resolve.** |

Three principles the chapter should argue for, each supported by implementation
evidence in §8:

1. **Union is not merge.** Combining two knowledge bases must preserve which
   source each rule came from and what its original identifier was. A union that
   flattens provenance destroys the only information that can later resolve a
   conflict.
2. **Contradiction is a first-class result, not an error.** A contradiction
   detected between two authoritative sources is a *finding about the
   organization*, frequently a valuable one. The architecture's job is to
   surface it with structured evidence, not to silently pick a winner.
3. **Semantic equivalence never overrides deterministic alignment.** Where rules
   align by identifier or citation, that alignment stands; model-judged
   equivalence is advisory and marked for review.

The chapter should also state the limits plainly: these operations are defined
over *typed rules with declared scope*, not over free text. Two documents cannot
be intersected; two rule sets can.

---

## 8. Grounding: two real implementations

The chapter must not stay conceptual. Both projects are public, and between them
they cover the entire pipeline this chapter describes.

### 8.1 `policy-to-knowledge` — documents to a queryable graph

A 15-agent pipeline (eleven extraction, four comparison) turning compliance
documents into a knowledge graph where every rule traces to its source passage,
with a JanusGraph-backed explorer for query, annotation, and versioning.

What it supplies to the chapter:

- **The set operations of §7, already implemented** in
  `apps/pipeline/agents/agent_9_set_operations.py`: intersection, left and right
  difference, union, and contradictions, each emitted as a separate artifact.
- **Union with preserved provenance** — merged rules carry `sources`,
  `original_ids` per source graph, `match_type`, `confidence`, and the reasoning
  behind the match, with both original rules retained for display.
- **Contradictions that preserve both sides** — a contradiction entry keeps both
  rules intact with their own provenance rather than resolving them. This is the
  concrete form of principle 2 above.
- **A relationship taxonomy** — `IDENTICAL`, `EQUIVALENT`, `CONTRADICTORY`,
  `UNRELATED` — separating deterministic matching from semantic judgement.
- **`schemas/rule_v2.schema.json`** — a rule schema whose *required* fields
  include `applicability_scope`, `scope_basis`, `responsible_party`,
  `counterparties`, `exceptions`, `exception_basis`, `test_vectors`, and
  `field_evidence`. That field list is itself an argument: a rule without
  declared scope, declared basis, and its own test vectors is not executable
  knowledge.

### 8.2 `policy-logic-forge` — policy text to verified, executable logic

A thirteen-agent pipeline structured as **Extract → Prove → Project**: extract
rules with an LLM, decide whether to believe them, then project survivors into
standards-compliant models.

What it supplies to the chapter:

- **The Extract/Prove/Project split**, which is the single most transferable
  idea in either repository. Extraction is probabilistic; verification must not
  be. The chapter should generalize this as an architectural principle for any
  knowledge pipeline that uses a model.
- **Independent grounding verification** — `agent_09` does not trust the
  citation a rule carries; it rebuilds the evidence from the raw corpus. On one
  real run it **rejected 44% of the dependency and conflict claims that the
  pipeline's own deterministic guard had already accepted.** That number belongs
  in the chapter: it is the empirical case for independent verification.
- **A four-invariant executable-readiness gate** with a remediation loop — the
  model of "knowledge is not ready until it provably satisfies stated
  invariants".
- **Real DMN, BPMN, CMMN, and SBVR artifacts** generated from extracted rules,
  which lets §6.6 show the standards being produced rather than described.
- **LExec IR** — a typed intermediate representation with provenance at the
  effect level (`chunk_path`, `section_id`, byte offsets, `source_sha256`), an
  explicit three-valued null model, and a documented refusal at table
  boundaries when a value is unknown. This is what "machine-consumable" actually
  looks like when taken seriously.
- **RegDelta** — differential execution across policy versions, with semantic
  candidates always marked `review_required` and never allowed to change
  deterministic alignment. This is principle 3 above, implemented.
- **LinkML as the canonical business information model**, chosen because *a
  schema can be checked where a UML diagram can only be read*. That sentence is
  worth quoting directly; it captures the chapter's whole attitude.
- **Machine-checked properties** discharged by exhaustive enumeration rather
  than by example.

### 8.3 The worked example running through the chapter

One policy statement, followed end to end, appearing in each representation:

```text
Policy sentence
  → Extraction (typed rule + conditions + outcomes + scope)
  → Independent grounding verification (evidence rebuilt from the corpus)
  → Knowledge graph (entities, relationships, dependencies)
  → DMN decision table / SBVR vocabulary
  → Executable guardrail at the effect boundary
  → Agent reasoning
  → Governed action
```

The AML example already in `policy-logic-forge` is a good candidate:
*"Transactions exceeding $10,000 require compliance officer approval before
processing."* It is one sentence, it exercises every layer, and its LExec
lowering is already documented — including the instructive quirk that
`transaction_amount` lowers to a real rather than an integer, because the IR
refuses to infer an integer theory from an integral-looking value.

---

## 9. Proposed chapter outline

Following the book's established chapter template, with the sections this
subject needs.

| § | Section | Substance |
|---|---|---|
| 1 | What this chapter delivers | The four consumption modes, stated as the chapter's contract |
| 2 | Solution blueprint | The Knowledge Fabric layer diagram |
| 3 | Why RAG is not a knowledge architecture | The argument, with the failure modes of each consumption mode |
| 4 | The knowledge fabric layers | §6.1–6.5 |
| 5 | Standards that already exist | §6.6 — BPMN, DMN, CMMN, SBVR, evaluated not evangelized |
| 6 | From policy text to enforceable logic | §8.2 — Extract / Prove / Project |
| 7 | Knowledge algebra | §7 — union, intersection, difference, contradiction |
| 8 | Governance and provenance | §6.7 |
| 9 | Grounding, corrections, and evidence boundary | Per book convention |
| 10 | Implementation reference | Verified examples (§11) |
| 11 | Reference architecture: the Enterprise Knowledge Hub | §10 |
| 12 | Debugging playbook | Stale authority, ontology drift, silent contradiction, catalog rot |
| 13 | Production checklist | — |
| 14 | Exercises / Technical review questions | Per book convention |
| 15 | Transition | Into the developer platform Part |

Target length **3,000–3,600 words**, placing it among the book's substantial
chapters without exceeding chapter 21's 3,393.

---

## 10. The reference architecture to conclude with

A single diagram plus a contract table, showing how the representations coexist
and how an agent discovers and consumes them at run time:

```text
                 ┌──────────────── Governance plane ────────────────┐
                 │ ownership · versioning · effective dates ·        │
                 │ provenance · confidence · permissions · lifecycle │
                 └───────────────────────┬──────────────────────────┘
                                         │ applies to every artifact below
  ┌──────────┬───────────┬───────────────┼────────────┬──────────────┬──────────┐
  │ Semantic │ Ontology  │ Rules &       │ Process &  │ Business     │ Capability│
  │ index    │ & graph   │ decisions     │ case models│ data catalog │ catalog   │
  │ (RAG)    │ (KG/OWL)  │ (SBVR/DMN)    │(BPMN/CMMN) │ (semantics)  │ (tools)   │
  └────┬─────┴─────┬─────┴──────┬────────┴─────┬──────┴──────┬───────┴────┬──────┘
       │           │            │              │             │            │
       ▼           ▼            ▼              ▼             ▼            ▼
    Context     Reasoning   Constraints     Planning      Data access   Action
       └───────────┴────────────┴──────────────┴─────────────┴────────────┘
                                         │
                              Knowledge resolution API
                    (one query surface; permissions enforced here)
                                         │
                                   Agent runtime
```

The chapter should insist on the **knowledge resolution API** as the single
consumption surface. Agents must not hold connection strings to six stores; they
ask one service, which resolves, authorizes, and attributes.

---

## 11. Verified examples to build

The book's contract (see `examples/README.md` and `AGENTS.md`) is that **every
code listing is a real file that CI executes**. This chapter must follow it —
which also means the examples below are the chapter's acceptance tests, not
decoration.

| Example | Demonstrates | Verification |
|---|---|---|
| `knowledge/policy_to_rule.py` | A policy sentence as a typed, scoped rule with source provenance | `test` — asserts required fields and a resolvable citation |
| `knowledge/grounding_verifier.py` | Rebuilding evidence from the corpus; rejecting a fabricated citation | `test` — a planted hallucinated citation must fail |
| `knowledge/knowledge_graph.py` | Traversal answering a question similarity cannot | `test` — multi-hop dependency resolution |
| `knowledge/rule_as_guardrail.py` | A rule enforced at the effect boundary | `test` — a prohibited effect is refused before dispatch |
| `knowledge/set_operations.py` | Union / intersection / difference with preserved provenance | `test` — union keeps both `original_ids`; intersection is symmetric |
| `knowledge/contradiction_detection.py` | Structured contradiction, escalated not resolved | `test` — conflicting rules raise with both sides intact |
| `knowledge/data_catalog.py` | Discovering an entity, its meaning, sensitivity, and access constraint | `test` — a restricted field is not returned to an unauthorized purpose |
| `knowledge/capability_catalog.py` | Discovering a capability with effects and prerequisites | `test` — a mutating tool is not selected without an approval prerequisite |
| `knowledge/dmn_decision.py` | A DMN table evaluated by an agent | `test` — hit policy honoured; unknown input refuses rather than guesses |
| `knowledge/resolution_api.py` | Context + rules + process + data + capability composed before one action | `test` — end-to-end, with permission denial covered |

Ten examples is more than any existing chapter carries, which is appropriate: it
is the chapter making the argument that this layer is buildable.

---

## 12. Figures, tables, and assets

New diagrams must be registered in `config/diagrams.json` and meet the book's
asset contract (1800 × 1000 px, ≥255 effective dpi at publication width).

| Asset | Type |
|---|---|
| Knowledge fabric layer architecture | diagram |
| The knowledge chain (institutional → action) | diagram |
| Policy → extraction → verification → graph → guardrail pipeline | diagram |
| Knowledge algebra over two graphs | diagram |
| Enterprise Knowledge Hub reference architecture | diagram |
| Four consumption modes | table |
| Representation form comparison, with costs and when not to use | table |
| Standards comparison (BPMN/DMN/CMMN/SBVR) | table |
| Governance metadata contract | table |

---

## 13. Citations required

BPMN, DMN, CMMN, and SBVR are OMG specifications and must be added to
`config/references.json` with version, URL, access date, and a **narrow
permitted scope** per the book's citation discipline — each supports the
existence and semantics of its own standard and nothing more. LinkML and
JanusGraph likewise if referenced by name.

The two projects are the author's own work and must be presented as **book-authored
implementation evidence, not third-party validation.** The 44% rejection figure
is a measurement from one run of one pipeline; it should be stated with that
scope attached, not generalized into a claim about LLM extraction in general.

---

## 14. Risks and open questions

- **Scope.** This chapter could become three. The four-consumption-mode frame is
  what keeps it one; anything that does not serve that frame should be cut.
- **Overlap with chapter 19** is the single largest risk. The boundary in §3
  must be written into both chapters' transitions, not just this one's opening.
- **Standards fatigue.** BPMN/DMN/CMMN/SBVR can swallow the chapter. Budget
  ~500 words total and lead with what an agent *does* with each artifact.
- **Ontologies are where enterprise programmes go to die.** The chapter should
  say so and give a smallest-useful-ontology heuristic rather than encouraging a
  modelling exercise.
- **Self-citation.** Two of the author's own repositories carry the chapter's
  empirical weight. That is legitimate and it must be labelled.
- **Renumbering cost.** Inserting at position 05 renumbers 22 chapters and their
  figure captions. The v2.0.0 restructure built the machinery for exactly this
  (`reports/restructure-map.json`, the derived validators), so the cost is
  mechanical — but it is a major version bump, not a patch.

---

## 15. Acceptance criteria

The chapter is done when a reader can:

1. Explain why RAG alone cannot serve an agent that takes action.
2. Name the four consumption modes and the distinct failure mode of each.
3. Choose a representation for a given knowledge need, and say when not to.
4. Trace a policy sentence to an enforced guardrail, with provenance intact at
   every step.
5. Compute union, intersection, difference, and contradiction over two knowledge
   bases, and say what an agent may do with each result.
6. Describe how an agent discovers data and capabilities at run time.
7. State the governance metadata every knowledge artifact must carry.
8. Build a minimal knowledge hub from the reference architecture.

And when the repository can: all ten examples pass in CI, all diagrams are
registered and meet the asset contract, all standards are cited with scoped
permissions, and `make validate` is green.

---

## 16. Execution brief

For handing to a coding or research agent. Work in this order; do not write
prose before step 3 is complete.

1. **Inspect both repositories directly.** Clone `policy-logic-forge` and
   `policy-to-knowledge`. Read `ARCHITECTURE.md` in the former (start with §1.1,
   the evidence spine, and §6, the executable model formats) and
   `apps/pipeline/agents/agent_9_set_operations.py` plus
   `schemas/rule_v2.schema.json` in the latter. Do not rely on this proposal's
   summary of them; verify every claim it makes, including the 44% figure and
   the `rule_v2` required-field list.
2. **Research the standards from primary sources.** OMG specifications for BPMN,
   DMN, CMMN, SBVR. Record version and access date for each. Resolve whether
   each is genuinely useful to an agent or merely available.
3. **Extract the generalizable architecture.** Identify which concepts in the two
   projects are specific to compliance policy and which generalize to any
   enterprise knowledge domain. The chapter is about the latter; the former is
   illustration. Extract/Prove/Project, independent grounding verification,
   provenance-preserving union, and non-resolving contradiction are the leading
   candidates.
4. **Build the ten examples first** (§11), as real files under `examples/` with
   behavioural tests, registered in `config/examples.json`. Prose written after
   working code will be more accurate than prose written before it — and the
   book's CI will reject listings that are not real.
5. **Write the chapter** against the outline in §9, citing examples by
   `[[EXAMPLE:id]]` marker rather than pasting code.
6. **Produce and register the diagrams** (§12).
7. **Add the citations** (§13) with narrow scopes.
8. **Run the full gate**: `make validate && make examples-run && make pdf`, then
   `make package`.
9. **Open a pull request** following `.github/pull_request_template.md`. Do not
   merge it.

Constraints that are not negotiable, from `AGENTS.md` and
`styles/CROSS-FORMAT-CONTRACT.md`:

- Edit `source/parts/*.md` only. Never hand-edit `book/manuscript.md`,
  `dist/*`, or `latex/content/book-content.tex`.
- Code goes in `examples/` with a behavioural test. Never paste code into
  `source/parts/`.
- Every `[Rxx]` citation must resolve to a registry entry with a scope that
  actually supports the claim.
- Book-authored recommendations stay labelled as guidance unless a cited source
  covers them.
