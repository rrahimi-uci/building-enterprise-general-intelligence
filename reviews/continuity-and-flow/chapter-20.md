# Chapter 20 — Security Starts Outside the Prompt: Continuity and Flow Review

Reviewed: `source/parts/06-part-vi.md:1–331` (Part VI orientation at `:1–14`, Chapter 20 at `:16–331`), plus the close of Ch 19 (`05-part-v.md:663–701`), the opening of Ch 21 (`06-part-vi.md:333–363`), and the cross-chapter passages cited below.

## Overall Assessment

Chapter 20 has the right core idea and states it well. A detector, a policy point, and an enforcement point are different things, and security comes from the enforcement points (`:32–45`). The injected-document worked example (`:236–256`) is the best demonstration of that idea in the book. The chapter's structure works against the idea, though:

- **The chapter's own vocabulary contradicts it.** "Policy and guardrail services own decisions" (`:58`, `:65`), "Defense-in-depth guardrails architecture" (Figure 20-1, `:71`), "Runtime guardrail…" (Figure 20-3, `:91`, which draws an Input Guardrail as the first gate that refuses), and the closing "The guardrail architecture establishes defense in depth" (`:331`). The section heading at `:28` says guardrails are not the boundary, and then the chapter names its architecture after them.
- **One layer model, three counts.** Figure 20-1 shows 6 layers, the table at `:73–83` has 9, and Ch 23 § Containment layers has 8. Ch 03's protection stack has 7 and the Part VI intro gives a fifth ordering.
- **The threat catalog is disconnected from the layer model.** The catalog intro promises that each card shows "where the first deterministic refusal should occur" (`:101–106`). No card names a refusal point or a layer. The cards are stock-phrased fragment lists (`:110–234`).
- **Ch 20 and Ch 23 split the security story badly.** Both assume a compromised model, both list layers, both catalog threats (T-cards here, an 11-row table in Ch 23), and both tell the injected-document story. A clean division is proposed in § Structural Recommendations, and chapter-23.md uses the same split.
- **The template is out of order.** The chapter has no case box and no design choice (it is the only Part VI chapter without them). Its core § Respond as if the model can be compromised comes after the evidence and code sections.

Verdict: keep the argument, fix the terminology, collapse to one layer model, tie the T-cards to that model, and give Ch 23 the containment mechanisms.

## Intended Reader Mental Model

After this chapter the reader should hold four things:

1. **Detector ≠ policy point ≠ enforcement point.** Detectors are probabilistic signals. Enforcement fails closed on the protected operation. The design question at each boundary is "what is the worst that happens if the control above this one is fooled?" (`:44–45`).
2. **One layer model.** Each layer has a control and an evidence record (`:73–83`). Trust is not inherited across the boundaries between layers (`:89`).
3. **Threats are paths, not checklists.** A threat enters at one layer and must be refused deterministically at a later one. The injected document is the worked path.
4. **Incident response starts from evidence, never from the model's account.** Detect → Contain → Revoke → Reconcile → Eradicate → Recover → Learn.

What the reader brings in: Ch 02 six gates, Ch 03 § Guardrails and authorization solve different problems (`01-part-i.md:1168`), Ch 04 § Trust boundaries (`02-part-ii.md:144`), Ch 06 § The trust hierarchy of instructions (`02-part-ii.md:641`), and Ch 19 gateways. The chapter cites none of them.

## Section-by-Section Flow Review

**Part VI orientation (`:1–14`, `# PART VI — SECURITY, IDENTITY, AND CONTROL`).**
- *Role:* frames the Part.
- *Adds:* "every control is tied to a boundary, a decision, a signal, and a recovery path", and "none can stand in for the others".
- *Issue 1:* it says "The order matters" and then gives authentication → authorization → guardrails → sandboxes → effect ledger (`:9–12`). That contradicts Ch 20's own request order at `:93` (input classification before authorization) and Figure 20-3 (guardrail before policy). It also does not match the chapter order (20 threats/detection, 21 identity, 22 effects, 23 containment).
- *Issue 2:* there is no one-line map of the four chapters, so the reader cannot see that Ch 20 and Ch 23 have different jobs.
- *Verdict:* rewrite (C20-R01).

**§ Why prompt defenses are not enough (`:20`).**
- *Role:* chapter intro.
- *Adds:* "a manipulated model may still be useful if the surrounding system limits…". This is the Part premise.
- *Verdict:* it duplicates the first paragraph of the next section (`:30`). Together the two form the double "why" opening that the map flags. Merge (C20-R03).

**§ Guardrails help, but they are not the security boundary (`:28`).**
- *Role:* the chapter's central mental model.
- *Adds:* the three-way split (`:32–37`), the worked contrast (`:39–45`), and the five-row control-question table (`:47–53`).
- *Verdict:* strong. This is the canonical home of "guardrail = detector", and the Ch 03 version is the preview. The control-question table is good and should stay here.

**§ Build security in layers (`:55`).**
- *Role:* the state-owner table.
- *Issue:* the H2 holds only one paragraph and a table, and the paragraph says "Policy and guardrail services own decisions" (`:58`), which contradicts `:32–37`. The heading also duplicates the next H2 ("How the layers reinforce one another").
- *Verdict:* fold the table into the next section, then fix the wording (C20-R02, C20-R03).

**§ How the layers reinforce one another (`:67`).**
- *Role:* the layer model.
- *Adds:* the 9-row Layer / Controls / Evidence table. This is the best layer list in the book because it has an evidence column.
- *Issues:*
  - Figure 20-1 shows 6 different layers ("Input inspection … Evidence and audit", per `assets/diagrams/src/security-depth.gv`) and is titled "guardrails architecture".
  - The opening paragraph (`:69`) is repeated almost word for word in design-review Q1 (`:323`).
- *Verdict:* make the 9-row table the book's only layer model and redraw the figure to match (C20-R04).

**§ Follow the request across each trust boundary (`:85`).**
- *Role:* trust boundaries and the request sequence.
- *Adds:* "Trust is not inherited through a chain" (`:89`), which is excellent, and the SECURITY AND GOVERNANCE box on indirect injection (`:97`).
- *Issues:*
  - Figure 20-2 shows 3–4 boundaries, but Ch 04 § Trust boundaries already has the 8-row table, and this chapter never cites it.
  - `:93` is an 11-clause run-on sentence: the book's fifth end-to-end flow, with a step order that does not match Ch 02's six gates.
  - Figure 20-3 makes the Input Guardrail refuse the request ("refuse, nothing dispatched"). That is the opposite of the chapter thesis.
- *Verdict:* cite Ch 04, cut `:93`, and fix Figure 20-3 (C20-R05, C20-R06).

**§ How attacks show up in practice (`:99`).**
- *Role:* the threat catalog.
- *Intro (`:101–106`):* "lenses over one runtime path" is the right framing. It promises "where the first deterministic refusal should occur", and the cards do not deliver that.
- *Verdict:* restructure the cards (C20-R07).

**§ T-01 — Direct prompt injection (`:108`) through § T-16 — Supply-chain attacks (`:228`), assessed as a group.**
- *Role:* 16 lookup cards.
- *Adds:* the breadth of known threat classes, cross-checked against OWASP (R15/R16).
- *Common issues:*
  - **Stock phrasing.** Every card uses "The business risk is…", "Look for…", "Reduce the likelihood with these measures:", "At runtime, use these controls:", and "If it happens, follow this recovery path:". The text after those colons is capitalized fragments (for example `:112`).
  - **No layer or refusal point**, so exercise 1 at `:316` ("trace it across the nine defense layers") has nothing to work from.
  - **Mixed controls.** "How to contain and recover" mixes runtime controls with post-incident recovery.
  - **Missing pointers.** T-01/T-02 do not point to Ch 06's instruction trust hierarchy, which is where instruction/data separation is built. T-09/T-15 do not point to Ch 21. T-07 does not point to Ch 22. T-12/T-13 do not point to Ch 19's A2A and MCP gateways. T-14 does not point to Ch 23.
  - T-12 says "Agent gateway" (lowercase). The map flags this as an orphan term (T4).
- *Card-specific notes:*
  - T-03 is reasonable.
  - T-04 and T-05 overlap: malicious context vs. poisoned corpus. They are distinct only by persistence, and the card text should say so in one clause.
  - T-10 and T-11 overlap the same way: exfiltration (active) vs. leakage (passive). This is acceptable if each card names the distinction.
- *Verdict:* keep the 16 H3s, since they serve as an index, but rewrite each into labeled fields with a layer line (C20-R07).

**§ Worked example — an injected mortgage document (`:236`).**
- *Role:* the canonical attack path.
- *Adds:* a five-step table (Ingest → Retrieve → Reason → Dispatch → Commit), each with the control that must hold and its evidence, plus the closing distinction "detection improves experience; containment preserves the property" (`:253–256`).
- *Verdict:* the chapter's best section. It should be the book's single full telling of this story (C20-R08).
- *Issues:* it uses "capability envelope" (Ch 21) and EgressGrant (Ch 23) without forward pointers.

**§ What the evidence lets us conclude (`:258`).**
- *Role:* citations.
- *Adds:* "enumerates known classes, not all classes". This is good, and it is the reason Ch 23's threats paragraph (`:1108`) is redundant.
- *Issue:* the incident lifecycle is uncited. R42 (NIST SP 800-61r3) is registered and is cited only in Ch 23's "draws on" sentence and Ch 27's evidence context.
- *Verdict:* add an incident row (C20-R10).

**§ A sensible place to start (`:266`).**
- *Role:* code. It holds only `[[EXAMPLE:input-guardrail]]`, an SDK input guardrail that blocks on string markers.
- *Issue:* in a chapter that argues detectors are not the boundary, the only runnable code is a detector, and no text frames it as one. The example docstring says the important property is "where it sits in the pipeline". A reader who skims will take away "add an input guardrail".
- *Verdict:* add one framing sentence (C20-R09).

**§ Respond as if the model can be compromised (`:270`).**
- *Role:* incident lifecycle.
- *Adds:* the seven phases plus the operator-question and required-record table. This is the book's only incident lifecycle, and it is good.
- *Issues:*
  - The heading restates the Part premise, which Ch 23 states three more times. The section is really about incident response.
  - It sits after the evidence and code sections, so the reader meets it as an afterthought.
  - The paragraph at `:286–290` repeats the table's Contain/Revoke/Reconcile rows. Its scope list ("tool, MCP server, model route, Skill, memory namespace, tenant, or agent") is repeated verbatim in the checklist (`:310`).
  - It uses "Narrow kill switch" (`:280`) without pointing to Ch 23.
- *Verdict:* rename, move earlier, and condense (C20-R10).

**Template sections: § If this fails in production (`:292`), § What to verify before production (`:300`), § Put the idea to work (`:314`), § Questions to bring to design review (`:319`).**
- *If this fails:* strong. Step 3 (detection failure vs. enforcement failure) is the chapter thesis applied to debugging. Step 1's boundary list matches the 9-layer table, which is good.
- *Verify:*
  - The fourth check (approval bound to the exact proposal, `:308`) belongs to Ch 14/22.
  - No check captures the thesis that no detector is the only control in front of a protected operation.
- *Put the idea to work:* exercise 1 depends on cards mapped to layers (C20-R07). Exercise 2 says "the guardrail is reading content" and should say "the eligibility decision".
- *Questions:*
  - Q3 "Why is discovery not authorization?" (`:325`) is a near-duplicate of Ch 08 (`03-part-iii.md:347`).
  - The detection-vs-enforcement distinction, the chapter's main idea, has no question.
  - Q1's answer repeats `:69`.
- *Verdict:* small edits (C20-R11).

**§ Where this leads next (`:329`).** "The guardrail architecture establishes defense in depth" contradicts `:28`. Rewrite (C20-R02).

## Sparse or Underdeveloped Content

- **The T-cards are dense but under-explained.** Each card is about 60 words of fragments. The fix is not more text but better structure (a layer line and a first-refusal line, C20-R07).
- **Eradicate and Recover (`:283–284`)** get a single table row each. That is enough for this chapter. Ch 27 owns restoring a known release, so a pointer there is sufficient. Do not expand.
- **The step from detection to policy is never shown.** The chapter says a detector "identifies" and a policy point "decides", but never says how a detector finding reaches the policy point, for example as a session-risk attribute or an obligation. One sentence would close this (C20-R03). Ch 21's ABAC "current risk" attribute (`:369`) is where it lands, so cross-reference it.

## Missing Conceptual Connections

1. **Detector/policy/enforcement (`:32`) → T-cards (`:108–234`), missing the layer each card is refused at.** The catalog intro promises it; exercise 1 needs it. Location: every T-card (C20-R07).
2. **Trust is not inherited (`:89`) → Figure 20-2, missing Ch 04 § Trust boundaries (`02-part-ii.md:144`).** The 8-row table already lists each boundary's untrusted inputs and mandatory controls. Ch 20 should cite it instead of drawing a reduced version without reference (C20-R05).
3. **T-01/T-02 and the worked example → Ch 06 § The trust hierarchy of instructions (`02-part-ii.md:641`).** The instruction/data separation these cards rely on is built in Ch 06. There is no pointer (C20-R07).
4. **T-12/T-13 → Ch 19 § Two protocols, two responsibilities (`05-part-v.md:416`).** The MCP and A2A gateways that "validate identity, authority…" are Ch 19's. There is no pointer (C20-R07).
5. **Detector finding → ABAC "current risk" (Ch 21 `:369`, `:381`), missing the statement that findings become policy inputs** (C20-R03).
6. **Incident Reconcile phase (`:282`) → Ch 22 reconciliation.** The phase depends on Ch 22's Unknown state and reconciler. Add a forward pointer (C20-R10).
7. **Incident Contain phase (`:280`) → Ch 23 § Scoped operational kill switch.** Add a forward pointer (C20-R10).
8. **Worked example → Ch 21 capability envelope and Ch 23 EgressGrant.** Both are used before they are defined, with no pointer (C20-R08).

## Transition Problems

- **Ch 19 → Part VI → Ch 20.** Ch 19 closes with "Chapter 20 introduces defense in depth across all agentic trust boundaries" (`05-part-v.md:701`), which is good. The Part intro then states a control order that the chapter does not follow, and gives no chapter map (C20-R01).
- **Opening.** There is only an evidence-context blockquote, with no case box and no design choice. Every other Part VI chapter has both. Ch 23's case box currently tells the injected-document story; under the proposed split, Ch 20 should open with it (C20-R08).
- **Within the chapter.** § Build security in layers → § How the layers reinforce one another are two H2s for one idea. § A sensible place to start → § Respond as if… returns to core content after the template sections.
- **Ch 20 → Ch 21.** The closing sentence mislabels the chapter as "the guardrail architecture". Ch 21's opening never refers back to Ch 20's policy point. Ch 21 should name its PDP as the "policy point" of Ch 20 (see C21-R04).

## Redundant and Repetitive Concepts

| Repeated idea | Locations in Ch 20 | Verdict |
| --- | --- | --- |
| "A manipulated model must still be limited" | `:22–24`, `:30`, `:253–256`, § Respond heading `:270` | `:22` and `:30` are redundant (merge). `:253` is the payoff (keep). Rename `:270`. |
| Six-source enumeration "untrusted language, privileged tools, dynamic context, durable memory, third-party protocols, autonomous timing" | `:69`, Q1 `:323` | Redundant. Keep in the body; shorten Q1's answer to point at the layers. |
| End-to-end request steps | `:93`; Figure 20-3; Ch 02 six gates | `:93` is redundant. Remove it. |
| Containment scope list | `:286–288`, `:310` | Keep the checklist item. Cut the prose list. |
| Indirect injection screened as content | SECURITY box `:97`, T-02, Q2 `:324`, worked example | Reinforcement (each adds a facet). Keep. |

## Cross-Chapter Duplication

| Concept | Ch 20 location | Other location | Verdict and owner |
| --- | --- | --- | --- |
| Guardrails ≠ authorization, with the injected-document example | § Guardrails help… `:28` | Ch 03 § Guardrails and authorization solve different problems (`01-part-i.md:1168–1182`, with a 7-step protection stack) | **Redundant.** Ch 20 is canonical. Ch 03 shrinks to a 2–3 sentence preview plus pointer (Ch 03 owner, consistent with map S5). |
| Defense layers | `:73–83` (9), Figure 20-1 (6) | Ch 03 protection stack (7); Ch 23 § Containment layers (8, `:1059–1068`) and boundary table (5, `:1156`); Part VI intro order | **Redundant with drift.** Ch 20's 9-row table is canonical. Ch 23 maps its mechanisms onto it (C23-R03). Ch 03 points to it. |
| Threat catalog | T-01–T-16 | Ch 23 § Threats and required controls (`:1092–1106`, 11 rows) | **Redundant.** Ch 20 is canonical. Delete Ch 23's table and fold its two uncovered rows into T-cards (C20-R07, C23-R04). |
| Injected-document story | § Worked example `:236` | Ch 01 Tuesday (`01-part-i.md:98`); Ch 03 `:1170`; Ch 23 case box `:1027` and `:1057`; AP-13 | Ch 01 Tuesday is a **reinforcing** teaser. Ch 03 is **redundant**: preview only. Ch 23 is **redundant**: it should continue the Ch 20 example, not retell it (C23-R02). AP-13 is a different threat (memory write), so **reinforcement**. |
| "Assume the model is compromised" | `:22`, `:270` heading | Ch 23 `:1033`, `:1042`, `:1053`; Appendix F #1 | State it once in the Part intro. Ch 20 applies it to detection vs. enforcement, Ch 23 to reach. See S1 below. |
| Trust boundaries | Figure 20-2 | Ch 04 § Trust boundaries (8 rows) | **Reinforcement**, once Ch 20 cites Ch 04. |
| Request sequence | Figure 20-3, `:93` | Figure 4-2 `request-sequence`; Ch 02 six gates | Figure 20-3 is **reinforcement** only if it shows the detector/policy/enforcement split (C20-R06). `:93` is redundant. |
| Discovery ≠ authorization | Q3 `:325` | Ch 08 § Discovery is not permission plus Q (`03-part-iii.md:347`) | **Redundant** question. Replace it (C20-R11). |
| Incident lifecycle | § Respond… `:270` | Ch 23 `incidents:{id}:contain` API (`:1128`); Ch 27 evidence context citing NIST 800-61 (`08-part-viii.md:128`); Appendix B | Ch 20 is canonical. Ch 23's API is the instrument (reinforcement). Ch 27's evidence context should point to Ch 20 or be removed (Part VIII owner). |
| "Guardrail" as a whole architecture or enforced rule | `:58`, `:65`, Fig 20-1, Fig 20-3, `:331` | Ch 05 `02-part-ii.md:388`, `:416–418`, Figure 5-2 "policy-to-guardrail", `[[EXAMPLE:rule-as-guardrail]]`; Ch 28 § Illustrative starting guardrails (`08-part-viii.md:639`); Ch 07 platform row "Guardrails … action policy" (`03-part-iii.md:46`); Ch 01 band row "Identity, guardrails, approvals, containment" (`01-part-i.md:497`); Ch 04 plane row (`02-part-ii.md:43`) | **Contradicts the thesis.** Ch 20 fixes its own uses (C20-R02). The others need their owners: Ch 05 "enforced rule", Ch 28 "starting limits", Ch 07 "Detection (guardrails)" with "action policy" moved to a policy row. Ch 01 and Ch 04 can keep "guardrails" alongside identity/approvals, since that use is consistent with detection. |

## Structural Recommendations

**S1. Division of labour between Ch 20 and Ch 23 (agreed with chapter-23.md).**

| Concern | Ch 20 owns | Ch 23 owns |
| --- | --- | --- |
| Premise "the model can be manipulated" | Applied once: detectors will miss, so enforcement must not depend on them | Applied once: what a manipulated plan can *reach* |
| Layer model | The single 9-layer table (Layer / Controls / Evidence) and Figure 20-1 redrawn to it | No layer list of its own. Its fail-closed boundary table (Capability, Data, Credential, Execution, Egress, Effect) is labeled as a deepening of four Ch 20 layers. |
| Threats | T-01–T-16, each naming its refusal layer | No threats table |
| Injected-document story | The full worked example (attack path, controls, evidence), plus the case box | Its case box continues the Ch 20 example ("the detector missed it; what can it reach?"); no retelling |
| Detector/policy/enforcement | Canonical | Uses it |
| Incident response | The lifecycle (process) | The instruments: kill switch, `incidents:{id}:contain`, quarantine by digest |
| Mechanisms | none in depth | Sandbox profiles, egress grants and URL canonicalization, last-hop secret injection mechanics, DLP, taint lineage, runtime supply-chain admission |
| Governance record | — | Moves to Ch 26 |

**S2. Reorder Ch 20 into one argument:**
1. Opening boxes (new case box and design choice).
2. § Guardrails help… (merged with § Why prompt defenses…).
3. § How the layers reinforce one another (absorbs the state-owner table).
4. § Follow the request across each trust boundary.
5. § How attacks show up in practice (cards plus worked example).
6. § Respond to an incident from evidence (renamed and moved up).
7. Template sections: evidence → sensible place → if fails → verify → put to work → questions → next.

**S3. Do not convert the T-cards into one table.** A 16-row table with five columns does not print legibly, and the H3s serve as an index. Instead, give each card labeled fields that match the layer table (C20-R07).

## Concrete Recommended Changes

1. **C20-R01 · High · Rewrite.**
   - *Location:* `06-part-vi.md:9–14`, Part VI orientation, second paragraph.
   - *Issue:* "The order matters" lists authentication → authorization → guardrails → sandboxes → effect ledger. That contradicts `:93` and Figure 20-3 and does not match the chapter order. There is no chapter map.
   - *Why it matters:* the reader's first model of the Part is a sequence the next page contradicts.
   - *Change:*
     - Replace the "order matters" sentence with the claim that survives: each control answers a different question, and none substitutes for another.
     - State the premise once: assume the model can be manipulated.
     - Add one sentence mapping the chapters. Ch 20: where detection, policy, and enforcement sit, the threats they face, and incident response. Ch 21: who may act, and with how much authority. Ch 22: whether an effect may commit, retry, or recover. Ch 23: what a manipulated plan can still reach.
     - Keep the last sentence ("The model may propose…").
   - *Related:* C23-R01.

2. **C20-R02 · Critical · Rewrite (terminology).**
   - *Locations:* `:58`, `:65` (state-owner row), `:71` (Figure 20-1 caption), `:91` (Figure 20-3 caption), `:317`, `:331`.
   - *Issue:* "guardrail" is used for decision-owning services, for the whole architecture, and for eligibility. That contradicts `:28–37`.
   - *Why it matters:* the chapter's thesis is a vocabulary distinction, and the chapter breaks it six times.
   - *Change:*
     - `:58` → "Detectors raise findings; policy services own decisions; the effect boundary owns commitment."
     - `:65` state owner → "Detectors raise findings; policy and gateway services decide; the effect boundary commits."
     - Figure 20-1 caption → "Figure 20-1 — Defense-in-depth layers" (update `config/diagrams.json`, the `.gv` header comment, and the inline marker).
     - Figure 20-3 caption → "Figure 20-3 — Detection, policy, and enforcement for one protected effect".
     - `:317` → "…the eligibility decision is reading content rather than policy."
     - `:331` → "Layered detection and enforcement establish defense in depth; Chapter 21 makes enforcement specific to each caller by binding every action to an authenticated identity and a delegated grant."
   - *Related:* book-wide T10 (map S17). Other chapters' uses go to their owners (Ch 05, Ch 07, Ch 28).

3. **C20-R03 · Medium · Merge.**
   - *Locations:* `:20` § Why prompt defenses are not enough, `:28` § Guardrails help…, `:55` § Build security in layers.
   - *Issue:* two framing H2s say the same thing, and a third H2 holds only a table.
   - *Change:*
     - Delete the § Why prompt defenses are not enough heading. Keep its last sentence ("This chapter places detection, policy, and enforcement…") as the lead of § Guardrails help…, and cut its first two sentences, which duplicate `:30`.
     - After `:37`, add one sentence on how detection reaches policy: a detector finding becomes an input to the policy point, such as session risk or a required obligation, not a decision of its own. Cross-reference Ch 21 § What an authorization decision must answer.
     - Delete the § Build security in layers heading and move its state-owner table (with the C20-R02 wording) to the top of § How the layers reinforce one another.
   - *Related:* map §5.1 double-why.

4. **C20-R04 · High · Rewrite (diagram) and Condense.**
   - *Location:* `:67–83` § How the layers reinforce one another, Figure 20-1.
   - *Issue:* the figure shows 6 layers, the table 9, and Ch 23 8.
   - *Why it matters:* exercise 1 and If-fails step 1 rely on "nine layers". The figure teaches a different model.
   - *Change:*
     - Edit `assets/diagrams/src/security-depth.gv` to show the 9 table layers in table order: Channel/input, Context/memory, Model/output, Agent/workflow, Identity/policy, Tools/effects, Execution/egress, Supply chain/release, Detection/response. Keep the "effect boundary cannot be skipped" emphasis on Tools/effects.
     - Run `make diagrams` and update the checksum.
     - Add one sentence after the table: "Chapters 21–23 deepen the identity/policy, tools/effects, and execution/egress layers; no later chapter introduces a different layer list."
     - Cut `:69` second and third sentences, since Q1 carries the enumeration.
   - *Related:* C23-R03. Ch 03 protection stack (Ch 03 owner: reduce to pointer).

5. **C20-R05 · Medium · Cross-reference and Remove.**
   - *Location:* `:85–93` § Follow the request across each trust boundary.
   - *Issue:* the section does not cite Ch 04's 8-row boundary table, and the `:93` run-on is a fifth lifecycle.
   - *Change:*
     - After `:89`, add: "Chapter 4's trust-boundary table lists each boundary's untrusted inputs and mandatory controls; Figure 20-2 shows the four a single mortgage request crosses."
     - Delete `:93` entirely. Figure 20-3 and Ch 02's six gates already carry the sequence.
   - *Related:* map §7.1.

6. **C20-R06 · High · Rewrite (diagram).**
   - *Location:* Figure 20-3 `assets/diagrams/src/guardrail-sequence.mmd` (`:91`).
   - *Issue:* the "Input Guardrail" participant refuses the request and is the first gate. The figure teaches the guardrail as the enforcement point.
   - *Change:*
     - Rename the participant to "Content detector".
     - Replace the alt branch so the detector sends a finding (risk label) to the Policy Engine, and the Policy Engine refuses or proceeds.
     - Keep the approval, idempotency, and receipt steps. Rename the file id only if the registry convention allows it; otherwise change only the caption.
     - Run `make diagrams`.
   - *Related:* C20-R02. Figure 4-2 duplication (Ch 04 owner may then retire one of the two).

7. **C20-R07 · High · Rewrite.**
   - *Location:* `:108–234` § T-01 through § T-16.
   - *Issue:*
     - Stock-phrased fragments.
     - No refusal layer, so the intro's promise and exercise 1 are unmet.
     - Runtime controls are mixed with recovery.
     - No pointers to the chapters that build the controls.
     - Ch 23's threats table covers two classes with no card.
   - *Change:* rewrite each card as five labeled lines with no stock lead-ins:
     - **Path** (how it arrives, one sentence).
     - **Signals**.
     - **Prevent**.
     - **First deterministic refusal**: name the layer from the 9-row table and the control. Examples: T-02 → Identity/policy, "tool eligibility independent of content"; T-10 → Execution/egress, "egress grant".
     - **Recover**.
   - Add one pointer per card where a chapter builds the control:
     - T-01/T-02/T-04 → Ch 06 § The trust hierarchy of instructions
     - T-05 → Ch 05
     - T-06 → Ch 06 § Memory is not a bag of embeddings
     - T-07 → Ch 22
     - T-08 → Ch 10/28
     - T-09/T-15 → Ch 21
     - T-12/T-13 → Ch 19
     - T-14 → Ch 23
     - T-16 → Ch 27
   - Fold Ch 23's two uncovered rows:
     - Add "model/vendor compromise: provider isolation, retention controls, disable switch" to T-16's Prevent and Recover lines.
     - Add "cost/availability denial: admission quotas, tenant budgets, recursion limits" to T-08.
   - Change T-12 "Agent gateway" to the canonical A2A gateway name (per T4).
   - *Related:* C23-R04. Exercise 1 `:316`.

8. **C20-R08 · High · Add (opening boxes) and Cross-reference.**
   - *Locations:* after `:18` (evidence context), and § Worked example `:236`.
   - *Issue:* the chapter has no case box or design choice. Ch 23 currently owns the injected-document case box although Ch 20 owns the walk-through.
   - *Change:*
     - Add a WHERE THE MORTGAGE CASE STANDS box. In substance: a mortgage PDF contains an instruction to upload the applicant's bank records to an external address; the content detector may or may not flag it; Harborlight must ensure the outcome does not depend on that.
     - Add a THE DESIGN CHOICE box: "Treat detectors as signals; decide at policy points; fail closed at enforcement points that the model cannot bypass."
     - In the worked example, add "(Chapter 21)" after "capability envelope" (`:241`) and "(Chapter 23)" after EgressGrant (`:250`).
     - State in one clause that Ch 23 picks up the same document after detection has failed.
   - *Related:* C23-R02. Ch 03 `:1170` (Ch 03 owner: shrink to a preview that points here).

9. **C20-R09 · Medium · Add.**
   - *Location:* `:266–268` § A sensible place to start.
   - *Issue:* the only code is a detector, with no framing, in a chapter whose thesis is that detectors are not the boundary.
   - *Change:* before the marker, add one or two sentences: "This is a detector. It saves a model call when it fires; it proves nothing when it does not. The enforcement that must hold regardless is the Tool Gateway's exact-resource check in Chapter 2's governed Tool Gateway example." Do not add inline code.
   - *Related:* `[[EXAMPLE:governed-tool-gateway]]` (Ch 02).

10. **C20-R10 · High · Move, Rewrite, and Condense.**
    - *Location:* `:270–290` § Respond as if the model can be compromised.
    - *Issue:* the heading restates the premise. The section sits after the template sections. The prose repeats the table. There are no pointers to Ch 22/23. It is uncited.
    - *Change:*
      - Rename to "Respond to an incident from evidence, not from the model's account".
      - Move the section to directly after § Worked example (before § What the evidence lets us conclude).
      - Cut `:286–290` except its last sentence ("Reconcile which effects actually occurred… regression cases").
      - Add "(Chapter 23)" to "Narrow kill switch" (`:280`) and "(Chapter 22)" to the Reconcile row (`:282`).
      - Add an evidence row: "Incident lifecycle | Phase structure aligns with NIST SP 800-61r3's integration of incident response into risk management; the agent-specific phases (Revoke, Reconcile) are book-authored recommendations | R42", within R42's recorded scope. Add R42 to the "draws on" sentence.
    - *Related:* Ch 27 evidence context `08-part-viii.md:128` (Part VIII owner: point to Ch 20 or remove the incident claim).

11. **C20-R11 · Medium · Rewrite.**
    - *Locations:* § What to verify before production `:300–312`; § Questions to bring to design review `:319–327`.
    - *Issue:* the checklist lacks the thesis check and carries a Ch 14/22 check. Q3 duplicates Ch 08. The main distinction has no question.
    - *Change:*
      - Replace the fourth check (`:308`) with: "No detector is the only control in front of a protected operation; every protected operation has a deterministic enforcement point that fails closed."
      - Replace Q3 (`:325`) with: Q "What distinguishes a detection failure from an enforcement failure?" / A "A detection failure means a probabilistic signal missed the attack; it is expected and is fixed by tuning or new regression cases. An enforcement failure means a deterministic control allowed an unauthorized operation; it is a defect in policy, identity, or the effect boundary, and it is fixed in code."
      - Shorten Q1's answer to: "Each layer has its own boundary and evidence; a single classifier sees one layer and can be wrong."

12. **C20-R12 · Low · Rewrite.**
    - *Location:* T-04 `:132`, T-05 `:140`, T-10 `:180`, T-11 `:188`.
    - *Issue:* overlapping pairs have no stated distinction.
    - *Change:* add one clause each. T-04: "single-run, crafted for this task". T-05: "persisted in the corpus, affects many runs". T-10: "data is actively sent to a destination". T-11: "data surfaces passively in outputs, logs, traces, or caches".
