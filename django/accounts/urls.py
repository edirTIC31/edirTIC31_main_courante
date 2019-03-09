from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^login/$', views.login_operator, name='login'),
    url(r'^login/(?P<username>[\w.@+-]+)$', views.login_operator, name='login-ope'),
    url(r'^secure-login/$', views.login_administrator, name='login-admin'),
    url(r'^logout/$', logout, {'next_page': 'list-evenements'}, name='logout'),
]
