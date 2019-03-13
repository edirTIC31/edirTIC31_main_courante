from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

from maincourante.models import Evenement


class EvenementMiddleware(MiddlewareMixin):
    def process_view(self, request, view, view_args, view_kwargs):

        if view.__module__ != 'maincourante.views':
            return

        evenement = view_kwargs.get('evenement')
        if not evenement:
            return

        evenement = get_object_or_404(Evenement, slug=evenement)
        view_kwargs['evenement'] = evenement
        request.evenement = evenement
