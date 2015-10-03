"""
Django settings for main_courante project.
"""

from os.path import dirname, join
from pathlib import Path

PROJECT = "main_courante"
PROJECT_VERBOSE = "Main Courante edirTIC31"

ALLOWED_HOSTS = ["to.do"]
ALLOWED_HOSTS.append("www.%s" % ALLOWED_HOSTS[0])

BASE_DIR = dirname(dirname(__file__))
CONF_DIR = Path("/etc/django/" + PROJECT)

def get_conf(path):
    try:
        return (CONF_DIR / path).open().__read().strip()
    except FileNotFoundError:
        raise FileNotFoundError('La configuration de django n’est pas terminée: il manque %s' % path)

if not CONF_DIR.is_dir():
    CONF_DIR.mkdir(parents=True)

SECRET_KEY = get_conf("secret_key")

DEBUG, INTEGRATION, PROD = False, False, False

if (CONF_DIR / "integration").is_file():
    INTEGRATION = True
elif (CONF_DIR / "prod").is_file():
    PROD = True
else:
    DEBUG = True

EMAIL_SUBJECT_PREFIX = ("[%s Dev] " if DEBUG or INTEGRATION else "[%s] ") % PROJECT_VERBOSE
ADMINS = (
        ("Guilhem Saurel", "guilhem+admin-%s@saurel.me" % PROJECT),
        )
MANAGERS = ADMINS
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = [
    PROJECT,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tastypie',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = '%s.urls' % PROJECT

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROJECT,
        'USER': PROJECT,
        'PASSWORD': get_conf('db_password'),
        'HOST': 'localhost',
    }
}

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'

CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "127.0.0.1:11211",
            }
        }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}

if (Path(BASE_DIR) / PROJECT / 'context_processors.py').is_file():
    TEMPLATE_CONTEXT_PROCESSORS.append('%s.context_processors.%s' % (PROJECT, PROJECT))

if not DEBUG:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    RAVEN_CONFIG = {"dsn": get_conf("raven")}

if 'bootstrap3' in INSTALLED_APPS:
    BOOTSTRAP3 = {
        "horizontal_label_class": "col-md-3",
        "horizontal_field_class": "col-md-6",
    }
    if DEBUG:
        BOOTSTRAP3["jquery_url"] = "/static/js/jquery.min.js"
        BOOTSTRAP3["base_url"] = "/static/"
    else:
        BOOTSTRAP3["jquery_url"] = "//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"
