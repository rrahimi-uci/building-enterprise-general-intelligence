from __future__ import annotations

import pytest

from examples.knowledge.policy_to_rule import Predicate, Rule, SourceRef
from examples.knowledge.rule_as_guardrail import (
    Guardrail, PolicyViolation, UnknownUnderPolicy, guarded_dispatch,
)

RULE = Rule(
    rule_id="r_large_txn_approval", modality="obligation",
    conditions=(Predicate("transaction_amount", ">", 10000),),
    outcome=Predicate("approved_by_compliance", "=", True),
    jurisdiction="US", responsible_party="compliance_officer",
    effective_from="2026-01-01",
    source=SourceRef("aml_policy", "sec_4_2", 0, 85, "a" * 64),
)
GUARDS = [Guardrail(RULE)]


def transfer():
    return "transferred"


def test_a_compliant_effect_proceeds():
    facts = {"transaction_amount": 25000, "approved_by_compliance": True}
    assert guarded_dispatch(transfer, facts, GUARDS, jurisdiction="US", on_date="2026-06-01") == "transferred"


def test_an_unapproved_large_transfer_is_refused_before_it_runs():
    facts = {"transaction_amount": 25000, "approved_by_compliance": False}
    with pytest.raises(PolicyViolation) as caught:
        guarded_dispatch(transfer, facts, GUARDS, jurisdiction="US", on_date="2026-06-01")
    # The refusal names the rule and the policy section, so an operator can read
    # the sentence that refused them.
    assert caught.value.rule_id == "r_large_txn_approval"
    assert caught.value.source_section == "sec_4_2"


def test_a_small_transfer_is_untouched_because_the_rule_does_not_fire():
    facts = {"transaction_amount": 500, "approved_by_compliance": False}
    assert guarded_dispatch(transfer, facts, GUARDS, jurisdiction="US", on_date="2026-06-01") == "transferred"


def test_out_of_scope_jurisdiction_does_not_enforce_a_us_rule():
    facts = {"transaction_amount": 25000, "approved_by_compliance": False}
    assert guarded_dispatch(transfer, facts, GUARDS, jurisdiction="EU", on_date="2026-06-01") == "transferred"


def test_a_missing_fact_refuses_rather_than_permitting():
    # The most dangerous default in any policy engine is 'unknown means yes'.
    with pytest.raises(UnknownUnderPolicy):
        guarded_dispatch(transfer, {"approved_by_compliance": True}, GUARDS,
                         jurisdiction="US", on_date="2026-06-01")


def test_the_effect_never_runs_when_a_guardrail_refuses():
    ran = []
    facts = {"transaction_amount": 25000, "approved_by_compliance": False}
    with pytest.raises(PolicyViolation):
        guarded_dispatch(lambda: ran.append(1), facts, GUARDS,
                         jurisdiction="US", on_date="2026-06-01")
    assert ran == [], "enforcement must precede the effect, not report on it"
