from __future__ import annotations

import pytest

from examples.foundations.effect_idempotency import EffectLedger, EffectOutcomeUnknown


def test_replayed_effect_key_commits_once():
    ledger = EffectLedger()
    calls = []

    def apply():
        calls.append(1)
        return "receipt-1"

    effect_key = "mortgage:document-request:MORT-2026-000184:employment_verification"
    assert ledger.commit(effect_key, apply) == "receipt-1"
    assert ledger.commit(effect_key, apply) == "receipt-1"
    assert len(calls) == 1, "a replayed logical effect must not apply twice"


def test_distinct_keys_are_independent():
    ledger = EffectLedger()
    assert ledger.commit("a", lambda: "ra") == "ra"
    assert ledger.commit("b", lambda: "rb") == "rb"


def test_failure_does_not_poison_the_key():
    ledger = EffectLedger()
    with pytest.raises(RuntimeError):
        ledger.commit("k", lambda: (_ for _ in ()).throw(RuntimeError("downstream 500")))
    # The key is retryable because the effect never committed.
    assert ledger.commit("k", lambda: "receipt") == "receipt"
