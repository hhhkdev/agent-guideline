# React Native iOS 네이티브 UI 및 인터랙션 가이드

## 1. Safe Area 및 레이아웃 규칙

- `react-native-safe-area-context`의 `useSafeAreaInsets()`를 사용하여 동적 노치, Dynamic Island, 하단 홈 인디케이터 여백을 처리합니다.
- 하드코딩된 패딩(예: `paddingTop: 44`)은 기기별 화면 크기 차이로 인해 금지합니다.

## 2. 키보드 회피 및 한글 IME 처리

- iOS에서는 `KeyboardAvoidingView`의 `behavior="padding"`을 기본으로 사용하되, 헤더 높이를 고려한 `keyboardVerticalOffset`을 설정합니다.
- 한글 입력 시 조합 문자 상태에서 조합 중인 글자가 유실되지 않도록 `onChangeText`와 제어 컴포넌트(Controlled Component) 상태 업데이트 타이밍을 주의합니다.

## 3. 제스처 및 바텀 시트 (Gorhom BottomSheet 등)

- 스크롤 뷰와 제스처 핸들러의 충돌을 방지하기 위해 `BottomSheetScrollView` 또는 `gestureHandlerRootHOC`를 올바른 계층에 감쌉니다.
- iOS 특유의 Rubber-banding(바운스) 효과를 유지하면서 모달 닫기 제스처와 조화되도록 구성합니다.
