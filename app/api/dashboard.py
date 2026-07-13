from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.services.alert_history import get_alert_history
from app.services.monitoring_loop import get_monitoring_status

router = APIRouter()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Ops Monitor Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f7fb;
            color: #222;
        }

        h1 {
            margin-bottom: 8px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 32px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        }

        .label {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }

        .value {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .desc {
            font-size: 13px;
            color: #777;
        }

        .connected {
            color: #16803c;
        }

        .disconnected {
            color: #c62828;
        }

        .normal {
            color: #2563eb;
        }

        .warning {
            color: #d97706;
        }

        .architecture {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            margin-bottom: 24px;
        }

        pre {
            background: #111827;
            color: #f9fafb;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
        }

        button {
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            background-color: #2563eb;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background-color: #1d4ed8;
        }

        .button-area {
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
        }

        .alert-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 12px;
        }

        .alert-item {
            border-left: 4px solid #2563eb;
            background: #f9fafb;
            padding: 12px;
            border-radius: 8px;
        }

        .alert-item.incident {
            border-left-color: #c62828;
        }

        .alert-item.recovery {
            border-left-color: #16803c;
        }

        .alert-item.resource_alert {
            border-left-color: #d97706;
        }

        .alert-item.resource_recovery {
            border-left-color: #16803c;
        }

        .alert-item.notification_error {
            border-left-color: #7c3aed;
        }

        .alert-title {
            font-weight: bold;
            margin-bottom: 4px;
        }

        .alert-meta {
            font-size: 13px;
            color: #666;
        }

        .section {
            margin-bottom: 24px;
        }

        @media (max-width: 900px) {
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 600px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <h1>Ops Monitor Dashboard</h1>
    <p class="subtitle">Operational view for Nginx, FastAPI, PostgreSQL, and the monitoring loop</p>

    <div class="grid">
        <div class="card">
            <div class="label">API Status</div>
            <div id="api-status" class="value">checking...</div>
            <div class="desc">FastAPI application response status</div>
        </div>

        <div class="card">
            <div class="label">Database Status</div>
            <div id="db-status" class="value">checking...</div>
            <div class="desc">PostgreSQL connectivity status</div>
        </div>

        <div class="card">
            <div class="label">Memory Usage</div>
            <div id="memory-status" class="value">checking...</div>
            <div id="memory-desc" class="desc">-</div>
        </div>

        <div class="card">
            <div class="label">Disk Usage</div>
            <div id="disk-status" class="value">checking...</div>
            <div id="disk-desc" class="desc">-</div>
        </div>

        <div class="card">
            <div class="label">Monitoring Status</div>
            <div id="monitoring-status" class="value">checking...</div>
            <div id="monitoring-desc" class="desc">-</div>
        </div>

        <div class="card">
            <div class="label">Discord Alert</div>
            <div id="discord-status" class="value">checking...</div>
            <div class="desc">Webhook configuration status</div>
        </div>

        <div class="card">
            <div class="label">Monitor Interval</div>
            <div id="monitor-interval" class="value">-</div>
            <div class="desc">Background monitoring cycle interval</div>
        </div>

        <div class="card">
            <div class="label">Last Monitor Check</div>
            <div id="monitor-last-check" class="value">-</div>
            <div class="desc">Timestamp of the latest background check</div>
        </div>
    </div>

    <div class="architecture">
        <h2>Current Architecture</h2>
        <pre>Client
  ->
Nginx Container
  ->
FastAPI Container
  ->
PostgreSQL Container
  ->
Monitoring Loop
  ->
Discord Webhook</pre>
    </div>

    <div class="card section">
        <div class="label">Last Checked</div>
        <div id="checked-time" class="value">-</div>
        <div class="desc">Timestamp of the latest dashboard refresh</div>
    </div>

    <div class="card section">
        <h2>Recent Alerts</h2>
        <div class="desc">Latest incidents, recoveries, and resource threshold events</div>
        <div id="alert-list" class="alert-list">
            <div class="desc">loading...</div>
        </div>
    </div>

    <div class="button-area">
        <button onclick="loadDashboard()">Refresh Dashboard</button>
    </div>

    <script>
        async function loadHealth() {
            const response = await fetch("/health");
            return await response.json();
        }

        async function loadSystem() {
            const response = await fetch("/system");
            return await response.json();
        }

        async function loadAlerts() {
            const response = await fetch("/alerts");
            return await response.json();
        }

        async function loadMonitoringStatus() {
            const response = await fetch("/monitoring/status");
            return await response.json();
        }

        function renderAlerts(alerts) {
            const alertList = document.getElementById("alert-list");
            alertList.innerHTML = "";

            if (!alerts || alerts.length === 0) {
                alertList.innerHTML = '<div class="desc">No recent alerts.</div>';
                return;
            }

            const recentAlerts = alerts.slice(0, 5);

            recentAlerts.forEach(alert => {
                const item = document.createElement("div");
                item.className = "alert-item " + alert.type;

                item.innerHTML = `
                    <div class="alert-title">${alert.message}</div>
                    <div class="alert-meta">
                        type: ${alert.type} |
                        target: ${alert.target} |
                        status: ${alert.status} |
                        time: ${alert.timestamp}
                    </div>
                `;

                alertList.appendChild(item);
            });
        }

        async function loadDashboard() {
            const apiStatus = document.getElementById("api-status");
            const dbStatus = document.getElementById("db-status");
            const checkedTime = document.getElementById("checked-time");
            const memoryStatus = document.getElementById("memory-status");
            const memoryDesc = document.getElementById("memory-desc");
            const diskStatus = document.getElementById("disk-status");
            const diskDesc = document.getElementById("disk-desc");

            const monitoringStatus = document.getElementById("monitoring-status");
            const monitoringDesc = document.getElementById("monitoring-desc");
            const discordStatus = document.getElementById("discord-status");
            const monitorInterval = document.getElementById("monitor-interval");
            const monitorLastCheck = document.getElementById("monitor-last-check");

            try {
                const health = await loadHealth();
                const system = await loadSystem();
                const alerts = await loadAlerts();
                const monitoring = await loadMonitoringStatus();

                apiStatus.textContent = health.api;
                apiStatus.className = "value connected";

                dbStatus.textContent = health.database.status;
                dbStatus.className = "value " + health.database.status;

                checkedTime.textContent = health.timestamp;

                memoryStatus.textContent = system.memory.percent + "%";
                memoryStatus.className = "value normal";
                memoryDesc.textContent = system.memory.used_gb + "GB / " + system.memory.total_gb + "GB";

                diskStatus.textContent = system.disk.percent + "%";
                diskStatus.className = "value normal";
                diskDesc.textContent = system.disk.used_gb + "GB / " + system.disk.total_gb + "GB";

                monitoringStatus.textContent = monitoring.enabled ? "running" : "stopped";
                monitoringStatus.className = monitoring.enabled ? "value connected" : "value disconnected";
                monitoringDesc.textContent = "background task";

                discordStatus.textContent = monitoring.discord_webhook_configured ? "enabled" : "disabled";
                discordStatus.className = monitoring.discord_webhook_configured ? "value connected" : "value warning";

                monitorInterval.textContent = monitoring.interval_seconds + "s";
                monitorInterval.className = "value normal";

                monitorLastCheck.textContent = monitoring.last_check || "-";
                monitorLastCheck.className = "value normal";

                renderAlerts(alerts);

            } catch (error) {
                apiStatus.textContent = "error";
                apiStatus.className = "value disconnected";

                dbStatus.textContent = "unknown";
                dbStatus.className = "value disconnected";

                memoryStatus.textContent = "unknown";
                memoryStatus.className = "value disconnected";

                diskStatus.textContent = "unknown";
                diskStatus.className = "value disconnected";

                monitoringStatus.textContent = "unknown";
                monitoringStatus.className = "value disconnected";

                discordStatus.textContent = "unknown";
                discordStatus.className = "value disconnected";

                monitorInterval.textContent = "-";
                monitorLastCheck.textContent = "-";
                checkedTime.textContent = "-";

                renderAlerts([]);
            }
        }

        loadDashboard();
    </script>
</body>
</html>
"""


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return DASHBOARD_HTML


@router.get("/alerts")
def get_alerts() -> list[dict]:
    return get_alert_history()


@router.get("/monitoring/status")
def monitoring_status() -> dict:
    return get_monitoring_status()
