# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0003_indicatif'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicatif',
            options={'ordering': ['nom']},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(null=True, related_name='enfants', to='maincourante.Message'),
        ),
    ]
