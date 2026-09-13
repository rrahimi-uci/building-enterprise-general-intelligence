"""A deterministic, offline Model for the book's OpenAI Agents SDK examples.

The examples in this book must run in CI with no network access and no API key,
yet still exercise the real Agents SDK control flow: tool dispatch, structured
output parsing, guardrails, handoffs, and the run loop.

`ScriptedModel` implements the SDK's `Model` protocol and replays a fixed list
of turns, so a run is fully deterministic. It is a test double for the *model*
only -- every other component in an example is the genuine SDK.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterable

from agents.items import ModelResponse
from agents.models.interface import Model
from agents.usage import Usage
from openai.types.responses import (
    ResponseFunctionToolCall,
    ResponseOutputMessage,
    ResponseOutputText,
)


@dataclass
class ToolCall:
    """One scripted tool invocation."""

    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    call_id: str | None = None


@dataclass
class Say:
    """One scripted final message from the model."""

    text: str


Turn = ToolCall | Say


def _message(text: str) -> ResponseOutputMessage:
    return ResponseOutputMessage(
        id="msg_scripted",
        type="message",
        role="assistant",
        status="completed",
        content=[ResponseOutputText(type="output_text", text=text, annotations=[])],
    )


def _tool_call(call: ToolCall, index: int) -> ResponseFunctionToolCall:
    return ResponseFunctionToolCall(
        type="function_call",
        id=f"fc_{index}",
        call_id=call.call_id or f"call_{index}",
        name=call.name,
        arguments=json.dumps(call.arguments),
    )


class ScriptedModel(Model):
    """Replays `turns` in order, one per model invocation.

    Subclasses the SDK's `Model` base class rather than duck-typing it: the
    runner resolves `RunConfig.model` with an `isinstance` check, so a
    structurally-compatible class that does not inherit `Model` is silently
    ignored and the run falls through to the real OpenAI provider.

    Each element is either a `ToolCall` (the model asks for a tool) or a `Say`
    (the model produces its final answer). Exhausting the script raises, which
    keeps a broken example loud rather than silently looping.
    """

    def __init__(self, turns: Iterable[Turn]) -> None:
        self._turns = list(turns)
        self._index = 0
        self.calls: list[Turn] = []

    async def get_response(
        self,
        system_instructions: str | None,
        input: Any,
        model_settings: Any,
        tools: Any,
        output_schema: Any,
        handoffs: Any,
        tracing: Any,
        *,
        previous_response_id: str | None = None,
        conversation_id: str | None = None,
        prompt: Any = None,
        **kwargs: Any,
    ) -> ModelResponse:
        if self._index >= len(self._turns):
            raise AssertionError(
                f"ScriptedModel exhausted after {len(self._turns)} turns; "
                "the example asked the model for one more response than it scripted."
            )
        turn = self._turns[self._index]
        self._index += 1
        self.calls.append(turn)
        output = [_message(turn.text)] if isinstance(turn, Say) else [_tool_call(turn, self._index)]
        return ModelResponse(
            output=output,
            usage=Usage(requests=1, input_tokens=0, output_tokens=0, total_tokens=0),
            response_id=f"resp_scripted_{self._index}",
        )

    async def stream_response(self, *args: Any, **kwargs: Any):  # pragma: no cover
        raise NotImplementedError("The book's examples use non-streaming runs.")

    async def close(self) -> None:  # pragma: no cover
        return None
