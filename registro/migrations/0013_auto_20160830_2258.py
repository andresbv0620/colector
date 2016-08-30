# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0012_auto_20160820_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='nombre',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
