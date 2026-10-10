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
`mlflow.openai.autolog(disable_openai_agent_tracer=False)` explicitly: MLflow
3.15.2 otherwise disables its Agents SDK trace processor by default. The run
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
| `C03` | 3 | Provider-neutral runtime boundary | SDK tool allowlists and framework state must not own enterprise truth |

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

| Example | Chapter | Exercises |
|---|---|---|
| `foundations/capability_levels.py` | 01 | The prototype and the four agent levels; a retry duplicates an unprotected write |
| `foundations/agent_tool_loop.py` | 02 | Typed tool, structured output, bounded run |
| `foundations/governed_tool_gateway.py` | 02 | Validation, authorization, freshness, and effect idempotency |
| `foundations/effect_idempotency.py` | 22 | Logical effect keys, replay safety, Unknown outcomes |
| `patterns/bounded_react_loop.py` | 10 | Run budget enforced outside the model |
| `patterns/routing_handoff.py` | 11 | Handoff as an ownership transfer |
| `patterns/approval_gate.py` | 14 | Proposal-bound human approval and expiry |
| `security/input_guardrail.py` | 20 | Tripwire before the model is consulted |
| `observability/mlflow_tracing.py` | 24 | Agent and tool spans |
| `observability/mlflow_trace_configuration.py` | 24 | Autolog plus platform-owned spans |
| `observability/mlflow_evaluation.py` | 25 | Dataset evaluation and regression detection |
| `observability/mortgage_agents_mlflow.py` | 24 | Real Agents SDK tool run traced by MLflow |
| `observability/mlflow_trajectory_evaluation.py` | 25 | Deterministic and model-assisted trajectory scorers |
| `contracts.py` | 03, 04 | Shared step and platform contracts, `RiskClass` (two views) |
| `platform/skills_registry.py` | 08 | Policy-aware resolution, SemVer precedence, lifecycle outside the digest |
| `patterns/react_engine.py` | 10 | Turn, tool and no-progress budgets as typed stop reasons |
| `patterns/plan_compilation.py` | 12 | Binding a plan to its policy envelope |
| `patterns/approval_verification.py` | 14 | Binding a human approval, self-approval, expiry |
| `runtime/durable_state.py` | 15 | Run state as a replayable event fold |
| `runtime/step_execution.py` | 03 | Platform-owned adapter around the SDK |
| `mortgage/cumulative_case.py` | 01–03 | Cumulative synthetic mortgage checkpoints (`C01`–`C03`) |

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
