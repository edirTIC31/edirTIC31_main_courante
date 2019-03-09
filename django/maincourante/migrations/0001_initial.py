# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models

import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicatif',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nom', models.CharField(max_length=32)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='TimeStampedModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('cree', models.DateTimeField(auto_now_add=True, verbose_name='créé')),
                ('modifie', models.DateTimeField(verbose_name='modifié', auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(to='maincourante.TimeStampedModel', primary_key=True, auto_created=True, serialize=False, parent_link=True, on_delete=models.PROTECT)),
                ('nom', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, populate_from='nom', editable=False)),
                ('clos', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['clos', 'cree'],
            },
            bases=('maincourante.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='MessageSuppression',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(to='maincourante.TimeStampedModel', primary_key=True, auto_created=True, serialize=False, parent_link=True, on_delete=models.PROTECT)),
                ('raison', models.TextField()),
                ('operateur', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            bases=('maincourante.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='MessageVersion',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(to='maincourante.TimeStampedModel', primary_key=True, auto_created=True, serialize=False, parent_link=True, on_delete=models.PROTECT)),
                ('corps', models.TextField()),
                ('destinataire', models.ForeignKey(to='maincourante.Indicatif', related_name='+', on_delete=models.PROTECT)),
                ('expediteur', models.ForeignKey(to='maincourante.Indicatif', related_name='+', on_delete=models.PROTECT)),
                ('operateur', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
                ('thread', models.ForeignKey(to='maincourante.MessageThread', related_name='versions', on_delete=models.PROTECT)),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=('maincourante.timestampedmodel',),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='evenement',
            field=models.ForeignKey(to='maincourante.Evenement', on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='suppression',
            field=models.ForeignKey(to='maincourante.MessageSuppression', null=True, on_delete=models.PROTECT),
        ),
        migrations.AddField(
            model_name='indicatif',
            name='evenement',
            field=models.ForeignKey(to='maincourante.Evenement', on_delete=models.PROTECT),
        ),
        migrations.AlterUniqueTogether(
            name='indicatif',
            unique_together=set([('evenement', 'nom')]),
        ),
    ]
