# Runtime Security Hardening

## 1. 왜 CORS만으로는 부족한가

CORS는 브라우저의 교차 출처 요청을 제한하는 정책이지, 서버 자체를 보호하는 인증 장치는 아니다.

즉 아래 요청은 CORS와 상관없이 바로 들어올 수 있다.

```bash
curl http://localhost/health
```

운영성 있는 모니터링 서비스라면 "브라우저에서만 조심"이 아니라 "서버가 직접 인증과 노출 범위를 제어"해야 한다.

---

## 2. 이번에 적용한 보완 포인트

### 2.1 Basic Auth

민감한 운영 엔드포인트에 Basic Auth를 걸어서 브라우저와 `curl` 양쪽 모두 같은 기준으로 보호했다.

대상:

- `/dashboard`
- `/health`
- `/system`
- `/alerts`
- `/monitoring/status`
- `/docs`

핵심 포인트:

- 인증 정보가 없으면 `401`
- 서버 설정 자체가 비어 있으면 `503`
- 즉, 실수로 "무인증 공개" 상태가 되지 않도록 fail-closed 방식으로 막는다.

### 2.2 Public probe 최소화

운영에서는 컨테이너 헬스체크를 위해 공개 probe가 필요할 수 있다.  
대신 상세 상태를 다 보여주지 않고 최소 정보만 노출하는 방식이 좋다.

이번 적용:

- `/livez`: 프로세스 생존 여부
- `/readyz`: 서비스 준비 여부만 반환

`/readyz`는 DB 예외 문자열 같은 내부 정보는 노출하지 않는다.

### 2.3 Reverse proxy 방어선

Nginx에 아래 항목을 추가했다.

- rate limiting
- connection limiting
- `GET`, `HEAD` 이외 차단
- hidden file path 차단
- `server_tokens off`
- `Cache-Control: no-store`

이건 "완벽한 WAF"는 아니지만, 최소한의 운영형 방어선으로는 의미가 크다.

### 2.4 Trusted Host

허용한 `Host` 헤더만 받도록 제한해서 비정상 호스트 기반 요청을 줄였다.

---

## 3. 이번 변경이 포트폴리오에서 좋은 이유

- 모니터링 API를 단순 조회 API가 아니라 운영 자산으로 취급했다.
- "헬스체크는 필요하지만 정보 노출은 최소화"라는 균형을 잡았다.
- 앱 레벨 보호와 프록시 레벨 보호를 같이 적용했다.
- 보안 설정이 비어 있으면 열어두는 대신 실패하게 설계했다.

이런 판단은 미들웨어, 운영, 인프라 성향 포지션에서 꽤 좋은 신호다.

---

## 4. 다음에 이어서 해볼 만한 것

- Basic Auth 대신 사내 SSO 또는 reverse proxy auth 연동
- IP allowlist 추가
- structured logging + request id
- alert history 영속화
- Prometheus metrics + Grafana dashboard
