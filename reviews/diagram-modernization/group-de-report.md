# Group de report: stacks, ladders, maps and decision trees (7 figures)

Branch `diagrams/de` (from `main` at a5a98e1). Seven existing figures converted from Graphviz to TikZ; content unchanged. Before/after pairs (rendered the way the book places them) are in `group-de/`. Technical doubts are in `observations-de.md`.

## Per figure

| Figure | Q1 identical information | Q2 clearly more polished | Elements before / after | Natural size (in) |
|---|---|---|---|---|
| `book-map` (0-1) | YES | YES | 8 rows (number, title, topics) / 8 row cards, same text, same 8 hues, same order | 7.03 x 6.43 |
| `capability-ladder` (1-2) | YES | YES | 3 headings + 12 boxes / 3 headings + 12 cards; the "n . Name" label is now a number badge plus bold name | 6.99 x 3.93 |
| `deterministic-shell` (2-1) | YES | YES | 6 gates, 5 refusals + 1 annotation, 2 headings, 5 solid + 5 dashed edges / same | 7.04 x 5.76 |
| `security-depth` (20-1) | YES | YES | 9 rows, one emphasised / 9 row cards, row 6 heavier border | 7.05 x 6.77 |
| `model-routing` (28-2) | YES | YES | 7 nodes, 7 edges (yes/no) / same, "yes/no" now pills | 6.72 x 6.69 |
| `pattern-decision-tree` (16-1) | YES | YES | 2 clusters, 6 diamonds, 7 leaves, 12 edges / same (see note) | 7.05 x 8.25 |
| `pattern-routing` (11-1) | YES | YES | 7 nodes, 9 edges / same | 6.72 x 6.27 |

Every node text, every edge direction and style (solid flow, dashed refusal / authorization edges), every edge label and every hue is kept. The only text changes are typography: the dash that separated name and controls in `security-depth` is the line break between title and description; chapter references in `pattern-decision-tree` leaves moved from the label into a note line ("Ch 12/15"); "yes"/"no"/"then" and the other edge words are capitalised inside pills; two-line labels re-wrapped.

### Notes per figure

- **book-map**: row card = badge + bold Part title; the topics strip stays a separate right-hand column behind a hairline divider (stacking it under the title left too much empty width). Source has no edges (invisible chain), none drawn.
- **capability-ladder**: three grid columns kept; the three column headings become coloured headings over hairline rules. Failure cards red x3 and amber x1 as in the source.
- **deterministic-shell**: "the model's only job" (borderless teal text in the source) is a teal callout; five dashed red arrows run gate to refusal as in the source; five solid blue arrows between gates.
- **security-depth**: the source's double border on "Tools / effects" is a 2.4 pt border; weight, not colour, carries the emphasis.
- **model-routing**: decision spine on the left, outcomes on the right; both "no" edges still reach one "Refuse or escalate" card. The Graphviz version had "no" arrows crossing the area; now one goes around and one straight.
- **pattern-decision-tree**: the 10.7 in Graphviz render (shrunk to about 0.78) is re-laid out at 100 percent in 8.25 in by putting each "yes" leaf to the right of its diamond and each "no/then" down the spine; panel titles keep "1 ·" and "2 ·". The dashed slate "every shape, then" arrow runs between the panels at the spine, as the source's cluster-to-cluster edge.
- **pattern-routing**: authorization card sits below the specialists with two dashed red arrows converging, as in the source; fallback edge in slate.

### Problems found and fixed while iterating

- Diamonds: a bold first line and regular second line (a TikZ `align=center` quirk resets the font after `\\`); fixed with a local `\dgq` macro that sizes each line.
- Diamond widths: pgf enlarged diamonds beyond `minimum width` when text was wrapped unbraced; set per-figure widths and check by render.
- `capability-ladder` first render was 519 pt wide (7.2 in) and the heading sat on the first row; narrowed columns to 493 pt, raised the headings.
- `pattern-decision-tree` vertical gaps too small for pills on the arrows: pills are placed beside the vertical arrows (`anchor=west`) instead of on them; whole figure 594 pt (8.25 in) so it is placed at 100 percent.
- Title/description baseline offset in `book-map` columns: fixed with `anchor=base west` and a small shift.

### Remaining weaknesses

- `book-map` and `security-depth` are 8 to 9 identical cards: tidy and consistent, but intentionally plain (no icons were forced onto them).
- `pattern-decision-tree` is 8.25 of 8.3 in tall: a caption with two lines would move it near the limit (the book caption is one line; checked in the PDF).
- `capability-ladder` has no edges in the source, so no relation between the columns is drawn beyond alignment.
- Palette is unchanged; the one unusual use is an emphasised-by-weight row (security-depth row 6), which relies on the heavier border alone.

## Local macros proposed for promotion to `professional-diagrams.sty`

1. `\dgrow[opts]{name}{role}{(x,y)}{badge}{content}` with lengths `\dgrowh`, `\dgrowbw`: a row card with a solid role-coloured badge (number or Roman numeral) at the left and indented text. Defined at the top of `book-map`, `security-depth`, `capability-ladder` and `deterministic-shell` (same text in each; once promoted, delete the local copies). `\dgrow` could also take an optional right-hand column as used in `book-map` (title, divider, topics) via the `\bmrow` pattern in that file.
2. `\dgq{line1}{line2}`: two-line bold question for `dg decision` diamonds (the font resets after `\\`); in `model-routing`, `pattern-routing`, `pattern-decision-tree`. Better: have `dg decision` set the font on each line, or ship `\dgquestion`.
3. Column heading (bold coloured text over a 1 pt rule): written inline in `capability-ladder` and `deterministic-shell`; a `\dgcolhead{x}{y}{width}{role}{TEXT}` would remove the duplication.
4. Pill placed beside a vertical arrow (`pill=..., anchor=west, xshift=5pt`): used in `pattern-decision-tree` where gaps are too short for an on-line pill; could become `pill beside`.

## Installs

None.

## Validation (this worktree, venv paths from the brief)

| Check | Result |
|---|---|
| `make diagrams` | pass, no errors; only the seven figures' PDF/PNG changed, all other renders byte-identical (git shows only my files modified) |
| TikZ placement | all seven at scale >= 1.0 (widths 6.7 to 7.05 in; tallest `pattern-decision-tree` 8.25 in); fonts embedded (Liberation Sans Regular/Bold only in each PDF); no figure is resized below 9 pt |
| `make assemble build references latex latex-validate validate` | pass, 0 errors, 0 warnings; 44 diagram markers = 44 registered; DOCX 73 images (expected 73) |
| `make examples-run` | 30 tests passed |
| `make pdf` | 360 pages (the pilot report recorded 359 for its build; I did not isolate the reason), 0 Overfull `\hbox` in the log, no undefined references |
| Figures in the compiled PDF (printed pages given in the next column) | looked at at 100 dpi: book-map (xix), capability-ladder (p. 7), deterministic-shell (p. 20), pattern-routing (p. 121), pattern-decision-tree (p. 168), security-depth (p. 208), model-routing (p. 301): size, margins, caption centring and text legibility correct |
| Greyscale | contact sheet of four of the figures: gates, refusals, diamonds, dashed vs solid arrows and every label are distinguishable without colour |

## For the integrator

- Registry: after `git rm` of the seven `.gv` sources the renderer falls back to `<id>.tikz.tex`, but it only rewrites `sha256`, not `source`. I changed `source` for the seven ids to `assets/diagrams/src/<id>.tikz.tex` in my working copy of `config/diagrams.json` (unstaged, not committed, as instructed). Re-run after merging all groups: set `source` for these ids, then `make diagrams` (idempotent) and a changelog entry.
- `reports/diagram-render-report.json` also changed in my tree and is unstaged.
