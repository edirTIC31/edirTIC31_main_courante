from django.conf.urls import include, url

from tastypie.api import Api

from .api import *
from .views import MainView

v1_api = Api(api_name='v1')
v1_api.register(MessageThreadResource())
v1_api.register(IndicatifResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    # Evenement
    url(r'^$', 'maincourante.views.evenement_list', name='list-evenements'),
    url(r'^add/$', 'maincourante.views.evenement_add', name='add-evenement'),
    url(r'^(?P<evenement>[-\w]+)/live/$', 'maincourante.views.evenement_live', name='live'),
    url(r'^(?P<evenement>[-\w]+)/report/$', 'maincourante.views.evenement_report', name='report'),
    url(r'^(?P<evenement>[-\w]+)/manage/$', 'maincourante.views.evenement_manage', name='manage-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/cloture/$', 'maincourante.views.evenement_cloture', name='cloture-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/$', 'maincourante.views.indicatif_list', name='list-indicatifs'),
    # Indicatifs
    url(r'^(?P<evenement>[-\w]+)/indicatifs/$', 'maincourante.views.indicatif_search', name='search-indicatif'),
    # Message
    url(r'^(?P<evenement>[-\w]+)/$', 'maincourante.views.message_add', name='add-message'),
    url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/edit/$', 'maincourante.views.message_edit', name='edit-message'),
    url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/delete/$', 'maincourante.views.message_delete', name='delete-message'),
    url(r'^(?P<evenement>[-\w]+)/angular/$', MainView.as_view(), name='add-message-js'),
    url(r'^(?P<evenement>[-\w]+)/$', 'maincourante.views.message_edit', name='add-message'),
]
