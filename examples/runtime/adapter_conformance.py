"""An adapter conformance suite: parity is tested, never assumed.

A shared contract does not make two agent SDKs interchangeable. The platform
proves what an adapter actually does by driving it with scripted test models
and checking the promises of the Chapter 3 seam. A failing check becomes a
named gap to publish as a known limitation, not a difference to assume away.

The suite accepts any adapter with the shape
`execute(request, context, *, model) -> dict`, such as
`examples.runtime.step_execution.execute_step`.
"""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, get_args

from agents.exceptions import AgentsException
from agents.models.interface import Model

from examples._harness.scripted_model import Say, ScriptedModel
from examples.contracts import AgentStepResult

Adapter = Callable[..., Awaitable[dict[str, Any]]]
PLATFORM_STATUSES = frozenset(get_args(AgentStepResult.model_fields["status"].annotation))


class BlockingModel(Model):
    """A model that never answers, so the suite can cancel mid-run."""

    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.cancelled = False

    async def get_response(self, *args: Any, **kwargs: Any):
        self.started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.cancelled = True
            raise

    async def stream_response(self, *args: Any, **kwargs: Any):  # pragma: no cover
        raise NotImplementedError

    async def close(self) -> None:  # pragma: no cover
        return None


# --8<-- example:start
@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ConformanceReport:
    results: tuple[CheckResult, ...]

    @property
    def gaps(self) -> tuple[str, ...]:
        """Failed checks: publish each as a known limitation of this adapter."""
        return tuple(r.name for r in self.results if not r.passed)


VALID_OUTPUT = json.dumps(
    {"status": "completed", "summary": "Evidence reviewed.", "evidence_artifact_ids": []}
)


async def check_typed_disposition(execute: Adapter, request, context) -> CheckResult:
    result = await execute(request, context, model=ScriptedModel([Say(VALID_OUTPUT)]))
    status = result.get("status")
    return CheckResult("typed_disposition", status in PLATFORM_STATUSES,
                       f"status={status!r}")


async def check_usage_reported(execute: Adapter, request, context) -> CheckResult:
    result = await execute(request, context, model=ScriptedModel([Say(VALID_OUTPUT)]))
    return CheckResult("usage_reported", bool(result.get("usage")),
                       "usage present" if result.get("usage") else "no usage field")


async def check_cancellation(execute: Adapter, request, context,
                             timeout_s: float = 2.0) -> CheckResult:
    model = BlockingModel()
    task = asyncio.create_task(execute(request, context, model=model))
    await asyncio.wait_for(model.started.wait(), timeout_s)
    task.cancel()
    try:
        result = await asyncio.wait_for(task, timeout_s)
    except asyncio.CancelledError:
        return CheckResult("cancellation_propagates", model.cancelled,
                           "cancelled through to the model call")
    return CheckResult("cancellation_propagates", False,
                       f"swallowed cancellation and returned {result.get('status')!r}")


async def check_error_mapping(execute: Adapter, request, context) -> CheckResult:
    try:
        result = await execute(request, context, model=ScriptedModel([Say("not json")]))
    except AgentsException as error:
        return CheckResult("sdk_errors_mapped", False,
                           f"leaked SDK exception {type(error).__name__}")
    mapped = result.get("status") == "failed" and bool(result.get("error_code"))
    return CheckResult("sdk_errors_mapped", mapped, f"status={result.get('status')!r}")


async def run_conformance(execute: Adapter, request, context) -> ConformanceReport:
    checks = (check_typed_disposition, check_usage_reported,
              check_cancellation, check_error_mapping)
    return ConformanceReport(tuple([await c(execute, request, context) for c in checks]))

# --8<-- example:end
