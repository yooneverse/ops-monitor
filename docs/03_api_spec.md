# API 명세서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | API 명세서 |
| 프로젝트명 | Ops Monitor |
| 목적 | API 요청/응답 구조 및 상태값 정의 |
| 현재 구현 범위 | `/`, `/livez`, `/readyz`, `/health`, `/system`, `/alerts`, `/monitoring/status`, `/dashboard`, `/admin/database/restart` |
| 연계 서비스 범위 | `demo-notes`의 `/`, `/healthz`, `/api/notes` |

---

## 2. API 목록

| Method | Endpoint | 기능 | 상태 |
|---|---|---|---|
| GET | `/` | API 서버 실행 확인 | 완료 |
| GET | `/livez` | 프로세스 생존 확인 | 완료 |
| GET | `/readyz` | 준비 상태 확인 | 완료 |
| GET | `/health` | API 서버, DB, 메모 서비스 상태 확인 | 완료 |
| GET | `/system` | 메모리, 디스크 상태 확인 | 완료 |
| GET | `/alerts` | 최근 알림 이력 조회 | 완료 |
| GET | `/monitoring/status` | 모니터링 루프와 설정 상태 확인 | 완료 |
| GET | `/dashboard` | 운영 대시보드 화면 조회 | 완료 |
| POST | `/admin/database/restart` | DB 재시작 요청 | 완료 |
| GET | `/logs` | 로그 목록 조회 | 예정 |
| POST | `/logs` | 로그 생성 | 예정 |
| GET | `/incidents` | 장애 이력 목록 조회 | 예정 |
| POST | `/incidents` | 장애 이력 생성 | 예정 |
| PATCH | `/incidents/{incident_id}/recover` | 장애 복구 처리 | 예정 |

---

## 3. 공통 기준

| 항목 | 기준 |
|---|---|
| 응답 형식 | JSON |
| 시간 형식 | ISO 8601 |
| 민감정보 | 응답에 포함하지 않음 |
| 오류 메시지 | 내부 오류 원문 대신 정의된 메시지 반환 |
| 상태 확인 방식 | `/health`, `/readyz`, `/monitoring/status` 응답으로 구분 |
| 인증 기준 | 운영 API와 대시보드는 Basic Auth 필요 |

---

## 4. GET `/`

### 개요

API 서버 실행 여부를 확인한다.

### Request

```http
GET /
```

### Response 200

```json
{
  "message": "Ops Monitor API is running"
}
```

### 응답 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| message | string | API 서버 실행 메시지 |

---

## 5. GET `/livez`

### 개요

프로세스가 살아 있는지 확인한다.

### Request

```http
GET /livez
```

### Response 200

```json
{
  "status": "ok",
  "timestamp": "2026-07-21T21:00:00"
}
```

---

## 6. GET `/readyz`

### 개요

DB 연결 가능 여부를 기준으로 준비 상태를 반환한다.

### Request

```http
GET /readyz
```

### Response 200

```json
{
  "status": "ready",
  "timestamp": "2026-07-21T21:00:00"
}
```

### Response 503

```json
{
  "status": "not_ready",
  "timestamp": "2026-07-21T21:00:00"
}
```

---

## 7. GET `/health`

### 개요

API 서버 상태와 PostgreSQL 연결 상태를 확인한다.

### Request

```http
GET /health
```

### Response 200 - 정상 연결

```json
{
  "api": "ok",
  "database": {
    "status": "connected",
    "message": "Database connection successful"
  },
  "demo_notes": {
    "status": "connected",
    "message": "Demo notes service is available"
  },
  "timestamp": "2026-07-21T21:00:00"
}
```

### Response 200 - DB 연결 실패

```json
{
  "api": "ok",
  "database": {
    "status": "disconnected",
    "message": "Database connection failed"
  },
  "demo_notes": {
    "status": "disconnected",
    "message": "Demo notes service is unavailable"
  },
  "timestamp": "2026-07-21T21:00:00"
}
```

### Response 200 - 설정 누락

```json
{
  "api": "ok",
  "database": {
    "status": "error",
    "message": "DATABASE_URL is not set"
  },
  "demo_notes": {
    "status": "disabled",
    "message": "DEMO_NOTES_URL is not set"
  },
  "timestamp": "2026-07-21T21:00:00"
}
```

### 응답 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| api | string | API 서버 상태 |
| database.status | string | DB 연결 상태 |
| database.message | string | DB 연결 결과 메시지 |
| demo_notes.status | string | 메모 서비스 연결 상태 |
| demo_notes.message | string | 메모 서비스 연결 결과 메시지 |
| timestamp | string | 응답 생성 시각 |

### 상태 정의

| 상태값 | 의미 | 발생 조건 |
|---|---|---|
| connected | DB 연결 성공 | PostgreSQL 실행 및 연결 가능 |
| disconnected | DB 연결 실패 | PostgreSQL 중지 또는 연결 불가 |
| error | 설정 오류 | `DATABASE_URL` 누락 |
| disabled | 서비스 비활성화 | `DEMO_NOTES_URL` 미설정 |

### 처리 기준

| 상황 | HTTP 응답 | api | database.status |
|---|---|---|---|
| API 정상, DB 정상 | 200 | ok | connected |
| API 정상, DB 중지 | 200 | ok | disconnected |
| API 정상, 환경변수 누락 | 200 | ok | error |
| API 서버 미실행 | 응답 없음 | - | - |

---

## 8. GET `/system`

### 개요

현재 시스템 자원 사용량을 반환한다.

### 주요 응답 필드

- `memory.percent`
- `disk.percent`
- `timestamp`

---

## 9. GET `/alerts`

### 개요

최근 장애, 복구, 자원 경고 이력을 반환한다.

### 주요 응답 필드

- `type`
- `target`
- `message`
- `created_at`

---

## 10. GET `/monitoring/status`

### 개요

모니터링 루프 활성 상태와 운영 설정 메타데이터를 반환한다.

### 주요 응답 필드

- `enabled`
- `interval_seconds`
- `discord_webhook_configured`
- `monitor_auth_configured`
- `api_docs_enabled`
- `thresholds.memory_percent`
- `thresholds.disk_percent`
- `config_warnings`
- `last_check`

---

## 11. GET `/dashboard`

### 개요

운영자가 브라우저에서 확인하는 한글 관리자 대시보드 화면을 반환한다.

---

## 12. POST `/admin/database/restart`

### 개요

운영 화면에서 DB 재시작을 요청한다.

### Response 200

```json
{
  "status": "ok",
  "message": "DB 재시작 요청을 보냈습니다."
}
```

### Response 503

```json
{
  "status": "error",
  "message": "DB 재시작에 실패했습니다."
}
```

---

## 13. GET `/logs` 예정

### 개요

서비스 실행 로그와 오류 로그를 조회한다.

### Request

```http
GET /logs
```

### Target Response 200

```json
[
  {
    "id": 1,
    "level": "INFO",
    "message": "Health check requested",
    "source": "health_api",
    "created_at": "2026-07-04T22:40:00"
  }
]
```

### 응답 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| id | integer | 로그 ID |
| level | string | 로그 레벨 |
| message | string | 로그 메시지 |
| source | string | 로그 발생 위치 |
| created_at | string | 로그 생성 시각 |

### level

| Value | 의미 |
|---|---|
| INFO | 일반 실행 정보 |
| WARNING | 주의 필요 |
| ERROR | 오류 발생 |

---

## 14. POST `/logs` 예정

### 개요

서비스 실행 또는 오류 로그를 생성한다.

### Request

```http
POST /logs
```

### Target Request Body

```json
{
  "level": "INFO",
  "message": "Health check requested",
  "source": "health_api"
}
```

### Target Response 201

```json
{
  "id": 1,
  "level": "INFO",
  "message": "Health check requested",
  "source": "health_api",
  "created_at": "2026-07-04T22:40:00"
}
```

---

## 15. GET `/incidents` 예정

### 개요

장애 발생 및 복구 이력을 조회한다.

### Request

```http
GET /incidents
```

### Target Response 200

```json
[
  {
    "id": 1,
    "title": "PostgreSQL connection failed",
    "status": "RECOVERED",
    "severity": "HIGH",
    "cause": "PostgreSQL container stopped",
    "recovery_action": "Restarted PostgreSQL container",
    "occurred_at": "2026-07-04T22:35:00",
    "recovered_at": "2026-07-04T22:40:00"
  }
]
```

### 응답 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| id | integer | 장애 이력 ID |
| title | string | 장애 제목 |
| status | string | 장애 상태 |
| severity | string | 장애 심각도 |
| cause | string | 장애 원인 |
| recovery_action | string | 복구 조치 |
| occurred_at | string | 장애 발생 시각 |
| recovered_at | string | 장애 복구 시각 |

---

## 16. POST `/incidents` 예정

### 개요

장애 발생 이력을 생성한다.

### Request

```http
POST /incidents
```

### Target Request Body

```json
{
  "title": "PostgreSQL connection failed",
  "severity": "HIGH",
  "cause": "PostgreSQL container stopped"
}
```

### Target Response 201

```json
{
  "id": 1,
  "title": "PostgreSQL connection failed",
  "status": "OPEN",
  "severity": "HIGH",
  "cause": "PostgreSQL container stopped",
  "occurred_at": "2026-07-04T22:35:00",
  "recovered_at": null
}
```

---

## 17. PATCH `/incidents/{incident_id}/recover` 예정

### 개요

장애 복구 내용을 기록하고 상태를 `RECOVERED`로 변경한다.

### Request

```http
PATCH /incidents/{incident_id}/recover
```

### 경로 파라미터

| 파라미터 | 타입 | 설명 |
|---|---|---|
| incident_id | integer | 장애 이력 ID |

### Target Request Body

```json
{
  "recovery_action": "Restarted PostgreSQL container"
}
```

### Target Response 200

```json
{
  "id": 1,
  "title": "PostgreSQL connection failed",
  "status": "RECOVERED",
  "severity": "HIGH",
  "cause": "PostgreSQL container stopped",
  "recovery_action": "Restarted PostgreSQL container",
  "occurred_at": "2026-07-04T22:35:00",
  "recovered_at": "2026-07-04T22:40:00"
}
```

---

## 18. 상태값 정의

### incidents.status

| Value | 의미 |
|---|---|
| OPEN | 장애 발생 |
| RECOVERED | 복구 완료 |

### incidents.severity

| Value | 의미 |
|---|---|
| LOW | 낮은 영향도 |
| MEDIUM | 일부 기능 영향 |
| HIGH | 주요 기능 영향 |

---

## 19. 구현 상태

| 항목 | 상태 |
|---|---|
| Root API | 완료 |
| Liveness API | 완료 |
| Readiness API | 완료 |
| Health Check API | 완료 |
| 시스템 상태 API | 완료 |
| 최근 알림 API | 완료 |
| 모니터링 상태 API | 완료 |
| 대시보드 화면 | 완료 |
| DB 재시작 요청 API | 완료 |
| 로그 조회 API | 예정 |
| 로그 생성 API | 예정 |
| 장애 이력 조회 API | 예정 |
| 장애 이력 생성 API | 예정 |
| 장애 복구 처리 API | 예정 |

---

## 20. 다음 작업

| 작업 | 설명 |
|---|---|
| 로그 테이블 반영 | ERD 기준으로 logs 테이블 구현 |
| 장애 이력 테이블 반영 | incidents 테이블 구현 |
| `/logs` API 구현 | 로그 조회 및 생성 기능 추가 |
| `/incidents` API 구현 | 장애 이력 생성, 조회, 복구 처리 기능 추가 |
| Swagger 확인 | FastAPI `/docs`와 명세서 일치 여부 점검 |
