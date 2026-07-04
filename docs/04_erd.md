# ERD 설계서

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | ERD 설계서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 운영 모니터링 및 장애 대응 기록을 위한 데이터 구조 정의 |
| 현재 범위 | 사용자, 로그, 장애 이력 테이블 설계 |
| 구현 상태 | 설계 완료, 실제 테이블 구현 예정 |

---

## 2. 설계 목적

Ops Monitor는 서비스 상태 확인, 로그 기록, 장애 발생 및 복구 이력을 관리하는 운영 모니터링 미니 프로젝트이다.

이를 위해 다음 데이터를 저장할 수 있는 구조를 설계한다.

| 데이터 구분 | 목적 |
|---|---|
| 사용자 정보 | 운영자 또는 관리자 식별 |
| 로그 정보 | API 실행, 오류, 점검 기록 저장 |
| 장애 이력 | 장애 발생, 원인, 복구 조치 기록 |

---

## 3. 테이블 목록

| Table | Description | Status |
|---|---|---|
| users | 운영자 사용자 정보 | 예정 |
| logs | 서비스 실행 및 오류 로그 | 예정 |
| incidents | 장애 발생 및 복구 이력 | 예정 |

---

## 4. ERD 개요

초기 버전에서는 복잡한 권한 관리보다 운영 기록 구조를 단순하게 유지한다.

관계 구조는 다음과 같다.

```text
users
  └── logs

incidents
```

| 관계 | 설명 |
|---|---|
| users → logs | 사용자가 직접 발생시킨 로그가 있을 경우 연결 |
| incidents | 장애 이력은 독립적으로 관리 |
| logs ↔ incidents | 초기 버전에서는 직접 FK를 두지 않고, 필요 시 source 또는 message로 추적 |

---

## 5. users 테이블

운영자 사용자 정보를 저장한다.

### 5.1 테이블 정의

| Column | Type | Constraint | Description |
|---|---|---|---|
| id | integer | PK | 사용자 ID |
| username | varchar(50) | NOT NULL | 사용자명 |
| role | varchar(20) | NOT NULL | 사용자 역할 |
| created_at | timestamp | NOT NULL | 생성 시각 |

### 5.2 설계 기준

| 항목 | 기준 |
|---|---|
| 사용자명 | 실제 개인정보 대신 테스트용 이름 사용 |
| 역할 | 관리자, 운영자 등 시스템 역할 구분 |
| 인증 정보 | 초기 버전에서는 저장하지 않음 |
| 비밀번호 | 저장하지 않음 |

### 5.3 예시 데이터

| id | username | role | created_at |
|---|---|---|---|
| 1 | admin_user | ADMIN | 2026-07-04 22:00:00 |

---

## 6. logs 테이블

서비스 실행 및 오류 로그를 저장한다.

### 6.1 테이블 정의

| Column | Type | Constraint | Description |
|---|---|---|---|
| id | integer | PK | 로그 ID |
| level | varchar(20) | NOT NULL | 로그 레벨 |
| message | text | NOT NULL | 로그 메시지 |
| source | varchar(50) | NOT NULL | 로그 발생 위치 |
| user_id | integer | FK, NULL | 로그를 발생시킨 사용자 ID |
| created_at | timestamp | NOT NULL | 로그 발생 시각 |

### 6.2 로그 레벨

| Value | Description |
|---|---|
| INFO | 일반 실행 정보 |
| WARNING | 주의가 필요한 상태 |
| ERROR | 오류 발생 |

### 6.3 source 정의

| Source | Description |
|---|---|
| health_api | Health Check API 호출 |
| db_check | DB 연결 상태 확인 |
| docker | Docker 컨테이너 상태 확인 |
| system | 시스템 내부 처리 |

### 6.4 예시 데이터

| id | level | message | source | user_id | created_at |
|---|---|---|---|---|---|
| 1 | INFO | Health check requested | health_api | NULL | 2026-07-04 22:40:00 |
| 2 | ERROR | Database connection failed | db_check | NULL | 2026-07-04 22:45:00 |

---

## 7. incidents 테이블

장애 발생 및 복구 이력을 저장한다.

### 7.1 테이블 정의

| Column | Type | Constraint | Description |
|---|---|---|---|
| id | integer | PK | 장애 이력 ID |
| title | varchar(100) | NOT NULL | 장애 제목 |
| status | varchar(20) | NOT NULL | 장애 상태 |
| severity | varchar(20) | NOT NULL | 장애 심각도 |
| cause | text | NULL | 장애 원인 |
| recovery_action | text | NULL | 복구 조치 |
| occurred_at | timestamp | NOT NULL | 장애 발생 시각 |
| recovered_at | timestamp | NULL | 복구 완료 시각 |

### 7.2 status 정의

| Value | Description |
|---|---|
| OPEN | 장애 발생 상태 |
| RECOVERED | 복구 완료 상태 |

### 7.3 severity 정의

| Value | Description |
|---|---|
| LOW | 낮은 영향도 |
| MEDIUM | 일부 기능 영향 |
| HIGH | 주요 기능 영향 |

### 7.4 예시 데이터

| id | title | status | severity | cause | recovery_action |
|---|---|---|---|---|---|
| 1 | PostgreSQL connection failed | RECOVERED | HIGH | PostgreSQL container stopped | Restarted PostgreSQL container |

---

## 8. 데이터 저장 기준

| 항목 | 기준 |
|---|---|
| 개인정보 | 실제 개인정보 저장하지 않음 |
| 계정 정보 | 실제 운영 계정명 저장하지 않음 |
| 비밀번호 | 저장하지 않음 |
| DB 연결 문자열 | 저장하지 않음 |
| 로그 메시지 | 민감정보가 포함되지 않은 요약 메시지만 저장 |
| 장애 원인 | 실제 서버 경로, 계정명, 비밀번호 제외 |
| 시간 정보 | ISO 8601 또는 timestamp 형식 사용 |

---

## 9. 초기 구현 범위

| 항목 | 구현 여부 |
|---|---|
| users 테이블 모델 정의 | 예정 |
| logs 테이블 모델 정의 | 예정 |
| incidents 테이블 모델 정의 | 예정 |
| PostgreSQL 연결 확인 | 완료 |
| 테이블 자동 생성 | 예정 |
| 로그 저장 API | 예정 |
| 장애 이력 저장 API | 예정 |

---

## 10. 향후 확장 방향

| 확장 항목 | 설명 |
|---|---|
| logs와 incidents 연결 | 장애 발생 시 관련 로그를 incident와 연결 |
| user role 세분화 | ADMIN, OPERATOR 등 역할 관리 |
| created_by 추가 | 장애 이력 작성자 추적 |
| updated_at 추가 | 데이터 수정 시각 관리 |
| soft delete | 운영 기록 삭제 대신 비활성화 처리 |
| incident timeline | 장애 발생부터 복구까지 단계별 기록 |

---

## 11. 설계 고려사항

| 항목 | 고려 내용 |
|---|---|
| 단순성 | 초기 버전에서는 운영 기록에 필요한 최소 테이블만 구성 |
| 추적성 | 로그와 장애 이력을 통해 상태 변화 기록 |
| 보안성 | 개인정보, 비밀번호, 실제 연결 문자열 저장 제외 |
| 확장성 | 이후 장애 이력과 로그 간 관계 확장 가능 |
| 운영성 | Health Check 결과와 장애 기록을 연결할 수 있는 구조 유지 |

---

## 12. 다음 작업

| 작업 | 설명 |
|---|---|
| SQLAlchemy 모델 작성 | users, logs, incidents 모델 구현 |
| 테이블 생성 로직 추가 | FastAPI 실행 시 테이블 생성 또는 migration 구성 |
| 로그 API 구현 | `/logs` 조회 및 생성 기능 추가 |
| 장애 API 구현 | `/incidents` 생성, 조회, 복구 처리 기능 추가 |
| API 명세서 동기화 | 실제 구현 결과에 맞춰 API 명세서 수정 |