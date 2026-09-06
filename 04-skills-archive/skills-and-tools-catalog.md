# 📚 AI 에이전트 스킬 & 개발 툴 종합 카탈로그 (Skills & Tools Catalog)

> 실무 개발자들이 검증한 핵심 스킬(Skills)과 AI 도구들의 특성, 장단점 비교, 커뮤니티 평판 및 최적 활용 시나리오를 집대성한 가이드입니다.

---

## 1. AI 코딩 CLI & 툴 비교 매트릭스 (Which Tool When?)

| 도구 | 주 용도 | 강점 (Pros) | 약점 (Cons) | 커뮤니티 평판 & 팁 |
|---|---|---|---|---|
| **Claude Code** | 터미널 대화형 구현 & 리팩토링 | • 가장 정교한 프론트엔드 코드 생성<br>• `CLAUDE.md` 자동 학습<br>• 프롬프트 캐싱으로 빠른 응답 | • 5시간 롤링 윈도우 한도 존재<br>• 세션당 토큰 급증 주의 | ⭐⭐⭐⭐⭐ (4.9/5)<br>"단일 세션에서 복잡한 Next.js/React 기능 구현 시 현재 1위. 5시간 제한만 조심하면 됨." |
| **Google Antigravity** | IDE 통합 풀스택 & 브라우저 검증 | • Subagent 오케스트레이션 기본 탑재<br>• 대규모 컨텍스트(100만+)<br>• 내장 브라우저 레코딩 & Generative UI | • IDE 단위 무거움<br>• CLI 대비 속도 편차 | ⭐⭐⭐⭐☆ (4.7/5)<br>"아키텍처 설계, 다이어그램 시각화, 서브에이전트 협업 시 최강의 환경." |
| **OpenAI Codex CLI** | 규칙 기반 무인 실행 & 백그라운드 | • `prefix_rule`로 무인 승인 루프 가능<br>• 안정적인 o1/o3-mini 추론<br>• 빠른 Git/CI 처리 | • 복합 UI 레이아웃 직관성 보통<br>• 3시간 메시지 한도 | ⭐⭐⭐⭐☆ (4.5/5)<br>"리베이스, 린트 오류 해결, 도커 빌드 등 기계적 반복 작업 자동화에 최적." |
| **Cursor** | 실시간 인라인 자동완성 & 페어링 | • Copilot보다 압도적인 다중 파일 수정<br>• `.cursorrules`로 빠른 컨텍스트 주입 | • 복잡한 오케스트레이션 기능 부족 | ⭐⭐⭐⭐☆ (4.6/5)<br>"타이핑하는 순간 바로 코드를 뽑아주는 인라인 페어 프로그래밍에 최고." |

---

## 2. 필수 추천 스킬(Skills) 카탈로그

### ① UI / 프론트엔드 스킬

#### 1. `figma-implement-design` (Figma 1:1 코드 변환)
- **적용 도구**: Antigravity, Codex, Claude (Figma MCP 연동)
- **주요 기능**: Figma URL 또는 데스크톱 선택 노드로부터 디자인 토큰, Flexbox/AutoLayout, Tailwind 클래스 100% 일치 코드 생성.
- **개발자 의견**: "눈대중으로 마진 맞추던 시간을 90% 줄여줌. `app_colors.dart`나 Tailwind config와 연동하면 완벽함."
- **설치 명령어**: `python3 tools/harness-cli.py install-skill figma-implement-design`

#### 2. `flutter-design-token-guardian` (플러터 디자인 무결성)
- **적용 도구**: 전체 공통
- **주요 기능**: `Color(0x...)` 하드코딩 즉시 차단, `AppColors`/`AppTextStyles` 강제, `flutter analyze` 0 issues 완료 검증.
- **개발자 의견**: "에이전트가 제멋대로 인라인 스타일 쓰던 습관을 100% 교정해줌."

#### 3. `modern-dashboard-design-system` (다크 글래스모피즘 UI)
- **적용 도구**: React, Next.js, Web
- **주요 기능**: Linear/Vercel 스타일의 앰비언트 글로우, 서큘러 SVG 게이지, 반응형 마이크로 그리드 토큰 제공.

---

### ② 백엔드 & 풀스택 계약 스킬

#### 4. `tanstack-query-contract-generator` (API 3종 세트 일괄 생성)
- **적용 도구**: Next.js, React, Vite
- **주요 기능**: API 스펙으로부터 DTO 타입 정의, Axios 호출 함수, TanStack Query v5 훅, Query Key Factory, 캐시 무효화 정책 동시 생성.
- **개발자 의견**: "프론트/백엔드 통신 보일러플레이트 코딩 시간을 5분에서 10초로 단축."

#### 5. `spring-boot-jpa-architect` (Spring Boot 계층 무결성)
- **적용 도구**: Java, Kotlin, Spring Boot
- **주요 기능**: Entity 직접 노출 방지(Record DTO 강제), Lazy Loading N+1 방어, Gradle Test-driven 검증.

---

### ③ 배포 & Git 안전 스킬

#### 6. `react-native-ios-harness` (iOS 홈위젯 & EAS 배포 잠금)
- **적용 도구**: React Native, Expo, Swift
- **주요 기능**: Safe Area, 10pt 위젯 줄간격, Shared Keychain 보안, 네이티브 변경 시 EAS OTA 금지 정책 강제.

#### 7. `git-rebase-conflict-resolver` (비파괴적 안전 리베이스)
- **적용 도구**: 전체 공통
- **주요 기능**: 충돌 마커(`<<<<<<<`) 자동 감사, ours/theirs 안전 선택, 충돌 해결 후 검증 테스트 통과 시에만 continue.
