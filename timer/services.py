# timer/teams_service.py
import msal
import requests
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

class TeamsServiceError(Exception):
    pass

class TeamsService:
    TOKEN_CACHE_KEY = "graph_app_token"
    TOKEN_CACHE_TTL = getattr(settings, "MS_TOKEN_CACHE_TTL", 3300)

    @classmethod
    def _build_msal_app(cls, tenant_id=None):
        tenant = tenant_id or settings.MS_TENANT_ID
        authority = f"https://login.microsoftonline.com/{tenant}"
        return msal.ConfidentialClientApplication(
            client_id=settings.MS_CLIENT_ID,
            client_credential=settings.MS_CLIENT_SECRET,
            authority=authority
        )

    @classmethod
    def get_access_token(cls, tenant_id=None):
        tenant = tenant_id or settings.MS_TENANT_ID
        cache_key = f"{cls.TOKEN_CACHE_KEY}::{tenant}"
        token = cache.get(cache_key)
        if token:
            return token

        app = cls._build_msal_app(tenant_id=tenant)
        scope = [settings.MS_GRAPH_SCOPE]
        result = app.acquire_token_for_client(scopes=scope)
        if "access_token" not in result:
            logger.error("MSAL token error: %s", result)
            raise TeamsServiceError(f"Token generation failed: {result.get('error_description') or result}")
        token = result["access_token"]
        cache.set(cache_key, token, cls.TOKEN_CACHE_TTL)
        return token

    @classmethod
    def get_user_by_email(cls, email: str, access_token: str):
        url = f"{GRAPH_BASE}/users/{email}"
        r = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=15)
        if r.status_code == 404:
            raise TeamsServiceError(f"user not found: {email}")
        if r.status_code == 403:
            # permission denied
            raise TeamsServiceError(f"get_user failed: 403 {r.text}")
        if not r.ok:
            raise TeamsServiceError(f"get_user failed: {r.status_code} {r.text}")
        return r.json()

    @classmethod
    def create_chat_with_app(cls, user_email: str, access_token: str):
        url = f"{GRAPH_BASE}/chats"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        payload = {
            "chatType": "oneOnOne",
            "members": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"{GRAPH_BASE}/users('{user_email}')"
                },
                {
                    "@odata.type": "#microsoft.graph.aadAppConversationMember",
                    "roles": ["owner"],
                    # If Graph rejects using client id, change this to the app's objectId
                    "app@odata.bind": f"{GRAPH_BASE}/applications/{settings.MS_CLIENT_ID}"
                }
            ]
        }
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        if r.status_code in (200, 201):
            return r.json().get("id")
        if r.status_code == 409:
            try:
                body = r.json()
                if "id" in body:
                    return body["id"]
            except Exception:
                pass
        raise TeamsServiceError(f"create_chat failed: {r.status_code} {r.text}")

    @classmethod
    def send_message_to_chat(cls, chat_id: str, message_html: str, access_token: str):
        url = f"{GRAPH_BASE}/chats/{chat_id}/messages"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        payload = {"body": {"contentType": "html", "content": message_html}}
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        if r.status_code not in (200, 201):
            raise TeamsServiceError(f"send_message failed: {r.status_code} {r.text}")
        return r.json()

    @classmethod
    def notify_user_by_email(cls, user_email: str, html_message: str, tenant_id: str | None = None):
        token = cls.get_access_token(tenant_id)
        # Validate user - will raise TeamsServiceError(403) if insufficient perms
        cls.get_user_by_email(user_email, token)
        chat_id = cls.create_chat_with_app(user_email, token)
        sent = cls.send_message_to_chat(chat_id, html_message, token)
        return {"chat_id": chat_id, "message": sent}

    @classmethod
    def send_webhook_message(cls, html_message: str, webhook_url: str | None = None):
        hook = webhook_url or getattr(settings, "TEAMS_INCOMING_WEBHOOK", None)
        if not hook:
            raise TeamsServiceError("No incoming webhook configured")
        r = requests.post(hook, json={"text": html_message}, timeout=10)
        if r.status_code not in (200, 201):
            raise TeamsServiceError(f"Webhook send failed: {r.status_code} {r.text}")
        return r.text

    @classmethod
    def send_channel_message(cls, team_id: str, channel_id: str, html_message: str, tenant_id: str | None = None):
        token = cls.get_access_token(tenant_id)
        url = f"{GRAPH_BASE}/teams/{team_id}/channels/{channel_id}/messages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"body": {"contentType": "html", "content": html_message}}
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        if r.status_code not in (200, 201):
            raise TeamsServiceError(f"Channel message failed: {r.status_code} {r.text}")
        return r.json()
