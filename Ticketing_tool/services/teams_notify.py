# Ticketing_tool/services/teams_notify.py
import requests
from django.conf import settings
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

from .graph_auth import get_graph_access_token


def find_user_id_by_email(token: str, email: str):
    """
    Find Azure AD user by email (mail or userPrincipalName)
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = (
        f"{settings.MICROSOFT_GRAPH_BASE_URL}/users"
        f"?$filter=mail eq '{email}' or userPrincipalName eq '{email}'"
    )

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    users = resp.json().get("value", [])
    return users[0]["id"] if users else None


def send_teams_notification(user_email: str, title: str, message: str, link: str):
    """
    Sends Teams Activity Feed notification.
    Works only when IS_LOCAL = false (Render / production).
    """

    # Skip notifications in local mode
    if str(getattr(settings, "IS_LOCAL", "true")).lower() == "true":
        logger.warning("[INFO] Local mode ON → Teams notification SKIPPED.")
        return

    # Validate HTTPS link
    parsed = urlparse(link or "")
    if parsed.scheme != "https":
        raise ValueError(f"Invalid Teams webUrl (must be https): {link}")

    # Get Azure access token
    token = get_graph_access_token()

    # Lookup Teams/Azure AD user
    user_id = find_user_id_by_email(token, user_email)
    if not user_id:
        raise Exception(f"User not found in Azure AD/Teams: {user_email}")

    # Build Teams request
    url = (
        f"{settings.MICROSOFT_GRAPH_BASE_URL}/users/"
        f"{user_id}/teamwork/sendActivityNotification"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "topic": {
            "source": "text",
            "value": title,
            "webUrl": link,
            "displayName": title,
        },
        "activityType": "customAlert",
        "previewText": {"content": message},
        "templateParameters": [
            {"name": "message", "value": message},
            {"name": "link", "value": link},
        ],
    }

    response = requests.post(url, headers=headers, json=payload, timeout=10)

    if not response.ok:
        logger.error("Teams Notification FAILED: %s", response.text)
        raise Exception(f"Failed to send Teams notification: {response.text}")

    logger.info("Teams notification SENT → %s", user_email)
