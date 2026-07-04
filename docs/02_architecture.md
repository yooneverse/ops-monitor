# 아키텍처 설계서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | 아키텍처 설계서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 시스템 구성 요소, 요청 흐름, 장애 감지 흐름 정의 |
| 현재 구현 범위 | 로컬 FastAPI, Docker PostgreSQL, Health Check |
| 확장 예정 범위 | FastAPI 컨테이너화, Nginx Reverse Proxy, GitHub Actions |

---

## 2. 시스템 개요

Ops Monitor는 API 서버와 데이터베이스 상태를 확인하고, 장애 발생 시 감지 및 복구 흐름을 검증하기 위한 운영 모니터링 미니 프로젝트이다.

현재는 FastAPI 서버를 로컬에서 실행하고, PostgreSQL은 Docker Compose로 실행하는 구조이다.

최종적으로는 FastAPI, PostgreSQL, Nginx를 Docker Compose로 함께 실행하고, Nginx를 단일 진입점으로 사용하는 구조로 확장한다.

---

## 3. 현재 아키텍처

### 3.1 구성도

```text
Client
  ↓
FastAPI Local Server
  ↓
localhost:5432
  ↓
PostgreSQL Container
```

### 3.2 구성 요소

| 구성 요소 | 실행 위치 | 역할 | 상태 |
|---|---|---|---|
| Client | Local | API 요청 수행 | 완료 |
| FastAPI | Local | API 서버 및 Health Check 제공 | 완료 |
| PostgreSQL | Docker Container | DB 연결 상태 확인 대상 | 완료 |
| Docker Compose | Local | PostgreSQL 컨테이너 실행 | 완료 |
| Nginx | Docker Container | Reverse Proxy | 예정 |
| GitHub Actions | GitHub | 기본 CI 자동화 | 예정 |

---

## 4. 현재 요청 흐름

### 4.1 Root API 요청 흐름

```text
Client
  ↓
GET /
  ↓
FastAPI
  ↓
API 서버 실행 메시지 반환
```

### 4.2 Health Check 요청 흐름

```text
Client
  ↓
GET /health
  ↓
FastAPI
  ↓
DATABASE_URL 확인
  ↓
PostgreSQL 연결 테스트
  ↓
API 상태 + DB 상태 반환
```

### 4.3 Health Check 응답 기준

| 상황 | API 응답 | DB 상태 |
|---|---|---|
| FastAPI 정상, PostgreSQL 실행 | 200 | connected |
| FastAPI 정상, PostgreSQL 중지 | 200 | disconnected |
| FastAPI 정상, DATABASE_URL 누락 | 200 | error |
| FastAPI 미실행 | 응답 없음 | 확인 불가 |

---

## 5. 현재 DB 연결 구조

현재 FastAPI는 로컬 환경에서 실행되고, PostgreSQL은 Docker 컨테이너에서 실행된다.

```text
FastAPI Local Server
  ↓
localhost:5432
  ↓
PostgreSQL Container
```

FastAPI는 `.env` 파일에 정의된 `DATABASE_URL`을 사용해 PostgreSQL에 연결한다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>
```

실제 DB 계정명, 비밀번호, 데이터베이스명은 `.env`에서 관리하며 GitHub에 업로드하지 않는다.

---

## 6. 장애 감지 흐름

PostgreSQL 컨테이너가 중지되면 FastAPI는 DB 연결에 실패한다.

이 경우 `/health` API는 API 서버 상태와 DB 상태를 분리해 반환한다.

```text
PostgreSQL Container Stop
  ↓
GET /health
  ↓
FastAPI DB Connection Check
  ↓
Connection Failed
  ↓
database.status = disconnected
```

### 장애 감지 결과

| 단계 | 조치 | 확인 결과 |
|---|---|---|
| 1 | PostgreSQL 컨테이너 실행 | connected |
| 2 | PostgreSQL 컨테이너 중지 | disconnected |
| 3 | PostgreSQL 컨테이너 재시작 | connected |

---

## 7. 복구 확인 흐름

PostgreSQL 컨테이너를 재시작하면 FastAPI의 DB 연결 테스트가 다시 성공한다.

```text
PostgreSQL Container Start
  ↓
GET /health
  ↓
FastAPI DB Connection Check
  ↓
Connection Success
  ↓
database.status = connected
```

복구 여부는 `/health` API 응답을 통해 확인한다.

---

## 8. 목표 아키텍처

향후 FastAPI와 Nginx를 Docker Compose에 포함해 다음 구조로 확장한다.

```text
Client
  ↓
Nginx Container
  ↓
FastAPI Container
  ↓
PostgreSQL Container
```

### 목표 구성 요소

| 구성 요소 | 실행 위치 | 역할 |
|---|---|---|
| Client | Local 또는 외부 요청자 | API 요청 수행 |
| Nginx | Docker Container | Reverse Proxy |
| FastAPI | Docker Container | API 서버 |
| PostgreSQL | Docker Container | 데이터 저장소 |
| Docker Compose | Local 또는 Server | 전체 서비스 실행 관리 |
| GitHub Actions | GitHub | 코드 검증 자동화 |

---

## 9. 목표 요청 흐름

### 9.1 Nginx 적용 후 요청 흐름

```text
Client
  ↓
HTTP Request
  ↓
Nginx
  ↓
FastAPI
  ↓
PostgreSQL
```

Nginx는 외부 요청을 받아 FastAPI 컨테이너로 전달한다.

FastAPI는 API 요청을 처리하고, 필요한 경우 PostgreSQL에 연결한다.

### 9.2 Health Check 목표 흐름

```text
Client
  ↓
GET /health
  ↓
Nginx
  ↓
FastAPI
  ↓
PostgreSQL Connection Check
  ↓
Health Check Response
```

---

## 10. Docker Compose 확장 기준

현재는 PostgreSQL만 Docker Compose로 실행한다.

향후 확장 시 Compose 서비스는 다음과 같이 구성한다.

| Service | 역할 | 상태 |
|---|---|---|
| db | PostgreSQL 데이터베이스 | 완료 |
| app | FastAPI 애플리케이션 | 예정 |
| nginx | Reverse Proxy | 예정 |

FastAPI가 컨테이너 내부에서 실행되면 DB host는 `localhost`가 아니라 Compose 서비스명인 `db`를 사용한다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
```

향후 Nginx를 Reverse Proxy로 추가하여 외부 요청을 FastAPI 컨테이너로 전달한다.

---

## 11. 보안 및 설정 관리

| 항목 | 설계 기준 |
|---|---|
| DB 사용자명 | `.env`에서 관리 |
| DB 비밀번호 | `.env`에서 관리 |
| DB 연결 문자열 | `.env`에서 관리 |
| `.env` 파일 | Git 추적 제외 |
| `.env.example` | 예시값만 작성 |
| API 응답 | 실제 연결 문자열 및 내부 오류 원문 노출 금지 |
| 문서 | 실제 계정명, 비밀번호, 로컬 절대경로 블라인드 처리 |

---

## 12. 현재 완료 상태

| 항목 | 상태 |
|---|---|
| FastAPI 로컬 서버 구성 | 완료 |
| `/` API 구현 | 완료 |
| `/health` API 구현 | 완료 |
| PostgreSQL 연결 상태 확인 | 완료 |
| Docker Compose로 PostgreSQL 실행 | 완료 |
| DB 장애 감지 확인 | 완료 |
| DB 복구 확인 | 완료 |
| FastAPI 컨테이너화 | 예정 |
| Nginx Reverse Proxy 구성 | 예정 |
| GitHub Actions 구성 | 예정 |

---

## 13. 설계 고려사항

| 항목 | 고려 내용 |
|---|---|
| 운영성 | API와 DB 상태를 분리해 확인 |
| 장애 대응 | DB 중지 및 재시작 흐름을 Health Check로 검증 |
| 확장성 | FastAPI, PostgreSQL, Nginx를 Compose 구조로 확장 |
| 보안성 | 민감정보는 환경변수로 분리하고 문서에는 노출하지 않음 |
| 유지보수성 | API, DB 연결 로직, 문서를 분리해 관리 |
| 추적성 | 작업 기록과 트러블슈팅 기록을 별도 문서로 관리 |

---

## 14. 다음 작업

| 작업 | 설명 |
|---|---|
| FastAPI Dockerfile 작성 | API 서버 컨테이너 실행 환경 구성 |
| app 서비스 추가 | Docker Compose에 FastAPI 서비스 추가 |
| DATABASE_URL 변경 | Compose 내부 네트워크 기준으로 DB host를 `db`로 변경 |
| Nginx 설정 작성 | Reverse Proxy 설정 파일 작성 |
| nginx 서비스 추가 | Docker Compose에 Nginx 서비스 추가 |
| 요청 흐름 검증 | Nginx를 통해 `/health` API 호출 확인 |