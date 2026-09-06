# {PROJECT_NAME} — 프로젝트 하네스 (진입점)

> **이 파일은 에이전트 진입점 및 목차입니다.** 상세 규칙은 `docs/ai/` 하위 문서를 참조하세요.
> 에이전트는 본 문서를 먼저 읽고, 작업 의도에 부합하는 문서를 선택적으로 로드하여 진행합니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| **프로젝트명** | {PROJECT_NAME} |
| **핵심 스택** | {PRIMARY_STACK} (예: Next.js 14, TypeScript, Tailwind CSS) |
| **상태 관리** | {STATE_MANAGEMENT} (예: TanStack Query, Zustand, Riverpod) |
| **진입 URL / 포트** | {DEV_SERVER_URL} (예: http://localhost:3000) |

---

## 2. 하네스 라우터 (의도별 파이프라인)

| 커맨드 / 의도 | 로드할 가이드 문서 | 기본 목표 |
|---|---|---|
| `feat:` (신규 기능 개발) | `docs/ai/ARCHITECTURE.md`, `docs/ai/CONVENTIONS.md` | 계층 구조(Screen → Component → Hook) 준수 및 기능 구현 |
| `api:` (API/통신 연동) | `docs/ai/API.md`, `docs/ai/CONVENTIONS.md` | API 클라이언트 + 쿼리 훅 + 타입 정의 동시 작성 및 캐시 정책 반영 |
| `refactor:` (구조 개선) | `docs/ai/ARCHITECTURE.md`, `docs/ai/TECH_DEBT.md` | 기존 동작 유지, 중복 제거, 컴포넌트 분할 및 성능 최적화 |
| `style:` (UI/스타일링) | `docs/ai/TAILWIND_STYLING_GUIDE.md` | 디자인 시스템 토큰 준수, 반응형 및 다크모드 대응 |
| `review:` (코드/품질 점검) | `docs/ai/TECH_DEBT.md` | Golden Rules 위반 스캔, 기술 부채 식별 및 보고 |

---

## 3. 골든 룰 (Golden Principles — 절대 위반 금지)

1. **디자인 토큰 엄수**: 임의의 Hex 컬러나 하드코딩된 크기 사용 금지. 디자인 시스템 토큰을 필히 사용할 것.
2. **파일 길이 상한 준수**: 화면 컴포넌트 300줄, 일반 컴포넌트 250줄, 훅/유틸 150줄 이하로 유지하고 초과 시 분할할 것.
3. **결정론적 검증 완수**: 작업 완료 보고 전 반드시 아래 검증 명령어를 실행하여 0 에러/0 경고를 확인할 것.

---

## 4. 필수 검증 관문 (Verification Gate)

```bash
# 모든 변경 작업 완료 후 반드시 실행할 명령어
{VERIFICATION_COMMAND}
# 예: pnpm lint && pnpm typecheck
# 예: flutter analyze
```
