from django.http import Http404
from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource, Resource
from tastypie.constants import ALL


from .models import Evenement, Indicatif, MessageThread, MessageVersion

__all__ = ['IndicatifResource', 'MessageResource', 'EvenementResource']


class BaseAuthentication(Authentication):
    """
    On redéfinie la vérification de l’authentification,
    mais sans vérifier les CSRF.
    À virer si un token CSRF peut être récupéré coté js.
    """

    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()


class EvenementResource(ModelResource):

    class Meta:
        resource_name = 'evenement'
        queryset = Evenement.objects.all()
        allowed_methods = ['get']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()


class IndicatifResource(ModelResource):
    evenement = fields.ForeignKey(EvenementResource, 'evenement')

    class Meta:
        queryset = Indicatif.objects.all()
        allowed_methods = ['get']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'evenement': ['exact'],
        }


class Message:

    def __init__(self, thread):
        self.pk = thread.pk
        self.evenement = thread.evenement
        self.sender = thread.expediteur.nom
        self.receiver = thread.destinataire.nom
        self.body = thread.corps
        self.timestamp = thread.cree


class MessageResource(Resource):

    id = fields.IntegerField(attribute='pk')
    evenement = fields.ToOneField(EvenementResource, 'evenement')
    sender = fields.CharField(attribute='sender')
    receiver = fields.CharField(attribute='receiver')
    body = fields.CharField(attribute='body')
    timestamp = fields.DateTimeField(attribute='timestamp')

    class Meta:
        resource_name = 'message'
        collection_name = 'messages'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'delete']
        authentication = BaseAuthentication()
        authorization = DjangoAuthorization()

    def detail_uri_kwargs(self, bundle):
        return bundle.data

    def get_object_list(self, request):

        try:
            evenement = Evenement.objects.get(pk=int(request.GET.get('evenement')))
        except Evenement.DoesNotExist:
            return []
        except TypeError:
            return []

        threads = MessageThread.objects.filter(evenement=evenement)

        newer_than = request.GET.get('newer-than')
        if newer_than:
            try:
                newer_than = int(newer_than)
            except ValueError:
                pass
            else:
                threads = threads.filter(id__gt=newer_than)

        return [Message(thread) for thread in threads]

    def obj_get_list(self, bundle, **kwargs):

        return self.get_object_list(bundle.request, **kwargs)

    def get_thread(self, **kwargs):

        try:
            return get_object_or_404(MessageThread, pk=int(kwargs['pk']))
        except ValueError:
            raise Http404

    def obj_get(self, bundle, **kwargs):

        return Message(self.get_thread(**kwargs))

    def obj_create(self, bundle, **kwargs):

        try:
            evenement = bundle.data['evenement']
            sender = bundle.data['sender']
            receiver = bundle.data['receiver']
            body = bundle.data['body']
        except KeyError:
            raise ImmediateHttpResponse(response=HttpBadRequest())

        evenement = get_object_or_404(Evenement, slug=evenement)

        sender = Indicatif.objects.get_or_create(nom=sender, evenement=evenement)[0]
        receiver = Indicatif.objects.get_or_create(nom=receiver, evenement=evenement)[0]

        thread = MessageThread(evenement=evenement)
        thread.save()

        user = bundle.request.user
        version = MessageVersion(thread=thread, expediteur=sender, destinataire=receiver, operateur=user, corps=body)
        version.save()

        bundle.obj = Message(thread)

        return bundle

    def obj_update(self, bundle, **kwargs):
        thread = self.get_thread(**kwargs)

        body, sender, receiver = (bundle.data.get(name) for name in ['body', 'sender', 'receiver'])
        if body and body != thread.corps and not thread.deleted:
            user = bundle.request.user
            version = MessageVersion(thread=thread, operateur=user, corps=body, expediteur=sender, destinataire=receiver)
            version.save()

        bundle.obj = Message(thread)

        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        pass

    def obj_delete(self, bundle, **kwargs):

        thread = self.get_thread(**kwargs)

        try:
            reason = bundle.request.GET['reason']
        except KeyError:
            raise ImmediateHttpResponse(response=HttpBadRequest())

        if not thread.deleted:
            thread.suppression = reason
            thread.save()

    def rollbacks(self, bundles):
        pass
