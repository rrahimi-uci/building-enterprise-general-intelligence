"""A human approval gate that survives the wait.

The book's position is that the pause is the design problem, not the prompt: a
run held for approval may sit for days across deploys and token expiry. So the
decision context is persisted with the pause, the grant is bound to the exact
proposal, and an expired grant is a refusal rather than a warning.

The grant is also *issued* rather than constructed. A plain dataclass any caller
can build is not an approval: it lets the code that wants the effect mint its own
permission for it. Here the approval service signs, and the gate verifies.
"""
from __future__ import annotations

import copy
import hashlib
import hmac
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
    signature: str


class ApprovalExpired(Exception):
    """The grant lapsed before the effect committed."""


class ProposalMismatch(Exception):
    """The proposal changed after it was approved."""


class GrantNotAuthentic(Exception):
    """The grant was not issued by the approval service."""


class ApprovalService:
    """Issues signed grants. Only this component speaks for a human approver."""

    def __init__(self, secret: bytes) -> None:
        self._secret = secret

    def _signature(self, proposal_hash: str, approver_id: str, expires_at: datetime) -> str:
        payload = f"{proposal_hash}|{approver_id}|{expires_at.isoformat()}".encode()
        return hmac.new(self._secret, payload, hashlib.sha256).hexdigest()

    def issue(self, proposal_hash: str, approver_id: str, expires_at: datetime) -> ApprovalGrant:
        return ApprovalGrant(
            proposal_hash=proposal_hash, approver_id=approver_id, expires_at=expires_at,
            signature=self._signature(proposal_hash, approver_id, expires_at),
        )

    def verify(self, grant: ApprovalGrant) -> None:
        expected = self._signature(grant.proposal_hash, grant.approver_id, grant.expires_at)
        # compare_digest, not ==: an equality check on a signature leaks timing.
        if not hmac.compare_digest(expected, grant.signature):
            raise GrantNotAuthentic("grant was not issued by the approval service")


@dataclass
class PendingApprovals:
    """Persisted pauses. A real system stores these in the workflow database."""

    service: ApprovalService
    pending: dict[str, dict] = field(default_factory=dict)

    def pause(self, run_id: str, action: str, arguments: dict, ttl: timedelta) -> str:
        # Deep copy: the caller keeps a reference, and a nested value mutated
        # after the pause would otherwise change the proposal a real effect uses
        # without changing the digest that was approved.
        arguments = copy.deepcopy(arguments)
        self.pending[run_id] = {
            "digest": proposal_hash(action, arguments),
            "action": action,
            "arguments": arguments,
            # The context is stored with the pause. Reconstructing it later from
            # a transcript is exactly what fails after a deploy.
            "expires_at": datetime.now(timezone.utc) + ttl,
        }
        return self.pending[run_id]["digest"]

    def commit(self, run_id: str, grant: ApprovalGrant, now: datetime | None = None) -> str:
        record = self.pending[run_id]
        now = now or datetime.now(timezone.utc)
        # Authenticity first: an unsigned grant is not an approval, so there is
        # nothing to compare it against.
        self.service.verify(grant)
        # Recompute from the stored proposal rather than trusting the stored
        # digest, so tampering with the pending record is caught too.
        current = proposal_hash(record["action"], record["arguments"])
        if grant.proposal_hash != current:
            raise ProposalMismatch("the approved proposal is not the one being committed")
        if now >= grant.expires_at or now >= record["expires_at"]:
            raise ApprovalExpired("approval lapsed; re-request rather than assume consent")
        del self.pending[run_id]
        return f"committed {record['action']} approved by {grant.approver_id}"


# --8<-- example:end
