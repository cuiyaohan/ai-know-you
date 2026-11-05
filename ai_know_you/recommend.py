"""Recommend agent skills from a calibrated profile and render an install prompt.

The recommender is a small, transparent ruleset over the profile text. It is
intentionally explainable (every pick carries a reason) rather than a black box,
so the user can trust and audit what gets suggested.
"""

from __future__ import annotations

from typing import Dict, List

from .profile.models import Profile

_CATALOG: Dict[str, str] = {
    "coding-copilot": "代码协作 / 工程辅助类技能",
    "blunt-communicator": "直接、快节奏的沟通型技能",
    "goal-tracker": "目标设定与追踪类技能",
    "content-writer": "内容创作 / 写作类技能",
    "research-assistant": "资料检索与研究类技能",
    "privacy-guard": "隐私与本地优先处理类技能",
    "time-blocker": "时间块 / 精力管理类技能",
}


def recommend(p: Profile) -> List[Dict[str, str]]:
    text = " ".join(
        [
            p.occupation,
            p.city,
            p.notes.get("goal", ""),
            p.facts.get("success_in_3m", ""),
            p.preferences.get("communication_style", ""),
        ]
    ).lower()

    picks: List[Dict[str, str]] = []

    def add(name: str) -> None:
        if not any(x["name"] == name for x in picks):
            picks.append({"name": name, "reason": _CATALOG[name]})

    if any(k in text for k in ["dev", "code", "program", "indie", "engineer", "工程", "开发", "软件", "码"]):
        add("coding-copilot")
    if any(k in text for k in ["blunt", "direct", "fast", "直", "快", "简"]):
        add("blunt-communicator")
    if p.facts.get("success_in_3m") or "goal" in p.notes:
        add("goal-tracker")
    if any(k in text for k in ["write", "content", "创作", "公众号", "author", "文章", "写"]):
        add("content-writer")
    if any(k in text for k in ["research", "调研", "研究", "search"]):
        add("research-assistant")
    add("privacy-guard")
    if any(k in text for k in ["time", "节奏", "精力", "rhythm"]):
        add("time-blocker")
    if not picks:
        add("research-assistant")
    return picks


def render_skills_md(p: Profile) -> str:
    recs = recommend(p)
    names = [r["name"] for r in recs]
    lines = [
        "---",
        "title: SKILLS.md",
        "generated_by: ai-know-you",
        'schema_version: "1.0"',
        "---",
        "",
        "# 推荐技能 · Recommended Skills",
        "",
        "> 由 ai-know-you 基于你的用户档案自动推导。安装后你的 Agent 将更懂如何协助你。",
        "",
        "## 推荐清单",
        "",
    ]
    for r in recs:
        lines.append(f"- **{r['name']}** — {r['reason']}")
    lines += [
        "",
        "## 一键安装（复制下方提示词，粘贴给你的 Agent）",
        "",
        "```text",
        "请帮我安装以下技能（如尚未安装）：",
    ]
    for n in names:
        lines.append(f"- {n}")
    lines += [
        "",
        "这些是 ai-know-you 基于我的用户档案推荐的技能，请直接启用。",
        "```",
        "",
        "> 适用于支持技能安装的 Agent（如 WorkBuddy / Claude / Codex 等）。",
        "",
    ]
    return "\n".join(lines)


def render_install_prompt(p: Profile) -> str:
    names = [r["name"] for r in recommend(p)]
    head = "请帮我安装以下技能（如尚未安装）："
    body = "\n".join(f"- {n}" for n in names)
    tail = "\n\n这些是 ai-know-you 基于我的用户档案推荐的技能，请直接启用。"
    return head + "\n" + body + tail
