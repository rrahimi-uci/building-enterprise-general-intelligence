"""A run is served only by a worker that still understands its pinned release."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from examples.platform.release_compatibility import (
    ReleaseManifest, WorkerProfile, compatible, incompatibilities,
)

OLD_TOOL = "mortgage.document.request@1"
NEW_TOOL = "mortgage.document.request@2"


def release(**kw) -> ReleaseManifest:
    base = dict(
        release_id="mortgage-evidence-2026.09.1",
        digest="sha256:" + "a" * 64,
        agent_versions=("mortgage-evidence-agent@0.1.0",),
        skill_digests=("sha256:" + "b" * 64,),
        skill_pack_versions=("mortgage-evidence-pack@1.0.0",),
        workflow_build="wf-build-41",
        sdk_version="openai-agents==0.22.2",
        model_route_version="reasoning-standard@4",
        tool_versions=frozenset({"mortgage.case.read@1", OLD_TOOL}),
        policy_version="policy://mortgage@2026.09",
        schema_versions=frozenset({"document-request.v1"}),
        release_gate_decision_id="rgd-7781",
    )
    base.update(kw)
    return ReleaseManifest(**base)


def worker(**kw) -> WorkerProfile:
    base = dict(
        worker_pool="mortgage-wf-41",
        workflow_build="wf-build-41",
        sdk_version="openai-agents==0.22.2",
        tool_versions=frozenset({"mortgage.case.read@1", OLD_TOOL}),
        schema_versions=frozenset({"document-request.v1"}),
    )
    base.update(kw)
    return WorkerProfile(**base)


def test_old_pool_serves_run_pinned_to_old_release():
    assert compatible(release(), worker())


def test_worker_may_support_more_than_the_release_needs():
    w = worker(tool_versions=frozenset({"mortgage.case.read@1", OLD_TOOL, NEW_TOOL}),
               schema_versions=frozenset({"document-request.v1", "document-request.v2"}))
    assert compatible(release(), w)


def test_new_pool_cannot_serve_run_that_still_calls_the_old_tool():
    new_pool = worker(worker_pool="mortgage-wf-42", workflow_build="wf-build-42",
                      tool_versions=frozenset({"mortgage.case.read@1", NEW_TOOL}),
                      schema_versions=frozenset({"document-request.v2"}))
    reasons = incompatibilities(release(), new_pool)
    assert not compatible(release(), new_pool)
    assert reasons == [
        "workflow build wf-build-41 not served",
        f"tool {OLD_TOOL} not supported",
        "schema document-request.v1 not supported",
    ]


def test_sdk_drift_alone_breaks_compatibility():
    assert incompatibilities(release(), worker(sdk_version="openai-agents==0.23.0")) == [
        "SDK openai-agents==0.22.2 not served",
    ]


def test_release_manifest_is_immutable():
    r = release()
    with pytest.raises(ValidationError):
        r.workflow_build = "wf-build-42"
