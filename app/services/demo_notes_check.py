import logging

import requests

from app.config import get_settings

logger = logging.getLogger("uvicorn.error")


def check_demo_notes_service() -> dict[str, str]:
    service_url = get_settings().demo_notes_url

    if not service_url:
        return {
            "status": "disabled",
            "message": "DEMO_NOTES_URL is not set",
        }

    try:
        response = requests.get(service_url, timeout=3)
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Demo notes service check failed")
        return {
            "status": "disconnected",
            "message": "Demo notes service is unavailable",
        }

    return {
        "status": "connected",
        "message": "Demo notes service is available",
    }
