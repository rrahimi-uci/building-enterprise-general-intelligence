"""AP-04: retries at every layer versus one retry owner with a shared budget.

Retries compose multiplicatively. Three layers at 3, 3, and 2 attempts make
eighteen calls for one logical operation, exactly when the dependency is already
degraded. The correction gives one owner the retry decision, chosen by failure
class, and draws every attempt from a budget no layer can reset.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

Call = Callable[[], str]


class TransientError(Exception):
    """Worth retrying: throttling, a dropped connection before dispatch."""


class PermanentError(Exception):
    """Retrying cannot help: validation failure, permission denied."""


class OutcomeUnknown(Exception):
    """A mutation may have landed; reconcile, never retry (AP-05)."""


def with_retries(call: Call, attempts: int) -> Call:
    """A layer that is 'resilient' on its own terms."""
    def wrapped() -> str:
        for attempt in range(attempts):
            try:
                return call()
            except TransientError:
                if attempt == attempts - 1:
                    raise
        raise AssertionError("unreachable")
    return wrapped


# --8<-- example:start
@dataclass
class AttemptBudget:
    remaining: int                 # shared by the run, decreasing, never reset

    def take(self) -> bool:
        if self.remaining <= 0:
            return False
        self.remaining -= 1
        return True


# Anti-pattern: each layer is independently "resilient". 3 x 3 x 2 = 18.
def build_naive(transport: Call) -> Call:
    client = with_retries(transport, attempts=3)
    gateway = with_retries(client, attempts=3)
    return with_retries(gateway, attempts=2)          # the workflow layer


# Correction: transport and gateway never retry. One owner retries transient
# failures only, from the run's budget; permanent fails fast, unknown reconciles.
def build_governed(transport: Call, budget: AttemptBudget) -> Call:
    def owner() -> str:
        last: Exception | None = None
        while budget.take():
            try:
                return transport()
            except TransientError as error:           # PermanentError and
                last = error                          # OutcomeUnknown propagate
        raise last or TransientError("attempt budget exhausted")
    return owner
# --8<-- example:end
