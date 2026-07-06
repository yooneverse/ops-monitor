# Docker Compose Runtime

## 1. 학습 목적

Ops Monitor 프로젝트에서 Docker Compose가 단순 DB 실행 도구를 넘어, 애플리케이션 런타임 전체를 연결하는 방식으로 확장된 과정을 정리한다.

이 문서는 다음 개념을 이해하는 데 목적이 있다.

| 구분 | 정리 내용 |
|---|---|
| Dockerfile | FastAPI 애플리케이션 이미지 구성 |
| Compose 서비스 | `nginx`, `app`, `db` 역할 분리 |
| 네트워크 연결 | 컨테이너 간 통신 방식 |
| 설정 차이 | `ports`, `expose`, `env_file`, `depends_on` 의미 |
| 운영 관점 | 멀티 컨테이너 구성을 파일로 관리하는 이유 |

---

## 2. 왜 Compose 구성이 확장되었는가

초기에는 PostgreSQL만 컨테이너로 실행해도 프로젝트 목적을 일부 달성할 수 있었다.

하지만 실제 운영 구조에 가까워지려면 API 서버와 Reverse Proxy도 함께 컨테이너로 실행할 필요가 있다.

| 단계 | 구성 |
|---|---|
| 초기 | Local FastAPI + PostgreSQL Container |
| 확장 | Nginx Container + FastAPI Container + PostgreSQL Container |

이 변화는 개발 편의성보다 운영 구조 학습에 더 큰 의미가 있다.

---

## 3. Dockerfile의 역할

Dockerfile은 애플리케이션 이미지를 만드는 설계서이다.

Ops Monitor의 FastAPI 컨테이너는 다음 흐름으로 구성된다.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile 핵심 개념

| 명령 | 의미 |
|---|---|
| `FROM` | 기반 이미지 선택 |
| `WORKDIR` | 컨테이너 내부 작업 경로 설정 |
| `COPY` | 파일 복사 |
| `RUN` | 이미지 빌드 중 명령 실행 |
| `EXPOSE` | 컨테이너 내부 서비스 포트 명시 |
| `CMD` | 컨테이너 시작 시 기본 실행 명령 |

---

## 4. Compose 서비스 구조

현재 Compose는 세 개의 서비스를 사용한다.

| Service | 역할 |
|---|---|
| `nginx` | 외부 요청 수신 및 Reverse Proxy |
| `app` | FastAPI 애플리케이션 실행 |
| `db` | PostgreSQL 실행 |

구조는 다음과 같다.

```text
Client
  ↓
nginx
  ↓
app
  ↓
db
```

---

## 5. Compose 주요 설정

### 5.1 `build`

```yaml
app:
  build: .
```

`build`는 현재 디렉터리의 Dockerfile을 기준으로 이미지를 생성한다.

즉, `app` 서비스는 미리 만들어진 공개 이미지가 아니라 프로젝트 코드로 직접 빌드된 이미지이다.

---

### 5.2 `env_file`

```yaml
env_file:
  - .env
```

`env_file`은 컨테이너가 사용할 환경변수를 외부 파일에서 읽어오게 한다.

| 장점 | 설명 |
|---|---|
| 민감정보 분리 | DB 계정 정보와 연결 문자열을 코드 밖에서 관리 |
| 설정 재사용 | 여러 서비스가 같은 환경변수를 사용할 수 있음 |
| 문서화 용이 | `.env.example`과 짝으로 운영 가능 |

---

### 5.3 `ports`와 `expose`

이 둘은 비슷해 보이지만 목적이 다르다.

| 설정 | 의미 |
|---|---|
| `ports` | 호스트와 컨테이너 포트를 연결 |
| `expose` | 컨테이너 내부 네트워크에서 사용할 포트를 명시 |

Ops Monitor에서는 다음과 같이 사용한다.

| 서비스 | 설정 | 이유 |
|---|---|---|
| `nginx` | `ports: "80:80"` | 브라우저가 호스트를 통해 접근해야 함 |
| `db` | `ports: "5432:5432"` | 필요 시 로컬에서 직접 DB 확인 가능 |
| `app` | `expose: "8000"` | 외부 공개 없이 Nginx만 접근하면 됨 |

즉, `app`은 외부에 직접 노출하지 않고 Nginx 뒤에 배치하는 구조이다.

---

### 5.4 `depends_on`

```yaml
depends_on:
  - app
```

`depends_on`은 서비스 시작 순서를 표현한다.

| 관계 | 의미 |
|---|---|
| `nginx -> app` | Nginx가 app 서비스에 의존 |
| `app -> db` | app 서비스가 db 서비스에 의존 |

주의할 점은 `depends_on`이 "완전한 준비 완료"를 보장하는 것은 아니라는 것이다.  
단지 컨테이너 시작 순서를 표현하는 역할에 가깝다.

---

## 6. 컨테이너 간 통신 방식

Compose 환경에서는 같은 네트워크 안의 서비스명이 DNS 이름처럼 동작한다.

예를 들어 FastAPI 컨테이너에서 PostgreSQL에 연결할 때 host를 `db`로 사용할 수 있다.

```env
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@db:5432/<DB_NAME>
```

이 점이 로컬 실행 환경과 가장 큰 차이 중 하나이다.

| 실행 방식 | DB Host |
|---|---|
| 로컬 FastAPI + 컨테이너 DB | `localhost` |
| Compose 내부 FastAPI + 컨테이너 DB | `db` |

---

## 7. 왜 Nginx 앞단 구조가 필요한가

브라우저가 FastAPI에 직접 붙는 구조도 가능하지만, 운영 환경에서는 보통 Reverse Proxy를 앞단에 둔다.

그 이유는 다음과 같다.

| 이유 | 설명 |
|---|---|
| 요청 진입점 통일 | 외부 요청을 한 곳에서 수신 |
| 포트 추상화 | 내부 앱 포트를 외부에 직접 노출하지 않음 |
| 보안 헤더 처리 | 응답 헤더를 중앙에서 관리 |
| 확장성 | 정적 파일, SSL, 로드밸런싱 등 추가 가능 |

---

## 8. Compose 실행 흐름

```text
docker compose up --build -d
  ↓
Dockerfile 기반 app 이미지 빌드
  ↓
db 컨테이너 실행
  ↓
app 컨테이너 실행
  ↓
nginx 컨테이너 실행
  ↓
localhost 요청 수신
  ↓
Nginx가 app:8000으로 전달
```

---

## 9. 프로젝트 적용 정리

| 항목 | 적용 내용 |
|---|---|
| FastAPI 컨테이너화 | Dockerfile 작성 |
| Compose 확장 | `nginx`, `app`, `db` 구성 |
| 내부 포트 분리 | `app`은 `expose: 8000` 사용 |
| 외부 진입 | `nginx`가 `80:80`으로 공개 |
| 환경변수 주입 | `.env`를 `env_file`로 사용 |
| 네트워크 연결 | DB host를 `db` 서비스명으로 사용 |

---

## 10. 정리

어제 작업을 통해 Docker Compose는 단순히 컨테이너 여러 개를 켜는 도구가 아니라, 서비스 간 관계와 네트워크 구조, 실행 설정을 하나의 문서형 설정 파일로 관리하는 도구라는 점을 확인했다.

특히 `Dockerfile`, `env_file`, `expose`, `ports`, `depends_on`의 차이를 이해하면, 로컬 실행 구조와 운영용 컨테이너 구조가 어떻게 달라지는지 명확하게 파악할 수 있다.
