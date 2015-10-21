from enum import IntEnum
from django.contrib.auth.models import User
from django.db.models import Model, CharField, BooleanField, DateTimeField, \
        ForeignKey, IntegerField, TextField, SlugField


MAX_LENGTH = 100


__all__ = ['Evenement', 'Indicatif', 'MessageThread', 'MessageEvent']


def enum_to_choices(enum):
    return ((item.value, item.name) for item in list(enum))


class TimeStampedModel(Model):
    cree = DateTimeField('créé', auto_now_add=True, editable=False)
    modifie = DateTimeField('modifié', auto_now=True, editable=False)


class Evenement(TimeStampedModel):
    nom = CharField(max_length=MAX_LENGTH)
    slug = SlugField(max_length=32, unique=True)
    clos = BooleanField(default=False)

    def __str__(self):
        return '%s%s' % (self.nom, ' (clos)' if self.clos else '')


class Indicatif(Model):
    class Meta:
        ordering = ['nom']
        unique_together = ['evenement', 'nom']

    evenement = ForeignKey(Evenement)
    nom = CharField(max_length=32)

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
        return self.events.first().type == MessageEvent.TYPE.suppression.value

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
