# 06. 서브에이전트 CLI 조작 및 관리 가이드 (Subagent CLI Operations)

서브에이전트를 이론으로만 아는 것을 넘어, **터미널 명령어(CLI) 및 도구 호출 레벨에서 직접 띄우고, 상태를 감시하며, 취소 및 정리하는 실무 운용법**을 다룹니다.

---

## 1. 서브에이전트 생명주기 (Lifecycle States)

```
[호출 발주]  invoke_subagent / spawn
     │
     ▼
[RUNNING] ─── (작업 수행 중: 툴 호출 및 코드 수정)
     │
     ├─────► [WAITING_FOR_INPUT] ─── (부모의 추가 지시 대기)
     │
     ├─────► [IDLE] ──────────────── (태스크 완료 후 유휴 대기)
     │
     └─────► [KILL / DONE] ────────── (manage_subagents(kill) 로 프로세스/워크스페이스 회수)
```

---

## 2. 도구별 서브에이전트 제어 명령어

### ① Google Antigravity 도구 세트

| 작업 | 도구 호출 명세 | 설명 |
|---|---|---|
| **서브에이전트 생성** | `invoke_subagent(Subagents=[{"TypeName": "self", "Role": "QA", "Prompt": "..."}])` | 역할을 부여하여 백그라운드 분기 실행 |
| **활성 서브에이전트 조회** | `manage_subagents(Action="list")` | 실행 중인 ID, 역할, live state JSON 반환 |
| **단일 서브에이전트 종료** | `manage_subagents(Action="kill", ConversationIds=["conv-123"])` | 특정 에이전트 및 하위 워크스페이스 정리 |
| **전체 서브에이전트 일괄 종료** | `manage_subagents(Action="kill_all")` | 모든 자식 프로세스 즉시 중단 |
| **대화 및 지시문 전송** | `send_message(Recipient="conv-123", Message="...")` | 실행 중인 서브에이전트에게 추가 컨텍스트 주입 |

### ② Claude Code 터미널 환경
```bash
# 백그라운드 서브 태스크 발주
claude "docs/ai/ARCHITECTURE.md를 참고하여 auth 훅을 리팩토링하라" &

# 백그라운드 세션 프로세스 점검
ps aux | grep claude

# 서브 세션 강제 중단
kill -9 [PID]
```

### ③ Agent Hub CLI (`harness-cli.py subagent`)

```bash
# 1. 활성 서브에이전트 목록 및 상태 조회
python3 tools/harness-cli.py subagent list

# 2. 서브에이전트 계층 트리 구조 확인
python3 tools/harness-cli.py subagent tree

# 3. 새로운 서브에이전트 발주
python3 tools/harness-cli.py subagent dispatch \
  --role "Flutter Token Guardian" \
  --project CampusYA-FE \
  --prompt "하드코딩된 색상을 AppColors로 전수 치환하라"

# 4. 특정 서브에이전트 종료
python3 tools/harness-cli.py subagent kill [SUBAGENT_ID]
```

---

## 3. 서브에이전트 관리 시 필수 골든 룰

1. **좀비 프로세스 방지 (No Orphan Agents)**: 부모 작업이 완료되었거나 중단될 때는 반드시 `kill_all`을 호출하여 백그라운드 토큰 소모를 방지합니다.
2. **반응형 대기 (No Polling)**: 서브에이전트 상태를 루프(`while true; do check; done`)로 확인하지 마십시오. 이벤트 기반 Reactive Wakeup을 활용합니다.
3. **독립 워크스페이스 격리**: 서브에이전트 발주 시 `Workspace: 'branch'`를 사용하여 메인 작업 트리가 중간 파일로 오염되지 않도록 합니다.
