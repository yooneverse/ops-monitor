# Runtime Security Hardening

## Goal

This document describes the runtime hardening added to Ops Monitor so the service does not expose monitoring data to unauthenticated `curl` requests.

## What Changed

### 1. Basic authentication for sensitive endpoints

The following endpoints now require HTTP Basic Auth:

- `/dashboard`
- `/health`
- `/system`
- `/alerts`
- `/monitoring/status`
- `/docs`
- `/openapi.json`

Credentials are loaded from:

```env
MONITOR_USERNAME=<MONITOR_USERNAME>
MONITOR_PASSWORD=<MONITOR_PASSWORD>
```

If credentials are not configured, protected endpoints fail closed with `503 Service Unavailable` instead of opening anonymously.

### 2. Minimal public health endpoints

Two lightweight public probes were added for container orchestration and reverse proxy health checks:

- `/livez`
- `/readyz`

`/readyz` only returns `ready` or `not_ready` and avoids exposing detailed database failure information.

### 3. Trusted host filtering

The app now enforces an allowlist of valid `Host` headers.

```env
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
```

This helps reduce abuse through unexpected host header values.

### 4. Nginx rate limiting and method restrictions

The reverse proxy now adds:

- request rate limiting
- connection limiting
- `GET` and `HEAD` only
- hidden file blocking
- `server_tokens off`
- `Cache-Control: no-store`

These controls reduce casual scraping and accidental information exposure.

### 5. Authenticated API docs only when explicitly enabled

Swagger is no longer exposed by default.

```env
ENABLE_API_DOCS=false
```

When documentation is enabled, it is still protected by Basic Auth.

## Local Verification

Unauthenticated request:

```bash
curl -i http://localhost/health
```

Expected result:

- `401 Unauthorized` when auth is configured
- `503 Service Unavailable` when auth is missing

Authenticated request:

```bash
curl -i -u <MONITOR_USERNAME>:<MONITOR_PASSWORD> http://localhost/health
```

Readiness request:

```bash
curl -i http://localhost/readyz
```

Expected result:

- `200 OK` with `{"status":"ready", ...}`
- `503 Service Unavailable` with `{"status":"not_ready", ...}`

## Why This Matters For Portfolio Review

This hardening shows that the project treats observability endpoints as operational assets, not public demo routes. That is a stronger signal for middleware, platform, and infrastructure-oriented roles.
