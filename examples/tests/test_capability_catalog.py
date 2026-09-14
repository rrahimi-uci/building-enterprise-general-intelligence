from __future__ import annotations

import pytest

from examples.knowledge.capability_catalog import (
    Capability, CapabilityCatalog, CapabilityUnavailable,
)


def catalog() -> CapabilityCatalog:
    c = CapabilityCatalog()
    c.register(Capability("supplier.read", "1.0.0", "Read a supplier record",
                          effect="read", required_action="supplier:read"))
    c.register(Capability("supplier.update", "1.2.0", "Update a supplier record",
                          effect="write", required_action="supplier:write",
                          prerequisites=("approval.granted",), idempotent=True))
    c.register(Capability("payment.release", "2.0.0", "Release a payment",
                          effect="irreversible", required_action="payment:release",
                          prerequisites=("approval.granted", "sanctions.cleared"),
                          data_classes=frozenset({"financial"})))
    return c


def test_a_read_intent_never_surfaces_a_mutating_capability():
    found = catalog().discover(
        intent_effect="read", granted_actions=frozenset({"supplier:read", "supplier:write"}),
        satisfied=frozenset({"approval.granted"}), permitted_data=frozenset({"financial"}))
    assert [c.capability_id for c in found] == ["supplier.read"]


def test_an_ungranted_action_is_not_discoverable():
    found = catalog().discover(
        intent_effect="write", granted_actions=frozenset({"supplier:read"}),
        satisfied=frozenset({"approval.granted"}), permitted_data=frozenset())
    assert found == [], "a listed-but-forbidden tool is an invitation to try"


def test_an_unmet_prerequisite_hides_the_capability():
    found = catalog().discover(
        intent_effect="write", granted_actions=frozenset({"supplier:write"}),
        satisfied=frozenset(), permitted_data=frozenset())
    assert found == []


def test_a_data_class_the_caller_may_not_touch_excludes_the_capability():
    found = catalog().discover(
        intent_effect="irreversible", granted_actions=frozenset({"payment:release"}),
        satisfied=frozenset({"approval.granted", "sanctions.cleared"}),
        permitted_data=frozenset())        # no 'financial' permission
    assert found == []


def test_everything_satisfied_makes_the_irreversible_capability_available():
    found = catalog().discover(
        intent_effect="irreversible", granted_actions=frozenset({"payment:release"}),
        satisfied=frozenset({"approval.granted", "sanctions.cleared"}),
        permitted_data=frozenset({"financial"}))
    assert [c.capability_id for c in found] == ["payment.release"]


def test_selecting_with_nothing_eligible_raises_rather_than_guessing():
    with pytest.raises(CapabilityUnavailable):
        catalog().select(intent_effect="write", granted_actions=frozenset(),
                         satisfied=frozenset(), permitted_data=frozenset())
