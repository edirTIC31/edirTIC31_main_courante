from django.conf.urls import include, url
from django.contrib import admin

from .views import logout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout$', logout, name='logout'),
    url(r'^', include('maincourante.urls')),
]
