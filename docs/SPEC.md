# Spec - ai-know-you v0.1.0

> Status: confirmed (MVP) | Generated: 2026-11-05
> Scope: a local-first CLI wizard that turns "an agent knows nothing about you"
> into a portable, calibrated profile package.

## 1. Product definition

- **One-liner:** A standardized, re-runnable, portable onboarding pipeline that makes any AI agent truly know its user.
- **Target user:** Developers and power users who run AI agents and want them personalized without leaking private data.
- **Core problem:** Agents start from zero every session; "knowing the user" is ad-hoc and easily forgotten or hallucinated.

## 2. MVP scope (locked)

| Priority | Feature | Acceptance |
|----------|---------|------------|
| P0 | Stage 1 Intro (open questions) | Collects name/goal/use-case; writes to profile |
| P0 | Stage 2 Dig (follow-ups) | Deep mode drills into rhythm/style; surfaces contradictions |
| P0 | Stage 4 Calibrate | Agent states understanding; user confirms/corrects before save |
| P0 | Stage 5 Assemble | Writes SOUL/IDENTITY/USER/MEMORY/REDLINES + profile.md |
| P0 | Local-first storage | Markdown + YAML frontmatter under `<dir>/ai-know-you/` |
| P1 | Stage 3 Assess (optional) | Non-diagnostic comms/decision calibrators, opt-in |
| P1 | Privacy redaction | Sensitive categories detected and redacted pre-write |
| P1 | Revisit mechanism | `mark_revisit` + due-check; incremental updates later |

## 3. Out of scope (v1)

| Not doing | Reason |
|-----------|-------|
| Auto-install of agent skills | Needs per-agent auth; v2 |
| Web UI | CLI first; v2 |
| Cloud sync | Contradicts local-first principle by default |

## 4. Technical architecture (locked)

| Layer | Choice | Note |
|-------|--------|------|
| Language | Python >= 3.9 | Single binary via `pip install -e .` |
| CLI | click 8.1+ | Subcommands: run / sample / show / doctor |
| TUI | rich 13+ | Banners, prompts, structured output |
| Serialization | pyyaml 6+ | Frontmatter for profile.md |
| Storage | filesystem | `<dir>/ai-know-you/*.md` |

## 5. Data model

```
Profile
  identity: name, alias, occupation, city, pronouns
  facts:        dict   (stable-ish)
  preferences:  dict   (slow-moving)
  boundaries:   list   (red lines)
  notes:        dict   (free-form)
  assessments:  dict   (optional, stage 3)
  meta: schema_version, created_at, updated_at, revisits, calibrated
```

## 6. CLI surface

| Command | Args | Behavior |
|---------|------|----------|
| `run` | `--dir`, `--depth {fast,deep}`, `--assess/--no-assess` | Interactive 5-stage wizard |
| `sample` | `--dir` | Non-interactive demo with canned answers |
| `show` | `--dir` | Print stored profile summary + understanding |
| `doctor` | — | Environment self-check |

## 7. Output artifacts

`SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md`, `REDLINES.md`, `profile.md`
— all plain Markdown + YAML frontmatter, agent-agnostic.

## 8. Privacy rules

- Detect categories: credential, identity_doc, financial, health, precise_location.
- Redact before write; never persist raw sensitive values.
- No network calls, no telemetry, no accounts.

## 9. Verification

```bash
pip install -e .
ai-know-you doctor          # all checks ok
ai-know-you sample --dir ./demo-profile
ai-know-you show --dir ./demo-profile   # prints understanding
ls demo-profile/ai-know-you # 6 markdown files present
```
