# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0008_auto_20150812_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='descripcion',
            field=models.TextField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='descripcion',
            field=models.TextField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='direccion',
            field=models.TextField(max_length=50, blank=True),
        ),
    ]
