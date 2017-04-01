# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0026_auto_20170310_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='ficha',
            name='tipo',
            field=models.CharField(default=b'normal', max_length=50, choices=[(b'normal', b'normal'), (b'agrupada', b'agrupada'), (b'parrafo', b'parrafo')]),
        ),
        migrations.AlterField(
            model_name='ficha',
            name='descripcion',
            field=models.TextField(max_length=500, blank=True),
        ),
    ]
