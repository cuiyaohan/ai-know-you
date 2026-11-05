"""Stage 2 -- Dig deeper (follow-ups that drill into Stage 1)."""

from __future__ import annotations

from ..profile.models import Profile
from .session import Session


def run(s: Session, p: Profile) -> None:
    s.note("\n[bold cyan]Stage 2 / 5[/bold cyan]  [b]Dig deeper[/b]\n")

    goal = p.facts.get("primary_goal", "your goal")
    s.note(f"Let's drill into: [i]{goal}[/i]")

    success = s.text("What would 'done well' look like in about 3 months?")
    p.facts["success_in_3m"] = success

    blocker = s.text("What usually gets in the way -- time, focus, skills, or something else?")
    p.facts["typical_blocker"] = blocker

    frustration = s.text("A recurring frustration you'd love an assistant to stop causing?")
    if frustration:
        p.preferences["avoids"] = frustration

    if p.facts.get("session_depth") == "deep":
        rhythm = s.text("Describe a normal working day -- when are you sharp, when are you fried?")
        p.preferences["daily_rhythm"] = rhythm

        style = s.choice(
            "When you receive help, which feels best?",
            ["blunt-and-fast", "reasoned", "options-to-pick", "a-chat"],
            default="blunt-and-fast",
        )
        p.preferences["communication_style"] = {
            "blunt-and-fast": "direct and concise",
            "reasoned": "thorough with reasoning",
            "options-to-pick": "structured with options",
            "a-chat": "warm and conversational",
        }[style]

    # Contradiction probe (lightweight): early vs night owl.
    early = p.preferences.get("daily_rhythm", "").lower()
    if ("early" in early and "night" in early) or ("morning" in early and "late" in early):
        s.note("[yellow]Note:[/yellow] your rhythm description mentions both early and late -- "
               "I'll treat your real常态 as the one you confirm in Stage 4.")
