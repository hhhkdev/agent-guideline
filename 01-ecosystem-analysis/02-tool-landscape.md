# 02. 크로스 AI 에이전트 도구 지형도 및 통합 전략 (Cross-Tool Landscape)

현재 실무에서 활용 중인 AI 코딩 도구들(Claude Code, Codex CLI, Google Antigravity, Cursor, GitHub Copilot)의 특성과 설정 파일 스펙을 비교하고, 중복 설정 없이 하나의 아키텍처로 모든 툴을 커버하는 통합 하네스 전략을 정의합니다.

---

## 1. 도구별 스펙 비교

| 구분 | Claude Code (Anthropic) | Codex CLI (OpenAI) | Google Antigravity | Cursor |
|---|---|---|---|---|
| **실행 환경** | 터미널 CLI (Agentic REPL) | 터미널 CLI (TUI/Daemon) | 풀스택 IDE (VSCode 기반) | IDE (VSCode 포크) |
| **기본 진입점 파일** | `CLAUDE.md` | `AGENTS.md`, `.codex/rules` | `AGENTS.md`, Skills | `.cursorrules`, `.cursor/rules/*` |
| **확장 체계** | Slash commands, Plugins, MCP | Skills (`SKILL.md`), Rules | Skills (`SKILL.md`), MCP, Subagents | Rules, `.cursorrules`, MCP |
| **도구 실행 권한 제어** | 대화형 프롬프트 승인 | `prefix_rule(pattern, decision)` | 샌드박스 + `BypassSandbox` 승인 | Yolo/Confirm 모드 |
| **컨텍스트 주입 방식** | 세션 시작 시 `CLAUDE.md` 인덱싱 | 작업 시작 시 `AGENTS.md` 인덱싱 | 작업별 에이전트/스킬 컨텍스트 주입 | 파일별 룰 매칭 또는 전역 주입 |

---

## 2. 도구 간 상호 운용성(Interoperability)의 핵심 난제

1. **설정 파일 파편화**: 
   - Claude Code는 `CLAUDE.md`를 우선 탐색
   - Codex와 Antigravity는 `AGENTS.md`를 표준으로 권장
   - Cursor는 `.cursorrules` 또는 `.cursor/rules/*.mdc`를 요구
2. **명령어 패턴 차이**:
   - Claude Code: 대화형 슬래시 커맨드 (`/ods-feature`)
   - Codex: 규칙 기반 실행(`default.rules`) 및 스킬 호출
   - Antigravity: 서브에이전트(`invoke_subagent`), 스킬 폴더 시스템
3. **토큰 낭비와 컨텍스트 압박**:
   - 프로젝트 전체 규칙(아키텍처, 컨벤션, 배포규칙, 테스트규칙)을 한 파일에 모두 넣으면 진입 시점부터 수천 토큰을 소모하며 모델의 주의력(Attention)이 분산됨.

---

## 3. 단일 진입점 통합 전략 (Single Source of Truth)

우리는 **`AGENTS.md`를 단일 진입점(SSOT)**으로 삼고, 타 도구들은 심볼릭 링크나 얇은 어댑터(Thin Wrapper)를 통해 참조하도록 구성합니다.

```
[Repository Root]
├── AGENTS.md                  ← [SSOT] 마스터 하네스 라우터
├── CLAUDE.md                  ← AGENTS.md 참조 어댑터 (or Symlink)
├── .cursorrules               ← AGENTS.md 참조 어댑터 (or Symlink)
├── docs/
│   └── ai/                    ← 도메인별 분할 상세 문서 (On-demand)
│       ├── ARCHITECTURE.md
│       ├── CONVENTIONS.md
│       ├── API.md
│       └── WORKFLOWS.md
└── .skills/ (or ~/.codex/skills, ~/.gemini/antigravity/skills)
    └── [skill-name]/SKILL.md  ← 스킬 정의 (표준 규격 준수)
```

### 어댑터 구성 예시

**`CLAUDE.md` 파일:**
```markdown
# Claude Code Entrypoint

> 이 프로젝트는 `AGENTS.md`를 단일 진입점(SSOT)으로 사용합니다.
> 모든 작업 전 반드시 `AGENTS.md`의 규칙과 라우터를 준수하세요.

@AGENTS.md
```

**`AGENTS.md`의 표준 역할:**
- 프로젝트 핵심 스택 및 한 줄 요약
- 하네스 커맨드/라우터 표 (의도별 가이드 문서 맵핑)
- 절대 깨지면 안 되는 3~5대 원칙 (Golden Principles)
- 작업 종료 시 필수 실행할 단일 검증 명령어 (Verification Command)
