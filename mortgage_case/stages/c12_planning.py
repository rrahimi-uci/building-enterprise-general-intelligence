"""Chapter 12: compile proposed mortgage work into a bounded plan."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[12]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C12's typed-plan compilation checkpoint."""

    return run_checkpoint(12, scenario)
