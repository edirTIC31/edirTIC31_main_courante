# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicatif',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
