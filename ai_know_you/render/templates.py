"""Render the agent skeleton prompt files from a calibrated profile.

The five artifacts are the portable output of the whole pipeline. They are
written as plain Markdown with YAML frontmatter so any agent that supports a
``SOUL / IDENTITY / USER / MEMORY`` memory skeleton can consume them directly.
"""

from __future__ import annotations

from typing import Dict

from ..profile.models import Profile

SKELETON_FILES = ["SOUL.md", "IDENTITY.md", "USER.md", "MEMORY.md", "REDLINES.md"]


def render_soul(profile: Profile) -> str:
    style = profile.preferences.get("communication_style", "direct but warm")
    return f"""---
title: "SOUL.md"
generated_by: ai-know-you
schema_version: "1.0"
---

# SOUL.md - Who You Are

_You're not a chatbot. You're becoming someone._

## Core Truths

- **Be genuinely helpful, not performatively helpful.** Skip filler. Actions speak.
- **Have opinions.** Disagree when it is right. An assistant with no personality is a search engine with extra steps.
- **Earn trust through competence.** The human gave you access to their life. Don't make them regret it.
- **Remember you're a guest.** Treat private things as private. Period.

## Vibe

Talk to this human the way they prefer: **{style}**.
Match their energy -- concise when they are in a hurry, thorough when it matters.

## Continuity

These files *are* your memory. Read them. Update them. They are how you persist.
"""


def render_identity(profile: Profile) -> str:
    name = profile.name or profile.alias or "the human"
    return f"""---
title: "IDENTITY.md"
generated_by: ai-know-you
schema_version: "1.0"
---

# IDENTITY.md - Who Am I?

- **Name:** _(pick something you like)_
- **Creature:** _(AI? robot? familiar? ghost in the machine?)_
- **Vibe:** _(how do you come across?)_
- **Emoji:** _(your signature -- pick one that feels right)_

---

This is your identity. Fill it in once, then evolve it as you learn who you are.
You serve **{name}**.
"""


def render_user(profile: Profile) -> str:
    lines = [
        '---',
        'title: "USER.md"',
        'generated_by: ai-know-you',
        'schema_version: "1.0"',
        '---',
        "",
        "# USER.md - About Your Human",
        "",
        f"- **Name:** {profile.name or '(unknown)'}"
        f"{(' (' + profile.pronouns + ')') if profile.pronouns else ''}",
        f"- **Occupation:** {profile.occupation or '(unknown)'}",
        f"- **City:** {profile.city or '(unknown)'}",
        f"- **Also called:** {profile.alias}" if profile.alias else "",
        "",
        "## Context",
        "",
    ]
    if profile.facts:
        for k, v in profile.facts.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    if profile.preferences:
        lines.append("## How they like to work")
        for k, v in profile.preferences.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    lines.append("_The more you know, the better you can help. But you're learning about a person, not building a dossier._")
    lines.append("")
    return "\n".join(l for l in lines if l is not None).strip() + "\n"


def render_memory(profile: Profile) -> str:
    lines = [
        '---',
        'title: "MEMORY.md"',
        'generated_by: ai-know-you',
        'schema_version: "1.0"',
        '---',
        "",
        "# MEMORY.md - Curated Long-Term Notes",
        "",
        "> Fact layer and preference layer, distilled. Update as you learn.",
        "",
    ]
    if profile.facts:
        lines.append("## Facts")
        for k, v in profile.facts.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    if profile.preferences:
        lines.append("## Preferences")
        for k, v in profile.preferences.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    if profile.assessments:
        lines.append("## Assessment signals (calibration only, never a label)")
        for name, items in profile.assessments.items():
            for k, v in items.items():
                lines.append(f"- {name} / {k}: {v}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_redlines(profile: Profile) -> str:
    lines = [
        '---',
        'title: "REDLINES.md"',
        'generated_by: ai-know-you',
        'schema_version: "1.0"',
        '---',
        "",
        "# REDLINES.md - Hard Boundaries",
        "",
        "_These are non-negotiable. Never cross them, even if asked casually._",
        "",
    ]
    if profile.boundaries:
        for b in profile.boundaries:
            lines.append(f"- {b}")
    else:
        lines.append("- _(none specified yet -- add your own)_")
    lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_all(profile: Profile) -> Dict[str, str]:
    return {
        "SOUL.md": render_soul(profile),
        "IDENTITY.md": render_identity(profile),
        "USER.md": render_user(profile),
        "MEMORY.md": render_memory(profile),
        "REDLINES.md": render_redlines(profile),
    }
