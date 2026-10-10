"""A release promotes only if verified identities and evidence bind to these bytes."""
from __future__ import annotations

import hashlib

import pytest
from pydantic import ValidationError

from examples.platform.release_attestation import (
    ReleaseAttestation, VerifiedSignature, verify_release_artifact,
)

CONTENT = b"release-bundle mortgage-evidence-2026.09.1"
DIGEST = "sha256:" + hashlib.sha256(CONTENT).hexdigest()
SIGNERS = frozenset({"release-signer@harborlight.example"})
BUILDERS = frozenset({"https://ci.harborlight.example/builder@v3"})


def attestation(**kw) -> ReleaseAttestation:
    base = dict(release_id="mortgage-evidence-2026.09.1", artifact_sha256=DIGEST,
                source_revision="git:4f2c9e1", sbom_ref="sbom://mortgage-evidence/2026.09.1",
                provenance_ref="slsa://mortgage-evidence/2026.09.1",
                dependency_lock_digest="sha256:" + "c" * 64,
                evaluation_evidence_refs=("rgd-7781",))
    base.update(kw)
    return ReleaseAttestation(**base)


def signature(**kw) -> VerifiedSignature:
    base = dict(subject_digest=DIGEST, signer_identity="release-signer@harborlight.example",
                builder_identity="https://ci.harborlight.example/builder@v3")
    base.update(kw)
    return VerifiedSignature(**base)


def verify(content=CONTENT, att=None, sig=None):
    verify_release_artifact(content, att or attestation(), sig or signature(),
                            trusted_signers=SIGNERS, trusted_builders=BUILDERS)


def test_trusted_artifact_passes():
    verify()


def test_tampered_content_is_rejected():
    with pytest.raises(ValueError, match="digest mismatch"):
        verify(content=CONTENT + b"!")


def test_signature_over_another_artifact_is_rejected():
    with pytest.raises(ValueError, match="does not cover"):
        verify(sig=signature(subject_digest="sha256:" + "d" * 64))


def test_untrusted_signer_is_rejected():
    with pytest.raises(PermissionError, match="signer"):
        verify(sig=signature(signer_identity="someone@else.example"))


def test_untrusted_builder_is_rejected():
    with pytest.raises(PermissionError, match="build platform"):
        verify(sig=signature(builder_identity="laptop"))


def test_missing_provenance_is_rejected():
    with pytest.raises(ValueError, match="SBOM and provenance"):
        verify(att=attestation(provenance_ref=""))


def test_release_gate_evidence_is_required():
    with pytest.raises(ValidationError):
        attestation(evaluation_evidence_refs=())
