# Flutter & Riverpod — 프로젝트 하네스

> **진입점 목차 문서입니다.** 세부 규칙은 `docs/ai/` 하위 문서를 참조하세요.

---

## 1. 프로젝트 스택 요약

- **Framework**: Flutter (Dart 3+)
- **State Management**: Riverpod (`flutter_riverpod`, `riverpod_annotation`)
- **Routing**: `go_router`
- **Typography & Assets**: Pretendard, SVG Icons
- **Design Source**: Figma Token System

---

## 2. 하네스 라우터

| 커맨드 / 의도 | 로드할 가이드 문서 | 기본 목표 |
|---|---|---|
| `/screen` (화면 UI 개발) | `docs/ai/DESIGN_TOKENS.md`, `docs/ai/ARCHITECTURE.md` | `AppColors`, `AppTextStyles` 엄수, ConsumerStatefulWidget 또는 ConsumerWidget 분리 |
| `/state` (상태/프로바이더 연동) | `docs/ai/ARCHITECTURE.md` | Riverpod Notifier 작성 및 코드 제너레이션(`build_runner`) |
| `/analyze` (정적 분석 및 검증) | `docs/ai/ARCHITECTURE.md` | `flutter analyze` 0 issues 달성 |

---

## 3. 골든 룰 (Golden Rules)

1. **디자인 토큰 하드코딩 절대 금지**:
   - `Color(0xFF...)` 또는 `Colors.white` 사용 금지 → 반드시 `AppColors.*` 사용.
   - `TextStyle(...)` 인라인 정의 금지 → 반드시 `AppTextStyles.*` 사용.
2. **단일 검증 통과 원칙**:
   - 작업 완료 보고 전 **`flutter analyze`**를 실행하여 단 하나의 에러나 경고도 남아있지 않아야 한다.
3. **코드 제너레이션 동기화**:
   - Riverpod 또는 Freezed/JsonSerializable 수정 후 `dart run build_runner build --delete-conflicting-outputs` 실행.

---

## 4. 필수 검증 관문 (Verification Gate)

```bash
# 전체 정적 분석 (반드시 0 issues 확인)
flutter analyze
```
