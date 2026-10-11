# Pass 2 — citations, numbers, and freshness: Part V to the appendices

**Branch:** `pass2/b` (based on `fix/correctness-review-findings`). **Date:** 2026-10-11. **ID prefix:** P2-B.
**Ownership:** `source/parts/05-part-v.md` to `09-appendices.md` (Chapters 18–28, Closing Perspective, Appendices A–L). In `config/references.json`, only the `supports` text of references whose primary source was fetched today.

## Scope and method

1. **Claim-level citation support.** Every reference ID outside Appendix K was read in its sentence, row, or callout: 135 ID occurrences on 56 lines, which is 45 claim sites plus 11 "The discussion above draws on…" summaries. Bare IDs in "Source IDs" columns are included. Each site was compared with the reference's recorded `supports` scope. Where a claim named a version, behaviour, protocol rule, status, or number, the primary source was fetched. The Appendix D evidence callout carries 21 IDs, and all 15 Appendix D rows were checked against them cell by cell. The 7 Appendix E rows were checked against R01 and R49–R54.
2. **Appendix K.** `tools/assemble_manuscript.py` (`render_reference_sections`) regenerates Appendix K from the registry, so its 58 + 58 generated entries are registry renderings, not separate claims. 18 recorded scopes were checked against primary sources fetched today: R01, R05, R06, R07, R13, R15, R19, R20, R28, R29, R31, R33, R37, R38, R40, R51, R56, R57.
3. **Uncited factual claims.** Product, protocol, and regulatory statements in the owned Parts were checked. That includes SDK behaviour stated in Chapter 24, which was checked against the installed pinned packages.
4. **Numbers and tables.** Checked: Chapter 24's twelve-minute timeline; Chapter 28's 120/min × 4 min ≈ 480 permits and its 25 % reserve; all six Appendix L formulas; every enumerated count in the text (nine layers, eight field groups, seven recovery steps, three release rules, four trace questions, five segments, ten loop stages, last four Appendix A rows, seven-plus-one incident phases); the Chapter 18 lifecycle (7 rows) against the Chapter 19 A2A mapping (10 rows) and the A2A enum (9 values); Appendix C records against their chapter definitions (spot check of 8); the Closing Perspective table against Chapter 1's week; and the Appendix I version pins against `examples/requirements.txt`, `pyproject.toml`, CI workflows, and the installed dist-info.
5. **Freshness.** MCP, A2A, AWS Bedrock, Microsoft Agent Framework, Google ADK, LangGraph, PydanticAI, Dapr Agents, DBOS, CrewAI, Claude Managed Agents, MLflow, OpenAI Agents SDK, OpenTelemetry GenAI, OWASP, the EU AI Act, and NIST AI 600-1 were checked against current official pages. LlamaIndex, Restate, Temporal, Claude Agent SDK, DeepEval, Phoenix, Ragas, LangSmith, OpenAI evals, SLSA, CISA, and NIST SP 800-61 were checked for URL reachability only.

**Primary sources fetched 2026-10-11:**

- **MCP 2026-07-28:** changelog, Authorization, Authorization Security Considerations, and Extensions overview. `/specification/latest` redirects to 2026-07-28.
- **A2A:** v1.0.1 specification. GitHub releases show v1.0.1 (2026-05-28) as the latest.
- **AWS, Microsoft, Google, LangChain, Pydantic:** the AWS Bedrock multi-agent collaboration page, Microsoft Agent Framework overview (updated 2026-08-25), ADK agents, LangGraph persistence, and PydanticAI durable execution.
- **Dapr Agents:** index page and "Why Dapr Agents".
- **DBOS AI quickstart, CrewAI introduction, Claude Managed Agents overview.**
- **OpenAI Agents SDK:** index, Agents, and Human-in-the-loop pages.
- **OpenTelemetry:** the `opentelemetry.io` GenAI page and the `semantic-conventions-genai` repository, including `docs/gen-ai/gen-ai-agent-spans.md` (Status: Development).
- **OWASP:** Top 10 for Agentic Applications 2026, as the full PDF (57 pp.).
- **NIST:** AI 600-1 PDF.
- **EU AI Act:** European Commission regulatory-framework page.
- **Research and industry papers:** arXiv abstracts for ReAct and GAIA, and Anthropic's multi-agent research article.
- **PyPI:** JSON for `mlflow`, `openai-agents`, and `openai`.
- **Installed sources:** `mlflow/openai/autolog.py`, `mlflow/openai/_agent_tracer.py`, `agents/tracing/processors.py`, and the `openai_agents-0.22.2` METADATA in the pinned example environment.

## Findings

| ID | Location | Status | Evidence | Change made or recommended owner |
| --- | --- | --- | --- | --- |
| P2-B-01 | Ch 24 § MLflow tracing integration (`07-part-vii.md`) | **Confirmed Error** | The book said the examples pass `disable_openai_agent_tracer=False` "to register MLflow's Agents SDK trace processor". In MLflow 3.15.2, `autolog` calls `add_mlflow_trace_processor()` whatever the flag (`autolog.py` l. 95–101). With the default `True` it first calls `clear_trace_processors()`, which removes the SDK's `BatchTraceProcessor` exporter to `api.openai.com/v1/traces/ingest`. A probe confirmed it: default → `[MlflowOpenAgentTracingProcessor]`; `False` → `[BatchTraceProcessor, MlflowOpenAgentTracingProcessor]`. `make examples-run` prints "OPENAI_API_KEY is not set, skipping trace export", so the provider exporter is live in the examples. | Rewrote the sentence: MLflow's processor is registered either way, the flag decides whether the provider exporter is removed, and a deployment that must keep traces in-house should keep the default. **Owner: examples.** `examples/README.md` l. 75–76 and the comment in `examples/observability/mlflow_trace_configuration.py` (~l. 30) repeat the wrong reason. Correct them, and consider dropping `disable_openai_agent_tracer=False` in both examples (`mortgage_agents_mlflow.py` l. 48). The test asserting the default `True` stays valid. |
| P2-B-02 | App D, CrewAI row (pass-1 open item) | **Confirmed Error** (unsupported) | CrewAI's introduction never says "rapid prototyping", "prototype", "fast", or "lean". It calls itself production-ready ("For any production-ready application, start with a Flow"). R57 supports Crews and Flows only. | Strength now reads: Crews of role-playing agents with specific goals and tools, and event-driven Flows that manage state and control execution. "Accessible" was removed too. The "Recommended placement" column remains book judgment. |
| P2-B-03 | App D, Dapr Agents row | **Confirmed Error** (overreach) | "Why Dapr Agents" names workflows, actors, state, pub/sub, resiliency policies, and distributed tracing. It does not mention secrets or OpenTelemetry. R37's scope has no secrets. | Row now lists workflows, actors, state, pub/sub messaging, resiliency policies, and distributed tracing. |
| P2-B-04 | App D, PydanticAI row | Potential Issue | R36 (the durable-execution page) supports typed agents and backends: Temporal, DBOS, Prefect, Restate, and others. It does not cover model-provider abstraction or OpenTelemetry orientation. | Narrowed to typed agents with durable-execution integrations, naming the four co-maintained backends. |
| P2-B-05 | App D, Google ADK row | Potential Issue | The R32 page does not describe Google Cloud integration. The row also said "A2A 1.0", while the book pins 1.0.1. | Strength now reads "Composable model-driven agents, tools, and multi-agent workflows; A2A 1.0.1 defines…". |
| P2-B-06 | App D, Claude row | Potential Issue | The row said Managed Agents "hosts that harness", meaning the Agent SDK's harness. R56 describes a pre-built hosted harness and does not say it is the Claude Code loop. Beta status was confirmed today (`managed-agents-2026-04-01`). | Reworded as "a hosted agent harness, documented as beta". Sandboxes are now named "Anthropic-managed or self-hosted", as R56 does. |
| P2-B-07 | App D, Bedrock row; R33 | Potential Issue (scope gap) | The AWS page confirms Bedrock Agents is "now Amazon Bedrock Agents Classic", "no longer open to new customers", and points to AgentCore. The claim is true, but R33's recorded scope covered only the supervisor/collaborator pattern. | Widened R33 `supports` to record the maintenance status and the AgentCore pointer, using text fetched today. |
| P2-B-08 | App D, Microsoft Agent Framework row; R31 | Potential Issue (scope gap) | The overview confirms that it combines and succeeds AutoGen and Semantic Kernel, with sessions, middleware, type safety, telemetry, graph workflows, and providers. Go is in public preview, and the .NET Foundry package installs with `--prerelease`. R31's scope said only "agent and workflow abstractions". | Widened R31 `supports`. |
| P2-B-09 | App D, OpenAI Agents SDK row; R29 | Potential Issue (scope gap) | The row named MCP, HITL, RunState, sandbox, and structured outputs, which were outside R29's scope. The docs fetched today document all five: MCP integration, human-in-the-loop with `result.to_state()` / `RunState` serialization, sandbox agents, and `output_type` structured outputs. | Widened R29 `supports`. |
| P2-B-10 | App D, trend 6 | Potential Issue | "OWASP's agentic list centers on privileged action under manipulated context" was an interpretation not found in R15. The PDF ranks ASI01 Agent Goal Hijack, ASI02 Tool Misuse and Exploitation, and ASI03 Identity and Privilege Abuse first. | Replaced with that verifiable ranking. |
| P2-B-11 | Ch 21, "Non-human identity" evidence row | **Confirmed Error** (overreach) | The row cited R06 (MCP Authorization) for workload identity, delegation purpose, and rotation. R06 defines HTTP authorization for MCP, not workload identity. R08 supports only the subject/actor distinction. | Row now credits R08 with the subject/actor distinction and labels the rest as the book's recommendation. R06 was dropped from the row and its summary line; it stays cited in Ch 19 and App D. |
| P2-B-12 | Ch 23, "Incident control" row | Potential Issue | The row presented book-authored kill-switch scopes and evidence-preservation rules as sourced to R15. The OWASP PDF recommends a "supply chain kill switch" that can "instantly disable specific tools, prompts, or agent connections" and "kill-switches and credential revocation to instantly disable rogue agents". | Split the row: R15's recommendation, then the book's extensions labelled as such. |
| P2-B-13 | Ch 23 "Supply-chain admission" and Ch 27 "Supply chain" rows | Potential Issue | Book recommendations (verify both at admission; pin model, prompt, Skill, policy, and evaluation digests) sat unlabelled under R17 and R18. | Labelled them as book recommendations. Ch 27 now adds that SLSA provenance identifies the builder. |
| P2-B-14 | Ch 25, "Evaluation limit" row | Potential Issue | "Protect against benchmark leakage and tune judges with human feedback" and the release-blocker rule were attributed to R20 and R13. R20's page documents judges and trace-attached human feedback; it does not document judge alignment. NIST AI 600-1 MS-2.11-001 asks evaluators to document "possible training/test data cross contamination". | Row now states what each source says. The release-blocker rule is labelled as the book's recommendation. |
| P2-B-15 | App E, GAIA row | Potential Issue (minor) | The row listed "browsing, files, multimodality, and tools". The abstract and R51's scope say "reasoning, multi-modality handling, web browsing, and … tool-use". | Aligned the wording with the abstract. |
| P2-B-16 | Ch 26 § Make review predictable | **Confirmed Error** (inconsistency) | "Incidents enter the daily review", but the cadence table defines the row as "Daily or weekly". | Now reads "daily or weekly review". |
| P2-B-17 | App K body in `source/parts/09-appendices.md` | Potential Issue (not reader-facing) | The source copy lists only R01–R54 in both the bibliography and the matrix. The assembler replaces everything between `# Appendix K — References` and `# Appendix L —`, so `book/manuscript.md` correctly shows 58. A maintainer editing the source copy would be misled. | Not changed: an edit would conflict across four branches and be overwritten anyway. **Owner: tooling/registry.** Replace the source body with a one-line generated-content note, or have `make assemble` write the rendered section back. |
| P2-B-18 | `config/references.json` → `citation_style` | **Confirmed Error** (metadata) | The string reads "Numbered source identifiers [R01]…[R54]", but the registry holds R01–R58. | **Owner: registry metadata.** Change it to "[R01]…[R58]" or to wording without a count. |
| P2-B-19 | R35 and R18 URLs | Potential Issue | R35 redirects to `https://developers.llamaindex.ai/python/llamaagents/workflows/`. R18 redirects to `https://www.cisa.gov/topics/information-communications-technology-supply-chain-security/sbom`. Both resolve (200). | **Owner: registry metadata.** Update both URLs to the redirect targets after confirming the scopes still hold. |
| P2-B-20 | R21 (MLflow 3.15.2 release page) | Needs Verification | The page returns 403 to automated clients, so its content could not be read. The pin itself is verified: `mlflow-3.15.2.dist-info` is installed, the PyPI upload is dated 2026-08-26, and `examples/requirements.txt` matches. | No change. Re-read the page in a browser before release. |

### Checked with no issue (summary)

- **MCP 2026-07-28 (R05, R06; Ch 19 and App D).** All checked claims match the spec:
  - The core is stateless.
  - `initialize`/`notifications/initialized` and `Mcp-Session-Id` are removed.
  - Protocol version and capabilities travel in `_meta`.
  - `server/discover` is a MUST and serves up-front version selection.
  - Cross-call state uses explicit server-minted handles.
  - Tasks moved to an official extension, and Skills over MCP is an official extension. Extensions are disabled by default.
  - Authorization is OPTIONAL; PKCE is a MUST.
  - RFC 8707 audience validation and RFC 9728 discovery are required.
  - Short-lived tokens are a SHOULD.
  - Step-up scope challenges and RFC 9207 issuer validation are defined.
  - "MUST NOT pass through the token".
  - Ch 24's W3C trace context propagation across MCP matches the spec's `_meta` trace-context conventions.
  - The "SSRF-safe metadata retrieval" recommendation is a borderline reading: the spec names SSRF risk only for authorization servers fetching Client ID Metadata Documents. It is left as an engineering recommendation.
- **A2A v1.0.1 (R07).**
  - Operations match the spec: SendMessage, SendStreamingMessage, GetTask, ListTasks, CancelTask, SubscribeToTask, plus push-config operations and GetExtendedAgentCard.
  - All nine TaskState values match, including AUTH_REQUIRED and REJECTED.
  - Cancellation "success is not guaranteed".
  - Servers "MUST NOT reveal the existence of resources the client is not authorized to access".
  - The Ch 18/19 lifecycle mapping is complete and consistent.
- **R19.** GenAI conventions moved to the dedicated repository. Agent spans are marked Development. MCP and provider mappings are present.
- **Other sources.**
  - **R28:** confirms the orchestrator-worker architecture and the token trade-offs (about 4× chat for agents, about 15× for multi-agent).
  - **R40:** the risk categories and provider/deployer split match. Freshness: the AI Omnibus entered into force on 2026-07-27, putting Annex III high-risk obligations at 2 Dec 2027 and Annex I at 2 Aug 2028. The book's "phase in by date … confirm the current timeline" stays correct, and no change is needed.
  - **R01, R51:** the abstract claims match.
  - **R34:** documents checkpointers, threads, stores, HITL, time travel, and fault tolerance.
  - **R38:** documents durable workflows, queues, framework integrations, Python/TypeScript, and database-backed state.
  - **R56:** confirms beta status, agents, environments, sessions, SSE, and persisted history.
- **Numbers.**
  - Ch 24: 3 + 2 + 4 + 3 = 12 min, matching the text.
  - Ch 28: 120/min × 4 min = 480 (L = λW, steady state).
  - App L: the retry multiplier is the correct geometric sum for independent retries, and the permit-pool formula and token/cost formulas are dimensionally consistent.
  - Every enumerated count matches its list.
  - The Closing Perspective matches Chapter 1's Monday to Friday.
  - Appendix I pins match the requirements: openai-agents 0.22.2 declares `openai<4,>=3.0.0`, and openai 3.13.0 is installed.
  - Newer releases exist (mlflow 3.17.0, openai-agents 0.23.1, openai 3.28.0). The book correctly never calls its pins "latest".

## Counts

| Checked | Confirmed | Potential | Needs verification | No issue |
| ---: | ---: | ---: | ---: | ---: |
| ≈218 | 6 | 13 | 1 | ≈198 |

The ≈218 checked items are:

- 135 citation ID occurrences
- 15 Appendix D rows
- 18 registry scopes checked against primary sources
- about 30 number and table items
- 20 freshness sources

Counts are findings, not sentences. "No issue" means checked and not contradicted, not certified.

## Changes made (canonical files only)

- `source/parts/06-part-vi.md`: P2-B-11, P2-B-12, P2-B-13 (Ch 23).
- `source/parts/07-part-vii.md`: P2-B-01, P2-B-14.
- `source/parts/08-part-viii.md`: P2-B-13 (Ch 27), P2-B-16.
- `source/parts/09-appendices.md`: P2-B-02 to P2-B-06, P2-B-10, P2-B-15.
- `config/references.json` (`supports` text only): R29, R31, R33.

Every reference is still cited: validator reports 58 references, 58 cited, 147 bracketed occurrences.

## Not checked, and why

- **Pages read only partly or not at all:**
  - The A2A spec past character 100 000 was not read; that covers AgentSkill fields and agent-card signing detail.
  - LlamaIndex, Restate, Temporal, DeepEval, Phoenix, Ragas, LangSmith, OpenAI evals, SLSA, CISA, and NIST SP 800-61 were checked for reachability, not content. Pass 1 verified their scope wording; their citing sentences here make only generic claims.
  - The R21 page content is blocked (403).
  - R11, R12, R14, R39, R41, and R42 are stable standards or law, and their citing sentences stay within the recorded scope. Their texts were not re-read.
- **Visual and print checks:** no print-scale or visual inspection, and no DOCX or XeLaTeX PDF review (`make pdf` and `make qa-pdf` were not run).
- **Examples:** the example code, README, and tests are outside this ownership (see P2-B-01).
- **Environment:** the pinned example environment runs Python 3.14.4, while `pyproject.toml` declares `>=3.13,<3.14` and CI uses 3.13. Appendix I correctly says 3.13. This concerns the local environment, not the book.

## Validation

`make assemble build references latex latex-validate validate` passes with no errors or warnings: 8/28/12 topology, 58 references and 58 cited, 147 citation occurrences, 42 diagram markers, 57 code blocks, 71 DOCX images, 0 contrast failures, 0 title mismatches. `make examples-run` gives 257 passed (1 warning) for the examples and 30 passed for the mortgage case.
