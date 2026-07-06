# Ops Monitor

Ops Monitor는 FastAPI, PostgreSQL, Docker Compose, Nginx를 기반으로 구성한 운영 모니터링 프로젝트입니다.  
서비스 상태 확인, DB 연결 점검, 시스템 자원 조회, 기본 보안 기준 적용 결과를 제출용 문서 형태로 정리했습니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트명 | Ops Monitor |
| 목적 | API, DB, 시스템 자원 상태를 통합 점검하는 운영 모니터링 구성 구현 |
| 구성 | Nginx, FastAPI, PostgreSQL, Docker Compose |
| 주요 산출물 | API, 대시보드, 인프라 설정, 설계 문서, 보안 문서 |

---

## 2. 구현 범위

| 구분 | 내용 | 상태 |
|---|---|---|
| API 상태 확인 | `/` 엔드포인트로 서버 실행 여부 확인 | 완료 |
| DB 상태 확인 | `/health`로 DB 연결 상태 확인 | 완료 |
| 시스템 자원 조회 | `/system`으로 메모리/디스크 사용량 조회 | 완료 |
| 운영 대시보드 | `/dashboard`에서 주요 상태 시각화 | 완료 |
| Reverse Proxy | Nginx를 통한 요청 전달 | 완료 |
| 기본 보안 설정 | CORS 제한, 보안 헤더, 민감정보 분리 | 완료 |

---

## 3. 시스템 구성

```text
Client
  ↓
Nginx Container
  ↓
FastAPI Container
  ↓
PostgreSQL Container
```

| 구성 요소 | 역할 |
|---|---|
| Nginx | 외부 요청 수신, Reverse Proxy, 보안 헤더 적용 |
| FastAPI | 상태 점검 API 및 대시보드 제공 |
| PostgreSQL | DB 연결 상태 점검 대상 |
| Docker Compose | 컨테이너 실행 및 의존 관계 관리 |

---

## 4. 주요 기능

| 기능 | 설명 |
|---|---|
| Health Check | API 정상 응답 여부와 DB 연결 상태를 함께 반환 |
| System Check | 메모리/디스크 사용량을 수치로 반환 |
| Dashboard | 상태 정보를 카드형 화면으로 표시 |
| Security Baseline | `.env` 분리, CORS 제한, 보안 헤더, 오류 메시지 단순화 적용 |

---

## 5. API 요약

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/` | API 서버 실행 확인 |
| GET | `/health` | API 및 DB 연결 상태 확인 |
| GET | `/system` | 메모리/디스크 사용량 조회 |
| GET | `/dashboard` | 운영 대시보드 페이지 |
| GET | `/docs` | Swagger UI |

### `/health` 응답 예시

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

### `/system` 응답 예시

```json
{
  "memory": {
    "total_gb": 0.0,
    "used_gb": 0.0,
    "percent": 0.0
  },
  "disk": {
    "total_gb": 0.0,
    "used_gb": 0.0,
    "percent": 0.0
  }
}
```

---

## 6. 실행 방법

### 6.1 사전 준비

- Python 3.11 이상
- Docker Desktop

### 6.2 환경변수 설정

`.env.example`을 참고해 `.env` 파일을 생성합니다.

```env
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASSWORD>
POSTGRES_DB=<DB_NAME>
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
DISCORD_WEBHOOK_URL=<DISCORD_WEBHOOK_URL>
MONITOR_INTERVAL_SECONDS=60
MEMORY_ALERT_THRESHOLD=80
DISK_ALERT_THRESHOLD=80
```

### 6.3 환경변수 관리 기준

| 항목 | 설정 방법 |
|---|---|
| `.env` 생성 | `.env.example`을 복사해 실제 값 입력 |
| DB 계정 정보 | 실행 환경의 실제 값 사용 |
| Discord Webhook URL | 실제 웹훅 URL을 `.env`에만 저장 |
| Git 관리 | `.env`는 업로드하지 않고 `.env.example`만 추적 |

주의 사항:
- 실제 `DISCORD_WEBHOOK_URL`은 README, 문서, 코드에 직접 작성하지 않습니다.
- `.env` 파일은 개인 로컬 또는 배포 환경에서만 관리합니다.
- 예시 파일에는 플레이스홀더만 유지합니다.

### 6.4 컨테이너 실행

```bash
docker compose up --build -d
```

### 6.5 접속 주소

| 주소 | 설명 |
|---|---|
| `http://localhost/` | 기본 진입 |
| `http://localhost/dashboard` | 운영 대시보드 |
| `http://localhost/health` | 헬스체크 |
| `http://localhost/system` | 시스템 상태 조회 |

### 6.6 로컬 실행

```bash
uvicorn app.main:app --reload
```

---

## 7. 보안 적용 사항

| 항목 | 적용 내용 |
|---|---|
| 환경변수 분리 | 실제 계정 정보와 연결 문자열은 `.env`에서 관리 |
| Git 제외 | `.env`는 추적 제외, `.env.example`만 포함 |
| Discord Webhook 보호 | 실제 웹훅 URL은 `.env`에만 저장 |
| CORS 제한 | `http://localhost`, `http://127.0.0.1`만 허용 |
| 허용 메서드 | `GET` 중심 제한 |
| Nginx 보안 헤더 | `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy` 적용 |
| 오류 메시지 관리 | 상세 DB 예외 대신 고정 메시지 사용 |

상세 기준은 [docs/07_security.md](docs/07_security.md)에서 관리합니다.

---

## 8. 문서 구성

| 문서 | 내용 |
|---|---|
| [01_srs.md](docs/01_srs.md) | 요구사항 정의 |
| [02_architecture.md](docs/02_architecture.md) | 시스템 아키텍처 설계 |
| [03_api_spec.md](docs/03_api_spec.md) | API 명세 |
| [04_erd.md](docs/04_erd.md) | 데이터 모델 설계 |
| [05_docker_compose_design.md](docs/05_docker_compose_design.md) | Docker Compose 구성 문서 |
| [06_troubleshooting.md](docs/06_troubleshooting.md) | 문제 해결 기록 |
| [07_security.md](docs/07_security.md) | 보안 설정 기준 |
| [operation-log.md](docs/operation-log.md) | 운영 확인 및 작업 로그 |

---

## 9. 저장소 구조

```text
ops-monitor/
├── app/
│   ├── api/
│   ├── services/
│   └── main.py
├── docs/
├── nginx/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 10. 커밋 컨벤션

```text
init: 프로젝트 초기 설정
feat: 기능 추가
infra: 인프라 설정 추가
docs: 문서 작성 및 수정
fix: 오류 수정
chore: 기타 설정 변경
ci: CI 설정
```
