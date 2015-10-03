from enum import IntEnum
from django.contrib.auth.models import User
from django.db.models import Model, CharField, BooleanField, DateTimeField, ForeignKey, IntegerField, TextField


MAX_LENGTH = 100


def enum_to_choices(enum):
    return ((item.value, item.name) for item in list(enum))


class TimeStampedModel(Model):
    cree = DateTimeField('créé', auto_now_add=True)
    modifie = DateTimeField('modifié', auto_now=True)


class Evenement(TimeStampedModel):
    nom = CharField(max_length=MAX_LENGTH)
    clos = BooleanField(default=False)

    def __str__(self):
        return '%s%s' % (self.nom, ' (clos)' if self.clos else '')


class Message(TimeStampedModel):
    TYPE = IntEnum('type d’opération', 'creation suppression modification')

    operation = ForeignKey(Evenement)
    type = IntegerField(choices=enum_to_choices(TYPE), default=TYPE.creation)
    parent = ForeignKey('self')
    operateur = ForeignKey(User)
    expediteur = CharField(max_length=MAX_LENGTH, null=True)
    recipiendaire = CharField(max_length=MAX_LENGTH, null=True)
    corps = TextField(null=True)
    suppression = CharField('raison de la suppression', max_length=MAX_LENGTH, null=True)
