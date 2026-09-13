"""Durable run state as an event fold, so a run can be replayed, not just resumed.

The book argues that transcripts are not durable state. This models the run as
an ordered event history with a pure fold, which makes replay, partial resume,
and audit the same operation instead of three special cases.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

RunStatus = Literal["submitted", "running", "waiting", "needs_approval",
                    "succeeded", "failed", "canceled", "intervention_required"]
TERMINAL = frozenset({"succeeded", "failed", "canceled", "intervention_required"})

@dataclass(frozen=True)
class RunState:
    status: RunStatus = "submitted"
    state_version: int = 0
    current_node: str | None = None
    cancel_requested: bool = False
    unknown_effect_ids: tuple[str, ...] = ()
    terminal_reason: str | None = None

@dataclass(frozen=True)
class WorkflowEvent:
    kind: str
    data: dict[str, object]
    expected_state_version: int | None = None


# --8<-- region:core
def evolve(state: RunState, event: WorkflowEvent) -> RunState:
    if event.expected_state_version is not None and event.expected_state_version != state.state_version:
        raise ValueError("stale workflow event")
    if state.status in TERMINAL:
        raise ValueError("terminal workflow cannot transition")
    version = state.state_version + 1
    if event.kind == "RunAuthorized" and state.status == "submitted":
        start = str(event.data["start_node"])
        return replace(state, status="running", current_node=start, state_version=version)
    if event.kind == "ActivityCompleted" and state.status == "running":
        return replace(state, current_node=str(event.data["next_node"]), state_version=version)
    if event.kind == "WaitStarted" and state.status == "running":
        return replace(state, status="waiting", state_version=version)
    if event.kind == "WaitSatisfied" and state.status == "waiting":
        return replace(state, status="running", state_version=version)
    if event.kind == "ApprovalRequired" and state.status == "running":
        return replace(state, status="needs_approval", state_version=version)
    if event.kind == "ApprovalReceived" and state.status == "needs_approval":
        return replace(state, status="running", state_version=version)
    if event.kind == "EffectUnknown":
        effect_id = str(event.data["effect_id"])
        if effect_id in state.unknown_effect_ids:
            return replace(state, state_version=version)
        return replace(state, unknown_effect_ids=state.unknown_effect_ids + (effect_id,), state_version=version)
    if event.kind == "EffectReconciled":
        effect_id = str(event.data["effect_id"])
        return replace(state, unknown_effect_ids=tuple(e for e in state.unknown_effect_ids if e != effect_id), state_version=version)
    if event.kind == "CancelRequested":
        return replace(state, cancel_requested=True, state_version=version)
    if event.kind == "RunSucceeded" and state.status == "running":
        if state.unknown_effect_ids:
            raise ValueError("cannot succeed with unknown effects")
        return replace(state, status="succeeded", terminal_reason="accepted", state_version=version)
    if event.kind == "RunFailed":
        return replace(state, status="failed", terminal_reason=str(event.data["reason"]), state_version=version)
    if event.kind == "InterventionRequired":
        return replace(state, status="intervention_required", terminal_reason=str(event.data["reason"]), state_version=version)
    raise ValueError(f"invalid event {event.kind!r} from state {state.status!r}")


def decide(state: RunState) -> list[dict[str, object]]:
    if state.unknown_effect_ids:
        return [{"type": "reconcile_effect", "effect_id": e} for e in state.unknown_effect_ids]
    if state.cancel_requested:
        return [{"type": "close_canceled"}]
    if state.status in TERMINAL or state.status in {"waiting", "needs_approval", "submitted"}:
        return []
    if state.status == "running" and state.current_node:
        return [{"type": "schedule_activity", "node": state.current_node}]
    return [{"type": "require_intervention", "reason": "running workflow has no current node"}]


def replay(history: list[WorkflowEvent]) -> RunState:
    state = RunState()
    for event in history:
        state = evolve(state, event)
    return state

# --8<-- endregion:core
