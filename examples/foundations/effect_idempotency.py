"""Effect-level idempotency: making an at-least-once retry safe to repeat.

The book's position is that agentic systems cannot promise exactly-once
delivery, so they must make the *effect* idempotent instead. A logical effect
key identifies the intent; the ledger guarantees the intent commits once, even
if the agent, the queue, or the operator retries it.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# --8<-- example:start


class EffectOutcomeUnknown(Exception):
    """Raised when a dispatch timed out and the outcome cannot be proven."""


@dataclass
class EffectLedger:
    """Records the outcome of each logical effect exactly once."""

    _committed: dict[str, str] = field(default_factory=dict)
    _in_flight: set[str] = field(default_factory=set)

    def commit(self, effect_key: str, apply) -> str:
        # A replayed key returns the original receipt. The caller cannot tell
        # whether it won the race, and does not need to.
        if effect_key in self._committed:
            return self._committed[effect_key]
        if effect_key in self._in_flight:
            raise EffectOutcomeUnknown(f"{effect_key} is still in flight")
        self._in_flight.add(effect_key)
        try:
            receipt = apply()
        finally:
            self._in_flight.discard(effect_key)
        self._committed[effect_key] = receipt
        return receipt


# --8<-- example:end
