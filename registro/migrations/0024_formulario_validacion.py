# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0023_respuesta_ingresada'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='validacion',
            field=models.TextField(default=b''),
        ),
    ]
