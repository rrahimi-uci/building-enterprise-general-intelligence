# Chapter 22 — Make External Effects Safe to Retry

Source: `source/parts/06-part-vi.md`. Review baseline: `origin/main` at `6ebbc8b`; review date 2026-10-10. Status: issue-ledger review, **not a certification that every claim has independent source support**.

## Overall Correctness Assessment

The chapter's main scope is effect lifecycle, unique intent keys, receipts and reconciliation. The chapter text, surrounding Part, registered visual/example markers, and relevant cross-chapter contracts were examined. 2 actionable finding(s) are recorded below. Code-suite execution is book-level evidence, not proof of this chapter's full runtime behavior.

## Confirmed Technical/Factual Errors

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Claims Requiring Validation

- **Location:** No-native-key reconciliation, source/parts/06-part-vi.md:728-732
  **Status:** Potential Issue; **Category:** Technical correctness; **Severity:** High; **Confidence:** High.
  **Current content:** No match after the provider's visibility window is classified Declined.
  **Finding:** Absence in a query is not proof of absence unless the provider contract guarantees bounded completion and indexed visibility for all in-flight writes.
  **Evidence:** A delayed/asynchronous write can commit after the query window; the chapter's own Unknown semantics require proof, not a negative best-effort lookup.
  **Recommended correction:** Condition Declined on an explicit authoritative finality/visibility contract; otherwise retain Unknown or InterventionRequired.

  **Disposition (2026-10-11):** confirmed-adjusted — Declined-by-absence now requires the visibility window the connector's manifest declares; an empty query before that bound, or from a provider that declares none, "proves nothing" and resolves to InterventionRequired. The ToolManifest Effects row (now listing the reconciliation query and visibility window) and Appendix B triage step 4 were aligned (this corrective PR). Adjustment: Declined stays reachable under a declared contract rather than being withdrawn in favour of a permanent Unknown.

## Missing or Weak References

Citation presence was checked, but not every cited page was independently re-read against every attached clause. Any unsupported broad claim identified is listed under Claims Requiring Validation.

## Incorrect or Misused References

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Images and Diagram Validation

Registered visual(s): effect-lifecycle. Marker/caption ownership was checked against the chapter and registry; generated-image existence and baseline structural QA are documented in the overall report. No specific arrow/label error was confirmed here. Full print-scale inspection of every visual and all cover-image prose remains a separate verification gate.

## Table and Chart Validation

Tables were read for categorical consistency, units and stated assumptions; no numerical discrepancy was confirmed here unless listed below. Illustrative values are not empirical measurements. No independent cell-by-cell external attestation is claimed.

## Code Example Validation

Registered example(s): effect-idempotency. The pinned example/mortgage tests passed as a suite (264 passed); this does not establish semantic completeness. Confirmed issue(s) below.

- **Location:** examples/foundations/effect_idempotency.py:58-69
  **Status:** Confirmed Error; **Category:** Code; **Severity:** High; **Confidence:** High.
  **Current content:** Reusing a logical effect key with a different intent is a conflict.
  **Finding:** After a record is Declined, the intent-hash comparison is skipped and the same key is reused with a new intent, silently overwriting the prior record.
  **Evidence:** Code condition `record.state != "declined"` gates the hash comparison. Local reproduction accepted a changed intent after `DownstreamDeclined`. This contradicts source/parts/06-part-vi.md:929.
  **Recommended correction:** Compare intent hash for every existing record before state-specific retry handling; use a new key for a new intent and retain the prior record; test declined and reconciled-absent cases.

  **Disposition (2026-10-11):** confirmed — `EffectLedger.commit` now compares the intent hash before any state handling; a Declined or reconciled-absent record re-applies only the same intent and raises `EffectConflict` for a different one without running the callable or overwriting the prior record. Tests for the declined and reconciled-absent cases were added and fail on the previous code (this corrective PR).

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

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Recommended Corrections

1. Compare intent hash for every existing record before state-specific retry handling; use a new key for a new intent and retain the prior record; test declined and reconciled-absent cases. (applied)
2. Condition Declined on an explicit authoritative finality/visibility contract; otherwise retain Unknown or InterventionRequired. (applied with adjustment: the contract is the manifest-declared visibility window; without one the state is InterventionRequired)
