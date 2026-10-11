# Reference registry audit (pass 2, D)

Branch `pass2/d`, based on `ece479a`. Checked 2026-10-11.

## Scope and method

- **Items:** all 58 entries in `config/references.json`, all 58 records in `config/reference-verification.json`, the registry header, `tools/check_references.py`, and Appendix K as `make assemble` renders it in `book/manuscript.md`.
- **Fetching:** every registry URL was fetched with a browser user agent (`curl -L`, GET), and title, date and version strings were extracted from the saved page. Pages that refused automated clients were checked another way: ISO 42001 through the IEC webstore record (fetched with WebFetch); Little (1961) through Crossref DOI metadata; MLflow 3.15.2 through the GitHub release API and PyPI. Version and date facts came from primary records: GitHub release/tag APIs for A2A, CloudEvents, SLSA, MLflow and the OpenAI Agents SDK; the OMG spec index pages; arXiv abstract pages; and the SLSA v1.2 announcement found by web search. The SWE-bench ICLR 2024 venue was confirmed from the project's published BibTeX because OpenReview returned a challenge page.
- **Not done:** claim-by-claim support for each `[Rxx]` occurrence, and any edit to `supports` text, which belongs to other agents. The prose fixes below are recommendations only; `source/parts/` was not edited.

## Dating rule adopted

1. **Dated works** (papers, RFCs, standards, laws, articles, blog posts): the year of the cited version. For papers, use the venue year when the registry names a peer-reviewed venue; otherwise use the arXiv v1 year.
2. **Pinned releases and versioned specs:** the year the pinned version was released. The URL must point at that version's page, not at `latest`, `main`, or `stable`.
3. **Living documentation** (unversioned "current" pages): use `n.d.` unless the page itself shows a publication or last-updated date. If it does, use that date's year and record the date in the verification caveat. Copyright footers and machine-only metadata (JSON-LD `dateModified`, site build stamps) do not count as a shown date. A version number that the page shows is recorded as "(vX at access)".
4. Every entry keeps an access date (`verification.checked_on`), which Appendix K renders as "Accessed …".

Rule 3 is now enforced in `tools/check_references.py`. A living entry with a numeric year fails unless its verification caveat contains that year. The year must be `YYYY` or `n.d.`, and each verification record's date must equal the registry `checked_on`.

## HTTP outcomes (GET, 2026-10-11)

200 for 55 of 58 URLs. Three returned 403 to automated clients: R14 (iso.org), R21 (mlflow.org) and R43 (the DOI resolver forwards to pubsonline.informs.org). R04 first returned 429 from GitHub's rate limit and 200 on retry. Redirects: R13 DOI → NIST PDF (200); R18 → CISA topics URL; R35 → developers.llamaindex.ai; R57 → the current versioned CrewAI path. Trailing-slash redirects on R07, R17, R24, R29, R31, R32 and R36 are not significant.

## Findings

| ID | Location | Status | Evidence | Change made / owner |
| --- | --- | --- | --- | --- |
| P2-D-01 | R02 | Confirmed Error | Page shows "Published May 06, 2025" (author Tom Wheeler) and the URL is a blog post. The registry said 2024 / "Temporal documentation", while the verification record claimed the year had already been corrected to 2025. | year 2024 → 2025; version "Temporal documentation" → "Temporal blog". |
| P2-D-02 | R04 | Confirmed Error | The `main` branch file is headed "CloudEvents - Version 1.0.3-wip", an unreleased draft. The latest release is `ce@v1.0.2` (2022-02-06). No source supports the year 2024. | year 2024 → 2022; version "CloudEvents 1.0.x" → "CloudEvents 1.0.2"; URL `…/blob/main/…` → `…/blob/v1.0.2/cloudevents/spec.md`. |
| P2-D-03 | R15 | Confirmed Error | The page is titled "OWASP Top 10 for Agentic Applications for 2026" and dated December 9, 2025. | year 2026 → 2025; title gains "for 2026". |
| P2-D-04 | R17 | Confirmed Error | SLSA blog: v1.2 was announced and approved in November 2025 (RC2 review closed 24 Nov 2025); the `v1.2` tag is on a 2025-11-24 commit. | year 2026 → 2025. |
| P2-D-05 | R50, R52 | Potential Issue | The year convention was inconsistent. R01 uses its venue year (ICLR 2023), but R50 and R52 named ICLR 2024 and used the arXiv year 2023. R50's arXiv comment says "Published in ICLR 2024"; SWE-bench's BibTeX names ICLR 2024. | R50 and R52 year 2023 → 2024. |
| P2-D-06 | R41 | Potential Issue | `/TR/WCAG22/` now serves the Recommendation dated 12 December 2024, so the registry year (2023) and the undated link no longer identify the version. | year 2023 → 2024; version → "W3C Recommendation, 12 December 2024"; URL → `https://www.w3.org/TR/2024/REC-WCAG22-20241212/`. |
| P2-D-07 | R20 | Potential Issue | A `docs/latest` URL with "MLflow 3.x", while the book pins 3.15.2 (R21) and PyPI's current release is 3.17.0. A self-canonical 3.15.2 page exists with the same scope terms. | version → "MLflow 3.15.2 documentation"; URL → `https://mlflow.org/docs/3.15.2/genai/eval-monitor/`. |
| P2-D-08 | R12 | Potential Issue | The URL was NIST's AI RMF programme page, not the NIST AI 100-1 publication. That page also says AI RMF 1.0 is being revised (concept note released 7 April 2026). | URL → `https://doi.org/10.6028/NIST.AI.100-1` (resolves to the publication PDF). The revision is recorded in the caveat; re-check before the next release. |
| P2-D-09 | R18 | Potential Issue | `cisa.gov/sbom` redirects; the page title is "Software Bill of Materials (SBOM)" and no page date is shown. | URL → `https://www.cisa.gov/topics/information-communications-technology-supply-chain-security/sbom`; title updated; year → n.d. |
| P2-D-10 | R35 | Potential Issue | The docs.llamaindex.ai URL redirects to the new docs site. The page is self-canonical and describes workflows as event-driven and step-based, so the scope still holds. | URL → `https://developers.llamaindex.ai/python/llamaagents/workflows/`; year → n.d. |
| P2-D-11 | R48 | Potential Issue | A repository-root URL backed a specific measured claim. The 44% sentence is in ARCHITECTURE.md §1.1 at `393364f` (2026-09-04), the latest commit that touches the file. | URL → commit permalink `…/blob/393364fae6700c10f4f6f7f024e67a63631a2f9a/ARCHITECTURE.md#11-the-evidence-spine`; version → "ARCHITECTURE.md §1.1 at commit 393364f". |
| P2-D-12 | R03, R16, R18, R19, R22–R26, R29, R31–R38, R40 | Confirmed Error (pass-1 open item) | The dating convention was inconsistent: R55–R58 used n.d. and the other living pages used 2026. Per page: R31 shows "Last updated on 2026-08-25", R37 "Last modified October 8, 2026", R40 "Last update 3 August 2026", R24 "December 11, 2025"; the rest show no date. | 15 entries → n.d. (R03, R16, R18, R19, R22, R23, R25, R26, R29, R32, R33, R34, R35, R36, R38). R24 2026 → 2025. R31, R37 and R40 keep 2026 because the page shows it. R22 and R57 record the version shown at access (v4.2.8, v1.15.27). |
| P2-D-13 | R45 verification record | Confirmed Error (stale record) | The record said "1.5 is the latest formal version". The OMG DMN index now lists DMN 1.6 as formal (September 2026), plus a 1.7 beta. | Caveat updated; the pin to 1.5 is kept, since it is still a valid citation and no prose claims "latest". **Integrator / scope owner:** decide whether to re-pin to 1.6, which needs a scope re-check of decision tables, hit policies and FEEL. |
| P2-D-14 | R03 | Potential Issue | "AWS Prescriptive Guidance" is the publication series, not the author. The page sits in the guide "Cloud design patterns, architectures, and implementations" and shows no date. | author → "Amazon Web Services"; version → "AWS Prescriptive Guidance: Cloud design patterns, architectures, and implementations"; year 2024 → n.d. |
| P2-D-15 | R33, R36, R40 titles | Potential Issue | Page titles have changed: "Use multi-agent collaboration with Amazon Bedrock Agents"; product name "Pydantic AI"; Commission page title "AI Act". | Titles updated to match the pages. |
| P2-D-16 | Registry header | Confirmed Error | `citation_style` said `[R01]…[R54]` while the registry holds 58 entries; `verified_on` was 2026-09-13. | `[R54]` → `[R58]`; `verified_on` → 2026-10-11. |
| P2-D-17 | `tools/check_references.py` | Confirmed Error | `reports/citation-audit.md` and `citation-verification.json` hard-coded "Verified 2026-09-13" whatever the registry said. The living-doc rule only warned, and it accepted a hard-coded "2026". | Dates now read `verified_on`. Added the dating rule, a `YYYY`/`n.d.` format rule, and a record-date consistency rule. Negative tests on a temp copy produced the expected errors for each rule. |
| P2-D-18 | R21 | Needs Verification | mlflow.org returns 403 to curl and to the fetch tool, so the page itself cannot be read here. The GitHub release v3.15.2 (2026-08-26) and PyPI confirm the version and date. I tried switching the URL to the GitHub release, but `tools/validate_book.py:145` (stale-label regex `\bv(?:2\|3)\.\d+`) flags "v3.15.2" in the tag URL, so I reverted. | URL kept; caveat records the cross-check. **Validator owner:** if a verifiable link is preferred, exempt URLs from the stale-label regex and use `https://github.com/mlflow/mlflow/releases/tag/v3.15.2`. A human browser check of the mlflow.org page is still open. |
| P2-D-19 | R27 | Potential Issue (freshness) | The page now notes that "much of the tooling landscape described in this post has changed since December 2024". The book cites it only for the workflow/agent distinction (Ch 4 Evidence context; Appendix item 7), which the note does not affect. | Caveat records it. **Scope owner (optional):** append "does not support current tooling claims" to R27 `supports`. |
| P2-D-20 | `source/parts/09-appendices.md` Appendix K body | Potential Issue | The source holds a static copy of the Appendix K list and matrix. The assembler overwrites it, and the copy is already stale (no R55–R58, old access dates), which misleads anyone editing the source. | **Integrator:** replace the body with a one-line note that it is generated from `config/references.json` (assembly replaces everything between the Appendix K and L headings), or regenerate it. |
| P2-D-21 | Appendix K grouping (`tools/assemble_manuscript.py` `category_order`) | Potential Issue | WCAG (R41) and the OMG notations (R44–R47) render under "Protocols, identity, and event standards", which describes none of them. | Not changed (rendering choice, not a registry rule). **Integrator:** rename the heading to "Protocols and technical standards". |
| P2-D-22 | `09-appendices.md` lines 265, 280, 312, 565 | Potential Issue | The prose says "PydanticAI"; the vendor now writes "Pydantic AI" (R36 page and nav). | **Prose owner:** "PydanticAI" → "Pydantic AI". |
| P2-D-23 | `07-part-vii.md` line 556 | Potential Issue (minor) | "MLflow 3.x documents …" is still true, but R20 now pins the 3.15.2 docs. | **Prose owner (optional):** "MLflow 3.x" → "MLflow 3.15.2". |

## Verified with no metadata change (27)

R01, R05, R06, R07, R08, R09, R10, R11, R13, R14, R28, R30, R31, R37, R39, R42, R43, R44, R46, R47, R49, R51, R53, R54, R55, R56, R58. Only their access dates changed, and their verification records were refreshed. Notes:

- **R05/R06:** each page shows "Version 2026-07-28 (latest)".
- **R07:** v1.0.1 is the latest GitHub release (2026-05-28). The page's canonical tag points to `/latest/` (dev), and its header names protocol version 1.0.0 because patch releases do not change compatibility. The URL is correctly pinned.
- **R30:** published 2026-09-09; matches `examples/requirements.txt`.
- **R44/R46/R47:** still the latest formal BPMN, CMMN and SBVR versions.
- **R14:** IEC webstore: ISO/IEC 42001:2023, edition 1.0, published 2023-12-18.
- **R43:** Crossref: Operations Research 9(3):383–387, June 1961.
- **R01, R08–R11, R13, R39, R41:** previously caveated because extraction timed out; now fetched directly and marked `verified`.
- **R49–R54:** the records had no `caveat` field; one was added.

## Registry consistency (task 4)

- **Ids:** both files hold the same 58 ids in the same order, numbered R01–R58 with no gaps.
- **Dates:** every verification record's `verified` equals the registry `checked_on` (2026-10-11), and the checker now enforces this.
- **Duplicates:** no duplicate URLs or sources.
- **Appendix K:** renders all 58 entries in four categories (8 research, 13 standards, 12 governance, 25 frameworks), none uncategorised, each with "Accessed 11 October 2026". R14 sits under governance as pass 1 intended.
- **Statuses:** 50 `verified`, 8 `verified_with_caveat` (R07, R12, R14, R21, R27, R43, R45, R48).

## Full metadata change list (old → new)

All 58 entries: `verification.checked_on` 2026-09-13 / 2026-09-14 / 2026-10-10 → 2026-10-11. The header changes and the R02–R57 field changes are listed in the findings table. Every verification record got a new `verified` date, `method` and `caveat`, and statuses moved as follows:

- R01, R08, R09, R10, R11, R13, R39, R41: `verified_with_caveat` → `verified`.
- R12, R21, R27, R45: → `verified_with_caveat`.
- R07, R14, R43, R48: stay `verified_with_caveat`.

**Integrator merge note:** the URL changes (R04, R12, R18, R20, R35, R41, R48) sit on the line directly above `supports`. If a scope agent also edited `supports` on those entries, git will report a textual conflict; keep both edits. `checked_on` edits are two lines below `supports` and merge cleanly (tested).

## Counts

Checked 58 references plus the header, checker and renderer.

| Checked | Confirmed | Potential | Needs verification | No issue |
| ---: | ---: | ---: | ---: | ---: |
| 58 references + 3 registry artifacts | 8 (P2-D-01–04, 12, 13, 16, 17) | 14 (P2-D-05–11, 14, 15, 19–23) | 1 (P2-D-18) | 27 references |

The last five Potential items (P2-D-19–23) are recommendations for other owners; the other 22 findings are fixed in this branch.

## Could not check

- The mlflow.org release page (R21) and the iso.org page (R14) could not be read by automated clients.
- OpenReview was blocked by a challenge page.
- Claim-level support and scope text are out of my ownership.
- Visible "last updated" dates rendered only by client-side JavaScript would not appear in the static HTML I parsed. Mintlify pages (R23, R25, R34, R55, R57, R58) expose only a machine `dateModified`, which the rule deliberately ignores.

## Validation

`make assemble build references latex latex-validate validate`: pass (references 58, citation occurrences 147, 0 errors/warnings; validate 8/28/12, 0 errors). `make examples-run`: pass (30 mortgage-case tests). Generated artifacts are left unstaged.
