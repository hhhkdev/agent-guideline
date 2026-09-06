# React Native & Expo — 프로젝트 하네스

> **진입점 목차 문서입니다.** 상세 규칙은 `docs/ai/` 하위 문서를 로드하세요.

---

## 1. 프로젝트 스택 요약

- **Framework**: React Native, Expo (SDK 51+), Expo Router
- **Language**: TypeScript (Strict), Swift (Native Targets / Widgets)
- **Styling**: NativeWind (Tailwind CSS for RN) 또는 StyleSheet
- **State & Query**: TanStack Query, Zustand
- **Deployment**: EAS Build, EAS Update (OTA), Apple Developer Portal

---

## 2. 하네스 라우터

| 커맨드 / 의도 | 로드할 가이드 문서 | 기본 목표 |
|---|---|---|
| `/ui` (네이티브 UI/인터랙션) | `docs/ai/NATIVE_UI.md` | Safe Area, 키보드/한글 IME 처리, 모달/시트 제스처, 플랫폼별 UI |
| `/widget` (iOS 홈 위젯 개발) | `docs/ai/WIDGETS.md` | WidgetKit, App Group, Swift 타겟, shared Keychain/UserDefaults 연동 |
| `/release` (배포 및 OTA 관리) | `docs/ai/RELEASE_AND_OTA.md` | EAS Update 안전 잠금, 런타임 호환성, 네이티브 변경 검증 |
| `/refactor` (컴포넌트 분할) | `docs/ai/NATIVE_UI.md` | 화면 300줄/컴포넌트 350줄 상한 준수 및 리팩토링 |

---

## 3. 골든 룰 (Golden Rules)

1. **파일 길이 상한**:
   - Screen (`*-screen.tsx`): 권장 300줄, 최대 400줄
   - Component (`*.tsx`): 권장 350줄, 최대 500줄
   - Custom Hook (`use-*.ts`): 권장 150줄, 최대 250줄
2. **EAS OTA 안전 원칙**: 네이티브 의존성, entitlements, config plugin, `targets/` 파일 수정 시에는 **절대로 OTA(EAS Update)로 배포하지 않고 전체 네이티브 스토어 빌드를 수행**한다.
3. **네이티브 가정 금지**: React Native의 추상화가 네이티브(UIKit/Android)와 100% 동일하게 동작한다고 가정하지 말고 실제 시뮬레이터/기기 환경에서 검증한다.

---

## 4. 필수 검증 관문 (Verification Gate)

```bash
# 코드 린트
yarn lint

# 프로젝트 고유 규칙 검증 스크립트 실행
yarn release:check
```
