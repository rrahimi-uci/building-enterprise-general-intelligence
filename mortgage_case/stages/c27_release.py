"""Chapter 27: preserve active work with immutable release compatibility."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[27]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C27 release and compatible-worker checkpoint."""

    return run_checkpoint(27, scenario)
