from django.contrib.admin import site

from .models import Evenement, Indicatif, MessageThread, MessageVersion

site.register(Evenement)
site.register(Indicatif)
site.register(MessageThread)
site.register(MessageVersion)
