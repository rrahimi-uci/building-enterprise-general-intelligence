"""The book index: one term list, one placement rule, three renderings.

`config/index-terms.json` is the only list of indexed terms. Every renderer
places marks with the same rule, implemented once here: a term is marked at its
first mention in each chapter or appendix, in running text: paragraphs, list
items, quotations, table cells and callouts, never headings, code or figure
captions. The front
matter, Part pages, the closing perspective, the references appendix and the
glossary carry no marks.

The Markdown edition cannot know page numbers, so the assembler writes the
index with chapter and appendix locators. The XeLaTeX edition turns the same
marks into a page index with makeindex, and the DOCX edition into Word XE
fields under an INDEX field whose cached result is the Markdown list. Because
all three apply this module's rule, a locator appears in one edition exactly
when it appears in the others.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

INDEX_HEADING = "Index"
INDEX_MARKER = "[[INDEX]]"
GLOSSARY_HEADING = re.compile(r"^# Appendix ([A-Z]) — Glossary$", re.M)
CHAPTER_H1 = re.compile(r"^(\d{2}) — ")
APPENDIX_H1 = re.compile(r"^Appendix ([A-Z]) — ")


def load_terms(root: Path, manuscript: str) -> list[dict]:
    """Index entries with compiled patterns and their defining units.

    A glossary entry takes its defining chapters from the glossary table, so
    the bold locator cannot drift from the glossary's own "Chapter" column.
    """
    spec = json.loads((root / "config" / "index-terms.json").read_text(encoding="utf-8"))
    glossary = glossary_chapters(manuscript)
    entries = []
    for raw in spec["entries"]:
        defined = [f"{int(n):02d}" if str(n).isdigit() else str(n) for n in raw.get("defined_in", [])]
        if raw.get("glossary"):
            if raw["glossary"] not in glossary:
                raise SystemExit(f"Index term {raw['term']!r} names glossary entry {raw['glossary']!r}, which the glossary does not have")
            defined = glossary[raw["glossary"]]
        flags = 0 if raw.get("case_sensitive") else re.I
        phrases = "|".join(re.escape(m) for m in sorted(raw["match"], key=len, reverse=True))
        pattern = re.compile(r"(?<![\w-])(?:" + phrases + r")(?:s|es)?(?![\w])", flags)
        entries.append({
            "term": raw["term"],
            "pattern": pattern,
            "defined": defined,
            "scope": raw.get("scope", "auto"),
        })
    return sorted(entries, key=lambda e: sort_key(e["term"]))


def excluded_units(root: Path) -> set[str]:
    spec = json.loads((root / "config" / "index-terms.json").read_text(encoding="utf-8"))
    return set(spec.get("excluded_units", []))


def glossary_chapters(manuscript: str) -> dict[str, list[str]]:
    """Glossary term -> its defining chapters ("05"), from the glossary table."""
    match = GLOSSARY_HEADING.search(manuscript)
    if not match:
        return {}
    section = manuscript[match.end():]
    section = section[: section.find("\n# ")] if "\n# " in section else section
    result = {}
    for line in section.splitlines():
        row = re.match(r"^\| ([^|*][^|]*?) \| .* \| ([0-9, ]+) \|$", line)
        if row:
            result[row.group(1)] = [f"{int(n):02d}" for n in row.group(2).split(",")]
    return result


def sort_key(term: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", term.lower())


def unit_of(heading: str) -> str | None:
    """The locator unit an H1 opens: "05" for a chapter, "C" for an appendix."""
    chapter = CHAPTER_H1.match(heading)
    if chapter:
        return chapter.group(1)
    appendix = APPENDIX_H1.match(heading)
    if appendix:
        return appendix.group(1)
    return None


def plain(text: str) -> str:
    """Prose as the reader sees it: no link targets, emphasis or code ticks."""
    text = re.sub(r"\[([^\]]+)\]\(https?://[^)]+\)", r"\1", text)
    text = re.sub(r"\[R\d{2}\]", "", text)
    return text.replace("`", "").replace("*", "").replace("\\", "")


class Tracker:
    """Decides which terms to mark in each prose block, in reading order."""

    def __init__(self, entries: list[dict], excluded: set[str]):
        self.entries = entries
        self.excluded = excluded
        self.unit: str | None = None
        self.seen: set[str] = set()
        self.found: dict[str, list[str]] = {e["term"]: [] for e in entries}

    def heading(self, level: int, text: str) -> None:
        if level == 1:
            unit = unit_of(text)
            self.unit = None if unit in self.excluded else unit
            self.seen = set()

    def part(self) -> None:
        self.unit = None

    def marks(self, text: str) -> list[tuple[str, bool]]:
        """(term, defining) for each term first mentioned in this block."""
        if self.unit is None:
            return []
        prose = plain(text)
        result = []
        for entry in self.entries:
            term = entry["term"]
            if term in self.seen:
                continue
            if entry["scope"] == "defined" and self.unit not in entry["defined"]:
                continue
            if entry["pattern"].search(prose):
                self.seen.add(term)
                self.found[term].append(self.unit)
                result.append((term, self.unit in entry["defined"]))
        return result


def scan(manuscript: str, entries: list[dict], excluded: set[str]) -> dict[str, list[str]]:
    """Run the placement rule over the Markdown block structure.

    Mirrors the renderers' block parsers: a text block is a run of non-blank
    lines that is not a heading, code fence, diagram marker or cover; each table
    body row is read cell by cell as the renderers read it (header rows carry
    no marks).
    """
    tracker = Tracker(entries, excluded)
    lines = manuscript.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if line.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                i += 1
            i += 1
            continue
        if line.startswith("# PART "):
            tracker.part()
            i += 1
            while i < len(lines) and not lines[i].startswith("# "):
                i += 1
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            tracker.heading(len(heading.group(1)), heading.group(2).strip())
            i += 1
            continue
        if stripped.startswith("[["):
            i += 1
            continue
        if stripped.startswith("|"):
            # A header row names columns; only body rows carry marks.
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                for cell in re.split(r"(?<!\\)\|", lines[i].strip().strip("|")):
                    tracker.marks(cell)
                i += 1
            continue
        block = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|```|\||\[\[)", lines[i].strip()):
            block.append(lines[i].strip())
            i += 1
        tracker.marks(" ".join(block))
    return tracker.found


def locator_text(units: list[str], defined: list[str]) -> str:
    chapters = [u for u in units if u.isdigit()]
    appendices = [u for u in units if not u.isdigit()]
    def fmt(u: str) -> str:
        label = str(int(u)) if u.isdigit() else u
        return f"**{label}**" if u in defined else label
    parts = []
    if chapters:
        parts.append(", ".join(fmt(u) for u in chapters))
    if appendices:
        parts.append(("Appendix " if len(appendices) == 1 else "Appendices ") + ", ".join(fmt(u) for u in appendices))
    return "; ".join(parts)


def render_markdown(found: dict[str, list[str]], entries: list[dict]) -> str:
    """The index body written in place of [[INDEX]]."""
    lines = [
        "Numbers are chapters and letters are appendices; bold marks where a term "
        "is defined. Page numbers are in the PDF index and, once its fields are "
        "updated, in the Word index.",
        "",
    ]
    letter = None
    for entry in entries:
        units = found.get(entry["term"], [])
        if not units:
            continue
        initial = sort_key(entry["term"])[:1].upper()
        if initial != letter:
            letter = initial
            lines += ["", f"**{letter}**", ""]
        lines.append(f"- {entry['term']} — {locator_text(units, entry['defined'])}")
    return "\n".join(lines).replace("\n\n\n", "\n\n").strip()
