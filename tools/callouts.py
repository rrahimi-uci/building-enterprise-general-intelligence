#!/usr/bin/env python3
"""The one definition of the book's callout taxonomy.

Both renderers import this. The cross-format contract requires the DOCX and
XeLaTeX editions to present the same semantic box for the same marker, and the
only way to guarantee that is for them to read the same table -- a duplicated
mapping in two renderers drifts the first time someone adds a kind to one.

Authoring convention (canonical Markdown): a one-column table whose single cell
opens with the marker in bold.

    |  |
    | --- |
    | **BEST PRACTICE**  Version every tool manifest; resolve at dispatch. |

A guidance box carries an instruction the reader can act on. If it restates the
paragraph above it, delete it -- that is the test, not whether it is true.
"""
from __future__ import annotations

import re

# marker -> (latex environment, docx shading, printed title)
# Order matters: the first marker found in the text wins, so more specific
# markers precede the ones they contain (COMMON PITFALL before ANTI-PATTERN is
# irrelevant, but EVIDENCE CAVEAT must precede CAUTION).
CALLOUT_KINDS: list[tuple[str, str, str, str]] = [
    # --- guidance boxes -------------------------------------------------
    ("BEST PRACTICE", "bookbestpractice", "E7F5F3", "Best practice"),
    ("ARCHITECTURE GUIDANCE", "bookarchitecture", "EAF3FB", "Architecture guidance"),
    ("DEVELOPER GUIDELINE", "bookdeveloper", "EDF3FC", "Developer guideline"),
    ("PRODUCTION CONSIDERATION", "bookproduction", "F7ECF8", "Production consideration"),
    ("SECURITY AND GOVERNANCE", "booksecurity", "FCECEC", "Security and governance"),
    ("COMMON PITFALL", "bookantipattern", "FFF4DF", "Common pitfall"),
    ("ANTI-PATTERN", "bookantipattern", "FFF4DF", "Anti-pattern"),
    ("PERFORMANCE AND COST", "bookcost", "F6F5E3", "Performance and cost"),
    ("OBSERVABILITY TIP", "bookobservability", "E6F5F9", "Observability tip"),
    # --- narrative and evidence callouts carried over from v1.0.0 -------
    ("NORTHSTAR AT THIS POINT", "bookcallout", "EAF3FB", "Northstar at this point"),
    ("NORTH-STAR RULE", "bookcallout", "EAF3FB", "North-star rule"),
    ("DESIGN DECISION", "bookcallout", "EAF3FB", "Design decision"),
    ("IMPLEMENTATION NOTE", "bookcallout", "EAF3FB", "Implementation note"),
    ("SOURCE DISCIPLINE", "bookcallout", "EAF3FB", "Source discipline"),
    ("EVIDENCE CAVEAT", "bookcaution", "FFF4DF", "Evidence caveat"),
    ("CAUTION", "bookcaution", "FFF4DF", "Caution"),
    ("THREAT", "bookthreat", "FCECEC", "Threat"),
]

DEFAULT = ("bookcallout", "EAF3FB", "Architecture note")

# The eight kinds introduced for v2.0.0, used by the validators to report
# adoption per chapter.
GUIDANCE_MARKERS = [k[0] for k in CALLOUT_KINDS[:9]]

_MARKER_PREFIX = re.compile(r"^\s*\*\*[A-Za-z0-9 &/,'-]+\*\*[\s:.—-]*")


def classify(text: str) -> tuple[str, str, str]:
    """Return (latex_environment, docx_fill, title) for a callout body."""
    plain = re.sub(r"[*_`]", "", text).upper()
    for marker, environment, fill, title in CALLOUT_KINDS:
        if marker in plain:
            return environment, fill, title
    return DEFAULT


def strip_marker(text: str) -> str:
    """Remove the leading **MARKER**; the rendered box title already says it."""
    return _MARKER_PREFIX.sub("", text, count=1).strip() or text.strip()
