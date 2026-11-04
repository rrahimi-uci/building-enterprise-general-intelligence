"""Chapter 14: proposal-bound human authorization for one safe operation."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[14]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C14's exact-operation approval and stale-case checkpoint."""

    return run_checkpoint(14, scenario)
