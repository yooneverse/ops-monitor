# Docker Compose 설계서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | Docker Compose 설계서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 운영용 Compose 구성과 서비스 간 연결 구조 정의 |
| 현재 범위 | Nginx, FastAPI, PostgreSQL, 데모 메모 서비스 통합 구성 |
| 확장 범위 | 배포 자동화와 운영 보조 서비스 추가 |

---

## 2. 구성 목적

Ops Monitor는 서비스 운영 환경에서 API 서버와 데이터베이스 상태를 확인하고, 장애 발생 시 복구 흐름을 검증하기 위한 미니 프로젝트이다.

Docker Compose는 운영 화면, API, 데이터베이스, 데모 서비스를 같은 실행 단위로 묶어 실제 운영 프로젝트처럼 다루기 위해 사용한다.

현재 단계에서는 Nginx, FastAPI, PostgreSQL, 데모 메모 서비스를 함께 띄우고 상태 연결과 운영 흐름을 검증한다.

---

## 3. 현재 구성 범위

현재 Docker Compose 구성은 네 개 서비스로 이루어진다.

```text
Client
  ↓
Nginx
  ↓
FastAPI
  ↓
PostgreSQL

FastAPI
  ↓
데모 메모 서비스 상태 확인
```

| 구분 | 실행 위치 | 설명 |
|---|---|---|
| Nginx | Docker Container | 외부 진입점 |
| FastAPI | Docker Container | 운영 API와 대시보드 제공 |
| PostgreSQL | Docker Container | DB 연결 상태 확인 대상 |
| 데모 메모 서비스 | Docker Container | 운영용 메모 서비스 |

---

## 4. 서비스 구성

| Service | Image/Build | Container Name | Role |
|---|---|---|---|
| nginx | nginx:latest | ops-monitor-nginx | 외부 요청 진입점 |
| app | local build | ops-monitor-app | 운영 API와 대시보드 |
| db | postgres:16 | ops-monitor-db | PostgreSQL 데이터베이스 |
| notes | `demo-notes` build | ops-monitor-notes | 메모 서비스 |

### app 서비스

`app` 서비스는 `/dashboard`, `/health`, `/system`, `/alerts`, `/monitoring/status` 같은 운영 기능을 제공한다.

또한 `DEMO_NOTES_URL`을 통해 메모 서비스의 연결 상태를 함께 점검한다.

### db 서비스

`db` 서비스는 Ops Monitor와 데모 메모 서비스가 함께 사용하는 PostgreSQL 데이터베이스다.

운영 API의 DB 연결 확인 대상이면서, 메모 서비스의 실제 저장소 역할도 맡는다.

### notes 서비스

`notes` 서비스는 브라우저에서 직접 메모를 입력, 수정, 삭제할 수 있는 작은 운영 보조 서비스다.

대시보드가 단순 시각화 화면에 머물지 않고 실제 운영 중인 부가 서비스를 감시하는 구조를 만들기 위해 추가했다.

---

## 5. Docker Compose 설정

현재 `docker-compose.yml`은 `nginx`, `app`, `db`, `notes` 서비스로 구성한다.

문서에는 계정명, 비밀번호, 데이터베이스명을 직접 작성하지 않고 환경변수로 분리한다.

```yaml
services:
  nginx:
    image: nginx:latest
    container_name: ops-monitor-nginx
    restart: always
    ports:
      - "80:80"

  app:
    build: .
    container_name: ops-monitor-app
    restart: always
    env_file:
      - .env
    environment:
      DEMO_NOTES_URL: "http://notes:8010/healthz"

  db:
    image: postgres:16
    container_name: ops-monitor-db
    restart: always

  notes:
    build: ./demo-notes
    container_name: ops-monitor-notes
    restart: always
    env_file:
      - .env
    environment:
      DEMO_NOTES_DATABASE_URL: "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"

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

| 변수 | 예시 | 설명 |
|---|---|---|
| POSTGRES_USER | `<DB_USER>` | PostgreSQL 사용자명 |
| POSTGRES_PASSWORD | `<DB_PASSWORD>` | PostgreSQL 비밀번호 |
| POSTGRES_DB | `<DB_NAME>` | PostgreSQL 데이터베이스명 |
| DEMO_NOTES_URL | `http://notes:8010/healthz` | 메모 서비스 상태 점검 주소 |
| DEMO_NOTES_DATABASE_URL | `postgresql://...@db:5432/...` | 메모 서비스 DB 연결 문자열 |

실제 값은 `.env` 파일에서 관리하며, `.env` 파일은 GitHub에 업로드하지 않는다.

### 6.5 Port Mapping

| 호스트 포트 | 컨테이너 포트 | 설명 |
|---|---|---|
| 80 | 80 | Nginx 외부 접근 |
| 5432 | 5432 | 로컬에서 PostgreSQL 직접 점검 |
| 8010 | 8010 | 데모 메모 서비스 브라우저 접근 |

### 6.6 Volume

| 볼륨 | 마운트 경로 | 설명 |
|---|---|---|
| postgres_data | /var/lib/postgresql/data | PostgreSQL 데이터 영속성 확보 |

PostgreSQL 데이터가 컨테이너 삭제와 분리되어 유지될 수 있도록 named volume을 사용한다.

---

## 7. 서비스 연동 방식

FastAPI는 `.env` 파일의 `DATABASE_URL`을 통해 PostgreSQL에 연결한다.

Compose 내부에서는 DB host를 `db`로 사용한다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
```

`notes` 서비스도 PostgreSQL을 사용하며, 별도 테이블에 메모를 저장한다.

```env
DEMO_NOTES_DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
```

`/health` API는 DB와 메모 서비스 연결 상태를 함께 확인한다.

로컬에서 앱이나 메모 서비스를 직접 실행할 때는 `db` 호스트가 해석되지 않을 수 있다.

현재 구현은 실행 위치 차이를 다음처럼 흡수한다.

- 컨테이너 내부 실행: `db`
- 로컬 직접 실행: 필요 시 `localhost`로 보정

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

### 9.1 전체 서비스 실행

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

### 9.4 데모 메모 서비스 접속

```text
http://localhost:8010
```

### 9.5 PostgreSQL 컨테이너 중지

```bash
docker stop ops-monitor-db
```

### 9.6 PostgreSQL 컨테이너 재시작

```bash
docker start ops-monitor-db
```

---

## 10. 상태 점검 검증 결과

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

또한 메모 서비스는 DB 의존성이 있으므로, DB 장애 시 `demo_notes` 상태도 함께 영향을 받는다.

추가로 실제 복구 과정에서, `notes` 서비스에 전달한 `DEMO_NOTES_DATABASE_URL`이 Compose 치환 없이 문자열 그대로 들어가면 컨테이너가 인증 실패 후 재시작 루프에 들어갈 수 있다는 점을 확인했다.

그래서 현재 Compose 기준은 다음과 같다.

- `notes` 서비스에도 `env_file: .env`를 명시한다
- `DEMO_NOTES_DATABASE_URL`은 `${...}` 형태로 실제 치환되게 작성한다

---

## 11. 현재 완료 상태

| 항목 | 상태 |
|---|---|
| Nginx 컨테이너 구성 | 완료 |
| FastAPI 컨테이너 구성 | 완료 |
| PostgreSQL 컨테이너 구성 | 완료 |
| 데모 메모 서비스 컨테이너 구성 | 완료 |
| `/health` API DB 상태 응답 확인 | 완료 |
| `/health` API 메모 서비스 상태 응답 확인 | 완료 |
| PostgreSQL 컨테이너 중지 시 장애 감지 확인 | 완료 |
| PostgreSQL 컨테이너 재시작 시 복구 확인 | 완료 |

---

## 12. 확장 설계

현재 기본 운영 구성은 갖춰졌고, 다음 단계 확장은 운영 자동화와 배포 쪽에 가깝다.

```text
Client
  ↓
Nginx Container
  ↓
FastAPI Container
  ↓
PostgreSQL Container

FastAPI Container
  ↓
데모 메모 서비스 컨테이너
```

향후에는 다음 항목을 보강할 수 있다.

- 앱과 메모 서비스의 이미지 빌드 최적화
- 운영 명령의 권한 분리
- DB 마이그레이션 도입
- 배포 자동화

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

- DB 마이그레이션 도입 검토
- 데모 메모 서비스 인증 또는 권한 모델 검토
- 운영 액션을 늘릴 경우 감사 로그 추가
- 배포 자동화와 헬스체크 검증 스크립트 정리
