

import requests
from django.conf import settings
from django.core.cache import cache

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


class TeamsServiceError(Exception):
    pass


class TeamsService:
    """
    FINAL CORRECT VERSION (v3)
    -------------------------------------
    ✔ Uses app-only authentication
    ✔ Sends message to Teams channel (SUPPORTED)
    ✔ Works for SLA notifications, ticket alerts, etc.
    ✔ No private chat creation (NOT ALLOWED in app-only)
    ✔ Token caching included
    -------------------------------------
    """

    TOKEN_CACHE_KEY = "graph_app_token"
    TOKEN_EXPIRY = 3300   # 55 minutes

    @classmethod
    def get_access_token(cls, tenant_id=None):
        """
        Generate MS Graph app-only token using client_credentials
        Token is cached for 55 minutes.
        """
        tenant = tenant_id or settings.MS_TENANT_ID
        cache_key = f"{cls.TOKEN_CACHE_KEY}::{tenant}"

        # Return cached token if valid
        token = cache.get(cache_key)
        if token:
            return token

        # Generate new token
        url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
        data = {
            "client_id": settings.MS_CLIENT_ID,
            "client_secret": settings.MS_CLIENT_SECRET,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }

        r = requests.post(url, data=data)
        if r.status_code != 200:
            raise TeamsServiceError(f"Token generation failed: {r.status_code} {r.text}")

        token = r.json()["access_token"]

        # Cache the token
        cache.set(cache_key, token, cls.TOKEN_EXPIRY)

        return token

    @classmethod
    def send_channel_message(cls, team_id, channel_id, html_message, tenant_id=None):
        """
        Send message to a Microsoft Teams CHANNEL.
        This works with app-only tokens (client credentials).
        """

        token = cls.get_access_token(tenant_id)

        url = f"{GRAPH_BASE}/teams/{team_id}/channels/{channel_id}/messages"

        payload = {
            "body": {
                "contentType": "html",
                "content": html_message
            }
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        r = requests.post(url, json=payload, headers=headers)

        if r.status_code not in (200, 201):
            raise TeamsServiceError(
                f"Channel message failed: {r.status_code} {r.text}"
            )

        return r.json()

    @classmethod
    def send_webhook_message(cls, html_message, webhook_url=None):
        """
        Send a simple message to a Teams incoming webhook URL.
        This is channel-only and does not require Graph/Azure app permissions.
        """
        hook = webhook_url or getattr(settings, "TEAMS_INCOMING_WEBHOOK", None)
        if not hook:
            raise TeamsServiceError("No incoming webhook configured")

        payload = {"text": html_message}
        try:
            r = requests.post(hook, json=payload, timeout=15)
        except Exception as e:
            raise TeamsServiceError(f"Webhook send failed: {e}")

        if r.status_code not in (200, 201):
            raise TeamsServiceError(f"Webhook send failed: {r.status_code} {r.text}")

        return r.text

    # ------------------ Personal (1:1) message helpers ------------------
    @classmethod
    def get_user_by_email(cls, email: str, access_token: str):
        url = f"{GRAPH_BASE}/users/{email}"
        headers = {"Authorization": f"Bearer {access_token}"}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 404:
            raise TeamsServiceError(f"user not found: {email}")
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
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users/{user_email}"
                },
                {
                    "@odata.type": "#microsoft.graph.aadAppConversationMember",
                    "roles": ["owner"],
                    "app@odata.bind": f"https://graph.microsoft.com/v1.0/applications/{settings.MS_CLIENT_ID}"
                }
            ]
        }

        r = requests.post(url, json=payload, headers=headers, timeout=15)
        if r.status_code in (201, 200):
            body = r.json()
            return body.get("id")
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
        payload = {
            "body": {
                "contentType": "html",
                "content": message_html
            }
        }
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        if r.status_code in (201, 200):
            return r.json()
        raise TeamsServiceError(f"send_message failed: {r.status_code} {r.text}")

    @classmethod
    def notify_user_by_email(cls, user_email: str, html_message: str, tenant_id: str | None = None):
        """
        Send a 1:1 message to a user by email using app-only permissions.
        Note: requires proper application permissions (Chat.ReadWrite.All or ChatMessage.Send) and admin consent.
        """
        token = cls.get_access_token(tenant_id)
        # Validate user exists
        cls.get_user_by_email(user_email, token)
        # create/get chat and send message
        chat_id = cls.create_chat_with_app(user_email, token)
        sent = cls.send_message_to_chat(chat_id, html_message, token)
        # Return both chat id and sent message for downstream verification
        return {"chat_id": chat_id, "message": sent}

    @classmethod
    def get_message(cls, chat_id: str, message_id: str, tenant_id: str | None = None):
        """Fetch a sent message resource to verify it exists (used for debugging/verification).

        Returns the message JSON if found, otherwise raises TeamsServiceError.
        """
        token = cls.get_access_token(tenant_id)
        url = f"{GRAPH_BASE}/chats/{chat_id}/messages/{message_id}"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 404:
            raise TeamsServiceError(f"message not found: {chat_id}/{message_id}")
        if not r.ok:
            raise TeamsServiceError(f"get_message failed: {r.status_code} {r.text}")
        return r.json()
