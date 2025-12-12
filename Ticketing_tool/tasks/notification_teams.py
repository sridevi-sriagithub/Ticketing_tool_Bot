# Ticketing_tool/tasks/notification_teams.py
from celery import shared_task
import logging
from Ticketing_tool.services.teams_notify import send_teams_notification

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_teams_notification_task(self, user_email, title, message, link):
    """
    Celery Task wrapper for Teams Notification.
    Automatically retries if Microsoft Graph is busy or returns errors.
    """
    try:
        send_teams_notification(user_email, title, message, link)
        logger.info("Teams Notification Task SUCCESS → %s", user_email)

    except Exception as exc:
        logger.error("Teams Notification FAILED → retrying… (%s)", exc)
        raise self.retry(exc=exc)


    