# LaTeX Publication System — Book v1.0.0

This specification extends the book design system to XeLaTeX. It is normative for `latex/bookstyle.sty`, `tools/build_latex.py`, and the compiled PDF.

## 1. Authority and regeneration

Canonical prose remains `source/parts/*.md`. `book/manuscript.md`, `latex/content/book-content.tex`, the distributable `.tex`, DOCX, and Markdown are generated derivatives. Never reconcile a LaTeX-only prose edit; fix the canonical source and regenerate every format.

Presentation changes belong in `latex/bookstyle.sty` and this specification. Converter behavior belongs in `tools/build_latex.py`. Every change requires `tools/validate_latex.py`, a genuine XeLaTeX compile where an engine is available, PDF visual review, and a clean-package rebuild.

## 2. Engine and fonts

- Engine: XeLaTeX through `latexmk` when available.
- Body/display family: bundled Liberation Sans Regular/Bold/Italic/Bold Italic.
- Code family: bundled Liberation Mono Regular/Bold/Italic/Bold Italic.
- Font files reside in `latex/fonts/` and are distributed under the SIL Open Font License 1.1.
- No host font is required; substitution is a release failure.
- Main body size is 10 pt with 1.06 line spacing. Code is 7.4 pt with 9.2 pt leading; table text is never smaller than 7.2 pt.

## 3. Page architecture

- US Letter, portrait.
- Margins: top 0.68 in, bottom 0.65 in, left/right 0.72 in.
- Full-bleed 2550 × 3300 cover image.
- A designed title page follows the cover.
- Native linked table of contents and PDF bookmarks supplement the authored hierarchical reader map.
- Each Part, chapter, and appendix begins after a forced page break.
- All 8 Parts plus the appendices reference divider use standalone navy pages.
- Running header names the book; footer shows release and current/total page numbers.

## 4. Accessible palette

The LaTeX palette deliberately darkens body-size links and semantic colors while preserving the navy/cyan identity.

| Token | Hex | Primary use | Minimum tested contrast |
|---|---|---|---:|
| Book Navy | `#102A4C` | dividers, major hierarchy | 14.41:1 on white |
| Book Navy 2 | `#173E68` | secondary hierarchy | high contrast on white |
| Book Blue | `#1450A3` | links, H2, callout frames | 7.76:1 on white |
| Book Cyan | `#20B8D8` | Part/chapter eyebrow on navy | 6.11:1 on navy |
| Book Teal | `#0D6E69` | H4, balanced guidance | 6.08:1 on white |
| Book Amber | `#8A5600` | caution title field | 6.16:1 with white |
| Book Red | `#A62C2C` | threat title field | 6.96:1 with white |
| Book Ink | `#12233F` | body text | 15.70:1 on white |
| Book Slate | `#4A6078` | captions, headers, footers | 6.49:1 on white |
| Book Light | `#EEF4FA` | neutral panels and rows | dark text only |

Every semantic color is paired with a text label, heading, border, or structure. Do not encode status by color alone. `tools/validate_latex.py` fails if a designated normal-text pair falls below 4.5:1.

## 5. Structural mapping

| Canonical construct | XeLaTeX representation |
|---|---|
| `[[COVER]]` | full-page `BookCover` image |
| Book title/front matter | designed title page plus front chapters |
| `# PART …` | standalone `BookPartPage` with orientation |
| `# NN — …` | forced-page `BookChapter` with number eyebrow |
| `# Appendix X — …` | forced-page `BookAppendix` |
| H2/H3/H4 | unnumbered styled section hierarchy |
| paragraph/list/checklist | native paragraph, itemize, enumerate, visible check symbol |
| blockquote | breakable left-rule quote panel |
| one-column semantic table | labeled, breakable callout/caution/threat panel |
| multi-column GFM table | `longtable` with repeated dark header and alternating rows |
| fenced code | page-breakable `listings` panel with line numbers and wrapping |
| diagram marker | figure with `keepaspectratio`, maximum page-aware height, caption, and label |
| `[Rxx]` | hyperlink to the matching Appendix I reference target |
| `# Index` | `\BookIndex`: two-column makeindex page index (`latex/bookindex.ist`), listed in the TOC after the last appendix |

## 6. Tables

- Every Markdown table must be represented, as either a long table or a semantic callout. `tools/validate_latex.py` derives the expected total from the manuscript rather than asserting a fixed number, so the check survives editing.
- Headers repeat across page breaks.
- Header row uses white bold text on Book Navy.
- Body uses Book Ink on white/Book Light; color does not encode meaning.
- Columns share the line width exactly: `c` equal columns plus their `2c-2` inner separations equal `\linewidth`. Up to five source columns are supported.
- Dense four/five-column tables use 7.2 pt type, and inline code in a cell takes the cell's size. If a future table requires smaller text, split, rotate, or redesign it rather than silently shrinking.
- URLs and inline code are wrap-safe; a slash in cell text is a line-break opportunity (`\slash`), so slash-joined lists cannot overrun a column; cells use ragged-right alignment to avoid rivers and overfull justification.
- Short tables (up to eight rows, no cell over 110 characters) are a single `tabular` kept whole. Longer tables are a `longtable` with no reservation in front of it; its first body rows end in `\\*`, so the head never opens a page alone.
- Keep-together guards use `\BookNeedspace` (`\Needspace`), never `\needspace`: the latter plants a deferred breakpoint that a later `longtable` can capture, printing a stray or doubled head. A heading keeps the opening of the table, listing, or sub-heading that follows it; a listing label (`🐍 · …`, `JSON · …`) keeps its listing.

## 7. Code

- Preserve source exactly inside `lstlisting`.
- Show language label, line numbers, whitespace, and wrapped continuation marker.
- Ink, syntax, comment, string, and line-number colors are dark on `#F7F9FC`.
- Do not use shell escape, minted, remote highlighters, or network-dependent fonts.
- A code block containing the reserved `end lstlisting` terminator must fail generation and be redesigned safely.

## 8. Images and figures

- Cover: 300 effective dpi at Letter size.
- Technical diagrams: 255 effective dpi at the 7.06-inch LaTeX line width; no recompression occurs in the source project.
- Images use width and height limits with `keepaspectratio`; they cannot be stretched. The height cap is `0.86\textheight`, which still leaves room for a two-line caption; a tall portrait diagram is height-limited, so the cap sets its printed label size.
- Captions are semantic, centered, dark slate, and represented in surrounding prose.
- Decorative imagery is restricted to the cover.

## 9. Callouts

- Architecture/design/implementation notes: Book Blue frame, pale-blue field, dark text.
- Evidence caveats and cautions: Book Amber frame/title, pale-amber field, dark text.
- Threats: Book Red frame/title, pale-red field, dark text.
- Panels are breakable and never rely only on fill color.

## 10. Release validation

A LaTeX release must prove:

1. 8 narrative Parts plus one appendices divider.
2. 28 chapters and 10 appendices.
3. Current diagram and citation totals are derived from the canonical manuscript and diagram/reference registries. Historical totals must not be hard-coded into the style contract; code-block and table totals are likewise derived by the validators.
4. Balanced braces/environments outside verbatim code.
5. Every image and bundled font exists and passes minimum resolution/file-integrity gates.
6. Designated color pairs meet 4.5:1.
7. Generated source contains no unresolved Markdown markers or sandbox paths.
8. Project and distributable entry points are byte-identical.
9. A genuine XeLaTeX build succeeds in a TeX-enabled environment and its PDF receives pagination/visual QA before being called publication-final.

The approved DOCX-derived 213-page PDF in `latex/reference/` is a cross-format visual baseline only. It must never be presented as a XeLaTeX-compiled artifact.
