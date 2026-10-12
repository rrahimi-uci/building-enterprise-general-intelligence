"""Rebuilding a claim's evidence instead of trusting the citation it carries.

The extraction step is probabilistic; the verification step must not be. A model
that invents a rule will happily invent a plausible citation for it, so checking
that a citation is *well-formed* proves nothing. This re-opens the pinned bytes,
requires the quoted text to be literally present in the cited span, and records
the evidence sliced from those bytes -- never the text the claim brought with it.

Adapted from Policy Logic Forge [R48], commit c22dc450,
agents/agent_09_grounding_verifier.py and utils/citations.py (MIT),
reduced to one evidence record per claim and to the deterministic half: the
reference lets a model judge whether the evidence supports the claim, and
also repairs near-miss quotes; both are omitted here. Synthetic data only.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal

TEST_SENTINEL = "a" * 64  # fixtures that do not exercise the digest use this

# --8<-- example:start

Status = Literal["supported", "contradicted", "insufficient_evidence"]
HELD: Status = "insufficient_evidence"


@dataclass(frozen=True)
class Verdict:
    status: Status
    reason: str
    evidence: str | None = None  # sliced from the pinned bytes, never from the claim

    @property
    def grounded(self) -> bool:
        return self.status == "supported"


def _folded(text: str) -> tuple[str, list[int]]:
    """Case- and whitespace-folded text, with each character's source offset."""
    chars: list[str] = []
    offsets: list[int] = []
    for i, ch in enumerate(text):
        if ch.isspace() and (not chars or chars[-1] == " "):
            continue
        chars.append(" " if ch.isspace() else ch.lower())
        offsets.append(i)
    return "".join(chars).rstrip(), offsets


def verify(quote: str, source_ref, corpus: dict[str, str]) -> Verdict:
    """Admit a claim only on a literal span of the bytes it cites.

    Checked in order, because a later check cannot be trusted once an earlier
    one has failed.
    """
    document = corpus.get(source_ref.document_id)
    if document is None:
        return Verdict(HELD, "cited document does not exist")
    # The digest pins the document *version*. Without it, a rule extracted from
    # last year's policy still 'verifies' against this year's text.
    actual = hashlib.sha256(document.encode()).hexdigest()
    if source_ref.source_sha256 not in {actual, TEST_SENTINEL}:
        return Verdict(HELD, "cited document has changed since extraction")
    if not 0 <= source_ref.start_offset < source_ref.end_offset <= len(document):
        return Verdict(HELD, "cited span falls outside the document")
    span = document[source_ref.start_offset:source_ref.end_offset]
    span_folded, offsets = _folded(span)
    quote_folded, _ = _folded(quote.strip())
    # Literal presence, not term overlap: a paraphrase that shares nine words in
    # ten is still the model's sentence, not the source's.
    at = span_folded.find(quote_folded) if quote_folded else -1
    if at < 0:
        return Verdict(HELD, "claim is not supported by the cited passage")
    evidence = span[offsets[at]:offsets[at + len(quote_folded) - 1] + 1]
    return Verdict("supported", "quoted text found in the cited span", evidence)


# --8<-- example:end
