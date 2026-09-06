---
name: product-planning-and-prd
description: Formulate lean product specifications, PRD (Product Requirements Document), user personas, user journey maps, and feature prioritization (RICE/MoSCoW) for web and mobile products before engineering.
---

# Product Planning & PRD Generator

기획 단계에서 개발 에이전트와 엔지니어가 한 치의 오해 없이 기능 목적과 요구사항을 파악할 수 있도록 구조화된 제품 기획 명세서(PRD)를 도출합니다.

## 1. 기획 수립 4단계 파이프라인

```
[1단계: 문제 정의 및 고객 가치]
  - Who: 타깃 사용자 페르소나
  - Problem: 사용자가 겪는 핵심 결핍(Pain Point)
  - Solution: 본 기능이 제공하는 해결 가치 (Value Proposition)
       │
       ▼
[2단계: 린 캔버스 및 유저 저니 맵]
  - 유저 진입(Trigger) → 핵심 행동(Core Action) → 리워드(Reward) 플로우 다이어그램
       │
       ▼
[3단계: 기능 우선순위화 (RICE / MoSCoW)]
  - Must have (P0), Should have (P1), Could have (P2), Won't have (P3)
       │
       ▼
[4단계: 수용 기준 (Acceptance Criteria)]
  - Given-When-Then 규격으로 엔지니어링 및 QA 검증 기준 명문화
```

## 2. 표준 PRD 템플릿 규격

```markdown
# [PRD] {기능명 / 서비스명}

## 1. 개요 및 배경
- **목적**:
- **성공 지표(KPI)**: DAU +15%, 전환율(CVR) 3.5% 달성 등

## 2. 타깃 페르소나
- **이름/유형**: 취준생 개발자 민수 (26세)
- **Pain Point**: 매일 커밋을 유지하고 싶지만 동기부여가 부족하고 잔디가 끊기면 포기함.

## 3. 핵심 유저 플로우 (Mermaid)
```mermaid
graph LR
  A[푸시 알림 수신] --> B[위젯에서 오늘의 커밋 확인]
  B --> C[앱 진입 및 1D1S 챌린지 달성]
  C --> D[스트릭 배지 획득 및 공유]
```

## 4. 기능 명세 및 수용 기준 (Acceptance Criteria)

### Feature 1: 홈 위젯 투두 체크
- **Given**: 사용자가 로그인 상태이며 오늘의 미완료 투두가 1개 이상 존재할 때
- **When**: iOS 홈 위젯에서 투두 완료 버튼을 탭하면
- **Then**:
  1. API `PATCH /v1/todos/{id}` 요청이 발송된다.
  2. 위젯 캐시가 즉시 낙관적 업데이트(Optimistic Update)된다.
  3. 실패 시 App Group의 직전 상태로 롤백된다.
```
