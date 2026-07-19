# Runtime Configuration Guide

## Overview

This document describes the runtime validation and dashboard visibility that were added to keep `ops-monitor` practical and predictable in daily use.

The goal is simple:

- invalid monitoring settings should not crash the app at startup
- fallback behavior should be visible from the protected monitoring API
- operators should be able to see threshold and configuration quality from `/dashboard`

## What Changed

### 1. Safe integer validation

The application now validates key numeric environment variables before using them.

| Variable | Default | Accepted Range | Fallback Behavior |
|---|---|---|---|
| `MONITOR_INTERVAL_SECONDS` | `30` | `5` to `3600` | Reverts to `30` |
| `MEMORY_ALERT_THRESHOLD` | `80` | `1` to `100` | Reverts to `80` |
| `DISK_ALERT_THRESHOLD` | `80` | `1` to `100` | Reverts to `80` |

Blank credential values such as `"   "` are also normalized to `None`, so the app treats them as missing configuration instead of partially valid input.

### 2. Monitoring status now exposes configuration metadata

`GET /monitoring/status` now includes:

- `monitor_auth_configured`
- `api_docs_enabled`
- `thresholds.memory_percent`
- `thresholds.disk_percent`
- `config_warnings`

Example response:

```json
{
  "enabled": true,
  "interval_seconds": 30,
  "discord_webhook_configured": false,
  "monitor_auth_configured": true,
  "api_docs_enabled": false,
  "thresholds": {
    "memory_percent": 80,
    "disk_percent": 80
  },
  "config_warnings": [],
  "last_check": "2026-07-19T10:15:00"
}
```

This makes it easier to understand whether the monitor is healthy because of intended configuration or because the app silently fell back to defaults.

### 3. Dashboard shows why a status looks healthy or risky

The dashboard now surfaces:

- auto-refresh timing based on the monitoring interval
- threshold values used for memory and disk alerts
- a configuration health card
- visible configuration warnings
- safer alert rendering without string-based HTML injection

This is intentionally small-scope. It does not add a new admin system or a large front-end framework; it only makes the current operational screen more trustworthy.

## Recommended Runtime Checks

When changing `.env`, verify these three things together:

1. `GET /monitoring/status` shows the expected interval and thresholds.
2. `/dashboard` shows `Config Status = healthy`.
3. `config_warnings` is empty unless you are intentionally testing fallback behavior.

## Notes

- Fallback behavior is designed to keep the app running, not to hide bad configuration.
- If warnings appear in the dashboard, treat them as configuration debt to clean up soon.
- The validation ranges are conservative on purpose so the monitoring loop does not become excessively noisy or too slow to react.
