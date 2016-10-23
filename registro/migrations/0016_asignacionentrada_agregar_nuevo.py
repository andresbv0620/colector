# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0015_colector_respuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignacionentrada',
            name='agregar_nuevo',
            field=models.BooleanField(default=False),
        ),
    ]
