# Design System — 프로젝트 하네스

> **진입점 목차 문서입니다.** 세부 규칙은 `docs/ai/` 하위 문서를 로드하세요.

---

## 1. 프로젝트 스택 요약

- **Component Library**: React, TypeScript, Tailwind CSS
- **Documentation / Visual Testing**: Storybook 8+, Chromatic
- **Bundler & Build**: Vite / Rollup (`build:lib`, `build:css`)
- **Package Manager**: pnpm / yarn

---

## 2. 하네스 라우터

| 커맨드 / 의도 | 로드할 문서 | 기본 목표 |
|---|---|---|
| `/component` (신규 UI 컴포넌트) | `docs/ai/TOKEN_SPEC.md`, `docs/ai/STORYBOOK_RULES.md` | 토큰 기반 원자(Atomic) 컴포넌트 작성 및 Storybook 스토리 작성 |
| `/token` (디자인 토큰 추가/수정) | `docs/ai/TOKEN_SPEC.md` | Figma 스타일 동기화 및 CSS 변수/Tailwind config 반영 |
| `/storybook` (문서화 및 인터랙션) | `docs/ai/STORYBOOK_RULES.md` | Controls, Args, Docgen, 접근성(a11y) 검증 |

---

## 3. 골든 룰 (Golden Rules)

1. **무상태(Stateless) 원칙**: 디자인 시스템 컴포넌트는 비즈니스 로직이나 전역 상태를 포함하지 않으며, 제어 컴포넌트(Controlled Component) 형태로 props를 통해 동작해야 한다.
2. **모든 컴포넌트 1:1 Storybook 스토리 필수**: 컴포넌트 생성 시 반드시 대응되는 `*.stories.tsx`를 작성하고 기본/변형/비활성 상태를 망라해야 한다.
3. **독립 빌드 무결성**: 번들 산출물(`pnpm build:lib` 및 `pnpm build:css`)이 깨짐 없이 빌드되어야 한다.

---

## 4. 필수 검증 관문 (Verification Gate)

```bash
# 린트, 타입, 스토리북 빌드 검증
pnpm lint && pnpm type-check && pnpm build-storybook
```
