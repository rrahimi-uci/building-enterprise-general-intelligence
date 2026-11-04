"""Chapter 15: replay-safe waits and signals for long-running mortgage work."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[15]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C15's deterministic durable-workflow composition checkpoint."""

    return run_checkpoint(15, scenario)
