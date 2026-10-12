# Pass 2 — Visual and layout QA (P2-C)

Branch `pass2/c`, based on `fix/correctness-review-findings` (includes PR #82's prose edits). Date: 2026-10-11.

## Scope and method

Pass 1 did not look at figures, covers, or tables at print scale. This pass did, on a real XeLaTeX build.

- **PDF builds.** `make pdf` (three `xelatex` passes, TeX Live via `/Library/TeX/texbin`) for the baseline, then again after each fix. I parsed every log for overfull and underfull boxes and mapped them to physical pages with PyMuPDF.
- **Rendering.** I rendered all 341 pages to PNG at 150 dpi with `pdftoppm`, before and after, outside the repo. I read the following pages as images: every page with one of the 42 figures (baseline and final); the eight Part dividers and the appendices divider; the Closing Perspective; Appendix A; Appendices C, D, H, K and L; the five-column tables (Ch 8 "Unit", Ch 16 patterns, and the 26 per-chapter "State owner" summaries); and the four-column tables in Ch 4.
- **Each figure on its own.** I rendered each diagram source alone, at the scale it prints in the book, and measured its smallest printed label from the vector PDF's font sizes multiplied by the placement scale. I checked the labels, arrows, and caption against the chapter text.
- **Covers.** I read all 28 chapter covers at full resolution. I also extracted all 1,103 cover labels from `config/chapter-covers.json` (title, focus, themes, diagram title, groups, nodes, sub-labels, edges, components) and checked each one against its chapter's text in `book/manuscript.md` on this branch. Every flagged label was then reviewed by hand.
- **Registries.** I checked every `[[DIAGRAM:…]]` marker against `config/diagrams.json`: IDs, numbering, uniqueness, order, alt-text descriptions, and checksums.
- **Automated layout scans** over the whole PDF:
  - table heads printed twice;
  - table heads not followed by their own rows;
  - headings that end a page;
  - listing labels (`🐍 · …`, `JSON · …`) that end a page;
  - near-empty pages.
- No web sources were needed. This pass checks rendering and internal consistency, not external claims.

## Findings

| ID | Location | Status | Evidence | Change made / recommended owner |
|---|---|---|---|---|
| P2-C-01 | Ch 25 table "Close the loop…", Validate row (`source/parts/07-part-vii.md:460`), PDF p. 274 | Confirmed Error | 44.41 pt overfull: the unbreakable token `unit/contract/security/privacy/adversarial/load/cost/compatibility` ran past the column into the next one | Fixed in `tools/build_latex.py`: a `/` in table-cell text becomes `\slash`, which allows a line break. Now 0 pt. No prose change needed |
| P2-C-02 | Every five-column table (26 "State owner" summaries, Ch 8, Ch 16) and three alignments | Confirmed Error | 32 boxes 1.40 pt wider than the text block. The `0.94/c` column share ignored the `2c-2` tabcolseps | Column width is now `(\linewidth-(2c-2)\tabcolsep)/c`, so tables fill the measure exactly |
| P2-C-03 | Table of contents | Confirmed Error (cosmetic) | 445 TOC entries about 0.95 pt overfull: three-digit page numbers in a 1.55 em box | `\@pnumwidth` set to 1.9 em in `latex/bookstyle.sty` |
| P2-C-04 | Table heads printed twice: pp. 34, 36, 95, 133, 145, 246, 265, 338 (baseline) | Confirmed Error | Root cause, isolated with a test harness: `\needspace` (needspace v1.3) only plants a cheap breakpoint. TeX takes it later, inside the following `longtable`, whose output routine then prints its head on the next page as well. After my first fix the same mechanism also left a stray head above a code listing (Ch 3) | Added `\BookNeedspace` (= `\Needspace`, which measures and breaks immediately) and used it for every guard. Longtables get no reservation; their first one or two rows end in `\\*`, kept only while that opening block stays under 150 pt. Now 0 doubled or stray heads |
| P2-C-05 | Headings stranded at the foot of a page: pp. 68, 71, 94, 137, 144, 173, 201, 245, 264, 308, 312 (baseline) | Confirmed Error | Each heading was followed directly by a table or listing that did not fit below it | A heading now reserves room for the opening of the table, listing, or sub-heading that follows it. Now 0 |
| P2-C-06 | Listing labels at the end of a page, code on the next: 29 cases (e.g. pp. 31, 45, 56, 78–84, 105, 118, 126, 146, 164, 174, 189–192, 212, 227, 236, 255, 266, 279, 299, 300, 311, 332) | Confirmed Error | The listing's own guard came after its label, so the label could end a page | The label paragraph now reserves its listing (all of it if it fits on a page, otherwise 8 lines) and sets `\nopagebreak`. The listing's own guard is then skipped. Now 0 |
| P2-C-07 | 38 straight double quotes in prose and tables (e.g. p. 33 "is the user logged in") | Confirmed Error | With TeX ligatures, both quotes printed as closing quotes: the PDF text shows `”is the user logged in”` | The builder now converts straight quotes to opening and closing quotes outside code (`smart_double_quotes`). 86/86 balanced. DOCX and Markdown unchanged |
| P2-C-08 | Appendix C (and every table holding inline code) | Confirmed Error (cosmetic) | Inline code in 7.2 pt cells was set at the 8.6 pt body-code size, so identifiers looked oversized | Inline code in a table cell now takes the cell's size |
| P2-C-09 | Diagram legibility at print scale | Confirmed Error | DESIGN-SYSTEM §9 asks for at least 9 pt at final size. In the baseline, 13 figures printed labels below 7 pt: Fig 4-2 3.5 pt, 20-3 3.9, 4-1 4.2, 1-4 4.4, 1-3 and 25-1 5.2, 18-1 5.4, 16-1 5.8, 24-1 6.2, 22-1 6.3, 21-1 6.4, 23-1 6.7, 8-1 6.8. 29 printed below 9 pt | Reworked the sources: 1-4 laid out top to bottom; 1-3, 4-1, 25-1, 18-1 and 22-1 narrowed; 4-2 and 20-3 given a narrower Mermaid theme; 16-1, 8-1 and 13-1 fonts raised. Figure height cap raised from 0.76 to 0.86 `\textheight`. Now 1 figure below 7 pt (4-1 at 6.8 pt) and 25 below 9 pt. See P2-C-21 |
| P2-C-10 | Fig 1-3 `system-overview` | Confirmed Error | The "commits" xlabel sat on its arrow ("com\|mits") | xlabels changed to labels, which reserve their own space |
| P2-C-11 | Fig 7-2 `portability` | Confirmed Error | `dot` warned "f1 was already in a rankset, deleted from cluster" and removed both adapter clusters. The figure printed four unlabelled boxes, against the caption's "framework and provider adapters" | Rank constraints moved inside the clusters; edges land on each cluster (`lhead`); the alternatives are joined by "or". No warnings now |
| P2-C-12 | Fig 5-2 `policy-to-guardrail` vs Ch 5 text | Potential Issue | The figure's sample policy ("Transactions over $10,000 require compliance approval") is not the chapter's example, which is a pay statement accepted only within an age window | The figure now quotes the chapter's example |
| P2-C-13 | Fig 10-1 `pattern-react` vs Ch 10 text | Potential Issue | The "accept?" edge left Observe. The chapter says the reasoning step's terminal answer goes to the acceptance engine (step 5) and observations feed the next turn | Edge now runs from Reason ("answer: accept?"); fonts raised |
| P2-C-14 | Fig 17-1 `anti-before-after` | Confirmed Error | The connecting edge pushed the governed cluster down a rank, so the three concerns no longer lined up, and its label sat on the arrow across the cluster title | Clusters now side by side, row-aligned (`minlen=0`), with the label as its own node. Smallest label 8.4 → 9.3 pt |
| P2-C-15 | Fig 20-1 `security-depth` | Confirmed Error (cosmetic) | In the bold face that Graphviz substitutes, "Channel/input" and the other layer names read as run together | Spaced slashes ("Channel / input") |
| P2-C-16 | Figs 20-2 `security-boundaries`, 26-1 `governance-model` | Confirmed Error | A cluster title was crossed by an incoming edge ("delegated grant", "grants") | Cluster labels moved to the bottom or split |
| P2-C-17 | Figs 4-2 `request-sequence`, 20-3 `guardrail-sequence` | Confirmed Error | Mermaid step numbers 1–16 competed with the Ch 4 table's eight numbered steps, and self-message labels collided with the numbers | `autonumber` removed; theme sets `wrap`, narrower actors, and no mirrored actors |
| P2-C-18 | Fig 24-1 `causal-trace` | Confirmed Error (clarity) | Eight dotted evidence edges crossed the whole run spine to a store row at the top | Each store now sits beside the part of the run that writes to it |
| P2-C-19 | Figs 17-3, 17-4 | Confirmed Error (cosmetic) | The xlabels "transient", "unknown" and "yes" overlapped their arrows | More node separation and padded xlabels |
| P2-C-20 | `config/diagrams.json`; DOCX | Confirmed Error | 18 of 42 diagrams had no `description`. No DOCX image had alt text (0/71): `docPr/@descr` was never written | Added the 18 descriptions, written from each figure and its chapter. `tools/build_book.py` now writes alt text for diagrams (registry description), chapter covers (title and focus), and the book cover. DOCX: 71/71 |
| P2-C-21 | 25 figures still print a label below 9 pt (smallest: 4-1 at 6.8, 4-2 and 1-3 at 7.0, 25-1 at 7.1) | Potential Issue | Measured from the vector renders at placement scale | Owner: diagram sources (a follow-up pass). These need structural redesign, such as splitting Fig 4-1 into planes and spines or drawing Fig 4-2 vertically, not further tweaking |
| P2-C-22 | Chapter covers vs chapter text (AGENTS.md: "every label must come from the chapter's own text") | Confirmed Error | Labels not found in their chapter: Ch 1 "owns truth" and "Where truth lives"; Ch 7 "Rebuilt plumbing" and "behaviour" (the book spells it "behavior"); Ch 10 "Fit before loop", "Fit test", "Governed exits" and "Fit, bound, then exit"; Ch 13 "Reflector" and "Decided elsewhere"; Ch 14 "SoD"; Ch 16 "Hidden obligations", "Honest trade-offs", "Hidden Obligation" and "Honest Cost"; Ch 18 "Conversation advises, workflow decides", "Advisory conversation" and "declare done"; Ch 23 "Blast-radius limits", "Capability envelope" (Chapter 21's term), "Pre-retrieval authz" and "Enterprise data"; Ch 24 "Run identity"; Ch 25 "Automate, govern, prohibit" and "breach" | 35 label fields reworded to the chapter's own wording (e.g. Ch 10 "The loop is inside, the limits are outside" and "Information-dependent steps"; Ch 16 "Obligation first" and "What it costs"; Ch 24 "Run and release"; Ch 25 "The automation boundary" and "stop condition"). Re-rendered with `make chapter-covers` |
| P2-C-23 | Covers Ch 5 and Ch 19 | Confirmed Error (cosmetic) | Ch 5: the "enforce" pill sat under badge 3. Ch 19: the "pinned manifest", "tool call" and "validated result" pills overlapped | Pill positions adjusted in the spec |
| P2-C-24 | Fig 23-1 caption, `source/parts/06-part-vi.md:1023` | Potential Issue | The figure and its registry description include the DLP boundary, and so does Ch 23's text ("sandbox, egress, capability, credential, DLP, and effect controls"). The caption omits it | **Recommended prose change (owner: integrator):** `[[DIAGRAM:sandbox-egress\|Figure 23-1 — Containing manipulated content at capability, sandbox, egress, credential, DLP, and effect boundaries]]` |

## Before / after (XeLaTeX)

| Measure | Baseline | Final |
|---|---|---|
| Pages | 341 | 341 |
| Overfull boxes (all) | 478 (1 at 44.41 pt, 32 at 1.40 pt, 445 TOC at ~0.95 pt) | **0** |
| Overfull boxes > 3 pt | 1 (p. 274) | **0** |
| Underfull boxes | 10 | 6 (badness ≤ 7326: the justified Evidence-context paragraph in Appendix D, one Ch 5 paragraph, one table cell) |
| Doubled or stray table heads | 8 | **0** |
| Headings ending a page | 11 | **0** |
| Listing labels ending a page | 29 | **0** |
| Figures with a printed label < 7 pt | 13 | 1 |
| Figures with a printed label < 9 pt | 29 | 25 |
| DOCX images with alt text | 0 / 71 | 71 / 71 |
| Diagrams with a registry description | 24 / 42 | 42 / 42 |

The remaining log warnings were already present in the baseline: font-size substitutions at 3.6/3.7 pt, a microtype `footnote` patch warning, and the `latex/bookstyle` package-name notice.

## Counts

- **Checked:** 42 figures (source, print-scale render, and placement in the book); 28 covers (image plus 1,103 labels); 42 registry entries; 33 tables wider than three columns; 9 divider pages; the Closing Perspective; Appendices A, C, D, H, K and L; the whole-PDF layout scans.
- **Confirmed Errors:** 20 (P2-C-01 to -11, -14 to -20, -22, -23), all fixed. -03, -08, -15, -19 and -23 are cosmetic.
- **Potential Issues:** 4 (P2-C-12, -13, -21, -24). -12 and -13 were fixed; -21 and -24 are open, with owners named.
- **Needs Verification:** 0.
- **No issue:**
  - figure caption numbering is unique and sequential per chapter;
  - every marker resolves to exactly one registry entry;
  - the other 18 descriptions match their figures;
  - the other 18 covers, and the unflagged labels on all covers, come from their chapters;
  - the Part dividers, Closing Perspective, and Appendices A, H, K and L render without clipping or overflow;
  - colour is never the only carrier of meaning: shape, line style, and text labels carry it in every figure.

## Validation run

- `make assemble build references latex latex-validate validate`: pass (4 × `"pass": true`, no errors, no warnings).
- `make examples-run`: 257 passed (1 warning); `tests/mortgage_case`: 30 passed.
- `make diagrams`: pass; 42 renders, registry checksums updated. `make chapter-covers`: pass.
- `make pdf`: pass; 341 pages, 0 overfull boxes. The final PDF was copied to `~/Downloads/Enterprise-General-Intelligence-v1.0.0-LaTeX-pass2.pdf`.

## Not checked, and why

- **DOCX pagination.** LibreOffice is not installed, so `make qa-pdf` cannot run. The DOCX was validated structurally only (image count, alt text).
- **Cover labels.** I judged each label against the chapter's wording, not only its spelling. The 54 labels still flagged by the automated check are inflections or close paraphrases of chapter sentences (e.g. "proves" for "proof", "combine all" for "Combining every pattern"). I accepted them as faithful.
- **Diagram label sizes** were measured from text spans. Graphviz substitutes Helvetica/Arial for "Liberation Sans" on this host, so glyph widths differ slightly from the bundled font. The diagram renders do not embed the book's fonts; that is a pre-existing render-environment matter, outside this pass.
