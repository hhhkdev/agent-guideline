# EAS Update (OTA) 및 릴리즈 안전 정책

## 1. OTA 가능 여부 판별 매트릭스

| 변경 사항 | EAS Update (OTA) 가능 여부 | 필수 작업 |
|---|---|---|
| 순수 JS/TS 비즈니스 로직, 스타일 | ✅ 가능 | `eas update --branch production` |
| 신규 네이티브 라이브러리 추가 | ❌ 절대 불가 (앱 크래시 유발) | 버전 번호 올림 후 스토어 신규 빌드 |
| `app.config.ts`의 권한/플러그인 변경 | ❌ 절대 불가 | Expo Prebuild 및 스토어 빌드 |
| `targets/` (위젯, 익스텐션) 수정 | ❌ 절대 불가 | Xcode 네이티브 빌드 |
| 폰트 추가 및 네이티브 에셋 등록 | ❌ 절대 불가 | 스토어 바이너리 갱신 필요 |

## 2. 배포 전 점검 절차

1. `git diff`를 통해 `package.json`, `podfile`, `targets/` 등의 네이티브 파일 변경 유무 확인.
2. `yarn release:check` 스크립트 실행으로 클린 상태 확인.
3. staging 환경에 먼저 배포하여 실제 바이너리 기기에서 검증 완료 후 production 승격.
