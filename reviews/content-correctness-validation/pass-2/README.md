# Correctness validation — pass 2

Pass 1 (the files one level up, PR #81, fixes in PR #82) was a bounded issue ledger. Its overall report listed what it did not do: claim-level support for every citation, number and table checks, print-scale inspection of every visual, freshness of living vendor and protocol claims, and registry metadata. Pass 2 does those, against the text as corrected by PR #82, and fixes what is really wrong. Work date: 2026-10-11.

## Reports

| Report | Scope | Checked | Confirmed | Potential | Needs verification |
| --- | --- | --- | ---: | ---: | ---: |
| [Citations and numbers: front matter to Part IV](citations-and-numbers-front-to-part-iv.md) | Ch 01–17 | 47 claim–reference links, 16 uncited claims, ~40 numbers and tables, 7 freshness checks | 9 | 9 | 1 |
| [Citations and numbers: Part V to appendices](citations-and-numbers-part-v-to-appendices.md) | Ch 18–28, Closing Perspective, Appendices A–L | ~221 items, including 135 citation occurrences and all 15 Appendix D rows | 9 | 13 | 1 |
| [Reference registry audit](reference-registry-audit.md) | All 58 references, the checker and the Appendix K renderer | 58 references re-fetched | 8 | 14 | 1 |
| [Visual and layout QA](visual-and-layout-qa.md) | Real XeLaTeX PDF: 42 figures, 28 covers (1,103 labels), 33 wide tables, dividers, appendices | Every figure and cover page at print scale | 20 | 4 | 0 |
| **Total** | | | **46** | **40** | **3** |

Counts are findings, not sentences. "No issue" means checked and not contradicted, not certified.

## What changed in the book

- **Citations.** Evidence rows that cited a source for more than it says are split into the sourced fact and a labelled book recommendation (Ch 1, 6, 7, 9, 12, 13, 15, 21, 23, 25, 27). Factual errors corrected: CloudEvents extension names (Ch 4, Appendix C, and the companion `CloudEvent` model, which now serializes `tenantid`/`correlationid`/`causationid`); the OpenAI Agents SDK does ship skills at 0.22.2 (Ch 8); MLflow 3.15.2's `disable_openai_agent_tracer` (Ch 24 and the example comments); R02 (a 2025 Temporal blog post) no longer cited for replay; Appendix D's unsupported CrewAI, Dapr, PydanticAI and ADK claims removed.
- **Consistency.** InterventionRequired is non-terminal everywhere (Ch 15, 18, 19); Ch 22's effect states are "outcome states"; Ch 26's review cadence matches its table; Ch 2's flattened proposal JSON is labelled against the registered contract.
- **Registry.** Wrong years (R02, R04, R15, R17), titles and labels corrected; version-specific links pinned (CloudEvents 1.0.2, MLflow 3.15.2 docs, dated WCAG 2.2, a Policy Logic Forge commit); one dating rule (`n.d.` unless the page shows a date), enforced by `tools/check_references.py`; all 58 entries verified 2026-10-11. The source copy of Appendix K is now a stub; assembly generates the section.
- **Layout.** The XeLaTeX edition has 0 overfull lines (was 478, including one 44 pt line); table headers are never doubled or stranded; headings and code labels stay with what follows; curly quotes restored.
- **Visuals.** 18 diagram sources reworked for legibility, overlaps, and agreement with their chapters (Fig 5-2 and 10-1 now match the text; Fig 7-2's adapter groups restored); 35 cover labels in 10 chapters reworded to each chapter's own text; alt text on every DOCX image; Fig 23-1's caption names DLP.

## Still open

| ID | Item | Owner |
| --- | --- | --- |
| P2-C-21 | 25 figures still print a label below 9 pt (smallest 6.8 pt, Fig 4-1). Needs restructuring (split Fig 4-1, draw Fig 4-2 vertically), not more tweaking. | Diagram follow-up |
| P2-A-17 | Ch 14's approval-integrity row is "informed by R15", but the OWASP mitigation text was not retrievable. The row is already labelled book-authored. | Needs a human read of the OWASP PDF |
| P2-B-20, P2-D-18 | mlflow.org returns 403 to automated tools; the 3.15.2 pin is confirmed from PyPI and GitHub, but the release page itself needs a browser read. | Author |
| P2-A-19 | OMG DMN 1.6 became formal in September 2026; the book deliberately keeps its 1.5 pin. | Author decision |
| P2-D-19 | R27's page now says its tooling landscape has changed; the book cites it only for the workflow/agent distinction, which is unaffected. | Optional scope caveat |
| — | `tools/validate_book.py`'s stale-release check matches version strings inside URLs, which blocks linking R21 to its GitHub release. | Optional tooling change |
| — | DOCX pagination is unchecked (no LibreOffice locally). | Release QA |

Carried over from pass 1: the pinned run data behind the 44% figure (A-K) and the evaluator's one-call spend overrun (C13a) need the author.

## Validation

`make assemble build references latex latex-validate validate` pass (8/28/12, 58 references, 147 citations, all cited, 0 title mismatches); `make examples-run` pass (258 example tests and 30 mortgage-case tests); `make deterministic` byte-identical; `make pdf` builds 342 pages with 0 overfull boxes. `make qa-pdf` not run (no LibreOffice).
