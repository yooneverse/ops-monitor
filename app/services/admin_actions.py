import logging
import subprocess
from datetime import datetime
from pathlib import Path

from app.services.alert_history import add_alert_history

logger = logging.getLogger("uvicorn.error")
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def build_admin_action_result(
    *,
    status: str,
    message: str,
    requested_by: str,
) -> dict[str, str]:
    return {
        "status": status,
        "message": message,
        "action": "restart_database",
        "requested_by": requested_by,
        "timestamp": now_iso(),
    }


def record_admin_action(result: dict[str, str]) -> None:
    event_type = "admin_action" if result["status"] == "ok" else "admin_action_error"
    target_status = "completed" if result["status"] == "ok" else "failed"

    add_alert_history(
        {
            "type": event_type,
            "target": "database_restart",
            "status": target_status,
            "message": result["message"],
            "timestamp": result["timestamp"],
            "requested_by": result["requested_by"],
        }
    )


def restart_database_service(requested_by: str) -> dict[str, str]:
    command = ["docker", "compose", "restart", "db"]

    try:
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=True,
        )
    except FileNotFoundError:
        logger.exception("Docker CLI is not available")
        result = build_admin_action_result(
            status="error",
            message="Docker CLI를 찾을 수 없습니다.",
            requested_by=requested_by,
        )
        record_admin_action(result)
        return result
    except subprocess.TimeoutExpired:
        logger.exception("Database restart timed out")
        result = build_admin_action_result(
            status="error",
            message="DB 재시작 시간이 초과되었습니다.",
            requested_by=requested_by,
        )
        record_admin_action(result)
        return result
    except subprocess.CalledProcessError as error:
        logger.exception("Database restart failed")
        detail = error.stderr.strip() or error.stdout.strip() or "DB 재시작에 실패했습니다."
        result = build_admin_action_result(
            status="error",
            message=detail,
            requested_by=requested_by,
        )
        record_admin_action(result)
        return result

    detail = completed.stdout.strip() or "DB 재시작 요청을 보냈습니다."
    result = build_admin_action_result(
        status="ok",
        message=detail,
        requested_by=requested_by,
    )
    record_admin_action(result)
    return result
