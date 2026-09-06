# Claude Code Guide — {PROJECT_NAME}

> 이 프로젝트는 `AGENTS.md`를 단일 진입점(SSOT)으로 사용합니다.
> 모든 작업 전 반드시 `AGENTS.md`의 규칙과 라우터를 준수하세요.

@AGENTS.md

## Primary Commands

```bash
# Development
{DEV_COMMAND}       # e.g., pnpm dev, yarn start, flutter run

# Verification (Must pass with 0 issues before reporting done)
{VERIFY_COMMAND}    # e.g., pnpm lint && pnpm tsc --noEmit, flutter analyze

# Build & Test
{BUILD_COMMAND}     # e.g., pnpm build, flutter build
{TEST_COMMAND}      # e.g., pnpm test, flutter test
```

## Workflows & Session Rules

1. 작업을 시작할 때 요구사항에 부합하는 `docs/ai/*.md` 문서를 먼저 읽고 진행합니다.
2. 코드를 수정한 후에는 반드시 `{VERIFY_COMMAND}`를 터미널에서 실행하여 통과 여부를 검증합니다.
3. 수정 과정에서 발생한 잔여 기술 부채나 미완성 로직은 `docs/ai/TECH_DEBT.md`에 기록합니다.
