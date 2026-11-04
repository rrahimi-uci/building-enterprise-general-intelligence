"""Chapter 16: record bounded pattern choices for mortgage evidence work."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[16]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C16's executable pattern-selection checkpoint."""

    return run_checkpoint(16, scenario)
