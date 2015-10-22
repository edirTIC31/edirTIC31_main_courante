from django import forms
from django.forms.models import modelform_factory

from .models import MAX_LENGTH, Evenement, Indicatif


__all__ = ['EvenementForm', 'IndicatifForm', 'ClotureForm', \
        'MessageForm', 'EditMessageForm', 'DeleteMessageForm']


EvenementForm = modelform_factory(Evenement, fields=['nom', 'slug'])
IndicatifForm = modelform_factory(Indicatif, fields=['nom'])


class MessageForm(forms.Form):
    
    recipiendaire = forms.CharField(max_length=MAX_LENGTH)
    expediteur = forms.CharField(max_length=MAX_LENGTH)
    corps = forms.CharField(max_length=256)

class EditMessageForm(forms.Form):

    corps = forms.CharField(max_length=256,
            label="Message")

class DeleteMessageForm(forms.Form):

    raison = forms.CharField(max_length=256,
            label="Veuillez indiquer la raison de cette suppression")

class ClotureForm(forms.Form):

    def __init__(self, evenement, *args, **kwargs):
        super(ClotureForm, self).__init__(*args, **kwargs)
        self.evenement = evenement

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if nom != self.evenement.nom:
            raise forms.ValidationError("Vous n’avez pas rentré le nom de l’évènement correctement.")

    nom = forms.CharField(max_length=MAX_LENGTH)
