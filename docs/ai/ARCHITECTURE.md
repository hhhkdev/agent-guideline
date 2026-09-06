# 03. 아키텍처 가이드 (Architecture Guide)

## 1. 저장소 구성 (Repository Topology)

```
agent-guideline/
├── AGENTS.md                  # Layer 1: 단일 진입점 (SSOT)
├── CLAUDE.md                  # Multi-Tool 어댑터 (Claude Code 전용)
├── docs/ai/                   # Layer 3: 점진적 컨텍스트 (Progressive Context)
├── 01-ecosystem-analysis/     # 도구별 생태계 및 토큰 특성 분석
├── 02-harness-architecture/   # 하네스 5계층 및 컨텍스트 엔지니어링 원칙
├── 03-templates/              # 스택별 하네스 템플릿 (Next.js, RN, Flutter, Spring, etc.)
├── 04-skills-archive/         # 표준 규격 스킬 아카이브 (YAML Frontmatter)
├── 05-prompt-engineering/     # 역할 정의 및 메타 프롬프트 라이브러리
├── 06-tooling-and-mcp/        # CLI 도구 및 MCP 통합 명세
├── tools/                     # 자동화 도구 및 런타임 스크립트
│   ├── harness-cli.py         # 하네스 코어 CLI (스캔, 주입, 서브에이전트, 스킬 목록)
│   ├── agent-hub/             # 통합 웹 대시보드 서버 (Python HTTPServer + WebUI)
│   ├── desktop-app/           # 네이티브 macOS WebKit 데스크톱 앱 (Swift)
│   └── status-bar/            # 맥북 상단 메뉴바 쿼터 모니터 (Swift 데몬)
└── start.sh                   # 올인원 원클릭 런처
```

## 2. 5계층 하네스 동작 방식
1. **Entrypoint (`AGENTS.md`)**: 에이전트가 가장 먼저 읽는 100~150줄 분량의 압축 진입점.
2. **Intent Router (`ROUTER.md`)**: 사용자의 작업 요청 키워드에 따라 읽어야 할 세부 문서 지정.
3. **Progressive Context (`docs/ai/`)**: 작업에 직접 필요한 도메인 지식만 부분 로드하여 컨텍스트 과부하 방지.
4. **Verification Gate (`VERIFICATION.md`)**: 에이전트 완료 전 반드시 실행해야 하는 결정론적 검증 체계.
5. **Tech Debt & Monitoring (`TECH_DEBT.md`)**: 구현 중 발견된 타협점이나 개선 요구사항을 공식 기록.
