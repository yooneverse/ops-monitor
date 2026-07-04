# API 명세서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | API 명세서 |
| 프로젝트명 | Ops Monitor |
| 목적 | API 요청/응답 구조 및 상태값 정의 |
| 현재 구현 범위 | `/`, `/health` |
| 확장 예정 범위 | `/logs`, `/incidents` |

---

## 2. API 목록

| Method | Endpoint | 기능 | 상태 |
|---|---|---|---|
| GET | `/` | API 서버 실행 확인 | 완료 |
| GET | `/health` | API 서버 및 DB 연결 상태 확인 | 완료 |
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
| 상태 확인 방식 | `/health` 응답의 status 값으로 구분 |

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

### Response Field

| Field | Type | Description |
|---|---|---|
| message | string | API 서버 실행 메시지 |

---

## 5. GET `/health`

### 개요

API 서버 상태와 PostgreSQL 연결 상태를 확인한다.

### Request

```http
GET /health
```

### Response 200 - DB Connected

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

### Response 200 - DB Disconnected

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

### Response 200 - Environment Variable Error

```json
{
  "api": "ok",
  "database": {
    "status": "error",
    "message": "DATABASE_URL is not set"
  },
  "timestamp": "2026-07-04T22:23:48.969699"
}
```

### Response Field

| Field | Type | Description |
|---|---|---|
| api | string | API 서버 상태 |
| database.status | string | DB 연결 상태 |
| database.message | string | DB 연결 결과 메시지 |
| timestamp | string | 응답 생성 시각 |

### Status Definition

| Status | 의미 | 발생 조건 |
|---|---|---|
| connected | DB 연결 성공 | PostgreSQL 실행 및 연결 가능 |
| disconnected | DB 연결 실패 | PostgreSQL 중지 또는 연결 불가 |
| error | 설정 오류 | `DATABASE_URL` 누락 |

### 처리 기준

| 상황 | HTTP 응답 | api | database.status |
|---|---|---|---|
| API 정상, DB 정상 | 200 | ok | connected |
| API 정상, DB 중지 | 200 | ok | disconnected |
| API 정상, 환경변수 누락 | 200 | ok | error |
| API 서버 미실행 | 응답 없음 | - | - |

---

## 6. GET `/logs` 예정

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

### Response Field

| Field | Type | Description |
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

## 7. POST `/logs` 예정

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

## 8. GET `/incidents` 예정

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

### Response Field

| Field | Type | Description |
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

## 9. POST `/incidents` 예정

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

## 10. PATCH `/incidents/{incident_id}/recover` 예정

### 개요

장애 복구 내용을 기록하고 상태를 `RECOVERED`로 변경한다.

### Request

```http
PATCH /incidents/{incident_id}/recover
```

### Path Parameter

| Parameter | Type | Description |
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

## 11. 상태값 정의

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

## 12. 구현 상태

| 항목 | 상태 |
|---|---|
| Root API | 완료 |
| Health Check API | 완료 |
| DB 연결 상태 응답 | 완료 |
| DB 연결 실패 응답 | 완료 |
| 로그 조회 API | 예정 |
| 로그 생성 API | 예정 |
| 장애 이력 조회 API | 예정 |
| 장애 이력 생성 API | 예정 |
| 장애 복구 처리 API | 예정 |

---

## 13. 다음 작업

| 작업 | 설명 |
|---|---|
| 로그 테이블 반영 | ERD 기준으로 logs 테이블 구현 |
| 장애 이력 테이블 반영 | incidents 테이블 구현 |
| `/logs` API 구현 | 로그 조회 및 생성 기능 추가 |
| `/incidents` API 구현 | 장애 이력 생성, 조회, 복구 처리 기능 추가 |
| Swagger 확인 | FastAPI `/docs`와 명세서 일치 여부 점검 |