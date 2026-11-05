"""Stage 1 -- First acquaintance (open questions)."""

from __future__ import annotations

from ..profile.models import Profile
from .session import Session


def run(s: Session, p: Profile) -> None:
    s.note("\n[bold cyan]Stage 1 / 5[/bold cyan]  [b]First acquaintance[/b]\n")
    s.note("A handful of open questions to give the rest of the flow a target. There are no wrong answers.")

    p.name = s.text("What should I call you? (your name)")
    p.alias = s.text("What would you like the agent to call you? (nickname, optional)", default=p.name)
    p.pronouns = s.text("Your pronouns (optional)", default="")
    p.occupation = s.text("What do you do? (role / profession)")
    p.city = s.text("City / timezone (optional)", default="")

    goal = s.text("What is the single most important thing you want to get done right now?")
    p.facts["primary_goal"] = goal

    use_case = s.text("What will you mostly use this agent for? (coding / writing / research / life / other)")
    p.facts["agent_use_case"] = use_case

    depth = s.choice("How deep should this session go?", ["fast", "deep"], default="fast")
    p.facts["session_depth"] = depth
    if depth == "deep":
        s.note("[dim]Deep mode -- Stage 2 will ask a couple of extra follow-ups.[/dim]")
