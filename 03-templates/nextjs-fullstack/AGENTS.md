# Next.js Fullstack — 프로젝트 하네스

> **진입점 목차 문서입니다.** 세부 규칙은 `docs/ai/` 하위 문서를 로드하세요.

---

## 1. 프로젝트 스택 요약

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript (Strict Mode)
- **Styling**: Tailwind CSS, Class Variance Authority (cva), tailwind-merge, clsx
- **Data Fetching & State**: TanStack Query (v5), Axios / Fetch API, Zustand
- **Quality & Linting**: ESLint, Prettier, Knip, TypeScript compiler (`tsc --noEmit`)

---

## 2. 하네스 라우터

| 커맨드 / 작업 의도 | 로드할 문서 | 가이드 요약 |
|---|---|---|
| `/feat` (신규 기능 개발) | `docs/ai/ARCHITECTURE.md`, `docs/ai/CONVENTIONS.md` | `app/` 라우트 → `_components/` → `hooks/` 계층 분리 엄수 |
| `/api` (API 연동/통신) | `docs/ai/API.md` | DTO 타입 정의, Axios 호출 함수, TanStack Query 훅 및 캐시 무효화 |
| `/style` (스타일링/UI) | `docs/ai/TAILWIND_STYLING_GUIDE.md` | 토큰 컬러 준수, 임의의 arbitrary value(`[#123456]`) 금지 |
| `/refactor` (리팩토링) | `docs/ai/ARCHITECTURE.md`, `docs/ai/TECH_DEBT.md` | 파일 길이 분할(300줄 상한), 중복 로직 훅 추출 |
| `/review` (코드 리뷰) | `docs/ai/TECH_DEBT.md` | 골든 룰 위반 점검, 미사용 코드(Knip) 점검 |

---

## 3. 골든 룰 (Golden Rules)

1. **클라이언트 컴포넌트 최소화**: 기본적으로 Server Component로 유지하고, 인터랙션/상태가 필요한 리프(Leaf) 노드만 `'use client'` 지시자를 사용한다.
2. **단방향 의존성 계층**: `Page/Layout` → `Containers/Widgets` → `Presentational Components` → `Hooks/Utils`. 상위 계층이 하위 계층을 import하되 역방향 참조를 엄격히 금지한다.
3. **타입 안전성 (Zero `any`)**: 모든 API 응답과 폼 상태는 명시적 TypeScript interface 또는 type으로 정의한다.

---

## 4. 검증 관문 (Verification Gate)

작업 완료 전 다음 명령어를 순서대로 실행하고 모든 오류를 해결해야 합니다.

```bash
# 린트 및 미사용 파일/익스포트 점검
pnpm lint
pnpm knip

# 타입 검증 (빌드 없이 신속 확인)
pnpm tsc --noEmit
```
