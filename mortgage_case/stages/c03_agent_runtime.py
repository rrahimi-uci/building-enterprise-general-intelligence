"""Chapter 3: framework-neutral runtime with an offline implementation."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from ..domain.case import load_anchor_case
from ..platform.runtime import AgentStepRequest, ScriptedRuntime
from ..stage_report import StageReport


SCENARIOS = {"happy_path", "tool_allowlist_escape"}


def run(scenario: str = "happy_path") -> StageReport:
    """Run one bounded step without allowing SDK state to become business truth."""

    if scenario not in SCENARIOS:
        raise ValueError(f"C03 does not define scenario {scenario!r}")
    case = load_anchor_case()
    requested_tool = "mortgage.case.read@1"
    if scenario == "tool_allowlist_escape":
        requested_tool = "mortgage.los.write@1"
    request = AgentStepRequest(
        run_id="RUN-MORT-000184-C03",
        case_id=case.case_id,
        tenant_id=case.tenant_id,
        input_items="Review the authorized mortgage evidence and identify missing inputs.",
        agent_version="mortgage-evidence-agent@0.1.0",
        eligible_tool_versions=("mortgage.case.read@1", "mortgage.policy.read@1"),
        max_turns=4,
        # A fixed teaching deadline keeps the checkpoint output and tests
        # reproducible; production injects a workflow-owned clock.
        deadline=datetime(2099, 12, 31, 23, 59, tzinfo=timezone.utc),
    )
    result = asyncio.run(ScriptedRuntime(requested_tool=requested_tool).execute(request))
    status = "failed" if result.status == "failed" else "completed"
    return StageReport(
        chapter="C03",
        scenario=scenario,
        case_id=case.case_id,
        status=status,
        before="The deterministic shell has typed proposals but no provider-neutral runtime seam.",
        added="A bounded AgentRuntime request/result contract and an offline implementation enforce the tool allowlist outside the model.",
        after=(
            "The step returns a platform-owned result; framework state remains replaceable and cannot authorize a write."
            if result.status != "failed"
            else "The out-of-scope tool was rejected before execution."
        ),
        evidence=result.evidence_artifact_ids,
        failures=((result.error_code,) if result.error_code else ()),
        limitations=(
            "The OpenAI Agents SDK adapter is optional and provider-backed execution is opt-in.",
            "The offline runtime does not prove production authorization or workflow durability.",
        ),
        details={
            "result": result.model_dump(mode="json"),
            "eligible_tool_versions": list(request.eligible_tool_versions),
        },
    )
