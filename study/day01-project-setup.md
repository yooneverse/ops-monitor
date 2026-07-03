# Day 01. Project Setup

## 오늘의 목표

Ops Monitor 프로젝트의 기본 구조를 만들고, FastAPI 서버를 실행하여 `/health` API가 정상 동작하는지 확인.

## 오늘 진행한 내용

* `ops-monitor` 프로젝트 폴더 생성
* Git 저장소 초기화
* FastAPI 기본 서버 구현
* `/` API 구현
* `/health` API 구현
* Python 가상환경 활성화
* `requirements.txt` 기반 패키지 설치
* `.gitignore` 추가
* 레포 연결 및 push

## 프로젝트 초기 구조

```text
ops-monitor/
├── app/
│   └── main.py
├── docs/
├── nginx/
├── study/
├── .gitignore
├── README.md
└── requirements.txt
```

## 실행 명령어

```bash
uvicorn app.main:app --reload
```

## 확인한 주소

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/health
```

## 실행 결과

FastAPI 서버가 정상적으로 실행되었고, `/health` API를 통해 서버 상태를 확인할 수 있었다.

```json
{
  "api": "ok",
  "timestamp": "2026-07-03T00:00:00"
}
```

## 오늘 복기

FastAPI 서버는 `uvicorn`을 통해 실행하며, `--reload` 옵션을 사용하면 코드 변경 시 서버가 자동으로 다시 실행된다.

`/health` API는 서비스 운영에서 서버가 정상적으로 동작하는지 확인하는 기본 점검 API로 활용한다.

이번 단계에서는 API 서버 상태만 확인했지만, 이후 PostgreSQL 연결 상태까지 포함하여 API와 DB 상태를 함께 점검할 수 있도록 확장할 예정이다.

## 다음 작업

* PostgreSQL 연결 설정
* DB 연결 상태 확인 로직 구현
* `/health` API에 DB 상태 추가
