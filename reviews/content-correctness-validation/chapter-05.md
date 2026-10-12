# Chapter 05 — Give Knowledge an Owner

Source: `source/parts/02-part-ii.md`. Review baseline: `origin/main` at `6ebbc8b`; review date 2026-10-10. Status: issue-ledger review, **not a certification that every claim has independent source support**.

## Overall Correctness Assessment

The chapter's main scope is knowledge authority, rule sets, provenance, projections and promotion. The chapter text, surrounding Part, registered visual/example markers, and relevant cross-chapter contracts were examined. 1 actionable finding(s) are recorded below. Code-suite execution is book-level evidence, not proof of this chapter's full runtime behavior.

## Confirmed Technical/Factual Errors

- **Location:** Knowledge set operations, source/parts/02-part-ii.md:440
  **Status:** Confirmed Error; **Category:** Technical correctness; **Severity:** High; **Confidence:** High.
  **Current content:** The intersection is highest-confidence knowledge and safe to act on.
  **Finding:** Agreement between two sets does not establish source independence, current validity, authorization, or truth.
  **Evidence:** A shared stale source or overlapping but differently scoped rules can appear in both sets; Chapters 5–6 themselves require provenance, scope, freshness and ACLs.
  **Recommended correction:** Treat intersection as corroboration only; require current scoped authority, independent provenance where relevant, and policy check before action.

  **Disposition (2026-10-11):** confirmed — the intersection row now reads "Corroborated, not verified; the scope, freshness, and permission checks below still apply before action", and the `intersection` docstring in `examples/knowledge/set_operations.py:73` is aligned ("corroborated, not yet verified or authorized") (this corrective PR). Related, from A-K: the 44% sentence at :422 now says the figure is author-reported, from one run of the author's own pipeline.

## Claims Requiring Validation

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Missing or Weak References

Citation presence was checked, but not every cited page was independently re-read against every attached clause. Any unsupported broad claim identified is listed under Claims Requiring Validation.

## Incorrect or Misused References

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Images and Diagram Validation

Registered visual(s): knowledge-fabric; policy-to-guardrail. Marker/caption ownership was checked against the chapter and registry; generated-image existence and baseline structural QA are documented in the overall report. No specific arrow/label error was confirmed here. Full print-scale inspection of every visual and all cover-image prose remains a separate verification gate.

## Table and Chart Validation

Tables were read for categorical consistency, units and stated assumptions; no numerical discrepancy was confirmed here unless listed below. Illustrative values are not empirical measurements. No independent cell-by-cell external attestation is claimed.

## Code Example Validation

Registered example(s): knowledge-graph; policy-to-rule; rule-as-guardrail; capability-catalog; grounding-verifier; set-operations. The pinned example/mortgage tests passed as a suite (264 passed); this does not establish semantic completeness. No chapter-specific code defect was confirmed in this pass.

## Equations and Quantitative Validation

Any displayed arithmetic/formulas were checked against their stated assumptions where tractable. No chapter-specific mathematical defect was confirmed unless listed below.

## Terminology and Consistency Issues

Compared key terms with adjacent chapters and Appendix H; no separate terminology issue confirmed unless recorded below.

## Outdated Information

Living vendor/API claims require recheck against the pinned edition before publication; no blanket claim of currentness is made. Version-dependent behavior should remain explicitly scoped.

## Grammar, Spelling, and Typographical Issues

No high-confidence typo requiring a prose edit was confirmed in this chapter. This report does not substitute for a rendered page proofread.

## Cross-Chapter Contradictions

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Recommended Corrections

1. Treat intersection as corroboration only; require current scoped authority, independent provenance where relevant, and policy check before action. (applied)
