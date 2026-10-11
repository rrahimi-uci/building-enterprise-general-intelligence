from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from examples.knowledge.policy_to_rule import Predicate, Rule, SourceRef
from examples.knowledge.rule_as_guardrail import (
    EnforcedRule, PolicyViolation, UnknownUnderPolicy, guarded_dispatch,
)

RULE = Rule(
    rule_id="r_high_ltv_review", modality="obligation",
    conditions=(Predicate("requested_ltv", ">", Decimal("0.80")),),
    outcome=Predicate("underwriter_approved", "=", True),
    jurisdiction="US", responsible_party="human_underwriter",
    effective_from="2026-01-01",
    source=SourceRef("mortgage_underwriting_policy", "sec_4_2", 0, 100, "a" * 64),
)
GUARDS = [EnforcedRule(RULE)]


def submit_for_underwriting():
    return "submitted for human underwriting review"


def test_a_compliant_effect_proceeds():
    facts = {"requested_ltv": Decimal("0.85"), "underwriter_approved": True}
    assert guarded_dispatch(submit_for_underwriting, facts, GUARDS,
                            jurisdiction="US", on_date="2026-06-01") == "submitted for human underwriting review"


def test_an_unapproved_high_ltv_submission_is_refused_before_it_runs():
    facts = {"requested_ltv": Decimal("0.85"), "underwriter_approved": False}
    with pytest.raises(PolicyViolation) as caught:
        guarded_dispatch(submit_for_underwriting, facts, GUARDS,
                         jurisdiction="US", on_date="2026-06-01")
    # The refusal names the rule and the policy section, so an operator can read
    # the sentence that refused them.
    assert caught.value.rule_id == "r_high_ltv_review"
    assert caught.value.source_section == "sec_4_2"


def test_a_low_ltv_submission_is_untouched_because_the_rule_does_not_fire():
    facts = {"requested_ltv": Decimal("0.75"), "underwriter_approved": False}
    assert guarded_dispatch(submit_for_underwriting, facts, GUARDS,
                            jurisdiction="US", on_date="2026-06-01") == "submitted for human underwriting review"


def test_out_of_scope_jurisdiction_does_not_enforce_a_us_rule():
    facts = {"requested_ltv": Decimal("0.85"), "underwriter_approved": False}
    assert guarded_dispatch(submit_for_underwriting, facts, GUARDS,
                            jurisdiction="EU", on_date="2026-06-01") == "submitted for human underwriting review"


def test_a_missing_fact_refuses_rather_than_permitting():
    # The most dangerous default in any policy engine is 'unknown means yes'.
    with pytest.raises(UnknownUnderPolicy):
        guarded_dispatch(submit_for_underwriting, {"underwriter_approved": True}, GUARDS,
                         jurisdiction="US", on_date="2026-06-01")


def test_the_effect_never_runs_when_a_rule_refuses():
    ran = []
    facts = {"requested_ltv": Decimal("0.85"), "underwriter_approved": False}
    with pytest.raises(PolicyViolation):
        guarded_dispatch(lambda: ran.append(1), facts, GUARDS,
                         jurisdiction="US", on_date="2026-06-01")
    assert ran == [], "enforcement must precede the effect, not report on it"


# Where the two lanes meet: a rule extracted from policy prose, evaluated over a
# fact extracted from a document. The 60-day window is illustrative only.
AGE_WINDOW = Rule(
    rule_id="r_pay_statement_age", modality="prohibition",
    conditions=(Predicate("pay_statement_age_days", ">", 60),),
    outcome=Predicate("income_evidence_acceptable", "=", False),
    jurisdiction="US", responsible_party="evidence_review",
    effective_from="2026-01-01",
    source=SourceRef("mortgage_underwriting_policy", "sec_3_1", 0, 80, "a" * 64),
)


def _certified_statement(age_days: int, *, tampered: bool = False):
    from datetime import timedelta

    from examples.knowledge.document_ingestion import ExtractedField, verify_document
    from examples.tests.test_document_ingestion import CASE, TEXT, fields, record

    as_of = date(2026, 9, 5) + timedelta(days=age_days)
    age = ExtractedField("pay_statement_age_days", age_days, "days", "derived",
                         inputs=("pay_date",))
    derive = {"pay_statement_age_days": lambda v: (as_of - date.fromisoformat(v["pay_date"])).days}
    text = TEXT.replace("4,250.00", "5,250.00") if tampered else TEXT
    return verify_document(record(), fields(pay_statement_age_days=age), text,
                           case=CASE, derive=derive)


def test_the_age_window_reads_only_verified_document_facts():
    from examples.knowledge.document_ingestion import facts_for_rules

    accept = {"income_evidence_acceptable": True}  # what the agent proposes to record
    unverified = _certified_statement(15, tampered=True)  # never verified
    with pytest.raises(UnknownUnderPolicy):
        guarded_dispatch(lambda: "accepted", facts_for_rules(unverified) | accept,
                         [EnforcedRule(AGE_WINDOW)], jurisdiction="US", on_date="2026-09-20")
    with pytest.raises(PolicyViolation):
        guarded_dispatch(lambda: "accepted", facts_for_rules(_certified_statement(75)) | accept,
                         [EnforcedRule(AGE_WINDOW)], jurisdiction="US", on_date="2026-11-19")
    assert guarded_dispatch(lambda: "accepted", facts_for_rules(_certified_statement(15)) | accept,
                            [EnforcedRule(AGE_WINDOW)], jurisdiction="US",
                            on_date="2026-09-20") == "accepted"
