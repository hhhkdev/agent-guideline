# 🧠 Agent Guideline & Harness Ecosystem

> **AI 에이전트(Claude Code, Codex CLI, Antigravity, Cursor)를 위한 엔터프라이즈급 하네스 아키텍처, 템플릿, 스킬 아카이브 및 자동화 도구**

본 저장소는 실무 소프트웨어 엔지니어링 환경에서 AI 코딩 에이전트가 길을 잃지 않고, 프로젝트 고유의 아키텍처 원칙을 엄수하며, 자율적인 결정론적 검증(Deterministic Verification)을 완수할 수 있도록 돕는 체계적인 지침서 및 도구 모음입니다.

---

## 📑 목차

1. [핵심 철학 및 하네스 아키텍처](#-핵심-철학-및-하네스-아키텍처)
2. [저장소 디렉터리 구조](#-저장소-디렉터리-구조)
3. [프로젝트 생태계 분석 요약](#-프로젝트-생태계-분석-요약)
4. [스택별 하네스 템플릿](#-스택별-하네스-템플릿)
5. [아카이빙된 스킬 (Skills Archive)](#-아카이빙된-스킬-skills-archive)
6. [자동화 CLI 도구 (`harness-cli`)](#-자동화-cli-도구-harness-cli)
7. [크로스 AI 도구 운용 가이드](#-크로스-ai-도구-운용-가이드)

---

## 🏛 핵심 철학 및 하네스 아키텍처

AI 코딩 에이전트는 컨텍스트가 너무 적으면 프로젝트 컨벤션을 파괴하고, 너무 많으면 주의력(Attention)이 분산되어 환각을 일으킵니다. 이를 극복하기 위해 **5계층 하네스(5-Layer Harness)** 구조를 제안합니다.

```
┌────────────────────────────────────────────────────────┐
│  Layer 1. Entrypoint (AGENTS.md)                       │
│  - 100줄 이내 압축 진입점, 골든 룰, 단일 검증 관문    │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 2. Intent Router                                │
│  - 의도별(/feat, /api, /refactor 등) 가이드 문서 매핑  │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 3. Progressive Context (docs/ai/*)              │
│  - 필요할 때만 선별 로드되는 도메인별 상세 지식        │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 4. Verification Gate (Deterministic Feedback)   │
│  - lint, typecheck, analyze, custom rule scripts       │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 5. Tech Debt & Principles Monitoring            │
│  - 타협된 코드 기록(TECH_DEBT.md) 및 아키텍처 감시    │
└────────────────────────────────────────────────────────┘
```

자세한 원칙은 [`02-harness-architecture/01-harness-core-principles.md`](02-harness-architecture/01-harness-core-principles.md)를 참고하세요.

---

## 📂 저장소 디렉터리 구조

```
agent-guideline/
├── 01-ecosystem-analysis/       # 사용자 실제 17개 프로젝트 기술 스택 및 AI 준비도 분석
│   ├── 01-project-inventory.md
│   └── 02-tool-landscape.md
├── 02-harness-architecture/     # 하네스 설계 원칙 및 컨텍스트 관리 기법
│   ├── 01-harness-core-principles.md
│   ├── 02-context-engineering.md
│   └── 03-verification-harness.md
├── 03-templates/                # 즉시 복사하여 사용할 수 있는 스택별 프로덕션 템플릿
│   ├── universal/               # 범용 기본 템플릿 (AGENTS.md, CLAUDE.md)
│   ├── nextjs-fullstack/        # Next.js App Router + Tailwind + TanStack Query + Knip
│   ├── react-native-expo/       # React Native Expo + Swift Widgets + EAS OTA 안전잠금
│   ├── flutter-riverpod/        # Flutter + Riverpod + Design Tokens + flutter analyze
│   ├── spring-boot-jvm/         # Spring Boot 3 + JPA + Gradle + Docker Dev
│   └── design-system/           # Storybook + Tailwind Token System + Lib Build
├── 04-skills-archive/           # Antigravity / Codex 표준 규격의 재사용 가능 스킬
│   ├── react-native-ios-harness/
│   ├── flutter-design-token-guardian/
│   ├── tanstack-query-contract-generator/
│   ├── git-rebase-conflict-resolver/
│   └── figma-design-token-sync/
├── 05-prompt-engineering/       # 메타 프롬프트 및 역할 기반 페르소나 정의
│   ├── meta-prompts.md
│   └── role-based-prompts.md
├── 06-tooling-and-mcp/          # 도구 연동 및 MCP(Model Context Protocol) 가이드
│   ├── mcp-ecosystem-guide.md
│   └── developer-workflows.md
└── tools/
    └── harness-cli.py           # 프로젝트 스택 감지, 진단 및 하네스 자동 배포 CLI
```

---

## 📊 프로젝트 생태계 분석 요약

`/Users/hhhk/dev`의 실제 프로젝트 분석 결과 도출된 핵심 성향:

1. **프론트엔드/모바일 다중 플랫폼 중심**: Next.js App Router, React Native Expo, Flutter의 3대 축.
2. **엄격한 디자인 토큰 선호**: `CampusYA-FE`(`AppColors`, `AppTextStyles`), `teumteum-mobile`(Swift 홈 위젯 간격, 다크모드 대비), 독립 디자인 시스템 운영.
3. **결정론적 검증 절차**: `flutter analyze` 0 issues 강제, `verify:todo-ordering` 커스텀 스크립트 등 무결성 검증 루프 보유.

---

## 🛠 자동화 CLI 도구 (`harness-cli`)

프로젝트 디렉터리를 스캔하여 기술 스택을 감지하고, AI 하네스 준비도를 점수화하며, 최적화된 하네스를 1초 만에 자동 생성합니다.

### 1. 프로젝트 스캔 및 진단
```bash
python3 tools/harness-cli.py scan /Users/hhhk/dev/hivcd-backend
```
출력 예시:
```text
🔍 Scanning project at: /Users/hhhk/dev/hivcd-backend
============================================================
📦 Detected Category : spring-boot-jvm
🛠️  Tech Stack        : Spring Boot / JVM
🤖 Existing AI Setup : None
📊 AI Readiness Score: 0/100
⚠️  Needs setup. Run `python3 harness-cli.py init <path>` to install harness.
============================================================
```

### 2. 하네스 자동 초기화
```bash
python3 tools/harness-cli.py init /Users/hhhk/dev/hivcd-backend
```
자동으로 `AGENTS.md`, `CLAUDE.md`, `docs/ai/API_ARCHITECTURE.md`, `docs/ai/DOCKER_DEV.md`가 생성됩니다.

### 3. 아카이빙된 스킬 목록 조회
```bash
python3 tools/harness-cli.py list-skills
```

---

## 📦 아카이빙된 스킬 (Skills Archive)

| 스킬명 | 설명 | 주 적용 도메인 |
|---|---|---|
| `react-native-ios-harness` | Safe area, 한국어 IME 키보드, Swift 홈 위젯, EAS OTA 안전 배포 제어 | React Native / Expo |
| `flutter-design-token-guardian` | 하드코딩 색상/텍스트 차단, Riverpod 패턴 및 `flutter analyze` 무결성 강제 | Flutter |
| `tanstack-query-contract-generator` | DTO 인터페이스, API 클라이언트, TanStack Query 훅 및 캐시 무효화 3종 세트 일괄 생성 | Next.js / React |
| `git-rebase-conflict-resolver` | 충돌 마커 검사 및 비파괴적 안전 리베이스 계속 자동화 | 전체 프로젝트 공통 |
| `figma-design-token-sync` | Figma MCP 및 JSON 데이터를 Tailwind/Flutter 코드로 동기화 | Design System |

---

## 🤝 기여 및 로드맵

- [x] 사용자 17개 프로젝트 전수 분석 및 성향 리포트 작성
- [x] 5계층 하네스 아키텍처 및 토큰 예산 가이드 정립
- [x] 5대 주요 스택별 프로덕션 템플릿 제작 (Next.js, RN, Flutter, Spring Boot, Design System)
- [x] 핵심 스킬 5종 패키징 및 아카이빙
- [x] 자동 진단 및 스캐폴딩 CLI 도구(`harness-cli.py`) 개발
- [ ] Figma MCP 실시간 토큰 파서 통합
- [ ] Git Pre-commit 훅 기반의 에이전트 규칙 자동 검증기 추가
