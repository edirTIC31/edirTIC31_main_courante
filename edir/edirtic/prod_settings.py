"""
Django prod settings for edirtic project.
"""

from edirtic.settings import *

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

DEBUG = not (CONF_DIR / "prod").is_file()

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
