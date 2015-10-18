from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin

from .models import *
from .forms import *


class MainView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('expediteur', 'recipiendaire', 'corps')
    success_url = '/'

    def form_valid(self, form):
        form.instance.operateur = self.request.user
        form.instance.evenement = Evenement.objects.get(clos=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Evenement.objects.get(clos=False).message_set.all()
        return super().get_context_data(**kwargs)


##############
# Evenements #
##############

@login_required
def evenement_list(request):

    open_evenements = Evenement.objects.filter(clos=False)

    if open_evenements.count() == 1:
        return redirect(reverse('add-message', args=[open_evenements.first().slug]))

    closed_evenements = Evenement.objects.filter(clos=True)

    return render(request, 'maincourante/evenement_list.html', {
        'open_evenements': open_evenements,
        'closed_evenements': closed_evenements,
    })

@login_required
def evenement_manage(request, evenement):

    if evenement.clos:
        raise PermissionDenied

    return redirect(reverse('cloture-evenement', args=[evenement.slug]))

@login_required
def evenement_cloture(request, evenement):

    if evenement.clos:
        raise PermissionDenied

    form = ClotureForm(evenement, request.POST or None)

    if request.method == 'POST' and form.is_valid():
        evenement.clos = True
        evenement.save()
        return redirect(reverse('list-messages', args=[evenement.slug]))

    return render(request, 'maincourante/evenement_cloture.html', {
        'form': form,
    })

############
# Messages #
############

@login_required
def message_list(request, evenement):

    return render(request, 'maincourante/message_list.html', {
        'messages': Message.objects.filter(evenement=evenement),
    })

##############
# Indicatifs #
##############

@login_required
def indicatif_list(request, evenement):

    if evenement.clos:
        raise PermissionDenied

    form = IndicatifForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        indicatif = form.save(commit=False)
        indicatif.evenement = evenement
        indicatif.save()
        return redirect(reverse('list-indicatifs', args=[evenement.slug]))

    return render(request, 'maincourante/indicatif_list.html', {
        'indicatifs': Indicatif.objects.filter(evenement=evenement),
        'form': form,
    })
