# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maincourante', '0005_suppression_not_null'),
    ]

    operations = [
        migrations.RenameModel('MessageEvent', 'MessageVersion'),
        migrations.AlterField(
            model_name='messageversion',
            name='thread',
            field=models.ForeignKey(to='maincourante.MessageThread', related_name='versions'),
        ),
    ]
