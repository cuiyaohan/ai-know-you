"""Export a calibrated profile to several portable, tool-friendly formats.

Each exporter is pure-Python and dependency-light so the core pipeline never
blocks on optional extras. The :func:`export_all` helper is what the CLI
``export`` command calls.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import yaml

from .profile.models import Profile

_FIELDS = [
    "name", "alias", "occupation", "city", "pronouns",
    "facts", "preferences", "boundaries", "notes",
    "assessments", "schema_version", "created_at", "updated_at",
    "revisits", "calibrated", "agent_understanding",
]


def to_dict(p: Profile) -> Dict[str, Any]:
    """Flatten a Profile into a plain, JSON/YAML-safe dict."""
    return {k: getattr(p, k) for k in _FIELDS}


def export_json(p: Profile, path: str) -> str:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(to_dict(p), fh, ensure_ascii=False, indent=2)
    return path


def export_yaml(p: Profile, path: str) -> str:
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(to_dict(p), fh, allow_unicode=True, sort_keys=False)
    return path


def export_obsidian(p: Profile, path: str) -> str:
    """Obsidian-flavoured Markdown using properties + callouts."""
    lines: List[str] = [
        "---",
        "tags: [ai-know-you, profile]",
        "---",
        "",
        "# User Profile · ai-know-you",
        "",
        "> [!abstract] Identity",
        "",
        f"- name:: {p.name or 'Unknown'}",
        f"- occupation:: {p.occupation or 'Unknown'}",
        f"- city:: {p.city or 'Unknown'}",
        "",
    ]
    if p.facts:
        lines += ["> [!note] Facts (事实层)"]
        for k, v in p.facts.items():
            lines.append(f"- {k}:: {v}")
        lines.append("")
    if p.preferences:
        lines += ["> [!tip] Preferences (偏好层)"]
        for k, v in p.preferences.items():
            lines.append(f"- {k}:: {v}")
        lines.append("")
    if p.boundaries:
        lines += ["> [!warning] Boundaries (边界层)"]
        for b in p.boundaries:
            lines.append(f"- {b}")
        lines.append("")
    if p.agent_understanding:
        lines += ["> [!quote] Agent's Understanding", "", p.agent_understanding.strip(), ""]
    text = "\n".join(lines).strip() + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def _dot_escape(s: str) -> str:
    return str(s).replace('"', "'")[:24]


def export_dot(p: Profile, path: str) -> str:
    """Graphviz DOT of the profile relationship graph."""
    lines = [
        "digraph aky_profile {",
        "  rankdir=LR;",
        "  node [shape=box, style=\"rounded,filled\", fontcolor=white];",
        "  center [label=\"You\", shape=doublecircle, fillcolor=\"#4F46E5\"];",
    ]
    idx = 0
    for layer, color in (("facts", "#4F46E5"), ("preferences", "#0EA5E9"), ("boundaries", "#EF4444")):
        bucket = getattr(p, layer)
        items = bucket.items() if isinstance(bucket, dict) else [(None, b) for b in bucket]
        for k, _v in items:
            nid = f"{layer}_{idx}"
            idx += 1
            lines.append(f'  {nid} [label="{_dot_escape(k or "item")}", fillcolor="{color}"];')
            lines.append(f"  center -> {nid};")
    lines.append("}")
    text = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def export_all(p: Profile, out_dir: str) -> List[str]:
    os.makedirs(out_dir, exist_ok=True)
    written: List[str] = []
    written.append(export_json(p, os.path.join(out_dir, "profile.json")))
    written.append(export_yaml(p, os.path.join(out_dir, "profile.yaml")))
    written.append(export_obsidian(p, os.path.join(out_dir, "profile.obsidian.md")))
    written.append(export_dot(p, os.path.join(out_dir, "profile.dot")))
    return written
