# Runnable book examples

Every code listing in the book is the exact text of a file in this directory,
and CI executes it. There is no second copy to drift.

## How a listing reaches the page

```text
examples/foundations/agent_tool_loop.py   ← you edit this
examples/foundations/governed_tool_gateway.py
        │  region between the --8<-- markers
        ▼
config/examples.json                      ← registered here, with its tests
        │
        ▼
source/parts/01-part-i.md                ← cites the Chapter 2 listings
        │  tools/assemble_manuscript.py expands the marker
        ▼
book/manuscript.md → DOCX and XeLaTeX
```

Expansion happens once, at assembly, so the Markdown, DOCX, and LaTeX editions
all carry identical code without each renderer needing to know about examples.

## Named regions

One file can serve two chapters at two depths:

```python
# --8<-- region:step
...shown where [[EXAMPLE:contracts#step]] appears...
# --8<-- endregion:step
```

`[[EXAMPLE:contracts]]` renders the whole example region; `[[EXAMPLE:contracts#step]]`
renders just that sub-region. `tools/check_examples.py` fails the build if a cited
region does not exist or is never closed.

## Region markers

A file stays runnable end to end — imports, `__main__` guard, helpers — while
the book shows only the part that teaches something:

```python
# --8<-- example:start
...shown in the book...
# --8<-- example:end
```

Without markers the whole file is used. Prefer markers: a listing over ~68 lines
cannot fit on one page and will be split across a page break.

## Running them offline

Examples must run in CI with **no network and no API key**. Agent examples use
`_harness/scripted_model.py`, which implements the Agents SDK `Model` interface
and replays a fixed script. Everything else in the example — tool dispatch,
structured output parsing, guardrails, the run loop — is the genuine SDK.

```python
model = ScriptedModel([
    ToolCall("read_mortgage_case", {"case_id": "MORT-2026-000184"}),
    Say('{"case_id": "MORT-2026-000184", "needs_input": true, "summary": "..."}'),
])
result = await run("Does MORT-2026-000184 have all required evidence?", model=model)
```

`ScriptedModel` must subclass `agents.models.interface.Model`. The runner
resolves `RunConfig.model` with an `isinstance` check, so a structurally
compatible class that does not inherit from it is silently ignored and the run
falls through to the real OpenAI provider.

The Chapter 24 mortgage integration also uses the real Agents SDK runner, but
keeps the model scripted. It calls
`mlflow.openai.autolog(disable_openai_agent_tracer=False)`. In MLflow 3.15.2
autolog registers its Agents SDK trace processor either way; `False` also keeps
the SDK's own exporter, which sends nothing without an API key. The run
uses a SQLite tracking URI, records only safe synthetic metadata, and never
requires an API key.

## Cumulative mortgage case

The book’s new anchor implementation is a synthetic Harborlight mortgage intake.
It is intentionally additive: the focused examples below remain available for
their individual architectural lessons, while the cumulative case connects the
lessons across chapters.

| Checkpoint | Chapter | Capability added | Bottleneck made visible |
|---|---:|---|---|
| `C01` | 1 | Read-only evidence summary | Missing documents and the false confidence of a model answer |
| `C02` | 2 | Typed proposal, Decimal calculation, read-only command | Schema validity is not authorization or verified evidence |
| `C03` | 3 | Provider-neutral runtime interface | SDK tool allowlists and framework state must not own enterprise truth |

Run the current foundation from the repository root with the examples
environment:

```bash
.venv-examples/bin/python -m mortgage_case --chapter 1 --scenario missing_income_document --offline
.venv-examples/bin/python -m mortgage_case --chapter 2 --scenario stale_case_version --offline
.venv-examples/bin/python -m mortgage_case --chapter 3 --scenario tool_allowlist_escape --offline
```

Every fixture is marked `SYNTHETIC TRAINING DATA — NOT FOR CREDIT DECISIONS`.
The example prepares evidence and proposes next work; it never approves or
denies credit and never writes to a real loan-origination system.

## What is here

Every registered example, in chapter order. `config/examples.json` is the
authoritative list; `make examples` fails if a file, marker, or test is missing.

| Example | Chapter | Exercises |
|---|---|---|
| `foundations/capability_levels.py` | 01 | Prototype sketch, deliberately without gateway or effect controls |
| `mortgage/cumulative_case.py` | 01–03 | Cumulative synthetic mortgage case across Chapters 1-3 |
| `foundations/agent_tool_loop.py` | 02 | Bounded agent loop with a typed tool |
| `foundations/governed_tool_gateway.py` | 02 | A readable Tool Gateway with validation, authorization, and effect idempotency |
| `contracts.py` | 03–18 | Provider-neutral agent-step and platform contracts |
| `runtime/step_execution.py` | 03 | One bounded agent step behind a platform-owned adapter |
| `knowledge/document_ingestion.py` | 05 | A document's fields verified against its bytes before they become facts |
| `knowledge/enforced_rule.py` | 05 | A policy rule enforced at the effect boundary |
| `knowledge/gate_record.py` | 05, 27 | Gate findings routed by kind, and a quality budget that cannot pass by rounding |
| `knowledge/grounding_verifier.py` | 05 | Admitting a claim only on a literal span of the bytes it cites |
| `knowledge/knowledge_graph.py` | 05 | Traversal answering a question similarity cannot |
| `knowledge/policy_to_rule.py` | 05 | A policy sentence as a typed, scoped rule with provenance |
| `knowledge/set_operations.py` | 05 | Union, intersection, difference and contradiction over rule sets |
| `runtime/context_manifest.py` | 06 | One sealed ContextManifest per agent step |
| `runtime/adapter_conformance.py` | 07 | An adapter conformance suite that reports every gap |
| `knowledge/capability_catalog.py` | 08 | Discovering a capability with its effects and prerequisites |
| `platform/skills_registry.py` | 08, 09 | A Skill registry: policy-bound resolution and pinned Skill Packs |
| `patterns/bounded_react_loop.py` | 10 | Bounded ReAct loop with an explicit run budget |
| `patterns/react_engine.py` | 10 | A ReAct controller that owns the budgets |
| `patterns/route_validation.py` | 11 | Eligibility-first routing with validation and fallback |
| `patterns/routing_handoff.py` | 11 | Framework handoff: passing control to a specialist within one run |
| `patterns/plan_compilation.py` | 12 | Compiling a validated plan into a budget-bounded envelope |
| `patterns/evaluator_optimizer.py` | 13 | A bounded evaluator-optimizer whose judge cannot accept |
| `patterns/approval_gate.py` | 14 | A human approval gate that survives the wait |
| `patterns/approval_verification.py` | 14 | Verifying a human approval against this exact proposal |
| `runtime/durable_state.py` | 15 | Durable run state as a replayable event fold |
| `antipatterns/bound_approval.py` | 17 | AP-06 and its correction: the approval covers this exact proposal |
| `antipatterns/delegation_budget.py` | 17 | AP-11 and its correction: delegation draws on one budget |
| `antipatterns/memory_gate.py` | 17 | AP-13 and its correction: a memory write passes a gate |
| `antipatterns/retry_owner.py` | 17 | AP-04 and its correction: one retry owner, one shared budget |
| `antipatterns/state_projection.py` | 17 | AP-02 and its correction: typed state projected into context |
| `antipatterns/unknown_effect.py` | 17 | AP-05 and its correction: a timeout leaves the effect Unknown |
| `federation/artifact_adoption.py` | 19 | Adopting a remote artifact under local policy |
| `security/input_guardrail.py` | 20 | An input guardrail that trips before any tool runs |
| `security/capability_envelope.py` | 21 | Capability-envelope subset proof |
| `foundations/effect_idempotency.py` | 22 | Effect-level idempotency ledger |
| `security/egress_url.py` | 23 | Default-deny URL authorization for an egress grant |
| `security/kill_switch.py` | 23 | Scoped operational kill switch |
| `observability/mlflow_trace_configuration.py` | 24 | Configuring MLflow tracing around a governed agent step |
| `observability/mlflow_tracing.py` | 24 | Manually tracing agent and tool boundaries with MLflow |
| `observability/mortgage_agents_mlflow.py` | 24 | Tracing the mortgage Agents SDK runtime with MLflow |
| `observability/mlflow_evaluation.py` | 25 | Evaluating an agent against a dataset with MLflow |
| `observability/mlflow_trajectory_evaluation.py` | 25 | Combining deterministic and model-assisted MLflow trajectory scorers |
| `knowledge/knowledge_release.py` | 27 | A knowledge change published only after gates, an independent approval, and a verified bundle |
| `platform/release_attestation.py` | 27 | Release attestation bound to verified identities |
| `platform/release_compatibility.py` | 27 | Release compatibility check against a worker profile |
| `platform/admission_permit.py` | 28 | Capacity admission that grants, defers, or rejects |

## Adding an example

1. Write the file under a topic directory, with region markers.
2. Write a test under `tests/` that asserts **behaviour**, not just that it runs.
3. Register it in `config/examples.json` with its `tests` and pinned `libraries`.
4. Cite it from `source/parts/*.md` as `[[EXAMPLE:your-id]]`.
5. `make examples` to validate, `make examples-run` to execute.

## Verification modes

| Mode | Meaning |
|---|---|
| `test` | Executed by pytest in CI with assertions on behaviour. |
| `import` | Imported against the pinned SDK, proving every symbol exists, but not executed. Use only when execution genuinely needs a live provider. |

## Environment

```bash
make setup-examples     # .venv-examples with the pinned SDKs
make examples-run
```

The SDKs are pinned in `examples/requirements.txt` and deliberately kept **out** of the
book's own `requirements.txt` — the manuscript must build without them. Bumping
a pin is an editorial act: the prose describing that API has to be re-checked
against the new version. The current offline profile pins `openai==3.13.0`,
`openai-agents==0.22.2`, and `mlflow==3.15.2`.

MLflow 3.15 put the filesystem tracking store into maintenance mode for traces,
so the tests use a SQLite backend, and trace export is forced synchronous so
assertions do not race the background writer.
