# 05. 보안 샌드박스 및 격리 하네스 (Security & Sandbox Isolation)

AI 에이전트가 로컬 개발 환경에서 자율적으로 파일 생성, 수정, 터미널 명령을 수행할 때, **개발 대상 프로젝트 영역을 벗어나 시스템 주요 파일이나 민감한 자격 증명(Credentials)을 훼손하지 않도록 차단하는 안전 격리(Sandbox Isolation) 규격**을 정의합니다.

---

## 1. 3대 보안 위협 모델 (Threat Vectors)

1. **경로 탈출(Path Traversal / Escape)**:
   - 상대 경로(`../../`)나 심볼릭 링크를 통해 프로젝트 루트를 벗어나 `~/.ssh`, `~/.aws`, `/etc`, 시스템 루트 등에 접근하거나 덮어쓰는 사고.
2. **민감 자격 증명 유출 및 오염**:
   - `.env`, `.env.local`, API 키, 서비스 계정 JSON, OAuth 토큰 파일이 Git에 실수로 커밋되거나 프롬프트에 평문 주입되는 현상.
3. **파괴적 터미널 명령어 실행**:
   - 광범위한 삭제 명령어(`rm -rf *`, `rm -rf /`), 포트 강제 점유, 시스템 설정 변경(`sudo`, `chown`, 방화벽 변경) 실행.

---

## 2. 샌드박스 격리 5대 원칙 (Five Iron Rules)

```
┌─────────────────────────────────────────────────────────────┐
│  Rule 1. Strict Root Boundary: /Users/hhhk/dev/* ONLY       │
│  - 개발 작업은 지정된 dev 폴더 하위로만 엄격히 제한         │
├─────────────────────────────────────────────────────────────┤
│  Rule 2. Canonical Path Verification                        │
│  - realpath()를 통한 심볼릭 링크 및 상대 경로 탈출 원천 차단 │
├─────────────────────────────────────────────────────────────┤
│  Rule 3. Secret Shield & Gitignore Enforcement              │
│  - .env, id_rsa, *.pem, *.key, credentials 파일 수정/커밋 금지│
├─────────────────────────────────────────────────────────────┤
│  Rule 4. Command Whitelist & Destructive Guardrails         │
│  - git, pnpm, yarn, flutter, ./gradlew 등 안전 명령어만 허용│
├─────────────────────────────────────────────────────────────┤
│  Rule 5. Dry-Run & Audited Modification Logging             │
│  - 대규모 파일 변경 시 사전 영향도(Diff) 점검 필수          │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 구현 사양 (Implementation Spec)

### ① 정규화된 경로 검증 함수 (Python)
```python
def validate_safe_path(target_path, allowed_root="/Users/hhhk/dev"):
    canonical_root = os.path.realpath(allowed_root)
    canonical_target = os.path.realpath(target_path)
    
    # 루트 디렉터리와 대상 경로의 시작 위치 일치 검증
    if not canonical_target.startswith(canonical_root):
        raise SecurityException(
            f"Access Denied: Path '{canonical_target}' escapes allowed workspace '{canonical_root}'"
        )
    return canonical_target
```

### ② 민감 파일 차단 블랙리스트
```python
PROTECTED_PATTERNS = [
    ".env", ".env.*", "*.pem", "*.key", "id_rsa", "id_ed25519",
    "google_accounts.json", "oauth_creds.json", "credentials.json"
]
```

### ③ Git 안전 초기화 및 푸시 정책
- 신규 프로젝트 생성 시 즉시 기본 `.gitignore` 주입 (Node, Python, 환경변수, OS 파일 포함).
- 첫 커밋 전 `git status`로 `.env`나 키 파일 포함 여부 자동 감사.
- 원격 저장소(`git push`)는 사용자가 명시적으로 GitHub 리모트를 지정하고 승인했을 때만 연결.
