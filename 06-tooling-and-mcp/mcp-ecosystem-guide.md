# 01. MCP (Model Context Protocol) 생태계 가이드

MCP(Model Context Protocol)는 에이전트가 외부 도구, 데이터베이스, 디자인 툴, 브라우저와 안전하고 표준화된 방식으로 소통할 수 있게 해주는 개방형 표준 프로토콜입니다.

---

## 1. 프로젝트 맞춤 추천 MCP 서버 목록

| MCP 서버 | 주요 기능 | 사용자 프로젝트 활용처 |
|---|---|---|
| **Figma MCP** | Figma 파일, 프레임, 디자인 토큰, 컴포넌트 구조 실시간 조회 | `CampusYA-FE`, `1D1S-design-system`, `hivcd-*` 토큰 동기화 |
| **GitHub MCP** | PR 생성, 이슈 조회, 브랜치 관리, 리뷰 코멘트 작성 | 1D1S, teumteum 배포 및 릴리즈 관리 |
| **SQLite / Postgres MCP** | 로컬 데이터베이스 스키마 조회, 쿼리 테스트 | `hivcd-backend`, `please-2000won-backend` DB 점검 |
| **Filesystem MCP** | 보안 샌드박스 내 안전한 다중 디렉터리 파일 읽기/쓰기 | 대규모 프로젝트 간 파일 참조 |
| **Memory / Knowledge Graph** | 장기 컨텍스트 기억, 사용자 선호도 및 아키텍처 결정 기록 | 다중 세션에 걸친 프로젝트 지식 유지 |

---

## 2. MCP 설정 방법

### ① Antigravity (`~/.gemini/config/mcp_config.json`)
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-figma"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your_figma_token"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token"
      }
    }
  }
}
```

### ② Claude Code (`claude mcp add`)
```bash
claude mcp add figma npx -y @modelcontextprotocol/server-figma
claude mcp add github npx -y @modelcontextprotocol/server-github
```
