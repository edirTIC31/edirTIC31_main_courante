from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import BooleanField, CharField, DateTimeField, ForeignKey, Model, SlugField, TextField

from autoslug import AutoSlugField

MAX_LENGTH = 100

__all__ = ['User', 'Evenement', 'Indicatif', 'MessageThread', 'MessageEvent']


class TimeStampedModel(Model):
    cree = DateTimeField('créé', auto_now_add=True, editable=False)
    modifie = DateTimeField('modifié', auto_now=True, editable=False)


class Evenement(TimeStampedModel):
    class Meta:
        ordering = ['clos', 'cree']

    nom = CharField(max_length=MAX_LENGTH)
    slug = AutoSlugField(populate_from='nom', unique=True)
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
    suppression = CharField(max_length=250, null=True)

    @property
    def modified(self):
        return self.events.count() > 1

    @property
    def deleted(self):
        return self.suppression is not None

    def __str__(self):
        return "%s" % self.events.last()


class MessageEvent(TimeStampedModel):

    class Meta:
        ordering = ['pk']

    thread = ForeignKey(MessageThread, related_name='events')
    operateur = ForeignKey(User)
    expediteur = ForeignKey(Indicatif, related_name='+')
    destinataire = ForeignKey(Indicatif, related_name='+')
    corps = TextField()

    def __str__(self):
        return "[%s -> %s] %s" % (self.expediteur, self.destinataire, self.corps)
