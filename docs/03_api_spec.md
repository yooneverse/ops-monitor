# API 명세서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | API 명세서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 공개 프로브, 보호 API, 운영 액션 응답 구조를 정리 |
| 인증 기준 | 운영 API는 Basic Auth 보호 |

---

## 2. 공통 원칙

### 2.1 응답 형식

- 기본 응답 형식은 JSON
- 시각 값은 ISO 8601
- 내부 상세 예외 원문은 API 응답에 그대로 노출하지 않음

### 2.2 엔드포인트 분류

| 구분 | 엔드포인트 |
|---|---|
| 공개 프로브 | `/`, `/livez`, `/readyz` |
| 보호된 운영 API | `/health`, `/system`, `/alerts`, `/monitoring/status`, `/dashboard`, `/admin/database/restart` |

### 2.3 인증 기준

운영 API는 `MONITOR_USERNAME`, `MONITOR_PASSWORD`가 설정된 경우 Basic Auth가 필요하다.

- 인증 누락 또는 불일치: `401 Unauthorized`
- 인증 설정 자체가 없음: `503 Service Unavailable`

---

## 3. 공개 프로브

### 3.1 `GET /`

기본 실행 여부를 확인한다.

```json
{
  "message": "Ops Monitor API is running"
}
```

### 3.2 `GET /livez`

프로세스 생존 여부를 확인한다.

```json
{
  "status": "ok",
  "timestamp": "2026-08-04T10:00:00"
}
```

### 3.3 `GET /readyz`

DB 연결 기준으로 준비 상태를 확인한다.

성공:

```json
{
  "status": "ready",
  "timestamp": "2026-08-04T10:00:00"
}
```

실패:

```json
{
  "status": "not_ready",
  "timestamp": "2026-08-04T10:00:00"
}
```

---

## 4. 보호된 운영 API

### 4.1 `GET /health`

API, DB, 부가 서비스 상태를 함께 반환한다.

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
  "timestamp": "2026-08-04T10:00:00"
}
```

### 4.2 `GET /system`

메모리와 디스크 사용량을 반환한다.

```json
{
  "memory": {
    "total_gb": 31.92,
    "used_gb": 12.41,
    "percent": 38.9
  },
  "disk": {
    "total_gb": 476.11,
    "used_gb": 211.54,
    "percent": 44.43
  }
}
```

### 4.3 `GET /alerts`

최근 이벤트 이력을 반환한다.

예시:

```json
[
  {
    "type": "incident",
    "target": "database",
    "status": "disconnected",
    "message": "Database connection failed",
    "timestamp": "2026-08-04T10:10:00"
  },
  {
    "type": "admin_action",
    "target": "database_restart",
    "status": "completed",
    "message": "Container restarted",
    "timestamp": "2026-08-04T10:11:00",
    "requested_by": "ops-admin"
  }
]
```

### 4.4 `GET /monitoring/status`

모니터링 루프 상태와 설정 메타데이터를 반환한다.

```json
{
  "enabled": true,
  "interval_seconds": 30,
  "discord_webhook_configured": false,
  "monitor_auth_configured": true,
  "api_docs_enabled": false,
  "thresholds": {
    "memory_percent": 80,
    "disk_percent": 80
  },
  "config_warnings": [],
  "active_targets": [
    "database"
  ],
  "excluded_targets": [
    "demo_notes"
  ],
  "target_warnings": [],
  "last_check": "2026-08-04T10:15:00"
}
```

#### 필드 설명

| 필드 | 설명 |
|---|---|
| `active_targets` | 실제로 점검 중인 대상 |
| `excluded_targets` | 설정으로 제외된 대상 |
| `target_warnings` | 알 수 없는 제외 대상 등 점검 대상 관련 경고 |
| `config_warnings` | 잘못된 수치형 설정 등 런타임 설정 경고 |

### 4.5 `GET /dashboard`

HTML 운영 화면을 반환한다.  
대시보드는 아래 정보를 한 화면에서 제공한다.

- 서비스 상태
- 자원 상태
- 최근 알림
- 설정 경고
- 활성/제외 대상 정보
- 관리자 액션 실행 버튼

---

## 5. 운영 액션 API

### 5.1 `POST /admin/database/restart`

DB 재시작을 요청한다.

성공 예시:

```json
{
  "status": "ok",
  "message": "DB restart command sent",
  "action": "restart_database",
  "requested_by": "ops-admin",
  "timestamp": "2026-08-04T10:20:00"
}
```

실패 예시:

```json
{
  "status": "error",
  "message": "Docker CLI를 찾을 수 없습니다.",
  "action": "restart_database",
  "requested_by": "ops-admin",
  "timestamp": "2026-08-04T10:20:00"
}
```

#### 응답 필드

| 필드 | 설명 |
|---|---|
| `status` | `ok` 또는 `error` |
| `message` | 조치 결과 메시지 |
| `action` | 수행한 운영 액션 식별자 |
| `requested_by` | 인증된 수행자 |
| `timestamp` | 액션 처리 시각 |

---

## 6. 상태값 기준

### 6.1 서비스 상태

| 값 | 의미 |
|---|---|
| `connected` | 기대 상태 |
| `disconnected` | 기대 상태에서 벗어남 |
| `disabled` | 명시적으로 비활성 또는 제외 대상 |
| `error` | 설정 또는 점검 불가 상태 |

### 6.2 이벤트 타입

| 타입 | 의미 |
|---|---|
| `incident` | 정상에서 비정상으로 전이 |
| `recovery` | 비정상에서 정상으로 전이 |
| `resource_alert` | 자원 임계치 초과 |
| `resource_recovery` | 자원 임계치 회복 |
| `notification_error` | 외부 알림 채널 전송 실패 |
| `admin_action` | 운영 액션 성공 |
| `admin_action_error` | 운영 액션 실패 |

---

## 7. 설계 메모

이 API 명세는 단순 CRUD 문서가 아니라 운영 흐름 문서에 가깝다.

중요한 이유는 다음과 같다.

- 공개 프로브와 보호 API의 경계가 아키텍처 핵심이기 때문
- 운영 액션은 일반 데이터 수정 API와 성격이 다르기 때문
- 모니터링 상태 응답에는 "현재 값"보다 "점검 범위와 경고"가 더 중요하기 때문

---

## 8. 관련 문서

| 문서 | 설명 |
|---|---|
| `docs/01_srs.md` | 요구사항 |
| `docs/02_architecture.md` | 구조와 설계 이유 |
| `docs/07_security.md` | 보안 정책 |
| `docs/10_runtime_configuration.md` | 설정 검증 기준 |
