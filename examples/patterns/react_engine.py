"""A ReAct controller that owns the budgets the model cannot see.

The engine -- not the model -- owns turns, budgets, repeated-action detection,
and acceptance. That separation is what makes the loop bounded by construction
rather than by instruction.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol
from examples.contracts import AgentDecision

class DecisionModel(Protocol):
    """The reasoning boundary. The engine only needs one method from it."""

    async def decide(
        self, *, goal: str, observations: tuple[dict[str, object], ...]
    ) -> AgentDecision: ...


# A tool invocation carries its logical effect key, so a retry is reconcilable.
ToolInvoker = Callable[
    [str, dict[str, object], str | None], Awaitable[dict[str, object]]
]


@dataclass
class ReActLimits:
    maximum_turns: int = 6
    maximum_tool_calls: int = 4
    maximum_identical_observations: int = 2

    def __post_init__(self) -> None:
        if min(
            self.maximum_turns,
            self.maximum_tool_calls,
            self.maximum_identical_observations,
        ) < 1:
            raise ValueError("all ReAct limits must be positive")

# --8<-- region:core
class ReActEngine:
    """A bounded reason-act-observe loop with an external tool boundary."""

    def __init__(
        self,
        model: DecisionModel,
        invoke_tool: ToolInvoker,
        limits: ReActLimits = ReActLimits(),
    ) -> None:
        self.model = model
        self.invoke_tool = invoke_tool
        self.limits = limits

    @staticmethod
    def _observation_fingerprint(
        tool_id: str, arguments: dict[str, object], result: dict[str, object]
    ) -> str:
        payload = json.dumps(
            {"tool_id": tool_id, "arguments": arguments, "result": result},
            sort_keys=True,
            separators=(",", ":"),
            default=repr,
        ).encode()
        return hashlib.sha256(payload).hexdigest()

    async def run(self, goal: str) -> AgentDecision:
        observations: list[dict[str, object]] = []
        identical_observations: dict[str, int] = {}
        tool_calls = 0
        for _turn in range(self.limits.maximum_turns):
            decision = await self.model.decide(
                goal=goal, observations=tuple(observations)
            )
            if decision.disposition in {"answer", "needs_input", "delegate"}:
                return decision
            if decision.tool_call is None:
                raise ValueError("invoke_tool decision is missing tool_call")
            tool_calls += 1
            if tool_calls > self.limits.maximum_tool_calls:
                raise RuntimeError("tool-call budget exceeded")
            result = await self.invoke_tool(
                decision.tool_call.tool_id,
                decision.tool_call.arguments,
                decision.tool_call.logical_effect_key,
            )
            observations.append(
                {"tool": decision.tool_call.tool_id, "result": result}
            )
            fingerprint = self._observation_fingerprint(
                decision.tool_call.tool_id,
                decision.tool_call.arguments,
                result,
            )
            identical_observations[fingerprint] = (
                identical_observations.get(fingerprint, 0) + 1
            )
            if (
                identical_observations[fingerprint]
                >= self.limits.maximum_identical_observations
            ):
                raise RuntimeError("no-progress loop detected")
        raise RuntimeError("ReAct turn limit exceeded")

# --8<-- endregion:core
