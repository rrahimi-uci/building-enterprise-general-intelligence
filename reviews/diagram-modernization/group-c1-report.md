# Group c1 report: layered, grouped and tiered architecture figures (7)

Branch `diagrams/c1` (from `main` at a5a98e1). Seven Graphviz figures converted to native TikZ with the shared `professional-diagrams.sty` (not edited). Sources: `assets/diagrams/src/<id>.tikz.tex`; the `.gv` sources are removed with `git rm`. Before/after pairs: `group-c1/<id>-before-after.png`. Technical doubts: `observations-c1.md`.

Natural size and placement scale (from `make diagrams`; the validator refuses below 0.95): see the table.

| Figure | Natural size (in) | Placement scale | Smallest text |
|---|---|---|---|
| `developer-platform` (7-1) | 6.76 x 5.62 | 1.045 | 9 pt |
| `gateway-roles` (1-4) | 7.10 x 7.04 | 0.995 | 9 pt |
| `knowledge-fabric` (5-1) | 6.75 x 6.03 | 1.046 | 9 pt |
| `portability` (7-2) | 7.17 x 3.95 | 0.985 | 9 pt |
| `runtime-boundary` (3-1) | 7.11 x 8.17 | 0.993 | 9 pt |
| `runtime-offline` (25-2) | 7.06 x 4.13 | 1.0 | 9 pt |
| `security-boundaries` (20-2) | 6.92 x 6.46 | 1.02 | 9 pt |

(The originals printed at 3.5 x 7.2 in to 7.5 x 10.7 in, several shrunk; `gateway-roles` printed its smallest labels near 8 pt.)

## Per figure

### `developer-platform`
- **Q1 identical information: YES.** 4 bands, 4 cells each (16 cells); every label, including the "domain-owned" sub-label under "Skills · Skill Packs". The source's four tier-to-tier edges are invisible (`style=invis`), so none is drawn (0 edges before, 0 after).
- **Q2 clearly more polished: YES.** Solid dark header bars with white text became tinted groups with titled bands and rounded cards; consistent plum / teal / blue / red roles as before.
- Fixed during iteration: cell text baseline drift (descenders moved some cells 1 pt; `\strut`), the "Skills" cell had bold title (now regular like its siblings, sub-label in annotation style).

### `gateway-roles`
- **Q1: YES (current source, "A2A Gateway").** 11 nodes, 11 edges before and after; directions kept; dashed edges stay dashed (protected effect, external tools, external tasks); the double-headed agent/A2A edge stays double-headed; diamond (Human approval), cylinder (Systems of record) kept. All labels kept (capitalised).
- **Q2: YES.** Original was 7.5 in wide in a 10 x 6.7 layout shrunk to fit; redrawn at 1.0 with pills, orthogonal routing and the four outside nodes on one bottom row.
- Layout changes (logical structure unchanged): Tool Gateway centred, LLM Gateway left, A2A right so the outputs fan out below; the external nodes (Model providers, External MCP servers, Systems of record, External agents) sit on one bottom row.
- Fixed: "Read or pre-approved" pill hit the tool-to-sys line when the cylinder was offset; "Approved once" pill hid an arrowhead (bottom row lowered); cylinder too tall (`aspect=0.15`); diamond text (manual `\\` inside `\dgcontent` fails, used `text width` wrapping).

### `knowledge-fabric`
- **Q1: YES (current source, "release" in the governance list).** 5 bands/rows: Governance bar, 4 representation cells (blue / cyan / red / plum as in the source, with sub-labels), API bar, 4 mode cells (bold name + sub-label), Agent runtime bar; 4 edges (dashed amber "governs" + 3 plain) kept.
- **Q2: YES.** Tables with hairline borders became cards in two row panels; edges land on the row panels (the source landed them on the table), so "governs" is visibly aimed at the whole representations row.
- Fixed: first draft was 508 pt wide with bars narrower than the panels (re-gridded to 454 pt text width); arrow too close to the "Governs" pill (pitch increased).

### `portability`
- **Q1: YES.** Application code, Platform contracts (+ "AgentSpec · AgentStepRequest · ToolManifest"), two dashed groups (Framework adapters: Agents SDK, Graph runner; Provider adapters: Model A, Model B), 2 dotted "or" links (no arrowhead), 2 dashed "swap" edges landing on the groups, 1 solid "the only dependency" edge: 6 nodes + 2 clusters, 5 edges before and after.
- **Q2: YES.** Dashed groups with the pilot's treatment; "swap" and "or" are pills.
- Remaining weakness: the "or" pill breaks the dotted link into two short dotted stubs; acceptable.

### `runtime-boundary`
- **Q1: YES.** 11 nodes, 1 cluster, 12 edges before and after, labels, directions and styles kept (two dashed slate edges between Agent loop and Model provider, dashed amber "re-check exact action", red "denied", plum "verified commit", dotted plum "linked evidence"). The two note shapes (AgentStepRequest / AgentStepResult) are cards with a document icon (the note's folded corner is the only thing lost).
- **Q2: YES.** The original was 7.9 in wide x 9.8 in tall, shrunk; the redraw is 7.11 x 8.17 in at scale 0.993 by putting the result contract at the top right and the policy chain on the bottom right.
- Fixed: first layout was 593 pt tall (at the limit) and the policy-to-domain/refuse curves were uneven (diamond widened so both anchors drop straight); the "Re-check exact action" pill touched the arrow (gap widened); cylinder too tall.
- Remaining weakness: tall; pills on the short allowed/denied/verified-commit runs have only about 10 pt of arrow clearance.

### `runtime-offline`
- **Q1: YES (current source).** Two clusters (Runtime: 3 steps; Offline: Diagnose from traces, Propose change, Validate on held-out set, Owner approval (amber, rounded as in the source), Release with rollback), 6 chain edges + 1 dashed amber bridge "evidence, not a change" landing on the Offline cluster.
- **Q2: YES, clearly.** The 3.5 x 7.2 in column became a 7.06 x 4.13 in figure: both chains run left to right; the bridge leaves the last runtime step and lands above the first offline step; Offline title is below (the bridge enters from above).
- Layout change: the chains are horizontal instead of vertical (logical order unchanged).

### `security-boundaries`
- **Q1: YES.** 7 nodes + 2 dashed clusters (title at the bottom, as in the source), 6 edges: delegated grant, bounded step, prompt (dashed blue), never trusted (dashed red), proposal re-authorized (amber), committed effect; cylinder kept; the two dashed edges still cross the boundary line.
- **Q2: YES.** The two parallel crossings are now clean horizontals (prompt, never trusted) instead of a long diagonal; the trust boundary title is right-aligned so the effect edge does not cross it.
- Fixed: the two crossing pills were 20 pt apart (anchors moved to +/-14 pt); title collided with the tool-to-sys edge (right-aligned local group label).

## Local macros proposed for promotion to `professional-diagrams.sty`
- `\dgcell` / `\dgcellrow` (`developer-platform`): a centred 92 pt card in a tier band.
- `\dgrowcell` / `\dgrowpanel` (`knowledge-fabric`): a row cell and an untitled hairline panel around a row, useful as an arrow target (a `\dgband` equivalent: panel with no title).
- `\dgadapter` (`portability`), `\dgstep` (`runtime-offline`): thin wrappers; not worth promoting.
- A right-aligned bottom group label (`security-boundaries`, written inline): `\dggroupbelow` variant with `anchor=south east` for groups whose centre edge would cross a left-aligned title.
- Findings for the package: `\dgcontent` fails when an argument contains `\\` (etoolbox `\ifblank` on a non-expandable `\\`); give decisions a `text width` or avoid manual breaks. Cylinder default `aspect=0.22` is too tall on wide stores; the figures set `aspect=0.1 to 0.15`.

## Validation (on this branch)

| Check | Result |
|---|---|
| `make diagrams` | pass; only the 14 renders of these seven figures changed (all others byte-identical); placement scales 0.985 to 1.045 |
| `make assemble build references latex latex-validate validate` | pass, 0 errors, 0 warnings |
| `make examples-run` | pass, 30 passed |
| `make pdf` | pass; 362 pages, 0 Overfull `\hbox` in the XeLaTeX log; all seven figures inspected on their compiled pages (116, 37, 80, 117, 57, 290, 236): fonts embedded (Liberation Sans, FontAwesome 5 Free), 6.9 to 7.1 in wide, captions aligned, text legible |

## Integrator notes
- `config/diagrams.json` must point these seven entries at `assets/diagrams/src/<id>.tikz.tex` (done locally to render, left unstaged); `make diagrams` then rewrites the checksums.
- Not committed: `config/diagrams.json`, `CHANGELOG.md`, `reports/`, generated book artifacts.
