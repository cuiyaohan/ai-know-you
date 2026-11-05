<p align="center">
  <img src="assets/banner.svg" alt="ai-know-you" width="100%" />
</p>

<p align="center">
  <b>智能体时代的入职向导。</b><br/>
  一套标准化、可复跑、可移植的流程，让<b>任何</b> AI 智能体真正懂它的用户。
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
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

---

## 描述

`ai-know-you` 是一个开源的入职向导，让任何智能体从零开始「全方面懂你」——一次对话，生成可移植的用户档案与智能体骨架提示词。

基于 [MIT 许可证](LICENSE) 开源。完整中英描述与证书声明见 [DESCRIPTION.md](DESCRIPTION.md)。

## 为什么需要它

当你把一个全新的智能体（Claude Code、Codex、WorkBuddy，或你自建的）交到手里，它对你**一无所知**。它只能用一次次含糊的聊天慢慢摸索你，而且下个会话就忘光。

`ai-know-you` 把「了解你」变成**一次性的、可复跑的、可移植的流程**。跑一遍，你就得到一套*档案包*——带结构化 frontmatter 的纯 Markdown 文件——任何智能体都能加载，且完全归你所有。

> 一句话定位：**`ai-know-you` 就是智能体入职界的 `create-react-app`。**

## 功能特性

- **五阶段流水线。** 初识 → 深挖 → 可选测评 → **校准** → 装配。校准阶段是最大差异点：智能体先向你展示「我理解的你」，等你点头或纠正后才会落库——杜绝「我懂你了」式的幻觉。
- **分层档案模型。** 事实 / 偏好 / 边界各自独立演进，而不是塌缩成一团不分层的泥。
- **可移植骨架提示词。** 生成 `SOUL` / `IDENTITY` / `USER` / `MEMORY` / `REDLINES`——直接丢进任何支持记忆骨架的智能体。
- **多格式导出。** 一份档案可导出 `json`、`yaml`、Obsidian 风格 Markdown、以及 Graphviz `dot`。
- **关系图。** 把档案渲染成自包含 SVG（或 DOT），*看见*你的事实、偏好与边界如何连接。
- **零知识本地保险库。** 整个档案目录可用 AES-256-CBC + PBKDF2-HMAC-SHA256 封进单个 `.akyv` 文件（可选 `crypto` 依赖），数据不出本机。
- **可审计的技能推荐器。** 基于档案推导「一键安装技能」提示词，规则透明、可解释——每条推荐都带理由。
- **本地优先与隐私脱敏。** 敏感类别（凭据、证件、健康、精确定位）在写入前即被识别并脱敏。
- **复访机制。** 可重复运行以增量更新档案；流水线幂等且感知合并。

<p align="center">
  <img src="assets/profile-layers.svg" alt="分层档案模型" width="720" />
</p>

## 工作原理

<p align="center">
  <img src="assets/architecture.svg" alt="五阶段架构" width="760" />
</p>

1. **初识** —— 用几个反问播种身份，而非冷冰冰的表单。
2. **深挖** —— 深入目标、阻碍与工作风格；矛盾当场摆出并解决。
3. **测评**（可选） —— 简短校准问卷把认知风格信号折进档案（绝不当标签）。
4. **校准** —— 智能体输出*它对你的理解*供你审阅。你点头，或纠正它。只有这时才落库。
5. **装配** —— 渲染五份骨架文件、写出 `SKILLS.md`，并标记一个复访检查点。

<p align="center">
  <img src="assets/skeletons.svg" alt="骨架提示词" width="760" />
</p>

## 快速开始

```bash
pip install ai-know-you            # 核心
pip install "ai-know-you[crypto]"  # + 加密保险库
```

```bash
ai-know-you run       # 交互式五阶段向导
ai-know-you sample    # 非交互式演示（适合 CI / 文档）
ai-know-you show      # 打印已存档案
ai-know-you doctor    # 环境自检
```

## 一键安装技能

装配完成后，打开 `SKILLS.md`——里面有一段可直接复制的提示词。把它粘贴进任何支持技能的智能体（WorkBuddy / Claude / Codex / …）即可为你安装推荐技能集：

```
请帮我安装以下技能（如尚未安装）：
- coding-copilot
- blunt-communicator
- goal-tracker
- content-writer
- privacy-guard

这些是 ai-know-you 基于我的用户档案推荐的技能，请直接启用。
```

随时也可打印它：

```bash
ai-know-you skills
```

## 命令

| 命令 | 用途 |
| --- | --- |
| `ai-know-you run` | 交互式五阶段入职向导 |
| `ai-know-you sample` | 非交互式演示运行（适合 CI / 文档） |
| `ai-know-you show` | 打印已存档案 |
| `ai-know-you export` | 导出为 `json` / `yaml` / `obsidian` / `dot` |
| `ai-know-you graph` | 渲染档案关系图（SVG） |
| `ai-know-you skills` | 打印一键安装技能提示词 |
| `ai-know-you seal` / `unseal` | 加密 / 解密本地 `.akyv` 保险库 |
| `ai-know-you doctor` | 环境自检 |

## 关系图

<p align="center">
  <img src="assets/profile-graph.svg" alt="档案关系图" width="720" />
</p>

```bash
ai-know-you graph --dir ./my-profile
```

## 隐私与本地优先

所有数据都以纯 Markdown + YAML frontmatter 存于本地——跨智能体可移植、人类可读。无云端、无遥测。流水线会在敏感字段写入存储层之前就将其剥离（凭据、身份证号、健康数据、精确定位）。

## 路线图

- [ ] 实时档案 + 关系图的 Web 预览
- [ ] 领域专属测评的插件系统
- [ ] 跨设备的加密同步（仍零知识）
- [ ] 主流智能体记忆格式的模版包
- [ ] 落地页的 `asciinema` / GIF 演示

## 多语言

本 README 提供以下语言：

- [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

## 贡献

参见 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 与 [SPEC.md](docs/SPEC.md) 中的设计契约。路线图见 [ROADMAP.md](docs/ROADMAP.md)。

## 许可证

[MIT](LICENSE) © cuiyaohan。软件按「现状」提供，不作任何担保。
