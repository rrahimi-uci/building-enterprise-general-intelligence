"""Compiling a validated plan into an executable, budget-bounded envelope.

A plan is data before it is behaviour. Compiling it fixes the budgets, the
eligible tool versions, and a digest of exactly what was validated, so the thing
that executes is provably the thing the compiler validated.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from decimal import Decimal

from examples.contracts import CandidatePlan, RiskClass


_SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class PlanEnvelope:
    """Deterministic limits used to compile one candidate plan."""

    allowed_capabilities: frozenset[str]
    maximum_cost_usd: Decimal
    policy_digest: str
    maximum_nodes: int = 100
    maximum_risk: RiskClass = RiskClass.R4

    def __post_init__(self) -> None:
        if not isinstance(self.maximum_cost_usd, Decimal):
            raise TypeError("maximum_cost_usd must be Decimal")
        if not self.maximum_cost_usd.is_finite() or self.maximum_cost_usd < 0:
            raise ValueError("maximum_cost_usd must be finite and non-negative")
        if self.maximum_nodes < 1:
            raise ValueError("maximum_nodes must be positive")
        if not isinstance(self.maximum_risk, RiskClass):
            raise TypeError("maximum_risk must be a RiskClass (R0-R4)")
        if _SHA256.fullmatch(self.policy_digest) is None:
            raise ValueError("policy_digest must be a canonical sha256 digest")


def _sha256(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


# --8<-- region:core
def compile_plan(plan: CandidatePlan, envelope: PlanEnvelope) -> dict[str, object]:
    """Validate and bind a proposed plan to the policy envelope.

    Node maximum_cost_usd values are conservative reservations. Their sum is
    the compiled reservation even if runtime branches may be mutually exclusive.
    Actual spend is tracked separately and can never consume beyond the run grant.
    """

    if len(plan.nodes) > envelope.maximum_nodes:
        raise ValueError("node limit exceeded")
    by_id = {node.id: node for node in plan.nodes}
    if len(by_id) != len(plan.nodes):
        raise ValueError("duplicate node ID")

    for node in plan.nodes:
        if node.capability not in envelope.allowed_capabilities:
            raise PermissionError(f"capability not allowed: {node.capability}")
        if node.risk_class > envelope.maximum_risk:
            raise PermissionError(f"risk ceiling exceeded: {node.id}")
        unknown = set(node.depends_on) - by_id.keys()
        if unknown:
            raise ValueError(f"unknown dependencies for {node.id}: {sorted(unknown)}")

    reserved_cost = sum(
        (node.maximum_cost_usd for node in plan.nodes), Decimal("0")
    )
    if not reserved_cost.is_finite() or reserved_cost > envelope.maximum_cost_usd:
        raise ValueError("plan exceeds maximum cost")

    dependencies = {node.id: set(node.depends_on) for node in plan.nodes}
    ready = sorted(node_id for node_id, deps in dependencies.items() if not deps)
    order: list[str] = []
    while ready:
        current = ready.pop(0)
        order.append(current)
        for node_id, deps in dependencies.items():
            if current in deps:
                deps.remove(current)
                if not deps and node_id not in order and node_id not in ready:
                    ready.append(node_id)
        ready.sort()
    if len(order) != len(plan.nodes):
        raise ValueError("cycle detected")

    plan_payload = plan.model_dump(mode="json")
    envelope_payload = {
        "allowed_capabilities": sorted(envelope.allowed_capabilities),
        "maximum_cost_usd": str(envelope.maximum_cost_usd),
        "maximum_nodes": envelope.maximum_nodes,
        "maximum_risk": envelope.maximum_risk.name,
        "policy_digest": envelope.policy_digest,
    }
    return {
        "revision": plan.revision,
        "topological_order": tuple(order),
        "reserved_cost_usd": reserved_cost,
        "cost_semantics": "sum_of_per_node_maximum_reservations",
        "policy_digest": envelope.policy_digest,
        "plan_digest": _sha256(plan_payload),
        "compiled_plan_digest": _sha256(
            {"plan": plan_payload, "envelope": envelope_payload}
        ),
    }

# --8<-- endregion:core
