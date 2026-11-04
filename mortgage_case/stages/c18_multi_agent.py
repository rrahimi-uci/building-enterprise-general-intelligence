"""Chapter 18: coordinate narrowed child tasks without losing ownership."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[18]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C18's bounded specialist-delegation checkpoint."""

    return run_checkpoint(18, scenario)
