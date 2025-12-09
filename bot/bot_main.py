
# import logging
# from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
# from .cards import create_welcome_card
# from .api_service import (
#     get_jwt_token,
#     create_ticket,
#     list_tickets,
#     get_ticket_status
# )

# logger = logging.getLogger(__name__)

# # ✅ SECURE IN-MEMORY TOKEN STORE (per emulator user)
# USER_TOKENS = {}


# class MainBot(ActivityHandler):

#     async def on_message_activity(self, turn_context: TurnContext):
#         raw_text = turn_context.activity.text.strip()
#         text = raw_text.lower()

#         user_name = turn_context.activity.from_property.name
#         user_id = turn_context.activity.from_property.id

#         # ✅ LOG WITHOUT SENSITIVE DATA
#         logger.info(f"Message received from {user_name}")

#         # ✅ ================= LOGIN =================
#         if text.startswith("login"):
#             parts = raw_text.split(maxsplit=2)

#             if len(parts) != 3:
#                 await turn_context.send_activity(
#                     "❌ Secure Login Format:\n\n"
#                     "login email password\n\n"
#                     "Example:\n"
#                     "login swetha@gmail.com Swetha@123"
#                 )
#                 return

#             email = parts[1]
#             password = parts[2]  # ✅ Never log this

#             token = get_jwt_token(email, password)

#             if token:
#                 USER_TOKENS[user_id] = token
#                 await turn_context.send_activity("✅ Login Successful")
#             else:
#                 await turn_context.send_activity("❌ Invalid Credentials")

#             return

#         # ✅ ================= GREETING =================
#         if text in ["hello", "hi", "hey"]:
#             await turn_context.send_activity(
#                 MessageFactory.attachment(create_welcome_card(user_name))
#             )
#             return

#         # ✅ ================= AUTH PROTECTED COMMANDS =================
#         if text.startswith("ticket"):
#             await self._handle_ticket_command(turn_context, text)
#             return

#         # ✅ ================= SAFE HELP =================
#         await turn_context.send_activity(
#             "📌 Secure Bot Commands:\n\n"
#             "1️⃣ login email password\n"
#             "2️⃣ ticket create\n"
#             "3️⃣ ticket list\n"
#             "4️⃣ ticket status <ticket_id>\n"
#         )

#     # ✅ ================= TICKET HANDLER =================
#     async def _handle_ticket_command(self, turn_context: TurnContext, text: str):
#         user_id = turn_context.activity.from_property.id

#         # ✅ SESSION AUTH CHECK
#         if user_id not in USER_TOKENS:
#             await turn_context.send_activity("🔐 Please login first")
#             return

#         token = USER_TOKENS[user_id]

#         # ✅ ========== CREATE TICKET ==========
#         if "create" in text:
#             payload = {
#                 "title": "Bot Ticket",
#                 "description": "Created securely via Bot"
#             }

#             result, status = create_ticket(token, payload)

#             if status in [200, 201]:
#                 await turn_context.send_activity(
#                     f"✅ Ticket Created\n🎫 ID: {result.get('ticket_id', result.get('id'))}"
#                 )
#             else:
#                 await turn_context.send_activity("❌ Ticket creation failed")

#         # ✅ ========== LIST TICKETS (SECURE + FIXED) ==========
#         elif "list" in text:
#             tickets, status = list_tickets(token)

#             if status != 200:
#                 await turn_context.send_activity("❌ Unable to fetch tickets")
#                 return

#             try:
#                 ticket_list = tickets.get("results", {}).get("all_tickets", [])

#                 if not isinstance(ticket_list, list) or not ticket_list:
#                     await turn_context.send_activity("ℹ️ No tickets available")
#                     return

#                 msg = "🎟 Your Tickets (Latest 10):\n\n"

#                 for t in ticket_list[:10]:
#                     msg += (
#                         f"🎫 {t.get('ticket_id', 'N/A')} | "
#                         f"{t.get('service_domain', 'N/A')} | "
#                         f"{t.get('service_type', 'N/A')} | "
#                         f"{t.get('assignee', 'N/A')} | "
#                         f"{t.get('assignee_role', 'N/A')}\n"
#                     )

#                 await turn_context.send_activity(msg)

#             except Exception:
#                 logger.exception("Ticket List Parsing Error")
#                 await turn_context.send_activity("❌ Ticket format error")

#         # ✅ ========== TICKET STATUS ==========
#         elif "status" in text:
#             parts = text.split()

#             if len(parts) != 3:
#                 await turn_context.send_activity("❌ Use: ticket status <ticket_id>")
#                 return

#             ticket_id = parts[2]

#             data, status = get_ticket_status(token, ticket_id)

#             if status == 200 and isinstance(data, dict):
#                 await turn_context.send_activity(
#                     f"🎫 Ticket ID: {data.get('ticket_id')}\n"
#                     f"📌 Title: {data.get('title')}\n"
#                     f"📊 Status: {data.get('status')}"
#                 )
#             else:
#                 await turn_context.send_activity("❌ Ticket not found")

#         # ✅ ========== INVALID TICKET COMMAND ==========
#         else:
#             await turn_context.send_activity(
#                 "❌ Invalid Ticket Command\n\n"
#                 "Use:\n"
#                 "- ticket create\n"
#                 "- ticket list\n"
#                 "- ticket status <id>"
#             )


# import logging
# import uuid
# from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
# from .cards import create_welcome_card
# from .api_service import (
#     get_jwt_token,
#     create_ticket,
#     list_tickets,
#     get_ticket_status
# )

# logger = logging.getLogger(__name__)

# # ✅ SECURE IN-MEMORY TOKEN STORE (per emulator user)
# USER_TOKENS = {}


# class MainBot(ActivityHandler):

#     async def on_message_activity(self, turn_context: TurnContext):
#         raw_text = turn_context.activity.text.strip()
#         text = raw_text.lower()

#         user_name = turn_context.activity.from_property.name
#         user_id = turn_context.activity.from_property.id

#         # ✅ LOG WITHOUT SENSITIVE DATA
#         logger.info(f"Message received from {user_name}")

#         # ✅ ================= LOGIN =================
#         if text.startswith("login"):
#             parts = raw_text.split(maxsplit=2)

#             if len(parts) != 3:
#                 await turn_context.send_activity(
#                     "❌ Secure Login Format:\n\n"
#                     "login email password\n\n"
#                     "Example:\n"
#                     "login swetha@gmail.com Swetha@123"
#                 )
#                 return

#             email = parts[1]
#             password = parts[2]  # ✅ Never log this

#             token = get_jwt_token(email, password)

#             if token:
#                 USER_TOKENS[user_id] = token
#                 await turn_context.send_activity("✅ Login Successful")
#             else:
#                 await turn_context.send_activity("❌ Invalid Credentials")

#             return

#         # ✅ ================= GREETING =================
#         if text in ["hello", "hi", "hey"]:
#             await turn_context.send_activity(
#                 MessageFactory.attachment(create_welcome_card(user_name))
#             )
#             return

#         # ✅ ================= AUTH PROTECTED COMMANDS =================
#         if text.startswith("ticket"):
#             await self._handle_ticket_command(turn_context, text)
#             return

#         # ✅ ================= SAFE HELP =================
#         await turn_context.send_activity(
#             "📌 Secure Bot Commands:\n\n"
#             "1️⃣ login email password\n"
#             "2️⃣ ticket create\n"
#             "3️⃣ ticket list\n"
#             "4️⃣ ticket status <ticket_id>\n"
#         )

#     # ✅ ================= TICKET HANDLER =================
#     async def _handle_ticket_command(self, turn_context: TurnContext, text: str):
#         user_id = turn_context.activity.from_property.id

#         # ✅ SESSION AUTH CHECK
#         if user_id not in USER_TOKENS:
#             await turn_context.send_activity("🔐 Please login first")
#             return

#         token = USER_TOKENS[user_id]

#         # ✅ ========== CREATE TICKET (FIXED FOR YOUR MODEL) ==========
#         if "create" in text:
#             payload = {
#                 "ticket_id": f"BOT-{uuid.uuid4().hex[:8].upper()}",
#                 "service_domain": 1,     # ✅ MUST EXIST IN DB
#                 "service_type": 1,       # ✅ MUST EXIST IN DB
#                 "summary": "Bot Generated Ticket",
#                 "description": "Created securely via Microsoft Bot",
#                 "created_by": 47         # ✅ LOGGED-IN USER ID
#             }

#             result, status = create_ticket(token, payload)

#             if status in [200, 201]:
#                 await turn_context.send_activity(
#                     f"✅ Ticket Created\n🎫 ID: {result.get('ticket_id')}"
#                 )
#             else:
#                 await turn_context.send_activity(
#                     f"❌ Ticket creation failed\n{result}"
#                 )

#         # ✅ ========== LIST TICKETS (SECURE + FIXED) ==========
#         elif "list" in text:
#             tickets, status = list_tickets(token)

#             if status != 200:
#                 await turn_context.send_activity("❌ Unable to fetch tickets")
#                 return

#             try:
#                 ticket_list = tickets.get("results", {}).get("all_tickets", [])

#                 if not isinstance(ticket_list, list) or not ticket_list:
#                     await turn_context.send_activity("ℹ️ No tickets available")
#                     return

#                 msg = "🎟 Your Tickets (Latest 10):\n\n"

#                 for t in ticket_list[:10]:
#                     msg += (
#                         f"🎫 {t.get('ticket_id', 'N/A')} | "
#                         f"{t.get('service_domain', 'N/A')} | "
#                         f"{t.get('service_type', 'N/A')} | "
#                         f"{t.get('assignee', 'N/A')} | "
#                         f"{t.get('assignee_role', 'N/A')}\n"
#                     )

#                 await turn_context.send_activity(msg)

#             except Exception:
#                 logger.exception("Ticket List Parsing Error")
#                 await turn_context.send_activity("❌ Ticket format error")

#         # ✅ ========== TICKET STATUS ==========
#         elif "status" in text:
#             parts = text.split()

#             if len(parts) != 3:
#                 await turn_context.send_activity("❌ Use: ticket status <ticket_id>")
#                 return

#             ticket_id = parts[2]
#             data, status = get_ticket_status(token, ticket_id)

#             if status == 200 and isinstance(data, dict):
#                 await turn_context.send_activity(
#                     f"🎫 Ticket ID: {data.get('ticket_id')}\n"
#                     f"📌 Title: {data.get('title')}\n"
#                     f"📊 Status: {data.get('status')}"
#                 )
#             else:
#                 await turn_context.send_activity("❌ Ticket not found")

#         # ✅ ========== INVALID TICKET COMMAND ==========
#         else:
#             await turn_context.send_activity(
#                 "❌ Invalid Ticket Command\n\n"
#                 "Use:\n"
#                 "- ticket create\n"
#                 "- ticket list\n"
#                 "- ticket status <id>"
#             )








# # bot/bot_main.py

# import logging
# import uuid

# from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
# from .cards import create_welcome_card
# from .api_service import (
#     get_jwt_token,
#     create_ticket,
#     list_tickets,
#     get_ticket_status,
#     assign_ticket,
# )

# logger = logging.getLogger(__name__)

# # ✅ Secure in-memory JWT token store (per Teams/Emulator user)
# USER_TOKENS = {}

# # ✅ Per-user conversation state for multi-step "ticket create"
# USER_SESSIONS = {}


# class MainBot(ActivityHandler):
#     """
#     Main bot class that handles:
#     - login email password
#     - ticket create (multi-step input)
#     - ticket list
#     - ticket status <ticket_id>
#     """

#     async def on_message_activity(self, turn_context: TurnContext):
#         raw_text = (turn_context.activity.text or "").strip()
#         text = raw_text.lower()

#         user_name = turn_context.activity.from_property.name
#         user_id = turn_context.activity.from_property.id

#         logger.info(f"Message received from user: {user_name} ({user_id})")

#         # ========== 1) LOGIN ==========
#         if text.startswith("login"):
#             await self._handle_login(turn_context, raw_text, user_id)
#             return

#         # ========== 2) MULTI-STEP TICKET CREATION FLOW ==========
#         # If the user is in the middle of a "ticket create" conversation,
#         # we handle that FIRST (before other commands)
#         if user_id in USER_SESSIONS:
#             await self._handle_ticket_creation_flow(turn_context, raw_text, user_id)
#             return

#         # ========== 3) GREETING ==========
#         if text in ["hello", "hi", "hey"]:
#             await turn_context.send_activity(
#                 MessageFactory.attachment(create_welcome_card(user_name))
#             )
#             return

#         # ========== 4) TICKET COMMANDS ==========
#         if text.startswith("ticket"):
#             await self._handle_ticket_command(turn_context, text)

#             return

#         # ========== 5) HELP (DEFAULT) ==========
#         await turn_context.send_activity(
#             "📌 Bot Commands:\n\n"
#             "1️⃣ login <email> <password>\n"
#             "2️⃣ ticket create\n"
#             "3️⃣ ticket list\n"
#             "4️⃣ ticket status <ticket_id>\n"
#             "\nExample:\n"
#             "login swethadomatoti@gmail.com Swetha@123"
#         )

#     # ============================================================
#     #                     LOGIN HANDLER
#     # ============================================================
#     async def _handle_login(self, turn_context: TurnContext, raw_text: str, user_id: str):
#         parts = raw_text.split(maxsplit=2)

#         if len(parts) != 3:
#             await turn_context.send_activity(
#                 "❌ Secure Login Format:\n\n"
#                 "`login email password`\n\n"
#                 "Example:\n"
#                 "`login swethadomatoti@gmail.com Swetha@123`"
#             )
#             return

#         email = parts[1]
#         password = parts[2]  # 🔒 do NOT log this

#         token = get_jwt_token(email, password)

#         if token:
#             USER_TOKENS[user_id] = token
#             await turn_context.send_activity("✅ Login Successful")
#         else:
#             await turn_context.send_activity("❌ Invalid Credentials")

#     # ============================================================
#     #               MULTI-STEP TICKET CREATION FLOW
#     # ============================================================
#     async def _handle_ticket_creation_flow(self, turn_context: TurnContext, raw_text: str, user_id: str):
#         """
#         Handles the interactive flow AFTER user types `ticket create`:
#         1. Ask for summary
#         2. Ask for description
#         3. Ask for service_domain id
#         4. Ask for service_type id
#         Then calls /ticket/create/ with collected data.
#         """
#         session = USER_SESSIONS.get(user_id)

#         # ✅ Allow user to cancel at any time
#         if raw_text.lower() in ["cancel", "stop", "exit"]:
#             del USER_SESSIONS[user_id]
#             await turn_context.send_activity("❌ Ticket creation cancelled.")
#             return

#         step = session.get("step")

#         # STEP 1: SUMMARY
#         if step == "summary":
#             session["summary"] = raw_text
#             session["step"] = "description"
#             await turn_context.send_activity("📝 Please enter ticket **description**:")
#             return

#         # STEP 2: DESCRIPTION
#         if step == "description":
#             session["description"] = raw_text
#             session["step"] = "service_domain"
#             await turn_context.send_activity(
#                 "📝 Enter **Service Domain ID** (e.g., 1):"
#             )
#             return

#         # STEP 3: SERVICE DOMAIN
#         if step == "service_domain":
#             try:
#                 session["service_domain"] = int(raw_text)
#             except ValueError:
#                 await turn_context.send_activity("❌ Please enter a valid numeric Service Domain ID.")
#                 return

#             session["step"] = "service_type"
#             await turn_context.send_activity(
#                 "📝 Enter **Service Type ID** (e.g., 1):"
#             )
#             return

#         # STEP 4: SERVICE TYPE → CREATE TICKET
#         if step == "service_type":
#             try:
#                 session["service_type"] = int(raw_text)
#             except ValueError:
#                 await turn_context.send_activity("❌ Please enter a valid numeric Service Type ID.")
#                 return

#             # Build payload from collected data
#             payload = {
#                 "ticket_id": f"BOT-{uuid.uuid4().hex[:8].upper()}",
#                 "service_domain": session["service_domain"],
#                 "service_type": session["service_type"],
#                 "summary": session["summary"],
#                 "description": session["description"],
#                 # 🔒 created_by is taken from JWT (request.user in Django)
#             }

#             token = USER_TOKENS.get(user_id)
#             result, status = create_ticket(token, payload)

#             # Clear session after attempt
#             del USER_SESSIONS[user_id]

#             logger.info(f"BOT CREATE STATUS: {status}")
#             logger.info(f"BOT CREATE RESPONSE: {result}")

#             if status in [200, 201]:
#                 await turn_context.send_activity(
#                     f"✅ Ticket Created Successfully\n🎫 Ticket ID: {result.get('ticket_id')}"
#                 )
#             else:
#                 await turn_context.send_activity(
#                     f"❌ Ticket creation failed\n{result}"
#                 )
#             return

#     # ============================================================
#     #                     TICKET COMMANDS
#     # ============================================================
#     # async def _handle_ticket_command(self, turn_context: TurnContext, text: str, user_id: str):
#     #     """
#     #     Handles:
#     #     - ticket create
#     #     - ticket list
#     #     - ticket status <id>
#     #     """
#     #     if user_id not in USER_TOKENS:
#     #         await turn_context.send_activity("🔐 Please login first using:\n`login email password`")
#     #         return

#     #     token = USER_TOKENS[user_id]

#     #     # --------- ticket create (start flow) ---------
#     #     if text.strip() == "ticket create":
#     #         USER_SESSIONS[user_id] = {"step": "summary"}
#     #         await turn_context.send_activity("📝 Please enter ticket **summary**:")
#     #         return

#     #     # --------- ticket list ---------
#     #     if "list" in text:
#     #         tickets, status = list_tickets(token)

#     #         if status != 200:
#     #             await turn_context.send_activity("❌ Unable to fetch tickets.")
#     #             return

#     #         ticket_list = tickets.get("results", {}).get("all_tickets", [])

#     #         if not isinstance(ticket_list, list) or not ticket_list:
#     #             await turn_context.send_activity("ℹ️ No tickets available.")
#     #             return

#     #         msg = "🎟 Your Tickets (Latest 10):\n\n"
#     #         for t in ticket_list[:10]:
#     #             msg += (
#     #                 f"🎫 {t.get('ticket_id', 'N/A')} | "
#     #                 f"{t.get('summary', 'N/A')} | "
#     #                 f"{t.get('status', 'N/A')}\n"
#     #             )

#     #         await turn_context.send_activity(msg)
#     #         return

#     #     # --------- ticket status <id> ---------
#     #     if "status" in text:
#     #         parts = text.split()
#     #         if len(parts) != 3:
#     #             await turn_context.send_activity("❌ Use: `ticket status <ticket_id>`")
#     #             return

#     #         ticket_id = parts[2]
#     #         data, status = get_ticket_status(token, ticket_id)

#     #         if status == 200 and isinstance(data, dict):
#     #             await turn_context.send_activity(
#     #                 f"🎫 Ticket ID: {data.get('ticket_id')}\n"
#     #                 f"📌 Summary: {data.get('summary')}\n"
#     #                 f"📊 Status: {data.get('status')}"
#     #             )
#     #         else:
#     #             await turn_context.send_activity("❌ Ticket not found.")
#     #         return

#     #     # --------- fallback ---------
#     #     await turn_context.send_activity(
#     #         "❌ Invalid ticket command.\n\n"
#     #         "Use:\n"
#     #         "- `ticket create`\n"
#     #         "- `ticket list`\n"
#     #         "- `ticket status <id>`"
#     #     )

#     async def _ticket_status(self, turn_context: TurnContext, text: str, token: str):
#         parts = text.split()
#         if len(parts) != 3:
#             await turn_context.send_activity("❌ Use: `ticket status <ticket_id>`")
#             return

#         ticket_id = parts[2]

#         data, status = get_ticket_status(token, ticket_id)
#         if status == 200 and isinstance(data, dict):
#             await turn_context.send_activity(
#                 f"🎫 **Ticket ID:** `{data.get('ticket_id')}`\n"
#                 f"📌 **Summary:** {data.get('summary') or data.get('title')}\n"
#                 f"📊 **Status:** {data.get('status')}\n"
#                 f"👤 **Assignee:** {data.get('assignee') or 'Unassigned'}"
#             )
#         else:
#             await turn_context.send_activity("❌ Ticket not found.")

#     async def _handle_ticket_command(self, turn_context: TurnContext, text: str):
#         user_id = turn_context.activity.from_property.id

#         if user_id not in USER_TOKENS:
#             await turn_context.send_activity("🔐 Please login first")
#             return

#         token = USER_TOKENS[user_id]

#         # ✅ CREATE TICKET
#         if text.startswith("ticket create"):
#             payload = {
#                 "ticket_id": f"BOT-{uuid.uuid4().hex[:8].upper()}",
#                 "service_domain": 1,
#                 "service_type": 1,
#                 "summary": "Bot Ticket",
#                 "description": "Created from Bot"
#             }

#             result, status = create_ticket(token, payload)

#             if status in [200, 201]:
#                 await turn_context.send_activity(
#                     f"✅ Ticket Created\n🎫 ID: {result.get('ticket_id')}"
#                 )
#             else:
#                 await turn_context.send_activity(f"❌ Ticket creation failed\n{result}")

#         # ✅ LIST TICKETS
#         elif text.startswith("ticket list"):
#             tickets, status = list_tickets(token)

#             if status != 200:
#                 await turn_context.send_activity("❌ Unable to fetch tickets")
#                 return

#             ticket_list = tickets.get("results", {}).get("all_tickets", [])

#             if not ticket_list:
#                 await turn_context.send_activity("ℹ️ No tickets found")
#                 return

#             msg = "🎟 Tickets:\n\n"
#             for t in ticket_list[:10]:
#                 msg += f"🎫 {t.get('ticket_id')} | {t.get('status')} | {t.get('assignee', 'Unassigned')}\n"

#             await turn_context.send_activity(msg)

#         # ✅ TICKET STATUS
#         elif text.startswith("ticket status"):
#             parts = text.split()

#             if len(parts) != 3:
#                 await turn_context.send_activity("❌ Use: ticket status <ticket_id>")
#                 return

#             ticket_id = parts[2]
#             data, status = get_ticket_status(token, ticket_id)

#             if status == 200:
#                 await turn_context.send_activity(
#                     f"🎫 {data.get('ticket_id')}\n"
#                     f"📊 Status: {data.get('status')}\n"
#                     f"👤 Assignee: {data.get('assignee', 'Unassigned')}"
#                 )
#             else:
#                 await turn_context.send_activity("❌ Ticket not found")

#         # ✅ ✅ ✅ ADD THIS BLOCK (ASSIGN SUPPORT)
#         elif text.startswith("ticket assign"):
#             parts = text.split()

#             if len(parts) != 4:
#                 await turn_context.send_activity(
#                     "❌ Use:\n"
#                     "`ticket assign <ticket_id> <assignee_id>`\n\n"
#                     "Example:\n"
#                     "`ticket assign BOT-19C990A3 4`"
#                 )
#                 return

#             ticket_id = parts[2]

#             try:
#                 assignee_id = int(parts[3])
#             except ValueError:
#                 await turn_context.send_activity("❌ Assignee ID must be a number")
#                 return

#             result, status = assign_ticket(token, ticket_id, assignee_id)

#             if status == 200:
#                 await turn_context.send_activity(
#                     f"✅ Ticket `{ticket_id}` assigned to user `{assignee_id}`"
#                 )
#             else:
#                 await turn_context.send_activity(
#                     f"❌ Assignment failed: {result}"
#                 )

#         # ❌ INVALID COMMAND
#         else:
#             await turn_context.send_activity(
#                 "❌ Invalid ticket command.\n\n"
#                 "Use:\n"
#                 "- ticket create\n"
#                 "- ticket list\n"
#                 "- ticket status <id>\n"
#                 "- ticket assign <id> <user_id>"
#             )


#     async def _ticket_assign(self, turn_context: TurnContext, text: str, token: str):
#         """
#         Format:
#         ticket assign <ticket_id> <assignee_id>
#         Example:
#         ticket assign BOT-19C990A3 52
#         """
#         parts = text.split()
#         if len(parts) != 4:
#             await turn_context.send_activity(
#                 "❌ Use:\n"
#                 "`ticket assign <ticket_id> <assignee_id>`\n\n"
#                 "Example:\n"
#                 "`ticket assign BOT-19C990A3 52`"
#             )
#             return

#         ticket_id = parts[2]
#         try:
#             assignee_id = int(parts[3])
#         except ValueError:
#             await turn_context.send_activity("❌ assignee_id must be a number (User ID).")
#             return

#         result, status = assign_ticket(token, ticket_id, assignee_id)

#         if status == 200:
#             await turn_context.send_activity(
#                 f"✅ Ticket `{ticket_id}` assigned successfully to user ID `{assignee_id}`."
#             )
#         elif status == 404:
#             await turn_context.send_activity("❌ Ticket or user not found.")
#         elif status == 403:
#             await turn_context.send_activity("⛔ You don't have permission to assign this ticket.")
#         else:
#             await turn_context.send_activity(f"❌ Assignment failed.\n\nDetails: `{result}`")



import uuid
import logging
from botbuilder.core import ActivityHandler, TurnContext

from .api_service import (
    get_jwt_token, create_ticket, list_tickets,
    get_ticket_status, assign_ticket
)

logger = logging.getLogger(__name__)

USER_TOKENS = {}     # ✅ JWT stored per user
USER_SESSIONS = {}   # ✅ Ticket creation flow state


class MainBot(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext):
        raw_text = (turn_context.activity.text or "").strip()
        text = raw_text.lower()
        user_id = turn_context.activity.from_property.id

        # ✅ LOGIN
        if text.startswith("login"):
            await self._handle_login(turn_context, raw_text, user_id)
            return

        # ✅ IF IN TICKET CREATION SESSION
        if user_id in USER_SESSIONS:
            await self._handle_ticket_creation_flow(turn_context, raw_text, user_id)
            return

        # ✅ REQUIRE LOGIN FOR ALL TICKET COMMANDS
        if text.startswith("ticket") and user_id not in USER_TOKENS:
            await turn_context.send_activity("🔐 Please login first.")
            return

        # ✅ TICKET COMMANDS
        if text.startswith("ticket"):
            await self._handle_ticket_command(turn_context, text, user_id)
            return

        await turn_context.send_activity(
            "✅ Bot Commands:\n"
            "login <email> <password>\n"
            "ticket create\n"
            "ticket list\n"
            "ticket status <id>\n"
            "ticket assign <id> <user_id>"
        )

    # ===================== ✅ LOGIN =====================

    async def _handle_login(self, turn_context, raw_text, user_id):
        parts = raw_text.split(maxsplit=2)
        if len(parts) != 3:
            await turn_context.send_activity(
                "❌ Use: login email password\nExample: login test@gmail.com Pass@123"
            )
            return

        token = get_jwt_token(parts[1], parts[2])
        if token:
            USER_TOKENS[user_id] = token
            await turn_context.send_activity("✅ Login Successful")
        else:
            await turn_context.send_activity("❌ Invalid Credentials")

    # ===================== ✅ TICKET CREATE FLOW =====================

    async def _handle_ticket_creation_flow(self, turn_context, raw_text, user_id):
        session = USER_SESSIONS[user_id]
        step = session["step"]

        if step == "summary":
            session["summary"] = raw_text
            session["step"] = "description"
            await turn_context.send_activity("📝 Enter description:")
            return

        if step == "description":
            session["description"] = raw_text
            session["step"] = "service_domain"
            await turn_context.send_activity("📝 Enter Service Domain ID:")
            return

        if step == "service_domain":
            try:
                session["service_domain"] = int(raw_text)
            except:
                await turn_context.send_activity("❌ Enter numeric Service Domain ID")
                return
            session["step"] = "service_type"
            await turn_context.send_activity("📝 Enter Service Type ID:")
            return

        if step == "service_type":
            try:
                session["service_type"] = int(raw_text)
            except:
                await turn_context.send_activity("❌ Enter numeric Service Type ID")
                return

            payload = {
                "ticket_id": f"BOT-{uuid.uuid4().hex[:8].upper()}",
                "summary": session["summary"],
                "description": session["description"],
                "service_domain": session["service_domain"],
                "service_type": session["service_type"],
            }

            token = USER_TOKENS[user_id]
            result, status = create_ticket(token, payload)
            del USER_SESSIONS[user_id]

            if status in [200, 201]:
                await turn_context.send_activity(
                    f"✅ Ticket Created Successfully 🎫 {result.get('ticket_id')}"
                )
            else:
                await turn_context.send_activity(f"❌ Ticket creation failed {result}")

    # ===================== ✅ TICKET COMMANDS =====================

    async def _handle_ticket_command(self, turn_context, text, user_id):
        token = USER_TOKENS[user_id]

        # ✅ START TICKET CREATE SESSION
        if text == "ticket create":
            USER_SESSIONS[user_id] = {"step": "summary"}
            await turn_context.send_activity("📝 Enter ticket summary:")
            return

        # ✅ LIST
        if text == "ticket list":
            data, status = list_tickets(token)
            if status != 200:
                await turn_context.send_activity("❌ Failed to fetch tickets")
                return

            tickets = data.get("results", {}).get("all_tickets", [])
            msg = "🎟 Tickets:\n"
            for t in tickets:   # ✅ REMOVED [:10] LIMIT
                msg += f"{t.get('ticket_id')} | {t.get('status')} | {t.get('assignee','Unassigned')}\n"

            await turn_context.send_activity(msg)
            return

        # ✅ STATUS
        if text.startswith("ticket status"):
            parts = text.split()
            data, status = get_ticket_status(token, parts[2])
            if status == 200:
                await turn_context.send_activity(
                    f"🎫 {data.get('ticket_id')}\n"
                    f"📊 {data.get('status')}\n"
                    f"👤 {data.get('assignee','Unassigned')}"
                )
            else:
                await turn_context.send_activity("❌ Ticket not found")
            return

        # ✅ ASSIGN
        if text.startswith("ticket assign"):
            parts = text.split()
            ticket_id = parts[2]
            assignee_id = int(parts[3])

            result, status = assign_ticket(token, ticket_id, assignee_id)

            if status == 200:
                await turn_context.send_activity(
                    f"✅ Ticket `{ticket_id}` assigned to user `{assignee_id}`"
                )
            elif status == 403:
                await turn_context.send_activity("⛔ Permission denied")
            else:
                await turn_context.send_activity(f"❌ Assignment failed {result}")
            return

        await turn_context.send_activity("❌ Invalid ticket command")
