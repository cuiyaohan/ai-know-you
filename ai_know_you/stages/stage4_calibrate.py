"""Stage 4 -- Calibration (the differentiator).

The agent states, in plain language, what it understood about the user. The
user must confirm or correct before anything is written. This prevents the
"AI hallucinated that it knows you" failure mode.
"""

from __future__ import annotations

from ..profile.models import Profile
from .session import Session

MAX_ATTEMPTS = 3


def _compose(profile: Profile) -> str:
    who = profile.name or profile.alias or "You"
    lines = [
        f"Here is what I understood about {who}:",
        "",
        f"- You work as: {profile.occupation or 'unspecified'}.",
    ]
    if profile.city:
        lines.append(f"- Based in: {profile.city}.")
    if profile.facts.get("primary_goal"):
        lines.append(f"- Right now your top priority is: {profile.facts['primary_goal']}.")
    if profile.facts.get("agent_use_case"):
        lines.append(f"- You'll mainly use me for: {profile.facts['agent_use_case']}.")
    if profile.facts.get("success_in_3m"):
        lines.append(f"- 'Done well' looks like: {profile.facts['success_in_3m']}.")
    if profile.facts.get("typical_blocker"):
        lines.append(f"- What usually blocks you: {profile.facts['typical_blocker']}.")
    if profile.preferences:
        styled = profile.preferences.get("communication_style")
        if styled:
            lines.append(f"- Talk to you: {styled}.")
    if profile.boundaries:
        lines.append("- I will never: " + "; ".join(profile.boundaries) + ".")
    lines.append("")
    lines.append("If anything is off, tell me and I'll fix it before saving.")
    return "\n".join(lines)


def run(s: Session, p: Profile) -> None:
    s.note("\n[bold cyan]Stage 4 / 5[/bold cyan]  [b]Calibrate[/b]\n")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        understanding = _compose(p)
        s.note("[bold]My understanding of you:[/bold]")
        s.note(understanding)
        p.agent_understanding = understanding
        ok = s.confirm("Does this look right?", default=True)
        if ok:
            p.calibrated = True
            s.note("[green]Calibrated.[/green] Saving only after your go-ahead.")
            return
        correction = s.text("What should I change? (type the correction)")
        if correction:
            p.notes.setdefault("corrections", "")
            p.notes["corrections"] += f" [{attempt}] {correction}"
    p.calibrated = True
    s.note("[yellow]Used all correction rounds; proceeding with last version.[/yellow]")
