# FastAPI Monitoring

## 1. 학습 목적

Ops Monitor 프로젝트에서 FastAPI를 단순 실행 서버가 아니라 운영 상태 점검용 API 서버로 확장하는 과정을 정리한다.

이 문서는 다음 내용을 이해하는 것을 목표로 한다.

| 구분 | 정리 내용 |
|---|---|
| API 확장 방식 | 엔드포인트 추가와 라우터 분리 |
| 상태 점검 구조 | `/health`, `/system` 역할 차이 |
| 대시보드 구성 | FastAPI에서 HTML 응답 제공 |
| 브라우저 연동 | CORS 설정과 조회 전용 API 구성 |
| 운영 관점 | 상태 점검 API가 필요한 이유 |

---

## 2. 왜 FastAPI를 확장했는가

초기 단계의 FastAPI는 서버 실행 여부를 확인하는 수준에 가깝다.

하지만 운영 환경에서는 단순히 서버가 켜져 있는지보다 다음 항목을 함께 확인해야 한다.

| 확인 항목 | 설명 |
|---|---|
| API 응답 가능 여부 | 서버가 요청을 처리할 수 있는지 확인 |
| DB 연결 상태 | 애플리케이션이 의존하는 DB에 연결 가능한지 확인 |
| 시스템 자원 상태 | 메모리, 디스크 사용량이 정상 범위인지 확인 |
| 상태 시각화 | 사람이 빠르게 현재 상태를 읽을 수 있는 화면 제공 |

Ops Monitor에서는 이러한 목적 때문에 `/health`, `/system`, `/dashboard` 구성을 추가했다.

---

## 3. FastAPI 핵심 개념

### 3.1 FastAPI Application

FastAPI 애플리케이션은 전체 API 서버의 진입점이다.

```python
app = FastAPI(title="Ops Monitor")
```

`title`은 Swagger UI와 문서 식별에 사용된다.

---

### 3.2 Path Operation

Path Operation은 특정 URL과 HTTP Method에 대한 처리 로직이다.

```python
@app.get("/health")
def health_check():
    ...
```

| 요소 | 의미 |
|---|---|
| `@app.get()` | GET 요청 처리 등록 |
| `"/health"` | 요청 경로 |
| `health_check()` | 실제 응답 로직 |

---

### 3.3 APIRouter

기능이 늘어나면 모든 엔드포인트를 `main.py`에 작성하기 어렵다.

이때 `APIRouter`를 사용하면 기능별로 라우트를 분리할 수 있다.

```python
from fastapi import APIRouter

router = APIRouter()
```

Ops Monitor에서는 대시보드 페이지를 `app/api/dashboard.py`로 분리했다.

| 분리 대상 | 이유 |
|---|---|
| 대시보드 라우트 | HTML 응답 로직이 길고 별도 관리가 필요 |
| 메인 앱 | 서버 초기화와 핵심 상태 점검 API 중심으로 유지 |

---

### 3.4 Middleware

Middleware는 요청이 엔드포인트에 도달하기 전, 혹은 응답이 클라이언트에 반환되기 전에 공통 처리를 수행하는 계층이다.

Ops Monitor에서는 CORS 설정을 위해 Middleware를 사용했다.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

---

## 4. `/health`와 `/system`의 차이

두 API는 모두 상태 점검용이지만 대상이 다르다.

| Endpoint | 점검 대상 | 목적 |
|---|---|---|
| `/health` | API 서버, DB 연결 | 서비스 가용성 확인 |
| `/system` | 메모리, 디스크 사용량 | 서버 자원 상태 확인 |

### 4.1 `/health`

`/health`는 애플리케이션과 데이터베이스의 연결 상태를 함께 확인한다.

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

운영 환경에서는 Load Balancer, 모니터링 시스템, 배포 스크립트가 이 응답을 기준으로 상태를 판단할 수 있다.

---

### 4.2 `/system`

`/system`은 시스템 리소스 사용량을 반환한다.

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

이 API는 장애 감지보다는 운영 상태 관찰에 더 가깝다.

| 자원 | 확인 이유 |
|---|---|
| 메모리 | 프로세스 과부하 여부 확인 |
| 디스크 | 저장공간 부족 가능성 확인 |

---

## 5. `psutil`을 사용하는 이유

Python 표준 라이브러리만으로도 일부 시스템 정보를 조회할 수 있지만, 메모리/CPU/디스크 정보를 운영 관점에서 다루기에는 `psutil`이 훨씬 적합하다.

| 항목 | 설명 |
|---|---|
| `psutil.virtual_memory()` | 메모리 총량, 사용량, 사용률 조회 |
| `shutil.disk_usage()` | 디스크 총량, 사용량, 여유량 조회 |
| 사용 목적 | 운영 대시보드와 상태 API의 기초 데이터 제공 |

Ops Monitor에서는 메모리와 디스크 사용량을 GB 단위와 퍼센트 단위로 함께 반환하도록 구성했다.

---

## 6. FastAPI에서 HTML 응답을 주는 이유

FastAPI는 JSON API만 제공하는 프레임워크가 아니라, 필요하면 HTML도 직접 반환할 수 있다.

```python
from fastapi.responses import HTMLResponse
```

대시보드는 별도 프론트엔드 프레임워크 없이도 다음 목적을 빠르게 달성할 수 있다.

| 목적 | 설명 |
|---|---|
| 상태 시각화 | 숫자와 텍스트를 카드 형태로 표시 |
| 빠른 검증 | API 응답이 화면에 정상 반영되는지 즉시 확인 |
| 구조 학습 | API와 UI가 어떻게 연결되는지 이해 |

Ops Monitor의 `/dashboard`는 `/health`, `/system` 응답을 브라우저에서 다시 읽어 상태를 갱신하는 구조이다.

---

## 7. CORS를 왜 설정했는가

CORS는 브라우저가 다른 출처의 리소스를 요청할 때 적용하는 보안 정책이다.

현재 프로젝트는 로컬 대시보드와 상태 조회 API 중심이므로 허용 출처를 로컬로 제한했다.

| 설정 | 의미 |
|---|---|
| `allow_origins` | 허용할 출처 목록 |
| `allow_methods=["GET"]` | 조회 전용 API 범위 제한 |
| `allow_headers=["*"]` | 요청 헤더 허용 |
| `allow_credentials=True` | 인증정보 포함 요청 허용 가능 |

운영 환경에서 CORS를 무분별하게 넓게 열면 불필요한 접근 범위가 커질 수 있다.

---

## 8. 프로젝트 적용 정리

| 항목 | 적용 내용 |
|---|---|
| 라우터 분리 | `app/api/dashboard.py` 사용 |
| 상태 API | `/health`, `/system` 구현 |
| 시스템 자원 조회 | `psutil`, `shutil` 기반 |
| HTML 응답 | `/dashboard`에서 `HTMLResponse` 사용 |
| 브라우저 연동 | JavaScript `fetch()`로 상태 조회 |
| CORS 설정 | 로컬 출처와 GET 요청만 허용 |

---

## 9. 정리

실제 기반 작업을 통해 FastAPI는 단순 CRUD API 서버가 아니라, 운영 상태를 점검하고 시각화하는 모니터링 서버 역할도 수행할 수 있다는 점을 확인했다.

특히 `/health`와 `/system`의 역할을 분리하면 서비스 가용성과 자원 상태를 각각 명확하게 다룰 수 있고, 대시보드까지 연결하면 사람이 빠르게 상태를 파악할 수 있는 운영 화면을 구성할 수 있다.
