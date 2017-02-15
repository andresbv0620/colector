# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registro', '0017_ficha_repetible'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='pregunta_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='respuesta',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
