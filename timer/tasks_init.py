"""
Celery tasks for the Ticketing app.
Imports the Teams notification task from tasks_teams_notification module.
"""
from .tasks_teams_notification import send_teams_user_notification

__all__ = ['send_teams_user_notification']
