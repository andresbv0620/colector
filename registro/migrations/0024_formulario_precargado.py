# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0023_auto_20160211_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='precargado',
            field=models.CharField(default=b'NO', max_length=2, choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
        ),
    ]
