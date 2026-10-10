"""AP-02: the transcript as the record versus typed state projected into context.

Every mechanism that keeps a context window small is lossy. If the transcript is
the record, whatever survives compaction is what the system believes. The
correction writes decisions to a typed store with optimistic concurrency and
builds the prompt from a fresh snapshot of that store on every step.
"""
from __future__ import annotations

from dataclasses import dataclass, field


class StaleWrite(Exception):
    """The writer read an older version of the run state than the store holds."""


def summarize(messages: list[str], keep: int) -> list[str]:
    """Stand-in for compaction: keeps the outcome line, drops older detail."""
    return messages[-keep:]


@dataclass(frozen=True)
class DecisionRecord:
    authority: str
    disposition: str
    conditions: tuple[str, ...]


@dataclass
class StateStore:
    """Reference implementation; production uses a transactional store."""

    _records: list[DecisionRecord] = field(default_factory=list)
    version: int = 0

    def record(self, decision: DecisionRecord, *, expected_version: int) -> int:
        if expected_version != self.version:
            raise StaleWrite(f"expected version {expected_version}, store is at {self.version}")
        self._records.append(decision)
        self.version += 1
        return self.version

    def snapshot(self) -> tuple[DecisionRecord, ...]:
        return tuple(self._records)


# --8<-- example:start
# Anti-pattern: the transcript is the record, so whatever survives
# compaction is what the system believes.
def remember_naive(messages: list[str]) -> list[str]:
    messages.append("Legal approved, with an indemnity cap and 90-day notice.")
    messages.append("Legal approved.")
    return summarize(messages, keep=1)         # the conditions are gone


# Correction: the decision is a typed record; the prompt is a projection of it.
# Compaction can lose a sentence without losing the fact.
def remember(state: StateStore) -> list[str]:
    state.record(
        DecisionRecord(
            authority="legal",
            disposition="approved_with_conditions",
            conditions=("indemnity_cap_2m", "termination_notice_90d"),
        ),
        expected_version=state.version,        # optimistic concurrency
    )
    return project_context(state.snapshot())


def project_context(snapshot: tuple[DecisionRecord, ...]) -> list[str]:
    """Build the prompt's state section fresh from the store, every step."""
    return [
        f"{d.authority}: {d.disposition} ({', '.join(d.conditions)})" for d in snapshot
    ]
# --8<-- example:end
