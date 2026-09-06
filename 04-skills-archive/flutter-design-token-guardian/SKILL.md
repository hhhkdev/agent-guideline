---
name: flutter-design-token-guardian
description: Enforce design token usage, clean architecture, and strict zero-warning verification in Flutter projects. Use when creating or modifying Flutter widgets, styling, theme colors, typography, or when fixing issues reported by flutter analyze.
---

# Flutter Design Token Guardian

## 1. 디자인 토큰 검증 원칙
Flutter 위젯 코드 작성 시 색상이나 폰트 스타일을 하드코딩하는 것을 엄격히 방지합니다.

- **색상**:
  - `Color(0x...)`, `Colors.white`, `Colors.black` 금지.
  - 반드시 `AppColors.*` (예: `AppColors.neutral0`, `AppColors.blue500`, `AppColors.textMain`) 사용.
  - 신규 색상이 필요하면 `lib/core/theme/app_colors.dart`에 먼저 정의.
- **텍스트 스타일**:
  - 인라인 `TextStyle(fontSize: ...)` 금지.
  - 반드시 `AppTextStyles.*` (예: `AppTextStyles.h2`, `AppTextStyles.body3`) 사용.
  - 자간/행간/폰트패밀리(Pretendard)가 일괄 적용된 토큰 활용.

## 2. Riverpod 상태 관리 준수
- 비즈니스 로직과 API 페칭은 Notifier에 위임하고 위젯 `build()`는 순수 렌더링에 집중.
- 비동기 상태는 `AsyncValue` (`.when()`)로 빠짐없이 처리.

## 3. 검증 관문 실행
작업 완료 보고 전 반드시 아래 명령어를 실행하여 이슈가 0개임을 확인합니다.

```bash
flutter analyze
```
에러뿐만 아니라 모든 warning과 lint 경고를 해결해야 작업이 완료된 것으로 간주합니다.
