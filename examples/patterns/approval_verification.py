"""Verifying that an approval covers this exact proposal, and has not lapsed.

The companion to the approval gate: the gate persists the pause, this verifies
the decision at commit time. Timezone-aware timestamps are required rather than
assumed, because a naive datetime is how an expiry check silently passes.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


def _require_aware(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value


class ApprovalRequest(BaseModel):
    """Exact action reviewed by an eligible human approver; immutable after presentation."""

    tenant_id: str
    run_id: str
    actor_id: str
    tool_version: str
    logical_effect_key: str
    arguments: dict[str, Any]
    expected_resource_version: int
    policy_digest: str
    expires_at: datetime

    @field_validator("expires_at")
    @classmethod
    def expiry_is_aware(cls, value: datetime) -> datetime:
        return _require_aware(value, "expires_at")

    def digest(self) -> str:
        payload = json.dumps(
            self.model_dump(mode="json"), sort_keys=True, separators=(",", ":")
        ).encode()
        return "sha256:" + hashlib.sha256(payload).hexdigest()


# --8<-- region:core
class ApprovalDecision(BaseModel):
    approval_id: str
    proposal_hash: str
    tenant_id: str
    run_id: str
    approver_id: str
    approved_at: datetime
    expires_at: datetime
    policy_digest: str
    obligations: tuple[str, ...] = Field(default_factory=tuple)

    @field_validator("approved_at", "expires_at")
    @classmethod
    def timestamps_are_aware(cls, value: datetime, info) -> datetime:
        return _require_aware(value, info.field_name)

    @model_validator(mode="after")
    def expiry_follows_approval(self) -> "ApprovalDecision":
        if self.expires_at <= self.approved_at:
            raise ValueError("expires_at must be later than approved_at")
        return self


def verify_approval(
    proposal: ApprovalRequest,
    decision: ApprovalDecision,
    *,
    now: datetime,
    actual_resource_version: int,
) -> None:
    """Fail closed if the approval no longer matches the action or current state."""

    _require_aware(now, "now")
    if decision.proposal_hash != proposal.digest():
        raise PermissionError("approval is not bound to this proposal")
    if (decision.tenant_id, decision.run_id) != (proposal.tenant_id, proposal.run_id):
        raise PermissionError("approval scope mismatch")
    if decision.approver_id == proposal.actor_id:
        raise PermissionError("actor cannot self-approve")
    if decision.policy_digest != proposal.policy_digest:
        raise PermissionError("policy changed after approval")
    if now < decision.approved_at:
        raise PermissionError("approval is not yet effective")
    if now >= min(decision.expires_at, proposal.expires_at):
        raise PermissionError("approval expired")
    if actual_resource_version != proposal.expected_resource_version:
        raise PermissionError("resource changed after approval")


# --8<-- endregion:core
