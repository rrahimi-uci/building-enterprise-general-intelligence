"""A human approval gate that survives the wait.

The book's position is that the pause is the design problem, not the prompt: a
run held for approval may sit for days across deploys and token expiry. So the
decision context is persisted with the pause, the grant is bound to the exact
proposal, and an expired grant is a refusal rather than a warning.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

# --8<-- example:start


def proposal_hash(action: str, arguments: dict) -> str:
    """Bind a grant to one exact proposal, not to an intent."""
    payload = json.dumps({"action": action, "arguments": arguments}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


@dataclass(frozen=True)
class ApprovalGrant:
    proposal_hash: str
    approver_id: str
    expires_at: datetime


class ApprovalExpired(Exception):
    """The grant lapsed before the effect committed."""


class ProposalMismatch(Exception):
    """The proposal changed after it was approved."""


@dataclass
class PendingApprovals:
    """Persisted pauses. A real system stores these in the workflow database."""

    pending: dict[str, dict] = field(default_factory=dict)

    def pause(self, run_id: str, action: str, arguments: dict, ttl: timedelta) -> str:
        digest = proposal_hash(action, arguments)
        self.pending[run_id] = {
            "digest": digest,
            "action": action,
            # Copy: the caller keeps a reference to this dict, and mutating it
            # after the pause would leave the stored record disagreeing with the
            # digest that was approved.
            "arguments": dict(arguments),
            # The context is stored with the pause. Reconstructing it later from
            # a transcript is exactly what fails after a deploy.
            "expires_at": datetime.now(timezone.utc) + ttl,
        }
        return digest

    def commit(self, run_id: str, grant: ApprovalGrant, now: datetime | None = None) -> str:
        record = self.pending[run_id]
        now = now or datetime.now(timezone.utc)
        if grant.proposal_hash != record["digest"]:
            raise ProposalMismatch("the approved proposal is not the one being committed")
        if now >= grant.expires_at or now >= record["expires_at"]:
            raise ApprovalExpired("approval lapsed; re-request rather than assume consent")
        del self.pending[run_id]
        return f"committed {record['action']} approved by {grant.approver_id}"


# --8<-- example:end
