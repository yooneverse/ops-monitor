# Ops Monitor

Docker 기반 서비스 운영 환경을 구성하고, Health Check API를 통해 API 서버와 데이터베이스 상태를 확인하는 인프라 운영 미니 프로젝트입니다.

FastAPI, PostgreSQL, Docker Compose를 활용해 서비스 상태 점검, DB 장애 감지, 컨테이너 재시작을 통한 복구 확인 흐름을 실습합니다.

---

## 1. Project Overview

Ops Monitor는 서버 운영, 서비스 상태 점검, 장애 감지, 복구 확인 과정을 직접 경험하기 위해 진행하는 운영 모니터링 실습 프로젝트입니다.

현재는 FastAPI 서버를 로컬에서 실행하고, PostgreSQL은 Docker Compose로 컨테이너 실행하는 구조입니다.

`/health` API를 통해 API 서버 상태와 PostgreSQL 연결 상태를 함께 확인할 수 있습니다.

---

## 2. Project Goal

이 프로젝트의 목표는 단순 API 구현이 아니라, 서비스 운영 환경에서 필요한 상태 점검과 장애 대응 흐름을 직접 구성하는 것입니다.

| 목표 | 설명 |
|---|---|
| API 상태 확인 | FastAPI 서버가 정상 동작하는지 확인 |
| DB 연결 확인 | PostgreSQL 연결 성공 및 실패 상태 확인 |
| 장애 감지 | DB 컨테이너 중지 시 `disconnected` 상태 반환 |
| 복구 확인 | DB 컨테이너 재시작 후 `connected` 상태 복구 확인 |
| 운영 기록 | 작업 내용, 장애 상황, 복구 과정을 문서로 기록 |
| 실행 환경 관리 | Docker Compose 기반으로 PostgreSQL 실행 환경 구성 |
| 민감정보 보호 | 실제 계정명, 비밀번호, DB명, 연결 문자열은 문서에 직접 작성하지 않음 |

---

## 3. Tech Stack

| Category | Stack |
|---|---|
| Backend | FastAPI |
| Database | PostgreSQL |
| Container | Docker, Docker Compose |
| Language | Python |
| Config | `.env`, `.env.example` |
| Version Control | Git, GitHub |
| 예정 | Nginx, GitHub Actions |

---

## 4. Current Architecture

현재 구조는 다음과 같습니다.

```text
Client
  ↓
FastAPI Local Server
  ↓
localhost:5432
  ↓
PostgreSQL Container
```

| 구성 요소 | 실행 위치 | 역할 |
|---|---|---|
| FastAPI | Local | API 서버 및 Health Check 제공 |
| PostgreSQL | Docker Container | DB 연결 상태 확인 대상 |
| Docker Compose | Local | PostgreSQL 컨테이너 실행 관리 |

향후 FastAPI와 Nginx를 Docker Compose에 포함하여 다음 구조로 확장할 예정입니다.

```text
Client
  ↓
Nginx Container
  ↓
FastAPI Container
  ↓
PostgreSQL Container
```

---

## 5. Core Features

| 기능 | 설명 | 상태 |
|---|---|---|
| Root API | API 서버 실행 여부 확인 | 완료 |
| Health Check API | API 서버 및 DB 연결 상태 확인 | 완료 |
| PostgreSQL Container | Docker Compose로 PostgreSQL 실행 | 완료 |
| DB 장애 감지 | PostgreSQL 중지 시 `disconnected` 반환 | 완료 |
| DB 복구 확인 | PostgreSQL 재시작 시 `connected` 반환 | 완료 |
| 로그 관리 API | 서비스 로그 조회 및 생성 | 예정 |
| 장애 이력 API | 장애 발생 및 복구 이력 관리 | 예정 |
| Nginx Reverse Proxy | 외부 요청을 FastAPI로 전달 | 예정 |

---

## 6. API

### GET `/`

API 서버 실행 여부를 확인합니다.

```http
GET /
```

Response

```json
{
  "message": "Ops Monitor API is running"
}
```

---

### GET `/health`

API 서버 상태와 PostgreSQL 연결 상태를 확인합니다.

```http
GET /health
```

DB 연결 성공 시 응답:

```json
{
  "api": "ok",
  "database": {
    "status": "connected",
    "message": "Database connection successful"
  },
  "timestamp": "<TIMESTAMP>"
}
```

DB 연결 실패 시 응답:

```json
{
  "api": "ok",
  "database": {
    "status": "disconnected",
    "message": "Database connection failed"
  },
  "timestamp": "<TIMESTAMP>"
}
```

### Health Check Status

| Status | 의미 |
|---|---|
| connected | PostgreSQL 연결 성공 |
| disconnected | PostgreSQL 연결 실패 |
| error | 환경변수 설정 오류 |

---

## 7. Project Structure

```text
ops-monitor/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   │   └── db_check.py
│   └── models/
├── docs/
│   ├── 01_srs.md
│   ├── 02_architecture.md
│   ├── 03_api_spec.md
│   ├── 04_erd.md
│   ├── 05_docker_compose_design.md
│   ├── 08_troubleshooting.md
│   └── operation-log.md
├── study/
│   ├── day01-project-setup.md
│   ├── git-basic.md
│   ├── fastapi-base.md
│   └── docker-base.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 8. Docker Compose

현재 `docker-compose.yml`은 PostgreSQL 컨테이너 실행을 위한 `db` 서비스로 구성되어 있습니다.

DB 사용자명, 비밀번호, 데이터베이스명은 문서에 직접 작성하지 않고 환경변수로 분리합니다.

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

`.env.example` 예시는 다음과 같습니다.

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5432/your_db_name
```

실제 `.env` 파일은 GitHub에 업로드하지 않습니다.

---

## 9. Environment Variables

실제 실행 환경에서는 `.env.example`을 참고해 `.env` 파일을 생성합니다.

README와 문서에는 실제 값을 작성하지 않고, 아래처럼 플레이스홀더로 표기합니다.

```env
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASSWORD>
POSTGRES_DB=<DB_NAME>
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
```

현재 로컬 실행 단계에서는 DB host로 `localhost`를 사용합니다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>
```

향후 FastAPI를 Docker Compose 내부에서 실행할 경우 DB host는 Compose 서비스명인 `db`로 변경합니다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
```

---

## 10. How to Run

### 1. Repository Clone

```bash
git clone https://github.com/<GITHUB_ID>/ops-monitor.git
cd ops-monitor
```

### 2. Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Windows PowerShell을 사용하는 경우:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

`.env.example`을 참고해 `.env` 파일을 생성합니다.

```env
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASSWORD>
POSTGRES_DB=<DB_NAME>
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>
```

`.env` 파일은 Git 추적 대상에서 제외합니다.

### 5. Run PostgreSQL Container

```bash
docker compose up -d
```

컨테이너 실행 확인:

```bash
docker ps
```

로그 확인:

```bash
docker logs ops-monitor-db
```

### 6. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

### 7. Check API

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

---

## 11. Failure Recovery Scenario

PostgreSQL 컨테이너를 중지하여 DB 장애 상황을 생성하고, `/health` API에서 장애 감지 여부를 확인합니다.

### 1. DB 컨테이너 중지

```bash
docker stop ops-monitor-db
```

### 2. Health Check 확인

```http
GET /health
```

예상 결과:

```json
{
  "api": "ok",
  "database": {
    "status": "disconnected",
    "message": "Database connection failed"
  },
  "timestamp": "<TIMESTAMP>"
}
```

### 3. DB 컨테이너 재시작

```bash
docker start ops-monitor-db
```

### 4. 복구 확인

```http
GET /health
```

예상 결과:

```json
{
  "api": "ok",
  "database": {
    "status": "connected",
    "message": "Database connection successful"
  },
  "timestamp": "<TIMESTAMP>"
}
```

---

## 12. Operation Documentation

운영 과정에서 확인한 내용을 문서로 남겨 프로젝트의 흐름을 정리합니다.

| Document | Description |
|---|---|
| `docs/01_srs.md` | 기능 요구사항, 비기능 요구사항, 장애 대응 요구사항 정의 |
| `docs/02_architecture.md` | 현재 구성과 목표 아키텍처, 요청 흐름 정리 |
| `docs/03_api_spec.md` | API 엔드포인트와 응답 구조 정의 |
| `docs/04_erd.md` | 사용자, 로그, 장애 이력 테이블 설계 |
| `docs/05_docker_compose_design.md` | Docker Compose 서비스 구성 설계 |
| `docs/08_troubleshooting.md` | 프로젝트 진행 중 발생한 문제와 해결 과정 기록 |
| `docs/operation-log.md` | 날짜별 작업 내용과 운영 확인 결과 기록 |

---

## 13. Study Notes

프로젝트 구현 과정에서 필요한 개념은 `study/` 폴더에 정리합니다.

| Document | Description |
|---|---|
| `study/day01-project-setup.md` | 프로젝트 초기 세팅과 FastAPI 실행 기록 |
| `study/git-basic.md` | Git 기본 명령어와 커밋 흐름 정리 |
| `study/fastapi-base.md` | FastAPI 기본 구조와 `/health` API 정리 |
| `study/docker-base.md` | Docker 이미지, 컨테이너, Compose 개념과 PostgreSQL 컨테이너 실행 정리 |

---

## 14. Security Notes

민감정보와 개인정보가 GitHub에 노출되지 않도록 다음 기준을 적용합니다.

| 항목 | 처리 방식 |
|---|---|
| 실제 `.env` 파일 | Git 추적 제외 |
| DB 사용자명 | 문서에서는 `<DB_USER>`로 표기 |
| DB 비밀번호 | 문서에서는 `<DB_PASSWORD>`로 표기 |
| DB 이름 | 문서에서는 `<DB_NAME>`으로 표기 |
| DB Host | 문서에서는 `<DB_HOST>` 또는 실행 환경에 맞는 예시로 표기 |
| DB Port | 문서에서는 `<DB_PORT>` 또는 공개 가능한 기본 포트만 표기 |
| DB 연결 문자열 | 실제 값 대신 플레이스홀더 사용 |
| GitHub ID | README 예시에서는 `<GITHUB_ID>`로 표기 |
| 로컬 절대경로 | 문서에 작성하지 않음 |
| Windows 사용자명 | 문서에 작성하지 않음 |
| 오류 로그 | 개인 경로, 계정명, 연결 문자열 제거 후 기록 |

`.gitignore`에는 다음 설정을 포함합니다.

```gitignore
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.venv/
```

---

## 15. Commit Convention

커밋 메시지는 말머리만 영어 컨벤션을 사용하고, 내용은 한글로 작성합니다.

```text
init: 프로젝트 초기 설정
feat: 기능 추가
infra: 인프라 설정 추가
docs: 문서 작성 및 수정
ci: GitHub Actions 설정
fix: 오류 수정
chore: 기타 설정 변경
```

예시:

```text
init: 프로젝트 초기 구조 생성
chore: 깃 추적 제외 설정 추가
feat: DB 상태 확인 기능 추가
infra: PostgreSQL 도커 컴포즈 구성
docs: 운영 문서 구조 정리
docs: 리드미와 학습 문서 정리
chore: 파이썬 캐시 파일 추적 제거
```

---

## 16. Current Status

| 항목 | 상태 |
|---|---|
| FastAPI 기본 서버 | 완료 |
| `/` API | 완료 |
| `/health` API | 완료 |
| DB 연결 상태 확인 | 완료 |
| PostgreSQL Docker Compose 실행 | 완료 |
| DB 장애 감지 및 복구 확인 | 완료 |
| 운영 문서 정리 | 진행 중 |
| FastAPI 컨테이너화 | 예정 |
| Nginx Reverse Proxy | 예정 |
| GitHub Actions | 예정 |

---

## 17. Next Steps

| 작업 | 설명 |
|---|---|
| FastAPI Dockerfile 작성 | API 서버를 컨테이너로 실행하기 위한 이미지 구성 |
| docker-compose.yml에 app 서비스 추가 | FastAPI와 PostgreSQL을 함께 실행 |
| DATABASE_URL 변경 | Compose 내부 네트워크 기준으로 DB host를 `db`로 변경 |
| Nginx Reverse Proxy 구성 | Nginx를 통해 FastAPI 요청 전달 |
| 로그/장애 이력 API 구현 | `/logs`, `/incidents` API 추가 |