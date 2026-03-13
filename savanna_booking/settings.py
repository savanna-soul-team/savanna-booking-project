from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent


# Restore these lines
SECRET_KEY = config('SECRET_KEY', default='your-very-secret-key-here')
DEBUG = config('DEBUG', cast=bool, default=True) # Set default to True for development
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='localhost,127.0.0.1')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_daraja',
    'core',
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
]

ROOT_URLCONF = 'savanna_booking.urls'

TEMPLATES = [{
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
}]

WSGI_APPLICATION = 'savanna_booking.wsgi.application'

# ── Database ──────────────────────────────────────────────────
# Development: SQLite
# Production: PostgreSQL (set DATABASE_URL in .env)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Africa/Nairobi'
USE_I18N      = True
USE_TZ        = True

STATIC_URL    = '/static/'
STATIC_ROOT   = BASE_DIR / 'staticfiles'
MEDIA_URL     = '/media/'
MEDIA_ROOT    = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'

AUTH_USER_MODEL      = 'core.User'
LOGIN_URL            = '/login/'
LOGIN_REDIRECT_URL   = '/'
LOGOUT_REDIRECT_URL  = '/'

# ── Security (production only) ────────────────────────────────
if not DEBUG:
    SECURE_HSTS_SECONDS            = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD            = True
    SECURE_SSL_REDIRECT            = True
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    SECURE_BROWSER_XSS_FILTER      = True
    SECURE_CONTENT_TYPE_NOSNIFF    = True
    X_FRAME_OPTIONS                = 'DENY'

# ── M-Pesa (django-daraja) ────────────────────────────────────
# ── M-Pesa (django-daraja) ────────────────────────────────────
MPESA_ENVIRONMENT     = config('MPESA_ENV', default='sandbox')
# ── M-Pesa (django-daraja) ────────────────────────────────────
MPESA_ENVIRONMENT       = config('MPESA_ENV', default='sandbox')
MPESA_CONSUMER_KEY      = config('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET   = config('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE         = config('MPESA_SHORTCODE')
MPESA_EXPRESS_SHORTCODE = config('MPESA_EXPRESS_SHORTCODE')
MPESA_PASSKEY           = config('MPESA_PASSKEY')

# UNIVERSAL CALLBACK LOGIC
if DEBUG:
    # Locally: Use the Ngrok URL defined in your .env
    MPESA_CALLBACK_URL = config('MPESA_CALLBACK_URL')
else:
    # Production: Automatically build the URL using your live domain
    # Ensure you add DOMAIN_NAME (e.g., https://savanna-booking.com) to your production env
    DOMAIN_NAME = config('DOMAIN_NAME') 
    MPESA_CALLBACK_URL = f"{DOMAIN_NAME.rstrip('/')}/mpesa/callback/"

# ── Email (optional — for booking confirmations) ──────────────
EMAIL_BACKEND = config('EMAIL_BACKEND',
                       default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST     = config('EMAIL_HOST', default='')
EMAIL_PORT     = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS  = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER     = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL', default='noreply@savannabooking.com')