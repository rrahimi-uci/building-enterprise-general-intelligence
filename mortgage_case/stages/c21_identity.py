"""Chapter 21: bind delegated work to current identity and authority."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[21]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C21 identity and capability-envelope checkpoint."""

    return run_checkpoint(21, scenario)
