# Flutter 클린 아키텍처 및 Riverpod 패턴

## 1. 계층 구조 (Layering)

```
lib/
├── core/
│   ├── theme/
│   │   ├── app_colors.dart
│   │   └── app_text_styles.dart
│   ├── network/
│   └── utils/
├── features/
│   └── [feature_name]/
│       ├── data/             # API DTO, Repository 구현체, Data Source
│       ├── domain/           # Entity, Repository 인터페이스
│       └── presentation/     # UI
│           ├── screens/      # Screen 위젯
│           ├── widgets/      # Screen 내부 전용 위젯
│           └── controllers/  # Riverpod Notifier / State
```

## 2. Riverpod 권장 패턴

- 비동기 데이터는 `AsyncNotifier` 또는 `@riverpod Future<T>`를 사용합니다.
- UI에서는 `ref.watch(provider).when(data: ..., loading: ..., error: ...)`를 통해 모든 상태를 명시적으로 핸들링합니다.
- `ref.read`는 이벤트 콜백(onPressed 등) 내부에서만 사용하고, `build()` 내부에서는 항상 `ref.watch`를 사용합니다.
