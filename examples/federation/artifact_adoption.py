"""Adopt a remote artifact only under local policy (Chapter 19, `:adoptResult`).

A peer's artifact crosses a trust boundary. Schema and malware scanning happen
first; this check then decides whether this tenant may depend on it for this
purpose. Every refusal is a PermissionError naming the rule that failed.
"""
from __future__ import annotations

# --8<-- example:start
from datetime import datetime

from pydantic import BaseModel


class ArtifactDescriptor(BaseModel):
    artifact_id: str
    tenant_id: str
    data_classes: frozenset[str]
    region: str
    allowed_purposes: frozenset[str]
    provenance_digest: str
    content_sha256: str
    expires_at: datetime
    legal_hold: bool = False


class AdoptionPolicy(BaseModel):
    tenant_id: str
    allowed_data_classes: frozenset[str]
    allowed_regions: frozenset[str]
    purpose: str
    trusted_provenance_digests: frozenset[str]


def authorize_artifact_adoption(
    artifact: ArtifactDescriptor, policy: AdoptionPolicy, *,
    observed_sha256: str, now: datetime,
) -> None:
    if observed_sha256 != artifact.content_sha256:
        raise PermissionError("artifact content does not match its declared hash")
    if artifact.tenant_id != policy.tenant_id:
        raise PermissionError("cross-tenant artifact adoption denied")
    if not artifact.data_classes <= policy.allowed_data_classes:
        raise PermissionError("artifact classification exceeds policy")
    if artifact.region not in policy.allowed_regions:
        raise PermissionError("artifact region is not allowed")
    if policy.purpose not in artifact.allowed_purposes:
        raise PermissionError("artifact purpose is not allowed")
    if artifact.provenance_digest not in policy.trusted_provenance_digests:
        raise PermissionError("artifact provenance is not trusted")
    if now > artifact.expires_at and not artifact.legal_hold:
        raise PermissionError("artifact expired")
# --8<-- example:end
