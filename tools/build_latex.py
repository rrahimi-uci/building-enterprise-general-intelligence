#!/usr/bin/env python3
"""Generate the XeLaTeX representation of Book v1.0.0.

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

import book_index
import callouts
from build_info import build_date

# The index tracker for the build in progress. tools/book_index.py decides where
# a term is marked; this renderer only writes the \index commands.
INDEX: book_index.Tracker | None = None


def index_marks(text: str) -> str:
    """\\index commands for the terms book_index marks in this text."""
    if INDEX is None:
        return ""
    out = []
    for term, defining in INDEX.marks(text):
        display = escape_plain(term)
        for special in '"!@|':
            display = display.replace(special, '"' + special)
        out.append(r"\index{" + book_index.sort_key(term) + "@" + display + ("|textbf" if defining else "") + "}")
    return "".join(out)


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


BASENAME = "Enterprise-General-Intelligence-v1.0.0"


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
            raw: list[str] = []
            while i < len(lines) and not lines[i].startswith("# "):
                raw.append(lines[i])
                i += 1
            yield ("part", ident, title, part_intro(raw))
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


def part_intro(raw: list[str]) -> list[tuple[str, str]]:
    """A Part page's text: lead and closing paragraphs plus an optional list."""
    blocks: list[tuple[str, str]] = []
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            blocks.append(("para", " ".join(paragraph)))
            paragraph.clear()

    for line in raw:
        if not line.strip():
            flush()
        elif re.match(r"^[-*]\s+", line):
            flush()
            blocks.append(("bullet", re.sub(r"^[-*]\s+", "", line).strip()))
        elif line[:1] in (" ", "\t") and blocks and blocks[-1][0] == "bullet" and not paragraph:
            blocks[-1] = ("bullet", blocks[-1][1] + " " + line.strip())
        else:
            paragraph.append(line.strip())
    flush()
    return blocks


def render_part_intro(blocks: list[tuple[str, str]]) -> str:
    out: list[str] = []
    in_list = False
    for kind, text in blocks:
        if kind == "bullet" and not in_list:
            out.append(r"\begin{BookPartList}")
            in_list = True
        if kind != "bullet" and in_list:
            out.append(r"\end{BookPartList}")
            in_list = False
        out.append((r"\item " if kind == "bullet" else "") + inline(text) + ("" if kind == "bullet" else r"\par"))
    if in_list:
        out.append(r"\end{BookPartList}")
    return "\n".join(out)


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


QUOTE_OPENERS = set(" \t\n([{—–/“‘")


def smart_double_quotes(text: str) -> str:
    """Turn straight double quotes into typographic ones.

    With TeX ligatures on, XeLaTeX prints every straight `"` as a closing
    quote, so an opening quote came out backwards. A quote opens when it
    follows a space, a bracket or a dash (or starts the segment) and is
    followed by a non-space; otherwise it closes.
    """
    out = []
    for i, ch in enumerate(text):
        if ch != '"':
            out.append(ch)
            continue
        before = text[i - 1] if i else None
        after = text[i + 1] if i + 1 < len(text) else ""
        opens = (before is None or before in QUOTE_OPENERS) and after.strip() != ""
        if before is None and after and after in ".,;:!?)]}":
            opens = False
        out.append("“" if opens else "”")
    return "".join(out)


def escape_plain(text: str, cell: bool = False, quotes: bool = True) -> str:
    text = markdown_unescape(text)
    if quotes:
        text = smart_double_quotes(text)
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
    if cell:
        # A narrow table column cannot absorb a long slash-joined token such
        # as "unit/contract/security/...". \slash lets the line break after
        # the slash at the same penalty as after an explicit hyphen.
        mapping["/"] = r"\slash{}"
    segments = re.split(r"<br\s*/?>", text, flags=re.I)
    escaped = []
    for segment in segments:
        escaped.append("".join(mapping.get(ch, ch) for ch in segment))
    return r"\newline{}".join(escaped)


def inline_code(value: str, cell: bool = False) -> str:
    value = markdown_unescape(value)
    # In a table the code takes the cell's own size; the 8.6pt body-text style
    # set identifiers visibly larger than the 7.2pt text around them.
    style = "style=bookinline,basicstyle=\\ttfamily\\color{BookNavyTwo}" if cell else "style=bookinline"
    for delimiter in "!|+/;:@?":
        if delimiter not in value:
            return r"\lstinline[" + style + "]" + delimiter + value + delimiter
    return r"\texttt{" + escape_plain(value, quotes=False) + "}"


def inline(text: str, cell: bool = False) -> str:
    token = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\(https?://[^)]+\)|\[R\d{2}\]|(?<!\*)\*[^*\n]+\*)")
    output: list[str] = []
    position = 0
    for match in token.finditer(text):
        if match.start() > position:
            output.append(escape_plain(text[position:match.start()], cell))
        value = match.group(0)
        if value.startswith("**"):
            output.append(r"\textbf{" + inline(value[2:-2], cell) + "}")
        elif value.startswith("`"):
            output.append(inline_code(value[1:-1], cell))
        elif re.match(r"^\[[^\]]+\]\(https?://", value):
            link = re.match(r"^\[([^\]]+)\]\((https?://[^)]+)\)$", value)
            if link:
                output.append(r"\href{\detokenize{" + link.group(2) + "}}{" + inline(link.group(1), cell) + "}")
        elif re.fullmatch(r"\[R\d{2}\]", value):
            output.append(r"\BookCitation{" + value[1:-1] + "}")
        elif value.startswith("*"):
            output.append(r"\emph{" + inline(value[1:-1], cell) + "}")
        position = match.end()
    if position < len(text):
        output.append(escape_plain(text[position:], cell))
    return "".join(output)


def render_callout(rows: list[list[str]]) -> str:
    content = " ".join(row[0] for row in rows[1:] if row and row[0].strip()).strip()
    environment, _fill, title = callouts.classify(content)
    body = callouts.strip_marker(content)
    return "\n".join([
        r"\begin{" + environment + "}[" + escape_plain(title) + "]",
        inline(body) + index_marks(content),
        r"\end{" + environment + "}",
    ])


def table_header(row: list[str], columns: int) -> str:
    padded = row + [""] * (columns - len(row))
    return " & ".join(r"\color{white}\bfseries " + inline(cell, cell=True) for cell in padded) + r" \\"


# Table geometry, mirrored from bookstyle.sty so the builder can estimate how
# tall a table's opening rows will set. \linewidth is 7.06in; \tabcolsep 4pt.
LINEWIDTH_PT = 508.0
TABCOLSEP_PT = 4.0
TABLE_TEXTHEIGHT_PT = 698.85
# (average glyph advance, baselineskip) for the two table sizes: \small and
# 7.2/9pt, each under the 0.95 \setstretch. The advance is a conservative
# average for Liberation Sans running text.
TABLE_FONTS = {"small": (4.6, 10.45), "compact": (3.7, 8.55)}


def cell_lines(text: str, width_pt: float, advance_pt: float) -> int:
    plain = re.sub(r"[*`]|\[R\d{2}\]", "", markdown_unescape(text))
    chars_per_line = max(8, int(width_pt / advance_pt))
    lines, current = 1, 0
    for word in plain.split():
        if current and current + 1 + len(word) > chars_per_line:
            lines += 1
            current = len(word)
        else:
            current += (1 if current else 0) + len(word)
    return lines


def table_height(rows: list[list[str]], columns: int, body_rows: int | None = None) -> float:
    """Estimated set height of the header plus the first `body_rows` rows."""
    advance, baseline = TABLE_FONTS["small" if columns <= 3 else "compact"]
    width = (LINEWIDTH_PT - (2 * columns - 2) * TABCOLSEP_PT) / columns
    chosen = rows if body_rows is None else rows[: body_rows + 1]
    return sum(max(cell_lines(c, width, advance) for c in row) * baseline + 1.0 for row in chosen)


# The opening block a longtable keeps together: the head plus up to three body
# rows, joined by \\* so the page cannot break between them. Tall rows are
# kept only while the block stays short, so a table of long cells does not
# leave most of a page empty in front of it.
LONGTABLE_KEEP_PT = 150.0


def longtable_kept(rows: list[list[str]], columns: int) -> int:
    """How many leading body rows end in \\* (no page break after them)."""
    kept = 0
    for count in (1, 2):
        if len(rows) - 1 <= count:
            break
        if table_height(rows, columns, count + 1) > LONGTABLE_KEEP_PT:
            break
        kept = count
    return kept


def table_reservation(rows: list[list[str]], columns: int, compact: bool) -> float:
    """Room to reserve so a table never opens with a stranded header.

    A tabular cannot break, so reserve all of it. A longtable needs its header
    and the first rows on the opening page: when they do not fit, longtable
    breaks before its first row and carries the first head over, which prints
    the header twice on the next page.
    """
    # 1.2: the character-count model underestimates wrapped cells, and a
    # reservation that is slightly too large only moves a table a page early.
    opening = None if compact else longtable_kept(rows, columns) + 1
    height = 1.2 * table_height(rows, columns, opening) + 8.0
    return min(height, 0.45 * TABLE_TEXTHEIGHT_PT if not compact else 0.9 * TABLE_TEXTHEIGHT_PT)


def is_callout(rows: list[list[str]]) -> bool:
    return max(len(row) for row in rows) == 1 and bool(rows) and not rows[0][0].strip() and len(rows) >= 2


def compact_table(rows: list[list[str]]) -> bool:
    return len(rows) <= 8 and max(len(cell) for row in rows for cell in row) <= 110


def block_reservation(block: tuple, after: tuple | None = None) -> float:
    """Height a heading must keep with it when this block follows directly.

    A heading followed by another heading (H2 then H3) keeps both headings and
    whatever the second one opens with, so neither is left at a page foot.
    """
    if block[0] == "paragraph" and after is not None and after[0] == "code" and is_listing_label(block[1]):
        return listing_keep(after[2]) + LISTING_LABEL_PT
    if block[0] == "heading" and block[1] >= 2 and after is not None:
        inner = block_reservation(after)
        return inner + HEADING_HEIGHT_PT[min(block[1], 4)] if inner else 0.0
    if block[0] == "table" and not is_callout(block[1]):
        rows = block[1]
        return table_reservation(rows, max(len(r) for r in rows), compact_table(rows))
    if block[0] == "code":
        return min(len(block[2].splitlines()), 6) * CODE_BASELINE_PT + CODE_FRAME_PT
    return 0.0


# Height each heading level takes from the page, including the space above
# and below it and the parskip around it. Generous on purpose: when an H2 is
# immediately followed by an H3, the H2's reservation must exceed the H3's by
# at least the H2's real height, or the H3's own reservation strands the H2.
HEADING_HEIGHT_PT = {2: 52.0, 3: 38.0, 4: 28.0}


def render_table(rows: list[list[str]]) -> str:
    columns = max(len(row) for row in rows)
    if is_callout(rows):
        return render_callout(rows)
    # Columns fill the measure exactly: c widths plus the 2c-2 inner
    # separations equal \linewidth. A fixed 0.94 share left five-column tables
    # 1.4pt wider than the text block.
    width = r"\dimexpr(\linewidth-" + str(2 * columns - 2) + r"\tabcolsep)/" + str(columns) + r"\relax"
    specification = "@{}" + "".join("Y{" + width + "}" for _ in range(columns)) + "@{}"
    font_command = r"\small" if columns <= 3 else r"\fontsize{7.2}{9}\selectfont"

    # Short operational summaries should remain intact. A compact tabular is
    # also preferable here because a longtable at a forced page boundary can
    # print both its first-page and continuation header before the first row.
    compact = compact_table(rows)
    if compact:
        reserve = r"\BookNeedspace{" + format(table_reservation(rows, columns, True), ".1f") + "pt}"
        output = [reserve, r"\BookTableStart", font_command,
                  r"\begin{tabular}{" + specification + "}",
                  r"\rowcolor{BookNavy}", table_header(rows[0], columns)]
        for index, row in enumerate(rows[1:], 1):
            padded = row + [""] * (columns - len(row))
            if index % 2 == 0:
                output.append(r"\rowcolor{BookLight}")
            output.append(" & ".join(inline(cell, cell=True) + index_marks(cell) for cell in padded) + r" \\")
        output.extend([r"\end{tabular}", r"\BookTableEnd"])
        return "\n".join(output)

    # A longtable header alone at the foot of a page reads as a defect. The old
    # guard, needspace's \needspace, only plants a cheap breakpoint that TeX
    # takes later, once the page overfills -- by then inside the longtable, whose
    # output routine prints its head on top of the next page as well. That gave
    # doubled heads, and heads stranded above unrelated listings. So a longtable
    # gets no reservation at all (see \BookNeedspace). It already moves itself to the next
    # page when its head and first row do not fit, and up to two more body rows
    # are tied to it with \\* (see longtable_kept), so the head opens with rows
    # beneath it. Anything longer breaks with the head repeated.
    output = [r"\BookTableStart", font_command,
              r"\begin{longtable}{" + specification + "}"]
    # Define the first-page header separately from the continuation header.
    output.extend([
        r"\rowcolor{BookNavy}", table_header(rows[0], columns), r"\endfirsthead",
        r"\rowcolor{BookNavy}", table_header(rows[0], columns), r"\endhead",
    ])
    kept = longtable_kept(rows, columns)
    for index, row in enumerate(rows[1:], 1):
        padded = row + [""] * (columns - len(row))
        if index % 2 == 0:
            output.append(r"\rowcolor{BookLight}")
        end = r" \\*" if index <= kept else r" \\"
        output.append(" & ".join(inline(cell, cell=True) + index_marks(cell) for cell in padded) + end)
    output.extend([r"\end{longtable}", r"\BookTableEnd"])
    return "\n".join(output)


# Code is set at 7.4/9.2pt (see bookcode in bookstyle.sty). A listing that fits
# on one page should never be split, so reserve its height up front: the guard
# ejects the page when too little room is left, moving the whole listing over.
CODE_BASELINE_PT = 9.2
CODE_FRAME_PT = 20.0
# \textheight is 698.85pt, so ~73 code lines is the most that can ever sit on
# one page. Above that a listing must break however much space is reserved, and
# reserving would only strand a half-empty page in front of it. Listings that
# large are editorial debt: use the example region markers to show the part that
# teaches instead of the whole file.
CODE_MAX_RESERVE_PT = 643.0


LISTING_LABEL_PT = 16.0


def is_listing_label(text: str) -> bool:
    """A listing's caption: the one short, unpunctuated line just above its code.

    The caption carries the title only; the language is shown once, on the code
    panel's tab. Prose lead-ins end in a full stop and are never captions.
    """
    return ("\n" not in text and len(text) <= 120 and not text.endswith((".", ":", "?", "!"))
            and not text.startswith(("Figure", "|", "#", "-", "*")))


def listing_keep(code: str) -> float:
    """Height a listing must keep with its label: all of it when it fits on a
    page, otherwise its first eight lines."""
    lines = len(code.splitlines())
    height = lines * CODE_BASELINE_PT + CODE_FRAME_PT
    return height if height <= CODE_MAX_RESERVE_PT else 8 * CODE_BASELINE_PT + CODE_FRAME_PT


def code_reservation(code: str) -> str:
    r"""The \BookNeedspace guard that keeps a page-sized listing intact."""
    height = len(code.splitlines()) * CODE_BASELINE_PT + CODE_FRAME_PT
    if height > CODE_MAX_RESERVE_PT:
        return ""
    return r"\BookNeedspace{" + format(height, ".1f") + "pt}"


def render_code(language: str, code: str, labelled: bool = False) -> str:
    if "\\end{lstlisting}" in code:
        raise ValueError("Code block contains a reserved lstlisting terminator")
    language_map = {"python": "Python", "json": "bookjson", "bash": "bookbash", "yaml": "bookyaml", "text": ""}
    mapped = language_map.get(language.lower(), "")
    display_language = "🐍" if language.lower() == "python" else (language.upper() or "TEXT")
    options = ["style=bookcode", "title={" + escape_plain(display_language) + "}"]
    if mapped:
        options.append("language=" + mapped)
    lines = []
    # A labelled listing was reserved before its label; a second guard here
    # would add a breakpoint between the label and the code.
    reservation = "" if labelled else code_reservation(code)
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
                    text = prefix + inline(current[1]) + index_marks(current[1])
                output.append(r"\item " + text)
                index += 1
            output.append(r"\end{" + environment + "}")
            continue
        if kind == "part":
            if INDEX is not None:
                INDEX.part()
            if first_part:
                output.append(r"\mainmatter")
                first_part = False
            if block[1].upper() == "REFERENCE":
                stats["appendix_dividers"] += 1
            else:
                stats["parts"] += 1
            output.append(
                r"\BookPartPage{" + escape_plain(block[1]) + "}{" + inline(block[2])
                + "}{" + render_part_intro(block[3]) + "}"
            )
        elif kind == "heading":
            level, text = block[1], block[2]
            if INDEX is not None:
                INDEX.heading(level, text)
            if level == 1 and text == book_index.INDEX_HEADING:
                # The Markdown index lists chapter locators; the PDF prints the
                # page index makeindex builds from the \index marks instead.
                output.append(r"\BookIndex")
                break
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
            else:
                # A heading whose next block is a table or listing must not be
                # left alone at the foot of a page: reserve the heading and the
                # block's opening together, before the heading is set.
                following = blocks[index + 1] if index + 1 < len(blocks) else None
                after = blocks[index + 2] if index + 2 < len(blocks) else None
                keep = block_reservation(following, after) if following else 0.0
                if keep:
                    output.append(r"\BookNeedspace{" + format(keep + HEADING_HEIGHT_PT[min(level, 4)], ".1f") + "pt}")
                command = {2: "section", 3: "subsection"}.get(level, "subsubsection")
                output.append("\\" + command + "{" + inline(text) + "}")
        elif kind == "diagram":
            identifier, caption = block[1], block[2]
            if identifier not in diagram_files:
                raise KeyError("Unknown diagram identifier: " + identifier)
            stats["diagrams"] += 1
            output.append(r"\BookDiagram{" + diagram_files[identifier] + "}{" + inline(caption) + "}{" + escape_plain(identifier) + "}")
        elif kind == "code":
            stats["code_blocks"] += 1
            previous = blocks[index - 1] if index else None
            labelled = bool(previous and previous[0] == "paragraph" and is_listing_label(previous[1]))
            output.append(render_code(block[1], block[2], labelled))
        elif kind == "table":
            stats["tables"] += 1
            if max(len(row) for row in block[1]) == 1 and block[1] and not block[1][0][0].strip():
                stats["callouts"] += 1
            output.append(render_table(block[1]))
        elif kind == "quote":
            output.extend([r"\begin{bookquote}", inline(block[1]) + index_marks(block[1]), r"\end{bookquote}"])
        elif kind == "paragraph":
            text = block[1]
            following = blocks[index + 1] if index + 1 < len(blocks) else None
            if re.match(r"^Figure\s+\d", text):
                output.append(r"\BookFigureCaption{" + inline(text) + "}")
            elif following and following[0] == "code" and is_listing_label(text):
                # A listing's caption (its title) belongs to the listing:
                # reserve the label and the listing's opening together, so the
                # label never ends a page while its code starts on the next.
                output.append(r"\BookNeedspace{" + format(listing_keep(following[2]) + LISTING_LABEL_PT, ".1f") + "pt}")
                output.append(inline(text) + r"\par\nopagebreak")
            else:
                output.append(inline(text) + index_marks(text) + r"\par")
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
        r"\BookTitlePage{" + escape_plain(book["title"]) + "}{Book v" + book["version"] + " · Publication Release · " + build_date() + "}{" + escape_plain(book["author"]) + "}{A structured enterprise reference for executives, architects, platform teams, security leaders, SREs, and senior engineers.}",
        r"\input{latex/content/book-content.tex}",
        r"\BookCover{assets/cover/back-cover-v" + book["version"] + ".png}",
        r"\end{document}",
        "",
    ])


def write_compile_files(root: Path) -> None:
    latex_dir = root / "latex"
    compile_script = """#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
ENTRY="latex/Enterprise-General-Intelligence-v1.0.0.tex"
OUT="latex/build"
PDF_SOURCE="$OUT/Enterprise-General-Intelligence-v1.0.0.pdf"
PDF_DEST="dist/Enterprise-General-Intelligence-v1.0.0.pdf"
mkdir -p "$OUT" "dist"
# makeindex finds the book's index style through kpathsea, so it resolves the
# same way when latexmk runs makeindex from inside the output directory.
export INDEXSTYLE="$ROOT/latex:${INDEXSTYLE:-}"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$OUT" "$ENTRY"
elif command -v xelatex >/dev/null 2>&1; then
  xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$OUT" "$ENTRY"
  # The index: makeindex sorts the marks the first pass wrote.
  makeindex -q -s bookindex.ist -o "$OUT/Enterprise-General-Intelligence-v1.0.0.ind" "$OUT/Enterprise-General-Intelligence-v1.0.0.idx"
  for pass in 2 3; do xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$OUT" "$ENTRY"; done
else
  echo "XeLaTeX is required. Use the included Dockerfile.latex or CI workflow." >&2
  exit 2
fi
if [[ ! -s "$PDF_SOURCE" ]]; then
  echo "XeLaTeX did not produce a non-empty PDF at $PDF_SOURCE." >&2
  exit 1
fi
cp "$PDF_SOURCE" "$PDF_DEST"
if [[ ! -s "$PDF_DEST" ]]; then
  echo "The final XeLaTeX PDF is missing or empty at $PDF_DEST." >&2
  exit 1
fi
printf 'XeLaTeX PDF written to %s\\n' "$PDF_DEST"
"""
    (latex_dir / "compile.sh").write_text(compile_script, encoding="utf-8", newline="\n")
    (latex_dir / "compile.sh").chmod(0o755)
    latexmkrc = "$pdf_mode = 5;\n$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S';\n$out_dir = 'latex/build';\n$makeindex = 'makeindex -q -s bookindex.ist -o %D %S';\n"
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
    global INDEX
    INDEX = book_index.Tracker(book_index.load_terms(root, markdown), book_index.excluded_units(root))
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
        shutil.copy2(reference_pdf, reference_dir / "DOCX-layout-reference-draft.pdf")

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
