# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0017_empresa_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='codigo_secreto',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
