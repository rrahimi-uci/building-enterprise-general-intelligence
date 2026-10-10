"""AP-13: memory written by default versus a gated, purpose-bound write.

Writing by default means writing without provenance, purpose, or verification:
a fact lifted from a malicious document becomes a standing belief. The
correction treats a memory write as a candidate that must pass a gate, and
every admitted record carries the purpose and expiry that justify keeping it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta

TRUSTED_PROVENANCE = {"verified_system_of_record", "verified_human_entry"}
ALLOWED_PURPOSES = {"mortgage_evidence_review"}
SECRET = re.compile(r"\b\d{8,17}\b")  # account-number-shaped strings


@dataclass(frozen=True)
class MemoryCandidate:
    subject: str
    tenant: str
    purpose: str
    claim: str
    provenance: str
    ttl_days: int

    def as_record(self, today: date) -> dict[str, object]:
        return {
            "subject": self.subject, "tenant": self.tenant, "purpose": self.purpose,
            "claim": self.claim, "provenance": self.provenance,
            "expires_on": today + timedelta(days=self.ttl_days),
        }


@dataclass
class MemoryGate:
    reason: str = ""

    def admits(self, candidate: MemoryCandidate) -> bool:
        if candidate.provenance not in TRUSTED_PROVENANCE:
            self.reason = "untrusted provenance"
        elif candidate.purpose not in ALLOWED_PURPOSES:
            self.reason = "no declared purpose"
        elif SECRET.search(candidate.claim):
            self.reason = "secret-shaped content"
        elif candidate.ttl_days <= 0:
            self.reason = "no expiry"
        else:
            self.reason = ""
        return not self.reason


@dataclass
class MemoryStore:
    records: list[object] = field(default_factory=list)
    rejected: list[tuple[MemoryCandidate, str]] = field(default_factory=list)


# --8<-- example:start
# Anti-pattern: whatever the run produced becomes durable memory, with no
# provenance, no purpose, and no way to expire.
def remember_naive(memory: MemoryStore, subject: str, summary: str) -> None:
    memory.records.append((subject, summary))


# Correction: a write is a proposal that must survive a gate. Untrusted
# provenance cannot become durable memory, and every record carries the
# purpose that justifies its retention.
def remember(memory: MemoryStore, gate: MemoryGate,
             candidate: MemoryCandidate, today: date) -> bool:
    if gate.admits(candidate):        # source trust, purpose, no secrets, expiry
        memory.records.append(candidate.as_record(today))
        return True
    memory.rejected.append((candidate, gate.reason))   # audited, not silent
    return False
# --8<-- example:end
