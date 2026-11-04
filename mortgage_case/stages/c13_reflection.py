"""Chapter 13: critique and acceptance without model self-approval."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[13]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C13's separated candidate, critique, and acceptance checkpoint."""

    return run_checkpoint(13, scenario)
