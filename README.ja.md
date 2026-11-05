<p align="center">
  <img src="assets/logo.svg" alt="ai-know-you" width="160" height="160" />
</p>

<h1 align="center">ai-know-you</h1>

<p align="center">
  <b>エージェント時代のオンボーディング・ウィザード。</b><br/>
  <b>どの</b> AI エージェントにも、ユーザーを真に理解させる標準化された再実行可能で移植性の高いパイプライン。
</p>

<p align="center">
  <a href="https://github.com/cuiyaohan/ai-know-you/actions"><img src="https://img.shields.io/github/actions/workflow/status/cuiyaohan/ai-know-you/ci.yml?branch=main&label=CI" alt="CI" /></a>
  <img src="https://img.shields.io/github/v/release/cuiyaohan/ai-know-you?label=release&color=4F46E5" alt="release" />
  <img src="https://img.shields.io/badge/license-MIT-0EA5E9" alt="license" />
  <img src="https://img.shields.io/badge/python-3.9%2B-4F46E5" alt="python" />
  <img src="https://img.shields.io/github/stars/cuiyaohan/ai-know-you?style=social" alt="stars" />
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

---

## なぜ作られたのか

真新しいエージェント——Claude Code、Codex、WorkBuddy、あるいは自作のもの——を渡されても、それはあなたのことを**何も知りません**。曖昧なチャットを重ねながらゆっくり学び、次のセッションでは忘れてしまいます。

`ai-know-you` は「あなたを知る」を**一度で再現可能かつ移植可能な**フローにします。一度実行すれば、構造化された frontmatter を持つプレーンな Markdown ファイルからなる*プロフィールパッケージ*が得られ、どのエージェントでも読み込め、完全にあなたのものになります。

> 一言でいえば：**`ai-know-you` はエージェント・オンボーディングにおける `create-react-app` です。**

## 得られるもの

フローを実行すると、ローカルに移植可能なパッケージが生成されます：

| ファイル | 役割 |
|----------|------|
| `SOUL.md` | エージェントとは何か——その声と原則 |
| `IDENTITY.md` | エージェントの自己同一性（編集用） |
| `USER.md` | *あなた*に関する生きたプロフィール |
| `MEMORY.md` | 抽出された長期メモ（事実 + 好み） |
| `REDLINES.md` | 決して越えてはならない硬い境界線 |
| `profile.md` | 機械可読な frontmatter を含む完全な階層プロフィール |

すべて人間が読め、Git に優しく、特定のエージェントに依存しません。

## 5 つのステージ

<p align="center">
  <img src="assets/architecture.svg" alt="ai-know-you パイプライン" width="100%" />
</p>

1. **初識（Intro）**——基礎像を作るオープンな質問（あなたは誰か、目標、エージェントの使い方）。
2. **深挖（Dig）**——回答を掘り下げ、当てずっぽうではなく矛盾を顕在化させる。
3. **测评（Assess）**（任意）——非診断的なコミュニケーションスタイルのキャリブレーション。ラベル付けでも診断でもない。
4. **校准（Calibrate）**——エージェントがあなたを*どう理解したか*を述べ、保存する**前**にあなたが承認または修正する。「幻覚で『あなたを知っている』」を防ぐ。
5. **装配（Assemble）**——5 つのスケルトンファイルと構造化された `profile.md` を書き出す。

## 設計原則

- **ローカル優先。** すべてはあなたのディスク上に。クラウドもテレメトリもアカウントもなし。
- **プライバシー既定オン。** 機密カテゴリ（資格情報、身分証、健康、正確な位置）は書き込み前に検出・秘匿化される。
- **塊ではなく階層。** 事実・好み・境界が独立して進化し、プロフィールは長期間一貫する。
- **生きており、一度限りではない。** 復訪メカニズムが N 日ごと、または新しいシグナル検出時に差分更新する。
- **移植性。** 標準 Markdown + YAML frontmatter。 `SOUL/IDENTITY/USER/MEMORY` スケルトンを支持する任意のエージェントへそのまま投入可能。

## クイックスタート

```bash
# インストール
pip install -e .

# 対話型ウィザードを実行
ai-know-you run

# 非対話型のデモ・プロフィールを生成（CI / ドキュメントに最適）
ai-know-you sample --dir ./demo-profile

# 取得内容を確認
ai-know-you show

# 環境を検証
ai-know-you doctor
```

> 深度モード：`--depth fast`（約 5 分、十分）または `--depth deep`（約 30 分、より良い）。同じエンジン、異なる深度。第 3 ステージの評価は `--assess` で任意選択。

## 出力例

実行後、`USER.md` は次のようになります：

```markdown
# USER.md - About Your Human

- **Name:** Cui
- **Occupation:** indie developer / content creator
- **City:** Shenzhen

## Context
- **primary_goal**: ship ai-know-you to 100k GitHub stars
- **agent_use_case**: coding

## How they like to work
- **communication_style**: direct and concise
- **avoids**: assistants that reply too verbosely
```

## ロードマップ

- [ ] 第 3 ステージ評価のプラグインシステム（MBTI、ビッグファイブ、意思決定スタイル）
- [ ] 組み立て後のマッチするスキルの自動インストール
- [ ] 主要エージェント記憶フォーマット（Claude、Codex、WorkBuddy）との入出力
- [ ] 定期復訪デーモン
- [ ] ウィザードの Web UI
- [ ] 本 README へのさらなる言語追加

## 国際化

本 README は多言語で提供され、翻訳はコミュニティで維持されています——PR を歓迎します。

| 言語 | ファイル |
|------|----------|
| English | [README.md](README.md) |
| 简体中文 | [README.zh-CN.md](README.zh-CN.md) |
| 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 한국어 | [README.ko.md](README.ko.md) |

## コントリビュート

翻訳、新しい評価プラグイン、バグ修正——どんな助けも歓迎します。[CONTRIBUTING.md](docs/CONTRIBUTING.md) と [Spec](docs/SPEC.md) をご覧ください。お互いを大切に。

## ライセンス

[MIT](LICENSE) © ai-know-you contributors.
