from django.conf.urls import include, url

from tastypie.api import Api

from .api import MessageResource
from .views import MainView

v1_api = Api(api_name='v1')
v1_api.register(MessageResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    # Evenement
    url(r'^$', 'maincourante.views.evenement_list', name='list-evenements'),
    url(r'^add/$', 'maincourante.views.evenement_add', name='add-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/$', 'maincourante.views.evenement_manage', name='manage-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/cloture/$', 'maincourante.views.evenement_cloture', name='cloture-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/$', 'maincourante.views.indicatif_list', name='list-indicatifs'),
    # Message
    url(r'^(?P<evenement>[-\w]+)/$', MainView.as_view(), name='add-message'),
    url(r'^(?P<evenement>[-\w]+)/report/$', 'maincourante.views.message_list', name='list-messages'),
]
