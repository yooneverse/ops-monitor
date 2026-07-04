# 트러블슈팅 문서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | 트러블슈팅 문서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 프로젝트 진행 중 발생한 오류와 해결 과정을 기록 |
| 기록 기준 | 문제 상황, 원인, 조치 내용, 결과 중심으로 작성 |
| 민감정보 처리 | 사용자명, 로컬 절대경로, 계정명, 비밀번호, 연결 문자열은 블라인드 처리 |

---

## 2. 기록 컨벤션

트러블슈팅 기록은 다음 형식을 기준으로 작성한다.

| 항목 | 작성 내용 |
|---|---|
| 발생일 | 문제가 발생한 날짜 |
| 구분 | SETUP, ENV, DOCKER, API, DB, GIT 등 |
| 문제 상황 | 발생한 오류 또는 비정상 동작 |
| 원인 | 확인된 원인 또는 추정 원인 |
| 조치 | 실제 수행한 해결 방법 |
| 결과 | 해결 여부와 확인 결과 |
| 관련 명령어 | 문제 확인 또는 해결에 사용한 명령어 |
| 민감정보 처리 | 개인 경로, 사용자명, 비밀번호, 연결 문자열은 `<PRIVATE_*>` 형태로 처리 |

---

## 3. 트러블슈팅 목록

| Date | Type | Issue | Status |
|---|---|---|---|
| 2026-07-03 | ENV | Git Bash에서 공백 포함 경로 인식 오류 | 해결 |
| 2026-07-04 | DOCKER | Docker 명령어 미인식 | 해결 |
| 2026-07-04 | DOCKER | Docker Desktop 엔진 미실행 오류 | 해결 |
| 2026-07-04 | DB | PostgreSQL 미실행 상태에서 DB 연결 실패 | 정상 감지 |

---

## 4. 상세 기록

### 4.1 Git Bash 경로 인식 오류

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-03 |
| 구분 | ENV |
| 상태 | 해결 |

#### 문제 상황

가상환경의 Python으로 패키지를 설치하려고 했을 때 다음 오류가 발생했다.

```bash
bash: /c:/Users/<PRIVATE_USER>/<PRIVATE_PATH>/바탕: No such file or directory
```

#### 원인

프로젝트 경로에 공백이 포함되어 있었고, Git Bash가 따옴표 없는 경로를 공백 기준으로 분리해서 인식했다.

#### 조치

가상환경을 먼저 활성화한 뒤 `pip` 명령어를 실행했다.

```bash
source "../.venv/Scripts/activate"
pip install -r requirements.txt
```

또는 Python 실행 경로 전체를 따옴표로 감싸는 방식으로 해결할 수 있다.

```bash
"/c/Users/<PRIVATE_USER>/<PRIVATE_PATH>/.venv/Scripts/python.exe" -m pip install -r requirements.txt
```

#### 결과

의존성 설치가 정상적으로 진행되었고, FastAPI 서버 실행까지 완료했다.

---

### 4.2 Docker 명령어 미인식

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-04 |
| 구분 | DOCKER |
| 상태 | 해결 |

#### 문제 상황

Docker Compose로 PostgreSQL 컨테이너를 실행하려고 했을 때 다음 오류가 발생했다.

```bash
bash: docker: command not found
```

#### 원인

Docker Desktop이 설치되어 있지 않거나, 설치 후 현재 터미널 세션에서 Docker CLI 경로가 반영되지 않은 상태였다.

#### 조치

Docker Desktop을 설치한 뒤 새 Git Bash 터미널을 열어 Docker 명령어 인식 여부를 확인했다.

```bash
docker --version
docker compose version
```

#### 결과

Docker CLI가 정상 인식되었고, Docker Compose 명령어 실행 단계로 진행할 수 있었다.

---

### 4.3 Docker Desktop 엔진 미실행 오류

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-04 |
| 구분 | DOCKER |
| 상태 | 해결 |

#### 문제 상황

Docker CLI는 인식되었지만, Docker Compose 실행 시 Docker API 연결 오류가 발생했다.

```bash
unable to get image 'postgres:16': failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
```

#### 원인

Docker Desktop은 설치되어 있었지만, Docker Engine이 실행되지 않은 상태였다.

Docker CLI는 명령어를 인식했으나, 실제 컨테이너를 실행할 Docker Engine에 연결하지 못했다.

#### 조치

Docker Desktop을 실행하고, Docker Engine이 running 상태가 될 때까지 기다렸다.

이후 새 Git Bash 터미널에서 Docker 상태를 다시 확인했다.

```bash
docker version
docker compose version
```

Docker Server 정보가 정상적으로 표시된 뒤 PostgreSQL 컨테이너 실행을 다시 시도했다.

```bash
docker compose up -d
```

#### 결과

PostgreSQL 컨테이너가 정상 실행되었고, `/health` API에서 DB 연결 상태가 `connected`로 반환되었다.

---

### 4.4 PostgreSQL 미실행 상태에서 DB 연결 실패

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-04 |
| 구분 | DB |
| 상태 | 정상 감지 |

#### 문제 상황

PostgreSQL이 실행되지 않은 상태에서 `/health` API를 호출하자 DB 연결 실패가 발생했다.

#### 확인 결과

API 서버는 정상 응답했으며, DB 상태는 `disconnected`로 반환되었다.

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

#### 원인

PostgreSQL 서버가 실행되지 않아 DB 연결이 거부되었다.

#### 조치

Docker Compose로 PostgreSQL 컨테이너를 실행했다.

```bash
docker compose up -d
docker ps
docker logs ops-monitor-db
```

#### 결과

PostgreSQL 컨테이너 실행 후 `/health` API에서 DB 상태가 `connected`로 반환되었다.

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

---

## 5. 장애 감지 및 복구 확인

PostgreSQL 컨테이너를 중지해 DB 장애 상황을 생성했다.

```bash
docker stop ops-monitor-db
```

`/health` API에서 DB 상태가 `disconnected`로 반환되는 것을 확인했다.

이후 컨테이너를 재시작했다.

```bash
docker start ops-monitor-db
```

재시작 후 `/health` API에서 DB 상태가 다시 `connected`로 반환되는 것을 확인했다.

| 단계 | 확인 내용 | 결과 |
|---|---|---|
| PostgreSQL 실행 | `/health` 호출 | connected |
| PostgreSQL 중지 | `/health` 호출 | disconnected |
| PostgreSQL 재시작 | `/health` 호출 | connected |

---

## 6. 민감정보 처리 기준

| 항목 | 처리 방식 |
|---|---|
| Windows 사용자명 | `<PRIVATE_USER>` |
| 로컬 절대경로 | `<PRIVATE_PATH>` |
| DB 사용자명 | `<DB_USER>` |
| DB 비밀번호 | `<DB_PASSWORD>` |
| DB 이름 | `<DB_NAME>` |
| DB 연결 문자열 | `postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>` |
| 실제 `.env` 파일 | Git 추적 제외 |
| 문서 내 예시 | 실제 값 대신 플레이스홀더 사용 |

---

## 7. 재발 방지 기준

| 항목 | 기준 |
|---|---|
| 경로 실행 | 공백이 포함된 경로는 따옴표 처리 또는 가상환경 활성화 후 실행 |
| Docker 사용 | Docker Desktop 실행 상태 확인 후 Docker 명령어 실행 |
| Docker 확인 | `docker version`에서 Server 정보까지 확인 |
| DB 연결 | PostgreSQL 컨테이너 실행 상태 확인 후 `/health` 점검 |
| 오류 메시지 | 내부 상세 오류를 API 응답에 직접 노출하지 않음 |
| 민감정보 | DB 계정명, 비밀번호, 연결 문자열은 문서에 직접 작성하지 않음 |
| 로컬 환경 정보 | 사용자명과 개인 폴더 경로는 문서에 직접 작성하지 않음 |

---

## 8. 다음 기록 예정 항목

| 예정 항목 | 설명 |
|---|---|
| FastAPI 컨테이너 실행 오류 | Dockerfile 작성 후 발생 가능 이슈 기록 |
| Compose 내부 네트워크 연결 오류 | `localhost`와 `db` host 차이 관련 이슈 기록 |
| Nginx Reverse Proxy 연결 오류 | proxy_pass 설정 및 포트 연결 이슈 기록 |
| GitHub Actions 실패 | CI 설정 및 의존성 설치 오류 기록 |