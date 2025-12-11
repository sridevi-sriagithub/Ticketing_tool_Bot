from .base import *

DEBUG = True

SITE_URL = "http://127.0.0.1:8000"

# Local Email – Console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Enable Celery (Redis localhost)
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Skip Teams notifications locally
TEAMS_ENABLED = False
