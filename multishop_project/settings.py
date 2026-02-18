"""
====================================================
MULTISHOP - E-Commerce Website
Settings File
====================================================
Project  : MultiShop
Author   : Adarsh Pathak
GitHub   : AdarshPathak9628
Tech     : Django 6.0, MySQL, Bootstrap, Python 3.13
====================================================
"""

from pathlib import Path
from django.contrib.messages import constants as messages

# ============================================================
# BASE DIRECTORY
# This gives us the root path of the whole project
# All other paths are built from this
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY SETTINGS
# WARNING: Keep SECRET_KEY secret in production!
# WARNING: Set DEBUG = False when going live!
# ============================================================
SECRET_KEY = 'django-insecure-my$!!!51hl1n*x9i*6z(fw8x7n2=q88%rl1*c^u9ci-q^-)2pn'

DEBUG = True  # ← Change to False when going live

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # ← Add your domain when live


# ============================================================
# INSTALLED APPS
# All Django built-in apps + our custom app 'store'
# ============================================================
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our custom app
    # OLD NAME: 'products' — not descriptive
    # NEW NAME: 'store' — clearly means e-commerce store
    'store',
]


# ============================================================
# MIDDLEWARE
# These run on every request/response
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',        # ← Protects forms from attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URL CONFIGURATION
# Main urls.py is inside 'multishop' folder
# ============================================================
ROOT_URLCONF = 'multishop_project.urls'

# ⚠️ NOTE: Change this if your project folder name is different


# ============================================================
# TEMPLATES CONFIGURATION
# Django will look for HTML files in 'templates' folder
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # ← This tells Django where to find HTML templates
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

WSGI_APPLICATION = 'multishop_project.wsgi.application'


# ============================================================
# DATABASE — MySQL Configuration
#  OLD: SQLite (not good for real projects)
#  NEW: MySQL (professional, fast, reliable)
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # ← Using MySQL not SQLite
        'NAME': 'multishop_db',                # ← Database name
        'USER': 'root',                        # ← MySQL username
        'PASSWORD': 'Root@12',                 # ← Your MySQL password
        'HOST': '127.0.0.1',                   # ← Local computer
        'PORT': '3306',                        # ← MySQL default port
        'OPTIONS': {
            'charset': 'utf8mb4',              # ← Supports all characters & emojis
        },
    }
}


# ============================================================
# PASSWORD VALIDATION
# These rules apply when user creates a password
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        # Password cannot be similar to username/email
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Password must be at least 8 characters
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        # Password cannot be a common word like "password123"
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Password cannot be all numbers
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================================
# INTERNATIONALIZATION
# OLD: UTC timezone — wrong for India
# NEW: Asia/Kolkata — correct for India
# ============================================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'  # ← Indian Standard Time (IST)

USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC FILES — CSS, JavaScript, Images
# These are YOUR design files (Bootstrap, custom CSS etc)
# ============================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']   # ← Where static files are stored
STATIC_ROOT = BASE_DIR / 'staticfiles'     # ← Where collected for production


# ============================================================
# MEDIA FILES — Uploaded by Users
# Product images, category images, vendor images
# ============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'            # ← Where uploaded files are saved


# ============================================================
# AUTHENTICATION SETTINGS
# Where to redirect if user is not logged in
# ============================================================
LOGIN_URL = '/login/'                      # ← Go here if not logged in
LOGIN_REDIRECT_URL = '/'                   # ← Go here after login
LOGOUT_REDIRECT_URL = '/'                  # ← Go here after logout


# ============================================================
# MESSAGE TAGS — For Flash Messages (success, error etc)
# Used in templates like: {% if messages %}
# ============================================================
MESSAGE_TAGS = {
    messages.DEBUG:   'debug',
    messages.INFO:    'info',
    messages.SUCCESS: 'success',    # ← Green message
    messages.WARNING: 'warning',    # ← Yellow message
    messages.ERROR:   'danger',     # ← Red message (Bootstrap class)
}


# ============================================================
# DEFAULT PRIMARY KEY
# All models use BigAutoField (better than AutoField)
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'