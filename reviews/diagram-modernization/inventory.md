# Diagram inventory (44 figures)

Source of truth for the modernization. Counts come from `dot -Tplain` on each source with the house theme spliced in (nodes include invisible helper nodes only where the source has labelled ones; HTML-table figures count one node per table). Natural size is the Graphviz layout in inches; the book places a figure at 7.06 in wide, at most 8.3 in tall.

Difficulty: **E** easy (a stack of cards, no routing), **M** medium (some routing, groups or two columns), **H** hard (dense routing, long feedback edges, or a new construct).

Status: three figures are converted in the pilot (marked PILOT in the notes); 41 remain.

## Grouping

| Group | Figures | Count | What the TikZ system must provide |
|---|---|---|---|
| A. Flows with feedback loops | `dx-golden-path`, `learning-loop`, `pattern-durable`, `pattern-planning`, `pattern-react`, `pattern-reflection`, `reliability-economics`, `supervisor-worker` | 8 | loop card flow; large-radius outside feedback path (`rounded corners` + `|-`); pill on a path; side card with dashed link; ring layout for cycles (polar placement) |
| B. Vertical pipelines and state machines | `causal-trace`, `context-pipeline`, `document-ingestion`, `effect-lifecycle`, `evaluation-gate`, `identity-delegation`, `mortgage-case-lifecycle`, `policy-to-guardrail`, `release-recovery`, `sandbox-egress`, `skill-resolution` | 11 | vertical rank layout by explicit coordinates; diamond decision; cylinder store; note/doc shape; pills on every edge; elbow and curved paths; a "lane" helper for two-column pipelines |
| C. Layered, grouped and plane architectures | `developer-platform`, `gateway-roles`, `governance-model`, `knowledge-fabric`, `knowledge-lifecycle`, `portability`, `reference-architecture`, `runtime-boundary`, `runtime-offline`, `security-boundaries`, `system-overview` | 11 | `\dggroup` / `\dggroupbelow` container (done); dashed boundary variant (done: `dg group dashed`); tier band with cell row (to add: `\dgband`); side rail; cross-group labelled edges |
| D. Stacks, ladders and maps | `book-map`, `capability-ladder`, `deterministic-shell`, `security-depth` | 4 | row card with number/chip + title + description (to add: `\dgrow`); consistent row pitch; emphasised variant (heavy border); column headers |
| E. Decision trees | `model-routing`, `pattern-decision-tree`, `pattern-routing` | 3 | diamond with yes/no pills (done); two-pane stacked frame for the two-part decision tree; leaf cards with chapter references as annotation |
| F. Before/after pairs | `anti-ambient-authority`, `anti-approval-binding`, `anti-before-after`, `anti-retry-storm`, `pattern-hitl` | 5 | two titled side-by-side panels (group style) with ANTI-PATTERN / CORRECTION captions as pills or headers; red-line anti-pattern cards |
| G. Sequence diagrams (Mermaid) | `guardrail-sequence`, `request-sequence` | 2 | new sequence kit: participant header, dashed lifeline, solid/dotted message arrows with labels, self-message loop, `alt`/`opt` frame with title tab, note box (about 60 lines of macros) |

## Per-figure inventory

| id | group | nodes | edges | notable constructs | difficulty |
|---|---|---|---|---|---|
| `anti-ambient-authority` | F | 9 | 6 | two side-by-side columns with "ANTI-PATTERN"/"CORRECTION" captions; diamond decision, cylinder store, note | M |
| `anti-approval-binding` | F | 10 | 7 | two columns; note shape (immutable proposal); diamond; red/teal captions | M |
| `anti-before-after` | F | 7 | 6 | two titled clusters joined by one dashed amber edge; cylinder; 4-line cluster titles | M |
| `anti-retry-storm` | F | 12 | 9 | two columns; multiplier labels (x2, x3, x0); diamond; cylinder; short edge labels | M |
| `book-map` | D | 8 | 7 | HTML-table rows: Part number chip + title + topics strip, 8 rows, 8 hues | E |
| `capability-ladder` | D | 15 | 14 | 3 column header text, 4 rows of 3 pills, each column its own hue | E |
| `causal-trace` | B | 12 | 17 | two lanes, 9 dotted edges to 3 side stores (cylinders), 1 dashed, diamond | H |
| `context-pipeline` | B | 15 | 14 | 10 numbered steps, margin annotations, note shape for the manifest | E |
| `deterministic-shell` | D | 14 | 19 | 6-step gate column plus a "what it refuses" column joined by 5 dashed edges | M |
| `evaluation-gate` | B | 13 | 18 | fan-out/fan-in of 4 checks, diamond gate, waiver branch, long dashed regression feedback edge, cylinder, notes | H |
| `developer-platform` | C | 4 | 3 | 4 coloured tier bands each with a row of cells (HTML tables) | E |
| `dx-golden-path` | A | 9 | 11 | one cluster, serpentine 2x4 cycle, note below with two dashed edges | M |
| `gateway-roles` | C | 11 | 11 | gateway tree: 3 gateways, diamond, cylinder, 3 dashed, edge labels | M |
| `governance-model` | C | 7 | 4 | PILOT. two clusters, labelled edges, one dashed | M |
| `guardrail-sequence` | G | 6 | 12 | 6 participants, alt inside alt (not permitted / permitted / requires approval), self-message, dotted returns | H |
| `knowledge-fabric` | C | 5 | 4 | HTML-table bands: 4-cell row, API bar, 4-cell row, runtime bar, one dashed "governs" edge | M |
| `learning-loop` | A | 10 | 10 | 10-node ring (cycle) in two hues, 1 amber approval node | M |
| `model-routing` | E | 7 | 7 | 3 diamonds, yes/no labels, 2 terminal outcomes + refuse | M |
| `pattern-decision-tree` | E | 13 | 12 | two stacked titled clusters, 6 diamonds, yes/no/then labels, chapter refs in leaves; 10.7 in tall | H |
| `pattern-durable` | A | 6 | 7 | resume loop, cylinder x2, dashed process-dies path | M |
| `pattern-hitl` | F | 10 | 13 | two columns APPROVAL / INTERVENTION, note shape | E |
| `pattern-planning` | A | 6 | 6 | diamond with 3 exits, dashed replan loop back to the compiler | M |
| `pattern-react` | A | 6 | 6 | loop Reason-Act-Observe, 2 dashed, 3 exits from Reason | M |
| `pattern-reflection` | A | 8 | 9 | PILOT. loop + decision exits + dashed skip path + cap side node | H |
| `pattern-routing` | E | 7 | 9 | diamond classifier, 3 outcomes, dashed convergence to authorization | M |
| `policy-to-guardrail` | B | 8 | 7 | linear chain, diamond, note, rejection branch | E |
| `document-ingestion` | B | 9 | 13 | two diamonds, cylinder, note, dotted and dashed loops back to earlier nodes (repair, re-open) | H |
| `knowledge-lifecycle` | C | 13 | 20 | two dashed clusters (control plane / runtime plane), 2 diamonds, 6 dashed edges, cylinders, notes; densest flow; 8.3 x 10.7 in | H |
| `portability` | C | 6 | 5 | two dashed clusters (framework / provider adapters), dotted "or" edges, swap labels | M |
| `reference-architecture` | C | 42 | 48 | 9 clusters (6 plane bands + 2 side rails), 42 chips, cross-plane labelled edges, 3 dashed 3 dotted; 9.2 x 10.1 in. Largest figure | H |
| `request-sequence` | G | 8 | 16 | actor + 7 participants, note, opt block, self-messages, dotted returns | H |
| `release-recovery` | B | 10 | 11 | diamond, 3 dashed, two parallel branches converging | M |
| `reliability-economics` | A | 9 | 12 | diamond x2, 3 dashed + 3 dotted, feedback edges to admission and usage store | H |
| `runtime-offline` | C | 8 | 7 | two stacked clusters (runtime / offline), 1 dashed bridge; 3.5 x 7.2 in | E |
| `runtime-boundary` | C | 11 | 12 | one cluster, diamond, note, cylinder, dotted evidence edge | M |
| `mortgage-case-lifecycle` | B | 9 | 9 | diamond, 3 dashed, note, side branches | M |
| `security-boundaries` | C | 7 | 6 | two dashed trust-boundary clusters, 4 dashed edges, cylinder | M |
| `security-depth` | D | 9 | 8 | 9 numbered layer rows, one emphasised (heavy border) | E |
| `identity-delegation` | B | 10 | 11 | diamond, 5 dashed edges, notes, cylinder, dotted re-check loop, tall (10.4 in) | H |
| `effect-lifecycle` | B | 12 | 16 | PILOT. two diamonds, 5 dashed, labelled pills on every edge | H |
| `sandbox-egress` | B | 11 | 12 | diamond x2, notes, side store, refuse branch | M |
| `skill-resolution` | B | 9 | 9 | DISCOVERY / RESOLUTION side headings, notes, diamond, refusal branch | M |
| `supervisor-worker` | A | 11 | 17 | fan-out/fan-in (3 children, 3 workers), diamond, long dashed ownership edge, 2 free annotations | H |
| `system-overview` | C | 21 | 23 | 8 HTML-table layer rows, two side rails (Security, Platform) as clusters, dashed and dotted cross-edges | H |

## Sequence diagrams (`.mmd`): how they will be handled

`guardrail-sequence` (6 participants, nested `alt`) and `request-sequence` (actor, 7 participants, `opt`, a note, 16 messages) are the only Mermaid sources. Mermaid cannot load the shared fonts, palette, pills or icons, so these two would always look different from the other 42. Recommendation: draw them natively in TikZ with a small sequence kit added to `professional-diagrams.sty` (participant header cards, dashed lifelines, solid and dotted message arrows with labels, self-message loop, `alt`/`opt` frames with a title tab, note box). Both figures are portrait and narrow (about 6 in) so label size is not a problem. This is the one place the style system needs a new construct rather than a new combination of existing ones. A cheaper fallback, if the author prefers not to maintain a sequence kit, is to keep Mermaid and restyle `_theme.mermaid.json` to the palette and font; that gets colour and typeface right but not the card, pill or icon language.

## Observations from reading the contact sheet

- Placed text is already below the 9 pt floor in about a dozen figures. Graphviz lays these out at 7.5 to 9.4 in wide or 10.1 to 10.7 in tall, and the book shrinks them to fit 7.06 x 8.3 in (scale 0.75 to 0.85), so the smallest declared label prints at roughly 7.5 to 9 pt: `system-overview`, `reference-architecture`, `evaluation-gate`, `gateway-roles`, `pattern-decision-tree`, `knowledge-lifecycle`, `identity-delegation`, `supervisor-worker`, `reliability-economics`, `sandbox-egress`, `skill-resolution`. A TikZ redraw fixes this only if the figure is redrawn compactly at final size; `make diagrams` now fails a TikZ figure that would be placed under 95 percent scale.
- Four figures are the same before/after template (`anti-*`) and `pattern-hitl` is a two-column variant; they should share one macro and be converted together.
- `security-depth`, `book-map`, `capability-ladder` and `deterministic-shell` are stacks of row cards that Graphviz draws as HTML tables; these are the cheapest wins and the ones most improved by the card language.
- `reference-architecture` (42 nodes, 9 groups) and `system-overview` are the only figures that will need real design work beyond the shared styles.
