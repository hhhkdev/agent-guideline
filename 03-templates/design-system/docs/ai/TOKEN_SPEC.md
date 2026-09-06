# 디자인 토큰 규격 (TOKEN_SPEC.md)

## 1. 3계층 토큰 아키텍처

```
[글로벌 토큰 (Global Tokens)]  예: Blue-500 = #1780FF, Gray-900 = #191F28
               │
               ▼
[시맨틱 토큰 (Semantic Tokens)] 예: Color-Primary = {Global.Blue-500}, Text-Main = {Global.Gray-900}
               │
               ▼
[컴포넌트 토큰 (Component)]    예: Button-Primary-Bg = {Semantic.Color-Primary}
```

- 클라이언트 애플리케이션 및 컴포넌트에서는 가급적 **시맨틱 토큰(Semantic Tokens)**을 직접 참조하여, 다크모드 및 테마 변경 시 일관된 전환을 지원합니다.
