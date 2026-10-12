"""A document's fields verified against its bytes before they become facts.

A model proposes typed fields from a pay statement; deterministic code decides
which of them the platform may treat as facts. Verification re-opens the pinned
bytes through the same verifier the rule lane uses, checks extracted fields
against text and derived fields against their inputs, checks the record is
internally consistent and agrees with the case, and serves nothing unless every
decision-material field is supported. It proves the document says it, not that
it is true. Synthetic data only.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Callable, Literal

from examples.knowledge.grounding_verifier import HELD, Status, verify as ground
from examples.knowledge.policy_to_rule import SourceRef

# --8<-- region:record
Route = Literal["human_review", "targeted_repair", "case_management"]

# Which fields can block is the platform's declaration, never the extractor's.
PAY_STATEMENT = {"employer": True, "pay_date": True, "gross_pay": True,
                 "deductions": True, "net_pay": True, "ytd_gross": True,
                 "pay_statement_age_days": True, "employer_address": False}


@dataclass(frozen=True)
class DocumentRecord:
    """Intake's record of the bytes: the digest is authoritative, text a projection."""

    document_id: str
    kind: str
    sha256: str
    source_revision: str
    case_id: str
    acl_ref: str
    extractor_version: str  # model route and prompt digest
    label: str = "data"     # the text is data, never instruction


@dataclass(frozen=True)
class ExtractedField:
    name: str
    value: Decimal | str | int
    unit: str | None              # the unit lives on the field: "USD", "days"
    origin: Literal["extracted", "derived"]
    region: SourceRef | None = None   # extracted: where the document states it
    quote: str = ""                   # extracted: the text the model says it read
    inputs: tuple[str, ...] = ()      # derived: the fields it is computed from
    confidence: float = 0.0           # recorded for evaluation, never used to decide


@dataclass(frozen=True)
class FieldVerdict:
    name: str
    status: Status
    reason: str
    route: Route | None = None


def duplicate_of(record: DocumentRecord, seen: dict[str, str]) -> str | None:
    """Same bytes under a new name are the earlier document, not a second one."""
    return seen.get(record.sha256)
# --8<-- endregion:record


@dataclass(frozen=True)
class Certification:
    record: DocumentRecord
    verdicts: dict[str, FieldVerdict]
    values: dict[str, object] = field(default_factory=dict)
    complete: bool = False
    servable: bool = False
    route: Route | None = None


def _parse(text: str, like: object) -> object:
    if isinstance(like, Decimal):
        try:
            return Decimal(text.replace(",", "").replace("USD", "").strip())
        except InvalidOperation:
            return None
    return text.strip()


PRIORITY: tuple[Route, ...] = ("human_review", "targeted_repair", "case_management")

# Illustrative internal-consistency checks for a pay statement.
CONSISTENCY = (
    (("net_pay", "gross_pay", "deductions"),
     lambda g: g["net_pay"] == g["gross_pay"] - g["deductions"],
     "net is not gross minus deductions"),
    (("ytd_gross", "gross_pay"), lambda g: g["ytd_gross"] >= g["gross_pay"],
     "year-to-date is below the period"),
)


# --8<-- region:verify
def verify_document(record, fields, text, *, case, derive, verifier=ground):
    if hashlib.sha256(text.encode()).hexdigest() != record.sha256:
        held = {f.name: FieldVerdict(f.name, HELD, "bytes changed since extraction",
                                     "case_management") for f in fields}
        return Certification(record, held, complete=True, route="case_management")
    out: dict[str, FieldVerdict] = {}
    values: dict[str, object] = {}

    def fail(names, status, why, route):
        for n in names:
            out[n] = FieldVerdict(n, status, why, route)

    for f in (f for f in fields if f.origin == "extracted"):
        v = verifier(f.quote, f.region, {record.document_id: text})
        if v is None:
            continue  # no verdict for this field: the run is incomplete
        if not v.grounded:
            fail([f.name], v.status, v.reason, "targeted_repair")
        elif _parse(v.evidence, f.value) != f.value:  # the bytes decide, not the quote
            fail([f.name], "contradicted", f"bytes say {v.evidence!r}", "human_review")
        else:
            values[f.name] = f.value
    agree = [((k,), lambda g, k=k, e=e: g[k] == e, f"{k} disagrees with the case")
             for k, e in case.items()]
    for names, holds, why in (*CONSISTENCY, *agree):
        if all(n in values for n in names) and not holds(values):
            fail(names, "contradicted", why, "human_review")  # cannot tell which lies
    for f in (f for f in fields if f.origin == "derived"):
        if not all(n in values and n not in out for n in f.inputs):
            fail([f.name], HELD, "an input is not supported", "case_management")
        elif derive[f.name](values) != f.value:  # checked structurally, never as text
            fail([f.name], "contradicted", "derivation disagrees", "human_review")
        else:
            values[f.name] = f.value
    for f in fields:
        if f.name not in PAY_STATEMENT:
            fail([f.name], HELD, "not a declared field of this kind", None)
        elif f.name in values and f.name not in out:
            out[f.name] = FieldVerdict(f.name, "supported", "verified against bytes")
    named = {f.name for f in fields}
    fail([n for n, m in PAY_STATEMENT.items() if m and n not in named],
         HELD, "nothing extracted", "targeted_repair")
    complete = all(f.name in out for f in fields)  # one verdict per field
    blocking = [v for v in out.values()
                if PAY_STATEMENT.get(v.name) and v.status != "supported"]
    route = next((r for r in PRIORITY if any(v.route == r for v in blocking)), None)
    facts = {n: values[n] for n in values if out[n].status == "supported"}
    return Certification(record, out, facts, complete, complete and not blocking, route)


def facts_for_rules(cert: Certification) -> dict[str, object]:
    """Only a servable document yields facts; anything else leaves the rule unknown."""
    return dict(cert.values) if cert.servable else {}
# --8<-- endregion:verify
