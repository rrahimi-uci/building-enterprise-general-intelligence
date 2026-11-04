"""Chapter 20: contain instruction-like content outside the prompt."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[20]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C20 security-containment checkpoint through the platform composition."""

    return run_checkpoint(20, scenario)
