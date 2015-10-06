"""
WSGI config for edirtic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application

from .utils import define_default_settings


define_default_settings()

application = get_wsgi_application()
