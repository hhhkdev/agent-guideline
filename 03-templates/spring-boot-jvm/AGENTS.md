# Spring Boot & JVM — 프로젝트 하네스

> **진입점 목차 문서입니다.** 상세 규칙은 `docs/ai/` 하위 문서를 로드하세요.

---

## 1. 프로젝트 스택 요약

- **Framework**: Spring Boot 3.x, Spring Data JPA, Spring Security
- **Language**: Java 17+ / Kotlin
- **Build Tool**: Gradle (`./gradlew`)
- **Database**: PostgreSQL / MySQL, Redis
- **Infra / Container**: Docker, Docker Compose

---

## 2. 하네스 라우터

| 커맨드 / 의도 | 로드할 문서 | 기본 목표 |
|---|---|---|
| `/endpoint` (API 추가) | `docs/ai/API_ARCHITECTURE.md` | Controller → Service → Repository 계층 작성 및 DTO 분리 |
| `/entity` (도메인/DB 변경) | `docs/ai/API_ARCHITECTURE.md` | JPA 엔티티, 연관관계 매핑, 마이그레이션(Flyway/Liquibase) |
| `/docker` (환경 구성) | `docs/ai/DOCKER_DEV.md` | Docker Compose 기반 로컬 DB/Redis 실행 및 검증 |

---

## 3. 골든 룰 (Golden Rules)

1. **엔티티 노출 금지**: JPA Entity를 Controller 응답으로 직접 반환하지 않는다. 반드시 별도 Response DTO로 변환하여 노출한다.
2. **N+1 문제 방지**: ManyToOne/OneToOne은 `FetchType.LAZY`를 기본으로 하고, 다량 조회 시 `fetch join` 또는 `@EntityGraph`를 적용한다.
3. **단위 테스트 통과**: 코드 수정 후 반드시 `./gradlew test --fail-fast`를 통과해야 한다.

---

## 4. 필수 검증 관문 (Verification Gate)

```bash
# 빌드 및 테스트 검증
./gradlew test --fail-fast
```
