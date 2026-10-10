# Chapter 21 — Carry Identity, Narrow Authority: Continuity and Flow Review

Reviewed: `source/parts/06-part-vi.md:333–632`, plus the close of Ch 20 (`:314–331`), the opening of Ch 22 (`:634–663`), Ch 03 § A tool is not the enterprise API and § Reauthorize the exact resource (`01-part-i.md:1067–1090`), Ch 18 § Monotonic child authority (`05-part-v.md:276–347`), Ch 06 § How context is assembled (`02-part-ii.md:613`), and AP-03 (`04-part-iv.md:1671`).

## Overall Assessment

Chapter 21 has the book's most complete authorization model: the subject and actor carried together, RBAC for eligibility and ABAC for the exact request, the authorization tuple, child grants derived by intersection, and last-hop audience-bound credentials. The implementation tables are rich, and the revocation, freshness, and outage guidance is practical, specific, and unique to this chapter.

Its problems are about order and repetition, not missing content:

- **Two identity triads.** § Keep the user, workload, and grant distinct (`:353`) is really about authentication / authorization / delegation. § Three identities every decision should preserve (`:365`) is subject / actor / purpose, and purpose is not an identity. A third label, "dual principal", appears at `:396`.
- **Restated rules.**
  - RBAC/ABAC is explained twice in one section (`:369`, `:379–383`).
  - Intersection is stated six times (`:385`, `:396`, `:407`, `:424`, `:511`, `:626`).
  - Authorization caching is stated three times (`:387`, `:407`, `:495–497`).
- **The key distinction is buried.** The chapter's clearest mental model, capability envelope (scope) versus credential lease (proof), appears only in the design-review table (`:625`).
- **The decision model arrives late.** The section that defines the decision, § What an authorization decision must answer (`:401`), is an H3 under a heading about data (`:389`), after a Required-analysis table.
- **The worked example is elsewhere.** Exact-resource reauthorization is asserted (`:385`, `:611`), but the concrete case is Ch 03's `MORT-2026-000999`, and this chapter never refers back to it.
- **The subset-proof code duplicates Ch 18.** It is identical to Ch 18 § Monotonic child authority (verified with `diff`).

Verdict: reorder the chapter into who → what is decided → how authority travels → where data is checked → implementation. Deduplicate the rules, and make Ch 21 the only home for the envelope proof.

## Intended Reader Mental Model

After this chapter the reader should hold:

1. **Two identities plus one bound.** The *subject* (whose authority) and the *actor* (which workload) are both carried on every protected request. *Purpose* bounds what that authority may be used for.
2. **One decision per exact request.** The tuple at `:405` is evaluated at each retrieval, delegation, tool call, memory write, and publication. Roles make a request eligible; attributes and current state permit it. Deny wins. Grants intersect, never union.
3. **Scope versus proof.** A capability envelope states the maximum scope and its lineage. A credential lease is short-lived proof for one audience, action, and resource, delivered only to the connector. A child envelope must be a provable subset of its parent.
4. **Authority decays.** Caches are keyed on everything that can change. Revocation invalidates. Waits force re-evaluation. When freshness cannot be established, the request fails closed.

What the reader brings in:
- Ch 01 vocabulary: downscoping, audience binding, RBAC/ABAC → Ch 21.
- Ch 03 field group "Identity: tenant, subject, actor, purpose" (`01-part-i.md:1041`) and § Reauthorize the exact resource.
- Ch 11 "a routing decision cannot grant permission".
- Ch 18 child tasks and the envelope code.
- AP-03 ambient authority.
- Ch 20's detector / policy point / enforcement point.

## Section-by-Section Flow Review

**Opening boxes (`:335–343`).**
- The evidence context (R08/R09/R10), the case box (loan officer, agent, connector, specialist), and the design choice ("Carry subject plus actor identity; exchange for short-lived last-hop credentials only after exact resource authorization") are all good.
- The case box names four actors, which nicely sets up Figure 21-1.

**§ Why every action needs an identity and a narrow grant (`:345`).**
- *Role:* intro.
- *Adds:* "a helpful assistant can quietly become a privilege-escalation path".
- *Verdict:* fine, but it is the first of two framing H2s.

**§ Keep the user, workload, and grant distinct (`:353`).**
- *Role:* defines authentication, authorization, and delegation, followed by the state-owner table.
- *Issues:* the heading names user / workload / grant, but the paragraph defines authn / authz / delegation, and the next H2 introduces a different triad.
- *Verdict:* merge into the intro and retitle the content (C21-R01).

**§ Three identities every decision should preserve (`:365`).**
- *Role:* the subject / actor / purpose model.
- *Adds:* the Harborlight paragraph (`:367`), which is excellent, and the three-row table.
- *Issues:*
  - "Three identities" while the row for purpose answers "why".
  - The section also carries four unrelated jobs: RBAC/ABAC (`:369`, then again `:379–383`), child-grant intersection (`:385`), the gateway step (`:385`), and the caching rule (`:387`), all before the decision tuple is introduced.
- *Verdict:* rename it, and move the other four jobs to the sections that own them (C21-R01, C21-R02).

**§ Carry identity all the way to the data (`:389`).**
- *Role:* nominally the data plane.
- *Content:* a Required-analysis table (`:391–399`), then three H3s.
- *Issues:*
  - The heading promises data. The table is a general summary of the chapter, and its "Recommended architecture" row repeats the intersection rule.
  - The "Design alternatives" row (shared service account, token passthrough, impersonation, OBO, capability tokens, brokered connector) is the only place the chapter weighs alternatives, but each one appears as a single word with no reason it is rejected.
- *Verdict:* condense the table (C21-R05).

**§ What an authorization decision must answer (`:401`).**
- *Role:* the core decision model: the tuple, intersection with deny-wins, and the loan-officer example.
- *Verdict:* the strongest section, buried as an H3 under the data heading. It should come straight after the identities (C21-R02).
- *Issue:* the cache sentence at `:407` duplicates `:387` and `:495`.

**§ How identity travels through the request (`:418`).**
- *Role:* Figure 21-1 plus narrative.
- *Adds:* "only the connector-facing gateway receives a short-lived credential", and "a remote agent can own a task without becoming a new source of authority" (a good bridge back to Ch 19).
- *Missing:* the envelope-versus-lease definition (C21-R03).

**§ Data-plane controls (`:429`).**
- *Role:* retrieval-side enforcement.
- *Adds:* tenant resolved before search, row/field authorization before results reach the model, ACL change treated as index invalidation, workload identity (SPIFFE), and a PDP that runs independently of the LLM.
- *Verdict:* good. It is **reinforcement** of Ch 06's "authorization precedes retrieval", but it does not cite Ch 06 (C21-R06).

**§ A workable implementation (`:438`), § Who should own each decision (`:440`).**
- *Role:* seven components.
- *Issues:*
  - "Connector Gateway/PEP" (`:448`) is the Tool Gateway under another name (map T4). "PEP" is not expanded before this chapter (Ch 04 `02-part-ii.md:141` uses "PDP/PEP" unexpanded; Ch 23 `:1114` is the first to write "policy enforcement points"), and it is Ch 20's "enforcement point". [verified: corrected — "never expanded" was too strong; Ch 23 expands it later]
  - "Authorization Service/PDP" is Ch 20's "policy point".
  - "Access Broker/STS" is the same component as Ch 22's "Credential Broker" (`:735`).
- *Verdict:* rename and cross-link (C21-R04).

**§ The contracts between components (`:452`).**
- *Role:* the APIs.
- *Issues:*
  - "authority envelope" (`:460`) and "grant" (`:462–463`) are used alongside "capability envelope" (`:458`), which is three names in one table (T6).
  - `credentials:exchange` collides with Ch 23's `credentials:lease` (`:1125`).
  - The JSON excerpt uses `crm.account:read:acct_17` and `approval:pricing-write`, which are off-thread for a Harborlight chapter.
- *Verdict:* rewrite (C21-R04, C21-R08).

**§ Records worth preserving (`:481`).**
- *Role:* seven entities.
- *Issues:*
  - The CapabilityEnvelope fields (`:486`) do not match the code (`:544–556`). The record has explicit denies and a parent grant; the code has a cost ceiling and delegation depth; neither has all of them.
  - CredentialLease lacks a credential kind, which Ch 23's SecretLease needs (see C23-R07).
- *Verdict:* align (C21-R07).

**§ Consistency and revocation policy (`:493`).**
- *Role:* freshness and caching.
- *Adds:* online decision for writes and R3/R4, cache key composition, per-source high-water mark, and honest recording of a source that cannot express delegation.
- *Verdict:* the canonical home for authorization caching (map registry). Absorb `:387` and `:407` here.
- *Issue:* the forward reference "(risk classes, Chapter 22)" is fine, but R-classes already appeared in Ch 12. See C22-R05.

**§ Scalability and isolation (`:500`).**
- *Role:* scale.
- *Adds:* batch authorization for retrieval and an explicit IdP/STS-outage policy, both unique and valuable.
- *Verdict:* keep.

**SECURITY AND GOVERNANCE box (`:509–511`).**
- "Delegation must narrow monotonically… a chain that can widen anywhere can widen everywhere." The phrasing is strong, but it is the fifth statement of intersection.
- *Verdict:* keep it as the single memorable statement, and cut the restatements elsewhere (C21-R02).

**§ What the evidence lets us conclude (`:513`).**
- *Role:* one claim row.
- *Issues:*
  - The evidence context cites R08/R09/R10, the table cites R06/R08, and the "draws on" sentence lists R06/R08/R09.
  - R10 is never named after the context line, and R09 supports no claim row.
- *Verdict:* align (C21-R09).

**§ A sensible place to start (`:521`) / § Capability-envelope subset proof (`:524`).**
- *Role:* the subset proof.
- *Issues:*
  - The H2 is empty and is followed by an H3 (map §5.3 pattern).
  - The code is byte-identical to Ch 18 (`05-part-v.md:280–347`).
  - The code is inline, although AGENTS.md says code belongs in `examples/`.
  - `maximum_risk: int` does not say which scale it uses.
- *Verdict:* make this the canonical home and move the code to `examples/` (C21-R07).

**Template sections: § If this fails in production (`:597`), § What to verify before production (`:603`), § Put the idea to work (`:615`), § Questions to bring to design review (`:620`).**
- *If this fails:* three good steps. Step 3 (revoke a role during a wait) is a good test.
- *Verify:* checks 1–5 are good. Check 4 (exact resource reauthorized before the lease) is the Ch 03 example's rule, which supports adding the back-reference.
- *Put the idea to work:* fine.
- *Questions:* Q2 contains the envelope-vs-credential definition that belongs in the body (C21-R03). Q5 (authorization in retrieval) is a reinforcement of Ch 06 and is acceptable.

**§ Where this leads next (`:630`).** "Identity and delegated authority answer who may ask; Chapter 22 proves whether a specific tool effect may execute, commit, retry, or recover." Good.

## Sparse or Underdeveloped Content

- **Alternatives are listed, not weighed.** The Required-analysis "Design alternatives" row (`:395`) lists six options. The reader never learns why token passthrough or impersonation fails: passthrough loses audience binding and actor attribution, and impersonation erases the actor. Two sentences, replacing the table row, would close the gap (C21-R05). AP-03 covers the shared service account, so point there instead of repeating it.
- **Envelope versus lease is never explained in prose.** It is the chapter's most important distinction and appears only at `:625` (C21-R03).
- **The PrincipalChain record (`:485`) has no prose.** "Delegation chain" and "append-only, depth bounded" are never connected to Figure 21-1 or to delegation depth in the code. One clause in § How identity travels would fix this.
- **Do not expand** the RBAC/ABAC or OAuth mechanics. The chapter already has enough detail, and the evidence context limits the protocol claims appropriately.

## Missing Conceptual Connections

1. **Gateway reauthorization (`:385`, check `:611`) → Ch 03 § Reauthorize the exact resource (`01-part-i.md:1084–1090`).** The `MORT-2026-000999` denial is the concrete case this chapter asserts but never shows. Add a one-sentence back-reference instead of a new example (C21-R02).
2. **Child-grant narrowing (`:385`) → Ch 18 durable child tasks and Ch 11 § A routing decision cannot grant permission.** The reader saw child envelopes in Ch 11/18 without a definition. Ch 21 should say that this is where those envelopes are defined (C21-R07).
3. **PDP / PEP (`:446`, `:448`) → Ch 20 policy point / enforcement point (`:32–37`).** The same concepts appear under different names, and no link joins them (C21-R04).
4. **Ch 20 detector finding → ABAC "current risk" (`:369`, `:381`).** Ch 20 never says how a detector reaches policy, and Ch 21 is where it lands. Add one clause to the ABAC sentence (pairs with C20-R03).
5. **Data-plane controls (`:429`) → Ch 06 § How context is assembled (`02-part-ii.md:613`).** The authorization-before-retrieval rule is canonical in Ch 06. Add a back-reference (C21-R06).
6. **Credential lease → Ch 23 secret injection (`:1169`).** Ch 23 delivers secrets at the last hop. Its SecretLease should be a kind of CredentialLease, not a parallel entity (C21-R07, C23-R07).
7. **Ch 19 MCP authorization (`05-part-v.md:600`, audience binding, no token passthrough) → Ch 21.** The rule is first stated in Ch 19, before audience binding is explained here. Ch 21 should note that the Ch 19 MCP rule is an instance of the last-hop credential (one clause in § How identity travels).

## Transition Problems

- **Ch 20 → Ch 21.** Ch 20 closes on "enforceable per caller". Ch 21 opens on identity without naming Ch 20's policy point and enforcement point, so the reader has to work out the mapping alone (C21-R04).
- **Within the chapter.**
  - § Keep the user… → § Three identities… is a triad switch.
  - § Three identities… → § Carry identity all the way to the data jumps from identity to a general Required-analysis table.
  - The decision model then appears as an H3 under the data heading. The reader meets intersection and caching (`:385–387`) before the tuple that explains them (`:405`).
- **Ch 21 → Ch 22.** The closing sentence is good. Ch 22 then re-teaches "authorize at invocation against delegated grant ∩ actor policy" in a SECURITY box (`:910`). That box belongs here and should be removed from Ch 22 (C22-R09).

## Redundant and Repetitive Concepts

| Repeated idea | Locations | Verdict |
| --- | --- | --- |
| RBAC = coarse role, ABAC = request facts | `:369` (second sentence), `:379–383` | Redundant. Keep `:379–383` and move it into § What an authorization decision must answer. Cut the `:369` sentence. |
| Intersection / monotonic narrowing | `:385`, `:396`, `:407`, `:424`, SECURITY box `:511`, Q3 `:626`, checklist `:609` | Partly redundant. Keep `:407` (the rule), `:424` (applied in the figure), the box (the memorable form), and the checklist. Cut `:385`'s first sentence and shorten `:396`. |
| Authorization caching | `:387`, `:407` (last two sentences), `:495–497` | Redundant. Keep only § Consistency and revocation policy. |
| Reauthorize after a wait | `:387`, `:462`, `:495`, `:507`, Q4 `:627`, If-fails step 3 | Reinforcement (each instance applies the rule). Cut only `:387`. |
| Gateway mints a last-hop credential after exact reauthorization | `:385`, `:396`, `:426`, check `:611`, Q2/Q5 | Keep `:426` and the check. Cut `:385`'s final two sentences, which C21-R02 replaces with a pointer to Ch 03. |
| Identity triad naming | `:353` heading, `:365` heading, "dual principal" `:396` | Inconsistent (map T20). Rename (C21-R01). |

## Cross-Chapter Duplication

| Concept | Ch 21 location | Other location | Verdict and owner |
| --- | --- | --- | --- |
| CapabilityEnvelope and `derive_child` code | § Capability-envelope subset proof `:528–595` | Ch 18 § Monotonic child authority `05-part-v.md:280–347` (identical) | **Redundant.** Ch 21 is canonical (agrees with map S11). **Requires Ch 18 owner:** replace the Ch 18 code with two sentences ("a child envelope must be a provable subset of its parent: same subject, narrower actions, resources, purposes, data classes, regions, risk, cost, depth, and lifetime; Chapter 21 gives the proof") and the shared example marker if one is created (C21-R07). |
| Exact-resource reauthorization | `:385`, `:611` | Ch 03 § Reauthorize the exact resource (`01-part-i.md:1084`), with the MORT-2026-000999 example | **Reinforcement**, if linked. Ch 03 keeps the concrete preview; Ch 21 owns the decision model and refers back. Ch 03 owner: add "Chapter 21 gives the decision tuple" in place of any further elaboration. |
| Tool Gateway questions (who, tenant/purpose/resource, eligible tool, action, quota, data handling) | the tuple `:405` | Ch 03 § A tool is not the enterprise API (`01-part-i.md:1067–1082`) | **Reinforcement.** Ch 03's six questions preview the tuple. Ch 03 owner may shorten them to a pointer. |
| Identity field group (subject, actor, purpose) | § Three identities `:365` | Ch 03 AgentStepRequest Identity row (`01-part-i.md:1041`) | **Reinforcement**, consistent triad. Keep it. |
| Capability envelope name drift | `:458`, `:460` "authority envelope", `:462–463` "grant" | Ch 11 "run envelope"; Ch 12 `authority_envelope_id`; Ch 18 "authority ceiling", `capability_grant_id`; P-07 "capability lease" | **Terminology drift (T6).** Canonical: *capability envelope* (scope), identified by `grant_id`; *credential lease* (proof). Ch 21 states this once (C21-R03). Other owners rename. |
| Credentials API and entity | `credentials:exchange` `:459`, CredentialLease `:488`, Access Broker/STS `:447` | Ch 22 Credential Broker `:735`; Ch 23 `credentials:lease` `:1125` and SecretLease `:1139` | **Redundant.** Ch 21 is canonical. Ch 22 references the Access Broker/STS (C22-R07). Ch 23 drops its API and entity (C23-R07). |
| Authorization-scoped caching | § Consistency and revocation `:493` | Ch 06 § Scalability and token economics; Ch 19 caching row and `05-part-v.md:589`; Ch 28 #6 and Q (`08-part-viii.md:732`) | Ch 21 is canonical (map). Other owners point here. |
| Authorize at invocation against grant ∩ actor policy | `:396`, `:407` | Ch 22 SECURITY box `:910` | **Redundant** in Ch 22. Remove it there (C22-R09). |
| Ambient authority fix | whole chapter | AP-03 (`04-part-iv.md:1671`) | **Reinforcement.** AP-03 is the anti-pattern view. Add a one-line back-reference in § Why every action needs… ("the replacement for AP-03's ambient authority"). |

## Structural Recommendations

Reorder the chapter so that each concept is defined before it is used:

1. Opening boxes.
2. **§ Why every action needs an identity and a narrow grant.** Merge `:345` with the authn / authz / delegation paragraph from `:355–359`. Add the AP-03 back-reference. Place the state-owner table here.
3. **§ Subject, actor, and purpose** (renamed from § Three identities…). Keep the Harborlight paragraph, the "every protected request carries…" sentence, and the table.
4. **§ What an authorization decision must answer** (promoted to H2). Contents: the tuple; one RBAC/ABAC paragraph (from `:379–383`, plus the detector-finding clause); intersection and deny-wins; the loan-officer example; and the Ch 03 back-reference for the exact resource.
5. **§ How identity travels through the request.** Contents: Figure 21-1, the child-grant paragraph (from `:385`, trimmed), the envelope-vs-lease definition, PrincipalChain in one clause, and the Ch 19 MCP note.
6. **§ Carry identity all the way to the data.** Data-plane controls with the Ch 06 back-reference, followed by the condensed alternatives paragraph.
7. **§ A workable implementation** (owners, contracts, records), then § Consistency and revocation policy (absorbing `:387` and `:407`'s cache sentences), § Scalability and isolation, and the SECURITY box.
8. Template sections, with the subset proof as the example.

## Concrete Recommended Changes

1. **C21-R01 · High · Rewrite (headings) and Merge.**
   - *Location:* `:345` § Why every action needs…, `:353` § Keep the user, workload, and grant distinct, `:365` § Three identities every decision should preserve, `:396`.
   - *Issue:* the chapter uses two triads, calls purpose an identity, and adds "dual principal" as a third label.
   - *Why it matters:* readers cannot tell which three things every decision must preserve.
   - *Change:*
     - Delete the § Keep the user… heading. Move its paragraph (`:355–359`) and the state-owner table to the end of § Why every action needs….
     - Rename § Three identities… to "Subject, actor, and purpose".
     - Change `:371` to "Two identities and one purpose should remain visible in records and APIs:".
     - In the Required-analysis row `:396`, replace "Carry a dual principal: subject … and actor …" with "Carry subject and actor together".
   - *Related:* map T20.

2. **C21-R02 · High · Move and Condense.**
   - *Location:* `:369`, `:379–387` (in § Three identities…), `:401–416` § What an authorization decision must answer.
   - *Issue:* RBAC/ABAC, intersection, the gateway step, and caching appear before the decision tuple, and some appear twice.
   - *Change:*
     - Promote § What an authorization decision must answer to H2, placed directly after § Subject, actor, and purpose.
     - Move `:379–383` (RBAC/ABAC) into it after the tuple. Add the clause "current risk includes findings from Chapter 20's detectors."
     - Delete the `:369` RBAC/ABAC sentence.
     - Delete `:385`'s first sentence (intersection is restated at `:407`) and its last two sentences. In their place, after the loan-officer example, add: "Chapter 3's request for `MORT-2026-000999` is this rule in action: the tool, schema, and arguments were valid, and the gateway still denied the resource because it lay outside the envelope."
     - Move `:387` to § Consistency and revocation policy and merge it with the existing bullets.
     - Delete `:407`'s last two sentences ("Cache only low-risk…").
   - *Related:* Ch 03 owner (keep the example as a preview).

3. **C21-R03 · High · Add (move from the Q table).**
   - *Location:* § How identity travels through the request `:418–427`.
   - *Issue:* the scope-vs-proof distinction appears only in Q2 (`:625`), and the chapter uses three names for the envelope.
   - *Change:* after `:427`, add two sentences:
     - "A capability envelope states the maximum scope a run or child task may use and records its lineage; its `grant_id` is what other services call 'the grant'. A credential lease is short-lived proof minted from that envelope for one audience, action, and resource, delivered only to the connector."
     - Add one clause: "Chapter 19's ban on MCP token passthrough is the same rule at a protocol boundary."
     - Keep Q2 as reinforcement.
   - *Related:* T6, C21-R08.

4. **C21-R04 · Medium · Rewrite.**
   - *Location:* § Who should own each decision `:442–450`.
   - *Issue:* "Connector Gateway/PEP" and "Authorization Service/PDP" are not linked to Ch 20's policy and enforcement points, and "Connector Gateway" is a new name for the Tool Gateway.
   - *Change:*
     - Rename the row to "Tool Gateway (enforcement point)", with this responsibility text: "Enforce decisions, inject credentials, validate resources and effects, strip secrets; MCP/A2A traffic arrives through Chapter 19's protocol gateways first".
     - Rename "Authorization Service/PDP" to "Authorization Service (policy decision point)".
     - Add one sentence before the table: "The policy decision point and enforcement point are Chapter 20's policy point and enforcement point; detectors feed the first and never replace the second."
   - *Related:* T4, C22-R07.

5. **C21-R05 · Medium · Condense.**
   - *Location:* the Required-analysis table under § Carry identity all the way to the data `:391–399`.
   - *Issue:* the table restates the chapter, and it is the H2's only direct content, under a heading about data.
   - *Change:* replace the table with one paragraph placed after § Data-plane controls:
     - A shared service account fails because it erases the subject (AP-03).
     - Token passthrough fails because it loses audience binding and actor attribution.
     - Impersonation fails because it erases the actor.
     - Token exchange (on-behalf-of) and capability tokens work only when a brokered connector reauthorizes the exact resource.
     - Keep the Harborlight example sentence ("the LOS connector receives a five-minute token scoped to that case and operation").
     - Drop the Problem, Why it is difficult, Recommended architecture, and Failure scenarios rows. The failure scenarios are covered by § If this fails and T-09/T-15.
   - *Related:* map S16. If the synthesizer keeps the Required-analysis tables book-wide, keep only the Design alternatives and Enterprise example rows.

6. **C21-R06 · Low · Cross-reference.**
   - *Location:* § Data-plane controls `:429–436`.
   - *Issue:* the section reinforces Ch 06 without citing it.
   - *Change:* add a lead sentence: "Chapter 6 places authorization before retrieval in context assembly; these controls make that ordering hold in the stores themselves."

7. **C21-R07 · High · Move and Rewrite (code; requires Ch 18 owner).**
   - *Location:* § A sensible place to start `:521` / § Capability-envelope subset proof `:524–595`; § Records worth preserving `:486`, `:488`.
   - *Issue:* the code is identical to Ch 18's. It is inline, contrary to AGENTS.md. Its fields do not match the record. `maximum_risk` has no scale. The H2 is empty.
   - *Change:* **Reconciled (see overall-book-review.md §D-17):** As stated, but register the example with `book_chapters: [21]` only. Ch 18 carries the two-sentence rule and a pointer (C18-R01) and no example marker.
     - Move the code to a new `examples/` file, for example `examples/security/capability_envelope.py`. Register it in `config/examples.json` with `book_chapters: [18, 21]` and a behavioural test that attempts each broadening (actions, purposes, data classes, regions, risk, cost, depth, lifetime, resource prefix, subject change).
     - Replace the inline block with `[[EXAMPLE:capability-envelope]]` and one lead sentence under the H2, then delete the empty-H2 + H3 pattern.
     - Add a comment that `maximum_risk` is the R0–R4 ordinal from Chapter 22.
     - Align the CapabilityEnvelope record (`:486`) with the code by adding "cost ceiling, delegation depth". Note that explicit denies and the parent grant are carried by the record but omitted from the excerpt.
     - Add "credential kind (token or stored secret), use count" to CredentialLease (`:488`) so Ch 23 can drop SecretLease.
     - **Ch 18 owner:** delete § Monotonic child authority's code and replace it with the two-sentence rule and a forward pointer to Ch 21.
   - *Related:* C23-R07. Map S11.

8. **C21-R08 · Medium · Rewrite.**
   - *Location:* § The contracts between components `:456–479`.
   - *Issue:* the table uses "authority envelope" and "grant" alongside "capability envelope", and the JSON excerpt is off-thread.
   - *Change:*
     - `:460` "authority envelope" → "capability envelope ID".
     - `:462–463`: either keep `/v1/grants/{grant_id}` and rely on the C21-R03 definition, or rename to `/v1/capability-envelopes/{grant_id}:revalidate|:revoke`. Prefer the rename for consistency with `:458`.
     - JSON: `"effective_scope": ["mortgage.case:read:MORT-2026-000184"]`, `"obligations": ["redact:ssn", "log:regulated", "approval:document-request"]`.
   - *Related:* map T16 (case identifiers).

9. **C21-R09 · Low · Rewrite (citations).**
   - *Location:* § What the evidence lets us conclude `:513–519`; evidence context `:335`.
   - *Issue:* R10 is cited only in the context line, R09 supports no claim row, and R06 is absent from the context line.
   - *Change:*
     - Add a claim row: "Audience-bound last-hop credentials | Resource indicators constrain token audience; protected-resource metadata lets a client discover which authorization server protects a resource; neither defines enterprise policy | R09; R10".
     - Make the "draws on" sentence list R06; R08; R09; R10.
     - Keep each claim within its registry scope.

10. **C21-R10 · Low · Cross-reference.**
    - *Location:* § Why every action needs an identity and a narrow grant `:345–351`.
    - *Issue:* the section has no link to AP-03, which named the failure this chapter fixes.
    - *Change:* add one clause: "This is the replacement for Chapter 17's ambient authority (AP-03)."

11. **C21-R11 — Low — Cross-reference.** *Added in reconciliation (see overall-book-review.md §D-29).*
   - **Location:** End of § If this fails in production.
   - **Issue:** Same request as C05-R16.
   - **Change:** Add one line: "If a shared service account or a broad token stands in for the subject, see AP-03 in Chapter 17."
   - **Related:** C17-R03, C21-R10.

## Verification log

- **Line references checked:** 68 (all `06-part-vi.md` refs for `:333–632`, plus Ch 03, 06, 11, 12, 17, 18, 19, 22, 23, 28 cross-refs); 0 fixed.
- **Claims removed:** none.
- **Claims softened:**
  - "'PEP' is never expanded" → not expanded before Ch 21; Ch 23 `:1114` spells it out.
- **Important claims confirmed:**
  - Two triads: `:353` heading "Keep the user, workload, and grant distinct" over a paragraph defining authentication / authorization / delegation (`:355–359`); `:365` heading "Three identities every decision should preserve" over subject / actor / purpose (`:371–377`); "dual principal" at `:396`.
  - RBAC/ABAC stated at `:369` and again at `:379–383`; caching at `:387`, `:407`, `:495–497`; intersection/narrowing at `:385`, `:396`, `:407`, `:424`, `:511`, `:626` (plus checklist `:609`).
  - The subset-proof code `:528–595` is byte-identical to Ch 18 `05-part-v.md:280–347` (`diff` empty).
  - CapabilityEnvelope record `:486` lists explicit denies and parent grant; the code has `maximum_cost_usd` and `delegation_depth` instead; CredentialLease `:488` has no credential kind.
  - Evidence: context cites R08/R09/R10 (`:335`); the claim row cites R06; R08 (`:517`); "draws on" lists R06; R08; R09 (`:519`). R10 appears nowhere else in the chapter. C21-R09's proposed row matches R09's scope ("resource indicators used to constrain token audience") and R10's ("protected-resource metadata used in authorization discovery").
  - `:625` is the only prose statement of envelope (scope) versus credential (proof).
  - Ch 03 `MORT-2026-000999` denial is at `01-part-i.md:1084–1090`; `:1041` carries the Identity field group; `:1067–1082` the six gateway questions.
  - Name drift confirmed: "run envelope" `03-part-iii.md:268`, `04-part-iv.md:335`, `:565`; `authority_envelope_id` `04-part-iv.md:456`; "authority ceiling" `05-part-v.md:77`, `:102`; `capability_grant_id` `05-part-v.md:268`, `:627`; "capability lease" P-07 `04-part-iv.md:1441`. AP-03 is `04-part-iv.md:1671`, inside Ch 17 (`:1499`).
  - Ch 22's SECURITY box `:908–910` restates grant ∩ actor policy.
- **Recommendations amended:** none. C21-R07 remains consistent with D-17 and D-23; C21-R11 with D-29.
- **Not verified:** the Ch 06 "authorization precedes retrieval" wording at `02-part-ii.md:613` was located by heading only; the Ch 19 caching row `05-part-v.md:577` and Ch 28 Q `08-part-viii.md:732` were confirmed to exist but not compared in detail.
