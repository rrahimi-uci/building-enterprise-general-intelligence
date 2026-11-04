"""Chapter 10: bounded ReAct evidence work for the synthetic mortgage case."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[10]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C10's bounded, read-only reasoning checkpoint."""

    return run_checkpoint(10, scenario)
