# Security Settings

## 1. 문서 개요

| 항목 | 내용 |
|---|---|
| 문서명 | 보안 설정 문서 |
| 프로젝트명 | Ops Monitor |
| 작성 목적 | 기본 보안 설정 기준과 적용 범위를 정리 |
| 적용 범위 | 환경변수 관리, API 접근 제한, Nginx 보안 헤더, 로그 보안 |
| 참고 문서 | `03_api_spec.md`, `05_docker_compose_design.md`, `06_troubleshooting.md`, `operation-log.md` |

---

## 2. 보안 기준 요약

| 구분 | 기준 |
|---|---|
| 민감정보 관리 | 실제 계정 정보와 연결 문자열은 `.env`로 분리 |
| Git 관리 | `.env`는 제외, `.env.example`만 포함 |
| API 접근 | 로컬 출처만 허용, `GET` 요청 중심으로 제한 |
| Reverse Proxy | Nginx 기본 보안 헤더 적용 |
| 로그 관리 | 비밀번호, 전체 연결 문자열, 내부 상세 오류 미기록 |

---

## 3. 민감정보 관리

실행 환경의 DB 계정명, 비밀번호, DB 이름, 연결 문자열은 코드와 문서에 직접 기록하지 않는다.

| 파일 | 용도 | Git 업로드 |
|---|---|---|
| `.env` | 실제 실행 환경변수 | 제외 |
| `.env.example` | 예시 환경변수 | 포함 |

### 3.1 관리 원칙

| 항목 | 기준 |
|---|---|
| DB 계정명 | `.env`에서 관리 |
| DB 비밀번호 | `.env`에서 관리 |
| DB 이름 | `.env`에서 관리 |
| DATABASE_URL | `.env`에서 관리 |
| 문서 예시 | 실제 값 대신 예시 값 또는 플레이스홀더 사용 |

### 3.2 예시 형식

```env
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASSWORD>
POSTGRES_DB=<DB_NAME>
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
```

---

## 4. API 접근 정책

FastAPI에는 CORS 정책을 적용하며, 현재 범위는 로컬 대시보드와 상태 조회 API 기준으로 제한한다.

### 4.1 CORS 기준

| 항목 | 설정 |
|---|---|
| 허용 출처 | `http://localhost`, `http://127.0.0.1` |
| 허용 메서드 | `GET` |
| 허용 헤더 | `*` |
| 자격증명 | 허용 |

### 4.2 적용 목적

| 항목 | 목적 |
|---|---|
| 로컬 출처 제한 | 불필요한 외부 브라우저 요청 범위 축소 |
| GET 중심 제한 | 현재 조회성 API 범위와 일치 |
| 대시보드 연동 | `/dashboard`, `/health`, `/system` 호출 범위 관리 |

---

## 5. Nginx 보안 헤더

Nginx Reverse Proxy에는 기본 보안 헤더를 적용한다.

| Header | 설정 값 | 목적 |
|---|---|---|
| `X-Content-Type-Options` | `nosniff` | 브라우저의 MIME 타입 임의 해석 방지 |
| `X-Frame-Options` | `DENY` | iframe 삽입 방지 |
| `X-XSS-Protection` | `1; mode=block` | 구형 브라우저 XSS 필터 사용 |
| `Referrer-Policy` | `no-referrer-when-downgrade` | 외부 요청 시 참조 URL 노출 범위 제한 |

### 5.1 적용 위치

| 파일 | 역할 |
|---|---|
| `nginx/default.conf` | Reverse Proxy 및 보안 헤더 설정 |
| `docker-compose.yml` | Nginx 컨테이너 실행 구성 |

---

## 6. 로그 보안 기준

로그와 API 오류 응답에는 민감정보를 직접 기록하지 않는다.

| 항목 | 기록 여부 | 사유 |
|---|---|---|
| DB 비밀번호 | 금지 | 인증 정보 노출 위험 |
| 전체 `DATABASE_URL` | 금지 | 계정명, 비밀번호 포함 가능 |
| 로컬 사용자 경로 | 금지 | 개인 정보 포함 가능 |
| 상세 DB 오류 원문 | 금지 | 내부 구조 노출 가능 |

### 6.1 DB 연결 실패 메시지

DB 연결 실패 시 상세 예외 대신 아래 고정 메시지를 사용한다.

```text
Database connection failed
```

---

## 7. 현재 적용 현황

| 영역 | 상태 | 비고 |
|---|---|---|
| 환경변수 분리 | 적용 | `.env`, `.env.example` 분리 |
| `.env` Git 제외 | 적용 | `.gitignore` 반영 |
| Nginx 보안 헤더 | 적용 | `nginx/default.conf` 설정 |
| CORS 출처 제한 | 적용 | 로컬 출처만 허용 |
| 로그 민감정보 제외 | 적용 | DB 오류 메시지 단순화 |
| 인증/인가 | 미적용 | 향후 확장 가능 |
| HTTPS | 미적용 | 운영 환경 적용 대상 |

---

## 8. 연계 문서

| 문서 | 연계 내용 |
|---|---|
| `03_api_spec.md` | `/health`, `/system`, `/dashboard` API 범위 |
| `05_docker_compose_design.md` | `.env`, Compose, Nginx 실행 구조 |
| `06_troubleshooting.md` | DB 연결 실패와 복구 기록 |
| `operation-log.md` | 운영 중 보안 관련 변경 이력 기록 |
