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

Classification reads *only the leading bold marker*, never the body. Matching
anywhere in the body is how an `**EVIDENCE BOUNDARY**` note whose text mentions
"threat model" came out as a red Threat box, and how twelve `**PROBLEM**`
callouts lost their label to a generic "Architecture note".
"""
from __future__ import annotations

import re

# marker -> (latex environment, docx shading, printed title)
KINDS: dict[str, tuple[str, str, str]] = {
    # --- guidance boxes, introduced in v2.0.0 ---------------------------
    "BEST PRACTICE": ("bookbestpractice", "E7F5F3", "Best practice"),
    "ARCHITECTURE GUIDANCE": ("bookarchitecture", "EAF3FB", "Architecture guidance"),
    "DEVELOPER GUIDELINE": ("bookdeveloper", "EDF3FC", "Developer guideline"),
    "PRODUCTION CONSIDERATION": ("bookproduction", "F7ECF8", "Production consideration"),
    "SECURITY AND GOVERNANCE": ("booksecurity", "FCECEC", "Security and governance"),
    "COMMON PITFALL": ("bookantipattern", "FFF4DF", "Common pitfall"),
    "ANTI-PATTERN": ("bookantipattern", "FFF4DF", "Anti-pattern"),
    "PERFORMANCE AND COST": ("bookcost", "F6F5E3", "Performance and cost"),
    "OBSERVABILITY TIP": ("bookobservability", "E6F5F9", "Observability tip"),
    # --- narrative and evidence callouts carried over from v1.0.0 -------
    "NORTHSTAR AT THIS POINT": ("bookcallout", "EAF3FB", "Northstar at this point"),
    "NORTH-STAR RULE": ("bookcallout", "EAF3FB", "North-star rule"),
    "DESIGN DECISION": ("bookcallout", "EAF3FB", "Design decision"),
    "IMPLEMENTATION NOTE": ("bookcallout", "EAF3FB", "Implementation note"),
    "SOURCE DISCIPLINE": ("bookcallout", "EAF3FB", "Source discipline"),
    "PROBLEM": ("bookcallout", "EAF3FB", "The problem"),
    "THE PRODUCTION STANDARD": ("bookcallout", "EAF3FB", "The production standard"),
    # An evidence boundary is a caveat about what the evidence supports. It is
    # emphatically not a threat; the two were conflated until this was fixed.
    "EVIDENCE BOUNDARY": ("bookcaution", "FFF4DF", "Evidence boundary"),
    "EVIDENCE CAVEAT": ("bookcaution", "FFF4DF", "Evidence caveat"),
    "CAUTION": ("bookcaution", "FFF4DF", "Caution"),
    "THREAT": ("bookthreat", "FCECEC", "Threat"),
}

DEFAULT = ("bookcallout", "EAF3FB", "Architecture note")

# The eight guidance kinds, for validators reporting adoption.
GUIDANCE_MARKERS = [
    "BEST PRACTICE", "ARCHITECTURE GUIDANCE", "DEVELOPER GUIDELINE",
    "PRODUCTION CONSIDERATION", "SECURITY AND GOVERNANCE", "COMMON PITFALL",
    "PERFORMANCE AND COST", "OBSERVABILITY TIP",
]

# Every environment the LaTeX renderer can emit, for the validators to count.
ENVIRONMENTS = sorted({v[0] for v in KINDS.values()} | {DEFAULT[0]})

# A bold run at the very start of the callout body, and nowhere else.
_LEADING_MARKER = re.compile(r"^\s*\*\*([^*]{1,80})\*\*[\s:.—-]*")

# Longer than this and the bold run is a sentence the author emphasised, not a
# label. Two such runs exist in the book; they stay in the body untouched.
_MAX_TITLE = 48


def _leading_marker(text: str) -> str | None:
    match = _LEADING_MARKER.match(text)
    return match.group(1).strip() if match else None


def _key(marker: str) -> str:
    return re.sub(r"\s+", " ", marker).upper()


def classify(text: str) -> tuple[str, str, str]:
    """Return (latex_environment, docx_fill, title) from the leading marker.

    An unrecognized marker keeps its own text as the box title rather than being
    relabelled: losing an author's label is worse than not having a dedicated
    style for it.
    """
    marker = _leading_marker(text)
    if marker is None:
        return DEFAULT
    kind = KINDS.get(_key(marker))
    if kind is not None:
        return kind
    if len(marker) <= _MAX_TITLE:
        return DEFAULT[0], DEFAULT[1], marker.title()
    return DEFAULT


def strip_marker(text: str) -> str:
    """Remove the leading marker only when it became the box title.

    A bold run too long to be a title stays in the body, because the rendered box
    would otherwise drop the sentence entirely.
    """
    marker = _leading_marker(text)
    if marker is None:
        return text.strip()
    if _key(marker) in KINDS or len(marker) <= _MAX_TITLE:
        return _LEADING_MARKER.sub("", text, count=1).strip() or text.strip()
    return text.strip()
