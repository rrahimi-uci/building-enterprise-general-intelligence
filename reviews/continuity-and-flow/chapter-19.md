# Chapter 19 — Crossing System Boundaries: MCP, A2A, and Local Control: Continuity and Flow Review

Reviewed: `source/parts/05-part-v.md:386–701` (Chapter 19). For transitions I also read the Part V orientation (`:1–7`), the Ch 18 close (`:349–384`), and the opening of Ch 20 (`06-part-vi.md:1–40`) plus T-12/T-13 (`:196–210`). For duplication I checked:

- Ch 01 § Each control point answers a different question (`01-part-i.md:515–556`)
- Figures 1-4, 19-1, and 19-2 (`assets/diagrams/src/gateway-roles.gv`, `gateway-position.gv`, `model-routing.gv`)
- Ch 04 § Architecture layers and § Trust boundaries (`02-part-ii.md:128–155`)
- Ch 06 § Cross-boundary artifact adoption policy (`:865–910`)
- Ch 08 (`03-part-iii.md:250`, `:308`)
- Ch 22 MCP paragraph (`06-part-vi.md:724`)
- Ch 28 § Optimize in the order that changes outcomes and the PERFORMANCE box (`08-part-viii.md:571–653`)
- Appendix D (`09-appendices.md:90`, `:111`)
- `config/references.json` (R05–R07, R09, R10, R21)
- `config/examples.json`

## Overall Assessment

The MCP/A2A core is the book's clearest treatment of "a protocol does not transfer trust". It is strong in four places:

- the two-protocol comparison table
- the agent-card caveat
- the federated-task APIs, which separate cancellation persistence from relay
- the state-mapping table, with `CompletedPendingValidation` as a quarantine state

The chapter has three structural problems.

1. **It is two chapters.** Lines `:552–593` are an LLM Gateway mini-chapter. It has no link to MCP, A2A, task ownership, or artifacts. The intro admits it is an add-on (`:404–405`). Its component table and Figure 19-1 duplicate Ch 01's control-point table and Figure 1-4, with drift: an "Orchestration layer" row is added, and Figure 19-1 shows no Agent Gateway or MCP Gateway. The LLM Gateway is used in Ch 01, 03, 04 (as "model gateway"), and 07 long before Ch 19 defines it.
2. **It owns contracts that belong to Ch 18 and drops ones it should own.** § What the TaskEnvelope needs to carry is the canonical TaskEnvelope specification, but it sits in the federated chapter. `A2ATaskEnvelope` re-declares Ch 18's code with renamed fields. Its status enum matches neither the chapter's own canonical states nor A2A's task states. Meanwhile the MCP side has no record at all: `ServerManifest` appears only in the state-owner row.
3. **It contradicts Ch 01 on effects.** `:438` says the MCP Gateway "wraps mutating calls in effect semantics". Ch 01's ARCHITECTURE GUIDANCE and Figure 1-4 say the opposite: a mutating MCP call still passes the Tool Gateway, which owns effects. Ch 19 also never connects Ch 01's orphan "Agent Gateway" to its own "A2A Gateway".

Protocol caveats are handled well in the evidence table but almost never reach the prose. The MLflow MCP Registry note is uncited and vendor-specific, and its code is unregistered and untested.

## Intended Reader Mental Model

The reader should leave with these points:

1. MCP standardizes tool/resource/prompt access, and the caller keeps ownership. A2A standardizes task delegation, and ownership moves to the peer.
2. Neither protocol carries business authorization, so each terminates at a local gateway that re-establishes identity, policy, quotas, provenance, and schema.
3. The MCP Gateway decides server and tool trust and eligibility. Effects still go through the Tool Gateway.
4. The A2A Gateway translates Ch 18's TaskEnvelope into a remote task. It maps remote states onto the canonical local lifecycle and quarantines returned artifacts until local adoption.
5. Registry entries and agent cards are discovery metadata, pinned by digest, never grants.

The reader arrives with Ch 18's task tree, TaskEnvelope, and narrowing rule, with Ch 08's "discovery is not permission", and with Ch 01's control-point table. The chapter should apply those concepts across a trust boundary, not re-teach them.

## Section-by-Section Flow Review

**Opening callouts (`:388–396`).** The evidence context pins MCP 2026-07-28 and A2A v1.0.1 and states the key negative ("neither transfers authorization or acceptance"). That is good. The case box introduces an employment-verification MCP server and a property-appraisal partner agent via A2A, but does not connect the partner to Ch 18's internal "property review" specialist (C19-R12). The design choice is crisp. **Good.**

**§ Why interoperability does not transfer trust (`:398–405`).** *Role:* intro. *Adds:* the follow-a-call framing. *Issues:* `:400–402` restates the design choice, and `:404–405` ("It closes by placing the LLM Gateway among those boundaries") announces an unrelated appendix to the chapter. *Verdict:* merge with the next section and delete the LLM sentence (C19-R09, R01).

**§ Re-establish trust at every protocol boundary (`:407–414`).** *Role:* second framing H2 plus the state-owner table. *Adds:* two concrete examples: an accurate but unauthorized MCP server, and an A2A peer that accepts a task without the evidence to act. *Issues:*
- The final sentence repeats the design choice.
- The state-owner row's "Core contracts" lists ServerManifest (never defined) and A2ATaskEnvelope (to be removed).

*Verdict:* this is the double-"why" opening (map §5.1). Merge (C19-R09) and fix the contracts row (C19-R03, R08).

**§ Two protocols, two responsibilities (`:416–438`).** *Role:* the chapter's core concept. *Adds:* the five-row comparison table, which is excellent and unique. *Issues:*
1. `:430–434` restates the table's last row in prose.
2. `:436` is a one-sentence orphan paragraph that the table already says.
3. `:438` gives the MCP Gateway effect wrapping, which contradicts Ch 01 (`01-part-i.md:531–536`, `:552`) and Figure 1-4's Tool Gateway → MCP Gateway edge.
4. `:438` names an "A2A Gateway" with no relationship to Ch 01's "Agent Gateway".
5. MCP authorization essentials (audience binding, no token passthrough) appear only in the evidence table (`:600`), in Ch 22 (`06-part-vi.md:724`), and in Appendix D's MCP row (`09-appendices.md:111`), never in this section's prose. [verified: corrected — Appendix D also carries the passthrough caveat]

*Verdict:* keep the table. Rewrite `:430–438` (C19-R02, R07, R10).

**### Registry model (`:440–442`).** *Role:* registry entry contents. *Adds:* a complete field list, and "Discovery never substitutes for authorization". The latter reinforces Ch 08 § Discovery is not permission and AP-12 without citing either. *Issue:* this is the record the state-owner row calls ServerManifest, but it is never named. It also mixes MCP server and A2A peer entries without saying so. *Verdict:* good. Name the records and add the cross-reference (C19-R08, R15).

**### MLflow MCP Registry note (`:444–446`).** *Role:* a vendor aside. *Issues:*
- "MLflow 3.15.0 introduced experimental MCP Registry capabilities" has no citation. No registry entry covers it; R21 pins only the 3.15.2 release as the examples' baseline.
- The maturity caveat duplicates Appendix D's MLflow row (`09-appendices.md:90`).
- It sits under the "Two protocols" H2 and interrupts the move from the registry to task delegation.

*Verdict:* reduce it to one clause inside § Registry model, with the caveat left in Appendix D (C19-R06).

**§ Pass tasks between agents without losing ownership (`:448–458`).** *Role:* an H2 wrapper plus a Required-analysis table. *Adds:* the Recommended-architecture row gives the decision rule, which is valuable: workflow-native child tasks inside one platform, A2A across deployment or vendor boundaries, MCP for tools. *Issues:*
- The title echoes Ch 11 ("Route the Work Without Losing Ownership") and Ch 18's thesis, and suggests local handoff.
- Design alternatives duplicate the Protocol roles table.
- The Enterprise example repeats the case box.

*Verdict:* retitle and condense (C19-R11).

**### Protocol roles (`:460–471`).** *Role:* positions MCP and A2A among other mechanisms. *Adds:* direct call, child workflow, event bus, and blackboard rows; the agent-card caveat (`:471`), which is unique and important. *Issues:*
- The MCP and A2A rows partly restate the two-protocol table. That is acceptable, because here they are compared with non-protocol mechanisms.
- The blackboard row overlaps Ch 18's peer-swarm row. That is reinforcement.
- "Filter advertised skills" should note that an A2A AgentSkill is not a Ch 08 Skill (`03-part-iii.md:308`).

*Verdict:* keep, with one cross-reference (C19-R15).

**### What the TaskEnvelope needs to carry (`:473–484`).** *Role:* the fullest TaskEnvelope specification in the book. *Issue:* it specifies the *local* envelope (requester subject, caller workload, idempotency, retry ownership) inside the federated chapter, after Ch 18 has already shown a thinner version in code. *Verdict:* move to Ch 18 and keep only the federated delta (C19-R03, C18-R04).

**### Ownership and failure rules (`:486–493`).** *Role:* normative rules. *Issues:*
- Bullet 1 (one owner, transactional transfer), bullet 4 (child failure is data; join contract), and bullet 5 (aggregators validate) restate Ch 18's orchestration rules, Join/Aggregation Service, and JoinPolicy.
- Bullets 2 (receiver options; terminal tasks accept no new work) and 3 (cancellation down, compensation not automatic) are general task rules that Ch 18 lacks.
- Only bullet 6 (no shared mutable state across trust domains) is federated-specific.

*Verdict:* split (C19-R05).

**## A workable implementation (`:495`) → ### Who should own each decision (`:497–499`).** *Adds:* seven A2A components. *Issues:*
- It is written as prose, while Ch 18 uses a table (map §5.1 format drift).
- The "Agent Directory" overlaps Ch 18's "Agent Registry" with no stated relationship, and `agents:resolve` (`:507`) returns both local and remote agents.
- No MCP Gateway component or record exists, so the implementation is A2A-only.

*Verdict:* acceptable. Add one sentence relating the Directory to the Registry (C19-R07). Do not add an MCP implementation block; naming ServerManifest in § Registry model is sufficient (C19-R08).

**### The contracts between components (`:501–515`).** *Adds:* peer registration, card refresh pending policy, federated-task CRUD, cancel ("persist parent cancellation first"), callbacks with dedupe, and `:adoptResult`. These are strong and unique. *Issues:*
- `POST /v1/federated-tasks` "creates an internal durable child task". It should say it does so through Ch 18's Task Service (`POST /v1/runs/{run_id}/tasks`), so readers do not see two task-creation paths.
- `:515` usefully repeats the evidence-table caveat that `/v1` bridges are not A2A endpoints.

*Verdict:* good. Add one pointer (C19-R03).

**### Records worth preserving (`:517–527`).** *Adds:* RemoteAgent, PeerTrustPolicy, FederatedTask, FederatedMessage, RemoteArtifact, CallbackSubscription, PeerObservation ("evidence for routing, not silent trust escalation", an excellent line). FederatedTask already carries the federated delta (remote task/context IDs, peer, state mapping), so it makes A2ATaskEnvelope unnecessary. *Verdict:* good.

**### State mapping and ownership (`:529–539`).** *Role:* local ↔ remote state mapping. *Adds:* `CompletedPendingValidation` as quarantine, and "CancelRequested: stop issuing new authority; continue monitoring possible effects". Both are excellent. *Issues:*
- Column 1 is the canonical *local* task lifecycle that Ch 18 lacks (C18-R03).
- Column 2 uses paraphrases ("Task working/streaming", "Cancel sent") instead of the pinned A2A 1.0.1 task-state names.
- Remote rejection and auth-required outcomes are not mapped.

*Verdict:* keep the mapping and source column 1 from Ch 18 (C19-R04).

**### Scalability, federation, and failure isolation (`:541–550`).** *Adds:* eight federated-specific bullets: per-peer circuit breaking, audience-bound artifact references, span links, "card changes cannot alter an in-flight task's pinned contract", recursive delegation only with explicit depth, and "do not automatically resubmit a potentially active remote task". This is not boilerplate. W3C trace context and span links are used before Ch 24 (low severity). *Verdict:* **good, keep.**

**§ What belongs at the LLM Gateway—and what does not (`:552–565`).** *Role:* gateway scope plus a six-row component table plus Figure 19-1. *Issues:*
- The table duplicates Ch 01's control-point table (`01-part-i.md:522–529`) with a different column scheme, and adds an "Orchestration layer" row that is not a control point.
- Figure 19-1 is a reduced duplicate of Figure 1-4. It shows API → Agent runtime directly, with no Agent Gateway, which contradicts Figure 1-4's API → Agent Gateway → runtime path.
- Nothing here relates to MCP, A2A, or tasks.

*Verdict:* remove from Ch 19 (C19-R01).

**§ What the LLM Gateway needs to enforce (`:567–581`).** *Role:* the only full LLM Gateway contract in the book. *Adds:* an 11-row capability table. It is valuable, but its home is the architecture: Ch 04 already has a "Model plane" layer (`02-part-ii.md:137`) and a "Platform → model vendor" trust boundary (`:153`) with no contract behind them. *Verdict:* move to Ch 04 (C19-R01).

**§ Filter for policy before optimizing cost or quality (`:583–589`) with Figure 19-2.** *Role:* policy-first model routing. *Issues:*
- Ch 28 restates the rule once, in the PERFORMANCE AND COST box (`:653`, "Route on policy first, then on price"), which paraphrases Figure 19-2's own source comment ("model choice is a governance decision before it is an economic one"). Item 4 "Route models" (`08-part-viii.md:576`) covers routing on cost and difficulty without the policy-first rule, and item 6 "Cache safely" (`:578`) is about cache keys, not routing. [verified: corrected — "three times" overstated; only the box states policy-first routing]
- The cache-key sentence (`:589`) is a fourth statement of authorization-scoped caching (Ch 06, Ch 21, Ch 28; map registry).

*Verdict:* move to Ch 28 and drop the cache sentence (C19-R01).

**§ What to measure at the LLM Gateway (`:591–593`).** *Adds:* a route-level metric list and a deployment note (regional, bulkheads, keep platform-owned contracts when buying a gateway). *Verdict:* send the metrics to Ch 28 with routing and the deployment note to Ch 04 (C19-R01).

**§ What the evidence lets us conclude (`:595–603`).** *Role:* three protocol corrections. *Adds:* MCP statelessness and optional extensions; MCP authorization (PKCE, audience binding, no token passthrough); A2A pinned operations, best-effort cancel, and task-existence leakage. *Issue:* these are normative engineering rules held only in an evidence table. The prose never says "never pass the inbound token upstream" or "do not reveal whether a task exists to an unauthorized caller", and never says that Tasks over MCP are an optional extension, so durable ownership must not depend on it. *Verdict:* keep the table and promote the rules into prose (C19-R02, R13). The scopes cited (R05, R06, R07, R09, R10) match their registry entries.

**## A sensible place to start (`:605`)** is an empty wrapper H2.

**### A2A task envelope (`:608–636`).** *Issues:*
- It shares eight fields with Ch 18's TaskEnvelope, renames two (`owner`, `expected_version`), and drops `cancellation_parent_id` (although cancellation is one of A2A's headline features) and `capability`.
- Its `status` literal (`submitted, working, waiting, completed, failed, cancel_requested, canceled`) is neither the chapter's canonical local states (`:531–539`) nor A2A's task states. It therefore teaches a third state vocabulary (map T12).

*Verdict:* remove (C19-R03).

**### MLflow MCP Registry adapter (`:638–664`).** *Issue:* it is inline, unregistered, and untested code that calls an experimental API. The code policy in AGENTS.md says listings belong in `examples/` with a behavioural test. *Verdict:* remove or register (C19-R06). Once both excerpts go, fill the section with the moved adoption check (C19-R16).

**Template close: § If this fails in production (`:666–670`), § What to verify before production (`:672–682`), § Put the idea to work (`:684–687`), § Questions to bring to design review (`:689–697`).**
- *If this fails* has three steps that fit (registry, local decision, artifact).
- *Verify* has five items that cover the chapter. None mentions the LLM Gateway, which confirms that material is extraneous.
- *Put the idea to work:* #1 is good. #2 "Define an A2A TaskEnvelope" perpetuates the duplicate contract.
- *Questions:* Q1–Q5 are good. Q4 (artifact adoption) is the only place the adoption sequence is written out, which supports making Ch 19 the adoption home. Q5's "pin … in the release manifest" bridges well to Ch 27.

*Verdict:* fix exercise #2 (C19-R03).

**§ Where this leads next (`:699–701`).** "Gateways control protocol and model access, but not the entire attack surface…" sets up Ch 20 well. "Model access" depends on whether C19-R01 is adopted (C19-R14).

## Sparse or Underdeveloped Content

- **MCP Gateway mechanics.** One sentence (`:438`) carries the MCP side, and its effect claim is wrong (C19-R02). This needs no new section. It needs a corrected three-sentence paragraph that states the gateway's decision, its hand-off to the Tool Gateway, and the token rules now held in the evidence table.
- **Artifact adoption.** This is the chapter's most important downstream operation (the `CompletedPendingValidation` state at `:536`, `:adoptResult` at `:513`, Q4, RemoteArtifact), but it has no prose explanation. Ch 06 holds the only adoption code (`02-part-ii.md:865–910`), with no prose there either. Move that excerpt here and introduce it with two sentences (C19-R16). Do not write a new section.
- **MCP protocol revision management.** The evidence row says 2026-07-28 removed sessions and added `server/discover` version selection, and § Registry model lists "protocol version and profile". The prose never says the gateway pins a revision per server. One clause is enough (C19-R13).

## Missing Conceptual Connections

- **Ch 01 Tool Gateway owns effects (including over MCP) → Ch 19 MCP Gateway, missing B: "mutating MCP calls continue to the Tool Gateway".** Location: `:438`. Without it, the reader concludes there are two effect owners.
- **Ch 01 Agent Gateway ("may this workload start, receive, or delegate this task?") → Ch 19 A2A Gateway, missing B: "the A2A Gateway is the Agent Gateway's external face".** Location: `:438` or `:499`. Ch 19 is the only chapter that can resolve this orphan (map §4 row 3).
- **Ch 18 TaskEnvelope → A2A task, missing B: which fields the translation adds (remote task and context IDs, peer and card digest, protocol version).** Location: `:438` ("translates local TaskEnvelope to the negotiated protocol").
- **Ch 18 internal property-review specialist → Ch 19 external appraisal partner, missing B: "same task, now owned across a trust boundary".** Location: case box `:392`. This makes the Part a single progression rather than two vignettes.
- **Ch 08 § Discovery is not permission / AP-12 → § Registry model "Discovery never substitutes for authorization", missing B: the cross-reference.** Location: `:442`, `:507`.
- **Ch 08 Skill vs A2A AgentSkill (`03-part-iii.md:308`) → "filter advertised skills" (`:471`), missing B: an advertised A2A skill is metadata, not a certified Ch 08 Skill.**
- **Ch 21 audience binding and token exchange → MCP authorization row (`:600`), missing B: a pointer to Ch 21 § Carry identity all the way to the data.** This is a low-severity forward reference that is already signposted by the evidence context.

## Transition Problems

- **In (Ch 18 → Ch 19).**
  - Ch 18 promises "external tools, agents, and model providers". Ch 19's opening never mentions Ch 18's task tree or TaskEnvelope, so the Part reads as two separate essays.
  - Fix in the case box (C19-R12) and the A2A Gateway sentence (C19-R03).
  - Ch 18's closing should drop "model providers" if C19-R01 is adopted (C18-R15).
- **Within.**
  - The double-why opening (C19-R09).
  - The MLflow aside breaking the registry-to-delegation flow (C19-R06).
  - The jump at `:552` from federated scalability to the LLM Gateway, which has no transition sentence and no conceptual link (C19-R01).
- **Out (Ch 19 → Ch 20).** The bridge "Gateways control protocol … access, but not the entire attack surface" works. Ch 20 T-12 and T-13 restate the gateways as threat controls, which is reinforcement. T-12 says "Agent gateway" in lowercase. Once C19-R07 settles the name, the Ch 20 review should use "A2A Gateway".

## Redundant and Repetitive Concepts

| Concept | Occurrences in Ch 19 | Verdict |
| --- | --- | --- |
| "A protocol does not transfer trust" | Evidence context, case box, design choice, `:400–402`, `:409`, `:430–434`, Q1 | Redundant opening. Keep the evidence context, the case box, the design choice, the comparison table, and Q1. Cut `:400–402` and `:430–434` (C19-R09, R10). |
| TaskEnvelope fields | `:438`, `:473–484`, `:523` (FederatedTask), `:621–636` | Redundant. Keep only FederatedTask (C19-R03). |
| One owner, join, aggregator validation | `:488`, `:491`, `:492` vs Ch 18 | Cross-chapter redundancy (C19-R05) |
| Discovery ≠ grant | `:442`, `:471`, `:507` | Reinforcement within the chapter. Acceptable. |
| Caching with full keys | `:548`, `:577`, `:589` | `:548` (card cache by signed digest) is unique. `:577`/`:589` leave with the LLM Gateway (C19-R01). |

## Cross-Chapter Duplication

| Ch 19 location | Other location | Verdict | Action / owner |
| --- | --- | --- | --- |
| § What belongs at the LLM Gateway… table (`:558–565`) + Figure 19-1 | Ch 01 § Each control point… table (`01-part-i.md:522–529`) + Figure 1-4 | **Redundancy with drift.** "Orchestration layer" row added; Figure 19-1 omits the Agent and MCP Gateways. | Ch 01 canonical. Delete both from Ch 19 (C19-R01). |
| § What the LLM Gateway needs to enforce (`:569–581`) | Ch 04 Model plane row (`02-part-ii.md:137`), "Platform → model vendor" boundary (`:153`), "model gateway" in cells (`:87`); Ch 07 platform row (`03-part-iii.md:47`) | Ch 19 holds the only contract; the others are mentions | **Move to Ch 04** (C19-R01). The Ch 04 review owns the insertion and the "model gateway" → "LLM Gateway" rename. |
| § Filter for policy… + Figure 19-2 + § What to measure… | Ch 28 item 4 (`08-part-viii.md:576`), PERFORMANCE AND COST box (`:653`) | **Redundancy** (the policy-first rule is stated in Ch 19 prose, in Figure 19-2's source comment, and in the Ch 28 box; Ch 28 item 4 is the routing step it should attach to) | **Move to Ch 28** (C19-R01). The Ch 28 review owns the insertion, which replaces the box. [verified: softened — "four times" counted item 6, which is about caching] |
| `:589` cache-key sentence; `:577` Caching row | Ch 06 § Scalability and token economics; Ch 21 § Consistency and revocation policy; Ch 28 item 6, `:637`, Q `:732` | Redundancy (map: Ch 21 canonical) | Drop from the moved material. Keep one Caching row in the Ch 04 table with "(Chapter 21)". |
| § What the TaskEnvelope needs to carry (`:473–484`) | Ch 18 code (`:261`), JSON (`:115`), Delegation rule (`:77`); Appendix C (`09-appendices.md:68`) | Canonical content in the wrong chapter | **Move to Ch 18** (C18-R04, C19-R03) |
| `A2ATaskEnvelope` (`:621–636`) | Ch 18 `TaskEnvelope` (`:261–274`) | **Redundancy with drift.** Correcting the concept map: 8 shared fields, not 10 identical. | Remove (C19-R03) |
| § Ownership and failure rules bullets 1, 4, 5 | Ch 18 § Recommended orchestration rules; Join/Aggregation Service; JoinPolicy | Redundancy | Delete. Bullets 2–3 move to Ch 18 (C19-R05, C18-R03). |
| `:438` MCP Gateway "wraps mutating calls in effect semantics" | Ch 01 ARCHITECTURE GUIDANCE (`01-part-i.md:552`), Figure 1-4 | **Contradiction** | Ch 01 is right. Fix Ch 19 (C19-R02). |
| Evidence row "MCP authorization" (`:600`) | Ch 22 MCP paragraph (`06-part-vi.md:724`) | Redundancy (map: Ch 19 canonical for the MCP Gateway) | Ch 19 states it in prose (C19-R02). The Ch 22 review reduces its paragraph to a pointer. |
| § Registry model "Discovery never substitutes…" | Ch 08 § Discovery is not permission; AP-12 | Reinforcement (applies the rule to servers and peers) | Cross-reference (C19-R15) |
| Q4 / `:adoptResult` / RemoteArtifact | Ch 06 § Cross-boundary artifact adoption policy (code only) | Split concept | Ch 19 canonical. Move the Ch 06 code here (C19-R16). The Ch 06 review deletes it there. |
| § MLflow MCP Registry note (`:444–446`) | Appendix D MLflow row (`09-appendices.md:90`) and Appendix I (`:234`, "MLflow 3.15.0 introduced the MCP Registry") | Redundancy of the maturity caveat; the uncited "3.15.0 introduced" claim also appears in Appendix I | Keep the caveat in Appendix D (C19-R06) [verified: corrected — `:234` is in Appendix I, not Appendix D] |
| T-12 / T-13 (`06-part-vi.md:196–210`) | Ch 19 gateways | Reinforcement (threat view) | None, except the name (C19-R07) |

## Structural Recommendations

1. **Take the LLM Gateway out.** The contract goes to Ch 04 and routing plus metrics go to Ch 28. Ch 19 keeps one bridging sentence. This agrees with concept map S4, which gives (a) Ch 04 and (b) Ch 28 as alternatives. I recommend splitting along that line rather than choosing one, for two reasons:
   - The enforcement contract is an architecture control point. Ch 04 already names the Model plane and the vendor trust boundary but defines neither, and placing it there removes the Ch 01/03/07 forward dependency.
   - Policy-first routing is already restated in Ch 28's PERFORMANCE AND COST box, and Ch 28 item 4 is the routing step it belongs to. [verified: softened — was "three times"]

   Both Ch 01 (already overloaded, map §2) and Ch 23 were considered and rejected. Ch 23's containment layers can cite the Ch 04 table for provider-bound redaction. This mildly diverges from the map's registry line "Routing (model) — wherever the LLM Gateway lands": routing lands in Ch 28, while the Ch 04 table keeps its "deterministic eligibility before optimization" row as the one-line rule.
2. **Make Ch 19 the federated delta of Ch 18.** The TaskEnvelope and the local lifecycle move to Ch 18. Ch 19 keeps FederatedTask, the state mapping, the peer and trust records, and adoption.
3. **Resulting outline:**
   - opening
   - § Why interoperability does not transfer trust (merged)
   - § Two protocols, two responsibilities (table, gateway paragraph, Registry model)
   - § Delegate work across a trust boundary (Protocol roles, agent card, cross-domain rule)
   - § A workable implementation
   - evidence
   - § A sensible place to start (adoption check)
   - template close
4. Make Ch 19 the defining home for the **Agent/A2A Gateway** and **artifact adoption**.

## Concrete Recommended Changes

1. **C19-R01 — High — Move + Remove**
   - **Location:** `05-part-v.md:552–593`, § What belongs at the LLM Gateway—and what does not, § What the LLM Gateway needs to enforce, § Filter for policy before optimizing cost or quality, § What to measure at the LLM Gateway. Also `:404–405`.
   - **Issue:** This is an LLM Gateway mini-chapter inside the MCP/A2A chapter. It duplicates Ch 01's table and Figure 1-4, and the gateway is defined 18 chapters after its first use (Ch 01 `01-part-i.md:526`). [verified: corrected — was "15 chapters"]
   - **Why it matters:** The reader's mental model of Ch 19 ("protocols terminate at local gateways") is diluted, and the model plane has no contract where the architecture is taught.
   - **Change:** **Reconciled (see overall-book-review.md §D-08):** As stated, with names aligned to C04-R01/R05. (b) Place the H3 under § From planes to deployable layers, after the layer table, titled "### What the LLM Gateway enforces" (layer: Model access; plane: Gateways and integration); Ch 04's side is C04-R19. (c) The move into Ch 28 is decided; C28-R07 implements it. (d) Write "…the LLM Gateway that terminates it sits in the Gateways and integration plane (Chapter 4), and model routing is treated as a cost decision in Chapter 28."
     - (a) **Delete** `:556–565` (Figure 19-1 and the component table). Retire `gateway-position` from `config/diagrams.json` and remove its rendered assets; `tools/validate_book.py` requires the set of `[[DIAGRAM:…]]` markers to equal the registry exactly and derives the expected DOCX image count from the registry, so an unused registered diagram fails validation. Ch 01 Figure 1-4 is canonical. [verified: amended — the "leave it unused" option is not permitted by the validator]
     - (b) **Move to Ch 04** (owner: the Ch 04 review): `:554` (scope paragraph, keeping "It does not own business workflow, tool effects, agent delegation, or the external API perimeter"), the `:569–581` capability table, and `:593`'s last sentence ("Centralization adds latency…"). Place them as a new H3 under § A practical reference architecture, after § Architecture layers (`02-part-ii.md:128`), titled along the lines of "### What the model plane enforces: the LLM Gateway". Change the Caching row's Control to "Key every security and semantic dependency (Chapter 21)".
     - (c) **Move to Ch 28** (owner: the Ch 28 review): `:587`, `:589`'s first sentence (the route record), Figure 19-2 (renumbered), and `:593`'s metric list. They replace the PERFORMANCE AND COST box (`08-part-viii.md:653`) and expand item 4 "Route models" (`:576`). Drop `:589`'s cache sentences; Ch 28 item 6 already covers them.
     - (d) In Ch 19, replace `:404–405` with: "Model providers are a third external boundary; the LLM Gateway that terminates it is part of the model plane (Chapter 4), and model routing is treated as a cost decision in Chapter 28."
   - **Related:** C18-R15, C19-R14. Ch 01, Ch 03, and Ch 07 references to the LLM Gateway then resolve backward to Ch 04.

2. **C19-R02 — High — Rewrite**
   - **Location:** `:438` (MCP Gateway sentence), § Two protocols, two responsibilities.
   - **Issue:** It assigns effect semantics to the MCP Gateway, contradicting Ch 01. The MCP authorization rules live only in the evidence table.
   - **Why it matters:** The reader concludes that MCP mutations bypass the Tool Gateway, which is the exact failure Ch 01's ARCHITECTURE GUIDANCE warns against.
   - **Change:** Replace the MCP sentence with: "The MCP Gateway resolves a pinned ServerManifest, authenticates the endpoint, filters tools to the caller's eligible set, validates schemas, and constrains egress. It validates audience-bound tokens and never passes an inbound token upstream. A mutating MCP call then continues to the Tool Gateway (Chapter 1), which reauthorizes the exact resource, enforces idempotency, and records the effect receipt; the MCP Gateway decides whether the server and tool may be used, not whether the effect may happen."
   - **Related:** The Ch 22 review should reduce `06-part-vi.md:724` to "MCP authorization is handled at the MCP Gateway (Chapter 19); the Tool Gateway still owns the effect."

3. **C19-R03 — High — Move + Remove**
   - **Location:** `:473–484` (§ What the TaskEnvelope needs to carry), `:608–636` (§ A2A task envelope), `:414` (state-owner row), `:438` (A2A sentence), `:508`, `:687`.
   - **Issue:** The canonical TaskEnvelope specification sits in the federated chapter, and a drifted copy is in code.
   - **Why it matters:** Readers see three envelope shapes and three state vocabularies across two chapters.
   - **Change:**
     - Move the field-group table to Ch 18 (C18-R04).
     - Delete the `A2ATaskEnvelope` H3 and code.
     - Rewrite the A2A sentence at `:438`: "The A2A Gateway verifies peer identity and trust profile, translates Chapter 18's TaskEnvelope into an A2A task (adding the remote task and context IDs, peer and card digest, and protocol version, recorded in FederatedTask), persists status, enforces deadlines and quotas, and quarantines returned artifacts until local adoption."
     - State-owner row Core contracts → "ServerManifest · FederatedTask · RemoteArtifact".
     - API `:508` purpose: prefix with "Create a child task through the Task Service (Chapter 18) and dispatch…".
     - Exercise `:687` → "Map a local TaskEnvelope to a FederatedTask, including state mapping, cancellation, and artifact adoption."

4. **C19-R04 — Medium — Rewrite**
   - **Location:** `:529–539`, § State mapping and ownership.
   - **Issue:** Column 1 is the local lifecycle, which now lives in Ch 18. Column 2 paraphrases A2A states and omits remote rejection and auth-required outcomes.
   - **Change:**
     - Add a lead-in: "Local states are the task lifecycle of Chapter 18; the gateway maps each remote state onto one of them."
     - Replace column 2 entries with the exact task-state names of the pinned A2A 1.0.1 specification: `TASK_STATE_SUBMITTED`, `WORKING`, `COMPLETED`, `FAILED`, `CANCELED`, `INPUT_REQUIRED`, `REJECTED`, `AUTH_REQUIRED` (§4.1.3 of R07, checked 2026-10-10; there is no "waiting" or "cancel_requested" state).
     - Add a row for remote rejection → Failed (parent applies its join policy).
     - Add a row for authentication-required → NeedsInput (routed to the credential/approval path, not the user prompt).
   - **Related:** C18-R03.

5. **C19-R05 — Medium — Remove + Move**
   - **Location:** `:486–493`, § Ownership and failure rules.
   - **Issue:** Bullets 1, 4, and 5 restate Ch 18. Bullets 2 and 3 are general rules that Ch 18 lacks.
   - **Change:**
     - Move bullets 2 and 3 to Ch 18's task lifecycle (C18-R03).
     - Delete bullets 1, 4, and 5.
     - Fold bullet 6 into the end of the `:471` paragraph as: "Across trust domains, never share mutable state: exchange immutable artifacts or versioned patches under optimistic concurrency."
     - Delete the H3.

6. **C19-R06 — Medium — Condense + Remove (citation and code policy)**
   - **Location:** `:444–446` (§ MLflow MCP Registry note) and `:638–664` (§ MLflow MCP Registry adapter).
   - **Issue:** The version claim is uncited, vendor-specific, and duplicates Appendix D's caveat. The code is unregistered and untested against an experimental API.
   - **Change:**
     - Delete the note H3.
     - Append to § Registry model (`:442`): "An operational registry—for example MLflow's experimental MCP Registry (Appendix D)—can host these entries; it holds metadata, not authorization."
     - Either add a registry entry for the MLflow MCP Registry documentation or release to `config/references.json` and cite it in Appendix D's MLflow row (`09-appendices.md:90`) and Appendix I (`:234`), or remove "3.15.0 introduced" from Appendix I `:234` (the only other place the version claim is made). [verified: corrected — the "3.15.0 introduced" wording is in Appendix I, not Appendix D's row]
     - Delete the adapter excerpt from Ch 19. If the author wants to keep it, register it as `examples/observability/mlflow_mcp_registry.py` in `config/examples.json` with a behavioural test, and cite it from Appendix D, not from Ch 19.

7. **C19-R07 — Medium — Add (definition)**
   - **Location:** `:438` (after the A2A sentence) and `:499`.
   - **Issue:** Ch 01's Agent Gateway is never developed. Ch 19's A2A Gateway and Agent Directory are never related to it or to Ch 18's Agent Registry.
   - **Change:** **Reconciled (see overall-book-review.md §D-07):** Replace the first added sentence with: "The A2A Gateway is the agent-to-agent control point in Chapter 1's gateway table: it decides whether this external peer may receive or return this task, and it terminates the protocol; inside the platform the same decision is made by the Task Service (Chapter 18)." Ch 01 renames its Agent Gateway row to A2A Gateway (C01-R10), so the phrase "external face of the Agent Gateway" is withdrawn. The `:499` addition and the T-12 rename stand.
     - Add: "The A2A Gateway is the external face of the Agent Gateway introduced in Chapter 1: it makes the same decision—may this workload send or receive this task?—for remote peers, and also terminates the protocol."
     - At `:499`, after "Agent Directory stores validated cards and endpoint metadata", add "for remote agents alongside the Agent Registry's local versions (Chapter 18); `agents:resolve` queries both".
   - **Related:** The Ch 01 review may add a forward pointer from its Agent Gateway row to Ch 19. The Ch 20 review should change T-12's "Agent gateway" to "A2A Gateway".

8. **C19-R08 — Medium — Rewrite (naming)**
   - **Location:** `:442`, § Registry model.
   - **Issue:** ServerManifest is listed as a core contract but never defined, and the paragraph mixes server and peer entries.
   - **Change:** Open with "A ServerManifest (MCP) or RemoteAgent entry (A2A) contains…". Keep the field list. Add "pinned by digest; a changed manifest is a new version that must pass policy before use".

9. **C19-R09 — Medium — Merge**
   - **Location:** `:398–414`, § Why interoperability does not transfer trust and § Re-establish trust at every protocol boundary.
   - **Issue:** This is a double framing that restates the design choice.
   - **Change:**
     - Keep the first H2's title and the first two sentences of `:400–402`.
     - Append `:409`'s two concrete examples (an accurate but unauthorized MCP server; an A2A peer without evidence to act).
     - Replace `:402–405` with the C19-R01(d) sentence.
     - Keep the state-owner table.
     - Delete the second H2 heading and its closing sentence.

10. **C19-R10 — Low — Condense**
    - **Location:** `:430–436`, § Two protocols, two responsibilities.
    - **Change:** Replace `:430–434` with "That last row is the one that matters: neither protocol carries business authorization, so each terminates at a gateway that supplies the decision the protocol omits." Delete `:436`.

11. **C19-R11 — Low — Rewrite + Condense**
    - **Location:** `:448–458`, § Pass tasks between agents without losing ownership.
    - **Change:**
      - Retitle to "Delegate work across a trust boundary".
      - In the Required-analysis table, delete the Design alternatives row (the Protocol roles table follows) and the Enterprise example row (it duplicates the case box).
      - Keep Problem, Why it is difficult, Recommended architecture, Trade-offs, and Failure scenarios.

12. **C19-R12 — Low — Rewrite (case continuity)**
    - **Location:** `:392`, the case box.
    - **Change:** Second sentence → "Harborlight consumes a third-party employment-verification MCP server, and the property-review specialist from Chapter 18 is now a partner-operated agent reached through A2A." Keep the rest.

13. **C19-R13 — Low — Add (protocol caveats into prose)**
    - **Location:** `:442` (§ Registry model) and `:509` (GET federated-task row).
    - **Change:**
      - In § Registry model, add: "The gateway pins one MCP protocol revision per server and negotiates explicitly; Tasks and Skills over MCP are optional extensions, so durable ownership never depends on them."
      - In the `:509` purpose, append: "Unauthorized callers receive the same response whether or not the task exists."
    - These state the evidence table's A2A and MCP corrections (`:599`, `:601`) where engineers will read them. No new section.

14. **C19-R14 — Low — Rewrite**
    - **Location:** `:701`, § Where this leads next.
    - **Change:** If C19-R01 is adopted: "Gateways control what crosses a protocol boundary, but not the entire attack surface; Chapter 20 introduces defense in depth across all agentic trust boundaries."

15. **C19-R15 — Low — Cross-reference**
    - **Location:** `:442`, `:471`.
    - **Change:** After "Discovery never substitutes for authorization" add "(Chapter 8 § Discovery is not permission; AP-12)". After "filter advertised skills through enterprise policy" add "—an advertised A2A skill is discovery metadata, not a certified Skill in the sense of Chapter 8".

16. **C19-R16 — Low — Move (from Ch 06)**
    - **Location:** `:605`, § A sensible place to start. Source: `02-part-ii.md:865–910`, Ch 06 § Cross-boundary artifact adoption policy.
    - **Issue:** Once C19-R03 and C19-R06 are applied, the section is empty. The book's only adoption code sits in Ch 06 with no prose, while adoption is taught here (`:adoptResult`, `CompletedPendingValidation`, Q4).
    - **Change:** **Reconciled (see overall-book-review.md §D-18):** Registering the code is required, not optional: move it to `examples/` (for example `examples/federation/artifact_adoption.py`; `federation/` would be a new package, or use the existing `examples/security/` or `examples/platform/`) with a behavioural test (cross-tenant refusal, region or purpose mismatch, untrusted provenance, hash mismatch), register it for chapter 19, and cite `[[EXAMPLE:artifact-adoption]]` under the H3. No inline code.
      - Move the `ArtifactDescriptor` / `AdoptionPolicy` / `authorize_artifact_adoption` excerpt here as "### Remote artifact adoption check".
      - Introduce it with: "`:adoptResult` runs this check after schema, hash, and scan validation and before the parent workflow may depend on the artifact."
      - Ideally register it in `examples/` with a test rather than keeping it inline.
    - **Related:** The Ch 06 review deletes the excerpt there (agrees with concept map S8).

## Verification log

**Line references:** 88 checked against `source/parts/05-part-v.md`, `01-part-i.md`, `02-part-ii.md`, `03-part-iii.md`, `04-part-iv.md`, `06-part-vi.md`, `08-part-viii.md`, `09-appendices.md`, `config/references.json`, `config/examples.json`, and the three diagram sources; 1 fixed (`09-appendices.md:234` is Appendix I, not Appendix D); 0 others off by more than ±3 lines.

**Claims removed:** none.

**Claims softened:**
- "Ch 28 restates the rule three times" / "the same rule stated four times" → once (the PERFORMANCE AND COST box `:653`); item 4 `:576` has no policy-first rule and item 6 `:578` is about cache keys. Applies to the section review, the cross-chapter table, and Structural Recommendation 1. C19-R01(c) (move routing to Ch 28 item 4, replacing the box) is unchanged.
- "MCP authorization essentials appear only in the evidence table and Ch 22" → also Appendix D's MCP row (`09-appendices.md:111`).
- "defined 15 chapters after first use" → 18 (first use Ch 01 `:526`).

**Claims confirmed (most consequential):**
- `:438` contradiction: Ch 19 says the MCP Gateway "wraps mutating calls in effect semantics"; Ch 01 `:552` ARCHITECTURE GUIDANCE says "A tool invoked over MCP still passes the Tool Gateway"; Ch 01's table gives the MCP Gateway "What it does not decide: Whether the resulting effect is authorized"; `gateway-roles.gv` routes `tool -> mcp` and its header comment says "An MCP tool call still passes the Tool Gateway". Ch 19's own component table (`:563–564`) also gives idempotency and effect receipts to the Tool Gateway, not the MCP Gateway, so the sentence contradicts the chapter itself as well as Ch 01.
- Figure 19-1 (`gateway-position.gv`) has nodes agent, api, tool, llm, sys, prov only; edge `api -> agent`. Figure 1-4 has `api -> task(Agent Gateway) -> agent` and an MCP Gateway node. Drift confirmed.
- Ch 19 component table (`:558–565`) adds an "Orchestration layer" row absent from Ch 01 `:522–529` (and omits Ch 01's Human approval gate row).
- `ServerManifest` occurs exactly once in `source/parts/` and nowhere in `examples/` or `config/` (`05-part-v.md:414`).
- "Agent Gateway" occurs in prose three times (`01-part-i.md:525`, `05-part-v.md:561`, `06-part-vi.md:202` as "Agent gateway") plus `gateway-roles.gv`, matching D-07.
- MLflow "3.15.0 introduced" (`:446`): no `[Rxx]` on the paragraph; the only MLflow registry entries are R20 (evaluation docs, 3.x) and R21 (3.15.2 release, scope "Pins the reproducibility baseline used for book examples"). The same uncited claim is in Appendix I `09-appendices.md:234`. `register_mcp_server` appears nowhere in `examples/` or `config/examples.json`.
- A2A 1.0.1 (R07, fetched 2026-10-10) TaskState values are SUBMITTED, WORKING, COMPLETED, FAILED, CANCELED, INPUT_REQUIRED, REJECTED, AUTH_REQUIRED (plus UNSPECIFIED); the `A2ATaskEnvelope` enum's "waiting" and "cancel_requested" are not A2A states, and the state-mapping table (`:531–539`) omits REJECTED and AUTH_REQUIRED. The evidence row's operation list (`:601`) matches the spec's SendMessage, GetTask, ListTasks, CancelTask, SubscribeToTask.
- Field comparison with Ch 18's `TaskEnvelope`: 8 shared names, 2 renamed, 2 dropped, `status` added (see chapter-18.md log).
- Ch 19 (`:386–701`) never mentions "Chapter 18" or "task tree"; the only chapter cross-reference in it is to Chapter 20 (`:701`).
- Ch 04 "Model plane" layer (`02-part-ii.md:137`), "Platform → model vendor" boundary (`:153`), "model gateway" at `:22`/`:87`; Ch 07 LLM Gateway row (`03-part-iii.md:47`); Ch 03 uses at `01-part-i.md:1192`, `:1286`.
- W3C trace context and span links first appear in Ch 19 `:547`; the definition is Ch 24 (`07-part-vii.md:136`).
- `authorize_artifact_adoption` exists only at `02-part-ii.md:895` (Ch 06 § Cross-boundary artifact adoption policy, code directly under the H3 with no prose).
- `tools/validate_book.py` requires the marker multiset to equal the diagram registry and derives the expected DOCX image count from the registry, so retiring `gateway-position` must include the registry entry (C19-R01(a) amended).

**Recommendations amended:** C19-R01(a) (retiring the diagram is mandatory); C19-R04 (exact A2A state names supplied); C19-R06 (the "3.15.0 introduced" removal targets Appendix I `:234`); C19-R16 (package path note).

**Not verifiable here:** whether an MLflow MCP Registry document exists that could become a registry entry (not fetched; the recommendation leaves both options open). The concept-map row and section references (S4, S8, §4 row 3, T12) were confirmed to exist but their contents were not re-audited beyond what the claims required.
