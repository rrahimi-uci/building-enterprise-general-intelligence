#!/usr/bin/env python3
"""Render the book-cover artwork from code: the book's thesis as one picture.

The cover art is a vector composition, not stock imagery, so it can say what
the book argues. A bounded model sits at the centre and only *proposes*; a
deterministic shell of gates surrounds it; governed, pinned knowledge forms the
next ring; and a durable, governed workflow carries the four controls the book
builds -- admission, policy, the gateway, and evaluation and release. Intent
enters on the left; only a verified effect reaches the systems of record on the
right; and evidence loops back underneath into evaluation and release.

The visual language (deep-navy field, cyan/blue accents, role-coloured glyphs)
is shared with the chapter covers in `tools/render_chapter_covers.py`, whose
icon glyphs this module reuses so a role reads the same everywhere.

Output: `assets/cover/cover-art.png`, 2550 x 3300 px (US Letter at 300 dpi). The
top third is left quiet for the title, which `tools/generate_cover.py` sets on
top. This step needs rsvg-convert and runs locally (`make cover-art`); the PNG is
committed so the normal build and CI never need an SVG renderer.

Idempotent by content: an unchanged render leaves the file alone.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_chapter_covers import icon, rasterize, sha256, t  # noqa: E402

W, H = 2550, 3300
CX, CY = 1275, 1860            # centre of the governed platform
R_PLATFORM, R_KNOW, R_SHELL, R_CORE = 600, 405, 250, 140

NAVY_TOP, NAVY_MID, NAVY_DEEP = "#071833", "#0A2149", "#030B19"
CYAN, CYAN_SOFT, BLUE, TEAL = "#20B8D8", "#5FD4EE", "#3D8BF2", "#2FC2B5"
AMBER, PLUM, INK, INK_SOFT = "#F2B35A", "#C98BE0", "#FFFFFF", "#D6E5F5"


def hexagon(cx: float, cy: float, r: float) -> str:
    """Flat-topped hexagon points."""
    return " ".join(f"{cx + r * math.cos(math.radians(a)):.1f},{cy + r * math.sin(math.radians(a)):.1f}"
                    for a in range(0, 360, 60))


def label(x: float, y: float, text: str, size: int = 38, color: str = INK_SOFT, anchor: str = "middle") -> str:
    return t(x, y, text, size, color, bold=True, anchor=anchor, spacing=5)


def defs() -> str:
    return f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{NAVY_DEEP}"/><stop offset="0.32" stop-color="{NAVY_TOP}"/>
  <stop offset="0.62" stop-color="{NAVY_MID}"/><stop offset="1" stop-color="{NAVY_DEEP}"/></linearGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{CYAN}" stop-opacity="0.30"/><stop offset="0.55" stop-color="{BLUE}" stop-opacity="0.10"/>
  <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="platform" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#0E3466" stop-opacity="0.85"/><stop offset="0.8" stop-color="#0A2449" stop-opacity="0.55"/>
  <stop offset="1" stop-color="#081B38" stop-opacity="0.35"/></radialGradient>
<radialGradient id="core" cx="0.42" cy="0.38" r="0.7">
  <stop offset="0" stop-color="#B9FFF6"/><stop offset="0.35" stop-color="{TEAL}"/><stop offset="1" stop-color="#0A4A57"/></radialGradient>
<radialGradient id="corehalo" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{TEAL}" stop-opacity="0.75"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{BLUE}" stop-opacity="0.2"/><stop offset="0.5" stop-color="{CYAN_SOFT}"/>
  <stop offset="1" stop-color="{PLUM}"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#143862"/><stop offset="1" stop-color="#0B2447"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="bigglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
<marker id="tip" viewBox="0 0 12 12" refX="4" refY="6" markerWidth="4.5" markerHeight="4.5" orient="auto" markerUnits="strokeWidth">
  <path d="M0,0 L12,6 L0,12 Z" fill="{CYAN_SOFT}"/></marker>
<marker id="tip-amber" viewBox="0 0 12 12" refX="4" refY="6" markerWidth="4.5" markerHeight="4.5" orient="auto" markerUnits="strokeWidth">
  <path d="M0,0 L12,6 L0,12 Z" fill="{AMBER}"/></marker>
</defs>"""


def background() -> str:
    out = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
           f'<circle cx="{CX}" cy="{CY}" r="1250" fill="url(#halo)"/>']
    # A faint circuit floor: a square grid that fades away from the platform.
    grid = []
    for k in range(-30, 31):
        grid.append(f"M{CX + k * 110},{CY - 1500} V{CY + 1500}")
        grid.append(f"M{CX - 1500},{CY + k * 110} H{CX + 1500}")
    out.append(f'<g opacity="0.05" stroke="{CYAN_SOFT}" stroke-width="2"><path d="{" ".join(grid)}"/></g>')
    # Deterministic star-field of tiny nodes, denser near the platform.
    rnd = random.Random(42)
    dots = []
    for _ in range(260):
        a, d = rnd.uniform(0, 2 * math.pi), abs(rnd.gauss(0, 900)) + 700
        x, y = CX + d * math.cos(a), CY + d * 0.8 * math.sin(a)
        if 0 < x < W and 1150 < y < H - 250:
            dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice((2, 3, 3, 4))}" '
                        f'fill="{rnd.choice((CYAN_SOFT, BLUE, INK_SOFT))}" opacity="{rnd.uniform(0.15, 0.45):.2f}"/>')
    out.append("".join(dots))
    return "\n".join(out)


def platform() -> str:
    """Outer ring: the durable, governed workflow that carries the controls."""
    ticks = []
    for deg in range(0, 360, 4):
        r0 = R_PLATFORM + 56 + (10 if deg % 20 == 0 else 0)
        a = math.radians(deg)
        ticks.append(f"M{CX + (R_PLATFORM + 46) * math.cos(a):.1f},{CY + (R_PLATFORM + 46) * math.sin(a):.1f} "
                     f"L{CX + r0 * math.cos(a):.1f},{CY + r0 * math.sin(a):.1f}")
    return f"""
<circle cx="{CX}" cy="{CY}" r="{R_PLATFORM}" fill="url(#platform)"/>
<circle cx="{CX}" cy="{CY}" r="{R_PLATFORM}" fill="none" stroke="{BLUE}" stroke-width="16" opacity="0.45" filter="url(#glow)"/>
<circle cx="{CX}" cy="{CY}" r="{R_PLATFORM}" fill="none" stroke="{BLUE}" stroke-width="5"/>
<circle cx="{CX}" cy="{CY}" r="{R_PLATFORM - 22}" fill="none" stroke="{BLUE}" stroke-width="2" opacity="0.45"/>
<path d="{' '.join(ticks)}" stroke="{CYAN_SOFT}" stroke-width="3" opacity="0.35"/>
{label(CX, CY - R_PLATFORM + 150, "DURABLE · GOVERNED WORKFLOW", 30, CYAN_SOFT)}"""


def knowledge() -> str:
    """Middle ring: governed, pinned knowledge and context."""
    nodes = []
    for deg in (205, 240, 300, 335):
        a = math.radians(deg)
        x, y = CX + R_KNOW * math.cos(a), CY + R_KNOW * math.sin(a)
        nodes.append(f'<rect x="{x - 26:.1f}" y="{y - 26:.1f}" width="52" height="52" rx="10" fill="#0A2A44" '
                     f'stroke="{CYAN}" stroke-width="3"/>'
                     f'<path d="M{x - 12:.1f},{y - 8:.1f} H{x + 12:.1f} M{x - 12:.1f},{y + 1:.1f} H{x + 12:.1f} '
                     f'M{x - 12:.1f},{y + 10:.1f} H{x + 4:.1f}" stroke="{CYAN_SOFT}" stroke-width="3" stroke-linecap="round"/>')
    return f"""
<circle cx="{CX}" cy="{CY}" r="{R_KNOW}" fill="#0B2E55" fill-opacity="0.55" stroke="{CYAN}" stroke-width="4" stroke-dasharray="26 14"/>
<circle cx="{CX}" cy="{CY}" r="{R_KNOW}" fill="none" stroke="{CYAN}" stroke-width="12" opacity="0.25" filter="url(#glow)"/>
{''.join(nodes)}
{label(CX, CY + 300, "GOVERNED KNOWLEDGE", 28, CYAN_SOFT)}"""


def shell_and_core() -> str:
    """The deterministic shell of gates, and the bounded model inside it."""
    gates = []
    for deg in (0, 180):          # where the request path crosses the shell
        a = math.radians(deg)
        x, y = CX + R_SHELL * math.cos(a), CY + R_SHELL * math.sin(a)
        gates.append(f'<polygon points="{x},{y - 34} {x + 34},{y} {x},{y + 34} {x - 34},{y}" fill="#2B1F08" '
                     f'stroke="{AMBER}" stroke-width="5"/>'
                     f'<polyline points="{x - 13},{y} {x - 3},{y + 10} {x + 14},{y - 10}" fill="none" stroke="{AMBER}" '
                     f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    # A small neural network inside the core: the part that reasons.
    rnd = random.Random(7)
    pts = [(CX + rnd.uniform(-78, 78), CY + rnd.uniform(-70, 70)) for _ in range(9)] + [(CX, CY)]
    links = []
    for i, (x1, y1) in enumerate(pts):
        for x2, y2 in pts[i + 1:]:
            if math.hypot(x2 - x1, y2 - y1) < 105:
                links.append(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}")
    net = (f'<path d="{" ".join(links)}" stroke="#E9FFFC" stroke-width="3" opacity="0.65"/>'
           + "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{9 if (x, y) == (CX, CY) else 6}" fill="#FFFFFF"/>'
                     for x, y in pts))
    return f"""
<polygon points="{hexagon(CX, CY, R_SHELL)}" fill="#120E05" fill-opacity="0.35" stroke="{AMBER}" stroke-width="14" opacity="0.35" filter="url(#glow)"/>
<polygon points="{hexagon(CX, CY, R_SHELL)}" fill="none" stroke="{AMBER}" stroke-width="5"/>
<polygon points="{hexagon(CX, CY, R_SHELL - 16)}" fill="none" stroke="{AMBER}" stroke-width="2" opacity="0.5"/>
<circle cx="{CX}" cy="{CY}" r="300" fill="url(#corehalo)" filter="url(#bigglow)"/>
<polygon points="{hexagon(CX, CY, R_CORE)}" fill="url(#core)" stroke="#B9FFF6" stroke-width="4"/>
{net}
{''.join(gates)}
{label(CX, CY + 162, "MODEL PROPOSES", 26, INK)}"""


def badge(x: float, y: float, kind: str, color: str, text: str, text_dy: float) -> str:
    """One platform control on the outer ring: a lit disc with a role glyph."""
    return (f'<circle cx="{x}" cy="{y}" r="104" fill="{color}" opacity="0.30" filter="url(#glow)"/>'
            f'<circle cx="{x}" cy="{y}" r="82" fill="url(#card)" stroke="{color}" stroke-width="6"/>'
            + icon(kind, x, y, 40, color)
            + label(x, y + text_dy, text, 36, INK))


def flows() -> str:
    """Intent in, verified effect out, evidence back into evaluation and release."""
    y = CY
    xs_in, xs_out = 330, 2225
    beam = (f'<path d="M{xs_in + 110},{y} H{CX - R_SHELL - 40}" stroke="{CYAN_SOFT}" stroke-width="10" '
            f'stroke-linecap="round" marker-end="url(#tip)"/>'
            f'<path d="M{CX + R_SHELL + 40},{y} H{xs_out - 150}" stroke="{CYAN_SOFT}" stroke-width="10" '
            f'stroke-linecap="round" marker-end="url(#tip)"/>')
    glow = (f'<path d="M{xs_in + 110},{y} H{xs_out - 150}" stroke="{CYAN}" stroke-width="30" opacity="0.25" '
            f'filter="url(#glow)"/>')
    intent = (f'<circle cx="{xs_in}" cy="{y}" r="112" fill="{BLUE}" opacity="0.25" filter="url(#glow)"/>'
              f'<circle cx="{xs_in}" cy="{y}" r="94" fill="url(#card)" stroke="{BLUE}" stroke-width="6"/>'
              + icon("actor", xs_in, y, 46, BLUE)
              + label(xs_in, y + 170, "INTENT", 38, INK))
    stack = []
    for i, dy in enumerate((-70, 0, 70)):
        stack.append(f'<g transform="translate({xs_out},{y + dy})">'
                     f'<ellipse cx="0" cy="-26" rx="92" ry="22" fill="#2A1735" stroke="{PLUM}" stroke-width="5"/>'
                     f'<path d="M-92,-26 V26 A92,22 0 0 0 92,26 V-26" fill="#1E1028" stroke="{PLUM}" stroke-width="5"/>'
                     f'<path d="M-92,0 A92,22 0 0 0 92,0" fill="none" stroke="{PLUM}" stroke-width="3" opacity="0.6"/></g>')
    systems = (f'<ellipse cx="{xs_out}" cy="{y}" rx="190" ry="190" fill="{PLUM}" opacity="0.18" filter="url(#bigglow)"/>'
               + "".join(reversed(stack))
               + label(xs_out, y + 190, "SYSTEMS OF RECORD", 36, INK))
    # Evidence loop: dotted, from the systems of record back to evaluation and release.
    ex, ey = CX, CY + R_PLATFORM
    evidence = (f'<path d="M{xs_out},{y + 235} C{xs_out},{y + 560} {ex + 520},{ey + 210} {ex + 108},{ey + 22}" '
                f'fill="none" stroke="{AMBER}" stroke-width="8" stroke-dasharray="2 22" stroke-linecap="round" '
                f'marker-end="url(#tip-amber)"/>')
    gap_in = (xs_in + 94 + CX - R_PLATFORM - 82) / 2      # between intent and admission
    gap_out = (CX + R_PLATFORM + 82 + xs_out - 92) / 2     # between gateway and the records
    tags = (label(gap_in, y - 40, "REQUEST", 28, CYAN_SOFT)
            + label(gap_out, y - 92, "VERIFIED", 26, CYAN_SOFT)
            + label(gap_out, y - 58, "EFFECT", 26, CYAN_SOFT)
            + label(2060, CY + 690, "EVIDENCE", 30, AMBER))
    return glow + beam + intent + systems + evidence + tags


def compose() -> str:
    controls = (badge(CX - R_PLATFORM, CY, "human", BLUE, "ADMISSION", -128)
                + badge(CX, CY - R_PLATFORM, "control", AMBER, "POLICY", -128)
                + badge(CX + R_PLATFORM, CY, "service", BLUE, "GATEWAY", -128)
                + badge(CX, CY + R_PLATFORM, "graph", AMBER, "EVALUATE · RELEASE", 150))
    body = background() + platform() + knowledge() + flows() + shell_and_core() + controls
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}{body}</svg>')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--svg", action="store_true", help="also keep the SVG next to the PNG")
    args = ap.parse_args()
    out = args.root.resolve() / "assets" / "cover" / "cover-art.png"
    svg = compose()
    if args.svg:
        out.with_suffix(".svg").write_text(svg, encoding="utf-8")
    rasterize(svg, out)
    print(json.dumps({"cover_art": str(out.relative_to(args.root.resolve())), "sha256": sha256(out),
                      "width": W, "height": H}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
