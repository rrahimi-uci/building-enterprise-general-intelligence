# Group a report: flows with feedback loops (7 figures)

Branch `diagrams/a`. Every figure is a TikZ source (`assets/diagrams/src/<id>.tikz.tex`), drawn at final size (placement scale 0.99 to 1.05, text 9 to 10.5 pt). The seven `.gv` sources are removed with `git rm`. Before/after pairs: `group-a/<id>-before-after.png`. Technical doubts: `observations-a.md`.

## Per figure (Q1 identical information, Q2 clearly more polished)

| Figure | Q1 | Q2 | Nodes / edges before -> after | Natural size / scale |
|---|---|---|---|---|
| `dx-golden-path` (7-3) | YES | YES | 8 steps + group + note, 11 edges (8 solid, 3 dashed) -> same | 6.92 x 3.81 in / 1.02 |
| `learning-loop` (25-3) | YES | YES | 10 nodes, 10 edges -> same | 7.04 x 5.81 / 1.00 |
| `pattern-durable` (15-1) | YES | YES | 6 nodes (2 cylinders), 7 edges (2 dashed) -> same | 6.96 x 3.10 / 1.01 |
| `pattern-planning` (12-1) | YES | YES | 6 nodes (1 diamond), 6 edges (2 dashed) -> same | 7.11 x 5.78 / 0.99 |
| `pattern-react` (10-1) | YES | YES | 6 nodes, 6 edges (2 dashed) -> same | 6.96 x 4.68 / 1.01 |
| `reliability-economics` (28-1) | YES | YES | 9 nodes (2 diamonds), 12 edges (3 dashed amber, 1 dashed blue, 3 dotted) -> same | 6.76 x 7.85 / 1.05 |
| `supervisor-worker` (18-1) | YES | YES | 11 nodes (1 diamond), 17 edges + 2 free annotations -> same | 7.10 x 6.00 / 0.995 |

Each source has its original-to-restyled mapping comment at the top.

### Layout decisions (structure unchanged)
- `dx-golden-path`: the serpentine 2 x 4 stays; the five listed words of the note become chips; the three dashed edges rise from the note to Package, Promote, Operate. Icons name each step.
- `learning-loop`: the circo ring becomes an ellipse in the source's positions (Approve top left, Observe lower right, clockwise); edges arc gently outward; square corners kept on the four blue boxes and on Approve (boxes in the source).
- `pattern-durable`: the vertical chain becomes two rows (run on top, recovery below) so "resume" (over the top) and "continue" (through the middle) are short, uncrossed loops.
- `pattern-planning`: chain stays vertical; the two exits leave the diamond's side vertices; the replan loop runs outside on the left with a two-line pill.
- `pattern-react`: the loop is one column on the left, the two exits fan out to the right so neither exit sits inside the loop; the controller stays above; "next need" runs outside on the left.
- `reliability-economics`: main flow in one column; Safe degradation on the right with both dashed edges entering it; the three dotted edges converge on the usage store; "tune permits and routes" runs outside on the left to Admission.
- `supervisor-worker`: three columns (child task over worker); fan-in diamond; the long ownership edge runs down the left (it ran down the right in the source) so the two free annotations stay beside their rows as red callouts.

### Problems found and fixed during iteration
- Local key `step` clashed with a built-in TikZ key (renamed `gstep`).
- Chips overlapped (fixed with a `matrix` row); the "code" icon touched its label (swapped for `hammer`).
- `pattern-planning`: loop pill misplaced; figure too narrow (11 percent upscale), widened cards.
- `pattern-react`: arrows crowded with pills on S-curves (replaced by orthogonal exits with pills on straight runs); the return arc ran into the Reason icon (more offset).
- `reliability-economics`: first draft 541 pt wide (placed at 0.94, rejected by the 95 percent rule): pills moved from the outer verticals to horizontal runs and the card widened.
- `supervisor-worker`: first draft 540 pt wide; the ownership pill moved to the top run.

### Remaining weaknesses
- Icons are decorative; `supervisor-worker` has no icons on its child/worker rows (width), only on Supervisor and Accepted outcome.
- `pattern-planning` is lopsided to the left because of the left-hand loop and the long run of the loop.
- Curved fans in `reliability-economics` (Pass/Fail) share the diamond's bottom vertex.

## Local macros proposed for promotion
- `note red` (callout with role-ink text): `callout=<role>, text=dg-<role>-ink` as a ready style, `note <role>`.
- A matrix-based chip row (`\matrix[matrix of nodes, column sep=8pt, nodes={chip=blue}]`), needs `\usetikzlibrary{matrix}`.
- `\dgtitlesize ... \\ {\dgdescsize ...}` label helper for diamonds (used in 4 figures: `dgdiamondlabel{title}{description}`).
- `pill` with a two-line (bold + regular) body (`\\[-1pt]{\fontsize{9}{10}\selectfont\mdseries ...}`) as `\dgpilltwo{a}{b}`.

## Validation (venv paths from the brief)
- `make diagrams`: pass; only the seven figures changed, all other renders byte-identical (git status shows only these 7 PDF/PNG pairs).
- `make assemble build references latex latex-validate validate`: pass, 0 errors, 0 warnings; 44 markers = 44 registered; DOCX 73 images (expected 73).
- `make examples-run`: 30 passed.
- `make pdf`: 360 pages, 0 Overfull boxes, no undefined references; figures inspected in the compiled book PDF (Figures 7-3, 10-1, 12-1, 15-1, 18-1, 25-3, 28-1): fonts embedded (renderer check), text readable, centred, captions aligned.
- Not committed (integrator re-runs): `config/diagrams.json` (the seven `source` fields now point at the `.tikz.tex` files in my working copy and the sha256 values), `CHANGELOG.md`, `reports/`, and generated book artifacts.
