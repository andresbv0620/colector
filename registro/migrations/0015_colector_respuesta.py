# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0014_auto_20160913_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='colector',
            name='respuesta',
            field=models.ManyToManyField(to='registro.Respuesta', blank=True),
        ),
    ]
