# 런타임 보안 강화

## 목표

이 문서는 Ops Monitor에 적용한 런타임 보안 강화 내용을 정리합니다. 목적은 인증되지 않은 `curl` 요청에 모니터링 데이터가 그대로 노출되지 않도록 하는 것입니다.

## 변경 사항

### 1. 민감 엔드포인트 기본 인증 적용

아래 엔드포인트는 이제 HTTP Basic Auth가 필요합니다.

- `/dashboard`
- `/health`
- `/system`
- `/alerts`
- `/monitoring/status`
- `/docs`
- `/openapi.json`

인증 정보는 아래 환경 변수에서 읽습니다.

```env
MONITOR_USERNAME=<MONITOR_USERNAME>
MONITOR_PASSWORD=<MONITOR_PASSWORD>
```

인증 정보가 설정되지 않으면 보호 대상 엔드포인트는 익명으로 열리지 않고 `503 Service Unavailable`을 반환하도록 닫힌 상태로 동작합니다.

### 2. 최소 공개 헬스 체크 엔드포인트 추가

컨테이너 오케스트레이션과 리버스 프록시 헬스 체크를 위해 가벼운 공개 프로브 두 개를 추가했습니다.

- `/livez`
- `/readyz`

`/readyz`는 `ready` 또는 `not_ready`만 반환하며, 데이터베이스 장애 세부 정보를 외부에 노출하지 않습니다.

### 3. Trusted Host 필터링 적용

애플리케이션은 이제 허용된 `Host` 헤더 목록만 받도록 제한합니다.

```env
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
```

이 설정은 예상하지 못한 Host 헤더 값으로 인한 오용 가능성을 줄이는 데 도움이 됩니다.

### 4. Nginx 요청 제한과 메서드 제한

리버스 프록시에 아래 제어를 추가했습니다.

- 요청 수 제한
- 연결 수 제한
- `GET`, `HEAD`만 허용
- 숨김 파일 차단
- `server_tokens off`
- `Cache-Control: no-store`

이 제어들은 단순 스크래핑과 의도치 않은 정보 노출 가능성을 줄이기 위한 것입니다.

### 5. API 문서는 명시적으로 켠 경우에만 노출

Swagger 문서는 이제 기본값으로 노출되지 않습니다.

```env
ENABLE_API_DOCS=false
```

문서를 활성화하더라도 Basic Auth 보호는 그대로 유지됩니다.

### 6. 운영 액션 추적 추가

보호된 운영 액션은 이제 단순 명령 실행으로 끝나지 않고 아래 정보를 함께 남깁니다.

- 액션 종류
- 수행자
- 수행 시각
- 성공 또는 실패 결과

이 기준을 추가한 이유는 운영 도구에서 "누가 조치를 실행했는가"가 보안과 운영 감사성 모두에 중요하기 때문이다.

### 7. 공개 프로브와 운영 정보의 분리 유지

`/livez`, `/readyz`는 외부 프로브와 배포 시스템을 위한 최소 노출 범위를 유지하고,  
`/health`, `/alerts`, `/monitoring/status`, `/dashboard`는 인증된 운영자만 볼 수 있도록 구분한다.

이 구분은 단순 편의가 아니라 정보 노출 경계를 아키텍처 수준에서 분리하려는 선택이다.

## 로컬 검증

인증 없이 요청:

```bash
curl -i http://localhost/health
```

예상 결과:

- 인증이 설정된 경우 `401 Unauthorized`
- 인증 정보가 없는 경우 `503 Service Unavailable`

인증 포함 요청:

```bash
curl -i -u <MONITOR_USERNAME>:<MONITOR_PASSWORD> http://localhost/health
```

준비 상태 요청:

```bash
curl -i http://localhost/readyz
```

예상 결과:

- `{"status":"ready", ...}`와 함께 `200 OK`
- `{"status":"not_ready", ...}`와 함께 `503 Service Unavailable`

## 포트폴리오 관점에서 중요한 이유

이 보강은 이 프로젝트가 관측성 엔드포인트를 공개 데모용 URL이 아니라 실제 운영 자산으로 다룬다는 점을 보여줍니다. 미들웨어, 플랫폼, 인프라 성격의 역할에 더 설득력 있는 신호가 됩니다.

또한 운영 액션 추적까지 포함함으로써, 단순 조회형 상태판이 아니라 운영 통제와 기록까지 의식한 설계라는 점을 설명하기 쉬워진다.
