<p align="center">
  <img src="assets/banner.svg" alt="ai-know-you" width="100%" />
</p>

<p align="center">
  <b>에이전트 시대의 온보딩 위저드.</b><br/>
  <b>어떤</b> AI 에이전트든 사용자를 진짜로 알게 만드는 표준화되고 재실행 가능하며 이식성 높은 파이프라인.
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
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ja.md">日本語</a>
</p>

---

## 개요

`ai-know-you` 는 어떤 에이전트든 제로부터 "사용자를 진짜로 이해"하게 만드는 오픈소스 온보딩 위저드입니다——한 번의 대화로 이식 가능한 사용자 프로필과 에이전트용 스켈레톤 프롬프트를 생성합니다.

[MIT 라이선스](LICENSE) 로 공개되어 있습니다. 완전한 한·영 설명과 라이선스 선언은 [DESCRIPTION.md](DESCRIPTION.md) 를 참고하세요.

## 왜 만들었는가

새로운 에이전트——Claude Code, Codex, WorkBuddy, 또는 직접 만든 것——를 받으면 그것은 당신에 대해 **전혀 모릅니다**. 모호한 채팅을 거듭하며 천천히 배우고, 다음 세션에는 잊어버립니다.

`ai-know-you` 는 "당신을 아는 것"을 **한 번에, 반복 가능하고 이식 가능한** 흐름으로 만듭니다. 한 번 실행하면 구조화된 frontmatter 를 가진 순수 Markdown 파일로 된 *프로필 패키지*가 생성되어, 어떤 에이전트든 불러올 수 있고 전적으로 당신의 것이 됩니다.

> 한 줄 정의: **`ai-know-you` 는 에이전트 온보딩의 `create-react-app` 입니다.**

## 기능

- **5 단계 파이프라인.** 첫만남 → 파고들기 → 선택 평가 → **보정** → 조립. 차별점은 보정 단계: 에이전트는 먼저 "내가 이해한 당신"을 보여주고, 당신이 고개를 끄덕이거나 수정한 뒤에야 저장합니다——"알 것 같다"는 환각을 막습니다.
- **계층 프로필 모델.** 사실 / 선호 / 경계가 각각 독립적으로 진화하여 한 덩어리로 뭉치지 않습니다.
- **이식 가능한 스켈레톤 프롬프트.** `SOUL` / `IDENTITY` / `USER` / `MEMORY` / `REDLINES` 를 생성——메모리 스켈레톤을 지원하는 어떤 에이전트에도 그대로 투입 가능.
- **다중 형식 내보내기.** 하나의 프로필에서 `json`, `yaml`, Obsidian 형식 Markdown, Graphviz `dot` 을 출력.
- **관계 도표.** 프로필을 자체 완결형 SVG(또는 DOT)로 렌더해 사실·선호·경계의 연결을 *시각화*합니다.
- **제로 지식 로컬 금고.** 프로필 전체를 AES-256-CBC + PBKDF2-HMAC-SHA256 으로 단일 `.akyv` 파일에 봉인(선택적 `crypto` 종속). 데이터는 장치를 떠나지 않습니다.
- **감사 가능한 스킬 추천기.** 프로필에서 "원클릭 스킬 설치" 프롬프트를 도출. 규칙은 투명하고 설명 가능——각 추천에 이유가 붙습니다.
- **로컬 우선과 프라이버시 비식별화.** 민감 범주(자격 증명, 신분증, 건강, 정밀 위치)는 쓰기 전에 감지·비식별화됩니다.
- **재방문 메커니즘.** 재실행으로 증분 갱신. 파이프라인은 멱등하며 병합을 인식합니다.

<p align="center">
  <img src="assets/profile-layers.svg" alt="계층 프로필 모델" width="720" />
</p>

## 작동 방식

<p align="center">
  <img src="assets/architecture.svg" alt="5 단계 아키텍처" width="760" />
</p>

1. **첫만남 (Intro)** —— 차가운 양식이 아니라 몇 가지 되묻기로 정체성을 심습니다.
2. **파고들기 (Dig)** —— 목표·장애·작업 방식을 깊이 파고들며 모순을 현장에서 드러내 해결합니다.
3. **평가 (Assess)** (선택) —— 짧은 캘리브레이션 질문으로 인지 스타일 신호를 접습니다(절대 라벨화하지 않음).
4. **보정 (Calibrate)** —— 에이전트가 *당신에 대한 이해*를 출력해 검토합니다. 고개를 끄덕이거나 수정합니다. 그때만 저장합니다.
5. **조립 (Assemble)** —— 5 개의 스켈레톤 파일을 렌더하고 `SKILLS.md` 를 쓴 뒤 재방문 체크포인트를 찍습니다.

<p align="center">
  <img src="assets/skeletons.svg" alt="스켈레톤 프롬프트" width="760" />
</p>

## 빠른 시작

```bash
pip install ai-know-you            # 코어
pip install "ai-know-you[crypto]"  # + 암호화 금고
```

```bash
ai-know-you run       # 대화형 5 단계 위저드
ai-know-you sample    # 비대화형 데모 (CI / 문서용)
ai-know-you show      # 저장된 프로필 출력
ai-know-you doctor    # 환경 자가 진단
```

## 원클릭 스킬 설치

조립이 끝나면 `SKILLS.md` 가 생성됩니다——그 안에 복사 가능한 프롬프트가 있습니다. 스킬을 지원하는 에이전트(WorkBuddy / Claude / Codex / …)에 붙여넣기만 하면 추천 스킬 세트가 설치됩니다：

```
請幫我安裝以下技能（如尚未安裝）：
- coding-copilot
- blunt-communicator
- goal-tracker
- content-writer
- privacy-guard

這些是 ai-know-you 基於我的用戶檔案推薦的技能，請直接啟用。
```

언제든 출력할 수 있습니다：

```bash
ai-know-you skills
```

## 명령어

| 명령어 | 용도 |
| --- | --- |
| `ai-know-you run` | 대화형 5 단계 온보딩 위저드 |
| `ai-know-you sample` | 비대화형 데모 실행 (CI / 문서용) |
| `ai-know-you show` | 저장된 프로필 출력 |
| `ai-know-you export` | `json` / `yaml` / `obsidian` / `dot` 로 내보내기 |
| `ai-know-you graph` | 프로필 관계 도표 렌더 (SVG) |
| `ai-know-you skills` | 원클릭 스킬 설치 프롬프트 출력 |
| `ai-know-you seal` / `unseal` | 로컬 `.akyv` 금고 암호화 / 복호화 |
| `ai-know-you doctor` | 환경 자가 진단 |

## 관계 도표

<p align="center">
  <img src="assets/profile-graph.svg" alt="프로필 관계 도표" width="720" />
</p>

```bash
ai-know-you graph --dir ./my-profile
```

## 프라이버시와 로컬 우선

모든 데이터는 로컬의 순수 Markdown + YAML frontmatter 로 저장됩니다——에이전트 간 이식 가능, 인간도 읽을 수 있음. 클라우드도 텔레메트리도 없음. 파이프라인은 민감 필드를 저장 계층에 쓰기 전에 strip 합니다(자격 증명, 신분증 번호, 건강 데이터, 정밀 위치).

## 로드맵

- [ ] 라이브 프로필 + 관계 도표의 Web 미리보기
- [ ] 도메인별 평가의 플러그인 시스템
- [ ] 장치 간 암호화 동기화 (여전히 제로 지식)
- [ ] 주요 에이전트 기억 형식용 템플릿 세트
- [ ] 랜딩 페이지의 `asciinema` / GIF 데모

## 다국어

이 README 는 다음 언어로 제공됩니다：

- [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

## 기여

설계 계약은 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 와 [SPEC.md](docs/SPEC.md) 를 참고하세요. 로드맵은 [ROADMAP.md](docs/ROADMAP.md) 에 있습니다.

## 라이선스

[MIT](LICENSE) © cuiyaohan. 이 소프트웨어는 "있는 그대로" 제공되며 어떠한 보증도 없습니다.
