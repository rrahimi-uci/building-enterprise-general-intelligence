#!/usr/bin/env python3
"""Assemble the canonical Markdown book from ordered part files.

Canonical editable sources live in source/parts. This assembler also renders
Appendix K and Appendix M from config/references.json so citation metadata has
one machine-readable source of truth, and expands [[EXAMPLE:id]] markers from
config/examples.json so every code listing in the book is the exact text of a
file that CI executes.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_between(text: str, start_heading: str, end_heading: str, replacement: str) -> str:
    start = text.find(start_heading)
    end = text.find(end_heading, start + len(start_heading))
    if start < 0 or end < 0:
        raise ValueError(f"Missing section boundary: {start_heading!r} -> {end_heading!r}")
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


def render_reference_sections(text: str, references: list[dict]) -> str:
    category_order = [
        ("Research foundations", {"research"}),
        ("Protocols, identity, and event standards", {"protocol specification", "internet standard", "standard", "observability standard"}),
        ("Security, governance, law, and assurance", {"official guidance", "community guidance", "community standard", "law", "official legal guidance"}),
        ("Frameworks, evaluation, and industry implementation guidance", {"framework documentation", "framework release", "vendor documentation", "industry guidance", "industry report", "architecture pattern"}),
    ]
    ref_lines = [
        "# Appendix K — References", "", "## Citation policy", "",
        "References are numbered by stable registry identifier. Each citation supports only the scoped claim recorded in `config/references.json`; access dates document the verification point for online material. Standards, official guidance, community guidance, vendor documentation, research, and law are deliberately labeled rather than treated as equivalent authority.", "",
    ]
    seen = set()
    for heading, types in category_order:
        group = [r for r in references if r["type"] in types and r["id"] not in seen]
        if not group:
            continue
        ref_lines += ["## " + heading, ""]
        for r in group:
            seen.add(r["id"])
            ref_lines.append(f"* **[{r['id']}]** {r['author_or_organization']} ({r['year']}). *{r['title']}*. {r['publication_or_version']}. [Primary or authoritative source]({r['url']}). Accessed 13 September 2026. **Supports:** {r['supports']}")
        ref_lines.append("")
    for r in references:
        if r["id"] not in seen:
            ref_lines.append(f"* **[{r['id']}]** {r['author_or_organization']} ({r['year']}). *{r['title']}*. {r['publication_or_version']}. [Source]({r['url']}). Accessed 13 September 2026. **Supports:** {r['supports']}")
    text = replace_between(text, "# Appendix K — References", "# Appendix L —", "\n".join(ref_lines))

    trace_lines = [
        "# Appendix M — Citation and Claim Traceability Matrix", "",
        "This matrix defines exactly what each citation is permitted to support. It prevents a source from being stretched beyond its evidence. Book-authored patterns, metrics, formulas, examples, and architecture recommendations remain design guidance unless a source explicitly covers them.", "",
        "| ID | Source class | Permitted claim scope | Verification note |", "|---|---|---|---|",
    ]
    for r in references:
        scope = str(r["supports"]).replace("|", "\\|")
        trace_lines.append(f"| {r['id']} | {r['type']} | {scope} | Verified {r['verification']['checked_on']}; re-check living sources before use. |")
    text = replace_between(text, "# Appendix M — Citation and Claim Traceability Matrix", "# Appendix N —", "\n".join(trace_lines))
    return text


EXAMPLE_MARKER = re.compile(r"^\[\[EXAMPLE:([a-z0-9][a-z0-9-]*)\]\]$", re.M)


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
        body = path.read_text(encoding="utf-8")
        if start in body:
            if end not in body:
                raise SystemExit(f"Example {entry['id']}: region start without a matching end")
            body = body.split(start, 1)[1].split(end, 1)[0]
        lines = [line.rstrip() for line in body.splitlines()]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        language = entry.get("language", "python")
        count += 1
        caption = f"{language.upper()} · {entry['title']}"
        return "\n".join([caption, "", "```" + language, *lines, "```"])

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
    expected_prefixes = ["00-"] + [f"{i:02d}-" for i in range(1, 14)]
    if len(parts) != 14 or any(not p.name.startswith(prefix) for p, prefix in zip(parts, expected_prefixes)):
        raise SystemExit("Expected ordered files 00-* through 13-*; update this guard intentionally when book topology changes.")

    manuscript = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in parts) + "\n"
    refs_doc = json.loads((root / "config" / "references.json").read_text(encoding="utf-8"))
    refs = refs_doc["references"]
    manuscript = render_reference_sections(manuscript, refs)
    manuscript, example_count = expand_examples(manuscript, root)

    canonical = root / "book" / "manuscript.md"
    distribution = root / "dist" / "Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0.md"
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
        "cited_reference_ids": ids,
    }
    (root / "reports" / "assembly-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
