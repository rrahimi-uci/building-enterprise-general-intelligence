from __future__ import annotations

from examples.knowledge.grounding_verifier import verify
from examples.knowledge.policy_to_rule import SourceRef

SENTENCE = "Transactions exceeding $10,000 require compliance officer approval before processing."
DOC = f"4.2 Approval thresholds. {SENTENCE} Lower amounts proceed automatically."
CORPUS = {"aml_policy": DOC}
START = DOC.index("Transactions")


def ref(**kw) -> SourceRef:
    base = dict(document_id="aml_policy", section_id="sec_4_2", start_offset=START,
                end_offset=START + len(SENTENCE), source_sha256="a" * 64)
    base.update(kw)
    return SourceRef(**base)


def test_a_real_claim_against_its_real_passage_is_grounded():
    assert verify(SENTENCE, ref(), CORPUS).grounded


def test_a_fabricated_citation_cannot_pass():
    # The span is well-formed and inside the document; it simply does not say
    # what the claim says. This is the failure a format check never catches.
    invented = "Transactions exceeding $500 require board approval."
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
