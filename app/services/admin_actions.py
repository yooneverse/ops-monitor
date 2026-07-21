import logging
import subprocess
from pathlib import Path


logger = logging.getLogger("uvicorn.error")
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def restart_database_service() -> dict[str, str]:
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
        return {
            "status": "error",
            "message": "Docker CLI를 찾을 수 없습니다.",
        }
    except subprocess.TimeoutExpired:
        logger.exception("Database restart timed out")
        return {
            "status": "error",
            "message": "DB 재시작 시간이 초과되었습니다.",
        }
    except subprocess.CalledProcessError as error:
        logger.exception("Database restart failed")
        detail = error.stderr.strip() or error.stdout.strip() or "DB 재시작에 실패했습니다."
        return {
            "status": "error",
            "message": detail,
        }

    detail = completed.stdout.strip() or "DB 재시작 요청을 보냈습니다."
    return {
        "status": "ok",
        "message": detail,
    }
