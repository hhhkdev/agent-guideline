# 01. 개발 프로젝트 생태계 분석 보고서 (Project Ecosystem Inventory)

본 문서는 `/Users/hhhk/dev` 환경에 존재하는 실제 프로젝트들의 기술 스택, 아키텍처 패턴, 현재 AI 도입 현황을 심층 분석하여 맞춤형 에이전트 하네스 및 스킬셋을 도출하기 위한 기초 분석서입니다.

---

## 1. 프로젝트 전수 조사 및 분류

| 분류 | 프로젝트명 | 주 기술 스택 | 현재 AI 설정 | 주요 특징 및 도메인 |
|---|---|---|---|---|
| **Web Frontend** | `1D1S-client` | Next.js, React, Tailwind CSS, TypeScript | `AGENTS.md`, `CLAUDE.md`, `docs/ai/*` | 1일1커밋 플랫폼. 커스텀 하네스 라우터(`/ods-*`) 및 `docs/ai/` 분할 구조 도입 완료 |
| **Web Frontend** | `1D1S-admin` | Next.js, Tailwind CSS, TypeScript | 없음 | 1D1S 관리자 콘솔. Localias 기반 로컬 도메인 구성 |
| **Web Frontend** | `hivcd-frontend` | Next.js, Tailwind CSS, TypeScript | 없음 | 홍익대 시각디자인과(HIVCD) 예약/전시 플랫폼 |
| **Web Frontend** | `book-tierlist-client`| Next.js, Tailwind CSS, TypeScript | `AGENTS.md`, `CLAUDE.md` | 도서 티어리스트 웹 클라이언트 |
| **Web Frontend** | `wordledle-client` | Next.js, Tailwind CSS, TypeScript | `AGENTS.md`, `CLAUDE.md` | 워들 기반 단어 게임 |
| **Web Frontend** | `please-2000won-frontend`| Vite, React, Tailwind CSS, TypeScript | Claude session 히스토리만 존재 | 결제/기부 관련 프론트엔드 |
| **Web Frontend** | `teumteum-admin` | Next.js, Tailwind CSS, TypeScript | `.claude` | 틈틈 서비스 어드민 |
| **Web Frontend** | `teumteum-support` | Vite, React, Tailwind CSS, TypeScript | `.claude` | 틈틈 지원/고객센터 웹 |
| **Web Frontend** | `onebite-blog` | Vite, React, TypeScript | 없음 | 기술 블로그/학습 프로젝트 |
| **Design System** | `1D1S-design-system` | Storybook, Tailwind, Vite, TypeScript | 없음 | 1D1S 전용 컴포넌트 라이브러리 |
| **Design System** | `hivcd-design-system` | Storybook, Tailwind, Vite, TypeScript | Claude session 히스토리만 존재 | HIVCD 전용 디자인 시스템 |
| **Mobile App** | `teumteum-mobile` | React Native, Expo, Tailwind, Swift | `AGENTS.md`, `CLAUDE.md`, Codex Skill | 틈틈 모바일 앱. EAS OTA 잠금, iOS 홈 위젯(Swift), 파일 길이 엄격 제한 |
| **Mobile App** | `teumteum-deploy` | Expo, React Native (배포 파이프라인) | `AGENTS.md`, `CLAUDE.md` | 틈틈 빌드/배포 및 검증 스크립트 |
| **Mobile App** | `CampusYA-FE` | Flutter, Dart, Riverpod, go_router | `AGENTS.md`, `CLAUDE.md`, `.gemini` | 캠퍼스야 앱. 디자인 토큰(AppColors/AppTextStyles) 및 `flutter analyze` 무결성 검증 |
| **Mobile App** | `igem-alginate-film-mobile`| Expo, React Native | 없음 | 바이오/연구 관련 모바일 앱 |
| **Backend** | `hivcd-backend` | Spring Boot, JVM/Gradle, Docker | 없음 | HIVCD 서비스 API 서버 |
| **Backend** | `please-2000won-backend` | Spring Boot, JVM/Gradle, Docker | Claude session 히스토리만 존재 | 결제/백엔드 서비스 |
| **Backend** | `teumteum-server` | Backend 서비스 | 없음 | 틈틈 메인 백엔드 |
| **Tooling/Extension**| `gdg-hiu-figma-plugin` | TypeScript, Figma Plugin API | 없음 | GDG Figma 자동화 플러그인 |

---

## 2. 개발 생태계 경향성 (Key Tendencies)

### ① 프론트엔드 & 모바일 중심의 다중 플랫폼
- **Web**: Next.js App Router와 Vite 기반 SPA가 주를 이루며, 스타일링은 100% **Tailwind CSS**를 채택.
- **Mobile**: **React Native(Expo)**와 **Flutter** 투 트랙으로 운영.
- **Design System 분리**: 제품 앱과 별도로 `1D1S-design-system`, `hivcd-design-system`처럼 Storybook 기반 패키지를 별도 관리.

### ② 고도화된 UI/UX 디테일 및 디자인 토큰 준수 성향
- `CampusYA-FE`: 하드코딩된 색상/스타일을 엄격히 금지하고 `AppColors`, `AppTextStyles` 토큰만 사용하도록 강제.
- `teumteum-mobile`: iOS 홈 위젯 레이아웃, 줄 간격(10pt), 슬롯 분배, 다크모드 대비율 등 픽셀 단위 디테일과 네이티브(Swift) 연동 규칙이 고도로 정형화되어 있음.
- `Figma 연동`: `gdg-hiu-figma-plugin` 제작 및 Figma MCP 도입 등 Figma ↔ 코드 간 동기화에 높은 관심.

### ③ 멀티 AI 에이전트 툴 혼용
- **Claude Code (`CLAUDE.md`, `.claude`)**: 대화형 터미널 작업, 세션 로그 관리.
- **Codex CLI (`.codex`)**: 규칙 기반 커맨드 승인(`default.rules`), 커스텀 스킬(`teumteum-ios-expo/SKILL.md`).
- **Antigravity / Gemini (`.gemini`)**: IDE 통합, Subagent 호출, MCP 기반 브라우저/시스템 연동.
- **공통 문제점**: 각 툴마다 설정 파일 명칭(`AGENTS.md` vs `CLAUDE.md` vs `SKILL.md`)이 분산되어 프로젝트마다 동기화 비용 발생.

---

## 3. 현재 AI 적용 수준별 격차 분석

```
[Level 4: 구조화된 하네스] 1D1S-client (라우터 + docs/ai/* 계층 분리)
        ▲
[Level 3: 규칙 및 스킬화] teumteum-mobile, CampusYA-FE (도메인 특화 규칙, 검증 루프)
        ▲
[Level 2: 기본 가이드라인] book-tierlist-client, wordledle-client (단일 AGENTS.md)
        ▲
[Level 1: AI 흔적만 있음] teumteum-admin, hivcd-design-system, please-2000won-* (세션 캐시만 존재)
        ▲
[Level 0: AI 설정 없음]   hivcd-backend, please-2000won-backend, 1D1S-admin, gdg-figma-plugin
```

---

## 4. 도출된 핵심 요구사항 및 아카이빙 목표

1. **단일 진입점과 모듈형 하네스 (Harness Architecture)**
   - `1D1S-client`의 라우터 패턴을 표준화하여 모든 프로젝트에 즉시 이식 가능한 템플릿 제작.
   - 대형 프로젝트에서 컨텍스트 오염을 막는 `docs/ai/` 분할 로딩 원칙 확립.
2. **기술 스택별 Golden Standard 템플릿 라이브러리**
   - Next.js + Tailwind + TanStack Query
   - React Native + Expo + iOS WidgetKit (Swift)
   - Flutter + Riverpod + Clean Architecture + Design Tokens
   - Spring Boot + Gradle + JPA + Docker
   - Storybook 기반 Design System
3. **크로스 툴 호환성 (Universal Agent Configuration)**
   - `AGENTS.md`(범용/Antigravity/Codex), `CLAUDE.md`(Claude Code), `.cursorrules`(Cursor)의 단일 원본 관리 전략.
4. **자주 쓰는 패턴의 Skill 패키지화**
   - Git rebase 충돌 해결 자동화 (`git-rebase-conflict-resolver`)
   - Flutter / Web 디자인 토큰 강제 가디언 (`design-token-guardian`)
   - iOS Native / Expo 설정 검증 (`react-native-ios-harness`)
   - API 스펙 기반 TanStack Query 훅 생성기 (`tanstack-query-contract-generator`)
5. **자동 스캐폴딩 스크립트**
   - 프로젝트 디렉터리를 감지하여 적절한 하네스를 자동 생성하는 CLI 도구 제공.
