from django.conf.urls import url
#from django.conf import settings

#from django.contrib.auth.models import User

from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^logout/$', auth_views.logout, {'next_page': 'list-evenements'}, name='logout'),
    url(r'^login/$', views.login, name='login'),
    #url(r'^login/$', 'accounts.views.login_operator', name='login-passless'),
    url(r'^login/operator/(?P<username>[\w.@+-]+)$', views.login_operator, name='login-operator'),
    url(r'^login/admin/$', views.login_administrator, name='login-admin'),
]

#if settings.PASSLESS_LOGIN:
#    urlpatterns += [
#    ]
#else:
#    urlpatterns += [
#        url(r'^login/$', auth_views.login, {'template_name': 'accounts/login_with_password.html'}, name='login'),
#    ]
