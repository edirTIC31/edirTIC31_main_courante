from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from .models import Message


class BaseAuthentication(Authentication):
    """
    On redéfinie la vérification de l’authentification,
    mais sans vérifier les CSRF.
    """

    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        allowed_methods = ['get', 'post']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()

    def hydrate(self, bundle):
        bundle.obj.operateur = bundle.request.user
        return bundle
