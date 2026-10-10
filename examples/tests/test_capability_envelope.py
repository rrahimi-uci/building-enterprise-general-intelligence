from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from examples.contracts import RiskClass
from examples.security.capability_envelope import CapabilityEnvelope, derive_child

NOW = datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc)

PARENT = CapabilityEnvelope(
    grant_id="grant-run-98217",
    subject_id="loan-officer-17",
    actor_id="mortgage-evidence-agent@0.1.0",
    actions=frozenset({"mortgage.case.read", "mortgage.document.request"}),
    resource_prefixes=frozenset({"mortgage://cases/MORT-2026-000184"}),
    purposes=frozenset({"prepare-mortgage-evidence"}),
    data_classes=frozenset({"income", "identity"}),
    regions=frozenset({"us-east"}),
    maximum_risk=RiskClass.R3,
    maximum_cost_usd=Decimal("5.00"),
    delegation_depth=2,
    expires_at=NOW + timedelta(hours=1),
)

# A read-only specialist: a different actor, narrower on every dimension.
CHILD = replace(
    PARENT,
    grant_id="grant-child-1",
    actor_id="tax-fields-specialist@0.3.0",
    actions=frozenset({"mortgage.case.read"}),
    resource_prefixes=frozenset({"mortgage://cases/MORT-2026-000184/documents"}),
    data_classes=frozenset({"income"}),
    maximum_risk=RiskClass.R1,
    maximum_cost_usd=Decimal("1.00"),
    delegation_depth=1,
    expires_at=NOW + timedelta(minutes=15),
)


def test_a_narrower_child_with_a_new_actor_is_accepted():
    assert derive_child(PARENT, CHILD, now=NOW) is CHILD


@pytest.mark.parametrize(
    ("change", "reason"),
    [
        ({"subject_id": "underwriter-3"}, "subject cannot change"),
        ({"actions": CHILD.actions | {"mortgage.case.update"}}, "actions broadened"),
        ({"purposes": frozenset({"marketing"})}, "purposes broadened"),
        ({"data_classes": frozenset({"income", "bank"})}, "data classes broadened"),
        ({"regions": frozenset({"eu-west"})}, "regions broadened"),
        ({"maximum_risk": RiskClass.R4}, "risk ceiling raised"),
        ({"maximum_cost_usd": Decimal("5.01")}, "cost ceiling raised"),
        ({"delegation_depth": 2}, "delegation depth was not reduced"),
        ({"expires_at": NOW + timedelta(hours=2)}, "lifetime extended"),
        (
            {"resource_prefixes": frozenset({"mortgage://cases/MORT-2026-000999"})},
            "resource scope broadened",
        ),
    ],
)
def test_every_broadening_is_refused(change, reason):
    with pytest.raises(PermissionError, match=reason):
        derive_child(PARENT, replace(CHILD, **change), now=NOW)


def test_a_sibling_prefix_is_not_inside_the_parent_resource():
    # "...000184-old" shares a string prefix but is a different resource.
    sibling = replace(
        CHILD, resource_prefixes=frozenset({"mortgage://cases/MORT-2026-000184-old"})
    )
    with pytest.raises(PermissionError, match="resource scope broadened"):
        derive_child(PARENT, sibling, now=NOW)


def test_an_expired_parent_cannot_delegate():
    with pytest.raises(PermissionError, match="expired"):
        derive_child(PARENT, CHILD, now=NOW + timedelta(hours=1))
