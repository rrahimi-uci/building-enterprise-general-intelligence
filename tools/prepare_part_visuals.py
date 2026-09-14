#!/usr/bin/env python3
"""Crop the source Part visuals into the artwork panels the book renders.

The source visuals were authored as complete 16:9 divider pages for the v1.0.0
twelve-Part structure: each one bakes in its own PART badge, Part title, focus
statement, theme chips and a "BOOK v1.0.0" footer.

v2.0.0 has eight Parts, so five of the eight needed visuals carry the wrong
Roman numeral, and every one carries a stale release footer. Rather than ship
pixels that contradict the page they sit on, this tool keeps only the artwork
panel -- the illustration and its four numbered component labels -- and lets the
renderers draw the Part identity from the canonical Markdown, where it is
correct by construction.

Deterministic: the same source and crop box always produce the same bytes, and
the digests are recorded in config/part-visuals.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

# Minimum effective resolution at the rendered width, matching the book's
# asset contract for diagrams.
MINIMUM_DPI = 255.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def crop_box(size: tuple[int, int], box: dict) -> tuple[int, int, int, int]:
    width, height = size
    return (
        int(width * box["left"]), int(height * box["top"]),
        int(width * box["right"]), int(height * box["bottom"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--check", action="store_true",
                        help="verify existing assets without rewriting them")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    registry = json.loads((root / "config" / "part-visuals.json").read_text(encoding="utf-8"))
    box = registry["crop_box"]
    rendered_width_in = registry["rendered_width_inches"]

    records = []
    errors = []
    for entry in registry["visuals"]:
        source = root / entry["source"]
        target = root / entry["file"]
        if not source.exists():
            errors.append(f"Part {entry['part']}: missing source {entry['source']}")
            continue
        with Image.open(source) as image:
            cropped = image.convert("RGB").crop(crop_box(image.size, box))
        effective_dpi = cropped.width / rendered_width_in
        if effective_dpi < MINIMUM_DPI:
            errors.append(
                f"Part {entry['part']}: {effective_dpi:.0f} dpi at "
                f"{rendered_width_in}in is below the {MINIMUM_DPI:.0f} dpi contract"
            )
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            # optimize=True keeps the output stable for a given Pillow build and
            # holds the eight panels to a few megabytes in total.
            cropped.save(target, format="PNG", optimize=True)
        if not target.exists():
            errors.append(f"Part {entry['part']}: missing generated asset {entry['file']}")
            continue
        digest = sha256(target)
        if entry.get("sha256") and entry["sha256"] != digest:
            message = f"Part {entry['part']}: digest changed for {entry['file']}"
            (errors.append(message) if args.check else records)
        records.append({
            "part": entry["part"], "file": entry["file"], "source": entry["source"],
            "pixels": [cropped.width, cropped.height],
            "effective_dpi": round(effective_dpi, 1), "sha256": digest,
            "bytes": target.stat().st_size,
        })

    report = {
        "visuals": len(records),
        "rendered_width_inches": rendered_width_in,
        "minimum_effective_dpi": MINIMUM_DPI,
        "records": records,
        "errors": errors,
        "pass": not errors,
    }
    (root / "reports" / "part-visuals-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
