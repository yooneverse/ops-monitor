# FastAPI Basic

## 학습 목적

Ops Monitor 프로젝트의 API 서버를 구성하기 위해 FastAPI의 기본 실행 구조를 정리한다.

## FastAPI란

FastAPI는 Python 기반의 웹 API 프레임워크이다.

간단한 코드로 API 서버를 만들 수 있고, `/docs` 경로에서 자동 API 문서를 확인할 수 있다.

Ops Monitor 프로젝트에서는 서비스 상태를 확인하는 `/health` API를 만들기 위해 FastAPI를 사용한다.

## 기본 서버 코드

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Ops Monitor")


@app.get("/")
def root():
    return {
        "message": "Ops Monitor API is running"
    }


@app.get("/health")
def health_check():
    return {
        "api": "ok",
        "timestamp": datetime.now().isoformat()
    }
```

## 코드 설명

### FastAPI 앱 생성

```python
app = FastAPI(title="Ops Monitor")
```

FastAPI 애플리케이션을 생성한다.

`title`은 API 문서에서 프로젝트 이름처럼 표시된다.

### Root API

```python
@app.get("/")
def root():
    return {
        "message": "Ops Monitor API is running"
    }
```

서버가 실행 중인지 간단히 확인하는 기본 API이다.

### Health Check API

```python
@app.get("/health")
def health_check():
    return {
        "api": "ok",
        "timestamp": datetime.now().isoformat()
    }
```

API 서버 상태를 확인하는 점검용 API이다.

운영 환경에서는 서버가 정상적으로 응답하는지 확인하는 기본 지표로 활용할 수 있다.

## 실행 명령어

```bash
uvicorn app.main:app --reload
```

## 명령어 의미

```text
uvicorn        FastAPI 앱을 실행하는 ASGI 서버
app.main       app 폴더의 main.py 파일
app            main.py 안에 있는 FastAPI 객체 이름
--reload       코드 변경 시 서버 자동 재시작
```

## 확인 주소

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 프로젝트 적용

현재 `/health` API는 FastAPI 서버 상태만 확인한다.

이후 PostgreSQL 연결 상태를 추가하여 다음과 같은 구조로 확장할 예정이다.

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

## 다음 학습 내용

* PostgreSQL 연결
* 환경변수 관리
* DB 연결 실패 처리
* Docker 환경에서 FastAPI 실행
