# Ops Monitor Hardening Roadmap

## 1. 문서 목적

이 문서는 Ops Monitor 프로젝트에 적용한 보안 보강과 운영성 개선 사항을 한 번에 학습하기 위한 종합 스터디 문서다.

이번 변경은 단순히 "기능이 동작한다" 수준을 넘어서 아래 질문에 답할 수 있게 만드는 데 목적이 있다.

- 왜 CORS만으로는 서비스가 보호되지 않는가
- 왜 모니터링 API도 인증이 필요한가
- 왜 헬스체크는 공개하되 정보는 최소화해야 하는가
- 왜 앱 레벨과 프록시 레벨 보안을 같이 가져가야 하는가
- 왜 자동 테스트와 컨테이너 헬스체크가 운영 포트폴리오에서 중요한가

---

## 2. 이번에 보강한 전체 항목

이번에 적용한 핵심 항목은 아래와 같다.

| 구분 | 적용 내용 | 목적 |
|---|---|---|
| 인증 | Basic Auth | `curl` 포함 비인증 접근 차단 |
| 앱 보안 | Trusted Host | 비정상 `Host` 헤더 제한 |
| 공개 헬스체크 | `/livez`, `/readyz` | 최소 정보만 공개 |
| 보호 엔드포인트 | `/health`, `/system`, `/alerts`, `/monitoring/status`, `/dashboard`, `/docs` | 운영 정보 보호 |
| 프록시 보안 | rate limit, connection limit, method limit | 무분별한 조회와 스캐닝 완화 |
| 프록시 헤더 | `server_tokens off`, `Cache-Control: no-store` | 정보 노출 축소 |
| Compose | app/db healthcheck, healthy depends_on | 실행 순서와 준비 상태 관리 |
| 테스트 | `unittest` 기반 보안/준비 상태 검증 | 회귀 방지 |
| 문서 | `docs`, `study` 보강 | 학습과 포트폴리오 설명력 강화 |

---

## 3. 왜 CORS만으로는 부족한가

CORS는 브라우저가 다른 출처로 요청할 때 동작하는 정책이다.  
즉 "브라우저 기반 프런트엔드"에는 영향을 주지만, 서버 자체를 보호하는 인증 장치는 아니다.

예를 들어 아래 요청은 브라우저가 아니라 직접 서버로 접근하므로 CORS와 무관하게 실행될 수 있다.

```bash
curl http://localhost/health
```

따라서 운영형 모니터링 프로젝트에서는 아래 원칙이 필요하다.

- 브라우저 정책과 별개로 서버가 직접 인증을 수행해야 한다.
- 공개해야 하는 엔드포인트와 숨겨야 하는 엔드포인트를 구분해야 한다.
- 헬스체크는 오케스트레이션용 probe와 운영자용 상세 상태 조회를 분리해야 한다.

---

## 4. Basic Auth를 선택한 이유

이번 프로젝트는 유료 서비스 없이 로컬과 오픈소스 기반으로 끝내는 것이 조건이었다.  
그 조건에서 가장 현실적이고 즉시 적용 가능한 보호 장치가 HTTP Basic Auth다.

### 4.1 장점

- 브라우저와 `curl`에서 모두 같은 방식으로 동작한다.
- FastAPI와 Nginx 앞단 구조에서 적용이 쉽다.
- 추가 인프라가 필요 없다.
- 로컬 포트폴리오 프로젝트에서 운영 보호 의도를 보여주기 좋다.

### 4.2 한계

- 사용자/권한 체계가 세밀하지 않다.
- 세션 관리나 토큰 만료 개념이 없다.
- 대규모 서비스의 최종 형태로 보기에는 단순하다.

즉, Basic Auth는 "실무 최종형"이라기보다 "운영 엔드포인트를 최소 기준으로 닫아두는 첫 단계"라고 이해하면 된다.

---

## 5. 어떤 엔드포인트를 보호했는가

### 5.1 인증이 필요한 엔드포인트

- `/dashboard`
- `/health`
- `/system`
- `/alerts`
- `/monitoring/status`
- `/docs`
- `/openapi.json`

이 엔드포인트들은 아래 정보를 담고 있거나 유추 가능하게 만든다.

- DB 연결 상태
- 시스템 메모리/디스크 사용률
- 최근 장애 및 복구 이력
- 모니터링 주기와 알림 설정 여부
- API 구조와 스키마

이런 정보는 운영 편의성에는 도움이 되지만 외부에 그대로 노출되면 공격자에게도 유용하다.

### 5.2 공개 엔드포인트로 남긴 항목

- `/`
- `/livez`
- `/readyz`

공개 엔드포인트는 최대한 단순하게 유지했다.

---

## 6. `/livez`와 `/readyz`를 분리한 이유

운영 환경에서는 "프로세스가 살아 있는가"와 "서비스가 실제 트래픽을 받을 준비가 되었는가"를 분리해 보는 것이 중요하다.

### 6.1 `/livez`

`/livez`는 애플리케이션 프로세스 자체가 살아 있는지만 확인한다.

예시 응답:

```json
{
  "status": "ok",
  "timestamp": "2026-07-10T19:00:00"
}
```

### 6.2 `/readyz`

`/readyz`는 DB 연결 여부를 기준으로 준비 상태만 판정한다.  
중요한 점은 DB 예외 메시지나 내부 상세 구조를 그대로 반환하지 않는다는 것이다.

예시 응답:

```json
{
  "status": "ready",
  "timestamp": "2026-07-10T19:00:00"
}
```

또는

```json
{
  "status": "not_ready",
  "timestamp": "2026-07-10T19:00:00"
}
```

이렇게 하면 공개 probe는 유지하면서도 상세 장애 정보 노출은 줄일 수 있다.

---

## 7. Trusted Host가 왜 필요한가

HTTP 요청에는 `Host` 헤더가 들어간다.  
리버스 프록시나 애플리케이션이 이 값을 그대로 신뢰하면 예상하지 못한 라우팅, URL 생성, 보안 우회 문제가 생길 수 있다.

이번에는 허용한 호스트만 받도록 제한했다.

```env
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
```

학습 포인트:

- 로컬 개발에서는 `localhost`, `127.0.0.1` 정도로 충분하다.
- 배포 환경에서는 실제 도메인을 명시적으로 넣어야 한다.
- `"*"`로 열어두면 Trusted Host를 쓰는 의미가 거의 사라진다.

---

## 8. Nginx에서 추가한 보안 요소

### 8.1 rate limiting

짧은 시간에 과도한 요청이 들어오는 것을 완화한다.

```nginx
limit_req_zone $binary_remote_addr zone=monitor_api_limit:10m rate=10r/s;
```

의미:

- 클라이언트 IP 기준으로 초당 요청량을 제한한다.
- 무차별 조회나 단순 스캐닝을 완화한다.

### 8.2 connection limiting

동시에 너무 많은 연결을 붙이지 못하게 제한한다.

```nginx
limit_conn_zone $binary_remote_addr zone=monitor_conn_limit:10m;
```

### 8.3 method 제한

현재 서비스는 조회형 API 중심이므로 `GET`, `HEAD`만 허용해도 충분하다.

```nginx
limit_except GET HEAD { deny all; }
```

이렇게 하면 불필요한 `POST`, `PUT`, `DELETE` 요청이 초기에 차단된다.

### 8.4 hidden file 차단

```nginx
location ~ /\.(?!well-known).* {
    deny all;
}
```

실수로 숨김 파일 경로가 노출되는 일을 줄여준다.

### 8.5 서버 정보 축소

```nginx
server_tokens off;
```

Nginx 버전 노출을 줄여서 공격자가 서버 지문을 바로 얻기 어렵게 만든다.

### 8.6 캐시 금지

```nginx
add_header Cache-Control "no-store" always;
```

모니터링 응답이 중간 캐시나 브라우저에 남는 위험을 줄인다.

---

## 9. Docker Compose healthcheck를 넣은 이유

컨테이너가 "떠 있다"와 "정상 준비 완료"는 다르다.  
운영에서는 readiness 개념이 중요하다.

### 9.1 app healthcheck

애플리케이션 컨테이너는 `/livez`를 통해 살아 있는지 확인한다.

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/livez', timeout=3)"]
```

### 9.2 db healthcheck

DB는 `pg_isready`로 준비 상태를 본다.

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
```

### 9.3 `depends_on.condition: service_healthy`

단순 컨테이너 시작 순서가 아니라 "상대 서비스가 healthy 상태인가"까지 보게 된다.

장점:

- 앱이 DB 준비 전 시점에 너무 빨리 붙으려는 문제를 줄인다.
- Nginx가 준비되지 않은 app으로 요청을 프록시하는 상황을 줄인다.

---

## 10. 왜 테스트를 꼭 붙여야 하는가

운영형 기능은 UI보다 조건 분기가 중요하다.  
특히 아래 항목은 사람이 매번 수동으로 검증하면 빠뜨리기 쉽다.

- 인증 정보가 없을 때 503으로 닫히는가
- 잘못된 인증이면 401이 나가는가
- 올바른 인증이면 통과하는가
- readiness 응답이 상세 DB 정보를 노출하지 않는가
- 환경 변수 파싱이 예상대로 되는가

이번에는 `unittest`로 최소 회귀 테스트를 넣었다.

학습 포인트:

- 테스트가 많지 않아도 "보안 정책이 열리지 않는가"를 확인하는 것 자체가 중요하다.
- 운영성 로직은 단순 성공 케이스보다 실패/미설정 케이스를 많이 검증해야 한다.

---

## 11. 실습해볼 `curl` 예시

### 11.1 인증 없이 보호 엔드포인트 접근

```bash
curl -i http://localhost/health
```

기대 결과:

- 인증 설정이 있으면 `401 Unauthorized`
- 인증 설정이 없으면 `503 Service Unavailable`

### 11.2 인증 포함 접근

```bash
curl -i -u <MONITOR_USERNAME>:<MONITOR_PASSWORD> http://localhost/health
```

기대 결과:

- `200 OK`
- DB 상태 포함 JSON 응답

### 11.3 readiness 확인

```bash
curl -i http://localhost/readyz
```

기대 결과:

- DB 준비 완료 시 `200`
- DB 미준비 시 `503`
- 상세 오류 문자열 대신 `ready` 또는 `not_ready` 중심 응답

---

## 12. 포트폴리오 관점에서 왜 좋은가

이번 보강은 단순 보안 설정 추가가 아니라 "운영 엔드포인트를 어떤 철학으로 다뤘는가"를 보여준다.

### 12.1 미들웨어 개발자 관점

- 서비스 경계에서 인증을 강제했다.
- 운영용 API와 공개 probe를 분리했다.
- 상태 전이와 운영 이벤트를 의식한 설계를 했다.

### 12.2 운영/인프라 개발자 관점

- reverse proxy 레벨과 app 레벨 보안을 같이 적용했다.
- healthcheck와 readiness 개념을 컨테이너 구성에 반영했다.
- 테스트와 문서까지 남겨 재현 가능성을 높였다.

면접에서 설명하기 좋은 포인트:

- "CORS는 브라우저 정책이라 `curl`을 못 막습니다. 그래서 Basic Auth와 공개 probe 분리를 적용했습니다."
- "상세 상태 조회는 닫고, 오케스트레이션용 readiness만 최소 정보로 열어두었습니다."
- "Nginx, FastAPI, Compose 각각의 레이어에서 어떤 보호 장치를 둘지 나눠서 설계했습니다."

---

## 13. 이번 변경의 한계와 다음 단계

이번 변경은 비용 없이 적용 가능한 현실적인 1차 보강이다.  
다만 아래 항목은 이후 확장 주제로 남아 있다.

### 13.1 한계

- Basic Auth는 사용자/권한 분리가 약하다.
- alert history가 아직 메모리 기반이라 재시작 시 사라진다.
- 구조화 로그와 request id가 아직 없다.
- 메트릭 수집과 시각화가 없다.

### 13.2 다음 단계 제안

- alert history를 DB에 영속화
- structured logging + request id
- Prometheus metrics + Grafana
- IP allowlist
- Slack/Email/Webhook 추상화
- pytest 기반 엔드포인트 테스트 확장
- HTTPS/TLS 및 인증서 운영 시나리오 추가

---

## 14. 함께 읽으면 좋은 문서

- `study/runtime-security-hardening.md`
- `study/fastapi-db-health-logging.md`
- `study/nginx-reverse-proxy.md`
- `study/docker-compose-runtime.md`
- `study/github-actions-ci.md`
- `docs/08_runtime_security.md`

이 문서를 먼저 읽고, 이후 세부 문서를 보면 전체 그림이 더 잘 잡힌다.
