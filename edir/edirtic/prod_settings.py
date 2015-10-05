"""
Django settings for maincourante project.
"""

from edirtic.settings import *

from os.path import dirname, abspath, join
from pathlib import Path



ALLOWED_HOSTS = ["to.do"]
ALLOWED_HOSTS.append("www.%s" % ALLOWED_HOSTS[0])

CONF_DIR = Path("/etc/django/" + PROJECT)

def get_conf(path):
    try:
        return (CONF_DIR / path).open().read().strip()
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



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROJECT,
        'USER': PROJECT,
        'PASSWORD': get_conf('db_password'),
        'HOST': 'localhost',
    }
}



LOGIN_REDIRECT_URL = '/'

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

BOOTSTRAP3["jquery_url"] = "//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"


