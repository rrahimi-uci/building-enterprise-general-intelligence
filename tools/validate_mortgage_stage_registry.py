#!/usr/bin/env python3
"""Validate the cumulative mortgage checkpoint registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    registry = json.loads((root / "config" / "mortgage_stages.json").read_text(encoding="utf-8"))
    stages = registry["stages"]
    errors: list[str] = []
    if len(stages) != 28:
        errors.append(f"expected 28 checkpoint entries, found {len(stages)}")
    if registry.get("anchor_case_id") != "MORT-2026-000184":
        errors.append("anchor_case_id must be MORT-2026-000184")

    seen: set[str] = set()
    implemented: list[str] = []
    for expected_chapter, stage in enumerate(stages, start=1):
        stage_id = stage.get("id")
        if stage_id in seen:
            errors.append(f"duplicate checkpoint {stage_id}")
        seen.add(stage_id)
        if stage_id != f"C{expected_chapter:02d}":
            errors.append(f"checkpoint {stage_id!r} is not aligned to chapter {expected_chapter}")
        if stage.get("chapter") != expected_chapter:
            errors.append(f"{stage_id}: chapter number does not match its position")
        if stage.get("status") == "implemented":
            implemented.append(stage_id)
            module = stage.get("module", "")
            module_name, separator, function_name = module.partition(":")
            if not separator or not function_name:
                errors.append(f"{stage_id}: implemented entry must be module:function")
            else:
                module_path = root.joinpath(*module_name.split("."))
                module_path = module_path.with_suffix(".py")
                if not module_path.exists():
                    errors.append(f"{stage_id}: missing module {module_path.relative_to(root)}")
            for field in ("entry_point", "scenarios", "tests", "technologies"):
                if not stage.get(field):
                    errors.append(f"{stage_id}: missing {field}")
            for test in stage.get("tests", []):
                if not (root / test).exists():
                    errors.append(f"{stage_id}: missing test {test}")
        elif stage.get("status") != "planned":
            errors.append(f"{stage_id}: status must be implemented or planned")

    if implemented != registry.get("implemented_checkpoints"):
        errors.append("implemented_checkpoints does not match stage statuses")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(json.dumps({"pass": True, "checkpoints": 28, "implemented": implemented}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
