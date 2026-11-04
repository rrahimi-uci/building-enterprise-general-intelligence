"""Chapter 5: compose governed, versioned mortgage knowledge."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[5]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C05 knowledge checkpoint through the shared composition."""

    return run_checkpoint(5, scenario)
