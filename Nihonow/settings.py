"""
Django settings for Nihonow project.
"""
import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-po^n&a(ii85f@0xqb_q$*pq#3m8^qcup-pkmof7b*(9bs$%m27'

DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', '.now.sh', 'localhost']

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'treasures.apps.TreasuresConfig',
    'chatbot',
    'dojo',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.RobotsTagMiddleware',
]

ROOT_URLCONF = 'Nihonow.urls'

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

WSGI_APPLICATION = 'Nihonow.wsgi.application'
ASGI_APPLICATION = 'Nihonow.asgi.application'

# Ably API Key
ABLY_API_KEY = 'y7OU_w.GT0IiA:Caz6bpm8n4q0UhrCO8827IqtsQV_yPa7oWXYytJDX-8'

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'RZBFSItwfdWjSabpIvRJDFiEuwyoSCVL',
        'HOST': 'shortline.proxy.rlwy.net',
        'PORT': '26709',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'veerababusaviti21@gmail.com'
EMAIL_HOST_PASSWORD = 'ilkg mkaz mela bbuy'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AUTHENTICATION_BACKENDS = [
    'treasures.auth_backend.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'treasures': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "Nihonow Admin",
    "site_header": "Nihonow Admin",
    "welcome_sign": "Welcome to Nihonow Admin",
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "custom_css": "custom.css",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-red",
    "accent": "accent-red",
    "navbar": "navbar-red navbar-dark",
    "no_navigation_bar": False,
    "show_sidebar_compact": False,
    "sidebar_fixed": True,
}
