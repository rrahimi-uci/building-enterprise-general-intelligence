"""The engine, not the model, must enforce every bound."""
from __future__ import annotations

import pytest

from examples.contracts import AgentDecision, ToolCall
from examples.patterns.react_engine import ReActEngine, ReActLimits


class ScriptedDecisions:
    def __init__(self, decisions): self._d = list(decisions); self.turns = 0
    async def decide(self, *, goal, observations):
        self.turns += 1
        return self._d[min(self.turns - 1, len(self._d) - 1)]


def call(tool="lookup", **args):
    return AgentDecision(disposition="invoke_tool",
                         tool_call=ToolCall(tool_id=tool, arguments=args))


async def _tool(tool_id, arguments, effect_key):
    return {"status": "ok", "tool": tool_id}


def test_limits_reject_a_nonsense_configuration():
    # __post_init__ only runs because ReActLimits is a dataclass -- it was not one
    # in the published listing, so this validation was dead code.
    with pytest.raises(ValueError, match="positive"):
        ReActLimits(maximum_turns=0)


async def test_an_answer_ends_the_loop_immediately():
    model = ScriptedDecisions([AgentDecision(disposition="answer", answer="done")])
    result = await ReActEngine(model, _tool).run("goal")
    assert result.answer == "done"
    assert model.turns == 1


async def test_tool_call_budget_is_enforced_by_the_engine():
    model = ScriptedDecisions([call(q="a"), call(q="b"), call(q="c")])
    engine = ReActEngine(model, _tool, ReActLimits(maximum_turns=9, maximum_tool_calls=2,
                                                   maximum_identical_observations=9))
    with pytest.raises(RuntimeError, match="tool-call budget"):
        await engine.run("goal")


async def test_a_no_progress_loop_is_detected():
    # Same tool, same arguments, same result: the fingerprint repeats.
    model = ScriptedDecisions([call(q="same")])
    engine = ReActEngine(model, _tool, ReActLimits(maximum_turns=9, maximum_tool_calls=9,
                                                   maximum_identical_observations=2))
    with pytest.raises(RuntimeError, match="no-progress"):
        await engine.run("goal")


async def test_turn_limit_bounds_a_loop_that_never_answers():
    model = ScriptedDecisions([call(q="a"), call(q="b"), call(q="c"), call(q="d")])
    engine = ReActEngine(model, _tool, ReActLimits(maximum_turns=2, maximum_tool_calls=9,
                                                   maximum_identical_observations=9))
    with pytest.raises(RuntimeError, match="turn limit"):
        await engine.run("goal")
