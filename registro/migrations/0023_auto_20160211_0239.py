# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0022_auto_20160210_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='precargado',
            field=models.CharField(default=b'NO', max_length=2, choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
        ),
        migrations.AddField(
            model_name='entrada',
            name='validacion',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
