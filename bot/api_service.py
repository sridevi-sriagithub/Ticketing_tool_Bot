import requests
import logging
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:8000"

# ✅ LOGIN & GET JWT TOKEN
def get_jwt_token(email, password):
    import requests

    url = "http://127.0.0.1:8000/user/api/login/"

    payload = {
        "email": email,
        "password": password
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("🔹 BOT LOGIN PAYLOAD:", payload)   # ✅ DEBUG
    response = requests.post(url, json=payload, headers=headers)

    print("🔹 BOT LOGIN STATUS:", response.status_code)  # ✅ DEBUG
    print("🔹 BOT LOGIN RESPONSE:", response.text)      # ✅ DEBUG

    if response.status_code == 200:
        data = response.json()
        return data.get("access")

    return None






def create_ticket(token, payload):
    url = f"{BASE_URL}/ticket/create/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        return response.json(), response.status_code
    except:
        return {"error": response.text}, response.status_code


# ✅ LIST TICKETS
def list_tickets(token):
    url = f"{BASE_URL}/ticket/all/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json(), response.status_code


# # ✅ TICKET STATUS
# def get_ticket_status(token, ticket_id):
#     url = f"{BASE_URL}/ticket/tickets/{ticket_id}/"
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     response = requests.get(url, headers=headers)
#     return response.json(), response.status_code

def get_ticket_status(token: str, ticket_id: str):
    url = f"{BASE_URL}/ticket/tickets/{ticket_id}/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        json_data = resp.json() if resp.content else {}
        return json_data, resp.status_code
    except Exception:
        logger.exception("[BOT] Error in get_ticket_status()")
        return {"error": "Ticket status failed"}, 500
    
def assign_ticket(token, ticket_id, assignee_id):
    url = f"http://127.0.0.1:8000/ticket/assign-ticket/{ticket_id.upper()}/"


    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {"assignee": assignee_id}

    response = requests.put(url, json=payload, headers=headers)

    try:
        data = response.json()
    except Exception:
        data = {"raw_response": response.text}

    return data, response.status_code
