"""Chapter 22: make protected effects idempotent and recoverable."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS
from ..platform.checkpoints import run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[22]


def run(scenario: str = "happy_path") -> StageReport:
    """Run the C22 effect-ledger checkpoint without duplicating platform logic."""

    return run_checkpoint(22, scenario)
