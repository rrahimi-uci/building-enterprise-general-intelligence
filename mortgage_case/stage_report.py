"""Reader-visible evidence emitted by each implemented checkpoint."""

from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StageReport(BaseModel):
    """Stable, redacted report for one chapter checkpoint.

    The report describes the learning delta; it is not an audit record and it
    never represents a lending decision or a committed external effect.
    """

    model_config = ConfigDict(extra="forbid")

    chapter: str = Field(pattern=r"^C(?:0[1-9]|1[0-9]|2[0-8])$")
    scenario: str = Field(min_length=1)
    case_id: str = Field(pattern=r"^MORT-\d{4}-\d{6}$")
    status: Literal["completed", "needs_input", "refused", "failed"]
    before: str = Field(min_length=1)
    added: str = Field(min_length=1)
    after: str = Field(min_length=1)
    evidence: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    details: dict[str, object] = Field(default_factory=dict)

    def as_json(self) -> str:
        """Serialize deterministically for examples and snapshot tests."""

        return json.dumps(
            self.model_dump(mode="json"),
            indent=2,
            sort_keys=True,
        )
