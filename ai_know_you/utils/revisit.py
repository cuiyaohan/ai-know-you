"""Revisit mechanism -- the profile is alive, not a one-shot questionnaire.

Instead of asking everything once, ai-know-you can be scheduled to re-check in
every N days, or to trigger an incremental update when a new signal is observed
(e.g. the user mentions a changed goal). This module decides *whether* a revisit
is due and records the cadence.
"""

from __future__ import annotations

import datetime as _dt
import os


DEFAULT_INTERVAL_DAYS = 30


def last_touch_path(base_dir: str) -> str:
    return os.path.join(base_dir, "ai-know-you", ".last_revisit")


def mark_revisit(base_dir: str) -> None:
    directory = os.path.join(base_dir, "ai-know-you")
    os.makedirs(directory, exist_ok=True)
    with open(last_touch_path(base_dir), "w", encoding="utf-8") as fh:
        fh.write(_dt.datetime.now().isoformat(timespec="seconds"))


def days_since_revisit(base_dir: str) -> float | None:
    path = last_touch_path(base_dir)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        stamp = fh.read().strip()
    try:
        last = _dt.datetime.fromisoformat(stamp)
    except ValueError:
        return None
    return (_dt.datetime.now() - last).total_seconds() / 86400.0


def is_revisit_due(base_dir: str, interval_days: int = DEFAULT_INTERVAL_DAYS) -> bool:
    since = days_since_revisit(base_dir)
    if since is None:
        return False
    return since >= interval_days
