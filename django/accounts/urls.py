from django.conf.urls import url

from django.contrib.auth.models import User


urlpatterns = [
    url(r'^login/$', 'accounts.views.login_operator', name='login'),
    url(r'^login/(?P<username>[\w.@+-]+)$', 'accounts.views.login_operator', name='login-ope'),
    url(r'^secure-login/$', 'accounts.views.login_administrator', name='login-admin'),
    url(r'^create/$', 'accounts.views.create_user', name='create-user'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
]
