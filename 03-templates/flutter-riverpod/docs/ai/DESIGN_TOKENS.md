# Flutter 디자인 토큰 가이드

## 1. 컬러 토큰 매핑 규칙

```dart
// ❌ 금지 (Hardcoded colors)
color: Color(0xFF1780FF)
color: Colors.white
color: Color(0xFF191F28)

// ✅ 올바른 사용법
color: AppColors.blue500        // 메인 브랜드 컬러
color: AppColors.neutral0        // White 대체
color: AppColors.neutral900      // Black 대체
color: AppColors.textMain        // 기본 텍스트
color: AppColors.neutral200      // 구분선 / 테두리
```

- 신규 색상이 필요한 경우 임의 추가하지 않고 Figma 디자인 토큰 명칭을 확인한 후 `app_colors.dart`에 정의 후 사용합니다.

---

## 2. 타이포그래피 토큰 매핑 규칙

```dart
// ❌ 금지
style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)

// ✅ 올바른 사용법
style: AppTextStyles.h2          // 대제목
style: AppTextStyles.h4          // 섹션 헤더
style: AppTextStyles.body3       // 본문 텍스트
style: AppTextStyles.caption1     // 보조 설명
```
