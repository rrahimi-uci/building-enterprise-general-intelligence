"""May this worker serve this run's pinned release?

Rollback moves new starts to another release; a run already admitted keeps the
ReleaseManifest its RunManifest references. A worker may serve that run only if
it executes the same workflow build and SDK and still understands every tool and
schema version the release can call. The worker is described by what it
supports -- a WorkerProfile -- not by a release of its own.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


# --8<-- example:start
class ReleaseManifest(BaseModel):
    """Immutable, signed graph of everything that can change behavior."""

    model_config = ConfigDict(frozen=True)

    release_id: str
    digest: str
    agent_versions: tuple[str, ...]
    skill_digests: tuple[str, ...]
    skill_pack_versions: tuple[str, ...]
    workflow_build: str
    sdk_version: str
    model_route_version: str
    tool_versions: frozenset[str]
    policy_version: str
    schema_versions: frozenset[str]
    release_gate_decision_id: str  # Chapter 25 ReleaseGateDecision


class WorkerProfile(BaseModel):
    """What one worker pool can execute, independent of any release."""

    model_config = ConfigDict(frozen=True)

    worker_pool: str
    workflow_build: str
    sdk_version: str
    tool_versions: frozenset[str]
    schema_versions: frozenset[str]


def incompatibilities(release: ReleaseManifest, worker: WorkerProfile) -> list[str]:
    """Every reason the worker cannot serve a run pinned to this release."""
    reasons: list[str] = []
    if worker.workflow_build != release.workflow_build:
        reasons.append(f"workflow build {release.workflow_build} not served")
    if worker.sdk_version != release.sdk_version:
        reasons.append(f"SDK {release.sdk_version} not served")
    reasons += [f"tool {t} not supported"
                for t in sorted(release.tool_versions - worker.tool_versions)]
    reasons += [f"schema {s} not supported"
                for s in sorted(release.schema_versions - worker.schema_versions)]
    return reasons


def compatible(release: ReleaseManifest, worker: WorkerProfile) -> bool:
    return not incompatibilities(release, worker)
# --8<-- example:end
