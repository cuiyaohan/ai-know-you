# Contributing to ai-know-you

Thanks for wanting to help! This project lives or dies by its community, so every
PR — translation, bug fix, or new assessment plugin — is welcome.

## Getting started

```bash
git clone https://github.com/cuiyaohan/ai-know-you
cd ai-know-you
pip install -e .
ai-know-you doctor
```

## How to contribute

1. Fork and create a branch from `main`.
2. Keep changes focused. One logical change per PR.
3. Run `ai-know-you doctor` and `ai-know-you sample` before pushing.
4. Open a PR with a clear description of the *why*.

## Code style

- Python 3.9+ compatible (no 3.10-only syntax in core paths).
- `ruff` clean is appreciated; `black` formatting is fine.
- No emoji as functional icons (project rule).
- Keep files under ~300 lines; split when they grow.

## Adding an assessment (Stage 3)

Assessments are **non-diagnostic calibrators**, never psychological instruments.
To add one, append a `Quiz` to `ai_know_you/assess/quizzes.py`:

```python
NEW = Quiz(
    key="my_calibrator",
    title="...?",
    disclaimer="Not a diagnosis. Calibrates tone only.",
    questions=[("prompt", ["opt1", "opt2"])],
    scorer=lambda a: {"trait": "value"},
)
```

Then register it in `ALL_QUIZZES`.

## Translating the README

This README ships in multiple languages. To add or fix one:

- Edit `README.<lang>.md` (see the language table in any README).
- Keep structure identical to `README.md`.
- Link the new file in every language's navigation block.

## Conduct

Be excellent to each other. Assume good faith. Disagree on ideas, not people.
