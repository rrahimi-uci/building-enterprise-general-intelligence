"""Chapter 6: compose an authorized, reproducible context projection."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[6]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C06 context checkpoint through the shared composition."""

    return run_checkpoint(6, scenario)
