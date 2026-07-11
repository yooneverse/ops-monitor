# Docker Compose Healthcheck Troubleshooting

## 1. 문제 상황

`ops-monitor-app` 컨테이너가 실행 중인데도 Docker Compose에서 `unhealthy`로 판정되는 문제가 발생할 수 있습니다.

이번 케이스에서는 다음 메시지가 확인됐습니다.

```text
dependency failed to start: container ops-monitor-app is unhealthy
```

## 2. 실제 원인

직접 원인은 앱 속도 자체보다 헬스체크 경로와 실행 중 코드의 불일치였습니다.

- Compose healthcheck는 `/livez`를 호출하고 있었습니다.
- 하지만 실행 중 컨테이너에는 예전 코드가 올라가 있어 `/livez`가 없었습니다.
- 결과적으로 앱은 떠 있어도 healthcheck는 계속 `404 Not Found`를 받아 `unhealthy`가 됐습니다.

즉, 이번 문제는 "앱이 너무 느려서 죽음"보다는 "최신 코드가 컨테이너에 반영되지 않음"에 더 가까웠습니다.

## 3. 이번에 적용한 해결

### 3.1 최신 코드가 바로 반영되도록 Compose 수정

`app` 서비스에 바인드 마운트를 추가했습니다.

```yaml
volumes:
  - ./app:/app/app:ro
  - ./logs:/app/logs
```

이렇게 하면 로컬의 `app` 디렉터리 코드가 컨테이너 안에서 바로 보입니다.

장점:

- 예전 이미지가 남아 있어서 라우트가 어긋나는 문제를 줄일 수 있음
- 작은 코드 수정 후 매번 전체 rebuild 부담이 줄어듦

주의:

- Python 패키지 목록이 바뀌면 여전히 이미지 rebuild는 필요함

### 3.2 DB 체크 경량화

기존에는 상태 확인 때마다 DB 엔진을 새로 만들 가능성이 있었습니다.  
이번에는 같은 `DATABASE_URL`에 대해서는 엔진을 재사용하도록 바꿨습니다.

적용 포인트:

- `create_engine()` 캐싱
- `pool_pre_ping=True`
- PostgreSQL 연결 타임아웃 설정

효과:

- `/readyz`, `/health`, 백그라운드 모니터링 루프에서 반복 비용 감소
- DB 응답 지연 시 오래 멈추는 현상 완화

### 3.3 모니터링 루프 토글 추가

개발 중에는 백그라운드 모니터링까지 항상 켤 필요가 없을 수 있습니다.

```env
ENABLE_MONITORING_LOOP=true
```

필요 시 `false`로 두면 앱은 뜨되 모니터링 루프는 시작하지 않습니다.

효과:

- 개발 중 초기 부하 감소
- 원인 분리 테스트가 쉬워짐

## 4. 확인 방법

### 상태 확인

```bash
docker-compose ps
docker-compose logs app --tail=100
```

정상일 때는 `/livez`가 `404`가 아니라 성공 응답을 반환해야 합니다.

### 라우트 확인

```bash
docker-compose exec -T app python -c "import app.main as m; print([getattr(route, 'path', None) for route in m.app.routes])"
```

여기서 `/livez`, `/readyz`가 보여야 최신 코드가 반영된 것입니다.

## 5. 정리

이번 사례에서 기억할 핵심은 다음 두 가지입니다.

1. `unhealthy`는 무조건 느림 문제는 아니다.
2. Docker healthcheck와 실제 컨테이너 코드가 서로 맞는지 먼저 확인해야 한다.

Compose 기반 프로젝트에서는 "앱 코드", "이미지", "컨테이너 실행 상태"가 서로 어긋날 수 있으므로, 헬스체크 실패 시에는 로그와 현재 컨테이너 내부 라우트를 함께 보는 습관이 중요합니다.
