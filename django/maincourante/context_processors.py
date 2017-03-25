def evenement(request):
    c = {}
    if hasattr(request, 'evenement'):
        c.update({
            'evenement': request.evenement,
        })
    return c
