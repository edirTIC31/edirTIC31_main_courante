from tastypie.resources import ModelResource
from .models import Message


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        allowed_methods = ['get', 'post']

    def hydrate(self, bundle):
        bundle.obj.operateur = bundle.request.user
        return bundle
