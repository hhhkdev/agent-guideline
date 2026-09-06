# Docker 및 로컬 개발 환경 가이드

## 1. Docker Compose 로컬 인프라 구동

로컬 개발에 필요한 데이터베이스와 캐시는 `docker-compose.yml`을 통해 띄웁니다.

```bash
# 로컬 인프라 백그라운드 구동
docker compose up -d

# 실행 상태 점검
docker compose ps

# 로그 모니터링
docker compose logs -f
```

## 2. Spring Boot 프로파일 분리

- `application-local.yml`: 로컬 Docker 인프라 연동 (`localhost:5432` 등)
- `application-test.yml`: H2 인메모리 또는 Testcontainers 연동
- `application-prod.yml`: 실서버 환경 변수 바인딩
