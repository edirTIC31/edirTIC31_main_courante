from django.contrib.admin import ModelAdmin, site

from .models import *


site.register(Evenement)
site.register(Indicatif)
site.register(MessageThread)
site.register(MessageEvent)
