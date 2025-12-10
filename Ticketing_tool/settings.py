from pathlib import Path
import os
# import environ


# env = environ.Env()
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))



# # Base directory
# BASE_DIR = Path(__file__).resolve().parent.parent

import environ
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# ================================
# MICROSOFT GRAPH / TEAMS SETTINGS
# ================================
SITE_URL = os.getenv("SITE_URL")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

MICROSOFT_GRAPH_BASE_URL = os.getenv(
    "MICROSOFT_GRAPH_BASE_URL",
    "https://graph.microsoft.com/v1.0"
)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", default="no-reply@example.com")
SENDGRID_FROM_NAME = os.getenv("SENDGRID_FROM_NAME", default="Support Team")

# MS_CLIENT_ID = env("MS_CLIENT_ID")
# MS_CLIENT_SECRET = env("MS_CLIENT_SECRET")
# # For multi-tenant: use the tenant id of your own app for token by default,
# # but store tenant_id per-customer if you want to send from their tenant.
# MS_TENANT_ID = env("MS_TENANT_ID")  

# # Optional: target Team/Channel IDs (used when sending channel messages)
# # Add these to your .env if you plan to send to a channel via Graph
# MS_TEAM_ID = env("MS_TEAM_ID", default=None)
# MS_CHANNEL_ID = env("MS_CHANNEL_ID", default=None)

# # Optional incoming webhook (simpler channel-only delivery)
# TEAMS_INCOMING_WEBHOOK = env("TEAMS_INCOMING_WEBHOOK", default=None)

# # Default Graph scope for client credentials
# MS_GRAPH_SCOPE = "https://graph.microsoft.com/.default"

# # Token cache TTL (seconds) - keep less than token expiry (3600s)
# MS_TOKEN_CACHE_TTL = 3300

# # Step 1: Define BASE_DIR
# BASE_DIR = Path(__file__).resolve().parent.parent

# Step 2: Initialize environ and load .env
# env = environ.Env()
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# # Step 3: Read webhook
# TEAMS_INCOMING_WEBHOOK = env("TEAMS_INCOMING_WEBHOOK")



# TEAMS_INCOMING_WEBHOOK = os.environ.get("TEAMS_INCOMING_WEBHOOK")


# Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-+hi)_oc5b4amw)o&%mk__mykl=5#v9f8lyf1oy1of%7$cg3z2(')  # Use an environment variable in production
DEBUG = True
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.0.174', '192.168.0.150']
ALLOWED_HOSTS = ['*']  # Add your domain or IP address here
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# CORS - Not needed since frontend and backend are on the same domain
# Remove CORS settings
CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    "http://localhost:8000", 
     "*" # Allow requests from React frontend Add on
]

# ================= MICROSOFT / TEAMS (LOCAL DEV DEFAULTS) =================

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery_email',
    'rest_framework',
    'login_details',
    'timer.apps.TimerConfig',
    'solution_groups',
    'roles_creation',
    'organisation_details',
    'knowledge_article',
    'category',
    'priority',
    'personal_details',
    'project_details',
    'resolution',
    'five_notifications',
    'history',
    'services',
    # 'celery',
    # 'django_celery_results',
    'cloudinary_storage',
    'cloudinary',
    'mptt',
    'bot'
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "Ticketing_tool.middleware.jwt_csrf_middleware.JWTCSRFExemptMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'roles_creation.middlewares.RoleBasedAccessControlMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'Ticketing_tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../Frontend/build'),  # Add React build path here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ticketing_tool.wsgi.application'

# Database configuration (PostgreSQL)
DATABASES = {
    'default': {   
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Collect static files into STATIC_ROOT (for production use)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../Frontend/build/static'),  # Path to the React build directory
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory where static files will be collected

# Media files (for uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
AUTH_USER_MODEL = 'login_details.User'

# Email settings
EMAIL_BACKEND= 'sendgrid_backend.SendgridBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'sridevigedela05@gmail.com'
EMAIL_HOST_PASSWORD = 'ulgn jako ckts xodq'
# DEFAULT_FROM_EMAIL = "teerdavenigedela@gmail.com"

# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"


SENDGRID_SANDBOX_MODE_IN_DEBUG = env.bool("SENDGRID_SANDBOX_MODE_IN_DEBUG", default=False)
SENDGRID_ECHO_TO_STDOUT = env.bool("SENDGRID_ECHO_TO_STDOUT", default=False)

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@example.com")

# EMAIL_HOST_USER = 'teerdavenigedela@gmail.com'
# EMAIL_HOST_PASSWORD = 'vcig blpb lbdg sact'
# # Celery configuration
# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis connection URL
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Kolkata'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# #working
# CELERY_BROKER_URL = env("CELERY_BROKER_URL", default='redis://localhost:6379/0')  # Redis connection URL (assuming Redis is running locally)
# # Use an explicit result backend; prefer redis or django-db depending on your setup
# CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default='django-db')
# CELERY_ACCEPT_CONTENT = ['application/json']  # Celery task content serialization format
# CELERY_TASK_SERIALIZER = 'json'  # Task serialization format
# CELERY_RESULT_SERIALIZER = 'json'  # Result serialization format
# CELERY_TIMEZONE = 'Asia/Kolkata'
# CELERY_CACHE_BACKEND = 'django-cache'



  # Timezone for Celery tasks
#CELERY_RESULT_BACKEND = 'django-db'  # Use Django database as the result backend

# APPEND_SLASH=False
# broker_connection_retry_on_startup = 
# celery setting.
CELERY_CACHE_BACKEND = 'default'

# JWT settings for REST framework
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # ✅ correct
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

# Cloudinary settings



# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

# Security settings (for production)
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
X_FRAME_OPTIONS = 'DENY'

# Ensure your SECRET_KEY is kept secret in production (don't hardcode it in settings.py)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# SITE_URL = "http://192.168.1.12:8000/"
SITE_URL = "http://192.168.1.12:8000"

ASGI_APPLICATION = "Ticketing_tool.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # for development
    },
}


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dngaxesdz',
    'API_KEY': '983585494285258',
    'API_SECRET': 'uYYsOTYP3tHUj_9Qa5Fn7KXH4_I',
    'SECURE': True,  
    'AUTHENTICATED': False
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CORS_ALLOWED_ORIGINS = [
    "https://smba.trafficmanager.net",  # Microsoft Bot Service
    "https://eur.smba.trafficmanager.net",
    "https://api.botframework.com",
]

# CSRF exemptions for bot endpoint
CSRF_TRUSTED_ORIGINS = [
    "https://smba.trafficmanager.net",
    "https://eur.smba.trafficmanager.net",
    "https://your-domain.com",  # Replace with your actual domain
]


# ================= MICROSOFT / TEAMS (LOCAL DEV DEFAULTS) =================
# MS_TENANT_ID = os.getenv("MS_TENANT_ID", "")          # empty in local
# MS_CLIENT_ID = os.getenv("MS_CLIENT_ID", "")
# MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET", "")

# TEAMS_INCOMING_WEBHOOK = os.getenv("TEAMS_INCOMING_WEBHOOK", "")
# MS_TEAM_ID = os.getenv("MS_TEAM_ID", "")
# MS_CHANNEL_ID = os.getenv("MS_CHANNEL_ID", "")


