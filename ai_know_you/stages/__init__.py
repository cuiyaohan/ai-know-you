"""Stage package: the five-phase onboarding pipeline.

Phases
------
1. Intro      -- open questions to build a base picture
2. Dig        -- follow-ups that drill into the first answers
3. Assess     -- optional, non-diagnostic self-calibration quizzes
4. Calibrate  -- agent states what it understood; user confirms/corrects
5. Assemble   -- write the portable skeleton prompt files
"""

from .session import Session

__all__ = ["Session"]
