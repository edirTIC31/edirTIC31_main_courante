# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='slug',
            field=models.SlugField(default='marathon-2015', unique=True, max_length=32),
            preserve_default=False,
        ),
    ]
