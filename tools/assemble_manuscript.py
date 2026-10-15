#!/usr/bin/env python3
"""Assemble the canonical Markdown book from ordered part files.

Canonical editable sources live in source/parts. This assembler also renders
Appendix I -- the reference list -- from config/references.json so citation metadata has one machine-readable source
of truth, expands [[EXAMPLE:id]] markers from config/examples.json so every
code listing in the book is the exact text of a file that CI executes, writes
the index in place of [[INDEX]] from config/index-terms.json, and resolves the
{{BUILD_DATE}} token to the build month.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

import book_index
from build_info import BUILD_DATE_TOKEN, build_date


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_section(text: str, start_heading: str, replacement: str) -> str:
    """Replace one H1 section, from its heading to the next H1."""
    start = text.find(start_heading)
    if start < 0:
        raise ValueError(f"Missing section heading: {start_heading!r}")
    end = text.find("\n# ", start + len(start_heading))
    if end < 0:
        raise ValueError(f"Section {start_heading!r} has no following H1")
    return text[:start] + replacement.rstrip() + "\n\n" + text[end + 1:]


def accessed(r: dict) -> str:
    """Format the recorded verification date, e.g. 2026-09-13 -> 13 September 2026."""
    months = ("January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December")
    year, month, day = (int(x) for x in r["verification"]["checked_on"].split("-"))
    return f"{day} {months[month - 1]} {year}"


def short_version(r: dict) -> str:
    """The edition or version, without the file-level pointers some entries keep."""
    version = str(r["publication_or_version"])
    return version.split(":", 1)[0] if version.startswith("Repository at commit") else version


def reference_line(r: dict) -> str:
    """One concise entry: who, when, what, which version, where, verified when."""
    title = r["title"] if r["title"].endswith(("?", "!")) else r["title"] + "."
    return (f"* **[{r['id']}]** {r['author_or_organization']} ({r['year']}). *{title}* "
            f"{short_version(r)}. [Source]({r['url']}). Accessed {accessed(r)}.")


def render_reference_sections(text: str, references: list[dict]) -> str:
    category_order = [
        ("Research foundations", {"research"}),
        ("Protocols and technical standards", {"protocol specification", "internet standard", "standard", "observability standard"}),
        ("Security, governance, law, and assurance", {"official guidance", "community guidance", "community standard", "management system standard", "law", "official legal guidance"}),
        ("Frameworks, evaluation, and industry implementation guidance", {"framework documentation", "framework release", "vendor documentation", "industry guidance", "industry report", "architecture pattern"}),
    ]
    ref_lines = [
        "# Appendix I — References", "", "## Citation policy", "",
        "References are numbered by stable registry identifier and grouped by kind of source, so a standard, official guidance, vendor documentation, research, and law are never presented as equivalent authority. Each citation supports only a narrow claim; that permitted scope is recorded in the book's source registry and checked at every build. Access dates record when online material was last verified.", "",
    ]
    seen = set()
    for heading, types in category_order:
        group = [r for r in references if r["type"] in types and r["id"] not in seen]
        if not group:
            continue
        ref_lines += ["## " + heading, ""]
        for r in group:
            seen.add(r["id"])
            ref_lines.append(reference_line(r))
        ref_lines.append("")
    for r in references:
        if r["id"] not in seen:
            ref_lines.append(reference_line(r))
    # The permitted scope of each source stays in the registry, where the
    # citation checker enforces it; printing it made every entry a paragraph.
    text = replace_section(text, "# Appendix I — References", "\n".join(ref_lines))
    return text


EXAMPLE_MARKER = re.compile(r"^\[\[EXAMPLE:([a-z0-9][a-z0-9-]*)(?:#([a-z0-9-]+))?\]\]$", re.M)


def example_region(body: str, start: str, end: str, region: str | None) -> str:
    """Return the whole example region, or one named sub-region within it.

    Named regions let a single verified file serve two chapters at two depths --
    the agent-step contracts a foundations chapter needs, and the full platform
    contract set the architecture chapter needs -- without a second copy that can
    drift. Earlier drafts had exactly that duplication.
    """
    if region:
        open_marker = f"# --8<-- region:{region}"
        close_marker = f"# --8<-- endregion:{region}"
        if open_marker not in body:
            raise SystemExit(f"Example region {region!r} not found")
        if close_marker not in body:
            raise SystemExit(f"Example region {region!r} is never closed")
        body = body.split(open_marker, 1)[1].split(close_marker, 1)[0]
    elif start in body:
        if end not in body:
            raise SystemExit("Example region start without a matching end")
        body = body.split(start, 1)[1].split(end, 1)[0]
    # Drop any nested region markers so they never reach the page.
    lines = [l.rstrip() for l in body.splitlines() if "# --8<--" not in l]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def expand_examples(text: str, root: Path) -> tuple[str, int]:
    """Replace each [[EXAMPLE:id]] with the live source of that example.

    Expanding at assembly time, rather than in each renderer, is what keeps the
    Markdown, DOCX, and LaTeX editions byte-consistent: they all consume the one
    manuscript that already has the real code in it. It also means a listing in
    the book cannot drift from the file CI runs -- there is only one copy.
    """
    registry = json.loads((root / "config" / "examples.json").read_text(encoding="utf-8"))
    start = registry["region_markers"]["start"]
    end = registry["region_markers"]["end"]
    by_id = {e["id"]: e for e in registry["examples"]}
    count = 0

    def render(match: re.Match[str]) -> str:
        nonlocal count
        entry = by_id.get(match.group(1))
        if entry is None:
            raise SystemExit(f"[[EXAMPLE:{match.group(1)}]] is not in config/examples.json")
        path = root / entry["path"]
        if not path.exists():
            raise SystemExit(f"Example {entry['id']} points at missing file {entry['path']}")
        rendered = example_region(path.read_text(encoding="utf-8"), start, end, match.group(2))
        if not rendered.strip():
            raise SystemExit(f"Example {entry['id']} rendered empty")
        language = entry.get("language", "python")
        count += 1
        # The caption is the title alone. The language is shown once, on the
        # code panel's tab (a snake for Python), which every renderer builds
        # from the fence; repeating it in the caption printed it twice.
        return "\n".join([entry["title"], "", "```" + language, rendered, "```"])

    return EXAMPLE_MARKER.sub(render, text), count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    parts_dir = root / "source" / "parts"
    parts = sorted(parts_dir.glob("*.md"))
    if not parts:
        raise SystemExit(f"No Markdown sources found in {parts_dir}")
    expected_prefixes = ["00-"] + [f"{i:02d}-" for i in range(1, 10)]
    if len(parts) != 10 or any(not p.name.startswith(prefix) for p, prefix in zip(parts, expected_prefixes)):
        raise SystemExit("Expected ordered files 00-* through 09-*; update this guard intentionally when book topology changes.")

    manuscript = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in parts) + "\n"
    refs_doc = json.loads((root / "config" / "references.json").read_text(encoding="utf-8"))
    refs = refs_doc["references"]
    manuscript = render_reference_sections(manuscript, refs)
    manuscript, example_count = expand_examples(manuscript, root)
    if manuscript.count(BUILD_DATE_TOKEN) != 1:
        raise SystemExit(f"Expected one {BUILD_DATE_TOKEN} token on the title page")
    manuscript = manuscript.replace(BUILD_DATE_TOKEN, build_date())
    if manuscript.count(book_index.INDEX_MARKER) != 1:
        raise SystemExit(f"Expected one {book_index.INDEX_MARKER} marker")
    index_entries = book_index.load_terms(root, manuscript)
    found = book_index.scan(manuscript, index_entries, book_index.excluded_units(root))
    manuscript = manuscript.replace(book_index.INDEX_MARKER, book_index.render_markdown(found, index_entries))

    canonical = root / "book" / "manuscript.md"
    distribution = root / "dist" / "Enterprise-General-Intelligence-v1.0.0.md"
    canonical.parent.mkdir(parents=True, exist_ok=True)
    distribution.parent.mkdir(parents=True, exist_ok=True)
    canonical.write_text(manuscript, encoding="utf-8", newline="\n")
    distribution.write_text(manuscript, encoding="utf-8", newline="\n")

    ids = sorted(set(re.findall(r"\[(R\d{2})\]", manuscript)))
    report = {
        "canonical_source": "source/parts/*.md",
        "ordered_parts": [p.relative_to(root).as_posix() for p in parts],
        "bytes": len(manuscript.encode("utf-8")),
        "sha256": sha256_bytes(manuscript.encode("utf-8")),
        "parts": len(re.findall(r"^# PART [IVXLCDM]+ — ", manuscript, re.M)),
        "chapters": len(re.findall(r"^# \d{2} — ", manuscript, re.M)),
        "appendices": len(re.findall(r"^# Appendix ", manuscript, re.M)),
        "citation_occurrences": len(re.findall(r"\[R\d{2}\]", manuscript)),
        "expanded_examples": example_count,
        "build_date": build_date(),
        "index_terms": sum(1 for units in found.values() if units),
        "index_locators": sum(len(units) for units in found.values()),
        "cited_reference_ids": ids,
    }
    (root / "reports" / "assembly-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
