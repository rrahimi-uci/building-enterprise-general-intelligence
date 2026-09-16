from __future__ import annotations

from decimal import Decimal

from examples.knowledge.policy_to_rule import Predicate, Rule, SourceRef

SENTENCE = "Mortgage cases with requested LTV above 80% require human underwriter approval before submission."
CORPUS = {"mortgage_underwriting_policy": f"4.2 Review thresholds. {SENTENCE}"}


def rule(**kw) -> Rule:
    start = CORPUS["mortgage_underwriting_policy"].index("Mortgage")
    base = dict(
        rule_id="r_high_ltv_review", modality="obligation",
        conditions=(Predicate("requested_ltv", ">", Decimal("0.80")),),
        outcome=Predicate("underwriter_approved", "=", True),
        jurisdiction="US", responsible_party="human_underwriter",
        effective_from="2026-01-01",
        source=SourceRef("mortgage_underwriting_policy", "sec_4_2", start,
                         start + len(SENTENCE), "a" * 64),
    )
    base.update(kw)
    return Rule(**base)


def test_the_rule_can_produce_the_sentence_it_came_from():
    # Provenance that cannot be resolved back to text is decoration.
    assert rule().source.excerpt(CORPUS) == SENTENCE


def test_scope_prevents_applying_a_rule_where_it_does_not_belong():
    r = rule()
    assert r.applies_in("US", "2026-06-01")
    assert not r.applies_in("EU", "2026-06-01"), "jurisdiction must bind"
    assert not r.applies_in("US", "2025-12-31"), "a rule cannot apply before it took effect"


def test_identity_is_by_content_so_two_extractions_agree():
    # Same sentence extracted twice under different ids is the same rule.
    assert rule().digest() == rule(rule_id="r_other").digest()


def test_a_different_threshold_is_a_different_rule():
    changed = rule(conditions=(Predicate("requested_ltv", ">", Decimal("0.90")),))
    assert changed.digest() != rule().digest()
