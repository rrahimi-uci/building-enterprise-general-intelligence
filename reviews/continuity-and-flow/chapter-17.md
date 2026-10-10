# Chapter 17 — Architecture Patterns That Fail in Production: Continuity and Flow Review

Reviewed: `source/parts/04-part-iv.md:1499–1873`. Context read: Ch 16 close (`:1495–1497`), Ch 18 opening (`05-part-v.md:1–83`), Part IV intro (`:1–7`), Appendix A and B (`09-appendices.md:8–60`), Ch 01 § Anti-pattern — the autonomous monolith (`01-part-i.md:458–478`), Ch 06 § Memory is not a bag of embeddings (`02-part-ii.md:663`), Ch 22 § A reliable protocol… (`06-part-vi.md:665–688`), every chapter's § If this fails in production (all 28, compared side by side), diagram sources `anti-*.gv`, `config/chapter-covers.json` entries for Ch 17.

## Overall Assessment

This is the best-written diagnostic material in the book. Every card starts from a legitimate goal ("no card here describes carelessness"). Each names the mechanism of failure, gives a concrete symptom, a replacement, a migration path, and repair metrics, and states its cost honestly. The thesis line, "a probabilistic component was handed a job that belongs to deterministic infrastructure" (`:1513`), unifies the catalog. Grouping by violated boundary is the right organizing choice.

**Placement decision: keep Ch 17 where it is, and make the forward dependencies explicit.** Evidence:

- **7 of 16 cards are fully grounded by Ch 01–15:** AP-01 (Ch 01/03/15), AP-02 (Ch 06/15), AP-06 (Ch 14), AP-07 (Ch 02/13), AP-09 (Ch 05), AP-10 (Ch 13), AP-13 (Ch 06).
- **3 are previewed well enough to read:** AP-04 (Ch 03 § One retry owner), AP-05 (Ch 01 Wednesday, Ch 03, Ch 15 rule `:1237`), AP-11 (Ch 10 budgets).
- **6 correct with mechanisms built later:** AP-03 (Ch 21), AP-08 (Ch 18), AP-12 (Ch 19/22), AP-14 (Ch 24), AP-15 (Ch 25/27), AP-16 (Ch 27).
  - The map is internally inconsistent here. §2 says six, and §9 S2 says "ten of the sixteen". My count agrees with six, plus three partials.
- Anti-patterns are **problem statements**. Meeting a failure shape before its fix is sound teaching; Ch 01's Monday–Friday narrative does the same. By contrast, Ch 16's P-cards are *solution* summaries, and those do not survive being read early (see chapter-16.md).
- The book already treats Ch 17 as the catalog that home chapters point to: Ch 01 (`01-part-i.md:477–478`, "Chapter 17 catalogs this failure as AP-01") and Ch 06 (`02-part-ii.md:663`, AP-13 and AP-02). Moving Ch 17 would renumber those references and 11 chapters for little gain.

What the chapter lacks is the signposting that makes the six forward cards honest previews. No card says where its correction is built, or which earlier chapter already prevents it.

Secondary problems:

- **Opening and labels.** There are two framing H2s that repeat each other. "The trade-off field" (`:1544`) names a field that the card structure does not have. The prioritization advice is split between `:1544` and a closing COMMON PITFALL.
- **Group heading.** "Approval, acceptance and governance" contains no governance card.
- **Code.** AP-05's correction treats a null lookup as "genuinely absent; now safe to retry", which contradicts Ch 22 and Appendix B (they also classify *executing* and *unprovable*). AP-06's correction uses the proposal digest as the idempotency key, which conflates Ch 22's logical effect key with the intent hash.
- **Examples.** AP-06's prose example (a $10,000 payment) and its code (underwriting evidence package) disagree. AP-03 mixes a "support agent" with "the onboarding task". AP-14 and AP-15 both use model swaps back to back.
- **Terminology drift:** "capability lease" (Figure 17-2, §6 T6), "risk tier" (AP-12, §6 T11), AP-07's terminal list (§6 T12), and unlabeled "onboarding" (§6 T17).

## Intended Reader Mental Model

After Ch 17 the reader should hold:

- **What.** Sixteen recurring failure shapes, each a responsibility boundary given to the wrong component, recognizable by a first symptom.
- **Why.** Fixing the symptom (a prompt, a retry, a classifier) leaves the boundary intact, so the failure returns under another name.
- **How.** Symptom → card → violated boundary → replacement → migration path → metric that proves the repair.
- **When.** Correct in order of effect blast radius. AP-04, AP-05, and AP-06 come first. Do not apply all sixteen to a read-only assistant.
- **Trade-offs.** Every correction costs latency, flexibility, or engineering time.
- **Relationships.** Each card is either already prevented by a chapter the reader has read, or is the problem statement for a chapter in Parts V–VIII. Each chapter's "If this fails in production" gives the runtime triage steps; the card gives the structural repair.

The chapter delivers the first five. The relationship layer is missing.

## Section-by-Section Flow Review

**§ Why failure patterns are easier to recognize than design rules (`:1501`).** Role: framing ("failures rarely arrive wearing the name of an anti-pattern"). Fine on its own.

**§ Start with the first visible symptom (`:1509`).** Role: second framing H2.
- `:1511` repeats `:1503–1505` almost item for item: duplicate email or write, an unowned case, missing evidence, a run that cannot be resumed or reconstructed.
- `:1513` holds the thesis and is the chapter's key paragraph.
- Figure 17-1 (`:1515`) is the monolith-versus-governed before/after. It is placed in the framing, not next to AP-01, which it illustrates.
- `:1517` explains the grouping and announces "the same four parts", which § How to read a card then explains.

Verdict: merge with the previous H2.

**### Find the failure by its first symptom (`:1519`).** Role: the symptom lookup table (ID, name, first symptom, violated boundary). It is the most useful desk aid in Part IV. *Issues:* rows follow group order, so the IDs read out of sequence (AP-01, AP-11, AP-02…) and the reason is never stated. It is one of three symptom tables in the book (Ch 05 If-fails, this one, Appendix B). The columns differ, though: this table diagnoses, while Appendix B prescribes a response.

**### How to read a card (`:1540`).** Role: explains the four labeled parts. Good.
- *Issue:* `:1544` refers to "the trade-off field", but cost lives inside **How to know the repair worked** ("The price of the safer design is clear"). It is not a separate field.
- *Issue:* "Correct in order of the blast radius" is the right guidance. The concrete priority list (AP-04, AP-05, AP-06 first) is held back to the closing COMMON PITFALL (`:1869`), after all sixteen cards.

**§ Reasoning and control flow (`:1546`).** The group intro (`:1548`) ("the model is allowed to decide when to stop") is precise and fits both cards.

**### AP-01 — Autonomous monolith (`:1550`).**
- Fully grounded (Ch 01 § Anti-pattern — the autonomous monolith; Ch 03; Ch 15).
- Reinforcement, not redundancy: the card adds the migration path and metrics, and Ch 01 forward-references it.
- Its example (a duplicate document request after a deploy) is the same incident as Ch 01 Monday and AP-05's. That is acceptable, because the cause differs (no durable record vs timeout).
- Figure 17-1 belongs here.

**### AP-11 — Unbounded loops and recursive delegation (`:1560`).**
- Previewed by Ch 10 (external budgets). The correction (monotonic budgets, acyclic ownership) is Ch 18's and Ch 28's subject. Ch 18 `05-part-v.md:47` restates it ("caps depth, children… across the entire task tree").
- Code: fine as illustration. Its `parent.reserve` foreshadows Ch 28's BudgetReservation and Ch 12's.
- The 5⁵ = 3,125 arithmetic is correct.
- No forward pointer.

**§ Context, knowledge and memory (`:1591`).** The group intro ("a convenient representation is mistaken for an authoritative one") is excellent.

**### AP-02 — Prompt as database (`:1595`).**
- Grounded (Ch 06, Ch 15). Ch 06 `02-part-ii.md:663` points here.
- The code uses `ContextManifest.project(...)`, a fourth ContextManifest surface alongside Ch 06's three shapes (map §7.3). It is acceptable as illustration once Ch 06 unifies the schema.
- The example (contract renewal) is off-thread but shows transfer, which is consistent with `:1542`.

**### AP-09 — Vector store as source of truth (`:1624`).** Grounded (Ch 05 § Why similarity cannot tell you what to trust). Reinforcement. The example ("superseded spending limit") could be Harborlight's superseded underwriting policy, but that is optional.

**### AP-13 — Memory write by default (`:1634`).** Grounded (Ch 06). The example is on-thread (a malicious mortgage document's bank account), and it is the fifth telling of the injected-document scenario (map §7.3). Here it adds a new facet (persistence), so it is reinforcement.

**§ Security and delegated authority (`:1665`).** The intro ("*can* versus *may*") is excellent.
- Figure 17-2's caption (`:1669`) says "capability lease". The book's canonical terms are capability envelope for scope and credential lease for proof (§6 T6; Ch 21 Q `06-part-vi.md:625`).

**### AP-03 — Ambient authority (`:1671`).**
- The correction depends on Ch 21 (subject plus workload identity, envelope by intersection, audience-bound lease). It is jargon-dense at this point, and there is no forward pointer.
- The example mixes domains: "The support agent's token… Nothing in the onboarding task requires it". Two unrelated scenarios sit in two sentences, and "onboarding" is the unlabeled supplier thread (§6 T17).

**### AP-10 — LLM judge as security gate (`:1681`).** Grounded (Ch 13: "a model score… is not permission", `:666`). Ch 20 elaborates. Reinforcement.

**### AP-12 — Ungated tool discovery and catalog dumping (`:1691`).**
- Discovery ≠ permission is grounded in Ch 08. The MCP catalog and the "approved tool slice bound to a lease" are Ch 19/21/22 material.
- "Risk tier" (`:1697`) should be "risk class" (tool eligibility uses R0–R4; §6 T11).

**§ Effects, retries and recovery (`:1701`).**
- The intro's parenthetical, "(the latter two are comparative examples)" (`:1703`), is awkward.
- The core line, "a failed call is not a failed effect, and an unacknowledged call is not an absent one", is excellent.

**### AP-04 — Retry everywhere (`:1707`).**
- Previewed by Ch 03 § One retry owner. Ch 22 is canonical.
- The 3 × 3 × 2 math is correct, and the code is a clear contrast.
- No pointer to Ch 22.

**### AP-05 — Timeout means failure (`:1737`).** Previewed (Ch 01, 03, 15). Ch 22 is canonical.
- *Code defect.* The correction's final branch says `return effect.resolve(committed=None)  # genuinely absent; now safe to retry` (`:1763`).
- A null lookup can also mean that the request is still executing or not yet visible. Ch 22 (`06-part-vi.md:681`) resolves to "committed, declined, partial, or intervention-required" only after reconciliation *establishes* the result. Appendix B (`09-appendices.md:57`) classifies "committed, absent, partial, executing, or unprovable".
- The card therefore teaches a weaker rule than the chapter that owns it.

**§ Approval, acceptance and governance (`:1768`).**
- The heading names governance, but both cards concern approval and acceptance. Governance-adjacent cards (AP-15, AP-16) sit under § Platform, release and operations.
- The intro (`:1770`), "make the decision an artifact: something with a hash, an owner, an expiry, and an independent check", is excellent.

**### AP-06 — Boolean or conversational approval (`:1774`).** Grounded (Ch 14). Figure 17-4 vs Figure 14-1 is reinforcement (anti-pattern vs pattern).
- *Example/code mismatch.* The prose uses a $10,000 → $100,000 payment, while the code uses `underwriting.submit_evidence_package`.
- *Code issues:*
  - `idempotency_key=proposal.digest()` (`:1803`) makes the idempotency key change whenever any argument changes. Ch 22 `06-part-vi.md:669` separates the logical effect key (business intent) from the intent hash.
  - The code checks hash and expiry but not policy or resource version, although the prose says "Revalidate immediately before commit" (`:1780`).
- **How to replace it** duplicates Ch 14 § Approval contract in miniature. That is acceptable as card reinforcement.

**### AP-07 — Model says done (`:1809`).**
- Grounded (Ch 02 § Deterministic acceptance; Ch 13).
- The terminal list "accepted, blocked, needs-input, failed, or unknown-effect" (`:1815`) is one of seven terminal vocabularies (§6 T12). These are acceptance outcomes, not run states, and the card does not say so.
- The example "Onboarding reports complete while the sanctions screening is stale" is the unlabeled supplier thread.

**§ Multi-agent collaboration (`:1819`) / ### AP-08 — Multi-agent chat as workflow (`:1821`).**
- No group intro; the other single-card groups also lack one, which is acceptable.
- The correction is Ch 18's entire thesis (TaskEnvelope, one owner, deterministic join). Ch 18's case box (`05-part-v.md:15`) repeats "a plausible multi-agent conversation is not a coordination protocol" without referring back.
- The example (finance and legal) could use Ch 18's Harborlight specialists (income verification and policy), which would set up Ch 18 directly.

**§ Observability and evidence (`:1831`) / ### AP-14 — Telemetry without causal or effect lineage (`:1833`).**
- The correction is Ch 24's ("one causal run graph"). No pointer.
- The example is a model swap that lowers latency while completion falls. That overlaps AP-15's model-swap example (`:1851`), Ch 01 Friday, and Ch 27's walkthrough (map §7.3, "cheaper model silently regresses").

**§ Platform, release and operations (`:1843`).** The intro ("unversioned speed is" the problem) is good.

**### AP-15 — Model or provider swap as configuration (`:1847`).** The correction (ChangeBundle, slice evaluation, canary, rollback target) is Ch 25/27 material, and "ChangeBundle" is undefined here. The slice example is strong.

**### AP-16 — In-place change and test after release (`:1857`).** The correction (ReleaseManifest, signed promotion, canary, verified rollback) is Ch 27's. "If the emergency path is slower than the console, the console wins" is a memorable line.

**COMMON PITFALL (`:1867–1869`).** "Audit AP-04, AP-05, AP-06 first." This is valuable prioritization, but it arrives after the reader has finished the cards. It belongs with `:1544`'s "correct in order of the blast radius".

**§ Where this leads next (`:1871`).** "After removing unsafe local architectures, Chapter 18 considers when multiple agents add justified specialization rather than accidental complexity." "Local architectures" mis-describes a catalog that includes release and operations. The sentence also misses the actual hinge: AP-08 and AP-11 are exactly the problems Ch 18 solves.

**Absent template sections.** There is no If-fails, verify, exercises, or design-review section. That is appropriate for a catalog chapter, and none should be added.

## Sparse or Underdeveloped Content

None in the sense of missing explanation. The cards are the right depth. The one gap is **relational**: each card needs a one-line "Prevented in / Built in" tag (C17-R03). That turns the six forward cards into signposted previews and the ten grounded cards into recall that sends the reader back to the right chapter.

## Missing Conceptual Connections

- **Home chapter → card → (missing: "where this correction is built") → reader.** This is needed for all 16 cards. Mapping:
  - AP-01: Ch 01, 03, 15
  - AP-11: Ch 10; built in Ch 18, 28
  - AP-02: Ch 06, 15
  - AP-09: Ch 05
  - AP-13: Ch 06
  - AP-03: built in Ch 21
  - AP-10: Ch 13; Ch 20
  - AP-12: Ch 08; built in Ch 19, 22
  - AP-04: Ch 03; built in Ch 22
  - AP-05: Ch 15; built in Ch 22
  - AP-06: Ch 14
  - AP-07: Ch 02, 13, 15
  - AP-08: built in Ch 18
  - AP-14: built in Ch 24
  - AP-15: built in Ch 25, 27
  - AP-16: built in Ch 27
- **Each chapter's § If this fails in production → (missing: "if the cause is structural, see AP-xx") → Ch 17.** These are complementary layers, verified across all 28 If-fails sections: they are runtime triage steps ("recompute the proposal hash", "replay history with the pinned build"), while the cards are structural diagnoses. **I disagree with map §9 S2**, which proposes replacing the per-chapter lists with AP pointers. The lists carry procedure the cards do not. Add a pointer line instead. For my chapters, see C14-R14 and C15-R12. Other chapters' owners add theirs: Ch 05 → AP-09, Ch 06 → AP-02/AP-13, Ch 10 → AP-11, Ch 13 → AP-10/AP-07, Ch 18 → AP-08/AP-11, Ch 21 → AP-03, Ch 22 → AP-04/AP-05, Ch 24 → AP-14, Ch 27 → AP-15/AP-16.
- **Ch 17 AP-08/AP-11 → (missing: "Chapter 18 builds the replacement") → Ch 18 opening.** Two-sided: Ch 17's closing (C17-R10), and one back-reference clause in Ch 18's § Why more agents do not automatically make a better system (owner: Ch 18).
- **Later chapters (Ch 19, 21, 22, 24, 25, 27) → (missing: "Chapter 17 named this failure as AP-xx") → back-reference.** One clause each, owned by those chapters, at most once per chapter. This mirrors the existing Ch 01/Ch 06 forward references and closes the loop.

## Transition Problems

- **In (Ch 16 → 17, `:1497`).** Adequate. See C16-R09 for the revised wording that sets up the forward tags.
- **Within.**
  - The two framing H2s repeat each other (`:1503` / `:1511`).
  - Figure 17-1 is separated from AP-01 by the symptom table and the reading guide.
  - The priority advice is split between `:1544` and `:1869`.
  - The groups for Multi-agent and Observability have no intro sentence. That is acceptable, and none is needed.
- **Out (Ch 17 → 18, `:1873`).** It mis-describes the catalog as "local architectures" and misses the AP-08/AP-11 hinge (C17-R10). On the Ch 18 side, its case box and § Treat collaboration as durable work restate AP-08 and AP-11 without acknowledging them (owner: Ch 18; one clause).

## Redundant and Repetitive Concepts

| Concept | Occurrences | Verdict |
| --- | --- | --- |
| "Incidents arrive as symptoms, not labels" | `:1503–1507`, `:1511` | Redundant. Merge. |
| "Each card has the same parts" | `:1517`, `:1542` | `:1517`'s last sentence is redundant with § How to read a card. |
| Correct by blast radius / AP-04-05-06 first | `:1544`, `:1869` | Split guidance. Co-locate it. |
| Model-swap example | AP-14 `:1837`, AP-15 `:1851` | Overlapping. Change AP-14's example. |
| Stock phrases ("The replacement is explicit:", "The migration path is clear:", "The price of the safer design is clear:") | ×16 each | Templated. The field labels already say what follows. |

## Cross-Chapter Duplication

| Card | Overlapping chapter sections | Verdict |
| --- | --- | --- |
| AP-01 | Ch 01 § Anti-pattern — the autonomous monolith (`01-part-i.md:458–478`); Figure 17-1 | Reinforcement (Ch 01 forward-references it). |
| AP-02 | Ch 06 § Four kinds of state…; Ch 15 § Durable state is more than chat history; Ch 15 COMMON PITFALL | Reinforcement. The Ch 15 box is removed (C15-R02). |
| AP-09 | Ch 05 § Why similarity cannot tell you what to trust | Reinforcement. |
| AP-13 | Ch 06 § Memory is not a bag of embeddings; Ch 20 T-06 | Reinforcement. |
| AP-03 | Ch 21 § Three identities…, § Records worth preserving; Figure 21-1; Figure 18-1 | Preview. Three narrowing figures (map §7.1) is acceptable, since they show problem, delegation tree, and identity. |
| AP-10 | Ch 13 § Give evaluation its own independent path; Ch 20 § Guardrails help… | Reinforcement. |
| AP-12 | Ch 08 § Discovery is not permission; Ch 19 § Registry model; Ch 20 T-13; Ch 22 Discovery Service | Preview plus reinforcement. |
| AP-04 | Ch 03 § One retry owner; Ch 22 § The mechanics that make retries safe | Reinforcement (adds the multiplication argument). Ch 03's full table is the redundant one (owner: Ch 03, per map S5). |
| AP-05 | Ch 01 Wednesday; Ch 03 § One retry owner; Ch 15 rule `:1237`; Ch 22 § A reliable protocol…; Appendix B runbook | Reinforcement, but the code contradicts Ch 22 and Appendix B (C17-R05). |
| AP-06 | Ch 03 § Bind approval to the exact proposal; Ch 14 § Approval contract and code; Figure 14-1 | Reinforcement. Ch 14 is canonical. Code fixes in C17-R06. |
| AP-07 | Ch 02 § Deterministic acceptance; Ch 13; Ch 15 § Terminal correctness; Ch 18 rule "Termination" | Reinforcement. The terminal list must align (C17-R07). |
| AP-08, AP-11 | Ch 18 case box, § Treat collaboration as durable work, § Recommended orchestration rules; Ch 28 budgets | Preview. Ch 18 should acknowledge it (owner: Ch 18). |
| AP-14 | Ch 24 § A useful trace tells the story of the run; Ch 01 Friday | Preview. |
| AP-15 | Ch 07 Q (`03-part-iii.md:171`); Ch 27 § Treat the full behavior as the release; Ch 01 Friday; Ch 03 § Framework upgrades… | Preview plus reinforcement. The near-duplicate design-review question across Ch 07 and Ch 27 is their owners' to resolve. |
| AP-16 | Ch 27 § Rollback and active runs, § Versioned objects | Preview. |
| § Find the failure by its first symptom | Appendix B (`09-appendices.md:39–50`); Ch 05 If-fails table | Different columns (diagnose vs respond). Recommend the Appendix B owner add an "Anti-pattern" column with AP IDs per row (e.g. "Duplicate business write" → AP-04/AP-05; "Run stuck after approval" → AP-06; "Repeated tool loop" → AP-11) rather than merging the tables. Owner: Appendix B. |

## Structural Recommendations

1. **Keep Ch 17 in place.** Add a **Prevented in / Built in** line to every card (C17-R03), and say in the opening that six cards preview Parts V–VIII.
2. Merge the two framing H2s. Move Figure 17-1 into AP-01. Put the priority guidance in § How to read a card (C17-R01, C17-R02, C17-R09).
3. Rename the § Approval, acceptance and governance group to § Approval and acceptance (C17-R08).
4. Keep the AP IDs as they are. They are referenced by Appendix A, Ch 01, Ch 06, three diagram sources, `config/diagrams.json`, and `config/chapter-covers.json`. State once that IDs are stable identifiers and cards are ordered by boundary (C17-R02).
5. Leave the inline anti-pattern/correction code in place for this pass, but fix the two defects (C17-R05, C17-R06). The `AGENTS.md` rule ("never write code directly into `source/parts/`") applies to these six blocks. Converting them to `examples/` entries with behavioural tests is a separate, book-wide decision for the synthesizer, and should not be bundled with this chapter's flow edits.

## Concrete Recommended Changes

1. **C17-R01 · Medium · Merge.**
   - **Location:** `04-part-iv.md:1501–1517`, § Why failure patterns are easier to recognize than design rules and § Start with the first visible symptom.
   - **Issue:** Double framing. `:1511` repeats `:1503–1507`.
   - **Change:**
     - Keep the `:1501` heading.
     - Body: `:1503–1507`, then `:1513` (the thesis), then `:1517`'s first sentence (grouping by boundary). End with one new sentence: "Seven cards describe failures the earlier chapters already prevent; three were previewed; six are corrected by mechanisms Parts V–VIII build, and each card says where."
     - Delete the `:1509` heading, `:1511`, and `:1517`'s second sentence.
     - Move Figure 17-1 (`:1515`) to directly after the AP-01 heading (`:1550`).

2. **C17-R02 · Medium · Rewrite.**
   - **Location:** ### How to read a card (`:1540–1544`).
   - **Issue:** "Trade-off field" names a non-existent field. The priority advice is split from the closing box. The out-of-order IDs are unexplained.
   - **Change:**
     - In `:1542`, add the fifth element: "**Prevented in / Built in** names the chapter that already prevents the failure or the later chapter that builds its replacement."
     - In `:1544`, change "The trade-off field matters" to "The cost sentence that closes each card matters". After "Correct in order of the blast radius of the effects involved", append the COMMON PITFALL's content: "Start with AP-04, AP-05, and AP-06: they produce duplicate payments, duplicate records, and unauthorized effects while looking like ordinary diligence."
     - Add: "IDs are stable identifiers; cards are ordered by the boundary they violate."
     - Delete the COMMON PITFALL box (`:1867–1869`).

3. **C17-R03 · High · Add (one line per card).**
   - **Location:** the end of each of the 16 cards, after **How to know the repair worked**: AP-01 `:1558`, AP-11 `:1589`, AP-02 `:1622`, AP-09 `:1632`, AP-13 `:1663`, AP-03 `:1679`, AP-10 `:1689`, AP-12 `:1699`, AP-04 `:1735`, AP-05 `:1766`, AP-06 `:1807`, AP-07 `:1817`, AP-08 `:1829`, AP-14 `:1841`, AP-15 `:1855`, AP-16 `:1865`.
   - **Issue:** Six cards depend on Parts V–VIII and nothing says so. Ten cards could send the reader back to their prevention chapter.
   - **Why it matters:** This converts the chapter into an honest hinge, recall for Ch 01–15 and a preview for Ch 18–28, without moving it.
   - **Change:** Add `**Prevented in / Built in.**` followed by the mapping:
     - AP-01: Prevented in Chapters 1, 3, and 15.
     - AP-11: Prevented in Chapter 10; built in Chapters 18 and 28.
     - AP-02: Chapters 6 and 15.
     - AP-09: Chapter 5.
     - AP-13: Chapter 6.
     - AP-03: Built in Chapter 21.
     - AP-10: Chapter 13; Chapter 20.
     - AP-12: Chapter 8; built in Chapters 19 and 22.
     - AP-04: Chapter 3; built in Chapter 22.
     - AP-05: Chapter 15; built in Chapter 22.
     - AP-06: Chapter 14.
     - AP-07: Chapters 2, 13, and 15.
     - AP-08: Built in Chapter 18.
     - AP-14: Built in Chapter 24.
     - AP-15: Built in Chapters 25 and 27.
     - AP-16: Built in Chapter 27.
   - **Related:** C16-R04(a) uses the same chapter mapping for P-cards. Keep the two consistent.

4. **C17-R04 · Medium · Rewrite (stock phrasing).**
   - **Location:** all 16 cards.
   - **Change:**
     - Delete "The replacement is explicit:" and start **How to replace it** with the replacement itself.
     - Replace "The migration path is clear:" with "Migrate in steps:".
     - Replace "The price of the safer design is clear:" with "The cost:".
   - Do not otherwise alter the card prose.

5. **C17-R05 · High · Rewrite (code correctness).**
   - **Location:** AP-05 code block, `:1756–1764`.
   - **Issue:** A null lookup is treated as proof of absence and licenses an immediate retry. That contradicts Ch 22 `06-part-vi.md:681` and Appendix B `09-appendices.md:57`.
   - **Why it matters:** The card teaches a weaker rule than the canonical chapter on the most expensive failure in the catalog.
   - **Change:** Replace the last two lines with three:
     - `if actual is not None: return effect.resolve(committed=actual)` (it landed; adopt it)
     - `if downstream.confirms_absent(effect.key): return await retry_with_same_key(effect)` (authoritatively absent; retry with the *same* key)
     - `return effect.escalate(EffectState.INTERVENTION_REQUIRED)` (still executing or unprovable; do not guess)
   - Keep the comment style.
   - **Related:** Ch 22 owns the state names; use theirs.

6. **C17-R06 · Medium · Rewrite (example and code).**
   - **Location:** AP-06, `:1778` (example) and `:1791–1804` (code).
   - **Issue:** The prose (payment) and code (evidence package) disagree. `idempotency_key=proposal.digest()` conflates the intent hash with the logical effect key. No policy or version recheck despite `:1780`.
   - **Change:**
     - Example → "An authorization given to submit the evidence package for case version 3 is reused after the case moved to version 5 and the package gained a document nobody reviewed." This keeps it on Harborlight and matches the code.
     - In the code, pass `idempotency_key=effect.logical_key` and keep `proposal.digest()` only in the hash comparison.
     - Add one line before the call: `policy.recheck(proposal, expected_version=case.version)` with the comment "# current policy and resource state, immediately before commit".

7. **C17-R07 · Medium · Rewrite (terminology).**
   - **Location:** AP-07 **How to replace it** (`:1815`).
   - **Issue:** The outcome list is one of seven terminal vocabularies (§6 T12) and is not identified as acceptance outcomes.
   - **Change:** **Reconciled (see overall-book-review.md §D-12):** Use: "An independent, executable acceptance check over authoritative state returns an AcceptanceDecision—accepted, rejected with typed defects, or escalated (Chapter 13); only an accepted decision lets the run reach Succeeded (Chapter 15). While an effect is Unknown or required input is missing, acceptance is not attempted." Original text, superseded: "An independent, executable acceptance check over authoritative state returns an acceptance decision (accepted, blocked, needs input, failed, or unknown effect); only an accepted decision lets the run reach Succeeded (Chapter 15)."
   - **Related:** C15-R04 (the canonical run-state table).

8. **C17-R08 · Low · Rewrite.**
   - **Location:** the § Approval, acceptance and governance heading (`:1768`).
   - **Change:** Rename to `## Approval and acceptance`. Update any generated TOC.

9. **C17-R09 · Low · Rewrite (terminology).**
   - **Location and change:**
     - Figure 17-2 caption (`:1669`) and `config/diagrams.json` description for `anti-ambient-authority`: change "a narrowed, short-lived capability lease" to "a narrowed capability envelope and a short-lived credential lease". Check the label inside `anti-ambient-authority.gv` and run `make diagrams`.
     - AP-03 (`:1677`): "Broad token becomes policy → scoped lease" → "policy → capability envelope → credential lease".
     - AP-12 (`:1697`): "risk tier" → "risk class".
     - AP-15 (`:1853`): the first use of "ChangeBundle" gets "(the versioned change proposal that Chapter 25 evaluates and Chapter 27 promotes)".

10. **C17-R10 · Medium · Rewrite.**
    - **Location:** § Where this leads next (`:1873`).
    - **Issue:** "Local architectures" is inaccurate, and the AP-08/AP-11 hinge is missing.
    - **Change:** "Several of these failures are corrected by mechanisms the rest of the book builds. Chapter 18 starts with AP-08 and AP-11: how specialists can share work with one owner per task, narrowed authority, explicit joins, and a bounded task tree."
    - **Related:** Ch 18 owner adds one clause to § Why more agents do not automatically make a better system (`05-part-v.md:21–28`): "Chapter 17 named the failures (AP-08, AP-11); this chapter builds the protocol."

11. **C17-R11 · Low · Rewrite (examples).**
    - **Locations and changes:** **Reconciled (see overall-book-review.md §D-21):** The supplier thread is retired, so no "(supplier onboarding)" labels: AP-03 uses the Harborlight text below, and AP-07 becomes "The evidence review reports complete while the second pay statement's verification is stale." The AP-14, AP-08, and AP-04 items stand.
      - AP-03 (`:1675`): "The mortgage evidence agent runs under a service account that can export every applicant record; the evidence-review task needs one case. The account was reused because it already existed."
      - AP-14 (`:1837`): replace the model-swap example, which duplicates AP-15, with "A retrieval cache raises its hit rate and cuts latency, while stale-evidence rejections at acceptance double. Both facts are true and neither dashboard contains both."
      - AP-07 (`:1813`) and AP-03 (if not rewritten): label "(supplier onboarding)", or move to Harborlight per the §9 S13 decision.
      - AP-08 (`:1825`), optional: "The income-verification and policy specialists each wait for the other's artifact…", which sets up Ch 18's case.
      - AP-04 group intro (`:1703`): drop "(the latter two are comparative examples)".

12. **C17-R12 · Low · Cross-reference (owner: Appendix B).**
    - **Location:** `09-appendices.md:39–50`.
    - **Change:** Add an "Anti-pattern" column so each runbook row names its card. Do not merge the tables; they answer different questions.
