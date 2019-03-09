from django.conf import settings
from django.conf.urls import include, url

from tastypie.api import Api

from . import views
from .api import EvenementResource, IndicatifResource, MessageResource

v1_api = Api(api_name='v1')
v1_api.register(EvenementResource())
v1_api.register(IndicatifResource())
v1_api.register(MessageResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    # Evenement
    url(r'^$', views.EvenementListView.as_view(), name='list-evenements'),
    url(r'^add/$', views.EvenementCreateView.as_view(), name='add-evenement'),
    url(r'^(?P<evenement>[-\w]+)/report/$', views.evenement_report, name='report'),
    url(r'^(?P<evenement>[-\w]+)/manage/$', views.evenement_manage, name='manage-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/cloture/$', views.evenement_cloture, name='cloture-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/$', views.indicatif_list, name='list-indicatifs'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/(?P<indicatif>[0-9]+)/delete/$',
        views.indicatif_delete,
        name='delete-indicatif'),
    # Indicatifs
    url(r'^(?P<evenement>[-\w]+)/indicatifs/$', views.indicatif_search, name='search-indicatif'),
]

if settings.ANGULAR:
    urlpatterns += [
        # Live
        url(r'^(?P<evenement>[-\w]+)/live/$', views.evenement_live_angular, name='live'),
        # Message
        url(r'^(?P<evenement>[-\w]+)/$', views.message_angular, name='add-message'),
    ]
else:
    urlpatterns += [
        # Live
        url(r'^(?P<evenement>[-\w]+)/live/$', views.evenement_live, name='live'),
        # Message
        url(r'^(?P<evenement>[-\w]+)/$', views.message_add, name='add-message'),
        url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/edit/$', views.message_edit, name='edit-message'),
        url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/delete/$',
            views.message_delete,
            name='delete-message'),
        url(r'^(?P<evenement>[-\w]+)/message/last/$', views.message_last, name='last-messages'),
    ]
