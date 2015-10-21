from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from .models import *


__all__ = ['MessageThreadResource', 'IndicatifResource']


class BaseAuthentication(Authentication):
    """
    On redéfinie la vérification de l’authentification,
    mais sans vérifier les CSRF.
    """

    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()


class IndicatifResource(ModelResource):

    class Meta:
        queryset = Indicatif.objects.all()
        allowed_methods = ['get']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()


class MessageThreadResource(ModelResource):

    class Meta:
        queryset = MessageThread.objects.all()
        allowed_methods = ['get', 'post', 'put']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate(self, bundle):
        # Include the request IP in the bundle.
        if bundle.obj.parent:
            bundle.data['parent'] = int(bundle.obj.parent.id)
        return bundle

    def hydrate(self, bundle):
        bundle.obj.operateur = bundle.request.user
        bundle.obj.evenement = Evenement.objects.get(clos=False)
        if 'parent' in bundle.data:
            bundle.obj.parent = MessageThread.objects.get(id=int(bundle.data['parent']))
        return bundle
