# Chapter 24 — Follow a Run from Request to Verified Outcome

Source: `source/parts/07-part-vii.md`. Review baseline: `origin/main` at `6ebbc8b`; review date 2026-10-10. Status: issue-ledger review, **not a certification that every claim has independent source support**.

## Overall Correctness Assessment

The chapter's main scope is causal trace, workflow/effect/audit separation and worked latency example. The chapter text, surrounding Part, registered visual/example markers, and relevant cross-chapter contracts were examined. 2 actionable finding(s) are recorded below. Code-suite execution is book-level evidence, not proof of this chapter's full runtime behavior.

## Confirmed Technical/Factual Errors

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Claims Requiring Validation

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Missing or Weak References

Citation presence was checked, but not every cited page was independently re-read against every attached clause. Any unsupported broad claim identified is listed under Claims Requiring Validation.

## Incorrect or Misused References

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Images and Diagram Validation

Registered visual(s): causal-trace. Marker/caption ownership was checked against the chapter and registry; generated-image existence and baseline structural QA are documented in the overall report. No specific arrow/label error was confirmed here. Full print-scale inspection of every visual and all cover-image prose remains a separate verification gate.

## Table and Chart Validation

Tables were read for categorical consistency, units and stated assumptions; no numerical discrepancy was confirmed here unless listed below. Illustrative values are not empirical measurements. No independent cell-by-cell external attestation is claimed.

## Code Example Validation

Registered example(s): mlflow-tracing; mlflow-trace-configuration; mortgage-agents-mlflow [audited: corrected — the original text named no ids; these are the three registry entries and markers for Chapter 24]. The pinned example/mortgage tests passed as a suite (264 passed); this does not establish semantic completeness. No chapter-specific code defect was confirmed in this pass.

## Equations and Quantitative Validation

Any displayed arithmetic/formulas were checked against their stated assumptions where tractable. No chapter-specific mathematical defect was confirmed unless listed below.

## Terminology and Consistency Issues

Compared key terms with adjacent chapters and Appendix H; no separate terminology issue confirmed unless recorded below.

The chapter's canonical H1 matches its cover title but differs from `config/book.json`; see [B-01 metadata-title drift](metadata-title-drift.md). This is one systemic metadata finding, not an additional per-chapter error count.

## Outdated Information

Living vendor/API claims require recheck against the pinned edition before publication; no blanket claim of currentness is made. Version-dependent behavior should remain explicitly scoped.

## Grammar, Spelling, and Typographical Issues

No high-confidence typo requiring a prose edit was confirmed in this chapter. This report does not substitute for a rendered page proofread.

## Cross-Chapter Contradictions

- **Location:** Worked example, source/parts/07-part-vii.md:16-18,77-99
  **Status:** Confirmed Error; **Category:** Internal consistency; **Severity:** Medium; **Confidence:** High.
  **Current content:** Opening says the evidence review completes slowly; example reports 12 minutes while effect remains Unknown.
  **Finding:** 3+2+4+3=12 minutes is time to an unresolved state, not verified completion; Chapters 15 and 22 require reconciliation before success.
  **Evidence:** Worked table explicitly says the effect ledger is open; source/parts/04-part-iv.md:1002 says a run reaches Succeeded only through executable acceptance.
  **Recommended correction:** Call it time to intervention/unresolved effect, or add subsequent reconciliation and its elapsed time before saying completed.

- **Location:** Trace and replay semantics, source/parts/07-part-vii.md:164
  **Status:** Potential Issue; **Category:** Internal consistency; **Severity:** Medium; **Confidence:** High.
  **Current content:** A fork may reauthorize external effects, followed by 'None of the three may create a live effect.'
  **Finding:** The statement conflates diagnostic replay with a new authorized run; reauthorization is inconsistent with a blanket ban if it permits a new effect.
  **Evidence:** Chapter 4's `:fork` is a new run; Chapter 22 requires new authorization and effect identity for live mutations.
  **Recommended correction:** Say replay/diagnostic replay never create live effects; a fork can do so only as a separately authorized new run under Chapter 22.

## Recommended Corrections

1. Call it time to intervention/unresolved effect, or add subsequent reconciliation and its elapsed time before saying completed.
2. Say replay/diagnostic replay never create live effects; a fork can do so only as a separately authorized new run under Chapter 22.
