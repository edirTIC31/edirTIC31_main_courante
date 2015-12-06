from django.conf.urls import url

from django.contrib.auth.models import User


urlpatterns = [
    url(r'^login/$', 'accounts.views.login', name='login'),
    url(r'^login/(?P<username>[\w.@+-]+)$', 'accounts.views.passless_login', name='passless-login'),
    url(r'^create/$', 'accounts.views.create_user', name='create-user'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
]
