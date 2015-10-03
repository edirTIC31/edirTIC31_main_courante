from django.contrib.admin import ModelAdmin, site

from .models import Evenement, Message

site.register(Evenement)
site.register(Message)
