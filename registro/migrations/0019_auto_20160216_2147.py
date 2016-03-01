# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0018_empresa_codigo_secreto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respuesta',
            old_name='nombre',
            new_name='valor',
        ),
        migrations.AddField(
            model_name='entrada',
            name='defecto',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='form_asociado',
            field=models.ForeignKey(blank=True, to='registro.Formulario', null=True),
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
        migrations.AddField(
            model_name='entrada',
            name='validacion',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='formulario',
            name='precargado',
            field=models.CharField(default=b'NO', max_length=2, choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', b'TEXTO'), (b'2', b'PARRAFO'), (b'3', b'OPCION'), (b'4', b'UNICA'), (b'5', b'MULTIPLE'), (b'6', b'FOTO'), (b'7', b'FECHA'), (b'8', b'NUMERO'), (b'9', b'SCAN'), (b'10', b'DINAMICA UNICA'), (b'11', b'DINAMICA MULTIPLE'), (b'12', b'GPS'), (b'13', b'FORMULA'), (b'14', b'FIRMA'), (b'15', b'DECIMAL')]),
        ),
    ]
