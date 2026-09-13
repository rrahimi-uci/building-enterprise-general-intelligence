#!/usr/bin/env python3
"""Validate, and optionally execute, every runnable code example in the book.

Examples are real files under `examples/`, not prose. This tool is the contract
between them and the manuscript:

  * every `[[EXAMPLE:id]]` marker in source/parts resolves to a registry entry;
  * every registry entry is cited at least once, or is explicitly retained;
  * every registered file exists and its excerpt region resolves;
  * with --run, the example test suite executes and must pass.

Run it with the book virtualenv for validation. `--run` additionally needs the
examples virtualenv, which carries the pinned SDKs; pass it with --python.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = re.compile(r"\[\[EXAMPLE:([a-z0-9][a-z0-9-]*)(?:#([a-z0-9-]+))?\]\]")


def load_registry(root: Path) -> dict:
    return json.loads((root / "config" / "examples.json").read_text(encoding="utf-8"))


def excerpt(path: Path, start: str, end: str) -> str:
    """Return the region between the markers, or the whole file if absent.

    The markers let a file stay runnable -- imports, __main__ guard, helpers --
    while the book shows only the part that teaches something.
    """
    text = path.read_text(encoding="utf-8")
    if start not in text:
        return text.strip()
    body = text.split(start, 1)[1]
    if end not in body:
        raise ValueError(f"{path}: opening region marker has no matching '{end}'")
    body = body.split(end, 1)[0]
    lines = [line.rstrip() for line in body.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def markers_in_sources(root: Path) -> dict[str, list[tuple[str, str | None]]]:
    """Map example id -> [(source file, region or None)] for every citation."""
    found: dict[str, list[tuple[str, str | None]]] = {}
    for part in sorted((root / "source" / "parts").glob("*.md")):
        for match in MARKER.finditer(part.read_text(encoding="utf-8")):
            found.setdefault(match.group(1), []).append((part.name, match.group(2)))
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--run", action="store_true", help="execute the example test suite")
    parser.add_argument("--python", default=sys.executable,
                        help="interpreter that has examples/requirements.txt installed")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    registry = load_registry(root)
    start = registry["region_markers"]["start"]
    end = registry["region_markers"]["end"]
    entries = registry["examples"]

    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    rendered: dict[str, int] = {}

    for entry in entries:
        eid = entry["id"]
        if eid in seen:
            errors.append(f"duplicate example id: {eid}")
        seen.add(eid)
        path = root / entry["path"]
        if not path.exists():
            errors.append(f"{eid}: missing file {entry['path']}")
            continue
        try:
            body = excerpt(path, start, end)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not body.strip():
            errors.append(f"{eid}: excerpt region is empty")
        rendered[eid] = len(body.splitlines())
        if entry.get("verify") not in registry["verification_modes"]:
            errors.append(f"{eid}: unknown verification mode {entry.get('verify')!r}")
        for test in entry.get("tests", []):
            if not (root / test).exists():
                errors.append(f"{eid}: missing test file {test}")
        if entry.get("verify") == "test" and not entry.get("tests"):
            errors.append(f"{eid}: verify=test but no tests are declared")

    cited = markers_in_sources(root)
    by_id = {e["id"]: e for e in entries}
    for eid, citations in cited.items():
        if eid not in seen:
            errors.append(f"[[EXAMPLE:{eid}]] has no entry in config/examples.json")
            continue
        # A named region must exist in the file, or the page silently loses content.
        body = (root / by_id[eid]["path"]).read_text(encoding="utf-8")
        for source_file, region in citations:
            if region is None:
                continue
            if f"# --8<-- region:{region}" not in body:
                errors.append(f"{source_file} cites {eid}#{region}, which the file does not define")
            elif f"# --8<-- endregion:{region}" not in body:
                errors.append(f"{eid}: region {region!r} is never closed")
    for entry in entries:
        if entry["id"] not in cited and not entry.get("retained_for_future_use"):
            warnings.append(f"{entry['id']}: registered but never cited from source/parts")

    tests_passed = None
    if args.run and not errors:
        cmd = [args.python, "-m", "pytest", "examples/tests", "-q"]
        proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        tests_passed = proc.returncode == 0
        sys.stderr.write(proc.stdout[-4000:])
        if not tests_passed:
            errors.append("example test suite failed")

    report = {
        "examples": len(entries),
        "cited": len(cited),
        "uncited": [w.split(":")[0] for w in warnings],
        "rendered_lines": rendered,
        "tests_executed": bool(args.run),
        "tests_passed": tests_passed,
        "errors": errors,
        "warnings": warnings,
        "pass": not errors,
    }
    (root / "reports" / "examples-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
