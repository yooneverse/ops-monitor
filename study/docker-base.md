# Docker Basic

## 1. 학습 목적

Ops Monitor 프로젝트에서 PostgreSQL을 컨테이너로 실행하고, 이후 FastAPI와 Nginx까지 Docker Compose로 함께 구성하기 위해 Docker 기본 개념을 정리한다.

이 문서는 Docker를 처음 보거나, 시간이 지난 뒤 다시 프로젝트를 확인할 때 다음 내용을 빠르게 이해할 수 있도록 작성한다.

| 구분 | 정리 내용 |
|---|---|
| Docker를 사용한 이유 | 로컬 설치 없이 PostgreSQL 실행 환경 구성 |
| 컨테이너 개념 | Image, Container, Compose의 차이 |
| 프로젝트 적용 | PostgreSQL 컨테이너 실행 및 Health Check 연동 |
| 운영 흐름 | 컨테이너 중지, 재시작을 통한 장애 감지 및 복구 확인 |
| 민감정보 처리 | 사용자명, 비밀번호, 실제 DB 이름, 연결 문자열은 플레이스홀더로 표기 |

---

## 2. Docker를 사용한 이유

Ops Monitor에서는 PostgreSQL을 로컬 PC에 직접 설치하지 않고 Docker 컨테이너로 실행했다.

로컬에 직접 DB를 설치하면 설치 과정, 버전, 환경 설정이 PC마다 달라질 수 있다. 반면 Docker를 사용하면 필요한 실행 환경을 이미지로 가져와 컨테이너로 실행할 수 있기 때문에, 같은 설정으로 데이터베이스 환경을 반복해서 구성할 수 있다.

이번 프로젝트에서는 PostgreSQL 컨테이너를 실행하고, FastAPI의 `/health` API에서 DB 연결 상태를 확인했다.

### 프로젝트에서 Docker를 사용한 목적

| 목적 | 설명 |
|---|---|
| 환경 분리 | 로컬 PC 환경과 PostgreSQL 실행 환경을 분리 |
| 실행 재현성 | 같은 이미지와 설정으로 동일한 DB 환경 구성 |
| 관리 편의성 | 컨테이너 시작, 중지, 재시작 명령어로 DB 상태 관리 |
| 장애 실습 | 컨테이너 중지를 통해 DB 장애 상황 생성 |
| 확장 준비 | 이후 FastAPI, Nginx도 컨테이너로 함께 실행할 수 있도록 준비 |

---

## 3. 핵심 개념

### 3.1 Image

Image는 컨테이너를 만들기 위한 실행 환경 템플릿이다.

애플리케이션을 실행하려면 운영체제 환경, 실행 파일, 라이브러리, 설정 등이 필요하다. Docker Image는 이러한 실행 환경을 미리 묶어둔 것이다.

Ops Monitor에서는 PostgreSQL 실행을 위해 다음 이미지를 사용했다.

```text
postgres:16
```

| 항목 | 내용 |
|---|---|
| Image | `postgres:16` |
| 의미 | PostgreSQL 16 버전을 실행하기 위한 이미지 |
| 사용 목적 | PostgreSQL 데이터베이스 컨테이너 생성 |

---

### 3.2 Container

Container는 Image를 실제로 실행한 인스턴스이다.

Image가 실행 환경의 템플릿이라면, Container는 그 템플릿을 바탕으로 실제 동작하는 실행 단위이다.

Ops Monitor에서는 `postgres:16` 이미지를 실행해 다음 컨테이너를 만들었다.

```text
ops-monitor-db
```

| 구분 | 설명 | 프로젝트 적용 |
|---|---|---|
| Image | 컨테이너를 만들기 위한 실행 환경 템플릿 | `postgres:16` |
| Container | 이미지를 실제로 실행한 인스턴스 | `ops-monitor-db` |

### Image와 Container 흐름

```text
postgres:16 Image
  ↓
ops-monitor-db Container
  ↓
PostgreSQL 실행
  ↓
FastAPI /health DB Connection Check
```

---

### 3.3 Docker Compose

Docker Compose는 여러 컨테이너를 하나의 설정 파일로 정의하고 실행하기 위한 도구이다.

현재 Ops Monitor에서는 PostgreSQL 컨테이너 하나만 Docker Compose로 실행했다. 하지만 최종적으로는 FastAPI, PostgreSQL, Nginx를 함께 실행하는 구조로 확장할 예정이다.

목표 구조는 다음과 같다.

```text
Nginx Container
  ↓
FastAPI Container
  ↓
PostgreSQL Container
```

컨테이너가 하나뿐이라면 `docker run` 명령어로 실행할 수도 있다. 하지만 서비스가 여러 개로 늘어나면 매번 긴 실행 명령어를 입력하는 방식은 관리하기 어렵다.

Docker Compose를 사용하면 실행 설정을 `docker-compose.yml` 파일에 정리해두고, 하나의 명령어로 필요한 서비스를 실행할 수 있다.

```bash
docker compose up -d
```

---

## 4. docker run 대신 Docker Compose를 선택한 이유

PostgreSQL 컨테이너만 실행한다면 `docker run` 명령어를 사용할 수도 있다.

예시는 다음과 같다.

```bash
docker run -d \
  --name ops-monitor-db \
  -p 5432:5432 \
  -e POSTGRES_USER=<DB_USER> \
  -e POSTGRES_PASSWORD=<DB_PASSWORD> \
  -e POSTGRES_DB=<DB_NAME> \
  postgres:16
```

하지만 이 방식은 설정이 길고, 나중에 FastAPI와 Nginx가 추가되면 관리가 복잡해진다.

Docker Compose를 사용하면 같은 설정을 파일로 분리할 수 있다.

```yaml
services:
  db:
    image: postgres:16
    container_name: ops-monitor-db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
```

Ops Monitor는 단순히 PostgreSQL을 한 번 실행하는 것이 아니라, 운영 환경 구성과 장애 대응 흐름을 실습하는 프로젝트이다. 따라서 실행 명령어보다 서비스 구성을 파일로 남길 수 있는 Docker Compose가 더 적합하다.

### Docker Compose를 선택한 이유

| 이유 | 설명 |
|---|---|
| 설정 관리 | 이미지, 포트, 환경변수, 볼륨 설정을 파일로 관리 |
| 실행 일관성 | 같은 `docker-compose.yml`로 동일한 환경 반복 실행 |
| 확장성 | 이후 FastAPI와 Nginx 컨테이너 추가 가능 |
| 운영 흐름 실습 | 컨테이너 실행, 중지, 재시작을 통해 장애 감지 및 복구 실습 |
| 문서화 용이 | 실행 구조가 명령어가 아니라 설정 파일로 남음 |
| 민감정보 분리 | DB 사용자명, 비밀번호, DB 이름을 환경변수로 분리 가능 |

---

## 5. Ops Monitor의 현재 Docker 구성

현재 단계에서는 PostgreSQL만 Docker Compose로 실행한다.

FastAPI 서버는 로컬에서 실행하고, PostgreSQL은 Docker 컨테이너에서 실행한다.

```text
Local FastAPI
  ↓
localhost:5432
  ↓
PostgreSQL Container
```

### 현재 구성 요소

| 구성 요소 | 실행 위치 | 역할 |
|---|---|---|
| FastAPI | Local | `/health` API 제공 |
| PostgreSQL | Docker Container | DB 연결 상태 확인 대상 |
| Docker Compose | Local | PostgreSQL 컨테이너 실행 관리 |

---

## 6. 환경변수와 민감정보 관리

DB 계정명, 비밀번호, 데이터베이스명, 연결 문자열은 실제 값으로 문서에 작성하지 않는다.

실제 값은 `.env` 파일에서 관리하고, `.env` 파일은 Git에 올리지 않는다.

문서에서는 다음과 같이 플레이스홀더를 사용한다.

```env
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASSWORD>
POSTGRES_DB=<DB_NAME>
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>
```

`.env.example`에는 실제 값이 아닌 예시값만 작성한다.

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5432/your_db_name
```

`.gitignore`에는 다음 설정을 포함한다.

```gitignore
.env
.env.*
!.env.example
```

---

## 7. Docker Compose 실행 흐름

현재 프로젝트에서 Docker Compose를 사용하는 흐름은 다음과 같다.

```text
docker-compose.yml 작성
  ↓
docker compose up -d
  ↓
PostgreSQL Container 실행
  ↓
FastAPI /health 호출
  ↓
DB 연결 상태 확인
```

PostgreSQL 컨테이너가 실행 중이면 `/health` API는 `connected`를 반환한다.

PostgreSQL 컨테이너가 중지되면 `/health` API는 `disconnected`를 반환한다.

이를 통해 Docker Compose가 단순 실행 도구가 아니라, 서비스 운영 상태를 재현하고 점검하는 기반이 될 수 있다는 점을 확인했다.

---

## 8. 사용한 명령어

### 8.1 Docker 버전 확인

```bash
docker --version
docker compose version
```

Docker CLI와 Docker Compose 사용 가능 여부를 확인한다.

---

### 8.2 PostgreSQL 컨테이너 실행

```bash
docker compose up -d
```

`-d` 옵션은 컨테이너를 백그라운드에서 실행한다는 의미이다.

---

### 8.3 실행 중인 컨테이너 확인

```bash
docker ps
```

현재 실행 중인 컨테이너 목록을 확인한다.

확인 대상은 다음 컨테이너이다.

```text
ops-monitor-db
```

---

### 8.4 컨테이너 로그 확인

```bash
docker logs ops-monitor-db
```

PostgreSQL 컨테이너가 정상 실행되었는지 로그로 확인한다.

---

### 8.5 컨테이너 중지

```bash
docker stop ops-monitor-db
```

PostgreSQL 컨테이너를 중지하여 DB 장애 상황을 만든다.

---

### 8.6 컨테이너 재시작

```bash
docker start ops-monitor-db
```

중지된 PostgreSQL 컨테이너를 다시 실행해 복구 상태를 확인한다.

---

## 9. Health Check와 연결된 점

Ops Monitor의 `/health` API는 API 서버 상태와 DB 연결 상태를 함께 반환한다.

PostgreSQL 컨테이너 상태에 따라 `/health` 응답이 달라진다.

| PostgreSQL 컨테이너 상태 | `/health` DB 상태 | 의미 |
|---|---|---|
| 실행 전 | `disconnected` | DB 연결 실패 |
| 실행 중 | `connected` | DB 연결 성공 |
| 중지됨 | `disconnected` | DB 장애 상태 감지 |
| 재시작 후 | `connected` | DB 복구 확인 |

### 연결 성공 응답

```json
{
  "api": "ok",
  "database": {
    "status": "connected",
    "message": "Database connection successful"
  },
  "timestamp": "2026-07-04T22:40:00"
}
```

### 연결 실패 응답

```json
{
  "api": "ok",
  "database": {
    "status": "disconnected",
    "message": "Database connection failed"
  },
  "timestamp": "2026-07-04T22:23:48.969699"
}
```

---

## 10. 장애 감지 및 복구 실습

PostgreSQL 컨테이너를 중지하여 DB 장애 상황을 만들었다.

```bash
docker stop ops-monitor-db
```

이후 `/health` API에서 DB 상태가 `disconnected`로 반환되는 것을 확인했다.

다시 컨테이너를 실행했다.

```bash
docker start ops-monitor-db
```

재시작 후 `/health` API에서 DB 상태가 다시 `connected`로 반환되는 것을 확인했다.

### 실습 결과

| 단계 | 수행 작업 | 확인 결과 |
|---|---|---|
| 1 | PostgreSQL 컨테이너 실행 | `connected` |
| 2 | PostgreSQL 컨테이너 중지 | `disconnected` |
| 3 | PostgreSQL 컨테이너 재시작 | `connected` |

이를 통해 컨테이너 상태 변화가 서비스 Health Check 결과와 연결되는 흐름을 이해할 수 있었다.

---

## 11. 헷갈렸던 점

### 11.1 Docker 명령어가 인식되지 않음

처음에는 Docker Desktop이 설치되지 않아 다음 오류가 발생했다.

```bash
bash: docker: command not found
```

Docker Desktop 설치 후 새 터미널을 열어 해결했다.

---

### 11.2 Docker Engine이 실행되지 않음

Docker CLI는 인식되었지만 Docker Engine이 실행되지 않아 다음 오류가 발생했다.

```bash
failed to connect to the docker API
```

Docker Desktop을 실행하고 Docker Engine이 running 상태가 된 뒤 다시 실행해 해결했다.

---

## 12. 민감정보 처리 기준

| 항목 | 처리 방식 |
|---|---|
| Windows 사용자명 | 문서에 작성하지 않음 |
| 로컬 절대경로 | 문서에 작성하지 않음 |
| DB 사용자명 | `<DB_USER>` |
| DB 비밀번호 | `<DB_PASSWORD>` |
| DB 이름 | `<DB_NAME>` |
| DB 연결 문자열 | `postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>` |
| 실제 `.env` 파일 | Git 추적 제외 |
| `.env.example` | 예시값만 작성 |

---

## 13. 프로젝트 적용 정리

| 항목 | 적용 내용 |
|---|---|
| Image | PostgreSQL 16 이미지 사용 |
| Container | PostgreSQL 컨테이너 실행 |
| Compose | `docker-compose.yml`로 DB 서비스 정의 |
| Port | 로컬 FastAPI에서 `localhost:5432`로 DB 접근 |
| Health Check | `/health` API에서 DB 연결 상태 확인 |
| 장애 확인 | 컨테이너 중지 후 `disconnected` 확인 |
| 복구 확인 | 컨테이너 재시작 후 `connected` 확인 |
| 민감정보 관리 | 실제 DB 설정값은 `.env`로 분리하고 문서에는 플레이스홀더 사용 |
| 문서화 | Docker Compose 설계서, 운영 로그, 트러블슈팅 문서에 기록 |

---
