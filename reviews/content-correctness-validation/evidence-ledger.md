# Correctness evidence ledger

Baseline `6ebbc8b`, reviewed 2026-10-10. Status vocabulary: **Confirmed Error** means the current text/code contradicts a directly checked invariant, implementation or source scope; **Potential Issue** means a consequential ambiguity or conditional failure; **Needs Verification** means adequate primary evidence or replay material is missing. Links point to the supporting primary source, local implementation, or chapter report; a linked source is not treated as proof beyond its stated scope. B-01 is counted once despite affecting 22 chapters.

| ID / Location | Claim | Status | Evidence | Source type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| C01 / Ch 1 level one | Model has no mechanism for not knowing | Potential Issue | [Chapter 1](chapter-01.md); abstention can be generated, but independent truth checking is absent | Technical reasoning / manuscript context | Qualify truth/calibration limitation |
| C05 / Ch 5 set operations | Intersection is safe to act on | Confirmed Error | [Chapter 5](chapter-05.md); agreement cannot establish freshness, scope, independence or authorization | Logic / internal contract | Downgrade to corroboration signal |
| C06 / Ch 6 performance card | Most systems cannot benefit from more retrieval | Needs Verification | [Chapter 6](chapter-06.md); no defined population or measurement | Missing empirical source | Scope to workload or supply study |
| C07 / Ch 7 CLI | `agentctl` commands describe golden path | Potential Issue | [Chapter 7](chapter-07.md); no repository executable/CLI implementation | Repository source inspection | Mark pseudocommands or implement/test |
| C13a / Ch 13 evaluator | Spend is bounded by `maximum_cost_usd` | Confirmed Error | [Example source](../../examples/patterns/evaluator_optimizer.py) lines 87–99; acceptance precedes spend check; existing test allows $1.20 under $1.00 cap | Executable source/test | Reserve/check cost before call and before acceptance |
| C13b / Ch 13 evaluator | Thresholded scores are required to accept | Confirmed Error | [Example source](../../examples/patterns/evaluator_optimizer.py) lines 52–65; local empty-score call returned `accepted` | Executable source/reproduction | Require every configured criterion and finite score |
| C13c / Figure 13-1 | Diagram shows full acceptance/revision path | Potential Issue | [Rendered diagram](../../assets/diagrams/pattern-reflection.png) and [Chapter 13](chapter-13.md) | Visual/source comparison | Show explicit reject/escalate path |
| C15 / Ch 15 replay | Replay does not repeat calls | Potential Issue | [Temporal activity example](https://docs.temporal.io/develop/python/integrations/openrouter) records post-response failure and retry; completed history replay differs from Activity retry | Official documentation | Add completed-history qualifier |
| C20 / Ch 20 T-04/T-05 | Authorized evidence filters deterministically refuse poisoned facts | Potential Issue | [Chapter 20](chapter-20.md); provenance/ACL checks do not prove factual truth | Threat-model reasoning | State residual false-content risk |
| C22a / Ch 22 effect key | Reuse with different intent conflicts | Confirmed Error | [Example source](../../examples/foundations/effect_idempotency.py) lines 58–69; changed intent after Declined bypasses hash check; local reproduction | Executable source/reproduction | Compare hash before all state handling |
| C22b / Ch 22 reconciliation | No match after visibility window proves Declined | Potential Issue | [Chapter 22](chapter-22.md); requires guaranteed downstream finality and query completeness | Distributed-systems reasoning | Keep Unknown absent a contractual finality bound |
| C24a / Ch 24 worked trace | Review completed in 12 minutes | Confirmed Error | [Chapter 24](chapter-24.md): 3+2+4+3=12 minutes but effect remains Unknown and ledger open | Arithmetic / cross-chapter invariant | Call it time to unresolved state or include reconciliation |
| C24b / Ch 24 fork | Fork may reauthorize effects; none of replay/fork may create live effect | Potential Issue | [Chapter 24](chapter-24.md); new-run authorization and blanket prohibition are in tension | Internal contract comparison | Separate diagnostic replay from authorized new run |
| C25 / Ch 25 repeated runs | `pass^k` describes repeated-run reliability | Potential Issue | [Chapter 25](chapter-25.md); `P(all k pass)=p^k` needs IID assumptions; phrase “or equivalent” mitigates | Probability reasoning | State assumptions and prefer empirical all-k pass |
| C28 / Ch 28 R43 | Little's Law supports entire sizing/economics row | Confirmed Error | [Little 1961 DOI](https://doi.org/10.1287/opre.9.3.383); registry scope limits R43 to `L=λW` | Original research / registry | Attach R43 only to mean formula |
| A-D / Appendix D | Claude Agent SDK, CrewAI, Restate capability rows | Needs Verification | [Appendices](appendices-validation.md); appendix itself acknowledges no registered source | Missing official documentation | Register primary sources or mark provisional |
| A-H1 / Appendix H | Gateway makes an effect happen exactly once | Confirmed Error | [Appendices](appendices-validation.md), [Chapter 22](chapter-22.md) rejects cross-system exactly-once | Internal contract / distributed systems | Define logical idempotent effect protocol |
| A-H2 / Appendix H | Idempotency key is caller-supplied | Potential Issue | [Appendices](appendices-validation.md); shell may derive and bind logical key | Internal terminology comparison | Distinguish trusted derived key from provider key |
| A-L / Appendix L | Effective rate multiplies nodes and fan-out | Potential Issue | [Appendices](appendices-validation.md); undefined factors can double-count branches; [Little's Law](https://doi.org/10.1287/opre.9.3.383) supports only `L=λW` | Dimensional/counting analysis | Use measured attempts per external run |
| A-K / Appendix K R48 | One pipeline run rejected 44% | Needs Verification | [Author's repository documentation](https://github.com/rrahimi-uci/policy-logic-forge/blob/main/ARCHITECTURE.md) contains figure; raw run denominator/commit not pinned in book | Primary author report, no raw replay | Retain narrow wording; pin raw run/counts if empirical |
| B-01 / 22 chapter titles | `config/book.json` titles match canonical chapter H1s | Confirmed Error | [Exact comparison](metadata-title-drift.md) of manuscript, book metadata and cover spec: 22 mismatches; current rendered H1s not proven wrong | Local source/config comparison | Synchronize metadata and add equality validator |

## Primary-source checks and limits

- [MCP 2026-07-28 core specification](https://modelcontextprotocol.io/specification/2026-07-28) and [A2A v1.0.1 specification](https://a2a-protocol.org/v1.0.1/specification/) were used to check the edition-specific protocol framing in Chapter 19. No direct protocol error was confirmed in this pass; that is not a certification of every normative statement.
- [OpenAI Agents SDK documentation](https://developers.openai.com/api/docs/guides/agents/sdk) and [evaluation guidance](https://developers.openai.com/api/docs/guides/agent-evals) were checked for the SDK/evaluation boundary; pinned example imports/tests passed, but live provider calls were not exercised.
- [AWS Bedrock multi-agent documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html) supports Appendix D's Classic-maintenance caveat at review time. Recheck living product status before release.
- [Little's original paper](https://doi.org/10.1287/opre.9.3.383) establishes the mean queueing identity, not the book's utilization, fairness or economic recommendations.
- A repository URL resolving, a citation ID matching, or a test importing an SDK does **not** establish substantive claim support or live effect safety.
- Every registry URL received an HTTP HEAD check; see [the access log](reference-access-check.md) for all 54 statuses [58 registered after this corrective PR; R55–R58 were verified separately on 2026-10-10] and GET/browser follow-up on non-200 responses.

[audited 2026-10-10: all relative links in this ledger resolve (ten chapter/appendix reports, metadata-title-drift.md, reference-access-check.md, `examples/patterns/evaluator_optimizer.py`, `examples/foundations/effect_idempotency.py`, `assets/diagrams/pattern-reflection.png`, which is the registered Figure 13-1). The three quoted line ranges were opened and point at the described code: lines 87–99 are the `evaluate_and_revise` loop in which `spent` accrues (89), `accepted` returns (93–94) before the `maximum_cost_usd` check (98–99); lines 52–65 are `AcceptanceEngine.__init__`/`decide`, which accept on empty `scores`; lines 58–69 are `EffectLedger.commit`, where a `declined` record bypasses the `intent_hash` comparison (61–63) and is overwritten (69). External links: the four registry URLs used here are the registry URLs; the non-registry links (Temporal OpenRouter integration page, two OpenAI developer pages, Policy Logic Forge `ARCHITECTURE.md`) all returned HTTP 200. The Temporal page does describe per-Activity retry policy and one HTTP call per attempt; whether it supports the exact C15 wording is left to the C15 fixing agent. Statuses in this table equal the `**Status:**` labels in the chapter and appendix reports for all 21 ids (8 Confirmed Error, 10 Potential Issue, 3 Needs Verification).]

## Dispositions (2026-10-11)

Each finding was re-verified against the source before it was fixed; the table above is left as recorded. **Confirmed** means the finding held as written; **confirmed-adjusted** means it held but its wording, severity or scope was narrowed; none was rejected or ruled out of scope. The full disposition text sits under each finding in its chapter or appendix report.

| ID | Disposition | Where / note |
| --- | --- | --- |
| C01 | confirmed-adjusted | Ch 1 :169 "no reliable way of knowing what it does *not* know" |
| C05 | confirmed | Ch 5 intersection row "corroborated, not verified"; `set_operations.py` docstring aligned |
| C06 | confirmed-adjusted | Ch 6 :760 prevalence claim replaced by a measure-your-own-workload recommendation; no citation added |
| C07 | confirmed-adjusted | Ch 7 :90 `agentctl` labelled an illustrative command surface |
| C13a | confirmed | Overrun candidate escalated, never accepted; no call once spend ≥ cap; tests added. **Documented limitation:** no per-call reservation (the generator has no cost ceiling), so the last call can still overrun the cap by its own cost — stated on `RevisionLimits` |
| C13b | confirmed | Every configured criterion must be present and finite; executable checks decided first; test added |
| C13c | confirmed-adjusted (Low) | Figure 13-1 redrawn: judge → engine only; engine owns accept / reject→Revise / escalate→Human; sha updated; print-scale check pending |
| C15 | confirmed-adjusted (Medium) | Ch 15 :1070 retry-after-unrecorded-result sentence added |
| C20 | confirmed-adjusted | T-04/T-05 refusals state residual risk (provenance ≠ truth) and point to corroboration, Recover, human review, Ch 23 |
| C22a | confirmed | Intent hash checked before any state handling; different intent after Declined/absent → `EffectConflict`; tests added |
| C22b | confirmed-adjusted | Declined-by-absence requires a manifest-declared visibility window, else InterventionRequired; ToolManifest row and Appendix B step 4 aligned |
| C24a | confirmed-adjusted | Wording ("to return its summary"; run cannot close); arithmetic was correct, "Confirmed Error" overstated |
| C24b | confirmed | Fork = sandbox run with mocked/read-only effects; acting again = new authorized run via `POST /v1/runs` |
| C25 | confirmed-adjusted | pass^k defined as empirical all-k pass rate; independence assumption stated; no citation |
| C28 | confirmed | Evidence row split; R43 supports L = λW only; sizing method labelled book-authored |
| A-D | confirmed | R55–R58 registered (n.d., checked 2026-10-10); Appendix D cites them; Claude row rewritten with beta caution; CrewAI "rapid prototyping" kept as book judgment |
| A-H1 | confirmed-adjusted | Appendix H and Ch 1 :431 Tool Gateway no longer "exactly once" |
| A-H2 | confirmed-adjusted | Idempotency key platform-derived, intent-bound, never model-chosen (Appendix H, Ch 1 :346) |
| A-K | confirmed-adjusted, **partially addressed** | Ch 5 :422 labels 44% author-reported, single run. **Open:** pinned run artifact with numerator/denominator still needs the author's data |
| A-L | confirmed-adjusted | λ_eff = λ_external × E[attempted activities per external run], measured per resource class; retry multiplier only without traces |
| B-01 | confirmed | 22 `config/book.json` titles synchronized; `validate_book.py` title-equality check added (`chapter_title_mismatches` = 0) |

Tally: 8 confirmed, 12 confirmed-adjusted, 1 confirmed-adjusted and partially addressed (A-K), 0 rejected, 0 out of scope.
