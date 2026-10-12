# Book Design System — v1.0.0

This document is the visual and editorial contract for every representation of the book. `config/book.json`, `config/style-tokens.json`, and `tools/build_book.py` are the executable counterparts.

## 1. Publication hierarchy

| Level | Markdown | DOCX style | Pagination rule | Purpose |
|---|---|---|---|---|
| Cover | `[[COVER]]` | full-page image | page 1 | identity, title, author, edition |
| Title/front matter | H1/H2 as authored | Title, Subtitle, headings | follows cover | scope, audience, reading map, TOC |
| Part | `# Part <Roman> — <Title>` | Book Part | standalone page | conceptual phase and orientation |
| Chapter cover | none (from `config/chapter-covers.json`) | full-page image, no heading | standalone page before each chapter | explains the chapter's central concept at a glance |
| Chapter | `# Chapter NN — <Title>` | Heading 1 | new page, after its cover | primary learning unit |
| Appendix | `# Appendix X — <Title>` | Heading 1 | new page | reference/operational material |
| Section | `##` | Heading 2 | keep with next | major chapter argument |
| Subsection | `###` | Heading 3 | keep with next | decomposed concept |
| Local topic | `####` | Heading 4 | keep with next | limited local hierarchy |

Do not skip heading levels. Do not start body content with a duplicate H1 title. Every Part page states what the reader will decide or build and how the Part connects to the previous and next layers.

The book and chapter cover artwork carries no printed release version. Version metadata remains in the title page, running footer, and release artifact names.

## 2. Narrative component model

A chapter should normally contain:

1. Opening promise and prerequisites.
2. Problem/system context.
3. Definitions, boundaries, and invariants.
4. Architecture and control/data-flow explanation.
5. Patterns, anti-patterns, threats, or decisions.
6. Enterprise example and implementation guidance.
7. Detection/operational metrics and trade-offs.
8. Evidence notes for sourced claims.
9. Concise synthesis and transition to the next chapter.

Pattern and anti-pattern material uses this sequence when applicable:

**Problem → Anti-Pattern → Why It Fails → Recommended Pattern → Architecture → Enterprise Example → Detection Metrics → Trade-offs**

Continuous learning uses:

**Observe → Measure → Detect → Diagnose → Recommend → Validate → Approve → Deploy → Monitor → Learn**

Always distinguish runtime adaptation from governed offline improvement, and automated changes from approval-required changes.

## 3. Typography

Primary font: Arial. Monospace font: Courier New. If unavailable, use a metric-compatible substitute and rerun pagination QA.

| Element | Size | Weight/color | Spacing |
|---|---:|---|---|
| Title | 30 pt | bold, Navy | 14 pt before / 7 pt after |
| Subtitle | 14 pt | Teal | 8 / 5 pt |
| Part title | 28 pt | bold, White | centered on Navy field |
| H1 | 24 pt | bold, Navy | 14 / 7 pt |
| H2 | 16 pt | bold, Blue | 9 / 5 pt |
| H3 | 12 pt | bold, Navy 2 | 7 / 4 pt |
| H4 | 10 pt | bold, Teal | 5 / 3 pt |
| Body | 10 pt | Ink | 6 pt after, 1.1667 line spacing |
| Caption | 8.5 pt | italic, slate | 2 / 6 pt |
| Inline code | 8.7 pt | Courier New, slate | inline |
| Code | 7.25 pt | Courier New | line-numbered panel |
| Header | 7.2 pt | bold, slate | book title |
| Footer | 7.5 pt | slate | version and page number |

Avoid manual direct formatting when a named style exists. Style changes belong in configuration and the builder, then require full visual regression review.

## 4. Color tokens

| Token | Hex | Use |
|---|---|---|
| Navy | `#102A4C` | major headings, dividers, authority |
| Navy 2 | `#173E68` | secondary hierarchy |
| Blue | `#1769D2` | H2, links, active architecture |
| Cyan | `#20B8D8` | accents, Part identifiers |
| Teal | `#118A84` | H4, balanced positive guidance |
| Amber | `#E09A32` | cautions and decisions |
| Red | `#C94A4A` | threats, failure, prohibited paths |
| Light | `#EEF4FA` | neutral panels/table shading |
| Ink | `#12233F` | body text |
| White | `#FFFFFF` | reversed text |

Never encode meaning by color alone. Pair color with titles, labels, icons, line styles, or explicit status text.

## 5. Page geometry and navigation

- Page size: US Letter, portrait.
- Margins: top 0.68 in, bottom 0.65 in, left 0.72 in, right 0.72 in.
- Header distance: 0.25 in; footer distance: 0.28 in.
- First page uses different header/footer.
- Part and appendix-divider pages are standalone.
- Each chapter/appendix begins on a fresh page near the top margin.
- Header names the book; footer shows `BOOK v<version> | PAGE <field>`.
- TOC uses the canonical H1 order. The Markdown TOC is source-authored; DOCX heading styles permit native navigation/update.
- Avoid orphan headings: headings keep with their following paragraph/table.

## 6. Markdown conventions

- UTF-8, LF line endings, one trailing newline.
- ATX headings only (`#` through `####`).
- One blank line between blocks.
- Fenced code blocks with an explicit language whenever known.
- GFM tables; escape literal `|` as `\|`.
- Bullets use `-`; ordered lists use `1.` unless a stable number is semantically required.
- Citation markers are stable `[Rxx]` identifiers.
- Diagram markers occupy their own line: `[[DIAGRAM:id|caption]]`.
- Cover marker: `[[COVER]]` once in front matter.
- External links use `[label](https://…)`; never use raw private/session URLs.
- Do not use layout-only HTML in canonical Markdown.

## 7. Tables

Tables must answer a decision, comparison, contract, or traceability question—not merely compress prose.

- Use a concise header row and consistent column count.
- Header cells: Navy background, white bold text.
- Body rows: alternating white/light fill when legibility benefits.
- Font size: 7.4–8.3 pt depending on column count; never below 7 pt without redesign.
- Avoid more than six dense columns on Letter portrait pages; split or rotate the information model instead.
- Keep units in headers and define acronyms nearby.
- For long evidence matrices, repeat headers in Word when supported and keep each cell atomic.
- Callout tables use one cell and a semantic label such as `Design decision`, `Evidence caveat`, or `North-star rule`.

## 8. Code

- Every code block declares language unless intentionally plain text.
- Examples must state whether they are complete, illustrative, pseudocode, or production-ready.
- Never include live credentials, private endpoints, or undeclared external dependencies.
- Keep lines short enough for 6.85-inch text width; prefer 88 characters.
- DOCX panels use a dark/light controlled palette, line numbers, Courier New, and lightweight deterministic token color.
- Validate extractable Python/JSON/YAML where feasible; explain intentionally partial fragments.

## 9. Diagrams and images

- Every visual must teach an architectural concept or, on the cover only, establish identity.
- Publication width: 6.85 in maximum.
- Prefer source dimensions that render crisply at 300 dpi.
- Put `[[DIAGRAM:id|caption]]` on its own line; the ID must exist in `config/diagrams.json`.
- Caption immediately follows the image in DOCX and is embedded in the marker for Markdown portability.
- Labels use the book font/color system, remain legible in grayscale, and avoid text smaller than 9 pt at final size. Check the printed size, not the source size: a figure wider than about 7.5 inches is scaled down to the column, and its labels with it.
- Show trust boundaries, data/control flows, and policy enforcement explicitly when relevant.
- Do not use decorative AI images inside technical chapters.
- Replacement assets require registry, checksum, PDF, and contact-sheet review.

## 10. Callouts and learning sections

Callouts are authored as a one-column Markdown table whose single cell opens
with the kind in bold. `tools/callouts.py` is the one definition both renderers
read, so a kind cannot mean one thing in DOCX and another in the PDF.

```markdown
|  |
| --- |
| **BEST PRACTICE**  Validate, authorize, and commit outside the model. |
```

### Narrative and evidence callouts

- **Mortgage case at this point:** where the Harborlight running case now stands.
- **North-star rule:** a durable design principle.
- **Design decision:** a choice with explicit consequences.
- **Evidence caveat / Source discipline:** what a source supports and does not.
- **Caution:** a failure mode, maturity issue, or operational hazard.
- **Implementation note:** concrete guidance that would interrupt the main flow.
- **Threat:** an attack the architecture must withstand.

### Guidance boxes

| Kind | Frame | Ground | Carries |
|---|---|---|---|
| Best practice | teal | pale teal | The thing to do, stated as an instruction |
| Architecture guidance | navy 2 | pale blue | A boundary or ownership decision |
| Developer guideline | blue | pale indigo | A rule that shapes code the reader writes |
| Production consideration | plum | pale plum | What changes once real traffic and real time arrive |
| Security and governance | red | pale red | An authorization, evidence, or policy obligation |
| Common pitfall / Anti-pattern | amber | pale amber | The mistake, named, and what to do instead |
| Performance and cost | olive | pale olive | Where the money and the latency actually go |
| Observability tip | deep cyan | pale cyan | What to record so a later investigation can succeed |

**The test for a guidance box:** it must contain an instruction the reader can
act on. If it restates the paragraph above it, delete it — being true is not
sufficient. Keep each to a few sentences, one theme, and never rely on colour
alone: the title states the kind, so the palette is a fast index, not the signal.

Callouts are not substitutes for argument. Follow them with implementation or
evidence where the reader will need it.

## 10a. Diagrams

Every diagram is generated from an editable source in `assets/diagrams/src/` and
rendered twice: a **vector PDF** that XeLaTeX embeds, and a **raster PNG** for the
DOCX edition, which cannot embed PDF. Never hand-edit a render.

Graphviz (`.gv`) is the default. Mermaid (`.mmd`) is used where a sequence
diagram genuinely reads better than a box-and-arrow graph. The shared house
style lives in `assets/diagrams/src/_theme.gv` and is spliced in at render time,
so restyling the whole book is one edit.

**Role is carried by colour and shape together**, so a component type is
identifiable without a legend and the figure still reads in greyscale print:

| Role | Shape | Colour |
|---|---|---|
| Agent runtime, reasoning | rounded box | teal |
| Platform service, API | box | blue |
| Store, ledger, record | cylinder | indigo |
| Knowledge, policy, evidence | note | cyan |
| Decision or policy check | diamond | amber |
| Outside the trust boundary | box | slate |
| Committed effect, outcome | rounded box | plum |
| Anti-pattern or refusal | rounded box | red |

Edges: solid for flow, dashed for control or policy, dotted for evidence.

**Sizing.** A figure is placed at the full column width, so a source should lay
out at roughly 6.5–7.5 inches wide and no more than about 8.5 inches tall. Wider
than that and the text is scaled below body size; taller and it will not share a
page with its caption. Long sequential flows read better vertically on a portrait
page than horizontally.

**Choose the form for the concept.** Layered models for planes and stacks,
sequence diagrams for protocols and ordering, decision trees for selection,
cycles for loops, side-by-side clusters for before-and-after. Forcing every idea
into one diagram style is how diagrams stop carrying information.

## 11. Pattern, anti-pattern, and threat cards

Use the templates in `templates/`.

- Pattern IDs should remain stable when language changes.
- Anti-patterns must state the mechanism of failure, not only a negative label.
- Detection metrics must be observable and specify numerator/denominator or event definition where possible.
- Trade-offs include complexity, cost, latency, control, portability, and organizational burden.
- Threat cards identify asset, trust boundary, adversary/precondition, attack path, control, residual risk, evidence, and incident signal.

## 12. References

- Registry: `config/references.json`.
- In-text form: `[Rxx]` at the claim it supports.
- Appendix K: generated bibliography.
- Appendix K: generated reference list, with the claim-scope traceability matrix as its closing section. It absorbs the former Appendix M so a reader checking a citation holds one appendix letter, not two.
- Prefer primary standards, official documentation, peer-reviewed research, and binding legal texts.
- Living documentation uses `n.d.` and an access date.
- Versions/pins are recorded separately from publication year.
- A source never automatically validates book-authored recommendations, benchmarks, or estimates.

## 13. Accessibility and inclusive design

- Use descriptive headings and captions.
- Avoid directional references that depend only on page position.
- Pair color with explicit labels.
- Use sufficient contrast and readable minimum type sizes.
- Explain all diagrams in surrounding prose.
- Expand uncommon abbreviations on first use.
- Use gender-neutral language when pronouns are not known.

## 14. Change control

A design-system change requires:

1. Updated design documentation and tokens.
2. Updated builder/template.
3. Rebuild of Markdown/DOCX.
4. Deterministic hash check.
5. PDF visual regression on representative pages.
6. Changelog entry and migration note.
7. Clean-package rebuild.

No undocumented manual adjustment is part of the release process.
