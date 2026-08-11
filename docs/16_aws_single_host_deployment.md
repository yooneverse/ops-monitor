# AWS 단일 호스트 배포 메모

## 1. 목적

이 문서는 Ops Monitor를 AWS에서 단일 호스트로 배포할 때 기준이 되는 구성을 정리한다.

현재 범위는 기능 확장보다 배포, 점검, 장애 재현, 복구 확인 흐름을 검증하는 데 둔다.

---

## 2. 배포 기준

- 인스턴스: `EC2 t4g.small`
- 운영체제: `Ubuntu 24.04 LTS` 또는 Amazon Linux 계열
- 실행 방식: `Docker Compose`
- 배포 단위: `nginx`, `app`, `db`, `notes` 컨테이너를 한 호스트에서 함께 실행

---

## 3. 현재 배포 구성

```text
Internet
  ->
EC2
  ->
Nginx :80
  ->
FastAPI app :8000
  ->
PostgreSQL :5432
  ->
Demo Notes :8010
```

외부 공개는 `Nginx`를 통해서만 처리한다.

`db`, `notes` 컨테이너는 실행 중이어도 보안 그룹에서는 외부 포트를 열지 않는다.

---

## 4. 사용하는 것

- `EC2 t4g.small` 1대
- `gp3` EBS 최소 용량
- 보안 그룹
- Docker Engine / Docker Compose
- `.env` 기반 런타임 설정

---

## 5. 사용하지 않는 것

- `EKS`
- `Kubernetes`
- `RDS`
- `NAT Gateway`
- `Load Balancer`
- `Elastic IP`

이 프로젝트의 현재 목적은 다중 노드 운영이 아니라 단일 호스트에서 운영 흐름을 검증하는 것이다.

---

## 6. 보안 그룹 기준

- 열어둘 포트: `80`
- 필요 시 일시적으로 열 포트: `22`
- 열지 않을 포트: `5432`, `8010`

SSH가 필요 없으면 `22`도 닫아두는 편이 낫다.

---

## 7. 환경 변수 기준

`.env.example`을 기준으로 아래 값을 실제 배포용으로 채운다.

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `DATABASE_URL`
- `MONITOR_USERNAME`
- `MONITOR_PASSWORD`
- `ALLOWED_HOSTS`
- `MONITOR_INTERVAL_SECONDS`
- `MEMORY_ALERT_THRESHOLD`
- `DISK_ALERT_THRESHOLD`
- `DISCORD_WEBHOOK_URL`

`ALLOWED_HOSTS`에는 `localhost` 외에 EC2 public IPv4 또는 연결할 도메인을 포함해야 한다.

예:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,12.34.56.78
```

---

## 8. 배포 순서

1. EC2 생성
2. Docker와 Docker Compose 설치
3. 프로젝트 코드 업로드 또는 클론
4. `.env` 작성
5. `docker compose up --build -d` 실행
6. `/`, `/livez`, `/readyz`, `/dashboard` 확인

---

## 9. 배포 후 확인 항목

- `GET /`
- `GET /livez`
- `GET /readyz`
- `GET /dashboard`
- 로그 디렉터리 생성 여부
- DB 연결 정상 여부
- `notes` 상태 반영 여부

---

## 10. 비용 메모

- 컴퓨트는 `t4g.small` 무료 체험 범위를 우선 활용한다.
- 비용 위험은 공인 IPv4, EBS, 불필요한 관리형 서비스에서 커진다.
- 인스턴스를 사용하지 않을 때는 `Stop` 상태로 전환한다.

---

## 11. 현재 판단

Ops Monitor는 현재 구조상 단일 호스트 배포만으로도 다음을 검증할 수 있다.

- 공개 헬스 체크와 보호 API 분리
- 점검 루프 실행
- 장애 감지와 복구 확인
- 운영 액션 수행과 이력 기록

따라서 첫 배포는 단순한 구성을 유지하는 편이 적절하다.
