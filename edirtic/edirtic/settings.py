"""
Django settings for edirtic project.
"""

from os.path import dirname, abspath, join, isfile

PROJECT = "edirtic"
PROJECT_VERBOSE = "Main Courante edirTIC31"

BASE_DIR = dirname(dirname(abspath(__file__)))
SECRET_KEY = '11+)$2+ulb9nn)x4(g4wedajo4=!olbn%_d8ebqo!xw(j!r8&1'
DEBUG = not isfile('/etc/django/%s/prod' % PROJECT)

ALLOWED_HOSTS = []
EMAIL_SUBJECT_PREFIX = ("[%s Dev] " if DEBUG else "[%s] ") % PROJECT_VERBOSE

INSTALLED_APPS = [
    PROJECT,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maincourante',
    'tastypie',
    'bootstrap3',
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static_dest') if DEBUG else '/var/www/%s/static_dest' % PROJECT
LOGIN_REDIRECT_URL = '/'

BOOTSTRAP3 = {
    'jquery_url': STATIC_URL + 'js/jquery.min.js',
    'base_url': STATIC_URL,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-6',
}

if not DEBUG:
    from pathlib import Path

    ALLOWED_HOSTS.append("edirtic.saurel.me")
    ALLOWED_HOSTS.append("www.%s" % ALLOWED_HOSTS[-1])

    CONF_DIR = Path("/etc/django/" + PROJECT)

    def get_conf(path):
        try:
            return (CONF_DIR / path).open().read().strip()
        except FileNotFoundError:
            raise FileNotFoundError('La configuration de django n’est pas terminée: il manque %s' % path)

    if not CONF_DIR.is_dir():
        CONF_DIR.mkdir(parents=True)

    SECRET_KEY = get_conf("secret_key")

    ADMINS = (
            ("Guilhem Saurel", "guilhem+admin-%s@saurel.me" % PROJECT),
            )
    MANAGERS = ADMINS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': PROJECT,
            'USER': PROJECT,
            'PASSWORD': get_conf('db_password'),
            'HOST': 'localhost',
        }
    }

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
