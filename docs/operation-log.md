# 운영 작업 기록

## 기록 컨벤션

운영 작업 기록은 날짜별로 작성하며, 다음 항목을 기준으로 정리한다.

### 작성 형식

- 작업 일자: `YYYY-MM-DD`
- 작업 구분: `SETUP`, `FEATURE`, `INFRA`, `CHECK`, `TROUBLESHOOTING`, `DOCS`
- 작업 요약: 당일 수행한 핵심 작업을 1~3줄로 정리
- 확인 명령어: 실제 실행한 명령어 기록
- 확인 결과: 정상 동작, 실패, 복구 여부 기록
- 다음 작업: 이어서 진행할 작업 기록

### 작업 구분 기준

| Type | Description |
|---|---|
| SETUP | 프로젝트 초기 환경 구성 |
| FEATURE | API 또는 기능 구현 |
| INFRA | Docker, DB, Nginx 등 인프라 구성 |
| CHECK | 실행 결과 및 상태 확인 |
| TROUBLESHOOTING | 오류 발생 및 해결 기록 |
| DOCS | 문서 작성 및 정리 |

---

## 2026-07-03

### Type

`SETUP`, `FEATURE`, `DOCS`

### Summary

Ops Monitor 프로젝트 초기 구조를 생성하고, FastAPI 기본 서버와 `/health` API를 구현했다.  
GitHub Repository 연결, `.gitignore` 설정, README 및 study 문서 초안을 작성했다.

### Commands

```bash
git init
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Check

```text
GET /
GET /health
```

### Result

- FastAPI 서버 정상 실행 확인
- `/` API 응답 확인
- `/health` API에서 API 서버 상태 확인
- GitHub Repository push 완료
- README 및 study 문서 작성 완료

### Next

- PostgreSQL 연결 상태 확인 로직 추가
- `/health` API에 DB 상태 응답 추가

---

## 2026-07-04

### Type

`FEATURE`, `INFRA`, `CHECK`, `TROUBLESHOOTING`

### Summary

`/health` API에 PostgreSQL 연결 상태 확인 로직을 추가했다.  
Docker Compose로 PostgreSQL 컨테이너를 실행하고, DB 연결 성공·실패 상태가 Health Check 응답에 반영되는지 확인했다.

### Commands

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
docker compose up -d
docker ps
docker logs ops-monitor-db
docker stop ops-monitor-db
docker start ops-monitor-db
```

### Check

```text
GET /health
```

### Result

- PostgreSQL 미실행 상태에서 `database.status = disconnected` 확인
- Docker Desktop 설치 및 실행 완료
- Docker Compose로 PostgreSQL 컨테이너 실행 완료
- PostgreSQL 실행 상태에서 `database.status = connected` 확인
- PostgreSQL 컨테이너 중지 시 `disconnected` 확인
- PostgreSQL 컨테이너 재시작 후 `connected` 복구 확인

### Issue

Docker Compose 실행 시 Docker Desktop 엔진 미실행 오류가 발생했다.

```text
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
```

### Resolution

Docker Desktop을 실행한 뒤 Docker Engine 상태를 확인하고, 새 Git Bash 터미널에서 Docker Compose를 다시 실행했다.

### Next

- FastAPI 애플리케이션 Dockerfile 작성
- FastAPI를 Docker Compose 서비스에 추가
- Nginx Reverse Proxy 구성
- Docker Compose 설계서 및 API 명세서 업데이트

---

## 2026-07-05

### Type

`FEATURE`, `INFRA`, `CHECK`, `DOCS`

### Summary

FastAPI 애플리케이션을 컨테이너로 실행할 수 있도록 Dockerfile과 Docker Compose 구성을 확장했다.  
`/system` API와 `/dashboard` 페이지를 추가하고, Nginx Reverse Proxy 및 기본 보안 설정 문서를 정리했다.

### Commands

```bash
docker compose up --build -d
docker ps
uvicorn app.main:app --reload
git status
git log --oneline
```

### Check

```text
GET /
GET /health
GET /system
GET /dashboard
```

### Result

- FastAPI 컨테이너 실행 구조와 Docker Compose 멀티 서비스 구성을 정리
- `/system` API에서 메모리, 디스크 사용량 반환 구조 확인
- `/dashboard` 페이지에서 상태 조회 흐름 구성 완료
- Nginx가 `app:8000`으로 요청을 전달하는 Reverse Proxy 설정 반영
- CORS 제한과 Nginx 보안 헤더 적용
- 보안 설정 문서와 제출용 README 정리 완료

### Next

- 로그 조회 API와 장애 이력 API 설계
- Dashboard 데이터 구조 확장
- HTTPS 및 인증/인가 적용 범위 검토
