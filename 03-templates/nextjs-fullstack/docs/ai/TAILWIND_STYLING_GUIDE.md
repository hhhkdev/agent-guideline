# Tailwind CSS 스타일링 가이드

## 1. 디자인 토큰 준수 원칙

- **임의의 Hex/RGB 직접 입력 금지**: `bg-[#1A73E8]` 같은 하드코딩 대신 설정된 테마 토큰(`bg-primary`, `bg-neutral-100` 등) 사용.
- **클래스 병합**: 조건부 스타일링은 `clsx`와 `tailwind-merge`를 결합한 `cn()` 유틸리티 함수를 반드시 사용.

```tsx
// ✅ Good
import { cn } from '@/utils/cn';

export const Button = ({ className, variant = 'primary', ...props }: ButtonProps) => {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-lg px-4 py-2 font-medium transition-colors',
        variant === 'primary' && 'bg-primary text-white hover:bg-primary-dark',
        variant === 'outline' && 'border border-neutral-300 text-neutral-800 hover:bg-neutral-50',
        className
      )}
      {...props}
    />
  );
};
```

## 2. 반응형 및 모바일 퍼스트

- 기본 클래스는 모바일 기준이며, 미디어 쿼리 접두사(`sm:`, `md:`, `lg:`, `xl:`)를 통해 점진적으로 확장합니다.
- `flex flex-col md:flex-row`
