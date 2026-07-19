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
        :root {
            color-scheme: light;
            --bg: #f3f5f9;
            --panel: #ffffff;
            --panel-alt: #eef3ff;
            --border: #d7dfef;
            --text: #172033;
            --muted: #62708a;
            --ok: #197a43;
            --warn: #b86a00;
            --danger: #b42318;
            --accent: #1858d6;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: "Segoe UI", Arial, sans-serif;
            margin: 0;
            background:
                radial-gradient(circle at top left, rgba(24, 88, 214, 0.08), transparent 28%),
                linear-gradient(180deg, #f7f9fc 0%, var(--bg) 100%);
            color: var(--text);
        }

        .shell {
            max-width: 1240px;
            margin: 0 auto;
            padding: 32px 20px 48px;
        }

        h1,
        h2,
        h3,
        p {
            margin-top: 0;
        }

        h1 {
            margin-bottom: 10px;
            font-size: 32px;
        }

        .subtitle {
            color: var(--muted);
            margin-bottom: 18px;
            max-width: 760px;
            line-height: 1.5;
        }

        .topbar {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 24px;
        }

        .summary-banner {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 16px;
            margin-bottom: 24px;
        }

        .summary-card,
        .section-card,
        .card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: 0 16px 40px rgba(21, 33, 61, 0.06);
        }

        .summary-card {
            padding: 22px 24px;
        }

        .summary-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: #eef7f1;
            color: var(--ok);
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .summary-status.warning {
            background: #fff5e8;
            color: var(--warn);
        }

        .summary-status.danger {
            background: #fff0ef;
            color: var(--danger);
        }

        .summary-copy {
            color: var(--muted);
            line-height: 1.6;
        }

        .meta-list {
            display: grid;
            gap: 12px;
        }

        .meta-row {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            font-size: 14px;
        }

        .meta-row span:first-child {
            color: var(--muted);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
            margin-bottom: 24px;
        }

        .card {
            padding: 20px;
        }

        .label {
            font-size: 14px;
            color: var(--muted);
            margin-bottom: 8px;
        }

        .value {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            word-break: break-word;
        }

        .desc {
            font-size: 13px;
            color: var(--muted);
            line-height: 1.5;
        }

        .connected {
            color: var(--ok);
        }

        .disconnected {
            color: var(--danger);
        }

        .normal {
            color: var(--accent);
        }

        .warning {
            color: var(--warn);
        }

        .architecture {
            padding: 24px;
            margin-bottom: 24px;
        }

        pre {
            background: #111827;
            color: #f9fafb;
            padding: 20px;
            border-radius: 12px;
            overflow-x: auto;
        }

        button {
            padding: 10px 16px;
            border: 1px solid #1347ab;
            border-radius: 10px;
            background-color: var(--accent);
            color: white;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background-color: #164ec2;
        }

        .button-area {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 24px;
        }

        .button-meta {
            color: var(--muted);
            font-size: 14px;
        }

        .alert-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 12px;
        }

        .alert-item {
            border-left: 4px solid var(--accent);
            background: #f9fafb;
            padding: 12px;
            border-radius: 10px;
        }

        .alert-item.incident {
            border-left-color: var(--danger);
        }

        .alert-item.recovery {
            border-left-color: var(--ok);
        }

        .alert-item.resource_alert {
            border-left-color: var(--warn);
        }

        .alert-item.resource_recovery {
            border-left-color: var(--ok);
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
            color: var(--muted);
        }

        .section {
            margin-bottom: 24px;
        }

        .section-card {
            padding: 24px;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: baseline;
        }

        .warning-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 14px;
        }

        .warning-item {
            background: #fff8ee;
            border: 1px solid #f5d8a8;
            color: #8f4d00;
            border-radius: 10px;
            padding: 12px 14px;
            font-size: 14px;
            line-height: 1.5;
        }

        @media (max-width: 900px) {
            .summary-banner,
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .topbar {
                align-items: flex-start;
                flex-direction: column;
            }
        }

        @media (max-width: 600px) {
            .shell {
                padding-left: 16px;
                padding-right: 16px;
            }

            .summary-banner,
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="shell">
        <div class="topbar">
            <div>
                <h1>Ops Monitor Dashboard</h1>
                <p class="subtitle">Operational view for Nginx, FastAPI, PostgreSQL, and the monitoring loop. The dashboard now surfaces runtime configuration quality so misconfigured thresholds or intervals are easy to spot before they turn into noisy alerts.</p>
            </div>
            <div class="button-area">
                <button onclick="loadDashboard()">Refresh Dashboard</button>
                <div id="refresh-hint" class="button-meta">Auto refresh: waiting for monitoring status...</div>
            </div>
        </div>

        <div class="summary-banner">
            <div class="summary-card">
                <div id="summary-status" class="summary-status">Collecting runtime signals</div>
                <div id="summary-copy" class="summary-copy">Dashboard is loading the latest API, database, system, and monitoring metadata.</div>
            </div>

            <div class="summary-card meta-list">
                <div class="meta-row">
                    <span>Last dashboard refresh</span>
                    <strong id="checked-time">-</strong>
                </div>
                <div class="meta-row">
                    <span>Last monitor check</span>
                    <strong id="monitor-last-check">-</strong>
                </div>
                <div class="meta-row">
                    <span>Config warnings</span>
                    <strong id="config-warning-count">0</strong>
                </div>
            </div>
        </div>

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
                <div id="discord-desc" class="desc">Webhook configuration status</div>
            </div>

            <div class="card">
                <div class="label">Threshold Policy</div>
                <div id="threshold-summary" class="value">-</div>
                <div id="threshold-desc" class="desc">Runtime alert thresholds for memory and disk</div>
            </div>

            <div class="card">
                <div class="label">Config Status</div>
                <div id="config-status" class="value">checking...</div>
                <div id="config-desc" class="desc">Environment validation and feature toggles</div>
            </div>
        </div>

        <div class="section-card architecture">
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

        <div class="section-card section">
            <div class="section-header">
                <h2>Configuration Warnings</h2>
                <div class="desc">Validation messages for runtime configuration</div>
            </div>
            <div id="warning-list" class="warning-list">
                <div class="desc">No configuration warnings detected.</div>
            </div>
        </div>

        <div class="section-card section">
            <h2>Recent Alerts</h2>
            <div class="desc">Latest incidents, recoveries, and resource threshold events</div>
            <div id="alert-list" class="alert-list">
                <div class="desc">loading...</div>
            </div>
        </div>
    </div>

    <script>
        const dashboardState = {
            refreshTimer: null,
        };

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

        function setStatusValue(element, text, tone) {
            element.textContent = text;
            element.className = "value " + tone;
        }

        function getUsageTone(percent, threshold) {
            return percent >= threshold ? "warning" : "connected";
        }

        function renderWarnings(warnings) {
            const warningList = document.getElementById("warning-list");
            warningList.innerHTML = "";

            if (!warnings || warnings.length === 0) {
                const emptyState = document.createElement("div");
                emptyState.className = "desc";
                emptyState.textContent = "No configuration warnings detected.";
                warningList.appendChild(emptyState);
                return;
            }

            warnings.forEach(message => {
                const item = document.createElement("div");
                item.className = "warning-item";
                item.textContent = message;
                warningList.appendChild(item);
            });
        }

        function renderAlerts(alerts) {
            const alertList = document.getElementById("alert-list");
            alertList.innerHTML = "";

            if (!alerts || alerts.length === 0) {
                const emptyState = document.createElement("div");
                emptyState.className = "desc";
                emptyState.textContent = "No recent alerts.";
                alertList.appendChild(emptyState);
                return;
            }

            const recentAlerts = alerts.slice(0, 5);

            recentAlerts.forEach(alert => {
                const item = document.createElement("div");
                item.className = "alert-item " + alert.type;
                const title = document.createElement("div");
                const meta = document.createElement("div");

                title.className = "alert-title";
                title.textContent = alert.message;

                meta.className = "alert-meta";
                meta.textContent =
                    "type: " + alert.type +
                    " | target: " + alert.target +
                    " | status: " + alert.status +
                    " | time: " + alert.timestamp;

                item.appendChild(title);
                item.appendChild(meta);
                alertList.appendChild(item);
            });
        }

        function renderSummary(health, monitoring) {
            const summaryStatus = document.getElementById("summary-status");
            const summaryCopy = document.getElementById("summary-copy");
            const warningCount = monitoring.config_warnings.length;
            const databaseConnected = health.database.status === "connected";

            if (!databaseConnected) {
                summaryStatus.textContent = "Database attention required";
                summaryStatus.className = "summary-status danger";
                summaryCopy.textContent = "The API is reachable, but the database is not connected. Use the alert history below to confirm whether this is a fresh incident or an ongoing outage.";
                return;
            }

            if (warningCount > 0) {
                summaryStatus.textContent = "Runtime configuration needs review";
                summaryStatus.className = "summary-status warning";
                summaryCopy.textContent = "Core services are reachable, but one or more runtime settings were invalid and have fallen back to safe defaults. Review the configuration warnings before trusting alert timing or threshold behavior.";
                return;
            }

            summaryStatus.textContent = "Runtime signals look healthy";
            summaryStatus.className = "summary-status";
            summaryCopy.textContent = "API, database, and monitoring metadata are aligned. Thresholds, credentials, and background polling are all configured without validation warnings.";
        }

        function scheduleAutoRefresh(intervalSeconds) {
            if (dashboardState.refreshTimer) {
                window.clearTimeout(dashboardState.refreshTimer);
            }

            const safeIntervalSeconds = Math.max(intervalSeconds || 30, 15);
            document.getElementById("refresh-hint").textContent =
                "Auto refresh every " + safeIntervalSeconds + "s";

            dashboardState.refreshTimer = window.setTimeout(loadDashboard, safeIntervalSeconds * 1000);
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
            const discordDesc = document.getElementById("discord-desc");
            const monitorLastCheck = document.getElementById("monitor-last-check");
            const thresholdSummary = document.getElementById("threshold-summary");
            const thresholdDesc = document.getElementById("threshold-desc");
            const configStatus = document.getElementById("config-status");
            const configDesc = document.getElementById("config-desc");
            const configWarningCount = document.getElementById("config-warning-count");

            try {
                const [health, system, alerts, monitoring] = await Promise.all([
                    loadHealth(),
                    loadSystem(),
                    loadAlerts(),
                    loadMonitoringStatus(),
                ]);
                const thresholds = monitoring.thresholds || { memory_percent: 80, disk_percent: 80 };
                const warningCount = monitoring.config_warnings.length;

                setStatusValue(apiStatus, health.api, "connected");
                setStatusValue(dbStatus, health.database.status, health.database.status);

                checkedTime.textContent = health.timestamp;
                monitorLastCheck.textContent = monitoring.last_check || "-";
                configWarningCount.textContent = String(warningCount);

                memoryStatus.textContent = system.memory.percent + "%";
                memoryStatus.className = "value " + getUsageTone(system.memory.percent, thresholds.memory_percent);
                memoryDesc.textContent =
                    system.memory.used_gb + "GB / " + system.memory.total_gb +
                    "GB used (threshold " + thresholds.memory_percent + "%)";

                diskStatus.textContent = system.disk.percent + "%";
                diskStatus.className = "value " + getUsageTone(system.disk.percent, thresholds.disk_percent);
                diskDesc.textContent =
                    system.disk.used_gb + "GB / " + system.disk.total_gb +
                    "GB used (threshold " + thresholds.disk_percent + "%)";

                setStatusValue(
                    monitoringStatus,
                    monitoring.enabled ? "running" : "stopped",
                    monitoring.enabled ? "connected" : "disconnected"
                );
                monitoringDesc.textContent =
                    "interval " + monitoring.interval_seconds +
                    "s" + (monitoring.api_docs_enabled ? " | docs enabled" : " | docs disabled");

                setStatusValue(
                    discordStatus,
                    monitoring.discord_webhook_configured ? "enabled" : "disabled",
                    monitoring.discord_webhook_configured ? "connected" : "warning"
                );
                discordDesc.textContent =
                    monitoring.monitor_auth_configured
                        ? "Webhook and monitor credentials are configured independently."
                        : "Webhook can work without API credentials, but protected endpoints still need auth.";

                thresholdSummary.textContent =
                    "mem " + thresholds.memory_percent + "% / disk " + thresholds.disk_percent + "%";
                thresholdSummary.className = "value normal";
                thresholdDesc.textContent = "Background alerts use these values for resource warning and recovery events.";

                setStatusValue(
                    configStatus,
                    warningCount === 0 ? "healthy" : "check",
                    warningCount === 0 ? "connected" : "warning"
                );
                configDesc.textContent =
                    "auth " + (monitoring.monitor_auth_configured ? "configured" : "missing") +
                    " | " + warningCount + " validation warning(s)";

                renderSummary(health, monitoring);
                renderWarnings(monitoring.config_warnings);
                renderAlerts(alerts);
                scheduleAutoRefresh(monitoring.interval_seconds);

            } catch (error) {
                setStatusValue(apiStatus, "error", "disconnected");
                setStatusValue(dbStatus, "unknown", "disconnected");
                setStatusValue(memoryStatus, "unknown", "disconnected");
                setStatusValue(diskStatus, "unknown", "disconnected");
                setStatusValue(monitoringStatus, "unknown", "disconnected");
                setStatusValue(discordStatus, "unknown", "disconnected");
                setStatusValue(thresholdSummary, "-", "disconnected");
                setStatusValue(configStatus, "unknown", "disconnected");
                monitorLastCheck.textContent = "-";
                checkedTime.textContent = "-";
                configWarningCount.textContent = "-";
                document.getElementById("summary-status").textContent = "Dashboard request failed";
                document.getElementById("summary-status").className = "summary-status danger";
                document.getElementById("summary-copy").textContent = "The dashboard could not load one or more protected endpoints. Verify API credentials and backend availability, then refresh again.";
                document.getElementById("refresh-hint").textContent = "Auto refresh every 30s";

                renderWarnings(["Dashboard refresh failed. Verify credentials and backend connectivity."]);
                renderAlerts([]);
                scheduleAutoRefresh(30);
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
