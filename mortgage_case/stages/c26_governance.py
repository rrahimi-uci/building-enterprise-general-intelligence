"""Chapter 26: keep operating controls owned, evidenced, and time-bounded."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[26]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C26 governance-record checkpoint."""

    return run_checkpoint(26, scenario)
