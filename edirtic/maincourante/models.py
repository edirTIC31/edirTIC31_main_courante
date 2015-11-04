from enum import IntEnum
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Model, CharField, BooleanField, DateTimeField, \
        ForeignKey, IntegerField, TextField, SlugField


MAX_LENGTH = 100


__all__ = ['User', 'Evenement', 'Indicatif', 'MessageThread', 'MessageEvent']


def enum_to_choices(enum):
    return ((item.value, item.name) for item in list(enum))


class TimeStampedModel(Model):
    cree = DateTimeField('créé', auto_now_add=True, editable=False)
    modifie = DateTimeField('modifié', auto_now=True, editable=False)


class Evenement(TimeStampedModel):
    class Meta:
        ordering = ['clos', 'cree']

    nom = CharField(max_length=MAX_LENGTH)
    slug = SlugField(max_length=32, unique=True)
    clos = BooleanField(default=False)

    def __str__(self):
        return '%s%s' % (self.nom, ' (clos)' if self.clos else '')

    def get_absolute_url(self):
        return reverse('add-message', args=[self.slug])


class Indicatif(Model):
    class Meta:
        ordering = ['nom']
        unique_together = ['evenement', 'nom']

    evenement = ForeignKey(Evenement)
    nom = CharField(max_length=32)
    deleted = BooleanField(default=False)

    def __str__(self):
        return self.nom


class MessageThread(Model):

    class Meta:
        ordering = ['-pk']

    evenement = ForeignKey(Evenement)
    expediteur = ForeignKey(Indicatif, related_name='+')
    recipiendaire = ForeignKey(Indicatif, related_name='+')

    @property
    def modified(self):
        return self.events.filter(type=MessageEvent.TYPE.modification.value).exists()

    @property
    def deleted(self):
        return self.events.filter(type=MessageEvent.TYPE.suppression.value).exists()

    def get_last_version(self):
        return self.events.filter(type__in=[MessageEvent.TYPE.modification.value, MessageEvent.TYPE.creation.value).first()

    def __str__(self):
        return "[%s -> %s] %s" % (self.expediteur, self.recipiendaire, self.events.first().__str__())

class MessageEvent(TimeStampedModel):

    TYPE = IntEnum('type d’évènement', 'creation suppression modification')

    class Meta:
        ordering = ['-pk']

    thread = ForeignKey(MessageThread, related_name='events')
    type = IntegerField(choices=enum_to_choices(TYPE), default=TYPE.creation.value)
    operateur = ForeignKey(User)
    corps = TextField()

    def __str__(self):
        return "%s" % self.corps
