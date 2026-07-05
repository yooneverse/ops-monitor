# Ops Monitor

Ops Monitor는 FastAPI, PostgreSQL, Docker Compose, Nginx를 기반으로 구성한 운영 모니터링 실습 프로젝트입니다.  
서비스 상태 확인, DB 연결 점검, 시스템 자원 조회, 기본 보안 설정 문서화를 하나의 제출물 형태로 정리했습니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트명 | Ops Monitor |
| 프로젝트 유형 | 인프라 운영 및 모니터링 미니 프로젝트 |
| 주요 목적 | API 상태, DB 연결 상태, 시스템 자원 상태를 통합 확인 |
| 실행 구조 | Nginx + FastAPI + PostgreSQL |
| 문서 범위 | 요구사항, 아키텍처, API, ERD, Compose, 트러블슈팅, 보안 설정, 운영 기록 |

---

## 2. 핵심 기능

| 기능 | 설명 |
|---|---|
| Dashboard | `/dashboard`에서 운영 상태를 카드형 UI로 조회 |
| Health Check | `/health`에서 API 및 DB 연결 상태 확인 |
| System Check | `/system`에서 메모리/디스크 사용량 조회 |
| Reverse Proxy | Nginx를 통해 FastAPI 요청 전달 |
| Containerized Runtime | Docker Compose로 `nginx`, `app`, `db` 실행 |
| Security Baseline | `.env` 분리, CORS 제한, Nginx 보안 헤더, 민감정보 비노출 기준 적용 |

---

## 3. 시스템 아키텍처

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
| Nginx | Reverse Proxy, 보안 헤더 적용, 외부 요청 수신 |
| FastAPI | 상태 확인 API 및 대시보드 제공 |
| PostgreSQL | 상태 점검 대상 데이터베이스 |
| Docker Compose | 멀티 컨테이너 실행 및 의존 관계 관리 |

---

## 4. API 구성

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/` | API 서버 실행 확인 |
| GET | `/health` | API 상태 및 DB 연결 상태 확인 |
| GET | `/system` | 메모리/디스크 사용량 조회 |
| GET | `/dashboard` | 운영 대시보드 HTML 페이지 |
| GET | `/docs` | FastAPI Swagger UI |

### `/health` 응답 예시

```json
{
  "api": "ok",
  "database": {
    "status": "connected",
    "message": "Database connection successful"
  },
  "timestamp": "2026-07-05T16:00:00"
}
```

### `/system` 응답 예시

```json
{
  "memory": {
    "total_gb": 15.9,
    "used_gb": 6.31,
    "percent": 39.7
  },
  "disk": {
    "total_gb": 237.98,
    "used_gb": 101.22,
    "percent": 42.53
  }
}
```

---

## 5. 기술 스택

| Category | Stack |
|---|---|
| Backend | FastAPI, Uvicorn |
| Database | PostgreSQL 16 |
| ORM / DB Access | SQLAlchemy, psycopg2-binary |
| Infra | Docker, Docker Compose, Nginx |
| System Monitoring | psutil |
| Configuration | `.env`, `.env.example` |
| Documentation | Markdown |

---

## 6. 실행 방법

### 6.1 사전 준비

- Python 3.11+
- Docker Desktop

### 6.2 환경변수 설정

`.env.example`을 기준으로 `.env` 파일을 생성합니다.

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
DATABASE_URL=postgresql://your_db_user:your_db_password@db:5432/your_db_name
```

### 6.3 Docker Compose 실행

```bash
docker compose up --build -d
```

### 6.4 접속 주소

| 주소 | 설명 |
|---|---|
| `http://localhost/` | Nginx 경유 기본 진입 |
| `http://localhost/dashboard` | 운영 대시보드 |
| `http://localhost/health` | 헬스체크 |
| `http://localhost/system` | 시스템 상태 조회 |

### 6.5 로컬 개발 실행

컨테이너 대신 로컬에서 FastAPI만 실행하려면 아래 명령을 사용합니다.

```bash
uvicorn app.main:app --reload
```

---

## 7. 보안 기준

| 항목 | 적용 내용 |
|---|---|
| 민감정보 분리 | 실제 DB 계정 정보와 연결 문자열은 `.env`에서 관리 |
| Git 제외 | `.env`는 추적 제외, `.env.example`만 포함 |
| CORS 제한 | `http://localhost`, `http://127.0.0.1`만 허용 |
| 허용 메서드 | `GET` 중심 제한 |
| Nginx 보안 헤더 | `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy` 적용 |
| 오류 메시지 | 상세 DB 예외 대신 고정 메시지 사용 |

상세 기준은 [docs/09_security.md](docs/09_security.md)에서 관리합니다.

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
| [09_security.md](docs/09_security.md) | 보안 설정 기준 |
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

커밋 말머리는 영어, 설명은 한글 기준으로 작성합니다.

```text
init: 프로젝트 초기 설정
feat: 기능 추가
infra: 인프라 설정 추가
docs: 문서 작성 및 수정
fix: 오류 수정
chore: 기타 설정 변경
ci: CI 설정
```
