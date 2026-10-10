#!/usr/bin/env python3
"""Generate the XeLaTeX representation of Book v2.1.0.

The canonical Markdown remains the semantic source. This tool converts the
restricted publication Markdown vocabulary into a styled, self-contained
XeLaTeX project with bundled redistributable fonts and registered assets.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

import callouts


def chapter_covers(root: Path) -> dict[str, str]:
    """Chapter number ("01") -> cover image path, from the cover spec."""
    path = root / "config" / "chapter-covers.json"
    if not path.exists():
        return {}
    spec = json.loads(path.read_text(encoding="utf-8"))
    return {f"{c['chapter']:02d}": f"{spec['output_dir']}/{c['file']}" for c in spec["chapters"]}


def book_release(root: Path) -> str:
    """The single source of the release identifier.

    Hard-coding it meant a generated report could claim 1.0.0 while every other
    artifact said 2.0.0 -- the evidence disagreeing with the thing it certifies.
    """
    return json.loads((root / "config" / "book.json").read_text(encoding="utf-8"))["book"]["version"]


BASENAME = "Enterprise-General-Intelligence-v2.1.0"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def split_row(line: str) -> list[str]:
    text = line.strip().strip("|")
    cells: list[str] = []
    buf: list[str] = []
    escaped = False
    in_code = False
    for ch in text:
        if escaped:
            buf.append(ch)
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            buf.append(ch)
            continue
        if ch == "`":
            in_code = not in_code
            buf.append(ch)
            continue
        if ch == "|" and not in_code:
            cells.append("".join(buf).strip().replace("\\|", "|"))
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip().replace("\\|", "|"))
    return cells


def separator_row(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def parse_markdown(markdown: str):
    lines = markdown.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped == "[[COVER]]":
            yield ("cover",)
            i += 1
            continue
        diagram = re.fullmatch(r"\[\[DIAGRAM:([^|\]]+)\|(.+)\]\]", stripped)
        if diagram:
            yield ("diagram", diagram.group(1), diagram.group(2))
            i += 1
            continue
        part = re.match(r"^# PART (.+?) — (.+)$", line)
        if part:
            ident, title = part.groups()
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            intro: list[str] = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                intro.append(lines[i].strip())
                i += 1
            yield ("part", ident, title, " ".join(intro))
            continue
        if line.startswith("```"):
            language = line[3:].strip() or "text"
            code: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            if i >= len(lines):
                raise ValueError("Unclosed code fence")
            i += 1
            yield ("code", language, "\n".join(code))
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            yield ("heading", len(heading.group(1)), heading.group(2).strip())
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and separator_row(lines[i + 1]):
            rows = [split_row(line)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            yield ("table", rows)
            continue
        if re.match(r"^[-*]\s+\[[ xX]\]\s+", line):
            checked = "checked" if re.match(r"^[-*]\s+\[[xX]\]", line) else "unchecked"
            value = re.sub(r"^[-*]\s+\[[ xX]\]\s+", "", line)
            yield ("check", checked, value)
            i += 1
            continue
        if re.match(r"^[-*]\s+", line):
            text, i = list_item(lines, i, re.sub(r"^[-*]\s+", "", line))
            yield ("bullet", text)
            continue
        if re.match(r"^\d+\.\s+", line):
            text, i = list_item(lines, i, re.sub(r"^\d+\.\s+", "", line))
            yield ("number", text)
            continue
        if line.startswith("> "):
            yield ("quote", line[2:].strip())
            i += 1
            continue
        paragraph = [stripped]
        i += 1
        while i < len(lines):
            candidate = lines[i]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if candidate.startswith(("#", "```", "> ")):
                break
            if candidate_stripped.startswith("|") or candidate_stripped.startswith("[[DIAGRAM:"):
                break
            if candidate_stripped == "[[COVER]]":
                break
            if re.match(r"^[-*]\s+", candidate) or re.match(r"^\d+\.\s+", candidate):
                break
            paragraph.append(candidate_stripped)
            i += 1
        yield ("paragraph", " ".join(paragraph))


def list_item(lines: list[str], i: int, first: str) -> tuple[str, int]:
    """Join a hard-wrapped list item's indented continuation lines."""
    parts = [first.strip()]
    i += 1
    while (i < len(lines) and lines[i][:1] in (" ", "\t") and lines[i].strip()
           and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i])):
        parts.append(lines[i].strip())
        i += 1
    return " ".join(parts), i


def markdown_unescape(text: str) -> str:
    return re.sub(r"\\([\\`*_{}\[\]()#+.!|<>\-])", r"\1", text)


def escape_plain(text: str) -> str:
    text = markdown_unescape(text)
    mapping = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "✓": r"\ensuremath{\checkmark}",
        "🐍": r"\BookSnake",
    }
    segments = re.split(r"<br\s*/?>", text, flags=re.I)
    escaped = []
    for segment in segments:
        escaped.append("".join(mapping.get(ch, ch) for ch in segment))
    return r"\newline{}".join(escaped)


def inline_code(value: str) -> str:
    value = markdown_unescape(value)
    for delimiter in "!|+/;:@?":
        if delimiter not in value:
            return r"\lstinline[style=bookinline]" + delimiter + value + delimiter
    return r"\texttt{" + escape_plain(value) + "}"


def inline(text: str) -> str:
    token = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\(https?://[^)]+\)|\[R\d{2}\]|(?<!\*)\*[^*\n]+\*)")
    output: list[str] = []
    position = 0
    for match in token.finditer(text):
        if match.start() > position:
            output.append(escape_plain(text[position:match.start()]))
        value = match.group(0)
        if value.startswith("**"):
            output.append(r"\textbf{" + inline(value[2:-2]) + "}")
        elif value.startswith("`"):
            output.append(inline_code(value[1:-1]))
        elif re.match(r"^\[[^\]]+\]\(https?://", value):
            link = re.match(r"^\[([^\]]+)\]\((https?://[^)]+)\)$", value)
            if link:
                output.append(r"\href{\detokenize{" + link.group(2) + "}}{" + inline(link.group(1)) + "}")
        elif re.fullmatch(r"\[R\d{2}\]", value):
            output.append(r"\BookCitation{" + value[1:-1] + "}")
        elif value.startswith("*"):
            output.append(r"\emph{" + inline(value[1:-1]) + "}")
        position = match.end()
    if position < len(text):
        output.append(escape_plain(text[position:]))
    return "".join(output)


def render_callout(rows: list[list[str]]) -> str:
    content = " ".join(row[0] for row in rows[1:] if row and row[0].strip()).strip()
    environment, _fill, title = callouts.classify(content)
    body = callouts.strip_marker(content)
    return "\n".join([
        r"\begin{" + environment + "}[" + escape_plain(title) + "]",
        inline(body),
        r"\end{" + environment + "}",
    ])


def table_header(row: list[str], columns: int) -> str:
    padded = row + [""] * (columns - len(row))
    return " & ".join(r"\color{white}\bfseries " + inline(cell) for cell in padded) + r" \\"


def render_table(rows: list[list[str]]) -> str:
    columns = max(len(row) for row in rows)
    if columns == 1 and rows and not rows[0][0].strip() and len(rows) >= 2:
        return render_callout(rows)
    width = 0.94 / columns
    specification = "@{}" + "".join("Y{" + format(width, ".4f") + r"\linewidth}" for _ in range(columns)) + "@{}"
    font_command = r"\small" if columns <= 3 else r"\fontsize{7.2}{9}\selectfont"

    # Short operational summaries should remain intact. A compact tabular is
    # also preferable here because a longtable at a forced page boundary can
    # print both its first-page and continuation header before the first row.
    compact = len(rows) <= 8 and max(len(cell) for row in rows for cell in row) <= 110
    if compact:
        output = [r"\needspace{5\baselineskip}", r"\BookTableStart", font_command,
                  r"\begin{tabular}{" + specification + "}",
                  r"\rowcolor{BookNavy}", table_header(rows[0], columns)]
        for index, row in enumerate(rows[1:], 1):
            padded = row + [""] * (columns - len(row))
            if index % 2 == 0:
                output.append(r"\rowcolor{BookLight}")
            output.append(" & ".join(inline(cell) for cell in padded) + r" \\")
        output.extend([r"\end{tabular}", r"\BookTableEnd"])
        return "\n".join(output)

    # A longtable header alone at the foot of a page reads as a defect. Reserve
    # the header plus a few body rows so the table starts where it can breathe;
    # anything longer still breaks naturally, with the header repeated.
    output = [r"\needspace{5\baselineskip}", r"\BookTableStart", font_command,
              r"\begin{longtable}{" + specification + "}"]
    # Define the first-page header separately from the continuation header.
    # Without an explicit first head, longtable can emit its continuation head
    # in addition to the rows that precede \endhead at a page boundary.
    output.extend([
        r"\rowcolor{BookNavy}", table_header(rows[0], columns), r"\endfirsthead",
        r"\rowcolor{BookNavy}", table_header(rows[0], columns), r"\endhead",
    ])
    for index, row in enumerate(rows[1:], 1):
        padded = row + [""] * (columns - len(row))
        if index % 2 == 0:
            output.append(r"\rowcolor{BookLight}")
        output.append(" & ".join(inline(cell) for cell in padded) + r" \\")
    output.extend([r"\end{longtable}", r"\BookTableEnd"])
    return "\n".join(output)


# Code is set at 7.4/9.2pt (see bookcode in bookstyle.sty). A listing that fits
# on one page should never be split, so reserve its height up front: needspace
# ejects the page when too little room is left, moving the whole listing over.
CODE_BASELINE_PT = 9.2
CODE_FRAME_PT = 20.0
# \textheight is 698.85pt, so ~73 code lines is the most that can ever sit on
# one page. Above that a listing must break however much space is reserved, and
# reserving would only strand a half-empty page in front of it. Listings that
# large are editorial debt: use the example region markers to show the part that
# teaches instead of the whole file.
CODE_MAX_RESERVE_PT = 330.0


def code_reservation(code: str) -> str:
    """The \needspace guard that keeps a page-sized listing intact."""
    height = len(code.splitlines()) * CODE_BASELINE_PT + CODE_FRAME_PT
    if height > CODE_MAX_RESERVE_PT:
        return ""
    return r"\needspace{" + format(height, ".1f") + "pt}"


def render_code(language: str, code: str) -> str:
    if "\\end{lstlisting}" in code:
        raise ValueError("Code block contains a reserved lstlisting terminator")
    language_map = {"python": "Python", "json": "bookjson", "bash": "bookbash", "yaml": "bookyaml", "text": ""}
    mapped = language_map.get(language.lower(), "")
    display_language = "🐍" if language.lower() == "python" else (language.upper() or "TEXT")
    options = ["style=bookcode", "title={" + escape_plain(display_language) + "}"]
    if mapped:
        options.append("language=" + mapped)
    lines = []
    reservation = code_reservation(code)
    if reservation:
        lines.append(reservation)
    lines += [r"\begin{lstlisting}[" + ",".join(options) + "]", code, r"\end{lstlisting}"]
    return "\n".join(lines)


def reference_target(text: str) -> str:
    match = re.match(r"\*\*\[(R\d{2})\]\*\*", text)
    return (r"\BookReferenceTarget{" + match.group(1) + "}") if match else ""


def render_content(blocks: list[tuple], diagram_files: dict[str, str], book_title: str, covers: dict[str, str] | None = None) -> tuple[str, dict[str, int]]:
    output: list[str] = ["% Generated from book/manuscript.md. Do not hand-edit."]
    stats = {"parts": 0, "appendix_dividers": 0, "chapters": 0, "chapter_covers": 0, "appendices": 0, "diagrams": 0, "code_blocks": 0, "tables": 0, "callouts": 0, "citations": 0}
    index = 0
    if blocks and blocks[0][0] == "cover":
        index = 1
    if index < len(blocks) and blocks[index][0] == "heading" and blocks[index][2] == book_title:
        index += 1
        skipped = 0
        while index < len(blocks) and blocks[index][0] == "paragraph" and skipped < 3:
            index += 1
            skipped += 1
    covers = covers or {}
    output.extend([r"\frontmatter", r"\tableofcontents", r"\clearpage"])
    first_part = True
    in_appendices = False
    while index < len(blocks):
        block = blocks[index]
        kind = block[0]
        if kind in {"bullet", "number", "check"}:
            environment = "enumerate" if kind == "number" else "itemize"
            output.append(r"\begin{" + environment + "}")
            while index < len(blocks) and blocks[index][0] in ({"number"} if environment == "enumerate" else {"bullet", "check"}):
                current = blocks[index]
                if current[0] == "check":
                    symbol = r"$\boxtimes$" if current[1] == "checked" else r"$\square$"
                    text = symbol + " " + inline(current[2])
                else:
                    prefix = reference_target(current[1])
                    text = prefix + inline(current[1])
                output.append(r"\item " + text)
                index += 1
            output.append(r"\end{" + environment + "}")
            continue
        if kind == "part":
            if first_part:
                output.append(r"\mainmatter")
                first_part = False
            if block[1].upper() == "REFERENCE":
                stats["appendix_dividers"] += 1
            else:
                stats["parts"] += 1
            output.append(
                r"\BookPartPage{" + escape_plain(block[1]) + "}{" + inline(block[2])
                + "}{" + inline(block[3]) + "}"
            )
        elif kind == "heading":
            level, text = block[1], block[2]
            chapter = re.match(r"^(\d{2}) — (.+)$", text)
            appendix = re.match(r"^Appendix ([A-Z]) — (.+)$", text)
            if level == 1 and chapter:
                stats["chapters"] += 1
                if chapter.group(1) in covers:
                    stats["chapter_covers"] += 1
                    output.append(r"\BookChapterCover{" + covers[chapter.group(1)] + "}")
                output.append(r"\BookChapter{" + chapter.group(1) + "}{" + inline(chapter.group(2)) + "}")
            elif level == 1 and appendix:
                if not in_appendices:
                    output.extend([r"\clearpage", r"\appendix"])
                    in_appendices = True
                stats["appendices"] += 1
                output.append(r"\BookAppendix{" + appendix.group(1) + "}{" + inline(appendix.group(2)) + "}")
            elif level == 1:
                output.append(r"\BookFrontChapter{" + inline(text) + "}")
            elif level == 2:
                output.append(r"\section{" + inline(text) + "}")
            elif level == 3:
                output.append(r"\subsection{" + inline(text) + "}")
            else:
                output.append(r"\subsubsection{" + inline(text) + "}")
        elif kind == "diagram":
            identifier, caption = block[1], block[2]
            if identifier not in diagram_files:
                raise KeyError("Unknown diagram identifier: " + identifier)
            stats["diagrams"] += 1
            output.append(r"\BookDiagram{" + diagram_files[identifier] + "}{" + inline(caption) + "}{" + escape_plain(identifier) + "}")
        elif kind == "code":
            stats["code_blocks"] += 1
            output.append(render_code(block[1], block[2]))
        elif kind == "table":
            stats["tables"] += 1
            if max(len(row) for row in block[1]) == 1 and block[1] and not block[1][0][0].strip():
                stats["callouts"] += 1
            output.append(render_table(block[1]))
        elif kind == "quote":
            output.extend([r"\begin{bookquote}", inline(block[1]), r"\end{bookquote}"])
        elif kind == "paragraph":
            text = block[1]
            if re.match(r"^Figure\s+\d", text):
                output.append(r"\BookFigureCaption{" + inline(text) + "}")
            else:
                output.append(inline(text) + r"\par")
        index += 1
    joined = "\n\n".join(output) + "\n"
    stats["citations"] = joined.count(r"\BookCitation{")
    return joined, stats


def make_main(book: dict) -> str:
    """Title page text comes from config/book.json, so a retitle is one edit."""
    return "\n".join([
        "% Compile from the package root: latexmk -xelatex latex/" + BASENAME + ".tex",
        r"\documentclass[10pt,letterpaper,openany]{book}",
        r"\usepackage{latex/bookstyle}",
        r"\begin{document}",
        r"\BookCover{assets/cover/cover-v" + book["version"] + ".png}",
        r"\BookTitlePage{" + escape_plain(book["title"]) + "}{Book v" + book["version"] + " · Publication Release · September 2026}{" + escape_plain(book["author"]) + "}{A structured enterprise reference for executives, architects, platform teams, security leaders, SREs, and senior engineers.}",
        r"\input{latex/content/book-content.tex}",
        r"\end{document}",
        "",
    ])


def write_compile_files(root: Path) -> None:
    latex_dir = root / "latex"
    compile_script = """#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
ENTRY="latex/Enterprise-General-Intelligence-v2.1.0.tex"
OUT="latex/build"
mkdir -p "$OUT"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$OUT" "$ENTRY"
elif command -v xelatex >/dev/null 2>&1; then
  for pass in 1 2 3; do xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$OUT" "$ENTRY"; done
else
  echo "XeLaTeX is required. Use the included Dockerfile.latex or CI workflow." >&2
  exit 2
fi
cp "$OUT/Enterprise-General-Intelligence-v2.1.0.pdf" "dist/Enterprise-General-Intelligence-v2.1.0-LaTeX.pdf"
"""
    (latex_dir / "compile.sh").write_text(compile_script, encoding="utf-8", newline="\n")
    (latex_dir / "compile.sh").chmod(0o755)
    latexmkrc = "$pdf_mode = 5;\n$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S';\n$out_dir = 'latex/build';\n"
    (root / ".latexmkrc").write_text(latexmkrc, encoding="utf-8", newline="\n")
    dockerfile = """FROM texlive/texlive:latest-full
WORKDIR /book
COPY . /book
RUN chmod +x latex/compile.sh && latex/compile.sh
CMD ["latex/compile.sh"]
"""
    (root / "Dockerfile.latex").write_text(dockerfile, encoding="utf-8", newline="\n")


def copy_fonts(root: Path) -> list[dict]:
    font_dir = root / "latex" / "fonts"
    font_dir.mkdir(parents=True, exist_ok=True)
    sources = [
        Path("/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf"),
        Path("/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf"),
        Path("/usr/share/fonts/liberation-sans/LiberationSans-Italic.ttf"),
        Path("/usr/share/fonts/liberation-sans/LiberationSans-BoldItalic.ttf"),
        Path("/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf"),
        Path("/usr/share/fonts/liberation-mono/LiberationMono-Bold.ttf"),
        Path("/usr/share/fonts/liberation-mono/LiberationMono-Italic.ttf"),
        Path("/usr/share/fonts/liberation-mono/LiberationMono-BoldItalic.ttf"),
    ]
    records = []
    for source in sources:
        target = font_dir / source.name
        # The bundled font is tracked release evidence: its hash is recorded in
        # RELEASE-MANIFEST.json and CHECKSUMS.sha256, and XeLaTeX embeds exactly
        # these bytes. Once it exists it wins. Copying the host's build over it
        # would silently change a published artifact on nothing but a difference
        # in which distribution the build happened to run on.
        if not target.exists():
            if not source.exists():
                raise FileNotFoundError("Bundled font is missing and no system source is available: " + target.name)
            shutil.copy2(source, target)
        records.append({"file": target.relative_to(root).as_posix(), "sha256": sha256(target), "license": "SIL Open Font License 1.1"})
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    markdown_path = root / "book" / "manuscript.md"
    markdown = markdown_path.read_text(encoding="utf-8")
    diagram_doc = json.loads((root / "config" / "diagrams.json").read_text(encoding="utf-8"))
    # XeLaTeX embeds the vector PDF where one exists, so a figure stays sharp at
    # any zoom and in print; the DOCX build uses the PNG beside it because
    # python-docx cannot embed PDF. Same source, two renders, one registry.
    diagram_files = {}
    for item in diagram_doc["diagrams"]:
        vector = Path(item["file"]).with_suffix(".pdf")
        diagram_files[item["id"]] = vector.as_posix() if (root / vector).exists() else item["file"]
    blocks = list(parse_markdown(markdown))
    book_cfg = json.loads((root / "config" / "book.json").read_text(encoding="utf-8"))["book"]
    content, stats = render_content(blocks, diagram_files, book_cfg["title"], chapter_covers(root))

    latex_dir = root / "latex"
    content_dir = latex_dir / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    main_path = latex_dir / (BASENAME + ".tex")
    content_path = content_dir / "book-content.tex"
    dist_path = root / "dist" / (BASENAME + ".tex")
    main_text = make_main(book_cfg)
    main_path.write_text(main_text, encoding="utf-8", newline="\n")
    content_path.write_text(content, encoding="utf-8", newline="\n")
    dist_path.write_text(main_text, encoding="utf-8", newline="\n")
    fonts = copy_fonts(root)
    write_compile_files(root)

    reference_pdf = root / "qa" / "render" / (BASENAME + ".pdf")
    reference_dir = latex_dir / "reference"
    reference_dir.mkdir(parents=True, exist_ok=True)
    if reference_pdf.exists():
        shutil.copy2(reference_pdf, reference_dir / "DOCX-layout-reference-v1.0.0.pdf")

    report = {
        "release": book_release(root),
        "engine": "XeLaTeX",
        "canonical_markdown": markdown_path.relative_to(root).as_posix(),
        "canonical_markdown_sha256": sha256(markdown_path),
        "main_tex": main_path.relative_to(root).as_posix(),
        "main_tex_sha256": sha256(main_path),
        "content_tex": content_path.relative_to(root).as_posix(),
        "content_tex_sha256": sha256(content_path),
        "style": "latex/bookstyle.sty",
        "fonts": fonts,
        "statistics": stats,
        "source_bytes": main_path.stat().st_size + content_path.stat().st_size,
        "compile_command": "latex/compile.sh",
    }
    (root / "reports" / "latex-build-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
