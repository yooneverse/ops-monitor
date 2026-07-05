from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="ko">
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
        <p class="subtitle">Nginx, FastAPI, PostgreSQL 기반 서비스 상태 모니터링</p>

        <div class="grid">
            <div class="card">
                <div class="label">API Status</div>
                <div id="api-status" class="value">checking...</div>
                <div class="desc">FastAPI 서버 응답 상태</div>
            </div>

            <div class="card">
                <div class="label">Database Status</div>
                <div id="db-status" class="value">checking...</div>
                <div class="desc">PostgreSQL 연결 상태</div>
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
        </div>

        <div class="architecture">
            <h2>Current Architecture</h2>
            <pre>Client
  ↓
Nginx Container
  ↓
FastAPI Container
  ↓
PostgreSQL Container</pre>
        </div>

        <div class="card">
            <div class="label">Last Checked</div>
            <div id="checked-time" class="value">-</div>
        </div>

        <br />

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

            async function loadDashboard() {
                const apiStatus = document.getElementById("api-status");
                const dbStatus = document.getElementById("db-status");
                const checkedTime = document.getElementById("checked-time");
                const memoryStatus = document.getElementById("memory-status");
                const memoryDesc = document.getElementById("memory-desc");
                const diskStatus = document.getElementById("disk-status");
                const diskDesc = document.getElementById("disk-desc");

                try {
                    const health = await loadHealth();
                    const system = await loadSystem();

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
                } catch (error) {
                    apiStatus.textContent = "error";
                    apiStatus.className = "value disconnected";

                    dbStatus.textContent = "unknown";
                    dbStatus.className = "value disconnected";

                    memoryStatus.textContent = "unknown";
                    memoryStatus.className = "value disconnected";

                    diskStatus.textContent = "unknown";
                    diskStatus.className = "value disconnected";

                    checkedTime.textContent = "-";
                }
            }

            loadDashboard();
        </script>
    </body>
    </html>
    """