"""Bind verified signing and build identities to the release allowlists.

Signature verification itself is delegated to the signing toolchain; this check
receives that toolchain's verified result. It then binds the result to this
exact artifact, checks the verified identities against the allowlists, and
requires SBOM, provenance, and release-gate evidence before promotion.
"""
from __future__ import annotations

import hashlib

from pydantic import BaseModel, ConfigDict, Field


# --8<-- example:start
class VerifiedSignature(BaseModel):
    """Output of the signing toolchain after it has verified the signature."""

    model_config = ConfigDict(frozen=True)

    subject_digest: str  # the artifact digest the signature covers
    signer_identity: str
    builder_identity: str


class ReleaseAttestation(BaseModel):
    model_config = ConfigDict(frozen=True)

    release_id: str
    artifact_sha256: str
    source_revision: str
    sbom_ref: str
    provenance_ref: str
    dependency_lock_digest: str
    evaluation_evidence_refs: tuple[str, ...] = Field(min_length=1)


def verify_release_artifact(
    content: bytes,
    attestation: ReleaseAttestation,
    signature: VerifiedSignature,
    *,
    trusted_signers: frozenset[str],
    trusted_builders: frozenset[str],
) -> None:
    digest = "sha256:" + hashlib.sha256(content).hexdigest()
    if digest != attestation.artifact_sha256:
        raise ValueError("artifact digest mismatch")
    if signature.subject_digest != digest:
        raise ValueError("signature does not cover this artifact")
    if signature.signer_identity not in trusted_signers:
        raise PermissionError("untrusted release signer")
    if signature.builder_identity not in trusted_builders:
        raise PermissionError("untrusted build platform")
    if not attestation.sbom_ref or not attestation.provenance_ref:
        raise ValueError("SBOM and provenance are required")
# --8<-- example:end
