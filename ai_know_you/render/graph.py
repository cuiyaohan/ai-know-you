"""Render the user profile as a relationship map.

Produces both a self-contained SVG (no external dependencies, renders anywhere)
and a Graphviz DOT string. The map places a central "You" node and fans the
facts / preferences / boundaries layers out around it, colour-coded by layer.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

from ..profile.models import Profile

LAYER_COLORS = {"facts": "#4F46E5", "preferences": "#0EA5E9", "boundaries": "#EF4444"}
LAYER_LABELS = {"facts": "Facts", "preferences": "Preferences", "boundaries": "Boundaries"}


def _items(p: Profile) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for layer in ("facts", "preferences", "boundaries"):
        bucket = getattr(p, layer)
        if isinstance(bucket, dict):
            for k in bucket:
                out.append((layer, str(k)))
        else:
            for v in bucket:
                out.append((layer, str(v)))
    return out


def _layout(n: int) -> Tuple[int, int, int, int, List[Tuple[float, float]]]:
    w, h = 900, 540
    cx, cy = w // 2, h // 2
    r = 200
    pts: List[Tuple[float, float]] = []
    for i in range(max(n, 1)):
        ang = -math.pi / 2 + 2 * math.pi * i / max(n, 1)
        x = cx + r * math.cos(ang)
        y = cy + r * 0.78 * math.sin(ang)
        pts.append((x, y))
    return w, h, cx, cy, pts


def _short(s: str) -> str:
    s = str(s).replace('"', "'")
    return s[:22] + ("…" if len(s) > 22 else "")


def render_svg(p: Profile, path: str) -> str:
    items = _items(p)
    n = max(len(items), 1)
    w, h, cx, cy, pts = _layout(n)
    parts: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,Arial">',
        f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>',
    ]
    for x, y in pts:
        parts.append(
            f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#CBD5E1" stroke-width="1.5"/>'
        )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="#4F46E5"/>')
    parts.append(
        f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" fill="#FFFFFF" font-size="15" font-weight="600">You</text>'
    )
    for (layer, label), (x, y) in zip(items, pts):
        color = LAYER_COLORS[layer]
        tx = _short(label)
        bw = max(96, len(tx) * 7 + 20)
        parts.append(
            f'<rect x="{x - bw / 2:.1f}" y="{y - 16:.1f}" width="{bw:.1f}" height="32" rx="8" fill="{color}"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" fill="#FFFFFF" font-size="12">{tx}</text>'
        )
    lx, ly = 20, h - 70
    for layer, color in LAYER_COLORS.items():
        parts.append(f'<rect x="{lx}" y="{ly}" width="14" height="14" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{lx + 20}" y="{ly + 12}" fill="#334155" font-size="12">{LAYER_LABELS[layer]}</text>')
        ly += 22
    parts.append("</svg>")
    svg = "\n".join(parts)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    return path


def render_dot(p: Profile) -> str:
    items = _items(p)
    lines = [
        "digraph aky {",
        '  rankdir=LR; center [label="You", shape=doublecircle, fillcolor="#4F46E5", style=filled, fontcolor=white];',
    ]
    for i, (layer, label) in enumerate(items):
        color = LAYER_COLORS[layer]
        nid = f"n{i}"
        lines.append(f'  {nid} [label="{_short(label)}", fillcolor="{color}", style=filled, fontcolor=white];')
        lines.append(f"  center -> {nid};")
    lines.append("}")
    return "\n".join(lines) + "\n"
