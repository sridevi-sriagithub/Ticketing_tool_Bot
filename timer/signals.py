



# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

Ticket = apps.get_model("timer", "Ticket")
SLATimer = apps.get_model("timer", "SLATimer")


# @receiver(post_save, sender=Ticket)
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


# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import pytz

Ticket = apps.get_model("timer", "Ticket")
SLATimer = apps.get_model("timer", "SLATimer")
from timer.models import WorkingHours


@receiver(post_save, sender=Ticket)
def check_ticket_working_hours(sender, instance, created, **kwargs):
    if created:
        try:
            wh = WorkingHours.objects.first()  # or filter by organisation if needed
            if not wh:
                return

            # Convert ticket creation time to IST
            ist = pytz.timezone('Asia/Kolkata')
            created_time_ist = instance.created_at.astimezone(ist)

            # Compare
            if wh.start_hour <= created_time_ist.time() <= wh.end_hour:
                instance.is_within_working_hours = True
            else:
                instance.is_within_working_hours = False

            instance.save(update_fields=["is_within_working_hours"])

        except Exception as e:
            print("⚠️ Error checking working hours:", e)



# timer/signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import Ticket
from .tasks_teams_notification import send_teams_user_notification_sync
import logging

logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Ticket)
# def ticket_assigned_notify(sender, instance, created, **kwargs):
#     print("🔔 [signal-triggered] Ticket post_save fired", flush=True)
#     print(f"[debug] Using Azure tenant: {settings.MS_TENANT_ID}", flush=True)

#     if created and instance.assignee:
#         html = f"🔔 <b>New Ticket Assigned</b><br>ID: {instance.ticket_id}<br>Title: {instance.summary or ''}"
#         print("➡️ Notification routes: PERSONAL → WEBHOOK → CHANNEL", flush=True)

#         if instance.assignee.email:
#             print(f"📤 Trying PERSONAL Teams notify → {instance.assignee.email}", flush=True)
#             try:
#                 send_teams_user_notification_sync(email=instance.assignee.email, html_message=html, tenant_id=None, ticket_id=instance.ticket_id)
#                 print("✅ Personal Teams notify sent", flush=True)
#                 return
#             except Exception as e:
#                 print(f"❌ Personal notify failed → {e}", flush=True)
#                 logger.exception("Personal Teams notify failed")

#         # webhook fallback
#         if settings.TEAMS_INCOMING_WEBHOOK:
#             try:
#                 send_teams_user_notification_sync(email=None, html_message=html, tenant_id=None, ticket_id=instance.ticket_id)
#                 print("✅ Webhook notify sent", flush=True)
#                 return
#             except Exception as e:
#                 print(f"❌ Webhook notify failed → {e}", flush=True)
#                 logger.exception("Webhook notify failed")

#         # channel fallback
#         if settings.MS_TEAM_ID and settings.MS_CHANNEL_ID:
#             try:
#                 send_teams_user_notification_sync(email=None, html_message=html, tenant_id=None, ticket_id=instance.ticket_id)
#                 print("✅ Channel notify sent", flush=True)
#                 return
#             except Exception as e:
#                 print(f"❌ Channel notify failed → {e}", flush=True)
#                 logger.exception("Channel notify failed")

#         print("⚠️ No Teams delivery method succeeded", flush=True)
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Ticket
from .tasks_teams_notification import send_teams_user_notification_sync
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Ticket)
def ticket_assigned_notify(sender, instance, created, **kwargs):
    print("🔔 [signal-triggered] Ticket post_save fired", flush=True)

    # ✅ Safely read settings (no crash in local)
    tenant_id = getattr(settings, "MS_TENANT_ID", "") or None
    webhook_url = getattr(settings, "TEAMS_INCOMING_WEBHOOK", "") or None
    team_id = getattr(settings, "MS_TEAM_ID", "") or None
    channel_id = getattr(settings, "MS_CHANNEL_ID", "") or None

    # ✅ If nothing is configured → just skip Teams notification in local
    if not any([tenant_id, webhook_url, (team_id and channel_id)]):
        print("[warning] Teams credentials/webhook not configured. Skipping Teams notification.", flush=True)
        return

    print(f"[debug] Using Azure tenant: {tenant_id}", flush=True)

    if created and instance.assignee:
        html = (
            f"🔔 <b>New Ticket Assigned</b><br>"
            f"ID: {instance.ticket_id}<br>"
            f"Title: {instance.summary or ''}"
        )
        print("➡️ Notification routes: PERSONAL → WEBHOOK → CHANNEL", flush=True)

        # PERSONAL
        if instance.assignee.email:
            print(f"📤 Trying PERSONAL Teams notify → {instance.assignee.email}", flush=True)
            try:
                send_teams_user_notification_sync(
                    email=instance.assignee.email,
                    html_message=html,
                    tenant_id=tenant_id,
                    ticket_id=instance.ticket_id,
                )
                print("✅ Personal Teams notify sent", flush=True)
                return
            except Exception as e:
                print(f"❌ Personal notify failed → {e}", flush=True)
                logger.exception("Personal Teams notify failed")

        # WEBHOOK fallback
        if webhook_url:
            try:
                send_teams_user_notification_sync(
                    email=None,
                    html_message=html,
                    tenant_id=tenant_id,
                    ticket_id=instance.ticket_id,
                )
                print("✅ Webhook notify sent", flush=True)
                return
            except Exception as e:
                print(f"❌ Webhook notify failed → {e}", flush=True)
                logger.exception("Webhook notify failed")

        # CHANNEL fallback
        if team_id and channel_id:
            try:
                send_teams_user_notification_sync(
                    email=None,
                    html_message=html,
                    tenant_id=tenant_id,
                    ticket_id=instance.ticket_id,
                )
                print("✅ Channel notify sent", flush=True)
                return
            except Exception as e:
                print(f"❌ Channel notify failed → {e}", flush=True)
                logger.exception("Channel notify failed")

        print("⚠️ No Teams delivery method succeeded", flush=True)
