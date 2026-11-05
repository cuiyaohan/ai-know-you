"""Optional, non-diagnostic self-assessment modules (Stage 3).

IMPORTANT: these are communication-style calibrators, NOT psychological or
medical instruments. Results are used only to tune *how* the agent talks to the
user. No result is ever written as a fixed personality label.

Each module exposes:
    key        -- stable id used in the profile
    title      -- human label
    questions  -- list of (prompt, options) where options map to a trait
    score(answers) -> dict of trait -> value
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple


@dataclass
class Quiz:
    key: str
    title: str
    disclaimer: str
    questions: List[Tuple[str, List[str]]] = field(default_factory=list)
    scorer: Callable[[List[int]], Dict[str, str]] = lambda _: {}


COMMUNICATION = Quiz(
    key="communication_style",
    title="How do you like to be talked to?",
    disclaimer="Not a personality test. Used only to calibrate tone.",
    questions=[
        ("When you ask for help, you usually want...",
         ["A direct answer, fast", "The reasoning behind it", "Options to choose from", "A conversation about it"]),
        ("Feedback lands best when it is...",
         ["Blunt and specific", "Gentle and encouraging", "In writing, structured", "Casual and brief"]),
        ("Your ideal explanation is...",
         ["One sentence", "A short list", "A diagram", "A story"]),
    ],
    scorer=lambda a: {
        "communication_style": (
            "direct and concise" if a.count(0) >= 2
            else "thorough with reasoning" if a.count(1) >= 2
            else "warm and conversational" if a.count(3) >= 2
            else "structured and written"
        )
    },
)

DECISION = Quiz(
    key="decision_style",
    title="How do you make decisions?",
    disclaimer="Not a psychology instrument. Calibrates how options are framed.",
    questions=[
        ("Faced with a choice, you first...",
         ["Eliminate bad options", "Compare the best ones", "Trust your gut", "Ask someone you trust"]),
        ("You feel best after a decision when...",
         ["It is reversible", "It is the optimal one", "It felt right", "Others approved"]),
    ],
    scorer=lambda a: {
        "decision_style": (
            "risk-aware / reversible-first" if a.count(0) >= 1
            else "optimizing" if a.count(1) >= 1
            else "intuitive" if a.count(2) >= 1
            else "consultative"
        )
    },
)

ALL_QUIZZES: List[Quiz] = [COMMUNICATION, DECISION]


def get_quiz(key: str) -> Quiz | None:
    for q in ALL_QUIZZES:
        if q.key == key:
            return q
    return None
