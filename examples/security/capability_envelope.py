"""Capability-envelope subset proof: a child grant can only narrow its parent.

A capability envelope states the maximum scope a run or child task may use. A
child envelope is accepted only when it is a provable subset of its parent on
every dimension: same subject, no new actions, resources, purposes, data
classes, or regions, no higher risk class or cost ceiling, strictly less
delegation depth, and no longer lifetime. The actor may change; the subject may
not. Explicit denies and the parent grant ID live on the full record and are
omitted here.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from examples.contracts import RiskClass

# --8<-- example:start


def _resource_within(child: str, parent: str) -> bool:
    if parent.endswith("://"):
        return child.startswith(parent)
    normalized = parent.rstrip("/")
    return child == normalized or child.startswith(normalized + "/")


@dataclass(frozen=True)
class CapabilityEnvelope:
    grant_id: str
    subject_id: str
    actor_id: str
    actions: frozenset[str]
    resource_prefixes: frozenset[str]
    purposes: frozenset[str]
    data_classes: frozenset[str]
    regions: frozenset[str]
    maximum_risk: RiskClass  # effect risk class R0-R4 (Chapter 22)
    maximum_cost_usd: Decimal
    delegation_depth: int
    expires_at: datetime

    def assert_current(self, now: datetime | None = None) -> None:
        current = now or datetime.now(timezone.utc)
        if self.expires_at <= current:
            raise PermissionError("capability envelope expired")


def derive_child(
    parent: CapabilityEnvelope,
    child: CapabilityEnvelope,
    *,
    now: datetime | None = None,
) -> CapabilityEnvelope:
    """Prove monotonic narrowing; actor identity may change, subject may not."""

    parent.assert_current(now)
    if child.subject_id != parent.subject_id:
        raise PermissionError("subject cannot change")
    if not child.actions <= parent.actions:
        raise PermissionError("actions broadened")
    if not child.purposes <= parent.purposes:
        raise PermissionError("purposes broadened")
    if not child.data_classes <= parent.data_classes:
        raise PermissionError("data classes broadened")
    if not child.regions <= parent.regions:
        raise PermissionError("regions broadened")
    if child.maximum_risk > parent.maximum_risk:
        raise PermissionError("risk ceiling raised")
    if child.maximum_cost_usd > parent.maximum_cost_usd:
        raise PermissionError("cost ceiling raised")
    if child.delegation_depth >= parent.delegation_depth:
        raise PermissionError("delegation depth was not reduced")
    if child.expires_at > parent.expires_at:
        raise PermissionError("lifetime extended")
    for resource in child.resource_prefixes:
        if not any(_resource_within(resource, allowed) for allowed in parent.resource_prefixes):
            raise PermissionError("resource scope broadened")
    return child


# --8<-- example:end
