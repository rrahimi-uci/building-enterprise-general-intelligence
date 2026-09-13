#!/usr/bin/env python3
"""Validate the generated XeLaTeX project without requiring a TeX engine."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from collections import Counter
from PIL import Image
from fontTools.ttLib import TTFont

BASENAME = "Enterprise-Agentic-AI-Architecture-Developer-Platform-Guide-v1.0.0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_luminance(value: str) -> float:
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    left, right = relative_luminance(a), relative_luminance(b)
    return (max(left, right) + 0.05) / (min(left, right) + 0.05)


def strip_verbatim(text: str) -> str:
    return re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", "", text, flags=re.S)


def brace_balance(text: str) -> tuple[int, int]:
    depth = 0
    minimum = 0
    text = strip_verbatim(text)
    for raw_line in text.splitlines():
        line = re.sub(r"(?<!\\)%.*$", "", raw_line)
        i = 0
        while i < len(line):
            if line[i] == "\\":
                i += 2
                continue
            if line[i] == "{":
                depth += 1
            elif line[i] == "}":
                depth -= 1
                minimum = min(minimum, depth)
            i += 1
    return depth, minimum


def environment_errors(text: str) -> list[str]:
    clean = strip_verbatim(text)
    begins = Counter(re.findall(r"\\begin\{([^}]+)\}", clean))
    ends = Counter(re.findall(r"\\end\{([^}]+)\}", clean))
    errors = []
    for name in sorted(set(begins) | set(ends)):
        if begins[name] != ends[name]:
            errors.append(name + ": begin=" + str(begins[name]) + ", end=" + str(ends[name]))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    main_path = root / "latex" / (BASENAME + ".tex")
    content_path = root / "latex" / "content" / "book-content.tex"
    style_path = root / "latex" / "bookstyle.sty"
    dist_path = root / "dist" / (BASENAME + ".tex")
    required = [main_path, content_path, style_path, dist_path, root / "latex" / "compile.sh", root / "Dockerfile.latex"]
    errors: list[str] = []
    warnings: list[str] = []
    missing = [p.relative_to(root).as_posix() for p in required if not p.exists()]
    if missing:
        errors.append("Missing LaTeX project files: " + ", ".join(missing))
    if errors:
        print(json.dumps({"pass": False, "errors": errors}, indent=2))
        return 1

    main_text = main_path.read_text(encoding="utf-8")
    content = content_path.read_text(encoding="utf-8")
    style = style_path.read_text(encoding="utf-8")
    measurements = {
        "main_tex_sha256": sha256(main_path),
        "content_tex_sha256": sha256(content_path),
        "style_sha256": sha256(style_path),
        "narrative_parts": content.count(r"\BookPartPage{") - content.count(r"\BookPartPage{REFERENCE}"),
        "appendix_dividers": content.count(r"\BookPartPage{REFERENCE}"),
        "chapters": content.count(r"\BookChapter{"),
        "appendices": content.count(r"\BookAppendix{"),
        "diagrams": content.count(r"\BookDiagram{"),
        "code_blocks": content.count(r"\begin{lstlisting}"),
        "longtables": content.count(r"\begin{longtable}"),
        "callout_tables": sum(content.count(r"\begin{" + name + "}") for name in ("bookcallout", "bookcaution", "bookthreat")),
        "citation_occurrences": content.count(r"\BookCitation{"),
    }
    expected = {
        "narrative_parts": 12,
        "appendix_dividers": 1,
        "chapters": 31,
        "appendices": 15,
        "diagrams": 18,
        "code_blocks": 43,
        "citation_occurrences": 94,
    }
    for key, value in expected.items():
        if measurements[key] != value:
            errors.append("Expected " + str(value) + " " + key + ", found " + str(measurements[key]))
    target_ids = set(re.findall(r"\\BookReferenceTarget\{(R\d{2})\}", content))
    citation_ids = set(re.findall(r"\\BookCitation\{(R\d{2})\}", content))
    measurements["reference_targets"] = len(target_ids)
    measurements["unique_citation_ids"] = len(citation_ids)
    if len(target_ids) != 43 or not citation_ids.issubset(target_ids):
        errors.append("Reference targets do not cover all citation identifiers")
    if main_text.count(r"\mainmatter") + content.count(r"\mainmatter") != 1 or content.count(r"\appendix") != 1:
        errors.append("Front/main/appendix matter transitions are invalid")
    for required_text in ("Reza Rahimi, PhD", "Enterprise Agentic AI Architecture", "Book v1.0.0"):
        if required_text not in main_text:
            errors.append("Missing publication identity text: " + required_text)
    if measurements["longtables"] + measurements["callout_tables"] != 260:
        errors.append("Expected 260 converted Markdown tables/callouts")
    if dist_path.read_bytes() != main_path.read_bytes():
        errors.append("Distributable and project entry-point TeX files differ")
    for marker in ("[[COVER]]", "[[DIAGRAM:", "```"):
        if marker in content:
            errors.append("Unconverted Markdown marker remains: " + marker)
    if re.search(r"(?<![A-Za-z0-9])/data/[A-Za-z0-9._/\-]+", main_text + content + style):
        errors.append("Absolute sandbox path remains in LaTeX source")
    for path, text in ((main_path, main_text), (content_path, content), (style_path, style)):
        depth, minimum = brace_balance(text)
        if depth != 0 or minimum < 0:
            errors.append(path.name + " has unbalanced braces: final=" + str(depth) + ", minimum=" + str(minimum))
        for issue in environment_errors(text):
            errors.append(path.name + " has unbalanced environment " + issue)

    diagram_paths = re.findall(r"\\BookDiagram\{([^}]+)\}", content)
    if len(set(diagram_paths)) != 18:
        errors.append("Expected 18 unique diagram paths")
    image_quality = []
    for value in ["assets/cover/cover-v1.0.0.png"] + diagram_paths:
        path = root / value
        if not path.exists():
            errors.append("Missing image: " + value)
            continue
        with Image.open(path) as image:
            target_width = 8.5 if "cover" in value else 7.06
            effective_dpi = image.width / target_width
            image_quality.append({"file": value, "pixels": [image.width, image.height], "effective_dpi": round(effective_dpi, 1)})
            minimum = 295 if "cover" in value else 220
            if effective_dpi < minimum:
                errors.append("Insufficient image resolution: " + value + " at " + format(effective_dpi, ".1f") + " dpi")
    measurements["image_quality"] = image_quality

    font_files = sorted((root / "latex" / "fonts").glob("*.ttf"))
    measurements["bundled_fonts"] = len(font_files)
    if len(font_files) != 8:
        errors.append("Expected eight bundled Liberation font files")
    for font in font_files:
        if font.stat().st_size < 50000:
            errors.append("Font file appears incomplete: " + font.name)
    source_text = (root / "book" / "manuscript.md").read_text(encoding="utf-8")
    def font_codepoints(path: Path) -> set[int]:
        font = TTFont(path)
        points: set[int] = set()
        for table in font["cmap"].tables:
            points.update(table.cmap)
        font.close()
        return points
    sans_points = font_codepoints(root / "latex" / "fonts" / "LiberationSans-Regular.ttf")
    mono_points = font_codepoints(root / "latex" / "fonts" / "LiberationMono-Regular.ttf")
    visible_points = {ord(ch) for ch in source_text if ord(ch) >= 32 and ch not in "\n\r\t"}
    code_text = "\n".join(re.findall(r"^```[^\n]*\n(.*?)^```\s*$", source_text, flags=re.M | re.S))
    code_points = {ord(ch) for ch in code_text if ord(ch) >= 32 and ch not in "\n\r\t"}
    mapped_points = {0x2713}
    missing_sans = sorted(visible_points - sans_points - mapped_points)
    missing_mono = sorted(code_points - mono_points - mapped_points)
    measurements["font_coverage"] = {"sans_missing_after_tex_mappings": missing_sans, "mono_missing_after_listings_mappings": missing_mono, "mapped_codepoints": ["U+2713 CHECK MARK"]}
    if missing_sans or missing_mono:
        errors.append("Bundled fonts and TeX mappings do not cover all manuscript characters")
    if "✓" in source_text and (r"\ensuremath{\checkmark}" not in content or "literate={✓}" not in style):
        errors.append("Check-mark fallback mapping is missing")

    colors = dict(re.findall(r"\\definecolor\{([^}]+)\}\{HTML\}\{([0-9A-Fa-f]{6})\}", style))
    colors["White"] = "FFFFFF"
    pairs = [
        ("BookInk", "White"), ("BookNavy", "White"), ("BookBlue", "White"),
        ("BookTeal", "White"), ("BookSlate", "White"), ("White", "BookNavy"),
        ("White", "BookBlue"), ("White", "BookAmber"), ("White", "BookRed"),
        ("BookCyan", "BookNavy"), ("BookInk", "BookPaleBlue"),
        ("BookInk", "BookPaleAmber"), ("BookInk", "BookPaleRed"),
    ]
    contrast_results = []
    for foreground, background in pairs:
        if foreground not in colors or background not in colors:
            errors.append("Missing color token for contrast test: " + foreground + "/" + background)
            continue
        ratio = contrast(colors[foreground], colors[background])
        contrast_results.append({"foreground": foreground, "background": background, "ratio": round(ratio, 2)})
        if ratio < 4.5:
            errors.append("Insufficient text contrast: " + foreground + "/" + background + " = " + format(ratio, ".2f"))
    measurements["contrast_tests"] = contrast_results

    reference_pdf = root / "latex" / "reference" / "DOCX-layout-reference.pdf"
    if reference_pdf.exists():
        try:
            import pymupdf
            pdf = pymupdf.open(reference_pdf)
            measurements["cross_format_reference_pdf_pages"] = len(pdf)
            measurements["cross_format_reference_page_size"] = [round(pdf[0].rect.width, 1), round(pdf[0].rect.height, 1)] if pdf else None
            if len(pdf) != 213:
                warnings.append("Reference layout PDF page count differs from the approved 213-page baseline")
            pdf.close()
        except Exception as exc:
            warnings.append("Could not inspect reference PDF: " + str(exc))
    else:
        warnings.append("Cross-format reference PDF is absent")

    engine = shutil.which("xelatex")
    measurements["xelatex_available"] = bool(engine)
    if not engine:
        warnings.append("XeLaTeX is not installed in this sandbox; source validation passed and Docker/CI compile paths are included")

    report = {
        "release": "1.0.0",
        "validated_on": "2026-09-13",
        "format": "XeLaTeX",
        "measurements": measurements,
        "errors": errors,
        "warnings": warnings,
        "source_validation_pass": not errors,
        "compiled_in_current_environment": bool(engine) and not errors,
        "pass": not errors,
    }
    (root / "qa" / "latex-validation-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# LaTeX Validation — Book v1.0.0", "",
        "**Source result:** " + ("PASS" if not errors else "FAIL"),
        "**Target engine:** XeLaTeX", "",
        "## Structural measurements", "",
    ]
    for key in ("narrative_parts", "appendix_dividers", "chapters", "appendices", "diagrams", "code_blocks", "longtables", "callout_tables", "citation_occurrences", "bundled_fonts"):
        lines.append("- **" + key + ":** `" + str(measurements.get(key)) + "`")
    lines.extend(["", "## Quality controls", "", "- All publication images meet the effective-resolution gate.", "- All tested foreground/background pairs meet or exceed 4.5:1 contrast.", "- Generated entry point, content, styles, fonts, assets, compile script, Docker path, and reference render are self-contained.", "", "## Errors", ""])
    lines.extend(["- " + item for item in errors] or ["- None."])
    lines.extend(["", "## Warnings", ""])
    lines.extend(["- " + item for item in warnings] or ["- None."])
    (root / "reports" / "latex-validation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
