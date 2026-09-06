# 05. 결정론적 검증 관문 (Deterministic Verification Gate)

에이전트는 작업을 완료했다고 선언하기 전에 반드시 다음 검증 관문을 실행하여 무결성을 입증해야 합니다.

## 1. 필수 검증 명령어

```bash
# 1. 하네스 CLI 구동 및 스킬 목록 무결성 검증
python3 tools/harness-cli.py list-skills

# 2. 파이썬 문법 및 린트 검증
python3 -m py_compile tools/agent-hub/server.py tools/harness-cli.py

# 3. 토큰 쿼터 및 실시간 2026 모델 감지 검증
curl -s http://127.0.0.1:8765/api/tokens | python3 -m json.tool
```

## 2. 완료 체크리스트
- [ ] 린트 및 파이썬 컴파일 에러 0건
- [ ] 스킬 목록이 깨짐 없이 출력됨
- [ ] 서버 엔드포인트 정상 응답 (HTTP 200)
- [ ] 모바일/태블릿/데스크톱 화면에서 반응형 레이아웃 깨짐 없음
