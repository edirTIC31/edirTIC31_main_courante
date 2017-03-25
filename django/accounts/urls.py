from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views


urlpatterns = [
    url(r'^logout/$', auth_views.logout, {'next_page': 'list-evenements'}, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/operator/(?P<username>[\w.@+-]+)$', views.login_operator, name='login-operator'),
    url(r'^login/admin/$', views.login_administrator, name='login-admin'),
]
