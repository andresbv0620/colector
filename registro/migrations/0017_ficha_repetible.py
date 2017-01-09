# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0016_asignacionentrada_agregar_nuevo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ficha',
            name='repetible',
            field=models.BooleanField(default=False),
        ),
    ]
