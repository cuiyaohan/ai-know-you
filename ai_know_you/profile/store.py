"""Local-first persistence for the user profile.

Everything lives on disk as plain Markdown + YAML frontmatter so the artifact
is portable across agents and readable by humans. No cloud, no telemetry.
Sensitive fields are stripped before they ever reach this module (see
``ai_know_you.utils.privacy``).
"""

from __future__ import annotations

import os
from typing import Optional

import yaml

from .models import Profile

PROFILE_FILENAME = "profile.md"

# Frontmatter keys we persist. Order is cosmetic only.
_FRONTMATTER_KEYS = (
    "name",
    "alias",
    "occupation",
    "city",
    "pronouns",
    "schema_version",
    "created_at",
    "updated_at",
    "revisits",
    "calibrated",
)


def profile_dir(base_dir: str) -> str:
    return os.path.join(base_dir, "ai-know-you")


def profile_path(base_dir: str) -> str:
    return os.path.join(profile_dir(base_dir), PROFILE_FILENAME)


def save_profile(profile: Profile, base_dir: str) -> str:
    """Write the profile to ``<base_dir>/ai-know-you/profile.md``. Returns path."""
    import datetime as _dt

    profile.touch()
    directory = profile_dir(base_dir)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, PROFILE_FILENAME)

    front: dict = {}
    for key in _FRONTMATTER_KEYS:
        val = getattr(profile, key)
        if val in (None, "", 0, False):
            continue
        front[key] = val

    body = _render_body(profile)
    document = "---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False) + "---\n" + body
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(document)
    return path


def load_profile(base_dir: str) -> Optional[Profile]:
    path = profile_path(base_dir)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    if not raw.startswith("---"):
        return None
    _, fm, body = raw.split("---", 2)
    data = yaml.safe_load(fm) or {}
    profile = Profile()
    for key, value in data.items():
        if hasattr(profile, key):
            setattr(profile, key, value)
    _parse_body(profile, body)
    return profile


def _render_body(profile: Profile) -> str:
    out: list[str] = []
    if profile.agent_understanding:
        out.append("## Agent's Understanding\n")
        out.append(profile.agent_understanding.strip() + "\n")

    if profile.facts:
        out.append("## Facts\n")
        for k, v in profile.facts.items():
            out.append(f"- **{k}**: {v}")
        out.append("")

    if profile.preferences:
        out.append("## Preferences\n")
        for k, v in profile.preferences.items():
            out.append(f"- **{k}**: {v}")
        out.append("")

    if profile.boundaries:
        out.append("## Boundaries (red lines)\n")
        for b in profile.boundaries:
            out.append(f"- {b}")
        out.append("")

    if profile.assessments:
        out.append("## Assessments\n")
        for name, items in profile.assessments.items():
            out.append(f"### {name}\n")
            for k, v in items.items():
                out.append(f"- **{k}**: {v}")
            out.append("")

    if profile.notes:
        out.append("## Notes\n")
        for k, v in profile.notes.items():
            out.append(f"- **{k}**: {v}")
        out.append("")

    return "\n".join(out).strip() + "\n"


def _parse_body(profile: Profile, body: str) -> None:
    """Best-effort parse of the Markdown body back into the profile layers."""
    section = None
    buffer: list[str] = []
    lines = body.splitlines()
    for line in lines:
        if line.startswith("## "):
            section = line[3:].strip().lower()
            continue
        if section == "facts" and line.startswith("- **"):
            k, _, v = line[4:].partition("**: ")
            profile.facts[k] = v
        elif section == "preferences" and line.startswith("- **"):
            k, _, v = line[4:].partition("**: ")
            profile.preferences[k] = v
        elif section == "boundaries (red lines)" and line.startswith("- "):
            profile.boundaries.append(line[2:].strip())
        elif section == "agent's understanding":
            buffer.append(line)
    if buffer:
        profile.agent_understanding = "\n".join(buffer).strip()
