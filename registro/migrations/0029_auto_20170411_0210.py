# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0028_auto_20170406_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha',
            name='nombre',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
