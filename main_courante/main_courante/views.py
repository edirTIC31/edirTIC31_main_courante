from django.views.generic import CreateView
from braces.views import LoginRequiredMixin
from .models import Message, Evenement


class MainView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('expediteur', 'recipiendaire', 'corps')
    success_url = '/'

    def form_valid(self, form):
        form.instance.operateur = self.request.user
        form.instance.evenement = Evenement.objects.get(clos=False)
        return super().form_valid(form)
