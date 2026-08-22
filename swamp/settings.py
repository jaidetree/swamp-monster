"""
Django settings for the swamp project.

Ported from the Phoenix app's config/*.exs: `lib/swamp/repo.ex` maps to
DATABASES below, `lib/swamp/mailer.ex` maps to the Anymail/Postmark
EMAIL_BACKEND config.
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-local-dev-only-do-not-use-in-production",
)

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "adminsortable2",
    "markdownify",
    "anymail",
    "content",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "swamp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "swamp.wsgi.application"

# Database — mapped from lib/swamp/repo.ex (Ecto.Adapters.Postgres). Local
# dev/CI point DATABASE_URL at the Nix-provisioned local Postgres started by
# scripts/db; production points it at Crunchy Bridge.
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://localhost:5432/swamp_dev",
    ),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files — WhiteNoise serves STATIC_ROOT (collectstatic output) at
# runtime; STATICFILES_DIRS is where the Tailwind CLI build (see
# static_src/css/app.css -> static/css/app.css) and other pre-built assets
# live before collectstatic bakes them into STATIC_ROOT at image build time.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media — owner-uploaded Work/WorkImage/etc files. Local filesystem storage
# only (the "default" entry in STORAGES above); the concrete Cloudflare R2
# backend lands in a later ticket (16-media-storage-cloudflare-r2).
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-markdownify — renders `content` app Markdown fields (Work.description,
# WorkImage.caption, ...) via the `|markdownify` template filter. A restrictive
# allowed-tags whitelist: enough for prose (paragraphs, emphasis, links, lists)
# with no raw HTML/script/embed surface for owner-authored content.
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            "a",
            "b",
            "blockquote",
            "em",
            "i",
            "li",
            "ol",
            "p",
            "strong",
            "ul",
        ],
        "WHITELIST_ATTRS": ["href", "title"],
        "WHITELIST_PROTOCOLS": ["http", "https", "mailto"],
    },
}

# Email — mapped from lib/swamp/mailer.ex (Swoosh.Mailer). Config only: no
# Postmark API key is required to wire the setting itself, only to send.
EMAIL_BACKEND = "anymail.backends.postmark.EmailBackend"
ANYMAIL = {
    "POSTMARK_SERVER_TOKEN": env("POSTMARK_SERVER_TOKEN", default=""),
}
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@swamp-monster-leather.com")

# Where contact-form notification emails are sent — the Swamp Monster inbox.
CONTACT_NOTIFICATION_EMAIL = env(
    "CONTACT_NOTIFICATION_EMAIL", default="hello@swamp-monster-leather.com"
)
