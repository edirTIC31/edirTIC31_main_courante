from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView

from .forms import ClotureForm, DeleteMessageForm, EditMessageForm, IndicatifForm, MessageForm
from .models import Evenement, Indicatif, MessageEvent, MessageThread


##############
# Evenements #
##############


class EvenementListView(LoginRequiredMixin, ListView):
    model = Evenement


class EvenementCreateView(LoginRequiredMixin, CreateView):
    model = Evenement
    fields = ['nom', 'slug']


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

    messages = MessageThread.objects.filter(evenement=evenement)\
            .exclude(events__type=MessageEvent.TYPE.suppression.value).all()[:10]
    return render(request, 'maincourante/evenement_live.html', {
        'messages': messages,
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
            expediteur = Indicatif.objects.get(evenement=evenement, nom=expediteur)
        except Indicatif.DoesNotExist:
            expediteur = Indicatif(evenement=evenement, nom=expediteur)
            expediteur.save()
        recipiendaire = form.cleaned_data['recipiendaire']
        try:
            recipiendaire = Indicatif.objects.get(evenement=evenement, nom=recipiendaire)
        except Indicatif.DoesNotExist:
            recipiendaire = Indicatif(evenement=evenement, nom=recipiendaire)
            recipiendaire.save()

        thread = MessageThread(evenement=evenement,
                expediteur=expediteur,
                recipiendaire=recipiendaire)
        thread.save()
        MessageEvent(thread=thread, operateur=request.user,
                corps=form.cleaned_data['corps']).save()

        reponse = form.cleaned_data['reponse']
        if reponse:
            thread = MessageThread(evenement=evenement,
                    expediteur=recipiendaire,
                    recipiendaire=expediteur)
            thread.save()
            MessageEvent(thread=thread, operateur=request.user,
                    corps=reponse).save()

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


@login_required
def message_last(request, evenement):

    deleted = request.GET.get('deleted')
    if deleted:
        deleted = deleted == '1'
    else:
        deleted = True

    tools = request.GET.get('tools')
    if tools:
        tools = tools == '1'
    else:
        tools = False

    messages = MessageThread.objects.filter(evenement=evenement)
    if not deleted:
        messages = messages.exclude(events__type=MessageEvent.TYPE.suppression.value)
    messages = messages.all()[:10]

    c = {
        'evenement': evenement,
        'messages': messages,
        'deleted': deleted,
        'tools': tools,
    }

    return render_to_response('maincourante/tags/messages.html', context=c)


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
def indicatif_delete(request, evenement, indicatif):

    if evenement.clos:
        raise PermissionDenied

    indicatif = get_object_or_404(Indicatif, pk=indicatif, deleted=False)

    indicatif.deleted = True
    indicatif.save()

    return redirect(reverse('list-indicatifs', args=[evenement.slug]))


@login_required
def indicatif_search(request, evenement):

    term = request.GET.get('query')
    if not term:
        raise Http404

    indicatifs = Indicatif.objects.filter(evenement=evenement, deleted=False, nom__istartswith=term)[:10]

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


###########
# Angular #
###########


@login_required
def message_angular(request, evenement):

    return render(request, 'maincourante/message_angular.html')
