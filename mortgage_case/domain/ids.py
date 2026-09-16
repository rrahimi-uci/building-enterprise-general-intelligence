"""Small helpers for stable, non-secret resource identifiers."""

from __future__ import annotations

import re

from .errors import MortgageCaseError


CASE_ID_PATTERN = re.compile(r"^MORT-\d{4}-\d{6}$")


def validate_case_id(case_id: str) -> str:
    """Return a case ID only if it has the public synthetic format."""

    if not CASE_ID_PATTERN.fullmatch(case_id):
        raise MortgageCaseError("INVALID_CASE_ID", "case ID has the wrong format")
    return case_id


def case_resource_uri(case_id: str) -> str:
    """Build the canonical resource URI used by the read-only gateway."""

    return f"mortgage://case/{validate_case_id(case_id)}"
