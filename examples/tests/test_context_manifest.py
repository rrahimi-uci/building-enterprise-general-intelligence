"""The ContextManifest must enforce what Chapter 06 says it records."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from examples.runtime.context_manifest import ContextBudget, ContextManifest, ContextSegment

DIGEST = "sha256:" + "c" * 64
AT = datetime(2026, 9, 10, 21, 0, tzinfo=timezone.utc)


def segment(segment_id: str, kind: str, tier: int, tokens: int = 100) -> ContextSegment:
    return ContextSegment(
        segment_id=segment_id, kind=kind, trust_tier=tier,
        source_uri=f"doc://{segment_id}", source_revision="rev17", sha256=DIGEST,
        authorization_decision_id="dec_1", freshness=AT, tokens=tokens,
    )


def manifest(*segments: ContextSegment) -> ContextManifest:
    return ContextManifest(
        context_id="CTX-7281", run_id="RUN-98217", run_manifest_digest=DIGEST,
        node_id="evidence_review", step_request_id="step_1", revision=1,
        policy_version="policy://mortgage@2026.09",
        budget=ContextBudget(max_tokens=2000, caps={
            "instructions": 400, "request": 200, "state": 300,
            "conversation": 200, "evidence": 600, "memory": 100}),
        segments=segments, created_at=AT,
    )


BASE = (
    segment("sys", "system_instruction", 1),
    segment("ask", "user_request", 3),
    segment("state", "run_state", 4),
    segment("policy", "enterprise_data", 4, tokens=300),
)


def test_a_retrieved_document_cannot_claim_a_higher_tier():
    with pytest.raises(ValidationError, match="tier 4"):
        segment("policy", "enterprise_data", 1)
    with pytest.raises(ValidationError, match="tier 4"):
        segment("pref", "memory", 3)


def test_a_section_over_its_cap_is_refused_not_truncated():
    with pytest.raises(ValidationError, match="evidence"):
        manifest(*BASE, segment("more", "enterprise_data", 4, tokens=400))


def test_duplicate_segments_are_refused():
    with pytest.raises(ValidationError, match="unique"):
        manifest(*BASE, segment("policy", "enterprise_data", 4))


def test_a_sealed_manifest_detects_any_change():
    sealed = manifest(*BASE).seal()
    assert sealed.verify()
    tampered = sealed.model_copy(update={"segments": BASE[:-1]})
    assert not tampered.verify()


def test_in_loop_tool_results_become_a_new_revision_of_the_same_step():
    first = manifest(*BASE).seal()
    second = first.revise((segment("lookup", "tool_result", 4),), at=AT)
    assert (second.step_request_id, second.revision) == ("step_1", 2)
    assert second.verify() and second.manifest_sha256 != first.manifest_sha256
    assert first.revision == 1  # the earlier revision is unchanged evidence


def test_only_tool_results_may_join_after_assembly():
    with pytest.raises(ValueError, match="only tool results"):
        manifest(*BASE).seal().revise((segment("note", "memory", 4),), at=AT)
