# Contributing

## Principles

- Improve the reader's end-to-end mental model, not only the local paragraph.
- Preserve clear distinctions between deterministic workflow, bounded agent autonomy, runtime adaptation, and governed offline improvement.
- Prefer primary sources and narrow claim scopes.
- Keep examples vendor-neutral unless a named implementation is the subject.
- Treat accessibility, security, governance, reliability, and operability as architecture—not append-on topics.

## Workflow

1. Edit `source/parts/*.md` and configuration registries only.
2. Follow templates in `templates/` and rules in `styles/`.
3. Run `make assemble`, inspect the diff, and run `make build validate`.
4. Add or update tests when changing a tool.
5. For structural or visual changes, run `make qa-pdf` and inspect the contact sheet.
6. Update `CHANGELOG.md` under an Unreleased heading or the target version.
7. Include the reason, affected chapters, citation impact, diagram impact, and backward-compatibility considerations in the change review.

## Versioning

- Patch: corrections that do not alter architecture contracts or chapter topology.
- Minor: additive chapters/components or material guidance additions that preserve existing contracts.
- Major: incompatible taxonomy, canonical-source, build, design-system, or architecture-contract changes.

## Prohibited shortcuts

Do not manually format the final DOCX, edit `book/manuscript.md` as the source, paste unverified citations, invent benchmark results, suppress failed QA, or publish Notion before the package rebuild is clean.
