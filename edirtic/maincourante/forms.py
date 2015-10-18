from django.forms.models import modelform_factory

from .models import Indicatif


__all__ = ['IndicatifForm']


IndicatifForm = modelform_factory(Indicatif, fields=['nom'])
