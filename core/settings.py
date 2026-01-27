from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-kiosk-dev-key'
DEBUG = True
ALLOWED_HOSTS = ['*'] # Liberado para acessar via IP no Tablet

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'survey', # <--- NOSSO APP
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # <--- APONTANDO PARA A PASTA TEMPLATES
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

# --- CONFIGURAÇÃO CELERY ---
# settings.py

# Se estiver rodando via Docker, o host é 'redis'. Se for local, é 'localhost'
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
# Configuração para rodar LOCAL no Windows:
#CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
#CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# DICA: Para funcionar tanto no seu PC (sem docker full) quanto no docker da pessoa
# Você pode usar: os.environ.get('REDIS_HOST', 'localhost') se quiser ser sofisticado.

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo'
CSRF_TRUSTED_ORIGINS = [
    'https://raiox.virtu-intelligence.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]