"""The provider-neutral contracts every agent step and platform API shares.

One file, several views. Chapter 03 shows the agent-step subset (region
``step``); chapter 04 shows the run, artifact, and event contracts (region
``platform``). In earlier drafts these were separate listings that had already
drifted apart -- the shorter one was not even a prefix of the longer.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import IntEnum
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel, BeforeValidator, ConfigDict, Field, PlainSerializer, field_validator,
    model_validator,
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


# --8<-- region:platform
Digest = Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")]
# A Skill or pack pin names its version and its content digest: name@1.2.3#sha256:...
PinnedRef = Annotated[str, Field(pattern=r"^[\w.-]+@[\w.+-]+#sha256:[0-9a-f]{64}$")]


class RuntimeBinding(BaseModel):
    model_config = ConfigDict(frozen=True)
    adapter: str
    sdk: str


class RunBudget(BaseModel):
    model_config = ConfigDict(frozen=True)
    usd: Decimal = Field(gt=0)
    tokens: int = Field(gt=0)
    steps: int = Field(gt=0)
    delegation_depth: int = Field(ge=0)


class RunManifest(BaseModel):
    """Written once at admission and never edited; new versions mean a new run.

    Release pins (agent build, prompt and policy bundles, tool contracts) are
    reached through ``release_manifest``; this record holds what was resolved
    for this run inside that release.
    """

    model_config = ConfigDict(frozen=True)
    run_id: str
    tenant_id: str
    subject: str                     # the initiating subject
    actor: str                       # the acting workload identity
    purpose: str
    risk_tier: Literal["T0", "T1", "T2", "T3", "T4"]   # use-case tier, Chapter 26
    release_manifest: Digest
    agent: str
    runtime: RuntimeBinding
    skills: tuple[PinnedRef, ...]
    skill_pack: PinnedRef
    model_route: str                 # chosen within the release's eligible set
    knowledge_snapshots: tuple[str, ...]
    capability_envelope: str
    budget: RunBudget
    retention_class: str
    trace_id: str


class ArtifactRef(BaseModel):
    """How runs, events, and results point at an artifact: by version and hash."""

    model_config = ConfigDict(frozen=True)
    artifact_id: str
    version: int = Field(ge=1)
    media_type: str
    sha256: Digest
    created_by_run: str
    tenant_id: str
    classification: str
    residency: str


class CloudEvent(BaseModel):
    """CloudEvents 1.0 envelope for a fact that already happened.

    Large or sensitive payloads travel by ``dataref`` and ``datahash``; ``data``
    is optional and only for small, non-sensitive facts.
    """

    specversion: Literal["1.0"] = "1.0"
    id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    type: str = Field(min_length=1)
    subject: str | None = None
    time: datetime
    dataschema: str | None = None
    tenant_id: str
    correlation_id: str
    causation_id: str | None = None
    traceparent: str | None = None
    dataref: str | None = None
    datahash: Digest | None = None
    data: dict[str, Any] | None = None

    @field_validator("source")
    @classmethod
    def source_is_uri_reference(cls, value: str) -> str:
        if ":" not in value and not value.startswith("/"):
            raise ValueError("source must be a URI-reference")
        return value

    @model_validator(mode="after")
    def reference_carries_its_hash(self) -> "CloudEvent":
        if (self.dataref is None) != (self.datahash is None):
            raise ValueError("dataref and datahash travel together")
        return self


def deduplication_key(event: CloudEvent) -> tuple[str, str]:
    """Producers make (source, id) unique per distinct event; consumers dedupe on it."""
    return event.source, event.id

# --8<-- endregion:platform
