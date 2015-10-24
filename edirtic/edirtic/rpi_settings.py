from .settings import *

from pathlib import Path


CONF_DIR = Path("/etc/django/" + PROJECT)

def get_conf(path):
    try:
        return (CONF_DIR / path).open().read().strip()
    except FileNotFoundError:
        raise FileNotFoundError('La configuration de django n’est pas terminée: il manque %s' % path)

SECRET_KEY = get_conf('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/srv/www/edirtic/static/'
STATIC_URL = '/static/'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/srv/www/edirtic/log/debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
