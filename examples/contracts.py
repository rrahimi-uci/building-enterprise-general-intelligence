"""The provider-neutral contracts every agent step and platform API shares.

One file, two views. Chapter 03 needs the agent-step subset; chapter 04 needs
the full platform set. In earlier drafts these were two listings that had already
drifted apart -- the shorter one was not even a prefix of the longer.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import IntEnum
from typing import Annotated, Any, Callable, Literal

from pydantic import (
    BaseModel, BeforeValidator, ConfigDict, Field, PlainSerializer, field_validator,
)

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
    # invoke_tool is a read the loop may run; proposed_action is a mutation that
    # leaves the loop as a proposal for the six gates.
    disposition: Literal[
        "answer", "needs_input", "invoke_tool", "proposed_action", "delegate"
    ]
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

class RiskClass(IntEnum):
    """Effect risk class (Chapter 22): R0 pure transform to R4 irreversible action."""

    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4


def _risk_class(value: object) -> object:
    # Accept RiskClass.R1 or "R1"; refuse a bare number, which reads as a tier.
    if isinstance(value, str) and value in RiskClass.__members__:
        return RiskClass[value]
    if not isinstance(value, RiskClass):
        raise ValueError("risk class must be R0-R4, not a bare number")
    return value


Risk = Annotated[
    RiskClass,
    BeforeValidator(_risk_class),
    PlainSerializer(lambda risk: risk.name, return_type=str),
]


class SkillRequirement(BaseModel):
    capability: str
    purpose: str
    risk_ceiling: Risk
    required_data_classes: frozenset[str] = frozenset()
    region: str

class PlanNode(BaseModel):
    id: str
    capability: str
    depends_on: tuple[str, ...] = ()
    maximum_cost_usd: Decimal = Field(ge=0)
    maximum_attempts: int = Field(ge=1, le=10)
    risk_class: Risk

    @field_validator("maximum_cost_usd", mode="before")
    @classmethod
    def reject_binary_float_costs(cls, value: object) -> object:
        if isinstance(value, float):
            raise ValueError("maximum_cost_usd must be Decimal or a decimal string")
        return value

class CandidatePlan(BaseModel):
    revision: int = Field(ge=1)
    nodes: tuple[PlanNode, ...] = Field(min_length=1, max_length=100)

# --8<-- region:task
class TaskEnvelope(BaseModel):
    """The one child-task contract (Chapter 18), grouped as the field-group table."""

    model_config = ConfigDict(frozen=True)

    # Identity
    task_id: str
    run_id: str
    parent_task_id: str | None = None
    tenant_id: str
    subject_id: str
    owner_agent: str  # receiving agent@version
    # Goal
    goal: str
    acceptance_contract: str
    deadline: datetime
    # Data and contract
    input_artifact_ids: tuple[str, ...] = ()
    output_schema: str
    # Authority: the capability envelope this task may use (Chapter 21)
    capability_grant_id: str
    delegation_depth: int = Field(ge=0)  # further delegation levels allowed
    # Budgets
    maximum_cost_usd: Decimal = Field(ge=0)
    # Reliability
    idempotency_key: str
    depends_on: tuple[str, ...] = ()
    cancellation_parent_id: str | None = None
    state_version: int = 0
    # Observability
    trace_context: str  # W3C traceparent


SubsetCheck = Callable[[str, str], bool]  # (parent grant, child grant) -> provably narrower?


class TaskConflict(Exception):
    """An idempotency key was reused for a different task."""


class TaskService:
    def __init__(self, is_subset: SubsetCheck) -> None:
        self._is_subset = is_subset
        self._by_key: dict[tuple[str, str], TaskEnvelope] = {}
        self._remaining: dict[str, Decimal] = {}

    def create_child(self, parent: TaskEnvelope, child: TaskEnvelope) -> TaskEnvelope:
        existing = self._by_key.get((child.run_id, child.idempotency_key))
        if existing is not None:
            if existing != child:
                raise TaskConflict(child.idempotency_key)
            return existing  # redelivery: same task, no second withdrawal
        if (child.run_id, child.parent_task_id) != (parent.run_id, parent.task_id):
            raise ValueError("child must name its parent task and run")
        if (child.tenant_id, child.subject_id) != (parent.tenant_id, parent.subject_id):
            raise PermissionError("tenant and subject cannot change")
        if child.delegation_depth >= parent.delegation_depth:
            raise PermissionError("delegation depth was not reduced")
        if child.deadline > parent.deadline:
            raise PermissionError("child deadline exceeds the parent's")
        remaining = self._remaining.get(parent.task_id, parent.maximum_cost_usd)
        if child.maximum_cost_usd > remaining:
            raise PermissionError("budget exceeds the parent's remaining budget")
        if not self._is_subset(parent.capability_grant_id, child.capability_grant_id):
            raise PermissionError("capability envelope is not a subset of the parent's")
        self._remaining[parent.task_id] = remaining - child.maximum_cost_usd
        self._by_key[(child.run_id, child.idempotency_key)] = child
        return child

# --8<-- endregion:task
