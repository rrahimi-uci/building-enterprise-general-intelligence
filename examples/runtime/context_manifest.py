"""One ContextManifest per agent step: what the model saw, by reference.

Chapter 06 says a prompt is a disposable, authorized projection and that the
manifest, not logged plaintext, is the record of it. This model enforces the
three rules that make that record trustworthy: a segment's trust tier follows
from its kind and cannot be raised; every section stays inside a cap fixed
before retrieval; and the sealed hash changes if anything recorded changes.
Tool results observed inside the step's loop arrive as a new revision.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

# --8<-- region:core
Kind = Literal[
    "system_instruction", "skill_instruction", "user_request",
    "run_state", "conversation", "enterprise_data", "tool_result", "memory",
]
# Tier follows from kind. Content cannot promote itself to direct behavior.
TRUST_TIER: dict[str, int] = {
    "system_instruction": 1, "skill_instruction": 2, "user_request": 3,
    "run_state": 4, "conversation": 4, "enterprise_data": 4,
    "tool_result": 4, "memory": 4,
}
SECTION: dict[str, str] = {
    "system_instruction": "instructions", "skill_instruction": "instructions",
    "user_request": "request", "run_state": "state", "conversation": "conversation",
    "enterprise_data": "evidence", "tool_result": "evidence", "memory": "memory",
}
Digest = Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")]


class ContextSegment(BaseModel):
    model_config = ConfigDict(frozen=True)
    segment_id: str
    kind: Kind
    trust_tier: int
    source_uri: str
    source_revision: str
    sha256: Digest
    authorization_decision_id: str
    freshness: datetime
    tokens: int = Field(ge=0)

    @model_validator(mode="after")
    def tier_follows_kind(self) -> "ContextSegment":
        if self.trust_tier != TRUST_TIER[self.kind]:
            raise ValueError(f"{self.kind} is tier {TRUST_TIER[self.kind]}, "
                             f"not tier {self.trust_tier}")
        return self


class ContextBudget(BaseModel):
    """Per-section caps, fixed before retrieval."""

    model_config = ConfigDict(frozen=True)
    max_tokens: int = Field(gt=0)
    caps: dict[str, int]


class ContextManifest(BaseModel):
    model_config = ConfigDict(frozen=True)
    context_id: str
    run_id: str
    run_manifest_digest: Digest
    node_id: str
    step_request_id: str
    revision: int = Field(ge=1)
    policy_version: str
    budget: ContextBudget
    segments: tuple[ContextSegment, ...]
    omitted_candidate_ids: tuple[str, ...] = ()
    redactions: tuple[str, ...] = ()
    created_at: datetime
    manifest_sha256: Digest | None = None

    @model_validator(mode="after")
    def stays_inside_the_budget(self) -> "ContextManifest":
        ids = [s.segment_id for s in self.segments]
        if len(ids) != len(set(ids)):
            raise ValueError("segment ids must be unique")
        allocation: dict[str, int] = {}
        for segment in self.segments:
            section = SECTION[segment.kind]
            allocation[section] = allocation.get(section, 0) + segment.tokens
        for section, used in allocation.items():
            if used > self.budget.caps.get(section, 0):
                raise ValueError(f"section {section!r} exceeds its cap")
        if sum(allocation.values()) > self.budget.max_tokens:
            raise ValueError("context exceeds max_tokens")
        return self

    def digest(self) -> str:
        body = self.model_dump(mode="json", exclude={"manifest_sha256"})
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
        return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()

    def seal(self) -> "ContextManifest":
        return self.model_copy(update={"manifest_sha256": self.digest()})

    def verify(self) -> bool:
        return self.manifest_sha256 == self.digest()

    def revise(self, observed: tuple[ContextSegment, ...], *,
               at: datetime) -> "ContextManifest":
        """Append in-loop tool results as a new revision of the same step."""
        if any(s.kind != "tool_result" for s in observed):
            raise ValueError("only tool results may join a step after assembly")
        revised = ContextManifest.model_validate({
            **self.model_dump(exclude={"manifest_sha256"}),
            "revision": self.revision + 1,
            "segments": self.segments + observed,
            "created_at": at,
        })
        return revised.seal()

# --8<-- endregion:core
