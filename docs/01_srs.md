# 요구사항 명세서 (SRS)

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | 요구사항 명세서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 시스템의 기능 요구사항, 비기능 요구사항, 장애 대응 요구사항 정의 |
| 현재 구현 범위 | FastAPI 기본 서버, `/health` API, PostgreSQL 연결 상태 확인 |
| 확장 예정 범위 | 로그 관리, 장애 이력 관리, Docker Compose 통합, Nginx Reverse Proxy |

---

## 2. 프로젝트 개요

Ops Monitor는 Docker 기반 서비스 운영 환경을 구성하고, API 서버와 데이터베이스 상태를 점검하기 위한 운영 모니터링 미니 프로젝트이다.

서비스가 정상적으로 실행되는지 확인하고, 장애 발생 시 상태 확인, 로그 점검, 복구 과정을 기록하는 흐름을 구현하는 것을 목표로 한다.

---

## 3. 시스템 목적

| 목적 | 설명 |
|---|---|
| 서비스 상태 확인 | API 서버와 DB 연결 상태를 `/health` API로 확인 |
| 장애 감지 | DB 중지 또는 연결 실패 상태를 응답값으로 구분 |
| 복구 확인 | PostgreSQL 컨테이너 재시작 후 정상 연결 여부 확인 |
| 운영 기록 | 실행, 점검, 장애, 복구 과정을 문서로 기록 |
| 환경 일관성 | Docker Compose 기반 실행 환경 구성 |

---

## 4. 사용자 정의

| 사용자 | 설명 |
|---|---|
| 운영자 | API 서버와 DB 상태를 확인하고 장애 여부를 점검하는 사용자 |
| 관리자 | 로그와 장애 이력을 관리하는 사용자 |
| 개발자 | 서비스 구성, API, Docker 환경을 유지보수하는 사용자 |

초기 버전에서는 별도 인증 기능을 구현하지 않는다.

---

## 5. 현재 구현 범위

| ID | 항목 | 설명 | 상태 |
|---|---|---|---|
| IMPL-01 | FastAPI 기본 서버 | FastAPI 기반 API 서버 구성 | 완료 |
| IMPL-02 | Root API | `/` 요청 시 서버 실행 메시지 반환 | 완료 |
| IMPL-03 | Health Check API | `/health` 요청 시 API 상태 반환 | 완료 |
| IMPL-04 | DB 상태 확인 | PostgreSQL 연결 상태 확인 | 완료 |
| IMPL-05 | Docker PostgreSQL 실행 | Docker Compose로 PostgreSQL 컨테이너 실행 | 완료 |
| IMPL-06 | DB 장애 감지 | PostgreSQL 중지 시 `disconnected` 반환 | 완료 |
| IMPL-07 | DB 복구 확인 | PostgreSQL 재시작 후 `connected` 반환 | 완료 |

---

## 6. 기능 요구사항

### 6.1 API 서버

| ID | 요구사항 | 설명 | 우선순위 | 상태 |
|---|---|---|---|---|
| FR-API-01 | Root API 제공 | API 서버 실행 여부를 확인할 수 있어야 한다. | High | 완료 |
| FR-API-02 | Health Check API 제공 | API 서버와 DB 상태를 확인할 수 있어야 한다. | High | 완료 |
| FR-API-03 | Swagger 문서 제공 | FastAPI 기본 `/docs`를 통해 API 확인이 가능해야 한다. | Medium | 완료 |

### 6.2 데이터베이스 상태 확인

| ID | 요구사항 | 설명 | 우선순위 | 상태 |
|---|---|---|---|---|
| FR-DB-01 | DB 연결 성공 확인 | PostgreSQL 연결 성공 시 `connected` 상태를 반환해야 한다. | High | 완료 |
| FR-DB-02 | DB 연결 실패 확인 | PostgreSQL 연결 실패 시 `disconnected` 상태를 반환해야 한다. | High | 완료 |
| FR-DB-03 | 환경변수 누락 확인 | `DATABASE_URL` 누락 시 `error` 상태를 반환해야 한다. | Medium | 완료 |

### 6.3 로그 관리

| ID | 요구사항 | 설명 | 우선순위 | 상태 |
|---|---|---|---|---|
| FR-LOG-01 | 로그 목록 조회 | 서비스 실행 및 오류 로그를 조회할 수 있어야 한다. | Medium | 예정 |
| FR-LOG-02 | 로그 생성 | 주요 이벤트 발생 시 로그를 저장할 수 있어야 한다. | Medium | 예정 |
| FR-LOG-03 | 로그 레벨 구분 | INFO, WARNING, ERROR 단위로 로그를 구분해야 한다. | Medium | 예정 |

### 6.4 장애 이력 관리

| ID | 요구사항 | 설명 | 우선순위 | 상태 |
|---|---|---|---|---|
| FR-INC-01 | 장애 이력 조회 | 장애 발생 및 복구 이력을 조회할 수 있어야 한다. | Medium | 예정 |
| FR-INC-02 | 장애 이력 생성 | 장애 발생 시 원인과 상태를 기록할 수 있어야 한다. | Medium | 예정 |
| FR-INC-03 | 장애 복구 처리 | 복구 조치 후 장애 상태를 `RECOVERED`로 변경할 수 있어야 한다. | Medium | 예정 |

---

## 7. 비기능 요구사항

| ID | 요구사항 | 설명 | 우선순위 | 상태 |
|---|---|---|---|---|
| NFR-01 | 실행 환경 일관성 | Docker Compose를 통해 동일한 DB 실행 환경을 구성해야 한다. | High | 일부 완료 |
| NFR-02 | 상태 확인 가능성 | `/health` API로 API와 DB 상태를 확인할 수 있어야 한다. | High | 완료 |
| NFR-03 | 장애 추적성 | 장애 발생, 확인, 복구 과정을 문서로 추적할 수 있어야 한다. | High | 진행 중 |
| NFR-04 | 설정 분리 | DB 접속 정보는 환경변수로 분리해야 한다. | High | 완료 |
| NFR-05 | 민감정보 보호 | 계정명, 비밀번호, 연결 문자열은 문서와 응답에 노출하지 않아야 한다. | High | 완료 |
| NFR-06 | 유지보수성 | API, 서비스 로직, 모델을 분리해 관리해야 한다. | Medium | 진행 중 |
| NFR-07 | 확장성 | FastAPI, PostgreSQL, Nginx를 Compose 환경으로 확장할 수 있어야 한다. | Medium | 예정 |

---

## 8. 장애 대응 요구사항

| ID | 요구사항 | 설명 | 상태 |
|---|---|---|---|
| IR-01 | DB 장애 감지 | PostgreSQL 연결 실패 시 `/health` API에서 장애 상태를 반환해야 한다. | 완료 |
| IR-02 | DB 복구 확인 | PostgreSQL 재시작 후 `/health` API에서 정상 상태를 확인해야 한다. | 완료 |
| IR-03 | 로그 확인 | 장애 발생 시 Docker 로그 또는 애플리케이션 로그를 확인할 수 있어야 한다. | 일부 완료 |
| IR-04 | 복구 기록 | 장애 원인, 확인 명령어, 복구 조치를 문서에 기록해야 한다. | 진행 중 |
| IR-05 | 응답 메시지 관리 | 내부 오류 원문을 그대로 노출하지 않고 정의된 메시지를 반환해야 한다. | 완료 |

---

## 9. 데이터 요구사항

| 데이터 | 설명 | 상태 |
|---|---|---|
| 사용자 데이터 | 운영자 또는 관리자 식별 정보 | 예정 |
| 로그 데이터 | API 호출, 오류, 점검 기록 | 예정 |
| 장애 이력 데이터 | 장애 발생, 원인, 복구 조치 기록 | 예정 |

민감정보 저장 기준은 다음과 같다.

| 항목 | 저장 여부 |
|---|---|
| 실제 비밀번호 | 저장하지 않음 |
| 실제 DB 연결 문자열 | 저장하지 않음 |
| 개인 로컬 경로 | 저장하지 않음 |
| 사용자 개인정보 | 저장하지 않음 |
| 테스트용 사용자명 | 허용 |

---

## 10. 환경 요구사항

| 항목 | 내용 |
|---|---|
| OS | Windows 로컬 환경, Ubuntu Server 확장 예정 |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Container | Docker, Docker Compose |
| Reverse Proxy | Nginx 예정 |
| CI/CD | GitHub Actions 예정 |
| Config | `.env`, `.env.example` |

---

## 11. 완료 기준

### 1차 완료 기준

| 항목 | 기준 | 상태 |
|---|---|---|
| FastAPI 서버 실행 | 로컬에서 API 서버 실행 가능 | 완료 |
| `/health` API | API 상태와 DB 연결 상태 반환 | 완료 |
| PostgreSQL 컨테이너 | Docker Compose로 실행 가능 | 완료 |
| DB 장애 감지 | 컨테이너 중지 시 `disconnected` 반환 | 완료 |
| DB 복구 확인 | 컨테이너 재시작 시 `connected` 반환 | 완료 |
| 운영 기록 | operation-log에 작업 결과 기록 | 진행 중 |

### 최종 완료 기준

| 항목 | 기준 | 상태 |
|---|---|---|
| FastAPI 컨테이너화 | FastAPI를 Docker Compose 서비스로 실행 | 예정 |
| Nginx Reverse Proxy | Nginx를 통해 FastAPI 요청 전달 | 예정 |
| 로그 API | `/logs` 조회 및 생성 가능 | 예정 |
| 장애 이력 API | `/incidents` 생성, 조회, 복구 처리 가능 | 예정 |
| GitHub Actions | 기본 CI workflow 구성 | 예정 |
| README 정리 | 실행 방법, 기술 선택 이유, 트러블슈팅 포함 | 진행 중 |

---

## 12. 제외 범위

초기 버전에서는 다음 항목을 제외한다.

| 제외 항목 | 사유 |
|---|---|
| 사용자 인증 | 인프라 운영 흐름 검증이 우선 |
| 프론트엔드 Dashboard | API 및 운영 문서 중심으로 진행 |
| 실서버 배포 | 로컬 Docker 기반 운영 흐름 검증 목적 |
| HTTPS | Nginx 기본 Reverse Proxy 구성 후 확장 가능 |
| 복잡한 권한 관리 | 초기 버전에서는 운영 기록 구조가 우선 |

---

## 13. 관련 문서

| 문서 | 설명 |
|---|---|
| `docs/02_architecture.md` | 시스템 구성과 요청 흐름 |
| `docs/03_api_spec.md` | API 요청 및 응답 명세 |
| `docs/04_erd.md` | 데이터 테이블 설계 |
| `docs/05_docker_compose_design.md` | Docker Compose 구성 |
| `docs/08_troubleshooting.md` | 오류 및 해결 기록 |
| `docs/operation-log.md` | 날짜별 운영 작업 기록 |

---

## 14. 다음 작업

| 작업 | 설명 |
|---|---|
| FastAPI Dockerfile 작성 | API 서버 컨테이너 실행 환경 구성 |
| Compose에 app 서비스 추가 | FastAPI와 PostgreSQL을 함께 실행 |
| DATABASE_URL 변경 | Compose 내부 네트워크 기준으로 DB host 변경 |
| Nginx 설정 작성 | Reverse Proxy 구성 |
| 로그/장애 테이블 구현 | ERD 기준으로 모델 작성 |