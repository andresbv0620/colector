# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0004_auto_20160324_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='titulo_reporte',
            field=models.ForeignKey(blank=True, to='registro.Entrada', null=True),
        ),
    ]
