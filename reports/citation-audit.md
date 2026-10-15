# Citation Audit — Book v1.0.0

**Result:** PASS
**References:** 64
**Citation occurrences:** 182
**Verified:** 2026-10-13

All sources were checked against their recorded claim scope. The audit validates attribution, not the book's independently authored architecture recommendations.

## Source-by-source status

| ID | Status | Method | Caveat |
|---|---|---|---|
| R01 | verified | direct primary-source review | arXiv abstract page fetched: title, authors, arXiv:2210.03629 (v1 6 Oct 2022) and the comment that v3 is the ICLR camera-ready version; year follows the ICLR 2023 venue. |
| R02 | verified | direct primary-source review | Temporal blog post by Tom Wheeler, published 6 May 2025 (shown on the page); registry year 2025 and label 'Temporal blog'. |
| R03 | verified | direct primary-source review | AWS Prescriptive Guidance page in 'Cloud design patterns, architectures, and implementations'; the page shows no publication or update date, so the year is n.d. |
| R04 | verified | direct primary-source review | Pinned to the CloudEvents 1.0.2 tag (released 6 Feb 2022), the latest released version. The main branch now carries the 1.0.3-wip draft, so the former main-branch link was a moving target. |
| R05 | verified | direct primary-source review | Versioned page fetched; it shows 'Version 2026-07-28 (latest)'. |
| R06 | verified | direct primary-source review | Versioned page fetched; it shows 'Version 2026-07-28 (latest)'. |
| R07 | verified_with_caveat | direct primary-source review | v1.0.1 page fetched; the GitHub v1.0.1 release is dated 28 May 2026 and is the latest release. The page's canonical tag points to /latest/ (the unreleased dev build), and its header names 1.0.0 as the latest protocol version because patch releases do not change protocol compatibility. |
| R08 | verified | direct primary-source review | RFC page fetched: RFC 8693, January 2020. |
| R09 | verified | direct primary-source review | RFC page fetched: RFC 8707, February 2020. |
| R10 | verified | direct primary-source review | RFC page fetched: RFC 9728, April 2025. |
| R11 | verified | direct primary-source review | CSRC publication page fetched: SP 800-207, published August 2020. |
| R12 | verified_with_caveat | direct primary-source review | Link moved from the AI RMF programme page to the NIST AI 100-1 DOI, which resolves to the January 2023 publication. NIST's programme page states that AI RMF 1.0 is being revised (concept note released 7 April 2026); re-check before the next release. |
| R13 | verified | direct primary-source review | DOI resolves (GET) to the official NIST AI 600-1 PDF (July 2024). |
| R14 | verified_with_caveat | IEC webstore publication record | iso.org returned 403 to automated clients (curl and fetch tool). The IEC webstore record (webstore.iec.ch/publication/90574, fetched) lists ISO/IEC 42001:2023, edition 1.0, published 18 December 2023, with no amendments. |
| R15 | verified | direct primary-source review | Page fetched: 'OWASP Top 10 for Agentic Applications for 2026', dated 9 December 2025 on the page; year 2025, 2026 edition. |
| R16 | verified | direct primary-source review | Living cheat sheet; the page shows no publication or update date, so the year is n.d. |
| R17 | verified | direct primary-source review | Version 1.2 page fetched, status Approved; the SLSA blog announced v1.2 in November 2025 (RC2 review closed 24 November 2025), so the year is 2025. |
| R18 | verified | direct primary-source review | cisa.gov/sbom now redirects to the topics URL recorded here; page title 'Software Bill of Materials (SBOM)'. No page-level date is shown, so the year is n.d. |
| R19 | verified | direct primary-source review | Repository README fetched; the conventions are in development status and the repository shows no release date, so the year is n.d. |
| R20 | verified | direct primary-source review | Pinned to the MLflow 3.15.2 documentation page (self-canonical), matching the R21 example baseline; the former docs/latest link moved with each release. 3.17.0 is the current PyPI release. |
| R21 | verified_with_caveat | official GitHub release record and PyPI metadata | mlflow.org returned 403 to automated clients (curl and fetch tool), so the page itself could not be read here. The official MLflow GitHub release v3.15.2 (published 26 August 2026) and PyPI metadata confirm the version and date. The pin is a reproducibility baseline, not a latest-version claim; 3.17.0 is current. |
| R22 | verified | direct primary-source review | Living documentation; the page shows no date and the version selector shows v4.2.8, so the year is n.d. and the version at access is recorded. |
| R23 | verified | direct primary-source review | Living documentation (page title 'What is Arize Phoenix?'); no visible date, so the year is n.d. |
| R24 | verified | direct primary-source review | Living documentation; the page shows a last-update date of December 11, 2025, so the year is 2025. |
| R25 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. |
| R26 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. |
| R27 | verified_with_caveat | direct primary-source review | Article published 19 December 2024. The page now carries a note that much of the tooling landscape it describes has changed since December 2024; cite it for the workflow/agent distinction, not as current tooling guidance. |
| R28 | verified | direct primary-source review | Article published 13 June 2025 (shown on the page). |
| R29 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. The pinned SDK baseline is R30. On 2026-10-13 the Running agents page (turn limit, sessions, RunState resumption, durable-execution integrations) and the Tracing page (enabled by default, OpenAI backend export, trace_include_sensitive_data default true) were re-read, and the defaults were confirmed in the v0.22.2 source: DEFAULT_MAX_TURNS = 10 and OPENAI_AGENTS_TRACE_INCLUDE_SENSITIVE_DATA defaulting to true. |
| R30 | verified | direct primary-source review | GitHub release v0.22.2 fetched; published 9 September 2026. Matches examples/requirements.txt. |
| R31 | verified | direct primary-source review | Living documentation; the page shows 'Last updated on 2026-08-25', so the year is 2026. |
| R32 | verified | direct primary-source review | Living documentation at adk.dev (self-canonical); no visible date, so the year is n.d. |
| R33 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. The page states Bedrock Agents Classic is in maintenance mode and closed to new customers; the manuscript records the caveat and AgentCore direction. |
| R34 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. |
| R35 | verified | direct primary-source review | The docs.llamaindex.ai workflow URL now redirects to the developers.llamaindex.ai page recorded here (self-canonical), which describes workflows as event-driven and step-based. No visible date, so the year is n.d. |
| R36 | verified | direct primary-source review | Living documentation for Pydantic AI; no visible date, so the year is n.d. |
| R37 | verified | direct primary-source review | Living documentation; the page shows 'Last modified October 8, 2026', so the year is 2026. |
| R38 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. |
| R39 | verified | direct primary-source review | EUR-Lex page fetched (HTTP 200): Regulation (EU) 2016/679 of 27 April 2016. The book does not provide legal advice. |
| R40 | verified | direct primary-source review | Commission policy page now titled 'AI Act'; it shows 'Last update 3 August 2026', so the year is 2026. Legal reliance must use the binding text. |
| R41 | verified | direct primary-source review | Pinned to the dated WCAG 2.2 Recommendation of 12 December 2024, the version /TR/WCAG22/ served at access (first published as a Recommendation in October 2023). |
| R42 | verified | direct primary-source review | CSRC publication page fetched: SP 800-61 Rev. 3, published April 2025. |
| R43 | verified_with_caveat | Crossref DOI metadata | The publisher returned 403 to automated clients. Crossref metadata confirms Little, J. D. C., 'A Proof for the Queuing Formula: L = λW', Operations Research 9(3):383-387, June 1961. |
| R44 | verified | OMG specification page | Version 2.0.2, formal, publication date January 2014; still the latest formal BPMN version. |
| R45 | verified_with_caveat | OMG specification page | Version 1.5, formal, August 2024, as cited. OMG has since published DMN 1.6 (formal, September 2026) and a 1.7 beta; the book's pin to 1.5 remains a valid citation but 1.5 is no longer the latest formal version. |
| R46 | verified | OMG specification page | Version 1.1, formal, December 2016; still the latest formal CMMN version. |
| R47 | verified | OMG specification page | Version 1.5, formal, December 2019; still the latest formal SBVR version. |
| R48 | verified_with_caveat | direct inspection of a read-only clone at commit c22dc450 (2026-09-11): ARCHITECTURE.md, docs/, and the modules and tests named in the registry scope; nothing executed | Book-authored project. Scope widened to the elements the book points at (registry supports text). The URL stays pinned to commit 393364f (4 September 2026), the latest change to ARCHITECTURE.md, whose content is identical at c22dc450. The book cites no measurement from this repository. The quality budget and decision-material claim classification are defined and tested but not wired into the pipeline stages. |
| R49 | verified | direct primary-source review | arXiv abstract page fetched: title, authors, arXiv:2308.08155, submitted 16 August 2023. |
| R50 | verified | direct primary-source review | arXiv abstract page fetched; comment 'Published in ICLR 2024'. Year follows the recorded venue (2024). |
| R51 | verified | direct primary-source review | arXiv abstract page fetched: title, authors, arXiv:2311.12983, submitted 21 November 2023. |
| R52 | verified | direct primary-source review | arXiv abstract page fetched (arXiv:2310.06770); the ICLR 2024 venue was confirmed from the project's published BibTeX. Year follows the recorded venue (2024). |
| R53 | verified | direct primary-source review | arXiv abstract page fetched: title, authors, arXiv:2406.12045, submitted 17 June 2024. |
| R54 | verified | direct primary-source review | arXiv abstract page fetched: title, authors, arXiv:2406.13352, submitted 19 June 2024. |
| R55 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. |
| R56 | verified | direct primary-source review | Living documentation; the page labels Managed Agents beta and shows no date, so the year is n.d. |
| R57 | verified | direct primary-source review | Living documentation; /en/introduction resolves to the current versioned path (v1.15.27) and shows no date, so the year is n.d. and the version at access is recorded. |
| R58 | verified | direct primary-source review | Living documentation; no visible date, so the year is n.d. |
| R59 | verified | direct primary-source review | Accessed 2026-10-14; scope limited to the registry supports text. |
| R60 | verified | direct primary-source review | Accessed 2026-10-14; scope limited to the registry supports text. |
| R61 | verified | direct primary-source review | Accessed 2026-10-14; scope limited to the registry supports text. |
| R62 | verified | direct primary-source review | Accessed 2026-10-14; scope limited to the registry supports text. |
| R63 | verified | direct primary-source review | Accessed 2026-10-14; scope limited to the registry supports text. |
| R64 | verified | direct primary-source review | Accessed 2026-10-14; scope limited to the registry supports text. |

## Errors

- None.

## Warnings

- None.
