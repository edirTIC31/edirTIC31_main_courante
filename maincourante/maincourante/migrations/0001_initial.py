# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeStampedModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('cree', models.DateTimeField(auto_now_add=True, verbose_name='créé')),
                ('modifie', models.DateTimeField(auto_now=True, verbose_name='modifié')),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(to='maincourante.TimeStampedModel', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=100)),
                ('clos', models.BooleanField(default=False)),
            ],
            bases=('maincourante.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(to='maincourante.TimeStampedModel', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(1, 'creation'), (2, 'suppression'), (3, 'modification')], default=1)),
                ('expediteur', models.CharField(max_length=100, null=True)),
                ('recipiendaire', models.CharField(max_length=100, null=True)),
                ('corps', models.TextField(null=True)),
                ('suppression', models.CharField(max_length=100, null=True, verbose_name='raison de la suppression')),
                ('operateur', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('evenement', models.ForeignKey(to='maincourante.Evenement')),
                ('parent', models.ForeignKey(to='maincourante.Message', null=True)),
            ],
            bases=('maincourante.timestampedmodel',),
        ),
    ]
