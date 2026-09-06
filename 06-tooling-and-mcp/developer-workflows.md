# 02. 실무 개발자 워크플로우 (Multi-Agent Developer Workflows)

현대 AI 보조 개발에서는 특정 툴 하나에 종속되기보다, 작업의 성격(탐색, 구현, 리팩토링, 검증)에 따라 최적의 도구를 교차 활용하는 전략이 가장 높은 생산성을 냅니다.

---

## 1. 도구별 추천 역할 분담 (Tool Matrix)

| 단계 | 작업 내용 | 추천 도구 | 선정 사유 |
|---|---|---|---|
| **1. 탐색 및 계획 (Plan)** | 대규모 리팩토링, 아키텍처 구상, 문서 분석 | **Antigravity IDE** | Planning Mode, Mermaid 다이어그램, 아티팩트 가시화 우수 |
| **2. 고속 터미널 구현 (Exec)** | 기능 추가, API 연동, 컴포넌트 개발 | **Claude Code** | 빠른 CLI 반응성, 슬래시 커맨드 라우터(`/ods-*`)와 긴밀한 통합 |
| **3. 규칙 기반 자율 실행 (Rules)** | 반복적인 리베이스, 기계적 린트 수정, 배치 | **Codex CLI** | `prefix_rule` 기반 무인 승인 실행, 백그라운드 데몬 구동 |
| **4. 복합 멀티모달 / UI 검증** | 브라우저 기반 렌더링, 시각적 피드백 | **Antigravity** | 내장 브라우저 레코딩, Generative UI 위젯 |

---

## 2. 터미널 권한 관리 모범 사례

반복적인 `y/n` 확인 질문에 방해받지 않으면서도 시스템 보안을 해치지 않는 설정법:

### Codex CLI (`~/.codex/rules/default.rules`)
자주 실행하는 안전한 읽기 및 검증 명령어를 사전 승인:
```text
prefix_rule(pattern=["git", "status"], decision="allow")
prefix_rule(pattern=["git", "diff"], decision="allow")
prefix_rule(pattern=["pnpm", "lint"], decision="allow")
prefix_rule(pattern=["pnpm", "test"], decision="allow")
prefix_rule(pattern=["flutter", "analyze"], decision="allow")
```

### Git Rebase 안전 자동화
```text
prefix_rule(pattern=["/bin/zsh", "-lc", "GIT_EDITOR=true git rebase --continue"], decision="allow")
```
