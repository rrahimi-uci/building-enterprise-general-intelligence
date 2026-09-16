"""The platform adapter must return its own contract, not the SDK's."""
from __future__ import annotations

from dataclasses import dataclass

from examples._harness.scripted_model import ScriptedModel, Say, ToolCall
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


def _request():
    return StepRequest(input_items="Review mortgage case MORT-2026-000184", max_turns=4,
                       run_id="r-1", agent_version="1.4.0")


async def test_step_returns_the_platform_contract():
    model = ScriptedModel([
        Say('{"status": "completed", "summary": "Mortgage evidence review may continue.",'
            ' "evidence_artifact_ids": []}'),
    ])
    context = PlatformContext(tenant_id="harborlight-us-west", subject_id="MORT-2026-000184", actor_id="mortgage-agent",
                              run_id="r-1", gateway=StubGateway())
    out = await execute_step(_request(), context, model=model)
    # The caller sees the platform's own dict, never an SDK RunResult.
    assert isinstance(out, dict)
    assert out["status"] == "completed"
    assert "decision_summary" in out
