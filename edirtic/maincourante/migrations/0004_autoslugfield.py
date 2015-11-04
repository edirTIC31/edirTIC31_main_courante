# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maincourante', '0003_expediteur_destinataire_modifiables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='nom', editable=False, unique=True),
        ),
    ]
