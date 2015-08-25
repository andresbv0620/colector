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
    ]
