# GitHub Actions CI

## 1. 학습 목적

Ops Monitor 프로젝트에 적용한 GitHub Actions 기반 CI의 목적과 구성 흐름을 정리한다.

이 문서는 다음 내용을 빠르게 이해하는 것을 목표로 한다.

| 구분 | 정리 내용 |
|---|---|
| CI 목적 | 코드 변경 시 기본 검증 자동화 |
| Workflow 구조 | trigger, job, step의 관계 |
| 검증 범위 | Python 문법, FastAPI import, Compose 설정, Docker build |
| 실행 조건 | `main`, PR, 수동 실행, `paths` 필터 |
| 구분 포인트 | CI workflow와 Dependency Graph의 차이 |

---

## 2. CI를 적용하는 이유

로컬에서는 정상 동작하더라도 원격 저장소 기준으로는 다음 문제가 뒤늦게 발견될 수 있다.

| 항목 | 위험 |
|---|---|
| 문법 오류 | push 이후 실행 불가 |
| import 오류 | 앱 시작 실패 |
| 환경 파일 누락 | Compose 검증 실패 |
| 컨테이너 빌드 오류 | 배포 전 단계 차단 |

CI는 이런 문제를 push 또는 PR 시점에 먼저 확인하는 자동 검증 장치다.

---

## 3. GitHub Actions 기본 구조

GitHub Actions는 `.github/workflows/*.yml` 파일에 작업 흐름을 정의한다.

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

| 요소 | 의미 |
|---|---|
| `name` | 워크플로 이름 |
| `on` | 실행 조건 |
| `jobs` | 실행할 작업 묶음 |
| `steps` | 각 job 내부의 순차 작업 |

---

## 4. Ops Monitor CI 검증 흐름

현재 프로젝트의 CI는 기본 동작 검증에 집중한다.

```text
checkout
  -> python 설정
  -> 의존성 설치
  -> .env 준비
  -> Python compile 검사
  -> FastAPI import 검사
  -> Docker Compose 설정 검사
  -> Docker image build 검사
```

### 4.1 코드 체크아웃

```yaml
- uses: actions/checkout@v4
```

저장소 코드를 runner로 가져오는 단계다.

### 4.2 Python 환경 준비

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
```

프로젝트 실행 기준과 맞는 Python 버전을 runner에 준비한다.

### 4.3 의존성 설치

```yaml
- run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

애플리케이션 import와 build 검증 전에 필수 패키지를 설치한다.

### 4.4 `.env` 예시 파일 활용

실제 비밀값은 GitHub에 올리지 않으므로, CI에서는 `.env.example`을 복사해 최소 실행 조건만 맞춘다.

```yaml
- run: cp .env.example .env
```

---

## 5. 현재 검증 항목

### 5.1 Python 소스 문법 검사

```yaml
- run: python -m compileall app
```

### 5.2 FastAPI 앱 import 검사

```yaml
- run: python -c "from app.main import app; print(app.title)"
```

### 5.3 Docker Compose 설정 검사

```yaml
- run: |
    if command -v docker-compose >/dev/null 2>&1; then
      docker-compose config
    else
      docker compose config
    fi
```

### 5.4 Docker 이미지 빌드 검사

```yaml
- run: docker build -t ops-monitor-ci .
```

---

## 6. 트리거 정제 기준

프로젝트 초반에는 브랜치 범위와 실행 시점을 넓게 잡기 쉽지만, 제출용 또는 운영형 프로젝트에서는 언제 CI가 돌아야 하는지 기준을 정리하는 것이 좋다.

Ops Monitor에서는 다음 기준으로 정리한다.

| 항목 | 적용 내용 |
|---|---|
| `push` | `main` 브랜치만 |
| `pull_request` | `main` 대상 PR |
| `workflow_dispatch` | 수동 실행 허용 |
| `paths` | 앱 코드, Docker, workflow, 의존성 파일 변경 시 실행 |

예시:

```yaml
on:
  push:
    branches:
      - main
    paths:
      - "app/**"
      - ".github/workflows/ci.yml"
      - "Dockerfile"
      - "docker-compose.yml"
      - "requirements.txt"
      - ".env.example"
  pull_request:
    branches:
      - main
```

이렇게 하면 `README.md`, `docs/**`, `study/**`만 수정했을 때는 불필요한 CI 실행을 줄일 수 있다.

---

## 7. `docker-compose`와 `docker compose` 차이

Compose 명령은 환경에 따라 두 형태가 섞여 있다.

| 명령 | 설명 |
|---|---|
| `docker-compose` | 독립 실행형 Compose |
| `docker compose` | Docker CLI 플러그인형 Compose |

로컬에서는 한쪽만 동작하고, GitHub Actions runner에서는 다른 쪽만 제공되는 경우가 있다.  
따라서 CI에서는 두 형태를 모두 대응하는 방식이 안전하다.

---

## 8. CI와 Dependency Graph의 차이

헷갈리기 쉬운 부분이지만, GitHub Actions CI와 Dependency Graph는 역할이 다르다.

| 항목 | CI Workflow | Dependency Graph |
|---|---|---|
| 목적 | 코드 검증 자동화 | 의존성 목록 분석 |
| 정의 위치 | `.github/workflows/*.yml` | GitHub 기본 기능 |
| 실행 방식 | 이벤트 기반 실행 | 백그라운드 스캔 |
| 로그 | Actions run 로그 제공 | 별도 run 로그 없음 |
| 기준 파일 | workflow 파일 | `requirements.txt` 등 의존성 파일 |

즉, Dependency Graph가 안 보인다고 해서 CI가 안 도는 것은 아니다.
반대로 CI가 돌아도 Dependency Graph 반영이 바로 보이지 않을 수 있다.

---

## 9. `requirements.txt` 관리 기준

현재 프로젝트의 기준 의존성 파일은 루트 `requirements.txt`다.

| 파일 | 역할 |
|---|---|
| `requirements.txt` | 앱 실행, Docker build, CI 설치 기준 |
| `app/requirements.txt` | 현재 프로젝트 기준 외부/실험성 패키지 혼합 파일 |

따라서 `app/requirements.txt`는 프로젝트 기준 의존성으로 사용하지 않고 `.gitignore`로 제외하는 것이 적절하다.

---

## 10. 정리

이번 정리를 통해 CI는 단순한 테스트 실행이 아니라, 프로젝트가 최소 실행 가능 상태인지 자동으로 확인하는 기반이라는 점을 다시 정리할 수 있었다.

또한 GitHub Actions workflow, Dependency Graph, 의존성 파일 관리를 분리해서 이해해야 실행 여부와 의존성 인식 이슈를 정확하게 설명할 수 있다.
