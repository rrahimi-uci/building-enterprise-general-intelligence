"""The conformance suite must pass a conforming adapter and name every gap."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from agents.exceptions import AgentsException

from examples.runtime.adapter_conformance import run_conformance
from examples.runtime.step_execution import PlatformContext, execute_step


@dataclass
class StepRequest:
    input_items: str
    max_turns: int
    run_id: str
    agent_version: str


class StubGateway:
    async def invoke(self, *args, **kwargs):  # pragma: no cover - not reached here
        return {"status": "ok"}


REQUEST = StepRequest(input_items="Review mortgage case MORT-2026-000184", max_turns=4,
                      run_id="RUN-98217", agent_version="mortgage-evidence-agent@0.1.0")
CONTEXT = PlatformContext(tenant_id="harborlight-us-west", subject_id="MORT-2026-000184",
                          actor_id="mortgage-evidence-agent", run_id="RUN-98217",
                          gateway=StubGateway())


async def conforming_adapter(request, context, *, model=None):
    """Chapter 3's adapter plus the error mapping the platform contract requires."""
    try:
        return await execute_step(request, context, model=model)
    except AgentsException as error:
        return {"status": "failed", "error_code": f"adapter.{type(error).__name__}",
                "usage": "unavailable"}


async def cancellation_swallowing_adapter(request, context, *, model=None):
    """A framework that drops cancellation and reports success anyway."""
    try:
        return await conforming_adapter(request, context, model=model)
    except asyncio.CancelledError:
        return {"status": "completed", "usage": "0"}


async def test_a_conforming_adapter_has_no_gaps():
    report = await run_conformance(conforming_adapter, REQUEST, CONTEXT)
    assert report.gaps == ()
    assert {r.name for r in report.results} == {
        "typed_disposition", "usage_reported", "cancellation_propagates", "sdk_errors_mapped",
    }


async def test_dropped_cancellation_is_reported_as_a_gap():
    report = await run_conformance(cancellation_swallowing_adapter, REQUEST, CONTEXT)
    assert report.gaps == ("cancellation_propagates",)
    detail = next(r.detail for r in report.results if r.name == "cancellation_propagates")
    assert "swallowed" in detail


async def test_a_leaked_sdk_exception_is_reported_as_a_gap():
    async def leaking_adapter(request, context, *, model=None):
        result = await conforming_adapter(request, context, model=model)
        if result["status"] == "failed":
            raise AgentsException("framework-native failure")
        return result

    report = await run_conformance(leaking_adapter, REQUEST, CONTEXT)
    assert report.gaps == ("sdk_errors_mapped",)


async def test_chapter_3_adapter_meets_the_runtime_interface_and_names_any_gap():
    # The deliberately small Chapter 3 adapter must keep the core promises;
    # anything it does not yet do must surface as a named gap, never silently.
    report = await run_conformance(execute_step, REQUEST, CONTEXT)
    assert set(report.gaps) <= {"sdk_errors_mapped"}
    assert all(r.detail for r in report.results)
