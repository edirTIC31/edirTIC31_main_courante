"""
WSGI config for edirtic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from os.path import dirname, abspath, join, isfile

from django.core.wsgi import get_wsgi_application


BASE_DIR = dirname(abspath(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edirtic.local_settings" if isfile(join(BASE_DIR, 'local_settings.py')) else "edirtic.settings")

application = get_wsgi_application()
