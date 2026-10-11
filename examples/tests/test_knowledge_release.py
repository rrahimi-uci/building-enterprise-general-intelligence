from __future__ import annotations

import copy
from decimal import Decimal

import pytest

from examples.knowledge.enforced_rule import (
    EnforcedRule, PinnedRelease, ReleaseNotEvaluable, rules_for,
)
from examples.knowledge.knowledge_release import (
    GATES, Approval, Candidate, Control, Gate, Obligation, PublishRefused, Registry,
    Requirement, discharges, promote, publish, resolve, rollback,
)
from examples.knowledge.policy_to_rule import Predicate, Rule, SourceRef

# Harborlight, synthetic: one requirement -> one obligation -> one control.
AGE_RULE = Rule(
    rule_id="r_pay_statement_age", modality="prohibition",
    conditions=(Predicate("pay_statement_age_days", ">", Decimal(30)),),
    outcome=Predicate("income_evidence_acceptable", "=", False),
    jurisdiction="US", responsible_party="evidence_review", effective_from="2026-10-01",
    source=SourceRef("upstream_base", "sec_3_1", 0, 80, "a" * 64),
)
OBJECTS = (
    Requirement("REQ-income-current", AGE_RULE.source),
    Obligation("OBL-income-evidence", "REQ-income-current", "underwriting", "US", "2026-10-01"),
    Control("CTL-age-window", "OBL-income-evidence", AGE_RULE.digest()),
)
STREAM = "mortgage-policy"


def candidate(target_live=None, **overrides) -> Candidate:
    values = dict(change_id="change/pay-statement-age-window", author="analyst.kim",
                  objects=OBJECTS, pinned_base="upstream-base@2026.08",
                  target_live=target_live, resolver_version="1.4.0")
    return Candidate(**(values | overrides))


def passing() -> list[Gate]:
    return [Gate(name, True) for name in GATES]


def approved(c: Candidate, approver="owner.okafor") -> Approval:
    return Approval(approver, c.digest())


def live(env="staging") -> tuple[Registry, str]:
    registry = Registry()
    first = candidate()
    publish(registry, STREAM, env, first, passing(), approved(first))
    return registry, first.digest()


def test_a_control_cites_the_obligation_and_requirement_it_discharges():
    obligation, requirement = discharges(OBJECTS[2], OBJECTS)
    assert obligation.obligation_id == "OBL-income-evidence"
    assert requirement.source.source_sha256 == "a" * 64
    with pytest.raises(StopIteration):
        discharges(Control("CTL-orphan", "OBL-missing", "0" * 64), OBJECTS)


def test_an_author_cannot_approve_their_own_change():
    c = candidate()
    with pytest.raises(PublishRefused):
        publish(Registry(), STREAM, "staging", c, passing(), approved(c, approver=c.author))


def test_approval_on_an_edited_candidate_is_invalid():
    c = candidate()
    edited = candidate(resolver_version="1.4.1")
    with pytest.raises(PublishRefused):
        publish(Registry(), STREAM, "staging", edited, passing(), approved(c))


def test_a_candidate_whose_target_moved_is_stale_and_refused():
    registry, _ = live()
    c = candidate(change_id="change/other", target_live=None)   # expected nothing live
    with pytest.raises(PublishRefused):
        publish(registry, STREAM, "staging", c, passing(), approved(c))


def test_a_failed_gate_leaves_the_old_release_live():
    registry, old = live()
    c = candidate(change_id="change/next", target_live=old)
    gates = passing()[:-1] + [Gate("staleness", False)]
    with pytest.raises(PublishRefused):
        publish(registry, STREAM, "staging", c, gates, approved(c))
    assert resolve(registry, STREAM, "staging") == old


def test_a_retry_with_the_same_attempt_digest_allocates_no_second_version():
    registry, old = live()
    c = candidate(change_id="change/next", target_live=old)
    first = publish(registry, STREAM, "staging", c, passing(), approved(c))
    again = publish(registry, STREAM, "staging", c, passing(), approved(c))
    assert first is again and first.version == 2 and len(registry.releases) == 2


def test_promotion_carries_the_identical_digest_or_refuses():
    registry, digest = live()
    assert promote(registry, STREAM, "staging", "production", expected=None) == digest
    assert resolve(registry, STREAM, "production") == resolve(registry, STREAM, "staging")
    registry.pointers[(STREAM, "production")] = "diverged"
    with pytest.raises(PublishRefused):
        promote(registry, STREAM, "staging", "production", expected=digest)


def test_rollback_moves_the_pointer_and_rewrites_nothing():
    registry, old = live("production")
    c = candidate(change_id="change/next", target_live=old)
    new = publish(registry, STREAM, "production", c, passing(), approved(c)).digest
    history = copy.deepcopy(registry.releases)
    rollback(registry, STREAM, "production", old)
    assert resolve(registry, STREAM, "production") == old
    assert registry.releases == history and new in registry.releases
    with pytest.raises(PublishRefused):
        rollback(registry, STREAM, "production", "not-a-release")


def test_the_runtime_cannot_resolve_a_draft():
    registry = Registry()
    draft = candidate()                       # submitted, never published
    with pytest.raises(LookupError):
        resolve(registry, STREAM, "production")
    pin = PinnedRelease(STREAM, draft.digest(), "draft", (EnforcedRule(AGE_RULE),))
    with pytest.raises(ReleaseNotEvaluable):
        rules_for({STREAM: pin}, STREAM)
