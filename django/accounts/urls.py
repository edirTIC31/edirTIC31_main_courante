from django.conf.urls import url
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': 'list-evenements'}, name='logout'),
]

if settings.PASSLESS_LOGIN:
    urlpatterns += [
        url(r'^login/$', 'accounts.views.login_operator', name='login'),
        url(r'^login/(?P<username>[\w.@+-]+)$', 'accounts.views.login_operator', name='login-ope'),
        url(r'^secure-login/$', 'accounts.views.login_administrator', name='login-admin'),
    ]
else:
    urlpatterns += [
        url(r'^login/$', auth_views.login, {'template_name': 'accounts/login_with_password.html'}, name='login'),
    ]
