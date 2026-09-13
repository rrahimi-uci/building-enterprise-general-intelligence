# Skill: End-to-End Editorial Reviewer

## Objective

Review the book as a single learning and decision system. Detect problems that section-by-section polishing misses.

## Review passes

1. **Reader promise:** title, preface, audience, scope, prerequisites, and conclusion align.
2. **Macro progression:** Parts move rationally from intent/platform foundations to runtime behavior, state/context, integration, collaboration, security/reliability, evidence/governance, operations, and evolution.
3. **Dependency graph:** concepts are defined before use; no chapter assumes a later concept without signposting.
4. **Transitions:** each chapter synthesis closes its argument and creates a reason for the next chapter.
5. **Duplication/contradiction:** collapse repeated definitions and reconcile conflicting advice.
6. **Terminology:** one canonical term per concept; expand abbreviations; distinguish agent, workflow, model, runtime, gateway, tool, protocol, and platform.
7. **Decision utility:** tables, diagrams, patterns, examples, and metrics help readers make an architecture or operating decision.
8. **Accessibility:** descriptive headings/captions, color-independent meaning, readable examples, inclusive language.
9. **Release integrity:** TOC, headings, references, appendices, version, and navigation agree.

## Method

- Read front matter, all Part orientations, chapter openings/syntheses, and appendices first to form a map.
- Then read end-to-end, recording issues by severity: blocker, major, moderate, editorial.
- Fix root causes rather than adding caveats everywhere.
- Re-read changed transitions and all occurrences of renamed terms.
- Produce `reports/editorial-audit.md` with scope, findings, resolutions, residual risks, and release recommendation.

## Exit criteria

No blockers; every major issue is resolved or explicitly accepted; the structure validator passes; stale terms/versions and repeated boilerplate are absent; a new reader can explain why each Part follows the previous one.
