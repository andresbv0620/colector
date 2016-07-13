# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0006_auto_20160706_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='nombre',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
