# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0007_auto_20150812_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='ciudad',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='descripcion',
            field=models.TextField(unique=True, max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='direccion',
            field=models.TextField(unique=True, max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='email',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='industria',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='pais',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
