# Pilot report: TikZ modernization of the book's diagrams

Branch `feat/diagram-modernization` (from `origin/main` at 2d1d480). Pilot only: three figures converted, 41 untouched.

## What was built

| Piece | Where |
|---|---|
| Shared TikZ design system (palette, cards, decision, store, chip, pill, callout, groups, connectors, icons, type scale) | `latex/styles/professional-diagrams.sty` |
| Pipeline: `.tikz.tex` sources rendered by XeLaTeX to a cropped vector PDF, PNG rasterised from it at the 255 dpi contract; loud failures; registry checksums kept in sync | `tools/render_diagrams.py` |
| Validators: TikZ source loads the package, has a vector render, embeds fonts; source suffix recognised | `tools/validate_latex.py` |
| Docs: source types, drawing rules | `AGENTS.md`, `styles/DESIGN-SYSTEM.md` section 10a, `latex/README.md`, `README.md`, `Makefile`, `CHANGELOG.md` |
| TeX package bootstrap for diagram rendering | `tools/bootstrap_tex.sh --diagrams` |
| Inventory of 44 figures, style guide, style sheet, content observations, before/after pairs | `reviews/diagram-modernization/` |
| Three restyled figures | `assets/diagrams/src/{pattern-reflection,governance-model,effect-lifecycle}.tikz.tex` (the `.gv` sources are removed; git history keeps them) |

Pipeline behaviour verified: a TikZ error fails `make diagrams` with exit 1 and the first TeX error (tested with an undefined macro); a second run leaves every PNG, PDF and the registry byte-identical; the PDF is byte-stable (fixed `SOURCE_DATE_EPOCH`); a figure placed below 95 percent scale or with an unembedded font fails the render; a checkout with no Graphviz sources would not need `dot`.

## The three pilots

Pairs are in `pilot/` (rendered as the book places them) and embedded in `style-guide.md`.

### 1. `pattern-reflection` (Figure 13-1): flow with feedback loop

- **Question 1, identical technical information: YES.** All 8 nodes, all 9 edges with original direction and style (the two dashed edges stay dashed), and every label survive: "fails · judge skipped", "score + rationale · never self-accepts", "accepted", "rejected", "escalated / cap · no progress", "while under cap". The four words "schema · evidence · arithmetic · policy" became four chips. Nothing from the reference image's invented content was added (no step badges, no bullets).
- **Question 2, clearly more polished: YES.** Cards with icons and shadow hairlines, role-coloured pills, an outside rounded feedback loop, balanced columns, 9 to 10.5 pt text at 100 percent placement (the original printed at about 10 pt, with the "score + rationale" label running into the dashed edge).
- Problems found and fixed during iteration: pill shapes were distorted when a pill sat on a rounded path (inherited the path's corner radius; fixed with `sharp corners` and a capsule shape); the "While under cap" pill and the loop corner collided and pushed the canvas past 7.06 in (pill now placed explicitly on the top run); the judge-to-engine arrowhead was hidden by its pill (moved the gate right, pill centred on the straight run); the chk-to-gate dashed line was slanted by 10 pt (aligned anchors); pill tint too grey (explicit per-role tints).

### 2. `governance-model` (Figure 26-1): grouped architecture

- **Question 1: YES.** Two groups with their titles, six cards, three labelled solid edges, the dashed amber "high-risk only" edge from "Supply chain agents" to the board, square vs rounded card corners as in the source. The "Domain teams" title stays at the bottom as in the source.
- **Question 2: YES, modestly.** The original is already clean; the gain is hierarchy (group tint, card icons, pills, aligned grid). It is the least dramatic of the three and relies on icons for visual interest (see open decision 3).
- Problems found and fixed: arrows crossed the "Domain teams" label when it was placed at the top (moved to the bottom as in the source); long words hyphenated ("excep-tions", fixed globally by disabling hyphenation); the dashed-edge pill sat on the group border (moved down the edge).

### 3. `effect-lifecycle` (Figure 22-1): state machine, 12 states and 16 transitions

- **Question 1: YES.** All 12 states with their two-line labels, both diamonds, all 16 transitions with their labels, directions, and solid/dashed styles (checked edge by edge against `effect-lifecycle.gv` in git history, including the two arrows that now point upward, "found committed" and "proven absent").
- **Question 2: YES, clearly.** The original is scaled to 0.78 in the book (10.7 in tall), so its edge labels print at about 8.6 pt and every edge label floats beside a long curve. The redraw is 6.9 x 8.2 in, placed at 1.0, text at 9 to 10.5 pt, every label is a pill on its own edge, and the three columns separate the happy path, the failure paths and the compensation chain.
- Problems found and fixed: the first layout was 572 pt wide (declined and approval collided on the right); the "denied / expired" and "precondition fails" routes overlapped (distinct anchors, two-line pill); a backward stub on the "reversal fails" detour.

## Validation (all on this branch, with the venv paths from the brief)

| Check | Result |
|---|---|
| `make diagrams` | pass; whole set about 23 s (each TikZ compile 3 to 4 s); only the three pilot renders changed |
| `make assemble build references latex latex-validate validate` | pass, 0 errors, 0 warnings; 44 markers = 44 registered; DOCX 73 images (expected 73) |
| `make examples-run` | pass; 30 tests in `tests/mortgage_case` passed |
| `make deterministic` | DOCX byte-identical across two builds (`c22796a0...`) |
| `make pdf` | 359 pages (same as a recent main build), 0 Overfull `\hbox` (none above 3 pt), no undefined references |
| `make package` into the scratchpad, clean extract | `validate_latex`, `render_diagrams --check` pass from the extracted package; manifest and checksums regenerated |
| Figures in the compiled PDF (pages 163, 253, 299) | fonts embedded (Liberation Sans, FontAwesome 5 Free), 7.0 in wide, margins and caption alignment correct, text readable |
| Greyscale | all three read in greyscale; role is carried by shape, line style and label text (red and blue edges are indistinguishable in grey, as they were in the originals; the pill words say which path it is) |

Measured contrast for the palette is in the style guide (all text pairs at least 5.2:1, ink at least 12.4:1).

## Remaining visual weaknesses

- `governance-model` is plain next to the other two; icon choices there are the most subjective (see `content-observations.md`).
- Shadows are faint by design; at 110 dpi screen they are barely visible. If the author wants more depth, one constant changes it.
- The reference image's hand-drawn curved arrows with variable width are not reproduced; connectors are uniform 1.2 pt. This is deliberate (print, greyscale, consistency).
- The effect-lifecycle bottom detour ("reversal fails") is long; a placement with the compensation chain on the right would shorten it but would cross the reconcile fan. Acceptable.
- Pills on a curved path (`Accepted`, `Cannot prove`) sit on the curve's midpoint, which can look off-centre against the arrow; fine at print size.
- Figures are float pages with a lot of white space (`\BookDiagram` is `[htbp]` and several diagrams share a page with only their caption). Not changed.

## Conversion plan for the other 41

Estimates are agent iteration time per figure including inspection (E about 30 min, M about 75 min, H about 2.5 h): about 4 h + 26 h + 30 h, roughly 60 h in total, 8 to 10 sessions. Proposed groups, in order:

| # | Group | Figures | Effort | New construct needed |
|---|---|---|---|---|
| 1 | Stacks, ladders, maps (4) and tier bands | `security-depth`, `book-map`, `capability-ladder`, `deterministic-shell`, `developer-platform`, `knowledge-fabric` | 6 x E/M, about 5 h | `\dgrow` (row card with number chip), `\dgband` (tier band with cell row) |
| 2 | Before/after pairs | `anti-ambient-authority`, `anti-approval-binding`, `anti-before-after`, `anti-retry-storm`, `pattern-hitl` | 5 x M, about 6 h | one two-panel macro with ANTI-PATTERN / CORRECTION headers |
| 3 | Flows with feedback loops | `pattern-react`, `pattern-planning`, `pattern-durable`, `learning-loop`, `dx-golden-path`, `reliability-economics`, `supervisor-worker` | 5 M + 2 H, about 9 h | ring layout helper; same loop and pill styles |
| 4 | Decision trees | `model-routing`, `pattern-routing`, `pattern-decision-tree` | 2 M + 1 H, about 5 h | yes/no pills (exists), two-pane frame |
| 5 | Vertical pipelines and state machines | `context-pipeline`, `policy-to-guardrail`, `mortgage-case-lifecycle`, `release-recovery`, `sandbox-egress`, `skill-resolution`, `document-ingestion`, `identity-delegation`, `evaluation-gate`, `causal-trace` | 2 E, 4 M, 4 H, about 14 h | nothing new; two-lane helper optional |
| 6 | Layered, grouped and plane architectures | `system-overview`, `gateway-roles`, `knowledge-lifecycle`, `runtime-boundary`, `runtime-offline`, `portability`, `security-boundaries`, `reference-architecture` | 3 M, 2 E, 3 H, about 14 h | dashed groups (exists), side rails, `reference-architecture` needs a compact 42-chip layout |
| 7 | Sequence diagrams | `guardrail-sequence`, `request-sequence` | 2 H, about 5 h | sequence kit (lifelines, messages, `alt`/`opt` frames, notes) |

Group 7 is the only one that needs a new kit; the alternative (keep Mermaid, restyle `_theme.mermaid.json`) is described in the inventory. Do the tall flows last: `identity-delegation`, `knowledge-lifecycle`, `pattern-decision-tree` are 10.4 to 10.7 in tall in Graphviz and must be redrawn compactly (at most 8.3 in) or `make diagrams` will refuse them.

## Installs performed

- `tlmgr --usermode install standalone fontawesome5` (BasicTeX 2026; installed into `~/Library/texmf`, no sudo). `shadows.blur` is not part of this TeX Live (it needs the separate `pgf-blur` package), so shadows use the stock `shadows` library; no further package was needed. `tcolorbox` was already in the user tree.
- No system packages, no Python packages. `poppler` (`pdftoppm`, `pdfinfo`, `pdffonts`) was already present.

## Risks

- **DOCX raster quality.** The PNG is rasterised from the PDF with poppler at 300 to 314 dpi effective (2069 to 2148 px wide), above the 255 dpi contract; shadows and thin lines survive. PNGs are 130 to 300 KB (similar to the originals), so the DOCX did not grow (44.95 MB against 45.19 MB).
- **Greyscale print.** Verified for the pilots. Hue differences vanish (as before); distinctions that matter rely on shape, dash style and text.
- **Build time.** About 4 s per TikZ figure; 44 figures would add roughly 3 minutes to `make diagrams`, which is a local-only target.
- **CI.** CI never renders diagrams, only validates committed renders and compiles the book from them. Contributors who edit a `.tikz.tex` need `standalone`, `fontawesome5` and poppler locally; the container build is unaffected. A CI job that re-renders and diffs would catch a stale render, at the cost of a TeX Live image with `fontawesome5`; not added.
- **Single point of change.** One edit to the `.sty` restyles every converted figure, including the checksums of all of them; regenerate with `make diagrams` and review contact sheets.
- **Font Awesome licence.** FontAwesome 5 Free is SIL OFL 1.1 for the font (icons CC BY 4.0). The icons appear only in the rendered figures; the CTAN package is not redistributed in the repo. A line in the book's credits may be wanted for CC BY attribution.
- **Fixed dates.** The PDFs embed 2026-01-01 as their creation date so they are byte-stable.

## Open decisions for the author

1. Go ahead with bulk conversion, and in which PR granularity: by type group as proposed above (7 PRs; each regenerates the 45 MB DOCX), or by Part as for the prose (a Part's figures are spread over several groups, so shared-style fixes would land in different PRs).
2. Sequence diagrams: native TikZ kit (recommended) or restyled Mermaid.
3. Icons: keep them throughout, keep them only where they name the concept, or drop them (the governance figure is where they are most open to question).
4. The six content questions in `content-observations.md` (the review-board edge, the one-to-one control-to-team pairing, the missing "Partial" exit, the shared "Declined" state, the dashed approval edges, the colour of the "fails" edge): confirm or correct the source, then I will follow.
5. Whether `navy` and `green` (the two roles added to the house palette) should be in `styles/DESIGN-SYSTEM.md` section 10a's role table, and whether to record the new type scale there.
6. Whether to remove the Graphviz sources of converted figures (done in the pilot) or keep them beside the TikZ for a release.
