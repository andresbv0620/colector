# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0021_auto_20160207_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='defecto',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='maximo',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='minimo',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='requerido',
            field=models.CharField(default=b'SI', max_length=2, choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
        ),
    ]
