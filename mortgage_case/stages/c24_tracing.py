"""Chapter 24: produce privacy-safe causal trace evidence."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[24]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C24 tracing checkpoint with the platform-owned privacy controls."""

    return run_checkpoint(24, scenario)
