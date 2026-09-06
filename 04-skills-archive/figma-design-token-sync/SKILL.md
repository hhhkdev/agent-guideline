---
name: figma-design-token-sync
description: Translate Figma variables, color styles, and typography tokens extracted via Figma MCP or plugin into code tokens for Tailwind CSS, CSS Variables, or Flutter AppColors.
---

# Figma Design Token Sync

## 1. 토큰 변환 파이프라인
1. Figma MCP 또는 플러그인 JSON 덤프에서 디자인 토큰 구조 추출.
2. 토큰 명칭을 케밥케이스(CSS/Tailwind) 및 카멜케이스(Flutter Dart)로 정규화.
3. CSS Variables (`globals.css`), Tailwind Theme 확장 (`tailwind.config.ts`), Flutter `app_colors.dart`에 자동 갱신.

## 2. 변환 규칙
- **Color**: Hex8/RGBA 값을 Hex6 또는 CSS `rgba()`로 변환.
- **Typography**:
  - `fontFamily`: Pretendard 우선 매핑.
  - `fontSize`, `lineHeight`, `fontWeight`, `letterSpacing` 묶음 객체 생성.
- **Elevation / Shadow**: Box-shadow 규격에 맞게 변환.
