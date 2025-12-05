from __future__ import annotations
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from .utils.teams import TeamsService, TeamsServiceError
import sys

logger = get_task_logger(__name__)


# @shared_task(bind=True, max_retries=3, default_retry_delay=60)
# def send_teams_user_notification(self, email: str | None, html_message: str, tenant_id: str | None = None, ticket_id: str | None = None):
#     """
#     Try to send a personal Teams message via Graph (app-only).
#     If that fails and a webhook is configured, fall back to incoming webhook.
#     Retries on failure and saves delivery status to Notification model for tracking.
#     """
#     from .models import Notification, Ticket

#     # Print to console for real-time visibility
#     print(f"\n{'='*80}")
#     print(f"[TEAMS NOTIFICATION] Starting send to {email or 'webhook'}")
#     print(f"[TEAMS NOTIFICATION] Ticket ID: {ticket_id}")
#     print(f"{'='*80}\n")
#     sys.stdout.flush()

#     ticket = None
#     if ticket_id:
#         try:
#             ticket = Ticket.objects.get(ticket_id=ticket_id)
#             print(f"[TEAMS NOTIFICATION] Found ticket: {ticket.ticket_id}")
#         except Ticket.DoesNotExist:
#             print(f"[TEAMS NOTIFICATION] WARNING: Ticket {ticket_id} not found")
#             logger.warning(f"Ticket {ticket_id} not found for notification tracking")

#     # Create notification record
#     notif = None
#     try:
#         notif = Notification.objects.create(
#             ticket=ticket,
#             recipient_email=email,
#             method='graph_1to1' if email else 'webhook',
#             status='queued'
#         )
#         print(f"[TEAMS NOTIFICATION] Created notification record (ID: {notif.id}, Status: queued)")
#     except Exception as e:
#         print(f"[TEAMS NOTIFICATION] ERROR: Failed to create Notification record: {e}")
#         logger.exception("Failed to create Notification record: %s", e)

#     if not email:
#         # Nothing to do for personal send — try webhook instead
#         print(f"[TEAMS NOTIFICATION] No email provided; attempting webhook fallback")
#         logger.debug("No email provided for personal Teams notify; attempting webhook fallback")
#         try:
#             result = TeamsService.send_webhook_message(html_message)
#             if notif:
#                 notif.status = 'sent'
#                 notif.response = {'method': 'webhook', 'result': result}
#                 notif.save()
#             print(f"[TEAMS NOTIFICATION] ✅ SUCCESS: Webhook message sent successfully")
#             print(f"{'='*80}\n")
#             sys.stdout.flush()
#             logger.info("Webhook message sent successfully")
#             return result
#         except Exception as e:
#             print(f"[TEAMS NOTIFICATION] ❌ FAILED: Webhook send failed: {e}")
#             print(f"{'='*80}\n")
#             sys.stdout.flush()
#             logger.exception("Webhook fallback failed: %s", e)
#             if notif:
#                 notif.status = 'failed'
#                 notif.error_message = str(e)
#                 notif.save()
#             raise

#     try:
#         print(f"[TEAMS NOTIFICATION] Attempting personal 1:1 send to {email}")
#         logger.info("Sending Teams 1:1 to %s", email)
#         resp = TeamsService.notify_user_by_email(email, html_message, tenant_id=tenant_id)
#         message_id = resp.get('id') if isinstance(resp, dict) else None
#         if notif:
#             notif.status = 'sent'
#             notif.message_id = message_id
#             notif.response = resp if isinstance(resp, dict) else {'result': str(resp)}
#             notif.save()
#         print(f"[TEAMS NOTIFICATION] ✅ SUCCESS: Teams 1:1 sent to {email}")
#         print(f"[TEAMS NOTIFICATION] Message ID: {message_id}")
#         print(f"{'='*80}\n")
#         sys.stdout.flush()
#         logger.info("Teams 1:1 sent to %s (message_id: %s)", email, message_id)
#         return resp
#     except Exception as exc:
#         print(f"[TEAMS NOTIFICATION] ⚠️ Personal 1:1 send failed for {email}: {exc}")
#         logger.exception("Personal Teams send failed for %s: %s", email, exc)

#         # Try webhook fallback if configured
#         webhook = getattr(settings, 'TEAMS_INCOMING_WEBHOOK', None)
#         if webhook:
#             print(f"[TEAMS NOTIFICATION] Attempting webhook fallback")
#             try:
#                 logger.info("Attempting webhook fallback for %s", email)
#                 result = TeamsService.send_webhook_message(html_message, webhook_url=webhook)
#                 if notif:
#                     notif.status = 'sent'
#                     notif.method = 'webhook'
#                     notif.response = {'fallback': True, 'result': result}
#                     notif.save()
#                 print(f"[TEAMS NOTIFICATION] ✅ SUCCESS: Webhook fallback succeeded for {email}")
#                 print(f"{'='*80}\n")
#                 sys.stdout.flush()
#                 logger.info("Webhook fallback succeeded for %s", email)
#                 return result
#             except Exception as e:
#                 print(f"[TEAMS NOTIFICATION] ❌ Webhook fallback also failed: {e}")
#                 logger.exception("Webhook fallback also failed for %s: %s", email, e)
#                 if notif:
#                     notif.status = 'failed'
#                     notif.error_message = f"1:1 failed: {str(exc)}; webhook fallback also failed: {str(e)}"
#                     notif.save()
#         else:
#             print(f"[TEAMS NOTIFICATION] No webhook configured for fallback")

#         # Retries will be attempted by Celery
#         if notif:
#             notif.status = 'retrying'
#             notif.save()

#         print(f"[TEAMS NOTIFICATION] Celery will retry (attempt {self.request.retries + 1}/3)")
#         try:
#             raise self.retry(exc=exc)
#         except Exception:
#             # If retry raises (max retries exceeded), re-raise original
#             print(f"[TEAMS NOTIFICATION] ❌ FINAL FAILURE: Max retries exceeded for {email}")
#             print(f"[TEAMS NOTIFICATION] Error: {exc}")
#             print(f"{'='*80}\n")
#             sys.stdout.flush()
#             if notif:
#                 notif.status = 'failed'
#                 notif.error_message = str(exc)
#                 notif.save()
#             raise

# timer/teams_notify.py
import logging
from django.conf import settings
# from .teams_service import TeamsService, TeamsServiceError
from .models import Notification, Ticket

logger = logging.getLogger(__name__)

def send_teams_user_notification_sync(*, email: str | None = None, html_message: str, tenant_id: str | None = None, ticket_id: str | None = None):
    """
    Synchronous Teams notification wrapper (keyword-only).
    Use this from synchronous code (signals/views).
    """
    # Resolve ticket (best-effort)
    ticket = None
    if ticket_id:
        ticket = Ticket.objects.filter(ticket_id=ticket_id).first()

    # Create Notification record (best-effort)
    notif = None
    try:
        notif = Notification.objects.create(
            ticket=ticket,
            recipient_email=email,
            method='graph_1to1' if email else 'webhook',
            status='queued'
        )
    except Exception:
        logger.exception("Failed to create Notification record (non-fatal)")

    # 1) Personal send via Graph (preferred)
    if email:
        try:
            logger.info("Attempting Teams 1:1 send to %s", email)
            resp = TeamsService.notify_user_by_email(user_email=email, html_message=html_message, tenant_id=tenant_id)
            if notif:
                notif.status = 'sent'
                notif.response = resp
                notif.save()
            return resp
        except Exception as e:
            logger.exception("Teams 1:1 send failed for %s: %s", email, e)
            if notif:
                notif.status = 'failed'
                notif.error_message = str(e)
                notif.save()
            # fall through to webhook fallback

    # 2) Webhook fallback
    webhook = getattr(settings, "TEAMS_INCOMING_WEBHOOK", None)
    if webhook:
        try:
            logger.info("Attempting webhook fallback")
            res = TeamsService.send_webhook_message(html_message, webhook_url=webhook)
            if notif:
                notif.status = 'sent'
                notif.method = 'webhook'
                notif.response = {'result': res}
                notif.save()
            return res
        except Exception as e:
            logger.exception("Webhook fallback failed: %s", e)
            if notif:
                notif.status = 'failed'
                notif.error_message = f"Webhook fallback failed: {e}"
                notif.save()

    # 3) Channel fallback
    team_id = getattr(settings, "MS_TEAM_ID", None)
    channel_id = getattr(settings, "MS_CHANNEL_ID", None)
    if team_id and channel_id:
        try:
            logger.info("Attempting channel fallback")
            res = TeamsService.send_channel_message(team_id, channel_id, html_message, tenant_id=tenant_id)
            if notif:
                notif.status = 'sent'
                notif.method = 'channel'
                notif.response = res
                notif.save()
            return res
        except Exception as e:
            logger.exception("Channel fallback failed: %s", e)
            if notif:
                notif.status = 'failed'
                notif.error_message = f"Channel fallback failed: {e}"
                notif.save()

    # All failed
    raise Exception("All Teams notification methods failed.")


# Optional Celery task wrapper (only if you want queued delivery).
# If you run on Windows and don't want Celery, you can ignore/delete this part.
try:
    from celery import shared_task

    @shared_task(bind=True, max_retries=3, default_retry_delay=60)
    def send_teams_user_notification_task(self, email=None, html_message=None, tenant_id=None, ticket_id=None):
        """
        Celery task wrapper. It accepts positional/keyword args (Celery-style).
        Internally delegates to the sync function using keyword arguments.
        Use .delay(...) to queue.
        """
        try:
            # Ensure we call sync function with keyword-only style to avoid positional duplicates
            return send_teams_user_notification_sync(email=email, html_message=html_message, tenant_id=tenant_id, ticket_id=ticket_id)
        except Exception as exc:
            logger.exception("Celery send_teams_user_notification_task failed: %s", exc)
            # retry if you want
            try:
                raise self.retry(exc=exc)
            except Exception:
                # bubbling out if retry exhausted
                raise

except Exception:
    # celery not available; that's fine — only sync function will be used.
    send_teams_user_notification_task = None
