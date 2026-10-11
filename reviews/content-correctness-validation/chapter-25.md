# Chapter 25 — Improve the System Without Handing It Control

Source: `source/parts/07-part-vii.md`. Review baseline: `origin/main` at `6ebbc8b`; review date 2026-10-10. Status: issue-ledger review, **not a certification that every claim has independent source support**.

## Overall Correctness Assessment

The chapter's main scope is evaluation slices, repeated-run reliability and release gates. The chapter text, surrounding Part, registered visual/example markers, and relevant cross-chapter contracts were examined. 1 actionable finding(s) are recorded below. Code-suite execution is book-level evidence, not proof of this chapter's full runtime behavior.

## Confirmed Technical/Factual Errors

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Claims Requiring Validation

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Missing or Weak References

Citation presence was checked, but not every cited page was independently re-read against every attached clause. Any unsupported broad claim identified is listed under Claims Requiring Validation.

## Incorrect or Misused References

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Images and Diagram Validation

Registered visual(s): evaluation-gate; runtime-offline; learning-loop. Marker/caption ownership was checked against the chapter and registry; generated-image existence and baseline structural QA are documented in the overall report. No specific arrow/label error was confirmed here. Full print-scale inspection of every visual and all cover-image prose remains a separate verification gate.

## Table and Chart Validation

Tables were read for categorical consistency, units and stated assumptions; no numerical discrepancy was confirmed here unless listed below. Illustrative values are not empirical measurements. No independent cell-by-cell external attestation is claimed.

## Code Example Validation

Registered example(s): mlflow-evaluation; mlflow-trajectory-evaluation [audited: corrected — the original text named no ids; these are the two registry entries and markers for Chapter 25]. The pinned example/mortgage tests passed as a suite (264 passed); this does not establish semantic completeness. No chapter-specific code defect was confirmed in this pass.

## Equations and Quantitative Validation

Any displayed arithmetic/formulas were checked against their stated assumptions where tractable. No chapter-specific mathematical defect was confirmed unless listed below.

- **Location:** Repeated-run reliability, source/parts/07-part-vii.md:391
  **Status:** Potential Issue; **Category:** Mathematics; **Severity:** Medium; **Confidence:** High.
  **Current content:** Use `pass^k or equivalent` for repeated-run reliability.
  **Finding:** `pass^k` is a valid shorthand only for identically distributed independent attempts. The chapter does not state that assumption; repeated runs often share model, prompt, source and failure mode. The phrase `or equivalent` softens the claim, so this is an ambiguity rather than a demonstrated bad calculation.
  **Evidence:** Probability of k successes is `P(A1∩…∩Ak)`, equal to `p^k` only under the stated assumptions.
  **Recommended correction:** Measure empirical all-k pass on paired repeated trajectories; allow `p^k` only as an explicitly labeled IID approximation.

## Terminology and Consistency Issues

Compared key terms with adjacent chapters and Appendix H; no separate terminology issue confirmed unless recorded below.

The chapter's canonical H1 matches its cover title but differs from `config/book.json`; see [B-01 metadata-title drift](metadata-title-drift.md). This is one systemic metadata finding, not an additional per-chapter error count.

## Outdated Information

Living vendor/API claims require recheck against the pinned edition before publication; no blanket claim of currentness is made. Version-dependent behavior should remain explicitly scoped.

## Grammar, Spelling, and Typographical Issues

No high-confidence typo requiring a prose edit was confirmed in this chapter. This report does not substitute for a rendered page proofread.

## Cross-Chapter Contradictions

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Recommended Corrections

1. Measure empirical all-k pass on paired repeated trajectories; allow `p^k` only as an explicitly labeled IID approximation.
