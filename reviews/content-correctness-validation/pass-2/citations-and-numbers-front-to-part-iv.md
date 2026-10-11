# Pass 2-A: citations, uncited claims, numbers, and freshness, from the front matter through Part IV

**Scope:** `source/parts/00-front-matter.md` through `source/parts/04-part-iv.md` (front matter and Chapters 1–17), plus the `supports` text of `config/references.json` entries whose primary source was fetched for this pass. **Branch:** `pass2/a`, based on `fix/correctness-review-findings`. **Date:** 2026-10-11. **ID prefix:** P2-A.

## Scope and method

1. **Claim-level citation support.** Every citation attached in these files was checked against its reference's recorded `supports` scope:
   - 24 bracketed `[Rxx]` occurrences, the ones the validator counts: front matter 1, Part I 5, Part II 7, Part III 3, Part IV 8.
   - 23 bare-ID attachments in 14 "What the evidence lets us conclude" rows.

   That makes **47 claim–reference attachments**. For each, the attached sentence or table row was read in full. When the scope was ambiguous or the claim was specific, the primary source was fetched or the pinned package was inspected (see the list below).
2. **Uncited factual claims.** Read all of Chapters 1–17 for product, protocol, standard, statistical, and date claims without a citation. 16 candidates were assessed. Most are book-authored judgment, worded as such, or illustrative examples. Three were reworded.
3. **Numbers and tables.** Checked about 40 counts, arithmetic results, and cross-table correspondences. Examples: 10-problem and four-theme groupings; demo-week-to-row mapping; 9 bands to 9 plane rows; 7 planes to 11 layers (2+1+2+3+1+1+1); 6 gates and "first five"; ten principles split 1–3/4–6/7–10; R0–R4 against Chapter 22; 6 Hub views; 10 context stages with authorization at stage 3; 4 trust tiers and 8 segment kinds; 15 platform capabilities; 6 Skill states; 4 bindings; 7 compatibility checks against the review answer; 6 framework-edge mechanisms; 10 control-flow steps against Chapter 16's step references; dispositions and step statuses against `examples/contracts.py`; 5^5 = 3,125; 3×3×2 = 18; the 7/7/2 anti-pattern split and the 16 cards; the "Ten lines" demo against `capability_levels.py`; and the quadratic token claim.
4. **Freshness.** Checked the OpenAI Agents SDK (pinned 0.22.2), MLflow (pinned 3.15.2), the OMG standard versions, and MCP Skills against current releases and official docs.

**Primary sources fetched or inspected on 2026-10-11:**
- **OpenAI Agents SDK.** Docs: index, agents, guardrails, tracing, human-in-the-loop, tools. GitHub releases (v0.22.2 is dated 2026-09-09; latest is v0.23.1, dated 2026-10-02). The installed `openai-agents==0.22.2` package was introspected for `Agent`, `Runner`, guardrails, `RunState`, `ModelSettings.retry`, `RunConfig.trace_metadata`, and the shell-tool and sandbox `Skill` types.
- **CloudEvents.** The core spec and the dataref extension.
- **AWS.** The transactional-outbox page.
- **Temporal.** "The definitive guide to Durable Execution", which is a blog post by Tom Wheeler dated 6 May 2025.
- **Durable-execution frameworks.** PydanticAI durable-execution overview and the DBOS AI quickstart.
- **Microsoft Agent Framework.** The overview page, dated 2026-07-29.
- **Google ADK.** The agents page.
- **MLflow.** The eval-monitor docs, plus releases (latest 3.17.0).
- **Anthropic.** "Building Effective Agents".
- **ReAct.** The arXiv abstract.
- **NIST AI 600-1.** The full-text PDF, extracted locally.
- **OWASP.** The AI Agent Security Cheat Sheet, and the Agentic Top 10 landing page (landing page only).
- **OMG.** The DMN version list.
- **MCP.** SEP-2640 (Skills Extension, Final, Extensions Track).
- **Policy Logic Forge.** `ARCHITECTURE.md` §1.1.

## Findings

| ID | Location | Status | Evidence | Change made or recommended owner |
| --- | --- | --- | --- | --- |
| P2-A-01 | Ch 1 evidence row "Grounding boundary" (`01-part-i.md` ~462), R01; R13 | Confirmed Error (scope) | R01 supports only the definition of ReAct and its benchmark results; R13 lists confabulation among GAI risks (AI 600-1 §2, item 2). Neither supports "a benchmark or demo does not establish authorization…" or "every output should carry evidence", which are book-authored. | Split the row. "Reported capability and risk" keeps R01 and R13. "Grounding boundary (book-authored recommendation)" gets no source. |
| P2-A-02 | Ch 4 § Event contract (`02-part-ii.md` ~238) | Confirmed Error | The CloudEvents spec says attribute names "MUST consist of lower-case letters [a-z] or digits [0-9]", and extensions follow the same rule. `tenant_id`, `correlation_id`, and `causation_id` are invalid extension names. | Prose now names the tenant, correlation, and causation extensions and states the naming rule, so `tenant_id` must serialize as `tenantid`. **Cross-owner:** `examples/contracts.py` `CloudEvent` should add wire aliases (`tenantid`, `correlationid`, `causationid`) with a test. Appendix C (`09-appendices.md:236`) should drop the underscore names. |
| P2-A-03 | Ch 6 evidence row "Privacy lifecycle" (~766), R13; R39 | Confirmed Error (scope) | GDPR (R39) supports purpose limitation, lawful basis, and data-subject and erasure rights. AI 600-1 §2.4 (R13) supports leakage and the risks to consent and purpose specification. Legal-hold precedence, residency, provider retention controls, and "proof that derived summaries/indexes were handled" are engineering recommendations in neither source. | Split the row. "Privacy obligations" keeps R13 and R39. "Privacy lifecycle (book-authored recommendation)" gets no source. |
| P2-A-04 | Ch 7 evidence row "Framework portability" (~100), R29; R31; R32 | Potential Issue | Each source documents only its own framework. None states that the SDKs "differ in cancellation, streaming, tool, approval, and error semantics"; that comparison was not verified. | Split the row. "Framework abstractions" keeps the three sources. "Framework portability (book-authored recommendation)" now says "do not assume these SDKs share…". The pointer sentence now reads "the portability row". |
| P2-A-05 | Ch 8 evidence row "Terminology" (~307) | Confirmed Error | The pinned `openai-agents==0.22.2` ships `ShellToolLocalSkill`, `ShellToolSkillReference`, inline skills, and a sandbox `Skills` capability. The SDK tools docs say "Local shell skills are available with `ShellTool(environment={…"skills": […]})`". "It is not an OpenAI Agents SDK primitive" is therefore wrong at the pinned version. | Rewritten: Skill "is not identical to A2A AgentSkill metadata, to Skills served over MCP, or to the skills the OpenAI Agents SDK can attach to its shell tool." R29 added to the row and to the "draws on" line. MCP Skills exist as SEP-2640 (Final, Extensions Track), which R05's "extensions" scope covers. |
| P2-A-06 | Ch 9 evidence row "Distribution security" (~442), R16; R17 | Confirmed Error (scope) | R16 lists "Supply Chain Attacks" as a key risk but gives no controls for pinning, SBOM, signing, provenance, publisher trust, or revocation. R17 supports only build provenance and levels. | Split the row. "Supply-chain risk" keeps R16 and R17. "Distribution security (book-authored recommendation)" gets no source. |
| P2-A-07 | Ch 12 evidence row "Durable scheduling" (~520), R02 | Confirmed Error (scope) | The R02 page, fetched today, defines durable execution as "crash-proof execution" that "resumes in a new process" and supports long waits. It does not describe replay or event history. The row's "which is why…" was an unlabelled book inference. | The R02 clause is narrowed to resuming after failure and supporting long waits. The workflow-scheduling clause is labelled the book's recommendation. |
| P2-A-08 | Ch 15 evidence row "Durable progress" (~1121), R02 | Confirmed Error (scope) | Same source: "through replay and durable timers" is not in R02. | Narrowed to crash-proof resumption and long waits. Replay is now stated as one engine design, the one this chapter's reducer uses, and not something the source specifies. |
| P2-A-09 | Ch 15 evidence context (~927), R02; R36; R38 | Potential Issue | PydanticAI lists 8 backends and says each wraps calls as durable units. DBOS replays completed calls from checkpoints. No source states that "replay semantics vary by backend". | That clause is now labelled the book's caution. The cited part keeps resumption after failure and framework integration with several backends. |
| P2-A-10 | `config/references.json` R02 `supports` | Confirmed Error (registry scope) | The recorded scope claimed "replay, durable timers". The page has neither as a mechanism. | `supports` was narrowed, from today's fetch, to crash-proof resumption, reliable long waits, and long-running processes, and states that it does not describe replay. **Cross-owner (registry metadata):** R02 `year` "2024" should be 2025 (published 6 May 2025), and `publication_or_version` "Temporal documentation" should be "Temporal blog". Set `checked_on` to 2026-10-11. |
| P2-A-11 | Ch 3 (~841, ~918), R29; R30 | Potential Issue (scope narrower than claim) | The recorded R29 scope omitted the runner, structured output, interruptions/`RunState`, and tool guardrails. Today's fetch of the docs (agents: `output_type` "use structured outputs"; guardrails: "Tool guardrails wrap FunctionTool instances"; HITL: `RunResult.interruptions`, `RunState`, approve/reject; tracing: `trace_include_sensitive_data`) and inspection of the 0.22.2 package confirm every claim. | R29 `supports` widened to what was fetched: agents, runner, function tools, structured output types, input/output/tool guardrails, handoffs, sessions, results with interruptions and resumable RunState, shell-tool skills, and tracing with sensitive-data control. No prose change. **Cross-owner:** set R29 `checked_on` to 2026-10-11. |
| P2-A-12 | Ch 13 evidence row "Evaluation tooling" (~653), R20 | Confirmed Error (scope) | "Current evaluation platforms support…" generalizes from one source. R20 documents MLflow only: datasets, `@scorer` custom scorers, built-in LLM judges, and feedback attached to traces. | Now reads "MLflow's evaluation documentation covers…". |
| P2-A-13 | Ch 15 § Terminal correctness and run-state table (~1002, ~1012) | Potential Issue (internal consistency) | InterventionRequired was called "a valid terminal operational state". Yet the same section says "no run may close while an effect is Unknown", Ch 14 routes unsettled Unknown effects to InterventionRequired, and Ch 14's intervention responses (supply information, choose an alternative) resume the run. | Reworded: automated work stops, an intervention task opens, and the run closes only through that task's response. The table row now says "non-terminal until its response resolves the run". **Cross-owner (Part V):** `05-part-v.md:88` and `:371` group InterventionRequired with terminal child-task states. Check that the child's InterventionRequired is meant to be terminal *for the child*, and say so. |
| P2-A-14 | Ch 1 level one (~169) | Potential Issue (uncited number) | "training data that may be two years stale" is a quantitative claim with no source. | Now reads "training data frozen at a past cutoff". |
| P2-A-15 | Ch 4 (~92) | Potential Issue | "Seven planes is the smallest set that keeps every authoritative record in exactly one place" claims a minimality the chapter does not show. | Now reads "Seven planes are enough to keep…". |
| P2-A-16 | Ch 17 AP-12 (~1361) | Potential Issue (uncited empirical claim) | "Selection accuracy falls as the catalog grows" is stated as measured fact with no source. | Now reads "Selection gets harder as the catalog grows", followed by the existing mechanism sentence. |
| P2-A-17 | Ch 14 evidence row "Approval integrity" (~869), R15 | Needs Verification | The row is labelled "book-authored recommendation, informed by R15's mitigation guidance". The R15 landing page has no list content, and the PDF's mitigation text was not retrieved, so the "informed by" link could not be confirmed. | No change. The claim is already labelled book-authored. **Owner:** registry or citation owner, to confirm from the OWASP Agentic Top 10 PDF that a human-confirmation or approval mitigation exists (for example under ASI09), or else drop R15 from this row. |
| P2-A-18 | Ch 2 proposal JSON (~564–574) | Potential Issue (low) | The illustrative JSON uses top-level `tool` and `arguments`, an `uncertainty` string, and string evidence IDs. The registered `AgentDecision` uses `tool_call{tool_id, arguments}`, an `uncertainties` list, and `EvidenceRef`. The text claims only that the contract "defines the dispositions", so this is not an error. | No change. **Recommendation (Part I owner):** align the JSON to `AgentDecision`'s field names, or label it "simplified". |
| P2-A-19 | R45 (DMN), registry | Potential Issue (freshness) | The OMG list shows DMN 1.6 formal (September 2026). R45 pins 1.5 (August 2024). Chapter 5's prose has no version, so nothing reader-facing is wrong. | **Cross-owner (registry metadata):** keep 1.5 deliberately and say so, or move to 1.6 after checking that the hit-policy semantics cited are unchanged. |

**Freshness, no issue.** OpenAI Agents SDK v0.22.3, v0.23.0, and v0.23.1 exist. The book pins 0.22.2, says "pin", and never calls it latest. MLflow 3.17.0 exists against pinned 3.15.2 (R21), and no text in these Parts calls it current. The Microsoft Agent Framework and Google ADK pages still document the agent and workflow abstractions R31 and R32 record. The R48 44% sentence is still present verbatim in `ARCHITECTURE.md` §1.1, and the book's single-run wording matches it.

## Counts

| Measure | Count |
| --- | ---: |
| Claim–reference attachments checked | 47 (24 bracketed + 23 bare-ID) |
| Attachments with a finding | 21 |
| Attachments with no issue | 26 |
| Uncited-claim candidates assessed | 16 (3 findings) |
| Numeric, count, and table-consistency items checked | about 40 (1 finding: P2-A-13) |
| Living-dependency freshness checks | 7 (1 finding: P2-A-19) |
| **Findings** | **19**: 9 Confirmed Error (P2-A-01, 02, 03, 05, 06, 07, 08, 10, 12) / 9 Potential Issue (04, 09, 11, 13, 14, 15, 16, 18, 19) / 1 Needs Verification (17) |
| Fixed within ownership | 16 (P2-A-01 to P2-A-16). P2-A-17, 18, and 19 are recommendations only. P2-A-02, 10, 11, and 13 also carry cross-owner follow-ups. |

No reference lost its last citation. R02, R13, R16, R17, R20, R29, R31, R32, and R39 are all still cited. Validator after the change: 58 references, 147 bracketed citation occurrences, all 58 cited.

## Validation

`make assemble build references latex latex-validate validate` passed with `"errors": []` and `"pass": true`: 8/28/12, 57 code blocks, 42 diagram markers, 71 DOCX images, 0 contrast failures, 0 title mismatches. `make examples-run` ran 257 passed (1 warning) plus 30 mortgage-case tests passed. Generated artifacts were regenerated locally and left unstaged.

## What was not checked

- R15's mitigation text: the PDF was not retrieved (P2-A-17).
- R14 (ISO 42001) and other paywalled or unfetched sources. None is cited in these Parts.
- Live SDK behaviour beyond static introspection: no model calls were made.
- Every normative statement of MCP 2026-07-28: only the SEP-2640 existence and status relevant to Ch 8 were checked.
- Whether CloudEvents tooling in the companion code would actually reject the underscore names: the example code was not changed or executed against a CloudEvents SDK.
- The appendix, Part V, and registry follow-ups listed above, which are outside this ownership.
