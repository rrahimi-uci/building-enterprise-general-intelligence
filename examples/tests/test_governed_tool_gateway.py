"""The Tool Gateway keeps authority, freshness, and effect identity external."""
from __future__ import annotations

import pytest

from examples.foundations.governed_tool_gateway import (
    EffectOutcomeUnknown,
    InvocationContext,
    StaleResource,
    ToolGateway,
    ToolGatewayError,
    ToolIntent,
    ToolManifest,
)


def context(*, version: int = 7) -> InvocationContext:
    return InvocationContext(
        allowed_actions=frozenset({"mortgage:evidence_request"}),
        eligible_tool_versions=frozenset({"mortgage.document.request@1"}),
        actual_resource_version=version,
    )


def manifest() -> ToolManifest:
    return ToolManifest(
        tool_id="mortgage.document.request",
        version="1",
        description="Request one missing mortgage evidence document.",
        input_schema="MortgageDocumentRequest",
        required_action="mortgage:evidence_request",
        mutating=True,
        idempotency_required=True,
    )


async def test_stale_proposal_is_rejected_before_dispatch():
    calls: list[str] = []

    async def connector(arguments, effect_key):
        calls.append(effect_key or "read")
        return {"receipt": "document-request:MORT-2026-000184"}

    gateway = ToolGateway()
    gateway.register(manifest(), connector)

    with pytest.raises(StaleResource):
        await gateway.invoke(
            intent=ToolIntent(
                tool_version="mortgage.document.request@1",
                arguments={"case_id": "MORT-2026-000184", "document_kind": "employment_verification"},
                expected_resource_version=6,
                logical_effect_key="mortgage:document-request:MORT-2026-000184:employment_verification",
            ),
            context=context(version=7),
        )

    assert calls == []


async def test_unauthorized_action_is_rejected():
    async def connector(arguments, effect_key):
        return {"receipt": "must-not-run"}

    gateway = ToolGateway()
    gateway.register(manifest(), connector)

    with pytest.raises(ToolGatewayError):
        await gateway.invoke(
            intent=ToolIntent(
                tool_version="mortgage.document.request@1",
                arguments={"case_id": "MORT-2026-000184", "document_kind": "employment_verification"},
                expected_resource_version=7,
                logical_effect_key="mortgage:document-request:MORT-2026-000184:employment_verification",
            ),
            context=InvocationContext(
                allowed_actions=frozenset({"mortgage:case:read"}),
                eligible_tool_versions=frozenset({"mortgage.document.request@1"}),
                actual_resource_version=7,
            ),
        )


async def test_replaying_a_committed_effect_returns_one_receipt():
    calls = 0

    async def connector(arguments, effect_key):
        nonlocal calls
        calls += 1
        return {"receipt": "document-request:MORT-2026-000184", "effect_key": effect_key}

    gateway = ToolGateway()
    gateway.register(manifest(), connector)
    intent = ToolIntent(
        tool_version="mortgage.document.request@1",
        arguments={"case_id": "MORT-2026-000184", "document_kind": "employment_verification"},
        expected_resource_version=7,
        logical_effect_key="mortgage:document-request:MORT-2026-000184:employment_verification",
    )

    first = await gateway.invoke(intent=intent, context=context())
    replay = await gateway.invoke(intent=intent, context=context())

    assert calls == 1
    assert replay.output == first.output


async def test_unknown_outcome_is_not_blindly_retried():
    calls = 0

    async def connector(arguments, effect_key):
        nonlocal calls
        calls += 1
        raise TimeoutError("response lost after dispatch")

    gateway = ToolGateway()
    gateway.register(manifest(), connector)
    intent = ToolIntent(
        tool_version="mortgage.document.request@1",
        arguments={"case_id": "MORT-2026-000184", "document_kind": "employment_verification"},
        expected_resource_version=7,
        logical_effect_key="mortgage:document-request:MORT-2026-000184:employment_verification",
    )

    with pytest.raises(EffectOutcomeUnknown):
        await gateway.invoke(intent=intent, context=context())
    with pytest.raises(EffectOutcomeUnknown):
        await gateway.invoke(intent=intent, context=context())

    assert calls == 1
