"""A human approval gate that survives the wait.

The book's position is that the pause is the design problem, not the prompt: a
run held for approval may sit for days across deploys and token expiry. So the
decision context is persisted with the pause, the approval decision is bound to
the exact proposal, and an expired decision is a refusal.

The approval decision is also *issued* rather than constructed. A plain
dataclass any caller can build is not an approval: it lets the code that wants
the effect mint its own permission for it. Here the Approval Service signs, and
the gate verifies.
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
    """Bind an approval decision to one exact proposal, not to an intent."""
    payload = json.dumps({"action": action, "arguments": arguments}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


@dataclass(frozen=True)
class ApprovalDecision:
    proposal_hash: str
    approver_id: str
    expires_at: datetime
    signature: str


class ApprovalExpired(Exception):
    """The approval decision lapsed before the effect committed."""


class ApprovalMismatch(Exception):
    """The proposal changed after it was approved."""


class ApprovalNotAuthentic(Exception):
    """The approval decision was not issued by the Approval Service."""


class ApprovalService:
    """Issues signed decisions. Only this component speaks for a human reviewer."""

    def __init__(self, secret: bytes) -> None:
        self._secret = secret

    def _signature(self, proposal_hash: str, approver_id: str, expires_at: datetime) -> str:
        payload = f"{proposal_hash}|{approver_id}|{expires_at.isoformat()}".encode()
        return hmac.new(self._secret, payload, hashlib.sha256).hexdigest()

    def issue(self, proposal_hash: str, approver_id: str, expires_at: datetime) -> ApprovalDecision:
        return ApprovalDecision(
            proposal_hash=proposal_hash, approver_id=approver_id, expires_at=expires_at,
            signature=self._signature(proposal_hash, approver_id, expires_at),
        )

    def verify(self, decision: ApprovalDecision) -> None:
        expected = self._signature(decision.proposal_hash, decision.approver_id, decision.expires_at)
        # compare_digest, not ==: an equality check on a signature leaks timing.
        if not hmac.compare_digest(expected, decision.signature):
            raise ApprovalNotAuthentic("decision was not issued by the Approval Service")


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

    def commit(self, run_id: str, decision: ApprovalDecision, now: datetime | None = None) -> str:
        record = self.pending[run_id]
        now = now or datetime.now(timezone.utc)
        # Authenticity first: an unsigned decision is not an approval, so there is
        # nothing to compare it against.
        self.service.verify(decision)
        # Recompute from the stored proposal rather than trusting the stored
        # digest, so tampering with the pending record is caught too.
        current = proposal_hash(record["action"], record["arguments"])
        if decision.proposal_hash != current:
            raise ApprovalMismatch("the approved proposal is not the one being committed")
        if now >= decision.expires_at or now >= record["expires_at"]:
            raise ApprovalExpired("approval lapsed; request it again")
        del self.pending[run_id]
        return f"committed {record['action']} approved by {decision.approver_id}"


# --8<-- example:end
