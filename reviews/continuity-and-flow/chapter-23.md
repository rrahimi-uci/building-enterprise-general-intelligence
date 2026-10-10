# Chapter 23 — Contain the Damage When a Model Is Manipulated: Continuity and Flow Review

Reviewed: `source/parts/06-part-vi.md:1021–1303`, plus the close of Ch 22 (`:984–1019`), the opening of Ch 24 (`07-part-vii.md:1–40`), Ch 20 in full (`06-part-vi.md:16–331`), Ch 21 credential material (`:447`, `:459`, `:488`), Ch 26 § Governance starts with clear decisions and owners (`08-part-viii.md:21`), and Ch 27 § Governance controls / Emergency Control / § Release attestation verification (`08-part-viii.md:266`, `:289`, `:385`).

## Overall Assessment

Chapter 23's unique value is its containment mechanisms:

- sandbox profiles and leases;
- egress grants with destination canonicalization (the URL code and its bullets on DNS rebinding, redirects, and private address ranges);
- last-hop secret injection;
- taint lineage (SecurityLabel, TaintEdge, and the "follow one piece of data" paragraph);
- the scoped kill switch;
- the five-row fail-closed boundary table under Figure 23-1.

None of these appears elsewhere at this depth.

The rest of the chapter re-teaches Ch 20:

- **Three consecutive framing H2s** state the same premise (`:1033`, `:1042`, `:1053`). The Required-analysis "Recommended architecture" row says it a fourth time ("Assume model compromise", `:1087`).
- **A fourth layer list.** § Containment layers (`:1059–1068`) has 8 layers. Ch 20 has a 9-row table (the canonical one) and a 6-layer figure.
- **A second threat catalog.** § Threats and required controls (`:1092–1106`) has 11 rows that overlap Ch 20's T-01–T-16, and the paragraph at `:1108` repeats Ch 20's evidence claim that a list is not proof.
- **The injected document, again.** The case box (`:1027`) and `:1057` retell the Ch 20 worked example as if it were new.
- **No cross-references.** The chapter never mentions Ch 20, 21, or 22 by number, although its capability, credential, and effect boundaries are built there.
- **Material owned elsewhere.** It also carries:
  - a governance-record paragraph that belongs to Ch 26 (`:1070`);
  - a governance-sources evidence row (`:1186`);
  - a second credentials API and entity (`credentials:lease`, SecretLease) that duplicate Ch 21;
  - a RecoveryObjectives (RTO/RPO) class inside the kill-switch excerpt, which is disaster-recovery material for Ch 27.

Verdict: cut the chapter down to containment mechanics. Its opening should continue Ch 20's example rather than retell it. The division of labour is in chapter-20.md § Structural Recommendations (S1), and this file applies it.

## Intended Reader Mental Model

After this chapter the reader should hold:

1. **Reach, not obedience.** A manipulated model can misuse only the tools, data, and destinations already eligible for its node. It cannot obtain credentials, create clients, reach unapproved hosts, weaken policy, bypass approval, or mark an effect committed (`:1057`).
2. **Every boundary fails closed with a reason.** Capability, data, credential, execution, egress, and effect each have a refusal action and leave evidence (`:1156–1162`).
3. **Containment follows the data.** Labels and taint edges travel with every derived context, artifact, and effect, so disclosure can be explained and derived copies can be deleted (`:1072–1078`).
4. **Emergency control is scoped.** A kill switch stops new risky work at the narrowest safe scope, overrides cached allows, and preserves evidence and effect reconciliation.

What the reader brings in: Ch 20's layers, threats, and the injected-document path; Ch 21's capability envelope and credential lease; Ch 22's effect states. The chapter should rely on these explicitly.

## Section-by-Section Flow Review

**Opening boxes (`:1023–1031`).**
- *Evidence context (R17/R18/R39: SBOM, SLSA, GDPR):* no claim in the chapter uses these sources (C23-R10).
- *Case box:* retells Ch 20's injected document ("A mortgage document contains a hidden instruction to upload applicant records…").
- *Design choice:* "prompt injection may manipulate reasoning but cannot reach unauthorized data, credentials, network destinations, or effects" is the right thesis.
- *Verdict:* rewrite the case box as a continuation of Ch 20 (C23-R02), and fix the citations (C23-R10).

**§ Why the model should be treated as a potentially compromised component (`:1033`).**
- *Role:* intro.
- *Adds:* "what the manipulated plan can reach", the chapter's actual question.
- *Issue:* first of three framing H2s.
- *Verdict:* merge (C23-R01).

**§ Contain the blast radius with independent layers (`:1042`).**
- *Role:* the state-owner table plus one sentence listing eight control types.
- *Issues:*
  - It is the second framing H2.
  - "UseCaseRecord" in Core contracts is an orphan (map §4) and is governance material, not containment.
- *Verdict:* merge, and fix the table (C23-R01, C23-R05).

**§ Start from the assumption that the model can be manipulated (`:1053`).**
- *Role:* the premise again (`:1055`), then the Harborlight application (`:1057`).
- *Verdict:* `:1057` is the chapter's best paragraph and should be the anchor of the merged opening. `:1055` duplicates `:1035–1040`.

**§ Containment layers (`:1059`).**
- *Role:* a list of 8 layers.
- *Issues:*
  - It is the fourth layer list in the book, with a different count from Ch 20's 9-row table and from this chapter's own 5-row boundary table (`:1156`).
  - Items 1, 3, and 6 summarize Ch 21 and Ch 22. Item 8 (governance) is Ch 26.
  - The governance paragraph `:1070` belongs to Ch 26.
  - The data-lineage paragraph `:1072–1078` is unique and excellent, but it is placed under a governance digression.
- *Verdict:* remove the list, move governance to Ch 26, and relocate the lineage paragraph (C23-R03, C23-R05, C23-R06).

**§ Turn that assumption into concrete controls (`:1080`).**
- *Role:* the Required-analysis table.
- *Issues:*
  - Its "Recommended architecture" row restates the premise.
  - Its "Enterprise example" (a legal-research agent) is off-thread.
  - Its "Failure scenarios" row restates Ch 20's T-cards.
  - The only idea it adds is "isolated two-model architectures", which appears in the alternatives row and is never discussed.
- *Verdict:* remove (C23-R04).

**§ Threats and required controls (`:1092`).**
- *Role:* an 11-row threat table.
- *Issues:*
  - Nine rows duplicate T-cards: T-01/02, T-10, T-07/08, T-09/15, T-12/13, T-05/06, T-14, T-11, T-16.
  - Two rows have no card: "Model/vendor compromise" and "Cost/availability denial".
  - `:1108` repeats Ch 20's evidence claim.
- *Verdict:* remove, and fold the two uncovered rows into Ch 20's T-16 and T-08 (C23-R04, matching C20-R07).

**§ A workable implementation (`:1110`), § Who should own each decision (`:1112`).**
- *Role:* owners, written as prose.
- *Issues:*
  - "Content Security Gateway" and "Egress Gateway" add gateway names (map T4). Figure 23-1 itself says "Egress proxy", and so does the bullet at `:1167`.
  - "Secret/Credential Broker" duplicates Ch 21's Access Broker/STS.
  - "Policy enforcement points mediate each trust boundary" is Ch 20/21 content.
- *Verdict:* rename, and convert to a table for consistency with Ch 21 and the merged Ch 22 (C23-R07, C23-R12).

**§ The contracts between components (`:1116`).**
- *Role:* nine APIs.
- *Issues:*
  - `credentials:lease` (`:1125`) duplicates Ch 21's `credentials:exchange`.
  - `security/decisions:authorize` (`:1121`) overlaps Ch 21's `authorization:check`. It is defensible if it is defined as a call that returns containment obligations (sandbox, egress, redaction) and delegates the allow/deny decision to Ch 21's policy decision point.
  - `incidents/{id}:contain` is the instrument for Ch 20's Contain phase but does not say so.
- *Verdict:* C23-R07, C23-R08.

**§ Records worth preserving (`:1130`).**
- *Role:* nine entities.
- *Verdict:* SecurityLabel, TaintEdge, SandboxProfile, SandboxLease, EgressGrant, SecurityFinding, and KillSwitch are canonical here.
- *Issues:*
  - SecretLease duplicates Ch 21's CredentialLease (C23-R07).
  - SupplyChainAttestation overlaps Ch 27 § Release attestation verification. Keep it here as the *runtime admission* record and point to Ch 27 for promotion (C23-R08).

**§ Defense-in-depth request path (`:1144`).**
- *Role:* Figure 23-1 plus the fail-closed table.
- *Adds:* "Read this figure as a containment argument" (`:1148`), and the Boundary / Question / Fail-closed table, which is the chapter's real frame.
- *Issues:*
  - The heading reuses Ch 20's "defense in depth" and invites the reader to look for a second layer model.
  - The table omits a Credential row, although the figure includes the secret broker.
- *Verdict:* rename, promote, and extend (C23-R03).

**§ Sandboxing and egress rules (`:1164`).**
- *Role:* five mechanism bullets.
- *Verdict:* canonical, concrete, and essential. Keep.
- *Note:* the secret-injection bullet (`:1169`) is the containment mechanic for Ch 21's lease. Add a pointer.

**§ What changes as usage grows (`:1172`).**
- *Role:* scale.
- *Verdict:* good. "Audit delivery failure cannot silently permit an R3/R4 effect" (`:1178`) and the digest-scoped quarantine bullet are unique. Keep.

**§ What the evidence lets us conclude (`:1182`).**
- *Rows:*
  - Row 1 (the governance sources NIST AI RMF, ISO 42001, OWASP, EU AI Act) is governance material and belongs in Ch 26.
  - Row 2 (kill switch, R15) is good.
- *Issues:* the "draws on" sentence lists R12/R14/R15/R40/R42. R42 supports no row, and the evidence-context sources R17/R18/R39 are absent.
- *Verdict:* C23-R10.

**§ A sensible place to start (`:1191`), with § Default-deny URL authorization (`:1194`) and § Scoped operational kill switch (`:1226`).**
- *Role:* code.
- *URL authorization:* good. It returns resolved addresses, but nothing says the caller must connect only to those addresses, which is the anti-DNS-rebinding property the bullet at `:1167` claims.
- *Kill switch:* the excerpt bundles RecoveryObjectives (RTO/RPO, minimum safe capabilities), which is unrelated to kill switches and is Ch 27's disaster-recovery content.
- *Both:* inline code, contrary to AGENTS.md, and an empty H2.
- *Verdict:* C23-R09, C23-R13.

**Template sections: § If this fails in production (`:1268`), § What to verify before production (`:1274`), § Put the idea to work (`:1286`), § Questions to bring to design review (`:1291`).**
- *If this fails:* good. Step 1 ("follow the tainted content") applies the lineage model.
- *Verify:* good. Check 1 states the chapter's thesis precisely. Check 4 (pinning) is reinforcement of Ch 27 and acceptable.
- *Put the idea to work:* exercise 1 ("threat-model an injected mortgage PDF") redoes Ch 20's worked example (C23-R11).
- *Questions:*
  - Q1 ≈ Ch 20 Q1 (C23-R11).
  - Q2 is the premise again.
  - Q4 (credentials) ≈ Ch 21 Q2 / § How identity travels.
  - Q3 (sandbox) and Q5 (kill switch) are Ch 23's own and good.

**§ Where this leads next (`:1301`).** "Security controls now produce events and evidence; Chapter 24 turns those signals into end-to-end traces." Good. Ch 24's opening does not call back to it, which is acceptable.

## Sparse or Underdeveloped Content

- **Kill switch prose.** The kill switch is canonical here, but its design rules (narrowest scope, deny precedence over cached allows, measured propagation, checkpointing workflows, reconciling rather than abandoning in-flight effects) appear only in the Q5 answer (`:1299`), the record (`:1141`), and the evidence row (`:1187`). Add two or three sentences of body text (C23-R08). Do not add more code.
- **Privacy.** The evidence context (R39) and Ch 22's closing promise privacy. The body has one paragraph of data lineage (`:1072–1078`) and a scan-before-reuse bullet (`:1170`). Make the lineage paragraph explicitly the privacy mechanism: minimization at projection, retention and deletion propagating along TaintEdges, and residency carried on labels. Two sentences are enough. Otherwise remove "privacy" from Ch 22's closing (C23-R10).
- **"Isolated two-model architectures" (`:1086`).** This is a real containment option (a quarantined model reads untrusted content, and a privileged model never sees it). It is named once and never explained. Either explain it in one sentence under the merged opening or drop it. Recommend one sentence, because it is a containment technique no other chapter covers (C23-R04).

## Missing Conceptual Connections

1. **Merged opening → Ch 20 § Worked example.** The chapter should begin where Ch 20's example ends, with detection failed and the question becoming reach (C23-R02).
2. **Fail-closed table rows → their building chapters.** Capability → Ch 21 capability envelope. Credential → Ch 21 credential lease. Effect → Ch 22 Unknown/reconcile. No row cites a chapter (C23-R03, C23-R08).
3. **Containment mechanisms → Ch 20's layer table.** The chapter deepens four of Ch 20's nine layers (Identity/policy, Context/memory, Execution/egress, Supply chain/release) and should say which (C23-R03).
4. **`incidents/{id}:contain` and the kill switch → Ch 20 § Respond… Contain/Revoke phases.** The instrument is never linked to the process (C23-R08).
5. **Kill switch → Ch 27 Emergency Control (`08-part-viii.md:289`).** The same capability appears in two Parts with no link (C23-R08).
6. **SupplyChainAttestation → Ch 27 § Release attestation verification (`08-part-viii.md:385`).** This chapter covers runtime admission and Ch 27 covers promotion. The split is never stated (C23-R08).
7. **Taint lineage → Ch 05 provenance and Ch 06 ContextManifest.** TaintEdge extends content provenance into derived artifacts and effects. Add a one-clause back-reference (C23-R06).

## Transition Problems

- **Ch 22 → Ch 23.** Ch 22's closing names "privacy", which the body barely delivers (C23-R10). Ch 23's opening then switches back to the Ch 20 premise without acknowledging that Ch 20 already argued it. To the reader it feels like the Part restarting.
- **Within the chapter.**
  - Three framing H2s, then a governance digression inside "Containment layers", then two template tables, then the implementation, and only then the figure that frames the chapter (`:1146`). The containment frame arrives about 110 lines in.
  - Moving the figure and fail-closed table to the front fixes the order (C23-R03).
- **Ch 23 → Ch 24.** Good. The closing hands off security events to tracing.

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict |
| --- | --- | --- |
| Premise "assume the model can be manipulated" | `:1031` (design choice), `:1035`, `:1044–1047`, `:1055`, `:1087`, Q2 `:1296` | Redundant. Keep the design choice, one sentence in the merged opening, and the Q (reworded, C23-R11). |
| Control-type enumeration (capability, data, credential, execution, network, effect, supply chain, governance) | `:1038–1039`, `:1044–1045`, `:1061–1068` | Redundant. Replace with the fail-closed table plus a mapping sentence (C23-R03). |
| "Lists are not proof; injection defenses are probabilistic" | `:1085`, `:1108`, Q1 `:1295` | Redundant (and duplicates Ch 20's evidence row). Keep none here. Ch 20 owns it. |
| Kill-switch scopes | API `:1127`, record `:1141`, scale `:1180`, evidence `:1187`, code, Q5 | Reinforcement across artifacts. Acceptable once body prose exists (C23-R08). |
| Credential delivery at the last hop | containment layer 3 `:1063`, bullet `:1169`, SecretLease, Q4 `:1298` | Partly redundant with Ch 21. Keep the bullet (mechanics). Cut the rest (C23-R07, C23-R11). |

## Cross-Chapter Duplication

| Concept | Ch 23 location | Other location | Verdict and owner |
| --- | --- | --- | --- |
| "Assume compromise" premise | `:1033`, `:1042`, `:1053` | Ch 20 `:22`, `:270` heading; Appendix F #1 | Redundant. The Part intro states it once (C20-R01). Ch 23 applies it once to reach (C23-R01). Ch 20 applies it to detection vs enforcement. |
| Defense / containment layers | § Containment layers (8), boundary table (5) | Ch 20 table (9) + Figure 20-1 (6); Ch 03 stack (7) | Redundant with drift. Ch 20's table is canonical. Ch 23 keeps only its fail-closed table, framed as a deepening (C23-R03, C20-R04). |
| Threat catalog | § Threats and required controls | Ch 20 T-01–T-16 | Redundant. Delete here and fold the two extra rows into T-08/T-16 (C23-R04, C20-R07). |
| Injected-document story | case box `:1027`, `:1057` | Ch 20 § Worked example (canonical); Ch 01 Tuesday; Ch 03 `:1170` | Redundant as a retelling. It becomes a continuation (C23-R02). |
| Incident containment | `incidents/{id}:contain`, kill switch | Ch 20 § Respond… (lifecycle); Ch 27 Emergency Control | Reinforcement once linked. Ch 20 owns the process, Ch 23 the instruments, and Ch 27 the release-side emergency path (C23-R08). |
| Credentials | `credentials:lease` `:1125`, SecretLease `:1139`, Secret/Credential Broker `:1114` | Ch 21 `credentials:exchange` `:459`, CredentialLease `:488`, Access Broker/STS `:447`; Ch 22 Credential Broker `:735` | Redundant. Ch 21 is canonical (C23-R07, C21-R07, C22-R07). |
| Sandbox lease | SandboxLease `:1137` | Ch 22 SandboxLease `:770`, Sandbox Broker `:737` | Ch 23 is canonical. Ch 22 removes its copy (C22-R07). |
| Governance record / use-case inventory | `:1068`, `:1070`, UseCaseRecord `:1051` | Ch 26 § Governance starts with clear decisions and owners (use-case record row, `08-part-viii.md:35`); Ch 27 § Governance controls, GovernanceRecord `08-part-viii.md:316`; Ch 25 checklist | Redundant (four homes). **Requires Ch 26 owner** to absorb the field list from `:1070` into its use-case record. Ch 23 removes it (C23-R05). |
| Governance sources evidence row | `:1186` | Ch 26 § What the evidence lets us conclude (`08-part-viii.md:78`) | Move to Ch 26 (**requires Ch 26 owner**). |
| Supply chain | SupplyChainAttestation `:1142`, layer 7 | Ch 27 § Release attestation verification; Ch 09 evidence row; T-16 | Reinforcement: runtime admission here, promotion in Ch 27. State the split (C23-R08). |
| RTO/RPO RecoveryObjectives | kill-switch excerpt `:1260–1265` | Ch 27 DR / Appendix L | Misplaced. Remove it here. **Ch 27 owner** may adopt it (C23-R09). |
| Egress naming | "Egress Gateway" `:1114` | Figure 23-1 "Egress proxy"; `:1167` "egress proxy"; T-10 "Egress proxy" | Internal and cross-chapter drift (T4). Use "egress proxy" (C23-R12). |

## Structural Recommendations

Apply the Ch 20 / Ch 23 division of labour (chapter-20.md S1). Target outline:

1. **Opening boxes.** Keep the evidence context with its citations fixed. The case box continues Ch 20's example. Keep the design choice.
2. **§ Assume the model can be manipulated** (one H2, replacing `:1033`, `:1042`, and `:1053`). Contents:
   - one premise sentence (from `:1035–1037`);
   - the Harborlight paragraph (`:1057`);
   - one sentence naming which of Ch 20's layers this chapter deepens;
   - the one-sentence two-model option;
   - the state-owner table, with Core contracts "SandboxProfile · EgressGrant · TaintEdge · KillSwitch".
3. **§ The containment path** (promoted from H3 `:1144`). Figure 23-1 and the fail-closed table, extended with a Credential row and pointers to Ch 21/22.
4. **§ Sandboxing and egress rules.**
5. **§ Follow the data through every transformation** (new H3 or H2 built from `:1072–1078`): lineage, privacy, and the Ch 05/06 back-reference.
6. **§ Stop new risky work without abandoning effects** (new short H3). Kill-switch rules, linked to the Ch 20 Contain phase and Ch 27 Emergency Control.
7. **§ A workable implementation.** Owners as a table; contracts without `credentials:lease`; records without SecretLease; scale.
8. Template sections. Code moves to `examples/`, and RecoveryObjectives is removed.

## Concrete Recommended Changes

1. **C23-R01 · High · Merge.**
   - *Location:* `:1033` § Why the model should be treated as a potentially compromised component, `:1042` § Contain the blast radius with independent layers, `:1053` § Start from the assumption that the model can be manipulated.
   - *Issue:* three framing H2s state one premise.
   - *Why it matters:* the reader spends 25 lines on a premise that Ch 20 and the Part intro already established, before meeting anything new.
   - *Change:*
     - Replace the three H2s with one: "Assume the model can be manipulated—then limit what it can reach".
     - Body:
       - (a) `:1035–1037` (keep "the practical question is … what the manipulated plan can reach");
       - (b) `:1057` verbatim;
       - (c) the new sentence "This chapter deepens four of Chapter 20's layers—identity and policy, context and memory, execution and egress, and supply chain—with the mechanisms that make each one fail closed";
       - (d) the state-owner table (C23-R05 wording).
     - Delete `:1038–1040`, `:1044–1047`, and `:1055`.
   - *Related:* C20-R01 (the Part intro carries the premise).

2. **C23-R02 · High · Rewrite.**
   - *Location:* case box `:1025–1027`; § Put the idea to work item 1 `:1288`.
   - *Issue:* the case box retells Ch 20's worked example as new, and the exercise repeats it.
   - *Change:*
     - Case box, in substance: "The injected mortgage document from Chapter 20 has passed the content detector and the model has followed it, proposing to upload applicant records to an external address. The question is no longer whether Harborlight noticed, but what the manipulated plan can reach: sandbox, egress, capability, credential, DLP, and effect controls must each refuse on their own."
     - Exercise 1: "Take each step of Chapter 20's injected-document example and name the boundary in Figure 23-1 that refuses it, its fail-closed action, and the evidence it leaves."
   - *Related:* C20-R08.

3. **C23-R03 · High · Remove, Move, and Rewrite.**
   - *Location:* § Containment layers `:1059–1068`; § Defense-in-depth request path `:1144–1162`.
   - *Issue:* the chapter has a fourth layer list (8) next to its own 5-row table. The real frame appears late, under a heading that borrows Ch 20's term.
   - *Change:*
     - Delete the numbered list `:1061–1068` and its H3.
     - Rename § Defense-in-depth request path to "The containment path", promote it to H2, and move it directly after the merged opening.
     - Add a Credential row to the fail-closed table: "Credential | Does this workload need a secret for this audience and action now? | Withhold the lease; never place a secret in prompt, code, or sandbox environment".
     - Append pointers in the Question cells: Capability → "(Chapter 21)", Credential → "(Chapter 21)", Effect → "(Chapter 22)".
   - *Related:* C20-R04.

4. **C23-R04 · High · Remove.**
   - *Location:* § Turn that assumption into concrete controls `:1080–1108`, including § Threats and required controls `:1092`.
   - *Issue:*
     - The Required-analysis table restates the premise and has an off-thread example.
     - The threats table duplicates Ch 20's T-cards.
     - `:1108` duplicates Ch 20's evidence claim.
   - *Change:*
     - Delete the whole H2 and its H3.
     - Before deleting, transfer:
       - (a) the "Model/vendor compromise" controls (provider isolation, retention controls, fallback or disable switch) into Ch 20 T-16;
       - (b) the "Cost/availability denial" controls (admission quotas, tenant budgets, recursion limits, circuit breakers) into Ch 20 T-08;
       - (c) one sentence for "isolated two-model architectures" into the merged opening: "Where untrusted content must be read, a quarantined model can summarize it into typed fields for a privileged model that never sees the raw text."
     - Present (c) as a book-authored option. Do not add a citation without a registered source.
   - *Related:* C20-R07.

5. **C23-R05 · Medium · Move (requires Ch 26 owner).**
   - *Location:* `:1068` (governance item), `:1070` (governance-record paragraph), state-owner table `:1051` (UseCaseRecord), evidence row `:1186`.
   - *Issue:* governance material sits in a containment chapter, and UseCaseRecord is an orphan.
   - *Change:*
     - Delete `:1070` here. **Ch 26 owner** adds its field list (business purpose, autonomy, data, tools, external effects, human controls, model/vendor dependencies, region, risk classification, evaluations, release, owner, approvers, exceptions, incidents, review date, retirement plan) to Ch 26's use-case record, reconciled with Ch 27's GovernanceRecord.
     - In the state-owner table, change "governance registry" to "kill-switch service", and change Core contracts to "SandboxProfile · EgressGrant · TaintEdge · KillSwitch".
     - Move evidence row 1 (governance sources, R12/R14/R15/R40) to Ch 26 § What the evidence lets us conclude (**Ch 26 owner**).
   - *Related:* map S3 and S10.

6. **C23-R06 · Medium · Move and Cross-reference.**
   - *Location:* `:1072–1078` (data lineage paragraph, currently under § Containment layers).
   - *Issue:* the chapter's most distinctive idea is buried after a governance digression and is not linked to provenance.
   - *Change:*
     - Move the paragraph to a new H3 "Follow the data through every transformation", placed after § Sandboxing and egress rules.
     - Add one lead clause: "Taint lineage extends Chapter 5's provenance and Chapter 6's ContextManifest from sources to every derived artifact and effect."
     - End with a reference to SecurityLabel and TaintEdge in § Records worth preserving.
   - *Related:* C23-R10 (privacy sentences go here).

7. **C23-R07 · Medium · Remove (credentials canonical in Ch 21).**
   - *Location:* owners `:1114` ("Secret/Credential Broker"); API `:1125` `POST /v1/credentials:lease`; record `:1139` SecretLease; containment layer 3 `:1063`.
   - *Issue:* a duplicate credentials API and entity, with a colliding endpoint name.
   - *Change:*
     - Delete the `credentials:lease` row and the SecretLease record.
     - In owners, replace "the Secret/Credential Broker prevents secret exposure" with "Chapter 21's Access Broker issues credential leases, including leases for stored secrets; this chapter governs how they are injected".
     - Keep the `:1169` bullet (injection mechanics) and add "(credential leases, Chapter 21)".
     - **Ch 21 owner:** add credential kind and use count to CredentialLease (C21-R07).
   - *Related:* C22-R07.

8. **C23-R08 · Medium · Add and Cross-reference.**
   - *Location:* new H3 after § The containment path (kill switch), plus `:1127`, `:1128`, `:1142`.
   - *Issue:* the chapter has no references to Ch 20, 21, 22, or 27. Kill-switch design rules exist only in Q5.
   - *Change:*
     - Add H3 "Stop new risky work without abandoning effects", with three sentences: a kill switch is the instrument for Chapter 20's Contain and Revoke phases; it targets the narrowest safe scope (tenant, agent release, tool version, connector, model route, data source) and its deny overrides cached allows; workflows checkpoint, and in-flight effects are reconciled (Chapter 22) rather than abandoned. Its release-side counterpart is Chapter 27's Emergency Control.
     - In the `incidents/{id}:contain` row, add "(implements Chapter 20's Contain phase)".
     - In SupplyChainAttestation, add "runtime admission; promotion evidence is Chapter 27's".
   - *Related:* C20-R10. Ch 27 owner may add a back-reference at Emergency Control.

9. **C23-R09 · Medium · Remove and Move (code).**
   - *Location:* § A sensible place to start `:1191`; § Scoped operational kill switch `:1226–1266`; § Default-deny URL authorization `:1194–1224`.
   - *Issue:* the code is inline, contrary to AGENTS.md. RecoveryObjectives is unrelated disaster-recovery content. The H2 is empty.
   - *Change:*
     - Delete the RecoveryObjectives class from the excerpt. **Ch 27 owner** may adopt it in its DR material.
     - Move both excerpts to `examples/security/` (for example `egress_url.py` and `kill_switch.py`), register them in `config/examples.json` with behavioural tests (rejecting non-HTTPS, credentials in the URL, a non-443 port, an unlisted host, and a private address; requiring a kill-switch scope; scope matching), and cite them with `[[EXAMPLE:...]]`.
     - Give the H2 a one-sentence lead instead of the empty-H2 + H3 pattern.

10. **C23-R10 · Medium · Rewrite (citations and privacy).**
    - *Locations:* evidence context `:1023`; § What the evidence lets us conclude `:1184–1189`; the new lineage H3 (C23-R06).
    - *Issue:*
      - The context cites R17/R18/R39, which support no claim.
      - The "draws on" sentence lists R42, which supports no row.
      - The privacy promise (Ch 22 closing, R39) is barely delivered.
    - *Change:*
      - Add claim rows within registry scope:
        - "Supply-chain admission | SBOM inventory and SLSA build provenance answer different questions; runtime admission should verify both for pinned artifacts | R17; R18".
        - "Data minimization and deletion (EU context only) | GDPR principles inform minimization and erasure obligations for EU personal data; jurisdiction-specific analysis is still required | R39".
      - Keep the kill-switch row. Remove the governance row (C23-R05).
      - Set "draws on" to R15; R17; R18; R39. Drop R42 unless an incident claim is added. Ch 20 now carries R42 (C20-R10).
      - In the lineage H3, add two sentences: projection minimizes fields before materialization; retention and deletion propagate along TaintEdges to derived contexts, caches, traces, and artifacts.

11. **C23-R11 · Medium · Rewrite.**
    - *Location:* § Questions to bring to design review `:1293–1299`.
    - *Issue:* Q1 duplicates Ch 20 Q1, Q2 restates the premise, and Q4 duplicates Ch 21.
    - *Change:*
      - Merge Q1 and Q2 into: Q "What can a manipulated model still do inside a correct containment design?" / A "Misuse only the tools, data, and destinations already eligible for its node; it cannot obtain credentials, reach unapproved hosts, weaken policy, bypass approval, or mark an effect committed."
      - Replace Q4 with: Q "Why must security labels follow derived artifacts?" / A "Disclosure and deletion apply to copies as well as sources; without taint edges from source to context, artifact, trace, and effect, governance cannot explain a later leak or erase derived data."
      - Keep Q3 and Q5.

12. **C23-R12 · Low · Rewrite.**
    - *Location:* § Who should own each decision `:1114`.
    - *Issue:* the owners are given as prose, inconsistent with Ch 21 and Ch 22. "Content Security Gateway" and "Egress Gateway" multiply gateway names, and Figure 23-1 says "Egress proxy".
    - *Change:*
      - Convert to a Component / Responsibility table.
      - Rename to "Content inspection service" and "Egress proxy".
      - Drop "policy enforcement points mediate each trust boundary" (Ch 20/21 content) in favor of "the Tool Gateway and protocol gateways enforce containment obligations returned with each decision".
    - *Related:* map T4.

13. **C23-R13 · Low · Add.**
    - *Location:* § Default-deny URL authorization (`:1206–1223`, or its moved example file).
    - *Issue:* the function returns resolved addresses, but nothing requires the caller to use them, which is the anti-rebinding property claimed at `:1167`.
    - *Change:* add one sentence of lead text or a docstring line: "The egress proxy must connect only to the returned addresses for this grant; resolving again at connect time reopens DNS rebinding."
