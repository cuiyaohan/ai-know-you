<p align="center">
  <img src="assets/banner.svg" alt="ai-know-you" width="100%" />
</p>

<p align="center">
  <b>智慧體時代的入職嚮導。</b><br/>
  一套標準化、可複跑、可移植的流程，讓<b>任何</b> AI 智慧體真正懂它的使用者。
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
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

---

## 描述

`ai-know-you` 是一個開源的入職嚮導，讓任何智慧體從零開始「全方面懂你」——一次對話，生成可移植的使用者檔案與智慧體骨架提示詞。

基於 [MIT 許可證](LICENSE) 開源。完整中英描述與證書聲明見 [DESCRIPTION.md](DESCRIPTION.md)。

## 為什麼需要它

當你拿到一個全新的智慧體（Claude Code、Codex、WorkBuddy，或你自建的）時，它對你**一無所知**。它只能用一次次含糊的對話慢慢摸索你，而且下個會話就忘光。

`ai-know-you` 把「了解你」變成**一次性的、可複跑的、可移植的流程**。跑一遍，你就得到一套*檔案包*——帶結構化 frontmatter 的純 Markdown 檔案——任何智慧體都能載入，且完全歸你所有。

> 一句話定位：**`ai-know-you` 就是智慧體入職界的 `create-react-app`。**

## 功能特性

- **五階段流水線。** 初識 → 深挖 → 可選測評 → **校準** → 裝配。校準階段是最大差異點：智慧體先向你展示「我理解中的你」，等你點頭或糾正後才會落庫——杜絕「我懂你了」式的幻覺。
- **分層檔案模型。** 事實 / 偏好 / 邊界各自獨立演進，而不是塌縮成一團不分層的泥。
- **可移植骨架提示詞。** 生成 `SOUL` / `IDENTITY` / `USER` / `MEMORY` / `REDLINES`——直接丟進任何支援記憶骨架的智慧體。
- **多格式匯出。** 一份檔案可匯出 `json`、`yaml`、Obsidian 風格 Markdown、以及 Graphviz `dot`。
- **關係圖。** 把檔案渲染成自包含 SVG（或 DOT），*看見*你的事實、偏好與邊界如何連接。
- **零知識本地保險庫。** 整個檔案目錄可用 AES-256-CBC + PBKDF2-HMAC-SHA256 封進單個 `.akyv` 檔案（可選 `crypto` 依賴），資料不出本機。
- **可審計的技能推薦器。** 基於檔案推導「一鍵安裝技能」提示詞，規則透明、可解釋——每條推薦都帶理由。
- **本地優先與隱私脫敏。** 敏感類別（憑證、證件、健康、精確位置）在寫入前即被識別並脫敏。
- **復訪機制。** 可重複執行以增量更新檔案；流水線冪等且感知合併。

<p align="center">
  <img src="assets/profile-layers.svg" alt="分層檔案模型" width="720" />
</p>

## 工作原理

<p align="center">
  <img src="assets/architecture.svg" alt="五階段架構" width="760" />
</p>

1. **初識** —— 用幾個反問播種身份，而非冷冰冰的表單。
2. **深挖** —— 深入目標、阻礙與工作風格；矛盾當場擺出並解決。
3. **測評**（可選） —— 簡短校準問卷把認知風格信號折進檔案（絕不當標籤）。
4. **校準** —— 智慧體輸出*它對你的理解*供你審閱。你點頭，或糾正它。只有這時才落庫。
5. **裝配** —— 渲染五份骨架檔案、寫出 `SKILLS.md`，並標記一個復訪檢查點。

<p align="center">
  <img src="assets/skeletons.svg" alt="骨架提示詞" width="760" />
</p>

## 快速開始

```bash
pip install ai-know-you            # 核心
pip install "ai-know-you[crypto]"  # + 加密保險庫
```

```bash
ai-know-you run       # 互動式五階段嚮導
ai-know-you sample    # 非互動式示範（適合 CI / 文件）
ai-know-you show      # 列印已存檔案
ai-know-you doctor    # 環境自檢
```

## 一鍵安裝技能

裝配完成後，開啟 `SKILLS.md`——裡面有一段可直接複製的提示詞。把它貼進任何支援技能的智慧體（WorkBuddy / Claude / Codex / …）即可為你安裝推薦技能集：

```
請幫我安裝以下技能（如尚未安裝）：
- coding-copilot
- blunt-communicator
- goal-tracker
- content-writer
- privacy-guard

這些是 ai-know-you 基於我的使用者檔案推薦的技能，請直接啟用。
```

隨時也可列印它：

```bash
ai-know-you skills
```

## 命令

| 命令 | 用途 |
| --- | --- |
| `ai-know-you run` | 互動式五階段入職嚮導 |
| `ai-know-you sample` | 非互動式示範執行（適合 CI / 文件） |
| `ai-know-you show` | 列印已存檔案 |
| `ai-know-you export` | 匯出為 `json` / `yaml` / `obsidian` / `dot` |
| `ai-know-you graph` | 渲染檔案關係圖（SVG） |
| `ai-know-you skills` | 列印一鍵安裝技能提示詞 |
| `ai-know-you seal` / `unseal` | 加密 / 解密本地 `.akyv` 保險庫 |
| `ai-know-you doctor` | 環境自檢 |

## 關係圖

<p align="center">
  <img src="assets/profile-graph.svg" alt="檔案關係圖" width="720" />
</p>

```bash
ai-know-you graph --dir ./my-profile
```

## 隱私與本地優先

所有資料都以純 Markdown + YAML frontmatter 存於本地——跨智慧體可移植、人類可讀。無雲端、無遙測。流水線會在敏感欄位寫入儲存層之前就將其剝離（憑證、身分證號、健康資料、精確位置）。

## 路線圖

- [ ] 即時檔案 + 關係圖的 Web 預覽
- [ ] 領域專屬測評的插件系統
- [ ] 跨裝置的加密同步（仍零知識）
- [ ] 主流智慧體記憶格式的模版包
- [ ] 落地頁的 `asciinema` / GIF 示範

## 多語言

本 README 提供以下語言：

- [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

## 貢獻

參見 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 與 [SPEC.md](docs/SPEC.md) 中的設計契約。路線圖見 [ROADMAP.md](docs/ROADMAP.md)。

## 授權

[MIT](LICENSE) © cuiyaohan。軟體按「現狀」提供，不作任何擔保。
