from tastypie.resources import ModelResource
from .models import Message


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        allowed_methods = ['get']

