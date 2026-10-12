# Group b1 report: TikZ conversion of five pipeline figures

Branch `diagrams/b1` (from `main` at a5a98e1). Figures: `causal-trace` (24-1), `context-pipeline` (6-1), `document-ingestion` (5-3), `evaluation-gate` (25-1), `identity-delegation` (21-1). Sources are `assets/diagrams/src/<id>.tikz.tex`; the `.gv` sources are removed with `git rm` (history keeps them). Before/after pairs are in `group-b1/`; technical doubts are in `observations-b1.md`.

## Verdicts

Q1 = identical technical information; Q2 = clearly more polished, professional and readable than the original. Counts are original / restyled.

| Figure | Q1 | Q2 | Nodes | Edges | New size (in), placed at 1.0 | Original natural size (in), placed scale |
|---|---|---|---|---|---|---|
| `causal-trace` | YES | YES | 12 / 12 | 17 / 17 (8 solid, 1 dashed, 8 dotted) | 6.89 x 7.62 | 9.51 x 9.11, about 0.74 |
| `context-pipeline` | YES | YES | 11 steps + 3 annotations / same | 10 / 10, plus 3 leader lines | 6.81 x 7.42 | 6.33 x 7.58, about 1.0 |
| `document-ingestion` | YES | YES | 9 / 9 | 10 / 10 (7 solid, 1 dashed, 1 dotted, 1 red) | 6.96 x 7.82 | 8.72 x 8.75, about 0.81 |
| `evaluation-gate` | YES | YES | 13 / 13 | 18 / 18 (1 dashed) | 7.02 x 8.13 | 10.46 x 8.06, about 0.67 |
| `identity-delegation` | YES | YES | 10 / 10 | 11 / 11 (5 dashed) | 6.81 x 7.80 | 7.97 x 12.08, about 0.69 |

All five are drawn at final size: text 9 to 10.5 pt at 100 percent placement (the renderer enforces at least 95 percent scale), none scaled.

### `causal-trace` (two lanes, three side stores)
- **Q1 YES.** Nine run nodes with the policy diamond, three cylinders, the eight solid steps, the dashed "queue / resume" (workflow to tool) and the eight dotted evidence edges, each in its source colour (blue to the trace index, plum to the audit ledger, cyan to the content vault). Checked edge by edge against the source.
- **Q2 YES.** The original ran the dashed edge and the long "model/tool to trace" dotted edges across the whole figure and tangled at "Tool". Now the trace index sits on the left (its four edges run out on the left with no crossing among them), the vault and ledger on the right beside the steps that write to them; the dashed edge has its own lane with a pill.
- Fixed during iteration: `step` is a pgf key (renamed `run step`); the "queue / resume" pill sat against the workflow corner (moved to the lane below the model row).
- Remaining weakness: the dashed lane crosses three dotted edges on the right (the original had more crossings; a planar layout needs a 20 pt lane beyond the stores, which does not fit 7 in).

### `context-pipeline` (ten numbered steps)
- **Q1 YES.** The ten stage labels and their numbers (as badges, "1" to "10"), the red heavier step 3, the blue step 9, the amber manifest with a folded corner (the source's note shape), "model request", and the three margin annotations. No numbers or text added.
- **Q2 YES, modestly.** The original is already clean; the gain is hierarchy (badges, role colour, the emphasised step 3, tinted annotation panels with leaders) and the removal of the empty right half.
- Fixed during iteration: badge touching the text (left indent 2.35 em to 2.75 em); the last step had no glyph slot (paper-plane inside a badge, consistent with the numbered ones); annotation heights equalised.
- Remaining weakness: the right half is empty for seven of ten rows, as in the source.

### `document-ingestion` (Figure 5-3, current source)
- **Q1 YES.** Nine nodes with the two diamonds, the cylinder and the document note; all ten edges including the dotted "re-opens the pinned bytes" (cyan, verify to document), the dashed "repair one field" (route to extract) and both outcomes of the first diamond ("supported" teal, "contradicted or insufficient" red).
- **Q2 YES, clearly.** Pills replace the free-floating labels, the repair loop runs on the outside, the cylinder no longer dominates the left, and the two loops return to their targets without crossing the main flow.
- Fixed during iteration: `\\` does not work inside diamond/cylinder nodes without a `text width` (undefined `\tikzscope@linewidth`); the repair loop's arrowhead hit its rounded corner (lane moved out, radius 14 pt); canvas was 545 pt wide (shifted columns to 493 pt); the cylinder's end caps were huge at the default aspect (set locally to 0.07).
- Remaining weakness: "Supported" curves across empty space to the cylinder; acceptable.

### `evaluation-gate` (Figure 25-1)
- **Q1 YES.** All 13 nodes (cylinder, two notes plus the case note), fan-out of four checks and fan-in to the gate, the three gate outcomes (pass plum, residual risk amber, fail red), the waiver branch (approved + expires, denied), "privacy-reviewed", and the long dashed red "future regression" edge back to the dataset.
- **Q2 YES, clearly.** The original is placed at about 0.67 in the book (a 9.5 pt label prints at about 6.4 pt) with diagonal arrows from every check; now orthogonal bus routing, cards at 9.5 to 10.5 pt, pills on the labelled edges, and the regression loop travels the right margin with its own pill.
- Layout change (logical structure unchanged): the dataset moves to the top right so the dashed edge reaches it along the margin.
- Fixed during iteration: width 513 pt (lane at 464 pt, dataset narrowed); S-curved fan edges replaced by elbow connectors; gate-to-checks arrows clustered next to the "Pass" corner (targets moved inward); height trimmed from 596 to 586 pt.
- Remaining weakness: the check cards break "schema . auth . budget . effects" over two lines; the "Approved + expires" pill covers most of a short edge.

### `identity-delegation` (was 10.4 in tall)
- **Q1 YES.** Ten nodes (diamond, two note cards, cylinder), the eleven edges with directions and styles (five dashed: allow + obligations, delegate, re-check exact action in amber, approved scope, short-lived lease), all labels. The re-check edge is dashed as in the source (the inventory said dotted; see observations).
- **Q2 YES, clearly.** From 8.0 x 12.1 in placed at 0.69 to 6.8 x 7.8 in at 100 percent: the delegation chain in the left column, the credential path in the right, the re-check lane straight up the middle, no edge crossing another.
- Fixed during iteration: gateway-to-LOS arrow slanted (offset anchor); cylinder aspect.

## Local macros proposed for promotion

Each is defined at the top of the figure(s) that use it.
- `\dgdoccorner{node}{role}`: folded corner for a note-shaped card (used in `context-pipeline`, `document-ingestion`, `evaluation-gate`, `identity-delegation`). Four figures of this group repeat it; the source's `shape=note` appears in many other figures.
- `num=<n>` style: round number badge in the card's leading slot (also accepts a glyph, as in the "Model request" badge).
- `note tag=<role>` and `leader=<role>`: annotation panel and a thin leader line (`context-pipeline`).
- `check`, `run step`: figure-specific sizing; not for promotion.
- Style-guide note to add: for decision and store nodes, always set `text width` when the label uses `\\` (otherwise XeLaTeX stops with an undefined `\tikzscope@linewidth`); and for wide cylinders set `aspect` to about 0.07 to 0.14.

## Validation (venv paths from the brief, in `wt-dg-b1`)

| Check | Result |
|---|---|
| `make diagrams` | pass; only the five figures' PDF/PNG changed (PNG/PDF of the other 39 untouched); second run idempotent |
| `make assemble build references latex latex-validate validate` | pass, 0 errors, 0 warnings, 44 markers = 44 registered, DOCX 73 images |
| `make examples-run` | pass, 30 tests |
| `make pdf` | pass, 359 pages, 0 Overfull `\hbox`, no undefined references |
| Figures in the compiled PDF (pages 87-88, 103, 246, 274, 285) | rendered and inspected: fonts embedded, 100 percent placement, margins and caption alignment correct, text readable |

## Notes for the integrator

- `config/diagrams.json` still points these five ids at the removed `.gv` files. I set the five `source` values to `assets/diagrams/src/<id>.tikz.tex` locally to validate but left the file unstaged as instructed; the integrator must make that change (or the renderer falls back by id, but `latex-validate` fails with "editable source is missing") and let `make diagrams` rewrite the checksums.
- No installs. `professional-diagrams.sty` was not edited.
