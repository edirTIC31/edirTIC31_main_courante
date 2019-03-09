from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    url(r'^login/$', views.login_operator, name='login'),
    url(r'^login/(?P<username>[\w.@+-]+)$', views.login_operator, name='login-ope'),
    url(r'^secure-login/$', views.login_administrator, name='login-admin'),
    url(r'^logout/$', LogoutView.as_view(next_page='list-evenements'), name='logout'),
]
