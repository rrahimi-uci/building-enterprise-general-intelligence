# Skill: Citation Verifier

## Objective

Ensure each citation is credible, accurate, current enough for its claim, and scoped so it cannot be stretched beyond the evidence.

## Source priority

1. Binding legal/standards text.
2. Official specification or regulator/government publication.
3. Peer-reviewed paper or canonical research artifact.
4. Official project/vendor documentation or release note.
5. Reputable secondary analysis only when a primary source is unavailable.

## Procedure

1. Inventory claims that require attribution: definitions, protocol behavior, standard requirements, legal statements, research findings, vendor features, versions/dates, and external benchmarks.
2. Open the primary source and verify title, author/organization, publication/version, URL, and exact supporting passage.
3. Record one narrow `scope` sentence in `config/references.json`; use `n.d.` for undated living pages and preserve `verified` access date.
4. Add `[Rxx]` next to the supported claim. Do not cite at a distance that makes scope ambiguous.
5. If evidence is partial, weaken the prose or split the claim. If unavailable, remove/qualify it—never infer support.
6. Record maturity, deprecation, maintenance, jurisdiction, and pinning caveats.
7. Run `tools/check_references.py`; assemble to regenerate Appendices K and M.
8. Produce/update `reports/citation-verification.json` and `reports/citation-audit.md`.

## Critical distinctions

- A framework page documents a feature; it does not prove the feature is reliable for all enterprises.
- A security checklist suggests controls; it does not prove a system is secure.
- A legal overview is not legal advice and may not replace binding text.
- A dependency pin is not a claim that the version is latest.
- Book formulas, thresholds, architectures, and examples are author guidance unless explicitly sourced.

## Exit criteria

Every marker resolves exactly once, every registered source is cited or intentionally retained, no unsupported compound claim remains, and verification methods/limitations are transparent.
