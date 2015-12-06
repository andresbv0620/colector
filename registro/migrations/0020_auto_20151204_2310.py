# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0019_auto_20150824_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='form_asociado',
            field=models.ForeignKey(blank=True, to='registro.Formulario', null=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', b'TEXTO'), (b'2', b'PARRAFO'), (b'3', b'OPCION'), (b'4', b'UNICA'), (b'5', b'MULTIPLE'), (b'6', b'FOTO'), (b'7', b'FECHA'), (b'8', b'NUMERO'), (b'9', b'SCAN'), (b'10', b'DINAMICA'), (b'11', b'GPS')]),
        ),
    ]
