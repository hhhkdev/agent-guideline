# Next.js & TypeScript 코딩 컨벤션

## 1. 네이밍 규칙

- **컴포넌트 파일 및 이름**: PascalCase (예: `UserProfileCard.tsx`, `UserProfileCard`)
- **페이지 및 라우트 파일**: kebab-case 또는 소문자 (예: `page.tsx`, `layout.tsx`)
- **훅 파일 및 이름**: camelCase, `use` 접두사 (예: `useUserProfile.ts`, `useUserProfile`)
- **상수**: UPPER_SNAKE_CASE (예: `DEFAULT_PAGE_SIZE = 20`)
- **타입/인터페이스**: PascalCase (DTO의 경우 접미사 `Dto`, 요청 객체는 `Request` 명시)

## 2. 모범 사례

1. **Early Return 패턴 사용**: 중첩된 if-else를 피하고 빠른 반환으로 가독성 유지.
2. **Boolean 네이밍**: `is`, `has`, `should`, `can` 접두사 사용 (예: `isLoading`, `hasPermission`).
3. **Props 전달**: 불필요한 prop drilling 대신 적절한 컴포지션(children 패턴) 또는 Context/Zustand 활용.
4. **구조 분해 할당(Destructuring)**: 컴포넌트 인자에서 즉시 구조 분해.
