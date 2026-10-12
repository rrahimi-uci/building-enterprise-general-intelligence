# Group c2 report: knowledge-lifecycle, reference-architecture, system-overview

Branch `diagrams/c2`. Pairs: `group-c2/<id>-before-after.png`. All three were redrawn in native TikZ with the shared package; nothing in `latex/styles/professional-diagrams.sty` was touched. Natural size and placement scale come from `make diagrams`.

| Figure | Natural size (in) | Placement scale | Before |
|---|---|---|---|
| knowledge-lifecycle (5-4) | 7.12 x 8.38 | 0.99 | 8.3 x 10.7, shrunk to about 0.78 (labels at about 9.4 pt) |
| reference-architecture (4-1) | 6.80 x 8.26 | 1.005 | 9.2 x 10.1, shrunk to about 0.77 |
| system-overview (1-3) | 6.91 x 8.17 | 1.016 | shrunk to about 0.8 |

Smallest text is 9 pt on the page in all three (chips and notes 9 pt, descriptions 9.5 pt, pills 9 pt bold), against 7 to 9 pt printed before.

## knowledge-lifecycle (Figure 5-4)

- **Q1 identical information: YES.** 12 nodes (7 control plane, 5 runtime plane) plus the boundary text; 17 visible edges (the 3 invisible ordering edges of the source are not drawn); both dashed planes and titles; both diamonds; both cylinders; the note shape (production) kept as a folded-corner card. Line styles kept: red solid "blocking finding", red dashed "repaired . re-check", amber dashed "request changes . back to Draft", slate dashed "staleness" and "proposed change (never a write)", cyan dotted "decision record", thick registry-to-production connector. Re-wrapping only: the first line of a node became the bold title (for example "Authoritative sources" / "regulations . standards / contracts . internal policies"); the dot that joined title and description was dropped, no word changed.
- **Q2 more polished: YES.** Two plane groups with pills on every edge, roles per the style guide, repair loop as two labelled parallel arrows, return edges routed in side lanes, whole figure 8.4 in tall at scale 0.99 instead of 0.78.
- Layout decisions: sources/extract in one row, graph under extract, repair beside the gates diamond, registry beside the approval diamond (as in the source); the runtime plane title moved to the top right (a bottom title needs another 22 pt); two lanes on the right carry the two upward edges.
- Problems found and fixed: first layout was 645 pt tall (cylinders far taller than their text; `aspect` lowered locally); `\\` inside a diamond needs `text width` or TikZ fails; the boundary note and the "proposed change" pill collided with plane borders and the runtime title (gap between planes opened to 34 pt, title shifted); staleness pill covered the gates diamond (moved beside its curve); the permit-or-refuse arrow was slanted (anchors aligned).
- Remaining weaknesses: the rotated "request changes" pill is the one rotated label; the left half of the second row is empty; the figure is 0.99 scale, not 1.0 (width 7.12 in).

## reference-architecture (Figure 4-1)

- **Q1: YES.** 40 visible chips (the source's 42 include the invisible placeholders e3, d3), 9 clusters (six planes, "Edge and admission" sub-plane, two rails), 6 labelled solid request-path edges, 3 dashed red control edges (all leave PDP / PEP), 3 dotted amber evidence edges (arrowheads at the OTel collector, as `dir=back` does in the source). Every chip text is unchanged (re-wrapped as in the source: "API Gateway / . WAF", "Planner . / coordinator"). The two-line cluster titles of the gateway and systems planes keep both phrases (second phrase in italic regular).
- **Q2: YES, clearly.** Planes are rows of chips, rails are full-height spines, the request path descends one column, and the three dashed and three dotted edges are routed orthogonally into lanes. Before: 9.2 x 10.1 in shrunk to 0.77, smallest label printed at about 7.5 pt; now 9 pt at scale 1.005.
- Chip order within a plane changed only where it straightens the request path into one column (API clients first in Experience; Knowledge Hub and Context Service swapped; Skills and Topology swapped so the dotted edge leaves from the free right end; MCP servers and Domain systems swapped). Planes, memberships and edges are unchanged.
- Titles are right-aligned in each plane so the single-column request path never crosses a title.
- Problems found and fixed: arrows crossed the left-aligned plane titles (titles moved right, two-line titles for the two long ones); pills straddled plane borders (placed at gap centres); "PDP / PEP" was truncated by the `\foreach` slash separator (braced); planes of unequal width (explicit plane rectangles).
- Remaining weakness: three dotted lines run in adjacent lanes 6 pt apart; they stay distinguishable but are the densest spot.

## system-overview (Figure 1-3)

- **Q1: YES.** 7 band cards with Part badge, name and description in the source's words and line breaks, the two rails (7 chips each, titles "VI . Security", "III . VIII . Platform"), the 6 solid authority arrows with the three labels (proposes, authorizes, commits), the dotted amber "learns" loop, 2 dashed red and 2 dashed slate edges. The recent relabelling (Control points, Evidence, Channels, Collaboration) is as in the current source (the source's eight HTML rows are seven).
- **Q2: YES.** The badge, a filled cell in the source, is a filled tab in the role colour; colour roles map as before (slate, teal, plum, cyan, blue, plum, amber); labels are pills; the loop and rail edges run in their own lanes without crossing; scale 1.016 instead of about 0.8.
- Problems found and fixed: the "Learns" label is a rotated pill because the right lane is 36 pt wide; cross edges ordered so that none crosses another.
- Remaining weakness: the rails are as tall as the stack with seven widely spaced chips, as in the source.

## Local macros proposed for promotion

`band card` / `band badge` (row card with a filled Part tab, `system-overview`), `rail chip`, `pchip` and `pcyl` (small role chips and cylinder chips, `reference-architecture`), `\plane` (fixed-width titled plane with a top-right title), `thick edge` (2.4 pt boundary connector with a large head), a folded-corner "note" card (drawn in `knowledge-lifecycle`), a `dg decision` note: it needs `text width` when its text contains `\\`.

## Validation (this branch)

`make diagrams`: pass, only the three figures changed, all other renders byte-identical (git status). `make assemble build references latex latex-validate validate`: pass, 0 errors, 0 warnings, DOCX 73 images (expected 73). `make examples-run`: 30 passed. `make pdf`: 360 pages, 0 Overfull hbox, fonts embedded (Liberation Sans, FontAwesome in the book). The three figures were inspected in the compiled PDF (pages 36, 67, 92): readable, margins and captions correct. Greyscale: all three read without colour (shape, dash style and pill words carry the meaning).
