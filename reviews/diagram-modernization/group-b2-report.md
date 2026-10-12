# Group b2 report: five vertical pipelines / state machines converted to TikZ

Branch `diagrams/b2`. Figures: `mortgage-case-lifecycle`, `policy-to-guardrail`, `release-recovery`, `sandbox-egress`, `skill-resolution`. Before/after pairs (as the book places them) are in `group-b2/`.

## Per figure

| Figure | Q1 identical technical information | Q2 clearly more polished | Nodes / edges before -> after | Natural size, placement scale |
|---|---|---|---|---|
| `mortgage-case-lifecycle` (Fig 1-1) | YES | YES | 9 / 9 -> 9 / 9 | 7.01 x 6.05 in, 1.00 |
| `policy-to-guardrail` (Fig 5-2) | YES | YES | 8 / 7 -> 8 / 7 | 6.30 x 7.63 in, 1.09 |
| `release-recovery` (Fig 27-1) | YES | YES | 10 / 11 -> 10 / 11 | 6.41 x 7.99 in, 1.04 |
| `sandbox-egress` (Fig 23-1) | YES | YES | 11 / 12 -> 11 / 12 | 6.88 x 8.09 in, 1.03 |
| `skill-resolution` (Fig 8-1) | YES | YES | 9 / 9 (6 nodes, 3 text elements; 5 edges) -> same | 6.94 x 6.57 in, 1.00 |

Placement scale = how much the book scales the figure (min of 7.06 / width and 8.3 / height). All are 1.00 or more, so the 9 pt text prints at 9 pt or larger (before: several of these printed at about 8 to 9 pt).

### Element maps (full maps are the header comments of each `.tikz.tex`)

- `mortgage-case-lifecycle`: note -> cyan card; diamond -> amber diamond; the box (Loan-origination) -> slate square card; three dashed edges (request > verify "after arrival", review > los "authorized effect only", summary > stop "unsupported claim") and the dotted edge (intake > summary "metadata only") keep their line style; "no" / "yes" keep the amber / blue roles of the original. Layout: serpentine in two columns (the original is one tall column with a void on the right).
- `policy-to-guardrail`: reads the current source ("Enforced rule at the effect boundary"); the quoted policy sentence keeps its original line break; the two box nodes (Project, Enforced rule) are square cards, the others rounded as in the source; "no" is the red edge to Rejected beside the diamond, "yes" the teal edge down.
- `release-recovery`: two parallel binding branches (Canary, Prior) converge on Active runs; Active runs reaches Compatible worker by two routes (direct, and via Fence/reconcile > Regional recovery); "fail" stays a dashed red return to the source, the two unlabelled edges stay unlabelled.
- `sandbox-egress`: reads the current source ("Access Broker/STS"). Layout: left leg down to the sandbox, the connection crosses to the egress proxy, right leg read upward to the effect ledger, refusal node at the bottom with three red edges (denied, profile violation, blocked / approval missing) arriving from the left lane, the sandbox and the right lane. Two dashed edges (one-use destination grant, scoped secret) keep their style. The credential note is a cyan card with a key icon.
- `skill-resolution`: the two side headings (DISCOVERY . what exists, RESOLUTION . what this run may use) became the titles of two groups; the red "the model may describe the need — and nothing below" note stays beside Candidates as a red callout; the refusal edge is dashed red, the pinned-release edge solid blue, both unlabelled as in the source.

## Problems found and fixed during iteration

- `mortgage-case-lifecycle`: first draft (single column) left a large void bottom-right (445 x 563 pt, scaled up 1.06) -> serpentine in two columns, 505 x 436 pt, filled width. Diamond tip protruded beyond the card edge on the left -> narrowed.
- `policy-to-guardrail`: first draft 614 pt tall (placed at 0.97) -> row pitch tightened to 549 pt; policy quote wrapped with an orphan word -> explicit line break as in the source; all pills moved to the longest straight run.
- `release-recovery`: "compatible execution" route was drawn as a horizontal-first path (arrow entered the worker sideways) -> explicit down-left-down route with the pill on the horizontal run; "existing binding" arrow was slanted by 5 pt -> anchors aligned; fail-loop pill moved to the middle of the vertical run.
- `sandbox-egress`: the "profile violation" edge first came out diagonal (mixed `|-` anchors) -> explicit orthogonal route; the first reasoning attempts at putting the refusal node in the middle of the U or beside a single column either crossed edges or exceeded 8.3 in, so the layout is the U with a bottom refusal node (no crossings, 583 pt tall).
- `skill-resolution`: groups touched -> 12 pt more gap; the two diamond exits were slightly slanted -> explicit vertical drops from the diamond boundary.

## Remaining weaknesses

- `sandbox-egress`: the centre of the U (between the two legs, upper half) is empty; the diamonds are as wide as the labels require (190 pt), which leaves no room for the refusal node inside the U.
- `policy-to-guardrail`: the right side below the Rejected card is empty (the chain is linear; same as the original).
- Dashed arrowheads at 1.2 pt are thin on screen at 80 dpi but fine in the PDF (same as the pilot).
- Greyscale: red and blue edges are not distinguishable by colour alone; the pill words ("Denied", "Fail", "Profile violation", "Blocked / approval missing"), dashed style and the red refusal card carry the meaning.

## Local macros proposed for promotion

None needed. Everything uses the shared package as is (`dg card`, `dg decision`, `pill`, `callout`, `\dggroup`, `dashed flow`, `dotted flow`, `turn`, `icon`). Candidate small additions: a `dg note` card style (folded corner) for the two source "note" nodes (they are plain cyan/slate cards here), and a helper for the explicit orthogonal "lane" route used by the refusal edges in `sandbox-egress`.

Icons used: `file-alt`, `clipboard-check`, `calculator`, `users`, `server`, `shield-alt`, `robot`, `key`, `clipboard-list`, `search`. New to the style guide's list: `key`, `search` (both FontAwesome 5 Free solid, already installed).

## Validation (this branch, venv paths from the brief)

| Check | Result |
|---|---|
| `make diagrams` | pass; only the five figures' PDF/PNG changed, all others byte-identical; second run idempotent; placement scales 1.00 to 1.09 |
| `make assemble build references latex` | pass (44 markers = 44 registered) |
| `make latex-validate` | FAILS on `release-recovery.png: Insufficient image resolution ... 242 dpi`: a tool bug, not a figure defect. `validate_latex.py` tests `"cover" in value`, and `release-recovery` contains "cover", so the PNG is judged against the 8.5 in / 295 dpi cover contract. With a local, uncommitted one-line fix (`value.startswith("assets/cover/")`, reverted afterwards) `latex-validate` and `validate` pass with 0 errors, 0 warnings. The integrator must apply that fix (see `observations-b2.md` item 5) |
| `make validate` | pass with the local fix above |
| `make examples-run` | pass; 30 passed |
| `make pdf` (with the local fix) | 360 pages, 0 Overfull `\hbox`, no undefined references; fonts embedded (Liberation Sans, FontAwesome 5 Free); Figures 1-1 (p. 30), 5-2 (p. 85 of the PDF), 8-1 (p. 122), 23-1 (p. 265), 27-1 (p. 309) inspected page by page: size, margins and caption alignment correct, text readable |

## Integrator notes

- `config/diagrams.json` is the renderer's source of truth: `source` must be set to `assets/diagrams/src/<id>.tikz.tex` for the five ids (done locally, deliberately not committed, together with the regenerated sha256 values; `make diagrams` rewrites the checksums idempotently).
- The five `.gv` sources are removed with `git rm`.
