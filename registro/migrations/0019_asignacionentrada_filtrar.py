# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0018_auto_20170215_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignacionentrada',
            name='filtrar',
            field=models.BooleanField(default=False),
        ),
    ]
