"""
Django settings for mythology_project project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv # <<< AJOUTER CET IMPORT

# Charger les variables d'environnement depuis le fichier .env
# Assurez-vous que ce fichier est à la racine de votre projet (même niveau que manage.py)
# et qu'il n'est PAS versionné (ajoutez-le à .gitignore)
load_dotenv() # <<< APPELER CETTE FONCTION AU DÉBUT

BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-8)-220u69!9+=o+p(bj07__5zlj+#wu5g0uger8po5c+)ys$5x')

# Debug setting - False in production
DEBUG = os.getenv('DEBUG', 'True').lower() in ['true', '1', 'yes']

# Allowed hosts for production
ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'mythpedia',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mythology_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mythology_project.wsgi.application'

# Database configuration
# Check if we're in production (Railway) and use PostgreSQL, otherwise use SQLite
if 'RAILWAY_ENVIRONMENT' in os.environ or 'DATABASE_URL' in os.environ:
    # Production database (PostgreSQL on Railway)
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
    except ImportError:
        # Fallback if dj_database_url is not installed
        import urllib.parse
        db_url = os.environ.get('DATABASE_URL', '')
        if db_url:
            parsed = urllib.parse.urlparse(db_url)
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': parsed.path[1:],  # Remove leading slash
                    'USER': parsed.username,
                    'PASSWORD': parsed.password,
                    'HOST': parsed.hostname,
                    'PORT': parsed.port or 5432,
                }
            }
        else:
            # If DATABASE_URL is not set, use SQLite as fallback
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
else:
    # Development database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'mythpedia:mythology_list'
LOGOUT_REDIRECT_URL = 'login'

# --- CONFIGURATION EMAIL POUR GMAIL ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Charger les identifiants depuis les variables d'environnement (fichier .env)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER_PY') 
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD_PY')

# Vérification (optionnelle mais utile pour le débogage)
if not EMAIL_HOST_USER:
    print("ATTENTION: La variable d'environnement EMAIL_HOST_USER_PY n'est pas définie dans le fichier .env !")
if not EMAIL_HOST_PASSWORD:
    print("ATTENTION: La variable d'environnement EMAIL_HOST_PASSWORD_PY n'est pas définie dans le fichier .env !")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL_FOR_SUGGESTIONS = EMAIL_HOST_USER

# --- CONFIGURATION POUR DJANGO REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
