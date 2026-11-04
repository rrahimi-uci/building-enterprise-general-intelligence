"""Chapter 8: compose immutable, policy-resolved mortgage Skills."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[8]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C08 Skill checkpoint through the shared composition."""

    return run_checkpoint(8, scenario)
