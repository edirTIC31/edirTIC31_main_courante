from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, Http404

from braces.views import LoginRequiredMixin

from .models import *
from .forms import *


class MainView(LoginRequiredMixin, CreateView):
    model = MessageThread
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

    #if open_evenements.count() == 1:
    #    return redirect(reverse('add-message', args=[open_evenements.first().slug]))

    closed_evenements = Evenement.objects.filter(clos=True)

    return render(request, 'maincourante/evenement_list.html', {
        'open_evenements': open_evenements,
        'closed_evenements': closed_evenements,
    })

@login_required
def evenement_add(request):

    form = EvenementForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        evenement = form.save()
        return redirect(reverse('add-message', args=[evenement.slug]))

    return render(request, 'maincourante/evenement_add.html', {
        'form': form,
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
        return redirect(reverse('report', args=[evenement.slug]))

    return render(request, 'maincourante/evenement_cloture.html', {
        'form': form,
    })

@login_required
def evenement_report(request, evenement):

    return render(request, 'maincourante/evenement_report.html', {
        'messages': MessageThread.objects.filter(evenement=evenement),
    })

@login_required
def evenement_live(request, evenement):

    return render(request, 'maincourante/evenement_live.html', {
        'messages': MessageThread.objects.filter(evenement=evenement).all()[:10],
    })


############
# Messages #
############

@login_required
def message_add(request, evenement, message=None):

    form = MessageForm(request.POST or None)
    edit_form = EditMessageForm()
    delete_form = DeleteMessageForm()

    if request.method == 'POST' and form.is_valid():

        expediteur = form.cleaned_data['expediteur']
        try:
            expediteur = Indicatif.objects.get(nom=expediteur)
        except Indicatif.DoesNotExist:
            expediteur = Indicatif(evenement=evenement, nom=expediteur)
            expediteur.save()
        recipiendaire = form.cleaned_data['recipiendaire']
        try:
            recipiendaire = Indicatif.objects.get(nom=recipiendaire)
        except Indicatif.DoesNotExist:
            recipiendaire = Indicatif(evenement=evenement, nom=recipiendaire)
            recipiendaire.save()

        thread = MessageThread(evenement=evenement,
                expediteur=expediteur,
                recipiendaire=recipiendaire)
        thread.save()
        event = MessageEvent(thread=thread, operateur=request.user,
                corps=form.cleaned_data['corps']).save()

        return redirect(reverse('add-message', args=[evenement.slug]))

    return render(request, 'maincourante/message_add.html', {
        'messages': MessageThread.objects.filter(evenement=evenement)\
                .exclude(events__type=MessageEvent.TYPE.suppression.value)\
                .all()[:10],
        'add_form': form,
        'edit_form': edit_form,
        'delete_form': delete_form,
    })

@login_required
def message_edit(request, evenement, message):

    thread = get_object_or_404(MessageThread, evenement=evenement, id=message)

    if thread.events.first().type == MessageEvent.TYPE.suppression.value:
        raise Http404

    form = EditMessageForm(request.POST)

    if form.is_valid():

        event = MessageEvent(thread=thread, operateur=request.user,
                type=MessageEvent.TYPE.modification.value,
                corps=form.cleaned_data['corps'])
        event.save()

    return redirect(reverse('add-message', args=[evenement.slug]))

@login_required
@require_http_methods(["POST"])
def message_delete(request, evenement, message):

    thread = get_object_or_404(MessageThread, evenement=evenement, id=message)

    if thread.events.first().type == MessageEvent.TYPE.suppression.value:
        raise Http404

    form = DeleteMessageForm(request.POST)

    if form.is_valid():

        event = MessageEvent(thread=thread, operateur=request.user,
                type=MessageEvent.TYPE.suppression.value,
                corps=form.cleaned_data['raison'])
        event.save()

    return redirect(reverse('add-message', args=[evenement.slug]))


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

@login_required
def indicatif_search(request, evenement):

    term = request.GET.get('query')
    if not term:
        raise Http404

    indicatifs = Indicatif.objects.filter(nom__icontains=term)[:10]

    response = []
    for indicatif in indicatifs:
        response += [{
            'value': indicatif.nom,
            'data': indicatif.nom,
        }]

    c = {
        'suggestions': response,
    }

    return JsonResponse(c, safe=False)
