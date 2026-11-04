"""Chapter 7: compose the offline paved road for mortgage agent teams."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[7]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C07 developer-platform checkpoint through shared composition."""

    return run_checkpoint(7, scenario)
