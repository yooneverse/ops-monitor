from functools import lru_cache


def build_dashboard_styles() -> str:
    return """
    <style>
        :root {
            color-scheme: light;
            --bg: #f4f8fd;
            --sidebar-bg: #ffffff;
            --content-bg: #f7fbff;
            --panel: #ffffff;
            --panel-muted: #fbfdff;
            --border: #d8e3f1;
            --border-strong: #c8d5e8;
            --text: #1b2738;
            --muted: #677991;
            --accent: #2b86d9;
            --accent-soft: #edf6ff;
            --lime: #88c64c;
            --lime-soft: #f1f8e7;
            --ok: #30945a;
            --warn: #cb8b18;
            --warn-soft: #fff5e5;
            --danger: #c94f45;
            --danger-soft: #fff0ee;
            --shadow: 0 16px 38px rgba(39, 73, 128, 0.08);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            color: var(--text);
            background:
                linear-gradient(180deg, #fafdff 0%, var(--bg) 100%);
            word-break: keep-all;
            overflow-wrap: anywhere;
        }

        h1,
        h2,
        h3,
        p {
            margin-top: 0;
        }

        .dashboard-shell {
            display: grid;
            grid-template-columns: 248px minmax(0, 1fr);
            min-height: 100vh;
        }

        .sidebar {
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
        }

        .brand {
            height: 88px;
            padding: 0 22px;
            display: flex;
            align-items: center;
            background: linear-gradient(135deg, #28c0c8, #2b86d9);
            color: white;
        }

        .brand-mark {
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -0.04em;
        }

        .sidebar-body {
            padding: 16px 14px 24px;
            overflow: auto;
        }

        .search-box {
            width: 100%;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: #f8fbff;
            padding: 10px 12px;
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 18px;
        }

        .nav-section {
            margin-bottom: 20px;
        }

        .nav-title {
            padding: 12px 8px 10px;
            font-size: 12px;
            font-weight: 800;
            color: #7f8ea4;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            border-top: 1px solid #eef3f8;
        }

        .nav-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 10px 8px;
            border-radius: 8px;
            color: var(--text);
            font-size: 14px;
        }

        .nav-item.active {
            background: linear-gradient(90deg, var(--accent-soft), #f8fcff);
            color: var(--accent);
            font-weight: 700;
        }

        .main {
            min-width: 0;
            background: var(--content-bg);
        }

        .utility-bar {
            height: 60px;
            padding: 0 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(10px);
        }

        .utility-left,
        .utility-right {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .icon-button {
            width: 34px;
            height: 34px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: white;
            color: var(--accent);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 700;
        }

        .utility-text {
            font-size: 13px;
            color: var(--muted);
        }

        .avatar {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2b86d9, #88c64c);
            color: white;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 800;
        }

        .content {
            padding: 22px;
        }

        .page-header {
            display: flex;
            align-items: flex-end;
            gap: 14px;
            padding: 10px 4px 22px;
        }

        .page-header h1 {
            margin-bottom: 0;
            font-size: 34px;
            letter-spacing: -0.03em;
        }

        .page-subtitle {
            color: var(--muted);
            font-size: 14px;
            line-height: 1.5;
            padding-bottom: 4px;
        }

        .surface {
            border: 1px solid var(--border);
            border-radius: 14px;
            background: var(--panel);
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .surface + .surface {
            margin-top: 18px;
        }

        .surface-header {
            padding: 18px 22px;
            border-bottom: 1px solid #eef3f8;
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: center;
        }

        .surface-title {
            font-size: 12px;
            font-weight: 800;
            color: #70839d;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .surface-heading {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .surface-copy {
            font-size: 13px;
            color: var(--muted);
            line-height: 1.5;
        }

        .surface-body {
            padding: 18px 18px 20px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }

        .metric-card {
            min-width: 0;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--panel-muted);
            padding: 18px;
            display: grid;
            gap: 12px;
        }

        .metric-card.primary {
            background: linear-gradient(135deg, #f3f8ff, #fbfdff);
            border-color: var(--border-strong);
        }

        .metric-top {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
        }

        .metric-label {
            font-size: 13px;
            font-weight: 700;
            color: #61748f;
        }

        .metric-icon {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: 700;
            color: var(--accent);
            background: linear-gradient(135deg, var(--accent-soft), #f9fcff);
        }

        .metric-icon.lime {
            color: #5b9f1f;
            background: linear-gradient(135deg, var(--lime-soft), #fbfff6);
        }

        .metric-icon.warn {
            color: var(--warn);
            background: linear-gradient(135deg, var(--warn-soft), #fffaf0);
        }

        .metric-icon.danger {
            color: var(--danger);
            background: linear-gradient(135deg, var(--danger-soft), #fff8f7);
        }

        .metric-value {
            font-size: 31px;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.05;
        }

        .metric-subvalue {
            font-size: 14px;
            color: var(--muted);
            line-height: 1.5;
        }

        .metric-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            font-size: 12px;
        }

        .meta-chip {
            padding: 6px 10px;
            border-radius: 999px;
            background: white;
            border: 1px solid #e8eff8;
            color: #70839d;
        }

        .detail-grid {
            display: grid;
            grid-template-columns: 1.1fr 1fr;
            gap: 18px;
        }

        .subpanel {
            min-width: 0;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--panel-muted);
            padding: 18px;
        }

        .subpanel-header {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
            margin-bottom: 16px;
        }

        .subpanel-title {
            font-size: 16px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }

        .subpanel-copy {
            font-size: 13px;
            color: var(--muted);
            line-height: 1.5;
        }

        .subpanel-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }

        .primary-button {
            padding: 10px 16px;
            border: 1px solid #2371c4;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent), #30a2d1);
            color: white;
            font-weight: 700;
            cursor: pointer;
        }

        .helper-text {
            font-size: 12px;
            color: var(--muted);
        }

        .warning-list {
            display: grid;
            gap: 10px;
        }

        .warning-item {
            border: 1px solid #f1d39f;
            background: var(--warn-soft);
            color: #8f4d00;
            border-radius: 10px;
            padding: 12px 14px;
            font-size: 14px;
            line-height: 1.5;
        }

        .warning-item.empty {
            border-color: #d8efe0;
            background: #f3fbf5;
            color: #3f7d55;
        }

        .alerts-list {
            display: grid;
            gap: 10px;
        }

        .alert-item {
            border: 1px solid #e7edf7;
            border-left: 4px solid var(--accent);
            border-radius: 10px;
            background: white;
            padding: 12px 14px;
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
            border-left-color: var(--lime);
        }

        .alert-item.notification_error {
            border-left-color: #8b6ed6;
        }

        .alert-title {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .alert-meta {
            font-size: 12px;
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

        @media (max-width: 1180px) {
            .summary-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .detail-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 900px) {
            .dashboard-shell {
                grid-template-columns: 1fr;
            }

            .sidebar {
                display: none;
            }

            .content {
                padding: 16px;
            }

            .page-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
        }

        @media (max-width: 640px) {
            .summary-grid {
                grid-template-columns: 1fr;
            }

            .utility-bar,
            .surface-header,
            .subpanel-header {
                flex-direction: column;
                align-items: flex-start;
            }

            .subpanel-actions {
                justify-content: flex-start;
            }
        }
    </style>
    """


def build_sidebar() -> str:
    return """
        <aside class="sidebar">
            <div class="brand">
                <div class="brand-mark">Ops</div>
            </div>
            <div class="sidebar-body">
                <input class="search-box" value="운영 메뉴 검색" readonly />

                <div class="nav-section">
                    <div class="nav-title">운영 개요</div>
                    <div class="nav-item active"><span>대시보드</span><span>•</span></div>
                    <div class="nav-item"><span>서비스 상태</span><span>›</span></div>
                    <div class="nav-item"><span>장애 이력</span><span>›</span></div>
                    <div class="nav-item"><span>알림 채널</span><span>›</span></div>
                </div>

                <div class="nav-section">
                    <div class="nav-title">모니터링 관리</div>
                    <div class="nav-item"><span>모니터링 루프</span><span>›</span></div>
                    <div class="nav-item"><span>임계치 설정</span><span>›</span></div>
                    <div class="nav-item"><span>런타임 설정</span><span>›</span></div>
                    <div class="nav-item"><span>로그 리포트</span><span>›</span></div>
                </div>

                <div class="nav-section">
                    <div class="nav-title">보호된 영역</div>
                    <div class="nav-item"><span>인증 상태</span><span>›</span></div>
                    <div class="nav-item"><span>호스트 정책</span><span>›</span></div>
                    <div class="nav-item"><span>문서 노출 제어</span><span>›</span></div>
                </div>
            </div>
        </aside>
    """


def build_utility_bar() -> str:
    return """
        <div class="utility-bar">
            <div class="utility-left">
                <div class="icon-button">☰</div>
                <div class="icon-button">⌂</div>
                <div class="utility-text">운영 콘솔</div>
            </div>
            <div class="utility-right">
                <div class="utility-text">보호된 모니터링 환경</div>
                <div class="avatar">OM</div>
            </div>
        </div>
    """


def build_page_header() -> str:
    return """
        <div class="page-header">
            <h1>대시보드</h1>
            <div class="page-subtitle">서비스 상태, 설정 경고, 최근 알림을 관리자 화면처럼 빠르게 훑을 수 있도록 구성한 운영 개요 페이지입니다.</div>
        </div>
    """


def build_summary_surface() -> str:
    return """
        <section class="surface">
            <div class="surface-header">
                <div>
                    <div class="surface-title">Today</div>
                    <div class="surface-heading">운영 요약</div>
                    <div class="surface-copy">핵심 상태와 자원 지표를 먼저 확인하고, 아래에서 경고와 최근 알림을 이어서 확인할 수 있습니다.</div>
                </div>
            </div>
            <div class="surface-body">
                <div class="summary-grid">
                    <div class="metric-card primary">
                        <div class="metric-top">
                            <div class="metric-label">API 상태</div>
                            <div class="metric-icon">A</div>
                        </div>
                        <div id="api-status" class="metric-value normal">확인 중...</div>
                        <div class="metric-subvalue">대시보드 기준으로 가장 먼저 보는 서비스 응답 상태</div>
                        <div class="metric-meta">
                            <div class="meta-chip">운영 진입점</div>
                        </div>
                    </div>

                    <div class="metric-card primary">
                        <div class="metric-top">
                            <div class="metric-label">데이터베이스 상태</div>
                            <div class="metric-icon lime">DB</div>
                        </div>
                        <div id="db-status" class="metric-value normal">확인 중...</div>
                        <div class="metric-subvalue">PostgreSQL 연결 상태와 장애 가능성 확인</div>
                        <div class="metric-meta">
                            <div class="meta-chip">핵심 의존성</div>
                        </div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-top">
                            <div class="metric-label">메모리 사용량</div>
                            <div class="metric-icon">M</div>
                        </div>
                        <div id="memory-status" class="metric-value normal">확인 중...</div>
                        <div id="memory-desc" class="metric-subvalue">-</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-top">
                            <div class="metric-label">디스크 사용량</div>
                            <div class="metric-icon">D</div>
                        </div>
                        <div id="disk-status" class="metric-value normal">확인 중...</div>
                        <div id="disk-desc" class="metric-subvalue">-</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-top">
                            <div class="metric-label">모니터링 상태</div>
                            <div class="metric-icon lime">⟳</div>
                        </div>
                        <div id="monitoring-status" class="metric-value normal">확인 중...</div>
                        <div id="monitoring-desc" class="metric-subvalue">-</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-top">
                            <div class="metric-label">디스코드 알림</div>
                            <div class="metric-icon">N</div>
                        </div>
                        <div id="discord-status" class="metric-value normal">확인 중...</div>
                        <div id="discord-desc" class="metric-subvalue">웹훅 설정 상태</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-top">
                            <div class="metric-label">알림 기준</div>
                            <div class="metric-icon warn">!</div>
                        </div>
                        <div id="threshold-summary" class="metric-value warning">-</div>
                        <div id="threshold-desc" class="metric-subvalue">자원 경고를 발생시키는 기준값</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-top">
                            <div class="metric-label">설정 상태</div>
                            <div class="metric-icon danger">C</div>
                        </div>
                        <div id="config-status" class="metric-value warning">확인 중...</div>
                        <div id="config-desc" class="metric-subvalue">환경 검증과 기능 설정 상태</div>
                    </div>
                </div>
            </div>
        </section>
    """


def build_detail_surface() -> str:
    return """
        <section class="surface">
            <div class="surface-header">
                <div>
                    <div class="surface-title">Details</div>
                    <div class="surface-heading">운영 세부 현황</div>
                    <div class="surface-copy">설정 경고와 최근 알림을 분리해서, 점검할 것과 이미 발생한 일을 서로 다른 시선으로 보도록 구성했습니다.</div>
                </div>
            </div>
            <div class="surface-body">
                <div class="detail-grid">
                    <div class="subpanel">
                        <div class="subpanel-header">
                            <div>
                                <div class="subpanel-title">설정 경고</div>
                                <div class="subpanel-copy">런타임 설정 검증 메시지</div>
                            </div>
                        </div>
                        <div id="warning-list" class="warning-list">
                            <div class="warning-item empty">설정 경고가 없습니다.</div>
                        </div>
                    </div>

                    <div class="subpanel">
                        <div class="subpanel-header">
                            <div>
                                <div class="subpanel-title">최근 알림</div>
                                <div class="subpanel-copy">최신 장애, 복구, 자원 임계치 이벤트</div>
                            </div>
                            <div class="subpanel-actions">
                                <button class="primary-button" onclick="loadDashboard()">로그 갱신</button>
                                <div id="refresh-hint" class="helper-text">자동 갱신: 모니터링 상태를 기다리는 중...</div>
                            </div>
                        </div>
                        <div id="alert-list" class="alerts-list">
                            <div class="alert-item">
                                <div class="alert-title">알림을 불러오는 중입니다.</div>
                                <div class="alert-meta">데이터를 확인한 뒤 최신 이력이 여기에 표시됩니다.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    """


def build_dashboard_script() -> str:
    return """
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
            element.className = "metric-value " + tone;
        }

        function getUsageTone(percent, threshold) {
            return percent >= threshold ? "warning" : "connected";
        }

        function renderWarnings(warnings) {
            const warningList = document.getElementById("warning-list");
            warningList.innerHTML = "";

            if (!warnings || warnings.length === 0) {
                const emptyState = document.createElement("div");
                emptyState.className = "warning-item empty";
                emptyState.textContent = "설정 경고가 없습니다.";
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
                emptyState.className = "alert-item";
                emptyState.innerHTML =
                    '<div class="alert-title">최근 알림이 없습니다.</div>' +
                    '<div class="alert-meta">현재 기록된 장애, 복구, 임계치 이벤트가 없습니다.</div>';
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
                    "유형: " + alert.type +
                    " | 대상: " + alert.target +
                    " | 상태: " + alert.status +
                    " | 시각: " + alert.timestamp;

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
                summaryStatus.textContent = "데이터베이스 확인 필요";
                summaryStatus.className = "summary-status danger";
                summaryCopy.textContent = "API는 응답하지만 데이터베이스가 연결되어 있지 않습니다. 아래 알림 이력으로 새 장애인지, 지속 중인 장애인지 확인해 주세요.";
                return;
            }

            if (warningCount > 0) {
                summaryStatus.textContent = "런타임 설정 점검 필요";
                summaryStatus.className = "summary-status warning";
                summaryCopy.textContent = "핵심 서비스는 응답하지만 일부 런타임 설정이 잘못되어 안전한 기본값으로 대체되었습니다. 경고를 확인한 뒤 임계치나 갱신 주기를 신뢰하는 편이 좋습니다.";
                return;
            }

            summaryStatus.textContent = "운영 신호 양호";
            summaryStatus.className = "summary-status";
            summaryCopy.textContent = "API, 데이터베이스, 모니터링 메타데이터가 정상적으로 맞물려 있습니다. 임계치, 인증 정보, 백그라운드 점검 설정에도 검증 경고가 없습니다.";
        }

        function scheduleAutoRefresh(intervalSeconds) {
            if (dashboardState.refreshTimer) {
                window.clearTimeout(dashboardState.refreshTimer);
            }

            const safeIntervalSeconds = Math.max(intervalSeconds || 30, 15);
            document.getElementById("refresh-hint").textContent =
                "자동 갱신: " + safeIntervalSeconds + "초마다";

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
                memoryStatus.className = "metric-value " + getUsageTone(system.memory.percent, thresholds.memory_percent);
                memoryDesc.textContent =
                    system.memory.used_gb + "GB / " + system.memory.total_gb +
                    "GB 사용 중 (임계치 " + thresholds.memory_percent + "%)";

                diskStatus.textContent = system.disk.percent + "%";
                diskStatus.className = "metric-value " + getUsageTone(system.disk.percent, thresholds.disk_percent);
                diskDesc.textContent =
                    system.disk.used_gb + "GB / " + system.disk.total_gb +
                    "GB 사용 중 (임계치 " + thresholds.disk_percent + "%)";

                setStatusValue(
                    monitoringStatus,
                    monitoring.enabled ? "실행 중" : "중지됨",
                    monitoring.enabled ? "connected" : "disconnected"
                );
                monitoringDesc.textContent =
                    "주기 " + monitoring.interval_seconds +
                    "초" + (monitoring.api_docs_enabled ? " | 문서 활성화" : " | 문서 비활성화");

                setStatusValue(
                    discordStatus,
                    monitoring.discord_webhook_configured ? "활성화" : "비활성화",
                    monitoring.discord_webhook_configured ? "connected" : "warning"
                );
                discordDesc.textContent =
                    monitoring.monitor_auth_configured
                        ? "웹훅과 모니터링 인증 정보가 각각 설정되어 있습니다."
                        : "웹훅은 없어도 되지만 보호된 API에는 인증 정보가 필요합니다.";

                thresholdSummary.textContent =
                    "메모리 " + thresholds.memory_percent + "% / 디스크 " + thresholds.disk_percent + "%";
                thresholdSummary.className = "metric-value warning";
                thresholdDesc.textContent = "메모리나 디스크 사용량이 이 기준 이상이면 경고 이벤트를 기록합니다.";

                setStatusValue(
                    configStatus,
                    warningCount === 0 ? "정상" : "점검 필요",
                    warningCount === 0 ? "connected" : "warning"
                );
                configDesc.textContent =
                    "인증 " + (monitoring.monitor_auth_configured ? "설정됨" : "누락") +
                    " | 검증 경고 " + warningCount + "건";

                renderSummary(health, monitoring);
                renderWarnings(monitoring.config_warnings);
                renderAlerts(alerts);
                scheduleAutoRefresh(monitoring.interval_seconds);

            } catch (error) {
                setStatusValue(apiStatus, "오류", "disconnected");
                setStatusValue(dbStatus, "알 수 없음", "disconnected");
                setStatusValue(memoryStatus, "알 수 없음", "disconnected");
                setStatusValue(diskStatus, "알 수 없음", "disconnected");
                setStatusValue(monitoringStatus, "알 수 없음", "disconnected");
                setStatusValue(discordStatus, "알 수 없음", "disconnected");
                setStatusValue(thresholdSummary, "-", "disconnected");
                setStatusValue(configStatus, "알 수 없음", "disconnected");
                monitorLastCheck.textContent = "-";
                checkedTime.textContent = "-";
                configWarningCount.textContent = "-";
                document.getElementById("summary-status").textContent = "대시보드 요청 실패";
                document.getElementById("summary-status").className = "summary-status danger";
                document.getElementById("summary-copy").textContent = "보호된 엔드포인트 중 하나 이상을 불러오지 못했습니다. API 인증 정보와 백엔드 상태를 확인한 뒤 다시 갱신해 주세요.";
                document.getElementById("refresh-hint").textContent = "자동 갱신: 30초마다";

                renderWarnings(["대시보드 갱신에 실패했습니다. 인증 정보와 백엔드 연결 상태를 확인해 주세요."]);
                renderAlerts([]);
                scheduleAutoRefresh(30);
            }
        }

        loadDashboard();
    </script>
    """


@lru_cache(maxsize=1)
def get_dashboard_html() -> str:
    return (
        "<!DOCTYPE html>"
        '<html lang="ko">'
        "<head>"
        '<meta charset="UTF-8" />'
        "<title>Ops Monitor 대시보드</title>"
        f"{build_dashboard_styles()}"
        "</head>"
        "<body>"
        '<div class="dashboard-shell">'
        f"{build_sidebar()}"
        '<main class="main">'
        f"{build_utility_bar()}"
        '<div class="content">'
        f"{build_page_header()}"
        f"{build_summary_surface()}"
        f"{build_detail_surface()}"
        "</div>"
        "</main>"
        "</div>"
        f"{build_dashboard_script()}"
        "</body>"
        "</html>"
    )
