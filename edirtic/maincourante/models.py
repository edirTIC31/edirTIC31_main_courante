from enum import IntEnum
from django.contrib.auth.models import User
from django.db.models import Model, CharField, BooleanField, DateTimeField, \
        ForeignKey, IntegerField, TextField, SlugField


MAX_LENGTH = 100


__all__ = ['Evenement', 'Indicatif', 'Message']


def enum_to_choices(enum):
    return ((item.value, item.name) for item in list(enum))


class TimeStampedModel(Model):
    cree = DateTimeField('créé', auto_now_add=True)
    modifie = DateTimeField('modifié', auto_now=True)


class Evenement(TimeStampedModel):
    nom = CharField(max_length=MAX_LENGTH)
    slug = SlugField(max_length=32, unique=True)
    clos = BooleanField(default=False)

    def __str__(self):
        return '%s%s' % (self.nom, ' (clos)' if self.clos else '')


class Indicatif(Model):
    class Meta:
        ordering = ['nom']

    evenement = ForeignKey(Evenement)
    nom = CharField(max_length=32, unique=True)

    def __str__(self):
        return self.nom


class Message(TimeStampedModel):
    TYPE = IntEnum('type d’opération', 'creation suppression modification')

    evenement = ForeignKey(Evenement)
    type = IntegerField(choices=enum_to_choices(TYPE), default=TYPE.creation.value)
    parent = ForeignKey('self', null=True)
    operateur = ForeignKey(User)
    expediteur = CharField(max_length=MAX_LENGTH, null=True)
    recipiendaire = CharField(max_length=MAX_LENGTH, null=True)
    corps = TextField(null=True)
    suppression = CharField('raison de la suppression', max_length=MAX_LENGTH, null=True)

    def __str__(self):
        return "[%s -> %s] %s" % (self.expediteur, self.recipiendaire, self.corps)
