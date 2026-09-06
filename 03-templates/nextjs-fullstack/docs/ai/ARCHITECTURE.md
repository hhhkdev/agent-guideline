# Next.js 아키텍처 및 디렉터리 가이드라인

## 1. 디렉터리 구조 원칙

```
src/
├── app/                      # Next.js App Router (Routing, Layout, Page)
│   ├── (auth)/               # Route Groups (괄호 폴더)
│   ├── dashboard/
│   │   ├── _components/      # 해당 페이지 전용 컴포넌트 (비공개)
│   │   ├── _hooks/           # 해당 페이지 전용 훅
│   │   └── page.tsx          # 얇은 진입점 페이지 (300줄 미만)
│   ├── layout.tsx
│   └── globals.css
├── components/               # 2개 이상의 도메인에서 공유되는 공통 컴포넌트
│   ├── ui/                   # Button, Input, Modal 등 디자인 시스템 기본 컴포넌트
│   └── common/               # Header, Footer, Navigation 등
├── hooks/                    # 전역 공통 훅
├── services/                 # API 호출 함수 및 데이터 계층
│   ├── client.ts             # Axios/Fetch 인스턴스 (인터셉터, 에러 핸들링)
│   └── [domain]/             # 도메인별 API 함수 및 타입
├── stores/                   # 클라이언트 전역 상태 (Zustand 등)
├── types/                    # 전역 공용 타입 정의
└── utils/                    # 순수 유틸리티 함수 (포맷팅, 날짜 계산 등)
```

## 2. 컴포넌트 설계 계층

1. **Page (`page.tsx`)**:
   - 데이터 페칭(Server Component) 또는 최상위 뷰 조립만 담당.
   - 비즈니스 로직을 직접 품지 않고 서브 컴포넌트로 위임.
2. **Container/Section (`_components/DashboardWidget.tsx`)**:
   - 도메인 단위의 비즈니스 로직과 UI 블록을 연결.
3. **Presentational UI (`components/ui/*`)**:
   - 상태가 없고 props에 의해서만 렌더링되는 재사용 가능한 순수 컴포넌트.
