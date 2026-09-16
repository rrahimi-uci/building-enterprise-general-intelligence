"""A small, readable Tool Gateway around a deterministic effect ledger.

The gateway is the boundary between a model's ToolIntent and a business
effect. It validates the eligible tool version, checks delegated authority,
rejects stale resource assumptions, and makes mutating calls idempotent.

The ledger below is intentionally in memory so the example stays runnable
offline. A production implementation would persist these transitions
atomically with the same logical-effect guarantees.
"""

# --8<-- example:start

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable, Literal


Connector = Callable[
    [dict[str, object], str | None],
    Awaitable[dict[str, object]],
]


class ToolGatewayError(RuntimeError):
    """The gateway rejected the proposal before or during execution."""


class StaleResource(ToolGatewayError):
    """The proposal was based on an older resource version."""


class EffectOutcomeUnknown(ToolGatewayError):
    """Dispatch may have happened, but its outcome is not yet proven."""


@dataclass(frozen=True)
class ToolManifest:
    """The capability contract published by the platform."""

    tool_id: str
    version: str
    description: str
    input_schema: str
    required_action: str
    mutating: bool
    idempotency_required: bool = False

    @property
    def tool_version(self) -> str:
        return f"{self.tool_id}@{self.version}"


@dataclass(frozen=True)
class ToolIntent:
    """A model proposal; it carries intent, not authority."""

    tool_version: str
    arguments: dict[str, object]
    expected_resource_version: int | None = None
    logical_effect_key: str | None = None


@dataclass(frozen=True)
class InvocationContext:
    """The current, platform-issued authority and resource snapshot."""

    allowed_actions: frozenset[str]
    eligible_tool_versions: frozenset[str]
    actual_resource_version: int | None = None


@dataclass(frozen=True)
class ToolResult:
    status: Literal["succeeded", "unknown"]
    output: dict[str, object] = field(default_factory=dict)
    effect_key: str | None = None


@dataclass
class EffectRecord:
    """The durable record a real implementation would store transactionally."""

    logical_effect_key: str
    intent: dict[str, object]
    state: Literal["pending", "executing", "committed", "unknown"] = "pending"
    receipt: dict[str, object] | None = None


class InMemoryEffectLedger:
    """Keep one logical effect and its receipt for this runnable example."""

    def __init__(self) -> None:
        self._records: dict[str, EffectRecord] = {}

    def begin(
        self,
        logical_effect_key: str,
        intent: dict[str, object],
    ) -> EffectRecord:
        existing = self._records.get(logical_effect_key)
        if existing is not None:
            if existing.intent != intent:
                raise ToolGatewayError("effect key was reused for a different intent")
            return existing

        record = EffectRecord(logical_effect_key, intent)
        self._records[logical_effect_key] = record
        return record

    def mark_executing(self, logical_effect_key: str) -> None:
        self._records[logical_effect_key].state = "executing"

    def mark_unknown(self, logical_effect_key: str) -> None:
        self._records[logical_effect_key].state = "unknown"

    def mark_committed(
        self,
        logical_effect_key: str,
        receipt: dict[str, object],
    ) -> EffectRecord:
        record = self._records[logical_effect_key]
        record.state = "committed"
        record.receipt = receipt
        return record


@dataclass(frozen=True)
class RegisteredTool:
    manifest: ToolManifest
    connector: Connector


class ToolGateway:
    """Validate, authorize, and execute one typed proposal."""

    def __init__(self, effect_ledger: InMemoryEffectLedger | None = None) -> None:
        self._tools: dict[str, RegisteredTool] = {}
        self._effects = effect_ledger or InMemoryEffectLedger()

    def register(self, manifest: ToolManifest, connector: Connector) -> None:
        """Register an immutable tool version with its connector."""

        if manifest.tool_version in self._tools:
            raise ToolGatewayError("tool version is already registered")
        if manifest.mutating and not manifest.idempotency_required:
            raise ToolGatewayError("mutating tools must declare idempotency")
        self._tools[manifest.tool_version] = RegisteredTool(manifest, connector)

    def discover(self, context: InvocationContext) -> tuple[ToolManifest, ...]:
        """Expose only eligible tools whose actions are currently delegated."""

        return tuple(
            item.manifest
            for key, item in sorted(self._tools.items())
            if key in context.eligible_tool_versions
            and item.manifest.required_action in context.allowed_actions
        )

    async def invoke(
        self,
        *,
        intent: ToolIntent,
        context: InvocationContext,
    ) -> ToolResult:
        """Run a proposal only after all deterministic checks pass."""

        # Eligibility is a platform decision, not something the model can add
        # to its own proposal.
        if intent.tool_version not in context.eligible_tool_versions:
            raise ToolGatewayError("tool version is not eligible for this run")

        registered = self._tools.get(intent.tool_version)
        if registered is None:
            raise ToolGatewayError("eligible tool version is not registered")

        manifest = registered.manifest
        if manifest.required_action not in context.allowed_actions:
            raise ToolGatewayError("required action is outside delegated authority")

        # Optimistic concurrency prevents a well-authorized caller from
        # overwriting state that changed after the model formed its proposal.
        if intent.expected_resource_version is not None:
            if context.actual_resource_version != intent.expected_resource_version:
                raise StaleResource("resource version changed before commit")

        if not manifest.mutating:
            output = await registered.connector(intent.arguments, None)
            return ToolResult(status="succeeded", output=output)

        if not intent.logical_effect_key:
            raise ToolGatewayError("mutating tools require a logical effect key")

        effect_intent = {
            "tool_version": intent.tool_version,
            "arguments": intent.arguments,
            "expected_resource_version": intent.expected_resource_version,
        }
        record = self._effects.begin(intent.logical_effect_key, effect_intent)

        # A replay of a committed effect returns its original receipt instead
        # of dispatching the downstream mutation a second time.
        if record.state == "committed":
            return ToolResult(
                status="succeeded",
                output=record.receipt or {},
                effect_key=intent.logical_effect_key,
            )

        # Unknown and in-flight outcomes need reconciliation or intervention;
        # blindly retrying them would defeat the idempotency boundary.
        if record.state in {"executing", "unknown"}:
            raise EffectOutcomeUnknown(intent.logical_effect_key)

        self._effects.mark_executing(intent.logical_effect_key)
        try:
            receipt = await registered.connector(
                intent.arguments,
                intent.logical_effect_key,
            )
        except Exception as exc:
            self._effects.mark_unknown(intent.logical_effect_key)
            raise EffectOutcomeUnknown(intent.logical_effect_key) from exc

        committed = self._effects.mark_committed(
            intent.logical_effect_key,
            receipt,
        )
        return ToolResult(
            status="succeeded",
            output=committed.receipt or {},
            effect_key=intent.logical_effect_key,
        )


# --8<-- example:end
