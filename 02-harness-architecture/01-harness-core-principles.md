# 01. 에이전트 하네스 핵심 원칙 (Harness Core Principles)

에이전트 하네스(Agent Harness)는 LLM 코딩 에이전트가 소프트웨어 프로젝트에서 **길을 잃지 않고, 프로젝트의 아키텍처 원칙을 준수하며, 자율적으로 검증을 완료**할 수 있도록 통제하는 구조적 가이드라인 체계입니다.

---

## 1. 하네스가 필요한 이유

LLM 기반 코딩 에이전트에게 발생하기 쉬운 3대 실패 모드:
1. **컨텍스트 표류 (Context Drift)**: 복잡한 리팩토링이나 기능 추가 시 프로젝트의 고유 설계 패턴(예: 계층 분리, 디자인 토큰)을 무시하고 일반적인 LLM 학습 데이터의 관성대로 코딩함.
2. **컨텍스트 과부하 (Context Bloat)**: 수천 줄의 가이드라인을 한 번에 읽으면 정작 중요한 규칙을 망각하거나(Attention dilution), 엉뚱한 규칙을 잘못 적용함.
3. **가짜 완료 보고 (Hallucinated Completion)**: 컴파일 에러나 런타임 오류, 린트 경고가 남아있음에도 "모든 작업이 완료되었습니다"라고 사용자에게 보고함.

하네스는 이 세 가지 실패 모드를 시스템적으로 차단합니다.

---

## 2. 하네스 5계층 아키텍처 (The 5-Layer Harness Architecture)

```
┌────────────────────────────────────────────────────────┐
│  Layer 1. Entrypoint (AGENTS.md)                       │
│  - 프로젝트 개요, Golden Rules, 검증 커맨드            │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 2. Intent Router                                │
│  - 작업 성격별 가이드 문서 맵핑 (/feat, /api, /refactor)│
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 3. Progressive Context (docs/ai/*)              │
│  - 필요할 때만 선별 로드되는 도메인 상세 지식          │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 4. Verification Gate (Deterministic Feedback)   │
│  - lint, typecheck, analyze, custom rule scripts       │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Layer 5. Tech Debt & Principles Monitoring            │
│  - 위반 사항 스캔 및 기술 부채 등록 원칙              │
└────────────────────────────────────────────────────────┘
```

### Layer 1. Entrypoint (진입점)
- 저장소 루트의 `AGENTS.md` 파일.
- **최대 100~150줄 내외로 압축 유지**.
- 프로젝트의 스택 요약과 하네스 라우터 표, 절대 위반 금지 규칙(Golden Rules)만 포함.

### Layer 2. Intent Router (의도 라우터)
- 사용자의 프롬프트 의도에 따라 에이전트가 어떤 문서나 스킬을 로드해야 하는지 명시.
- 예: 기능 추가 시 `docs/ai/ARCHITECTURE.md`, API 연동 시 `docs/ai/API.md`.

### Layer 3. Progressive Context (점진적 컨텍스트)
- `docs/ai/` 디렉터리에 모듈화된 상세 문서들.
- 단일 파일이 300줄을 넘지 않도록 작고 명확하게 유지.
- 예: `API.md`, `ARCHITECTURE.md`, `CONVENTIONS.md`, `TAILWIND_STYLING_GUIDE.md`.

### Layer 4. Verification Gate (검증 게이트)
- 에이전트가 "완료되었습니다"라고 말하기 전에 반드시 실행하고 출력이 0 오류여야 하는 결정론적(Deterministic) 커맨드.
- Flutter: `flutter analyze`
- Next.js/React: `pnpm lint && pnpm typecheck`
- React Native: `yarn release:check` 또는 검증 스크립트

### Layer 5. Tech Debt & Principles Monitoring (기술 부채 감시)
- 완벽하지 못한 임시 수정이나 추후 개선이 필요한 사항은 `docs/ai/TECH_DEBT.md`에 명시하도록 규칙화.
- 단순 구현을 넘어 지속 가능한 코드 품질을 강제.
