<div align="center">
  <h1>Ops Monitor</h1>
  <p>Docker 컨테이너 기반 서비스 모니터링 프로젝트</p>
  <img src="docs/assets/ops-monitor-wordmark-main.png" alt="Ops Monitor" width="460" />
  <br />
  <br />
  <p>
    <code>FastAPI</code>
    <code>PostgreSQL</code>
    <code>Docker Compose</code>
    <code>Nginx</code>
  </p>
</div>

---

## 1. 프로젝트 개요

Ops Monitor는 서비스가 정상 동작하는지 확인하고, 장애 징후를 빠르게 파악하며, 운영 로그를 날짜별로 남기는 과정을 직접 구현해 보기 위해 만든 프로젝트입니다.

- 공개 상태 확인 API와 보호된 운영 조회 API를 분리했습니다.
- DB 상태, 시스템 자원, 이벤트 이력을 한곳에서 확인할 수 있습니다.
- 운영 중 필요한 기본 보안 설정과 일일 로그 정리를 함께 다룹니다.

## 2. 커밋 원칙

```text
init   : 프로젝트 초기 설정
feat   : 기능 추가
infra  : 인프라 및 실행 환경 변경
test   : 테스트 추가 또는 보강
docs   : 문서 작성 및 수정
fix    : 오류 수정
chore  : 기타 정리
ci     : CI 설정 변경
```

## 3. 아키텍처

<div align="center">
  <img src="docs/assets/ops-monitor-architecture-simple.png" alt="Ops Monitor Architecture" width="920" />
</div>

전체 흐름은 단순하게 구성했습니다.

- 사용자의 요청은 `Nginx`를 거쳐 `FastAPI`로 전달됩니다.
- 애플리케이션은 상태 조회 API, 대시보드, 모니터링 루프를 제공합니다.
- 이벤트와 로그는 날짜별 파일로 정리되고, 필요 시 알림 채널로 전송됩니다.

### 구성 요소

| 구성 요소 | 역할 |
|---|---|
| Nginx | 요청 전달, 기본 보안 헤더, 접근 제한 |
| FastAPI | 상태 조회 API, 대시보드, 운영 기능 제공 |
| PostgreSQL | 연결 상태 확인 및 예시 데이터 저장 |
| Monitoring Loop | 주기적 상태 점검과 이벤트 생성 |
| Alert Channel | 장애 및 복구 알림 전송 |
| Daily Logs | 날짜별 로그와 리포트 생성 |

## 4. 주요 기능

| 구분 | 내용 |
|---|---|
| Public Health | `/`, `/livez`, `/readyz` |
| Protected Ops API | `/health`, `/system`, `/alerts`, `/monitoring/status` |
| Dashboard | `/dashboard` |
| Monitoring | DB 상태, 메모리, 디스크, 이벤트 점검 |
| Alerts | 웹훅 기반 장애 및 복구 알림 |
| Logging | 애플리케이션 로그, 이벤트 로그, 일일 리포트 생성 |
| Security | Basic Auth, Trusted Host, rate limit, 숨김 경로 차단 |

## 5. 주소 정리

### 공개 주소

| Method | Path | 설명 |
|---|---|---|
| GET | `/` | 기본 확인 |
| GET | `/livez` | 프로세스 생존 확인 |
| GET | `/readyz` | 준비 상태 확인 |

### 보호된 주소

| Method | Path | 설명 |
|---|---|---|
| GET | `/health` | 앱 및 DB 상태 |
| GET | `/system` | 시스템 자원 상태 |
| GET | `/alerts` | 최근 이벤트 이력 |
| GET | `/monitoring/status` | 모니터링 루프 상태 |
| GET | `/dashboard` | 운영 대시보드 |

## 6. 보안과 로그

### 보안

- Basic Auth로 운영용 조회 주소를 보호합니다.
- 인증 정보가 없으면 보호된 기능은 열리지 않도록 구성했습니다.
- 허용된 `Host`만 통과하도록 제한합니다.
- Nginx에서 method 제한, rate limit, 숨김 경로 차단을 적용합니다.

### 로그

| 경로 | 설명 |
|---|---|
| `logs/application/YYYY-MM-DD.log` | 애플리케이션 로그 |
| `logs/access/YYYY-MM-DD.log` | 접근 로그 |
| `logs/events/YYYY-MM-DD.jsonl` | 이벤트 원본 로그 |
| `logs/reports/YYYY-MM-DD.md` | 일일 리포트 |

## 7. 문서 모음

### 설계 및 기록 문서

| 문서 | 내용 |
|---|---|
| [01_srs.md](docs/01_srs.md) | 요구사항 정리 |
| [02_architecture.md](docs/02_architecture.md) | 아키텍처 설명 |
| [03_api_spec.md](docs/03_api_spec.md) | API 명세 |
| [04_erd.md](docs/04_erd.md) | 데이터 모델 |
| [05_docker_compose_design.md](docs/05_docker_compose_design.md) | Compose 설계 |
| [06_troubleshooting.md](docs/06_troubleshooting.md) | 문제 해결 기록 |
| [07_security.md](docs/07_security.md) | 기본 보안 정리 |
| [08_runtime_security.md](docs/08_runtime_security.md) | 런타임 보안 보강 |
| [operation-log.md](docs/operation-log.md) | 작업 기록 |
