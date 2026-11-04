"""Chapter 28: simulate capacity, cost, deadlines, and safe degradation."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[28]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C28 capacity and resilience checkpoint."""

    return run_checkpoint(28, scenario)
