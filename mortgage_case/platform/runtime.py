"""Provider-neutral bounded runtime contracts for Chapter 3."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentStepRequest(BaseModel):
    """Platform request translated into whichever agent framework is selected."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    case_id: str = Field(pattern=r"^MORT-\d{4}-\d{6}$")
    tenant_id: str = Field(min_length=1)
    input_items: str = Field(min_length=1)
    agent_version: str = Field(min_length=1)
    eligible_tool_versions: tuple[str, ...] = ()
    max_turns: int = Field(default=4, ge=1, le=20)
    deadline: datetime

    @field_validator("deadline")
    @classmethod
    def deadline_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("deadline must be timezone-aware")
        return value.astimezone(timezone.utc)


class AgentStepResult(BaseModel):
    """Platform-owned result; no SDK result or session object crosses the runtime interface."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["completed", "needs_input", "proposed_action", "failed"]
    summary: str = Field(min_length=1)
    evidence_artifact_ids: tuple[str, ...] = ()
    tool_calls: tuple[str, ...] = ()
    error_code: str | None = None
    usage: dict[str, int] = Field(default_factory=dict)


class AgentRuntime(Protocol):
    """The only interface a workflow needs from an agent framework."""

    async def execute(self, request: AgentStepRequest) -> AgentStepResult: ...


class ScriptedRuntime:
    """Offline runtime that enforces the same tool allowlist as the adapter."""

    def __init__(self, *, requested_tool: str | None = None) -> None:
        self.requested_tool = requested_tool

    async def execute(self, request: AgentStepRequest) -> AgentStepResult:
        if self.requested_tool and self.requested_tool not in request.eligible_tool_versions:
            return AgentStepResult(
                status="failed",
                summary="The requested capability is outside the step allowlist.",
                error_code="TOOL_NOT_ELIGIBLE",
            )
        return AgentStepResult(
            status="completed",
            summary="The bounded runtime returned a mortgage evidence-review proposal.",
            evidence_artifact_ids=("ARTIFACT-EVIDENCE-000184",),
            tool_calls=((self.requested_tool,) if self.requested_tool else ()),
            usage={"turns": 1, "tool_calls": 1 if self.requested_tool else 0},
        )
