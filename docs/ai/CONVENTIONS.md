# 04. 개발 규칙 및 컨벤션 (Conventions)

## 1. 코드 및 스크립트 작성 규칙
- **Zero External Dependencies**: `tools/` 내 파이썬 스크립트는 외부 `pip install` 없이 Python 3 표준 라이브러리(`urllib`, `http.server`, `sqlite3`, `json`, `subprocess`)만으로 구동 가능해야 합니다.
- **Mac / Linux 네이티브 호환**: 모든 셸 명령어 및 스크립트는 macOS zsh 환경 및 Linux bash 환경에서 오류 없이 실행되어야 합니다.
- **철저한 샌드박스 보안**: 로컬 파일 시스템 탐색이나 작업은 반드시 사용자 지정 샌드박스 경로(`/Users/hhhk/dev`) 내부로 한정되며, 상위 경로(`..`) 탈출 공격을 차단합니다.

## 2. 스킬 규격 (Skill Spec)
- 모든 스킬은 `04-skills-archive/<skill-name>/SKILL.md` 형식으로 저장합니다.
- 상단에 반드시 YAML Frontmatter (`name`, `description`)를 포함해야 합니다.

## 3. 커밋 메시지 규칙 (Conventional Commits)
- `feat:` 신규 하네스 템플릿, 스킬, CLI 기능 추가
- `fix:` UI 버그 수정, 쿼터 계산 오류 수정, 레이아웃 깨짐 개선
- `docs:` 가이드라인 문서 작성 및 보완
- `refactor:` 코드 구조 개선 및 하네스 아키텍처 정밀화
