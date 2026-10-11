# B-01 — Chapter-title metadata drift

**Status:** Confirmed Error. **Category:** Internal consistency / publication metadata. **Severity:** Medium. **Confidence:** High.

**Location:** `config/book.json` → `structure.chapters[*].title`; compare each canonical H1 in `source/parts/*.md` and `config/chapter-covers.json`.

**Current content and finding:** 22 of 28 chapter titles in book metadata are older variants. All 28 titles in `config/chapter-covers.json` match the canonical manuscript H1s. The current builders appear to derive chapter headings from Markdown and cover titles from the cover spec, so this is metadata/source-of-truth drift, not a demonstrated error in the rendered chapter headings. The structural validator checks chapter counts, not title equality. A future consumer of the metadata could publish misleading navigation or catalog entries.

| Chapter | `config/book.json` title | Canonical manuscript and chapter-cover title |
| --- | --- | --- |
| 03 | Keep the Framework in Its Lane | Keep the Agent Framework in Its Lane |
| 04 | The Architecture Around the Model | Design the Architecture Around the Model |
| 07 | Build the Paved Road for Agent Teams | Build a Paved Road for Agent Teams |
| 09 | From Skills to a Domain Platform | Turn Skills into a Coherent Domain Platform |
| 10 | ReAct Without the Runaway Loop | Use ReAct Without Creating a Runaway Loop |
| 11 | Route the Work—and Transfer Ownership | Route the Work Without Losing Ownership |
| 12 | Plans Are Proposals Until the System Compiles Them | Turn Proposed Plans into Safe, Executable Work |
| 13 | Use Critique to Improve, Not to Self-Approve | Use Critique to Improve—Never to Self-Approve |
| 14 | Put People Where Judgment Matters | Put People Where Their Judgment Matters |
| 15 | Keep Work Alive Across Time and Failure | Keep Long-Running Work Alive Through Failure |
| 16 | Patterns for Real Enterprise Work | Choose Patterns That Fit Real Enterprise Work |
| 17 | The Shapes That Fail in Production | Architecture Patterns That Fail in Production |
| 19 | Crossing the Boundary: MCP, A2A, and Local Control | Crossing System Boundaries: MCP, A2A, and Local Control |
| 20 | Security Starts Beyond the Prompt | Security Starts Outside the Prompt |
| 21 | Carry Identity and Narrow Authority | Carry Identity, Narrow Authority |
| 22 | Make Effects Safe to Retry | Make External Effects Safe to Retry |
| 23 | Contain a Manipulated Model | Contain the Damage When a Model Is Manipulated |
| 24 | Follow One Run from Request to Receipt | Follow a Run from Request to Verified Outcome |
| 25 | Improve the System Without Losing Control | Improve the System Without Handing It Control |
| 26 | Make Governance an Operating System | Make Governance Part of How the Platform Runs |
| 27 | Release Without Breaking Work in Flight | Release New Behavior Without Breaking Work in Flight |
| 28 | Make Performance a Business Decision | Treat Performance as a Business Decision |

**Evidence:** Exact-title comparison of the 28 numbered H1s against the two JSON registries on `6ebbc8b` produced 22 mismatches for `config/book.json` and zero for `config/chapter-covers.json`. `tools/validate_book.py` checks the 28-chapter count but does not compare titles.

[audited: the table was re-derived by script on 2026-10-10 — 22 mismatches on exactly chapters 03, 04, 07, 09–17, 19–28; every row's two cells are byte-exact against `config/book.json` and the manuscript H1 (which equals the cover-spec title in all 28 cases). Builder title sources, verified by reading the tools: `tools/build_book.py` parses chapter headings from assembled Markdown (`^(#{1,4})\s+(.+)$`, line 139) and reads `config/book.json` only for the book title, author, version and design tokens (lines 86, 302) and `config/chapter-covers.json` only for cover image paths (lines 275–279); `tools/build_latex.py` does the same (headings from Markdown, `book.json` for the title page at line 461, covers at lines 20–25); `tools/render_chapter_covers.py` draws `ch["title"]` from `config/chapter-covers.json` (line 528) and reads `book.json` only for book metadata and `structure.parts` order (lines 721–726); `tools/validate_book.py` counts chapters by regex (line 98), checks DOCX core-property title against `book.json` `book.title` (lines 194–196) and cover count/size/hash (lines 174–188), and never reads chapter titles. No script under `tools/` reads `structure.chapters[*].title`, so "appear to derive … from Markdown" above can be read as established for the current toolchain.]

**Recommended correction:** In a subsequent manuscript/metadata PR, synchronize `config/book.json` to canonical H1 titles and add a validator that asserts title equality across manuscript, book metadata and cover spec. Do not alter titles in this review-only PR.

**Second-pass critique:** Do not claim a DOCX/LaTeX heading defect from this mismatch alone; current renderer code reads headings from assembled Markdown. The risk is stale metadata and future integrations, not proven current page text.
