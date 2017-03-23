from accounts.utils import is_operator


def evenement(request):

    c = {}

    if hasattr(request, 'evenement'):
        c.update({
            'evenement': request.evenement,
        })

    return c

def user_is_operator(request):

    c = {}

    if request.user.is_authenticated():
        c.update({
            'user_is_operator': is_operator(request.user),
        })

    return c
