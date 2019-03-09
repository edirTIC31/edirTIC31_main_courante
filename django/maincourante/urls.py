from django.conf import settings
from django.urls import include, path

from tastypie.api import Api

from . import views
from .api import EvenementResource, IndicatifResource, MessageResource

v1_api = Api(api_name='v1')
v1_api.register(EvenementResource())
v1_api.register(IndicatifResource())
v1_api.register(MessageResource())

urlpatterns = [
    path('api/', include(v1_api.urls)),
    # Evenement
    path('', views.EvenementListView.as_view(), name='list-evenements'),
    path('add/', views.EvenementCreateView.as_view(), name='add-evenement'),
    path('<slug:evenement>/report/', views.evenement_report, name='report'),
    path('<slug:evenement>/manage/', views.evenement_manage, name='manage-evenement'),
    path('<slug:evenement>/manage/cloture/', views.evenement_cloture, name='cloture-evenement'),
    path('<slug:evenement>/manage/indicatifs/', views.indicatif_list, name='list-indicatifs'),
    path('<slug:evenement>/manage/indicatifs/<int:indicatif>/delete', views.indicatif_delete, name='delete-indicatif'),
    # Indicatifs
    path('<slug:evenement>/indicatifs/', views.indicatif_search, name='search-indicatif'),
]

if settings.ANGULAR:
    urlpatterns += [
        # Live
        path('<slug:evenement>/live/', views.evenement_live_angular, name='live'),
        # Message
        path('<slug:evenement>/', views.message_angular, name='add-message'),
    ]
else:
    urlpatterns += [
        # Live
        path('<slug:evenement>/live/', views.evenement_live, name='live'),
        # Message
        path('<slug:evenement>/', views.message_add, name='add-message'),
        path('<slug:evenement>/message/<int:message>/edit/', views.message_edit, name='edit-message'),
        path('<slug:evenement>/message/<int:message>/delete/', views.message_delete, name='delete-message'),
        path('<slug:evenement>/message/last/', views.message_last, name='last-messages'),
    ]
