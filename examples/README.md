# Runnable book examples

Every code listing in the book is the exact text of a file in this directory,
and CI executes it. There is no second copy to drift.

## How a listing reaches the page

```text
examples/foundations/agent_tool_loop.py   ← you edit this
        │  region between the --8<-- markers
        ▼
config/examples.json                      ← registered here, with its tests
        │
        ▼
source/parts/04-part-iv.md                ← cited as [[EXAMPLE:agent-tool-loop]]
        │  tools/assemble_manuscript.py expands the marker
        ▼
book/manuscript.md → DOCX and XeLaTeX
```

Expansion happens once, at assembly, so the Markdown, DOCX, and LaTeX editions
all carry identical code without each renderer needing to know about examples.

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
    ToolCall("lookup_supplier", {"supplier_id": "S-1001"}),
    Say('{"supplier_id": "S-1001", "active": true, "summary": "..."}'),
])
result = await run("Is supplier S-1001 active?", model=model)
```

`ScriptedModel` must subclass `agents.models.interface.Model`. The runner
resolves `RunConfig.model` with an `isinstance` check, so a structurally
compatible class that does not inherit from it is silently ignored and the run
falls through to the real OpenAI provider.

## What is here

| Example | Chapter | Exercises |
|---|---|---|
| `foundations/agent_tool_loop.py` | 02 | Typed tool, structured output, bounded run |
| `foundations/effect_idempotency.py` | 21 | Logical effect keys, replay safety |
| `patterns/bounded_react_loop.py` | 08 | Run budget enforced outside the model |
| `patterns/routing_handoff.py` | 09 | Handoff as an ownership transfer |
| `patterns/approval_gate.py` | 12 | Proposal binding, grant expiry |
| `security/input_guardrail.py` | 18 | Tripwire before the model is consulted |
| `observability/mlflow_tracing.py` | 23 | Agent and tool spans |
| `observability/mlflow_trace_configuration.py` | 23 | Autolog plus platform-owned spans |
| `observability/mlflow_evaluation.py` | 24 | Dataset scoring and regression detection |

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

The SDKs are pinned in `requirements.txt` and deliberately kept **out** of the
book's own `requirements.txt` — the manuscript must build without them. Bumping
a pin is an editorial act: the prose describing that API has to be re-checked
against the new version.

MLflow 3.15 put the filesystem tracking store into maintenance mode for traces,
so the tests use a SQLite backend, and trace export is forced synchronous so
assertions do not race the background writer.
