def build_dashboard_styles() -> str:
    return """
    <style>
        :root {
            color-scheme: light;
            --bg: #eef3f9;
            --panel: #ffffff;
            --panel-soft: #f7fafc;
            --panel-strong: #f3f8ff;
            --sidebar: #f8fbff;
            --line: #d8e1ec;
            --line-strong: #c6d3e2;
            --text: #1d2a3a;
            --muted: #61748b;
            --accent: #0f5fa8;
            --accent-soft: #e8f3ff;
            --ok: #2c8b57;
            --ok-soft: #edf8f1;
            --warn: #be7a19;
            --warn-soft: #fff7e8;
            --danger: #c95344;
            --danger-soft: #fff2ef;
            --shadow: 0 24px 60px rgba(30, 52, 80, 0.08);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: "Segoe UI", "Noto Sans KR", sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at top right, rgba(15, 95, 168, 0.08), transparent 28%),
                linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
            word-break: keep-all;
            overflow-wrap: anywhere;
        }

        button,
        input {
            font: inherit;
        }

        .site-shell {
            display: grid;
            grid-template-columns: 268px minmax(0, 1fr);
            min-height: 100vh;
        }

        .site-shell.sidebar-collapsed {
            grid-template-columns: 92px minmax(0, 1fr);
        }

        .sidebar {
            display: flex;
            flex-direction: column;
            background: var(--sidebar);
            border-right: 1px solid var(--line);
            min-width: 0;
        }

        .brand {
            padding: 22px;
            background: linear-gradient(135deg, #0d4d89, #1782bc);
            color: white;
        }

        .brand-label {
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            opacity: 0.82;
        }

        .brand-title {
            margin-top: 10px;
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -0.04em;
        }

        .brand-copy {
            margin-top: 8px;
            font-size: 13px;
            line-height: 1.6;
            opacity: 0.88;
        }

        .sidebar-body {
            padding: 16px 14px 24px;
            overflow: auto;
        }

        .search-box {
            width: 100%;
            padding: 11px 12px;
            border: 1px solid var(--line);
            border-radius: 10px;
            background: white;
            color: var(--muted);
        }

        .nav-group {
            margin-top: 18px;
        }

        .nav-title {
            padding: 12px 8px 10px;
            color: #7b8da2;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .nav-item {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-top: 4px;
            padding: 11px 10px;
            border: 0;
            border-radius: 12px;
            background: transparent;
            color: var(--text);
            font-size: 14px;
            text-align: left;
            cursor: pointer;
        }

        .nav-item.active {
            background: linear-gradient(90deg, var(--accent-soft), rgba(255, 255, 255, 0.94));
            color: var(--accent);
            font-weight: 700;
        }

        .nav-item.is-hidden,
        .nav-group.is-hidden {
            display: none;
        }

        .nav-badge {
            min-width: 28px;
            padding: 0 8px;
            height: 24px;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #eaf0f7;
            color: #6c8097;
            font-size: 11px;
            font-weight: 800;
        }

        .nav-item.active .nav-badge {
            background: var(--accent);
            color: white;
        }

        .sidebar-footer {
            margin-top: 20px;
            padding: 14px 12px;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: white;
        }

        .sidebar-footer-title {
            margin-bottom: 10px;
            color: #70849a;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .sidebar-footer-row {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            color: var(--muted);
            font-size: 13px;
        }

        .site-shell.sidebar-collapsed .brand-copy,
        .site-shell.sidebar-collapsed .nav-title,
        .site-shell.sidebar-collapsed .search-box,
        .site-shell.sidebar-collapsed .sidebar-footer-title,
        .site-shell.sidebar-collapsed .sidebar-footer-row span,
        .site-shell.sidebar-collapsed .sidebar-footer-row strong,
        .site-shell.sidebar-collapsed .nav-item > span:first-child {
            display: none;
        }

        .site-shell.sidebar-collapsed .brand {
            padding: 22px 14px;
            text-align: center;
        }

        .site-shell.sidebar-collapsed .brand-title {
            font-size: 24px;
        }

        .site-shell.sidebar-collapsed .nav-item {
            justify-content: center;
            padding: 11px 0;
        }

        .main {
            min-width: 0;
        }

        .topbar {
            height: 64px;
            padding: 0 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            border-bottom: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(12px);
        }

        .topbar-left,
        .topbar-right {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .icon-button {
            width: 38px;
            height: 38px;
            border: 1px solid var(--line);
            border-radius: 10px;
            background: white;
            color: var(--accent);
            cursor: pointer;
        }

        .topbar-copy {
            color: var(--muted);
            font-size: 13px;
        }

        .avatar {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0f5fa8, #46a7d7);
            color: white;
            font-size: 12px;
            font-weight: 800;
        }

        .content {
            padding: 22px;
        }

        .page-header {
            display: grid;
            grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
            gap: 16px;
            margin-bottom: 18px;
        }

        .hero-panel,
        .quick-panel,
        .surface {
            border: 1px solid var(--line);
            border-radius: 18px;
            background: var(--panel);
            box-shadow: var(--shadow);
        }

        .hero-panel {
            padding: 22px;
            background:
                linear-gradient(135deg, rgba(15, 95, 168, 0.05), rgba(255, 255, 255, 0.95)),
                white;
        }

        .hero-kicker,
        .panel-kicker,
        .surface-title {
            color: #73879d;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .hero-headline {
            margin-top: 10px;
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.18;
        }

        .hero-summary {
            margin-top: 10px;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.7;
        }

        .hero-meta {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin-top: 18px;
        }

        .hero-meta-card {
            padding: 14px;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.86);
        }

        .hero-meta-label {
            color: var(--muted);
            font-size: 12px;
            margin-bottom: 8px;
        }

        .hero-meta-value {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .quick-panel {
            padding: 18px;
            display: grid;
            gap: 14px;
            background: linear-gradient(180deg, #fcfdff, #f6faff);
        }

        .panel-heading {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .panel-copy {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .quick-actions {
            display: grid;
            gap: 10px;
        }

        .action-button,
        .confirm-button {
            padding: 10px 14px;
            border: 1px solid var(--line-strong);
            border-radius: 12px;
            background: white;
            color: var(--text);
            cursor: pointer;
        }

        .action-button.primary,
        .confirm-button.primary {
            border-color: #0f5fa8;
            background: linear-gradient(135deg, #0f5fa8, #2a8cc6);
            color: white;
        }

        .quick-hint,
        .action-feedback {
            color: var(--muted);
            font-size: 12px;
            line-height: 1.6;
        }

        .section-stack {
            display: grid;
            gap: 18px;
        }

        .surface {
            overflow: hidden;
        }

        .surface-header {
            padding: 18px 20px;
            border-bottom: 1px solid #ebf0f5;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
        }

        .surface-heading {
            margin-top: 6px;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .surface-copy {
            margin-top: 8px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .surface-tools {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            justify-content: flex-end;
        }

        .tool-chip {
            padding: 8px 12px;
            border-radius: 999px;
            border: 1px solid var(--line);
            background: var(--panel-soft);
            color: #6b7f95;
            font-size: 12px;
            font-weight: 700;
        }

        .surface-body {
            padding: 18px;
        }

        .report-center-grid {
            display: grid;
            grid-template-columns: minmax(320px, 0.9fr) minmax(0, 1.1fr);
            gap: 18px;
        }

        .report-queue {
            display: grid;
            gap: 10px;
        }

        .report-list-item {
            padding: 16px;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--panel-soft);
            cursor: pointer;
            transition: border-color 150ms ease, transform 150ms ease, box-shadow 150ms ease;
        }

        .report-list-item:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 28px rgba(16, 53, 87, 0.06);
        }

        .report-list-item.active {
            border-color: #8dbce0;
            background: var(--accent-soft);
        }

        .report-list-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
        }

        .report-title {
            font-size: 16px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .report-summary {
            margin-top: 8px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .report-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }

        .status-pill,
        .meta-pill {
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 800;
        }

        .status-pill {
            background: #ecf1f8;
            color: #687d94;
            text-transform: uppercase;
        }

        .status-pill.critical {
            background: var(--danger-soft);
            color: var(--danger);
        }

        .status-pill.high {
            background: #fff3e1;
            color: #b06e12;
        }

        .status-pill.medium {
            background: var(--warn-soft);
            color: var(--warn);
        }

        .status-pill.low {
            background: var(--ok-soft);
            color: var(--ok);
        }

        .status-pill.confirmed {
            background: var(--ok-soft);
            color: var(--ok);
        }

        .meta-pill {
            border: 1px solid var(--line);
            background: white;
            color: #678099;
        }

        .report-detail {
            display: grid;
            gap: 16px;
            padding: 18px;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: linear-gradient(180deg, #ffffff, #fbfdff);
            min-height: 100%;
        }

        .detail-head {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
        }

        .detail-title {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.3;
        }

        .detail-headline {
            margin-top: 8px;
            color: #365b7e;
            font-size: 15px;
            line-height: 1.6;
        }

        .detail-summary {
            color: var(--muted);
            font-size: 14px;
            line-height: 1.7;
        }

        .detail-section {
            display: grid;
            gap: 10px;
        }

        .detail-section-title {
            font-size: 13px;
            font-weight: 800;
            color: #6d8299;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .detail-list {
            margin: 0;
            padding-left: 18px;
            color: var(--text);
            font-size: 14px;
            line-height: 1.7;
        }

        .detail-actions {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 10px;
        }

        .detail-feedback {
            color: var(--muted);
            font-size: 12px;
            line-height: 1.5;
        }

        .board-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }

        .board-card {
            padding: 16px;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--panel-soft);
        }

        .board-card.wide {
            grid-column: span 2;
        }

        .board-card.full {
            grid-column: span 4;
        }

        .board-card-title {
            font-size: 13px;
            font-weight: 800;
            color: #64788f;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .board-list {
            display: grid;
            gap: 10px;
            margin-top: 14px;
        }

        .board-item {
            padding: 12px 14px;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: white;
        }

        .board-item-top {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
        }

        .board-item-label {
            font-size: 14px;
            font-weight: 700;
        }

        .board-item-value {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .board-item-detail {
            margin-top: 6px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .tone-ok {
            color: var(--ok);
        }

        .tone-warning {
            color: var(--warn);
        }

        .tone-critical {
            color: var(--danger);
        }

        .timeline-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            gap: 16px;
        }

        .timeline-list,
        .alert-list {
            display: grid;
            gap: 10px;
        }

        .timeline-item,
        .alert-item {
            padding: 14px 15px;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: white;
        }

        .timeline-item-top,
        .alert-item-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
        }

        .timeline-title,
        .alert-title {
            font-size: 15px;
            font-weight: 700;
            line-height: 1.5;
        }

        .timeline-summary,
        .alert-summary {
            margin-top: 8px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .timestamp {
            color: #7b90a7;
            font-size: 12px;
            white-space: nowrap;
        }

        .empty-state {
            padding: 18px;
            border: 1px dashed var(--line-strong);
            border-radius: 14px;
            background: #fcfdff;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.7;
        }

        .is-hidden-view {
            display: none;
        }

        @media (max-width: 1180px) {
            .page-header,
            .report-center-grid,
            .timeline-grid {
                grid-template-columns: 1fr;
            }

            .board-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .board-card.full,
            .board-card.wide {
                grid-column: span 2;
            }

            .hero-meta {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 860px) {
            .site-shell {
                grid-template-columns: 1fr;
            }

            .sidebar {
                display: none;
            }

            .board-grid {
                grid-template-columns: 1fr;
            }

            .board-card.full,
            .board-card.wide {
                grid-column: span 1;
            }

            .hero-meta {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """


def build_sidebar() -> str:
    return """
        <aside class="sidebar">
            <div class="brand">
                <div>
                    <div class="brand-label">Operations Workspace</div>
                    <div class="brand-title">Ops Monitor</div>
                    <div class="brand-copy">분석 보고서가 작성되고 확인되는 운영 사이트</div>
                </div>
            </div>
            <div class="sidebar-body">
                <input id="menu-search" class="search-box" type="search" placeholder="메뉴 검색" />

                <div class="nav-group">
                    <div class="nav-title">보고서</div>
                    <button class="nav-item active" type="button" data-nav-view="overview"><span>운영 개요</span><span class="nav-badge">기본</span></button>
                    <button class="nav-item" type="button" data-nav-view="reports"><span>분석 보고서</span><span id="nav-reports-badge" class="nav-badge">0</span></button>
                    <button class="nav-item" type="button" data-nav-view="approvals"><span>확인 대기</span><span id="nav-approvals-badge" class="nav-badge">0</span></button>
                </div>

                <div class="nav-group">
                    <div class="nav-title">운영 현황</div>
                    <button class="nav-item" type="button" data-nav-view="operations"><span>운영 보드</span><span id="nav-operations-badge" class="nav-badge">확인 중</span></button>
                    <button class="nav-item" type="button" data-nav-view="timeline"><span>타임라인</span><span id="nav-timeline-badge" class="nav-badge">0</span></button>
                    <button class="nav-item" type="button" data-nav-view="alerts"><span>이벤트 로그</span><span id="nav-alerts-badge" class="nav-badge">0</span></button>
                </div>

                <div class="nav-group">
                    <div class="nav-title">관리</div>
                    <button class="nav-item" type="button" data-nav-view="actions"><span>운영 액션</span><span id="nav-actions-badge" class="nav-badge">0</span></button>
                    <button class="nav-item" type="button" data-nav-view="config"><span>설정 경고</span><span id="nav-config-badge" class="nav-badge">0</span></button>
                </div>

                <div class="sidebar-footer">
                    <div class="sidebar-footer-title">Workspace</div>
                    <div class="sidebar-footer-row"><span>최근 갱신</span><strong id="sidebar-generated-at">-</strong></div>
                </div>
            </div>
        </aside>
    """


def build_topbar() -> str:
    return """
        <div class="topbar">
            <div class="topbar-left">
                <button id="sidebar-toggle" class="icon-button" type="button" aria-label="사이드바 토글">☰</button>
                <div class="topbar-copy">운영 보고서와 확인 이력을 다루는 사이트형 대시보드</div>
            </div>
            <div class="topbar-right">
                <div id="workspace-generated-at" class="topbar-copy">마지막 집계 -</div>
                <div class="avatar">OM</div>
            </div>
        </div>
    """


def build_header() -> str:
    return """
        <div class="page-header" data-views="overview reports approvals">
            <section class="hero-panel">
                <div class="hero-kicker">Daily Briefing</div>
                <div id="overview-headline" class="hero-headline">운영 워크스페이스를 불러오는 중입니다.</div>
                <div id="overview-summary" class="hero-summary">현재 운영 상태와 분석 보고서 큐를 집계하고 있습니다.</div>
                <div class="hero-meta">
                    <div class="hero-meta-card">
                        <div class="hero-meta-label">확인 대기 보고서</div>
                        <div id="overview-pending-count" class="hero-meta-value">-</div>
                    </div>
                    <div class="hero-meta-card">
                        <div class="hero-meta-label">확인 완료 보고서</div>
                        <div id="overview-confirmed-count" class="hero-meta-value">-</div>
                    </div>
                    <div class="hero-meta-card">
                        <div class="hero-meta-label">최근 이벤트</div>
                        <div id="overview-alert-count" class="hero-meta-value">-</div>
                    </div>
                    <div class="hero-meta-card">
                        <div class="hero-meta-label">점검 주기</div>
                        <div id="overview-interval" class="hero-meta-value">-</div>
                    </div>
                </div>
            </section>

            <aside class="quick-panel">
                <div>
                    <div class="panel-kicker">Quick Control</div>
                    <div class="panel-heading">운영 액션</div>
                    <div class="panel-copy">보고서 확인과 보호된 조치를 같은 사이트 안에서 이어서 처리할 수 있습니다.</div>
                </div>
                <div class="quick-actions">
                    <button id="confirm-report-button" class="confirm-button primary" type="button">선택 보고서 확인 완료</button>
                    <button id="db-restart-button" class="action-button" type="button">데이터베이스 재시작</button>
                    <button id="workspace-refresh-button" class="action-button" type="button">워크스페이스 새로고침</button>
                </div>
                <div id="workspace-action-feedback" class="action-feedback">운영 워크스페이스가 준비되면 보고서 확인과 조치를 진행할 수 있습니다.</div>
                <div id="workspace-refresh-hint" class="quick-hint">자동 갱신: 대기 중</div>
            </aside>
        </div>
    """


def build_report_center_surface() -> str:
    return """
        <section class="surface" data-views="overview reports approvals">
            <div class="surface-header">
                <div>
                    <div class="surface-title">Report Center</div>
                    <div class="surface-heading">운영 보고서 센터</div>
                    <div class="surface-copy">상태값을 나열하는 대신, 운영자가 확인해야 할 분석 보고서를 큐와 상세 검토 화면으로 분리했습니다.</div>
                </div>
                <div class="surface-tools">
                    <div class="tool-chip">분석 보고서</div>
                    <div class="tool-chip">확인 처리</div>
                    <div class="tool-chip">운영 복기</div>
                </div>
            </div>
            <div class="surface-body">
                <div class="report-center-grid">
                    <div id="report-list" class="report-queue">
                        <div class="empty-state">보고서 큐를 준비하는 중입니다.</div>
                    </div>
                    <div id="report-detail" class="report-detail">
                        <div class="empty-state">왼쪽 보고서를 선택하면 상세 분석과 권장 조치를 확인할 수 있습니다.</div>
                    </div>
                </div>
            </div>
        </section>
    """


def build_operations_surface() -> str:
    return """
        <section class="surface" data-views="overview operations config actions">
            <div class="surface-header">
                <div>
                    <div class="surface-title">Operations Board</div>
                    <div class="surface-heading">운영 보드</div>
                    <div class="surface-copy">서비스 상태, 자원 사용량, 설정 경고, 최근 운영 액션을 각각 독립된 보드로 정리합니다.</div>
                </div>
            </div>
            <div class="surface-body">
                <div class="board-grid">
                    <div class="board-card wide">
                        <div class="board-card-title">서비스 상태</div>
                        <div id="service-board" class="board-list">
                            <div class="empty-state">서비스 보드를 준비하는 중입니다.</div>
                        </div>
                    </div>
                    <div class="board-card">
                        <div class="board-card-title">자원 사용량</div>
                        <div id="resource-board" class="board-list">
                            <div class="empty-state">자원 보드를 준비하는 중입니다.</div>
                        </div>
                    </div>
                    <div class="board-card">
                        <div class="board-card-title">설정 경고</div>
                        <div id="config-warning-list" class="board-list">
                            <div class="empty-state">설정 경고를 확인하는 중입니다.</div>
                        </div>
                    </div>
                    <div class="board-card full">
                        <div class="board-card-title">운영 액션 감사</div>
                        <div id="action-feed" class="board-list">
                            <div class="empty-state">최근 운영 액션 이력을 확인하는 중입니다.</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    """


def build_timeline_surface() -> str:
    return """
        <section class="surface" data-views="overview timeline alerts actions">
            <div class="surface-header">
                <div>
                    <div class="surface-title">Timeline</div>
                    <div class="surface-heading">운영 타임라인과 이벤트 로그</div>
                    <div class="surface-copy">보고서 작성 근거가 되는 운영 타임라인과 최근 이벤트를 함께 확인할 수 있습니다.</div>
                </div>
            </div>
            <div class="surface-body">
                <div class="timeline-grid">
                    <div>
                        <div class="board-card-title">운영 타임라인</div>
                        <div id="timeline-list" class="timeline-list">
                            <div class="empty-state">타임라인을 준비하는 중입니다.</div>
                        </div>
                    </div>
                    <div>
                        <div class="board-card-title">최근 이벤트</div>
                        <div id="alert-list" class="alert-list">
                            <div class="empty-state">이벤트 로그를 준비하는 중입니다.</div>
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
            workspace: null,
            activeView: "overview",
            selectedReportId: null,
            refreshTimer: null,
        };

        async function fetchJson(url, options) {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(url + " 요청 실패");
            }
            return await response.json();
        }

        function setText(id, text) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = text;
            }
        }

        function formatPriorityLabel(priority) {
            const labels = {
                critical: "Critical",
                high: "High",
                medium: "Medium",
                low: "Low",
            };
            return labels[priority] || priority;
        }

        function buildEmptyState(message) {
            const wrapper = document.createElement("div");
            wrapper.className = "empty-state";
            wrapper.textContent = message;
            return wrapper;
        }

        function captureScrollPosition() {
            return {
                x: window.scrollX,
                y: window.scrollY,
            };
        }

        function restoreScrollPosition(position) {
            if (!position) {
                return;
            }

            window.scrollTo({
                left: position.x,
                top: position.y,
                behavior: "auto",
            });
        }

        function renderOverview(overview, generatedAt) {
            setText("overview-headline", overview.headline);
            setText("overview-summary", overview.summary);
            setText("overview-pending-count", String(overview.pending_reports));
            setText("overview-confirmed-count", String(overview.confirmed_reports));
            setText("overview-alert-count", String(overview.recent_alerts));
            setText("overview-interval", String(overview.monitor_interval_seconds) + "초");
            setText("workspace-generated-at", "마지막 집계 " + generatedAt);
            setText("sidebar-generated-at", generatedAt);
        }

        function renderReportQueue(reports) {
            const reportList = document.getElementById("report-list");
            reportList.innerHTML = "";

            if (!Array.isArray(reports) || reports.length === 0) {
                reportList.appendChild(buildEmptyState("현재 생성된 분석 보고서가 없습니다."));
                return;
            }

            reports.forEach(report => {
                const item = document.createElement("button");
                const top = document.createElement("div");
                const titleWrap = document.createElement("div");
                const title = document.createElement("div");
                const summary = document.createElement("div");
                const priority = document.createElement("div");
                const meta = document.createElement("div");
                const categoryChip = document.createElement("div");
                const confirmationChip = document.createElement("div");

                item.type = "button";
                item.className = "report-list-item";
                if (report.report_id === dashboardState.selectedReportId) {
                    item.classList.add("active");
                }
                item.dataset.reportId = report.report_id;

                top.className = "report-list-top";
                title.className = "report-title";
                summary.className = "report-summary";
                priority.className = "status-pill " + report.priority;
                meta.className = "report-meta";
                categoryChip.className = "meta-pill";
                confirmationChip.className = "status-pill " + (report.confirmed ? "confirmed" : report.priority);

                title.textContent = report.title;
                summary.textContent = report.headline;
                priority.textContent = formatPriorityLabel(report.priority);
                categoryChip.textContent = report.category;
                confirmationChip.textContent = report.confirmed ? "확인 완료" : "확인 대기";

                titleWrap.appendChild(title);
                titleWrap.appendChild(summary);
                top.appendChild(titleWrap);
                top.appendChild(priority);
                meta.appendChild(categoryChip);
                meta.appendChild(confirmationChip);
                item.appendChild(top);
                item.appendChild(meta);
                reportList.appendChild(item);
            });
        }

        function renderReportDetail(report) {
            const detail = document.getElementById("report-detail");
            const confirmButton = document.getElementById("confirm-report-button");
            detail.innerHTML = "";

            if (!report) {
                detail.appendChild(buildEmptyState("선택 가능한 보고서가 없습니다."));
                if (confirmButton) {
                    confirmButton.disabled = true;
                }
                return;
            }

            if (confirmButton) {
                confirmButton.disabled = Boolean(report.confirmed);
            }

            const head = document.createElement("div");
            const titleWrap = document.createElement("div");
            const title = document.createElement("div");
            const headline = document.createElement("div");
            const confirmation = document.createElement("div");
            const summary = document.createElement("div");
            const factSection = document.createElement("div");
            const actionSection = document.createElement("div");
            const ownerSection = document.createElement("div");

            head.className = "detail-head";
            title.className = "detail-title";
            headline.className = "detail-headline";
            confirmation.className = "status-pill " + (report.confirmed ? "confirmed" : report.priority);
            summary.className = "detail-summary";

            title.textContent = report.title;
            headline.textContent = report.headline;
            confirmation.textContent = report.confirmed
                ? "확인 완료 · " + (report.confirmed_by || "-")
                : "확인 대기";
            summary.textContent = report.summary;

            titleWrap.appendChild(title);
            titleWrap.appendChild(headline);
            head.appendChild(titleWrap);
            head.appendChild(confirmation);

            factSection.className = "detail-section";
            factSection.innerHTML = '<div class="detail-section-title">주요 근거</div>';
            const factList = document.createElement("ul");
            factList.className = "detail-list";
            report.facts.forEach(fact => {
                const item = document.createElement("li");
                item.textContent = fact;
                factList.appendChild(item);
            });
            factSection.appendChild(factList);

            actionSection.className = "detail-section";
            actionSection.innerHTML = '<div class="detail-section-title">권장 조치</div>';
            const actionList = document.createElement("ul");
            actionList.className = "detail-list";
            report.recommended_actions.forEach(actionText => {
                const item = document.createElement("li");
                item.textContent = actionText;
                actionList.appendChild(item);
            });
            actionSection.appendChild(actionList);

            ownerSection.className = "detail-section";
            ownerSection.innerHTML =
                '<div class="detail-section-title">담당 영역</div>' +
                '<div class="detail-summary">' + (report.owner || "-") + '</div>';

            detail.appendChild(head);
            detail.appendChild(summary);
            detail.appendChild(factSection);
            detail.appendChild(actionSection);
            detail.appendChild(ownerSection);
        }

        function renderServiceBoard(items) {
            const container = document.getElementById("service-board");
            container.innerHTML = "";

            if (!Array.isArray(items) || items.length === 0) {
                container.appendChild(buildEmptyState("서비스 상태 데이터가 없습니다."));
                return;
            }

            items.forEach(item => {
                const wrapper = document.createElement("div");
                wrapper.className = "board-item";
                wrapper.innerHTML =
                    '<div class="board-item-top">' +
                        '<div class="board-item-label">' + item.label + '</div>' +
                        '<div class="board-item-value tone-' + item.tone + '">' + item.status + '</div>' +
                    '</div>' +
                    '<div class="board-item-detail">' + item.detail + '</div>';
                container.appendChild(wrapper);
            });
        }

        function renderResourceBoard(items) {
            const container = document.getElementById("resource-board");
            container.innerHTML = "";

            if (!Array.isArray(items) || items.length === 0) {
                container.appendChild(buildEmptyState("자원 상태 데이터가 없습니다."));
                return;
            }

            items.forEach(item => {
                const wrapper = document.createElement("div");
                wrapper.className = "board-item";
                wrapper.innerHTML =
                    '<div class="board-item-top">' +
                        '<div class="board-item-label">' + item.label + '</div>' +
                        '<div class="board-item-value tone-' + item.tone + '">' + item.value + '</div>' +
                    '</div>' +
                    '<div class="board-item-detail">' + item.detail + '</div>';
                container.appendChild(wrapper);
            });
        }

        function renderConfigWarnings(warnings) {
            const container = document.getElementById("config-warning-list");
            container.innerHTML = "";

            if (!Array.isArray(warnings) || warnings.length === 0) {
                container.appendChild(buildEmptyState("설정 경고가 없습니다."));
                return;
            }

            warnings.forEach(message => {
                const wrapper = document.createElement("div");
                wrapper.className = "board-item";
                wrapper.innerHTML =
                    '<div class="board-item-label tone-warning">보완 필요</div>' +
                    '<div class="board-item-detail">' + message + '</div>';
                container.appendChild(wrapper);
            });
        }

        function renderActionFeed(actionFeed) {
            const container = document.getElementById("action-feed");
            container.innerHTML = "";

            if (!Array.isArray(actionFeed) || actionFeed.length === 0) {
                container.appendChild(buildEmptyState("최근 기록된 운영 액션이 없습니다."));
                return;
            }

            actionFeed.forEach(action => {
                const tone = action.type === "admin_action_error" ? "critical" : "warning";
                const wrapper = document.createElement("div");
                wrapper.className = "board-item";
                wrapper.innerHTML =
                    '<div class="board-item-top">' +
                        '<div class="board-item-label">' + (action.message || "운영 액션") + '</div>' +
                        '<div class="meta-pill tone-' + tone + '">' + (action.status || "-") + '</div>' +
                    '</div>' +
                    '<div class="board-item-detail">' +
                        (action.timestamp || "-") +
                    '</div>';
                container.appendChild(wrapper);
            });
        }

        function renderTimeline(items) {
            const container = document.getElementById("timeline-list");
            container.innerHTML = "";

            if (!Array.isArray(items) || items.length === 0) {
                container.appendChild(buildEmptyState("운영 타임라인 항목이 없습니다."));
                return;
            }

            items.forEach(item => {
                const wrapper = document.createElement("div");
                wrapper.className = "timeline-item";
                wrapper.innerHTML =
                    '<div class="timeline-item-top">' +
                        '<div class="timeline-title">' + item.title + '</div>' +
                        '<div class="timestamp">' + (item.timestamp || "-") + '</div>' +
                    '</div>' +
                    '<div class="timeline-summary">' + item.summary + '</div>';
                container.appendChild(wrapper);
            });
        }

        function renderAlerts(alerts) {
            const container = document.getElementById("alert-list");
            container.innerHTML = "";

            if (!Array.isArray(alerts) || alerts.length === 0) {
                container.appendChild(buildEmptyState("최근 이벤트가 없습니다."));
                return;
            }

            alerts.forEach(alert => {
                const wrapper = document.createElement("div");
                wrapper.className = "alert-item";
                wrapper.innerHTML =
                    '<div class="alert-item-top">' +
                        '<div class="alert-title">' + (alert.message || "이벤트 메시지 없음") + '</div>' +
                        '<div class="timestamp">' + (alert.timestamp || "-") + '</div>' +
                    '</div>' +
                    '<div class="alert-summary">' +
                        (alert.type || "event") + ' · ' + (alert.target || "-") + ' · ' + (alert.status || "-") +
                    '</div>';
                container.appendChild(wrapper);
            });
        }

        function updateSidebarMeta(workspace) {
            const reports = workspace.reports || [];
            const pendingReports = reports.filter(report => !report.confirmed);
            const actionFeed = workspace.action_feed || [];

            setText("nav-reports-badge", String(reports.length));
            setText("nav-approvals-badge", String(pendingReports.length));
            setText("nav-operations-badge", workspace.overview.operational_state === "stable" ? "양호" : "점검");
            setText("nav-timeline-badge", String((workspace.timeline || []).length));
            setText("nav-alerts-badge", String((workspace.alerts || []).length));
            setText("nav-actions-badge", String(actionFeed.length));
            setText("nav-config-badge", String((workspace.config_warnings || []).length));
        }

        function renderWorkspace(workspace) {
            dashboardState.workspace = workspace;

            const reports = Array.isArray(workspace.reports) ? workspace.reports : [];
            const reportExists = reports.some(report => report.report_id === dashboardState.selectedReportId);
            if (!reportExists) {
                dashboardState.selectedReportId = reports.length > 0 ? reports[0].report_id : null;
            }

            renderOverview(workspace.overview, workspace.generated_at || "-");
            renderReportQueue(reports);
            renderReportDetail(
                reports.find(report => report.report_id === dashboardState.selectedReportId) || null
            );
            renderServiceBoard(workspace.service_board || []);
            renderResourceBoard(workspace.resource_board || []);
            renderConfigWarnings(workspace.config_warnings || []);
            renderActionFeed(workspace.action_feed || []);
            renderTimeline(workspace.timeline || []);
            renderAlerts(workspace.alerts || []);
            updateSidebarMeta(workspace);
            scheduleAutoRefresh(workspace.monitoring ? workspace.monitoring.interval_seconds : 30);
        }

        function scheduleAutoRefresh(intervalSeconds) {
            if (dashboardState.refreshTimer) {
                window.clearTimeout(dashboardState.refreshTimer);
            }

            const safeIntervalSeconds = Math.max(Number(intervalSeconds) || 30, 15);
            setText("workspace-refresh-hint", "자동 갱신: " + safeIntervalSeconds + "초마다");
            dashboardState.refreshTimer = window.setTimeout(loadWorkspace, safeIntervalSeconds * 1000);
        }

        function filterSidebarMenu(query) {
            const normalizedQuery = String(query || "").trim().toLowerCase();

            document.querySelectorAll(".nav-group").forEach(group => {
                const items = Array.from(group.querySelectorAll(".nav-item"));
                let visibleCount = 0;

                items.forEach(item => {
                    const label = (item.querySelector("span")?.textContent || "").toLowerCase();
                    const matched = normalizedQuery === "" || label.includes(normalizedQuery);
                    item.classList.toggle("is-hidden", !matched);
                    if (matched) {
                        visibleCount += 1;
                    }
                });

                group.classList.toggle("is-hidden", visibleCount === 0);
            });
        }

        function applySidebarView(view) {
            dashboardState.activeView = view;

            document.querySelectorAll("[data-nav-view]").forEach(item => {
                item.classList.toggle("active", item.dataset.navView === view);
            });

            document.querySelectorAll("[data-views]").forEach(section => {
                const views = String(section.dataset.views || "").split(" ");
                const visible = view === "overview" || views.includes(view);
                section.classList.toggle("is-hidden-view", !visible);
            });
        }

        async function confirmSelectedReport() {
            const feedback = document.getElementById("workspace-action-feedback");
            const confirmButton = document.getElementById("confirm-report-button");
            const reportId = dashboardState.selectedReportId;

            if (!reportId || !confirmButton) {
                return;
            }

            confirmButton.disabled = true;
            if (feedback) {
                feedback.textContent = "보고서 확인 상태를 기록하는 중입니다.";
            }

            try {
                const result = await fetchJson("/dashboard/reports/" + encodeURIComponent(reportId) + "/confirm", {
                    method: "POST",
                });
                if (feedback) {
                    feedback.textContent = "보고서 확인 완료: " + (result.title || reportId);
                }
                await loadWorkspace();
            } catch (error) {
                if (feedback) {
                    feedback.textContent = "보고서 확인 처리에 실패했습니다.";
                }
            } finally {
                confirmButton.disabled = false;
            }
        }

        async function restartDatabase() {
            const feedback = document.getElementById("workspace-action-feedback");
            const restartButton = document.getElementById("db-restart-button");

            if (!restartButton) {
                return;
            }

            const confirmed = window.confirm("데이터베이스를 재시작할까요?");
            if (!confirmed) {
                return;
            }

            restartButton.disabled = true;
            if (feedback) {
                feedback.textContent = "데이터베이스 재시작 요청을 전송하는 중입니다.";
            }

            try {
                const result = await fetchJson("/admin/database/restart", {
                    method: "POST",
                });
                if (feedback) {
                    feedback.textContent = result.message || "DB 재시작 요청을 처리했습니다.";
                }
                window.setTimeout(loadWorkspace, 3000);
            } catch (error) {
                if (feedback) {
                    feedback.textContent = "DB 재시작 요청에 실패했습니다.";
                }
            } finally {
                restartButton.disabled = false;
            }
        }

        function bindDashboardInteractions() {
            const shell = document.querySelector(".site-shell");
            const sidebarToggle = document.getElementById("sidebar-toggle");
            const menuSearch = document.getElementById("menu-search");
            const refreshButton = document.getElementById("workspace-refresh-button");
            const confirmButton = document.getElementById("confirm-report-button");
            const restartButton = document.getElementById("db-restart-button");

            if (sidebarToggle && !sidebarToggle.dataset.bound) {
                sidebarToggle.dataset.bound = "true";
                sidebarToggle.addEventListener("click", () => {
                    shell.classList.toggle("sidebar-collapsed");
                });
            }

            if (menuSearch && !menuSearch.dataset.bound) {
                menuSearch.dataset.bound = "true";
                menuSearch.addEventListener("input", event => {
                    filterSidebarMenu(event.target.value);
                });
            }

            if (refreshButton && !refreshButton.dataset.bound) {
                refreshButton.dataset.bound = "true";
                refreshButton.addEventListener("click", loadWorkspace);
            }

            if (confirmButton && !confirmButton.dataset.bound) {
                confirmButton.dataset.bound = "true";
                confirmButton.addEventListener("click", confirmSelectedReport);
            }

            if (restartButton && !restartButton.dataset.bound) {
                restartButton.dataset.bound = "true";
                restartButton.addEventListener("click", restartDatabase);
            }

            document.querySelectorAll("[data-nav-view]").forEach(item => {
                if (item.dataset.bound) {
                    return;
                }

                item.dataset.bound = "true";
                item.addEventListener("click", () => {
                    applySidebarView(item.dataset.navView);
                });
            });

            document.addEventListener("click", event => {
                const reportItem = event.target.closest("[data-report-id]");
                if (!reportItem) {
                    return;
                }

                dashboardState.selectedReportId = reportItem.dataset.reportId;
                if (dashboardState.workspace) {
                    renderReportQueue(dashboardState.workspace.reports || []);
                    renderReportDetail(
                        (dashboardState.workspace.reports || []).find(
                            report => report.report_id === dashboardState.selectedReportId
                        ) || null
                    );
                }
            });

            applySidebarView(dashboardState.activeView);
            filterSidebarMenu(menuSearch ? menuSearch.value : "");
        }

        async function loadWorkspace() {
            bindDashboardInteractions();
            const scrollPosition = captureScrollPosition();

            try {
                const workspace = await fetchJson("/dashboard/workspace");
                renderWorkspace(workspace);
                restoreScrollPosition(scrollPosition);
            } catch (error) {
                const feedback = document.getElementById("workspace-action-feedback");
                setText("overview-headline", "운영 워크스페이스를 불러오지 못했습니다.");
                setText("overview-summary", "보호된 운영 API 응답과 인증 상태를 먼저 확인해 주세요.");
                setText("workspace-refresh-hint", "자동 갱신: 30초마다");
                if (feedback) {
                    feedback.textContent = "워크스페이스 집계 요청이 실패했습니다.";
                }
                scheduleAutoRefresh(30);
                restoreScrollPosition(scrollPosition);
            }
        }

        loadWorkspace();
    </script>
    """


def get_dashboard_html() -> str:
    return (
        "<!DOCTYPE html>"
        '<html lang="ko">'
        "<head>"
        '<meta charset="UTF-8" />'
        "<title>Ops Monitor 운영 워크스페이스</title>"
        f"{build_dashboard_styles()}"
        "</head>"
        "<body>"
        '<div class="site-shell">'
        f"{build_sidebar()}"
        '<main class="main">'
        f"{build_topbar()}"
        '<div class="content">'
        f"{build_header()}"
        '<div class="section-stack">'
        f"{build_report_center_surface()}"
        f"{build_operations_surface()}"
        f"{build_timeline_surface()}"
        "</div>"
        "</div>"
        "</main>"
        "</div>"
        f"{build_dashboard_script()}"
        "</body>"
        "</html>"
    )
