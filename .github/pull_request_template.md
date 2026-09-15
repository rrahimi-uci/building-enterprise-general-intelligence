<!--
Complete every applicable section. A reviewer should understand what changed and
why without reconstructing the reasoning from the diff. Delete a section only
when it genuinely does not apply, and say why it does not.
-->

## Goal and motivation

<!-- What problem does this solve, and why now? -->

## What changed

<!-- The substance of the change, grouped by area. Not a file list. -->

## Why this approach

<!-- Alternatives considered and why this one won. -->

## Architectural and implementation decisions

<!-- Decisions a future maintainer would otherwise have to rediscover:
     canonical-source contract, cross-format contract, design system, build
     determinism, packaging. Write "None" if the change makes no such decision. -->

## Manuscript impact

- **Affected Parts/chapters/appendices:**
- **Citation impact** (`config/references.json`, new or changed `[Rxx]`):
- **Diagram impact** (`config/diagrams.json`, `assets/diagrams/`):
- **Structural invariants** (8 Parts / 28 chapters / 12 appendices — preserved?):
- **Backward compatibility** (does any existing contract change?):

## Testing performed

<!-- Commands actually run and their real results. Report failures honestly;
     a known failure with a stated reason is acceptable, a silent one is not. -->

| Check | Command | Result |
|---|---|---|
| Assemble | `make assemble` | |
| DOCX build | `make build` | |
| References | `make references` | |
| LaTeX source validation | `make latex-validate` | |
| Structural validation | `make validate` | |
| XeLaTeX PDF | `make pdf` | |
| Determinism | `make deterministic` | |
| Pagination QA | `make qa-pdf` | |

## Risks, limitations, and side effects

<!-- What could this break? What is explicitly out of scope or left undone? -->

## Documentation, configuration, migration, and deployment implications

<!-- README / AGENTS.md / CONTRIBUTING.md / styles/ updates, dependency or CI
     changes, anything a maintainer must do after merging. -->

## Related issues, epics, or milestones

<!-- Closes #123, relates to ... -->

## Release checklist

<!-- Required only for release PRs; see RELEASE-CHECKLIST.md. -->

- [ ] `CHANGELOG.md` updated
- [ ] `RELEASE-MANIFEST.json` and `CHECKSUMS.sha256` regenerated (`make package`)
- [ ] Clean-package test passed from the extracted ZIP
