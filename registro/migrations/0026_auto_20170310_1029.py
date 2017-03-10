# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0025_auto_20170310_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulario',
            name='validacion',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
