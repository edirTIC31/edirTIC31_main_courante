from django.contrib.admin import site

from .models import Evenement, Indicatif, MessageEvent, MessageThread

site.register(Evenement)
site.register(Indicatif)
site.register(MessageThread)
site.register(MessageEvent)
