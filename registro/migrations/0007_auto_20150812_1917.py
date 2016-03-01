# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0006_auto_20150810_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='almacenamiento',
            field=models.CharField(unique=True, max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='cantidad_colectores',
            field=models.IntegerField(default=0, unique=True, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 19, 17, 31, 12778, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='valor',
            field=models.CharField(unique=True, max_length=50, blank=True),
        ),
    ]
