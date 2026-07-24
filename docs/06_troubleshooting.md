# 트러블슈팅 문서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | 트러블슈팅 문서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 프로젝트 진행 중 발생한 오류와 해결 과정을 기록 |
| 기록 기준 | 문제 상황, 원인, 조치 내용, 결과 중심으로 작성 |
| 민감정보 처리 | 사용자명, 로컬 경로, 계정명, 비밀번호, 연결 문자열은 비식별 처리 |

---

## 2. 기록 컨벤션

트러블슈팅 기록은 아래 형식을 기준으로 작성한다.

| 항목 | 작성 내용 |
|---|---|
| 발생일 | 문제가 발생한 날짜 |
| 구분 | `ENV`, `DOCKER`, `API`, `DB`, `CI` 등 |
| 문제 상황 | 발생한 오류 또는 비정상 동작 |
| 원인 | 확인된 원인 또는 추정 원인 |
| 조치 | 실제 수행한 해결 방법 |
| 결과 | 해결 여부와 확인 결과 |
| 관련 명령어 | 문제 확인 또는 해결에 사용한 명령 |

---

## 3. 트러블슈팅 목록

| Date | Type | Issue | Status |
|---|---|---|---|
| 2026-07-03 | ENV | Git Bash에서 공백 포함 경로 인식 오류 | 해결 |
| 2026-07-04 | DOCKER | Docker 명령어 미인식 | 해결 |
| 2026-07-04 | DOCKER | Docker Desktop Engine 미실행 상태 오류 | 해결 |
| 2026-07-04 | DB | PostgreSQL 미실행 상태에서 DB 연결 실패 | 정상 감지 |
| 2026-07-06 | CI | GitHub Actions runner Compose 명령 차이로 CI 실패 | 해결 |
| 2026-07-21 | APP | 로컬 실행 시 `db` host 해석 실패로 메모 서비스 연결 오류 | 해결 |
| 2026-07-21 | DOCKER | `demo-notes` 컨테이너 환경변수 치환 오류로 재시작 반복 | 해결 |
| 2026-07-21 | UI | `demo-notes` 빈 데이터 상태와 연결 실패 상태가 구분되지 않음 | 해결 |

---

## 4. 상세 기록

### 4.1 Git Bash 경로 인식 오류

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-03 |
| 구분 | ENV |
| 상태 | 해결 |

#### 문제 상황

가상환경 Python으로 패키지를 설치하려는 과정에서 경로 인식 오류가 발생했다.

```bash
bash: /c:/Users/<PRIVATE_USER>/<PRIVATE_PATH>: No such file or directory
```

#### 원인

프로젝트 경로에 공백이 포함되어 있었고, Git Bash가 이를 하나의 경로로 처리하지 못했다.

#### 조치

가상환경을 먼저 활성화한 뒤 `pip` 명령을 실행하거나, Python 실행 경로 전체를 따옴표로 감싸서 실행했다.

```bash
source "../.venv/Scripts/activate"
pip install -r requirements.txt
```

```bash
"/c/Users/<PRIVATE_USER>/<PRIVATE_PATH>/.venv/Scripts/python.exe" -m pip install -r requirements.txt
```

#### 결과

의존성 설치가 정상 수행되었고 FastAPI 서버 실행까지 이어졌다.

---

### 4.2 Docker 명령어 미인식

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-04 |
| 구분 | DOCKER |
| 상태 | 해결 |

#### 문제 상황

Docker Compose로 PostgreSQL 컨테이너를 실행하려는 시점에 Docker 명령이 인식되지 않았다.

```bash
bash: docker: command not found
```

#### 원인

Docker Desktop이 설치되지 않았거나, 설치 후 현재 셸 세션에 Docker CLI 경로가 반영되지 않은 상태였다.

#### 조치

Docker Desktop을 설치한 뒤 터미널을 다시 열고 Docker 명령 인식 여부를 확인했다.

```bash
docker --version
docker compose version
```

#### 결과

Docker CLI와 Compose 명령이 정상 인식되었고, 이후 컨테이너 실행 단계로 진행할 수 있었다.

---

### 4.3 Docker Desktop Engine 미실행 상태 오류

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-04 |
| 구분 | DOCKER |
| 상태 | 해결 |

#### 문제 상황

Docker CLI는 인식되었지만 Compose 실행 시 Docker API 연결 오류가 발생했다.

```bash
unable to get image 'postgres:16': failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
```

#### 원인

Docker Desktop은 설치되어 있었지만 Docker Engine이 실제로 실행 중이 아니었다.

#### 조치

Docker Desktop을 실행하고 Engine이 running 상태가 될 때까지 기다린 뒤 Docker 상태를 다시 확인했다.

```bash
docker version
docker compose version
docker compose up -d
```

#### 결과

PostgreSQL 컨테이너가 정상 실행되었고 `/health` API에서 DB 상태가 `connected`로 반환되었다.

---

### 4.4 PostgreSQL 미실행 상태에서 DB 연결 실패

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-04 |
| 구분 | DB |
| 상태 | 정상 감지 |

#### 문제 상황

PostgreSQL이 실행되지 않은 상태에서 `/health` API를 호출하자 DB 연결 실패가 응답에 반영되었다.

#### 확인 결과

API 서버는 정상 응답했고 DB 상태만 `disconnected`로 반환되었다.

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

PostgreSQL 서비스가 실행되지 않아 DB 연결이 거부되었다.

#### 조치

Docker Compose로 PostgreSQL 컨테이너를 실행하고 상태를 점검했다.

```bash
docker compose up -d
docker ps
docker logs ops-monitor-db
```

#### 결과

PostgreSQL 실행 후 `/health` API에서 DB 상태가 `connected`로 변경되었다.

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

### 4.5 GitHub Actions runner Compose 명령 차이

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-06 |
| 구분 | CI |
| 상태 | 해결 |

#### 문제 상황

GitHub Actions에서 `CI / validate` 실행 중 Compose 설정 검증 단계가 실패했다.

```text
All checks have failed
CI / validate (push)
```

#### 원인

워크플로는 `docker-compose config`를 기준으로 작성되어 있었지만, GitHub Actions runner 환경에서는 `docker compose`만 제공되거나 반대로 독립형 Compose만 존재할 수 있다.

즉, Compose 기능 자체의 문제가 아니라 명령 형태 호환성 문제였다.

#### 조치

워크플로의 Compose 검증 단계를 아래처럼 수정해 두 형식을 모두 지원하도록 보완했다.

```yaml
- name: Validate Docker Compose config
  run: |
    if command -v docker-compose >/dev/null 2>&1; then
      docker-compose config
    else
      docker compose config
    fi
```

#### 결과

CI가 특정 Compose 명령 형식에 고정되지 않도록 보완되었고, runner 환경 차이로 인한 검증 실패 가능성을 줄였다.

---

### 4.6 로컬 실행 시 `db` host 해석 실패

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-21 |
| 구분 | APP |
| 상태 | 해결 |

#### 문제 상황

`demo-notes` 또는 앱을 로컬에서 직접 실행할 때 DB 연결 오류가 발생했다.

```text
([Errno -5] No address associated with hostname)
```

#### 원인

Docker Compose 내부에서는 DB host로 `db`를 사용하지만, 로컬 직접 실행 환경에서는 `db` 호스트명이 해석되지 않았다.

즉, 같은 설정 문자열을 컨테이너와 로컬 실행에 그대로 공유하면서 실행 환경 차이가 드러난 문제였다.

#### 조치

DB 연결 문자열을 바로 바꾸는 대신, 실행 위치를 보고 host를 보정하도록 정리했다.

- 컨테이너 내부 실행: `db` 유지
- 로컬 직접 실행: `localhost`로 보정

관련 코드:

- `app/services/db_check.py`
- `demo-notes/app.py`

#### 결과

로컬 실행과 Compose 실행이 같은 프로젝트 설정을 공유하더라도, 각 실행 위치에 맞는 DB host를 사용할 수 있게 되었다.

---

### 4.7 `demo-notes` 컨테이너 환경변수 치환 오류

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-21 |
| 구분 | DOCKER |
| 상태 | 해결 |

#### 문제 상황

브라우저에서 `http://localhost:8010` 접속 시 아래처럼 응답이 비어 있는 현상이 발생했다.

```text
ERR_EMPTY_RESPONSE
```

컨테이너 상태를 확인해보니 `ops-monitor-notes`가 계속 재시작 중이었다.

#### 원인

`DEMO_NOTES_DATABASE_URL`에 들어가야 할 값이 Compose 치환 없이 문자열 그대로 전달되면서 DB 인증에 실패했다.

대표적인 증상은 아래와 같았다.

```text
password authentication failed for user "${POSTGRES_USER}"
```

즉, 메모 서비스 자체의 라우팅 문제가 아니라 컨테이너 시작 단계의 DB 인증 실패 문제였다.

#### 조치

`docker-compose.yml`을 다음 기준으로 수정했다.

- `notes` 서비스에도 `env_file: .env` 명시
- `DEMO_NOTES_DATABASE_URL`을 `${POSTGRES_USER}` 형식으로 실제 치환되게 수정

이후 `notes` 컨테이너만 재빌드 및 재시작했다.

```bash
docker-compose up -d --build notes
docker ps -a
docker logs ops-monitor-notes
```

#### 결과

`ops-monitor-notes` 컨테이너가 재시작 루프에서 벗어나 `healthy` 상태로 올라왔고, `http://localhost:8010`에서 `200` 응답을 확인했다.

---

### 4.8 빈 데이터 상태와 연결 실패 상태 구분 부족

| 항목 | 내용 |
|---|---|
| 발생일 | 2026-07-21 |
| 구분 | UI |
| 상태 | 해결 |

#### 문제 상황

초기 메모 서비스는 데이터가 없는 경우와 DB 연결이 실패한 경우를 화면에서 분리해 보여주지 못했다.

이 때문에 사용자는 "정상적인 빈 상태"인지, "서비스가 실제로 죽은 상태"인지 구분하기 어려웠다.

#### 원인

메모 목록을 불러오는 흐름이 성공만 전제하고 있었고, 실패 시 화면 안에서 별도 상태를 표현하는 기준이 부족했다.

또한 루트 페이지 자체가 DB 초기화 실패에 영향을 받아 응답이 불안정해질 수 있었다.

#### 조치

`demo-notes/app.py`를 아래 기준으로 정리했다.

- 루트 페이지 `/`는 가능한 한 바로 응답
- 데이터가 0개면 `저장된 메모가 없습니다.` 표시
- `/api/notes` 실패 시 `메모 서비스를 불러오지 못했습니다. DB 연결 상태를 확인해주세요.` 표시

#### 결과

이후에는 "빈 메모 상태"와 "저장소 연결 실패 상태"가 화면에서 분리되었고, 운영자가 브라우저 화면만 보고도 상황을 더 정확히 판단할 수 있게 되었다.

---

## 5. 재발 방지 기준

| 항목 | 기준 |
|---|---|
| 경로 실행 | 공백 포함 경로는 따옴표 처리 또는 가상환경 활성화 후 실행 |
| Docker 사용 | Docker Desktop 실행 상태 확인 후 Docker 명령 수행 |
| Docker 확인 | `docker version`에서 Server 정보까지 확인 |
| DB 연결 | PostgreSQL 컨테이너 실행 상태 확인 후 `/health` 점검 |
| 실행 환경 차이 | 로컬 직접 실행과 Compose 내부 host 차이를 함께 고려 |
| Compose 변수 | 문자열 치환이 필요한 값은 `${...}` 형태와 `env_file` 적용 여부 함께 점검 |
| CI 호환성 | 로컬과 runner의 명령 차이를 고려해 fallback 구조 적용 |
| 오류 메시지 | 내부 상세 오류를 API 응답에 직접 노출하지 않음 |
| 화면 상태 표현 | 빈 상태와 연결 실패 상태를 동일하게 처리하지 않음 |
| 민감정보 | 계정명, 비밀번호, 연결 문자열은 문서에 직접 기록하지 않음 |

---

## 6. 다음 기록 예정 항목

| 예정 항목 | 설명 |
|---|---|
| FastAPI 컨테이너 실행 오류 | Dockerfile 또는 import 관련 이슈 발생 시 기록 |
| Compose 네트워크 연결 오류 | `localhost`와 `db` host 차이 관련 이슈 기록 |
| Nginx Reverse Proxy 연결 오류 | `proxy_pass` 설정 및 포트 연결 이슈 기록 |
| GitHub Actions 의존성 설치 오류 | 패키지 버전, OS 차이, 빌드 실패 이슈 기록 |
