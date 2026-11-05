<p align="center">
  <img src="assets/banner.svg" alt="ai-know-you" width="100%" />
</p>

<p align="center">
  <b>Agent-era onboarding wizard.</b><br/>
  A standardized, re-runnable, portable pipeline that makes <i>any</i> AI agent truly know its user.
</p>

<p align="center">
  <a href="https://github.com/cuiyaohan/ai-know-you/actions"><img src="https://img.shields.io/github/actions/workflow/status/cuiyaohan/ai-know-you/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <img src="https://img.shields.io/github/v/release/cuiyaohan/ai-know-you?label=release&color=4F46E5" alt="release" />
  <img src="https://img.shields.io/badge/license-MIT-0EA5E9" alt="license" />
  <img src="https://img.shields.io/badge/python-3.9%2B-4F46E5" alt="python" />
  <img src="https://img.shields.io/github/stars/cuiyaohan/ai-know-you?style=social" alt="stars" />
  <img src="https://img.shields.io/github/last-commit/cuiyaohan/ai-know-you?label=last%20commit" alt="last commit" />
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

---

## Description

`ai-know-you` is an open-source onboarding wizard that makes any Agent "fully understand you" from scratch — one conversation to a portable user profile and Agent skeleton prompts.

Licensed under the [MIT License](LICENSE). See [DESCRIPTION.md](DESCRIPTION.md) for the full bilingual description and license declaration.

## Why this exists

When you hand a fresh agent — Claude Code, Codex, WorkBuddy, or your own — it knows **nothing** about you. It learns you the slow way: one ambiguous chat at a time, and it forgets by next session.

`ai-know-you` turns "getting to know you" into a **single, repeatable, portable flow**. Run it once and you get a *profile package* — plain Markdown files with structured frontmatter — that any agent can load and that you fully own.

> The mental model: **`ai-know-you` is the `create-react-app` of agent onboarding.**

## Features

- **Five-stage pipeline.** Intro → Dig → optional Assessment → **Calibration** → Assembly. The Calibration stage is the differentiator: the agent shows you *"here is what I understood about you"* and waits for your approval or correction before anything is locked in — no hallucinated "I know you now."
- **Layered profile model.** Facts / Preferences / Boundaries evolve on independent cadences instead of collapsing into one undifferentiated blob.
- **Portable skeleton prompts.** Generates `SOUL` / `IDENTITY` / `USER` / `MEMORY` / `REDLINES` — drop them into any agent that supports a memory skeleton.
- **Multi-format export.** Emit `json`, `yaml`, Obsidian-flavoured Markdown, and Graphviz `dot` from a single profile.
- **Relationship graph.** Render the profile as a self-contained SVG (or DOT) to *see* how your facts, preferences and boundaries connect.
- **Zero-knowledge local vault.** Seal the whole profile directory with AES-256-CBC + PBKDF2-HMAC-SHA256 into a single `.akyv` file (optional `crypto` extra). Nothing leaves your machine.
- **Auditable skill recommender.** Derives a one-click skill install prompt from your profile with a transparent, explainable ruleset — every suggestion carries a reason.
- **Local-first & privacy-redacted.** Sensitive categories (credentials, IDs, health, precise location) are detected and redacted before they are ever written.
- **Revisit mechanism.** Re-run to incrementally update the profile; the pipeline is idempotent and merge-aware.

<p align="center">
  <img src="assets/profile-layers.svg" alt="Layered profile model" width="720" />
</p>

## How it works

<p align="center">
  <img src="assets/architecture.svg" alt="Five-stage architecture" width="760" />
</p>

1. **Intro** — seed identity with a few反问 (counter-questions) instead of a cold form.
2. **Dig** — deepen on goals, blockers and working style; contradictions are surfaced and resolved on the spot.
3. **Assessment** (optional) — a short calibration quiz folds cognitive-style signals into the profile (never as a label).
4. **Calibration** — the agent outputs *its understanding of you* for review. You nod, or you correct it. Only then is it persisted.
5. **Assembly** — renders the five skeleton files, writes `SKILLS.md`, and marks a revisit checkpoint.

<p align="center">
  <img src="assets/skeletons.svg" alt="Skeleton prompts" width="760" />
</p>

## Quick start

```bash
pip install ai-know-you            # core
pip install "ai-know-you[crypto]"  # + encrypted vault
```

```bash
ai-know-you run       # interactive five-stage wizard
ai-know-you sample    # non-interactive demo (great for CI / docs)
ai-know-you show      # print the stored profile
ai-know-you doctor    # environment self-check
```

## One-click skill install

After Assembly, open `SKILLS.md` — it contains a ready-to-copy prompt. Paste it into any agent that supports skills (WorkBuddy / Claude / Codex / …) and it installs the recommended set for you:

```
请帮我安装以下技能（如尚未安装）：
- coding-copilot
- blunt-communicator
- goal-tracker
- content-writer
- privacy-guard

这些是 ai-know-you 基于我的用户档案推荐的技能，请直接启用。
```

You can also print it any time with:

```bash
ai-know-you skills
```

## Commands

| Command | Purpose |
| --- | --- |
| `ai-know-you run` | Interactive five-stage onboarding wizard |
| `ai-know-you sample` | Non-interactive demo run (CI / docs friendly) |
| `ai-know-you show` | Print the stored profile |
| `ai-know-you export` | Export to `json` / `yaml` / `obsidian` / `dot` |
| `ai-know-you graph` | Render the profile relationship map (SVG) |
| `ai-know-you skills` | Print a one-click skill install prompt |
| `ai-know-you seal` / `unseal` | Encrypt / decrypt the local `.akyv` vault |
| `ai-know-you doctor` | Environment self-check |

## Relationship graph

<p align="center">
  <img src="assets/profile-graph.svg" alt="Profile relationship graph" width="720" />
</p>

```bash
ai-know-you graph --dir ./my-profile
```

## Privacy & local-first

Everything lives on disk as plain Markdown + YAML frontmatter — portable across agents and readable by humans. No cloud, no telemetry. The pipeline strips sensitive fields (credentials, national IDs, health data, precise location) before they ever reach the storage layer.

## Roadmap

- [ ] Web UI preview of the live profile + graph
- [ ] Plugin system for domain-specific assessments
- [ ] Encrypted sync between machines (still zero-knowledge)
- [ ] Template packs for popular agent memory formats
- [ ] `asciinema` / GIF demo on the landing page

## Multilingual

This README is available in:

- [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) and the design contract in [SPEC.md](docs/SPEC.md). The roadmap lives in [ROADMAP.md](docs/ROADMAP.md).

## License

[MIT](LICENSE) © cuiyaohan. The software is provided "as is", without warranty of any kind.
