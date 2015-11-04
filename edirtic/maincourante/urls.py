from django.conf.urls import include, url

from tastypie.api import Api

from .api import EvenementResource, IndicatifResource, MessageResource
from .views import EvenementCreateView, EvenementListView

v1_api = Api(api_name='v1')
v1_api.register(EvenementResource())
v1_api.register(IndicatifResource())
v1_api.register(MessageResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    # Evenement
    url(r'^$', EvenementListView.as_view(), name='list-evenements'),
    url(r'^add/$', EvenementCreateView.as_view(), name='add-evenement'),
    url(r'^(?P<evenement>[-\w]+)/live/$', 'maincourante.views.evenement_live', name='live'),
    url(r'^(?P<evenement>[-\w]+)/report/$', 'maincourante.views.evenement_report', name='report'),
    url(r'^(?P<evenement>[-\w]+)/manage/$', 'maincourante.views.evenement_manage', name='manage-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/cloture/$', 'maincourante.views.evenement_cloture', name='cloture-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/$', 'maincourante.views.indicatif_list', name='list-indicatifs'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/(?P<indicatif>[0-9]+)/delete/$', 'maincourante.views.indicatif_delete', name='delete-indicatif'),
    # Indicatifs
    url(r'^(?P<evenement>[-\w]+)/indicatifs/$', 'maincourante.views.indicatif_search', name='search-indicatif'),
    # Message
    url(r'^(?P<evenement>[-\w]+)/$', 'maincourante.views.message_add', name='add-message'),
    url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/edit/$', 'maincourante.views.message_edit', name='edit-message'),
    url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/delete/$', 'maincourante.views.message_delete', name='delete-message'),
    url(r'^(?P<evenement>[-\w]+)/message/last/$', 'maincourante.views.message_last', name='last-messages'),
    url(r'^(?P<evenement>[-\w]+)/angular/$', 'maincourante.views.message_angular', name='message-angular'),
    url(r'^(?P<evenement>[-\w]+)/$', 'maincourante.views.message_edit', name='add-message'),
]
