# AI Context Index — Agent Guideline

> 본 문서는 LLM 코딩 에이전트(Claude Code, Antigravity, OpenAI Codex 등)가 점진적으로 필요한 컨텍스트를 선별 로드할 수 있도록 돕는 인덱스 문서입니다.

---

## 1. 하네스 5계층 라우팅

| 레이어 | 문서 경로 | 핵심 내용 |
|---|---|---|
| **Layer 1. 진입점** | `AGENTS.md` | 저장소 요약, 골든 룰 3원칙, 필수 검증 관문 |
| **Layer 2. 의도 라우터** | `docs/ai/ROUTER.md` | 커맨드별 맵핑 및 가이드 디렉터리 연계 |
| **Layer 3. 아키텍처** | `docs/ai/ARCHITECTURE.md` | 허브 구조, 하네스 5계층 상세, 컨트롤 서버/CLI 스펙 |
| **Layer 3. 규칙/컨벤션** | `docs/ai/CONVENTIONS.md` | 코드 스타일, 커밋 컨벤션, 스킬 작성 규격 |
| **Layer 4. 검증 관문** | `docs/ai/VERIFICATION.md` | 결정론적 검증 명령어, 린트 및 무결성 테스트 |
| **Layer 5. 기술 부채** | `docs/ai/TECH_DEBT.md` | 개선 필요 항목, 보안/샌드박스 백로그 |

---

## 2. 세부 가이드라인 챕터

- `01-ecosystem-analysis/`: 도구별(Claude, Gemini, Codex, Cursor) 특성 및 토큰 이코노미
- `02-harness-architecture/`: 하네스 5계층 아키텍처 및 서브에이전트 오케스트레이션
- `03-templates/`: 신규 프로젝트 스택별 하네스 템플릿 아카이브
- `04-skills-archive/`: Antigravity/Codex 표준 규격의 재사용 가능 스킬셋
- `05-prompt-engineering/`: 메타 프롬프트, 역할 정의 프롬프트 템플릿
- `06-tooling-and-mcp/`: CLI 유틸리티 및 MCP 연동 명세서
