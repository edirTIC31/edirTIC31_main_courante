from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_operator, name='login'),
    path('login/<username>', views.login_operator, name='login-ope'),
    path('secure-login/', views.LoginAdministrator.as_view(), name='login-admin'),
    path('logout/', LogoutView.as_view(next_page='list-evenements'), name='logout'),
]
