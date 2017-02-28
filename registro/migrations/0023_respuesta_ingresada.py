# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0022_auto_20170228_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='ingresada',
            field=models.BooleanField(default=False),
        ),
    ]
