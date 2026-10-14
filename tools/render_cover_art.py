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


def note(x: float, y: float, text: str, size: int = 25, color: str = INK_SOFT) -> str:
    """A muted, lower-case detail line under a label."""
    return t(x, y, text, size, color, anchor="middle", spacing=1.5, opacity=0.78)


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
{checkpoints()}
{release_arc()}
{label(CX, CY - R_PLATFORM + 150, "DURABLE · GOVERNED WORKFLOW", 30, CYAN_SOFT)}"""


def checkpoints() -> str:
    """Durable checkpoints on the workflow ring: where a run can resume."""
    out = []
    for deg in (32, 58, 122, 148, 212, 238, 302, 328):
        a = math.radians(deg)
        x, y = CX + R_PLATFORM * math.cos(a), CY + R_PLATFORM * math.sin(a)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="{TEAL}" opacity="0.35" filter="url(#soft)"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#062A33" stroke="{TEAL}" stroke-width="4"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#B9FFF6"/>')
    return "".join(out)


def release_arc() -> str:
    """A reviewed release flows from evaluation back up into the platform's policy."""
    r = 468
    a0, a1 = math.radians(103), math.radians(226)
    x0, y0 = CX + r * math.cos(a0), CY + r * math.sin(a0)
    x1, y1 = CX + r * math.cos(a1), CY + r * math.sin(a1)
    bx, by = CX - 58, CY + R_PLATFORM - 58          # leaves the evaluate-and-release badge
    return (f'<path d="M{bx},{by} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" '
            f'stroke="{AMBER}" stroke-width="7" stroke-dasharray="2 18" stroke-linecap="round" '
            f'marker-end="url(#tip-amber)"/>')


def knowledge() -> str:
    """Middle ring: governed, pinned knowledge and context."""
    # Four kinds of governed knowledge, each a released, pinned artifact:
    # documents, the knowledge graph, enforceable rules, and governed memory.
    nodes = []
    for deg, kind in ((205, "record"), (240, "graph"), (300, "control"), (335, "store")):
        a = math.radians(deg)
        x, y = CX + R_KNOW * math.cos(a), CY + R_KNOW * math.sin(a)
        nodes.append(f'<rect x="{x - 32:.1f}" y="{y - 32:.1f}" width="64" height="64" rx="12" fill="#0A2A44" '
                     f'stroke="{CYAN}" stroke-width="3"/>' + icon(kind, x, y, 21, CYAN_SOFT))
    return f"""
<circle cx="{CX}" cy="{CY}" r="{R_KNOW}" fill="#0B2E55" fill-opacity="0.55" stroke="{CYAN}" stroke-width="4" stroke-dasharray="26 14"/>
<circle cx="{CX}" cy="{CY}" r="{R_KNOW}" fill="none" stroke="{CYAN}" stroke-width="12" opacity="0.25" filter="url(#glow)"/>
{''.join(nodes)}
{label(CX, CY + 292, "GOVERNED KNOWLEDGE", 28, CYAN_SOFT)}
{note(CX, CY + 330, "documents · graph · rules · memory", 24, CYAN_SOFT)}"""


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
{label(CX, CY + 162, "MODEL PROPOSES", 26, INK)}
{label(CX - R_SHELL - 92, CY - 44, "VALIDATE", 22, AMBER)}
{label(CX + R_SHELL + 98, CY - 44, "AUTHORIZE", 22, AMBER)}"""


def badge(x: float, y: float, kind: str, color: str, text: str, detail: str, below: bool = False) -> str:
    """One platform control on the outer ring: a lit disc with a role glyph,
    its name, and a muted line naming what it checks."""
    ly, ny = (y + 150, y + 192) if below else (y - 166, y - 124)
    return (f'<circle cx="{x}" cy="{y}" r="104" fill="{color}" opacity="0.30" filter="url(#glow)"/>'
            f'<circle cx="{x}" cy="{y}" r="82" fill="url(#card)" stroke="{color}" stroke-width="6"/>'
            + icon(kind, x, y, 40, color)
            + label(x, ly, text, 36, INK) + note(x, ny, detail))


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
              + label(xs_in, y + 170, "INTENT", 38, INK) + note(xs_in, y + 210, "users · APIs · events"))
    stack = []
    for i, dy in enumerate((-70, 0, 70)):
        stack.append(f'<g transform="translate({xs_out},{y + dy})">'
                     f'<ellipse cx="0" cy="-26" rx="92" ry="22" fill="#2A1735" stroke="{PLUM}" stroke-width="5"/>'
                     f'<path d="M-92,-26 V26 A92,22 0 0 0 92,26 V-26" fill="#1E1028" stroke="{PLUM}" stroke-width="5"/>'
                     f'<path d="M-92,0 A92,22 0 0 0 92,0" fill="none" stroke="{PLUM}" stroke-width="3" opacity="0.6"/></g>')
    systems = (f'<ellipse cx="{xs_out}" cy="{y}" rx="190" ry="190" fill="{PLUM}" opacity="0.18" filter="url(#bigglow)"/>'
               + "".join(reversed(stack))
               + label(xs_out, y + 190, "SYSTEMS OF RECORD", 36, INK)
               + note(xs_out, y + 230, "records · SaaS · partners"))
    # The receipt comes back from the system of record: proof of what happened.
    receipt = (f'<path d="M{xs_out - 100},{y + 40} H{CX + R_PLATFORM + 95}" stroke="{CYAN}" stroke-width="5" '
               f'stroke-dasharray="2 14" stroke-linecap="round" marker-end="url(#tip)"/>'
               + note((CX + R_PLATFORM + xs_out) / 2 + 10, y + 82, "receipt", 24, CYAN_SOFT))
    # Evidence loop: dotted, from the systems of record back to evaluation and release.
    ex, ey = CX, CY + R_PLATFORM
    evidence = (f'<path d="M{xs_out},{y + 262} C{xs_out},{y + 560} {ex + 520},{ey + 210} {ex + 108},{ey + 22}" '
                f'fill="none" stroke="{AMBER}" stroke-width="8" stroke-dasharray="2 22" stroke-linecap="round" '
                f'marker-end="url(#tip-amber)"/>')
    gap_in = (xs_in + 94 + CX - R_PLATFORM - 82) / 2      # between intent and admission
    tags = (label(gap_in, y - 40, "REQUEST", 28, CYAN_SOFT)
            + label(2060, CY + 690, "EVIDENCE", 30, AMBER))
    return glow + beam + intent + systems + receipt + evidence + tags


def approval() -> str:
    """Proposal-bound human approval, consulted by the gateway for protected effects."""
    gx, gy = CX + R_PLATFORM, CY
    ax, ay = gx + 305, gy - 262
    return (f'<path d="M{ax - 40},{ay + 40} L{gx + 72},{gy - 42}" stroke="{AMBER}" stroke-width="4" '
            f'stroke-dasharray="12 10" opacity="0.9"/>'
            f'<circle cx="{ax}" cy="{ay}" r="70" fill="{AMBER}" opacity="0.25" filter="url(#glow)"/>'
            f'<circle cx="{ax}" cy="{ay}" r="56" fill="url(#card)" stroke="{AMBER}" stroke-width="5"/>'
            + icon("human", ax, ay, 28, AMBER)
            + label(ax + 82, ay - 6, "HUMAN", 26, INK, anchor="start")
            + label(ax + 82, ay + 28, "APPROVAL", 26, INK, anchor="start"))


def key() -> str:
    """A compact key beside the author block."""
    x0, y0 = 1460, 2742
    rows = [
        (f'<path d="M{x0 + 40},{y0 + 62} h70" stroke="{CYAN_SOFT}" stroke-width="8" stroke-linecap="round"/>',
         "request and verified effect"),
        (f'<path d="M{x0 + 40},{y0 + 122} h70" stroke="{AMBER}" stroke-width="7" stroke-dasharray="2 14" '
         f'stroke-linecap="round"/>', "evidence and release"),
    ]
    rows2 = [
        (f'<polygon points="{x0 + 520},{y0 + 44} {x0 + 538},{y0 + 62} {x0 + 520},{y0 + 80} {x0 + 502},{y0 + 62}" '
         f'fill="#2B1F08" stroke="{AMBER}" stroke-width="4"/>', "deterministic gate"),
        (f'<circle cx="{x0 + 520}" cy="{y0 + 122}" r="11" fill="#062A33" stroke="{TEAL}" stroke-width="4"/>',
         "durable checkpoint"),
    ]
    out = [f'<rect x="{x0}" y="{y0}" width="935" height="178" rx="26" fill="#05193A" fill-opacity="0.82" '
           f'stroke="{CYAN}" stroke-opacity="0.45" stroke-width="3"/>']
    for i, (glyph, text) in enumerate(rows):
        out.append(glyph + t(x0 + 135, y0 + 72 + i * 60, text, 28, INK_SOFT))
    for i, (glyph, text) in enumerate(rows2):
        out.append(glyph + t(x0 + 560, y0 + 72 + i * 60, text, 28, INK_SOFT))
    return "".join(out)


def compose() -> str:
    controls = (badge(CX - R_PLATFORM, CY, "human", BLUE, "ADMISSION", "identity · risk · budgets")
                + badge(CX, CY - R_PLATFORM, "control", AMBER, "POLICY", "decide · enforce · audit")
                + badge(CX + R_PLATFORM, CY, "service", BLUE, "GATEWAY", "tools · MCP · A2A")
                + badge(CX, CY + R_PLATFORM, "graph", AMBER, "EVALUATE · RELEASE",
                        "evals · canary · rollback", below=True))
    body = (background() + platform() + knowledge() + flows() + shell_and_core() + controls
            + approval() + key())
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
