"""A remote artifact is adopted only when every local rule holds."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from examples.federation.artifact_adoption import (
    AdoptionPolicy, ArtifactDescriptor, authorize_artifact_adoption,
)

NOW = datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc)
HASH = "a" * 64

APPRAISAL = ArtifactDescriptor(
    artifact_id="artifact://partner/appraisal-review/MORT-2026-000184",
    tenant_id="harborlight", data_classes=frozenset({"confidential"}),
    region="us-east", allowed_purposes=frozenset({"mortgage-evidence-review"}),
    provenance_digest="sha256:partner-attestation", content_sha256=HASH,
    expires_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
)
POLICY = AdoptionPolicy(
    tenant_id="harborlight", allowed_data_classes=frozenset({"confidential", "internal"}),
    allowed_regions=frozenset({"us-east"}), purpose="mortgage-evidence-review",
    trusted_provenance_digests=frozenset({"sha256:partner-attestation"}),
)


def adopt(artifact=APPRAISAL, policy=POLICY, *, observed=HASH, now=NOW):
    authorize_artifact_adoption(artifact, policy, observed_sha256=observed, now=now)


def test_a_conforming_artifact_is_adopted():
    adopt()  # no exception


@pytest.mark.parametrize("artifact, reason", [
    (APPRAISAL.model_copy(update={"tenant_id": "other-bank"}), "cross-tenant"),
    (APPRAISAL.model_copy(update={"region": "eu-west"}), "region"),
    (APPRAISAL.model_copy(update={"allowed_purposes": frozenset({"marketing"})}), "purpose"),
    (APPRAISAL.model_copy(update={"data_classes": frozenset({"restricted"})}), "classification"),
    (APPRAISAL.model_copy(update={"provenance_digest": "sha256:unknown"}), "provenance"),
])
def test_each_local_rule_refuses_on_its_own(artifact, reason):
    with pytest.raises(PermissionError, match=reason):
        adopt(artifact)


def test_content_that_does_not_match_its_hash_is_refused():
    with pytest.raises(PermissionError, match="hash"):
        adopt(observed="b" * 64)


def test_expiry_is_enforced_unless_a_legal_hold_applies():
    late = datetime(2026, 10, 1, tzinfo=timezone.utc)
    with pytest.raises(PermissionError, match="expired"):
        adopt(now=late)
    adopt(APPRAISAL.model_copy(update={"legal_hold": True}), now=late)
