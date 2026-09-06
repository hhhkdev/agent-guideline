# Spring Boot 계층형 아키텍처 가이드

## 1. 계층별 책임

```
src/main/java/com/example/domain/
├── controller/        # HTTP 요청/응답 매핑, 검증(@Valid), Swagger 문서화
├── dto/               # Request, Response DTO (Record 사용 권장)
├── service/           # 비즈니스 로직, 트랜잭션(@Transactional)
├── repository/        # Spring Data JPA 인터페이스 및 Querydsl 쿼리
└── entity/            # JPA 엔티티 정의 (BaseTimeEntity 상속)
```

## 2. DTO & Record 활용

Java 14+ Record를 활용하여 불변 DTO를 선언합니다.

```java
public record CreateUserRequest(
    @NotBlank(message = "이름은 필수입니다.") String name,
    @Email(message = "올바른 이메일 형식이 아닙니다.") String email
) {}
```
