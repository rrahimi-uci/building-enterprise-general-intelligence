"""Compilation binds a plan to its envelope, or refuses it."""
from __future__ import annotations

import pytest
from decimal import Decimal

from examples.contracts import CandidatePlan, PlanNode, RiskClass
from examples.patterns.plan_compilation import PlanEnvelope, compile_plan

DIGEST = "sha256:" + "a" * 64


def node(node_id="n1", capability="mortgage.case.read", cost=Decimal("0.25"), risk=RiskClass.R1, deps=()):
    return PlanNode(id=node_id, capability=capability, maximum_cost_usd=cost,
                    maximum_attempts=2, risk_class=risk, depends_on=tuple(deps))


def envelope(**kw):
    base = dict(allowed_capabilities=frozenset({"mortgage.case.read", "mortgage.evidence.verify"}),
                maximum_cost_usd=Decimal("1.0"), policy_digest=DIGEST,
                maximum_nodes=5, maximum_risk=RiskClass.R2)
    base.update(kw)
    return PlanEnvelope(**base)


def plan(*nodes):
    return CandidatePlan(revision=1, nodes=tuple(nodes))


def test_a_conforming_plan_compiles_and_is_bound_to_the_policy():
    compiled = compile_plan(plan(node()), envelope())
    # The digest is what proves the executed plan is the validated plan.
    assert compiled["compiled_plan_digest"].startswith("sha256:")


def test_float_budget_is_rejected_at_the_compilation_boundary():
    with pytest.raises(TypeError, match="must be Decimal"):
        envelope(maximum_cost_usd=1.0)


def test_capability_outside_the_envelope_is_refused():
    with pytest.raises(PermissionError, match="capability not allowed"):
        compile_plan(plan(node(capability="mortgage.los.write")), envelope())


def test_risk_ceiling_is_enforced_per_node():
    with pytest.raises(PermissionError, match="risk ceiling"):
        compile_plan(plan(node(risk=RiskClass.R4)), envelope())


def test_envelope_risk_is_a_risk_class_not_a_number():
    with pytest.raises(TypeError, match="RiskClass"):
        envelope(maximum_risk=2)


def test_total_reserved_cost_cannot_exceed_the_grant():
    with pytest.raises(ValueError, match="maximum cost"):
        compile_plan(
            plan(node("n1", cost=Decimal("0.8")), node("n2", cost=Decimal("0.8"))),
            envelope(),
        )


def test_duplicate_node_ids_are_refused():
    with pytest.raises(ValueError, match="duplicate node ID"):
        compile_plan(plan(node("n1"), node("n1")), envelope())


def test_dangling_dependency_is_refused():
    with pytest.raises(ValueError, match="unknown dependencies"):
        compile_plan(plan(node("n1", deps=("missing",))), envelope())


def test_node_limit_is_enforced():
    with pytest.raises(ValueError, match="node limit"):
        compile_plan(
            plan(*[node(f"n{i}", cost=Decimal("0.05")) for i in range(6)]),
            envelope(),
        )
