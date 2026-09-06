# 03. 결정론적 검증 하네스 (Deterministic Verification Harness)

에이전트가 "완료되었습니다"라고 답변할 때, 실제로는 타입 오류나 린트 경고, 혹은 아키텍처 규칙 위반이 숨어있는 경우가 빈번합니다. 이를 방지하기 위해 **기계적이고 결정론적인(Deterministic) 검증 커맨드**를 하네스의 필수 관문(Gatekeeper)으로 설정합니다.

---

## 1. 검증 하네스의 기본 구조

```
[코드 수정 완료]
       │
       ▼
[1단계: 문법 및 타입 체크 (Type Safety)]
       │   └── 에러 발생 시 즉시 자체 수정 (Self-Healing Loop)
       ▼
[2단계: 린트 및 스타일 체크 (Linter & Formatter)]
       │   └── 미사용 변수, 잘못된 임포트, 규칙 위반 자동 수정
       ▼
[3단계: 프로젝트 고유 도메인 규칙 검증 (Custom Rules Script)]
       │   └── 예: 디자인 토큰 하드코딩 검사, 파일 길이 초과 검사
       ▼
[4단계: 단위 및 통합 테스트 (Automated Tests)]
       │   └── 핵심 비즈니스 로직 통과 확인
       ▼
[최종 검증 완료 보고 (Verified Done)]
```

---

## 2. 스택별 필수 검증 명령어 세트

### ① Flutter (`CampusYA-FE` 스타일)
```bash
# 수정 후 단일 파일 또는 전체 프로젝트 분석
flutter analyze

# 규칙: 결과에 0 issues가 나올 때까지 보고를 종료하지 않는다.
```

### ② Next.js / TypeScript (`1D1S-client`, `hivcd-frontend` 스타일)
```bash
# 린트 및 미사용 코드(Knip) 점검
pnpm lint
pnpm knip # 또는 npm run knip

# 타입 검증 (빌드 없이 빠른 체크)
pnpm tsc --noEmit
```

### ③ React Native / Expo (`teumteum-mobile` 스타일)
```bash
# 린트 및 커스텀 비즈니스 규칙 검증
yarn lint
node scripts/verify-todo-ordering-rules.mjs

# 배포 전 안전 검증
yarn release:check --mode ota --base release/x.y.z --require-clean
```

### ④ Spring Boot / Gradle (`hivcd-backend`, `please-2000won-backend`)
```bash
# 빌드 및 단위 테스트 검증
./gradlew test --fail-fast
./gradlew check
```

---

## 3. 커스텀 규칙 검증 스크립트 작성 가이드

린터(ESLint, Dart Analyzer 등)로 잡아내기 힘든 프로젝트 고유 규칙은 간단한 Node.js나 Python 스크립트로 작성하여 검증 루프에 포함시킵니다.

### 예시: 디자인 토큰 하드코딩 방지 검사기 (`scripts/verify-tokens.mjs`)
```javascript
import fs from 'fs';
import path from 'path';

// Hex 코드(#FFFFFF 등)가 직접 쓰인 컴포넌트 탐지
const HEX_REGEX = /#(?:[0-9a-fA-F]{3}){1,2}\b/g;

function scanDirectory(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !['node_modules', '.next'].includes(entry.name)) {
      scanDirectory(fullPath);
    } else if (entry.isFile() && /\.(tsx|jsx|dart)$/.test(entry.name)) {
      const content = fs.readFileSync(fullPath, 'utf8');
      const matches = content.match(HEX_REGEX);
      if (matches && !fullPath.includes('token') && !fullPath.includes('color')) {
        console.error(`❌ 하드코딩된 색상 발견 (${fullPath}):`, matches);
        process.exit(1);
      }
    }
  }
}

scanDirectory('src');
console.log('✅ 모든 디자인 토큰 검증 통과');
```
