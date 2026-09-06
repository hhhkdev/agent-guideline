# Agent Guideline — 프로젝트 하네스 (진입점)

> 본 저장소는 AI 에이전트 하네스, 프롬프트, 스킬셋, 컨텍스트 엔지니어링 가이드라인을 아카이빙하고 관리하는 허브입니다.
> 에이전트는 본 문서를 먼저 읽고, 작업 의도에 부합하는 문서를 로드하여 진행합니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| **프로젝트명** | `agent-guideline` |
| **목적** | AI 보조 개발을 위한 하네스 템플릿, 스킬 아카이브, 컨텍스트 엔지니어링 가이드라인 구축 |
| **도구** | Python 3 (CLI 스크립트), Markdown (가이드 및 스펙), Antigravity/Codex/Claude 스킬 규격 |

---

## 2. 하네스 라우터

| 커맨드 / 의도 | 로드할 문서 및 디렉터리 | 기본 목표 |
|---|---|---|
| `/analysis` (프로젝트 분석) | `01-ecosystem-analysis/` | 기술 스택 분석, 도구별 특성 파악 |
| `/harness` (하네스 아키텍처) | `02-harness-architecture/` | 하네스 5계층, 컨텍스트 예산 배분, 결정론적 검증 체계 고도화 |
| `/template` (템플릿 확장) | `03-templates/` | 신규 스택별 템플릿 추가 및 기존 템플릿 개선 |
| `/skill` (신규 스킬 추가) | `04-skills-archive/` | Antigravity/Codex 표준 규격의 `SKILL.md` 작성 및 등록 |
| `/prompt` (프롬프트 관리) | `05-prompt-engineering/` | 메타 프롬프트 및 역할 정의 프롬프트 갱신 |
| `/tool` (CLI / MCP 확장) | `06-tooling-and-mcp/`, `tools/` | `harness-cli.py` 기능 추가 및 MCP 가이드 갱신 |

---

## 3. 골든 룰 (Golden Rules)

1. **단일 진입점 압축 원칙**: `AGENTS.md`는 항상 100~150줄 내외로 간결하게 유지하며, 세부 지식은 반드시 하위 문서로 분리한다.
2. **실무 코드 기반 구체성**: 가이드 문서는 모호한 조언이 아닌, 실제 프로젝트 경로, 명령어, 검증 코드 스니펫을 포함해야 한다.
3. **스킬 표준 규격 준수**: 스킬은 상단 YAML Frontmatter (`name`, `description`)와 구체적인 실행 절차를 필히 갖추어야 한다.

---

## 4. 필수 검증 관문 (Verification Gate)

```bash
# harness-cli 구동 및 스킬 목록 정합성 검증
python3 tools/harness-cli.py list-skills
```
