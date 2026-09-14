"""Discovering what an agent may do, with the consequences attached.

A tool list tells an agent what exists. A capability catalog tells it what an
action *costs*: whether it mutates, what it needs first, who may invoke it, and
what happens if it is retried. Selecting on names alone is how an agent picks a
mutating endpoint for a read-only question.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# --8<-- example:start

Effect = Literal["read", "write", "irreversible"]


@dataclass(frozen=True)
class Capability:
    capability_id: str
    version: str
    description: str
    effect: Effect
    required_action: str
    prerequisites: tuple[str, ...] = field(default_factory=tuple)
    idempotent: bool = False
    data_classes: frozenset[str] = frozenset()


class CapabilityUnavailable(Exception):
    """No capability satisfies the request under the caller's grant."""


@dataclass
class CapabilityCatalog:
    capabilities: dict[str, Capability] = field(default_factory=dict)

    def register(self, capability: Capability) -> None:
        self.capabilities[capability.capability_id] = capability

    def discover(self, *, intent_effect: Effect, granted_actions: frozenset[str],
                 satisfied: frozenset[str], permitted_data: frozenset[str]) -> list[Capability]:
        """Everything the caller may actually invoke right now.

        Four filters, and the order matters: an agent should never see a
        capability it cannot use, because a listed-but-forbidden tool is an
        invitation to try.
        """
        eligible = []
        for capability in self.capabilities.values():
            if capability.effect != intent_effect:
                continue
            if capability.required_action not in granted_actions:
                continue
            if not set(capability.prerequisites) <= satisfied:
                continue
            if not capability.data_classes <= permitted_data:
                continue
            eligible.append(capability)
        # Reversible first: when two capabilities both satisfy the intent, the
        # one that can be undone is the safer default.
        order = {"read": 0, "write": 1, "irreversible": 2}
        return sorted(eligible, key=lambda c: (order[c.effect], not c.idempotent, c.capability_id))

    def select(self, **kwargs) -> Capability:
        found = self.discover(**kwargs)
        if not found:
            raise CapabilityUnavailable("no capability satisfies this request under the caller's grant")
        return found[0]


# --8<-- example:end
