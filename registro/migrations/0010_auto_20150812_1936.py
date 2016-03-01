# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0009_auto_20150812_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='Formulario_diligenciado',
        ),
        migrations.AddField(
            model_name='entrada',
            name='descripcion',
            field=models.TextField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='ficha',
            name='descripcion',
            field=models.TextField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='formulario_diligenciado',
            name='colector',
            field=models.ForeignKey(blank=True, to='registro.Colector', null=True),
        ),
        migrations.AddField(
            model_name='formulario_diligenciado',
            name='empresa',
            field=models.ForeignKey(blank=True, to='registro.Empresa', null=True),
        ),
        migrations.AddField(
            model_name='formulario_diligenciado',
            name='entrada',
            field=models.ForeignKey(blank=True, to='registro.Entrada', null=True),
        ),
        migrations.AddField(
            model_name='formulario_diligenciado',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 19, 36, 36, 140782, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formulario_diligenciado',
            name='gps',
            field=models.CharField(unique=True, max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='formulario_diligenciado',
            name='respuesta',
            field=models.ForeignKey(blank=True, to='registro.Respuesta', null=True),
        ),
    ]
