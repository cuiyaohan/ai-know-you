"""ai-know-you command-line interface.

Subcommands
-----------
run     interactive five-stage onboarding wizard
sample  non-interactive demo that writes a sample profile (great for CI/docs)
show    print the stored profile for a directory
doctor  environment self-check
"""

from __future__ import annotations

import os
import sys

import click
from rich.console import Console

import ai_know_you
from ai_know_you.profile import store
from ai_know_you.profile.models import Profile
from ai_know_you.stages import Session
from ai_know_you.stages import stage1_intro, stage2_dig, stage3_assess, stage4_calibrate, stage5_assemble
from ai_know_you.utils import revisit

console = Console()


BANNER = r"""
 [bold cyan]  _    _  __          _    _                  _  [/bold cyan]
 [bold cyan] | |  (_)/ _|        | |  | |                | | [/bold cyan]
 [bold cyan] | | ___| |_ __ _ ___| | _| | __ _ _ __ ___  | | [/bold cyan]
 [bold cyan] | |/ / |  _/ _` / __| |/ / |/ _` | '__/ _ \ | | [/bold cyan]
 [bold cyan] |   <| | || (_| \__ \   <| | (_| | | |  __/ | | [/bold cyan]
 [bold cyan] |_|\_\_|_| \__,_|___/_|\_\_|\__,_|_|  \___| |_| [/bold cyan]
            [dim]Agent-era onboarding wizard[/dim]
"""


def _default_dir() -> str:
    return os.getcwd()


def _run_pipeline(base_dir: str, session: Session, with_assess: bool) -> Profile:
    p = Profile()
    stage1_intro.run(session, p)
    stage2_dig.run(session, p)
    if with_assess:
        stage3_assess.run(session, p)
    stage4_calibrate.run(session, p)
    stage5_assemble.run(session, p, base_dir)
    revisit.mark_revisit(base_dir)
    return p


@click.group(invoke_without_command=True)
@click.version_option(version=ai_know_you.__version__, prog_name="ai-know-you")
@click.pass_context
def main(ctx: click.Context) -> None:
    """ai-know-you: make any agent truly know its user."""
    if ctx.invoked_subcommand is None:
        console.print(BANNER)
        console.print("Run [cyan]ai-know-you run[/cyan] to start the wizard, or "
                      "[cyan]--help[/cyan] for commands.\n")


@main.command()
@click.option("--dir", "base_dir", default=None, help="Output directory (default: current dir).")
@click.option("--depth", type=click.Choice(["fast", "deep"]), default="fast", help="Session depth.")
@click.option("--assess/--no-assess", default=False, help="Run optional calibration quiz.")
def run(base_dir: str | None, depth: str, assess: bool) -> None:
    """Interactive five-stage onboarding wizard."""
    base_dir = base_dir or _default_dir()
    console.print(BANNER)
    console.print(f"[bold]Target directory:[/bold] [cyan]{base_dir}[/cyan]\n")
    session = Session(console, interactive=True)
    # depth is captured inside stage 1; we surface it for clarity.
    session.note(f"[dim]Depth: {depth} | assessment: {'on' if assess else 'off'}[/dim]")
    _run_pipeline(base_dir, session, with_assess=assess)
    console.print("\n[bold green]Onboarding complete.[/bold green] Welcome to being known.")


@main.command()
@click.option("--dir", "base_dir", default="./demo-profile", help="Where to write the sample.")
def sample(base_dir: str) -> None:
    """Non-interactive demo run with built-in answers (CI / docs friendly)."""
    console.print(BANNER)
    answers = [
        "Cui", "Cui", "", "indie developer / content creator", "Shenzhen",
        "ship ai-know-you to 100k GitHub stars", "coding", "deep",
        "publish v1 and land the first 1000 stars", "fragmented time",
        "assistants that reply too verbosely", "sharp in the morning, fried after 10pm",
        "blunt-and-fast",
        "y",                       # stage 3: run calibration quiz?
        "1", "1", "1",             # communication quiz picks
        "1", "2",                  # decision quiz picks
        "y",                       # stage 4: understanding looks right?
    ]
    session = Session(console, answers=answers, interactive=False)
    console.print(f"[bold]Sample run ->[/bold] [cyan]{base_dir}[/cyan]\n")
    _run_pipeline(base_dir, session, with_assess=True)
    console.print("\n[bold green]Sample profile written.[/bold green]")


@main.command()
@click.option("--dir", "base_dir", default=None, help="Profile directory (default: current dir).")
def show(base_dir: str | None) -> None:
    """Print the stored profile."""
    base_dir = base_dir or _default_dir()
    p = store.load_profile(base_dir)
    if p is None:
        console.print("[yellow]No profile found at[/yellow] " + store.profile_dir(base_dir))
        raise SystemExit(1)
    console.print(p.summarize())
    console.print(p.agent_understanding or "(no understanding captured)")


@main.command()
def doctor() -> None:
    """Self-check the environment."""
    ok = True
    checks = [
        ("Python >= 3.9", sys.version_info >= (3, 9)),
        ("rich importable", _import_ok("rich")),
        ("pyyaml importable", _import_ok("yaml")),
        (f"writable: {_default_dir()}", os.access(_default_dir(), os.W_OK)),
    ]
    for label, passed in checks:
        mark = "[green]ok[/green]" if passed else "[red]FAIL[/red]"
        console.print(f"  {mark}  {label}")
        ok = ok and passed
    console.print("\n[bold green]doctor: environment ready[/bold green]" if ok
                  else "\n[bold red]doctor: issues found[/bold red]")
    raise SystemExit(0 if ok else 1)


def _import_ok(mod: str) -> bool:
    try:
        __import__(mod)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    main()
