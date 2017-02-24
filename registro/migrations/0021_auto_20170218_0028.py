# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0020_auto_20170217_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='nombre',
            field=models.CharField(max_length=2000, blank=True),
        ),
    ]
