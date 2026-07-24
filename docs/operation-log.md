# 운영 작업 기록

## 기록 컨벤션

운영 작업 기록은 날짜별로 작성하고, 아래 항목을 기준으로 정리한다.

### 작성 형식

- 작업 일자: `YYYY-MM-DD`
- 작업 구분: `SETUP`, `FEATURE`, `INFRA`, `CHECK`, `TROUBLESHOOTING`, `DOCS`
- 작업 요약: 당일 핵심 작업을 1~2문장으로 정리
- 확인 명령어: 실제 수행한 명령어 기록
- 확인 결과: 정상 동작, 실패, 복구 여부 기록
- 다음 작업: 이후 진행할 작업 기록

### 작업 구분 기준

| Type | Description |
|---|---|
| SETUP | 프로젝트 초기 환경 구성 |
| FEATURE | API 또는 기능 구현 |
| INFRA | Docker, DB, Nginx, CI 등 인프라 구성 |
| CHECK | 실행 결과 및 상태 확인 |
| TROUBLESHOOTING | 오류 발생 및 해결 기록 |
| DOCS | 문서 작성 및 정리 |

---

## 2026-07-03

### Type

`SETUP`, `FEATURE`, `DOCS`

### Summary

Ops Monitor 프로젝트 기본 구조를 생성하고 FastAPI 서버와 `/health` API 초안을 구성했다.
Git 저장소 연결, `.gitignore` 설정, README와 학습 문서 초안을 함께 정리했다.

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
- `/` 응답 확인
- `/health` API 기본 응답 확인
- GitHub 저장소 push 완료
- README 및 study 문서 초안 작성 완료

### Next

- PostgreSQL 연결 상태 확인 로직 추가
- `/health` API에 DB 상태 응답 확장

---

## 2026-07-04

### Type

`FEATURE`, `INFRA`, `CHECK`, `TROUBLESHOOTING`

### Summary

`/health` API에 PostgreSQL 연결 상태 확인 로직을 추가했다.  
Docker Compose로 PostgreSQL 컨테이너를 실행하고, DB 연결 성공과 실패 상태가 Health Check에 반영되는지 확인했다.

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
- PostgreSQL 컨테이너 중지 후 `disconnected` 확인
- PostgreSQL 컨테이너 재시작 후 `connected` 복구 확인

### Issue

Docker Compose 실행 시 Docker Engine 미실행 오류가 발생했다.

```text
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
```

### Resolution

Docker Desktop을 실행한 뒤 Docker Engine 상태를 확인하고, 다시 Compose 명령을 수행해 해결했다.

### Next

- FastAPI 애플리케이션 Dockerfile 작성
- FastAPI를 Docker Compose 서비스에 추가
- Nginx Reverse Proxy 구성
- Docker Compose 설계 및 API 명세 업데이트

---

## 2026-07-05

### Type

`FEATURE`, `INFRA`, `CHECK`, `DOCS`

### Summary

FastAPI 애플리케이션을 컨테이너로 실행할 수 있도록 Dockerfile과 Docker Compose 구성을 확장했다.  
`/system` API와 `/dashboard` 페이지를 추가하고, Nginx Reverse Proxy와 기본 보안 설정 문서를 정리했다.

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

- FastAPI 컨테이너 실행 구조와 Docker Compose 서비스 구성을 정리
- `/system` API에서 메모리와 디스크 사용량 반환 구조 확인
- `/dashboard` 페이지에서 상태 조회 화면 구성 완료
- Nginx가 `app:8000`으로 요청을 전달하는 Reverse Proxy 설정 반영
- CORS 제한과 Nginx 보안 헤더 적용
- 보안 설정 문서와 제출용 README 정리 완료

### Next

- 로그 조회 API와 알림 이력 API 설계
- Dashboard 데이터 구조 확장
- HTTPS 및 인증/인가 적용 범위 검토

---

## 2026-07-06

### Type

`FEATURE`, `INFRA`, `CHECK`, `TROUBLESHOOTING`, `DOCS`

### Summary

Discord Webhook 기반 알림 전송 구조와 백그라운드 모니터링 루프를 정리하고, `/alerts`, `/monitoring/status` 조회 범위를 확장했다.
GitHub Actions CI를 추가해 Python import, Compose 설정, Docker build를 검증하도록 구성했고, runner 환경에서 발생한 Compose 명령 차이도 보완했다.

### Commands

```bash
python -m compileall app
python -c "from app.main import app; print(app.title)"
docker-compose config
docker build -t ops-monitor-ci .
git status
git log --oneline
```

### Check

```text
GET /alerts
GET /monitoring/status
GitHub Actions CI / validate
```

### Result

- Discord Webhook 기반 알림 전송 서비스 추가
- 백그라운드 모니터링 루프와 상태 조회 API 구성
- 최근 알림 이력 조회 API와 Dashboard 연동 구조 확장
- `.env`, `.env.example`, `.gitignore` 기준으로 환경변수 관리 방식 재정리
- GitHub Actions에서 Python compile, FastAPI import, Compose config, Docker build 검증 구성
- CI 실패 원인이 `docker-compose`와 `docker compose` 실행 환경 차이였음을 확인하고 fallback 방식으로 수정
- README, 보안 문서, 학습 문서, 운영 로그 정리 반영

### Issue

GitHub Actions `CI / validate` 단계에서 Compose 검증 명령이 runner 환경과 맞지 않아 실패했다.

```text
All checks have failed
CI / validate (push)
```

### Resolution

CI 워크플로에서 `docker-compose`가 있으면 해당 명령을 사용하고, 없으면 `docker compose`로 fallback 하도록 수정했다.

### Next

- CI에 테스트 코드 또는 API smoke check 추가 검토
- Discord 알림 조건 세분화와 재전송 기준 정리
- 운영 문서와 제출 문서 간 역할 구분 보완

---

## 2026-07-07

### Type

`FEATURE`, `INFRA`, `CHECK`, `DOCS`

### Summary

알림 로직을 실제 장애 시나리오 기준으로 보완하고, 로컬에서도 재현 가능한 장애 테스트 기준을 정리했다.
GitHub Actions 트리거 범위를 정제하고, Dependency Graph와 CI workflow의 차이 및 `app/requirements.txt` 처리 기준까지 문서화했다.

### Commands

```bash
python -m compileall app
python -c "from app.main import app; print(app.title)"
docker stop ops-monitor-db
docker start ops-monitor-db
docker compose up -d --force-recreate app
docker compose up -d --build app
git status
git log --oneline
```

### Check

```text
GET /health
GET /alerts
GET /monitoring/status
GET /dashboard
```

### Result

- DB 초기 장애 상태도 `incident`로 감지하도록 모니터링 로직 보완
- 메모리 및 디스크 임계치 초과 이후 `resource_recovery` 알림 추가
- Discord Webhook 전송 실패 시 `notification_error` 이력 기록 추가
- `.env` 변경 후 DB 연결 테스트가 가능하도록 DB 설정 재조회 방식으로 수정
- Dashboard에 신규 알림 타입 스타일 반영
- CI를 `main`, `pull_request`, `workflow_dispatch` 기준으로 정제하고 코드/인프라 변경 시에만 실행되도록 `paths` 적용
- `app/requirements.txt`는 프로젝트 기준 의존성 파일이 아니라고 판단해 `.gitignore`로 정리
- 로컬 장애 테스트 시나리오와 CI/Dependency Graph 구분 내용을 학습 문서로 정리
- DB 컨테이너 중지 후 `/health = disconnected`, `/alerts = incident` 흐름 실측 확인
- DB 복구 후 `/health = connected`, `/alerts = recovery` 흐름 실측 확인
- 잘못된 Webhook URL과 낮은 threshold 설정에서 `resource_alert`와 `notification_error` 동시 기록 확인
- 정상 Webhook + 낮은 메모리 threshold 설정에서 `resource_alert` 생성 및 전송 실패 이력 없음 확인
- `.env` 변경은 단순 `docker restart`가 아니라 `docker compose up -d --force-recreate app`로 반영된다는 점 확인
- 최신 알림 로직 검증에는 `docker compose up -d --build app`으로 이미지 재빌드가 필요함을 확인

### Issue

알림 테스트를 컨테이너 중지/재시작만으로 보게 되면 운영 시나리오 설명 범위가 좁고, 중복 알림/복구 알림/전송 실패 처리 기준이 드러나지 않았다.

### Resolution

DB 연결 실패, Webhook 전송 실패, 임계치 초과, 복구, 중복 알림 방지 관점으로 로컬 테스트 기준을 분리하고 관련 로직을 코드에 반영했다.

실제 재현 과정에서는 DB 컨테이너 중지/복구, 테스트용 `.env` 변경, 앱 컨테이너 재생성, 이미지 재빌드까지 포함해 검증 흐름을 정리했다.

### Next

- API 테스트 또는 smoke test 추가
- 중복 알림 제한 정책을 시간 기준으로 확장 검토
- 운영 로그에 실제 장애 재현 결과 추가 기록

---

## 2026-07-21

### Type

`FEATURE`, `INFRA`, `CHECK`, `TROUBLESHOOTING`, `DOCS`

### Summary

운영 대시보드를 콘솔형 관리자 화면 기준으로 정제하고, `demo-notes`를 실제 운영 대상 서비스처럼 연결했다.
작업 중 로컬 실행과 Compose 실행의 DB host 차이, `notes` 컨테이너 환경변수 치환 오류, 빈 상태와 실패 상태 구분 부족 문제를 함께 해결했다.

### Commands

```bash
docker ps -a
docker logs ops-monitor-notes
docker-compose up -d --build notes
.venv\Scripts\python.exe -m unittest tests.test_demo_notes_app tests.test_runtime_hardening
```

### Check

```text
GET /dashboard
GET /health
GET http://localhost:8010
GET http://localhost:8010/healthz
```

### Result

- 대시보드를 한글 콘솔형 운영 화면 기준으로 재정리
- `demo-notes` 메모 생성, 수정, 삭제 흐름과 PostgreSQL 저장 구조 반영
- 로컬 직접 실행 시 `db` host를 `localhost`로 보정하는 기준 추가
- `notes` 컨테이너의 `DEMO_NOTES_DATABASE_URL` 치환 오류 수정
- `ops-monitor-notes` 컨테이너 `healthy` 상태와 `http://localhost:8010` 응답 복구 확인
- 메모가 없는 상태와 저장소 연결 실패 상태를 UI에서 분리
- 관련 문서와 스터디 문서 정리

### Issue

브라우저에서는 `ERR_EMPTY_RESPONSE`처럼 보였지만, 실제 원인은 `demo-notes` 컨테이너의 DB 인증 실패와 재시작 루프였다.

동시에 로컬 직접 실행 환경에서는 `db` host 해석 실패도 별도로 존재했다.

### Resolution

컨테이너 로그와 포트 상태를 먼저 확인해 브라우저 증상과 실제 원인을 분리했다.

그 뒤 Compose 환경변수 치환을 수정하고, 코드에서는 로컬/컨테이너 실행 차이를 흡수하도록 DB URL 보정 로직을 추가했다.

또한 빈 데이터와 연결 실패를 화면에서 구분하도록 메모 서비스의 오류 표현을 정리했다.

### Next

- `demo-notes` 인증 또는 권한 모델 검토
- 메모 서비스 마이그레이션 체계 검토
- 운영 액션 증가 시 감사 로그 범위 검토
