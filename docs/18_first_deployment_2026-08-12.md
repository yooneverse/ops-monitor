# 첫 배포 기록 - 2026-08-12

## 1. 개요

2026년 8월 12일에 Ops Monitor를 AWS EC2에 처음 배포했다.

이번 배포의 목적은 단일 호스트 기준으로 애플리케이션 실행, 공개 헬스 체크 응답, 준비 상태 확인, 대시보드 접근 가능 여부를 검증하는 것이다.

---

## 2. 배포 환경

- 클라우드: AWS EC2
- 리전: `ap-northeast-2` 또는 실제 배포 리전 확인 필요
- 인스턴스 타입: `t4g.small` 또는 실제 배포 인스턴스 타입 확인 필요
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

---

## 4. 결과

- 인스턴스 생성 완료
- 상태 검사 통과 완료
- 컨테이너 실행 완료
- `/readyz` 응답이 `ready` 상태로 확인됨
- 대시보드 접근 가능

---

## 5. 첨부 예정 캡처

아래 경로는 실제 캡처 파일 저장 후 갱신한다.

- `docs/assets/deploy-2026-08-12/readyz.png`
- `docs/assets/deploy-2026-08-12/dashboard.png`
- `docs/assets/deploy-2026-08-12/docker-compose-ps.png`

---

## 6. 메모

- `t4g.small` 사용 시 AMI 아키텍처를 `arm64`로 맞춰야 인스턴스 선택이 가능했다.
- `docker compose` 명령은 EC2 서버 내부에서 실행해야 한다.
- `/readyz`는 애플리케이션 기동 여부가 아니라 준비 상태를 확인하는 용도로 사용했다.
