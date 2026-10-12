# Chapter 13 — Use Critique to Improve—Never to Self-Approve

Source: `source/parts/04-part-iv.md`. Review baseline: `origin/main` at `6ebbc8b`; review date 2026-10-10. Status: issue-ledger review, **not a certification that every claim has independent source support**.

## Overall Correctness Assessment

The chapter's main scope is generator/evaluator split, deterministic checks, spend and acceptance. The chapter text, surrounding Part, registered visual/example markers, and relevant cross-chapter contracts were examined. 3 actionable finding(s) are recorded below. Code-suite execution is book-level evidence, not proof of this chapter's full runtime behavior.

## Confirmed Technical/Factual Errors

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Claims Requiring Validation

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Missing or Weak References

Citation presence was checked, but not every cited page was independently re-read against every attached clause. Any unsupported broad claim identified is listed under Claims Requiring Validation.

## Incorrect or Misused References

No separate confirmed finding in this category during this pass; absence of a finding does not certify exhaustive validation.

## Images and Diagram Validation

Registered visual(s): pattern-reflection. Marker/caption ownership was checked against the chapter and registry; generated-image existence and baseline structural QA are documented in the overall report. Specific issue below.

- **Location:** Figure 13-1 pattern-reflection
  **Status:** Potential Issue; **Category:** Figure/image; **Severity:** Low; **Confidence:** Medium.
  **Current content:** The diagram shows the acceptance engine and a revision path.
  **Finding:** The accepted path is explicit, but rejection/escalation from the acceptance engine to revision/human is not drawn; the judge-to-revise arrow could imply the judge directs revisions independently.
  **Evidence:** Visual inspection of rendered PNG against the loop and chapter caption.
  **Recommended correction:** Draw an explicit acceptance-engine reject/escalate branch or label the current arrows as advisory feedback.

  **Disposition (2026-10-11):** confirmed-adjusted (Low) — `assets/diagrams/src/pattern-reflection.gv` redrawn: the judge now feeds only the acceptance engine ("score + rationale · never self-accepts"), and the engine owns every exit — accepted, rejected → Revise, escalated (cap · no progress) → Human intervention; the PNG/PDF were re-rendered and the `config/diagrams.json` description and sha256 updated (this corrective PR). The new rendering has not yet been inspected at print scale.

## Table and Chart Validation

Tables were read for categorical consistency, units and stated assumptions; no numerical discrepancy was confirmed here unless listed below. Illustrative values are not empirical measurements. No independent cell-by-cell external attestation is claimed.

## Code Example Validation

Registered example(s): evaluator-optimizer. The pinned example/mortgage tests passed as a suite (264 passed); this does not establish semantic completeness. Confirmed issue(s) below.

- **Location:** examples/patterns/evaluator_optimizer.py:87-99
  **Status:** Confirmed Error; **Category:** Code; **Severity:** High; **Confidence:** High.
  **Current content:** The loop claims bounded spend and checks cost after candidate generation and after the acceptance return.
  **Finding:** A candidate costing beyond the cap can be accepted, and even a rejected candidate can push spending beyond the cap before escalation.
  **Evidence:** Code increments `spent` at line 89, accepts at 93–94, and only checks budget at 98–99. Existing test accepts two $0.60 candidates under a $1.00 cap after $1.20 spend.
  **Recommended correction:** Check an enforceable pre-call budget/reservation and validate actual cost before acceptance; document unavoidable post-call overage separately and test it.

  **Disposition (2026-10-11):** confirmed — a candidate whose generation cost broke the cap is now escalated (`budget_exhausted`), never accepted, and no further call starts once spend ≥ cap; two tests were added that fail on the previous code (this corrective PR). Documented limitation, not eliminated: a call's cost is known only afterwards and the `Generator` protocol carries no cost ceiling, so there is no per-call reservation and the last call can still overrun the cap by its own cost (stated on `RevisionLimits`). The existing two-$0.60 test therefore still spends $1.20 under a $1.00 cap, but now ends in escalation rather than acceptance.

- **Location:** examples/patterns/evaluator_optimizer.py:52-65
  **Status:** Confirmed Error; **Category:** Code; **Severity:** High; **Confidence:** High.
  **Current content:** Configured judge thresholds govern acceptance.
  **Finding:** An empty score tuple satisfies the loop vacuously and accepts a candidate although required `accuracy` score is missing.
  **Evidence:** `AcceptanceEngine({"accuracy": 0.8}).decide("answer", (), ())` returned `accepted` in the pinned test environment.
  **Recommended correction:** Reject/escalate when a required criterion is missing, unknown or non-finite; add a missing-score test.

  **Disposition (2026-10-11):** confirmed — `AcceptanceEngine.decide` now requires every configured criterion to be present with a finite score before it can accept, and consults judge evidence only once every executable check has passed; a test covers the missing, NaN and substitute-criterion cases (this corrective PR).

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

1. Check an enforceable pre-call budget/reservation and validate actual cost before acceptance; document unavoidable post-call overage separately and test it. (applied with adjustment: cost is validated before acceptance and before every further call, and the overage is documented and tested; no pre-call reservation was added because the generator has no cost ceiling, so the one-call overrun remains)
2. Reject/escalate when a required criterion is missing, unknown or non-finite; add a missing-score test. (applied)
3. Draw an explicit acceptance-engine reject/escalate branch or label the current arrows as advisory feedback. (applied: both branches drawn)
