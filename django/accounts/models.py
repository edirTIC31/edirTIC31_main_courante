from django.db.models import Model, OneToOneField, CharField
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


def generate_token():
    return get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')


class AuthToken(Model):
    user = OneToOneField(User)
    token = CharField(max_length=64, default=generate_token, unique=True)

    def __str__(self):
        return str(self.user)
