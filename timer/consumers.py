

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.apps import apps
# # from timer.models import SLATimer

# class TimerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
#         self.group_name = f"timer_{self.ticket_id}"
#         # sla_timer = await sync_to_async(self.get_sla_timer)()

        
#         # Join group
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#         # Get models dynamically
#         Ticket = apps.get_model('timer', 'Ticket')
#         SLATimer = apps.get_model('timer', 'SLATimer')

#         try:
#             ticket = await sync_to_async(Ticket.objects.get)(ticket_id=self.ticket_id)
#             sla_timer = await sync_to_async(SLATimer.objects.get)(ticket=ticket)
#         except Ticket.DoesNotExist:
#             await self.close()
#             return
#         except SLATimer.DoesNotExist:
#             sla_timer = None
    

#         await self.send(text_data=json.dumps({
#             "action": "timer_init",
#             "ticket_id": ticket.ticket_id,
#             "status": ticket.status,
#             "sla_status": sla_timer.sla_status if sla_timer else None,
#             "remaining_time": str(sla_timer.calculate_remaining_time()) if sla_timer else None,
#             "due_date": str(sla_timer.sla_due_date) if sla_timer else None,
#             # "server_time": str(sla_timer.modified_at),
#         }))
        
    

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get("action")

#         if action == "update_status":
#             await self.update_status(data)

#     async def update_status(self, data):
#         Ticket = apps.get_model('timer', 'Ticket')
#         SLATimer = apps.get_model('timer', 'SLATimer')

#         try:
#             ticket = await sync_to_async(Ticket.objects.get)(ticket_id=self.ticket_id)
#         except Ticket.DoesNotExist:
#             return

#         new_status = data.get("status")
#         if not new_status:
#             return

#         # Update ticket status
#         ticket.status = new_status
#         await sync_to_async(ticket.save)()

#         # Handle SLA timer
#         try:
#             sla_timer = await sync_to_async(SLATimer.objects.get)(ticket=ticket)
#         except SLATimer.DoesNotExist:
#             sla_timer = None

#         action_type = "status_update"
#         if sla_timer:
#             if new_status.lower() == "waiting for user response":
#                 await sync_to_async(sla_timer.pause_sla)()
#                 action_type = "timer_paused"
#             elif new_status.lower() in ["working in progress", "in progress"]:
#                 await sync_to_async(sla_timer.resume_sla)()
#                 action_type = "timer_resumed"
#             elif new_status.lower() in ["resolved", "closed"]:
#                 await sync_to_async(sla_timer.stop_sla)()
#                 action_type = "timer_stopped"

#         # Broadcast updated SLA info
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "timer_message",
#                 "action": action_type,
#                 "ticket_id": ticket.ticket_id,
#                 "status": ticket.status,
#                 "sla_status": sla_timer.sla_status if sla_timer else None,
#                 "remaining_time": str(sla_timer.calculate_remaining_time()) if sla_timer else None,
#                 "due_date": str(sla_timer.sla_due_date) if sla_timer else None
#             }
#         )
       

#     async def timer_message(self, event):
#         await self.send(text_data=json.dumps(event))


# import json
# import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.apps import apps
# from django.utils import timezone

# class TimerConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
#         self.group_name = f"timer_{self.ticket_id}"

#         # Join group
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#         # Send initial timer info
#         await self.send_initial_timer()

#         # Start heartbeat loop for live remaining_time updates
#         self.timer_task = asyncio.create_task(self.timer_loop())

#     async def disconnect(self, close_code):
#         # Cancel the heartbeat loop
#         if hasattr(self, "timer_task"):
#             self.timer_task.cancel()
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get("action")

#         if action == "update_status":
#             await self.update_status(data)

#     # ------------------------------
#     # Helper: Send initial timer snapshot
#     async def send_initial_timer(self):
#         Ticket = apps.get_model('timer', 'Ticket')
#         SLATimer = apps.get_model('timer', 'SLATimer')

#         try:
#             ticket = await sync_to_async(Ticket.objects.get)(ticket_id=self.ticket_id)
#             sla_timer = await sync_to_async(SLATimer.objects.get)(ticket=ticket)
#         except Ticket.DoesNotExist:
#             await self.close()
#             return
#         except SLATimer.DoesNotExist:
#             sla_timer = None

#         await self.send(text_data=json.dumps({
#             "action": "timer_init",
#             "ticket_id": ticket.ticket_id,
#             "status": ticket.status,
#             "sla_status": sla_timer.sla_status if sla_timer else None,
#             "remaining_time": str(sla_timer.calculate_remaining_time()) if sla_timer else None,
#             "due_date": str(sla_timer.sla_due_date) if sla_timer else None,
#         }))

#     # ------------------------------
#     # Heartbeat: send remaining_time every second
#     async def timer_loop(self):
#         Ticket = apps.get_model('timer', 'Ticket')
#         SLATimer = apps.get_model('timer', 'SLATimer')

#         while True:
#             try:
#                 ticket = await sync_to_async(Ticket.objects.get)(ticket_id=self.ticket_id)
#                 sla_timer = await sync_to_async(SLATimer.objects.get)(ticket=ticket)
#             except (Ticket.DoesNotExist, SLATimer.DoesNotExist):
#                 break

#             await self.channel_layer.group_send(
#                 self.group_name,
#                 {
#                     "type": "timer_message",
#                     "action": "timer_update",
#                     "ticket_id": ticket.ticket_id,
#                     "status": ticket.status,
#                     "sla_status": sla_timer.sla_status,
#                     "remaining_time": str(sla_timer.calculate_remaining_time()),
#                     "due_date": str(sla_timer.sla_due_date),
#                 }
#             )
#             await asyncio.sleep(1)  # 1-second updates

#     # ------------------------------
#     # Update ticket status and handle SLA actions
#     async def update_status(self, data):
#         Ticket = apps.get_model('timer', 'Ticket')
#         SLATimer = apps.get_model('timer', 'SLATimer')

#         try:
#             ticket = await sync_to_async(Ticket.objects.get)(ticket_id=self.ticket_id)
#         except Ticket.DoesNotExist:
#             return

#         new_status = data.get("status")
#         if not new_status:
#             return

#         # Update ticket status
#         ticket.status = new_status
#         await sync_to_async(ticket.save)()

#         # Handle SLA timer
#         try:
#             sla_timer = await sync_to_async(SLATimer.objects.get)(ticket=ticket)
#         except SLATimer.DoesNotExist:
#             sla_timer = None

#         action_type = "status_update"
#         if sla_timer:
#             if new_status.lower() == "waiting for user response":
#                 await sync_to_async(sla_timer.pause_sla)()
#                 action_type = "timer_paused"
#             elif new_status.lower() in ["working in progress", "in progress"]:
#                 await sync_to_async(sla_timer.resume_sla)()
#                 action_type = "timer_resumed"
#             elif new_status.lower() in ["resolved", "closed"]:
#                 await sync_to_async(sla_timer.stop_sla)()
#                 action_type = "timer_stopped"

#         # Broadcast immediate update
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "timer_message",
#                 "action": action_type,
#                 "ticket_id": ticket.ticket_id,
#                 "status": ticket.status,
#                 "sla_status": sla_timer.sla_status if sla_timer else None,
#                 "remaining_time": str(sla_timer.calculate_remaining_time()) if sla_timer else None,
#                 "due_date": str(sla_timer.sla_due_date) if sla_timer else None
#             }
#         )

#     # ------------------------------
#     # Receive broadcast messages from group
#     async def timer_message(self, event):
#         await self.send(text_data=json.dumps(event))


import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.apps import apps
from django.utils import timezone

class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
            self.group_name = f"timer_{self.ticket_id}"

            # Add to channel layer group
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

            # Send initial timer data
            await self.send_initial_timer()

            # Start heartbeat loop
            self.timer_task = asyncio.create_task(self.timer_loop())

        except Exception as e:
            print("WebSocket connect error:", e)
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "timer_task"):
            self.timer_task.cancel()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get("action")
            if action == "update_status":
                await self.update_status(data)
        except Exception as e:
            print("WebSocket receive error:", e)

    # ------------------------------
    # Helper: Safe reverse relation access
    @sync_to_async
    def get_ticket(self):
        Ticket = apps.get_model('timer', 'Ticket')
        return Ticket.objects.get(ticket_id=self.ticket_id)

    @sync_to_async
    def get_sla_timer(self, ticket):
        SLATimer = apps.get_model('timer', 'SLATimer')
        try:
            return ticket.sla_timers  # match your related_name
        except SLATimer.DoesNotExist:
            return None
    # ------------------------------
    # Initial timer snapshot
    async def send_initial_timer(self):
        try:
            ticket = await self.get_ticket()
            sla_timer = await self.get_sla_timer(ticket)
        except Exception as e:
            print("send_initial_timer error:", e)
            return  # Do NOT close, just skip sending initial data

        await self.send(text_data=json.dumps({
            "action": "timer_init",
            "ticket_id": ticket.ticket_id,
            "status": ticket.status,
            "sla_status": sla_timer.sla_status,
            "remaining_time": str(sla_timer.calculate_remaining_time()),
            "due_date": str(sla_timer.sla_due_date),
        }))

    # ------------------------------
    # Heartbeat loop: sends updates every second
    async def timer_loop(self):
        while True:
            try:
                ticket = await self.get_ticket()
                sla_timer = await self.get_sla_timer(ticket)

                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "timer_message",
                        "action": "timer_update",
                        "ticket_id": ticket.ticket_id,
                        "status": ticket.status,
                        "sla_status": sla_timer.sla_status,
                        "remaining_time": str(sla_timer.calculate_remaining_time()),
                        "due_date": str(sla_timer.sla_due_date),
                    }
                )
            except Exception as e:
                print("timer_loop error:", e)
            await asyncio.sleep(1)

    # ------------------------------
    # Status update handler
    async def update_status(self, data):
        new_status = data.get("status")
        if not new_status:
            return

        try:
            ticket = await self.get_ticket()
            ticket.status = new_status
            await sync_to_async(ticket.save)()
            sla_timer = await self.get_sla_timer(ticket)
        except Exception as e:
            print("update_status error:", e)
            return

        action_type = "status_update"
        if sla_timer:
            if new_status.lower() == "waiting for user response":
                await sync_to_async(sla_timer.pause_sla)()
                action_type = "timer_paused"
            elif new_status.lower() in ["working in progress", "in progress"]:
                await sync_to_async(sla_timer.resume_sla)()
                action_type = "timer_resumed"
            elif new_status.lower() in ["resolved", "closed"]:
                await sync_to_async(sla_timer.stop_sla)()
                action_type = "timer_stopped"

        try:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "timer_message",
                    "action": action_type,
                    "ticket_id": ticket.ticket_id,
                    "status": ticket.status,
                    "sla_status": sla_timer.sla_status,
                    "remaining_time": str(sla_timer.calculate_remaining_time()),
                    "due_date": str(sla_timer.sla_due_date),
                }
            )
        except Exception as e:
            print("group_send error in update_status:", e)

    # ------------------------------
    # Broadcast handler
    async def timer_message(self, event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            print("timer_message send error:", e)

