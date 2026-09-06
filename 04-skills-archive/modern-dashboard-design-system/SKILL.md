---
name: modern-dashboard-design-system
description: Apply high-end modern developer tool aesthetics (Linear/Vercel style), dark glassmorphism, responsive data layouts, circular quota gauges, and micro-interactions to web dashboards and control panels.
---

# Modern Dashboard Design System

초보적인 투박한 UI를 탈피하여, Linear, Vercel, Raycast 수준의 **세련된 다크 테마 엔지니어링 대시보드**를 구현하기 위한 디자인 토큰 및 인터랙션 규격입니다.

---

## 1. 비주얼 룩앤필 원칙 (Aesthetic Principles)

1. **초미세 경계선 (Subtle Borders)**:
   - 강한 회색 테두리 대신 `border border-white/[0.08]` 또는 `border-slate-800/80` 사용.
   - 다크 서피스 위에 미세한 음영과 레이어 깊이(Layer Depth) 형성.
2. **글래스모피즘 & 블러 (Glassmorphism)**:
   - `bg-slate-900/60 backdrop-blur-xl` 조합으로 하부 캔버스와 배경이 은은하게 비치도록 구성.
3. **라디얼 앰비언트 글로우 (Ambient Glow)**:
   - 중요 카드나 활성 상태 뒤에 `bg-indigo-500/10 blur-3xl`의 은은한 오로라 광원 배치.
4. **타이포그래피 위계 (Typography Hierarchy)**:
   - 숫자/지표: `JetBrains Mono` 또는 `ui-monospace` (tabular-nums 강제)
   - 제목/본문: `Pretendard` 또는 `Inter` (자간 `-0.02em` 타이트 조절)

---

## 2. 컬러 팔레트 및 시맨틱 토큰

```css
/* Backgrounds */
--bg-canvas: #06080e;        /* 최심층 백그라운드 */
--bg-surface: #0b0f19;       /* 기본 카드 서피스 */
--bg-elevated: #111726;      /* 팝오버 및 인스펙터 서피스 */

/* Accents */
--accent-primary: #6366f1;   /* Indigo 500 */
--accent-glow: #818cf8;      /* Indigo 400 */
--accent-emerald: #10b981;   /* Emerald 500 (정상/완료) */
--accent-amber: #f59e0b;     /* Amber 500 (주의/스캔 필요) */
--accent-rose: #f43f5e;      /* Rose 500 (위험/초과) */

/* Borders */
--border-subtle: rgba(255, 255, 255, 0.07);
--border-highlight: rgba(99, 102, 241, 0.35);
```

---

## 3. 구독 플랜 할당량(Quota) 게이지 설계

5시간 롤링 윈도우 및 주간 사용량을 한눈에 인지할 수 있는 시각화 컴포넌트:

```html
<!-- Circular / Radial Quota Gauge Component -->
<div class="relative w-24 h-24 flex items-center justify-center">
  <svg class="w-full h-full -rotate-90" viewBox="0 0 36 36">
    <!-- Background Track -->
    <path class="text-slate-800" stroke-width="3" stroke="currentColor" fill="none"
      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
    <!-- Progress Indicator -->
    <path class="text-indigo-500 transition-all duration-1000 ease-out" stroke-width="3"
      stroke-dasharray="78, 100" stroke-linecap="round" stroke="currentColor" fill="none"
      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
  </svg>
  <div class="absolute text-center">
    <span class="text-base font-bold font-mono text-white">78%</span>
    <span class="block text-[9px] text-slate-400">5h Window</span>
  </div>
</div>
```

---

## 4. 완벽한 반응형(Responsive) 레이아웃 규격

1. **모바일 (< 640px)**:
   - 1열 스택 그리드 (`grid-cols-1`)
   - 탭 네비게이션: 가로 스크롤 가능한 칩 형태 (`overflow-x-auto flex-nowrap`)
   - 데이터 테이블: 카드 뷰 또는 가로 스와이프 (`overflow-x-auto`) 지원
2. **태블릿 (640px ~ 1024px)**:
   - 2열 그리드 (`md:grid-cols-2`)
   - 메인 대시보드와 인스펙터 분할 레이아웃
3. **데스크톱 (> 1024px)**:
   - 3열 또는 12열 마이크로 그리드 (`lg:grid-cols-3`, `xl:grid-cols-12`)
