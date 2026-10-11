# Reference URL access check

Baseline `6ebbc8b`; checked 2026-10-10. Every registered URL received an HTTP HEAD request following redirects (`curl -L -I`, 12-second timeout). These are access results from this client, **not content-support verification**. Non-200 responses may be anti-bot, subscription or HEAD-specific behavior; do not call them broken without a GET/official-source check.

Result: 54/54 attempted; HEAD statuses 200: 49, 202: 1, 403: 3, 404: 1. [Post-sweep note, 2026-10-11: the registry now holds 58 references. R55–R58 (Claude Agent SDK overview, Claude Managed Agents overview, CrewAI introduction, Restate documentation) were registered by the corrective PR after this sweep and are not in the table below; their 2026-10-10 verification records are in `config/reference-verification.json`. R39 returned 200 on a 2026-10-10 re-check (see below).]

| ID | HEAD | Registry URL |
| --- | ---: | --- |
| R01 | 200 | [source](https://arxiv.org/abs/2210.03629) |
| R02 | 200 | [source](https://temporal.io/blog/what-is-durable-execution) |
| R03 | 200 | [source](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) |
| R04 | 200 | [source](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) |
| R05 | 200 | [source](https://modelcontextprotocol.io/specification/2026-07-28) |
| R06 | 200 | [source](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) |
| R07 | 200 | [source](https://a2a-protocol.org/v1.0.1/specification) |
| R08 | 200 | [source](https://datatracker.ietf.org/doc/html/rfc8693) |
| R09 | 200 | [source](https://datatracker.ietf.org/doc/html/rfc8707) |
| R10 | 200 | [source](https://datatracker.ietf.org/doc/html/rfc9728) |
| R11 | 200 | [source](https://csrc.nist.gov/pubs/sp/800/207/final) |
| R12 | 200 | [source](https://www.nist.gov/itl/ai-risk-management-framework) |
| R13 | 404 | [source](https://doi.org/10.6028/NIST.AI.600-1) |
| R14 | 403 | [source](https://www.iso.org/standard/42001) |
| R15 | 200 | [source](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| R16 | 200 | [source](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) |
| R17 | 200 | [source](https://slsa.dev/spec/v1.2) |
| R18 | 200 | [source](https://www.cisa.gov/sbom) |
| R19 | 200 | [source](https://github.com/open-telemetry/semantic-conventions-genai) |
| R20 | 200 | [source](https://mlflow.org/docs/latest/genai/eval-monitor/) |
| R21 | 403 | [source](https://mlflow.org/releases/3.15.2) |
| R22 | 200 | [source](https://deepeval.com/docs/metrics-introduction) |
| R23 | 200 | [source](https://arize.com/docs/phoenix) |
| R24 | 200 | [source](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/agents) |
| R25 | 200 | [source](https://docs.langchain.com/langsmith/evaluation) |
| R26 | 200 | [source](https://developers.openai.com/api/docs/guides/agent-evals) |
| R27 | 200 | [source](https://www.anthropic.com/engineering/building-effective-agents) |
| R28 | 200 | [source](https://www.anthropic.com/engineering/multi-agent-research-system) |
| R29 | 200 | [source](https://openai.github.io/openai-agents-python) |
| R30 | 200 | [source](https://github.com/openai/openai-agents-python/releases/tag/v0.22.2) |
| R31 | 200 | [source](https://learn.microsoft.com/en-us/agent-framework/overview) |
| R32 | 200 | [source](https://adk.dev/agents) |
| R33 | 200 | [source](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html) |
| R34 | 200 | [source](https://docs.langchain.com/oss/python/langgraph/persistence) |
| R35 | 200 | [source](https://docs.llamaindex.ai/en/stable/module_guides/workflow/) |
| R36 | 200 | [source](https://pydantic.dev/docs/ai/capabilities/durable_execution/overview) |
| R37 | 200 | [source](https://docs.dapr.io/developing-ai/dapr-agents) |
| R38 | 200 | [source](https://docs.dbos.dev/ai/ai-quickstart) |
| R39 | 202 | [source](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |
| R40 | 200 | [source](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) |
| R41 | 200 | [source](https://www.w3.org/TR/WCAG22/) |
| R42 | 200 | [source](https://csrc.nist.gov/pubs/sp/800/61/r3/final) |
| R43 | 403 | [source](https://doi.org/10.1287/opre.9.3.383) |
| R44 | 200 | [source](https://www.omg.org/spec/BPMN/2.0.2) |
| R45 | 200 | [source](https://www.omg.org/spec/DMN/1.5) |
| R46 | 200 | [source](https://www.omg.org/spec/CMMN/1.1) |
| R47 | 200 | [source](https://www.omg.org/spec/SBVR/1.5) |
| R48 | 200 | [source](https://github.com/rrahimi-uci/policy-logic-forge) |
| R49 | 200 | [source](https://arxiv.org/abs/2308.08155) |
| R50 | 200 | [source](https://arxiv.org/abs/2308.03688) |
| R51 | 200 | [source](https://arxiv.org/abs/2311.12983) |
| R52 | 200 | [source](https://arxiv.org/abs/2310.06770) |
| R53 | 200 | [source](https://arxiv.org/abs/2406.12045) |
| R54 | 200 | [source](https://arxiv.org/abs/2406.13352) |

## Exceptions checked after HEAD

- **R13:** HEAD returned 404 at the DOI resolver, but a redirected GET returned 200 at the [official NIST PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf); [NIST's publication page](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) confirms the DOI. Not a broken reference.
- **R14:** ISO returned 403 to this automated client. Access was not proven broken or claim support proven; a human browser/authorized standards access is needed.
- **R21:** MLflow returned 403 to this automated client; the [official MLflow 3.15.2 release page](https://mlflow.org/releases/3.15.2/) was independently discoverable via web indexing, and the pinned package installed and tests ran. Access restriction is not proof of a bad URL.
- **R39:** EUR-Lex returned 202 to HEAD, which is an accepted response rather than a loaded document. Verify the legal text in a browser before legal reliance. [Re-checked 2026-10-10 during the corrective PR's spot-check: HEAD now returns 200. The 202 was transient server behaviour, not a URL problem.]
- **R43:** DOI resolved to the publisher but returned 403 to this client. The [DOI record](https://doi.org/10.1287/opre.9.3.383) and paper title were checked separately; full text may require access.

No HEAD result certifies the reference's author, year, version, or support for every book claim. The substantive scope findings are in [evidence-ledger.md](evidence-ledger.md).

[audited 2026-10-10: the 54 ids and URLs in the table are identical to `id`/`url` in `config/references.json` (no missing, extra or altered entries) and the 200/202/403/404 tally of 49/1/3/1 matches the rows. The R13 follow-up was re-confirmed: `GET https://doi.org/10.6028/NIST.AI.600-1` redirects to `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` and returns 200, although a HEAD on the PDF itself returns 404 — so the 404 is HEAD-specific, not a broken DOI. The 54 HEAD requests were not re-run by the audit; a separate spot-check covers five of them.]
