"""Book-facing façade for the cumulative synthetic mortgage checkpoints."""

from __future__ import annotations

import json

from mortgage_case.stages.c01_baseline import run as run_c01
from mortgage_case.stages.c02_deterministic_shell import run as run_c02
from mortgage_case.stages.c03_agent_runtime import run as run_c03

# --8<-- example:start
# --8<-- region:c01
def chapter_01_case_summary() -> dict[str, object]:
    """Show the initial mortgage case without any protected side effect."""

    return run_c01("missing_income_document").model_dump(mode="json")

# --8<-- endregion:c01

# --8<-- region:c02
def chapter_02_deterministic_proposal() -> dict[str, object]:
    """Show a typed, read-only proposal and deterministic calculation."""

    return run_c02("happy_path").model_dump(mode="json")

# --8<-- endregion:c02

# --8<-- region:c03
def chapter_03_runtime_boundary() -> dict[str, object]:
    """Show the provider-neutral bounded runtime result."""

    return run_c03("happy_path").model_dump(mode="json")

# --8<-- endregion:c03
# --8<-- example:end


if __name__ == "__main__":  # pragma: no cover
    print(json.dumps(chapter_03_runtime_boundary(), indent=2, sort_keys=True))
