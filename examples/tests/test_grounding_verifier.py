from __future__ import annotations

from examples.knowledge.grounding_verifier import verify
from examples.knowledge.policy_to_rule import SourceRef

SENTENCE = "Mortgage cases with requested LTV above 80% require human underwriter approval before submission."
DOC = f"4.2 Review thresholds. {SENTENCE} Lower LTV cases remain in evidence review."
CORPUS = {"mortgage_underwriting_policy": DOC}
START = DOC.index("Mortgage")


def ref(**kw) -> SourceRef:
    base = dict(document_id="mortgage_underwriting_policy", section_id="sec_4_2", start_offset=START,
                end_offset=START + len(SENTENCE), source_sha256="a" * 64)
    base.update(kw)
    return SourceRef(**base)


def test_a_real_claim_against_its_real_passage_is_grounded():
    assert verify(SENTENCE, ref(), CORPUS).grounded


def test_a_fabricated_citation_cannot_pass():
    # The span is well-formed and inside the document; it simply does not say
    # what the claim says. This is the failure a format check never catches.
    invented = "Property inspections older than 180 days require title counsel approval before closing."
    verdict = verify(invented, ref(), CORPUS)
    assert not verdict.grounded
    assert "not supported" in verdict.reason


def test_a_citation_to_a_document_that_does_not_exist_fails():
    assert not verify(SENTENCE, ref(document_id="made_up_policy"), CORPUS).grounded


def test_a_span_outside_the_document_fails():
    assert not verify(SENTENCE, ref(end_offset=10_000), CORPUS).grounded


def test_a_changed_document_fails_even_with_a_valid_span():
    # Same offsets, different corpus version: the digest no longer matches.
    verdict = verify(SENTENCE, ref(source_sha256="b" * 64), CORPUS)
    assert not verdict.grounded
    assert "changed" in verdict.reason


def test_a_paraphrased_quote_is_not_grounded_even_at_high_overlap():
    # Every content word of the sentence survives; the source never wrote it.
    paraphrase = ("Mortgage cases with requested LTV above 80% require approval "
                  "by a human underwriter before submission.")
    verdict = verify(paraphrase, ref(), CORPUS)
    assert verdict.status == "insufficient_evidence"
    assert verdict.evidence is None


def test_the_recorded_quote_is_sliced_from_the_bytes_not_copied_from_the_claim():
    # Case and spacing differ from the source; the evidence is the source's text.
    sloppy = "  mortgage cases  with requested ltv ABOVE 80%  "
    verdict = verify(sloppy, ref(), CORPUS)
    assert verdict.grounded
    assert verdict.evidence == "Mortgage cases with requested LTV above 80%"
    assert verdict.evidence in DOC
