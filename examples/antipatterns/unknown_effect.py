"""AP-05: timeout as failure versus an Unknown effect settled by reconciliation.

A timeout describes the response, not the effect. The correction records the
effect in the ledger from Chapter 22's example, and when a call times out it
asks the downstream system of record what actually landed. Only proven absence
licenses a retry, and the retry reuses the same key. A request that is still
executing stays Unknown; one whose outcome cannot be proven goes to
InterventionRequired. Neither is guessed.
"""
from __future__ import annotations

from typing import Literal, Protocol

from examples.foundations.effect_idempotency import EffectLedger, EffectOutcomeUnknown

LookupStatus = Literal["committed", "absent", "executing", "unprovable"]


class DocumentService(Protocol):
    def request(self, payload: dict[str, object], idempotency_key: str | None = None) -> str: ...

    def lookup(self, idempotency_key: str) -> tuple[LookupStatus, str | None]: ...


# --8<-- example:start
# Anti-pattern: a timeout is treated as proof that nothing happened.
def request_document_naive(service: DocumentService, payload: dict[str, object]) -> str:
    try:
        return service.request(payload)
    except TimeoutError:
        return service.request(payload)       # the request may now exist twice


# Correction: Unknown blocks retry until the system of record decides.
def request_document(service: DocumentService, ledger: EffectLedger,
                     key: str, payload: dict[str, object]) -> str:
    def send() -> str:
        return service.request(payload, idempotency_key=key)

    try:
        return ledger.commit(key, payload, send)       # a timeout leaves it Unknown
    except EffectOutcomeUnknown:
        status, receipt = service.lookup(idempotency_key=key)
        if status == "committed":                      # it landed: adopt it
            ledger.reconcile(key, outcome="committed", evidence=receipt or "")
            return receipt or ""
        if status == "absent":                         # proven absent: same key
            ledger.reconcile(key, outcome="absent", evidence="downstream: absent")
            return ledger.commit(key, payload, send)
        if status == "unprovable":                     # InterventionRequired
            ledger.reconcile(key, outcome="unprovable", evidence="lookup inconclusive")
        raise                                          # executing: stays Unknown
# --8<-- example:end
