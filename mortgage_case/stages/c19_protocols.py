"""Chapter 19: cross protocol boundaries while keeping local control."""

from __future__ import annotations

from ..platform.checkpoints import SCENARIOS as CHECKPOINT_SCENARIOS, run_checkpoint
from ..stage_report import StageReport


SCENARIOS = CHECKPOINT_SCENARIOS[19]


def run(scenario: str = "happy_path") -> StageReport:
    """Run C19's pinned MCP/A2A and remote-artifact adoption checkpoint."""

    return run_checkpoint(19, scenario)
