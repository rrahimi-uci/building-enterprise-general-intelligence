# Overall book correctness and consistency validation

**Baseline:** `origin/main` `6ebbc8b`, reviewed 2026-10-10. **Disposition:** review findings for a subsequent corrective PR; **not publication certification**. No manuscript, registry, diagram source, cover spec, generated book or release package is changed in this review PR.

## Executive assessment

The book's core architecture is coherent: model reasoning is bounded by platform-owned authority, durable state, effect receipts, evidence, recovery and release gates. The synthetic Harborlight case is explicitly not an implemented production mortgage platform beyond C01–C03. Structural artifacts match the v1.0.0 baseline, and the runnable example suite passes. Nonetheless, several safety-relevant assertions and educational examples are wrong or require material qualification. The highest priority is the effect-key conflict bug, evaluator acceptance/budget bugs, and the claim that the intersection of two knowledge sets is automatically safe to act on. The metadata registry also contains 22 stale chapter titles.

These reports identify **8 confirmed errors**, **10 potential issues**, and **3 claims requiring verification** (21 distinct findings). B-01 is one systemic error despite 22 affected chapters. Counts are findings, not the number of sentences or files affected. “No confirmed issue” in a chapter report does not mean that chapter is certified. Full independent claim-by-claim citation support, all-cell table attestation, all-visual print-scale examination and live vendor behavior remain incomplete.

## Scope and evidence actually checked

- Read canonical front matter, eight Parts (28 chapters) and twelve appendices with chapter transitions; mapped registered examples, figures, captions and cross-chapter contracts. The [chapter reports](chapter-01.md) through [chapter 28](chapter-28.md), [appendix assessment](appendices-validation.md), [title-drift comparison](metadata-title-drift.md) and [evidence ledger](evidence-ledger.md) are the auditable output.
- Current `book/manuscript.md` SHA-256 is `383157e2c814dbdc37b9847fca819bd53175e417e2697b0e715a40ccbb257c04`, exactly the canonical hash in `qa/validation-report.json`. Current DOCX SHA-256 is `08776e38462b88a3036393723d9923d37b6b275aee6609d7902bc2fed1c93b07`, also matching that report. The report is dated 2026-09-13; it was **not freshly regenerated** for this review.
- That hash-bound baseline reports 8 Parts, 28 chapters, 12 appendices, 54 reference IDs, 139 citation occurrences, 42 diagram markers, 57 assembled code blocks, 324 Markdown tables, 71 DOCX inline images, zero structural warnings/errors and zero callout-contrast failures. The live registries contain 42 diagrams, 44 example entries, 28 chapter covers and 54 references.
- Ran `.venv-examples/bin/python -m pytest examples/tests tests/mortgage_case -q`: **264 passed**, one MLflow/SQLAlchemy deprecation warning. The test suite did not detect the three confirmed semantic code defects. Reproduced the missing-judge-score acceptance and changed-intent-after-decline bugs directly in the pinned environment; reviewed the spend-check branch against its existing test.
- Visually inspected the book cover, 28-cover overview montage and Chapter 22 cover, plus rendered Figures 13-1 and 22-1. Cover titles align with manuscript H1s and no printed release version was visible on the inspected covers. This is not a pixel-level examination of all 28 chapter covers or 42 diagrams; Figure 13-1's ambiguous reject path is recorded as a potential issue. All image assets are registered and hash-checked by the hash-bound baseline validator.
- Checked selected niche/current claims against official [MCP](https://modelcontextprotocol.io/specification/2026-07-28), [A2A](https://a2a-protocol.org/v1.0.1/specification/), [Temporal](https://docs.temporal.io/develop/python/integrations/openrouter), [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents/sdk), [OpenAI Evals](https://developers.openai.com/api/docs/guides/agent-evals), [AWS Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html), and [Little's original paper](https://doi.org/10.1287/opre.9.3.383). This is selective primary-source verification, not a re-reading of all 54 references at every citation occurrence.
- Sent live HTTP HEAD requests to all 54 registered reference URLs: 49 returned 200, one 202, three 403, and one DOI-resolver 404. The apparent 404 (R13) resolves on GET to NIST's official PDF; 403s can reflect automated-client restrictions. The [per-reference access log](reference-access-check.md) records statuses and caveats. URL access alone does not prove claim support.
- Compared all 28 canonical chapter headings with both `config/book.json` and `config/chapter-covers.json`: 22 metadata mismatches, zero cover-spec mismatches. The current build appears to use Markdown headings, so no reader-facing DOCX/LaTeX heading error is inferred from this alone.

## Findings by area

| Area | Confirmed | Potential | Needs verification | Highest-impact result |
| --- | ---: | ---: | ---: | --- |
| Technical/security claim | 1 | 4 | 1 | Chapter 5's knowledge intersection is not automatically safe; Chapter 22's negative lookup needs a finality contract. |
| Code/commands | 3 | 1 | 0 | Chapter 13's spend and missing-score acceptance, Chapter 22's intent-key reuse. |
| Figure/image | 0 | 1 | 0 | Figure 13-1 omits explicit acceptance-engine reject/escalate flow. |
| Citation/reference | 1 | 0 | 2 | R43 is overextended; Appendix D source gaps and R48 replay data remain. |
| Mathematics | 0 | 2 | 0 | `pass^k` assumes IID; Appendix L's work-rate factors may double-count. |
| Internal consistency/terminology | 3 | 2 | 0 | Chapter 24's unfinished “completed” run; Appendix H exactly-once overclaim; B-01 title drift. |
| **Total** | **8** | **10** | **3** | **21 distinct findings** |

The categories above are mutually exclusive **for counting**; an individual finding can implicate several review lenses. No confirmed table-cell arithmetic, chart-scale, equation derivation, spelling or punctuation error was found; this is a detection statement, not proof none exists. No newly introduced reference was fabricated. The apparent R48 source exists but has limited empirical replay evidence. No confirmed stale product/API assertion was found in the selected current-source checks; the remaining living references require a fresh release-time pass.

## Highest-risk chapters and cross-book issues

1. **Chapter 22 / Appendix H (effect safety):** the runnable ledger overwrites a declined key with altered intent; the glossary overpromises “exactly once”; negative-lookup reconciliation needs a bounded-finality guarantee. Together these can misteach a safety-critical protocol.
2. **Chapter 13 (acceptance correctness):** required evaluator scores can be absent yet accepted, and actual spending can cross the declared cap before either acceptance or escalation. Figure 13-1's reject path is unclear. The existing passing tests do not cover these edges.
3. **Chapter 5 (knowledge authority):** set intersection is presented as highest-confidence and safe without provenance, independence, freshness, authorization or scope checks.
4. **Chapter 24 (trace/state semantics):** twelve minutes end at an Unknown effect, not a verified completed review; the fork paragraph conflates diagnostic replay with separately authorized execution.
5. **Whole-book metadata B-01:** `config/book.json` titles diverge from 22 manuscript/cover titles. This violates a single coherent metadata source even though current rendered H1s appear sourced from Markdown.
6. **Chapter 28 / Appendix L:** R43 supports `L=λW` only; the sizing and economic recommendations are book-authored approximations, and the Appendix L rate factors need definitions.

## Citation and freshness conclusions

The registry and structural checks prove identifier completeness, not statement-level support. R43's scope is narrow; Appendix D openly identifies three unregistered framework sources. The R48 44% statement is present in the author's linked repository and is correctly bounded in the book to one run, but the run's numerator, denominator, corpus and code revision are not pinned for independent reproduction. Every living SDK, protocol and product claim should be checked at its exact pinned version or current official documentation immediately before any new release. The official MCP/A2A and AWS pages checked during this review did not reveal a direct contradiction in the cited framing.

## Second-pass critique of this review

- Downgraded Chapter 15 replay wording from “confirmed error” to **potential issue**: completed Activity history really is replay-safe; the missing distinction is Activity retry after an unrecorded external result.
- Downgraded `pass^k` from mathematical error to **potential issue**: it is valid under IID assumptions and the book adds “or equivalent,” but the assumption must be stated or an empirical all-k measure used.
- Downgraded Chapter 7 `agentctl` from non-existent-command error to **potential issue**: it could be a conceptual future CLI. The reproducibility problem is the lack of that label.
- Did not flag Chapter 28's 120/min × 4 min = 480 mean-concurrency example: the arithmetic is correct under its stated stable-workload assumption. Did not generalize R48's 44% to a model error rate.
- Separated B-01 metadata drift from a claimed DOCX/LaTeX heading fault; the latter was not observed.
- Retained uncertainty for visual semantics and citation support not independently checked. Passing structural QA and tests are not substitutes for source-content validation.

## Prioritized remediation plan

1. Fix Chapter 22's effect-key code and tests, Appendix H's exactly-once definition, and the conditional proof-of-absence language as one protocol correction. Test committed, declined, unknown, changed-intent and crash/ack-loss paths.
2. Fix Chapter 13's missing-score and spend semantics, add edge-case tests, then redraw/clarify Figure 13-1 from its editable source.
3. Correct Chapter 5's intersection table and Chapter 24's unresolved-run/fork language; keep approval, authority and effect state consistent across chapters.
4. Synchronize the 22 `config/book.json` titles and add a three-way title validator against canonical H1s and cover specs.
5. Narrow R43 attachment, define Appendix L work-rate variables and Chapter 25's repeated-run statistic; recheck associated numerical examples.
6. Close the Appendix D source gaps, pin R48 raw-run evidence if retained as empirical, and perform a separate full reference-to-claim/visual-print QA pass before certifying the publication.

## Release/PR implications

This review phase intentionally makes no book changes. A subsequent corrective PR must edit canonical files and registered visual specs/sources, regenerate artifacts through the repository build, update changelog/release evidence, run the full release gates (including genuine XeLaTeX and DOCX PDF visual review where available), and leave publication/Notion synchronization until the gates pass. This review-only PR should remain open for the owner's review; no merge or release claim is made.
