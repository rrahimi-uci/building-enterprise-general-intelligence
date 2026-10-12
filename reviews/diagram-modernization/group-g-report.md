# Group g report: sequence diagrams (Figures 20-3 and 4-2)

Both figures were the only Mermaid sources. They are now native TikZ built on `professional-diagrams.sty` plus one local kit, `assets/diagrams/src/_sequence-kit.tex`, which both figures `\input`. No change to `latex/styles/professional-diagrams.sty`, tools, config (other than the registry `source`/`sha256`, left unstaged) or docs.

## Verdicts

| Figure | Same technical information? | Clearly more polished? | Natural size / placement |
|---|---|---|---|
| `guardrail-sequence` (20-3) | YES | YES | 6.99 x 7.84 in, scale 1.00 |
| `request-sequence` (4-2) | YES | YES | 6.99 x 8.11 in, scale 1.00 |

Before/after: `group-g/guardrail-sequence-before-after.png`, `group-g/request-sequence-before-after.png` (left original, right new).

## Element maps (before and after)

`guardrail-sequence`: 6 participants, 12 messages (3 self-messages, 4 solid, 5 dotted), 2 alt blocks (outer with [not permitted] / [permitted] divider, inner [requires human approval]). After: 6 header cards, 6 lifelines, 12 messages in source order with the same solid/dotted style and the same labels (the source's `<br/>` breaks became a two-line pill), 2 frames and 1 divider with the same bracketed conditions. Count verified item by item against the current `.mmd` (`git show origin/main:assets/diagrams/src/guardrail-sequence.mmd`).

`request-sequence`: 1 actor + 7 participants, 16 messages (2 self), 1 note over Run Service..Policy & Identity, 1 opt frame [protected change]. After: 8 headers (the actor as a capsule with a person icon), 8 lifelines, 16 messages, 1 note box, 1 opt frame. No step numbers (the source has none by design).

Nothing added; nothing omitted. Typography changes only: none to labels (case, punctuation and wording are the source's).

## Design

- Participants: pastel role cards with an icon above a two-line title (one fixed height for alignment). Roles are shared across the two figures: Agent Runtime teal (robot), Content detector and Context Service cyan, Policy amber, Approval Service and the User plum, Run Service and Tool Gateway blue, System of Record slate (database).
- Messages: solid arrow = call, dotted arrow = return (shape-independent of colour); label in a pill above the line so an arrowhead is never covered; arrow and pill take the sender's role colour, except the refusal, which is red.
- Self-messages: a 15 pt loop with the label beside it (left of the lifeline for Tool Gateway, which is near the right edge).
- Frames: soft amber panel with a title tab ("alt" or "opt") and the condition in brackets in bold; the nested alt has a deeper tint; the divider is dashed. Lifelines pass behind pills and the note but never strike through a frame condition (a same-coloured halo).
- All text at least 9 pt; each figure is placed at scale 1.00 (no shrinking).

## Problems found and fixed while iterating

1. A two-line "signed approval, bound to this proposal" pill touched the preceding message: row spacing recalculated.
2. Frame tab and condition crossed lifelines: frame x extents moved off the lifelines and the condition text given a halo (rectangles on the background layer, conditions on the main layer, called after the lifelines).
3. The halo initially nicked the frame border: shifted down 1.5 pt and trimmed.
4. Header title lengths differed (one or two lines): all titles forced to two lines so icons and text align.
5. Labels wider than a short span (for example "request + delegated grant" over a 62 pt column) were nudged with a pill `xshift` so nothing leaves the card extent.

## Remaining weaknesses

- Pills on messages over a short span cover the neighbouring lifelines locally (intended; they are opaque).
- Row y coordinates are written by hand in each figure (the kit keeps a cursor `\sqy` but frames need absolute y). A third sequence figure would want an auto frame placement (see below).

## Local macros proposed for promotion to `professional-diagrams.sty`

The whole `_sequence-kit.tex`: `\sqhead`, `\sqlife`, `\sqcall`, `\sqret`, `\sqself`, `\sqnote`, `\sqframe`, `\sqdivider`, `\sqdown`, `\sqcondfill`, and the styles `sq head`, `sq person`, `sq life`, `sq tab`, `sq cond`. About 90 lines, using only palette, pill and callout from the shared package. If promoted, the `\input` line in the two figures goes away. `tools/render_diagrams.py` needed no change: XeLaTeX runs with the repository root as the working directory, so `\input{assets/diagrams/src/_sequence-kit.tex}` resolves.

## Validation

- `make diagrams`: both figures render; every other figure is byte-identical (only the 4 render files of this group changed). Fonts embedded (Liberation Sans, FontAwesome 5).
- `make assemble build references latex latex-validate validate`: pass, 0 errors, 0 warnings.
- `make examples-run`: 30 passed.
- `make pdf`: XeLaTeX compile succeeded, 359 pages, no overfull box reported. Figure 4-2 (PDF page 234) and Figure 20-3 (page 71) were rendered and inspected: fonts, margins and caption alignment as expected.

## Integrator notes

- `config/diagrams.json` must point both ids at `assets/diagrams/src/<id>.tikz.tex` (edited locally, not committed); re-run `make diagrams` for the checksums.
- `assets/diagrams/src/_theme.mermaid.json` is now unused by any diagram (no `.mmd` remain); the Mermaid branch of the renderer and `mmdc`/`rsvg-convert` are no longer needed. Not removed here.
