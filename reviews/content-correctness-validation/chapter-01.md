# Chapter 01 — What Turns an LLM Call into a Production System

Source: `source/parts/01-part-i.md`. Review baseline: `origin/main` at `6ebbc8b`; review date 2026-10-10. Status: issue-ledger review, **not a certification that every claim has independent source support**.

## Overall Correctness Assessment

The chapter's main scope is demo-to-production capability ladder; synthetic mortgage case; four levels; gateway and acceptance boundaries. The chapter text, surrounding Part, registered visual/example markers, and relevant cross-chapter contracts were examined. 1 actionable finding(s) are recorded below. Code-suite execution is book-level evidence, not proof of this chapter's full runtime behavior.

## Confirmed Technical/Factual Errors

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Claims Requiring Validation

- **Location:** Four levels / level one
  **Status:** Potential Issue; **Category:** Technical correctness; **Severity:** Low; **Confidence:** High.
  **Current content:** The model has no mechanism for not knowing.
  **Finding:** This is overbroad if read as inability to abstain; the real limitation is unreliable access to truth or calibrated uncertainty.
  **Evidence:** Technical distinction: an LLM can emit an abstention token or response while still lacking an independent correctness guarantee.
  **Recommended correction:** Qualify as no reliable built-in ground-truth check; distinguish abstention behavior from epistemic certainty.

## Missing or Weak References

Citation presence was checked, but not every cited page was independently re-read against every attached clause. Any unsupported broad claim identified is listed under Claims Requiring Validation.

## Incorrect or Misused References

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Images and Diagram Validation

Registered visual(s): mortgage-case-lifecycle; capability-ladder; system-overview; gateway-roles. Marker/caption ownership was checked against the chapter and registry; generated-image existence and baseline structural QA are documented in the overall report. No specific arrow/label error was confirmed here. Full print-scale inspection of every visual and all cover-image prose remains a separate verification gate.

## Table and Chart Validation

Tables were read for categorical consistency, units and stated assumptions; no numerical discrepancy was confirmed here unless listed below. Illustrative values are not empirical measurements. No independent cell-by-cell external attestation is claimed.

## Code Example Validation

Registered example(s): prototype-levels (regions `demo`, `level-one`, `level-two`, `level-three`); mortgage-cumulative-case (region `c01`) [audited: corrected — written as the registry ids and `[[EXAMPLE:id#region]]` markers actually used in the chapter]. The pinned example/mortgage tests passed as a suite (264 passed); this does not establish semantic completeness. No chapter-specific code defect was confirmed in this pass.

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

1. Qualify as no reliable built-in ground-truth check; distinguish abstention behavior from epistemic certainty.
