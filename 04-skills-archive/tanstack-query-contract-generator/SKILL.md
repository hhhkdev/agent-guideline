---
name: tanstack-query-contract-generator
description: Generate end-to-end type-safe API client functions, TanStack Query v5 hooks, Query Key factories, and cache invalidation policies from API specifications or Swagger schemas in Next.js / React projects.
---

# TanStack Query Contract Generator

## 1. 아키텍처 원칙
API 통신 코드를 생성할 때 반드시 3종 세트(Type, API Client, Query Hook)를 하나의 응집된 단위로 생성합니다.

```
src/services/[domain]/
├── types.ts      # DTO 및 Request/Response 인터페이스
├── api.ts        # Axios/Fetch 기반 순수 API 호출 함수
└── queries.ts    # queryKey factory, useQuery, useMutation 훅
```

## 2. 작성 템플릿 규칙
1. **Query Key Factory**:
   - 도메인 최상위 키와 하위 키를 배열 튜플로 정의 (`as const`).
2. **Optimistic Update 또는 Cache Invalidation**:
   - `mutation` 성공 시 관련 `queryKey`를 자동으로 무효화(`invalidateQueries`)하거나 캐시를 즉시 갱신(`setQueryData`).
3. **에러 타입 지정**:
   - 공통 API 에러 인터페이스(`ApiErrorResponse`)를 활용하여 제네릭 에러 핸들링 지원.
