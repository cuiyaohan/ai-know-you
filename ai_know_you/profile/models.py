"""Layered user-profile data model.

The profile is split into three independent layers so each can evolve on its
own cadence instead of becoming one undifferentiated blob:

    facts       -- who you are / what you are doing (stable-ish)
    preferences -- how you like to work and communicate (slow-moving)
    boundaries  -- red lines, no-go zones, hard constraints (rarely changes)

Plus a free-form ``notes`` bucket for anything that does not fit a layer.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Profile:
    """The full user profile produced by the ai-know-you pipeline."""

    # --- Identity -------------------------------------------------------
    name: str = ""
    alias: str = ""               # what the agent should call them
    occupation: str = ""
    city: str = ""
    pronouns: str = ""

    # --- Layered content ------------------------------------------------
    facts: Dict[str, str] = field(default_factory=dict)
    preferences: Dict[str, str] = field(default_factory=dict)
    boundaries: List[str] = field(default_factory=list)
    notes: Dict[str, str] = field(default_factory=dict)

    # --- Assessment (optional, stage 3) --------------------------------
    assessments: Dict[str, Dict[str, str]] = field(default_factory=dict)

    # --- Meta -----------------------------------------------------------
    schema_version: str = "1.0"
    created_at: str = field(default_factory=lambda: _dt.datetime.now().isoformat(timespec="seconds"))
    updated_at: str = field(default_factory=lambda: _dt.datetime.now().isoformat(timespec="seconds"))
    revisits: int = 0

    # --- Calibration ----------------------------------------------------
    calibrated: bool = False
    agent_understanding: str = ""  # the "here is what I understood about you" text

    def touch(self) -> None:
        self.updated_at = _dt.datetime.now().isoformat(timespec="seconds")

    def is_empty(self) -> bool:
        return not (
            self.name
            or self.occupation
            or self.facts
            or self.preferences
            or self.boundaries
        )

    def summarize(self) -> str:
        """A one-paragraph human-readable summary used by stage 4 calibration."""
        lines: List[str] = []
        who = self.name or self.alias or "You"
        lines.append(f"{who} " + (f"({self.pronouns}) " if self.pronouns else ""))
        if self.occupation:
            lines.append(f"works as {self.occupation}")
        if self.city:
            lines.append(f"based in {self.city}")
        extra = []
        if self.facts:
            extra.append(f"{len(self.facts)} fact entries")
        if self.preferences:
            extra.append(f"{len(self.preferences)} preference entries")
        if self.boundaries:
            extra.append(f"{len(self.boundaries)} hard boundaries")
        if extra:
            lines.append("with " + ", ".join(extra) + " captured")
        return " ".join(lines).strip() + "."


def empty_profile() -> Profile:
    return Profile()
