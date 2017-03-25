from django.contrib.admin import site

from .models import AuthToken

site.register(AuthToken)
