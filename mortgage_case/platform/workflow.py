"""Replay-safe workflow façade."""

from .enterprise import EventStore, ReferenceArchitecture


def fold_events(events):
    """Build a small status projection without performing I/O."""
    state = {"status": "created", "signals": 0, "sequence": 0}
    for event in events:
        state["sequence"] = event.sequence
        if event.event_type == "RunStarted":
            state["status"] = "running"
        elif event.event_type == "SignalReceived":
            state["signals"] += 1
        elif event.event_type == "RunCancelled":
            state["status"] = "cancelled"
    return state


__all__ = ["EventStore", "ReferenceArchitecture", "fold_events"]
