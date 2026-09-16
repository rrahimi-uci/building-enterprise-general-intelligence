from __future__ import annotations

import pytest

from examples.knowledge.capability_catalog import (
    Capability, CapabilityCatalog, CapabilityUnavailable,
)


def catalog() -> CapabilityCatalog:
    c = CapabilityCatalog()
    c.register(Capability("mortgage.case.read", "1.0.0", "Read a mortgage case",
                          effect="read", required_action="mortgage:case:read"))
    c.register(Capability("mortgage.document.request", "1.2.0",
                          "Request missing mortgage evidence",
                          effect="write", required_action="mortgage:evidence_request",
                          prerequisites=("approval.granted",), idempotent=True))
    c.register(Capability("mortgage.review.submit", "2.0.0",
                          "Submit a mortgage evidence package for human underwriting review",
                          effect="irreversible", required_action="mortgage:review:submit",
                          prerequisites=("approval.granted", "evidence.complete"),
                          data_classes=frozenset({"financial"})))
    return c


def test_a_read_intent_never_surfaces_a_mutating_capability():
    found = catalog().discover(
        intent_effect="read", granted_actions=frozenset({"mortgage:case:read", "mortgage:evidence_request"}),
        satisfied=frozenset({"approval.granted"}), permitted_data=frozenset({"financial"}))
    assert [c.capability_id for c in found] == ["mortgage.case.read"]


def test_an_ungranted_action_is_not_discoverable():
    found = catalog().discover(
        intent_effect="write", granted_actions=frozenset({"mortgage:case:read"}),
        satisfied=frozenset({"approval.granted"}), permitted_data=frozenset())
    assert found == [], "a listed-but-forbidden tool is an invitation to try"


def test_an_unmet_prerequisite_hides_the_capability():
    found = catalog().discover(
        intent_effect="write", granted_actions=frozenset({"mortgage:evidence_request"}),
        satisfied=frozenset(), permitted_data=frozenset())
    assert found == []


def test_a_data_class_the_caller_may_not_touch_excludes_the_capability():
    found = catalog().discover(
        intent_effect="irreversible", granted_actions=frozenset({"mortgage:review:submit"}),
        satisfied=frozenset({"approval.granted", "evidence.complete"}),
        permitted_data=frozenset())        # no 'financial' permission
    assert found == []


def test_everything_satisfied_makes_the_irreversible_capability_available():
    found = catalog().discover(
        intent_effect="irreversible", granted_actions=frozenset({"mortgage:review:submit"}),
        satisfied=frozenset({"approval.granted", "evidence.complete"}),
        permitted_data=frozenset({"financial"}))
    assert [c.capability_id for c in found] == ["mortgage.review.submit"]


def test_selecting_with_nothing_eligible_raises_rather_than_guessing():
    with pytest.raises(CapabilityUnavailable):
        catalog().select(intent_effect="write", granted_actions=frozenset(),
                         satisfied=frozenset(), permitted_data=frozenset())
