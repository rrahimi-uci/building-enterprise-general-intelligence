"""Chapter 11: deterministic routing and ownership boundaries."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[11]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C11's route-selection and ownership-transfer checkpoint."""

    return run_checkpoint(11, scenario)
