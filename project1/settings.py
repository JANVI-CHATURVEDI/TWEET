import os
from pathlib import Path

# BASE_DIR for project root
BASE_DIR = Path(__file__).resolve().parent.parent
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# Security
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['tweet-hveo.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_browser_reload',
    'tailwind',
    'theme',
    'tweet.apps.TweetConfig',
    'widget_tweaks', 
]

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ["127.0.0.1"]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # must be above others
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'project1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project1.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JS)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # dev files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    # collectstatic target
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user-uploaded)
MEDIA_ROOT = '/mnt/media/'  # path on Render persistent disk
MEDIA_URL = '/media/'

# Login redirects
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/tweet/' 
LOGOUT_REDIRECT_URL = '/tweet/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------
# Production-related tips
# ----------------------
# 1. On Render, make sure you add a build command in dashboard:
#    pip install -r requirements.txt && python manage.py collectstatic --noinput
# 2. All user-uploaded files (avatars, tweet photos) must use MEDIA_URL and MEDIA_ROOT.
#    WhiteNoise only serves STATIC_ROOT, not media files.
# 3. In templates:
#    - Static files: {% load static %} <img src="{% static 'images/logo.png' %}" />
#    - Media files: <img src="{{ tweet.user.profile.avatar.url }}" />
