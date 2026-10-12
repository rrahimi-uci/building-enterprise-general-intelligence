"""Effect-level idempotency: making an at-least-once retry safe to repeat.

The book's position is that agentic systems cannot promise exactly-once
delivery, so they must make the *effect* idempotent instead. A logical effect
key identifies the intent; the ledger guarantees the intent commits once, even
if the agent, the queue, or the operator retries it.

A failure is not proof that nothing happened. Only a decline the downstream
system actually sent releases the key. A timeout leaves the effect Unknown, and
nothing re-applies it until reconciliation settles the outcome. The example
omits Partial and compensation.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Callable, Literal

# --8<-- example:start

EffectState = Literal[
    "reserved", "executing", "committed", "declined", "unknown", "intervention_required"
]


class EffectConflict(Exception):
    """The logical key was reused with a different intent."""


class EffectOutcomeUnknown(Exception):
    """The effect may have happened; reconcile before anything retries it."""


class DownstreamDeclined(Exception):
    """The downstream system answered, and the answer proves no effect happened."""


@dataclass
class EffectRecord:
    intent_hash: str
    state: EffectState
    receipt: str | None = None
    evidence: str | None = None


def hash_intent(intent: dict[str, object]) -> str:
    payload = json.dumps(intent, sort_keys=True, separators=(",", ":"), default=str)
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()


@dataclass
class EffectLedger:
    """Reference implementation; production uses a transactional durable store."""

    _records: dict[str, EffectRecord] = field(default_factory=dict)

    def commit(self, key: str, intent: dict[str, object], apply: Callable[[], str]) -> str:
        digest = hash_intent(intent)
        record = self._records.get(key)
        if record is not None:
            # The intent hash is checked first, whatever the state: a declined
            # key is still this intent's key, and a new intent needs a new key.
            if record.intent_hash != digest:
                raise EffectConflict(f"{key} was reused with a different intent")
            if record.state == "committed":
                return record.receipt  # a replay returns the original receipt
            if record.state != "declined":
                raise EffectOutcomeUnknown(f"{key} is {record.state}; refusing to re-apply")
        # No record, or a decline that proved nothing happened: safe to apply.
        # Production writes "reserved" and "executing" durably before dispatch.
        record = self._records[key] = EffectRecord(digest, "reserved")
        record.state = "executing"
        try:
            receipt = apply()
        except DownstreamDeclined:
            record.state = "declined"
            raise
        except Exception as error:
            # A timeout or a lost connection proves nothing: the effect may have landed.
            record.state = "unknown"
            raise EffectOutcomeUnknown(f"{key} outcome is unknown") from error
        record.state, record.receipt = "committed", receipt
        return receipt

    def reconcile(
        self, key: str, *, outcome: Literal["committed", "absent", "unprovable"], evidence: str
    ) -> EffectRecord:
        """Settle an Unknown effect from downstream evidence, never from a guess."""
        record = self._records[key]
        if record.state != "unknown":
            raise EffectConflict(f"only an unknown effect is reconciled, not {record.state}")
        record.evidence = evidence
        if outcome == "committed":
            record.state, record.receipt = "committed", evidence
        elif outcome == "absent":
            record.state = "declined"
        else:
            record.state = "intervention_required"
        return record

    def get(self, key: str) -> EffectRecord:
        return self._records[key]


# --8<-- example:end
