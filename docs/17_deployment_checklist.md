# 배포 전 체크리스트

## 1. 목적

이 문서는 Ops Monitor를 AWS 단일 호스트에 배포하기 전에 확인할 항목과 배포 직후 점검 항목을 정리한다.

---

## 2. 배포 전 확인

### 코드와 문서

- [ ] 최신 변경 사항이 커밋되어 있다.
- [ ] README의 프로젝트 설명과 실제 구현 범위가 맞다.
- [ ] 아키텍처 문서가 단일 호스트 Compose 구성을 기준으로 정리되어 있다.

### 인프라 기준

- [ ] 배포 대상은 `EC2 t4g.small` 1대로 정했다.
- [ ] 불필요한 서비스(`EKS`, `RDS`, `NAT Gateway`, `Load Balancer`, `Elastic IP`)를 만들지 않는다.
- [ ] 스토리지는 `gp3` 최소 용량으로 잡는다.

### 보안 그룹

- [ ] `80` 포트만 외부에 연다.
- [ ] `22` 포트는 필요할 때만 연다.
- [ ] `5432`, `8010` 포트는 외부에 열지 않는다.

### 런타임 준비

- [ ] Docker가 설치되어 있다.
- [ ] Docker Compose가 동작한다.
- [ ] `.env` 파일을 만들었다.
- [ ] `.env`에 DB 계정과 모니터링 계정을 채웠다.
- [ ] `ALLOWED_HOSTS`에 EC2 public IPv4 또는 도메인을 넣었다.
- [ ] `ENABLE_API_DOCS` 값이 의도한 상태인지 확인했다.

---

## 3. 필수 환경 변수

- [ ] `POSTGRES_USER`
- [ ] `POSTGRES_PASSWORD`
- [ ] `POSTGRES_DB`
- [ ] `DATABASE_URL`
- [ ] `MONITOR_USERNAME`
- [ ] `MONITOR_PASSWORD`
- [ ] `ALLOWED_HOSTS`
- [ ] `MONITOR_INTERVAL_SECONDS`
- [ ] `MEMORY_ALERT_THRESHOLD`
- [ ] `DISK_ALERT_THRESHOLD`

선택 항목:

- [ ] `DISCORD_WEBHOOK_URL`
- [ ] `MONITORING_EXCLUDED_TARGETS`
- [ ] `ENABLE_API_DOCS`
- [ ] `LOG_DIR`

---

## 4. 배포 절차

- [ ] 프로젝트 코드를 서버에 올렸다.
- [ ] `.env`를 서버 기준으로 작성했다.
- [ ] `docker compose up --build -d`를 실행했다.
- [ ] 컨테이너가 모두 실행 중인지 확인했다.

확인 명령 예시:

```bash
docker compose ps
docker compose logs --tail=100
```

---

## 5. 배포 직후 점검

- [ ] `GET /` 응답 확인
- [ ] `GET /livez` 응답 확인
- [ ] `GET /readyz` 응답 확인
- [ ] `GET /dashboard` 접근 확인
- [ ] Basic Auth 동작 확인
- [ ] 로그 디렉터리 생성 확인
- [ ] DB 연결 상태 확인
- [ ] `demo_notes` 상태 반영 확인

---

## 6. 장애 재현 후보

### 후보 1. DB 중단

- [ ] DB 컨테이너 중단
- [ ] `/readyz` 상태 변화 확인
- [ ] 대시보드 상태 변화 확인
- [ ] alert history 또는 run report 기록 확인
- [ ] DB 재기동 후 recovery 확인

### 후보 2. demo-notes 중단

- [ ] `notes` 컨테이너 중단
- [ ] 대시보드 상태 변화 확인
- [ ] 이벤트 기록 확인
- [ ] 재기동 후 recovery 확인

---

## 7. 증거로 남길 항목

- [ ] 정상 배포 화면
- [ ] `/livez` 응답
- [ ] `/readyz` 응답
- [ ] 장애 발생 화면
- [ ] 복구 후 화면
- [ ] run report 또는 alert history
- [ ] 컨테이너 상태 확인 화면

---

## 8. 종료 전 확인

- [ ] 테스트 결과를 다시 확인했다.
- [ ] 캡처 파일 이름을 구분 가능하게 정리했다.
- [ ] 문서와 화면 설명이 같은 용어를 사용한다.
- [ ] 사용하지 않을 때는 인스턴스를 `Stop`한다.
