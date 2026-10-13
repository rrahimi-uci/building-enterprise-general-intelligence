"""Build-time facts shared by every renderer.

The title page shows the month the book was built, so a reader can tell which
build they hold. Every edition takes the date from build_date(), never from a
literal in the source: the canonical Markdown carries the {{BUILD_DATE}} token,
and the assembler and the LaTeX entry point both resolve it here.

SOURCE_DATE_EPOCH, the reproducible-builds convention, pins the date when a
rebuild must reproduce an earlier artifact byte for byte. Without it the date
is the current UTC month, which is stable across the two builds the
determinism check compares.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

BUILD_DATE_TOKEN = "{{BUILD_DATE}}"
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def build_date() -> str:
    """The build month, e.g. "October 2026"."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    moment = datetime.fromtimestamp(int(epoch), timezone.utc) if epoch else datetime.now(timezone.utc)
    return f"{MONTHS[moment.month - 1]} {moment.year}"
