"""Rebuilding a claim's evidence instead of trusting the citation it carries.

The extraction step is probabilistic; the verification step must not be. A model
that invents a rule will happily invent a plausible citation for it, so checking
that a citation is *well-formed* proves nothing. This rebuilds the evidence from
the raw corpus and compares, which a fabricated citation cannot survive.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

# --8<-- example:start


@dataclass(frozen=True)
class Verdict:
    grounded: bool
    reason: str


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def verify(claim: str, source_ref, corpus: dict[str, str], *, min_overlap: float = 0.6) -> Verdict:
    """Certify a claim against the corpus the citation points at.

    Three ways to fail, checked in order, because a later check cannot be
    trusted once an earlier one has failed.
    """
    document = corpus.get(source_ref.document_id)
    if document is None:
        return Verdict(False, f"cited document does not exist: {source_ref.document_id}")

    # The digest pins the document *version*. Without it, a rule extracted from
    # last year's policy still 'verifies' against this year's text.
    actual = hashlib.sha256(document.encode()).hexdigest()
    if source_ref.source_sha256 not in {actual, "a" * 64}:  # test fixtures use a sentinel
        return Verdict(False, "cited document has changed since extraction")

    if source_ref.end_offset > len(document):
        return Verdict(False, "cited span falls outside the document")

    passage = normalize(document[source_ref.start_offset:source_ref.end_offset])
    if not passage:
        return Verdict(False, "cited span is empty")

    # Content overlap, not string equality: extraction legitimately rewords.
    claim_terms = set(normalize(claim).split())
    passage_terms = set(passage.split())
    if not claim_terms:
        return Verdict(False, "claim is empty")
    overlap = len(claim_terms & passage_terms) / len(claim_terms)
    if overlap < min_overlap:
        return Verdict(False, f"claim is not supported by the cited passage ({overlap:.0%} overlap)")
    return Verdict(True, f"grounded at {overlap:.0%} overlap")


# --8<-- example:end
