from django.forms.models import modelform_factory

from django.contrib.auth.models import User


CreateUserForm = modelform_factory(User, fields=['username'])
