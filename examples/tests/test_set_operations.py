from __future__ import annotations

from decimal import Decimal

from examples.knowledge.policy_to_rule import Predicate, Rule, SourceRef
from examples.knowledge.set_operations import (
    contradictions, difference, intersection, union,
)

REF = SourceRef("doc", "sec", 0, 10, "a" * 64)


def rule(rid, *, ltv=Decimal("0.80"), outcome=True, modality="obligation",
         var="underwriter_approved"):
    return Rule(rule_id=rid, modality=modality,
                conditions=(Predicate("requested_ltv", ">", ltv),),
                outcome=Predicate(var, "=", outcome), jurisdiction="US",
                responsible_party="human_underwriter", effective_from="2026-01-01",
                source=REF)


def test_union_keeps_every_source_that_asserts_a_rule():
    g1 = {"regulator": [rule("REG-1")]}
    g2 = {"internal": [rule("INT-7")]}
    merged = union(g1, g2)
    assert len(merged) == 1, "one rule asserted twice is still one rule"
    entry = merged[0]
    assert set(entry.sources) == {"regulator", "internal"}
    # The original identifiers survive, which is what makes a later conflict
    # resolvable back to the document each side came from.
    assert entry.original_ids == {"regulator": "REG-1", "internal": "INT-7"}


def test_union_is_commutative_in_content():
    g1 = {"a": [rule("A1"), rule("A2", ltv=Decimal("0.90"))]}
    g2 = {"b": [rule("B1")]}
    assert {r.rule.digest() for r in union(g1, g2)} == {r.rule.digest() for r in union(g2, g1)}


def test_intersection_is_only_what_both_sides_assert():
    g1 = {"a": [rule("A1"), rule("A2", ltv=Decimal("0.90"))]}
    g2 = {"b": [rule("B1")]}
    shared = intersection(g1, g2)
    assert len(shared) == 1
    assert shared[0].rule.conditions[0].value == Decimal("0.80")


def test_difference_is_directional():
    g1 = {"a": [rule("A1"), rule("A2", ltv=Decimal("0.90"))]}
    g2 = {"b": [rule("B1")]}
    assert len(difference(g1, g2)) == 1
    assert difference(g2, g1) == []


def test_a_clash_on_the_same_subject_is_reported_with_both_sides():
    g1 = {"regulator": [rule("REG-1", outcome=True)]}
    g2 = {"internal": [rule("INT-1", outcome=False)]}
    found = contradictions(g1, g2)
    assert len(found) == 1
    clash = found[0]
    # Neither side is discarded, and the reason names both requirements.
    assert clash.left.rule_id == "REG-1" and clash.right.rule_id == "INT-1"
    assert "regulator requires" in clash.reason and "internal requires" in clash.reason


def test_rules_about_different_subjects_do_not_contradict():
    g1 = {"a": [rule("A1", var="underwriter_approved")]}
    g2 = {"b": [rule("B1", var="evidence_logged", outcome=False)]}
    assert contradictions(g1, g2) == []


def test_a_contradiction_is_not_silently_folded_into_the_union():
    g1 = {"regulator": [rule("REG-1", outcome=True)]}
    g2 = {"internal": [rule("INT-1", outcome=False)]}
    # Both survive the union as distinct rules; union never adjudicates.
    assert len(union(g1, g2)) == 2
    assert len(contradictions(g1, g2)) == 1
