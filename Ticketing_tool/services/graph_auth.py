# Ticketing_tool/services/graph_auth.py
import requests
from django.conf import settings

def get_graph_access_token():
    tenant = settings.AZURE_TENANT_ID
    client_id = settings.AZURE_CLIENT_ID
    client_secret = settings.AZURE_CLIENT_SECRET

    token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    resp = requests.post(token_url, data=data, timeout=10)
    resp.raise_for_status()
    return resp.json()["access_token"]
