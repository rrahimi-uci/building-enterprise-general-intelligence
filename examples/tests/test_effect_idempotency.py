from __future__ import annotations

import pytest

from examples.foundations.effect_idempotency import (
    DownstreamDeclined, EffectConflict, EffectLedger, EffectOutcomeUnknown,
)

KEY = "mortgage:document-request:MORT-2026-000184:pay_statement"
INTENT = {"case_id": "MORT-2026-000184", "document_kind": "pay_statement"}


def raising(error: Exception):
    def apply():
        raise error
    return apply


def test_replayed_effect_key_commits_once():
    ledger = EffectLedger()
    calls = []

    def apply():
        calls.append(1)
        return "receipt-1"

    assert ledger.commit(KEY, INTENT, apply) == "receipt-1"
    assert ledger.commit(KEY, INTENT, apply) == "receipt-1"
    assert len(calls) == 1, "a replayed logical effect must not apply twice"


def test_distinct_keys_are_independent():
    ledger = EffectLedger()
    assert ledger.commit("a", INTENT, lambda: "ra") == "ra"
    assert ledger.commit("b", INTENT, lambda: "rb") == "rb"


def test_a_key_reused_with_a_different_intent_is_a_conflict():
    ledger = EffectLedger()
    ledger.commit(KEY, INTENT, lambda: "receipt-1")
    with pytest.raises(EffectConflict):
        ledger.commit(KEY, {**INTENT, "document_kind": "bank_statement"}, lambda: "receipt-2")


def test_a_received_decline_is_recorded_and_releases_the_key():
    ledger = EffectLedger()
    with pytest.raises(DownstreamDeclined):
        ledger.commit(KEY, INTENT, raising(DownstreamDeclined("422: case is locked")))
    assert ledger.get(KEY).state == "declined"
    # The decline proved nothing happened, so a later attempt may apply.
    assert ledger.commit(KEY, INTENT, lambda: "receipt") == "receipt"


def test_a_timeout_is_unknown_and_is_never_re_applied():
    ledger = EffectLedger()
    with pytest.raises(EffectOutcomeUnknown):
        ledger.commit(KEY, INTENT, raising(TimeoutError("no response in 30s")))
    assert ledger.get(KEY).state == "unknown"
    calls = []
    with pytest.raises(EffectOutcomeUnknown):
        ledger.commit(KEY, INTENT, lambda: calls.append(1) or "receipt")
    assert calls == [], "an unknown effect must be reconciled, not retried"


def test_reconciliation_settles_an_unknown_effect_from_evidence():
    ledger = EffectLedger()
    for key in ("found", "absent", "unclear"):
        with pytest.raises(EffectOutcomeUnknown):
            ledger.commit(key, INTENT, raising(TimeoutError()))

    ledger.reconcile("found", outcome="committed", evidence="doc-request-771")
    assert ledger.commit("found", INTENT, lambda: "duplicate") == "doc-request-771"

    ledger.reconcile("absent", outcome="absent", evidence="no request in window")
    assert ledger.commit("absent", INTENT, lambda: "receipt") == "receipt"

    ledger.reconcile("unclear", outcome="unprovable", evidence="two candidate matches")
    assert ledger.get("unclear").state == "intervention_required"
    with pytest.raises(EffectOutcomeUnknown):
        ledger.commit("unclear", INTENT, lambda: "receipt")
