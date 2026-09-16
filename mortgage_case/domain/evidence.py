"""Candidate and verified-evidence boundaries."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CaseSummaryCandidate(BaseModel):
    """A model suggestion that is deliberately incapable of being a decision."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["CANDIDATE_READY", "NEEDS_INPUT"]
    summary: str = Field(min_length=1)
    available_document_ids: tuple[str, ...]
    missing_document_kinds: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    proposed_next_control: str = Field(min_length=1)
    lending_decision: Literal["not_provided"] = "not_provided"


class VerifiedEvidence(BaseModel):
    """A deterministic acceptance record, introduced after the baseline."""

    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    document_id: str
    field_name: str
    value: str
    source_revision: str
    verification_method: str
