"""
Django settings for mythology_project project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Charger les variables d'environnement (.env en local, Railway fournit des variables)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
#           BASE
# ------------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

DEBUG = os.getenv("DEBUG", "True") == "True"

# En production, Railway fournit RAILWAY_PUBLIC_DOMAIN
ALLOWED_HOSTS = [
    "*"
]

# ------------------------------
#           APPS
# ------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mythpedia',
    'widget_tweaks',
]

# ------------------------------
#         MIDDLEWARE
# ------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise pour servir les fichiers statiques en prod
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------
#         URLS / WSGI
# ------------------------------

ROOT_URLCONF = 'mythology_project.urls'
WSGI_APPLICATION = 'mythology_project.wsgi.application'

# ------------------------------
#           DATABASE
# ------------------------------

# On vérifie si Railway fournit une DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # MODE PRODUCTION (Railway)
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # MODE LOCAL (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ------------------------------
#       PASSWORD RULES
# ------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------
#       I18N / TIMEZONE
# ------------------------------

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# ------------------------------
#           STATIC & MEDIA
# ------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise : compression + hash
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------
#      AUTHENTIFICATION
# ------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'mythpedia:mythology_list'
LOGOUT_REDIRECT_URL = 'login'

# ------------------------------
#         EMAIL
# ------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER_PY')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD_PY')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL_FOR_SUGGESTIONS = EMAIL_HOST_USER
