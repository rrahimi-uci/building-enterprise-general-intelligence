#!/usr/bin/env python3
"""Render every diagram from its editable source to vector PDF and raster PNG.

Two outputs, because the two editions need different things:

  * PDF  -- vector, embedded by XeLaTeX. Stays sharp at any zoom and in print,
            which a 1800px raster does not.
  * PNG  -- raster at 300 dpi, because python-docx cannot embed PDF or SVG.

The source is the artifact a contributor edits; both renders are generated and
must never be hand-touched. Graphviz sources (.gv) get the shared house style
from `_theme.gv` spliced in at render time, so restyling the book is one edit.
Mermaid sources (.mmd) carry their theme in `_theme.mermaid.json`.

Idempotent by content: a render that would not change the pixels leaves the file
alone, because PDF and PNG encoders are not byte-reproducible across toolchain
builds and rewriting would churn the recorded digests on nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Publication width for a full-bleed figure, from the design system.
PUBLICATION_WIDTH_INCHES = 6.85
MINIMUM_DPI = 255
RENDER_DPI = 300


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def splice_theme(source: str, theme: str) -> str:
    """Insert the shared defaults just inside the graph's opening brace."""
    match = re.search(r"(digraph\s+[^\{]*\{)", source)
    if not match:
        raise ValueError("not a digraph source")
    body = "\n".join(l for l in theme.splitlines() if not l.strip().startswith("//"))
    return source[:match.end()] + "\n" + body + "\n" + source[match.end():]


def render_graphviz(source: Path, theme: Path, pdf: Path, png: Path) -> None:
    spliced = splice_theme(source.read_text(encoding="utf-8"), theme.read_text(encoding="utf-8"))
    with tempfile.NamedTemporaryFile("w", suffix=".gv", delete=False) as handle:
        handle.write(spliced)
        staged = Path(handle.name)
    try:
        subprocess.run(["dot", "-Tpdf", str(staged), "-o", str(pdf)], check=True, capture_output=True)
        subprocess.run(["dot", "-Tpng", f"-Gdpi={RENDER_DPI}", str(staged), "-o", str(png)],
                       check=True, capture_output=True)
    finally:
        staged.unlink(missing_ok=True)


def render_mermaid(source: Path, config: Path, pdf: Path, png: Path) -> None:
    with tempfile.TemporaryDirectory() as work:
        svg = Path(work) / "out.svg"
        command = ["mmdc", "-i", str(source), "-o", str(svg), "-b", "white"]
        if config.exists():
            command += ["-c", str(config)]
        subprocess.run(command, check=True, capture_output=True)
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf), str(svg)],
                       check=True, capture_output=True)
        # Width in pixels, not a dpi flag: rsvg's dpi applies to the SVG's own
        # units, and mermaid emits a pixel viewBox, so ask for the width we want.
        width = int(PUBLICATION_WIDTH_INCHES * RENDER_DPI)
        subprocess.run(["rsvg-convert", "-f", "png", "-w", str(width), "-o", str(png), str(svg)],
                       check=True, capture_output=True)


def identical_png(candidate: Path, existing: Path) -> bool:
    if not existing.exists():
        return False
    try:
        from PIL import Image
        with Image.open(candidate) as a, Image.open(existing) as b:
            return a.convert("RGB").tobytes() == b.convert("RGB").tobytes()
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--only", help="render a single diagram id")
    parser.add_argument("--check", action="store_true", help="verify without rendering")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    source_dir = root / "assets" / "diagrams" / "src"
    theme = source_dir / "_theme.gv"
    mermaid_config = source_dir / "_theme.mermaid.json"

    for binary in ("dot", "rsvg-convert"):
        if shutil.which(binary) is None:
            print(json.dumps({"pass": False, "errors": [f"{binary} is not installed"]}, indent=2))
            return 1

    registry = json.loads((root / "config" / "diagrams.json").read_text(encoding="utf-8"))
    records, errors = [], []

    for entry in registry["diagrams"]:
        diagram_id = entry["id"]
        if args.only and args.only != diagram_id:
            continue
        source = next((source_dir / f"{diagram_id}{ext}" for ext in (".gv", ".mmd")
                       if (source_dir / f"{diagram_id}{ext}").exists()), None)
        if source is None:
            errors.append(f"{diagram_id}: no editable source in assets/diagrams/src/")
            continue
        png = root / entry["file"]
        pdf = png.with_suffix(".pdf")

        if not args.check:
            with tempfile.TemporaryDirectory() as work:
                staged_pdf, staged_png = Path(work) / "d.pdf", Path(work) / "d.png"
                try:
                    if source.suffix == ".gv":
                        render_graphviz(source, theme, staged_pdf, staged_png)
                    else:
                        render_mermaid(source, mermaid_config, staged_pdf, staged_png)
                except subprocess.CalledProcessError as failure:
                    errors.append(f"{diagram_id}: render failed -- "
                                  + failure.stderr.decode()[-200:].strip())
                    continue
                if not identical_png(staged_png, png):
                    shutil.copy2(staged_png, png)
                    shutil.copy2(staged_pdf, pdf)

        if not png.exists():
            errors.append(f"{diagram_id}: missing {entry['file']}")
            continue
        from PIL import Image
        with Image.open(png) as image:
            width, height = image.size
        dpi = width / PUBLICATION_WIDTH_INCHES
        if dpi < MINIMUM_DPI:
            errors.append(f"{diagram_id}: {dpi:.0f} dpi at {PUBLICATION_WIDTH_INCHES}in "
                          f"is below the {MINIMUM_DPI} dpi contract")
        records.append({"id": diagram_id, "source": source.name, "pixels": [width, height],
                        "effective_dpi": round(dpi), "vector": pdf.exists(),
                        "sha256": sha256(png)})

    report = {"diagrams": len(records), "with_vector": sum(1 for r in records if r["vector"]),
              "records": records, "errors": errors, "pass": not errors}
    (root / "reports" / "diagram-render-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
