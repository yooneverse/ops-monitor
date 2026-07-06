import os
from datetime import datetime, timezone

import requests


def build_discord_payload(title: str, fields: dict[str, str], level: str = "info") -> dict:
    level_icon = {
        "info": "[알림]",
        "warning": "[주의]",
        "critical": "[긴급]",
        "recovery": "[복구]",
    }.get(level, "[알림]")

    description = "\n".join([f"**{key}**: {value}" for key, value in fields.items()])

    return {
        "username": "Ops Monitor",
        "embeds": [
            {
                "title": f"{level_icon} {title}",
                "description": description,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ],
    }


def send_discord_message(content: str) -> bool:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return False

    try:
        response = requests.post(
            webhook_url,
            json={
                "username": "Ops Monitor",
                "content": content,
            },
            timeout=5,
        )
        return response.status_code < 400

    except requests.RequestException:
        return False


def send_discord_alert(title: str, fields: dict[str, str], level: str = "info") -> bool:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return False

    payload = build_discord_payload(title, fields, level)

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        return response.status_code < 400

    except requests.RequestException:
        return False