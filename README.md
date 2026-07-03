# Ops Monitor

Docker 기반 서비스 운영 환경을 직접 구성하고, 장애 발생 시 로그 확인과 복구 흐름을 실습하기 위한 인프라 미니 프로젝트입니다.

FastAPI 애플리케이션, PostgreSQL 데이터베이스, Nginx Reverse Proxy를 Docker Compose로 구성하고, Health Check API와 로그 확인 기능을 통해 서비스 운영 관점의 기본 흐름을 구현하는 것을 목표로 합니다.

---

## 1. Project Overview

Ops Monitor는 서버 운영, 서비스 상태 점검, 장애 확인, 복구 과정을 직접 경험하기 위해 기획한 운영 모니터링 실습 프로젝트입니다.

단순히 API 기능을 구현하는 데 그치지 않고, 서비스가 실행되는 환경을 구성하고 문제가 발생했을 때 어떤 순서로 확인하고 복구할 수 있는지 정리하는 데 중점을 둡니다.

---

## 2. Project Goal

이 프로젝트의 목표는 서비스 운영 환경의 기본 구조를 직접 구성하고, 장애 상황을 확인·복구하는 흐름을 경험하는 것입니다.

주요 목표는 다음과 같습니다.

* FastAPI 기반 API 서버 구축
* PostgreSQL 데이터베이스 연동
* Docker Compose 기반 서비스 실행
* Nginx Reverse Proxy 구성
* Health Check API 구현
* 로그 확인을 통한 장애 원인 파악
* PostgreSQL 장애 상황 생성 및 복구 과정 문서화
* GitHub Actions 기반 기본 자동화 구성

---

## 3. Tech Stack

| Category        | Stack                  |
| --------------- | ---------------------- |
| OS              | Ubuntu Server          |
| Backend         | FastAPI                |
| Database        | PostgreSQL             |
| Web Server      | Nginx                  |
| Container       | Docker, Docker Compose |
| CI/CD           | GitHub Actions         |
| Version Control | Git, GitHub            |

---

## 4. System Architecture

```text
Client
  ↓
Nginx
  ↓
FastAPI
  ↓
PostgreSQL
```

Nginx는 외부 요청을 FastAPI 서버로 전달하는 Reverse Proxy 역할을 수행합니다.

FastAPI는 API 요청을 처리하고, PostgreSQL 연결 상태를 확인합니다.

PostgreSQL은 서비스 상태 확인 및 DB 장애 시나리오 실습을 위한 데이터베이스로 사용합니다.

---

## 5. Core Features

Ops Monitor는 서비스 운영 환경에서 필요한 기본 점검 흐름을 구현하는 것을 목표로 합니다.

* FastAPI 기반 API 서버 구성
* PostgreSQL 연결 상태 확인
* Docker Compose 기반 API, DB, Nginx 실행
* Nginx Reverse Proxy 적용
* Health Check API를 통한 API/DB 상태 확인
* 로그 확인을 통한 장애 원인 파악
* PostgreSQL 장애 발생 및 복구 과정 문서화
* GitHub Actions 기반 기본 자동화 구성

---

## 6. API

### Root API

```http
GET /
```

Response

```json
{
  "message": "Ops Monitor API is running"
}
```

### Health Check API

```http
GET /health
```

현재는 FastAPI 서버 상태를 확인합니다.

```json
{
  "api": "ok",
  "timestamp": "2026-07-03T00:00:00"
}
```

이후 PostgreSQL 연결 상태를 포함하여 API 서버와 DB 상태를 함께 확인할 수 있도록 확장할 예정입니다.

예상 응답 구조는 다음과 같습니다.

```json
{
  "api": "ok",
  "database": {
    "status": "connected",
    "message": "Database connection successful"
  },
  "timestamp": "2026-07-03T00:00:00"
}
```

---

## 7. Project Structure

```text
ops-monitor/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   └── models/
├── nginx/
│   └── default.conf
├── docs/
│   ├── 01_srs.md
│   ├── 02_architecture.md
│   ├── 03_api_spec.md
│   ├── 04_erd.md
│   ├── 05_docker_compose_design.md
│   ├── 06_nginx_design.md
│   ├── 07_github_actions.md
│   ├── 08_troubleshooting.md
│   └── operation-log.md
├── study/
│   ├── day01-project-setup.md
│   ├── git-basic.md
│   └── fastapi-basic.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 8. Failure Recovery Scenario

이 프로젝트에서는 PostgreSQL 장애 상황을 직접 생성하고, 로그 확인과 컨테이너 재시작을 통해 복구하는 흐름을 실습합니다.

예정된 장애 대응 흐름은 다음과 같습니다.

```text
1. PostgreSQL 컨테이너 중지
2. /health API 호출
3. DB 연결 실패 확인
4. docker logs 명령어로 로그 확인
5. PostgreSQL 컨테이너 재시작
6. /health API 재호출
7. DB 연결 정상 복구 확인
8. 장애 원인과 복구 과정을 문서화
```

장애 대응 기록은 `docs/08_troubleshooting.md`와 `docs/operation-log.md`에 정리합니다.

---

## 9. Operation Documentation

운영 과정에서 확인한 내용을 문서로 남겨 프로젝트의 흐름을 정리합니다.

| Document | Description |
|---|---|
| `docs/01_srs.md` | 기능 요구사항, 비기능 요구사항, 장애 대응 요구사항 정의 |
| `docs/02_architecture.md` | 현재 구성과 목표 아키텍처, 요청 흐름 정리 |
| `docs/03_api_spec.md` | API 엔드포인트와 응답 구조 정의 |
| `docs/04_erd.md` | 사용자, 로그, 장애 이력 테이블 설계 |
| `docs/05_docker_compose_design.md` | Docker Compose 서비스 구성 설계 |
| `docs/06_nginx_design.md` | Nginx Reverse Proxy 설정 방향 정리 |
| `docs/07_github_actions.md` | GitHub Actions 자동화 흐름 정리 |
| `docs/08_troubleshooting.md` | 프로젝트 진행 중 발생한 문제와 해결 과정 기록 |
| `docs/operation-log.md` | 날짜별 작업 내용과 운영 확인 결과 기록 |
---

## 10. Learning Points

이 프로젝트를 통해 다음 내용을 학습하고 정리합니다.

* Linux 기본 명령어
* FastAPI 서버 실행 구조
* PostgreSQL 연결 방식
* Docker 이미지 빌드 및 컨테이너 실행
* Docker Compose 기반 서비스 구성
* Nginx Reverse Proxy 설정
* Health Check API 설계
* 로그 기반 장애 확인
* 서비스 장애 복구 절차
* GitHub Actions 기반 자동화

---

## 11. Commit Convention

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
init: create FastAPI health check server
chore: add gitignore
docs: add initial README
feat: add database status check logic
infra: configure docker-compose
infra: configure Nginx reverse proxy
docs: add database failure recovery scenario
ci: add GitHub Actions workflow
```

---

## 12. Expected Outcome

최종적으로 이 프로젝트는 다음 내용을 보여주는 것을 목표로 합니다.

* Docker 기반 서비스 운영 환경 구성 경험
* API 서버와 DB 연결 상태 확인 경험
* Nginx Reverse Proxy 적용 경험
* Health Check API를 통한 서비스 상태 점검 경험
* 로그 확인을 통한 장애 원인 파악 경험
* DB 장애 발생 및 복구 과정 문서화 경험
* GitHub Actions를 활용한 기본 자동화 경험
