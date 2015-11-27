#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

def evenement(request):

    c = {}

    if hasattr(request, 'evenement'):
        c.update({
            'evenement': request.evenement,
        })

    return c
