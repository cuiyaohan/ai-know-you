"""Stage 3 -- Optional, non-diagnostic self-calibration quizzes."""

from __future__ import annotations

from ..assess.quizzes import ALL_QUIZZES, Quiz
from ..profile.models import Profile
from .session import Session


def _run_quiz(s: Session, quiz: Quiz) -> None:
    s.note(f"\n[dim]{quiz.title}[/dim]  [italic]{quiz.disclaimer}[/italic]")
    answers: list[int] = []
    for i, (prompt, options) in enumerate(quiz.questions, 1):
        s.note(f"  [b]{i}.[/b] {prompt}")
        for j, opt in enumerate(options):
            s.note(f"     [cyan]{j+1}.[/cyan] {opt}")
        pick = s.choice("     your pick", [str(n) for n in range(1, len(options) + 1)], default="1")
        answers.append(int(pick) - 1)
    result = quiz.scorer(answers)
    quiz_title = quiz.title.split("?")[0]
    p_key = quiz.key
    p_sub = quiz_title
    profile = s._profile  # type: ignore[attr-defined]
    profile.assessments.setdefault(p_key, {})[p_sub] = "; ".join(f"{k}={v}" for k, v in result.items())
    for trait, value in result.items():
        profile.preferences.setdefault(trait, value)
    s.note(f"  [green]ok[/green] recorded: {', '.join(f'{k}={v}' for k, v in result.items())}")


def run(s: Session, p: Profile) -> None:
    # Attach profile so quiz runner can write into it. Kept on the session to
    # avoid threading the profile through every helper.
    s._profile = p  # type: ignore[attr-defined]
    s.note("\n[bold cyan]Stage 3 / 5[/bold cyan]  [b]Optional calibration[/b]\n")
    s.note("Skip anytime. These are communication-style calibrators, never a diagnosis.")
    if not s.confirm("Run a quick calibration quiz?", default=False):
        s.note("[dim]Skipped. You can run it later with `ai-know-you run --assess`.[/dim]")
        return
    for quiz in ALL_QUIZZES:
        _run_quiz(s, quiz)
