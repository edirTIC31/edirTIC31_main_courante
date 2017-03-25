from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings


def create_readonly_user(sender, **kwargs):
    from django.contrib.auth.models import User
    from accounts.models import AuthToken
    user, _ = User.objects.get_or_create(username=settings.RO_USERNAME, first_name='Invité')
    AuthToken.objects.get_or_create(user=user)


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        post_migrate.connect(create_readonly_user, sender=self)
