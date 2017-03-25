from django.conf import settings
from django.core.urlresolvers import reverse

from accounts.utils import is_operator
from accounts.models import AuthToken


def user_is_operator(request):
    c = {}
    if request.user.is_authenticated():
        c.update({
            'user_is_operator': is_operator(request.user),
        })
    return c


def share_url(request):
    c = {}
    if request.user.is_authenticated():
        token = AuthToken.objects.get(user__username=settings.RO_USERNAME)
        share_url = 'https' if request.is_secure() else 'http'
        share_url += '://'
        share_url += request.META['HTTP_HOST']
        share_url += reverse('login-token', kwargs={'token': token.token})
        if hasattr(request, 'evenement'):
            share_url += '?next=' + reverse('live', kwargs={'evenement': request.evenement.slug})
        c.update({
            'share_url': share_url,
        })
    return c
