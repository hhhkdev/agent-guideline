---
name: git-rebase-conflict-resolver
description: Safely inspect, resolve, and advance git rebase conflicts across complex frontend and backend repositories without losing upstream changes or destroying working trees.
---

# Git Rebase Conflict Resolver

## 1. 충돌 분석 절차
1. `git status`로 현재 `rebase in progress` 상태 및 충돌 파일(Unmerged paths) 목록 확인.
2. 각 충돌 파일에서 충돌 마커(`<<<<<<<`, `=======`, `>>>>>>>`)의 위치와 내용을 검사.
3. 충돌의 본질이 단순 임포트 충돌인지, 상위 브랜치의 파괴적 변경(Breaking change)인지 판단.

## 2. 해결 및 진행 규칙
- 충돌 마커가 제거되었는지 정규식으로 검증:
  ```bash
  rg -n "^(<<<<<<<|=======|>>>>>>>)" [file_path]
  ```
- 양자택일(ours vs theirs)이 명확한 경우:
  ```bash
  git checkout --ours [file_path]   # 또는 --theirs
  ```
- 수동 병합 완료 후 스테이징 및 리베이스 계속:
  ```bash
  git add [file_path]
  GIT_EDITOR=true git rebase --continue
  ```
- 검증: 리베이스 완료 후 프로젝트 검증 명령어(린트/타입체크)를 실행하여 병합 후 빌드 깨짐이 없는지 확인.
