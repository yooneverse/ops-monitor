def build_dashboard_styles() -> str:
    return """
    <style>
        :root {
            color-scheme: light;
            --bg: #f4f9ff;
            --sidebar-bg: #ffffff;
            --content-bg: #f7fbff;
            --panel: #ffffff;
            --panel-muted: #fbfdff;
            --border: #d8e3f1;
            --border-strong: #c5d6ea;
            --text: #1d2a3b;
            --muted: #677991;
            --accent: #2c84d8;
            --accent-soft: #eaf5ff;
            --mint: #8ac756;
            --mint-soft: #f1f9e8;
            --ok: #2d9659;
            --warn: #d19324;
            --warn-soft: #fff7e7;
            --danger: #d95849;
            --danger-soft: #fff1ee;
            --shadow: 0 18px 42px rgba(44, 88, 142, 0.08);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            color: var(--text);
            background: linear-gradient(180deg, #fbfdff 0%, var(--bg) 100%);
            word-break: keep-all;
            overflow-wrap: anywhere;
        }

        button,
        input {
            font: inherit;
        }

        .dashboard-shell {
            display: grid;
            grid-template-columns: 252px minmax(0, 1fr);
            min-height: 100vh;
            transition: grid-template-columns 180ms ease;
        }

        .dashboard-shell.sidebar-collapsed {
            grid-template-columns: 92px minmax(0, 1fr);
        }

        .sidebar {
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            min-width: 0;
        }

        .brand {
            display: flex;
            align-items: center;
            height: 86px;
            padding: 0 22px;
            background: linear-gradient(135deg, #2bc0c8, #2c84d8);
            color: white;
        }

        .brand-mark {
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -0.04em;
        }

        .sidebar-body {
            padding: 16px 14px 22px;
            overflow: auto;
        }

        .search-box {
            width: 100%;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: #f8fbff;
            padding: 10px 12px;
            color: var(--muted);
            margin-bottom: 18px;
        }

        .nav-section {
            margin-bottom: 18px;
        }

        .nav-title {
            padding: 12px 8px 10px;
            border-top: 1px solid #edf2f8;
            font-size: 12px;
            font-weight: 800;
            color: #7a8ea7;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .nav-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 10px 8px;
            border-radius: 10px;
            border: 0;
            width: 100%;
            background: transparent;
            color: var(--text);
            font-size: 14px;
            text-align: left;
            cursor: pointer;
        }

        .nav-item.is-hidden,
        .nav-section.is-hidden {
            display: none;
        }

        .nav-item.active {
            background: linear-gradient(90deg, var(--accent-soft), #f8fcff);
            color: var(--accent);
            font-weight: 700;
        }

        .nav-item:focus-visible {
            outline: 2px solid rgba(44, 132, 216, 0.28);
            outline-offset: 2px;
        }

        .nav-badge {
            min-width: 24px;
            height: 24px;
            padding: 0 8px;
            border-radius: 999px;
            background: #edf4fb;
            color: #6b7f98;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 800;
        }

        .nav-item.active .nav-badge {
            background: var(--accent);
            color: white;
        }

        .sidebar-footer {
            margin-top: 18px;
            padding: 14px 12px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: linear-gradient(180deg, #f9fcff, #f3f9ff);
        }

        .sidebar-footer-title {
            margin-bottom: 10px;
            font-size: 12px;
            font-weight: 800;
            color: #70839d;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .sidebar-footer-row {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            font-size: 13px;
            color: var(--muted);
        }

        .dashboard-shell.sidebar-collapsed .brand {
            justify-content: center;
            padding: 0;
        }

        .dashboard-shell.sidebar-collapsed .brand-mark {
            font-size: 28px;
        }

        .dashboard-shell.sidebar-collapsed .search-box,
        .dashboard-shell.sidebar-collapsed .nav-title,
        .dashboard-shell.sidebar-collapsed .sidebar-footer-title,
        .dashboard-shell.sidebar-collapsed .sidebar-footer-row span,
        .dashboard-shell.sidebar-collapsed .sidebar-footer-row strong,
        .dashboard-shell.sidebar-collapsed .nav-item > span:first-child {
            display: none;
        }

        .dashboard-shell.sidebar-collapsed .nav-item {
            justify-content: center;
            padding: 10px 0;
        }

        .dashboard-shell.sidebar-collapsed .nav-badge {
            min-width: 30px;
            height: 30px;
            padding: 0;
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
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(10px);
        }

        .utility-left,
        .utility-right {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .icon-button {
            width: 36px;
            height: 36px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: white;
            color: var(--accent);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }

        .utility-text {
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
            background: linear-gradient(135deg, #2c84d8, #8ac756);
            color: white;
            font-size: 13px;
            font-weight: 800;
        }

        .content {
            padding: 22px;
        }

        .page-header {
            display: flex;
            flex-direction: column;
            align-items: stretch;
            gap: 14px;
            padding: 10px 4px 18px;
        }

        .page-header h1 {
            margin: 0;
            font-size: 34px;
            letter-spacing: -0.03em;
        }

        .header-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .header-kicker {
            color: #70839d;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .control-strip {
            display: grid;
            grid-template-columns: 1.35fr minmax(280px, 0.9fr);
            gap: 14px;
        }

        .control-panel {
            padding: 16px 18px;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: linear-gradient(135deg, #fafdff, #f3f8ff);
            box-shadow: var(--shadow);
        }

        .control-panel-title {
            font-size: 12px;
            font-weight: 800;
            color: #6e829c;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .control-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
        }

        .control-item {
            min-width: 0;
            padding: 12px 14px;
            border: 1px solid #dce8f8;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.9);
        }

        .control-label {
            color: #6a7f99;
            font-size: 12px;
            margin-bottom: 6px;
        }

        .control-value {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .launch-list {
            display: grid;
            gap: 10px;
        }

        .launch-link {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 14px;
            border: 1px solid #dce8f8;
            border-radius: 12px;
            background: white;
            color: var(--text);
            text-decoration: none;
        }

        .launch-link strong {
            font-size: 14px;
        }

        .launch-link span {
            color: var(--muted);
            font-size: 12px;
        }

        .page-subtitle {
            padding-bottom: 4px;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.5;
        }

        .surface {
            overflow: hidden;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: var(--panel);
            box-shadow: var(--shadow);
        }

        .surface + .surface {
            margin-top: 18px;
        }

        .surface-header {
            padding: 18px 22px;
            border-bottom: 1px solid #edf3f8;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }

        .surface-title {
            margin-bottom: 6px;
            font-size: 12px;
            font-weight: 800;
            color: #71839d;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .surface-heading {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .surface-copy {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .surface-tools,
        .subpanel-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            justify-content: flex-end;
        }

        .tool-chip,
        .filter-chip {
            padding: 8px 12px;
            border-radius: 999px;
            border: 1px solid #dce8f8;
            background: #f8fbff;
            color: #68809f;
            font-size: 12px;
            font-weight: 700;
        }

        .filter-chip {
            cursor: pointer;
        }

        .filter-chip.is-active {
            border-color: #2371c4;
            background: var(--accent-soft);
            color: var(--accent);
        }

        .primary-button {
            padding: 10px 16px;
            border: 1px solid #2371c4;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent), #31a0d4);
            color: white;
            font-weight: 700;
            cursor: pointer;
        }

        .helper-text {
            color: var(--muted);
            font-size: 12px;
        }

        .surface-body {
            padding: 18px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }

        .metric-card {
            min-width: 0;
            display: grid;
            gap: 12px;
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 14px;
            background: var(--panel-muted);
            cursor: pointer;
            transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 26px rgba(44, 132, 216, 0.08);
        }

        .metric-card.is-active {
            border-color: #69ace8;
            box-shadow: 0 0 0 2px rgba(44, 132, 216, 0.12);
        }

        .metric-card.is-hidden-view,
        .subpanel.is-hidden-view {
            display: none;
        }

        .metric-card.primary {
            background: linear-gradient(135deg, #f3f8ff, #fbfdff);
            border-color: var(--border-strong);
        }

        .metric-card.composite {
            grid-column: span 2;
            gap: 16px;
        }

        .metric-card.composite.wide {
            grid-column: span 4;
        }

        .metric-card.composite.status-group {
            grid-column: span 4;
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
            color: #60748f;
        }

        .metric-status-chip {
            display: inline-flex;
            align-items: center;
            padding: 5px 10px;
            border-radius: 999px;
            background: #eef4fb;
            color: #69809f;
            font-size: 11px;
            font-weight: 800;
        }

        .metric-icon {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--accent-soft), #f9fcff);
            color: var(--accent);
            font-size: 22px;
            font-weight: 800;
        }

        .metric-icon.lime {
            background: linear-gradient(135deg, var(--mint-soft), #fbfff6);
            color: #6aa62e;
        }

        .metric-icon.warn {
            background: linear-gradient(135deg, var(--warn-soft), #fffaf1);
            color: var(--warn);
        }

        .metric-icon.danger {
            background: linear-gradient(135deg, var(--danger-soft), #fff8f6);
            color: var(--danger);
        }

        .metric-value {
            font-size: 31px;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.05;
        }

        .metric-subvalue {
            color: var(--muted);
            font-size: 14px;
            line-height: 1.55;
        }

        .metric-visual {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .metric-visual-copy {
            min-width: 0;
            flex: 1;
        }

        .metric-donut {
            --percent: 0;
            --donut-color: var(--accent);
            width: 92px;
            height: 92px;
            border-radius: 50%;
            background:
                radial-gradient(closest-side, white 66%, transparent 67% 100%),
                conic-gradient(var(--donut-color) calc(var(--percent) * 1%), #e8eef8 0);
            display: grid;
            place-items: center;
            flex: 0 0 auto;
        }

        .metric-donut.connected {
            --donut-color: var(--ok);
        }

        .metric-donut.warning {
            --donut-color: var(--warn);
        }

        .metric-donut.disconnected {
            --donut-color: var(--danger);
        }

        .metric-donut-value {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: var(--text);
        }

        .composite-top {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            padding-bottom: 14px;
            border-bottom: 1px solid #e7eef8;
        }

        .composite-top.status-five {
            grid-template-columns: repeat(5, minmax(0, 1fr));
        }

        .composite-top.no-divider {
            padding-bottom: 0;
            border-bottom: 0;
        }

        .composite-bottom {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
        }

        .mini-metric {
            min-width: 0;
            padding: 14px;
            border: 1px solid #e4ecf8;
            border-radius: 12px;
            background: #ffffff;
            display: grid;
            gap: 12px;
        }

        .mini-metric-title {
            font-size: 13px;
            font-weight: 700;
            color: #60748f;
        }

        .status-tile {
            min-width: 0;
            padding: 14px;
            border: 1px solid #e4ecf8;
            border-radius: 12px;
            background: #ffffff;
            display: grid;
            gap: 10px;
        }

        .status-tile.primary {
            background: linear-gradient(135deg, #f3f8ff, #fbfdff);
        }

        .status-tile-head {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
        }

        .metric-bar {
            height: 8px;
            border-radius: 999px;
            background: #e8eef8;
            overflow: hidden;
        }

        .metric-bar > span {
            display: block;
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, var(--accent), #53b8d9);
        }

        .metric-bar.lime > span {
            background: linear-gradient(90deg, #4ca66b, #8ac756);
        }

        .metric-bar.warn > span {
            background: linear-gradient(90deg, #dda13a, #f1c56e);
        }

        .metric-meta,
        .alert-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .meta-chip,
        .alert-meta-chip {
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid #e7eef8;
            background: white;
            color: #6f839d;
            font-size: 12px;
        }

        .status-action-row {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
        }

        .secondary-button {
            padding: 8px 12px;
            border: 1px solid #d4e1f1;
            border-radius: 10px;
            background: white;
            color: #56708f;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
        }

        .action-feedback {
            font-size: 12px;
            color: var(--muted);
            line-height: 1.5;
        }

        .metrics-caption {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            color: var(--muted);
            font-size: 12px;
        }

        .summary-note {
            margin-top: 16px;
            padding: 14px 16px;
            border: 1px solid #dce8f8;
            border-radius: 14px;
            background: linear-gradient(135deg, #f8fbff, #fcfeff);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }

        .summary-note-label {
            margin-bottom: 6px;
            color: #70839d;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .summary-status {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .summary-copy {
            margin-top: 6px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .summary-note-meta {
            min-width: 220px;
            display: grid;
            gap: 8px;
        }

        .summary-note-row {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            color: var(--muted);
            font-size: 12px;
        }

        .summary-note-row.compact {
            align-items: flex-start;
        }

        .summary-note-row.compact strong {
            max-width: 150px;
            text-align: right;
            line-height: 1.5;
            font-size: 11px;
            color: #5f7490;
        }

        .detail-grid {
            display: grid;
            grid-template-columns: 1.08fr 1fr;
            gap: 18px;
        }

        .subpanel {
            min-width: 0;
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 14px;
            background: var(--panel-muted);
        }

        .subpanel-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 16px;
        }

        .subpanel-title {
            margin-bottom: 6px;
            font-size: 16px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .subpanel-copy {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .interaction-state {
            margin-top: 12px;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
        }

        .interaction-badge {
            padding: 7px 12px;
            border-radius: 999px;
            background: #eef5ff;
            color: var(--accent);
            font-size: 12px;
            font-weight: 700;
        }

        .interaction-reset {
            padding: 7px 12px;
            border: 1px solid #d8e4f5;
            border-radius: 999px;
            background: white;
            color: #65809f;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
        }

        .warning-list,
        .alerts-list {
            display: grid;
            gap: 10px;
        }

        .warning-item {
            padding: 12px 14px;
            border: 1px solid #f1d49e;
            border-radius: 10px;
            background: var(--warn-soft);
            color: #8d5105;
            font-size: 14px;
            line-height: 1.5;
        }

        .warning-item.empty {
            border-color: #d6eadb;
            background: #f3fbf5;
            color: #3f7d55;
        }

        .alert-item {
            position: relative;
            display: grid;
            grid-template-columns: 140px minmax(0, 1fr);
            gap: 14px;
            padding: 14px 16px;
            border: 1px solid #e7edf7;
            border-radius: 12px;
            background: white;
        }

        .alert-item::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            border-radius: 12px 0 0 12px;
            background: var(--accent);
        }

        .alert-item.incident {
            border-color: #f0d1cf;
            background: #fffaf9;
        }

        .alert-item.incident::before {
            background: var(--danger);
        }

        .alert-item.recovery {
            border-color: #d8ebdd;
            background: #fbfffc;
        }

        .alert-item.recovery::before {
            background: var(--ok);
        }

        .alert-item.resource_alert {
            border-color: #f0ddb7;
            background: #fffdf8;
        }

        .alert-item.resource_alert::before {
            background: var(--warn);
        }

        .alert-item.resource_recovery::before {
            background: var(--mint);
        }

        .alert-item.notification_error::before {
            background: #8c6ed6;
        }

        .alert-side {
            display: grid;
            gap: 8px;
        }

        .alert-kind {
            width: fit-content;
            min-width: 72px;
            padding: 6px 10px;
            border-radius: 999px;
            background: #eef4fb;
            color: #6980a0;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            text-align: center;
        }

        .alert-time,
        .alert-message {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.55;
        }

        .alert-title {
            margin-bottom: 6px;
            font-size: 14px;
            font-weight: 700;
        }

        .connected {
            color: var(--ok);
        }

        .disconnected,
        .danger {
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

            .control-strip,
            .control-grid {
                grid-template-columns: 1fr;
            }

            .page-header,
            .summary-note {
                flex-direction: column;
                align-items: flex-start;
            }
        }

        @media (max-width: 640px) {
            .summary-grid {
                grid-template-columns: 1fr;
            }

            .metric-card.composite,
            .metric-card.composite.wide,
            .metric-card.composite.status-group,
            .composite-top,
            .composite-bottom {
                grid-column: auto;
                grid-template-columns: 1fr;
            }

            .utility-bar,
            .surface-header,
            .subpanel-header,
            .header-top {
                flex-direction: column;
                align-items: flex-start;
            }

            .subpanel-actions {
                justify-content: flex-start;
            }

            .alert-item {
                grid-template-columns: 1fr;
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
                <input id="menu-search" class="search-box" type="search" placeholder="운영 메뉴 검색" aria-label="운영 메뉴 검색" />

                <div class="nav-section">
                    <div class="nav-title">운영 개요</div>
                    <button class="nav-item active" type="button" data-nav-view="overview"><span>대시보드</span><span class="nav-badge">전체</span></button>
                    <button class="nav-item" type="button" data-nav-view="services"><span>서비스 상태</span><span id="nav-services-badge" class="nav-badge">확인 중</span></button>
                    <button class="nav-item" type="button" data-nav-view="alerts"><span>장애 이력</span><span id="nav-alerts-badge" class="nav-badge">0</span></button>
                    <button class="nav-item" type="button" data-nav-view="notification"><span>알림 채널</span><span id="nav-notification-badge" class="nav-badge">확인 중</span></button>
                </div>

                <div class="nav-section">
                    <div class="nav-title">모니터링 관리</div>
                    <button class="nav-item" type="button" data-nav-view="monitoring"><span>모니터링 루프</span><span id="nav-monitoring-badge" class="nav-badge">확인 중</span></button>
                    <button class="nav-item" type="button" data-nav-view="thresholds"><span>임계치 설정</span><span id="nav-thresholds-badge" class="nav-badge">정책</span></button>
                    <button class="nav-item" type="button" data-nav-view="config"><span>환경 설정</span><span id="nav-config-badge" class="nav-badge">확인 중</span></button>
                    <button class="nav-item" type="button" data-nav-view="logs"><span>로그 리포트</span><span id="nav-logs-badge" class="nav-badge">최근</span></button>
                </div>

                <div class="nav-section">
                    <div class="nav-title">보호된 영역</div>
                    <button class="nav-item" type="button" data-nav-view="auth"><span>인증 상태</span><span id="nav-auth-badge" class="nav-badge">확인 중</span></button>
                    <button class="nav-item" type="button" data-nav-view="services"><span>인스턴스 점검</span><span id="nav-instance-badge" class="nav-badge">확인 중</span></button>
                    <button class="nav-item" type="button" data-nav-view="docs"><span>문서 노출 제어</span><span id="nav-docs-badge" class="nav-badge">확인 중</span></button>
                </div>

                <div class="sidebar-footer">
                    <div class="sidebar-footer-title">운영 환경</div>
                    <div class="sidebar-footer-row">
                        <span>대상</span>
                        <strong>Production</strong>
                    </div>
                    <div class="sidebar-footer-row">
                        <span>보호 상태</span>
                        <strong>Enabled</strong>
                    </div>
                </div>
            </div>
        </aside>
    """


def build_utility_bar() -> str:
    return """
        <div class="utility-bar">
            <div class="utility-left">
                <button id="sidebar-toggle" class="icon-button" type="button" aria-label="사이드바 토글">☰</button>
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
            <div class="header-top">
                <div>
                    <div class="header-kicker">Ops Monitor Console</div>
                    <h1>대시보드</h1>
                </div>
            </div>
            <div class="control-strip">
                <div class="control-panel">
                    <div class="control-panel-title">운영 개요</div>
                    <div class="control-grid">
                        <div class="control-item">
                            <div class="control-label">운영 환경</div>
                            <div class="control-value">Production</div>
                        </div>
                        <div class="control-item">
                            <div class="control-label">보호 상태</div>
                            <div class="control-value">Basic Auth</div>
                        </div>
                        <div class="control-item">
                            <div class="control-label">감시 대상</div>
                            <div id="tracked-targets" class="control-value">3 Services</div>
                        </div>
                    </div>
                </div>
                <div class="control-panel">
                    <div class="control-panel-title">빠른 실행</div>
                    <div class="launch-list">
                        <a class="launch-link" href="http://localhost:8010" target="_blank" rel="noreferrer">
                            <strong>Demo Notes 열기</strong>
                            <span>입력형 내부 서비스</span>
                        </a>
                        <a class="launch-link" href="http://localhost:8010/api/notes" target="_blank" rel="noreferrer">
                            <strong>메모 API 보기</strong>
                            <span>실제 감시 대상 API</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    """


def build_summary_surface() -> str:
    return """
        <section class="surface">
            <div class="surface-header">
                <div>
                    <div class="surface-title">실시간 상태</div>
                    <div class="surface-heading">운영 요약</div>
                </div>
                <div class="surface-tools">
                    <div class="tool-chip">운영 개요</div>
                    <div class="tool-chip">실시간 점검</div>
                    <div class="tool-chip">상호작용 지원</div>
                </div>
            </div>
            <div class="surface-body">
                <div id="summary-grid" class="summary-grid">
                    <div class="metric-card composite status-group" data-filter="all" data-views="overview services notification monitoring config auth docs">
                        <div class="composite-top status-five no-divider">
                            <div class="status-tile primary">
                                <div class="status-tile-head">
                                    <div>
                                        <div class="metric-label">API 상태</div>
                                        <div class="metric-status-chip">핵심</div>
                                    </div>
                                    <div class="metric-icon">A</div>
                                </div>
                                <div id="api-status" class="metric-value normal">확인 중...</div>
                                <div class="metric-meta">
                                    <div class="meta-chip">운영 진입점</div>
                                </div>
                            </div>

                            <div class="status-tile primary">
                                <div class="status-tile-head">
                                    <div>
                                        <div class="metric-label">데이터베이스 상태</div>
                                        <div class="metric-status-chip">핵심</div>
                                    </div>
                                    <div class="metric-icon lime">DB</div>
                                </div>
                                <div id="db-status" class="metric-value normal">확인 중...</div>
                                <div class="metric-meta">
                                    <div class="meta-chip">핵심 의존성</div>
                                </div>
                                <div class="status-action-row">
                                    <button id="db-restart-button" class="secondary-button" type="button">DB 재시작</button>
                                    <div id="db-action-feedback" class="action-feedback">관리자 재시작만 지원</div>
                                </div>
                            </div>

                            <div class="status-tile">
                                <div class="status-tile-head">
                                    <div>
                                        <div class="metric-label">모니터링 상태</div>
                                    </div>
                                    <div class="metric-icon lime">↻</div>
                                </div>
                                <div id="monitoring-status" class="metric-value normal">확인 중...</div>
                                <div id="monitoring-desc" class="metric-subvalue">-</div>
                                <div class="metric-meta">
                                    <div class="meta-chip">백그라운드 루프</div>
                                </div>
                            </div>

                            <div class="status-tile">
                                <div class="status-tile-head">
                                    <div>
                                        <div class="metric-label">디스코드 알림</div>
                                    </div>
                                    <div class="metric-icon">N</div>
                                </div>
                                <div id="discord-status" class="metric-value normal">확인 중...</div>
                                <div id="discord-desc" class="metric-subvalue">웹훅 설정 상태</div>
                                <div class="metric-meta">
                                    <div class="meta-chip">알림 채널</div>
                                </div>
                            </div>

                            <div class="status-tile">
                                <div class="status-tile-head">
                                    <div>
                                        <div class="metric-label">설정 상태</div>
                                    </div>
                                    <div class="metric-icon danger">C</div>
                                </div>
                                <div id="config-status" class="metric-value warning">확인 중...</div>
                                <div id="config-desc" class="metric-subvalue">환경 검증과 기능 설정 상태</div>
                                <div class="metric-meta">
                                    <div class="meta-chip">검증 경고</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="metric-card composite wide" data-filter="resource" data-views="overview thresholds services">
                        <div class="composite-bottom">
                            <div class="mini-metric">
                                <div class="mini-metric-title">메모리 사용량</div>
                                <div class="metric-visual">
                                    <div class="metric-visual-copy">
                                        <div id="memory-status" class="metric-value normal">확인 중...</div>
                                        <div id="memory-desc" class="metric-subvalue">-</div>
                                    </div>
                                    <div id="memory-donut" class="metric-donut normal">
                                        <div id="memory-donut-value" class="metric-donut-value">0%</div>
                                    </div>
                                </div>
                            </div>
                            <div class="mini-metric">
                                <div class="mini-metric-title">디스크 사용량</div>
                                <div class="metric-visual">
                                    <div class="metric-visual-copy">
                                        <div id="disk-status" class="metric-value normal">확인 중...</div>
                                        <div id="disk-desc" class="metric-subvalue">-</div>
                                    </div>
                                    <div id="disk-donut" class="metric-donut normal">
                                        <div id="disk-donut-value" class="metric-donut-value">0%</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="summary-note">
                    <div>
                        <div class="summary-note-label">운영 브리핑</div>
                        <div id="summary-status" class="summary-status">대시보드 상태를 확인하는 중입니다.</div>
                        <div id="summary-copy" class="summary-copy">현재 운영 상태를 요약합니다.</div>
                    </div>
                    <div class="summary-note-meta">
                        <div class="summary-note-row"><span>마지막 상태 확인</span><strong id="checked-time">-</strong></div>
                        <div class="summary-note-row"><span>모니터링 마지막 점검</span><strong id="monitor-last-check">-</strong></div>
                        <div class="summary-note-row"><span>데모 서비스</span><strong id="demo-notes-status">-</strong></div>
                        <div class="summary-note-row"><span>설정 경고 수</span><strong id="config-warning-count">-</strong></div>
                        <div class="summary-note-row compact"><span>알림 기준</span><strong id="threshold-summary">-</strong></div>
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
                    <div class="surface-title">운영 이벤트</div>
                    <div class="surface-heading">운영 세부 현황</div>
                </div>
            </div>
            <div class="surface-body">
                <div class="detail-grid">
                    <div class="subpanel" data-panel="warnings" data-views="overview config auth docs">
                        <div class="subpanel-header">
                            <div>
                                <div class="subpanel-title">설정 경고</div>
                            </div>
                        </div>
                        <div id="warning-list" class="warning-list">
                            <div class="warning-item empty">설정 경고가 없습니다.</div>
                        </div>
                    </div>

                    <div class="subpanel" data-panel="alerts" data-views="overview alerts logs notification monitoring services thresholds">
                        <div class="subpanel-header">
                            <div>
                                <div class="subpanel-title">최근 알림</div>
                                <div class="interaction-state">
                                    <div id="interaction-badge" class="interaction-badge">현재 필터: 전체</div>
                                    <button id="interaction-reset" class="interaction-reset" type="button">필터 해제</button>
                                </div>
                            </div>
                            <div class="subpanel-actions">
                                <button class="filter-chip is-active" type="button" data-alert-filter="all">전체</button>
                                <button class="filter-chip" type="button" data-alert-filter="incident">장애</button>
                                <button class="filter-chip" type="button" data-alert-filter="recovery">복구</button>
                                <button class="filter-chip" type="button" data-alert-filter="resource">자원</button>
                                <button class="primary-button" type="button" onclick="loadDashboard()">로그 갱신</button>
                                <div id="refresh-hint" class="helper-text">자동 갱신: 모니터링 상태를 확인하는 중...</div>
                            </div>
                        </div>
                        <div id="alert-list" class="alerts-list">
                            <div class="alert-item">
                                <div class="alert-side">
                                    <div class="alert-kind">loading</div>
                                    <div class="alert-time">로그 준비 중</div>
                                </div>
                                <div class="alert-main">
                                    <div class="alert-title">알림을 불러오는 중입니다.</div>
                                    <div class="alert-message">최신 운영 이벤트를 시간순으로 정리해서 보여줍니다.</div>
                                </div>
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
            activeMetricFilter: "all",
            activeAlertFilter: "all",
            latestAlerts: [],
            activeSidebarView: "overview",
        };

        async function fetchJson(url) {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(url + " 요청 실패");
            }
            return await response.json();
        }

        function setStatusValue(element, text, tone) {
            if (!element) {
                return;
            }
            element.textContent = text;
            element.className = "metric-value " + tone;
        }

        function setBarWidth(id, value) {
            const element = document.getElementById(id);
            if (!element) {
                return;
            }
            const safeValue = Math.max(0, Math.min(Number(value) || 0, 100));
            element.style.width = safeValue + "%";
        }

        function setDonutValue(donutId, valueId, percent, tone) {
            const donut = document.getElementById(donutId);
            const value = document.getElementById(valueId);
            const safePercent = Math.max(0, Math.min(Number(percent) || 0, 100));

            if (donut) {
                donut.style.setProperty("--percent", safePercent);
                donut.className = "metric-donut " + tone;
            }

            if (value) {
                value.textContent = safePercent + "%";
            }
        }

        function getUsageTone(percent, threshold) {
            return Number(percent) >= Number(threshold) ? "warning" : "connected";
        }

        function matchesMetricFilter(alert, filter) {
            if (filter === "all") {
                return true;
            }
            if (filter === "resource") {
                return String(alert.type || "").startsWith("resource") || ["memory", "disk"].includes(alert.target);
            }
            if (filter === "config") {
                return alert.type === "notification_error";
            }
            if (filter === "monitoring") {
                return alert.target === "monitoring" || alert.target === "healthcheck";
            }
            if (filter === "notification") {
                return alert.target === "discord" || alert.type === "notification_error";
            }
            return alert.target === filter;
        }

        function matchesAlertFilter(alert, filter) {
            if (filter === "all") {
                return true;
            }
            if (filter === "resource") {
                return String(alert.type || "").startsWith("resource");
            }
            return alert.type === filter;
        }

        function applyMetricFilter(filter) {
            dashboardState.activeMetricFilter = filter;
            document.querySelectorAll(".metric-card").forEach(card => {
                card.classList.toggle("is-active", filter !== "all" && card.dataset.filter === filter);
            });
            updateInteractionBadge();
            renderAlerts(dashboardState.latestAlerts);
        }

        function applyAlertFilter(filter) {
            dashboardState.activeAlertFilter = filter;
            document.querySelectorAll("[data-alert-filter]").forEach(button => {
                button.classList.toggle("is-active", button.dataset.alertFilter === filter);
            });
            updateInteractionBadge();
            renderAlerts(dashboardState.latestAlerts);
        }

        function getFilterLabel(filter) {
            const labels = {
                all: "전체",
                api: "API",
                database: "데이터베이스",
                resource: "자원",
                monitoring: "모니터링",
                notification: "알림 채널",
                config: "설정",
                incident: "장애",
                recovery: "복구",
            };
            return labels[filter] || filter;
        }

        function updateInteractionBadge() {
            const badge = document.getElementById("interaction-badge");
            if (!badge) {
                return;
            }

            const metricLabel = getFilterLabel(dashboardState.activeMetricFilter);
            const alertLabel = getFilterLabel(dashboardState.activeAlertFilter);
            const summary =
                dashboardState.activeMetricFilter === "all" && dashboardState.activeAlertFilter === "all"
                    ? "현재 필터: 전체"
                    : "현재 필터: " + metricLabel + " / " + alertLabel;

            badge.textContent = summary;
        }

        function resetInteractions() {
            applyMetricFilter("all");
            applyAlertFilter("all");
        }

        async function restartDatabase() {
            const restartButton = document.getElementById("db-restart-button");
            const feedback = document.getElementById("db-action-feedback");

            if (!restartButton || !feedback) {
                return;
            }

            const confirmed = window.confirm("데이터베이스를 재시작할까요?");
            if (!confirmed) {
                return;
            }

            restartButton.disabled = true;
            feedback.textContent = "DB 재시작 요청 중...";

            try {
                const response = await fetch("/admin/database/restart", {
                    method: "POST",
                });
                const result = await response.json();

                feedback.textContent = result.message || "DB 재시작 요청을 처리했습니다.";

                if (response.ok) {
                    window.setTimeout(loadDashboard, 3000);
                }
            } catch (error) {
                feedback.textContent = "DB 재시작 요청에 실패했습니다.";
            } finally {
                restartButton.disabled = false;
            }
        }

        function setBadgeText(id, text) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = text;
            }
        }

        function setText(id, text) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = text;
            }
        }

        function applySidebarView(view) {
            dashboardState.activeSidebarView = view;

            document.querySelectorAll("[data-nav-view]").forEach(item => {
                item.classList.toggle("active", item.dataset.navView === view);
            });

            document.querySelectorAll(".metric-card").forEach(card => {
                const views = String(card.dataset.views || "overview").split(" ");
                const visible = view === "overview" || views.includes(view);
                card.classList.toggle("is-hidden-view", !visible);
            });

            document.querySelectorAll(".subpanel").forEach(panel => {
                const views = String(panel.dataset.views || "overview").split(" ");
                const visible = view === "overview" || views.includes(view);
                panel.classList.toggle("is-hidden-view", !visible);
            });

            if (view === "overview") {
                resetInteractions();
                window.scrollTo({ top: 0, behavior: "smooth" });
                return;
            }

            if (view === "alerts" || view === "logs") {
                applyMetricFilter("all");
                applyAlertFilter(view === "alerts" ? "incident" : "all");
                document.getElementById("alert-list")?.scrollIntoView({ behavior: "smooth", block: "start" });
                return;
            }

            if (view === "notification") {
                applyMetricFilter("notification");
                applyAlertFilter("all");
                document.getElementById("alert-list")?.scrollIntoView({ behavior: "smooth", block: "start" });
                return;
            }

            if (view === "monitoring") {
                applyMetricFilter("monitoring");
                applyAlertFilter("all");
                document.getElementById("summary-grid")?.scrollIntoView({ behavior: "smooth", block: "start" });
                return;
            }

            if (view === "thresholds") {
                applyMetricFilter("resource");
                applyAlertFilter("resource");
                document.getElementById("summary-grid")?.scrollIntoView({ behavior: "smooth", block: "start" });
                return;
            }

            if (view === "config" || view === "auth" || view === "docs") {
                applyMetricFilter("config");
                applyAlertFilter("all");
                document.getElementById("warning-list")?.scrollIntoView({ behavior: "smooth", block: "start" });
                return;
            }

            if (view === "services") {
                applyMetricFilter("all");
                applyAlertFilter("all");
                document.getElementById("summary-grid")?.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }

        function filterSidebarMenu(query) {
            const normalizedQuery = String(query || "").trim().toLowerCase();

            document.querySelectorAll(".nav-section").forEach(section => {
                const items = Array.from(section.querySelectorAll(".nav-item"));
                let visibleCount = 0;

                items.forEach(item => {
                    const label = (item.querySelector("span")?.textContent || "").toLowerCase();
                    const matched = normalizedQuery === "" || label.includes(normalizedQuery);
                    item.classList.toggle("is-hidden", !matched);
                    if (matched) {
                        visibleCount += 1;
                    }
                });

                section.classList.toggle("is-hidden", visibleCount === 0);
            });
        }

        function bindDashboardInteractions() {
            const shell = document.querySelector(".dashboard-shell");
            const sidebarToggle = document.getElementById("sidebar-toggle");
            const resetButton = document.getElementById("interaction-reset");
            const menuSearch = document.getElementById("menu-search");
            const dbRestartButton = document.getElementById("db-restart-button");

            if (sidebarToggle && !sidebarToggle.dataset.bound) {
                sidebarToggle.dataset.bound = "true";
                sidebarToggle.addEventListener("click", () => {
                    shell.classList.toggle("sidebar-collapsed");
                });
            }

            document.querySelectorAll(".metric-card").forEach(card => {
                if (card.dataset.bound) {
                    return;
                }
                card.dataset.bound = "true";
                card.setAttribute("tabindex", "0");
                card.setAttribute("role", "button");
                card.addEventListener("click", () => {
                    const nextFilter = dashboardState.activeMetricFilter === card.dataset.filter ? "all" : card.dataset.filter;
                    applyMetricFilter(nextFilter);
                });
                card.addEventListener("keydown", event => {
                    if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        const nextFilter = dashboardState.activeMetricFilter === card.dataset.filter ? "all" : card.dataset.filter;
                        applyMetricFilter(nextFilter);
                    }
                });
            });

            document.querySelectorAll("[data-alert-filter]").forEach(button => {
                if (button.dataset.bound) {
                    return;
                }
                button.dataset.bound = "true";
                button.addEventListener("click", () => {
                    applyAlertFilter(button.dataset.alertFilter);
                });
            });

            if (resetButton && !resetButton.dataset.bound) {
                resetButton.dataset.bound = "true";
                resetButton.addEventListener("click", resetInteractions);
            }

            if (dbRestartButton && !dbRestartButton.dataset.bound) {
                dbRestartButton.dataset.bound = "true";
                dbRestartButton.addEventListener("click", restartDatabase);
            }

            if (menuSearch && !menuSearch.dataset.bound) {
                menuSearch.dataset.bound = "true";
                menuSearch.addEventListener("input", event => {
                    filterSidebarMenu(event.target.value);
                });
                menuSearch.addEventListener("search", event => {
                    filterSidebarMenu(event.target.value);
                });
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

            updateInteractionBadge();
            filterSidebarMenu(menuSearch ? menuSearch.value : "");
            applySidebarView(dashboardState.activeSidebarView);
        }

        function updateSidebarMeta(health, monitoring, alerts) {
            const alertCount = Array.isArray(alerts) ? alerts.length : 0;
            const databaseConnected = health && health.database && health.database.status === "connected";
            const demoNotesConnected = health && health.demo_notes && health.demo_notes.status === "connected";
            const servicesHealthy = health && health.api === "ok" && databaseConnected && demoNotesConnected;
            const warnings = monitoring && monitoring.config_warnings ? monitoring.config_warnings.length : 0;

            setBadgeText("nav-services-badge", servicesHealthy ? "정상" : "주의");
            setBadgeText("nav-alerts-badge", String(alertCount));
            setBadgeText("nav-notification-badge", monitoring && monitoring.discord_webhook_configured ? "활성" : "대기");
            setBadgeText("nav-monitoring-badge", monitoring && monitoring.enabled ? "실행" : "중지");
            setBadgeText(
                "nav-thresholds-badge",
                monitoring && monitoring.thresholds
                    ? monitoring.thresholds.memory_percent + "/" + monitoring.thresholds.disk_percent
                    : "-"
            );
            setBadgeText("nav-config-badge", warnings > 0 ? "경고 " + warnings : "정상");
            setBadgeText("nav-logs-badge", alertCount > 0 ? "최근 " + Math.min(alertCount, 9) : "비어 있음");
            setBadgeText("nav-auth-badge", monitoring && monitoring.monitor_auth_configured ? "설정됨" : "누락");
            setBadgeText("nav-instance-badge", servicesHealthy ? "활성" : "점검");
            setBadgeText("nav-docs-badge", monitoring && monitoring.api_docs_enabled ? "허용" : "차단");
            setText("tracked-targets", "3 Services");
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
            dashboardState.latestAlerts = Array.isArray(alerts) ? alerts : [];
            alertList.innerHTML = "";

            const filteredAlerts = dashboardState.latestAlerts
                .filter(alert => matchesMetricFilter(alert, dashboardState.activeMetricFilter))
                .filter(alert => matchesAlertFilter(alert, dashboardState.activeAlertFilter));

            if (filteredAlerts.length === 0) {
                const emptyState = document.createElement("div");
                emptyState.className = "alert-item";
                emptyState.innerHTML =
                    '<div class="alert-side">' +
                        '<div class="alert-kind">clear</div>' +
                        '<div class="alert-time">최근 이벤트 없음</div>' +
                    '</div>' +
                    '<div class="alert-main">' +
                        '<div class="alert-title">선택한 조건에 맞는 알림이 없습니다.</div>' +
                        '<div class="alert-message">상단 카드나 필터 버튼을 다시 눌러 다른 영역의 로그를 확인해 보세요.</div>' +
                    '</div>';
                alertList.appendChild(emptyState);
                return;
            }

            filteredAlerts.slice(0, 6).forEach(alert => {
                const item = document.createElement("div");
                const side = document.createElement("div");
                const kind = document.createElement("div");
                const time = document.createElement("div");
                const main = document.createElement("div");
                const title = document.createElement("div");
                const message = document.createElement("div");
                const meta = document.createElement("div");
                const targetChip = document.createElement("div");
                const statusChip = document.createElement("div");

                item.className = "alert-item " + (alert.type || "");
                side.className = "alert-side";
                kind.className = "alert-kind";
                time.className = "alert-time";
                main.className = "alert-main";
                title.className = "alert-title";
                message.className = "alert-message";
                meta.className = "alert-meta";
                targetChip.className = "alert-meta-chip";
                statusChip.className = "alert-meta-chip";

                kind.textContent = alert.type || "event";
                time.textContent = alert.timestamp || "-";
                title.textContent = alert.message || "이벤트 메시지 없음";
                message.textContent = "대상과 상태를 함께 보고 후속 대응이 필요한지 빠르게 판단할 수 있습니다.";
                targetChip.textContent = "대상: " + (alert.target || "-");
                statusChip.textContent = "상태: " + (alert.status || "-");

                side.appendChild(kind);
                side.appendChild(time);
                meta.appendChild(targetChip);
                meta.appendChild(statusChip);
                main.appendChild(title);
                main.appendChild(message);
                main.appendChild(meta);
                item.appendChild(side);
                item.appendChild(main);
                alertList.appendChild(item);
            });
        }

        function renderSummary(health, monitoring) {
            const summaryStatus = document.getElementById("summary-status");
            const summaryCopy = document.getElementById("summary-copy");
            const databaseConnected = health && health.database && health.database.status === "connected";
            const warningCount = (monitoring && monitoring.config_warnings ? monitoring.config_warnings.length : 0);

            if (!health) {
                summaryStatus.textContent = "상태 점검 실패";
                summaryStatus.className = "summary-status danger";
                summaryCopy.textContent = "핵심 상태 데이터를 가져오지 못했습니다. 인증 정보나 백엔드 응답을 먼저 확인해 주세요.";
                return;
            }

            if (!databaseConnected) {
                summaryStatus.textContent = "데이터베이스 점검 필요";
                summaryStatus.className = "summary-status danger";
                summaryCopy.textContent = "API는 열려 있어도 데이터베이스 연결이 끊기면 운영 흐름이 불안정해집니다. 최근 알림에서 관련 이력을 확인해 주세요.";
                return;
            }

            if (warningCount > 0) {
                summaryStatus.textContent = "설정 보완 필요";
                summaryStatus.className = "summary-status warning";
                summaryCopy.textContent = "서비스는 응답하지만 일부 보호 설정이나 환경 변수가 기본값으로 동작 중입니다. 설정 경고를 먼저 정리하는 편이 안전합니다.";
                return;
            }

            summaryStatus.textContent = "운영 상태 양호";
            summaryStatus.className = "summary-status connected";
            summaryCopy.textContent = "API, 데이터베이스, 모니터링 루프가 모두 응답 중이며 설정 경고도 없습니다.";
        }

        function scheduleAutoRefresh(intervalSeconds) {
            if (dashboardState.refreshTimer) {
                window.clearTimeout(dashboardState.refreshTimer);
            }

            const safeIntervalSeconds = Math.max(Number(intervalSeconds) || 30, 15);
            document.getElementById("refresh-hint").textContent = "자동 갱신: " + safeIntervalSeconds + "초마다";
            dashboardState.refreshTimer = window.setTimeout(loadDashboard, safeIntervalSeconds * 1000);
        }

        function fillUnavailableState() {
            setStatusValue(document.getElementById("api-status"), "알 수 없음", "disconnected");
            setStatusValue(document.getElementById("db-status"), "알 수 없음", "disconnected");
            setStatusValue(document.getElementById("memory-status"), "알 수 없음", "disconnected");
            setStatusValue(document.getElementById("disk-status"), "알 수 없음", "disconnected");
            setStatusValue(document.getElementById("monitoring-status"), "알 수 없음", "disconnected");
            setStatusValue(document.getElementById("discord-status"), "알 수 없음", "disconnected");
            setStatusValue(document.getElementById("config-status"), "알 수 없음", "disconnected");
            document.getElementById("demo-notes-status").textContent = "-";
            document.getElementById("threshold-summary").textContent = "-";
            document.getElementById("memory-desc").textContent = "-";
            document.getElementById("disk-desc").textContent = "-";
            document.getElementById("monitoring-desc").textContent = "-";
            document.getElementById("discord-desc").textContent = "-";
            document.getElementById("config-desc").textContent = "환경 검증 상태를 확인하지 못했습니다.";
            document.getElementById("checked-time").textContent = "-";
            document.getElementById("monitor-last-check").textContent = "-";
            document.getElementById("config-warning-count").textContent = "-";
            setBarWidth("api-bar", 20);
            setBarWidth("db-bar", 20);
            setDonutValue("memory-donut", "memory-donut-value", 0, "disconnected");
            setDonutValue("disk-donut", "disk-donut-value", 0, "disconnected");
        }

        async function loadDashboard() {
            bindDashboardInteractions();

            const [healthResult, systemResult, alertsResult, monitoringResult] = await Promise.allSettled([
                fetchJson("/health"),
                fetchJson("/system"),
                fetchJson("/alerts"),
                fetchJson("/monitoring/status"),
            ]);

            const health = healthResult.status === "fulfilled" ? healthResult.value : null;
            const system = systemResult.status === "fulfilled" ? systemResult.value : null;
            const alerts = alertsResult.status === "fulfilled" ? alertsResult.value : [];
            const monitoring = monitoringResult.status === "fulfilled" ? monitoringResult.value : null;

            if (!health && !system && !monitoring) {
                fillUnavailableState();
                updateSidebarMeta(null, null, alerts);
                document.getElementById("summary-status").textContent = "대시보드 요청 실패";
                document.getElementById("summary-status").className = "summary-status danger";
                document.getElementById("summary-copy").textContent = "상태 데이터를 전혀 가져오지 못했습니다. 인증 정보와 백엔드 연결을 먼저 확인해 주세요.";
                renderWarnings(["대시보드 상태 데이터를 불러오지 못했습니다."]);
                renderAlerts(alerts);
                scheduleAutoRefresh(30);
                return;
            }

            if (health) {
                const apiHealthy = health.api === "ok";
                const databaseConnected = health.database && health.database.status === "connected";
                const demoNotesConnected = health.demo_notes && health.demo_notes.status === "connected";
                setStatusValue(document.getElementById("api-status"), apiHealthy ? "정상" : String(health.api || "오류"), apiHealthy ? "connected" : "warning");
                setStatusValue(document.getElementById("db-status"), databaseConnected ? "연결됨" : "연결 안 됨", databaseConnected ? "connected" : "disconnected");
                document.getElementById("demo-notes-status").textContent = demoNotesConnected ? "연결됨" : "점검 필요";
                document.getElementById("checked-time").textContent = health.timestamp || "-";
                setBarWidth("api-bar", apiHealthy ? 100 : 28);
                setBarWidth("db-bar", databaseConnected ? 100 : 30);
            } else {
                setStatusValue(document.getElementById("api-status"), "알 수 없음", "disconnected");
                setStatusValue(document.getElementById("db-status"), "알 수 없음", "disconnected");
                document.getElementById("demo-notes-status").textContent = "-";
                document.getElementById("checked-time").textContent = "-";
                setBarWidth("api-bar", 20);
                setBarWidth("db-bar", 20);
            }

            if (system) {
                const monitoringThresholds = monitoring && monitoring.thresholds ? monitoring.thresholds : { memory_percent: 80, disk_percent: 80 };
                const memoryTone = getUsageTone(system.memory.percent, monitoringThresholds.memory_percent);
                const diskTone = getUsageTone(system.disk.percent, monitoringThresholds.disk_percent);
                setStatusValue(document.getElementById("memory-status"), system.memory.percent + "%", memoryTone);
                setStatusValue(document.getElementById("disk-status"), system.disk.percent + "%", diskTone);
                document.getElementById("memory-desc").textContent = system.memory.used_gb + "GB / " + system.memory.total_gb + "GB 사용 중 (임계치 " + monitoringThresholds.memory_percent + "%)";
                document.getElementById("disk-desc").textContent = system.disk.used_gb + "GB / " + system.disk.total_gb + "GB 사용 중 (임계치 " + monitoringThresholds.disk_percent + "%)";
                setDonutValue("memory-donut", "memory-donut-value", system.memory.percent, memoryTone);
                setDonutValue("disk-donut", "disk-donut-value", system.disk.percent, diskTone);
            } else {
                setStatusValue(document.getElementById("memory-status"), "알 수 없음", "disconnected");
                setStatusValue(document.getElementById("disk-status"), "알 수 없음", "disconnected");
                document.getElementById("memory-desc").textContent = "시스템 자원 데이터를 가져오지 못했습니다.";
                document.getElementById("disk-desc").textContent = "시스템 자원 데이터를 가져오지 못했습니다.";
                setDonutValue("memory-donut", "memory-donut-value", 0, "disconnected");
                setDonutValue("disk-donut", "disk-donut-value", 0, "disconnected");
            }

            if (monitoring) {
                const warningMessages = monitoring.config_warnings || [];
                const warningCount = warningMessages.length;
                setStatusValue(document.getElementById("monitoring-status"), monitoring.enabled ? "실행 중" : "중지됨", monitoring.enabled ? "connected" : "disconnected");
                setStatusValue(document.getElementById("discord-status"), monitoring.discord_webhook_configured ? "활성화" : "비활성화", monitoring.discord_webhook_configured ? "connected" : "warning");
                setStatusValue(document.getElementById("config-status"), warningCount === 0 ? "정상" : "보완 필요", warningCount === 0 ? "connected" : "warning");
                document.getElementById("monitoring-desc").textContent = "주기 " + monitoring.interval_seconds + "초" + (monitoring.api_docs_enabled ? " | 문서 노출 허용" : " | 문서 노출 비활성화");
                document.getElementById("discord-desc").textContent = monitoring.monitor_auth_configured ? "인증 및 알림 채널 구성이 확인되었습니다." : "보호용 인증 설정을 확인해 주세요.";
                document.getElementById("threshold-summary").textContent = "메모리 " + monitoring.thresholds.memory_percent + "% / 디스크 " + monitoring.thresholds.disk_percent + "%";
                document.getElementById("config-desc").textContent = "인증 " + (monitoring.monitor_auth_configured ? "설정됨" : "누락") + " | 검증 경고 " + warningCount + "건";
                document.getElementById("monitor-last-check").textContent = monitoring.last_check || "-";
                document.getElementById("config-warning-count").textContent = String(warningCount);
                renderWarnings(warningMessages);
                renderSummary(health, monitoring);
                updateSidebarMeta(health, monitoring, alerts);
                scheduleAutoRefresh(monitoring.interval_seconds);
            } else {
                setStatusValue(document.getElementById("monitoring-status"), "알 수 없음", "disconnected");
                setStatusValue(document.getElementById("discord-status"), "알 수 없음", "disconnected");
                setStatusValue(document.getElementById("config-status"), "알 수 없음", "disconnected");
                document.getElementById("monitoring-desc").textContent = "모니터링 상태 데이터를 가져오지 못했습니다.";
                document.getElementById("discord-desc").textContent = "알림 채널 상태를 가져오지 못했습니다.";
                document.getElementById("threshold-summary").textContent = "-";
                document.getElementById("config-desc").textContent = "설정 검증 상태를 가져오지 못했습니다.";
                document.getElementById("monitor-last-check").textContent = "-";
                document.getElementById("config-warning-count").textContent = "-";
                renderWarnings(["모니터링 설정 상태를 불러오지 못했습니다."]);
                renderSummary(health, null);
                updateSidebarMeta(health, null, alerts);
                scheduleAutoRefresh(30);
            }

            renderAlerts(alerts);
        }

        loadDashboard();
    </script>
    """


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
