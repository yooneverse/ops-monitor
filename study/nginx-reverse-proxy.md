# Nginx Reverse Proxy

## 1. 학습 목적

Ops Monitor 프로젝트에 Nginx를 추가한 이유와 Reverse Proxy의 기본 동작 원리를 정리한다.

이 문서는 다음 내용을 중심으로 구성한다.

| 구분 | 정리 내용 |
|---|---|
| Nginx 역할 | 왜 FastAPI 앞단에 두는가 |
| Reverse Proxy 개념 | 요청 전달 구조 이해 |
| 설정 항목 | `listen`, `location`, `proxy_pass`, `proxy_set_header` |
| 보안 헤더 | 왜 Nginx에서 함께 처리하는가 |
| 프로젝트 적용 | Compose와 결합된 실제 흐름 |

---

## 2. Reverse Proxy란

Reverse Proxy는 클라이언트 요청을 받아 내부 애플리케이션 서버로 전달하는 중간 서버이다.

```text
Client
  ↓
Reverse Proxy
  ↓
Application Server
```

브라우저는 내부 애플리케이션의 실제 포트나 구조를 직접 알 필요가 없다.  
대신 Reverse Proxy가 요청을 받아 적절한 내부 서비스로 전달한다.

---

## 3. 왜 Nginx를 사용하는가

FastAPI는 API 서버 역할에 집중하고, Nginx는 요청 진입점 관리에 집중할 수 있다.

| 이유 | 설명 |
|---|---|
| 진입점 통일 | 외부 요청을 한 포트에서 수신 |
| 앱 포트 숨김 | FastAPI 8000 포트를 외부에 직접 공개하지 않음 |
| 헤더 제어 | 보안 헤더를 중앙에서 일괄 적용 |
| 확장성 | 향후 HTTPS, 정적 파일, 캐시 적용 가능 |

Ops Monitor에서는 `localhost:80` 요청을 받아 `app:8000`으로 전달한다.

---

## 4. Nginx 핵심 설정

현재 프로젝트의 기본 설정은 다음 구조를 따른다.

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 4.1 `listen`

```nginx
listen 80;
```

Nginx가 수신할 포트를 의미한다.

| 포트 | 의미 |
|---|---|
| 80 | 기본 HTTP 요청 수신 포트 |

---

### 4.2 `location`

```nginx
location / {
    ...
}
```

어떤 경로 요청을 어떻게 처리할지 정의한다.

`/`는 루트 경로 이하의 전반적인 요청을 의미한다.

---

### 4.3 `proxy_pass`

```nginx
proxy_pass http://app:8000;
```

실제 요청을 어느 내부 서비스로 보낼지 지정한다.

여기서 `app`은 Docker Compose 서비스명이다.

| 항목 | 의미 |
|---|---|
| `http://` | HTTP 프로토콜 사용 |
| `app` | Compose 네트워크 내부 서비스명 |
| `8000` | FastAPI 컨테이너 내부 포트 |

---

### 4.4 `proxy_set_header`

프록시를 거치면 원래 클라이언트 정보가 사라질 수 있으므로, 필요한 헤더를 다시 전달한다.

| 설정 | 역할 |
|---|---|
| `Host $host` | 원래 요청 호스트 전달 |
| `X-Real-IP $remote_addr` | 클라이언트 실제 IP 전달 |
| `X-Forwarded-For $proxy_add_x_forwarded_for` | 프록시 경유 IP 체인 전달 |

이 헤더들은 애플리케이션 로깅, 접근 제어, 추후 분석에 중요하다.

---

## 5. 보안 헤더를 왜 Nginx에서 처리하는가

보안 헤더는 애플리케이션 코드에서도 설정할 수 있지만, Nginx에서 중앙 관리하면 여러 앱에 공통 적용하기 쉽다.

Ops Monitor에서는 다음 헤더를 사용했다.

| Header | 목적 |
|---|---|
| `X-Content-Type-Options` | MIME 타입 임의 해석 방지 |
| `X-Frame-Options` | iframe 삽입 방지 |
| `X-XSS-Protection` | 구형 브라우저 XSS 필터 활성화 |
| `Referrer-Policy` | 참조 URL 노출 범위 제한 |

설정 예시는 다음과 같다.

```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

---

## 6. 프로젝트 요청 흐름

```text
Browser Request
  ↓
localhost:80
  ↓
Nginx Container
  ↓
proxy_pass -> app:8000
  ↓
FastAPI Container
  ↓
Response
  ↓
Nginx Header Add
  ↓
Browser
```

이 구조 덕분에 브라우저는 FastAPI 포트를 직접 알지 않아도 된다.

---

## 7. Nginx와 Compose의 연결

Nginx가 `app:8000`에 접근할 수 있는 이유는 Compose가 같은 네트워크에 서비스를 배치하기 때문이다.

| 서비스 | 접근 대상 |
|---|---|
| `nginx` | `app:8000` |
| `app` | `db:5432` |

즉, 서비스명은 내부 DNS 이름처럼 동작한다.

---

## 8. 프로젝트 적용 정리

| 항목 | 적용 내용 |
|---|---|
| 외부 포트 | `80` |
| 내부 앱 포트 | `8000` |
| Reverse Proxy 대상 | `app` 서비스 |
| 보안 헤더 | 4종 적용 |
| FastAPI 직접 노출 | 하지 않음 |
| 대시보드 접근 | Nginx 경유 |

---

## 9. 정리

어제 작업을 통해 Nginx는 단순 웹서버가 아니라, 운영 환경에서 요청 진입점과 보안 헤더, 내부 서비스 연결을 담당하는 핵심 계층이라는 점을 확인했다.

특히 `proxy_pass`와 `proxy_set_header`의 의미를 이해하면, 왜 앱 서버 앞단에 Reverse Proxy를 두는지 구조적으로 설명할 수 있다.
