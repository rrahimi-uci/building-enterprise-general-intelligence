# Contributing

## Principles

- Improve the reader's end-to-end mental model, not only the local paragraph.
- Preserve clear distinctions between deterministic workflow, bounded agent autonomy, runtime adaptation, and governed offline improvement.
- Prefer primary sources and narrow claim scopes.
- Keep examples vendor-neutral unless a named implementation is the subject.
- Treat accessibility, security, governance, reliability, and operability as architecture—not append-on topics.

## Setup

```bash
make setup   # .venv + Python dependencies + any missing TeX packages
make help    # every target, grouped by purpose
```

Re-running `make setup` is safe. TeX packages install into your user tree, so it
never needs `sudo`.

## Workflow

Every change goes through a pull request against `main`. Never commit directly
to `main`.

1. Branch from `main`.
2. Edit `source/parts/*.md` and the configuration registries **only**. Never
   hand-edit `book/manuscript.md`, `dist/*`, or `latex/content/book-content.tex`.
3. Follow templates in `templates/` and rules in `styles/`.
4. Run `make assemble`, inspect the Markdown diff, then `make build latex` to
   regenerate DOCX and LaTeX from the same source.
5. Run `make validate`. Use `make draft` for a fast visual check while writing
   and `make pdf` before asking for review.
6. Add or update tests when changing a tool.
7. For structural or visual changes, run `make qa-pdf` and inspect the contact
   sheet.
8. Commit the regenerated artifacts along with the source change — CI fails a PR
   whose generated files are stale.
9. Update `CHANGELOG.md` under an Unreleased heading or the target version.
10. Fill in the pull request template. Record the reason, affected chapters,
    citation impact, diagram impact, backward compatibility, and the real result
    of every check you ran.

## What is generated and what is authored

| Authored by hand | Generated — never hand-edit |
|---|---|
| `source/parts/*.md` | `book/manuscript.md` |
| `config/*.json` | `dist/*.md`, `dist/*.docx`, `dist/*.tex` |
| `assets/**` | `latex/content/book-content.tex` |
| `latex/bookstyle.sty`, `styles/**` | `assets/cover/cover-v*.png`, `qa/**`, manifests, checksums |

Presentation changes belong in `latex/bookstyle.sty` (PDF), `config/book.json`
(DOCX), and `styles/` (the contract both must honor) — never in generated
content.

The compiled PDF (`dist/*-LaTeX.pdf`) is gitignored. It is rebuilt on demand and
published by CI, so a rebuild never churns a 7 MB binary through history.

## Versioning

- Patch: corrections that do not alter architecture contracts or chapter topology.
- Minor: additive chapters/components or material guidance additions that preserve existing contracts.
- Major: incompatible taxonomy, canonical-source, build, design-system, or architecture-contract changes.

## Prohibited shortcuts

Do not manually format the final DOCX, edit `book/manuscript.md` as the source, paste unverified citations, invent benchmark results, suppress failed QA, or publish Notion before the package rebuild is clean.
