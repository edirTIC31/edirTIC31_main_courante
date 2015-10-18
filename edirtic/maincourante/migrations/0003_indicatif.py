# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0002_evenement_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicatif',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nom', models.CharField(unique=True, max_length=32)),
                ('evenement', models.ForeignKey(to='maincourante.Evenement')),
            ],
        ),
    ]
