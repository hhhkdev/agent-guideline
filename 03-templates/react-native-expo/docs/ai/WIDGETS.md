# iOS 홈 위젯 (WidgetKit & Swift) 연동 가이드

## 1. 아키텍처 원칙

- **소스코드 원본**: `targets/home-widget/` 디렉터리가 원본이며, `ios/` 내부에 생성된 파일은 빌드 산출물로 취급합니다.
- **데이터 공유 메커니즘**:
  - 보안 토큰(Access/Refresh Token): **Shared Keychain** (`keychain-access-groups` 사용)에만 저장.
  - 비보안 설정 및 캐시 데이터: **App Group UserDefaults** 사용.
- **Expo Prebuild 주의사항**:
  - `@bacons/apple-targets` 사용 시 기존 타겟 위에 덮어쓰기 prebuild를 실행하지 않고, 필요 시 `npx expo prebuild --platform ios --clean`으로 새로 생성합니다.

## 2. 폰트 및 디자인 준수

- React Native 번들에 포함된 커스텀 폰트(Pretendard 등)는 별도 프로세스인 위젯에서 자동 공유되지 않으므로, `targets/home-widget/assets`에 폰트 파일을 직접 등록하고 익스텐션의 `Info.plist`에 추가해야 합니다.
- 위젯 패밀리(`systemSmall`, `systemMedium`, `systemLarge`)별 패딩과 줄 간격(예: 10pt)을 철저히 준수합니다.
