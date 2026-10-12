# Group f report: before/after panel figures

Branch `diagrams/f`. Five figures converted from Graphviz to TikZ. Before/after pairs are in `group-f/`.

## Shared template
The four `anti-*` figures and `pattern-hitl` share `assets/diagrams/src/_before-after.tex` (a local include, not a figure), which defines `\dgpanel` (panel plus centred header pill with icon and title, optional subtitle) and `dg note` (dog-eared note card). Each figure source `\input`s it, so panels, headers, arrow clearances and the note shape are identical across all five.

Semantics kept: red for the anti-pattern, teal for the correction. Without colour: the anti-pattern panel has a dashed border, the correction a solid one; headers carry a cross or tick icon and the words ANTI-PATTERN / CORRECTION. The ANTI-PATTERN / CORRECTION captions sat at the foot of each column in the Graphviz render (a `dot` ordering artefact, per the source comment); they are now headers at the top. This is a layout change only.

## Per figure (all YES / YES)

| Figure | Nodes before / after | Edges before / after | Notes |
|---|---|---|---|
| `anti-ambient-authority` (17-2) | 7 + 2 captions / 7 + 2 headers | 5 / 5 | Diamond, two cylinders kept. Left chain spread to the height of the right. |
| `anti-approval-binding` (17-4) | 8 + 2 / 8 + 2 | 6 / 6 | Read from the CURRENT source (v3 to v5, "Approval bound to digest . expires", "Commit . key = logical effect"). Both notes are dog-eared notes; "yes" is a pill. |
| `anti-before-after` (17-1) | 6 + 2 clusters + 1 label / same | 1 dashed amber edge via label / same | Panel titles keep source wording (Anti-pattern / the autonomous monolith; Governed / the same capabilities, separated); label is a pill on the edge. The source draws no edges inside clusters; none added. |
| `anti-retry-storm` (17-3) | 10 + 2 / 10 + 2 | 8 / 8 | Pills "transient" and "unknown". Both panels share one top and bottom. |
| `pattern-hitl` (14-1) | 8 + 2 / 8 + 2 | 8 / 8 | Heading arrows into the first step kept; rows aligned as in the source (rank=same). |

Problems found and fixed while iterating: unequal panel heights and header positions (added extent coordinates so both panels share top and bottom); cylinders too tall at the default aspect (aspect 0.12); note shape showed a shadow bleeding past the cut corner (the note no longer uses the card shadow); pill touching a diamond tip (gap increased to 44 pt); a line break that left "cancel" with a stray dot (break kept as in the source); header pill height mismatch in 17-1.

Remaining weaknesses: the shorter column in `anti-ambient-authority` and `anti-before-after` has long arrows or wide spacing; the "→" in the retry card renders small in Liberation Sans. Both are cosmetic.

## Placement and sizes
All five natural width 7.095 in (placed at 99.5 percent, so 9 pt labels print at about 8.95 pt); heights 4.57 to 6.85 in. `make diagrams` passes.

## Local macros proposed for promotion
`\dgpanel`, `panel head`, `dg note` (and `\dgpanelw`, `\dgheadgap`) from `_before-after.tex`.

## Validation
`make diagrams`: pass, only the five figures changed. `assemble build references latex latex-validate validate`: pass, 0 errors, 0 warnings. `examples-run`: 30 passed. `make pdf`: XeLaTeX compile succeeded (359 pages), 0 Overfull warnings; figures inspected on book pages 170 (14-1), 195 (17-1), 199 (17-2), 201 (17-3), 204 (17-4): fonts embedded (Liberation Sans, FontAwesome 5), margins and captions aligned. Installs: none.

`config/diagrams.json` (source paths and checksums) and `reports/diagram-render-report.json` are modified locally but not committed, for the integrator's `make diagrams` run.
