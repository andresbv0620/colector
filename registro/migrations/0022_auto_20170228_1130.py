# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0021_auto_20170218_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignacionentrada',
            name='respuesta_unica',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='nombre',
            field=models.CharField(max_length=3000, blank=True),
        ),
    ]
