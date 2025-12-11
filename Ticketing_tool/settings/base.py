from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ======================
# GLOBAL CONFIGURATION
# ======================
SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-secret")
DEBUG = False  # overridden in local.py
ALLOWED_HOSTS = ["*"]

SITE_URL = env("SITE_URL", default="http://127.0.0.1:8000")

AZURE_TENANT_ID = env("AZURE_TENANT_ID", default="")
AZURE_CLIENT_ID = env("AZURE_CLIENT_ID", default="")
AZURE_CLIENT_SECRET = env("AZURE_CLIENT_SECRET", default="")
MICROSOFT_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

SENDGRID_API_KEY = env("SENDGRID_API_KEY", default="")
SENDGRID_FROM_EMAIL = env("SENDGRID_FROM_EMAIL", default="no-reply@example.com")
SENDGRID_FROM_NAME = env("SENDGRID_FROM_NAME", default="Support Team")

USE_CELERY = False       # overridden in local.py
USE_SENDGRID = False     # overridden in production.py

# ======================
# APPS
# ======================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "channels",

    "login_details",
    "timer.apps.TimerConfig",
    "solution_groups",
    "roles_creation",
    "organisation_details",
    "knowledge_article",
    "category",
    "priority",
    "personal_details",
    "project_details",
    "resolution",
    "five_notifications",
    "history",
    "services",
    "bot",
    "mptt",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "Ticketing_tool.middleware.jwt_csrf_middleware.JWTCSRFExemptMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "Ticketing_tool.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "../Frontend/build")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Ticketing_tool.wsgi.application"
ASGI_APPLICATION = "Ticketing_tool.asgi.application"

# ======================
# DATABASE
# ======================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "login_details.User"

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "../Frontend/build/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ======================
# CHANNELS
# ======================
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}

# ======================
# DRF + JWT
# ======================
from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# ======================
# CLOUDINARY
# ======================
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "dngaxesdz",
    "API_KEY": "983585494285258",
    "API_SECRET": "uYYsOTYP3tHUj_9Qa5Fn7KXH4_I",
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ======================
# CORS
# ======================
CORS_ALLOW_ALL_ORIGINS = True
