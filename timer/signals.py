
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from datetime import datetime, timezone

Ticket = apps.get_model("timer", "Ticket")
SLATimer = apps.get_model("timer", "SLATimer")

# @receiver(post_save, sender=Ticket)
# def ticket_status_update(sender, instance, created, **kwargs):
#     if created:
#         return

#     try:
#         sla_timer = SLATimer.objects.get(ticket=instance)
#     except SLATimer.DoesNotExist:
#         return

#     # Automatically pause or resume based on status
#     if instance.status == "Waiting for User Response":
#         # if sla_timer.sla_status != "Paused":   # Prevent re-pausing
#             sla_timer.pause_sla()
  
#     elif instance.status == "Working in Progress":
#         sla_timer.resume_sla()

#     # Prepare WebSocket payload
#     remaining = sla_timer.calculate_remaining_time()
#     payload = {
#         "type": "timer_message",
#         "action": "status_update",
#         "ticket_id": instance.ticket_id,
#         "status": instance.status,
#         "sla_status": sla_timer.sla_status,
#         "remaining_time": str(remaining).split('.')[0] if remaining else None,
#         "due_date": str(sla_timer.sla_due_date) if sla_timer.sla_due_date else None,
#         # "server_time": str(sla_timer.modified_at)
#     }

#     # Send to WebSocket group
#     channel_layer = get_channel_layer()
#     group_name = f"timer_{instance.ticket_id}"
#     async_to_sync(channel_layer.group_send)(group_name, payload)


@receiver(post_save, sender=Ticket)
def ticket_status_update(sender, instance, created, **kwargs):
    if created:
        return

    try:
        sla_timer = SLATimer.objects.get(ticket=instance)
    except SLATimer.DoesNotExist:
        return

    # Pause only if status changed to 'Waiting for User Response' and not already paused
    if instance.status == "Waiting for User Response" and sla_timer.sla_status != "Paused":
        sla_timer.pause_sla()

    # Resume only if status changed to 'Working in Progress' and currently paused
    elif instance.status == "Working in Progress" and sla_timer.sla_status == "Paused":
        sla_timer.resume_sla()

    # Calculate remaining time safely
    remaining = sla_timer.calculate_remaining_time()

    # WebSocket payload
    payload = {
        "type": "timer_message",
        "action": "status_update",
        "ticket_id": instance.ticket_id,
        "status": instance.status,
        "sla_status": sla_timer.sla_status,
        "remaining_time": str(remaining).split('.')[0] if remaining else None,
        "due_date": str(sla_timer.sla_due_date) if sla_timer.sla_due_date else None,
    }

    # Send via WebSocket
    channel_layer = get_channel_layer()
    group_name = f"timer_{instance.ticket_id}"
    async_to_sync(channel_layer.group_send)(group_name, payload)
