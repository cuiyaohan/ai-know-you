"""Session: the I/O contract shared by every stage.

A Session wraps a ``rich`` console and an optional pre-seeded answer queue. When
the queue is present (sample / non-interactive mode) every prompt is answered
from it; otherwise the user is prompted interactively. This keeps the same
stage code path usable for real runs, demos, and CI smoke tests.
"""

from __future__ import annotations

from typing import List, Optional

from rich.console import Console
from rich.prompt import Confirm, Prompt


class Session:
    def __init__(
        self,
        console: Console,
        answers: Optional[List[str]] = None,
        interactive: bool = True,
    ) -> None:
        self.console = console
        self._answers = list(answers) if answers else None
        self.interactive = interactive and self._answers is None
        self._idx = 0

    def _next(self) -> Optional[str]:
        if self._answers is None:
            return None
        if self._idx >= len(self._answers):
            return ""
        val = self._answers[self._idx]
        self._idx += 1
        return val

    def text(self, prompt: str, default: str = "") -> str:
        canned = self._next()
        if canned is not None:
            self.console.print(f"[dim]{prompt}[/dim] [cyan]{canned}[/cyan]")
            return canned or default
        val = Prompt.ask(prompt, default=default, console=self.console)
        return val

    def choice(self, prompt: str, choices: List[str], default: Optional[str] = None) -> str:
        canned = self._next()
        if canned is not None:
            picked = canned if canned in choices else (default or choices[0])
            self.console.print(f"[dim]{prompt}[/dim] [cyan]{picked}[/cyan]")
            return picked
        val = Prompt.ask(
            prompt, choices=[c.lower() for c in choices], default=(default or choices[0]),
            console=self.console,
        )
        return val

    def confirm(self, prompt: str, default: bool = False) -> bool:
        canned = self._next()
        if canned is not None:
            val = canned.strip().lower() in ("y", "yes", "true", "1", "ok")
            self.console.print(f"[dim]{prompt}[/dim] [cyan]{val}[/cyan]")
            return val
        return Confirm.ask(prompt, default=default, console=self.console)

    def note(self, text: str) -> None:
        self.console.print(text)
