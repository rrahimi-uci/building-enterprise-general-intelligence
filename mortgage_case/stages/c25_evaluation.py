"""Chapter 25: gate releases with deterministic evaluation evidence."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[25]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C25 evaluation and fairness-gate checkpoint."""

    return run_checkpoint(25, scenario)
