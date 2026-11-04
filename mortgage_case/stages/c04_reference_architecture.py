"""Chapter 4: compose the mortgage run around platform-owned records."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[4]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C04 architecture checkpoint through the shared composition."""

    return run_checkpoint(4, scenario)
