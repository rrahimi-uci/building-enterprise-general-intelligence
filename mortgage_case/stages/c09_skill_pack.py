"""Chapter 9: compose the coherent mortgage domain Skill Pack."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[9]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C09 Skill Pack checkpoint through shared composition."""

    return run_checkpoint(9, scenario)
