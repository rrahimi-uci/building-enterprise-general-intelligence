"""The provider-neutral contracts every agent step and platform API shares.

One file, two views. Chapter 02 needs the agent-step subset; chapter 04 needs
the full platform set. Before v2.0.0 these were two listings that had already
drifted apart -- the shorter one was not even a prefix of the longer.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

# --8<-- region:step
class EvidenceRef(BaseModel):
    uri: str
    sha256: str
    source_revision: str
    authorization_decision_id: str

class ToolCall(BaseModel):
    tool_id: str
    arguments: dict[str, Any]
    logical_effect_key: str | None = None

class AgentDecision(BaseModel):
    disposition: Literal["answer", "needs_input", "invoke_tool", "delegate"]
    answer: str | None = None
    tool_call: ToolCall | None = None
    evidence: list[EvidenceRef] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)

class AgentStepRequest(BaseModel):
    run_id: str
    node_id: str
    state_version: int
    agent_version: str
    context_manifest_id: str
    eligible_tool_versions: tuple[str, ...]
    max_turns: int = Field(ge=1, le=20)
    deadline: datetime

class AgentStepResult(BaseModel):
    status: Literal["completed", "needs_input", "proposed_action", "failed"]
    decision: AgentDecision | None = None
    output_artifact_ids: tuple[str, ...] = ()
    usage: dict[str, int | float] = Field(default_factory=dict)
    error_code: str | None = None

# --8<-- endregion:step

class SkillRequirement(BaseModel):
    capability: str
    purpose: str
    maximum_risk: int = Field(ge=0, le=4)
    required_data_classes: frozenset[str] = frozenset()
    region: str

class PlanNode(BaseModel):
    id: str
    capability: str
    depends_on: tuple[str, ...] = ()
    maximum_cost_usd: float = Field(ge=0)
    maximum_attempts: int = Field(ge=1, le=10)
    risk_class: int = Field(ge=0, le=4)

class CandidatePlan(BaseModel):
    revision: int = Field(ge=1)
    nodes: tuple[PlanNode, ...] = Field(min_length=1, max_length=100)
