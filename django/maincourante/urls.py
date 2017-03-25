from django.conf.urls import include, url

from . import views


urlpatterns = [
    # Evenement
    url(r'^$', views.EvenementListView.as_view(), name='list-evenements'),
    url(r'^add/$', views.EvenementCreateView.as_view(), name='add-evenement'),
    url(r'^(?P<evenement>[-\w]+)/live/$', views.evenement_live, name='live'),
    url(r'^(?P<evenement>[-\w]+)/report/$', views.evenement_report, name='report'),
    url(r'^(?P<evenement>[-\w]+)/manage/$', views.evenement_manage, name='manage-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/cloture/$', views.evenement_cloture, name='cloture-evenement'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/$', views.indicatif_list, name='list-indicatifs'),
    url(r'^(?P<evenement>[-\w]+)/manage/indicatifs/(?P<indicatif>[0-9]+)/delete/$', views.indicatif_delete, name='delete-indicatif'),
    # Indicatifs
    url(r'^(?P<evenement>[-\w]+)/indicatifs/$', views.indicatif_search, name='search-indicatif'),
    # Message
    url(r'^(?P<evenement>[-\w]+)/$', views.message_add, name='add-message'),
    url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/edit/$', views.message_edit, name='edit-message'),
    url(r'^(?P<evenement>[-\w]+)/message/(?P<message>[0-9]+)/delete/$', views.message_delete, name='delete-message'),
    url(r'^(?P<evenement>[-\w]+)/message/last/$', views.message_last, name='last-messages'),
    url(r'^(?P<evenement>[-\w]+)/$', views.message_edit, name='add-message'),
]
