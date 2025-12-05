



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





# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Ticket   # your Ticket model
# from .utils.teams import send_simple_teams_message


# @receiver(post_save, sender=Ticket)
# def send_ticket_notifications(sender, instance, created, **kwargs):
#     if created:
#         # New ticket notification
#         message = (
#             f"📩 New Ticket Created\n"
#             f"ID: {instance.ticket_id}\n"
#             f"Title: {instance.summary}"
#         )
#         send_simple_teams_message(message)
#         print("TEAMS SIGNAL TRIGGERED: Created =", created)


#     else:
#         # Ticket update notification
#         message = (
#             f"🔄 Ticket Updated\n"
#             f"ID: {instance.ticket_id}\n"
#             f"Status: {instance.status}"
#         )
#         send_simple_teams_message(message)



from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from timer.utils.teams import TeamsService
from timer.tasks import send_teams_user_notification
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
# @receiver(post_save, sender=Ticket)
# def ticket_assigned_notify(sender, instance, created, **kwargs):
#     # adjust condition for assignment change
#     if instance.is_assigned and instance.just_assigned():  # implement just_assigned
#         try:
#             html = f"🔔 <b>Ticket Assigned</b><br>ID: {instance.ticket_id}<br>Title: {instance.ticket_title}"
#             TeamsService.notify_user_by_email(instance.assigned_to.email, html, tenant_id=instance.org.tenant_id)
#         except Exception as e:
#             # log error - don't crash the save flow
#             logger.exception("Teams notification failed: %s", e)



# @receiver(post_save, sender=Ticket)
# def ticket_assigned_notify(sender, instance, created, **kwargs):
#     try:
#         if created and instance.assignee:
#             html = (
#                 f"🔔 <b>New Ticket Assigned</b><br>"
#                 f"ID: {instance.ticket_id}<br>"
#                 f"Title: {instance.summary}"
#             )
#             TeamsService.notify_user_by_email(
#                 instance.assignee.email,
#                 html,
#                 tenant_id=instance.ticket_organization.tenant_id if instance.ticket_organization else None
#             )
#             return
        
#         if instance.is_assignee_changed() and instance.assignee:
#             html = (
#                 f"🔔 <b>Ticket Re-assigned</b><br>"
#                 f"ID: {instance.ticket_id}<br>"
#                 f"Title: {instance.summary}"
#             )
#             TeamsService.notify_user_by_email(
#                 instance.assignee.email,
#                 html,
#                 tenant_id=instance.ticket_organization.tenant_id if instance.ticket_organization else None
#             )

#     except Exception as e:
#         logger.exception("Teams notification failed: %s", e)

# @receiver(post_save, sender=Ticket)
# def ticket_assigned_notify(sender, instance, created, **kwargs):
#     try:
#         if created and instance.assignee:
#             html = (
#                 f"🔔 <b>New Ticket Assigned</b><br>"
#                 f"ID: {instance.ticket_id}<br>"
#                 f"Title: {instance.summary}"
#             )
#             # Try personal 1:1 (Graph) if we have an assignee email
#             sent = False
#             if getattr(instance, 'assignee', None) and getattr(instance.assignee, 'email', None):
#                 try:
#                     # Enqueue asynchronous send to avoid blocking the request/DB save
#                     send_teams_user_notification.delay(
#                         instance.assignee.email,
#                         html,
#                         instance.ticket_organization.tenant_id if instance.ticket_organization else None,
#                         instance.ticket_id
#                     )
#                     # immediate developer-facing console feedback (request process)
#                     print(f"[teams-signal] enqueued personal notify -> email={instance.assignee.email} ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception:
#                     logger.exception("Enqueue personal Teams notify failed, will try webhook/channel for ticket %s", instance.ticket_id)

#             # If not sent via personal message, try incoming webhook if configured
#             if not sent and getattr(settings, 'TEAMS_INCOMING_WEBHOOK', None):
#                 try:
#                     # enqueue webhook send as well so it's executed in background
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print(f"[teams-signal] enqueued webhook notify -> ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception:
#                     logger.exception("Enqueue webhook send failed for ticket %s", instance.ticket_id)

#             # Final fallback: channel send if team+channel IDs are configured
#             if not sent and getattr(settings, "MS_TEAM_ID", None) and getattr(settings, "MS_CHANNEL_ID", None):
#                 try:
#                     # channel send may require Graph and is run async as well
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print(f"[teams-signal] enqueued channel notify -> team={settings.MS_TEAM_ID} channel={settings.MS_CHANNEL_ID} ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception:
#                     logger.exception("Enqueue channel send failed for ticket %s", instance.ticket_id)

#             if not sent:
#                 logger.warning("No Teams delivery method succeeded for ticket %s (no webhook, no team/channel, or all methods failed)", instance.ticket_id)
#                 print(f"[teams-signal] no teams delivery method available for ticket={instance.ticket_id}", flush=True)
#             return
        
#         if instance.is_assignee_changed() and instance.assignee:
#             html = (
#                 f"🔔 <b>Ticket Re-assigned</b><br>"
#                 f"ID: {instance.ticket_id}<br>"
#                 f"Title: {instance.summary}"
#             )
#             sent = False
#             if getattr(instance, 'assignee', None) and getattr(instance.assignee, 'email', None):
#                 try:
#                     send_teams_user_notification.delay(
#                         instance.assignee.email,
#                         html,
#                         instance.ticket_organization.tenant_id if instance.ticket_organization else None,
#                         instance.ticket_id
#                     )
#                     print(f"[teams-signal] enqueued personal notify (reassign) -> email={instance.assignee.email} ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception:
#                     logger.exception("Enqueue personal Teams notify failed on reassignment for ticket %s", instance.ticket_id)

#             if not sent and getattr(settings, 'TEAMS_INCOMING_WEBHOOK', None):
#                 try:
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print(f"[teams-signal] enqueued webhook notify (reassign) -> ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception:
#                     logger.exception("Enqueue webhook send failed on reassignment for ticket %s", instance.ticket_id)

#             if not sent and getattr(settings, "MS_TEAM_ID", None) and getattr(settings, "MS_CHANNEL_ID", None):
#                 try:
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print(f"[teams-signal] enqueued channel notify (reassign) -> team={settings.MS_TEAM_ID} channel={settings.MS_CHANNEL_ID} ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception:
#                     logger.exception("Enqueue channel send failed on reassignment for ticket %s", instance.ticket_id)

#             if not sent:
#                 logger.warning("No Teams delivery method succeeded for reassigned ticket %s", instance.ticket_id)
#                 print(f"[teams-signal] no teams delivery method available for reassigned ticket={instance.ticket_id}", flush=True)
#         print("mail sent")
#     except Exception as e:
#         logger.exception("Teams notification failed: %s", e)


# @receiver(post_save, sender=Ticket)
# def ticket_assigned_notify(sender, instance, created, **kwargs):
#     print("🔔 [signal-triggered] Ticket post_save fired", flush=True)
#     print(f"[debug] created={created}", flush=True)
#     print(f"[debug] assignee={instance.assignee}", flush=True)
#     print(f"[debug] is_assignee_changed={instance.is_assignee_changed()}", flush=True)


#     try:
#         # Ticket Created + Assigned
#         if created and instance.assignee:
#             print(f"🆕 [ticket-created] Ticket ID={instance.ticket_id} assigned to {instance.assignee}", flush=True)

#             html = (
#                 f"🔔 <b>New Ticket Assigned</b><br>"
#                 f"ID: {instance.ticket_id}<br>"
#                 f"Title: {instance.summary}"
#             )

#             sent = False

#             print("➡️ Checking notification routes (personal → webhook → channel)...", flush=True)

#             # 1️⃣ PERSONAL TEAMS MESSAGE
#             if getattr(instance.assignee, 'email', None):
#                 print(f"📤 Trying PERSONAL Teams notify → {instance.assignee.email}", flush=True)
#                 try:
#                     send_teams_user_notification(
#                         instance.assignee.email,
#                         html,
#                         # instance.ticket_organization.tenant_id if instance.ticket_organization else None,
#                         instance.ticket_id
#                     )
#                     print(f"✅ [success] Personal notify enqueued → email={instance.assignee.email}", flush=True)
#                     sent = True
#                 except Exception as err:
#                     print(f"❌ [error] Personal Teams notify FAILED → {err}", flush=True)
#                     logger.exception("Enqueue personal Teams notify failed")

#             # 2️⃣ TEAMS WEBHOOK
#             if not sent and getattr(settings, 'TEAMS_INCOMING_WEBHOOK', None):
#                 print("📤 Trying WEBHOOK notify...", flush=True)
#                 try:
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print(f"✅ [success] Webhook notify enqueued → ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception as err:
#                     print(f"❌ [error] Webhook notify FAILED → {err}", flush=True)
#                     logger.exception("Webhook send failed")

#             # 3️⃣ TEAMS CHANNEL SEND
#             if not sent and getattr(settings, "MS_TEAM_ID", None) and getattr(settings, "MS_CHANNEL_ID", None):
#                 print(f"📤 Trying CHANNEL notify → Team={settings.MS_TEAM_ID}, Channel={settings.MS_CHANNEL_ID}", flush=True)
#                 try:
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print(f"✅ [success] Channel notify enqueued → ticket={instance.ticket_id}", flush=True)
#                     sent = True
#                 except Exception as err:
#                     print(f"❌ [error] Channel notify FAILED → {err}", flush=True)
#                     logger.exception("Channel send failed")

#             # FINAL CHECK
#             if not sent:
#                 print("⚠️ [warning] No Teams delivery method succeeded", flush=True)
#                 logger.warning("No Teams delivery method succeeded for ticket %s", instance.ticket_id)

#             print("✅ [END] Ticket create signal successfully executed.\n", flush=True)
#             return

#         # Ticket Re-assigned
#         if instance.is_assignee_changed() and instance.assignee:
#             print(f"🔄 [ticket-reassign] Ticket ID={instance.ticket_id} reassigned to {instance.assignee}", flush=True)

#             html = (
#                 f"🔔 <b>Ticket Re-assigned</b><br>"
#                 f"ID: {instance.ticket_id}<br>"
#                 f"Title: {instance.summary}"
#             )

#             sent = False
#             print("➡️ Checking notification routes (personal → webhook → channel)...", flush=True)

#             # 1️⃣ PERSONAL
#             if getattr(instance.assignee, 'email', None):
#                 print(f"📤 Trying PERSONAL Teams notify → {instance.assignee.email}", flush=True)
#                 try:
#                     send_teams_user_notification.delay(
#                         instance.assignee.email,
#                         html,
#                         instance.ticket_organization.tenant_id if instance.ticket_organization else None,
#                         instance.ticket_id
#                     )
#                     print(f"✅ [success] Personal notify enqueued (reassign)", flush=True)
#                     sent = True
#                 except Exception as err:
#                     print(f"❌ Personal notify failed → {err}", flush=True)

#             # 2️⃣ WEBHOOK
#             if not sent and getattr(settings, 'TEAMS_INCOMING_WEBHOOK', None):
#                 print("📤 Trying WEBHOOK notify (reassign)...", flush=True)
#                 try:
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print("✅ [success] Webhook notify enqueued (reassign)", flush=True)
#                     sent = True
#                 except Exception as err:
#                     print(f"❌ Webhook notify failed → {err}", flush=True)

#             # 3️⃣ CHANNEL SEND
#             if not sent and getattr(settings, "MS_TEAM_ID", None) and getattr(settings, "MS_CHANNEL_ID", None):
#                 print(f"📤 Trying CHANNEL notify (reassign)", flush=True)
#                 try:
#                     send_teams_user_notification.delay(None, html, None, instance.ticket_id)
#                     print("✅ [success] Channel notify enqueued (reassign)", flush=True)
#                     sent = True
#                 except Exception as err:
#                     print(f"❌ Channel notify failed → {err}", flush=True)

#             if not sent:
#                 print(f"⚠️ [warning] No Teams method succeeded (reassign)", flush=True)

#         print("📧 mail sent (end of signal)", flush=True)

#     except Exception as e:
#         print(f"🔥 [fatal-error] Teams notification failed → {e}", flush=True)
#         logger.exception("Teams notification failed")

# # timer/signals.py
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.conf import settings
# from .models import Ticket
# from .tasks_teams_notification import send_teams_user_notification_sync  # <- explicitly import the sync function
# import logging

# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Ticket)
# def ticket_assigned_notify(sender, instance, created, **kwargs):
#     print("🔔 [signal-triggered] Ticket post_save fired", flush=True)
#     print(f"[debug] Using Azure tenant: {settings.MS_TENANT_ID}", flush=True)

#     tenant = None  # default to settings.MS_TENANT_ID in TeamsService if None

#     if created and instance.assignee:
#         html = (
#             f"🔔 <b>New Ticket Assigned</b><br>"
#             f"ID: {instance.ticket_id}<br>"
#             f"Title: {instance.summary or ''}"
#         )

#         print("➡️ Notification routes: PERSONAL → WEBHOOK → CHANNEL", flush=True)

#         # PERSONAL
#         if instance.assignee.email:
#             print(f"📤 Trying PERSONAL Teams notify → {instance.assignee.email}", flush=True)
#             try:
#                 # ALWAYS call sync function with keyword-only args
#                 send_teams_user_notification_sync(
#                     email=instance.assignee.email,
#                     html_message=html,
#                     tenant_id=tenant,
#                     ticket_id=instance.ticket_id
#                 )
#                 print("✅ Personal Teams notify sent", flush=True)
#                 return
#             except Exception as e:
#                 print(f"❌ Personal notify failed → {e}", flush=True)
#                 logger.exception("Personal Teams notify failed")

#         # WEBHOOK fallback
#         if settings.TEAMS_INCOMING_WEBHOOK:
#             print("📤 Trying WEBHOOK notify...", flush=True)
#             try:
#                 send_teams_user_notification_sync(
#                     email=None,
#                     html_message=html,
#                     tenant_id=tenant,
#                     ticket_id=instance.ticket_id
#                 )
#                 print("✅ Webhook notify sent", flush=True)
#                 return
#             except Exception as e:
#                 print(f"❌ Webhook notify failed → {e}", flush=True)
#                 logger.exception("Webhook notify failed")

#         # CHANNEL fallback
#         if settings.MS_TEAM_ID and settings.MS_CHANNEL_ID:
#             print("📤 Trying CHANNEL notify...", flush=True)
#             try:
#                 send_teams_user_notification_sync(
#                     email=None,
#                     html_message=html,
#                     tenant_id=tenant,
#                     ticket_id=instance.ticket_id
#                 )
#                 print("✅ Channel notify sent", flush=True)
#                 return
#             except Exception as e:
#                 print(f"❌ Channel notify failed → {e}", flush=True)
#                 logger.exception("Channel notify failed")

#         print("⚠️ No Teams delivery method succeeded", flush=True)


# timer/signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import Ticket
from .tasks_teams_notification import send_teams_user_notification_sync
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Ticket)
def ticket_assigned_notify(sender, instance, created, **kwargs):
    print("🔔 [signal-triggered] Ticket post_save fired", flush=True)
    print(f"[debug] Using Azure tenant: {settings.MS_TENANT_ID}", flush=True)

    if created and instance.assignee:
        html = f"🔔 <b>New Ticket Assigned</b><br>ID: {instance.ticket_id}<br>Title: {instance.summary or ''}"
        print("➡️ Notification routes: PERSONAL → WEBHOOK → CHANNEL", flush=True)

        if instance.assignee.email:
            print(f"📤 Trying PERSONAL Teams notify → {instance.assignee.email}", flush=True)
            try:
                send_teams_user_notification_sync(email=instance.assignee.email, html_message=html, tenant_id=None, ticket_id=instance.ticket_id)
                print("✅ Personal Teams notify sent", flush=True)
                return
            except Exception as e:
                print(f"❌ Personal notify failed → {e}", flush=True)
                logger.exception("Personal Teams notify failed")

        # webhook fallback
        if settings.TEAMS_INCOMING_WEBHOOK:
            try:
                send_teams_user_notification_sync(email=None, html_message=html, tenant_id=None, ticket_id=instance.ticket_id)
                print("✅ Webhook notify sent", flush=True)
                return
            except Exception as e:
                print(f"❌ Webhook notify failed → {e}", flush=True)
                logger.exception("Webhook notify failed")

        # channel fallback
        if settings.MS_TEAM_ID and settings.MS_CHANNEL_ID:
            try:
                send_teams_user_notification_sync(email=None, html_message=html, tenant_id=None, ticket_id=instance.ticket_id)
                print("✅ Channel notify sent", flush=True)
                return
            except Exception as e:
                print(f"❌ Channel notify failed → {e}", flush=True)
                logger.exception("Channel notify failed")

        print("⚠️ No Teams delivery method succeeded", flush=True)
