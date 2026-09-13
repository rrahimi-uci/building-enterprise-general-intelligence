"""Run state must be a pure fold over events, so replay equals resume."""
from __future__ import annotations

import pytest

from examples.runtime.durable_state import RunState, WorkflowEvent, evolve, replay


def ev(kind, version, **data):
    return WorkflowEvent(kind=kind, data=data, expected_state_version=version)


AUTHORIZED = [ev("RunAuthorized", 0, start_node="n1"),
              ev("ActivityCompleted", 1, next_node="n2")]


def test_replay_of_a_history_equals_folding_it_step_by_step():
    state = RunState()
    for e in AUTHORIZED:
        state = evolve(state, e)
    assert replay(AUTHORIZED) == state, "replay and resume must not diverge"


def test_a_stale_event_is_rejected_rather_than_applied():
    state = evolve(RunState(), ev("RunAuthorized", 0, start_node="n1"))
    with pytest.raises(ValueError, match="stale"):
        evolve(state, ev("ActivityCompleted", 0, next_node="n2"))  # version already consumed


def test_a_run_cannot_succeed_with_an_unknown_effect_outstanding():
    state = replay([ev("RunAuthorized", 0, start_node="n1"),
                    ev("EffectUnknown", 1, effect_id="e-1")])
    with pytest.raises(ValueError, match="unknown effects"):
        evolve(state, ev("RunSucceeded", 2))


def test_reconciling_the_effect_unblocks_success():
    history = [
        ev("RunAuthorized", 0, start_node="n1"),
        ev("EffectUnknown", 1, effect_id="e-1"),
        ev("EffectReconciled", 2, effect_id="e-1"),
        ev("RunSucceeded", 3),
    ]
    assert replay(history).status == "succeeded"


def test_a_terminal_run_refuses_further_transitions():
    state = replay([ev("RunAuthorized", 0, start_node="n1"),
                    ev("RunFailed", 1, reason="downstream")])
    with pytest.raises(ValueError, match="terminal"):
        evolve(state, ev("ActivityCompleted", 2, next_node="n3"))
