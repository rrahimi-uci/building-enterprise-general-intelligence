# Appendices A–L — correctness and consistency validation

Source: `source/parts/09-appendices.md`, at `origin/main` `6ebbc8b`; review date 2026-10-10. Appendices are assessed as substantive content, not automatically trusted supporting matter. This is an issue ledger, not a certification of every external claim.

## Appendix-by-appendix assessment

| Appendix | Purpose and validation result |
| --- | --- |
| A — Pattern guide | Cross-references the twelve platform patterns to chapters and failure modes. No missing target confirmed in the reviewed links; examples of effects still depend on Chapter 22's pending correction. |
| B — Triage and runbooks | Unknown-effect triage correctly prohibits blind retry, but its proof-of-absence path inherits the Chapter 22 visibility-contract caveat. |
| C — Core contracts | Contract groups were compared with Chapters 4, 18, 19 and 22; no independent contract mismatch confirmed. |
| D — Agent framework comparison | Helpful layered comparison, explicitly not a production certification. Three rows acknowledge absent registered source support; see finding A-D below. Living product status needs recheck before release. |
| E — Research implications | Benchmark use is conceptual. Benchmark denominators and task counts should be rechecked against the cited original papers before treating them as fixed current facts. |
| F — Known limits | Limitations align with the book's bounded-reasoner model; no separate confirmed contradiction. |
| G — Adoption roadmap | Stage gates are book-authored recommendations, not empirical proof of any particular timeline. |
| H — Glossary | Two definitions materially overstate or misstate cross-chapter contracts; see A-H1 and A-H2. |
| I — Harborlight companion | Scope explicitly separates implemented C01–C03 from roadmap C04 onward; do not represent later chapters as runnable implementations. |
| J — Coding-agent prompt | Acceptance checklist is a specification, not evidence the full platform exists or has passed those gates. |
| K — References and evidence scope | 54 entries are structurally registered and cited per the baseline QA. Citation existence and registry status do not establish support for every attached sentence. R43 is overextended in Chapter 28, and R48's one-run result needs a pinned raw evidence package for independent reproduction. |
| L — Capacity/resilience | Little's Law statement and 120/min × 4 min = 480 example in Chapter 28 are arithmetically coherent as mean estimates. The effective-work-rate formula needs variable definitions to avoid double counting; see A-L. |

## Findings

### A-D — Unregistered framework source support

- **Location:** Appendix D evidence context and Claude Agent SDK, CrewAI, Restate rows, `source/parts/09-appendices.md:265-286`.
- **Status:** Needs Verification. **Category:** Citation/reference; **Severity:** Medium; **Confidence:** High.
- **Current content:** The appendix itself states that these three entries have no registered source in this edition, yet records concrete capability and maturity-adjacent statements.
- **Finding:** The caveat is honest, but the comparison is not independently auditable from the book's registry.
- **Evidence:** Appendix D's own evidence context; no corresponding Rxx scope for those entries.
- **Recommended correction:** Before using the matrix as a selection source, register current official vendor/project documentation with narrow support scopes or mark each relevant cell provisional.

### A-H1 — Tool Gateway cannot itself promise exactly-once

- **Location:** Appendix H, Tool Gateway, `source/parts/09-appendices.md:454`.
- **Status:** Confirmed Error. **Category:** Internal consistency; **Severity:** High; **Confidence:** High.
- **Current content:** The Tool Gateway “decides whether an effect may happen, for this subject, exactly once.”
- **Finding:** The gateway can authorize, reserve and coordinate an idempotent logical effect, but cannot independently guarantee exactly-once execution across workers, networks and downstream systems. Chapter 22 expressly rejects exactly-once as a cross-system assumption.
- **Evidence:** Chapter 22 Q&A at `source/parts/06-part-vi.md:973` and its Unknown/reconciliation protocol; `examples/foundations/effect_idempotency.py` only models logical effect deduplication.
- **Recommended correction:** Define the gateway as enforcing authorization and one logical business effect through a durable ledger, downstream idempotency or reconciliation; do not say the gateway makes an effect happen exactly once.

### A-H2 — Caller-supplied key conflicts with shell-derived key

- **Location:** Appendix H, Idempotency key, `source/parts/09-appendices.md:434`.
- **Status:** Potential Issue. **Category:** Terminology; **Severity:** Medium; **Confidence:** High.
- **Current content:** “A caller-supplied identifier” is the entire definition.
- **Finding:** Chapter 22 says the platform derives a stable logical key from tenant/run/node/intent and checks its intent hash. A downstream key may be passed by a trusted gateway, but arbitrary model/user input must not select another effect's identity.
- **Evidence:** Chapter 22's `effects:begin` and intent-hash contract, `source/parts/06-part-vi.md:835-864`.
- **Recommended correction:** Define a stable logical-effect identifier derived by the trusted platform or supplied by an authorized caller and bound to the intent; distinguish it from the downstream provider key.

### A-L — Ambiguous effective-work-rate product

- **Location:** Appendix L quantitative sizing table, `source/parts/09-appendices.md:819-826`.
- **Status:** Potential Issue. **Category:** Mathematics; **Severity:** Medium; **Confidence:** Medium.
- **Current content:** `lambda_eff = lambda_external × E[nodes] × E[fan-out] × retry_multiplier`.
- **Finding:** The variables are undefined. If `E[nodes]` already means all executed DAG nodes per run, multiplying by fan-out again double-counts branches; multiplying independent averages can also misestimate a correlated workload.
- **Evidence:** Dimensional/counting analysis. Little's Law [R43](https://doi.org/10.1287/opre.9.3.383) supplies `L = λW`, not the work-rate expansion.
- **Recommended correction:** Define `E[attempted activities per external run]` directly from traces, inclusive of fan-out and retries, and use `λ_eff = λ_external × E[attempted activities per run]` for each resource class; if factorizing, specify mutually exclusive factors and assumptions.

### A-K — R48 one-run metric is not independently replayable from the book

- **Location:** Appendix K R48, `source/parts/09-appendices.md:751`; Chapter 5, `source/parts/02-part-ii.md:422`.
- **Status:** Needs Verification. **Category:** Citation/reference; **Severity:** Medium; **Confidence:** Medium.
- **Current content:** One documented pipeline run reportedly rejected 44% of dependency/conflict claims after a deterministic guard.
- **Finding:** The linked author's repository does contain the 44% statement, so the reference is not invented and the manuscript appropriately avoids generalizing it. The book does not pin a raw run ID, counts, corpus revision, verifier version or denominator, limiting independent reproduction.
- **Evidence:** [Policy Logic Forge ARCHITECTURE.md](https://github.com/rrahimi-uci/policy-logic-forge/blob/main/ARCHITECTURE.md) §1.1; compare the book's narrow R48 scope.
- **Recommended correction:** Preserve the narrow one-run wording; attach a version-pinned run artifact and numerator/denominator if the figure is to serve as independently reproducible empirical evidence. Otherwise label it author-reported.

## Cross-appendix and second-pass notes

- Appendix B's “proven absent” state must be interpreted through a downstream finality contract; merely querying after an assumed delay is not enough.
- Appendix D correctly disclaims comparative production certification; this review does not convert declared vendor capabilities into validated operational guarantees.
- Appendix K's structural checks cover 54 registered references and 139 baseline citation occurrences; they do not prove claim-level support. R43 and R48 are the principal scope/reproducibility follow-ups found here.
- The H1 finding was rechecked against Chapter 22 before publication of this report. The H2 issue was downgraded from an error to a terminology ambiguity because callers may legitimately provide a key when the trusted gateway binds it.

## Recommended sequence

1. Correct the Appendix H Tool Gateway definition together with Chapter 22's effect-key example.
2. Define Appendix L's work-rate variables and use measured attempt counts by resource class.
3. Register authoritative sources for Appendix D's unsourced rows and pin R48's underlying run if the 44% statistic remains.
4. Re-run citation, structural and visual validation after any manuscript correction; no manuscript or generated release artifact was edited by this review.
