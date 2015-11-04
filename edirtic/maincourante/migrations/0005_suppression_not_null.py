# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0004_autoslugfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagethread',
            name='suppression',
            field=models.CharField(default='', max_length=250),
        ),
    ]
