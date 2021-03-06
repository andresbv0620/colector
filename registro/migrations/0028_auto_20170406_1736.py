# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0027_auto_20170331_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='ficha',
            name='grupo',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', b'TEXTO'), (b'2', b'PARRAFO'), (b'3', b'OPCION'), (b'4', b'UNICA'), (b'5', b'MULTIPLE'), (b'6', b'FOTO'), (b'7', b'FECHA'), (b'8', b'NUMERO'), (b'9', b'SCAN'), (b'10', b'DINAMICA UNICA'), (b'11', b'DINAMICA MULTIPLE'), (b'12', b'GPS'), (b'13', b'FORMULA'), (b'14', b'FIRMA'), (b'15', b'DECIMAL'), (b'16', b'DOCUMENTO'), (b'17', b'TIEMPO'), (b'18', b'LABEL'), (b'19', b'CHECKBOX'), (b'20', b'GRUPO BOTONES')]),
        ),
    ]
