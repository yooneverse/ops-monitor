# Docker Compose 설계서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | Docker Compose 설계서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | PostgreSQL 컨테이너 실행 구조와 향후 서비스 확장 방향 정의 |
| 현재 범위 | PostgreSQL 컨테이너 구성 및 FastAPI Health Check 연동 |
| 확장 범위 | FastAPI, Nginx 컨테이너 통합 구성 |

---

## 2. 구성 목적

Ops Monitor는 서비스 운영 환경에서 API 서버와 데이터베이스 상태를 확인하고, 장애 발생 시 복구 흐름을 검증하기 위한 미니 프로젝트이다.

Docker Compose는 PostgreSQL 데이터베이스를 컨테이너로 실행하고, 향후 FastAPI와 Nginx까지 동일한 실행 단위로 관리하기 위해 사용한다.

현재 단계에서는 PostgreSQL을 우선 컨테이너화하여 `/health` API의 DB 연결 상태 확인 기능을 검증한다.

---

## 3. 현재 구성 범위

현재 Docker Compose 구성 범위는 PostgreSQL 단일 컨테이너 실행이다.

FastAPI 애플리케이션은 로컬 환경에서 실행하며, PostgreSQL은 Docker 컨테이너로 실행한다.

```text
Local FastAPI
  ↓
localhost:5432
  ↓
PostgreSQL Container
```

| 구분 | 실행 위치 | 설명 |
|---|---|---|
| FastAPI | Local | `/health` API 제공 |
| PostgreSQL | Docker Container | DB 연결 상태 확인 대상 |
| Nginx | 예정 | Reverse Proxy 구성 예정 |

---

## 4. 서비스 구성

| Service | Image | Container Name | Role |
|---|---|---|---|
| db | postgres:16 | ops-monitor-db | PostgreSQL 데이터베이스 |

### db 서비스

`db` 서비스는 Ops Monitor의 데이터베이스 역할을 담당한다.

현재는 사용자, 로그, 장애 이력 테이블을 저장하기 위한 기반 데이터베이스로 사용되며, 우선적으로 `/health` API의 DB 연결 상태 확인 대상으로 활용한다.

---

## 5. Docker Compose 설정

현재 `docker-compose.yml`은 PostgreSQL 컨테이너 실행을 위한 `db` 서비스로 구성한다.

문서에는 계정명, 비밀번호, 데이터베이스명을 직접 작성하지 않고 환경변수로 분리한다.

```yaml
services:
  db:
    image: postgres:16
    container_name: ops-monitor-db
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 6. 설정 항목 상세

### 6.1 Image

| 항목 | 내용 |
|---|---|
| Image | postgres:16 |
| 선택 이유 | 안정적인 PostgreSQL 16 버전 기반으로 데이터베이스 컨테이너 구성 |

### 6.2 Container Name

| 항목 | 내용 |
|---|---|
| Container Name | ops-monitor-db |
| 설정 이유 | 컨테이너 상태 확인, 로그 조회, 중지 및 재시작 명령어 사용 시 식별 편의성 확보 |

### 6.3 Restart Policy

| 항목 | 내용 |
|---|---|
| Policy | always |
| 설정 이유 | 컨테이너 비정상 종료 시 재시작 가능성을 확보하기 위한 기본 설정 |

### 6.4 Environment Variables

| Variable | Example | Description |
|---|---|---|
| POSTGRES_USER | `<DB_USER>` | PostgreSQL 사용자명 |
| POSTGRES_PASSWORD | `<DB_PASSWORD>` | PostgreSQL 비밀번호 |
| POSTGRES_DB | `<DB_NAME>` | PostgreSQL 데이터베이스명 |

실제 값은 `.env` 파일에서 관리하며, `.env` 파일은 GitHub에 업로드하지 않는다.

### 6.5 Port Mapping

| Host Port | Container Port | Description |
|---|---|---|
| 5432 | 5432 | 로컬 FastAPI 서버에서 PostgreSQL 컨테이너 접근 |

현재 FastAPI가 로컬에서 실행되므로 `localhost:5432`를 통해 PostgreSQL 컨테이너에 접근한다.

### 6.6 Volume

| Volume | Mount Path | Description |
|---|---|---|
| postgres_data | /var/lib/postgresql/data | PostgreSQL 데이터 영속성 확보 |

PostgreSQL 데이터가 컨테이너 삭제와 분리되어 유지될 수 있도록 named volume을 사용한다.

---

## 7. FastAPI 연동 방식

FastAPI는 `.env` 파일의 `DATABASE_URL`을 통해 PostgreSQL에 연결한다.

현재는 FastAPI가 로컬에서 실행되므로 host를 `localhost`로 설정한다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>
```

`/health` API는 해당 환경변수를 사용해 DB 연결 가능 여부를 확인한다.

---

## 8. 보안 및 설정 관리 기준

민감정보가 GitHub에 노출되지 않도록 다음 기준을 적용한다.

| 항목 | 관리 방식 |
|---|---|
| 실제 DB 사용자명 | `.env`에서 관리 |
| 실제 DB 비밀번호 | `.env`에서 관리 |
| 실제 DB 이름 | `.env`에서 관리 |
| 문서 내 연결 문자열 | `<DB_USER>`, `<DB_PASSWORD>`, `<DB_NAME>` 형태로 마스킹 |
| 예시 환경변수 | `.env.example`에 샘플 값으로 작성 |
| 실제 환경변수 파일 | `.gitignore`를 통해 Git 추적 제외 |

`.gitignore`에는 다음 설정을 포함한다.

```gitignore
.env
.env.*
!.env.example
```

---

## 9. 실행 및 점검 명령어

### 9.1 PostgreSQL 컨테이너 실행

```bash
docker compose up -d
```

### 9.2 실행 중인 컨테이너 확인

```bash
docker ps
```

### 9.3 PostgreSQL 로그 확인

```bash
docker logs ops-monitor-db
```

### 9.4 PostgreSQL 컨테이너 중지

```bash
docker stop ops-monitor-db
```

### 9.5 PostgreSQL 컨테이너 재시작

```bash
docker start ops-monitor-db
```

---

## 10. Health Check 검증 결과

### 10.1 PostgreSQL 실행 전

PostgreSQL이 실행되지 않은 상태에서는 `/health` API에서 DB 상태가 `disconnected`로 반환된다.

```json
{
  "status": "disconnected",
  "message": "Database connection failed"
}
```

### 10.2 PostgreSQL 실행 후

PostgreSQL 컨테이너 실행 후에는 `/health` API에서 DB 상태가 `connected`로 반환된다.

```json
{
  "status": "connected",
  "message": "Database connection successful"
}
```

### 10.3 장애 및 복구 확인

PostgreSQL 컨테이너를 중지하면 `/health` API에서 `disconnected` 상태가 반환된다.

컨테이너를 재시작하면 `/health` API에서 다시 `connected` 상태가 반환된다.

이를 통해 DB 장애 감지와 복구 확인 흐름을 검증했다.

---

## 11. 현재 완료 상태

| 항목 | 상태 |
|---|---|
| PostgreSQL 컨테이너 구성 | 완료 |
| Docker Compose 실행 확인 | 완료 |
| 로컬 FastAPI와 PostgreSQL 연결 확인 | 완료 |
| `/health` API DB 상태 응답 확인 | 완료 |
| PostgreSQL 컨테이너 중지 시 장애 감지 확인 | 완료 |
| PostgreSQL 컨테이너 재시작 시 복구 확인 | 완료 |
| FastAPI 컨테이너화 | 예정 |
| Nginx Reverse Proxy 구성 | 예정 |

---

## 12. 확장 설계

향후 FastAPI와 Nginx를 Docker Compose 구성에 포함하여 다음 구조로 확장한다.

```text
Client
  ↓
Nginx Container
  ↓
FastAPI Container
  ↓
PostgreSQL Container
```

확장 후에는 FastAPI 컨테이너가 Docker 내부 네트워크를 통해 PostgreSQL 컨테이너에 접근한다.

이 경우 `DATABASE_URL`의 host는 `localhost`가 아니라 Compose 서비스명인 `db`로 변경한다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
```

---

## 13. 설계 고려사항

| 항목 | 고려 내용 |
|---|---|
| 환경 분리 | DB 접속 정보는 `.env`와 `.env.example`로 분리 |
| 민감정보 보호 | 문서와 README에는 실제 계정명, 비밀번호, 연결 문자열을 직접 작성하지 않음 |
| 데이터 유지 | PostgreSQL 데이터는 named volume으로 관리 |
| 장애 확인 | 컨테이너 중지 상태를 `/health` API에서 감지 |
| 확장성 | FastAPI, Nginx 컨테이너 추가를 고려한 Compose 구조 유지 |
| 운영 기록 | 실행, 장애, 복구 결과는 `operation-log.md`에 기록 |

---

## 14. 다음 작업

- FastAPI 애플리케이션 Dockerfile 작성
- FastAPI 서비스를 Docker Compose에 추가
- Compose 내부 네트워크 기준으로 `DATABASE_URL` 변경
- Nginx Reverse Proxy 컨테이너 구성
- Nginx를 통한 `/health` 요청 흐름 확인