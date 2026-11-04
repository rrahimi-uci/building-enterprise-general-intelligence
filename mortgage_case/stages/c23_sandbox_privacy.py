"""Chapter 23: enforce sandbox, egress, and privacy boundaries."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[23]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C23 sandbox and DLP checkpoint through the shared composition."""

    return run_checkpoint(23, scenario)
