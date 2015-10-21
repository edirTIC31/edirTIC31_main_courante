# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicatif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nom', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('expediteur', models.ForeignKey(to='maincourante.Indicatif', related_name='+')),
                ('recipiendaire', models.ForeignKey(to='maincourante.Indicatif', related_name='+')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='TimeStampedModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cree', models.DateTimeField(verbose_name='créé', auto_now_add=True)),
                ('modifie', models.DateTimeField(verbose_name='modifié', auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, to='maincourante.TimeStampedModel', serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=32, unique=True)),
                ('clos', models.BooleanField(default=False)),
            ],
            bases=('maincourante.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='MessageEvent',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, to='maincourante.TimeStampedModel', serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'creation'), (2, 'suppression'), (3, 'modification')], default=1)),
                ('corps', models.TextField()),
                ('operateur', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=('maincourante.timestampedmodel',),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='evenement',
            field=models.ForeignKey(to='maincourante.Evenement'),
        ),
        migrations.AddField(
            model_name='messageevent',
            name='thread',
            field=models.ForeignKey(to='maincourante.MessageThread', related_name='events'),
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
