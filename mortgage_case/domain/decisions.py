"""Typed model proposals and workflow commands."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .money import CalculationResult


class ExtractedFactCandidate(BaseModel):
    """A model-extracted candidate that still needs deterministic verification."""

    model_config = ConfigDict(extra="forbid")

    field_name: str = Field(min_length=1)
    value: str = Field(min_length=1)
    evidence_ref: str = Field(min_length=1)
    confidence_label: Literal["low", "medium", "high"]
    verified: Literal[False] = False


class WorkflowCommand(BaseModel):
    """A proposed next workflow operation with no side effect of its own."""

    model_config = ConfigDict(extra="forbid")

    command: Literal["request_document", "needs_input", "route_to_underwriter"]
    case_id: str
    case_version: int = Field(ge=1)
    document_kind: str | None = None
    reason: str = Field(min_length=1)


class AgentProposal(BaseModel):
    """The only output accepted from the deterministic shell boundary."""

    model_config = ConfigDict(extra="forbid")

    case_id: str
    case_version: int = Field(ge=1)
    summary: str = Field(min_length=1)
    candidate_facts: tuple[ExtractedFactCandidate, ...] = ()
    calculations: tuple[CalculationResult, ...] = ()
    next_command: WorkflowCommand | None = None
    requested_effect: Literal["none"] = "none"
