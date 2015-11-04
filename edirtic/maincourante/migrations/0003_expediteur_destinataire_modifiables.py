# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0002_indicatif_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evenement',
            options={'ordering': ['clos', 'cree']},
        ),
        migrations.AlterModelOptions(
            name='messageevent',
            options={'ordering': ['pk']},
        ),
        migrations.RemoveField(
            model_name='messageevent',
            name='type',
        ),
        migrations.RemoveField(
            model_name='messagethread',
            name='expediteur',
        ),
        migrations.RemoveField(
            model_name='messagethread',
            name='recipiendaire',
        ),
        migrations.AddField(
            model_name='messageevent',
            name='destinataire',
            field=models.ForeignKey(related_name='+', to='maincourante.Indicatif', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messageevent',
            name='expediteur',
            field=models.ForeignKey(related_name='+', to='maincourante.Indicatif', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messagethread',
            name='suppression',
            field=models.CharField(null=True, max_length=250),
        ),
    ]
