# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0002_auto_20160302_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='valor',
            field=models.CharField(unique=True, max_length=500, blank=True),
        ),
    ]
