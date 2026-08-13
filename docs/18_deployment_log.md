# 첫 배포 기록 - 2026-08-12

## 1. 개요

2026년 8월 12일 Ops Monitor AWS EC2 첫 배포.

이번 배포의 목적은 단일 호스트 기준으로 애플리케이션 실행, 공개 헬스 체크 응답, 준비 상태 확인, 대시보드 접근 가능 여부를 검증하는 것이다.

---

## 2. 배포 환경

- 클라우드: AWS EC2
- 리전: `ap-northeast-2`
- 인스턴스 타입: `t4g.small`
- 운영체제: Ubuntu 계열 AMI 사용
- 실행 방식: Docker Compose

---

## 3. 확인 항목

- 인스턴스 생성 및 상태 검사 통과
- Docker 및 Docker Compose 설치
- 프로젝트 실행
- `GET /` 확인
- `GET /livez` 확인
- `GET /readyz` 확인
- `/dashboard` 접근 확인
- Basic Auth 로그인 확인

---

## 4. 결과

- 인스턴스 생성 완료
- 상태 검사 통과 완료
- 컨테이너 실행 완료
- `GET /` 응답 확인 완료
- `GET /livez` 응답 확인 완료
- `/readyz` 응답이 `ready` 상태로 확인됨
- 대시보드 접근 가능
- Basic Auth 로그인 및 상태 패널 확인 가능

---

## 5. 첨부 캡처 기준

아래 항목을 배포 확인 증거로 사용한다.

- `docs/assets/deploy-2026-08-12/readyz.png`
- `docs/assets/deploy-2026-08-12/dashboard.png`
- `docs/assets/deploy-2026-08-12/docker-compose-ps.png`

실제 파일 이름은 다를 수 있으며, 배포 확인 시 아래 내용이 포함되도록 정리한다.

- `readyz`: `status=ready`
- `dashboard`: 인증 후 정상 화면
- `docker compose ps`: `nginx`, `app`, `db`, `notes` 실행 상태

---

## 6. 메모

- `t4g.small` 사용 시 AMI 아키텍처를 `arm64`로 맞춰야 함
- `/readyz`는 애플리케이션 기동 여부가 아니라 준비 상태를 확인하는 용도로 사용했다.
- 초기 배포 과정에서 예시 placeholder 값이 `.env`에 남아 있으면 DB 연결과 대시보드 인증이 모두 실패할 수 있음을 확인했다.
