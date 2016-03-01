# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0020_auto_20160218_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacionentrada',
            name='maximo',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='asignacionentrada',
            name='minimo',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
