#!/usr/bin/env python3
"""Render one Letter-size chapter cover visual per chapter from its spec.

Every visual is drawn from `config/chapter-covers.json`: the chapter identity
(Part, number, title, focus line, three themes) and an explanatory diagram of
the chapter's central concept, with exactly four numbered components. The spec
is the artifact a contributor edits; the PNGs in `cover-images/` are generated
and must never be hand-touched.

The page is US Letter portrait, 8.5 x 11 in at 300 dpi (2550 x 3300 px), so a
cover drops onto a book page without rescaling or cropping.

Visual language follows the Part visuals: deep-navy field, cyan/blue accents,
glowing 2.5D components. Role is carried by colour AND icon, mirroring the
Graphviz house style in `assets/diagrams/src/_theme.gv`, so a component type
reads without its colour. Prohibited paths are red, dashed, and carry a
no-entry mark.

Idempotent by content: a render that would not change the pixels leaves the
file alone, so recorded digests do not churn on encoder differences.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

from PIL import Image, ImageFont

DPI = 300
PAGE_W, PAGE_H = int(8.5 * DPI), int(11 * DPI)
MARGIN = 150

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
FONT_FILES = {False: ["Arial.ttf", "LiberationSans-Regular.ttf"],
              True: ["Arial Bold.ttf", "LiberationSans-Bold.ttf"]}

BG_TOP, BG_BOTTOM = "#071833", "#040E20"
INK_WHITE, INK_SOFT, INK_MUTED = "#FFFFFF", "#D6E5F5", "#8FA9C6"
PANEL_FILL, CARD_TOP, CARD_BOTTOM = "#0A1E3B", "#143862", "#0B2447"
ACCENTS = {"cyan": "#20B8D8", "blue": "#3D8BF2"}

# Same role vocabulary as _theme.gv, lifted for a dark field.
KIND_COLOR = {
    "model": "#2FC2B5",      # runtime / reasoning (teal)
    "service": "#4F9BF7",    # platform services (blue)
    "actor": "#4F9BF7",
    "store": "#8C9BFF",      # stores, ledgers (indigo)
    "record": "#8C9BFF",
    "knowledge": "#3CCBEA",  # knowledge, policy, evidence (cyan)
    "graph": "#3CCBEA",      # knowledge graph: entities and relationships (cyan)
    "control": "#F2B35A",    # gates and policy checks (amber)
    "human": "#F2B35A",
    "external": "#8FA3BC",   # outside the trust boundary (slate)
    "effect": "#C98BE0",     # committed effects and outcomes (plum)
    "bad": "#F06A6A",        # refusals, anti-patterns (red)
}
TONE = dict(KIND_COLOR, cyan="#20B8D8", blue="#3D8BF2", teal="#2FC2B5", amber="#F2B35A",
            red="#F06A6A", plum="#C98BE0", indigo="#8C9BFF", slate="#8FA3BC")
EDGE_STYLE = {
    "normal": {"color": "#5FD4EE", "dash": None},
    "feedback": {"color": "#2FC2B5", "dash": "18 12"},
    "async": {"color": "#4F9BF7", "dash": "4 12"},
    "prohibited": {"color": "#F06A6A", "dash": "20 12"},
}

# Diagram panel geometry (px). It starts below the identity block, which is
# two or three title lines tall, and always ends at PANEL_BOTTOM so the legend
# and footer sit at the same place on every page. Nodes are placed in a 12 x 8
# grid inside it.
PANEL_BOTTOM = 2770
PANEL_MIN_TOP, PANEL_GAP = 980, 80
GRID_COLS, GRID_ROWS = 12, 8
GRID_PAD_X, GRID_TOP, GRID_BOTTOM = 70, 150, 60


# --------------------------------------------------------------------- text
_fonts: dict = {}


def font(size: int, bold: bool = False):
    key = (size, bold)
    if key not in _fonts:
        for name in FONT_FILES[bold]:
            for base in (FONT_DIR, Path("/usr/share/fonts/truetype/liberation")):
                if (base / name).exists():
                    _fonts[key] = ImageFont.truetype(str(base / name), size)
                    break
            if key in _fonts:
                break
        else:
            raise SystemExit("Arial (or Liberation Sans) is required to measure text")
    return _fonts[key]


def text_width(text: str, size: int, bold: bool = False, spacing: float = 0) -> float:
    return font(size, bold).getlength(text) + spacing * max(0, len(text) - 1)


def wrap(text: str, size: int, width: float, bold: bool = False) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and text_width(trial, size, bold) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def t(x, y, s, size, color=INK_WHITE, bold=False, anchor="start", spacing=0, opacity=1.0):
    weight = ' font-weight="700"' if bold else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    op = f' fill-opacity="{opacity}"' if opacity < 1 else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Liberation Sans, sans-serif" '
            f'font-size="{size}"{weight}{ls}{op} fill="{color}" text-anchor="{anchor}">'
            f"{escape(s)}</text>")


# --------------------------------------------------------------------- icons
def icon(kind: str, cx: float, cy: float, r: float, color: str) -> str:
    """A 2r-sized glyph centred on (cx, cy). Shape alone identifies the role."""
    sf = f'stroke="{color}" stroke-width="{r * 0.13:.1f}" stroke-linecap="round" stroke-linejoin="round"'
    s = 'fill="none" ' + sf
    u = r / 10.0
    if kind == "model":  # hexagonal core with a lit node
        pts = " ".join(f"{cx + 9 * u * math.cos(math.radians(a)):.1f},{cy + 9 * u * math.sin(math.radians(a)):.1f}"
                       for a in range(30, 390, 60))
        return (f'<polygon points="{pts}" {s}/>'
                f'<circle cx="{cx}" cy="{cy}" r="{3.2 * u:.1f}" fill="{color}"/>'
                + "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + 6.5 * u * math.cos(math.radians(a)):.1f}" '
                          f'y2="{cy + 6.5 * u * math.sin(math.radians(a)):.1f}" {s}/>' for a in (90, 210, 330)))
    if kind == "control":  # gate: diamond with a check
        return (f'<polygon points="{cx},{cy - 9 * u} {cx + 9 * u},{cy} {cx},{cy + 9 * u} {cx - 9 * u},{cy}" {s}/>'
                f'<polyline points="{cx - 3.6 * u},{cy} {cx - 0.8 * u},{cy + 2.8 * u} {cx + 4 * u},{cy - 2.8 * u}" {s}/>')
    if kind == "store":  # cylinder
        return (f'<ellipse cx="{cx}" cy="{cy - 5.5 * u}" rx="{7.5 * u}" ry="{2.8 * u}" {s}/>'
                f'<path d="M{cx - 7.5 * u},{cy - 5.5 * u} V{cy + 5.5 * u} A{7.5 * u},{2.8 * u} 0 0 0 {cx + 7.5 * u},{cy + 5.5 * u} V{cy - 5.5 * u}" {s}/>'
                f'<path d="M{cx - 7.5 * u},{cy} A{7.5 * u},{2.8 * u} 0 0 0 {cx + 7.5 * u},{cy}" {s}/>')
    if kind == "record":  # ledger page
        return (f'<path d="M{cx - 6.5 * u},{cy - 9 * u} H{cx + 3 * u} L{cx + 6.5 * u},{cy - 5.5 * u} V{cy + 9 * u} H{cx - 6.5 * u} Z" {s}/>'
                + "".join(f'<line x1="{cx - 3.5 * u}" y1="{cy + k * u}" x2="{cx + 3.5 * u}" y2="{cy + k * u}" {s}/>'
                          for k in (-2.5, 1, 4.5)))
    if kind == "knowledge":  # stacked documents
        return (f'<rect x="{cx - 4.5 * u}" y="{cy - 9 * u}" width="{11 * u}" height="{14 * u}" rx="{1.5 * u}" {s}/>'
                f'<rect x="{cx - 7.5 * u}" y="{cy - 5.5 * u}" width="{11 * u}" height="{14.5 * u}" rx="{1.5 * u}" fill="{PANEL_FILL}" {sf}/>'
                f'<line x1="{cx - 4.8 * u}" y1="{cy - 1 * u}" x2="{cx + 0.8 * u}" y2="{cy - 1 * u}" {s}/>'
                f'<line x1="{cx - 4.8 * u}" y1="{cy + 3 * u}" x2="{cx + 0.8 * u}" y2="{cy + 3 * u}" {s}/>')
    if kind == "graph":  # entities joined by relationships
        pts = [(-6.5, -5), (6.5, -6.5), (5, 6), (-5.5, 6.5)]
        lines = "".join(f'<line x1="{cx + a[0] * u:.1f}" y1="{cy + a[1] * u:.1f}" x2="{cx + b[0] * u:.1f}" '
                        f'y2="{cy + b[1] * u:.1f}" {s}/>' for a, b in ((pts[0], pts[1]), (pts[1], pts[2]),
                                                                       (pts[0], pts[2]), (pts[2], pts[3])))
        return lines + "".join(f'<circle cx="{cx + x * u:.1f}" cy="{cy + y * u:.1f}" r="{2.6 * u:.1f}" '
                               f'fill="{PANEL_FILL}" {sf}/>' for x, y in pts)
    if kind == "human":  # person
        return (f'<circle cx="{cx}" cy="{cy - 4.5 * u}" r="{3.8 * u}" {s}/>'
                f'<path d="M{cx - 7.5 * u},{cy + 9 * u} C{cx - 7.5 * u},{cy + 1 * u} {cx + 7.5 * u},{cy + 1 * u} {cx + 7.5 * u},{cy + 9 * u}" {s}/>')
    if kind == "effect":  # target hit
        return (f'<circle cx="{cx}" cy="{cy}" r="{8.5 * u}" {s}/><circle cx="{cx}" cy="{cy}" r="{4.6 * u}" {s}/>'
                f'<circle cx="{cx}" cy="{cy}" r="{1.6 * u}" fill="{color}"/>')
    if kind == "external":  # building outside the boundary
        return (f'<rect x="{cx - 7 * u}" y="{cy - 6 * u}" width="{14 * u}" height="{15 * u}" {s}/>'
                f'<polyline points="{cx - 9 * u},{cy - 5 * u} {cx},{cy - 10 * u} {cx + 9 * u},{cy - 5 * u}" {s}/>'
                + "".join(f'<line x1="{cx + k * u}" y1="{cy - 2 * u}" x2="{cx + k * u}" y2="{cy + 9 * u}" {s}/>'
                          for k in (-3.5, 0, 3.5)))
    if kind == "actor":  # caller / request
        return (f'<rect x="{cx - 9 * u}" y="{cy - 7 * u}" width="{18 * u}" height="{12 * u}" rx="{1.8 * u}" {s}/>'
                f'<line x1="{cx - 4 * u}" y1="{cy + 9 * u}" x2="{cx + 4 * u}" y2="{cy + 9 * u}" {s}/>'
                f'<line x1="{cx}" y1="{cy + 5 * u}" x2="{cx}" y2="{cy + 9 * u}" {s}/>')
    if kind == "bad":  # refusal
        return (f'<circle cx="{cx}" cy="{cy}" r="{8.5 * u}" {s}/>'
                f'<line x1="{cx - 6 * u}" y1="{cy + 6 * u}" x2="{cx + 6 * u}" y2="{cy - 6 * u}" {s}/>')
    # service: stacked modules
    return (f'<rect x="{cx - 8.5 * u}" y="{cy - 8.5 * u}" width="{7.5 * u}" height="{7.5 * u}" rx="{1.4 * u}" {s}/>'
            f'<rect x="{cx + 1 * u}" y="{cy - 8.5 * u}" width="{7.5 * u}" height="{7.5 * u}" rx="{1.4 * u}" {s}/>'
            f'<rect x="{cx - 8.5 * u}" y="{cy + 1 * u}" width="{7.5 * u}" height="{7.5 * u}" rx="{1.4 * u}" {s}/>'
            f'<rect x="{cx + 1 * u}" y="{cy + 1 * u}" width="{7.5 * u}" height="{7.5 * u}" rx="{1.4 * u}" fill="{color}" fill-opacity="0.35" {sf}/>')


def no_entry(cx: float, cy: float, r: float = 24) -> str:
    red = EDGE_STYLE["prohibited"]["color"]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{BG_BOTTOM}" stroke="{red}" stroke-width="5"/>'
            f'<line x1="{cx - r * 0.62:.1f}" y1="{cy + r * 0.62:.1f}" x2="{cx + r * 0.62:.1f}" y2="{cy - r * 0.62:.1f}" '
            f'stroke="{red}" stroke-width="5" stroke-linecap="round"/>')


# --------------------------------------------------------------------- layout
class Diagram:
    def __init__(self, spec: dict, panel: tuple[int, int, int, int]):
        self.spec = spec
        px, py, pw, ph = panel
        self.x0, self.y0 = px + GRID_PAD_X, py + GRID_TOP
        self.cw = (pw - 2 * GRID_PAD_X) / GRID_COLS
        self.ch = (ph - GRID_TOP - GRID_BOTTOM) / GRID_ROWS
        self.boxes: dict[str, tuple[float, float, float, float]] = {}
        self.labels: list[tuple[float, float, float, float]] = []
        self.group_boxes: dict[str, tuple[float, float, float, float]] = {}
        self.badges = {c["ref"]: i + 1 for i, c in enumerate(spec["components"])}

    def gx(self, c: float) -> float:
        return self.x0 + c * self.cw

    def gy(self, r: float) -> float:
        return self.y0 + r * self.ch

    # Nodes ---------------------------------------------------------------
    def node_size(self, n: dict) -> tuple[float, float, list[str], list[str]]:
        label_size = n.get("size", 38)
        icon_w = 0 if n.get("noicon") else 118
        max_text = (n["w"] * self.cw if "w" in n else 470) - icon_w - 48
        lines = wrap(n["label"], label_size, max_text, bold=True)
        subs = wrap(n["sub"], 27, max_text) if n.get("sub") else []
        text_w = max(text_width(line, s, b) for line, s, b in
                     [(x, label_size, True) for x in lines] + [(x, 27, False) for x in subs])
        w = n["w"] * self.cw if "w" in n else max(300, icon_w + text_w + 56)
        h = n.get("h", 0) * self.ch or max(132, 54 + len(lines) * 44 + len(subs) * 34 + (6 if subs else 0))
        return w, h, lines, subs

    def render_node(self, n: dict) -> str:
        w, h, lines, subs = self.node_size(n)
        cx, cy = self.gx(n["at"][0]), self.gy(n["at"][1])
        x, y = cx - w / 2, cy - h / 2
        self.boxes[n["id"]] = (x, y, w, h)
        color = TONE[n.get("tone", n["kind"])]
        hot = n["id"] in self.badges
        depth = 16
        out = [f'<g>',
               f'<rect x="{x - 6:.1f}" y="{y + 4:.1f}" width="{w + 12:.1f}" height="{h + 18:.1f}" rx="24" '
               f'fill="{color}" fill-opacity="{0.42 if hot else 0.22}" filter="url(#glow)"/>',
               f'<rect x="{x:.1f}" y="{y + depth:.1f}" width="{w:.1f}" height="{h:.1f}" rx="20" fill="#06142B" '
               f'stroke="{color}" stroke-opacity="0.45" stroke-width="2"/>',
               f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="20" fill="url(#card)" '
               f'stroke="{color}" stroke-width="{4 if hot else 3}"/>',
               f'<rect x="{x + 3:.1f}" y="{y + 3:.1f}" width="{w - 6:.1f}" height="{h * 0.42:.1f}" rx="17" '
               f'fill="url(#sheen)"/>']
        tx = x + 32
        if not n.get("noicon"):
            ix, iy = x + 26, cy - 43
            out.append(f'<rect x="{ix:.1f}" y="{iy:.1f}" width="86" height="86" rx="18" fill="{color}" '
                       f'fill-opacity="0.16" stroke="{color}" stroke-opacity="0.55" stroke-width="2"/>')
            out.append(icon(n["kind"], ix + 43, iy + 43, 31, color))
            tx = x + 140
        label_size = n.get("size", 38)
        block = len(lines) * 44 + len(subs) * 34 + (6 if subs else 0)
        ty = cy - block / 2 + 34
        anchor = "start"
        if n.get("noicon"):
            tx, anchor = cx, "middle"
        for line in lines:
            out.append(t(tx, ty, line, label_size, INK_WHITE, bold=True, anchor=anchor))
            ty += 44
        for line in subs:
            out.append(t(tx, ty + 2, line, 27, INK_SOFT, anchor=anchor, opacity=0.9))
            ty += 34
        out.append("</g>")
        return "\n".join(out)

    # Groups --------------------------------------------------------------
    def render_group(self, g: dict) -> str:
        c0, r0, c1, r1 = g["box"]
        x, y, x1, y1 = self.gx(c0), self.gy(r0), self.gx(c1), self.gy(r1)
        w, h = x1 - x, y1 - y
        color = TONE[g.get("tone", "cyan")]
        style = g.get("style", "zone")
        if "id" in g:
            self.group_boxes[g["id"]] = (x, y, w, h - 16)
        out = []
        if style == "band":
            out.append(f'<rect x="{x:.1f}" y="{y + 14:.1f}" width="{w:.1f}" height="{h:.1f}" rx="22" fill="#030B19" '
                       f'stroke="{color}" stroke-opacity="0.35" stroke-width="2"/>')
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="22" fill="{color}" '
                       f'fill-opacity="0.07" stroke="{color}" stroke-opacity="0.7" stroke-width="2.5"/>')
        elif style == "boundary":
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="30" fill="{color}" '
                       f'fill-opacity="0.05" stroke="{color}" stroke-width="5" filter="url(#softglow)"/>')
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="30" fill="none" '
                       f'stroke="{color}" stroke-width="4"/>')
        else:
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="26" fill="{color}" '
                       f'fill-opacity="0.045" stroke="{color}" stroke-opacity="0.75" stroke-width="3" '
                       f'stroke-dasharray="16 10"/>')
        label = g["label"].upper()
        size = 28
        lw = text_width(label, size, True, 2.5)
        where = g.get("label_at", "top-left")
        lx = x + 34 if where.endswith("left") else x + w - 34 - lw
        ly = y if where.startswith("top") else y + h
        self.labels.append((lx - 16, ly - 25, lw + 32, 34))
        out.append(f'<rect x="{lx - 16:.1f}" y="{ly - 25:.1f}" width="{lw + 32:.1f}" height="50" rx="25" '
                   f'fill="{BG_BOTTOM}" stroke="{color}" stroke-width="2.5"/>')
        out.append(t(lx, ly + 10, label, size, color, bold=True, spacing=2.5))
        return "\n".join(out)

    # Edges ---------------------------------------------------------------
    def anchor(self, box, side: str):
        x, y, w, h = box
        return {"left": (x, y + h / 2, -1, 0), "right": (x + w, y + h / 2, 1, 0),
                "top": (x + w / 2, y, 0, -1), "bottom": (x + w / 2, y + h + 16, 0, 1)}[side]

    def sides(self, a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        dx = (bx + bw / 2) - (ax + aw / 2)
        dy = (by + bh / 2) - (ay + ah / 2)
        if abs(dx) / (aw + bw) >= abs(dy) / (ah + bh):
            return ("right", "left") if dx > 0 else ("left", "right")
        return ("bottom", "top") if dy > 0 else ("top", "bottom")

    def clip(self, box, x0, y0, x1, y1):
        """Where the segment from inside `box` toward (x1, y1) leaves the box."""
        x, y, w, h = box
        x, y, w, h = x - 4, y - 4, w + 8, h + 8 + 16
        best = 1.0
        dx, dy = x1 - x0, y1 - y0
        for edge, d, lo in ((x, dx, x0), (x + w, dx, x0), (y, dy, y0), (y + h, dy, y0)):
            if d:
                u = (edge - lo) / d
                if 0 < u < best:
                    px, py = x0 + u * dx, y0 + u * dy
                    if x - 0.5 <= px <= x + w + 0.5 and y - 0.5 <= py <= y + h + 0.5:
                        best = u
        return x0 + best * dx, y0 + best * dy

    def place_label(self, e: dict, pts, label_t: float):
        """First spot along the edge whose label clears every card and label."""
        if not e.get("label") and e.get("style") != "prohibited":
            return along(pts, label_t)
        w = text_width(e.get("label", ""), 28, True) + 36 + (70 if e.get("style") == "prohibited" else 0)
        h = 52
        fixed = "label_dx" in e or "label_dy" in e or e.get("label_fixed")
        tries = [label_t] if fixed else [label_t] + [label_t + d * s for d in (0.07, 0.14, 0.21, 0.28)
                                                       for s in (1, -1)]
        best = None
        for u in tries:
            if not 0.12 <= u <= 0.88 and u != label_t:
                continue
            mx, my = along(pts, u)
            mx, my = mx + e.get("label_dx", 0), my + e.get("label_dy", 0)
            rect = (mx - w / 2, my - h / 2, w, h)
            hits = [r for r in list(self.boxes.values()) + self.labels if overlap(rect, r)]
            if not hits:
                best = rect
                break
            if best is None:
                best = rect
        self.labels.append(best)
        return best[0] + w / 2, best[1] + h / 2

    def render_edge(self, e: dict) -> str:
        a = self.boxes.get(e["from"]) or self.group_boxes[e["from"]]
        b = self.boxes.get(e["to"]) or self.group_boxes[e["to"]]
        style_name = e.get("style", "normal")
        style = EDGE_STYLE[style_name]
        color = style["color"]
        route = e.get("route", "curve")
        off = e.get("offset", 0)  # separates parallel edges between one pair
        gap = 22  # leave room for the arrowhead
        label_t = e.get("label_t", 0.5)
        if route == "straight":
            acx, acy = a[0] + a[2] / 2, a[1] + a[3] / 2 + 8
            bcx, bcy = b[0] + b[2] / 2, b[1] + b[3] / 2 + 8
            L = math.hypot(bcx - acx, bcy - acy) or 1
            nx, ny = -(bcy - acy) / L, (bcx - acx) / L
            acx, acy, bcx, bcy = acx + nx * off, acy + ny * off, bcx + nx * off, bcy + ny * off
            sx, sy = self.clip(a, acx, acy, bcx, bcy)
            ex, ey = self.clip(b, bcx, bcy, acx, acy)
            if "from_side" in e:
                sx, sy, _, _ = self.anchor(a, e["from_side"])
            if "to_side" in e:  # land square on one face, clear of corner badges
                ex, ey, _, _ = self.anchor(b, e["to_side"])
                ey += e.get("to_dy", 0)
            L = math.hypot(ex - sx, ey - sy) or 1
            ex2, ey2 = ex - (ex - sx) / L * gap, ey - (ey - sy) / L * gap
            pts = [(sx, sy), (ex2, ey2)]
        else:
            s_side, t_side = self.sides(a, b)
            s_side, t_side = e.get("from_side", s_side), e.get("to_side", t_side)
            sx, sy, snx, sny = self.anchor(a, s_side)
            ex, ey, enx, eny = self.anchor(b, t_side)
            sx, sy = sx + off * abs(sny) + e.get("from_shift", 0), sy + off * abs(snx)
            ex, ey = ex + off * abs(eny) + e.get("to_shift", 0), ey + off * abs(enx)
            ex2, ey2 = ex + enx * gap, ey + eny * gap
            if route == "ortho" or "points" in e:
                if "points" in e:
                    mids = [(self.gx(c), self.gy(r)) for c, r in e["points"]]
                elif snx and enx:  # horizontal out, horizontal in
                    mx = (sx + ex2) / 2 + e.get("bend", 0)
                    mids = [(mx, sy), (mx, ey2)]
                elif sny and eny:
                    my = (sy + ey2) / 2 + e.get("bend", 0)
                    mids = [(sx, my), (ex2, my)]
                elif snx:
                    mids = [(ex2, sy)]
                else:
                    mids = [(sx, ey2)]
                pts = [(sx, sy)] + mids + [(ex2, ey2)]
            else:
                dist = math.hypot(ex - sx, ey - sy)
                k = e.get("pull", max(70, dist * 0.42))
                c1 = (sx + snx * k, sy + sny * k)
                c2 = (ex2 + enx * k, ey2 + eny * k)
                pts = [bezier((sx, sy), c1, c2, (ex2, ey2), i / 48) for i in range(49)]
                route = "sampled"
        d = rounded_path(pts, 0 if route == "sampled" else e.get("radius", 36))
        dash = f' stroke-dasharray="{style["dash"]}"' if style["dash"] else ""
        out = [f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="0.22" stroke-width="16" '
               f'stroke-linecap="round" stroke-linejoin="round" filter="url(#softglow)"/>',
               f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" '
               f'stroke-linejoin="round"{dash} marker-end="url(#arrow-{style_name})"/>']
        if style_name == "normal" and not e.get("nodots"):
            for tt in (0.14, 0.86):
                px, py = along(pts, tt)
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="#E8FBFF"/>')
        mx, my = self.place_label(e, pts, label_t)
        if style_name == "prohibited":
            if e.get("label"):
                lw = text_width(e["label"], 28, True)
                out.append(no_entry(mx - lw / 2 - 18, my))
                out.append(pill(mx + 35, my, e["label"], color))
            else:
                out.append(no_entry(mx, my))
        elif e.get("label"):
            out.append(pill(mx, my, e["label"], color))
        return "\n".join(out)


def overlap(a, b, pad: float = 10) -> bool:
    return not (a[0] + a[2] + pad <= b[0] or b[0] + b[2] + pad <= a[0]
                or a[1] + a[3] + pad <= b[1] or b[1] + b[3] + 16 + pad <= a[1])


def rounded_path(pts, radius: float) -> str:
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        l1, l2 = math.hypot(x1 - x0, y1 - y0) or 1, math.hypot(x2 - x1, y2 - y1) or 1
        r = min(radius, l1 / 2, l2 / 2)
        if r <= 0:
            d += f" L{x1:.1f},{y1:.1f}"
            continue
        ax, ay = x1 - (x1 - x0) / l1 * r, y1 - (y1 - y0) / l1 * r
        bx, by = x1 + (x2 - x1) / l2 * r, y1 + (y2 - y1) / l2 * r
        d += f" L{ax:.1f},{ay:.1f} Q{x1:.1f},{y1:.1f} {bx:.1f},{by:.1f}"
    d += f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return d


def along(pts, u: float):
    lengths = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    target = sum(lengths) * u
    for i, seg in enumerate(lengths):
        if target <= seg or i == len(lengths) - 1:
            f = target / seg if seg else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
        target -= seg
    return pts[-1]


def pill(cx: float, cy: float, label: str, color: str) -> str:
    w = text_width(label, 28, True) + 36
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - 24:.1f}" width="{w:.1f}" height="48" rx="24" '
            f'fill="{BG_BOTTOM}" stroke="{color}" stroke-width="2.5"/>'
            + t(cx, cy + 10, label, 28, INK_WHITE, bold=True, anchor="middle"))


def bezier(p0, p1, p2, p3, u):
    v = 1 - u
    return (v ** 3 * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u ** 3 * p3[0],
            v ** 3 * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u ** 3 * p3[1])


# --------------------------------------------------------------------- page
def defs(accent: str) -> str:
    arrows = "".join(
        f'<marker id="arrow-{name}" viewBox="0 0 12 12" refX="3" refY="6" markerWidth="5.2" markerHeight="5.2" '
        f'orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0 L12,6 L0,12 Z" fill="{s["color"]}"/></marker>'
        for name, s in EDGE_STYLE.items())
    return f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{accent}" stop-opacity="0.16"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CARD_TOP}"/><stop offset="1" stop-color="{CARD_BOTTOM}"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="20"/></filter>
<filter id="softglow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
{arrows}
</defs>"""


def iso_grid(panel: tuple[int, int, int, int]) -> str:
    """Faint isometric floor behind the diagram, echoing the Part visuals."""
    px, py, pw, ph = panel
    lines = []
    step = 90
    slope = math.tan(math.radians(30))
    span = pw + ph / slope
    k = -ph / slope
    while k < pw + ph / slope:
        x0 = px + k
        lines.append(f'M{x0:.0f},{py} L{x0 + ph / slope:.0f},{py + ph}')
        lines.append(f'M{x0 + ph / slope:.0f},{py} L{x0:.0f},{py + ph}')
        k += step / slope * 0.5 * 2
    del span
    return (f'<g clip-path="url(#panel)"><path d="{" ".join(lines)}" stroke="#3D8BF2" stroke-opacity="0.10" '
            f'stroke-width="1.5" fill="none"/></g>')


def render_page(ch: dict, part_titles: dict, book: dict) -> str:
    accent = ACCENTS["cyan" if ch["part_index"] % 2 else "blue"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" height="{PAGE_H}" '
           f'viewBox="0 0 {PAGE_W} {PAGE_H}">', defs(accent),
           f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="url(#bg)"/>',
           f'<rect x="40" y="40" width="{PAGE_W - 80}" height="{PAGE_H - 80}" fill="none" stroke="{accent}" '
           f'stroke-opacity="0.55" stroke-width="3"/>']

    # Identity block ------------------------------------------------------
    x = MARGIN
    out.append(f'<rect x="{x}" y="150" width="560" height="9" fill="{accent}"/>')
    out.append(t(x, 232, "ENTERPRISE GENERAL INTELLIGENCE PLATFORM", 36, INK_SOFT, bold=True, spacing=3))
    tag = f"PART {ch['part']}  ·  CHAPTER {ch['chapter']:02d}"
    tw = text_width(tag, 40, True, 2)
    out.append(f'<rect x="{x}" y="280" width="{tw + 72:.0f}" height="86" rx="43" fill="{accent}"/>')
    out.append(t(x + 36, 337, tag, 40, "#04122A", bold=True, spacing=2))
    out.append(t(x + tw + 112, 337, part_titles[ch["part"]].upper(), 32, INK_MUTED, bold=True, spacing=2.5))

    title = ch["title"].upper()
    width = PAGE_W - 2 * MARGIN
    for size in (124, 116, 108, 100, 92, 86):
        lines = wrap(title, size, width, bold=True)
        if len(lines) <= 3:
            break
    y = 400 + size * 1.0
    for line in lines:
        out.append(t(x, y, line, size, INK_WHITE, bold=True, spacing=-1))
        y += size * 1.08
    y += 6 - size * 1.08 + 46
    out.append(f'<rect x="{x}" y="{y:.0f}" width="150" height="10" fill="{accent}"/>')
    y += 96
    for line in wrap(ch["focus"], 54, width):
        out.append(t(x, y, line, 54, INK_SOFT))
        y += 70
    y += 8
    cx = x
    for theme in ch["themes"]:
        label = theme.upper()
        w = text_width(label, 30, True, 1.5) + 64
        out.append(f'<rect x="{cx}" y="{y:.0f}" width="{w:.0f}" height="70" rx="35" fill="#0B2245" '
                   f'stroke="{accent}" stroke-width="3"/>')
        out.append(t(cx + 32, y + 46, label, 30, INK_WHITE, bold=True, spacing=1.5))
        cx += w + 26
    header_bottom = y + 70
    top = max(PANEL_MIN_TOP, round(header_bottom + PANEL_GAP))
    panel = (MARGIN, top, PAGE_W - 2 * MARGIN, PANEL_BOTTOM - top)
    if panel[3] < 1600:
        raise ValueError(f"chapter {ch['chapter']}: identity block leaves too little room for the diagram")

    # Diagram panel -------------------------------------------------------
    px, py, pw, ph = panel
    out.append(f'<defs><clipPath id="panel"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="28"/></clipPath></defs>')
    out.append(f'<ellipse cx="{px + pw / 2}" cy="{py + ph / 2 + 60}" rx="{pw * 0.62}" ry="{ph * 0.55}" fill="url(#halo)"/>')
    out.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="28" fill="{PANEL_FILL}" fill-opacity="0.55" '
               f'stroke="{accent}" stroke-opacity="0.45" stroke-width="2.5"/>')
    out.append(iso_grid(panel))
    d = ch["diagram"]
    out.append(t(px + 60, py + 82, "CHAPTER CONCEPT", 30, accent, bold=True, spacing=3))
    out.append(t(px + 60 + text_width("CHAPTER CONCEPT", 30, True, 3) + 30, py + 82,
                 d["title"], 38, INK_WHITE, bold=True))
    dg = Diagram(d, panel)
    for g in d.get("groups", []):
        out.append(dg.render_group(g))
    nodes = [dg.render_node(n) for n in d["nodes"]]
    badge_at = {}
    for ref in dg.badges:
        if ref in dg.boxes:
            bx, by, _, _ = dg.boxes[ref]
            badge_at[ref] = (bx - 8, by - 8)
        else:
            g = next(g for g in d.get("groups", []) if g.get("id") == ref)
            badge_at[ref] = (dg.gx(g["box"][2]) - 8, dg.gy(g["box"][1]))
        x0, y0 = badge_at[ref]
        dg.labels.append((x0 - 40, y0 - 40, 80, 64))
    edges = [dg.render_edge(e) for e in d["edges"]]
    out += edges + nodes
    for ref, number in dg.badges.items():
        out.append(badge(*badge_at[ref], number, accent))
    for note in d.get("notes", []):
        out.append(t(dg.gx(note["at"][0]), dg.gy(note["at"][1]), note["text"], note.get("size", 30),
                     TONE.get(note.get("tone", ""), INK_MUTED), bold=note.get("bold", False),
                     anchor=note.get("anchor", "middle")))

    # Component legend ------------------------------------------------------
    ly = py + ph + 70
    out.append(t(x, ly, "KEY COMPONENTS", 30, accent, bold=True, spacing=3))
    legend = legend_keys(d)
    lx = PAGE_W - MARGIN
    for label, kind in reversed(legend):
        w = text_width(label, 26) + 58
        lx -= w
        if kind == "prohibited":
            out.append(no_entry(lx + 20, ly - 10, 16))
        else:
            out.append(icon(kind, lx + 20, ly - 10, 17, TONE[kind]))
        out.append(t(lx + 48, ly, label, 26, INK_MUTED))
        lx -= 30
    box_w = (width - 40) / 2
    for i, comp in enumerate(d["components"]):
        bx = x + (i % 2) * (box_w + 40)
        by = ly + 34 + (i // 2) * 128
        out.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{box_w:.0f}" height="104" rx="18" fill="#081A35" '
                   f'stroke="{accent}" stroke-opacity="0.8" stroke-width="3"/>')
        out.append(f'<rect x="{bx + 20:.0f}" y="{by + 18:.0f}" width="68" height="68" rx="16" fill="{accent}"/>')
        out.append(t(bx + 54, by + 66, str(i + 1), 40, "#04122A", bold=True, anchor="middle"))
        out.append(t(bx + 116, by + 66, comp["name"], 40, INK_WHITE, bold=True))

    # Footer ----------------------------------------------------------------
    fy = PAGE_H - 108
    out.append(t(x, fy, book['author'].upper(), 30, INK_SOFT, bold=True, spacing=1.5))
    out.append(t(PAGE_W - MARGIN, fy, f"CHAPTER {ch['chapter']:02d}", 30, accent, bold=True, spacing=3, anchor="end"))
    out.append("</svg>")
    return "\n".join(out)


def badge(x: float, y: float, number: int, accent: str) -> str:
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="44" fill="{accent}" fill-opacity="0.35" filter="url(#softglow)"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="34" fill="{accent}" stroke="#E8FBFF" stroke-width="4"/>'
            + t(x, y + 14, str(number), 40, "#04122A", bold=True, anchor="middle"))


def legend_keys(d: dict) -> list[tuple[str, str]]:
    names = {"model": "reasoning", "control": "gate / policy", "store": "store", "record": "record",
             "knowledge": "knowledge", "graph": "graph", "human": "human", "effect": "effect", "external": "external",
             "actor": "actor", "service": "service", "bad": "refusal"}
    names.update(d.get("legend", {}))
    seen, keys = set(), []
    for n in d["nodes"]:
        if n.get("noicon"):
            continue
        kind = n["kind"]
        if kind not in seen and kind in names:
            seen.add(kind)
            keys.append((names[kind], kind))
    if any(e.get("style") == "prohibited" for e in d["edges"]):
        keys.append(("prohibited path", "prohibited"))
    return keys


# --------------------------------------------------------------------- build
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rasterize(svg: str, png: Path) -> None:
    with tempfile.TemporaryDirectory() as work:
        src, raw = Path(work) / "c.svg", Path(work) / "c.png"
        src.write_text(svg, encoding="utf-8")
        subprocess.run(["rsvg-convert", "-f", "png", "-w", str(PAGE_W), "-h", str(PAGE_H),
                        "-o", str(raw), str(src)], check=True, capture_output=True)
        with Image.open(raw) as image:
            staged = Path(work) / "s.png"
            image.convert("RGB").save(staged, dpi=(DPI, DPI), optimize=True)
        if png.exists():
            with Image.open(staged) as a, Image.open(png) as b:
                if a.size == b.size and a.convert("RGB").tobytes() == b.convert("RGB").tobytes():
                    return
        shutil.copy2(staged, png)


def contact_sheet(files: list[Path], out: Path) -> None:
    cols, thumb_w = 7, 500
    thumb_h = int(thumb_w * PAGE_H / PAGE_W)
    gap = 30
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap, rows * thumb_h + (rows + 1) * gap), BG_BOTTOM)
    for i, f in enumerate(files):
        with Image.open(f) as image:
            thumb = image.resize((thumb_w, thumb_h), Image.LANCZOS)
        sheet.paste(thumb, (gap + (i % cols) * (thumb_w + gap), gap + (i // cols) * (thumb_h + gap)))
    with tempfile.TemporaryDirectory() as work:
        staged = Path(work) / "o.png"
        sheet.save(staged, dpi=(150, 150), optimize=True)
        if out.exists():
            with Image.open(staged) as a, Image.open(out) as b:
                if a.size == b.size and a.tobytes() == b.convert("RGB").tobytes():
                    return
        shutil.copy2(staged, out)


def validate(ch: dict) -> list[str]:
    errors = []
    d = ch["diagram"]
    ids = {n["id"] for n in d["nodes"]} | {g["id"] for g in d.get("groups", []) if "id" in g}
    if len(ch["themes"]) != 3:
        errors.append("needs exactly 3 themes")
    if len(d["components"]) != 4:
        errors.append("needs exactly 4 components")
    for c in d["components"]:
        if c["ref"] not in ids:
            errors.append(f"component ref {c['ref']!r} is not a node or group")
    for e in d["edges"]:
        for end in ("from", "to"):
            if e[end] not in ids:
                errors.append(f"edge endpoint {e[end]!r} is unknown")
    for n in d["nodes"]:
        if n["kind"] not in KIND_COLOR:
            errors.append(f"node {n['id']!r} has unknown kind {n['kind']!r}")
    return [f"chapter {ch['chapter']}: {e}" for e in errors]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--only", type=int, help="render a single chapter number")
    parser.add_argument("--svg", action="store_true", help="also keep the SVG next to each PNG")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if shutil.which("rsvg-convert") is None:
        print(json.dumps({"pass": False, "errors": ["rsvg-convert is not installed"]}, indent=2))
        return 1
    book = json.loads((root / "config" / "book.json").read_text(encoding="utf-8"))["book"]
    spec = json.loads((root / "config" / "chapter-covers.json").read_text(encoding="utf-8"))
    out_dir = root / spec["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    part_order = [p["id"] for p in json.loads((root / "config" / "book.json").read_text())["structure"]["parts"]]
    part_titles = {p["id"]: p["title"] for p in spec["parts"]}

    errors, records, files = [], [], []
    for ch in spec["chapters"]:
        errors += validate(ch)
    if errors:
        print(json.dumps({"pass": False, "errors": errors}, indent=2))
        return 1

    for ch in spec["chapters"]:
        ch["part_index"] = part_order.index(ch["part"]) + 1
        png = out_dir / ch["file"]
        files.append(png)
        if args.only and args.only != ch["chapter"]:
            continue
        svg = render_page(ch, part_titles, book)
        if args.svg:
            png.with_suffix(".svg").write_text(svg, encoding="utf-8")
        rasterize(svg, png)
    if not args.only:
        contact_sheet(files, out_dir / "00-overview-all-chapters.png")
    for png in files:
        if not png.exists():
            errors.append(f"missing {png.relative_to(root)}")
            continue
        with Image.open(png) as image:
            size, dpi = image.size, image.info.get("dpi", (0, 0))
        if size != (PAGE_W, PAGE_H) or round(dpi[0]) != DPI:
            errors.append(f"{png.name}: {size} at {dpi} is not Letter at {DPI} dpi")
        records.append({"file": str(png.relative_to(root)), "pixels": list(size), "sha256": sha256(png)})

    report = {"covers": len(records), "page": "US Letter 8.5x11 in", "dpi": DPI,
              "records": records, "errors": errors, "pass": not errors}
    (root / "reports" / "chapter-cover-report.json").write_text(json.dumps(report, indent=2) + "\n",
                                                                encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
