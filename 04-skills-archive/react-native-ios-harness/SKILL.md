---
name: react-native-ios-harness
description: Implement, debug, review, and verify iOS-first UI, native widgets (Swift), and EAS deployment behavior in React Native and Expo projects. Use when handling safe areas, iOS modals/sheets, Korean IME keyboard handling, WidgetKit integration, EAS OTA release checks, or Swift target configurations.
---

# React Native & iOS Native Harness

## 1. 런타임 및 환경 파악
1. 프로젝트 루트의 `AGENTS.md` 및 `package.json`에서 React Native, Expo SDK, React 버전을 확인합니다.
2. `app.config.ts` 또는 `app.json`의 플러그인 설정 및 iOS 번들 식별자(Bundle ID), 타겟 설정을 점검합니다.
3. 네이티브 코드 변경(`targets/`, `ios/`, config plugins) 여부를 파악합니다.

## 2. iOS UI 및 사용자 경험 원칙
- **Safe Area**: `react-native-safe-area-context`의 insets을 사용하여 Dynamic Island, 노치, 하단 인디케이터 여백을 동적으로 확보합니다.
- **키보드 회피**: iOS `KeyboardAvoidingView` 동작 시 헤더 오프셋을 계산하고, 한글 자모 조합이 끊기지 않도록 `onChangeText` 제어를 유지합니다.
- **레이아웃 여백**: 위젯 및 컴포넌트 내부의 행 간격(Line spacing)과 상/하단 여백이 시각적으로 균등하도록 고정 pt 단위를 적용합니다.

## 3. iOS 홈 위젯 (WidgetKit / Swift) 규칙
- 소스코드 원본은 `targets/home-widget/`에 위치하며, 빌드로 생성된 `ios/` 파일을 수동 편집하지 않습니다.
- Shared Keychain을 사용하여 민감한 토큰(Access Token)을 공유하고, App Group UserDefaults에는 일반 설정값만 보관합니다.
- Pretendard 등 커스텀 폰트는 위젯 타겟의 `assets`에 별도 배치하고 `Info.plist`에 명시합니다.

## 4. EAS Update (OTA) 안전 체크
- 네이티브 의존성, Swift 타겟, 권한 설정이 변경된 경우 절대 OTA(`eas update`)를 실행하지 않고 스토어 바이너리 빌드를 요구합니다.
- 변경 후 `yarn release:check` 또는 린트 명령어로 무결성을 확인합니다.
