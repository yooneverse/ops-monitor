import logging
import subprocess
from datetime import datetime
from pathlib import Path

from app.services.alert_history import add_alert_history

logger = logging.getLogger("uvicorn.error")
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def record_admin_action(
    *,
    status: str,
    message: str,
    requested_by: str,
) -> None:
    add_alert_history(
        {
            "type": "admin_action" if status == "ok" else "admin_action_error",
            "target": "database_restart",
            "status": "completed" if status == "ok" else "failed",
            "message": message,
            "timestamp": now_iso(),
            "requested_by": requested_by,
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
        result = {
            "status": "error",
            "message": "Docker CLI를 찾을 수 없습니다.",
        }
        record_admin_action(
            status=result["status"],
            message=result["message"],
            requested_by=requested_by,
        )
        return result
    except subprocess.TimeoutExpired:
        logger.exception("Database restart timed out")
        result = {
            "status": "error",
            "message": "DB 재시작 시간이 초과되었습니다.",
        }
        record_admin_action(
            status=result["status"],
            message=result["message"],
            requested_by=requested_by,
        )
        return result
    except subprocess.CalledProcessError as error:
        logger.exception("Database restart failed")
        detail = error.stderr.strip() or error.stdout.strip() or "DB 재시작에 실패했습니다."
        result = {
            "status": "error",
            "message": detail,
        }
        record_admin_action(
            status=result["status"],
            message=result["message"],
            requested_by=requested_by,
        )
        return result

    detail = completed.stdout.strip() or "DB 재시작 요청을 보냈습니다."
    result = {
        "status": "ok",
        "message": detail,
    }
    record_admin_action(
        status=result["status"],
        message=result["message"],
        requested_by=requested_by,
    )
    return result
