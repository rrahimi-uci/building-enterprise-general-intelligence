"""Chapter 17: refuse unsafe mortgage-agent anti-pattern selections."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[17]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C17's executable anti-pattern refusal checkpoint."""

    return run_checkpoint(17, scenario)
