# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicatif',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('suppression', models.CharField(max_length=250, default='')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='TimeStampedModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('cree', models.DateTimeField(auto_now_add=True, verbose_name='créé')),
                ('modifie', models.DateTimeField(auto_now=True, verbose_name='modifié')),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(primary_key=True, to='maincourante.TimeStampedModel', auto_created=True, parent_link=True, serialize=False)),
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
            name='MessageVersion',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(primary_key=True, to='maincourante.TimeStampedModel', auto_created=True, parent_link=True, serialize=False)),
                ('corps', models.TextField()),
                ('destinataire', models.ForeignKey(related_name='+', to='maincourante.Indicatif')),
                ('expediteur', models.ForeignKey(related_name='+', to='maincourante.Indicatif')),
                ('operateur', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(related_name='versions', to='maincourante.MessageThread')),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=('maincourante.timestampedmodel',),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='evenement',
            field=models.ForeignKey(to='maincourante.Evenement'),
        ),
        migrations.AddField(
            model_name='indicatif',
            name='evenement',
            field=models.ForeignKey(to='maincourante.Evenement'),
        ),
        migrations.AlterUniqueTogether(
            name='indicatif',
            unique_together=set([('evenement', 'nom')]),
        ),
    ]
