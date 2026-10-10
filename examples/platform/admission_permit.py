"""Admit work against scarce capacity: grant, defer, or reject -- never just fail.

Mirrors the `quotas:acquire` contract in Chapter 28. A request that fits current
capacity is granted. One that fits the hard limit but not current capacity is
deferred until capacity refills, provided that still meets its deadline. One
that can never fit, or would miss its deadline by waiting, is rejected so the
caller can choose a draft or degraded path. A tenant or workload-class mismatch
is an authorization error, not a capacity shortfall.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


# --8<-- example:start
@dataclass(frozen=True)
class CapacityPermit:
    tenant_id: str
    workload_class: str
    model_tokens: int
    tool_calls: int
    sandbox_seconds: int


@dataclass(frozen=True)
class AdmissionDecision:
    disposition: Literal["granted", "defer_until", "rejected"]
    permit: CapacityPermit | None = None
    retry_after: datetime | None = None
    reason: str | None = None


RESOURCES = ("model_tokens", "tool_calls", "sandbox_seconds")


def _shortfall(requested: CapacityPermit, limit: CapacityPermit) -> list[str]:
    return [r for r in RESOURCES if getattr(requested, r) > getattr(limit, r)]


def admit(requested: CapacityPermit, available: CapacityPermit,
          hard_limit: CapacityPermit, *, refill_at: datetime,
          deadline: datetime) -> AdmissionDecision:
    for scope in (available, hard_limit):
        if (requested.tenant_id, requested.workload_class) != (
                scope.tenant_id, scope.workload_class):
            raise PermissionError("permit tenant or workload class mismatch")
    if over := _shortfall(requested, hard_limit):
        return AdmissionDecision("rejected", reason="hard limit: " + ", ".join(over))
    if not _shortfall(requested, available):
        return AdmissionDecision("granted", permit=requested)
    if refill_at <= deadline:
        return AdmissionDecision("defer_until", retry_after=refill_at)
    return AdmissionDecision("rejected", reason="waiting would miss the deadline")
# --8<-- example:end
