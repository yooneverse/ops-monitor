# FastAPI DB Health Logging

## 1. 학습 목적

`/health` 응답만으로는 장애 원인을 빠르게 좁히기 어렵다.  
이번 변경은 "DB 연결을 언제 검사했는지", "왜 실패했는지", "헬스 체크가 어떤 결과로 끝났는지"를 로그에 남겨 장애 분석 시간을 줄이는 데 목적이 있다.

---

## 2. 이번에 적용한 로그 포인트

### 2.1 DB 연결 검사 시작 로그

`app/services/db_check.py`

```python
logger.info("Checking database connection...")
```

이 로그는 헬스 체크 호출이 실제 DB 연결 시도까지 도달했는지 확인할 때 유용하다.

확인 포인트:

- 요청은 들어왔는데 DB 검사 로그가 없으면 함수 진입 전 단계부터 의심할 수 있다.
- 주기 모니터링과 수동 호출이 섞여도 검사 시점을 로그로 추적할 수 있다.

### 2.2 환경 변수 누락 로그

```python
logger.error("DATABASE_URL is not set")
```

DB 접속 실패와 설정 누락은 원인이 다르다.  
환경 변수 누락을 분리해 기록하면 네트워크 문제와 설정 문제를 빠르게 구분할 수 있다.

### 2.3 예외 스택 포함 실패 로그

```python
logger.exception("Database connection failed")
```

`logger.exception()`은 에러 메시지뿐 아니라 traceback도 함께 남긴다.

왜 중요한가:

- `psycopg2.OperationalError`처럼 드라이버 단의 실제 실패 원인을 바로 볼 수 있다.
- `db` 호스트 해석 실패, 인증 실패, 타임아웃 같은 원인 분류가 쉬워진다.
- 장애 재현 문서와 운영 로그를 같은 기준으로 비교할 수 있다.

### 2.4 헬스 체크 결과 로그

`app/main.py`

```python
if status in {"disconnected", "error"}:
    logger.info("Health check completed with errors")
else:
    logger.info("Health check completed successfully")
```

헬스 체크 결과를 마지막에 한 번 더 남기면, 요청 하나가 어떤 결론으로 끝났는지 로그 흐름이 완성된다.

로그 흐름 예시:

1. `Checking database connection...`
2. `Database connection failed`
3. `Health check completed with errors`

---

## 3. `uvicorn.error` 로거를 쓴 이유

FastAPI를 Uvicorn으로 실행하면 `uvicorn.error` 로거는 기본 서버 로그 흐름에 자연스럽게 합쳐진다.

장점:

- 애플리케이션 로그와 서버 로그를 한 스트림에서 볼 수 있다.
- Docker 환경에서 `docker logs`만으로도 장애 흐름을 따라가기 쉽다.
- 별도 로깅 설정이 많지 않은 초기 프로젝트에서도 빠르게 적용할 수 있다.

주의점:

- 로그가 많아지면 `info` 레벨이 과도해질 수 있으므로 이후에는 구조화 로그나 레벨 기준 정리가 필요하다.

---

## 4. 이번 변경으로 배운 점

- 헬스 체크 API는 "상태 반환"만이 아니라 "장애 원인 추적 시작점" 역할도 해야 한다.
- DB 연결 실패 로그는 예외 메시지 자체보다 "어느 단계에서 실패했는지"를 함께 남길 때 더 유용하다.
- 운영 로그는 재현 문서와 같은 문장 구조를 가질수록 학습과 장애 대응 둘 다 쉬워진다.

---

## 5. 다음에 확장해볼 주제

- `logger.info(..., extra=...)` 형태의 구조화 로그 붙이기
- 요청 ID를 함께 남겨 `/health` 호출 단위 추적하기
- DB 연결 시간 측정 로그 추가하기
- 실패 원인별로 `error`와 `warning` 레벨 구분하기
