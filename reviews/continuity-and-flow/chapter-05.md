# Chapter 05 — Give Knowledge an Owner: Continuity and Flow Review

Reviewed: `source/parts/02-part-ii.md:342–585`. For transitions I also read Ch 04's knowledge-related tables and closing (`02-part-ii.md:36–44`, `:113–142`, `:228–242`, `:338–340`) and Ch 06 in full (`:587–947`), especially § Semantic knowledge's hand-off to it. I also checked Ch 03's retrieval-as-tool example (`01-part-i.md:1061`), Ch 08 § The Skill manifest (`03-part-iii.md:206–208`), Ch 22's ToolManifest, AP-09 (`04-part-iv.md:1624`), and the example registry entries for the seven `examples/knowledge/*` listings.

## Overall Assessment

This is the strongest chapter in Part II. It has one clear thesis (retrieval is one consumer of governed knowledge, not the knowledge itself) and a crisp failure taxonomy (four consumption modes, each failing differently). It adds three unique mechanisms that no other chapter re-teaches:

- extract → prove → project, with an honestly scoped measurement;
- set operations over rule sets ("union is not merge", "a contradiction is a result");
- three-valued rule evaluation.

Its code is all in tested `examples/`. The prose is tight.

The problems are mostly about connections rather than content:

1. **Terminology that contradicts the book's thesis.** "Guardrail" is used for an enforced rule (`:388`, `:418`, `:449`, `:459`, `:547`), the opposite of Ch 03 and Ch 20's "a guardrail is a detector, not the boundary".
2. **Three taxonomies that are never mapped to each other:** four consumption modes (`:373–378`), six representations (the H3s at `:390–432`), and six Hub views (`:528–535`). The Hub, the chapter's architectural synthesis, arrives *after* § A sensible place to start.
3. **An unreconciled boundary with Ch 06 and Ch 03.** Ch 05 says agents "ask one service" (`:526`). Ch 06 has a Context Assembler and a Retrieval Broker do the asking, and Ch 03 retrieves policy through a Tool Gateway façade. Nobody says these are one resolution surface.
4. **A weak link back to Ch 04.** The chapter never says which plane it fills or how its pinned knowledge versions reach the RunManifest.

## Intended Reader Mental Model

On arrival the reader knows that the architecture has a knowledge/context plane (Ch 04), that retrieved text is untrusted (Ch 04 trust boundaries), and RAG basics.

The reader should leave with:

- **What:** institutional knowledge is a set of owned, versioned, scoped artifacts.
- **Why:** similarity is not authority, currency, or permission, and each of the four modes fails differently.
- **How:** typed rules extracted with provenance, independently verified, owner-approved, projected into enforced constraints, combined with set operations, and served through one authorizing Hub.
- **When:** model only what an agent must traverse; adopt DMN first.
- **Relationships:** the Hub is the knowledge half of Ch 04's plane. Ch 06 consumes it per step. Ch 08 and Ch 22 own the capability artifacts that the Hub indexes.
- **Practical application:** a policy sentence can be turned into a rule that refuses an effect in a test.

## Section-by-Section Flow Review

**Opening callouts (`:344–350`).** *Role:* case box ("quotes the policy, then violates it") and design choice. *Verdict:* strong. It is a standalone vignette, not a continuation of C03's EVIDENCE_REVIEW state (map S12). *Issues:* the box says "starts building a knowledge layer". Use the plane name chosen in C04-R01.

**§ Why retrieval alone is not a knowledge strategy (`:352–359`).** *Role:* intro. *Adds:* four jobs behind "put it in a vector store". *Verdict:* good, but it names the four modes in different words from the table 20 lines later ("retrieve evidence, reason, enforce constraints, discover a capability" versus Context / Reasoning / Constraints / Action). *Issues:*

- There is no bridge from Ch 04.
- The phrase "source of truth, the policy engine, and the tool catalog" is a 3-item list beside a 4-mode claim.

**§ Treat knowledge as a set of products (`:361–367`).** *Role:* holds Figure 5-1 and the state-owner table. *Verdict:* an empty container (map §2). *Issues:*

- "Products" is never defined. The design choice says "governed artifacts" and the table says "KnowledgeArtifact".
- The figure is first described by the *next* section (`:371`).

**§ Why similarity cannot tell you what to trust (`:369–382`).** *Role:* the four-mode table and the Harborlight failure. *Adds:* the chapter's core diagnostic ("the fourth column is the argument"). *Verdict:* excellent. *Issues:* `:382` restates the case box closely. That is deliberate reinforcement, since it explains the box, and it is acceptable. Trim only if the box itself is shortened.

**§ How enterprise knowledge becomes usable (`:384–388`).** *Role:* the lead-in to the six representations. *Verdict:* misordered. *Issues:*

- `:386` (the pay-statement age-window rule: extract → preserve span → owner verifies → compile → record version) is the extract/prove/project pipeline in miniature, taught 60 lines before § Turn policy prose into logic the system can enforce. Its step list also differs from that section's: the owner-verification step appears here and nowhere in Extract/Prove/Project.
- `:388` uses "guardrail" for an enforced rule (T10).

**§ Semantic knowledge (`:390–394`).** *Role:* governed retrieval metadata. *Verdict:* good scoping. *Issues:* "Chapter 6 owns the mechanics — chunking, reranking, and the context window itself" is only partly kept. Ch 06 never teaches chunking: it appears as one stage name in an ingestion bullet (`:769`) and a field (`:732`). Reranking is one bullet (`:761`). Ch 06 does own ordering, ranking, budget, and the manifest.

**§ Ontology and knowledge graph (`:396–404`).** *Role:* traversal versus similarity. *Verdict:* good, with an honest caveat and a bounded-traversal warning. No issues.

**§ Business rules as enforceable constraints (`:406–418`).** *Role:* the core of the layer: rule shape, scope, and three-valued evaluation. *Verdict:* strong. *Issues:*

- "Guardrail" at `:416` (example id `rule-as-guardrail`) and twice at `:418` (T10).
- The sentence about "identity by content rather than by assigned identifier" (`:412`) depends on the example and should name what is hashed (the normalized rule and its source span).

**§ Business data catalog (`:420–422`).** *Role:* field semantics and sensitivity. *Verdict:* thin but sufficient. *Issues:* it does not say where the sensitivity class is used. That happens in Ch 06 stage 5 (Classify and sanitize) and in the manifest's redactions. Add one pointer and nothing more.

**§ Capability and API catalog (`:424–430`).** *Role:* capabilities with their consequences. *Verdict:* good, with correct pointers to Ch 08 and Ch 22. *Issues:*

- "It is the same artifact seen from discovery rather than from execution" leaves ownership open. Under Ch 04's single-writer rule, the Hub must *index* the Skill manifest (Ch 08 Skill Registry) and the ToolManifest (Ch 22), not own a second copy.
- "Filtering during discovery… should never appear" reinforces Ch 08 § Discovery is not permission. That is R, and acceptable.

**§ Process and decision models (`:432–443`).** *Role:* BPMN/DMN/CMMN/SBVR and what an agent does with each. *Verdict:* excellent. It is scoped by evidence (R44–R47) and opinionated ("DMN earns its place fastest"). No issues.

**§ Turn policy prose into logic the system can enforce (`:445–463`).** *Role:* Extract → Prove → Project, the 44% measurement, and the COMMON PITFALL. *Verdict:* the chapter's best section. *Issues:*

- *Missing step:* there is no human owner approval between Prove and Project, although `:386` requires "an eligible owner verify the interpretation". Automated grounding does not establish that the interpretation is correct.
- "Guardrail" appears in the figure caption (`:449`) and at `:459`.

**§ Combine knowledge without flattening its differences (`:465–488`).** *Role:* set operations and three rules of the architecture. *Verdict:* unique and strong; no other chapter covers it. *Issues:* none. The ARCHITECTURE GUIDANCE line "a corpus with a search box" lands well.

**§ Why provenance determines what you can trust (`:490–509`).** *Role:* governance metadata fields and the SECURITY box. *Verdict:* good. *Issues:*

- "Provenance" here means content lineage. Ch 09, 23, and 27 use it for build provenance (SLSA) without distinguishing the two (map §3).
- The section is the natural home for "the index is a disposable projection of the source revision" and for ingestion freshness. Both currently sit in Ch 06 (`:760`, `:769`), which leaves the Part intro's "how knowledge stays current" (`:5`) under-delivered in this chapter.

**§ What the evidence lets us conclude (`:511–518`).** Well-scoped claims. No issues.

**§ A sensible place to start (`:520–522`).** *Role:* says that the inline examples compose a hub. *Verdict:* fine as a one-paragraph summary. *Issues:* it is immediately followed by architecture content (§ Reference architecture), which inverts the chapter's arc.

**§ Reference architecture: the Enterprise Knowledge Hub (`:524–541`).** *Role:* six Hub views and one query surface. *Verdict:* the essential synthesis, but misplaced and unconnected. *Issues:*

- It comes after "start".
- The six views are not mapped to the four modes or to the six representation H3s.
- It does not say where it sits in Ch 04's planes and layers (Figure 4-1 shows "Context service · Search·vector index · Catalog·lineage · Memory·Skills" and no Hub).
- It does not say who its callers are. Ch 06 names a "Retrieval Broker" (`:707`) and `POST /v1/knowledge:search` (`:716`) without reference to the Hub, and Ch 03 retrieves policy through a Tool Gateway façade (`01-part-i.md:1061`).
- The PRODUCTION CONSIDERATION (`:541`) is the right idea, but it does not point to the RunManifest's `knowledge_snapshots` field (`:190`).

**§ If this fails in production (`:543–552`).** *Role:* a symptom table. *Verdict:* more useful than the three-step template. Keep it. *Issues:*

- "Is any guardrail evaluating it" (`:547`) uses the wrong term (T10).
- "Effect class" (`:551`) is an undefined term (map §4 row 29, "side-effect class"). Use Ch 22's ToolManifest effect semantics or risk class.
- Row 3 says "run manifest" in lowercase. Name the RunManifest.

**Template sections: § What to verify before production (`:554`), § Put the idea to work (`:565`), § Questions to bring to design review (`:572`).** *Verdict:* content is good and chapter-specific; exercises 2–4 are excellent. *Issues:* format drift only. The checklist uses plain bullets instead of the ✓ form, and the Q table header is "What a good answer demonstrates" instead of "Strong answer". The Q column is a better design, but it should be a book-wide decision, not a one-chapter deviation.

**§ Where this leads next (`:583–585`).** *Verdict:* good. It sets up Ch 06's three questions accurately.

## Sparse or Underdeveloped Content

- **The Hub's position and callers (`:524–537`).** Two sentences are missing: where the Hub sits in Ch 04's knowledge, context, and memory plane, and that the Context Assembler and read tools are its callers (C05-R02).
- **Owner approval in the pipeline (`:451–459`).** One sentence is missing (C05-R04).
- **Knowledge freshness (`:490–505`).** Index-as-projection and ingestion cursors are absent here (C05-R08).

Do not add a "How X works in practice" card or an "A workable implementation" section. The examples and the Hub table already do that job, and a card would only re-summarize (map §5.1).

## Missing Conceptual Connections

- **Ch 04 plane → Ch 05 Hub, missing "this chapter fills the knowledge half of the knowledge, context, and memory plane".** At `:354` and `:526`.
- **Four modes → six Hub views, missing the mapping.** At `:528–535`: Semantic → Context; Structural and Procedural → Reasoning; Normative → Constraints; Capability → Action; Governance → all four.
- **Ch 05 Hub → Ch 06 Retrieval Broker and Ch 03 retrieval tool, missing "one resolution surface, two call paths".** At `:537`: pre-step assembly by the Context Assembler, and in-step reads through a Tool Gateway read tool. Both resolve through the Hub and its permissions.
- **Prove → Project, missing owner approval.** At `:453–459`.
- **Capability catalog → Ch 08/Ch 22, missing "the Hub indexes; the registries own".** At `:430`.
- **Pinned knowledge (`:541`, `:549`, `:562`) → Ch 04 RunManifest `knowledge_snapshots` (`:190`).**

## Transition Problems

- **In (Ch 04 → Ch 05).** Ch 04 closes on "the reference architecture names a knowledge plane". Ch 05 opens with a case box and never mentions Ch 04, the plane, or Figure 4-1. Fix with C05-R13 and C04-R18.
- **Within the chapter.**
  - § Treat knowledge as a set of products (`:361`) interrupts the move from the "why" intro to the four-mode table.
  - `:386` pre-teaches the pipeline before the representations.
  - § A sensible place to start → § Reference architecture inverts summary and synthesis.
- **Out (Ch 05 → Ch 06).** Good. Ch 06's opening, however, does not pick up the thread (see C06-R06).

## Redundant and Repetitive Concepts

- **Four modes introduced twice** with different labels (`:354–356` and `:373–378`). Align the labels (C05-R03).
- **The extract → verify → compile chain** at `:386` and `:451–459`. Merge (C05-R04).
- **Permissions at the resolution boundary:** the SECURITY box (`:509`), the Hub (`:537`), and checklist item 8 (`:563`). This is deliberate reinforcement of the chapter's single security claim; keep it.
- **Version pinning:** PRODUCTION CONSIDERATION (`:541`), If-fails row 3, checklist item 7, and Q6. Reinforcement; acceptable once the RunManifest pointer is added.

## Cross-Chapter Duplication

| Ch 05 location | Other location | Verdict | Recommended owner |
| --- | --- | --- | --- |
| § Why similarity cannot tell you what to trust | AP-09 Vector store as source of truth (`04-part-iv.md:1624`); Ch 04 `:242` | R (AP-09 adds symptoms and repair metrics) | Ch 05 |
| § Capability and API catalog (`:430`) | Ch 08 § Discovery is not permission; Ch 22 § What a ToolManifest must declare | R, but the ownership is ambiguous | Ch 08/22 own the artifacts; Ch 05 owns discovery-side indexing (C05-R06) |
| § Why provenance determines what you can trust | Ch 06 ContextSegment/MemoryRecord fields (`:730–731`); Ch 27 supply-chain provenance | R (Ch 06 applies it); different meaning in Ch 27 | Ch 05 for content provenance; Ch 27 for build provenance |
| SECURITY box (`:509`) | Ch 06 stage 3 (`:625`, `:634–636`); Ch 21 § Data-plane controls (`06-part-vi.md:431`) | R | Ch 06 owns ordering; Ch 21 owns enforcement; Ch 05's one-line statement stays |
| § If this fails in production (symptom table) | Ch 17 § Find the failure by its first symptom; Appendix B | R (chapter-specific rows) | Keep; no change |
| Ingestion and index freshness | Ch 06 § Retrieval and memory consistency (`:760`), § Scalability and token economics (`:769`) | Misplaced in Ch 06 | Move to Ch 05 (C05-R08 / C06-R10) |

I disagree with the map on one point. It calls Ch 05 "otherwise self-contained". It is self-contained in mechanism, but it leaves the Hub-versus-Ch 06 broker relationship, the Ch 6 chunking promise, and capability ownership unresolved. Each of those creates a cross-chapter seam.

## Structural Recommendations

1. Delete § Treat knowledge as a set of products. Move Figure 5-1 and the state-owner table to the top of § Why similarity cannot tell you what to trust, where the figure is first discussed.
2. Move `:386` into § Turn policy prose into logic the system can enforce as its worked example. Keep `:388` (lineage) as the lead-in to the representations.
3. Move § Reference architecture: the Enterprise Knowledge Hub to directly after § Why provenance determines what you can trust and before § What the evidence lets us conclude. The order becomes: modes → representations → pipeline → combination → provenance → Hub (synthesis) → evidence → start.

## Concrete Recommended Changes

1. **C05-R01 — High — Rewrite.**
   - *Location:* `:388`, `:416`, `:418`, `:449` (Figure 5-2 caption and `assets/diagrams/src/policy-to-guardrail.gv` labels), `:459`, `:547`.
   - *Issue:* "guardrail" names an enforced rule, which contradicts Ch 03 § Guardrails and authorization solve different problems and Ch 20 § Guardrails help, but they are not the security boundary.
   - *Why:* the reader learns in Ch 03 that guardrails detect rather than enforce, and Ch 05 teaches the opposite.
   - *Change:*
     - Replace "guardrail" with "enforced rule" or "constraint at the effect boundary".
     - `:388`: "A constraint that cannot point to the sentence or decision behind it…".
     - `:418`: "A rule check that reads *unknown* as *permitted* is not a control."
     - Figure 5-2 caption: "…from policy text to an enforced constraint"; update the `.gv` labels and run `make diagrams`.
     - `:547`: "Is any rule evaluated at the effect boundary?"
     - Renaming the example id `rule-as-guardrail` → `rule-at-effect-boundary` (and the diagram id `policy-to-guardrail`) is optional. If done, update `config/examples.json` and `config/diagrams.json`.
   - *Related:* map T10.

2. **C05-R02 — High — Add.**
   - *Location:* § Reference architecture: the Enterprise Knowledge Hub, after `:537`.
   - *Issue:* the Hub's callers and position are undefined, and three retrieval paths in Ch 03, 05, and 06 are not reconciled.
   - *Why:* without this, the reader sees three "retrieval services" and cannot tell which enforces permissions.
   - *Change:* add two sentences.
     - "The Hub is the knowledge half of the knowledge, context, and memory plane (Chapter 4). It has two kinds of caller: the Context Assembler, which resolves pre-step context (Chapter 6), and read-only tools invoked through the Tool Gateway during a step (Chapter 3). Both reach the same permissions and attribution; neither holds store connections."
     - The Ch 06 side is C06-R06, which names the Retrieval Broker as the Hub's client. Ch 05 owns the Hub definition; Ch 06 must not define a second knowledge service.
   - *Related:* C06-R06, C04-R01.

3. **C05-R03 — High — Merge / Rewrite.**
   - *Location:* `:352–367` (§ Why retrieval alone is not a knowledge strategy; § Treat knowledge as a set of products).
   - *Issue:* an empty H2, the undefined "products", and two wordings of the four modes.
   - *Why:* the core taxonomy should be met once, under one set of names.
   - *Change:*
     - Delete the `:361` heading and move Figure 5-1 and the state-owner table under § Why similarity cannot tell you what to trust, before `:371`.
     - At `:354–356`, use the table's mode names: "four different jobs: supply context, support reasoning, enforce constraints, and enable action".
     - At `:358–359`, name all four: "cannot be the evidence source, the inference model, the policy engine, and the tool catalog at once".
     - Use "governed knowledge artifact" throughout and drop "products".
   - *Related:* map §2 Ch 05.

4. **C05-R04 — Medium — Move / Add.**
   - *Location:* `:386` (§ How enterprise knowledge becomes usable) and `:451–459` (§ Turn policy prose into logic the system can enforce).
   - *Issue:* the pipeline is previewed early with a different step list; owner approval is missing from Extract/Prove/Project.
   - *Why:* A (extract) → C (enforce) is missing B, the accountable human sign-off that makes a rule the organization's rule.
   - *Change:*
     - Move the `:386` paragraph to directly after `:447` as the worked example (it ties to Harborlight's pay-statement evidence).
     - After **Prove**, add one bold step: "**Approve.** An eligible owner accepts the interpretation; the approval, the source digest, and the rule version are recorded together. Verification shows the rule matches the text; approval makes it the organization's rule."
     - Keep `:388` as the lead-in to § How enterprise knowledge becomes usable.
   - *Related:* C05-R01.

5. **C05-R05 — Medium — Move / Add.**
   - *Location:* § Reference architecture: the Enterprise Knowledge Hub (`:524–541`).
   - *Issue:* the synthesis comes after "start", and it is not mapped to the modes or representations.
   - *Why:* the Hub is how the reader integrates the chapter's three taxonomies.
   - *Change:*
     - Move the whole H2 to after § Why provenance determines what you can trust.
     - Add a column "Serves mode / built from": Governance → all modes / § provenance; Semantic → Context / § Semantic knowledge; Structural → Reasoning / § Ontology, § Business data catalog; Normative → Constraints / § Business rules, DMN, SBVR; Procedural → Reasoning / BPMN, CMMN; Capability → Action / § Capability and API catalog.
     - In the PRODUCTION CONSIDERATION, add "(the RunManifest's `knowledge_snapshots`, Chapter 4)".
   - *Related:* C05-R09.

6. **C05-R06 — Medium — Rewrite.**
   - *Location:* `:430` (§ Capability and API catalog).
   - *Issue:* "the same artifact" leaves two writers of capability metadata.
   - *Why:* it violates Ch 04's one-writer rule at the first application.
   - *Change:* replace the last sentence with: "The catalog does not own these entries; it indexes the Skill manifests of Chapter 8 and the ToolManifests of Chapter 22 for discovery, and every invocation still resolves against those registries."

7. **C05-R07 — Medium — Rewrite.**
   - *Location:* `:392` (§ Semantic knowledge).
   - *Issue:* it promises that Ch 06 teaches chunking and reranking, which Ch 06 does not.
   - *Change:* "Chapter 6 owns how retrieved evidence enters a model call—authorization order, ranking, token allocation, and the ContextManifest." Do not add chunking to Ch 06; the book assumes RAG basics.

8. **C05-R08 — Medium — Move.**
   - *Location:* into § Why provenance determines what you can trust (after `:505`), from Ch 06 `:760` and `:769`.
   - *Issue:* how knowledge stays current (a Part II promise, `:5`) is taught in Ch 06's scale bullets.
   - *Why:* freshness belongs with provenance and supersession.
   - *Change:* add a short paragraph built from those two bullets: the source revision is authoritative and index entries are disposable projections carrying source revision, ACL pointer, ingestion time, and deletion state; ingestion runs as separate extract, classify, ACL, chunk, embed, and index stages with independent cursors, so a failed embedding never blocks an ACL deletion. Ch 06 deletes both bullets (C06-R10) and keeps deletion propagation through memory, summaries, and caches.
   - *Related:* C06-R10.

9. **C05-R09 — Low — Cross-reference.**
   - *Location:* `:549`, `:562`.
   - *Change:* "run manifest" → "RunManifest (Chapter 4)".

10. **C05-R10 — Low — Add.**
    - *Location:* `:500` (Provenance row) or `:505`.
    - *Change:* one clause: "content provenance (where a statement came from), distinct from the build provenance of released artifacts in Chapter 27".

11. **C05-R11 — Low — Rewrite.**
    - *Location:* `:551` (§ If this fails in production).
    - *Change:* "Does the catalog carry each capability's effect semantics and risk class (Chapter 22), and is discovery filtered on them?"

12. **C05-R12 — Low — Rewrite.**
    - *Location:* `:556–563`, `:574`.
    - *Change:* align with the book-wide template: ✓ items, and a "Strong answer" header. Alternatively, adopt "What a good answer demonstrates" book-wide; that is the synthesizer's decision.

13. **C05-R13 — Low — Add.**
    - *Location:* `:354` (first paragraph of § Why retrieval alone is not a knowledge strategy).
    - *Change:* open with: "Chapter 4 gave knowledge, context, and memory one plane; this chapter fills its knowledge half." Use the plane name from C04-R01.

14. **C05-R14 — Low — Cross-reference.**
    - *Location:* `:422` (§ Business data catalog).
    - *Change:* append "—the class Chapter 6's context pipeline uses to redact before a prompt is built."

15. **C05-R15 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** `02-part-ii.md:430` (§ Capability and API catalog).
   - **Issue:** C08-R04 asks Ch 05 to keep its discovery-filter sentence and point to Ch 08; no Ch 05 item did.
   - **Change:** Keep "a capability the caller may not invoke should never appear" and append "(Chapter 8 § Discovery is not permission; AP-12)". Apply with C05-R06, which rewrites the last sentence of the same paragraph.
   - **Related:** C08-R04, C05-R06.

16. **C05-R16 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** End of § If this fails in production.
   - **Issue:** The Ch 17 review asks home chapters to add one anti-pattern pointer to their If-fails lists (C17-R03 mapping).
   - **Change:** Add one line: "If the vector index is being treated as the source of truth, the repair is structural; see AP-09 in Chapter 17." Do not replace the list.
   - **Related:** C17-R03.
