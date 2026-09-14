from __future__ import annotations

from examples.knowledge.policy_to_rule import Predicate, Rule, SourceRef

SENTENCE = "Transactions exceeding $10,000 require compliance officer approval before processing."
CORPUS = {"aml_policy": f"4.2 Approval thresholds. {SENTENCE}"}


def rule(**kw) -> Rule:
    start = CORPUS["aml_policy"].index("Transactions")
    base = dict(
        rule_id="r_large_txn_approval", modality="obligation",
        conditions=(Predicate("transaction_amount", ">", 10000),),
        outcome=Predicate("requires_approval", "=", True),
        jurisdiction="US", responsible_party="compliance_officer",
        effective_from="2026-01-01",
        source=SourceRef("aml_policy", "sec_4_2", start, start + len(SENTENCE), "a" * 64),
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
    changed = rule(conditions=(Predicate("transaction_amount", ">", 25000),))
    assert changed.digest() != rule().digest()
