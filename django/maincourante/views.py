from braces.views import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView

from .forms import ClotureForm, DeleteMessageForm, EditMessageForm, IndicatifForm, MessageForm
from .models import Evenement, Indicatif, MessageThread, MessageVersion, MessageSuppression


##############
# Evenements #
##############


class EvenementListView(LoginRequiredMixin, ListView):
    model = Evenement


class EvenementCreateView(LoginRequiredMixin, CreateView):
    model = Evenement
    fields = ['nom']


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
        'msgs': MessageThread.objects.filter(evenement=evenement),
    })


@login_required
def evenement_live(request, evenement):

    messages = MessageThread.objects.filter(evenement=evenement).all()[:10]
    return render(request, 'maincourante/evenement_live.html', {
        'msgs': messages,
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

        expediteur, destinataire = (Indicatif.objects.get_or_create(evenement=evenement, nom=form.cleaned_data[nom])[0]
                for nom in ['expediteur', 'destinataire'])
        thread = MessageThread(evenement=evenement)
        thread.save()
        MessageVersion(thread=thread, operateur=request.user, expediteur=expediteur, destinataire=destinataire,
                corps=form.cleaned_data['corps']).save()

        reponse = form.cleaned_data['reponse']
        if reponse:
            thread = MessageThread(evenement=evenement)
            thread.save()
            MessageVersion(thread=thread, operateur=request.user, expediteur=destinataire, destinataire=expediteur,
                    corps=reponse).save()

        return redirect(reverse('add-message', args=[evenement.slug]))

    return render(request, 'maincourante/message_add.html', {
        'msgs': MessageThread.objects.filter(evenement=evenement).all()[:10],
        'add_form': form,
        'edit_form': edit_form,
        'delete_form': delete_form,
    })


@login_required
def message_edit(request, evenement, message):

    thread = get_object_or_404(MessageThread, evenement=evenement, id=message)

    if thread.deleted:
        raise Http404

    form = EditMessageForm(request.POST)

    if form.is_valid():

        # TODO: modifier aussi l’expéditeur et le destinataire
        event = MessageVersion(thread=thread, operateur=request.user,
                expediteur=thread.expediteur, destinataire=thread.destinataire,
                corps=form.cleaned_data['corps'])
        event.save()

    return redirect(reverse('add-message', args=[evenement.slug]))


@login_required
@require_http_methods(["POST"])
def message_delete(request, evenement, message):

    thread = get_object_or_404(MessageThread, evenement=evenement, id=message)

    if thread.deleted:
        raise Http404

    form = DeleteMessageForm(request.POST)

    if form.is_valid():

        suppression = MessageSuppression(operateur=request.user,
                raison=form.cleaned_data['raison'])
        suppression.save()
        thread.suppression = suppression
        thread.save()

    return redirect(reverse('add-message', args=[evenement.slug]))


@login_required
def message_last(request, evenement):

    deleted = request.GET.get('deleted')
    if deleted:
        deleted = deleted == '1'
    else:
        deleted = True

    history = request.GET.get('history')
    if history:
        history = history == '1'
    else:
        history = True

    tools = request.GET.get('tools')
    if tools:
        tools = tools == '1'
    else:
        tools = False

    messages = MessageThread.objects.filter(evenement=evenement).all()[:10]

    c = {
        'evenement': evenement,
        'messages': messages,
        'show_deleted': deleted,
        'show_history': history,
        'show_tools': tools,
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
