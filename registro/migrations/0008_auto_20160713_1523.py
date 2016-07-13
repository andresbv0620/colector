# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0007_auto_20160713_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha',
            name='nombre',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='nombre',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
