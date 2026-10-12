
"""
Django settings for config project.
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv


# =========================================================
# BASE DIRECTORY + ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local environment variables if .env exists.
# Vercel environment variables are configured in the dashboard.
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")

if not SECRET_KEY:
    if os.environ.get("VERCEL"):
        raise RuntimeError(
            "DJANGO_SECRET_KEY must be configured in Vercel Environment Variables."
        )
    SECRET_KEY = "django-insecure-local-development-only-change-me"

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "10.0.2.2",
    "10.53.11.125",
    "vetrix-u49j.vercel.app",
    "vetrix-u49j-3dtym01bt-asmiraseed15-1512.vercel.app",
]

# Add additional Vercel hostnames through an environment variable if needed.
extra_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS.extend(
    host.strip()
    for host in extra_hosts.split(",")
    if host.strip()
)

CSRF_TRUSTED_ORIGINS = [
    "https://vetrix-u49j.vercel.app",
    "https://vetrix-u49j-3dtym01bt-asmiraseed15-1512.vercel.app",
]

extra_csrf_origins = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS.extend(
    origin.strip()
    for origin in extra_csrf_origins.split(",")
    if origin.strip()
)

# HTTPS is used in production.
if os.environ.get("VERCEL"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",

    # VETRIX apps
    "accounts",
    "learning",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# DATABASE
# =========================================================

# Keep SQLite for local development.
# Configure a persistent production database before deploying
# if user accounts and learning progress must persist on Vercel.

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    # Requires dj-database-url and the appropriate database driver
    # to be installed in requirements.txt.
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# EMAIL CONFIGURATION
# =========================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

VETRIX_EMAIL_USER = os.environ.get(
    "VETRIX_EMAIL_USER", ""
).strip()

VETRIX_EMAIL_PASSWORD = os.environ.get(
    "VETRIX_EMAIL_PASSWORD", ""
).strip()

EMAIL_HOST_USER = VETRIX_EMAIL_USER

EMAIL_HOST_PASSWORD = VETRIX_EMAIL_PASSWORD

DEFAULT_FROM_EMAIL = VETRIX_EMAIL_USER


# =========================================================
# CORS CONFIGURATION
# =========================================================

# Configure the actual deployed frontend origin in Vercel.
# Do not leave all origins enabled in production.

CORS_ALLOW_ALL_ORIGINS = (
    os.environ.get("DJANGO_CORS_ALLOW_ALL", "False").lower()
    == "true"
)

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CORS_ALLOWED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]


# =========================================================
# DJANGO REST FRAMEWORK + JWT
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.authentication.VETRIXJWTAuthentication",
    ),
}


# =========================================================
# JWT SETTINGS
# =========================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,

    "AUTH_HEADER_TYPES": ("Bearer",),
}
