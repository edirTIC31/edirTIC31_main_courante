from django.contrib.auth.models import User
from django.db.models import PROTECT, BooleanField, CharField, DateTimeField, ForeignKey, Model, TextField
from django.urls import reverse

from autoslug import AutoSlugField

MAX_LENGTH = 100

__all__ = ['User', 'Evenement', 'Indicatif', 'MessageThread', 'MessageVersion', 'MessageSuppression']


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

    evenement = ForeignKey(Evenement, on_delete=PROTECT)
    nom = CharField(max_length=32)
    deleted = BooleanField(default=False)

    def __str__(self):
        return self.nom


class MessageSuppression(TimeStampedModel):

    operateur = ForeignKey(User, on_delete=PROTECT)
    raison = TextField()


class MessageThread(Model):
    class Meta:
        ordering = ['-pk']

    evenement = ForeignKey(Evenement, on_delete=PROTECT)
    suppression = ForeignKey(MessageSuppression, null=True, on_delete=PROTECT)

    @property
    def modified(self):
        return self.versions.count() > 1

    @property
    def deleted(self):
        return self.suppression is not None

    @property
    def last_version(self):
        return self.versions.last()

    @property
    def cree(self):
        return self.versions.first().cree

    @property
    def modifie(self):
        return self.last_version.cree

    @property
    def operateur(self):
        return self.last_version.operateur

    @property
    def expediteur(self):
        return self.last_version.expediteur

    @property
    def destinataire(self):
        return self.last_version.destinataire

    @property
    def corps(self):
        return self.last_version.corps

    def __str__(self):
        return str(self.last_version)


class MessageVersion(TimeStampedModel):
    class Meta:
        ordering = ['pk']

    thread = ForeignKey(MessageThread, related_name='versions', on_delete=PROTECT)
    operateur = ForeignKey(User, on_delete=PROTECT)
    expediteur = ForeignKey(Indicatif, related_name='+', on_delete=PROTECT)
    destinataire = ForeignKey(Indicatif, related_name='+', on_delete=PROTECT)
    corps = TextField()

    def __str__(self):
        return "[%s → %s] %s" % (self.expediteur, self.destinataire, self.corps)
